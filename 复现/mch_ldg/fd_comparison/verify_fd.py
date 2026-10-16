"""Independent Fourier-symbol, consistency, and conservation checks."""
import json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from mch.exact import profile
from fd import DirectFD
from fd_rusanov import RusanovFD

rows=[]
def check(name,value,tol):rows.append(dict(name=name,value=float(value),tolerance=tol,passed=bool(value<tol)))
for order in (2,4):
    d=DirectFD(63,-np.pi,np.pi,kappa=.6,order=order)
    theta=3*d.x;u=np.cos(theta)
    symbol=-(4*np.sin(3*d.h/2)**2/d.h**2) if order==2 else (-2*np.cos(6*d.h)+32*np.cos(3*d.h)-30)/(12*d.h**2)
    check(f'D2 symbol FD{order}',max(abs(d.d2(u)-symbol*u)),1e-10)
    check(f'Helmholtz FD{order}',max(abs(d.helmholtz(d.momentum(u))-u)),1e-11)
    u=1+.1*np.sin(d.x)+.03*np.cos(3*d.x)
    check(f'mass FD{order}',abs(d.mass(d.rhs(u))),1e-11)
    check(f'constant FD{order}',max(abs(d.rhs(np.ones(d.n)))),1e-11)
    errors=[]
    for n in (64,128,256):
        z=DirectFD(n,-np.pi,np.pi,order=order)
        e=max(abs(z.d1(np.sin(z.x))-np.cos(z.x)));errors.append(e)
    obs=np.log2(errors[-2]/errors[-1]);check(f'D1 order FD{order}',abs(obs-order),.03)
    # Smooth travelling-wave RHS consistency away from exponentially small tails.
    errors=[]
    for n in (128,256,512):
        z=DirectFD(n,-60.,60.,order=order)
        uu,rr=profile('5.1',z.x,0,alpha=.5,kappa=0.)
        truth=-(1+2/(1-.5**2))*rr
        errors.append(np.sqrt(z.h*np.sum((z.rhs(uu)-truth)**2)))
    obs=np.log2(errors[-2]/errors[-1]);check(f'full smooth RHS order FD{order}',abs(obs-order),.4)
d=RusanovFD(64,-np.pi,np.pi,order=2)
u=1+.1*np.sin(d.x)
check('Rusanov mass',abs(d.mass(d.rhs(u))),1e-11)
check('Rusanov constant',max(abs(d.rhs(np.ones(d.n)))),1e-11)
errors=[]
for n in (256,512,1024):
    z=RusanovFD(n,-60.,60.,order=2)
    uu,rr=profile('5.1',z.x,0,alpha=.5,kappa=0.)
    errors.append(np.sqrt(z.h*np.sum((z.rhs(uu)+(1+2/(1-.5**2))*rr)**2)))
check('Rusanov full smooth RHS first order',abs(np.log2(errors[-2]/errors[-1])-1),.15)
out=dict(total=len(rows),passed=sum(r['passed'] for r in rows),checks=rows)
Path('verification.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2));assert all(r['passed'] for r in rows)
