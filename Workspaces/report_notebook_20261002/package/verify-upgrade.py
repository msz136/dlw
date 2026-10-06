"""Test launcher upgrade in a disposable-by-retention fixture, never the report."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import shutil
import socket
import subprocess
import time
import urllib.request


PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent
WORKSPACE = PROJECT.parent.parent
PORT = 8768
BASE = f"http://127.0.0.1:{PORT}"
STAMP = dt.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
FIXTURE = PACKAGE / ("upgrade_fixture_" + STAMP)
FIXTURE_PROJECT = FIXTURE / "Workspaces" / PROJECT.name
SERVER = FIXTURE_PROJECT / "runtime" / "report_server.py"
STATE = SERVER.parent / f"server-state-{PORT}.json"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def port_open() -> bool:
    try:
        with socket.create_connection(("127.0.0.1", PORT), timeout=0.3):
            return True
    except OSError:
        return False


def health() -> dict:
    with opener.open(BASE + "/api/health", timeout=3) as response:
        return json.load(response)


def launch(idle: int, expected_returncode: int = 0) -> dict:
    proc = subprocess.run([str(FIXTURE / "Report.exe"), "--no-open", "--port", str(PORT),
                           "--idle-seconds", str(idle)], timeout=60,
                          creationflags=subprocess.CREATE_NO_WINDOW, check=False)
    outcomes = sorted((FIXTURE_PROJECT / "package" / "logs").glob("launcher_*.json"),
                      key=lambda path: path.stat().st_mtime_ns)
    outcome = json.loads(outcomes[-1].read_text(encoding="utf-8-sig"))
    if proc.returncode != expected_returncode:
        raise AssertionError(outcome)
    return outcome


def main() -> None:
    assert not port_open(), f"Test requires unused port {PORT}"
    for directory in (SERVER.parent, FIXTURE / "_lean_shared", FIXTURE_PROJECT / "lean_material"):
        directory.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PACKAGE / "Report.exe", FIXTURE / "Report.exe")
    for filename in ("report_server.py", "stepwise_lean.py"):
        shutil.copy2(PROJECT / "runtime" / filename, SERVER.parent / filename)
    for filename in ("check_lean.py", "runtime.json"):
        shutil.copy2(WORKSPACE / "_lean_shared" / filename, FIXTURE / "_lean_shared" / filename)
    shutil.copy2(PROJECT / "lean_material" / "stage_manifest.json",
                 FIXTURE_PROJECT / "lean_material" / "stage_manifest.json")
    (FIXTURE / "Report.html").write_text("<!doctype html><html><body>Launcher upgrade fixture</body></html>", encoding="utf-8")
    original_source = SERVER.read_text(encoding="utf-8")
    assert 'VERSION = "2.0.0"' in original_source
    # This fixture deliberately supplies a transient running-job protocol state;
    # it exercises launcher protection, without performing a scientific proof.
    busy_source = original_source.replace(
        "        self.jobs: dict[str, dict] = {}",
        "        self.jobs: dict[str, dict] = {'f' * 32: {'status': 'running'}}\n"
        "        threading.Timer(10, self.jobs.clear).start()",
        1,
    )
    assert busy_source != original_source
    SERVER.write_text(busy_source, encoding="utf-8")
    first = launch(60)
    first_health = health()
    assert first["started"] is True and first["migrated"] is False
    assert first_health["activeJobs"] == 1
    SERVER.write_text(original_source.replace('VERSION = "2.0.0"', 'VERSION = "2.0.1"'), encoding="utf-8")
    blocked = launch(3, expected_returncode=1)
    protected_health = health()
    assert blocked["status"] == "error"
    assert blocked["error"] == "旧版报告仍在计算。请等待当前运行完成后重新打开报告。"
    assert protected_health["pid"] == first["pid"] and protected_health["activeJobs"] == 1
    assert protected_health["status"] == "ready"
    deadline = time.monotonic() + 15
    while health()["activeJobs"] and time.monotonic() < deadline:
        time.sleep(0.25)
    assert health()["activeJobs"] == 0
    second = launch(3)
    second_health = health()
    assert second["started"] is True and second["migrated"] is True
    assert first["pid"] != second["pid"]
    assert second_health["version"] == "2.0.1"
    assert second_health["workspace"] == str(FIXTURE)
    assert second_health["script"] == str(SERVER)
    deadline = time.monotonic() + 15
    while port_open() and time.monotonic() < deadline:
        time.sleep(0.25)
    assert not port_open(), "Upgraded idle fixture must close itself"
    result = dict(passed=True, verifiedAtUtc=dt.datetime.now(dt.timezone.utc).isoformat(),
                  fixture=str(FIXTURE), port=PORT, oldPid=first["pid"], newPid=second["pid"],
                  upgrade="2.0.0 -> 2.0.1", busyProtocolFixture=True,
                  protectedActiveJob=True, activeJobsBefore=first_health["activeJobs"],
                  usedIdleOnlyStop=True, autoIdleExit=True, browserOpened=False,
                  rootServerUntouchedByTest=True, first=first, blocked=blocked, second=second)
    output = PACKAGE / ("upgrade_verification_" + STAMP + ".json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
