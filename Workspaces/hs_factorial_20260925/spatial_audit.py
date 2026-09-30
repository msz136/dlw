"""Independent spatial refinement at a small shared RK8 time step."""
import hashlib
import json
from pathlib import Path
from time import perf_counter
import numpy as np
from run_factorial import CORE, SPACES, evaluate
from hs_exact import Soliton
from hs_fixed import FixedSystem
from hs_solver import MovingSystem, solve

HERE=Path(__file__).resolve().parent
OUT=HERE/'out'
ref=Soliton((5.,),c=1.)
rows=[]
for edges in (200,400,800):
    a=8/edges
    X=np.linspace(-4,4,edges+1)
    u0,x0,_=ref.continuous_X(X,0.)
    for space in SPACES:
        if space=='fixed_difference':
            system=FixedSystem(np.linspace(-4,4,edges+1),1,ref)
            state=system.initial(0.)
        else:
            b=lambda t:float(ref.continuous_X(np.array([-4.]),t)[0][0])
            system=MovingSystem(a,1,edges,b,
                'sd' if space=='integrable_moving' else 'fd')
            state=system.pack(np.diff(u0),np.diff(x0),x0[0])
        tic=perf_counter()
        result=solve(system,state,0,.25,.00625,'rk8',outputs=(0.,.25),strict=False)
        if result.status!='completed' or result.rejected:
            raise RuntimeError(f'{space} {edges}: {result.status} {result.failure_reason}')
        values=evaluate(ref,system,.25,result.states[-1],space)
        row={'space':space,'edges':edges,'a_or_dx':a,'dt':.00625,
             'seconds':perf_counter()-tic,
             'core':values['common']['core'],'native':values['native'],
             'min_spacing':values['mesh']['min_spacing']}
        rows.append(row)
        print(space,edges,row['core']['u_linf'],row['core']['rho_linf'],flush=True)
result={'reference':'continuous exact 2HS single soliton',
        'method':'fixed-step DOP853 eighth-order main step',
        'time':.25,'core':[-2,2],'rows':rows,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(OUT/'spatial_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
