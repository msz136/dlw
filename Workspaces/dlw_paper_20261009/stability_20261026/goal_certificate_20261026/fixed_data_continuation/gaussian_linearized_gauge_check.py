"""Exact identities for the actual Gaussian pure-carrier response obstruction."""
from pathlib import Path
import json
import sympy as s

x,z,t=s.symbols('x z t', real=True)
Q=s.Function('Q')(x,z,t);P=s.Function('P')(x,z,t)
R=P-s.diff(Q,z)
RP=s.diff(P,t)-s.diff(P,x,2)-2*s.diff(Q*P,x)
RQ=s.diff(Q,z,t)-s.diff(Q*Q-s.diff(Q,x),x,z)-2*s.diff(P,x,2)
defect=s.simplify(s.diff(R,t)+s.diff(R,x,2)-2*s.diff(Q*R,x)-(RP-RQ))

Phi=s.Function('Phi')(x,t);r=s.Function('r')(x,t);V=s.Function('V')(x,t)
Rlin=Phi*r;Qb=s.diff(Phi,x)/Phi
fp=s.diff(Rlin,t)+s.diff(Rlin,x,2)-2*s.diff(Qb*Rlin,x)
gauge=s.simplify(fp-Phi*(s.diff(r,t)+s.diff(r,x,2)+V*r)-r*(s.diff(Phi,t)-s.diff(Phi,x,2)-V*Phi))

W=s.Function('W')(x,t);h=s.Function('h')(x,t)
Th=s.diff(h,x)-W*h
inter=s.diff(Th,t)+s.diff(Th,x,2)+2*s.diff(W,x)*Th
free=s.diff(h,t)+s.diff(h,x,2)
inter=s.simplify(inter-(s.diff(free,x)-W*free)+(s.diff(W,t)+s.diff(W,x,2)+2*W*s.diff(W,x))*h)

lam=s.symbols('lam',positive=True)
f=s.Function('f')(z);F=s.Function('F')(x);C=s.Function('C')(x)
u=lam*f*F;v=4-3*s.diff(u,z)
P1=(v-4+s.diff(u,z))/4
checks={}
for label,du,dv in [('u_only',f*f*C,0),('v_only',0,f*f*C)]:
    dP=(dv+s.diff(du,z))/4
    dR=(dv+3*s.diff(du,z))/4+s.diff(dP/P1,x,z)
    if label=='u_only':
        a=3*f*s.diff(f,z)/2;b=s.diff(f,z)/lam
    else:
        a=f*f/4;b=s.diff(f*f/s.diff(f,z),z)/(2*lam)
    expected=a*C-b*s.diff(C/F,x)
    checks[label]=s.simplify(dR-expected)==0
    E=a*F*F*C-b*(F*s.diff(C,x)-C*s.diff(F,x))
    checks[label+'_cleared_identity']=s.simplify(F*F*expected-E)==0

alpha=s.symbols('alpha',positive=True)
trig=s.sin(alpha*z)
a_u=3*trig*s.diff(trig,z)/2
a_v=trig*trig/4
checks['u_a_at_z1']=s.simplify(a_u.subs({alpha:s.pi/4,z:1})-3*s.pi/16)==0
checks['v_a_at_z1']=s.simplify(a_v.subs({alpha:s.pi/4,z:1})-s.Rational(1,8))==0

result=dict(date='2026-10-26',defect_exact=defect==0,gauge_exact=gauge==0,
            time_dependent_darboux_exact=inter==0,initial_direction_checks=checks,
            statement='No classical first variation in either actual pure-carrier direction around certified Gaussian base under stated response regularity',
            fixed_nonzero_epsilon_nonexistence_proved=False,reference_certified=False)
result['all_passed']=all([result['defect_exact'],result['gauge_exact'],result['time_dependent_darboux_exact'],*checks.values()])
assert result['all_passed']
Path(__file__).with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
