"""Check whether expanding the physical window changes the core ranking."""
import json
import numpy as np
from pathlib import Path
from time import perf_counter
from run_factorial import SPACES,evaluate
from hs_exact import Soliton
from hs_fixed import FixedSystem
from hs_solver import MovingSystem,solve

ref=Soliton((5.,),c=1.)
rows=[]
for half in (4.,5.):
    a=.02;edges=int(round(2*half/a))
    X=np.linspace(-half,half,edges+1)
    u0,x0,_=ref.continuous_X(X,0.)
    for space in SPACES:
        if space=='fixed_difference':
            system=FixedSystem(np.linspace(-half,half,edges+1),1,ref)
            z0=system.initial(0.)
        else:
            b=lambda t:float(ref.continuous_X(np.array([-half]),t)[0][0])
            system=MovingSystem(a,1,edges,b,
                'sd' if space=='integrable_moving' else 'fd')
            z0=system.pack(np.diff(u0),np.diff(x0),x0[0])
        tic=perf_counter()
        result=solve(system,z0,0,.25,.00625,'rk8',outputs=(0.,.25),strict=False)
        if result.status!='completed' or result.rejected:
            raise RuntimeError(f'{space} L={half} {result.status}')
        core=evaluate(ref,system,.25,result.states[-1],space)['common']['core']
        row={'space':space,'half_width':half,'edges':edges,'dt':.00625,
             'u_core_linf':core['u_linf'],'rho_core_linf':core['rho_linf'],
             'seconds':perf_counter()-tic}
        rows.append(row)
        print(row,flush=True)
(Path(__file__).resolve().parent/'out'/'domain_audit.json').write_text(
    json.dumps({'rows':rows,'status':'completed'},indent=2)+'\n',encoding='utf-8')
