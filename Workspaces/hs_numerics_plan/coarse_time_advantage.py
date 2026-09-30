"""Find a local regime where eighth order improves continuous total error too."""
import json
from pathlib import Path
import numpy as np
from hs_exact import Soliton
from hs_solver import MovingSystem,solve

ROOT=Path(__file__).resolve().parent
rows=[]
for p in (4.5,5.,5.5):
    ref=Soliton((p,))
    for a in (.01,.02,.03):
        k0=round(-4/a);k=np.arange(k0,round(4/a)+1)
        sy=MovingSystem(a,1,len(k)-1,
            lambda t:float(ref.lattice(np.array([k0]),a,t)[0][0]))
        z0=sy.exact_initial(ref,k0,0)
        ex=ref.lattice_state(k,a,1.)
        for method in ('euler','heun','rk4','rk8'):
            res=solve(sy,z0,0,1.,.5,method,strict=False)
            f=sy.fields(res.t[-1],res.states[-1])
            uc=ref.continuous_x(f['x'],res.t[-1])[0]
            rc=ref.continuous_density_cell_mean(f['x'][:-1],f['x'][1:],res.t[-1])
            rows.append({'p':p,'a':a,'T':1.,'dt':.5,'method':method,
                'status':res.status,'u_solve':float(max(abs(f['u']-ex['u']))),
                'rho_solve':float(max(abs(f['rho']-ex['rho']))),
                'u_total':float(max(abs(f['u']-uc))),
                'rho_total':float(max(abs(f['rho']-rc)))})
(ROOT/'out'/'coarse_time_advantage.json').write_text(json.dumps({
    'setup':'Finite-a exact initial data, common left boundary, T=1, dt=0.5. Euler, Heun, RK4 and fixed-step DOP853 RK8; physical continuous total error.',
    'rows':rows},indent=2),encoding='utf-8')
print('Wrote coarse_time_advantage.json',len(rows),'cases')
