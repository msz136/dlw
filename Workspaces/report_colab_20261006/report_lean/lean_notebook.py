"""Run the displayed Lean notebook cells with pinned Lean and Mathlib.

The work directory owns every compiled proof and cell artifact. Successful
earlier cells remain importable; rerunning a stage archives it and later stages.
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
import tarfile
import time
import urllib.request
import uuid

LEAN_VERSION = "4.34.0"
MATHLIB_COMMIT = "5ed2965256430c3649e86755f9576b54eca72435"
STAGES = ("import", "start", "endpoint")
MODULES = {
    route: {stage: f"Step{suffix}{stage.title()}" for stage in STAGES}
    for route, suffix in (("uw", "UW"), ("qrm", "QRM"))
}


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


def _download_runtime(destination):
    """Install official Linux x86_64 Lean and exact tagged Mathlib once."""
    import platform

    if sys.platform != "linux" or platform.machine() not in ("x86_64", "amd64"):
        raise RuntimeError("Automatic setup supports Linux x86_64 Colab runtimes only.")
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    cached = destination / "runtime.json"
    if cached.is_file():
        return json.loads(cached.read_text(encoding="utf-8"))
    lean_root = destination / f"lean-{LEAN_VERSION}-linux"
    lean = lean_root / "bin" / "lean"
    if not lean.is_file():
        url = ("https://github.com/leanprover/lean4/releases/download/"
               f"v{LEAN_VERSION}/lean-{LEAN_VERSION}-linux.tar.zst")
        archive = destination / f"lean-{LEAN_VERSION}-linux.tar.zst"
        print(f"Downloading official Lean {LEAN_VERSION} release…", flush=True)
        request = urllib.request.Request(url, headers={"User-Agent": "Report-Lean-Notebook"})
        with urllib.request.urlopen(request, timeout=180) as response, archive.open("wb") as target:
            shutil.copyfileobj(response, target)
        try:
            import zstandard
        except ImportError:
            _command([sys.executable, "-m", "pip", "install", "-q", "zstandard"])
            import zstandard
        unpacked = destination / f"lean-{LEAN_VERSION}-linux.tar"
        with archive.open("rb") as source, unpacked.open("wb") as target:
            zstandard.ZstdDecompressor().copy_stream(source, target)
        with tarfile.open(unpacked) as bundle:
            for member in bundle.getmembers():
                if not (destination / member.name).resolve().is_relative_to(destination):
                    raise RuntimeError("Lean archive member escapes the installation directory.")
            bundle.extractall(destination, filter="data")
    env = os.environ.copy()
    env["PATH"] = str(lean_root / "bin") + os.pathsep + env.get("PATH", "")
    _command([lean, "--version"], env=env)
    mathlib = destination / "mathlib"
    if not (mathlib / ".git").is_dir():
        _command(["git", "clone", "--depth", "1", "--branch", f"v{LEAN_VERSION}",
                  "https://github.com/leanprover-community/mathlib4.git", mathlib], env=env)
    commit = _command(["git", "rev-parse", "HEAD"], cwd=mathlib, env=env).stdout.strip()
    if commit != MATHLIB_COMMIT:
        raise RuntimeError(f"Mathlib tag does not match the pinned commit: {commit}")
    _command([lean_root / "bin" / "lake", "exe", "cache", "get"], cwd=mathlib,
             env=env, timeout=3600)
    paths = sorted(str(path.resolve()) for path in
                   (mathlib / ".lake" / "packages").glob("*/.lake/build/lib/lean")
                   if path.is_dir())
    paths.extend([str(mathlib / ".lake" / "build" / "lib" / "lean"),
                  str(lean_root / "lib" / "lean")])
    config = {"toolchain": f"leanprover/lean4:v{LEAN_VERSION}", "lean_exe": str(lean),
              "lean_paths": paths, "mathlib_tag": f"v{LEAN_VERSION}",
              "mathlib_commit": MATHLIB_COMMIT}
    cached.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return config


def _resolve_runtime(proofs_dir, runtime_config=None, allow_download=False):
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
        elif allow_download:
            config = _download_runtime(Path(proofs_dir).parent / "lean-runtime")
        else:
            raise RuntimeError("Pinned Lean runtime is missing; enable allow_download on Colab.")
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
    return config


class LeanNotebook:
    def __init__(self, proofs_dir, workdir=None, runtime_config=None, allow_download=False):
        self.proofs_dir = Path(proofs_dir).resolve(strict=True)
        if not self.proofs_dir.is_dir():
            raise ValueError("proofs_dir must be a directory of exact Lean sources.")
        self.config = _resolve_runtime(self.proofs_dir, runtime_config, allow_download)
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
        self.history = []
        self.env = os.environ.copy()
        self.env["LEAN_PATH"] = os.pathsep.join(
            [str(self.cell_lib), str(self.proof_lib)] + self.config["lean_paths"])
        self.env["PATH"] = str(Path(self.config["lean_exe"]).parent) + os.pathsep + self.env.get("PATH", "")

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
        self._archive(output)
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
            if result.returncode or re.search(r"declaration uses ['`]?sorry", result.stdout + result.stderr):
                raise LeanCellError(f"Lean failed for {source.name} (exit code {result.returncode}).")
            item["passed"] = True
            return item
        except BaseException as error:
            item.update(passed=False, error=str(error), seconds=time.monotonic() - started)
            self._archive(output)
            raise
        finally:
            (self.workdir / "history.json").write_text(
                json.dumps(self.history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _compile_closure(self, code):
        order, active, completed = [], set(), set()

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
            for dependency in _imports(source.read_text(encoding="utf-8-sig")):
                visit(dependency)
            active.remove(source)
            completed.add(source)
            order.append(source)

        for module in _imports(code):
            visit(module)
        for source in order:
            output = self.proof_lib / source.relative_to(self.proofs_dir).with_suffix(".olean")
            self._compile(source, self.proofs_dir, output)

    def run(self, route, stage, code):
        """Compile exactly the caller's cell text, then make its .olean importable."""
        if route not in MODULES or stage not in STAGES:
            raise ValueError("Use route uw/qrm and stage import/start/endpoint.")
        self._invalidate(route, stage)
        index = STAGES.index(stage)
        if index and STAGES[index - 1] not in self.success[route]:
            raise LeanCellError(f"Run '%%lean {route} {STAGES[index - 1]}' successfully first.")
        module = MODULES[route][stage]
        source = self.cell_sources / (module + ".lean")
        source.write_bytes(code.encode("utf-8"))
        if stage == "import":
            self._compile_closure(code)
        item = self._compile(source, self.cell_sources, self.cell_lib / (module + ".olean"))
        self.success[route][stage] = item["sha256"]
        return item

    def cell_magic(self, line, cell):
        arguments = line.strip().split()
        if len(arguments) != 2:
            raise ValueError("Usage: %%lean uw import|start|endpoint (or qrm).")
        self.run(arguments[0], arguments[1], cell)


def install_lean_magic(proofs_dir, workdir=None, runtime_config=None, allow_download=False):
    """Register %%lean in the current IPython shell and return its runtime."""
    from IPython import get_ipython

    shell = get_ipython()
    if shell is None:
        raise RuntimeError("install_lean_magic requires a running IPython notebook kernel.")
    notebook = LeanNotebook(proofs_dir, workdir, runtime_config, allow_download)
    shell.register_magic_function(notebook.cell_magic, magic_kind="cell", magic_name="lean")
    return notebook
