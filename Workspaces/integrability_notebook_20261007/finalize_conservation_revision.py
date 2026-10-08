"""Re-execute only the added explicit K/P goals after the initial full run.

This script refuses a failed/incomplete initial run, preserves it, executes
three actual cells in a fresh native kernel, and replaces only conservation.
All other cell sources, execution counters, metadata and outputs are retained.
"""
from __future__ import annotations

from contextlib import redirect_stdout
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

import nbformat

from execute_notebook import executor

HERE = Path(__file__).resolve().parent
NOTEBOOK = HERE / "DLW刘维尔可积性report.ipynb"
LATEST = HERE / "latest_source_draft.ipynb"
FULL_EVIDENCE = HERE / "integrability_execution_validation.json"
BEFORE = HERE / "before_conservation_revision"
PARTIAL = HERE / "conservation_revision.executed.ipynb"
PARTIAL_EVIDENCE = HERE / "conservation_revision_execution_validation.json"
REVISION_EVIDENCE = HERE / "conservation_revision_validation.json"
TARGET = "lean-conservation"
SELECTED = ["python-load", "lean-library", TARGET]


def sha(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def json_read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def json_write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, text):
        for stream in self.streams:
            stream.write(text)
            stream.flush()
        return len(text)

    def flush(self):
        for stream in self.streams:
            stream.flush()


