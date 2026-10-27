"""Exact cancellation checks for the current Gaussian inverse-Laplace jets."""
from pathlib import Path
import json
import sympy as s

x,z,t=s.symbols('x z t',real=True)
Q=s.Function('Q')(x,z,t)
P=s.Function('P')(x,z,t)
P2=P-s.diff(Q,z)
P_t=s.diff(P,x,2)+2*s.diff(Q*P,x)
Q_zt=s.diff(Q**2-s.diff(Q,x),x,z)+2*s.diff(P,x,2)
invariant=s.expand(P_t-Q_zt+s.diff(P2,x,2)-2*s.diff(Q*P2,x))
assert s.simplify(invariant)==0

g=s.Function('g')(x,t);h=s.Function('h')(x,t)
heat={s.diff(g,t):-s.diff(g,x,2),s.diff(h,t):-s.diff(h,x,2)}
q=s.diff(h/g,x)
q_equation=s.diff(q,t)+s.diff(q,x,2)+2*s.diff(s.diff(g,x)/g*q,x)
q_equation=q_equation.subs(s.diff(g,x,t),-s.diff(g,x,3)).subs(s.diff(h,x,t),-s.diff(h,x,3)).subs(heat)
assert s.simplify(q_equation)==0
square=s.diff(h*h/g,t)+s.diff(h*h/g,x,2)-2*g*q*q
assert s.simplify(square.subs(heat))==0
wronskian=2*g*g*q-2*(g*s.diff(h,x)-h*s.diff(g,x))
assert s.simplify(wronskian)==0

alpha,lam,eps,k=s.symbols('alpha lam eps k',real=True)
F=s.Function('F')(x)
u0=lam*s.sin(alpha*z)*F+eps*s.sin(alpha*z)**2*s.cos(k*x)
v0=4-3*lam*alpha*s.cos(alpha*z)*F
P10=(v0-4+s.diff(u0,z))/4
P00=(v0-4-s.diff(u0,z))/4
g0=-lam*alpha*F/2;h0=eps*alpha**2*s.cos(k*x)/2
assert s.simplify(P10.subs(z,0)-g0)==0
assert s.simplify(s.diff(P10,z).subs(z,0)-h0)==0
assert s.simplify(s.diff(P00,z).subs(z,0)+h0)==0
assert s.simplify(s.diff(P10,z,2).subs(z,0)+alpha**2*g0)==0
log_second=s.diff(P10,z,2)/P10-(s.diff(P10,z)/P10)**2
assert s.simplify(log_second.subs(z,0)+alpha**2+(h0/g0)**2)==0

result={'inverse_invariant_equation':True,'first_boundary_ratio_equation':True,
        'quadratic_heat_quotient_identity':True,'remaining_wronskian_forcing':True,
        'actual_initial_boundary_coefficients':True,'all_passed':True,
        'continuous_reference_certified':False,
        'meaning':'Exact low-jet cancellation; no all-order/nonexistence/reference conclusion.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
