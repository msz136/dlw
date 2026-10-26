"""Symbolic checks of the actual strip boundary terms and weak Lax relation."""
from pathlib import Path
import json
import sympy as s
x,z,t=s.symbols('x z t',real=True)
A,B=s.symbols('A B',real=True)
F=s.Function('F')(x);G=s.Function('H')(x)
k=s.pi/4
u0=A*s.sin(k*z)*F;v0=B*s.sin(k*z)*G
P0=(v0-s.diff(u0,z)-4)/4
moment=s.simplify(s.integrate(P0+1,(z,0,4)))
assert s.simplify(moment-B*G/(2*k))==0
top_u_t=s.simplify(-4*s.diff(moment,x,2))
top_V=s.simplify(-2*s.diff(moment,x))
assert s.simplify(top_u_t+2*B*s.diff(G,x,2)/k)==0
assert s.simplify(top_V+B*s.diff(G,x)/k)==0
U=s.Function('U')(x,z,t);P=s.Function('P')(x,z,t);V=s.Function('V')(x,z,t)
psi=s.Function('psi')(x,z,t)
def L(f): return s.diff(f,x,z)+U*s.diff(f,z)+P*f
def H(f): return -s.diff(f,x,2)+V*f
rhs=s.expand(H(L(psi))-L(H(psi))+2*s.diff(U,x)*L(psi))
rhs=rhs.subs(s.diff(V,x,z),-2*s.diff(P,x,2)).subs(s.diff(V,z),-2*s.diff(P,x))
expected=(s.diff(U**2-s.diff(U,x),x)-s.diff(V,x))*s.diff(psi,z)+(s.diff(P,x,2)+2*s.diff(U*P,x))*psi
assert s.simplify(rhs-expected)==0
out={'strip_moment':str(moment),'actual_top_u_t':str(top_u_t),'actual_top_V':str(top_V),
     'weak_lax_identity_checked':True,'transfer_operator_existence_proved':False,
     'original_initial_value_problem_certified':False,'eta_u':None,'eta_v':None}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
