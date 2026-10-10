"""Validate actual local proof-cache reuse and failure behavior without downloads."""
from concurrent.futures import ThreadPoolExecutor
import contextlib
import hashlib
import io
import json
from pathlib import Path
import time
import traceback
import uuid

from lean_notebook import LeanNotebook, LeanCellError, MODULES, _json_hash

HERE = Path(__file__).resolve().parent
PROOFS = HERE / "report_lean" / "proofs"
STAGES = json.loads((HERE.parent / "report_notebook_20261002" / "lean_material" /
                     "stage_manifest.json").read_text(encoding="utf-8-sig"))["cases"]
TEST_ROOT = HERE / "lean_validation_runs" / ("local_cache_" + uuid.uuid4().hex)
TEST_ROOT.mkdir(parents=True)
CACHE_ROOT = HERE / "lean_guard_cache" / uuid.uuid4().hex[:8]
report = {"test_root": str(TEST_ROOT), "six_stages": [], "guards": []}


def save():
    (HERE / "local_lean_validation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(session, route, stage, code):
    out, err = io.StringIO(), io.StringIO()
    start = time.monotonic()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            item = session.run(route, stage, code)
            result = {"passed": True, "compilation": item}
        except Exception as error:
            result = {"passed": False, "error": str(error), "error_type": type(error).__name__}
    result.update(stdout=out.getvalue(), stderr=err.getvalue(), seconds=time.monotonic() - start)
    return result


def guard(name, details):
    report["guards"].append({"name": name, "passed": True, **details})
    save()
    print("VERIFIED", name, flush=True)


try:
    actual = LeanNotebook(PROOFS, workdir=TEST_ROOT / "six_stages", cache_dir=HERE / "proof_cache")
    report.update(runtime=actual.runtime_identity, cache_dir=str(actual.cache_dir),
                  seed_runs=[str(path) for path in actual.seed_runs])
    for route in ("uw", "qrm"):
        for stage in ("import", "start", "endpoint"):
            code = STAGES[route][stage]["code"]
            result = run(actual, route, stage, code)
            result.update(route=route, stage=stage,
                          displayed_code_sha256=hashlib.sha256(code.encode("utf-8")).hexdigest())
            report["six_stages"].append(result)
            save()
            assert result["passed"], result
            assert (actual.cell_lib / (MODULES[route][stage] + ".olean")).is_file()
            print("COMPILED", route, stage, result["seconds"], flush=True)
    report["actual_cache_events"] = actual.cache_events
    report["actual_history"] = actual.history
    assert len([item for item in actual.history if "cells" in Path(item["source"]).parts]) == 6
    warm = LeanNotebook(PROOFS, workdir=TEST_ROOT / "warm_session", cache_dir=HERE / "proof_cache")
    for route in ("uw", "qrm"):
        result = run(warm, route, "import", STAGES[route]["import"]["code"])
        assert result["passed"], result
    assert all(item["origin"] == "warm_cache" for item in warm.cache_events), warm.cache_events
    assert len(warm.history) == 2 and all("cells" in Path(item["source"]).parts for item in warm.history)
    guard("new session imports exact persistent compiled proofs with zero proof recompilations",
          {"events": warm.cache_events, "history": warm.history})

    displayed = run(actual, "uw", "start", STAGES["uw"]["start"]["code"] + "\n#eval 1 + 2\n")
    assert displayed["passed"] and "3" in displayed["stdout"].splitlines(), displayed
    assert "endpoint" not in actual.success["uw"]
    bad = run(actual, "uw", "start", STAGES["uw"]["start"]["code"] +
              "\n#check local_cache_missing_declaration\n")
    assert not bad["passed"] and "local_cache_missing_declaration" in bad["stdout"] + bad["stderr"]
    assert "start" not in actual.success["uw"] and not (actual.cell_lib / "StepUWStart.olean").exists()
    guard("displayed cells compile current edits and failed compile archives prior artifact",
          {"edited_raw": displayed, "failed_raw": bad})

    tiny = TEST_ROOT / "tiny" / "proofs"
    tiny.mkdir(parents=True)
    base_code = "import Init\ntheorem cacheBase : 1 = 1 := rfl\n"
    (tiny / "CacheBase.lean").write_bytes(base_code.encode("utf-8"))
    (tiny / "CacheChild.lean").write_bytes(
        b"import CacheBase\ntheorem cacheChild : 1 = 1 := cacheBase\n")
    cold = LeanNotebook(tiny, workdir=TEST_ROOT / "cold", cache_dir=CACHE_ROOT / "cold", seed_runs=[])
    result = run(cold, "uw", "import", "import CacheChild\n")
    assert result["passed"], result
    assert len(cold.cache_events) == 2 and all(
        item["origin"] == "compiled_exact_sources" for item in cold.cache_events)
    before_keys = {item["module"]: item["key"] for item in cold.cache_events}
    guard("cold cache genuinely compiles both local proofs", {"raw": result, "events": cold.cache_events})

    (tiny / "CacheBase.lean").write_bytes((base_code + "#eval 37\n").encode("utf-8"))
    blocked = run(cold, "uw", "start", "import StepUWImport\n")
    assert not blocked["passed"] and "sources changed" in blocked["error"]
    assert cold.success["uw"] == {} and not (cold.cell_lib / "StepUWImport.olean").exists()
    changed = run(cold, "uw", "import", "import CacheChild\n")
    assert changed["passed"] and "37" in changed["stdout"].splitlines(), changed
    edited_events = cold.cache_events[-2:]
    assert all(item["key"] != before_keys[item["module"]] for item in edited_events)
    assert all(item["origin"] == "compiled_exact_sources" for item in edited_events)
    guard("dependency edit invalidates its dependent cache and existing stage prerequisites",
          {"blocked": blocked, "changed_raw": changed, "events": edited_events})

    (tiny / "CacheBase.lean").write_bytes(b"import Init\ntheorem cacheBase : False := by trivial\n")
    _, records = cold._proof_closure("import CacheChild\n")
    failed_key = _json_hash(cold._proof_descriptor("CacheBase", records))
    broken = run(cold, "uw", "import", "import CacheChild\n")
    assert not broken["passed"] and broken["error_type"] == "LeanCellError", broken
    assert not list((cold.cache_dir / failed_key).glob("*/ready.json"))
    assert not (cold.proof_lib / "CacheBase.olean").exists()
    assert not (cold.proof_lib / "CacheChild.olean").exists()
    assert cold.success["uw"] == {}
    guard("failed edited proof cannot publish or reuse stale proof artifacts",
          {"failed_key": failed_key, "raw": broken})

    (tiny / "CacheBase.lean").write_bytes(base_code.encode("utf-8"))
    corrupt_entry = Path(cold.cache_events[0]["entry"])
    artifact = corrupt_entry / "lib" / "lean" / "CacheBase.olean"
    original = artifact.read_bytes()
    (corrupt_entry / "CacheBase.before_integrity_probe.olean").write_bytes(original)
    artifact.write_bytes(original + b"corrupt")
    repaired = LeanNotebook(tiny, workdir=TEST_ROOT / "integrity", cache_dir=cold.cache_dir, seed_runs=[])
    result = run(repaired, "uw", "import", "import CacheChild\n")
    assert result["passed"], result
    assert repaired.cache_events[0]["origin"] == "compiled_exact_sources"
    assert repaired.cache_events[0]["entry"] != str(corrupt_entry)
    guard("artifact hash mismatch rejects corrupted cache and builds a new immutable entry",
          {"raw": result, "events": repaired.cache_events})

    concurrent_proofs = TEST_ROOT / "concurrent" / "proofs"
    concurrent_proofs.mkdir(parents=True)
    (concurrent_proofs / "ConcurrentProof.lean").write_bytes(
        b"import Init\ntheorem concurrentProof : 2 = 2 := rfl\n")
    def concurrent_import(index):
        notebook = LeanNotebook(concurrent_proofs, workdir=TEST_ROOT / f"concurrent_session_{index}",
                                cache_dir=CACHE_ROOT / "race", seed_runs=[])
        item = notebook.run("uw", "import", "import ConcurrentProof\n")
        return {"cell": item, "events": notebook.cache_events}
    with ThreadPoolExecutor(max_workers=2) as pool:
        concurrent = list(pool.map(concurrent_import, (0, 1)))
    entries = {result["events"][0]["entry"] for result in concurrent}
    for entry in entries:
        assert (Path(entry) / "ready.json").is_file()
    guard("concurrent sessions commit unique complete cache builds", {"sessions": concurrent})

    try:
        LeanNotebook(PROOFS, allow_download=True)
        raise AssertionError("Automatic downloads must be unavailable")
    except RuntimeError as error:
        assert "downloads are disabled" in str(error)
        guard("local-only setup rejects automatic download requests", {"error": str(error)})
    report["passed"] = True
except Exception as error:
    report.update(passed=False, error=str(error), traceback=traceback.format_exc())
    raise
finally:
    save()
