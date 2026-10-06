"""Extract the seven native Python cells and check actual executions.

This script uses existing local dependencies and does not install anything.
"""
from contextlib import redirect_stdout, redirect_stderr
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
import re
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "report_notebook_20261002" / "step_material" / "hs_cells.json"
script = (HERE / "hs_cells.py").read_text(encoding="utf-8")
sections = re.split(r"^# %% ([^\n]+)\n", script, flags=re.MULTILINE)
sources = {sections[i]: sections[i + 1].strip() + "\n"
           for i in range(1, len(sections), 2) if sections[i] != "[markdown]"}
cells = []
for old in json.loads(OLD.read_text(encoding="utf-8")):
    source = sources[old["id"]]
    cells.append({"id": old["id"], "title": old["title"], "lead": old["lead"],
                  "requires": old["requires"], "source": source})
(HERE / "hs_cells.json").write_text(json.dumps(cells, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
assert len(cells) == 7

def execute_all(edit=None):
    namespace = {"__name__": "__main__"}
    trace = []
    for index, cell in enumerate(cells):
        source = cell["source"]
        if edit and cell["id"] == "hs-config":
            source = source.replace(edit[0], edit[1])
        stdout, stderr = StringIO(), StringIO()
        begin = time.perf_counter()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exec(compile(source, f"<cell:{cell['id']}>", "exec"), namespace)
        trace.append({"id": cell["id"], "execution_count": index + 1,
                      "seconds": round(time.perf_counter() - begin, 6),
                      "stdout": stdout.getvalue(), "stderr": stderr.getvalue()})
    figures = []
    for fno in plt.get_fignums():
        fig = plt.figure(fno)
        figures.append({"lines": [len(ax.lines) for ax in fig.axes],
                        "xlabels": [ax.get_xlabel() for ax in fig.axes],
                        "ylabels": [ax.get_ylabel() for ax in fig.axes],
                        "finite_line_data": all(np.isfinite(line.get_ydata()).all()
                                                for ax in fig.axes for line in ax.lines)})
    plt.close("all")
    assert len(figures) == 2 and all(f["lines"] == [2] and f["finite_line_data"] for f in figures)
    return namespace, trace, figures

default, default_trace, default_figures = execute_all()
expected = {"Integrable": (0.010012749796509766, 0.0011496748742060303),
            "FD": (9.399310918062342e-7, 3.046420677166317e-6)}
default_values, differences = {}, {}
for name, target in expected.items():
    actual = default["hs_results"][name]
    default_values[name] = {k: float(actual[k]) for k in ("Eu", "Erho", "minDx", "minRho")}
    differences[name] = {"Eu": abs(float(actual["Eu"]) - target[0]),
                         "Erho": abs(float(actual["Erho"]) - target[1])}
assert max(v for item in differences.values() for v in item.values()) <= 1e-8
assert np.isfinite(default["hs_integrable"]).all() and np.isfinite(default["hs_fd"]).all()

edited, edited_trace, edited_figures = execute_all(("dt=0.003125, T=0.5,", "dt=0.003125, T=0.25,"))
edited_values = {name: {k: float(value[k]) for k in ("Eu", "Erho", "minDx", "minRho")}
                 for name, value in edited["hs_results"].items()}
assert edited["hs_steps"] == 80 and edited["hs_T"] == 0.25
assert all(edited_values[name]["Eu"] != default_values[name]["Eu"] for name in expected)
assert "hs_audit_rows" not in edited

missing = []
for cell_id in ("hs-reference", "hs-evolve", "hs-error"):
    cell = next(c for c in cells if c["id"] == cell_id)
    try:
        exec(compile(cell["source"], f"<cell:{cell_id}>", "exec"), {"__name__": "__main__"})
    except NameError as exc:
        missing.append({"cell": cell_id, "exception": type(exc).__name__, "message": str(exc)})
    else:
        raise AssertionError(f"{cell_id} must fail naturally without preceding cells")

record = {
    "status": "passed", "python": sys.version, "python_executable": sys.executable,
    "numpy": np.__version__, "pandas": pd.__version__, "matplotlib": matplotlib.__version__,
    "cell_count": len(cells),
    "source_sha256": {c["id"]: sha256(c["source"].encode()).hexdigest() for c in cells},
    "default": {"configuration": default["hs_cfg"], "results": default_values,
                "difference_from_report": differences, "tolerance": 1e-8,
                "sequential_execution": default_trace, "figures": default_figures},
    "edited_parameter": {"parameter": "T", "value": 0.25, "steps": 80,
                         "results": edited_values, "changed_actual_result": True,
                         "sequential_execution": edited_trace, "figures": edited_figures},
    "missing_preceding_cell": missing,
    "notes": "Sources are standard Python cells; figures and tables come from the current execution.",
}
(HERE / "hs_validation.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": record["status"], "default": default_values,
                  "differences": differences, "edited_T": edited_values,
                  "missing_dependencies": missing}, ensure_ascii=False, indent=2))
