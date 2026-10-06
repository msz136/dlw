"""Run against the started loopback service; retain an auditable JSON test report.

Default checks rejected requests and a genuine checker cancellation. --proof also
performs a complete fresh UW compilation, including the displayed example.
"""
import argparse
import datetime as dt
import http.client
import json
from pathlib import Path
import subprocess
import sys
import time
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent
BASE = "http://127.0.0.1:8766"
checks = []


def request(path, payload=None, method=None, headers=None, expected=200):
    raw = None if payload is None else json.dumps(payload).encode("utf-8")
    values = {"Content-Type": "application/json", "Origin": BASE}
    values.update(headers or {})
    req = urllib.request.Request(BASE + path, data=raw, method=method, headers=values)
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            status, content = response.status, response.read()
    except urllib.error.HTTPError as exc:
        status, content = exc.code, exc.read()
    assert status == expected, (path, expected, status, content[:600])
    return json.loads(content) if content else None


def record(name, details=None):
    checks.append({"name": name, "passed": True, "details": details})
    print("PASS " + name, flush=True)


def wait(job_id, terminal=True, limit=600):
    deadline = time.monotonic() + limit
    while time.monotonic() < deadline:
        value = request("/api/lean/" + job_id)
        if terminal and value["status"] != "running":
            return value
        if not terminal and value["log"].startswith("CHECK "):
            return value
        time.sleep(0.25)
    raise AssertionError("Job did not reach its expected state before the deadline")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--proof", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((HERE.parent / "lean_material" / "manifest.json").read_text(encoding="utf-8"))
    sources = {case["id"]: {Path(source["path"]).name: source["sha256"] for source in case["sources"]}
               for case in manifest["cases"]}
    health = request("/api/health")
    assert health["service"] == "aca-report-notebook" and "4.34.0" in health["leanVersion"]
    record("real Lean version and loopback health", health)

    # GETs cannot disclose an arbitrary workspace file or receive hostile origins.
    for path in ["/AGENTS.md", "/../AGENTS.md", "/%2e%2e/AGENTS.md", "/api/health?x=1"]:
        request(path, expected=404)
    record("static resource allowlist and encoded-path rejection")
    request("/api/health", headers={"Origin": "https://example.invalid"}, expected=403)
    request("/api/health", headers={"Origin": "null"}, expected=403)
    request("/api/health", headers={"Host": "attacker.invalid:8766"}, expected=403)
    request("/api/health", headers={"Sec-Fetch-Site": "cross-site"}, expected=403)
    record("host, Origin null, cross-origin and cross-site rejection")

    body = {"route": "uw", "expectedSources": sources["uw"]}
    request("/api/lean", body, headers={"Content-Type": "text/plain"}, expected=415)
    request("/api/lean", body, headers={"Origin": "https://example.invalid"}, expected=403)
    request("/api/lean", body, headers={"Origin": "null"}, expected=403)
    request("/api/lean", body, method="OPTIONS", expected=403)
    request("/api/lean", body, method="PUT", expected=405)
    request("/api/lean", {"route": "arbitrary", "expectedSources": sources["uw"]}, expected=400)
    request("/api/lean", {"route": "uw", "expectedSources": {}}, expected=409)
    request("/api/lean", {**body, "code": "arbitrary"}, expected=400)
    request("/api/lean", {"route": "uw", "expectedSources": {"../Contracts.lean": "0" * 64}}, expected=409)
    changed = dict(sources["uw"])
    changed["ExampleUW.lean"] = "0" * 64
    request("/api/lean", {"route": "uw", "expectedSources": changed}, expected=409)
    missing = dict(sources["uw"])
    missing.pop("Contracts.lean")
    request("/api/lean", {"route": "uw", "expectedSources": missing}, expected=409)
    # Oversized Content-Length must be rejected before a body is read.
    oversized = http.client.HTTPConnection("127.0.0.1", 8766, timeout=5)
    oversized.request("POST", "/api/lean", body=b"", headers={
        "Content-Type": "application/json", "Origin": BASE, "Content-Length": str(128 * 1024 + 1)
    })
    rejected = oversized.getresponse()
    assert rejected.status == 413
    rejected.read()
    oversized.close()
    request("/api/stop", {"token": "bad"}, expected=403)
    record("write request schema, body limit, route, source hashes and stop token rejection")

    req = urllib.request.Request(BASE + "/api/lean", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=25)
        raise AssertionError("POST without same-origin authorization should fail")
    except urllib.error.HTTPError as exc:
        assert exc.code == 403
    record("missing Origin rejected on writes")

    job_id = request("/api/lean", body, expected=202)["jobId"]
    running = wait(job_id, terminal=False, limit=30)
    assert running["status"] == "running" and running["sourceHashes"] == sources["uw"]
    request("/api/lean", body, expected=409)
    request("/api/lean/" + job_id + "/cancel", {})
    cancelled = wait(job_id, limit=30)
    assert cancelled["status"] == "cancelled" and cancelled["returncode"] != 0
    record("real checker run, one-run limit, Windows process-tree cancellation", {
        "jobId": job_id, "status": cancelled["status"], "returncode": cancelled["returncode"],
        "elapsedSeconds": cancelled["elapsedSeconds"], "log": cancelled["log"],
    })
    if args.proof:
        job_id = request("/api/lean", body, expected=202)["jobId"]
        verified = wait(job_id)
        assert verified["status"] == "ok", verified
        assert verified["returncode"] == 0 and verified["runResult"]["status"] == "PASSED"
        assert len(verified["runResult"]["files"]) == len(sources["uw"])
        assert len(verified["axioms"]) == 2
        record("fresh full UW closure, displayed example and endpoint axioms", {
            key: verified[key] for key in ["jobId", "status", "elapsedSeconds", "axioms", "resultPath"]
        })
    output = {"checkedAt": dt.datetime.now(dt.timezone.utc).isoformat(), "checks": checks}
    destination = HERE / ("service_verification_" + dt.datetime.now().strftime("%Y%m%d_%H%M%S") + ".json")
    destination.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(destination), flush=True)


if __name__ == "__main__":
    main()
