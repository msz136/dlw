"""Verify startup/shutdown without executing another Lean proof or opening a browser."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent.parent.parent
BASE = "http://127.0.0.1:8766"
checks = []


def health():
    try:
        with urllib.request.urlopen(BASE + "/api/health", timeout=3) as response:
            return json.load(response)
    except (OSError, urllib.error.URLError):
        return None


def powershell(script, *arguments):
    tag = dt.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    stdout_path = HERE / ("lifecycle_" + tag + ".out.log")
    stderr_path = HERE / ("lifecycle_" + tag + ".err.log")
    # Files avoid inherited-pipe EOF waits when Windows starts a detached child.
    with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        result = subprocess.run(["powershell.exe", "-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass",
                                 "-File", str(script), *arguments], stdout=stdout, stderr=stderr, timeout=40)
    output = stdout_path.read_text(encoding="utf-8", errors="replace")
    error = stderr_path.read_text(encoding="utf-8", errors="replace")
    assert result.returncode == 0, (script.name, result.returncode, output, error)
    return output.strip()


def record(name, details):
    checks.append({"name": name, "passed": True, "details": details})
    print("PASS " + name, flush=True)


def main():
    before = health()
    assert before and before["status"] == "ready"
    record("initial ready service", before)

    for name, target_name in [("启动报告.cmd", "Start Report.cmd"), ("停止报告.cmd", "Stop Report.cmd")]:
        wrapper = WORKSPACE / name
        source = wrapper.read_text(encoding="utf-8-sig")
        target = WORKSPACE / "Workspaces" / "report_notebook_20261002" / "runtime" / target_name
        match = re.search(r'^call\s+"%~dp0(.+)"\s*$', source, re.M | re.I)
        assert match and (WORKSPACE / match.group(1)).resolve() == target.resolve() and target.is_file()
        record("root wrapper path resolves: " + name, {"wrapper": str(wrapper), "target": str(target)})

    stopped = powershell(HERE / "stop-report.ps1")
    assert health() is None, "Health endpoint still available after stop"
    state = json.loads((HERE / "server-state.json").read_text(encoding="utf-8"))
    assert state["status"] == "stopped" and state["pid"] == before["pid"]
    record("graceful stop removes health endpoint and records stopped", {"previousPid": before["pid"], "message": stopped})
    powershell(HERE / "stop-report.ps1")
    assert health() is None
    record("repeated stop is safe", {"status": "stopped"})

    powershell(HERE / "start-report.ps1", "-NoOpenBrowser")
    first = health()
    assert first and first["status"] == "ready" and first["pid"] != before["pid"]
    record("hidden restart without opening browser", first)
    powershell(HERE / "start-report.ps1", "-NoOpenBrowser")
    second = health()
    assert second and first["pid"] == second["pid"]
    record("repeated start reuses service PID", {"pid": second["pid"]})

    for endpoint, filename in [("/Report.html", "Report.html"), ("/report/dlw_error_theory.html", "report/dlw_error_theory.html"),
                               ("/dlw_error_theory.html", "report/dlw_error_theory.html")]:
        with urllib.request.urlopen(BASE + endpoint, timeout=5) as response:
            remote = response.read()
            assert response.status == 200 and response.headers.get_content_type() == "text/html"
        digest = hashlib.sha256(remote).hexdigest()
        assert digest == hashlib.sha256((WORKSPACE / filename).read_bytes()).hexdigest()
        record("exact local HTML served after restart: " + filename, {"bytes": len(remote), "sha256": digest})

    for job_id in ["a1c7e05b39b64b98af0a641c6a53751f", "1a916b01896c4df39b9cd0ac9366be6c"]:
        with urllib.request.urlopen(BASE + "/api/lean/" + job_id, timeout=5) as response:
            job = json.load(response)
        assert job["status"] == "ok" and job["runResult"]["status"] == "PASSED"
        record("completed proof record remains readable after restart", {
            "jobId": job_id, "status": job["status"], "elapsedSeconds": job["elapsedSeconds"],
            "resultPath": job["resultPath"]
        })

    final = health()
    assert final and final["status"] == "ready"
    output = {"checkedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
              "checks": checks, "finalService": final,
              "newProofCompilations": 0, "openedDefaultBrowser": False}
    destination = HERE / ("lifecycle_verification_" + dt.datetime.now().strftime("%Y%m%d_%H%M%S") + ".json")
    destination.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(destination), flush=True)
    print("READY PID " + str(final["pid"]), flush=True)


if __name__ == "__main__":
    main()
