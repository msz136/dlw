"""Initial signed spatial residuals on the current paper's exact fields."""
from pathlib import Path
import sys, json, csv, hashlib
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "Workspaces/dlw_error_mechanism_20261013/sources"))
from leading_u_analysis import coefficients, rms, cosine
from common_sources import source_parts

raw = (ROOT / "notebook/DLW数值分析report.ipynb").read_bytes()
nb = json.loads(raw)
cells = {c.get("id"): "".join(c.get("source", [])) for c in nb["cells"]}
ns = {}
for key in ("imports", "config", "reference", "spatial", "sd_fd", "sd", "fd", "time"):
    exec(cells["dlw-" + key].replace("from IPython.display import display",
                                   "display=lambda *a,**k:None"), ns)
rows, exact_rows, checks, configs = [], [], [], {}
for case in "ABCD":
    cfg = ns["case_config"](case)
    configs[case] = cfg
    obj = ns["SDModel"](case, "FD", cfg)
    iy = np.flatnonzero(abs(obj.y) < cfg["eval_yhalf"])
    ix = np.flatnonzero(abs(obj.X.x) <= cfg["eval_half"] + 1e-10)
    js, x = np.r_[obj.js[0], obj.js[iy]], obj.X.x[ix]
    coef = coefficients(obj, js, x, 0.)
    saved = {"x": x, "y": obj.y[iy]}
    for kind in ("SD", "FD"):
        model = ns["SDModel" if kind == "SD" else "FDModel"](case, kind, cfg)
        parts = source_parts(model, 0., details=True)
        checks.append({"case": case, "method": kind, **parts["checks"],
                       "derivative_convention": coef["convention_linf"]})
        X = obj.X.dx**2 * coef["x"]
        Y = cfg["h"]**2 * coef[kind]
        truth = parts["fields"]["total"]["u"][np.ix_(iy, ix)]
        rows.append(dict(case=case, method="PE" if kind == "SD" else "FD",
                         rms_x=rms(X), rms_y=rms(Y), cosine=cosine(X, Y),
                         rms_sum=rms(X+Y), max_sum=float(abs(X+Y).max()),
                         rms_full=rms(truth), max_full=float(abs(truth).max()),
                         relative_field_difference=rms(X+Y-truth)/rms(truth)))
        saved[f"X_{kind}"], saved[f"Y_{kind}"] = X, Y
        for field in ("u", "v"):
            ex = parts["fields"]["x_stencil"][field][np.ix_(iy, ix)]
            ey = parts["fields"]["y_model"][field][np.ix_(iy, ix)]
            exact_rows.append(dict(case=case, method="PE" if kind == "SD" else "FD",
                                   field=field, rms_x=rms(ex), rms_y=rms(ey),
                                   cosine=cosine(ex, ey), rms_sum=rms(ex+ey),
                                   max_sum=float(abs(ex+ey).max())))
    np.savez_compressed(HERE / f"{case}_leading.npz", **saved)
    print(case, rows[-2:], flush=True)
for filename, data in (("leading_u.csv", rows), ("exact_uv.csv", exact_rows)):
    with (HERE / filename).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0]))
        writer.writeheader()
        writer.writerows(data)
print("CHECKS", json.dumps(checks), flush=True)
assert max(max(abs(v) for k, v in r.items() if k not in ("case", "method"))
           for r in checks) < 1e-8
(HERE / "verification.json").write_text(json.dumps(
    {"notebook_sha256": hashlib.sha256(raw).hexdigest(), "configs": configs,
     "checks": checks, "scope": "t=0 spatial RHS residual, not initial solution error",
     "sampling": "native fixed-grid nodes in paper regions; RMS without mean subtraction"},
    indent=2), encoding="utf-8")
