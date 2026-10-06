"""Execute all visible DLW cells and compare with their original JS implementation."""
from pathlib import Path
import contextlib
import hashlib
import io
import json
import subprocess
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "report_notebook_20261002" / "step_material" / "cells.json"
CELLS = json.loads((HERE / "dlw_cells.json").read_text(encoding="utf-8"))
NODE = Path("C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe")
CHECKS = []


def check(name, details):
    CHECKS.append(dict(name=name, passed=True, details=details))


def run_cell(index, ns, transform=None):
    cell = CELLS[index]
    source = transform(cell["code"]) if transform else cell["code"]
    capture = io.StringIO()
    displays = []
    start = time.perf_counter()
    with contextlib.redirect_stdout(capture):
        exec(compile(source, cell["id"], "exec"), ns)
    # Replace IPython display after preparation, preserving the actual objects.
    if index == 0:
        ns["display"] = lambda obj: displays.append(obj)
    return capture.getvalue(), displays, time.perf_counter()-start


def run(config_transform=None, core_transform=None):
    ns, stdout, tables = {}, [], []
    figures = []
    for index in range(len(CELLS)):
        if index:
            ns["display"] = lambda obj: tables.append(obj.copy())
        text, _, elapsed = run_cell(index, ns,
            config_transform if index == 1 else core_transform if index == 4 else None)
        stdout.append(dict(id=CELLS[index]["id"], text=text, seconds=elapsed))
    for number in plt.get_fignums():
        fig = plt.figure(number)
        figures.append(dict(lines=len(fig.axes[0].lines),
                            title=fig.axes[0].get_title()))
    plt.close("all")
    return ns["dlw"], stdout, tables, figures, ns


def original(parameter_b=False):
    js = r'''
const fs = require('fs');
const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
(async () => {
  const cells=JSON.parse(fs.readFileSync(process.argv[1],'utf8'));
  const lab={}, output=[];
  for(const cell of cells) {
    let code=cell.code;
    if(process.argv[2]==='B') code=code.replace('a: 2, p: 1, q: 2','a: 2, p: 4, q: -3');
    await new AsyncFunction('lab','emit',code)(lab,x=>output.push(x));
  }
  process.stdout.write(JSON.stringify({coeffRows:lab.dlw.coeffRows,
    convergence:lab.dlw.convergence, tau:lab.dlw.tau,finest:lab.dlw.finest,
    continuumDefect:lab.dlw.continuumDefect,
    zs:lab.dlw.zs, outputs:output.map(x=>({type:x.type, title:x.title}))}));
})();
'''
    result = subprocess.run([str(NODE), "-e", js, str(OLD), "B" if parameter_b else "A"],
                            check=True, capture_output=True, text=True, encoding="utf-8")
    return json.loads(result.stdout)


def compare(dlw, reference, label):
    assert [row[0] for row in dlw.coeffRows] == [row[0] for row in reference["coeffRows"]]
    actual_coeff = np.array([row[1:] for row in dlw.coeffRows])
    ref_coeff = np.array([row[1:] for row in reference["coeffRows"]])
    np.testing.assert_allclose(actual_coeff, ref_coeff, atol=1e-13, rtol=1e-12)
    actual_conv = np.array([row[1:] for row in dlw.convergence])
    ref_conv = np.array([[np.nan if value is None else value for value in row[1:]]
                         for row in reference["convergence"]])
    np.testing.assert_allclose(actual_conv, ref_conv, atol=3e-7, rtol=5e-6, equal_nan=True)
    all_series = []
    for scheme in ("SD", "FD"):
        np.testing.assert_allclose(dlw.tau[scheme], reference["tau"][scheme],
                                   atol=1e-13, rtol=1e-12)
        np.testing.assert_allclose(dlw.finest[scheme], reference["finest"][scheme],
                                   atol=2e-9, rtol=1e-8)
        all_series.append(float(np.max(np.abs(dlw.finest[scheme]-reference["finest"][scheme]))))
    assert dlw.continuumDefect < 1e-10
    return dict(parameter=label, coeffRows=dlw.coeffRows,
                convergence=dlw.convergence,
                sampled_points=len(dlw.zs), continuumDefect=dlw.continuumDefect,
                maximum_coefficient_deviation=float(np.max(np.abs(actual_coeff-ref_coeff))),
                maximum_plot_series_deviation=max(all_series),
                maximum_convergence_table_deviation=float(np.nanmax(np.abs(actual_conv-ref_conv))))


