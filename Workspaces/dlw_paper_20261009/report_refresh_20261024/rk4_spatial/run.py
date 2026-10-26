"""Same-RK4 comparison of current Endpoint-SD, full-potential Centered-SD and FD.

Outputs only into this directory. References are continuous exact soliton fields.
Usage: python run.py A (or B/C/D); python run.py collect
"""
from pathlib import Path
import hashlib
import json
import sys
import time
import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ROOT = PROJECT.parents[1]
SPATIAL = PROJECT / "spatial_audit_20261023"
PROBE = SPATIAL / "separated/reconstruction_probe"
OLD = PROBE / "rerun_20261024"
sys.path.insert(0, str(PROBE))
from rerun_20261024 import make, rhs as centered_rhs, transform
from run_separated import Model, HALF_WIDTHS

METHODS = ("Endpoint-SD", "Centered-SD", "FD")
DT, T, H, DX = 1e-4, .01, .1, .1


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    return path.relative_to(ROOT).as_posix()


def sources(extra=()):
    paths = [Path(__file__), SPATIAL / "run.py", PROBE / "rerun_20261024.py",
             PROBE / "probe.py", SPATIAL / "separated/run_separated.py",
             PROJECT / "paper_comparison_20261022/solver_snapshot.py", *extra]
    return [dict(path=rel(p), sha256=sha(p)) for p in paths]


def physical_error(m, u, v, yv, t):
    radius = HALF_WIDTHS[m.case]
    mx = abs(m.x) <= radius
    mu = abs(m.y) < radius
    mv = abs(yv) < radius
    eu = u - m.profile(m.y, t)[0]
    ev = v - m.profile(yv, t)[1]
    return [float(np.max(abs(eu[mu][:, mx]))), float(np.max(abs(ev[mv][:, mx])))]


def step(rhs, t, z):
    k1 = rhs(t, z)
    k2 = rhs(t + DT/2, z + DT*k1/2)
    k3 = rhs(t + DT/2, z + DT*k2/2)
    k4 = rhs(t + DT, z + DT*k3)
    return z + DT*(k1 + 2*k2 + 2*k3 + k4)/6


