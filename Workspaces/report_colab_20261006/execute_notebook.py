"""Execute the actual deliverable with the project Python kernel and keep outputs."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import nbformat
from jupyter_client import KernelManager
from nbclient import NotebookClient


HERE = Path(__file__).resolve().parent


def sha(data: str | bytes) -> str:
    return hashlib.sha256(data.encode("utf-8") if isinstance(data, str) else data).hexdigest()


def execute(path: Path, timeout: int = 600) -> dict:
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    original_bytes = path.read_bytes()
    original_sources = {cell.id: sha(cell.source) for cell in notebook.cells}
    backup_dir = HERE / "before_execute"
    backup_dir.mkdir(exist_ok=True)
    backup_number = 1
    while (backup_dir / f"Report.pre-execution.{backup_number:03d}.ipynb").exists():
        backup_number += 1
    backup = backup_dir / f"Report.pre-execution.{backup_number:03d}.ipynb"
    backup.write_bytes(original_bytes)
    build_validation_path = HERE / "build_validation.json"
    if build_validation_path.exists():
        (backup_dir / f"build_validation.pre-execution.{backup_number:03d}.json").write_bytes(build_validation_path.read_bytes())

    # Use this project's interpreter even if a global python3 kernel is registered.
    kernel_manager = KernelManager(kernel_name="python3")
    kernel_manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    starts, timings = {}, []

    def on_start(cell, cell_index, **kwargs):
        if cell.cell_type != "code":
            return
        starts[cell.id] = time.perf_counter()
        print(json.dumps({"execute_cell": cell.id, "index": cell_index}, ensure_ascii=False), flush=True)

    def on_executed(cell, cell_index, **kwargs):
        if cell.cell_type != "code":
            return
        elapsed = time.perf_counter() - starts.get(cell.id, time.perf_counter())
        timings.append({"id": cell.id, "index": cell_index, "seconds": round(elapsed, 3)})
        print(json.dumps({"executed_cell": cell.id, "seconds": round(elapsed, 3)}, ensure_ascii=False), flush=True)

    client = NotebookClient(
        notebook, km=kernel_manager, timeout=timeout, startup_timeout=60,
        resources={"metadata": {"path": str(path.resolve().parent)}}, allow_errors=False,
        on_cell_start=on_start, on_cell_executed=on_executed,
    )
    failure = None
    start = time.perf_counter()
    try:
        client.execute()
    except BaseException as error:
        failure = {"type": type(error).__name__, "message": str(error)}
    assert original_sources == {cell.id: sha(cell.source) for cell in notebook.cells}, "The kernel changed notebook source."
    nbformat.validate(notebook)
    nbformat.write(notebook, path)

    code_cells = []
    errors = []
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        outputs = []
        for output in cell.outputs:
            kind = output.output_type
            entry = {"type": kind}
            if kind == "stream":
                entry.update({"name": output.name, "characters": len(output.text), "text_sha256": sha(output.text)})
                if cell.id.startswith("lean-"):
                    entry["raw_text"] = output.text
            elif kind in {"display_data", "execute_result"}:
                entry["mime_types"] = list(output.data)
                entry["payload_sha256"] = {mime: sha(value if isinstance(value, str) else json.dumps(value, sort_keys=True)) for mime, value in output.data.items()}
            elif kind == "error":
                entry.update({"ename": output.ename, "evalue": output.evalue})
                errors.append({"cell": cell.id, "ename": output.ename, "evalue": output.evalue})
            outputs.append(entry)
        code_cells.append({"id": cell.id, "execution_count": cell.execution_count, "source_sha256": sha(cell.source), "outputs": outputs})
    validation = {
        "notebook": str(path), "notebook_sha256": sha(path.read_bytes()),
        "pre_execution_notebook_sha256": sha(original_bytes), "backup": str(backup),
        "python": sys.executable, "kernel": "project interpreter via ipykernel",
        "seconds": round(time.perf_counter() - start, 3),
        "nbformat_schema_valid": True, "cell_sources_unchanged": True,
        "success": failure is None and not errors and all(c["execution_count"] is not None for c in code_cells),
        "failure": failure, "error_outputs": errors,
        "code_cells": code_cells, "cell_timings": timings,
        "outputs_saved_in_deliverable": True,
    }
    (HERE / "execution_validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if build_validation_path.exists():
        build_validation = json.loads(build_validation_path.read_text(encoding="utf-8"))
        build_validation.setdefault("built_notebook_sha256", build_validation["notebook_sha256"])
        build_validation["notebook_sha256"] = validation["notebook_sha256"]
        build_validation["execution_validation"] = "execution_validation.json"
        build_validation["outputs"] = "Actual project-kernel outputs retained in the delivered notebook."
        build_validation_path.write_text(json.dumps(build_validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"success": validation["success"], "code_cells": len(code_cells), "errors": len(errors), "seconds": validation["seconds"], "notebook_sha256": validation["notebook_sha256"]}, ensure_ascii=False), flush=True)
    if not validation["success"]:
        raise RuntimeError(f"Notebook execution failed; actual outputs were saved: {failure or errors}")
    return validation


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--notebook", type=Path, default=HERE / "Report.ipynb")
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()
    execute(args.notebook, args.timeout)
