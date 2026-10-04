"""Fixed-source, loopback-only Report.html and genuine Lean checker service.

Only reviewed sequential proof cells can run. The import cell freshly builds
the theorem library; later cells share that exact session's checked artifacts.
There is no arbitrary source, shell, upload, or file endpoint.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
import os
from pathlib import Path
import re
import secrets
import signal
import subprocess
import sys
import threading
import time
import uuid

from stepwise_lean import StepwiseLean, PROOF_MODULES


SERVICE = "aca-report-notebook"
VERSION = "2.2.1"
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
WORKSPACE = PROJECT.parent.parent
REPORT = WORKSPACE / "Report.html"
CHECKER = WORKSPACE / "_lean_shared" / "check_lean.py"
RUNTIME_CONFIG = WORKSPACE / "_lean_shared" / "runtime.json"
PROOF_ROOT = PROJECT / "lean_material" / "proofs"
ORIGINAL_ROOT = WORKSPACE / "Workspaces" / "lean_contracts" / "proofs"
MANIFEST = PROJECT / "lean_material" / "manifest.json"
JOBS_DIR = HERE / "jobs"
PID_FILE = HERE / "server-state.json"
TARGETS = {"uw": "ExampleUW.lean", "qrm": "ExampleQRM.lean"}
ENDPOINTS = {
    "uw": ["DLWContract.ReportUW.semiPair_implies_report7",
           "DLWContract.ReportUW.semiPair_implies_report8"],
    "qrm": ["DLWContract.ReportQRM.semiPair_implies_report21",
            "DLWContract.ReportQRM.report22"],
}
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
MAX_BODY = 128 * 1024
MAX_LOG = 2 * 1024 * 1024
MAX_WALL_SECONDS = 20 * 60
JOB_ID = re.compile(r"[0-9a-f]{32}")
FILENAME = re.compile(r"[A-Za-z][A-Za-z0-9_]*\.lean")

spec = importlib.util.spec_from_file_location("aca_shared_lean_checker", CHECKER)
checker_module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(checker_module)


class RequestError(Exception):
    def __init__(self, message: str, status: int = 400):
        self.message, self.status = message, status


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path: Path, value: dict) -> None:
    # Retains every final job and run. Replacing this same-purpose state file
    # never deletes a proof, log, artifact, or user document.
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".pending")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def proof_closure(route: str) -> list[Path]:
    """Follow only ordinary local imports; shared Mathlib remains read-only."""
    config = json.loads(RUNTIME_CONFIG.read_text(encoding="utf-8-sig"))
    active, done, ordered = set(), set(), []

    def visit(path: Path) -> None:
        path = path.resolve(strict=True)
        if path.parent != PROOF_ROOT.resolve() or not FILENAME.fullmatch(path.name):
            raise RequestError("Proof paths must be reviewed .lean filenames directly under proofs.", 409)
        if path in active:
            raise RequestError("Cyclic proof imports.", 409)
        if path in done:
            return
        code = checker_module.visible_code(path.read_text(encoding="utf-8-sig"))
        if re.search(r"\b(sorry|admit|axiom)\b", code):
            raise RequestError(f"Proof placeholder or new axiom rejected in {path.name}.", 409)
        active.add(path)
        for match in re.finditer(r"^\s*(?:(?:public|private)\s+)?(?:meta\s+)?import\s+([^\n]+)", code, re.M):
            for module in match.group(1).split():
                if not re.fullmatch(r"[\w\u0080-\uffff]+(?:\.[\w\u0080-\uffff]+)*", module):
                    raise RequestError("Unreviewed import syntax.", 409)
                local = PROOF_ROOT.joinpath(*module.split(".")).with_suffix(".lean")
                if local.is_file():
                    if module.split(".")[0] in config["reserved_modules"]:
                        raise RequestError("Shadowing a shared module is prohibited.", 409)
                    visit(local)
        active.remove(path)
        done.add(path)
        ordered.append(path)

    visit(PROOF_ROOT / TARGETS[route])
    return ordered


def audit_sources(route: str, expected: object) -> tuple[list[Path], dict[str, str]]:
    if route not in TARGETS:
        raise RequestError("Unknown proof route.")
    if not isinstance(expected, dict) or not expected:
        raise RequestError("expectedSources must include the displayed proof and every local dependency.", 409)
    for name, value in expected.items():
        if not isinstance(name, str) or not FILENAME.fullmatch(name):
            raise RequestError("Only reviewed .lean filenames are accepted.", 409)
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            raise RequestError("Every source requires its exact SHA-256 hash.", 409)
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
        case = next(item for item in manifest["cases"] if item["id"] == route)
        recorded = {Path(item["path"]).name: item["sha256"] for item in case["sources"]}
        paths = proof_closure(route)
        actual = {path.name: sha256(path) for path in paths}
        original = {path.name: sha256(path if path.name == TARGETS[route] else ORIGINAL_ROOT / path.name)
                    for path in paths}
    except (OSError, ValueError, KeyError, StopIteration) as exc:
        raise RequestError(f"Reviewed proof material is unavailable: {exc}", 409) from exc
    if actual != recorded or actual != original:
        raise RequestError("Reviewed copies, manifest, and original proof sources differ. Refresh the report material before running.", 409)
    if expected != actual:
        raise RequestError("Displayed source hashes differ from the actual import closure. Refresh Report.html before running.", 409)
    target_code = checker_module.visible_code(paths[-1].read_text(encoding="utf-8-sig"))
    for declaration in ENDPOINTS[route]:
        short = declaration.rsplit(".", 1)[-1]
        if not re.search(r"^\s*#print\s+axioms\s+(?:" + re.escape(short) + "|" + re.escape(declaration) + r")\s*$", target_code, re.M):
            raise RequestError(f"Missing endpoint axiom inspection: {declaration}", 409)
    return paths, actual


def terminate_tree(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    if os.name == "nt":
        # A fixed native command, with the child's integer PID, also terminates Lean.
        subprocess.run(["taskkill.exe", "/PID", str(proc.pid), "/T", "/F"],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       creationflags=subprocess.CREATE_NO_WINDOW, timeout=20, check=False)
    else:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def axiom_evidence(log: str, declarations: list[str]) -> dict[str, list[str]]:
    found = {}
    for match in re.finditer(r"'([^'\n]+)' depends on axioms:\s*\[([^\]]*)\]", log):
        axioms = [part.strip() for part in match.group(2).split(",") if part.strip()]
        if set(axioms) - ALLOWED_AXIOMS:
            raise RuntimeError(f"Unexpected axioms in {match.group(1)}: {axioms}")
        found[match.group(1)] = axioms
    for match in re.finditer(r"'([^'\n]+)' does not depend on any axioms", log):
        found[match.group(1)] = []
    missing = [name for name in declarations if name not in found]
    if missing:
        raise RuntimeError("Endpoint axiom evidence missing: " + ", ".join(missing))
    return {name: found[name] for name in declarations}


def raw_compiler_run(command, *, cwd, env, timeout, on_output, input_text=None,
                     kill_command_run=subprocess.run):
    """Read compiler stdout/stderr directly while preserving its exit status."""
    flags = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW}
             if os.name == "nt" else {"start_new_session": True})
    proc = subprocess.Popen(command, cwd=cwd, env=env,
                            stdin=subprocess.PIPE if input_text is not None else subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding="utf-8", errors="replace", bufsize=1, **flags)
    expired = threading.Event()

    def expire() -> None:
        if proc.poll() is not None:
            return
        expired.set()
        if os.name == "nt":
            kill_command_run(["taskkill.exe", "/PID", str(proc.pid), "/T", "/F"],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             creationflags=subprocess.CREATE_NO_WINDOW, timeout=20, check=False)
        else:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass

    timer = threading.Timer(timeout, expire)
    timer.daemon = True
    timer.start()
    chunks = []
    try:
        if input_text is not None:
            proc.stdin.write(input_text)
            proc.stdin.close()
        assert proc.stdout
        for text in proc.stdout:
            chunks.append(text)
            on_output(text)
        code = proc.wait()
        text = "".join(chunks)
        if expired.is_set():
            raise subprocess.TimeoutExpired(command, timeout, output=text)
        return subprocess.CompletedProcess(command, code, stdout=text, stderr="")
    finally:
        timer.cancel()
        if proc.poll() is None:
            expire()
            proc.wait(timeout=25)


def stream_library_check(route: str) -> int:
    """Run the unchanged shared checker with a separate raw compiler channel.

    The trusted checker still chooses and audits its import closure and writes
    the standard result.json. Only its subprocess transport is replaced: Lean's
    stdout/stderr are read directly, not extracted from checker summary text.
    This fixed internal child mode is never an HTTP execution endpoint.
    """
    transport = sys.stdout
    original_run = subprocess.run
    config = json.loads(RUNTIME_CONFIG.read_text(encoding="utf-8-sig"))
    compiler = Path(config["lean_exe"]).resolve()
    allowed_sources = {path.resolve() for path in proof_closure(route)
                       if path.name != TARGETS[route]}

    def frame(channel: str, text: str) -> None:
        # ASCII framing avoids Windows pipe locale conversions; JSON decoding
        # restores every Unicode character in Lean's actual output unchanged.
        transport.write(json.dumps({"channel": channel, "text": text}, ensure_ascii=True) + "\n")
        transport.flush()

    class AuditWriter:
        def write(self, text: str) -> int:
            if text:
                frame("audit", text)
            return len(text)

        def flush(self) -> None:
            transport.flush()

    def compiler_run(command, **options):
        if (len(command) != 6 or Path(command[0]).resolve() != compiler or
                command[1] != "-R" or Path(command[2]).resolve() != PROOF_ROOT.resolve() or
                command[3] != "-o" or
                not Path(command[4]).resolve().is_relative_to((PROOF_ROOT / ".lean-runs").resolve()) or
                Path(command[5]).resolve() not in allowed_sources):
            raise RuntimeError("Unexpected compiler command in the fixed library checker.")
        return raw_compiler_run(command, cwd=options["cwd"], env=options["env"],
                                timeout=options["timeout"], on_output=lambda text: frame("compiler", text),
                                kill_command_run=original_run)

    previous_argv = sys.argv
    try:
        checker_module.subprocess.run = compiler_run
        sys.argv = [str(CHECKER), "--file", str(PROOF_ROOT / (PROOF_MODULES[route] + ".lean")),
                    "--root", str(PROOF_ROOT), "--timeout", "180"]
        with contextlib.redirect_stdout(AuditWriter()), contextlib.redirect_stderr(AuditWriter()):
            try:
                return checker_module.main()
            except Exception as exc:
                print(str(exc), file=sys.stderr)
                return 2
    finally:
        checker_module.subprocess.run = original_run
        sys.argv = previous_argv


class State:
    def __init__(self, port: int, idle_seconds: float = 180):
        self.port = port
        self.lock = threading.RLock()
        self.jobs: dict[str, dict] = {}
        self.processes: dict[str, subprocess.Popen] = {}
        self.stop_token = secrets.token_urlsafe(32)
        self.stopping = False
        self.idle_seconds = idle_seconds
        self.last_activity = time.monotonic()
        self.proof_finished = None
        self.page_leases: dict[str, float] = {}
        self.steps = StepwiseLean(self, sys.modules[__name__])
        config = json.loads(RUNTIME_CONFIG.read_text(encoding="utf-8-sig"))
        flags = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
        version_result = subprocess.run([config["lean_exe"], "--version"], capture_output=True,
                                        text=True, encoding="utf-8", errors="replace", timeout=15, **flags)
        self.lean_version = version_result.stdout.strip() if version_result.returncode == 0 else "unavailable"
        self.toolchain, self.mathlib_commit = config["toolchain"], config["mathlib_commit"]

    def snapshot(self, job: dict) -> dict:
        value = dict(job)
        if value["status"] == "running":
            value["elapsedSeconds"] = round(time.monotonic() - job["_started"], 3)
        return {key: item for key, item in value.items() if not key.startswith("_")}

    def save(self, job: dict) -> None:
        atomic_json(JOBS_DIR / job["jobId"] / "job.json", self.snapshot(job))

    def lookup(self, job_id: str) -> dict:
        with self.lock:
            if job_id in self.jobs:
                return self.snapshot(self.jobs[job_id])
            path = JOBS_DIR / job_id / "job.json"
            if not path.is_file():
                raise RequestError("Unknown Lean job.", 404)
            value = json.loads(path.read_text(encoding="utf-8"))
            if value["status"] == "running":
                value["status"] = "error"
                value["error"] = "The service stopped before this job completed. Run again."
            return value

    def create(self, route: str, expected: object, stage: str, session_id: object, cell_hash: object = None) -> dict:
        with self.lock:
            if self.stopping:
                raise RequestError("The report service is stopping.", 503)
            if any(job["status"] == "running" for job in self.jobs.values()):
                raise RequestError("A Lean proof is already running. Wait or cancel that run.", 409)
            paths, hashes = audit_sources(route, expected)
            if stage not in {"import", "start", "endpoint"}:
                raise RequestError("Unknown Lean cell stage.")
            _, cell = self.steps.audit_cell(route, stage)
            if cell_hash != cell["sha256"]:
                raise RequestError("Displayed Lean cell hash differs from the actual cell. Refresh Report.html.", 409)
            session_id = self.steps.prepare(route, stage, session_id, hashes)
            job_id = uuid.uuid4().hex
            job = dict(jobId=job_id, route=route, stage=stage, sessionId=session_id,
                       completedStages=list(self.steps.sessions[session_id]["completedStages"]),
                       status="running", log="", compilerOutput="",
                       elapsedSeconds=0, sourceHashes=hashes, returncode=None,
                       axioms={}, runResult=None, resultPath=None, error=None,
                       startedAt=dt.datetime.now(dt.timezone.utc).isoformat(),
                       _started=time.monotonic(), _cancel=False)
            self.jobs[job_id] = job
            self.last_activity = time.monotonic()
            self.save(job)
            if stage == "import":
                threading.Thread(target=self.run, args=(job, paths), daemon=True).start()
            else:
                threading.Thread(target=self.steps.run, args=(job,), daemon=True).start()
            return {"jobId": job_id, "status": "running", "sessionId": session_id, "stage": stage}

    def cancel(self, job_id: str) -> dict:
        with self.lock:
            job = self.jobs.get(job_id)
            if not job:
                return self.lookup(job_id)
            if job["status"] != "running":
                return self.snapshot(job)
            job["_cancel"] = True
            proc = self.processes.get(job_id)
        if proc is not None:
            terminate_tree(proc)
        # The runner records cancelled after reading the child's final output.
        return self.lookup(job_id)

    def run(self, job: dict, paths: list[Path]) -> None:
        proc = None
        timeout = None
        timed_out = threading.Event()
        try:
            # The import stage builds declarations and proofs, without running
            # the report's endpoint examples; those are a separate later cell.
            library_target = PROOF_ROOT / (PROOF_MODULES[job["route"]] + ".lean")
            library_paths = [path for path in paths if path.name != TARGETS[job["route"]]]
            library_hashes = {path.name: job["sourceHashes"][path.name] for path in library_paths}
            command = [sys.executable, "-u", str(Path(__file__).resolve()),
                       "--check-library-stream", job["route"]]
            flags = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {"start_new_session": True}
            proc = subprocess.Popen(command, cwd=WORKSPACE, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                                    errors="replace", bufsize=1, **flags)
            with self.lock:
                self.processes[job["jobId"]] = proc
                cancel_now = job["_cancel"]
            if cancel_now:
                terminate_tree(proc)

            def expire() -> None:
                timed_out.set()
                terminate_tree(proc)

            timeout = threading.Timer(MAX_WALL_SECONDS, expire)
            timeout.daemon = True
            timeout.start()
            last_save = time.monotonic()
            assert proc.stdout
            for line in proc.stdout:
                message = json.loads(line)
                if (set(message) != {"channel", "text"} or
                        message["channel"] not in {"audit", "compiler"} or
                        not isinstance(message["text"], str)):
                    raise RuntimeError("Invalid fixed-checker output frame.")
                field = "compilerOutput" if message["channel"] == "compiler" else "log"
                with self.lock:
                    if len(job[field]) + len(message["text"]) > MAX_LOG:
                        raise RuntimeError("Compiler log exceeded the report service limit.")
                    job[field] += message["text"]
                    if time.monotonic() - last_save >= 1:
                        self.save(job)
                        last_save = time.monotonic()
            returncode = proc.wait()
            with self.lock:
                job["returncode"] = returncode
            match = re.findall(r"^REPORT:\s*(.+?)\s*$", job["log"], re.M)
            run_result = None
            if match:
                result_path = Path(match[-1]).resolve(strict=True)
                if not result_path.is_relative_to((PROOF_ROOT / ".lean-runs").resolve()) or result_path.name != "result.json":
                    raise RuntimeError("Checker result path is outside its fixed run directory.")
                run_result = json.loads(result_path.read_text(encoding="utf-8"))
                with self.lock:
                    job["resultPath"], job["runResult"] = str(result_path), run_result
            if job["_cancel"]:
                with self.lock:
                    job["status"] = "cancelled"
                    job["error"] = "Run cancelled. No successful result is claimed."
                return
            if timed_out.is_set():
                raise RuntimeError("Lean run exceeded its total time limit.")
            if returncode != 0 or not run_result or run_result.get("status") != "PASSED":
                raise RuntimeError("The Lean checker did not return a fresh PASSED result.")
            if Path(run_result["target"]).resolve() != library_target.resolve() or Path(run_result["root"]).resolve() != PROOF_ROOT.resolve():
                raise RuntimeError("Checker target or proof root mismatch.")
            entries = run_result.get("files", [])
            result_hashes = {}
            for entry in entries:
                source = Path(entry["file"]).resolve()
                if source.parent != PROOF_ROOT.resolve() or not entry.get("passed") or entry.get("exit_code") != 0:
                    raise RuntimeError("A local proof module failed or escaped the fixed root.")
                result_hashes[source.name] = entry["sha256"]
            if len(entries) != len(library_hashes) or result_hashes != library_hashes:
                raise RuntimeError("Compiled source hashes do not match the displayed proof closure.")
            audit_sources(job["route"], job["sourceHashes"])
            # Audit library endpoints, then actually load that library in the
            # displayed import cell before the import stage can become OK.
            axiom_evidence(job["log"], ENDPOINTS[job["route"]])
            self.steps.import_checked(job, run_result)
            with self.lock:
                if job["_cancel"] or not self.steps.sessions[job["sessionId"]]["active"]:
                    raise RuntimeError("Lean cell cancelled or reset before completion.")
                job["status"] = "ok"
        except Exception as exc:
            if proc is not None and proc.poll() is None:
                terminate_tree(proc)
                proc.wait(timeout=25)
            with self.lock:
                job["status"] = "cancelled" if job["_cancel"] else "error"
                job["error"] = str(exc)
                if proc is not None:
                    job["returncode"] = proc.poll()
        finally:
            if timeout:
                timeout.cancel()
            with self.lock:
                job["elapsedSeconds"] = round(time.monotonic() - job["_started"], 3)
                self.processes.pop(job["jobId"], None)
                self.last_activity = time.monotonic()
                self.proof_finished = self.last_activity
                self.save(job)

    def lease(self, action: str, page_id: str) -> dict:
        if action not in {"open", "heartbeat", "close"}:
            raise RequestError("Unknown page session action.")
        if not isinstance(page_id, str) or not re.fullmatch(r"[0-9a-fA-F-]{32,36}", page_id):
            raise RequestError("A pageId generated for this browser page is required.")
        with self.lock:
            if self.stopping:
                raise RequestError("The report service is stopping.", 503)
            self.last_activity = time.monotonic()
            if action == "close":
                self.page_leases.pop(page_id, None)
            else:
                self.page_leases[page_id] = self.last_activity
        return dict(status="closed" if action == "close" else "active", pageId=page_id)

    def watch_idle(self, server: ThreadingHTTPServer) -> None:
        while not self.stopping:
            time.sleep(min(2, self.idle_seconds / 3))
            with self.lock:
                now = time.monotonic()
                active_pages = any(now - seen < 50 for seen in self.page_leases.values())
                active_jobs = any(job["status"] == "running" for job in self.jobs.values())
                grace = min(self.idle_seconds, 120) if self.proof_finished is not None else self.idle_seconds
                if active_pages or active_jobs or now - self.last_activity < grace:
                    continue
                self.stopping = True
            self.stop(server)
            return

    def stop(self, server: ThreadingHTTPServer) -> None:
        with self.lock:
            self.stopping = True
            running = [job_id for job_id, job in self.jobs.items() if job["status"] == "running"]
        for job_id in running:
            self.cancel(job_id)
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            with self.lock:
                if not any(job["status"] == "running" for job in self.jobs.values()):
                    break
            time.sleep(0.1)
        server.shutdown()


class ReportHTTPServer(ThreadingHTTPServer):
    # Windows SO_REUSEADDR can admit a second live listener on this address.
    # Bind must fail before any new process can replace the owner's state file.
    allow_reuse_address = os.name != "nt"


class Handler(BaseHTTPRequestHandler):
    server_version = "ACAReport/" + VERSION
    protocol_version = "HTTP/1.1"

    def setup(self) -> None:
        super().setup()
        self.connection.settimeout(15)

    @property
    def state(self) -> State:
        return self.server.state

    def log_message(self, message: str, *args) -> None:
        print(f"{self.log_date_time_string()} {self.address_string()} {message % args}", flush=True)

    def guard(self, write: bool = False) -> None:
        if self.client_address[0] != "127.0.0.1":
            raise RequestError("Loopback access only.", 403)
        host = self.headers.get("Host", "")
        allowed = {f"127.0.0.1:{self.state.port}", f"localhost:{self.state.port}"}
        if host not in allowed:
            raise RequestError("Unexpected Host header.", 403)
        origin = self.headers.get("Origin")
        if origin is not None and origin != "http://" + host:
            raise RequestError("Cross-origin access is prohibited.", 403)
        if write and origin != "http://" + host:
            raise RequestError("A same-origin request is required.", 403)
        if self.headers.get("Sec-Fetch-Site", "same-origin") not in {"same-origin", "none"}:
            raise RequestError("Cross-site access is prohibited.", 403)
        if "?" in self.path or "#" in self.path or "%" in self.path:
            raise RequestError("Query strings and encoded paths are not accepted.", 404)

    def respond(self, status: int, content: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Connection", "close")
        self.end_headers()
        self.close_connection = True
        if content:
            self.wfile.write(content)

    def json(self, status: int, value: dict) -> None:
        self.respond(status, json.dumps(value, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def body(self) -> dict:
        if self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
            raise RequestError("Content-Type must be application/json.", 415)
        if self.headers.get("Transfer-Encoding"):
            raise RequestError("Chunked request bodies are not accepted.", 400)
        try:
            length = int(self.headers.get("Content-Length", ""))
        except ValueError as exc:
            raise RequestError("A valid Content-Length is required.", 411) from exc
        if not 0 <= length <= MAX_BODY:
            raise RequestError("Request body is too large.", 413)
        try:
            raw = self.rfile.read(length)
            if len(raw) != length:
                raise ValueError("Incomplete request body")
            value = json.loads(raw)
        except (ValueError, UnicodeDecodeError) as exc:
            raise RequestError("Request body must be valid JSON.") from exc
        if not isinstance(value, dict):
            raise RequestError("JSON object required.")
        return value

    def do_GET(self) -> None:
        try:
            self.guard()
            if self.path in {"/", "/Report.html"}:
                with self.state.lock:
                    self.state.last_activity = time.monotonic()
                self.respond(200, REPORT.read_bytes(), "text/html; charset=utf-8")
            elif self.path in {"/report/dlw_error_theory.html", "/dlw_error_theory.html"}:
                self.respond(200, (WORKSPACE / "report" / "dlw_error_theory.html").read_bytes(), "text/html; charset=utf-8")
            elif self.path == "/favicon.ico":
                self.respond(204, b"", "image/x-icon")
            elif self.path == "/api/health":
                self.json(200, dict(service=SERVICE, version=VERSION, leanVersion=self.state.lean_version,
                                    toolchain=self.state.toolchain, mathlibCommit=self.state.mathlib_commit,
                                    pid=os.getpid(), port=self.state.port,
                                    workspace=str(WORKSPACE), script=str(Path(__file__).resolve()),
                                    activeJobs=sum(job["status"] == "running" for job in self.state.jobs.values()),
                                    status="stopping" if self.state.stopping else "ready"))
            elif self.path == "/api/lean/cells":
                self.json(200, self.state.steps.manifest)
            elif re.fullmatch(r"/api/lean/[0-9a-f]{32}", self.path):
                self.json(200, self.state.lookup(self.path.rsplit("/", 1)[-1]))
            else:
                raise RequestError("Unknown report resource.", 404)
        except RequestError as exc:
            self.json(exc.status, {"error": exc.message})
        except OSError as exc:
            self.json(503, {"error": f"Report resource unavailable: {exc}"})

    def do_POST(self) -> None:
        try:
            self.guard(write=True)
            body = self.body()
            if self.path == "/api/lean":
                if set(body) != {"route", "stage", "sessionId", "expectedSources", "expectedCellHash"} or not isinstance(body.get("route"), str) or not isinstance(body.get("stage"), str):
                    raise RequestError("Only route, stage, sessionId, expectedSources and expectedCellHash are accepted.")
                self.json(202, self.state.create(body["route"], body["expectedSources"], body["stage"], body["sessionId"], body["expectedCellHash"]))
            elif self.path == "/api/lean/reset":
                if set(body) != {"route", "sessionId"}:
                    raise RequestError("Reset requires route and sessionId.")
                self.json(200, self.state.steps.reset(body["route"], body["sessionId"]))
            elif self.path == "/api/session":
                if set(body) != {"action", "pageId"}:
                    raise RequestError("Page session requires action and pageId.")
                self.json(200, self.state.lease(body["action"], body["pageId"]))
            elif re.fullmatch(r"/api/lean/[0-9a-f]{32}/cancel", self.path):
                if body:
                    raise RequestError("Cancellation takes an empty JSON object.")
                self.json(200, self.state.cancel(self.path.split("/")[3]))
            elif self.path == "/api/stop":
                token = body.get("token")
                if set(body) not in ({"token"}, {"token", "idleOnly"}) or not isinstance(token, str) or not secrets.compare_digest(token, self.state.stop_token):
                    raise RequestError("Invalid local stop token.", 403)
                if "idleOnly" in body and body["idleOnly"] is not True:
                    raise RequestError("idleOnly must be true when supplied.")
                with self.state.lock:
                    if body.get("idleOnly") and any(job["status"] == "running" for job in self.state.jobs.values()):
                        raise RequestError("A Lean cell is running. Finish or cancel it before restarting.", 409)
                    self.state.stopping = True
                self.json(200, {"status": "stopping"})
                threading.Thread(target=self.state.stop, args=(self.server,), daemon=True).start()
            else:
                raise RequestError("Unknown report action.", 404)
        except RequestError as exc:
            self.json(exc.status, {"error": exc.message})
        except (OSError, ValueError) as exc:
            self.json(500, {"error": str(exc)})

    def do_OPTIONS(self) -> None:
        self.json(403, {"error": "Cross-origin preflight is not supported."})

    def do_PUT(self) -> None:
        self.json(405, {"error": "Method not allowed."})

    do_DELETE = do_PATCH = do_HEAD = do_PUT


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--idle-seconds", type=float, default=180)
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error("Use a non-privileged port.")
    if args.idle_seconds < 1:
        parser.error("Idle timeout must be at least one second.")
    global PID_FILE
    if args.port != 8766:
        PID_FILE = HERE / f"server-state-{args.port}.json"
    state = State(args.port, args.idle_seconds)
    server = ReportHTTPServer(("127.0.0.1", args.port), Handler)
    server.daemon_threads = True
    server.state = state
    atomic_json(PID_FILE, dict(service=SERVICE, version=VERSION, pid=os.getpid(),
                              python=sys.executable, script=str(Path(__file__).resolve()),
                              workspace=str(WORKSPACE),
                              port=args.port, token=state.stop_token, status="running"))
    threading.Thread(target=state.watch_idle, args=(server,), daemon=True).start()
    print(f"{SERVICE} {VERSION} http://127.0.0.1:{args.port}/Report.html", flush=True)
    try:
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        with state.lock:
            running = [job_id for job_id, job in state.jobs.items() if job["status"] == "running"]
        for job_id in running:
            state.cancel(job_id)
    finally:
        server.server_close()
        atomic_json(PID_FILE, dict(service=SERVICE, version=VERSION, pid=os.getpid(), port=args.port, status="stopped"))
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--check-library-stream" and sys.argv[2] in PROOF_MODULES:
        sys.exit(stream_library_check(sys.argv[2]))
    sys.exit(main())