def compute(case, method):
    dest = HERE / f"{case}_{method}_RK4.json"
    if dest.exists():
        print("Existing record retained:", dest.name, flush=True)
        return
    started = time.perf_counter()
    checks = {}
    extra = []
    if method == "Centered-SD":
        m, z0, inverse_checks = make(case, DX, H)
        checks.update(inverse_checks)
        yv = (m.y[1:] + m.y[:-1])/2
        u0, v0 = z0[0], transform(m, *z0)
        old_json, old_npz = OLD / f"time_{case}_RK4.json", OLD / f"time_{case}_RK4.npz"
        prior = json.loads(old_json.read_text())
        assert prior["spatial"] == "Centered-SD full potential"
        assert (prior["dx"], prior["h"], prior["dt"], prior["T"], prior["reached"], prior["status"]) == (DX, H, DT, T, T, "complete")
        state_data = np.load(old_npz)
        z = state_data["z"].copy()
        u, v = z[0], transform(m, *z)
        checks["stored_v_map_difference"] = float(np.max(abs(v-state_data["v"])))
        checks["recomputed_error_difference"] = max(abs(a-b) for a,b in zip(physical_error(m,u,v,yv,T),prior["error"]))
        assert checks["stored_v_map_difference"] < 1e-13
        assert checks["recomputed_error_difference"] < 1e-13
        # Continuous lower u time derivative is the common integration constant.
        rate = centered_rhs(m, 0., z0)
        checks["initial_lower_ut_difference"] = float(np.max(abs(rate[0,0]-m.ut(m.y[:1],0)[0])))
        state = "u,w; physical v obtained from current full-potential edge map"
        closure = "Exact continuous lower u_t; every w node including lower trace evolved by its equation; no upper y ghost."
        reached, status, reuse = T, "complete", rel(old_npz)
        evolution_seconds = prior["seconds"]
        extra = [old_json, old_npz]
    else:
        m = Model(case, method, DX, H)
        z0 = m.initial()
        yv = m.yv
        u0, v0 = z0
        initial_rate = m.rhs(0., z0)
        checks["initial_lower_ut_difference"] = float(np.max(abs(initial_rate[0,0]-m.ut(m.y[:1],0)[0])))
        z = z0.copy()
        reached, status, reuse = 0., "complete", None
        evolution_started = time.perf_counter()
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            try:
                for i in range(round(T/DT)):
                    new = step(m.rhs, i*DT, z)
                    if not np.isfinite(new).all() or np.max(abs(new)) > 1e6:
                        raise RuntimeError("nonfinite_or_amplitude_threshold")
                    z = new
                    reached = (i+1)*DT
            except (FloatingPointError, RuntimeError) as exc:
                status = "failed: " + str(exc)
        evolution_seconds = time.perf_counter()-evolution_started
        u, v = z
        state = "u,v; both physical fields evolved directly"
        closure = ("Exact continuous lower u_t and lower ghost u; backward/open chain; no upper y ghost." if method == "Endpoint-SD" else
                   "Exact continuous lower u_t and lower ghost u; upper ghost is exact continuous background plus quadratic extrapolation of perturbation.")

    error = physical_error(m, u, v, yv, reached)
    initial_error = physical_error(m, u0, v0, yv, 0.)
    checks["initial_physical_error"] = initial_error
    assert max(initial_error) < 1e-9
    # Save physical fields even on failure, explicitly at the last completed time.
    state_path = dest.with_suffix(".npz")
    np.savez_compressed(state_path, z=z, z0=z0, u=u, v=v, u0=u0, v0=v0,
                        x=m.x, y=m.y, yv=yv, reached=reached)
    record = dict(case=case, method=method, integrator="RK4", h=H, dx=m.dx,
                  dt=DT, T=T, reached=reached, status=status, error=error, state=state,
                  nx=m.nx, ny=len(m.y), a=m.a, computational_half_width=m.half,
                  region_half_width=HALF_WIDTHS[case], initial_error=initial_error,
                  metric="Absolute sampled maximum at native field locations, |x|<=R, |y|<R.",
                  reference="Continuous exact soliton physical fields; not a semi-discrete exact reference.",
                  spatial_x="Fourier differentiation; first-derivative Nyquist multiplier zero; no filtering or dealiasing.",
                  boundary=closure, checks=checks, reused_from=reuse,
                  evolution_seconds=evolution_seconds, processing_seconds=time.perf_counter()-started,
                  artifact=rel(state_path), artifact_sha256=sha(state_path), sources=sources(extra))
    dest.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps({k:record[k] for k in ("case","method","status","reached","error","evolution_seconds")}), flush=True)


def collect():
    rows, audits = [], []
    for case in "ABCD":
        for method in METHODS:
            path = HERE / f"{case}_{method}_RK4.json"
            record = json.loads(path.read_text())
            data = np.load(path.with_suffix(".npz"))
            m = Model(case, method, DX, H)
            if method == "Centered-SD":
                m.gauge = "mean"
                mapped = transform(m, *data["z"])
                map_error = float(np.max(abs(mapped-data["v"])))
                assert map_error < 1e-13
            else:
                map_error = float(np.max(abs(data["z"]-np.array([data["u"],data["v"]]))))
                assert map_error == 0.
            recalculated = physical_error(m, data["u"], data["v"], data["yv"], record["reached"])
            diff = max(abs(a-b) for a,b in zip(record["error"], recalculated))
            assert diff < 1e-13
            assert record["artifact_sha256"] == sha(path.with_suffix(".npz"))
            audits.append(dict(case=case,method=method,recomputed_error=recalculated,
                               record_difference=diff,stored_physical_map_difference=map_error))
            rows.append(record)
    (HERE/"results.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    (HERE/"validation.json").write_text(json.dumps(dict(
        records=len(rows),complete=sum(r["status"]=="complete" for r in rows),
        max_record_difference=max(a["record_difference"] for a in audits),
        audit=audits,
        interpretation="Same RK4 and step size across current implementations. Total physical-field error, not isolated spatial truncation error; RK4 in physical u,v versus auxiliary u,w is not invariant under the nonlinear physical-v map."
    ),indent=2),encoding="utf-8")
    print(json.dumps(dict(records=len(rows),complete=sum(r["status"]=="complete" for r in rows))),flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "collect":
        collect()
    else:
        for method in METHODS:
            compute(sys.argv[1], method)
