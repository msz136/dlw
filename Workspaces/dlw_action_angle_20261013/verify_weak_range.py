"""Finite algebra checks for the weak-range note; no analytic theorem certification."""
import json
from pathlib import Path
import sympy as s

q1,p1,q2,p2,q3,p3,t=s.symbols('q1 p1 q2 p2 q3 p3 t')
z=s.Matrix([q1,p1,q2,p2,q3,p3])
I1=q1*p1
F=q2*p2+q3*p3
def grad(f): return s.Matrix([s.diff(f,x) for x in z])
def exterior(a):
    return s.Matrix(6,6,lambda i,j:s.diff(a[j],z[i])-s.diff(a[i],z[j]))
def zero(a): return all(s.simplify(v)==0 for v in a)
O=s.diag(*[s.Matrix([[0,s.Rational(1,n*n)],[-s.Rational(1,n*n),0]]) for n in (1,2,3)])
D=grad(I1)*grad(F).T-grad(F)*grad(I1).T
beta=(I1*grad(F)-F*grad(I1))/2
alt=-F*grad(I1)
phi=s.Matrix([s.exp(-F)*q1,s.exp(F)*p1,q2,p2,q3,p3])
J=phi.jacobian(z)
Xs=[s.Matrix([z[j] if j==2*k else -z[j] if j==2*k+1 else 0 for j in range(6)]) for k in range(3)]
# i_V Omega has coefficient column Omega.T*V under the note's convention.
V=-O.T.inv()*beta
checks={
    'radial_primitive_sign':zero(exterior(beta)-D),
    'alternative_primitive_sign':zero(exterior(alt)-D),
    'all_three_generator_horizontal_identities':all(zero(D.T*X) for X in Xs),
    'explicit_map_pullback':zero(J.T*O*J-O-D),
    'radial_field_finite_contraction':zero((O+t*D).T*V+beta),
}
assert all(checks.values()),checks
out={'scope':'Exact finite algebra only; not the infinite range failure or DLW criterion verification.',
     'checks':checks,'passed':len(checks)}
Path(__file__).with_name('weak_range_validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out))
