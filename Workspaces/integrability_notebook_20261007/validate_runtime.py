"""Check real cell execution, failure recovery and isolated library tampering."""
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
import shutil

import integrability_runtime as runtime

HERE = Path(__file__).resolve().parent


def attempt(notebook, name, code):
    out, err = StringIO(), StringIO()
    failed = None
    with redirect_stdout(out), redirect_stderr(err):
        try:
            notebook.run_cell(name, code)
        except Exception as exc:
            failed = {"type": type(exc).__name__, "message": str(exc)}
    return {"stdout": out.getvalue(), "stderr": err.getvalue(), "failure": failed}


def main():
    notebook = runtime.IntegrabilityNotebook()
    rows = {}
    rows["self_contained_import"] = attempt(notebook, "early", "import FinalEndpoint\n")
    assert rows["self_contained_import"]["failure"] is None and len(notebook.history) == 1
    rows["import"] = attempt(notebook, "library", "import FinalEndpoint\n#check DLWLean.general_periodic_dlw_integrability\n")
    assert rows["import"]["failure"] is None
    rows["original"] = attempt(notebook, "editable", "import FinalEndpoint\n#eval (2 : Nat) + 3\n")
    rows["edited"] = attempt(notebook, "editable", "import FinalEndpoint\n#eval (2 : Nat) + 4\n")
    assert rows["original"]["stdout"].strip() == "5" and rows["edited"]["stdout"].strip() == "6"
    rows["failed_proof"] = attempt(notebook, "proof", "import FinalEndpoint\nexample : (1 : Nat) = 2 := by decide\n")
    assert rows["failed_proof"]["failure"] and "proof" not in notebook.last_cells
    rows["repaired"] = attempt(notebook, "proof", "import FinalEndpoint\nexample : (1 : Nat) = 1 := rfl\n#check Eq.refl\n")
    assert rows["repaired"]["failure"] is None and "proof" in notebook.last_cells

    # Test corruption only on an independent copy of the verified library.
    clone = HERE / "runtime_validation_library"
    clone.mkdir(exist_ok=True)
    record = json.loads(runtime.SEED_RESULT.read_text("utf-8-sig"))
    seed = clone / ".lean-runs" / "copied_verified_run" / "result.json"
    seed.parent.mkdir(parents=True, exist_ok=True)
    record["target"] = str(clone / "FinalEndpoint.lean")
    record["root"] = str(clone)
    for row in record["files"]:
        src = Path(row["file"])
        dst = clone / src.relative_to(runtime.PROOFS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        old_artifact = Path(row["artifact"])
        artifact = seed.parent / "lib" / "lean" / old_artifact.relative_to(runtime.SEED_RESULT.parent / "lib" / "lean")
        artifact.parent.mkdir(parents=True, exist_ok=True)
        for suffix in runtime.ARTIFACT_SUFFIXES:
            existing = old_artifact.with_suffix(suffix)
            if existing.is_file():
                shutil.copy2(existing, artifact.with_suffix(suffix))
        row.update(file=str(dst), artifact=str(artifact))
    seed.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", "utf-8")
    runtime.PROOFS, runtime.SEED_RESULT, runtime.SEED_MANIFEST = clone, seed, clone / "manifest.json"
    isolated = runtime.IntegrabilityNotebook(workdir=HERE / "runtime_validation_isolated_session")
    isolated._check_library()
    source = clone / "FinalEndpoint.lean"
    original = source.read_bytes()
    source.write_bytes(original + b"\n-- isolated source change\n")
    try:
        rows["source_changed"] = attempt(isolated, "library", "import FinalEndpoint\n")
        assert rows["source_changed"]["failure"] and not isolated.history
    finally:
        source.write_bytes(original)
    artifact = Path(record["files"][-1]["artifact"])
    original = artifact.read_bytes()
    artifact.write_bytes(original + b"isolated artifact change")
    try:
        rows["artifact_changed"] = attempt(isolated, "library", "import FinalEndpoint\n")
        assert rows["artifact_changed"]["failure"] and not isolated.history
    finally:
        artifact.write_bytes(original)
    isolated._check_library()
    result = {"success": True, "real_cell_history": str(notebook.workdir / "history.json"),
              "original_library_unchanged": True, "cases": rows}
    (HERE / "session_fix" / "runtime_validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(json.dumps({"success": True, "cases": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
