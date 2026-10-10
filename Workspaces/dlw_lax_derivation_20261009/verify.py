from pathlib import Path
import json
import sympy as s

HERE=Path(__file__).resolve().parent
x,t=s.symbols('x t')
h,c=s.symbols('h c', nonzero=True)
U,w,r,e,V=[s.Function(n)(x,t) for n in ['U','w','r','e','V']]
alpha=U/2+h*w/8
eta=U/2-h*w/8
Ea=s.diff(alpha,t)+s.diff(alpha,x,2)+2*alpha*s.diff(alpha,x)+s.diff(V,x)
Eb=s.diff(eta,t)+s.diff(eta,x,2)+2*eta*s.diff(eta,x)+s.diff(V,x)+h*s.diff(w,x,2)/2
checks={}
checks['riccati_difference']=s.expand(Ea-Eb-h/4*(s.diff(w,t)-s.diff(w,x,2)+s.diff(U*w,x)))==0
expected_sum=s.diff(U,t)+s.diff(U**2/2+h**2*w**2/32,x)+s.diff(U,x,2)+h*s.diff(w,x,2)/2+2*s.diff(V,x)
checks['riccati_sum']=s.expand(Ea+Eb-expected_sum)==0
ut=-s.diff(U**2/2+h**2*w**2/32+s.diff(U,x)+r,x)+2*s.diff(e,x)/c
vx=s.diff(r,x)/2-h*s.diff(w,x,2)/4-s.diff(e,x)/c
checks['physical_source_cancellation']=s.expand(expected_sum.subs({s.diff(U,t):ut,s.diff(V,x):vx}))==0
# Finite differential-operator multiplication checks the full Darboux defect.
def multiply(left,right):
    result={}
    for i,a in left.items():
        for j,b in right.items():
            for k in range(i+1):
                order=i+j-k
                result[order]=result.get(order,0)+s.binomial(i,k)*a*s.diff(b,x,k)
    return result
factor={1:s.Integer(1),0:-r}
heat_in={2:s.Integer(1),0:V}
heat_out={2:s.Integer(1),0:V+2*s.diff(r,x)}
left=multiply(heat_out,factor)
right=multiply(factor,heat_in)
defect={k:s.expand(left.get(k,0)-right.get(k,0)) for k in set(left)|set(right)}
defect[0]-=s.diff(r,t)
expected=-(s.diff(r,t)+s.diff(r,x,2)+2*r*s.diff(r,x)+s.diff(V,x))
checks['full_darboux_operator_identity']=all(s.expand(v-(expected if k==0 else 0))==0 for k,v in defect.items())
for n in range(2,7):
    gs=s.symbols(f'g0:{n}')
    us=s.symbols(f'U0:{n}')
    gxs=s.symbols(f'gx0:{n}')
    product_second=sum(gxs[j]-(us[j]/2-gs[j]/2)*gs[j] for j in range(n))+sum(gs[j]*gs[k] for j in range(n) for k in range(j))
    normalized_second=sum(gs)**2/2-sum(us[j]*gs[j] for j in range(n))/2+sum(gxs)
    checks[f'monodromy_second_coefficient_M{n}']=s.expand(product_second-normalized_second)==0
# The finite lattice identities used in the heat-potential reconstruction.
for n in range(2,9):
    shift=s.zeros(n)
    for j in range(n):shift[j,(j+1)%n]=1
    proj=s.eye(n)-s.ones(n)/n
    q=s.Matrix(n,n,lambda j,k:h if k<j else h/2 if k==j else 0)
    R=proj*q*proj
    delta=(s.eye(n)-shift.T)/h
    avg=(s.eye(n)+shift.T)/2
    checks[f'R_identity_M{n}']=s.simplify(delta*R-avg*proj)==s.zeros(n)
    checks[f'R_skew_M{n}']=R+R.T==s.zeros(n)
    checks[f'potential_shift_M{n}']=s.simplify((shift-s.eye(n))*(R/2-h*s.eye(n)/4)-h*proj/2)==s.zeros(n)
# Conservation of Pi(Uw) determines lambda; compare independent field jets.
n=3
u=s.Matrix([s.Function(f'u{j}')(x,t) for j in range(n)])
v=s.Matrix([s.Function(f'w{j}')(x,t) for j in range(n)])
proj=s.eye(n)-s.ones(n)/n
q=s.Matrix(n,n,lambda j,k:h if k<j else h/2 if k==j else 0)
R=proj*q*proj
rv=R*v.diff(x)
energy=sum(u[j]**2*v[j]/2+h**2*v[j]**3/96+v[j]*s.diff(u[j],x)+v[j]*rv[j]/2 for j in range(n))/n
mean_rate=sum(v[j]*(-s.diff(u[j]**2/2+h**2*v[j]**2/32+s.diff(u[j],x)+rv[j],x))+u[j]*(s.diff(v[j],x,2)-s.diff(u[j]*v[j],x)) for j in range(n))/n
checks['mean_product_identity']=s.expand(mean_rate+2*s.diff(energy,x)-s.diff(sum(u[j]*v[j] for j in range(n))/n,x,2))==0
assert all(checks.values()), checks
(HERE/'symbolic_validation.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(f'{len(checks)} exact symbolic checks passed')
