"""Authenticated Colab local runtime using this project's Python and Lean.

Official connection instructions:
https://research.google.com/colaboratory/local-runtimes.html
ServerApp.allow_origin/allow_credentials are the modern Jupyter Server
equivalents of the official NotebookApp flags. No legacy transport extension.
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.metadata
import json
import logging
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

PROJECT = Path(__file__).resolve().parent
PYTHON = PROJECT / ".venv" / "Scripts" / "python.exe"
PYTHONW = PROJECT / ".venv" / "Scripts" / "pythonw.exe"
PRIVATE = PROJECT / ".local_runtime"
STATE = PRIVATE / "connection.json"
CONNECTION = PRIVATE / "Colab连接地址.txt"
ORIGIN = "https://colab.research.google.com"
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def secure_directory() -> None:
    PRIVATE.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        account = os.environ["USERDOMAIN"] + "\\" + os.environ["USERNAME"]
        result = subprocess.run(
            ["icacls", str(PRIVATE), "/inheritance:r", "/grant:r",
             account + ":(OI)(CI)F", "*S-1-5-18:(OI)(CI)F"],
            capture_output=True, text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        if result.returncode:
            raise RuntimeError("Cannot restrict the local connection directory permissions.")
    else:
        PRIVATE.chmod(0o700)


def read_state() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8"))


def api(path: str, state: dict, method="GET", body=None, authenticated=True,
        origin=ORIGIN):
    headers = {"Origin": origin}
    if authenticated:
        headers["Authorization"] = "token " + state["token"]
    if body is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(body).encode()
    request = urllib.request.Request(state["base_url"] + path, data=body,
                                     method=method, headers=headers)
    return OPENER.open(request, timeout=8)


def healthy(state: dict) -> bool:
    try:
        with api("/api/status", state) as response:
            return response.status == 200
    except (OSError, KeyError, urllib.error.URLError):
        return False


def public_state(state: dict) -> dict:
    return {"running": healthy(state), "host": "127.0.0.1",
            "port": state["port"], "pid": state.get("pid"),
            "kernel": "python3", "python": str(PYTHON),
            "root_dir": str(PROJECT), "connection_file": str(CONNECTION)}


def start() -> dict:
    secure_directory()
    if STATE.exists():
        previous = read_state()
        if healthy(previous):
            return previous
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    token = secrets.token_urlsafe(36)
    state = {"host": "127.0.0.1", "port": port, "token": token,
             "base_url": f"http://127.0.0.1:{port}",
             "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
             "python": str(PYTHON), "root_dir": str(PROJECT)}
    STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    CONNECTION.write_text(state["base_url"] + "/?token=" + token + "\n",
                          encoding="utf-8")
    for name in ("config", "runtime", "data", "data/kernels/python3"):
        (PRIVATE / name).mkdir(parents=True, exist_ok=True)
    kernel = {"argv": [str(PYTHON), "-m", "ipykernel_launcher", "-f",
                       "{connection_file}"], "display_name": "Report 本地 Python",
              "language": "python", "metadata": {"debugger": True}}
    (PRIVATE / "data/kernels/python3/kernel.json").write_text(
        json.dumps(kernel, ensure_ascii=False, indent=2), encoding="utf-8")
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    executable = PYTHONW if os.name == "nt" else PYTHON
    with (PRIVATE / "server.log").open("a", encoding="utf-8") as log:
        process = subprocess.Popen([str(executable), str(Path(__file__)), "serve"],
                                   cwd=PROJECT, stdout=log, stderr=log,
                                   creationflags=flags)
    state["pid"] = process.pid
    STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if healthy(state):
            return state
        if process.poll() is not None:
            raise RuntimeError("The local runtime did not start; see .local_runtime/server.log.")
        time.sleep(0.2)
    raise RuntimeError("The local runtime is still starting; reopen this launcher shortly.")


def serve() -> None:
    state = read_state()
    os.environ["JUPYTER_CONFIG_DIR"] = str(PRIVATE / "config")
    os.environ["JUPYTER_DATA_DIR"] = str(PRIVATE / "data")
    os.environ["JUPYTER_RUNTIME_DIR"] = str(PRIVATE / "runtime")
    from traitlets.config import Config
    from jupyter_server.serverapp import ServerApp

    config = Config()
    config.ServerApp.ip = "127.0.0.1"
    config.ServerApp.port = state["port"]
    config.ServerApp.port_retries = 0
    config.ServerApp.root_dir = str(PROJECT)
    config.ServerApp.open_browser = False
    config.ServerApp.use_redirect_file = False
    config.ServerApp.allow_origin = ORIGIN
    config.ServerApp.allow_credentials = True
    config.ServerApp.disable_check_xsrf = False
    config.ServerApp.terminals_enabled = False
    config.ServerApp.jpserver_extensions = {}
    config.ServerApp.log_level = logging.WARNING
    config.IdentityProvider.token = state["token"]
    config.MappingKernelManager.default_kernel_name = "python3"
    app = ServerApp.instance(config=config)
    app.initialize([])
    # Jupyter initializes a new manager; kernel_dirs is an instance trait,
    # not a configuration-file option. Set it before the server starts.
    app.kernel_spec_manager.kernel_dirs = [str(PRIVATE / "data/kernels")]
    app.kernel_spec_manager.allowed_kernelspecs = {"python3"}
    app.kernel_spec_manager.ensure_native_kernel = False
    app.start()


def show_ui() -> None:
    import tkinter as tk
    from tkinter import messagebox
    window = tk.Tk()
    window.title("Colab 本地运行时")
    window.withdraw()
    try:
        start()
        url = CONNECTION.read_text(encoding="utf-8").strip()
    except Exception as error:
        messagebox.showerror("运行时未启动", str(error), parent=window)
        window.destroy()
        return
    window.deiconify()
    window.resizable(False, False)
    tk.Label(window, text="在 Colab 选择“连接到本地运行时”，粘贴下方地址。",
             padx=18, pady=12).pack()
    value = tk.StringVar(value=url)
    entry = tk.Entry(window, textvariable=value, width=88, state="readonly")
    entry.pack(padx=18)

    def copy():
        window.clipboard_clear()
        window.clipboard_append(url)
        window.update()
        label.configure(text="连接地址已复制；报告使用本机 Python、Lean 和 Mathlib。")

    tk.Button(window, text="复制连接地址", command=copy, padx=15).pack(pady=12)
    label = tk.Label(window, text="报告使用本机 Python、Lean 和 Mathlib。", padx=18)
    label.pack()
    tk.Label(window, text="关闭此窗口后，本地运行时继续运行。", padx=18, pady=12).pack()
    window.mainloop()


def validate() -> dict:
    """Exercise authenticated HTTP and real kernel execution, without exposing tokens."""
    import websocket
    state = start()
    record = {"checked_at": dt.datetime.now(dt.timezone.utc).isoformat(),
              "official_docs": "https://research.google.com/colaboratory/local-runtimes.html",
              "jupyter_server": importlib.metadata.version("jupyter_server"),
              "server": public_state(state), "browser_connected": False}
    try:
        with api("/api/status", state, authenticated=False) as response:
            record["unauthenticated_http_status"] = response.status
    except urllib.error.HTTPError as error:
        record["unauthenticated_http_status"] = error.code
    with api("/api/status", state) as response:
        record["authenticated_http_status"] = response.status
        record["cors_origin"] = response.headers.get("Access-Control-Allow-Origin")
        record["cors_credentials"] = response.headers.get("Access-Control-Allow-Credentials")
    with api("/api/kernelspecs", state) as response:
        record["kernelspecs"] = json.load(response)
    with api("/api/kernels", state, method="POST", body={"name": "python3"}) as response:
        kernel_id = json.load(response)["id"]
    session_id = uuid.uuid4().hex
    ws_url = state["base_url"].replace("http://", "ws://") + "/api/kernels/" + kernel_id
    ws_url += "/channels?session_id=" + session_id
    channel = websocket.create_connection(ws_url, timeout=50, origin=ORIGIN,
                    header=["Authorization: token " + state["token"]],
                    http_proxy_host=None)
    msg_id = uuid.uuid4().hex
    code = '''import json, os, subprocess, sys
from pathlib import Path
import numpy, pandas, matplotlib
project = Path.cwd()
runtime = json.loads((project.parents[1] / "_lean_shared/runtime.json").read_text(encoding="utf-8"))
source = project / ".local_runtime/LeanRuntimeSmoke.lean"
source.write_text("import Mathlib.Basic.Real.Basic\\n#check Real\\nexample (x : ℝ) : x = x := rfl\\n", encoding="utf-8")
environment = dict(os.environ)
environment["LEAN_PATH"] = os.pathsep.join(runtime["lean_paths"])
version = subprocess.run([runtime["lean_exe"], "--version"], capture_output=True, text=True, timeout=30)
compiled = subprocess.run([runtime["lean_exe"], str(source)], cwd=project, env=environment, capture_output=True, text=True, encoding="utf-8", timeout=90)
print("LOCAL_RUNTIME_RESULT=" + json.dumps({"python": sys.executable, "cwd": str(project), "numpy": numpy.__version__, "pandas": pandas.__version__, "matplotlib": matplotlib.__version__, "lean_exe": runtime["lean_exe"], "lean_version": version.stdout.strip(), "lean_returncode": compiled.returncode, "lean_stdout": compiled.stdout, "lean_stderr": compiled.stderr}, ensure_ascii=True))
'''
    message = {"header": {"msg_id": msg_id, "username": "local-validation",
                           "session": session_id, "msg_type": "execute_request",
                           "version": "5.3", "date": dt.datetime.now(dt.timezone.utc).isoformat()},
               "parent_header": {}, "metadata": {}, "channel": "shell", "buffers": [],
               "content": {"code": code, "silent": False, "store_history": False,
                           "user_expressions": {}, "allow_stdin": False,
                           "stop_on_error": True}}
    outputs = []
    try:
        channel.send(json.dumps(message))
        deadline = time.monotonic() + 130
        finished = False
        while time.monotonic() < deadline:
            incoming = json.loads(channel.recv())
            if incoming.get("parent_header", {}).get("msg_id") != msg_id:
                continue
            msg_type = incoming.get("msg_type", incoming.get("header", {}).get("msg_type"))
            if msg_type == "stream":
                outputs.append(incoming["content"]["text"])
            elif msg_type == "error":
                record["kernel_error"] = incoming["content"]
            elif msg_type == "execute_reply":
                record["execution_status"] = incoming["content"]["status"]
            elif msg_type == "status" and incoming["content"]["execution_state"] == "idle":
                finished = True
                break
        record["websocket_execution_completed"] = finished
        for line in "".join(outputs).splitlines():
            if line.startswith("LOCAL_RUNTIME_RESULT="):
                record["kernel_result"] = json.loads(line.split("=", 1)[1])
    finally:
        channel.close()
        # Shutdown removes only Jupyter's ephemeral process resources, not workspace files.
        with api("/api/kernels/" + kernel_id, state, method="DELETE"):
            pass
    result = record.get("kernel_result", {})
    record["passed"] = all((record["authenticated_http_status"] == 200,
        record["unauthenticated_http_status"] in (401, 403),
        record["cors_origin"] == ORIGIN, record["cors_credentials"] == "true",
        record.get("websocket_execution_completed"),
        record.get("execution_status") == "ok",
        Path(result.get("python", "")) == PYTHON,
        Path(result.get("cwd", "")) == PROJECT, result.get("lean_returncode") == 0))
    (PROJECT / "local_runtime_validation.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "serve", "ui", "status", "validate"],
                        nargs="?", default="ui")
    action = parser.parse_args().action
    if action == "serve":
        serve()
    elif action == "ui":
        show_ui()
    elif action == "validate":
        result = validate()
        print(json.dumps({"passed": result["passed"], "server": result["server"],
                          "validation_file": str(PROJECT / "local_runtime_validation.json")},
                         ensure_ascii=True))
        if not result["passed"]:
            raise SystemExit(1)
    else:
        state = start() if action == "start" else read_state()
        print(json.dumps(public_state(state), ensure_ascii=True))


if __name__ == "__main__":
    main()
