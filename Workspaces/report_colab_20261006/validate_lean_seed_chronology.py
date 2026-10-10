"""Check old-run dependency chronology with genuine Lean compiler artifacts."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import traceback
import uuid

from lean_notebook import LeanNotebook, LeanCellError, _json_hash

HERE = Path(__file__).resolve().parent
ROOT = HERE / "lean_validation_runs" / ("seed_chronology_" + uuid.uuid4().hex)
ROOT.mkdir(parents=True)
CACHE_ROOT = HERE / "seed_guard_cache" / uuid.uuid4().hex[:8]
report = {"root": str(ROOT), "guards": []}


def record(name, **details):
    report["guards"].append({"name": name, "passed": True, **details})
    (HERE / "lean_seed_chronology_validation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("VERIFIED", name, flush=True)


def compile_original(proofs, workdir):
    session = LeanNotebook(proofs, workdir=workdir, cache_dir=ROOT / "unused", seed_runs=[])
    for module in ("SeedBase", "SeedChild"):
        session._compile(proofs / (module + ".lean"), proofs, session.proof_lib / (module + ".olean"))
    return session


try:
    good = ROOT / "good" / "proofs"
    good.mkdir(parents=True)
    (good / "SeedBase.lean").write_bytes(b"import Init\ntheorem seedBase : 1 = 1 := rfl\n")
    (good / "SeedChild.lean").write_bytes(b"import SeedBase\ntheorem seedChild : 1 = 1 := seedBase\n")
    original = compile_original(good, ROOT / "good" / "runs" / "original")
    clean = LeanNotebook(good, workdir=ROOT / "clean", cache_dir=CACHE_ROOT / "good",
                         seed_runs=[original.workdir.parent])
    clean.run("uw", "import", "import SeedChild\n")
    assert all(item["origin"] == "validated_previous_run" for item in clean.cache_events)
    record("matching old sources and preceding dependencies seed actual artifacts",
           original_history=original.history, seeded_events=clean.cache_events, seed_checks=clean.history)

    bad = ROOT / "bad" / "proofs"
    bad.mkdir(parents=True)
    (bad / "SeedBase.lean").write_bytes(b"import Init\ntheorem seedBase : 2 = 2 := rfl\n")
    (bad / "SeedChild.lean").write_bytes(b"import SeedBase\ntheorem seedChild : 2 = 2 := seedBase\n")
    stale = compile_original(bad, ROOT / "bad" / "runs" / "original")
    # A later successful dependency build cannot validate an earlier dependent.
    (bad / "SeedBase.lean").write_bytes(b"import Init\ntheorem seedBase : 1 = 1 := rfl\n")
    stale._compile(bad / "SeedBase.lean", bad, stale.proof_lib / "SeedBase.olean")
    reject = LeanNotebook(bad, workdir=ROOT / "reject", cache_dir=CACHE_ROOT / "bad",
                          seed_runs=[stale.workdir.parent])
    _, records = reject._proof_closure("import SeedChild\n")
    key = _json_hash(reject._proof_descriptor("SeedChild", records))
    out, err = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            reject.run("uw", "import", "import SeedChild\n")
        raise AssertionError("A stale dependent must be rejected and its current source must fail")
    except LeanCellError as error:
        assert "type mismatch" in out.getvalue().lower(), out.getvalue()
        assert not list((reject.cache_dir / key).glob("*/ready.json"))
        assert not (reject.proof_lib / "SeedChild.olean").exists()
        assert reject.success["uw"] == {}
        assert any(Path(item["source"]).name == "SeedChild.lean" and not item["passed"]
                   for item in reject.history)
        record("later dependency build cannot seed an earlier dependent compiled from different source",
               original_history=stale.history, rejected_history=reject.history,
               current_dependent_key=key, stdout=out.getvalue(), stderr=err.getvalue(), error=str(error))

    proofs = HERE / "report_lean" / "proofs"
    audit = LeanNotebook(proofs, workdir=ROOT / "real_seed_audit", cache_dir=HERE / "proof_cache")
    order, records = audit._proof_closure("import ReportNonlinearQRM\n")
    for module in order:
        descriptor = audit._proof_descriptor(module, records)
        ready = audit._ready_entry(_json_hash(descriptor), descriptor)
        assert ready is not None
        audit._copy_artifacts(ready[0] / "lib" / "lean", audit.proof_lib, module)
    provenance = []
    for module in ("PkgQuotientRate", "ReportQRMCalculus", "ReportNonlinearQRM"):
        build = ROOT / "real_seed_audit" / module
        build.mkdir(parents=True)
        seeded = audit._try_seed(module, audit._proof_descriptor(module, records), build)
        assert seeded is not None and seeded["method"] == "validated_previous_run"
        provenance.append({"module": module, "provenance": seeded})
        print("AUDITED REAL SEED", module, flush=True)
    record("all three actual notebook seed histories pass recursive compile-time dependency audit",
           provenance=provenance)
    report["passed"] = True
except Exception as error:
    report.update(passed=False, error=str(error), traceback=traceback.format_exc())
    raise
finally:
    report["helper_source_sha256"] = hashlib.sha256((HERE / "lean_notebook.py").read_bytes()).hexdigest()
    (HERE / "lean_seed_chronology_validation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
