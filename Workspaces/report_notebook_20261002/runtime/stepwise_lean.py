"""Reviewed Lean notebook cells, with one fresh compilation per requested cell.

The import cell builds the complete theorem library once. Later cells import
that exact session's checked artifacts; source/artifact changes invalidate it.
No source sent by the browser is executed.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import threading
import time
import uuid

STAGES = ("import", "start", "endpoint")
PROOF_MODULES = {"uw": "ReportNonlinearUW", "qrm": "ReportNonlinearQRM"}
PREFIXES = {"uw": "StepUW", "qrm": "StepQRM"}
SESSION_ID = re.compile(r"[0-9a-f]{32}")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class StepwiseLean:
    def __init__(self, state, api):
        self.state, self.api = state, api
        self.root = api.PROJECT / "lean_material" / "steps"
        self.manifest_path = api.PROJECT / "lean_material" / "stage_manifest.json"
        self.manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        self.manifest_hash = digest(self.manifest_path)
        self.sessions = {}

    def audit_cell(self, route: str, stage: str) -> tuple[Path, dict]:
        if digest(self.manifest_path) != self.manifest_hash:
            raise self.api.RequestError("Lean cell material changed. Restart the report service.", 409)
        entry = self.manifest["cases"][route][stage]
        path = self.root / entry["filename"]
        if path.parent != self.root or digest(path) != entry["sha256"]:
            raise self.api.RequestError("The displayed Lean cell differs from its reviewed source.", 409)
        code = self.api.checker_module.visible_code(path.read_text(encoding="utf-8"))
        if re.search(r"\b(sorry|admit|axiom)\b", code):
            raise self.api.RequestError("Lean cell contains a placeholder or new axiom.", 409)
        return path, entry

    def prepare(self, route: str, stage: str, session_id: object, hashes: dict) -> str:
        if stage not in STAGES:
            raise self.api.RequestError("Unknown Lean cell stage.")
        for item in STAGES:
            self.audit_cell(route, item)
        if stage == "import":
            if session_id is not None:
                raise self.api.RequestError("Start a fresh import cell without a sessionId.", 409)
            session_id = uuid.uuid4().hex
            self.sessions[session_id] = dict(route=route, sourceHashes=hashes,
                                             completedStages=[], artifacts={}, active=True,
                                             runtimeHash=digest(self.api.RUNTIME_CONFIG))
            return session_id
        if not isinstance(session_id, str) or not SESSION_ID.fullmatch(session_id):
            raise self.api.RequestError("Run this route's import cell first.", 409)
        session = self.sessions.get(session_id)
        if not session or not session["active"] or session["route"] != route:
            raise self.api.RequestError("This Lean session is unavailable. Run import again.", 409)
        required = list(STAGES[:STAGES.index(stage)])
        if session["completedStages"][:len(required)] != required:
            raise self.api.RequestError("Run all preceding Lean cells first: " + ", ".join(required), 409)
        try:
            if session["sourceHashes"] != hashes or session["runtimeHash"] != digest(self.api.RUNTIME_CONFIG):
                raise ValueError("Lean sources or runtime changed.")
            for artifact, expected in session["artifacts"].items():
                if digest(Path(artifact)) != expected:
                    raise ValueError("An artifact from this session changed.")
        except (OSError, ValueError) as exc:
            session["active"] = False
            raise self.api.RequestError(str(exc) + " Run import again.", 409) from exc
        # Rerunning an earlier cell invalidates all downstream successes.
        session["completedStages"] = required
        return session_id

    def reset(self, route: str, session_id: object) -> dict:
        if route not in PROOF_MODULES:
            raise self.api.RequestError("Unknown proof route.")
        if not isinstance(session_id, str) or not SESSION_ID.fullmatch(session_id):
            raise self.api.RequestError("A valid sessionId is required.")
        with self.state.lock:
            session = self.sessions.get(session_id)
            if session and session["route"] != route:
                raise self.api.RequestError("Lean session belongs to another route.", 409)
            if session:
                session["active"] = False
                session["completedStages"] = []
            running = [job["jobId"] for job in self.state.jobs.values()
                       if job.get("sessionId") == session_id and job["status"] == "running"]
        for job_id in running:
            self.state.cancel(job_id)
        return dict(status="reset", route=route, sessionId=session_id, completedStages=[])

    def import_checked(self, job: dict, result: dict) -> None:
        """Called only after the standard checker freshly audited the library."""
        session = self.sessions[job["sessionId"]]
        session["library"] = str(Path(result["files"][-1]["artifact"]).parent)
        session["lib"] = str(self.api.JOBS_DIR / job["jobId"] / "lib" / "lean")
        session["libraryResultPath"] = job["resultPath"]
        for entry in result["files"]:
            artifact = Path(entry["artifact"])
            session["artifacts"][str(artifact)] = digest(artifact)
        self.compile_cell(job)

    def compile_cell(self, job: dict) -> None:
        state, api = self.state, self.api
        session = self.sessions[job["sessionId"]]
        if not session["active"] or job["_cancel"]:
            raise RuntimeError("Lean session was reset or the cell was cancelled.")
        path, entry = self.audit_cell(job["route"], job["stage"])
        config = json.loads(api.RUNTIME_CONFIG.read_text(encoding="utf-8-sig"))
        output = Path(session["lib"]) / path.with_suffix(".olean").name
        output.parent.mkdir(parents=True, exist_ok=True)
        env = os.environ.copy()
        env["LEAN_PATH"] = os.pathsep.join([session["lib"], session["library"]] + config["lean_paths"])
        command = [config["lean_exe"], "-R", str(self.root), "-o", str(output), str(path)]
        flags = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW}
                 if os.name == "nt" else {"start_new_session": True})
        proc = None
        timer = None
        expired = threading.Event()
        started = time.monotonic()
        cell_log = []
        try:
            with state.lock:
                job["log"] += f"CHECK CELL {path.name}\n"
                job["cellSourceHash"] = entry["sha256"]
                job["libraryResultPath"] = session["libraryResultPath"]
                state.save(job)
            proc = subprocess.Popen(command, cwd=self.root, env=env, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                                    errors="replace", bufsize=1, **flags)
            with state.lock:
                state.processes[job["jobId"]] = proc
                cancel_now = job["_cancel"]
            if cancel_now:
                api.terminate_tree(proc)
            def expire():
                expired.set()
                api.terminate_tree(proc)
            timer = threading.Timer(180, expire)
            timer.daemon = True
            timer.start()
            assert proc.stdout
            for line in proc.stdout:
                cell_log.append(line)
                with state.lock:
                    if len(job["log"]) + len(line) > api.MAX_LOG:
                        raise RuntimeError("Compiler log exceeded the report service limit.")
                    job["log"] += line
                    job["compilerOutput"] += line
                    state.save(job)
            code = proc.wait()
            job["returncode"] = code
            if job["_cancel"] or not session["active"]:
                raise RuntimeError("Lean cell cancelled. No successful result is claimed.")
            if expired.is_set():
                raise RuntimeError("Lean cell exceeded its time limit.")
            log = "".join(cell_log)
            if code != 0 or re.search(r"declaration uses ['`]?sorry", log) or not output.is_file():
                raise RuntimeError("The current Lean cell did not compile successfully.")
            api.audit_sources(job["route"], job["sourceHashes"])
            self.audit_cell(job["route"], job["stage"])
            for artifact, expected in session["artifacts"].items():
                if Path(artifact) != output and digest(Path(artifact)) != expected:
                    session["active"] = False
                    raise RuntimeError("A checked Lean dependency changed while this cell ran.")
            evidence = (api.axiom_evidence(log, api.ENDPOINTS[job["route"]])
                        if job["stage"] == "endpoint" else {})
            cell_result = dict(status="PASSED", route=job["route"], stage=job["stage"],
                               sessionId=job["sessionId"], source=str(path), sha256=entry["sha256"],
                               artifact=str(output), artifactSha256=digest(output),
                               exit_code=code, seconds=round(time.monotonic()-started, 3),
                               libraryResultPath=session["libraryResultPath"], axioms=evidence)
            result_path = api.JOBS_DIR / job["jobId"] / "cell-result.json"
            api.atomic_json(result_path, cell_result)
            with state.lock:
                session["artifacts"][str(output)] = cell_result["artifactSha256"]
                session["completedStages"] = list(STAGES[:STAGES.index(job["stage"])+1])
                job["completedStages"] = list(session["completedStages"])
                job["axioms"] = evidence
                job["cellResult"], job["cellResultPath"] = cell_result, str(result_path)
                job["log"] += f"PASSED CELL: {job['stage']}\n"
        finally:
            if timer:
                timer.cancel()
            if proc is not None and proc.poll() is None:
                api.terminate_tree(proc)
                proc.wait(timeout=25)
            with state.lock:
                state.processes.pop(job["jobId"], None)

    def run(self, job: dict) -> None:
        try:
            self.compile_cell(job)
            with self.state.lock:
                if job["_cancel"] or not self.sessions[job["sessionId"]]["active"]:
                    raise RuntimeError("Lean cell cancelled or reset before completion.")
                job["status"] = "ok"
        except Exception as exc:
            with self.state.lock:
                job["status"] = "cancelled" if job["_cancel"] else "error"
                job["error"] = str(exc)
        finally:
            with self.state.lock:
                job["elapsedSeconds"] = round(time.monotonic()-job["_started"], 3)
                self.state.last_activity = time.monotonic()
                self.state.proof_finished = self.state.last_activity
                self.state.save(job)
