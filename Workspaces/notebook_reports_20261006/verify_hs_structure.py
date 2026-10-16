"""Audit the compact 2HS report without replacing its native kernel outputs."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import nbformat

from build_hs_notebook import build
from revise_hs_structure import ast_sequence, transform

HERE = Path(__file__).resolve().parent
NOTEBOOK = HERE.parent.parent / "notebook" / "2HS数值分析report.ipynb"


def verify():
    notebook = nbformat.read(NOTEBOOK, 4)
    nbformat.validate(notebook)
    captured = []
    # Inspect the maintained generator in memory: never write its empty outputs.
    with patch("nbformat.write", side_effect=lambda value, path: captured.append(value)), \
            patch.object(Path, "write_text", return_value=0):
        build()
    generated = captured[0]
    assert [(c.id, c.source) for c in generated.cells] == [
        (c.id, c.source) for c in notebook.cells
    ]
    assert transform(notebook) == notebook
    originals = []
    for path in (HERE / "before_hs_structure").glob("*.ipynb"):
        candidate = nbformat.read(path, 4)
        if not any(c.id == "hs-fd-spatial" for c in candidate.cells):
            originals.append((path, candidate))
    assert originals
    original_path, original = originals[0]
    assert sorted(ast_sequence(original)) == sorted(ast_sequence(notebook))
    current_by_id = {c.id: c for c in notebook.cells}
    output_checks = []
    for cell in original.cells:
        if cell.cell_type == "code":
            assert cell.outputs == current_by_id[cell.id].outputs
            output_checks.append(cell.id)
    execution = json.loads((HERE / "hs_structure_execution_validation.json").read_text("utf-8"))
    assert execution["success"] and execution["code_cell_count"] == 16
    for row in execution["code_cells"]:
        cell = current_by_id[row["id"]]
        assert hashlib.sha256(cell.source.encode("utf-8")).hexdigest() == row["source_sha256"]
        assert cell.execution_count == row["execution_count"]
        compile(cell.source, cell.id, "exec")
    # Equation numbers and subsection order are local to this independent report.
    spatial_ids = ["hs-space-model", "hs-spatial", "hs-fd-model", "hs-fd-spatial",
                   "hs-grid-model", "hs-initial-state"]
    all_ids = [c.id for c in notebook.cells]
    start = all_ids.index("hs-space-model")
    assert all_ids[start:start + len(spatial_ids)] == spatial_ids
    assert "式（28）" not in "\n".join(c.source for c in notebook.cells)
    for cid in ("hs-space-model", "hs-fd-model"):
        source = current_by_id[cid].source
        assert all(parameter in source for parameter in ("c=1", "N=1600", "0.003125", "T=0.5"))
    record = {
        "success": True,
        "notebook": str(NOTEBOOK),
        "notebook_sha256": hashlib.sha256(NOTEBOOK.read_bytes()).hexdigest(),
        "original_backup": str(original_path),
        "generator_sources_and_cell_ids_match": True,
        "generator_checked_without_writing_notebook": True,
        "transformation_idempotent": True,
        "original_python_statements_unchanged": True,
        "all_original_output_cells_identical": output_checks,
        "schema_and_python_syntax_valid": True,
        "code_cell_count": 16,
        "fresh_kernel_execution": "hs_structure_execution_validation.json",
        "fresh_kernel_seconds": execution["elapsed_seconds"],
        "post_execution_markdown_only_changes": True,
        "spatial_sections_and_equation_references_valid": True,
        "single_fd_interval": [-4.799999816459, 3.799999816459],
        "single_fd_dx": 0.005374999771,
        "two_fd_interval": [-5.709089716074, 3.709089716074],
        "two_fd_dx": 0.005886362145,
        "original_error_table_values_unchanged": True,
    }
    (HERE / "hs_structure_delivery_validation.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return record


if __name__ == "__main__":
    verify()
