import json,math,sys
from pathlib import Path
import numpy as np
from fd3 import ThirdOrderFD
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from mch.exact import profile

rows=[]
def check(name,value,tol):rows.append(dict(name=name,value=float(value),tol=tol,passed=bool(value<tol)))
# Exact rational stencil moments: d/dx upwind is third order.
for side,offsets,weights in [('left',[-2,-1,0,1],[1,-6,3,2]),('right',[-1,0,1,2],[-2,-3,6,-1])]:
    for power in range(4):
        value=sum(w*j**power for j,w in zip(offsets,weights))
        check(f'{side} stencil moment {power}',abs(value-(6 if power==1 else 0)),.1)
errors=[]
for n in [128,256,512]:
    d=ThirdOrderFD(n,-np.pi,np.pi)
    err=max(abs(d.upwind_left(np.sin(d.x))-np.cos(d.x)));errors.append(err)
check('first derivative third order',abs(np.log2(errors[-2]/errors[-1])-3),.03)
d=ThirdOrderFD(63,-np.pi,np.pi,kappa=.6)
u=1+.1*np.sin(d.x)+.03*np.cos(3*d.x)
check('Helmholtz inverse',max(abs(d.helmholtz(d.momentum(u))-u)),1e-11)
check('mass conservation',abs(d.mass(d.rhs(u))),1e-11)
check('constant state',max(abs(d.rhs(np.ones(d.n)))),1e-11)
m=d.momentum(u);r=d.d1(u);a=u*u-r*r;speed=max(abs(a));F=2*d.kappa**2*u+a*m
q4=np.roll(m,2)-4*np.roll(m,1)+6*m-4*np.roll(m,-1)+np.roll(m,-2)
rhs2=d.helmholtz(-d.d1(F)-speed*q4/(12*d.h))
check('split equals central fourth plus h3 dissipation',max(abs(d.rhs(u)-rhs2)),1e-11)
errors=[]
for n in [256,512,1024]:
    z=ThirdOrderFD(n,-60.,60.)
    uu,rr=profile('5.1',z.x,0,alpha=.5,kappa=0.)
    errors.append(np.sqrt(z.h*np.sum((z.rhs(uu)+(1+2/(1-.5**2))*rr)**2)))
obs=float(np.log2(errors[-2]/errors[-1]));check('full RHS third order',abs(obs-3),.15)
out=dict(total=len(rows),passed=sum(r['passed'] for r in rows),rhs_errors=errors,rhs_observed_order=obs,checks=rows)
Path('verification_third.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2));assert all(r['passed'] for r in rows)
