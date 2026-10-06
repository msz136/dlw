"""Exact nonperiodic inverse / relative-variation / tangency checks.

The Hilbert-domain and Poisson statements are analytic proofs in the report,
not conclusions from these finite algebraic checks. No PDE trajectories.
"""
from pathlib import Path
import json
import sympy as s

HERE=Path(__file__).resolve().parent
x=s.symbols('x',real=True)
h,beta,eps=s.symbols('h beta eps',real=True,nonzero=True)
checks=[]
def zero(name,expr):
    out=s.simplify(s.expand(expr))
    checks.append({'name':name,'passed':out==0})
    if out!=0: raise AssertionError((name,out))

def R(seq,j):
    return h*s.Rational(1,2)*sum((1 if k<j else -1 if k>j else 0)*v for k,v in seq.items())
seqs=[{-2:s.Integer(2),0:s.Integer(-3),3:s.Integer(1)},
      {-2:s.Integer(2),0:s.Integer(-3),3:s.Integer(5)}]
for k,seq in enumerate(seqs):
    for j in range(-4,6):
        zero(f'sequence{k}: dR=M at j={j}',(R(seq,j)-R(seq,j-1))/h
             -(seq.get(j,0)+seq.get(j-1,0))/2)
    zero(f'sequence{k}: right tail',R(seq,10)-h*sum(seq.values())/2)
    zero(f'sequence{k}: left tail',R(seq,-10)+h*sum(seq.values())/2)
f,g=seqs
zero('skew kernel pair',sum(v*R(g,j) for j,v in f.items())
     +sum(v*R(f,j) for j,v in g.items()))
zero('zero sum inverse finite-tail support',R(f,10))

p,r,Ub,wb=[s.Function(n)(x) for n in ('p','r','Ub','wb')]
local=wb*p*p/2+Ub*p*r+p*p*r/2+beta*wb*r*r+beta*r**3/3+r*s.diff(p,x)
gp=s.diff(local,p)-s.diff(s.diff(local,s.diff(p,x)),x)
gr=s.diff(local,r)
zero('relative U gradient',gp-(wb*p+Ub*r+p*r-s.diff(r,x)))
zero('relative w local gradient',gr-(Ub*p+p*p/2+2*beta*wb*r+beta*r*r+s.diff(p,x)))
zero('U gradient as difference',(Ub+p)*(wb+r)-s.diff(wb+r,x)
     -(Ub*wb-s.diff(wb,x))-gp)
zero('w gradient as local difference',(Ub+p)**2/2+beta*(wb+r)**2+s.diff(Ub+p,x)
     -(Ub**2/2+beta*wb**2+s.diff(Ub,x))-gr)

theta,xi=s.symbols('theta xi',real=True)
zeta=s.symbols('zeta',nonzero=True)
dk=(1-1/zeta)/h
mk=(1+1/zeta)/2
K=h*s.Rational(1,2)*xi*s.cot(theta/2)
Klaurent=s.I*xi*h*(zeta+1)/(2*(zeta-1))
zero('spectral dK=MD',s.cancel(dk*Klaurent-mk*s.I*xi))
zero('K multiplier real',s.im(K))

# Necessary compatibility fails even when the first two constraints hold.
f=s.Function('f')(x)
c,U0=s.symbols('c U0',real=True,nonzero=True)
pv=[f,-f]
ut=[-s.diff(U0*z+z*z/2,x)-s.diff(z,x,2) for z in pv]
wt=[-c*s.diff(z,x) for z in pv]
flux_t=sum(c*ut[j]+(U0+pv[j])*wt[j] for j in range(2))
zero('vacuum constraints hold',c*sum(pv))
zero('vacuum flux tangency obstruction',flux_t+c*s.diff(sum(z*z for z in pv),x))

# Exact quadratic obstruction around any benchmark background, two sites.
U=[s.Function(f'U{j}')(x) for j in range(2)]
w=[s.Function(f'w{j}')(x) for j in range(2)]
pt=[w[1]*f,-w[0]*f]
zero('background perturbation flux constraint',sum(w[j]*pt[j] for j in range(2)))
delta_ut=[-s.diff(U[j]*eps*pt[j]+eps**2*pt[j]**2/2,x)-eps*s.diff(pt[j],x,2) for j in range(2)]
delta_wt=[-eps*s.diff(w[j]*pt[j],x) for j in range(2)]
flux_rate=sum(w[j]*delta_ut[j]+U[j]*delta_wt[j]+eps*pt[j]*delta_wt[j] for j in range(2))
quadratic=s.expand(flux_rate).coeff(eps,2)
zero('background quadratic obstruction',quadratic+s.diff(sum(w[j]*pt[j]**2 for j in range(2)),x))
zero('background explicit obstruction',sum(w[j]*pt[j]**2 for j in range(2))
     -w[0]*w[1]*(w[0]+w[1])*f*f)

coefficient_derivative=s.diff(wb,x)*p*p/2+s.diff(Ub,x)*p*r+beta*s.diff(wb,x)*r*r
zero('relative momentum bracket, modulo exact derivative',s.diff(p,x)*gp+s.diff(r,x)*gr
     +coefficient_derivative-s.diff(local-r*s.diff(p,x),x))
speed=s.symbols('speed',real=True)
partial_time=-speed*s.diff(wb,x)*p*p/2-speed*s.diff(Ub,x)*p*r-speed*beta*s.diff(wb,x)*r*r
zero('traveling relative Hamilton time correction',partial_time+speed*coefficient_derivative)
ps,qs=s.symbols('ps qs',real=True)
zero('single line x speed',(ps*ps-qs*qs)/(ps+qs)-(ps-qs))

result={'passed':all(c['passed'] for c in checks),'count':len(checks),'checks':checks,
        'scope':'Exact algebra. General dense Hilbert-domain Hamilton theorem and Jacobi proved analytically.'}
(HERE/'relative_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':result['passed'],'count':result['count']}))
