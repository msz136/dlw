"""Time self-convergence of the actual finite-h solver on one fixed x grid.

Pair adjacent step refinements; no exact-Gram spatial floor or reference solver
is subtracted. Orders concern this smooth, short-time, finite-dimensional IVP.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
from e2_e3_solver import make_case, integrate, NX_MAIN, T_END


def fields(P, W, G, X, C, t):
    u = C.u_from_P(P, G.u_row(C.jL, X.x, t))
    ext = np.concatenate((G.u_row(C.jL-1, X.x, t)[None, :], u,
                          G.u_row(C.jR+1, X.x, t)[None, :]), axis=0)
    return u, W + (ext[2:]-ext[:-2])/(2*C.h)


def study(h, method):
    G, X, C, rhs, P0, W0 = make_case('A', h, NX_MAIN)
    records, differences = [], []
    previous = None
    for n in (4, 8, 16, 32, 64):
        P, W, info = integrate(rhs, 0.0, T_END, P0, W0, T_END/n,
                               method=method, tol=1e-14, maxit=100)
        assert info['stopped'] is None and abs(info['final_t']-T_END)<1e-14
        assert info['steps']==n and np.isfinite(P).all() and np.isfinite(W).all()
        u, v = fields(P, W, G, X, C, T_END)
        state = (P, W, u, v)
        records.append(dict(n=n, dt=T_END/n, **info))
        if previous is not None:
            d = {key:float(np.max(np.abs(a-b)))
                 for key,a,b in zip(('P','W','u','v'),previous,state)}
            assert all(np.isfinite(x) and x>0 for x in d.values())
            row = {'coarse_n':n//2,'fine_n':n,'differences_Linf':d}
            if differences:
                row['orders']={key:float(np.log2(differences[-1]['differences_Linf'][key]/value))
                               for key,value in d.items()}
            differences.append(row)
            print(h, method, n, row, flush=True)
        previous = state
    # Check all evolved and reconstructed components; allow pre-asymptotic error.
    expected={'euler':1,'rk4':4,'trapezoid':2}[method]
    observed=list(differences[-1]['orders'].values())
    accepted=all(abs(p-expected)<0.35 for p in observed)
    return dict(h=h, method=method, nx=NX_MAIN, t_end=T_END,
                expected_order=expected, accepted=accepted,
                runs=records, successive_differences=differences)


def main():
    results=[study(h, method) for h in (1/4,1/8)
             for method in ('euler','rk4','trapezoid')]
    root=Path(__file__).resolve().parents[1]
    sources=[Path(__file__).resolve(),root/'experiments/e2_e3_solver.py',
             root/'lib/solver.py',root/'lib/gramtau.py']
    data=dict(experiment='E2_E3_time_self_convergence',
              comparison='same grid, same initial state, same time-dependent boundary; adjacent time steps',
              norm='Linf, all chain sites and periodic x nodes',
              limitation='Observed finite-dimensional short-time order; not a proof of nonlinear stability or continuum convergence.',
              source_sha256={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
              studies=results, passed=all(r['accepted'] for r in results))
    (root/'out/e2_e3_self_convergence.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    assert data['passed'], 'One or more measured orders failed the declared acceptance window'
    print('PASS: all six finite-h time self-convergence studies',flush=True)


if __name__=='__main__':
    main()
