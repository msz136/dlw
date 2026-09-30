"""Finite-a exact-soliton model error versus lattice spacing, p and time."""
import json
from pathlib import Path
import numpy as np
from hs_exact import Soliton

ROOT = Path(__file__).resolve().parent
rows=[]
for p in (4.5,5.,5.5):
    ref=Soliton((p,))
    for T in (0.,.25,.5,1.):
        for a in (.04,.02,.01,.005):
            k=np.arange(round(-4/a),round(4/a)+1)
            sd=ref.lattice_state(k,a,T)
            uc=ref.continuous_x(sd['x'],T)[0]
            rc=ref.continuous_density_cell_mean(sd['x'][:-1],sd['x'][1:],T)
            rows.append({'p':p,'T':T,'a':a,'u_linf':float(max(abs(sd['u']-uc))),
                         'rho_linf':float(max(abs(sd['rho']-rc))),
                         'u_per_a':float(max(abs(sd['u']-uc))/a),
                         'rho_per_a':float(max(abs(sd['rho']-rc))/a),
                         'min_d':float(min(sd['d']))})
c_rows=[]
for c in (.9,1.,1.1):
    ref=Soliton((5.,),c=c)
    a=.02;T=.5;k=np.arange(-200,201)
    sd=ref.lattice_state(k,a,T)
    uc=ref.continuous_x(sd['x'],T)[0]
    rc=ref.continuous_density_cell_mean(sd['x'][:-1],sd['x'][1:],T)
    c_rows.append({'c':c,'p':5.,'a':a,'T':T,
                   'u_linf':float(max(abs(sd['u']-uc))),
                   'rho_linf':float(max(abs(sd['rho']-rc)))})
(ROOT/'out'/'model_factor.json').write_text(json.dumps({
    'definition':'Finite-a exact one-soliton versus continuous exact solution at the same physical nodes, with continuous density averaged over exact edges.',
    'rows':rows,'c_scan':c_rows},indent=2),encoding='utf-8')
print('Wrote model_factor.json',len(rows),'spacing/shape/time cases and',len(c_rows),'c cases')
