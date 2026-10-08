"""Native Lean cells backed by the checked general-periodic DLW library.

Library reuse is tied to the standard checker's source hashes, compiler,
Mathlib, and immutable artifact hashes. Only the displayed cell is compiled.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SHARED = ROOT / "Workspaces" / "report_colab_20261006"
sys.path.insert(0, str(SHARED))
from lean_notebook import (ARTIFACT_SUFFIXES, LeanCellError, LeanNotebook,
                           _imports, _sha256, _visible_code)

PROOFS = ROOT / "Workspaces" / "dlw_integrability_lean_20261006"
SEED_RESULT = PROOFS / ".lean-runs" / "20261007_112653_73c4af05" / "result.json"
SEED_MANIFEST = HERE / "library_manifest.json"


class IntegrabilityNotebook(LeanNotebook):
    def __init__(self, workdir=None):
        super().__init__(
            PROOFS,
            workdir=workdir or HERE / "lean_runs" / uuid.uuid4().hex,
            runtime_config=ROOT / "_lean_shared" / "runtime.json",
            allow_download=False,
            cache_dir=HERE / "proof_cache",
            seed_runs=[],
        )
        self.library_ready = False
        self.last_cells = {}

    def _describe_library(self):
        report = json.loads(SEED_RESULT.read_text("utf-8-sig"))
        if (report["status"] != "PASSED" or report["toolchain"] != self.config["toolchain"]
                or report["mathlib_commit"] != self.config["mathlib_commit"]
                or Path(report["target"]).resolve() != PROOFS / "FinalEndpoint.lean"):
            raise LeanCellError("The general-periodic DLW proof library has no matching PASSED build.")
        records = report["files"]
        sources, artifacts, order = {}, {}, []
        lib = SEED_RESULT.parent / "lib" / "lean"
        for record in records:
            source = Path(record["file"]).resolve(strict=True)
            output = Path(record["artifact"]).resolve(strict=True)
            if not source.is_relative_to(PROOFS) or not output.is_relative_to(lib):
                raise LeanCellError("Invalid local library build paths.")
            if not record["passed"] or record["exit_code"] != 0 or _sha256(source) != record["sha256"]:
                raise LeanCellError("Proof sources changed: recheck FinalEndpoint with _lean_shared/Check-Lean.ps1.")
            code = _visible_code(source.read_text("utf-8-sig"))
            if re.search(r"\b(sorry|admit|axiom)\b", code):
                raise LeanCellError("A proof placeholder or a new axiom appeared in the library.")
            name = ".".join(source.relative_to(PROOFS).with_suffix("").parts)
            sources[name] = {"path": str(source), "sha256": record["sha256"], "imports": _imports(code)}
            order.append(name)
            for suffix in ARTIFACT_SUFFIXES:
                artifact = output.with_suffix(suffix)
                if artifact.is_file():
                    artifacts[str(artifact)] = _sha256(artifact)
        seen = set()
        for name in order:
            for imported in sources[name]["imports"]:
                local = PROOFS.joinpath(*imported.split(".")).with_suffix(".lean")
                if local.is_file() and imported not in seen:
                    raise LeanCellError("The checked library has an incomplete or unordered import closure.")
            seen.add(name)
        if len(sources) != 105 or "FinalEndpoint" not in sources:
            raise LeanCellError("Expected the complete 105-module FinalEndpoint closure.")
        return {"runtime_identity": self.runtime_identity, "result": str(SEED_RESULT),
                "result_sha256": _sha256(SEED_RESULT), "library": str(lib),
                "sources": sources, "artifacts": artifacts}

    def _check_library(self):
        current = self._describe_library()
        if SEED_MANIFEST.is_file():
            saved = json.loads(SEED_MANIFEST.read_text("utf-8"))
            if saved != current:
                self.library_ready = False
                raise LeanCellError("The checked proof library or local runtime changed; a new verified library manifest is required.")
        else:
            pending = HERE / ("library_manifest_" + uuid.uuid4().hex + ".pending.json")
            pending.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", "utf-8")
            pending.replace(SEED_MANIFEST)
        self.env["LEAN_PATH"] = os.pathsep.join([current["library"], *self.config["lean_paths"]])
        return current

    def run_cell(self, name, code):
        if not re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", name):
            raise ValueError("Usage: %%lean cell-name")
        # The displayed cells each explicitly import their own proof library.
        # Reuse is checked below, independently of a previous cell's execution.
        if name == "library":
            self.library_ready = False
        self.last_cells.pop(name, None)
        library = self._check_library()
        visible = _visible_code(code)
        if re.search(r"\b(sorry|admit|axiom)\b", visible):
            raise LeanCellError("Complete the displayed proof without sorry, admit, or a new axiom.")
        for imported in _imports(code):
            if (PROOFS.joinpath(*imported.split(".")).with_suffix(".lean").is_file()
                    and imported not in library["sources"]):
                raise LeanCellError("This source imports a local module outside the checked closure.")
        # Each attempt owns a module; reruns cannot accidentally import an older cell.
        module = "Cell" + uuid.uuid4().hex
        source = self.cell_sources / (module + ".lean")
        source.write_bytes(code.encode("utf-8"))
        item = self._compile(source, self.cell_sources, self.cell_lib / (module + ".olean"), timeout=300)
        item["cell"] = name
        item["library_manifest_sha256"] = _sha256(SEED_MANIFEST)
        self._save_history()
        # Refuse a result if a library source or artifact changed while compiling.
        self._check_library()
        self.last_cells[name] = item
        if name == "library":
            self.library_ready = True
        return item

    def cell_magic(self, line, cell):
        self.run_cell(line.strip(), cell)


def load_lean():
    from IPython import get_ipython
    shell = get_ipython()
    if shell is None:
        raise RuntimeError("Use a local notebook Python kernel.")
    notebook = shell.user_ns.get("_integrability_lean")
    if not isinstance(notebook, IntegrabilityNotebook):
        notebook = IntegrabilityNotebook()
    # Re-register even on reuse: another notebook can replace the cell magic.
    shell.register_magic_function(notebook.cell_magic, magic_kind="cell", magic_name="lean")
    shell.user_ns["_integrability_lean"] = notebook
