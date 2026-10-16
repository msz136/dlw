"""Exact finite model for Liouville averaging, not an infinite DLW proof."""
import json
from pathlib import Path
import sympy as s
q,p,z,a=s.symbols('q p z a',nonzero=True)
x=s.Matrix([q,p]); O=s.Matrix([[0,1],[-1,0]])
T=s.Matrix([q,p+q*q])
Phi=s.Matrix([z*q,(p+q*q)/z-z*z*q*q])
pulled=Phi.jacobian(x).inv()*Phi
average=pulled.applyfunc(lambda v:s.expand(v).coeff(z,0))
W=s.Matrix([q,p-q*q])
psi=s.Matrix([a*q,a*(p+q*q*(1-a))])
Xi=s.Matrix([q,p+q*q*(1-a)])
def sub(v,y):return v.subs({q:y[0],p:y[1]},simultaneous=True)
def zero(v):return all(s.simplify(y)==0 for y in v)
checks={
 'Euler_pullback_average':zero(average-W),
 'Liouville_scaling':zero(W.jacobian(x).T*O+O*W.jacobian(x)-2*O),
 'negative_flow_equation':zero(-a*psi.diff(a)+sub(W,psi)),
 'each_rescaled_map_symplectic':zero(Xi.jacobian(x).T*O*Xi.jacobian(x)-O),
 'limit_symplectic_conjugacy':zero(sub(T,Phi)-s.diag(z,1/z)*T) and zero(T.jacobian(x).T*O*T.jacobian(x)-O),
}
assert all(checks.values()),checks
out={'scope':'Finite polynomial canonical conjugacy: algebra only; no verification of the infinite analytic DLW inputs.',
     'checks':checks,'passed':len(checks)}
Path(__file__).with_name('liouville_average_validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out))