def main() -> dict:
    old_bytes = NOTEBOOK.read_bytes()
    evidence_bytes = FULL_EVIDENCE.read_bytes()
    original_evidence = json.loads(evidence_bytes.decode("utf-8"))
    assert original_evidence["success"], "The initial complete execution has not passed."
    assert original_evidence["code_cell_count"] == 15
    assert not original_evidence["errors"] and original_evidence["failure"] is None
    assert original_evidence["notebook_sha256"] == sha(old_bytes)
    assert "post_execution_lean_revision" not in original_evidence, "This revision was already applied."

    old = nbformat.read(NOTEBOOK, 4)
    latest = nbformat.read(LATEST, 4)
    assert len(old.cells) == len(latest.cells)
    assert [(c.id, c.cell_type) for c in old.cells] == [(c.id, c.cell_type) for c in latest.cells]
    changed_sources = [a.id for a, b in zip(old.cells, latest.cells) if a.source != b.source]
    assert changed_sources == [TARGET], f"Unexpected source changes: {changed_sources}"
    assert all(c.execution_count is not None for c in old.cells if c.cell_type == "code")
    assert all(not any(o.output_type == "error" for o in c.outputs)
               for c in old.cells if c.cell_type == "code")
    new_target = next(c for c in latest.cells if c.id == TARGET)
    assert "theorem hamiltonianConserved" in new_target.source
    assert "theorem momentumConserved" in new_target.source

    BEFORE.mkdir(exist_ok=True)
    initial_notebook = BEFORE / NOTEBOOK.name
    initial_evidence = BEFORE / FULL_EVIDENCE.name
    assert not initial_notebook.exists() and not initial_evidence.exists(), "Initial history already preserved."
    initial_notebook.write_bytes(old_bytes)
    initial_evidence.write_bytes(evidence_bytes)

    partial_cells = []
    for cell_id in SELECTED:
        cell = deepcopy(next(c for c in latest.cells if c.id == cell_id))
        assert cell.cell_type == "code"
        cell.outputs = []
        cell.execution_count = None
        partial_cells.append(cell)
    partial_notebook = nbformat.v4.new_notebook(cells=partial_cells, metadata=deepcopy(latest.metadata))
    nbformat.validate(partial_notebook)
    assert not PARTIAL.exists(), "A targeted execution already exists; inspect its evidence first."
    nbformat.write(partial_notebook, PARTIAL)

    histories_before = set((HERE / "lean_runs").glob("*/history.json"))
    with (HERE / "conservation_revision.stdout.txt").open("w", encoding="utf-8") as log:
        with redirect_stdout(Tee(sys.stdout, log)):
            partial_evidence = executor.execute(PARTIAL, "conservation_revision", timeout=600)
    assert partial_evidence["success"]
    assert partial_evidence["code_cell_count"] == 3
    partial_result = nbformat.read(PARTIAL, 4)
    assert [c.id for c in partial_result.cells] == SELECTED
    assert [c.execution_count for c in partial_result.cells] == [1, 2, 3]
    revised = deepcopy(next(c for c in partial_result.cells if c.id == TARGET))
    assert revised.source == new_target.source
    assert revised.outputs
    output_text = "\n".join(o.text for o in revised.outputs if o.output_type == "stream")
    assert "NotebookDLWConservation.hamiltonianConserved" in output_text
    assert "NotebookDLWConservation.momentumConserved" in output_text
    assert "sorryAx" not in output_text

    histories_after = set((HERE / "lean_runs").glob("*/history.json"))
    matching_histories = []
    for path in sorted(histories_after - histories_before):
        rows = json_read(path)
        if [r.get("cell") for r in rows] != ["library", "conservation"]:
            continue
        assert all(r["passed"] and r["exit_code"] == 0 for r in rows)
        assert all(Path(r["source"]).is_file() and Path(r["artifact"]).is_file() for r in rows)
        assert all(sha(Path(r["source"]).read_bytes()) == r["sha256"] for r in rows)
        assert all(sha(Path(r["artifact"]).read_bytes()) == r["artifact_sha256"] for r in rows)
        assert rows[1]["stdout"] == output_text.strip() + "\n" or rows[1]["stdout"].strip() == output_text.strip()
        matching_histories.append(path)
    assert len(matching_histories) == 1, "The actual targeted Lean compile history is ambiguous."

    merged = deepcopy(old)
    target_index = next(i for i, c in enumerate(merged.cells) if c.id == TARGET)
    merged.cells[target_index] = revised
    nbformat.validate(merged)
    assert [a.id for a, b in zip(old.cells, merged.cells) if a != b] == [TARGET]
    assert [(c.id, c.source) for c in merged.cells] == [(c.id, c.source) for c in latest.cells]
    nbformat.write(merged, NOTEBOOK)
    final_sha = sha(NOTEBOOK.read_bytes())

    revision = {
        "success": True,
        "mode": "initial complete execution plus a fresh three-cell native-kernel revision",
        "notebook": str(NOTEBOOK),
        "before_sha256": sha(old_bytes),
        "after_sha256": final_sha,
        "latest_source_draft": str(LATEST),
        "latest_source_sha256": sha(LATEST.read_bytes()),
        "changed_source_cells": changed_sources,
        "changed_saved_cells": [TARGET],
        "preserved_other_code_cells": 14,
        "preserved_other_code_sources_outputs_counts_and_metadata": True,
        "original_full_notebook": str(initial_notebook),
        "original_full_execution_evidence": str(initial_evidence),
        "original_full_evidence_sha256": sha(evidence_bytes),
        "partial_execution_notebook": str(PARTIAL),
        "partial_execution_validation": str(PARTIAL_EVIDENCE),
        "partial_executed_cells": SELECTED,
        "partial_execution_counts": [c.execution_count for c in partial_result.cells],
        "merged_target_execution_count": revised.execution_count,
        "compile_history": str(matching_histories[0]),
        "compile_history_sha256": sha(matching_histories[0].read_bytes()),
        "full_execution_elapsed_seconds": original_evidence["elapsed_seconds"],
        "partial_revision_elapsed_seconds": partial_evidence["elapsed_seconds"],
    }
    json_write(REVISION_EVIDENCE, revision)

    updated = deepcopy(original_evidence)
    updated["executed_notebook_sha256"] = original_evidence["notebook_sha256"]
    updated["notebook_sha256"] = final_sha
    updated["original_full_execution_validation"] = str(initial_evidence)
    updated["original_full_execution_notebook"] = str(initial_notebook)
    updated["verification_mode"] = revision["mode"]
    updated["post_execution_lean_revision"] = str(REVISION_EVIDENCE)
    updated["partial_revision_execution_validation"] = str(PARTIAL_EVIDENCE)
    updated["full_execution_elapsed_seconds"] = original_evidence["elapsed_seconds"]
    updated["partial_revision_elapsed_seconds"] = partial_evidence["elapsed_seconds"]
    updated["elapsed_seconds_note"] = "Original complete execution; the later partial revision is reported separately."
    target_row = deepcopy(next(r for r in partial_evidence["code_cells"] if r["id"] == TARGET))
    target_row["execution_provenance"] = str(PARTIAL_EVIDENCE)
    updated["code_cells"] = [target_row if r["id"] == TARGET else r for r in updated["code_cells"]]
    old_timing = deepcopy(next(r for r in updated["cell_timings"] if r["id"] == TARGET))
    updated["original_full_conservation_timing"] = old_timing
    new_timing = deepcopy(next(r for r in partial_evidence["cell_timings"] if r["id"] == TARGET))
    new_timing["execution_provenance"] = str(PARTIAL_EVIDENCE)
    updated["cell_timings"] = [new_timing if r["id"] == TARGET else r for r in updated["cell_timings"]]
    updated["preserved_other_code_cells"] = 14
    json_write(FULL_EVIDENCE, updated)
    print(json.dumps({"success": True, "notebook_sha256": final_sha,
                      "revision_evidence": str(REVISION_EVIDENCE),
                      "partial_revision_elapsed_seconds": partial_evidence["elapsed_seconds"]}, ensure_ascii=False))
    return revision


if __name__ == "__main__":
    main()
