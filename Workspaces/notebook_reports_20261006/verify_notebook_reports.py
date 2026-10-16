"""Audit the delivered native notebooks and source-preserving HTML archives."""
from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path
import re

import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
REPORTS = {
    "nonlinear": "非线性化report.ipynb",
    "hs": "2HS数值分析report.ipynb",
    "dlw": "DLW数值分析report.ipynb",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify() -> dict:
    rows = []
    preview = HERE / "preview"
    preview.mkdir(exist_ok=True)
    for name, filename in REPORTS.items():
        path = ROOT / "notebook" / filename
        notebook = nbformat.read(path, 4)
        nbformat.validate(notebook)
        evidence = json.loads((HERE / (name + "_execution_validation.json")).read_text("utf-8"))
        assert evidence.get("success", evidence.get("passed", False))
        assert evidence["notebook_sha256"] == sha(path.read_bytes())
        code = [cell for cell in notebook.cells if cell.cell_type == "code"]
        text = "\n".join(cell.source for cell in notebook.cells if cell.cell_type == "markdown")
        assert "现场" not in text
        assert all(cell.execution_count is not None for cell in code)
        assert not [output for cell in code for output in cell.outputs if output.output_type == "error"]
        assert len({cell.id for cell in notebook.cells}) == len(notebook.cells)
        lean = [cell for cell in code if cell.source.startswith("%%lean")]
        assert len(lean) == (6 if name == "nonlinear" else 0)
        if name == "nonlinear":
            assert set(re.findall(r"\\tag\{(\d+)\}", text)) == {str(i) for i in range(1, 23)}
            assert "2HS 单孤子" not in text
            assert not any("sorryAx" in output.get("text", "") for cell in lean for output in cell.outputs)
        if name == "hs":
            assert set(re.findall(r"\\tag\{(\d+)\}", text)) == {str(i) for i in range(1, 13)}
        figures = []
        for cell in code:
            for index, output in enumerate(cell.outputs):
                if "image/png" not in output.get("data", {}):
                    continue
                figure = preview / f"{name}-{cell.id}-{index}.png"
                figure.write_bytes(base64.b64decode(output.data["image/png"]))
                figures.append(str(figure.relative_to(ROOT)))
        assert len(figures) >= (2 if name == "nonlinear" else 3)
        rows.append({"relative_path": str(path.relative_to(ROOT)), "sha256": sha(path.read_bytes()),
                     "cells": len(notebook.cells), "code_cells": len(code),
                     "saved_png_figures": figures, "zero_errors": True,
                     "elapsed_seconds": evidence.get("elapsed_seconds", evidence.get("seconds")),
                     "native_execution_validation": str((HERE / (name + "_execution_validation.json")).relative_to(ROOT))})

    archive = json.loads((HERE / "html_archive_validation.json").read_text("utf-8"))
    assert archive["success"]
    for item in archive["archives"]:
        assert sha(Path(item["source"]).read_bytes()) == item["source_sha256"]
        assert Path(item["backup"]).read_bytes() == Path(item["source"]).read_bytes()
        assert sha(Path(item["archive"]).read_bytes()) == item["archive_sha256"]
        assert all(ref["exists"] for ref in item["local_references"])
    expected_original = "4a7c613a65b5a19424816c5eb165fe5045ad71ca88b4592dac5f21d1f56d2e53"
    assert sha((HERE / "before_split" / "Report.ipynb").read_bytes()) == expected_original
    assert sha((HERE / "before_split" / "Report.original_delivery.ipynb").read_bytes()) == expected_original
    assert not (ROOT / "notebook" / "Report.ipynb").exists()
    assert set(REPORTS.values()) <= {path.name for path in (ROOT / "notebook").glob("*.ipynb")}
    validation = {"success": True, "reports": rows, "html_archives_preserved": True,
                  "original_combined_notebook_preserved": True,
                  "scope_separated": True, "native_outputs_saved": True}
    (HERE / "delivery_validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return validation


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
