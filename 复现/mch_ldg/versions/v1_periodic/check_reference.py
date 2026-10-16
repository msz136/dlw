"""Independent finite-difference check of analytic travelling-wave PDE residuals."""
import json
from pathlib import Path
import numpy as np
from mch.exact import profile

records=[]
for case,kap,alpha in [('5.1',0.,.5),('5.2',1.,.5)]:
    x=np.linspace(-10,10,151);d=.0005
    u,r=profile(case,x,.1,alpha=alpha,kappa=kap)
    deriv=lambda z:profile(case,z,.1,alpha=alpha,kappa=kap)[1]
    rm2,rm,rp,rp2=[deriv(x+j*d) for j in (-2,-1,1,2)]
    uxx=(rm2-8*rm+8*rp-rp2)/(12*d)
    uxxx=(-rp2+16*rp-30*r+16*rm-rm2)/(12*d*d)
    c=2/(1-alpha*alpha)+(1 if case=='5.1' else 0)
    residual=(u*u-r*r-c)*(r-uxxx)+2*r*(u-uxx)**2+2*kap*kap*r
    records.append(dict(case=case,pde_residual_max=float(np.max(abs(residual))),passed=bool(np.max(abs(residual))<1e-6)))
# Two-soliton: independent spacetime differences applied to m_t+flux_x.
case='5.3';x=np.linspace(-5,10,101);t=.13;d=.0002
def ur(x,t):return profile(case,x,t,kappa=1.)
def momentum(x,t):
    u,r=ur(x,t)
    rx=(ur(x+d,t)[1]-ur(x-d,t)[1])/(2*d)
    return u-rx
def flux(x,t):
    u,r=ur(x,t)
    return 2*u+(u*u-r*r)*momentum(x,t)
res=(momentum(x,t+d)-momentum(x,t-d))/(2*d)+(flux(x+d,t)-flux(x-d,t))/(2*d)
records.append(dict(case=case,pde_residual_max=float(np.max(abs(res))),passed=bool(np.max(abs(res))<.003),note='Finite difference derivatives near a steep alpha=.7 soliton; not an exact symbolic check.'))
Path('results/reference_validation.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print(json.dumps(records,indent=2));assert all(r['passed'] for r in records)
