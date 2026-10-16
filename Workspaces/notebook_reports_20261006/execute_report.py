"""Execute an independent deliverable in a fresh project Python kernel."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
import uuid

from jupyter_client import KernelManager
from nbclient import NotebookClient
import nbformat

HERE = Path(__file__).resolve().parent


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def execute(path: Path, prefix: str, timeout: int = 600) -> dict:
    notebook = nbformat.read(path, 4)
    nbformat.validate(notebook)
    before = path.read_bytes()
    backup = HERE / "execution_inputs" / (prefix + "_" + uuid.uuid4().hex + ".ipynb")
    backup.parent.mkdir(exist_ok=True)
    backup.write_bytes(before)
    sources = {cell.id: cell.source for cell in notebook.cells}
    km = KernelManager(kernel_name="python3")
    km.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    timings, starts = [], {}

    def start(cell, cell_index, **kwargs):
        if cell.cell_type == "code":
            starts[cell.id] = time.perf_counter()
            print(json.dumps({"starting": cell.id, "index": cell_index}, ensure_ascii=False), flush=True)

    def done(cell, cell_index, **kwargs):
        if cell.cell_type == "code":
            timings.append({"id": cell.id, "seconds": round(time.perf_counter() - starts[cell.id], 3)})
            print(json.dumps(timings[-1], ensure_ascii=False), flush=True)

    client = NotebookClient(
        notebook, km=km, allow_errors=False, timeout=timeout, startup_timeout=60,
        resources={"metadata": {"path": str(path.parent)}},
        on_cell_start=start, on_cell_executed=done,
    )
    failure = None
    started = time.perf_counter()
    try:
        client.execute()
    except Exception as exc:
        failure = {"type": type(exc).__name__, "message": str(exc)}
    assert sources == {cell.id: cell.source for cell in notebook.cells}
    nbformat.validate(notebook)
    nbformat.write(notebook, path)
    errors, executed, output_rows = [], [], []
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        executed.append(cell.execution_count)
        row = {"id": cell.id, "execution_count": cell.execution_count,
               "source_sha256": sha(cell.source.encode("utf-8")), "outputs": []}
        for output in cell.outputs:
            info = {"type": output.output_type}
            if output.output_type == "stream":
                info.update(name=output.name, text=output.text)
            elif output.output_type in {"display_data", "execute_result"}:
                info["mime_types"] = sorted(output.data)
                info["payload_sha256"] = {
                    key: sha((value if isinstance(value, str) else json.dumps(value, sort_keys=True)).encode("utf-8"))
                    for key, value in output.data.items()
                }
                if "text/plain" in output.data:
                    info["text_plain"] = output.data["text/plain"]
            elif output.output_type == "error":
                info.update(ename=output.ename, evalue=output.evalue)
                errors.append({"cell": cell.id, "ename": output.ename, "evalue": output.evalue})
            row["outputs"].append(info)
        output_rows.append(row)
    validation = {
        "notebook": str(path), "notebook_sha256": sha(path.read_bytes()),
        "input_sha256": sha(before), "backup": str(backup),
        "python": sys.executable, "kernel": "fresh native project Python kernel",
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "success": failure is None and not errors and all(v is not None for v in executed),
        "schema_valid": True, "sources_unchanged": True,
        "code_cell_count": len(executed), "errors": errors, "failure": failure,
        "cell_timings": timings, "code_cells": output_rows,
        "outputs_saved": True,
    }
    (HERE / (prefix + "_execution_validation.json")).write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({k: validation[k] for k in ["success", "code_cell_count", "elapsed_seconds", "notebook_sha256"]}), flush=True)
    if not validation["success"]:
        raise RuntimeError(failure or errors)
    return validation


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--notebook", type=Path, required=True)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()
    execute(args.notebook.resolve(), args.prefix, args.timeout)
