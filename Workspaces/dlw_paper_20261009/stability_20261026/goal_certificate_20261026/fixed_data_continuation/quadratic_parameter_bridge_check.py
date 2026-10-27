from pathlib import Path
import json
import sympy as s

mu,beta=s.symbols('mu beta',real=True)
checks={}
for n in range(1,6):
    xn=s.exp(-beta*n)*s.chebyshevt(2**n,mu)
    xp=s.exp(-beta*(n-1))*s.chebyshevt(2**(n-1),mu)
    val=s.exp(-beta*n)*xn-2*s.exp(-2*beta)*xp*xp+s.exp(-2*beta*n)
    checks['exact_matching_'+str(n)]=s.simplify(s.expand(val))==0
for n in range(2,6):
    N=2**n
    for m in range(2,min(10,N)+1,2):
        product=s.prod(N*N-(2*j)**2 for j in range(m//2))
        checks['chebyshev_product_'+str(N)+'_'+str(m)]=abs(s.diff(s.chebyshevt(N,mu),mu,m).subs(mu,0))==product
S=s.Rational(1,50);T=s.Rational(1,100);be=s.Rational(1,1000);theta=s.Rational(1,4)
checks['strict_holder_condition']=theta<(S-T)/(S+be/2)
checks['positive_gap']=S-T-theta*(S+be/2)>0
assert all(bool(v) for v in checks.values())
result={'date':'2026-10-26','checks':{k:bool(v) for k,v in checks.items()},'all_passed':True,
 'parameters':{'S':str(S),'T':str(T),'beta':str(be),'theta':str(theta)},
 'conclusion':'Quadratic Gaussian-output smoothing + injective derivative + continuous bounded real lift + interior Holder estimate does not imply finite-order Gevrey parameter regularity.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
