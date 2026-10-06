"""Read-only check of actual finite-x/finite-y conservative flux algebra.

Uses the experiment's local RHS at t=0; no field trajectory or performance
ranking. Numerical exact-boundary overrides and RK integration are separate.
"""
import sys
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import experiment as ex

rows = []
for case in ex.CASES:
    for model in ('SD', 'FD'):
        for mesh in ('minus', 'zero', 'plus'):
            spec = dict(case=case, model=model, mesh=mesh, motion='moving',
                        variant='local_flux_check', nx=33,h=.125,dt=5e-6,T=.001)
            problem = ex.Problem(spec)
            state = problem.initial()
            P, Q, u, v, du, gh = problem.unpack(state,0.)
            Pt, Qt = problem.physical_rhs(P,Q,u,v,du,gh)
            Du_t = .5*(Pt[1:]+Pt[:-1])
            sigma = {'minus':-1,'zero':0,'plus':1}[mesh]
            vt = Qt[1:-1]+Du_t if model == 'SD' else Qt[1:-1]
            R_t = problem.monitor_weights @ (-(vt+sigma*Du_t)/4)
            R, flux = problem.density_flux(P,Q,u,v,du)
            defect = R_t+problem.X.d1(flux)
            scale = max(float(np.max(abs(R_t))),float(np.max(abs(problem.X.d1(flux)))),1.)
            velocity = ex.normalized_velocity(problem.X.x,R,flux)
            rows.append(dict(case=case,model=model,mesh=mesh,
                             interior_local_flux_defect=float(np.max(abs(defect[1:-1]))),
                             local_flux_scale=scale,
                             relative_defect=float(np.max(abs(defect[1:-1])))/scale,
                             endpoint_velocity=float(max(abs(velocity[0]),abs(velocity[-1]))),
                             initial_min_density=float(R.min())))
result = dict(kind='actual RHS conservative local algebra at initial state; no RK/global mass check',
              rows=rows, max_relative_defect=max(r['relative_defect'] for r in rows),
              passed=all(r['relative_defect']<1e-10 and r['endpoint_velocity']==0 for r in rows))
HERE.joinpath('implementation_flux_checks.json').write_text(
    json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},ensure_ascii=False,indent=2))
assert result['passed']
