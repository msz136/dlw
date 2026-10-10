"""Execute six exact Lean cells and check edit, failure and invalidation behavior."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import traceback
import uuid

from IPython.core.interactiveshell import InteractiveShell
from lean_notebook import LeanCellError, MODULES, install_lean_magic

HERE = Path(__file__).resolve().parent
MATERIAL = HERE.parent / "report_notebook_20261002" / "lean_material"
STAGE_MANIFEST = json.loads((MATERIAL / "stage_manifest.json").read_text(encoding="utf-8-sig"))
shell = InteractiveShell.instance()
session = install_lean_magic(MATERIAL / "proofs", workdir=HERE / "lean_validation_runs" / uuid.uuid4().hex)
report = {"toolchain": session.config["toolchain"], "mathlib_commit": session.config["mathlib_commit"],
          "workdir": str(session.workdir), "six_stages": [], "guards": [],
          "linux_colab_setup_verified": False}


def save():
    report["history"] = session.history
    (HERE / "lean_validation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(route, stage, code):
    stdout, stderr = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            shell.run_cell_magic("lean", f"{route} {stage}", code)
        return {"passed": True, "stdout": stdout.getvalue(), "stderr": stderr.getvalue()}
    except Exception as error:
        return {"passed": False, "stdout": stdout.getvalue(), "stderr": stderr.getvalue(),
                "error": str(error), "error_type": type(error).__name__}


def probe(name, operation):
    operation()
    report["guards"].append({"name": name, "passed": True})
    save()
    print("VERIFIED", name, flush=True)


def prerequisite_probe():
    result = run("uw", "endpoint", STAGE_MANIFEST["cases"]["uw"]["endpoint"]["code"])
    assert not result["passed"] and "start" in result["error"], result


try:
    probe("endpoint requires successful start", prerequisite_probe)
    for route in ("uw", "qrm"):
        for stage in ("import", "start", "endpoint"):
            expected = STAGE_MANIFEST["cases"][route][stage]
            code = expected["code"]
            assert hashlib.sha256(code.encode("utf-8")).hexdigest() == expected["sha256"]
            result = run(route, stage, code)
            result.update(route=route, stage=stage, sha256=expected["sha256"])
            report["six_stages"].append(result)
            save()
            assert result["passed"], result
            assert (session.cell_lib / (MODULES[route][stage] + ".olean")).is_file()
            print("COMPILED", route, stage, flush=True)

    def edited_start_probe():
        result = run("uw", "start", STAGE_MANIFEST["cases"]["uw"]["start"]["code"] + "\n#eval 1 + 2\n")
        assert result["passed"] and "3" in result["stdout"].splitlines(), result
        assert "import" in session.success["uw"] and "start" in session.success["uw"]
        assert "endpoint" not in session.success["uw"]
        assert (session.cell_lib / "StepUWImport.olean").is_file()
        assert not (session.cell_lib / "StepUWEndpoint.olean").exists()
        report["edited_start_raw"] = result

    probe("displayed edited code runs and invalidates downstream endpoint", edited_start_probe)

    def bad_start_probe():
        result = run("uw", "start", STAGE_MANIFEST["cases"]["uw"]["start"]["code"] +
                     "\n#check report_notebook_missing_declaration\n")
        assert not result["passed"] and result["error_type"] == "LeanCellError", result
        assert "report_notebook_missing_declaration" in result["stdout"] + result["stderr"], result
        assert "import" in session.success["uw"] and "start" not in session.success["uw"]
        assert not (session.cell_lib / "StepUWStart.olean").exists()
        report["bad_start_raw"] = result

    probe("bad displayed code raises and archives current artifact", bad_start_probe)
    probe("failed upstream stage blocks endpoint", prerequisite_probe)

    def bad_import_probe():
        result = run("qrm", "import", "#check report_notebook_missing_declaration\n")
        assert not result["passed"], result
        assert session.success["qrm"] == {}
        for stage in ("import", "start", "endpoint"):
            assert not (session.cell_lib / (MODULES["qrm"][stage] + ".olean")).exists()
        blocked = run("qrm", "start", STAGE_MANIFEST["cases"]["qrm"]["start"]["code"])
        assert not blocked["passed"] and "import" in blocked["error"], blocked
        report["bad_import_raw"] = result

    probe("failed import invalidates all route stages and blocks start", bad_import_probe)
    report["passed"] = True
except Exception as error:
    report.update(passed=False, error=str(error), traceback=traceback.format_exc())
    raise
finally:
    save()
