"""Run displayed Lean cells with the existing local Lean and Mathlib.

Proof artifacts live in an immutable project cache. Each session owns its cell
artifacts; rerunning a stage archives it and later stages.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid

LEAN_VERSION = "4.34.0"
MATHLIB_COMMIT = "5ed2965256430c3649e86755f9576b54eca72435"
STAGES = ("import", "start", "endpoint")
MODULES = {
    route: {stage: f"Step{suffix}{stage.title()}" for stage in STAGES}
    for route, suffix in (("uw", "UW"), ("qrm", "QRM"))
}
ARTIFACT_SUFFIXES = (".olean", ".olean.private", ".olean.server", ".ilean", ".ir")
CACHE_SCHEMA = 1


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _json_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(",", ":")).encode("utf-8")).hexdigest()


class LeanCellError(RuntimeError):
    """An unmet prerequisite, compiler error, or unsuccessful proof check."""


def _visible_code(source):
    """Mask nested Lean comments and string literals for import discovery."""
    result = list(source)
    index, depth, quoted = 0, 0, False
    while index < len(source):
        if depth:
            if source.startswith("/-", index):
                result[index:index + 2] = "  "
                depth += 1
                index += 2
                continue
            if source.startswith("-/", index):
                result[index:index + 2] = "  "
                depth -= 1
                index += 2
                continue
            if source[index] != "\n":
                result[index] = " "
            index += 1
            continue
        if quoted:
            if source[index] == "\\" and index + 1 < len(source):
                result[index:index + 2] = "  "
                index += 2
                continue
            if source[index] == '"':
                quoted = False
            if source[index] != "\n":
                result[index] = " "
            index += 1
            continue
        if source.startswith("/-", index):
            result[index:index + 2] = "  "
            depth = 1
            index += 2
            continue
        if source.startswith("--", index):
            stop = source.find("\n", index)
            if stop < 0:
                stop = len(source)
            result[index:stop] = " " * (stop - index)
            index = stop
            continue
        if source[index] == '"':
            result[index] = " "
            quoted = True
        index += 1
    return "".join(result)


def _imports(source):
    result = []
    for match in re.finditer(
        r"^\s*(?:(?:public|private)\s+)?(?:meta\s+)?import\s+([^\n]+)",
        _visible_code(source), re.MULTILINE,
    ):
        for module in match.group(1).split():
            if not re.fullmatch(r"[\w\u0080-\uffff]+(?:\.[\w\u0080-\uffff]+)*", module):
                raise LeanCellError(f"Unsupported import spelling: {module}")
            result.append(module)
    return result


def _command(command, *, cwd=None, env=None, timeout=1800):
    """Print actual process output and propagate failure without a success label."""
    result = subprocess.run(
        [str(part) for part in command], cwd=cwd, env=env, timeout=timeout,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n", flush=True)
    if result.stderr:
        print(result.stderr, end="" if result.stderr.endswith("\n") else "\n",
              file=sys.stderr, flush=True)
    if result.returncode:
        raise LeanCellError(f"Command exited with status {result.returncode}: {command[0]}")
    return result


def _resolve_runtime(proofs_dir, runtime_config=None, allow_download=False):
    if allow_download:
        raise RuntimeError("This notebook uses an existing local Lean/Mathlib runtime; automatic downloads are disabled.")
    if isinstance(runtime_config, dict):
        config = dict(runtime_config)
    else:
        candidate = Path(runtime_config) if runtime_config is not None else None
        if candidate is None:
            anchors = [Path(proofs_dir), Path.cwd(), Path(__file__).resolve().parent]
            candidates = []
            for anchor in anchors:
                candidates.extend(parent / "_lean_shared" / "runtime.json"
                                  for parent in (anchor, *anchor.parents))
            candidates.append(Path("C:/Users/msz/aca/_lean_shared/runtime.json"))
            candidate = next((path for path in candidates if path.is_file()), None)
        if candidate is not None and candidate.is_file():
            config = json.loads(candidate.read_text(encoding="utf-8-sig"))
        else:
            raise RuntimeError("Local Lean runtime is missing. Use the local Jupyter kernel and supply _lean_shared/runtime.json.")
    if config.get("toolchain") != f"leanprover/lean4:v{LEAN_VERSION}":
        raise RuntimeError("This notebook requires Lean 4.34.0.")
    if config.get("mathlib_commit") != MATHLIB_COMMIT:
        raise RuntimeError("This notebook requires the pinned Mathlib v4.34.0 commit.")
    if not Path(config["lean_exe"]).is_file():
        raise RuntimeError("Configured Lean executable does not exist.")
    for library in config["lean_paths"]:
        if not Path(library).is_dir():
            raise RuntimeError(f"Configured Lean library is missing: {library}")
    version = subprocess.run([config["lean_exe"], "--version"], capture_output=True,
                             text=True, timeout=30, encoding="utf-8", errors="replace")
    if version.returncode or not re.search(r"\b4\.34\.0\b", version.stdout):
        raise RuntimeError(f"Configured compiler has an unexpected version: {version.stdout}")
    config["compiler_version"] = version.stdout.strip()
    return config


class LeanNotebook:
    def __init__(self, proofs_dir, workdir=None, runtime_config=None, allow_download=False,
                 cache_dir=None, seed_runs=None):
        self.proofs_dir = Path(proofs_dir).resolve(strict=True)
        if not self.proofs_dir.is_dir():
            raise ValueError("proofs_dir must be a directory of exact Lean sources.")
        self.config = _resolve_runtime(self.proofs_dir, runtime_config, allow_download)
        self.runtime_identity = self._runtime_identity()
        self.cache_dir = (Path(cache_dir).resolve() if cache_dir is not None else
                          Path(__file__).resolve().parent / "proof_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        if seed_runs is None:
            project = Path(__file__).resolve().parent
            self.seed_runs = [self.proofs_dir.parent / "runs",
                              project / "report_lean" / "runs",
                              project / "lean_validation_runs"]
        else:
            self.seed_runs = [Path(path).resolve() for path in seed_runs]
        identifier = dt.datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8]
        self.workdir = (Path(workdir).resolve() if workdir is not None else
                        self.proofs_dir.parent / "runs" / identifier)
        self.workdir.mkdir(parents=True, exist_ok=True)
        self.cell_sources = self.workdir / "cells"
        self.cell_lib = self.workdir / "lib" / "lean"
        self.proof_lib = self.workdir / "proof-lib" / "lean"
        for path in (self.cell_sources, self.cell_lib, self.proof_lib):
            path.mkdir(parents=True, exist_ok=True)
        self.success = {route: {} for route in MODULES}
        self.route_sources = {}
        self.cache_events = []
        self.history = []
        self.env = os.environ.copy()
        self.env["LEAN_PATH"] = os.pathsep.join(
            [str(self.cell_lib), str(self.proof_lib)] + self.config["lean_paths"])
        self.env["PATH"] = str(Path(self.config["lean_exe"]).parent) + os.pathsep + self.env.get("PATH", "")

    def _runtime_identity(self):
        """Identify the actual compiler and the existing pinned Mathlib checkout."""
        mathlib = None
        for library in self.config["lean_paths"]:
            candidate = Path(library).resolve()
            if (candidate / "Mathlib.olean").is_file():
                mathlib = candidate.parents[3]
                break
        if mathlib is None or not (mathlib / "lake-manifest.json").is_file():
            raise RuntimeError("The local Mathlib library and lake-manifest.json are required.")
        revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=mathlib,
                                  capture_output=True, text=True, timeout=30)
        if revision.returncode or revision.stdout.strip() != MATHLIB_COMMIT:
            raise RuntimeError("The existing Mathlib checkout is not at the pinned commit.")
        return {"compiler_version": self.config["compiler_version"],
                "compiler_sha256": _sha256(self.config["lean_exe"]),
                "toolchain": self.config["toolchain"], "mathlib_commit": MATHLIB_COMMIT,
                "mathlib_manifest_sha256": _sha256(mathlib / "lake-manifest.json"),
                "lean_paths": [str(Path(path).resolve()) for path in self.config["lean_paths"]]}

    def _save_history(self):
        (self.workdir / "history.json").write_text(
            json.dumps(self.history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (self.workdir / "cache_events.json").write_text(
            json.dumps(self.cache_events, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _artifact_files(self, library, module):
        base = Path(library).joinpath(*module.split("."))
        return [base.with_suffix(suffix) for suffix in ARTIFACT_SUFFIXES
                if base.with_suffix(suffix).is_file()]

    def _archive_proof(self, module):
        for artifact in self._artifact_files(self.proof_lib, module):
            self._archive(artifact)

    def _changed_routes(self):
        changed = set()
        for route, sources in list(self.route_sources.items()):
            if any(not self.proofs_dir.joinpath(*module.split(".")).with_suffix(".lean").is_file()
                   or _sha256(self.proofs_dir.joinpath(*module.split(".")).with_suffix(".lean")) != digest
                   for module, digest in sources.items()):
                self._invalidate(route, "import")
                self.route_sources.pop(route, None)
                changed.add(route)
                for module in sources:
                    self._archive_proof(module)
        return changed

    def _archive(self, source):
        if source.exists():
            target = self.workdir / "archive" / (uuid.uuid4().hex + "_" + source.name)
            target.parent.mkdir(parents=True, exist_ok=True)
            source.replace(target)

    def _invalidate(self, route, stage):
        for later in STAGES[STAGES.index(stage):]:
            self.success[route].pop(later, None)
            module = MODULES[route][later]
            for suffix in (".olean", ".ilean", ".olean.private", ".olean.server"):
                self._archive(self.cell_lib / (module + suffix))
            self._archive(self.cell_sources / (module + ".lean"))

    def _compile(self, source, root, output, timeout=900):
        output.parent.mkdir(parents=True, exist_ok=True)
        for suffix in ARTIFACT_SUFFIXES:
            self._archive(output.with_suffix(suffix))
        started = time.monotonic()
        command = [self.config["lean_exe"], "-R", str(root), "-o", str(output), str(source)]
        item = {"source": str(source), "artifact": str(output), "command": command,
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}
        self.history.append(item)
        try:
            result = subprocess.run(command, cwd=root, env=self.env, capture_output=True,
                                    text=True, encoding="utf-8", errors="replace", timeout=timeout)
            item.update(stdout=result.stdout, stderr=result.stderr, exit_code=result.returncode,
                        seconds=time.monotonic() - started)
            if result.stdout:
                print(result.stdout, end="" if result.stdout.endswith("\n") else "\n", flush=True)
            if result.stderr:
                print(result.stderr, end="" if result.stderr.endswith("\n") else "\n",
                      file=sys.stderr, flush=True)
            if result.returncode or re.search(r"declaration uses ['`]?sorry|\bsorryAx\b", result.stdout + result.stderr):
                raise LeanCellError(f"Lean failed for {source.name} (exit code {result.returncode}).")
            if not output.is_file() or _sha256(source) != item["sha256"]:
                raise LeanCellError(f"Source changed during compilation or no artifact was produced: {source.name}")
            item["artifact_sha256"] = _sha256(output)
            item["artifact_companions"] = {
                artifact.name: _sha256(artifact) for artifact in
                (output.with_suffix(suffix) for suffix in ARTIFACT_SUFFIXES) if artifact.is_file()}
            item["runtime_identity"] = self.runtime_identity
            item["passed"] = True
            return item
        except BaseException as error:
            item.update(passed=False, error=str(error), seconds=time.monotonic() - started)
            for suffix in ARTIFACT_SUFFIXES:
                self._archive(output.with_suffix(suffix))
            raise
        finally:
            self._save_history()

    def _proof_closure(self, code):
        order, active, completed, records = [], set(), set(), {}

        def visit(module):
            source = self.proofs_dir.joinpath(*module.split(".")).with_suffix(".lean")
            if not source.is_file():
                return
            source = source.resolve(strict=True)
            if not source.is_relative_to(self.proofs_dir):
                raise LeanCellError(f"Proof import escapes proofs_dir: {module}")
            if source in completed:
                return
            if source in active:
                raise LeanCellError(f"Cyclic proof imports: {module}")
            active.add(source)
            dependencies = _imports(source.read_text(encoding="utf-8-sig"))
            for dependency in dependencies:
                visit(dependency)
            active.remove(source)
            completed.add(source)
            records[module] = {"module": module, "path": source.relative_to(self.proofs_dir).as_posix(),
                               "sha256": _sha256(source), "imports": dependencies}
            order.append(module)

        for module in _imports(code):
            visit(module)
        return order, records

    def _proof_descriptor(self, module, records):
        local = {}
        external = {}

        def visit(name):
            if name in local or name in external:
                return
            if name in records:
                local[name] = records[name]
                for dependency in records[name]["imports"]:
                    visit(dependency)
            else:
                artifacts = next((self._artifact_files(path, name)
                                  for path in self.config["lean_paths"]
                                  if Path(path).joinpath(*name.split(".")).with_suffix(".olean").is_file()), [])
                if not artifacts:
                    raise LeanCellError(f"Local runtime has no compiled import: {name}")
                external[name] = {artifact.name: _sha256(artifact) for artifact in artifacts}

        visit(module)
        return {"schema": CACHE_SCHEMA, "module": module, "runtime": self.runtime_identity,
                "sources": local, "external_imports": external}

    def _sources_match(self, descriptor):
        return all((self.proofs_dir / record["path"]).is_file() and
                   _sha256(self.proofs_dir / record["path"]) == record["sha256"]
                   for record in descriptor["sources"].values())

    def _ready_entry(self, key, descriptor):
        for manifest_path in sorted((self.cache_dir / key).glob("*/ready.json")):
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                if manifest.get("descriptor") != descriptor or manifest.get("key") != key:
                    continue
                library = manifest_path.parent / "lib" / "lean"
                actual = self._artifact_files(library, descriptor["module"])
                expected = manifest["artifacts"]
                if {artifact.relative_to(library).as_posix(): _sha256(artifact)
                    for artifact in actual} != expected or not any(name.endswith(".olean") for name in expected):
                    continue
                return manifest_path.parent, manifest
            except (OSError, ValueError, KeyError):
                continue
        return None

    def _copy_artifacts(self, library, destination, module):
        copied = {}
        for artifact in self._artifact_files(library, module):
            relative = artifact.relative_to(library)
            target = Path(destination) / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            before = _sha256(artifact)
            shutil.copy2(artifact, target)
            if _sha256(target) != before or _sha256(artifact) != before:
                raise LeanCellError(f"Compiled artifact changed while copying: {artifact}")
            copied[relative.as_posix()] = before
        if not any(name.endswith(".olean") for name in copied):
            raise LeanCellError(f"Missing compiled proof artifact: {module}")
        return copied

    def _try_seed(self, module, descriptor, build):
        """Audit old successful source records and validate their exact artifact copies."""
        histories = []
        for root in self.seed_runs:
            histories.extend(root.glob("*/history.json"))
        for history_path in sorted(set(histories), reverse=True):
            try:
                history = json.loads(history_path.read_text(encoding="utf-8"))
                latest, compiled_indices = {}, {}
                for index, item in enumerate(history):
                    source = Path(item.get("source", ""))
                    artifact_parts = Path(item.get("artifact", "")).parts
                    if source.suffix == ".lean" and "proof-lib" in artifact_parts:
                        relative = Path(*artifact_parts[artifact_parts.index("proof-lib") + 2:]).with_suffix("")
                        name = ".".join(relative.parts)
                        latest[name] = item
                        compiled_indices.setdefault(name, []).append(index)
                candidate = latest.get(module)
                if not candidate:
                    continue
                audited = set()
                def audit_compile_context(name, index):
                    """Use dependency records preceding this compile, recursively."""
                    if (name, index) in audited:
                        return
                    item = history[index]
                    if not item.get("passed") or item.get("exit_code") != 0 or item.get("sha256") != descriptor["sources"][name]["sha256"]:
                        raise ValueError("Historical dependency source does not match at compile time")
                    if Path(item["command"][0]).resolve() != Path(self.config["lean_exe"]).resolve():
                        raise ValueError("Historical dependency compiler does not match")
                    if "runtime_identity" in item and item["runtime_identity"] != self.runtime_identity:
                        raise ValueError("Historical dependency runtime does not match")
                    for dependency in descriptor["sources"][name]["imports"]:
                        if dependency in descriptor["sources"]:
                            preceding = [prior for prior in compiled_indices.get(dependency, []) if prior < index]
                            if not preceding:
                                raise ValueError("Dependency has no preceding successful compilation")
                            audit_compile_context(dependency, preceding[-1])
                    audited.add((name, index))
                audit_compile_context(module, compiled_indices[module][-1])
                def old_artifact(name, item):
                    original = Path(item["artifact"])
                    if original.is_file():
                        return original
                    # Validation runs were preserved by moving their entire directory.
                    return history_path.parent / "proof-lib" / "lean" / Path(*name.split(".")).with_suffix(".olean")
                for dependency, record in descriptor["sources"].items():
                    item = latest[dependency]
                    if not item.get("passed") or item.get("exit_code") != 0 or item.get("sha256") != record["sha256"]:
                        raise ValueError("Old source record does not match")
                    if Path(item["command"][0]).resolve() != Path(self.config["lean_exe"]).resolve():
                        raise ValueError("Old compiler does not match")
                    if "runtime_identity" in item and item["runtime_identity"] != self.runtime_identity:
                        raise ValueError("Old runtime does not match")
                    artifact = old_artifact(dependency, item)
                    if not artifact.is_file() or artifact.stat().st_mtime_ns > history_path.stat().st_mtime_ns:
                        raise ValueError("Old artifact missing or modified after validation")
                    if item.get("artifact_sha256") and _sha256(artifact) != item["artifact_sha256"]:
                        raise ValueError("Old artifact hash does not match")
                    if "artifact_companions" in item:
                        companions = {path.name: _sha256(path) for path in
                                      (artifact.with_suffix(suffix) for suffix in ARTIFACT_SUFFIXES) if path.is_file()}
                        if companions != item["artifact_companions"]:
                            raise ValueError("Old artifact companion hashes do not match")
                artifact = old_artifact(module, candidate)
                module_relative = Path(*module.split(".")).with_suffix(".olean")
                old_library = artifact
                for _ in module_relative.parts:
                    old_library = old_library.parent
                copied = self._copy_artifacts(old_library, build / "lib" / "lean", module)
                probe = build / "SeedCompatibility.lean"
                probe.write_text(f"import {module}\n", encoding="utf-8")
                old_env = self.env
                self.env = dict(old_env)
                self.env["LEAN_PATH"] = str(build / "lib" / "lean") + os.pathsep + old_env["LEAN_PATH"]
                try:
                    check = self._compile(probe, build, build / "check" / "SeedCompatibility.olean")
                    check["purpose"] = "seed artifact import compatibility check"
                finally:
                    self.env = old_env
                return {"method": "validated_previous_run", "history": str(history_path),
                        "history_sha256": _sha256(history_path), "source_record": candidate,
                        "copied_artifact_sha256": copied,
                        "compatibility_check": check}
            except (OSError, ValueError, KeyError, LeanCellError):
                # Incomplete old runs are evidence only; a real build is the fallback.
                continue
        return None

    def _cached_proof(self, module, descriptor):
        key = _json_hash(descriptor)
        self._archive_proof(module)
        found = self._ready_entry(key, descriptor)
        origin = "warm_cache"
        if found is None:
            build = self.cache_dir / key / ("build_" + uuid.uuid4().hex)
            library = build / "lib" / "lean"
            library.mkdir(parents=True, exist_ok=True)
            provenance = self._try_seed(module, descriptor, build)
            if provenance is None:
                source = self.proofs_dir / descriptor["sources"][module]["path"]
                output = library.joinpath(*module.split(".")).with_suffix(".olean")
                compiled = self._compile(source, self.proofs_dir, output)
                provenance = {"method": "compiled_exact_sources", "compilation": compiled}
            if not self._sources_match(descriptor):
                raise LeanCellError("Proof sources changed while building the cache; rerun the import cell.")
            manifest = {"schema": CACHE_SCHEMA, "key": key, "descriptor": descriptor,
                        "artifacts": {path.relative_to(library).as_posix(): _sha256(path)
                                      for path in self._artifact_files(library, module)},
                        "provenance": provenance, "completed_at": dt.datetime.now().isoformat()}
            # An entry is immutable and invisible to other sessions until readiness commits last.
            temporary = build / "ready.pending.json"
            temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            temporary.replace(build / "ready.json")
            found = self._ready_entry(key, descriptor)
            if found is None:
                raise LeanCellError(f"Cache artifact integrity verification failed: {module}")
            origin = provenance["method"]
        entry, manifest = found
        if not self._sources_match(descriptor):
            raise LeanCellError("Proof sources changed during cache reuse; rerun the import cell.")
        hashes = self._copy_artifacts(entry / "lib" / "lean", self.proof_lib, module)
        if hashes != manifest["artifacts"]:
            self._archive_proof(module)
            raise LeanCellError(f"Cached proof artifact hash changed: {module}")
        event = {"module": module, "key": key, "origin": origin, "entry": str(entry),
                 "source_sha256": descriptor["sources"][module]["sha256"], "artifact_sha256": hashes}
        self.cache_events.append(event)
        self._save_history()
        print(f"Lean proof import: {module} ({origin})", flush=True)

    def _compile_closure(self, code):
        order, records = self._proof_closure(code)
        for module in order:
            self._cached_proof(module, self._proof_descriptor(module, records))
        return {module: record["sha256"] for module, record in records.items()}

    def run(self, route, stage, code):
        """Compile exactly the caller's cell text, then make its .olean importable."""
        if route not in MODULES or stage not in STAGES:
            raise ValueError("Use route uw/qrm and stage import/start/endpoint.")
        changed = self._changed_routes()
        if route in changed and stage != "import":
            raise LeanCellError("Proof sources changed; rerun the import cell before this stage.")
        self._invalidate(route, stage)
        index = STAGES.index(stage)
        if index and STAGES[index - 1] not in self.success[route]:
            raise LeanCellError(f"Run '%%lean {route} {STAGES[index - 1]}' successfully first.")
        module = MODULES[route][stage]
        source = self.cell_sources / (module + ".lean")
        source.write_bytes(code.encode("utf-8"))
        if stage == "import":
            sources = self._compile_closure(code)
        item = self._compile(source, self.cell_sources, self.cell_lib / (module + ".olean"))
        self.success[route][stage] = item["sha256"]
        if stage == "import":
            self.route_sources[route] = sources
        return item

    def cell_magic(self, line, cell):
        arguments = line.strip().split()
        if len(arguments) != 2:
            raise ValueError("Usage: %%lean uw import|start|endpoint (or qrm).")
        self.run(arguments[0], arguments[1], cell)


def install_lean_magic(proofs_dir, workdir=None, runtime_config=None, allow_download=False,
                       cache_dir=None, seed_runs=None):
    """Register %%lean in the current IPython shell and return its runtime."""
    from IPython import get_ipython

    shell = get_ipython()
    if shell is None:
        raise RuntimeError("install_lean_magic requires a running IPython notebook kernel.")
    notebook = LeanNotebook(proofs_dir, workdir, runtime_config, allow_download, cache_dir, seed_runs)
    shell.register_magic_function(notebook.cell_magic, magic_kind="cell", magic_name="lean")
    return notebook
