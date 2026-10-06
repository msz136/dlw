"""Save and inspect the two public notebook sources; no runtime network dependency."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import urllib.request

HERE = Path(__file__).resolve().parent
entries = []
for name in ["01_reflected_inertia", "02_hardware_station_io"]:
    url = f"https://raw.githubusercontent.com/RussTedrake/manipulation/master/book/robot/exercises/{name}.ipynb"
    request = urllib.request.Request(url, headers={"User-Agent": "ACA-local-report-source-review/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read()
    destination = HERE / "refs" / (name + ".ipynb")
    destination.write_bytes(data)
    notebook = json.loads(data)
    cells = []
    for index, cell in enumerate(notebook["cells"]):
        source = "".join(cell.get("source", []))
        lines = [line for line in source.splitlines() if line.strip()]
        cells.append({"index": index, "type": cell["cell_type"], "lines": len(source.splitlines()),
                      "head": "\n".join(lines[:4]), "code": source if cell["cell_type"] == "code" else None})
    entries.append({"name": name, "url": url, "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(), "cells": cells})
    print(name, len(cells), "cells", flush=True)
    for cell in cells:
        print(f"{cell['index']:2d} {cell['type']:8s} {cell['lines']:3d} {cell['head'][:240]}")
(HERE / "refs" / "notebook_structure.json").write_text(json.dumps({
    "checkedAt": dt.datetime.now(dt.timezone.utc).isoformat(), "notebooks": entries
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
