"""Double-click to start the project-local runtime and copy its Colab URL."""
from pathlib import Path
import subprocess

project = Path(__file__).resolve().parent.parent / "Workspaces/report_colab_20261006"
subprocess.Popen([str(project / ".venv/Scripts/pythonw.exe"),
                  str(project / "local_runtime.py"), "ui"],
                 cwd=project, creationflags=subprocess.CREATE_NO_WINDOW)
