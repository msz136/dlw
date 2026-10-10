"""Validate the final byte-preserving setup without repeating the proven cells.

The full notebook was already executed. This final, narrow update changes only
newline fidelity and the native collapsed-cell title. All scientific cell
bodies and their real outputs remain those of the complete integration run.
"""
from __future__ import annotations

import ast
import base64
import difflib
import hashlib
import json
import sys
import zlib
from pathlib import Path

import nbformat
from jupyter_client import KernelManager
from nbclient import NotebookClient


HERE = Path(__file__).resolve().parent
FROZEN_PROOFS = HERE.parent / "report_notebook_20261002" / "lean_material" / "proofs"


def sha(data: str | bytes) -> str:
    return hashlib.sha256(data.encode("utf-8") if isinstance(data, str) else data).hexdigest()


def bundle(source: str) -> dict[str, str]:
    assignment = next(
        item for item in ast.parse(source).body
        if isinstance(item, ast.Assign) and isinstance(item.targets[0], ast.Name)
        and item.targets[0].id == "_lean_bundle"
    )
    return json.loads(zlib.decompress(base64.b64decode(ast.literal_eval(assignment.value))))


def finalize() -> dict:
    path = HERE / "Report.ipynb"
    notebook = nbformat.read(path, as_version=4)
    full_validation_path = HERE / "execution_validation.json"
    full_validation = json.loads(full_validation_path.read_text(encoding="utf-8"))
    assert full_validation["success"] and not full_validation["error_outputs"]
    preparation = next(cell for cell in notebook.cells if cell.id == "runtime-prepare")
    original_bootstrap = preparation.source
    final_bootstrap = (HERE / "bootstrap_source.txt").read_text(encoding="utf-8")
    assert final_bootstrap.startswith("# @title 准备 Lean 与 Mathlib\n")
    original_files, final_files = bundle(original_bootstrap), bundle(final_bootstrap)
    assert original_files.keys() == final_files.keys()
    for name in final_files:
        if name.startswith("proofs/"):
            assert original_files[name].replace("\r\n", "\n") == final_files[name].replace("\r\n", "\n"), name
    assert original_files["lean_notebook.py"].replace(
        'source.write_text(code, encoding="utf-8")', 'source.write_bytes(code.encode("utf-8"))'
    ) == final_files["lean_notebook.py"], "The final helper changed beyond stage-source byte fidelity."
    others_before = {cell.id: sha(cell.source) for cell in notebook.cells if cell.id != "runtime-prepare"}
    other_outputs_before = {cell.id: sha(json.dumps(cell.get("outputs", []), ensure_ascii=False, sort_keys=True)) for cell in notebook.cells if cell.id != "runtime-prepare"}
    backup_dir = HERE / "before_final_bootstrap"
    backup_dir.mkdir(exist_ok=True)
    assert not (backup_dir / "Report.full-run.ipynb").exists(), "Finalization evidence already exists; inspect before rerunning."
    (backup_dir / "Report.full-run.ipynb").write_bytes(path.read_bytes())
    (backup_dir / "execution.full-run.json").write_bytes(full_validation_path.read_bytes())
    (backup_dir / "build.full-run.json").write_bytes((HERE / "build_validation.json").read_bytes())

    single = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(final_bootstrap, id="runtime-prepare")])
    manager = KernelManager(kernel_name="python3")
    manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    client = NotebookClient(single, km=manager, timeout=120, startup_timeout=60, resources={"metadata": {"path": str(HERE)}}, allow_errors=False)
    client.execute()
    assert not [output for output in single.cells[0].outputs if output.output_type == "error"]
    checks = []
    for name, text in final_files.items():
        extracted = HERE / "report_lean" / name
        expected_original = (FROZEN_PROOFS / Path(name).name) if name.startswith("proofs/") else HERE / name
        expected_bytes = expected_original.read_bytes()
        assert text.encode("utf-8") == expected_bytes, "Embedded original bytes differ: " + name
        assert extracted.read_bytes() == expected_bytes, "Extracted original bytes differ: " + name
        checks.append({"name": name, "sha256": sha(expected_bytes), "bytes": len(expected_bytes), "embedded_matches_original": True, "extracted_matches_original": True})
    nbformat.write(single, HERE / "bootstrap_final_run.ipynb")

    preparation.source = final_bootstrap
    preparation.outputs = single.cells[0].outputs
    preparation.execution_count = single.cells[0].execution_count
    preparation.metadata["report_source"]["sha256"] = sha(final_bootstrap)
    preparation.metadata["execution"] = single.cells[0].metadata.get("execution", {})
    assert others_before == {cell.id: sha(cell.source) for cell in notebook.cells if cell.id != "runtime-prepare"}
    assert other_outputs_before == {cell.id: sha(json.dumps(cell.get("outputs", []), ensure_ascii=False, sort_keys=True)) for cell in notebook.cells if cell.id != "runtime-prepare"}
    nbformat.validate(notebook)
    nbformat.write(notebook, path)
    final_hash = sha(path.read_bytes())
    evidence = {
        "success": True, "notebook_sha256": final_hash,
        "full_run_notebook_backup": str(backup_dir / "Report.full-run.ipynb"),
        "full_run_notebook_sha256": full_validation["notebook_sha256"],
        "original_bootstrap_sha256": sha(original_bootstrap), "final_bootstrap_sha256": sha(final_bootstrap),
        "bootstrap_cell_source_sha256": sha(final_bootstrap),
        "bootstrap_source_file_sha256": sha((HERE / "bootstrap_source.txt").read_bytes()),
        "final_preparation_executed_with_project_kernel": True,
        "scientific_cell_sources_unchanged": True, "scientific_cell_outputs_unchanged": True,
        "proof_text_unchanged_after_newline_normalization": True,
        "helper_change": "Only writes displayed stage source with write_bytes instead of write_text.",
        "helper_diff": "".join(difflib.unified_diff(original_files["lean_notebook.py"].splitlines(keepends=True), final_files["lean_notebook.py"].splitlines(keepends=True))),
        "bundled_files": checks,
        "raw_setup_output": [{"type": output.output_type, "text": output.get("text", "")} for output in preparation.outputs],
        "nbformat_schema_valid": True,
        "execution_scope": "21 cells executed in the complete run; final setup was executed separately after the newline-preserving update. No mathematical statements, numerical methods, or scientific cell code changed.",
    }
    (HERE / "bootstrap_integration_validation.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    full_validation["full_run_notebook_sha256"] = full_validation["notebook_sha256"]
    full_validation["notebook_sha256"] = final_hash
    full_validation["bootstrap_integration_validation"] = "bootstrap_integration_validation.json"
    full_validation["execution_scope"] = evidence["execution_scope"]
    code_record = next(record for record in full_validation["code_cells"] if record["id"] == "runtime-prepare")
    code_record["source_sha256"] = sha(final_bootstrap)
    code_record["outputs"] = [{"type": output.output_type, "name": output.get("name"), "characters": len(output.get("text", "")), "text_sha256": sha(output.get("text", ""))} for output in preparation.outputs]
    full_validation_path.write_text(json.dumps(full_validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    build_path = HERE / "build_validation.json"
    built = json.loads(build_path.read_text(encoding="utf-8"))
    built["notebook_sha256"] = final_hash
    built["bootstrap_integration_validation"] = "bootstrap_integration_validation.json"
    built["final_bootstrap_sha256"] = sha(final_bootstrap)
    built["bootstrap_cell_source_sha256"] = sha(final_bootstrap)
    built["bootstrap_source_file_sha256"] = evidence["bootstrap_source_file_sha256"]
    build_path.write_text(json.dumps(built, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"success": True, "notebook_sha256": final_hash, "final_bootstrap_sha256": sha(final_bootstrap), "original_bytes_verified": len(checks)}, ensure_ascii=False))
    return evidence


if __name__ == "__main__":
    finalize()
