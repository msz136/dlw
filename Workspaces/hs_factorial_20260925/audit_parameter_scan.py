"""Spatial/domain controls and finite-a exact tracking for the selected waves."""
import hashlib
import json
from pathlib import Path
from time import perf_counter
import numpy as np

from run_parameter_scan import (A,CHOICES,HALF_WIDTH,OUT,SPACES,
                                evaluate,reference,run_one,setup)
from hs_solver import MovingSystem,solve

rows=[]
for p in (3,5,12,20):
    for a in ((.04,.02,.01,.005) if p==20 else (.04,.02,.01)):
        for space in SPACES:
            print('spatial',p,a,space,flush=True)
            row,_=run_one(p,space,'rk8',.00625,a=a,outputs=(.25,))
            rows.append(row)
spatial={'status':'completed','scope':'selected p values; 3 spaces; fine RK8 time step',
         'rows':rows}
(OUT/'spatial_controls.json').write_text(json.dumps(spatial,indent=2)+'\n',encoding='utf-8')

domain=[]
for p in (3,5,12,20):
    for space in SPACES:
        print('domain',p,space,flush=True)
        row,_=run_one(p,space,'rk8',.00625,half_width=HALF_WIDTH[p]+1,
                      outputs=(.25,))
        domain.append(row)
(OUT/'domain_controls.json').write_text(json.dumps(
    {'status':'completed','added_half_width':1,'rows':domain},indent=2)+'\n',encoding='utf-8')

lattice=[]
for p in (3,5,12,20):
    ref=reference(p)
    half=HALF_WIDTH[p];edges=int(round(2*half/A));k0=-edges//2
    b=lambda t:float(ref.lattice(np.array([k0]),A,t)[0][0])
    system=MovingSystem(A,1.,edges,b,'sd')
    z0=system.exact_initial(ref,k0,0.)
    tic=perf_counter()
    result=solve(system,z0,0,.25,.00625,'rk8',outputs=(0.,.25),strict=False)
    row={'p':p,'status':result.status,'reached':float(result.t[-1]),
         'rejected':result.rejected,'seconds':perf_counter()-tic,
         'failure_reason':result.failure_reason}
    if result.status=='completed':
        f=system.fields(.25,result.states[-1]);ex=ref.lattice_state(
            np.arange(k0,k0+edges+1),A,.25)
        row.update(u_solver_linf=float(np.max(abs(f['u']-ex['u']))),
                   rho_solver_linf=float(np.max(abs(f['rho']-ex['rho']))),
                   x_solver_linf=float(np.max(abs(f['x']-ex['x']))))
    lattice.append(row)
    print('finite-a',row,flush=True)
(OUT/'integrable_lattice_check.json').write_text(json.dumps(
    {'status':'completed','definition':'lattice exact initial and exact lattice left boundary; compares solver to finite-a exact soliton',
     'rows':lattice},indent=2)+'\n',encoding='utf-8')
print('controls complete',len(rows),len(domain),len(lattice),flush=True)
