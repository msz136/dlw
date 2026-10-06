"""Exact cyclic N=3 mean-reduction test of the simple full-flow Q4."""
import sympy as s
from pathlib import Path
import json
z=s.symbols('z'); h=s.Rational(1); beta=h*h/32; N=3
D=lambda f:s.expand(z*s.diff(f,z))
Pi=lambda f:s.expand(sum(f)/N)
P=lambda f:[s.expand(v-Pi(f)) for v in f]
E=s.Matrix([[0,1,0],[0,0,1],[1,0,0]])
Proj=s.eye(N)-s.ones(N,N)/N
R=s.simplify(((s.eye(N)-E.inv())+s.ones(N,N)/N).inv()*(s.eye(N)+E.inv())*h/2*Proj)
Rp=lambda f:[s.expand(v) for v in R*s.Matrix(f)]
c=s.Rational(-4); gamma=s.Rational(0)
p=[z+1/z,2*z-1/z,-3*z]
r=[z-1/z,z+2/z,-2*z-1/z]
B=s.expand((gamma-Pi([p[i]*r[i] for i in range(N)]))/c)
U=[s.expand(B+v) for v in p]; w=[c+v for v in r]
A=Rp([D(v) for v in w])
HU=[s.expand(U[i]*w[i]-D(w[i])) for i in range(N)]
HW=[s.expand(U[i]**2/2+beta*w[i]**2+D(U[i])+A[i]) for i in range(N)]
pt=P([-D(v) for v in HW]); rt=P([-D(v) for v in HU])
Bt=s.expand(-Pi([pt[i]*r[i]+p[i]*rt[i] for i in range(N)])/c)
Ut=[s.expand(v+Bt) for v in pt]; wt=rt
QU=[s.expand(U[i]**2*w[i]+2*beta*w[i]**3/3-2*U[i]*D(w[i])+4*D(D(w[i]))/3+w[i]*A[i]) for i in range(N)]
rdUw=Rp([D(U[i]*w[i]) for i in range(N)])
QW=[s.expand(U[i]**3/3+2*beta*U[i]*w[i]**2+2*U[i]*D(U[i])+4*D(D(U[i]))/3+U[i]*A[i]+rdUw[i]) for i in range(N)]
deriv=s.expand(sum(QU[i]*Ut[i]+QW[i]*wt[i] for i in range(N)))
bracket=deriv.coeff(z,0)
lam=s.expand(Bt+Pi([D(v) for v in HW]))
full=s.expand(sum(QU[i]*(-D(HW[i]))+QW[i]*(-D(HU[i])) for i in range(N)))
out={'N':N,'h':str(h),'c':str(c),'gamma':str(gamma),'p':[str(v) for v in p],'r':[str(v) for v in r],
     'R':str(R),'Q4_reduced_time_derivative_trace':str(bracket),'full_flow_trace':str(full.coeff(z,0)),
     'mean_drift_lambda':str(lam),'identity_drift':bool(s.expand(deriv-full-lam*sum(QU))==0)}
print(json.dumps(out,indent=2))
Path(__file__).with_name('reduced_q4_counterexample.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
