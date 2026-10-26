"""Read-only verification of current soliton tables; no manuscript mutation."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "Workspaces/dlw_paper_20261009"
PROBE = PROJECT / "spatial_audit_20261023/separated/reconstruction_probe"
SOURCE = PROBE / "rerun_20261024"
sys.path.insert(0, str(PROBE))
from rerun_20261024 import make, norms, transform

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def relative(path):
    return path.relative_to(ROOT).as_posix()

spatial = []
baselines = json.loads((SOURCE / "baselines.json").read_text())
for case in "ABCD":
    for method in ("Endpoint-SD", "Centered-SD", "FD"):
        if method == "Centered-SD":
            record = json.loads((SOURCE / f"spatial_{case}_0.1_0.1.json").read_text())
        else:
            record = next(r for r in baselines if r["case"] == case and r["method"] == method
                          and r["dx"] == .1 and r["h"] == .1)
        spatial.append(record)

temporal = json.loads((SOURCE / "temporal.json").read_text())
verified = []
for case in "ABCD":
    model, _, _ = make(case, .1, .1)
    edges = (model.y[1:] + model.y[:-1]) / 2
    exact_u = model.profile(model.y, .01)[0]
    exact_v = model.profile(edges, .01)[1]
    for method in ("Euler", "RK4", "CN"):
        path = SOURCE / f"time_{case}_{method}.npz"
        data = np.load(path)
        reconstructed = transform(model, *data["z"])
        computed = norms(model, data["z"][0] - exact_u, reconstructed - exact_v)
        record = next(r for r in temporal if r["case"] == case and r["method"] == method)
        delta = max(abs(a-b) for a,b in zip(record["error"], computed))
        map_delta = float(np.max(abs(reconstructed - data["v"])))
        assert delta < 1e-13 and map_delta < 1e-13, (case, method, delta, map_delta)
        verified.append(dict(case=case, method=method, recomputed_error=computed,
                             record_difference=delta, stored_v_map_difference=map_delta))

evidence = [SOURCE / "README.md", SOURCE / "baselines.json", SOURCE / "temporal.json",
            SOURCE / "methods.md", SOURCE / "experiments.md", PROBE / "rerun_20261024.py",
            PROBE / "rerun_baselines_20261024.py", PROBE / "probe.py",
            PROBE.parent / "run_separated.py", PROBE.parent.parent / "run.py",
            PROJECT / "paper_comparison_20261022/solver_snapshot.py"]
for case in "ABCD":
    evidence.append(SOURCE / f"spatial_{case}_0.1_0.1.json")
    for method in ("Euler", "RK4", "CN"):
        evidence.extend([SOURCE / f"time_{case}_{method}.json", SOURCE / f"time_{case}_{method}.npz"])

result = dict(
    audit_date="2026-10-24",
    spatial_reference="Analytic time derivatives of the continuous exact soliton fields, evaluated from exponential-sum moments; not semi-discrete exact solutions.",
    temporal_reference="Continuous exact soliton physical fields at T=0.01, evaluated directly from continuous tau functions.",
    reference_evaluation="float64 analytic formula evaluation; this audit is not an interval-arithmetic rounding certificate",
    metric="Absolute maximum sampled error at native field locations, |x|<=R and |y|<R; not relative error or a continuous-domain supremum certificate.",
    region_half_width=dict(A=5., B=10., C=30., D=30.),
    computational_half_width=dict(A=10., B=20., C=40., D=40.),
    field_locations=dict(u="y_k=-L+h/2+k*h", Endpoint_SD_v="y_k-h/2", Centered_SD_v="internal edge midpoints (y[k]+y[k-1])/2", FD_v="same nodes as u"),
    initialization="Common continuous u,v samples. Centered-SD obtains w through nonlinear inverse constraint with continuous lower w=v-u_y.",
    spatial_operators="Fourier x differentiation; first derivative Nyquist multiplier zero; second derivative retains -xi^2; centered full-potential primitive zeros zero/Nyquist modes; no filtering or dealiasing.",
    temporal_implementation="Centered-SD full potential, evolved state (u,w), physical v reconstructed afterward; h=dx=.1, dt=1e-4, T=.01. Every w node including lower trace evolves; exact continuous lower u_t supplies integration constant.",
    recommended_titles=dict(spatial="Initial physical time-derivative defects at t=0", temporal="Final physical-field errors at T=0.01 for Centered-SD"),
    interpretation="T=.01 values are total errors including spatial approximation, time integration, finite periodic computational interval, boundary handling, and roundoff; they do not isolate temporal truncation error or establish temporal order.",
    spatial=spatial,
    temporal=temporal,
    saved_npz_verification=verified,
    sources=[dict(path=relative(p), sha256=sha(p)) for p in evidence],
)
dest = Path(__file__).with_name("soliton_data_audit.json")
dest.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(dict(output=str(dest), spatial_records=len(spatial), temporal_records=len(temporal), max_record_difference=max(x["record_difference"] for x in verified), max_v_map_difference=max(x["stored_v_map_difference"] for x in verified)), indent=2))
