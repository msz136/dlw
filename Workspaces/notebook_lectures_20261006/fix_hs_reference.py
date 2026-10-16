"""Correct one equation reference, retaining actual compiled and numeric outputs."""
import hashlib
import json
from pathlib import Path

import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PATH = ROOT / "notebook" / "2HS数值分析report.ipynb"
EVIDENCE = ROOT / "Workspaces/notebook_reports_20261006/hs_execution_validation.json"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def executable_content(notebook):
    return json.dumps([{"id": c.id, "source": c.source,
                        "execution_count": c.execution_count, "outputs": c.outputs}
                       for c in notebook.cells if c.cell_type == "code"],
                      ensure_ascii=False, sort_keys=True).encode("utf-8")


def fix():
    before = PATH.read_bytes()
    notebook = nbformat.read(PATH, 4)
    cell = next(c for c in notebook.cells if c.id == "hs-time-model")
    old, new = "式（4）或（28）", "式（4）或（6）"
    assert old in cell.source
    backup = HERE / "before_reference_fix"
    backup.mkdir(exist_ok=True)
    (backup / PATH.name).write_bytes(before)
    (backup / EVIDENCE.name).write_bytes(EVIDENCE.read_bytes())
    code_before = executable_content(notebook)
    cell.source = cell.source.replace(old, new)
    assert executable_content(notebook) == code_before
    nbformat.validate(notebook)
    nbformat.write(notebook, PATH)
    validation = {"success": True, "notebook": str(PATH),
                  "before_sha256": sha(before), "after_sha256": sha(PATH.read_bytes()),
                  "markdown_cell": "hs-time-model", "old_reference": old, "correct_reference": new,
                  "code_sources_and_actual_outputs_unchanged": True,
                  "code_and_output_digest": sha(code_before),
                  "backup": str(backup / PATH.name)}
    record = HERE / "hs_reference_correction.json"
    record.write_text(json.dumps(validation, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    evidence = json.loads(EVIDENCE.read_text("utf-8"))
    evidence["executed_notebook_sha256"] = evidence["notebook_sha256"]
    evidence["notebook_sha256"] = validation["after_sha256"]
    evidence["post_execution_markdown_correction"] = str(record)
    EVIDENCE.write_text(json.dumps(evidence, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return validation


if __name__ == "__main__":
    print(json.dumps(fix(), ensure_ascii=False, indent=2))
