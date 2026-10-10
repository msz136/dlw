"""Execute the final local import adapter in a fresh native IPython kernel."""
import hashlib
import json
import sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

PROJECT = Path(__file__).resolve().parent
DELIVERY = PROJECT.parents[1] / "notebook" / "Report.ipynb"
source = nbformat.read(DELIVERY, as_version=4)
ids = ("runtime-prepare", "lean-uw-import", "lean-qrm-import")
cells = [nbformat.v4.new_code_cell(next(c.source for c in source.cells if c.id == key),id=key)
         for key in ids]
cells.append(nbformat.v4.new_code_cell('''import hashlib, json
print(json.dumps({
    "helper_sha256": hashlib.sha256((report_dir if "report_dir" in globals() else __import__("pathlib").Path("C:/Users/msz/aca/Workspaces/report_colab_20261006")).joinpath("lean_notebook.py").read_bytes()).hexdigest(),
    "history_count": len(lean_notebook_session.history),
    "all_compiled_sources_are_displayed_cells": all("cells" in __import__("pathlib").Path(item["source"]).parts for item in lean_notebook_session.history),
    "all_proof_cache_events_are_warm": all(item["origin"] == "warm_cache" for item in lean_notebook_session.cache_events),
    "proof_cache_events": len(lean_notebook_session.cache_events),
}))
''',id="measure-local-import"))
notebook = nbformat.v4.new_notebook(cells=cells)
manager = KernelManager(kernel_name="python3")
manager.kernel_spec.argv = [sys.executable,"-m","ipykernel_launcher","-f","{connection_file}"]
NotebookClient(notebook,km=manager,timeout=120,startup_timeout=60,
               resources={"metadata":{"path":str(DELIVERY.parent)}},allow_errors=False).execute()
nbformat.write(notebook,PROJECT / "local_import_smoke.ipynb")
text = "".join(o.text for o in notebook.cells[-1].outputs if o.output_type=="stream")
result = json.loads(text)
assert result["history_count"] == 2
assert result["all_compiled_sources_are_displayed_cells"]
assert result["all_proof_cache_events_are_warm"]
result["passed"] = True
(PROJECT / "local_import_smoke_validation.json").write_bytes((json.dumps(result,indent=2)+"\n").encode())
print(json.dumps(result))
