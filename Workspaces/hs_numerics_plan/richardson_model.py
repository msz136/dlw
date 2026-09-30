"""Cancel the observed leading finite-a model error on a common physical grid."""
import json
from pathlib import Path
import numpy as np
from hs_exact import Soliton
from hs_solver import MovingSystem, solve

ROOT=Path(__file__).resolve().parent
rows=[]
for p in (4.5,5.,5.5):
    ref=Soliton((p,))
    for T in (.25,.5,1.):
        x_common=np.linspace(-2.5,2.5,1001)
        uc,rc,_=ref.continuous_x(x_common,T)
        fields={}
        for a in (.04,.02,.01,.005):
            k0=round(-4/a);k=np.arange(k0,-k0+1)
            system=MovingSystem(a,1,len(k)-1,
                lambda t:float(ref.lattice(np.array([k0]),a,t)[0][0]))
            z0=system.exact_initial(ref,k0,0)
            res=solve(system,z0,0,T,.002,'rk4')
            f=system.fields(T,res.states[-1])
            mid=.5*(f['x'][:-1]+f['x'][1:])
            fields[a]=(np.interp(x_common,f['x'],f['u']),
                       np.interp(x_common,mid,f['rho']))
        for a in (.04,.02,.01):
            coarse=fields[a];fine=fields[a/2]
            extrap=(2*fine[0]-coarse[0],2*fine[1]-coarse[1])
            rows.append({'p':p,'T':T,'a_coarse':a,'a_fine':a/2,
                'u_coarse':float(max(abs(coarse[0]-uc))),
                'rho_coarse':float(max(abs(coarse[1]-rc))),
                'u_fine':float(max(abs(fine[0]-uc))),
                'rho_fine':float(max(abs(fine[1]-rc))),
                'u_extrap':float(max(abs(extrap[0]-uc))),
                'rho_extrap':float(max(abs(extrap[1]-rc)))})
(ROOT/'out'/'richardson_model.json').write_text(json.dumps({
    'setup':'Actual RK4 numerical 2-HS semi-discrete trajectories from exact finite-a initial states, dt=0.002; interpolate both to common physical x in [-2.5,2.5], then form 2 z_{a/2}-z_a.',
    'note':'Postprocessed extrapolation cancels leading smooth O(a) model term; the extrapolated field is not itself a solution of either semi-discrete system.',
    'rows':rows},indent=2),encoding='utf-8')
print('Wrote richardson_model.json',len(rows),'cases')
