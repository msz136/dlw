"""Reproduce the reported late-time stop without suppressing failed runs."""
import argparse
import json
from pathlib import Path
import numpy as np
from hs_exact import Soliton
from hs_solver import MovingSystem,solve

parser=argparse.ArgumentParser()
parser.add_argument('--case',choices=('single','double'),default='double')
parser.add_argument('--dt',type=float,default=.001)
args=parser.parse_args()
if args.case=='double':
    ref=Soliton((1.1,1.25)); a=.02;k0=-200;m=400;t0=-3.;t1=9.;outputs=[-3,0,3,6,9]
else:
    ref=Soliton((5.,)); a=.01;k0=-400;m=800;t0=0.;t1=10.;outputs=[0,2,4,6,8,10]
system=MovingSystem(a,1,m,lambda t:float(ref.lattice(np.array([k0]),a,t)[0][0]))
z0=system.exact_initial(ref,k0,t0)
result=solve(system,z0,t0,t1,args.dt,'rk4',outputs=outputs,strict=False)
k=np.arange(k0,k0+m+1)
out={'case':args.case,'dt':args.dt,'a':a,'status':result.status,
     'failure_reason':result.failure_reason,
     'accepted':result.accepted,'rejected':result.rejected,
     'stages':[]}
for t,z in zip(result.t,result.states):
    f=system.fields(t,z);ex=ref.lattice_state(k,a,t)
    out['stages'].append({'t':float(t),
                          'u_error':float(np.max(abs(f['u']-ex['u']))),
                          'rho_error':float(np.max(abs(f['rho']-ex['rho']))),
                          'min_d':float(f['d'].min())})
path=Path(__file__).resolve().parent/'out'/f"long_{args.case}_dt{args.dt:g}.json"
path.write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
