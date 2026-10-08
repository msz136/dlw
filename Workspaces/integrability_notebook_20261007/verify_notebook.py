"""Verify current notebook sources, math and authentic saved compiler output."""
import hashlib
import json
from pathlib import Path
import re

import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(value):
    return hashlib.sha256(value).hexdigest()


def verify():
    path = HERE / "DLW刘维尔可积性report.ipynb"
    notebook = nbformat.read(path, 4)
    nbformat.validate(notebook)
    draft = nbformat.read(HERE / "latest_source_draft.ipynb", 4)
    assert [(c.id,c.cell_type,c.source) for c in notebook.cells] == [(c.id,c.cell_type,c.source) for c in draft.cells]
    histories = []
    for file in (HERE / "lean_runs").glob("*/history.json"):
        histories += [dict(item, history=str(file)) for item in json.loads(file.read_text("utf-8"))]
    rows = []
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        assert cell.execution_count is not None
        assert not any(o.output_type == "error" for o in cell.outputs)
        if cell.source.startswith("%%lean"):
            code = cell.source.split("\n",1)[1]
            digest = sha(code.encode("utf-8"))
            saved = "".join(o.text for o in cell.outputs if o.output_type == "stream")
            runs = [item for item in histories if item.get("passed") and item.get("sha256") == digest
                    and (item.get("stdout", "") + item.get("stderr", "")) == saved]
            assert runs, (cell.id, "Source or saved output has no successful real compiler record")
            assert "sorryAx" not in saved
            rows.append({"cell": cell.id, "lean_source_sha256": digest,
                         "output_sha256": sha(saved.encode("utf-8")), "history": runs[-1]["history"],
                         "compiler_exit_code": runs[-1]["exit_code"], "exact_source_and_output_match": True})
    assert len(rows) == 14
    code = "\n".join(c.source for c in notebook.cells if c.cell_type == "code")
    markdown = "\n".join(c.source for c in notebook.cells if c.cell_type == "markdown")
    for name in ["FieldParameters", "PeriodicPhysicalState", "physicalDLW", "FactorSpectralFoundation",
                 "traceIdentification", "energyIdentity", "chargeConserved", "hamiltonianConserved",
                 "momentumConserved", "spectralCommutes", "familyCommutes", "nonzeroJacobian",
                 "oddGeneric", "familyGeneric", "periodicIntegrability"]:
        assert name in code, name
    assert "HasDerivAt" in code and ".det ≠ 0" in code and "LinearIndependent ℝ" in code
    assert "开稠密" in markdown and "有限前缀" in markdown and "形式 PDO" in markdown
    tags = re.findall(r"\\tag\{(\d+)\}", markdown)
    assert len(tags) == len(set(tags)) and len(tags) >= 18
    execution = json.loads((HERE / "integrability_execution_validation.json").read_text("utf-8"))
    assert execution["success"] and execution["notebook_sha256"] == sha(path.read_bytes())
    revised = json.loads((HERE / "nonlinear_revision" / "revision_validation.json").read_text("utf-8"))
    assert revised["success"] and revised["after_sha256"] == sha((ROOT / "notebook" / "非线性化report.ipynb").read_bytes())
    library = json.loads((HERE / "library_manifest.json").read_text("utf-8"))
    for item in library["sources"].values():
        assert sha(Path(item["path"]).read_bytes()) == item["sha256"]
    result = {"success": True, "notebook": str(path), "notebook_sha256": sha(path.read_bytes()),
              "cells": len(notebook.cells), "code_cells": 15, "lean_cells": 14,
              "sources_match_latest_reviewed_draft": True, "equation_tags": tags,
              "source_library_modules": len(library["sources"]), "source_library_unchanged": True,
              "raw_lean_outputs": rows, "nonlinear_key_definitions_verified": True}
    (HERE / "notebook_content_validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(json.dumps({"success": True, "lean_cells": len(rows), "equations": len(tags)}, ensure_ascii=False))


if __name__ == "__main__":
    verify()
