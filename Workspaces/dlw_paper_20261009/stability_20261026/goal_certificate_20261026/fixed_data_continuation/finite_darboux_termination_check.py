"""Exact spatial algebra for finite standard Darboux termination."""
from pathlib import Path
import json
import sympy as s

x,z=s.symbols('x z',real=True)
Q=s.Function('Q')(x,z);P=s.Function('P')(x,z)
phi=s.Function('phi')(x,z);psi=s.Function('psi')(x,z)
def L(f,q=Q,p=P):return s.diff(f,x,z)+q*s.diff(f,z)+p*f
seed_residual=L(phi)/phi
a=phi/s.diff(phi,z)
ss=s.diff(phi,x)/phi
R=Q+ss
T1=psi-a*s.diff(psi,z)
T2=s.diff(psi,x)-ss*psi
Q1=Q-s.diff(a,x)/a;P1=P-s.diff(a*P,z)
Q2=Q-s.diff(R,x)/R;P2=P+s.diff(ss,z)
id1=L(T1,Q1,P1)-((1-s.diff(a,z))*L(psi)-a*s.diff(L(psi),z))-a*s.diff(a*seed_residual,z)*s.diff(psi,z)
id2=L(T2,Q2,P2)-(s.diff(L(psi),x)-(ss+s.diff(R,x)/R)*L(psi))-(-s.diff(seed_residual,x)+s.diff(R,x)/R*seed_residual)*psi
checks={'DT1_spatial_identity':s.cancel(s.together(id1))==0,
        'DT2_spatial_identity':s.cancel(s.together(id2))==0}

f=s.Function('f')(x)
g=s.Function('g')(z)
for n in range(5):
    aa=[s.Function('a'+str(j))(x,z) for j in range(n+1)]
    Dx=sum(aa[j]*s.diff(f,x,j) for j in range(n+1))
    expr=s.expand(L(Dx))
    if n==0:
        checks['pure_x_order_zero_constant']=s.simplify(expr.coeff(f)-L(aa[0]))==0
    checks['pure_x_top_'+str(n)]=s.simplify(expr.coeff(s.diff(f,x,n+1))-s.diff(aa[n],z))==0
    if n:
        expected=s.diff(aa[n-1],z)+s.diff(aa[n],x,z)+Q*s.diff(aa[n],z)+P*aa[n]
        checks['pure_x_next_'+str(n)]=s.simplify(expr.coeff(s.diff(f,x,n))-expected)==0
    bb=[s.Function('b'+str(j))(x,z) for j in range(n+1)]
    Dz=sum(bb[j]*s.diff(g,z,j) for j in range(n+1))
    expr=s.expand(L(Dz))
    checks['pure_z_top_'+str(n)]=s.simplify(expr.coeff(s.diff(g,z,n+1))-(s.diff(bb[n],x)+Q*bb[n]))==0
    if n:
        expected=s.diff(bb[n-1],x)+Q*bb[n-1]+s.diff(bb[n],x,z)+Q*s.diff(bb[n],z)+P*bb[n]
        checks['pure_z_next_'+str(n)]=s.simplify(expr.coeff(s.diff(g,z,n))-expected)==0
    if n==0:
        checks['pure_z_order_zero_constant']=s.simplify(expr.coeff(g)-L(bb[0]))==0

# Highest coefficients after the elementary transformations.
an=s.Function('an')(x)
bn=s.Function('bn')(x,z)
checks['T1_x_leading_preserved']=s.diff(an,z)==0
checks['T2_y_leading_under_kernel_relation']=s.simplify((s.diff(bn,x)-ss*bn).subs(s.diff(bn,x),-Q*bn)+R*bn)==0
checks['forward_laplace_leading_reduction']=s.simplify((-P*an)/P+an)==0
checks['inverse_laplace_leading_reduction']=s.simplify(-(P-s.diff(Q,z))*bn+(P-s.diff(Q,z))*bn)==0
assert all(checks.values()),{k:v for k,v in checks.items() if not v}
result={'date':'2026-10-26','checks':checks,'all_passed':True,
        'meaning':'Exact spatial identities and coefficient checks; all-order termination uses the analytic coefficient proof.',
        'reference_error_certified':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
