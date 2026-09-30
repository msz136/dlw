"""Short-window response to a stated smooth perturbation of the exact lattice state."""
import json
from pathlib import Path
import numpy as np
from hs_exact import Soliton
from hs_solver import MovingSystem,solve
from run_study import primitive

ROOT=Path(__file__).resolve().parent
ref=Soliton((5.,));a=.01;k0=-400;m=800
system=MovingSystem(a,1,m,lambda t:float(ref.lattice(np.array([k0]),a,t)[0][0]))
clean=system.exact_initial(ref,k0,0)
x=system.fields(0,clean)['x'];mid=(x[1:]+x[:-1])/2
profile=np.exp(-(mid/.5)**2)*np.sin(2*np.pi*np.arange(m)/17)
eps=1e-6
perturbed=clean.copy();perturbed[:m]+=eps*profile
perturbed[m:2*m]+=eps*a*profile
outputs=[0,.25,.5,1.]
rows={}
for name,z in (('clean',clean),('perturbed',perturbed)):
    rows[name]=solve(system,z,0,1,.0005,'rk4',outputs=outputs,strict=False)
comparison=[]
for i in range(min(len(rows['clean'].t),len(rows['perturbed'].t))):
    t=rows['clean'].t[i]
    f0=system.fields(t,rows['clean'].states[i]);f1=system.fields(t,rows['perturbed'].states[i])
    comparison.append({'t':float(t),'u_difference_linf':float(np.max(abs(f1['u']-f0['u']))),
                       'rho_difference_linf':float(np.max(abs(f1['rho']-f0['rho']))),
                       'x_difference_linf':float(np.max(abs(f1['x']-f0['x'])))})
out={'a':a,'p':5,'epsilon':eps,'v_perturbation':'epsilon exp(-(xmid/0.5)^2) sin(2 pi edge_index/17)',
     'd_perturbation':'epsilon*a times the same profile','T':1,'dt':.0005,
     'status':{name:rows[name].status for name in rows},'comparison':comparison,
     'scope':'One smooth finite perturbation, no stability theorem.'}
(ROOT/'out'/'perturbation.json').write_text(json.dumps(primitive(out),indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
