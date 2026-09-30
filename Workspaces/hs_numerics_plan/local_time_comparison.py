"""Separate time-solver advantage from continuous-model error near a single soliton."""
import json
from pathlib import Path
import numpy as np
from hs_exact import Soliton
from hs_solver import MovingSystem, solve

ROOT=Path(__file__).resolve().parent
rows=[]
for p in (4.5,5.,5.5):
    ref=Soliton((p,))
    for a in (.01,.02,.03):
        k0=round(-4/a); k1=round(4/a); k=np.arange(k0,k1+1)
        system=MovingSystem(a,1,len(k)-1,
            lambda t:float(ref.lattice(np.array([k0]),a,t)[0][0]))
        z0=system.exact_initial(ref,k0,0)
        for T in (.25,.5,1.):
            exact=ref.lattice_state(k,a,T)
            for method in ('euler','heun','rk4','rk8'):
                dt=.1
                res=solve(system,z0,0,T,dt,method,strict=False)
                f=system.fields(res.t[-1],res.states[-1])
                uc=ref.continuous_x(f['x'],res.t[-1])[0]
                rc=ref.continuous_density_cell_mean(f['x'][:-1],f['x'][1:],res.t[-1])
                rows.append({'p':p,'a':a,'T':T,'method':method,'dt':dt,
                    'status':res.status,'u_solve':float(max(abs(f['u']-exact['u']))),
                    'rho_solve':float(max(abs(f['rho']-exact['rho']))),
                    'u_total':float(max(abs(f['u']-uc))),
                    'rho_total':float(max(abs(f['rho']-rc)))})
(ROOT/'out'/'local_time_comparison.json').write_text(json.dumps({
    'setup':'Semi-discrete exact initial state; same left boundary and dt=0.1; compare finite-a exact solver error and continuous physical total error.',
    'rows':rows},indent=2),encoding='utf-8')
print('Wrote local_time_comparison.json',len(rows),'cases')