default, output, tables, figures, ns = run()
check("Seven current visible Python cells execute without implicit replay", {
    "ids": [c["id"] for c in CELLS], "stdout": output,
    "table_shapes": [list(t.shape) for t in tables], "figures": figures})
assert len(figures) == 2 and all(f["lines"] == 4 for f in figures)
check("Default A reproduces original JS coefficient/convergence tables and every plotted point",
      compare(default, original(), "A=(2,1,2)"))

b, *_ = run(lambda src: src.replace("a=2, p=1, q=2", "a=2, p=4, q=-3"))
check("Editable parameter B reproduces independently recomputed original JS",
      compare(b, original(True), "B=(2,4,-3)"))
assert abs(b.coeffRows[0][1]-default.coeffRows[0][1]) > 0.5

edited, *_ = run(lambda src: src.replace("h=1/8", "h=1/16")
                                  .replace("points=1601", "points=801"))
assert len(edited.zs) == 801 and edited.h == 1/16
assert edited.convergence[0][1] == 1/16
assert edited.coeffRows[0][3] != default.coeffRows[0][3]
check("Changing displayed h and points changes actual tables and finest residual", {
    "h": edited.h, "points": len(edited.zs), "sampled_h2_tau": edited.coeffRows[0][3]})

modified, *_ = run(core_transform=lambda src: src.replace(
    "r1 = Omega*(plus", "r1 = 1.01*Omega*(plus"))
core_diff = float(np.max(np.abs(modified.finest["SD"][0]-default.finest["SD"][0])))
assert core_diff > 1e-2
check("Changing the displayed residual core changes computed curves", {"max_SD1_difference": core_diff})

missing = []
for target in range(1, len(CELLS)):
    fresh = {}
    run_cell(0, fresh)
    try:
        if target == 1:
            fresh["dlw"].ready.clear()
        run_cell(target, fresh)
    except RuntimeError as error:
        missing.append(dict(id=CELLS[target]["id"], message=str(error)))
    else:
        raise AssertionError("Skipped prerequisite unexpectedly executed: " + CELLS[target]["id"])
assert len(missing) == 6
check("Missing prerequisites reject current cell instead of running hidden cells", missing)

# Rerunning a definition invalidates numerical results even though old values exist.
run_cell(1, ns)
assert ns["dlw"].ready == {"prepare", "config"}
try:
    run_cell(6, ns)
except RuntimeError as error:
    check("Rerunning configuration invalidates downstream results", {"message": str(error)})
else:
    raise AssertionError("Old residual results survived an upstream rerun")

syntax_ns = {}
run_cell(0, syntax_ns)
try:
    run_cell(1, syntax_ns, lambda src: src + "\nif\n")
except SyntaxError:
    assert syntax_ns["dlw"].ready == {"prepare"}
    run_cell(1, syntax_ns)
    assert "config" in syntax_ns["dlw"].ready
    check("Real syntax failure is preserved and corrected source runs", {"exception": "SyntaxError"})
else:
    raise AssertionError("Bad source did not raise a Python syntax error")

assert all(not item["text"] for item in output if item["id"] != "error-main")
assert output[5]["text"].startswith("continuumDefect = ")
check("Definitions are silent; tables/figures and measured stdout are ordinary program output", {
    "stdout": output[5]["text"], "tables": 3, "figures": 2})
check("Sampling maxima are labelled separately from whole-waveform analytic bounds", {
    "coefficient_columns": list(tables[1].columns), "bounds_domain": "all real z",
    "plot_y_values_keep_sign": bool((default.tau["SD"][0] < 0).any())})

result = {"status": "passed", "python": sys.executable,
          "numpy": np.__version__, "matplotlib": matplotlib.__version__,
          "source": str(OLD), "source_sha256": hashlib.sha256(OLD.read_bytes()).hexdigest(),
          "cell_sources_sha256": {c["id"]: hashlib.sha256(c["code"].encode()).hexdigest() for c in CELLS},
          "checks": CHECKS}
(HERE / "dlw_validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(json.dumps({"status": "passed", "checks": len(CHECKS), "python": sys.executable,
                  "default_coefficients": default.coeffRows}, ensure_ascii=False))
