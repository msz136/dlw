"""Audit natural densities and isolate initial mesh differentiation/recovery defects."""
import json
from pathlib import Path
import numpy as np
import sympy as s
from natural_density_search import monitor_flux, reference, ale, ROOT

OUT=ROOT/'data/density_insights'; OUT.mkdir(exist_ok=True)
kinds=['rho','deficit','momentum','curvature_deficit','energy','rm','hierarchy2','spectral_plus','spectral_minus']
u,w,m,r,g,mx,gx=s.symbols('u w m r g mx gx', nonzero=True)
D={w:w*w/2+4*u+(r*r-1)/2,m:2*w*m+r*g,r:r*w,g:r*(m-2)+2*w*g}
X={u:w,w:m-2,m:mx,r:g,g:gx}
checks={}
for kind in kinds:
    R,Q=monitor_flux(kind,m,r,u,w,g)
    residual=s.simplify(sum(s.diff(R,v)*d for v,d in D.items())-w*R+sum(s.diff(Q+u*R,v)*d for v,d in X.items()))
    checks[kind]=str(residual)
    assert residual==0,(kind,residual)

rows=[]
for p in [(5.,),(1.1,1.25)]:
    sol=ale.Soliton(p)
    dense=np.linspace(-4,4,100001)
    ud,rd,md,_=reference(sol,dense,0)
    labels=sol.continuous_x(dense,0)[2]
    wt,o,b=sol._weights(labels,0)
    o=o-np.sum(wt*o,axis=0); b=b-np.sum(wt*b,axis=0)
    wd=np.sum(wt*o*o*b,axis=0)*rd
    gd=np.sum(wt*o*b*b,axis=0)*rd**3
    for kind in ['fixed']+kinds:
        R,_=monitor_flux(kind,md,rd,ud,wd,gd)
        mass=np.r_[0,np.cumsum((R[1:]+R[:-1])*np.diff(dense)/2)]
        x=np.interp(np.linspace(0,mass[-1],1000),mass,dense)
        ue,re,me,_=reference(sol,x,0)
        defect=ale.second_derivative(ue,x)-(me[1:-1]-2)
        recovered=ale.poisson(x,me,ue[0],ue[-1])
        h=np.diff(x); mask=abs(x)<=2.5
        rows.append(dict(p=list(p),kind=kind,min_R=float(min(R)),max_R=float(max(R)),
          mesh_ratio=float(max(h)/min(h)),max_adjacent_ratio=float(max(np.maximum(h[1:]/h[:-1],h[:-1]/h[1:]))),
          D2_defect=float(max(abs(defect[mask[1:-1]]))),
          isolated_poisson_error=float(max(abs((recovered-ue)[mask])))))

raw=[]
for name in ['results','curvature_deficit','hierarchy2','spectral_branches']:
    raw+=json.loads((ROOT/f'data/natural_density_search/{name}.json').read_text())
orders=[]
for p in [(5.,),(1.1,1.25)]:
    for kind in ['fixed']+kinds:
        group={z['nodes']:z for z in raw if z.get('p')==list(p) and z['kind']==kind}
        if 1000 in group and 2000 in group:
            orders.append(dict(p=list(p),kind=kind,**{q:float(np.log(group[1000][q]/group[2000][q])/np.log(1999/999)) for q in ['u','rho']}))
(OUT/'analysis.json').write_text(json.dumps(dict(conservation_residuals_c1=checks,initial_diagnostics=rows,observed_orders=orders),indent=2))
print(json.dumps({'conservation_checks':checks,'observed_order_range':[min(z[q] for z in orders for q in ['u','rho']),max(z[q] for z in orders for q in ['u','rho'])],'initial_diagnostics':rows},indent=2))
