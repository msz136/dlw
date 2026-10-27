"""Independent exact symbolic checks of the full nonlinear residual counterexample."""
from pathlib import Path
import json
import sympy as s

x,z,t=s.symbols('X z t', real=True)
U,V,d=[s.Function(name)(x,z,t) for name in ['U','V','d']]
def residual(u,v):
    return (s.diff(u,z,t)+s.diff(v,x,2)+s.diff(u*s.diff(u,z),x),
            s.diff(v,t)+s.diff(u,x,2,z)+s.diff(u*v,x)-4*s.diff(u,x))
def transformed(u,v):
    a=s.diff(u,z)+v; b=s.diff(u,z)-v
    return (s.diff(a,t)+s.diff(a,x,2)+s.diff(u*a,x)-4*s.diff(u,x),
            s.diff(b,t)-s.diff(b,x,2)+s.diff(u*b,x)+4*s.diff(u,x))
R1,R2=residual(U,V); Ra,Rb=transformed(U,V)
checks={
 'physical_R1':s.simplify(2*R1-Ra-Rb)==0,
 'physical_R2':s.simplify(2*R2-Ra+Rb)==0,
}
e=s.diff(d,z); A0=s.diff(U,z)+V; B0=s.diff(U,z)-V
Rap,Rbp=transformed(U+d,V+e)
Da=2*s.diff(e,t)+2*s.diff(e,x,2)+s.diff(2*U*e+d*A0+2*d*e,x)-4*s.diff(d,x)
Db=s.diff(d*B0,x)+4*s.diff(d,x)
checks['nonlinear_delta_Ra']=s.simplify(s.expand(Rap-Ra-Da))==0
checks['nonlinear_delta_Rb']=s.simplify(s.expand(Rbp-Rb-Db))==0

eps=s.symbols('epsilon',real=True)
W=s.Function('W')(z); chi=s.Function('chi')(t); phi=s.Function('phi')(x,t); Us=s.Function('Ustar')(x,t)
dd=eps*W*chi*phi; ee=s.diff(dd,z)
evaluated=Da.subs(d,dd).doit().subs(s.diff(phi,t),-s.diff(phi,x,2)-s.diff(Us*phi,x)).doit()
expected=(2*eps*s.diff(W,z)*s.diff(chi,t)*phi
 +2*eps*s.diff(W,z)*chi*((U-Us)*s.diff(phi,x)+(s.diff(U,x)-s.diff(Us,x))*phi)
 +eps*W*chi*(s.diff(A0,x)*phi+(A0-4)*s.diff(phi,x))
 +4*eps**2*W*s.diff(W,z)*chi**2*phi*s.diff(phi,x))
checks['transport_cancellation']=s.simplify(s.expand(evaluated-expected))==0
checks['all_passed']=all(checks.values())
out=Path(__file__).with_suffix('.json')
out.write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
assert checks['all_passed']
