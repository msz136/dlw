"""CSD0: former direct-(u,v) Centered-SD, four solitons, shared RK4 settings.

Usage: python run.py A/B/C/D; python run.py all; python run.py collect
Outputs remain in this directory. The original Model implementation is imported.
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
SEPARATED = SPATIAL / "separated"
sys.path.insert(0, str(SPATIAL))
sys.path.insert(0, str(SEPARATED))
from run_separated import Model, HALF_WIDTHS, fields, norm, step
import run as source_module
assert Path(source_module.__file__).resolve() == SPATIAL / "run.py"

H = DX = .1
DT, T = 1e-4, .01


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rel(p):
    return p.relative_to(ROOT).as_posix()


def source_hashes():
    paths = [Path(__file__), SPATIAL / "run.py", SEPARATED / "run_separated.py",
             PROJECT / "paper_comparison_20261022/solver_snapshot.py"]
    return [dict(path=rel(p), sha256=sha(p)) for p in paths]


def compute(case):
    dest = HERE / f"{case}_CSD0_RK4.json"
    if dest.exists():
        print("Existing record retained:", dest.name, flush=True)
        return
    started = time.perf_counter()
    m = Model(case, "Centered-SD", DX, H)
    z0 = m.initial()
    uj, _, tu = fields(m, m.y)
    _, vj, tv = fields(m, m.yv)
    reference_rate = np.array([tu[0], tv[1]])
    initial_rate = m.rhs(0., z0)
    initial_total = norm(m, initial_rate - reference_rate)
    source_initial = np.array([uj[0], vj[0]])
    initial_profile_difference = float(np.max(abs(source_initial - z0)))
    assert initial_profile_difference < 1e-12
    checks = dict(initial_analytic_profile_difference=initial_profile_difference,
                  initial_lower_ut_difference=float(np.max(abs(initial_rate[0, 0] - m.ut(m.y[:1], 0.)[0]))))
    old_spatial = json.loads((SEPARATED / "spatial.json").read_text())
    old_initial = next(r for r in old_spatial if r["case"] == case and
                       r["method"] == "Centered-SD" and r["h"] == H and r["dx"] == DX)
    checks["old_initial_total"] = old_initial["total"]
    checks["old_initial_total_difference"] = max(abs(a-b) for a, b in zip(initial_total, old_initial["total"]))
    assert checks["old_initial_total_difference"] < 1e-8
    initial = dict(case=case, method="CSD0", t=0., h=H, dx=m.dx, a=m.a,
                   total=initial_total, reference="Continuous exact soliton initial time derivatives, evaluated analytically from tau moments.",
                   state="u,v at the same y sites; w=v-delta_0 u", checks=checks.copy())
    z = z0.copy()
    reached, status = 0., "complete"
    evolution_started = time.perf_counter()
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        try:
            for i in range(round(T/DT)):
                zn = step(m, i*DT, z, DT)
                if not np.isfinite(zn).all() or np.max(abs(zn)) > 1e6:
                    raise RuntimeError("nonfinite_or_amplitude_threshold")
                z = zn
                reached = (i+1)*DT
        except (FloatingPointError, RuntimeError) as exc:
            status = "failed: " + str(exc)
    evolution_seconds = time.perf_counter()-evolution_started
    reference = np.array([m.profile(m.y, reached)[0], m.profile(m.yv, reached)[1]])
    error = norm(m, z-reference)
    reference0 = np.array([m.profile(m.y, 0.)[0], m.profile(m.yv, 0.)[1]])
    checks["initial_physical_error"] = norm(m, z0-reference0)
    # This is a new evolution. Compare its saved legacy trajectory as a regression only.
    legacy_npz = SEPARATED / f"time_{case}_RK4_0.0001.npz"
    legacy_record = SEPARATED / f"time_{case}_RK4_0.0001.json"
    if legacy_npz.exists():
        old_z = np.load(legacy_npz)["z"]
        checks["legacy_final_state_difference"] = float(np.max(abs(z-old_z)))
        checks["legacy_trajectory"] = rel(legacy_npz)
        checks["legacy_trajectory_sha256"] = sha(legacy_npz)
        checks["legacy_record_sha256"] = sha(legacy_record)
        assert checks["legacy_final_state_difference"] < 1e-12
    state_path = dest.with_suffix(".npz")
    np.savez_compressed(state_path, z=z, z0=z0, u=z[0], v=z[1], u0=z0[0], v0=z0[1],
                        initial_rate=initial_rate, reference_rate=reference_rate,
                        reference=reference, reference0=reference0,
                        x=m.x, y=m.y, yv=m.yv, reached=reached)
    rec = dict(case=case, method="CSD0", original_method_label="Centered-SD",
               integrator="RK4", h=H, dx=m.dx, dt=DT, T=T, reached=reached,
               status=status, error=error, nx=m.nx, ny=len(m.y), a=m.a,
               lambda_parameter=-2., computational_half_width=m.half,
               region_half_width=HALF_WIDTHS[case], initial_error=checks["initial_physical_error"],
               metric="Absolute sampled maximum at native field locations, |x|<=R, |y|<R.",
               reference="Continuous exact soliton physical fields.",
               state="u,v at the same y sites; auxiliary w=v-delta_0 u; original h^2 flux retained.",
               spatial_x="Fourier differentiation; first-derivative Nyquist multiplier zero; no filtering or dealiasing.",
               boundary="Exact continuous lower u_t and lower ghost u; upper ghost is exact continuous background plus quadratic extrapolation of perturbation.",
               reused_from=None, checks=checks, evolution_seconds=evolution_seconds,
               processing_seconds=time.perf_counter()-started, artifact=rel(state_path),
               artifact_sha256=sha(state_path), sources=source_hashes())
    initial["artifact"] = rec["artifact"]
    initial["artifact_sha256"] = rec["artifact_sha256"]
    initial["sources"] = rec["sources"]
    dest.write_text(json.dumps(rec, indent=2), encoding="utf-8")
    (HERE / f"{case}_CSD0_initial.json").write_text(json.dumps(initial, indent=2), encoding="utf-8")
    print(json.dumps(dict(case=case, status=status, initial=initial_total, error=error,
                          evolution_seconds=evolution_seconds)), flush=True)


def collect():
    results, initial, audits = [], [], []
    for case in "ABCD":
        dest = HERE / f"{case}_CSD0_RK4.json"
        rec = json.loads(dest.read_text())
        ini = json.loads((HERE / f"{case}_CSD0_initial.json").read_text())
        data = np.load(dest.with_suffix(".npz"))
        m = Model(case, "Centered-SD", DX, H)
        np.testing.assert_array_equal(data["x"], m.x)
        np.testing.assert_array_equal(data["y"], m.y)
        np.testing.assert_array_equal(data["yv"], m.yv)
        assert rec["status"] == "complete" and rec["reached"] == T
        assert rec["artifact_sha256"] == sha(dest.with_suffix(".npz"))
        truth = np.array([m.profile(m.y, T)[0], m.profile(m.yv, T)[1]])
        difference = float(np.max(abs(data["reference"]-truth)))
        assert difference == 0.
        final_error = norm(m, data["z"]-truth)
        initial_error = norm(m, data["initial_rate"]-data["reference_rate"])
        final_diff = max(abs(a-b) for a, b in zip(final_error, rec["error"]))
        initial_diff = max(abs(a-b) for a, b in zip(initial_error, ini["total"]))
        assert final_diff == 0. and initial_diff == 0.
        results.append(rec)
        initial.append(ini)
        audits.append(dict(case=case, recomputed_error=final_error,
                           recomputed_initial_total=initial_error, final_record_difference=final_diff,
                           initial_record_difference=initial_diff,
                           stored_reference_difference=difference,
                           initial_physical_error=rec["initial_error"],
                           old_initial_total_difference=rec["checks"]["old_initial_total_difference"],
                           legacy_final_state_difference=rec["checks"].get("legacy_final_state_difference")))
    (HERE / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    (HERE / "initial_results.json").write_text(json.dumps(initial, indent=2), encoding="utf-8")
    (HERE / "validation.json").write_text(json.dumps(dict(records=4, complete=4,
        max_final_record_difference=max(r["final_record_difference"] for r in audits),
        max_initial_record_difference=max(r["initial_record_difference"] for r in audits),
        audits=audits), indent=2), encoding="utf-8")
    print("Collected and verified four initial and final records.", flush=True)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    if arg == "collect":
        collect()
    elif arg == "all":
        for case in "ABCD":
            compute(case)
        collect()
    else:
        compute(arg)
