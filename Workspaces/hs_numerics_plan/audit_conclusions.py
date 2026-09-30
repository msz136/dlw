"""Targeted audit of common-initial-data comparison and late collision accuracy."""
import json
from pathlib import Path
import numpy as np
from hs_exact import Soliton
from hs_solver import MovingSystem,solve
from run_study import continuous_initial,metrics,primitive

OUT=Path(__file__).resolve().parent/'out'

def run_case(a,half_width,t1,dt,kind):
    ref=Soliton((5.,))
    m=int(round(2*half_width/a)); k0=-m//2
    b=lambda t:float(ref.continuous_X(np.array([k0*a]),t)[0][0])
    system=MovingSystem(a,1,m,b,kind)
    z=continuous_initial(ref,a,k0,m)
    r=solve(system,z,0,t1,dt,'rk4')
    met=metrics(ref,a,k0,system,t1,r.states[-1],False)
    f=system.fields(t1,r.states[-1])
    exact=ref.continuous_x(f['x'],t1)[0]
    mask=(f['x']>=-2)&(f['x']<=2)
    return {'a':a,'half_width':half_width,'T':t1,'dt':dt,'kind':kind,
            'physical_u_linf':met['physical_u']['linf'],
            'core_u_linf':float(np.max(abs(f['u'][mask]-exact[mask]))),
            'physical_rho_linf':met['physical_rho_cell']['linf'],
            'min_d':met['min_d']}

rows=[]
for kind in ('sd','fd'):
    for a in (.04,.02,.01):
        print('refinement',kind,a,flush=True)
        rows.append(run_case(a,4.,.25,.001,kind))
    for dt in (.001,.0005):
        print('step',kind,dt,flush=True)
        rows.append(run_case(.02,4.,.5,dt,kind))
    for width in (3.,4.,5.):
        print('domain',kind,width,flush=True)
        rows.append(run_case(.02,width,.25,.001,kind))
(OUT/'audit.json').write_text(json.dumps(primitive(rows),indent=2),encoding='utf-8')
print('Wrote',OUT/'audit.json')
