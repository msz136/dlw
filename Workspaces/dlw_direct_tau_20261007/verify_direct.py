"""Independent raw-bilinear residual and saved-run/convergence audit."""
from pathlib import Path
import hashlib
import json
import numpy as np
from direct_tau import Config, DirectBilinear, GramTau, CASES

HERE = Path(__file__).resolve().parent
OUT = HERE/'out'

def raw_residual(olda, oldb, newa, newb, dx, dt, s):
    # One fixed scale per row/field, shared by old and new time levels.
    sa = np.maximum(olda.max(axis=1), newa.max(axis=1))[:, None]
    sb = np.maximum(oldb.max(axis=1), newb.max(axis=1))[:, None]
    f0, f1 = np.exp(olda-sa), np.exp(newa-sa)
    g0, g1 = np.exp(oldb-sb), np.exp(newb-sb)
    f, g = (f0+f1)/2, (g0+g1)/2
    inside = np.arange(4, f.shape[1]-4)
    def derivative(value, offsets, coefficients, divisor):
        return sum(c*value[:, inside+k] for k, c in zip(offsets, coefficients))/divisor
    fx = derivative(f, (-2, -1, 1, 2), (1, -8, 8, -1), 12*dx)
    gx = derivative(g, (-2, -1, 1, 2), (1, -8, 8, -1), 12*dx)
    fxx = derivative(f, range(-4, 5), (1, -16, 64, 16, -130, 16, 64, -16, 1), 144*dx*dx)
    gxx = derivative(g, range(-4, 5), (1, -16, 64, 16, -130, 16, 64, -16, 1), 144*dx*dx)
    residual = (fxx*g[:, inside]-2*fx*gx+f[:, inside]*gxx
        +(f1[:, inside]*g0[:, inside]-f0[:, inside]*g1[:, inside])/dt
        +2*s*(fx*g[:, inside]-f[:, inside]*gx))
    normalized = residual/(f[:, inside]*g[:, inside])
    return float(abs(normalized).max())

def main():
    rows = json.loads((OUT/'results.json').read_text())
    assert len(rows) == 12 and all(r['completed'] and not r['reason'] for r in rows)
    assert all(r['linear_solves'] == 48*round(r['config']['T']/r['config']['dt']) for r in rows)
    assert max(r['exact_bilinear_residual'] for r in rows) < 1e-11
    audits, orders, comparisons = [], [], []
    for case in CASES:
        model = DirectBilinear(case)
        a0, b0 = model.initial
        # Perturb an interior layer to ensure the update does not reload exact interior tau.
        a0 = a0.copy()
        a0[7, model.inside] += 1e-7*np.sin(model.x[model.inside]*2)
        a1, b1 = model.advance(a0, b0, 0., model.cfg.dt)
        minus = raw_residual(a0, b0[:-1], a1, b1[:-1], model.dx, model.cfg.dt, 2-model.cfg.h/2)
        plus = raw_residual(a0, b0[1:], a1, b1[1:], model.dx, model.cfg.dt, 2+model.cfg.h/2)
        assert max(minus, plus) < 5e-9
        audits.append(dict(case=case, Bminus=minus, Bplus=plus))
        base = [np.load(OUT/f'{case}_n256_dt{k}.npz') for k in (1, 2, 4)]
        for field in ('alpha', 'beta', 'u', 'v'):
            mask = abs(base[0]['x']) <= 10
            d1 = float(abs(base[0][field][:, mask]-base[1][field][:, mask]).max())
            d2 = float(abs(base[1][field][:, mask]-base[2][field][:, mask]).max())
            p = float(np.log2(d1/d2))
            orders.append(dict(case=case, field=field, full_half_difference=d1,
                               half_quarter_difference=d2, observed_order=p))
        # Re-run main configurations after the failure-state bookkeeping repair.
        fresh, arrays = DirectBilinear(case).run()
        assert fresh['completed']
        assert all(np.array_equal(arrays[k], base[0][k]) for k in ('alpha', 'beta', 'u', 'v'))
        comparisons.append(dict(case=case, post_review_main_run_identical=True))
        for z in base:
            z.close()
    summary = dict(success=True, full_runs=12, all_reached=.01, independent_raw_bilinear_audits=audits,
        temporal_orders=orders, repaired_main_runs=comparisons,
        maximum_linear_residual=max(r['normalized_linear_residual'] for r in rows),
        maximum_analytic_reference_residual=max(r['exact_bilinear_residual'] for r in rows),
        source_sha256=hashlib.sha256((HERE/'direct_tau.py').read_bytes()).hexdigest(),
        reference='Finite-h Gram tau; given lowest G and nonperiodic analytic x strips',
        no_comparison_to_old_lower_u_boundary=True)
    (HERE/'validation.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(summary, indent=2), flush=True)

if __name__ == '__main__':
    main()
