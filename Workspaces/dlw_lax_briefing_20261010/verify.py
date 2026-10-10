from pathlib import Path
import json
import sympy as s
HERE=Path(__file__).resolve().parent
x,t=s.symbols('x t')
h=s.symbols('h',nonzero=True)
U,w,Un,wn,V,r=[s.Function(n)(x,t) for n in ['U','w','Un','wn','V','r']]
F=U**2/2+h**2*w**2/32
Fn=Un**2/2+h**2*wn**2/32
S=s.diff(U,t)+s.diff(F,x)+s.diff(U,x,2)+h*s.diff(w,x,2)/2
Sn=s.diff(Un,t)+s.diff(Fn,x)+s.diff(Un,x,2)+h*s.diff(wn,x,2)/2
N1=(s.diff(Un-U,t)+s.diff(Fn-F,x))/h+s.diff((Un-U)/h+(wn+w)/2,x,2)
checks={'potential_integrability':s.expand(Sn-S+h*s.diff(w,x,2)-h*N1)==0}
alpha=U/2+h*w/8
eta=U/2-h*w/8
Ea=s.diff(alpha,t)+s.diff(alpha,x,2)+2*alpha*s.diff(alpha,x)+s.diff(V,x)
Eb=s.diff(eta,t)+s.diff(eta,x,2)+2*eta*s.diff(eta,x)+s.diff(V,x)+h*s.diff(w,x,2)/2
checks['riccati_difference']=s.expand(Ea-Eb-h/4*(s.diff(w,t)-s.diff(w,x,2)+s.diff(U*w,x)))==0
checks['riccati_sum']=s.expand(Ea+Eb-S-2*s.diff(V,x))==0
physical={s.diff(V,x):-S/2,s.diff(w,t):s.diff(w,x,2)-s.diff(U*w,x)}
checks['alpha_residual_zero']=s.expand(Ea.subs(physical,simultaneous=True))==0
checks['eta_residual_zero']=s.expand(Eb.subs(physical,simultaneous=True))==0
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
checks['full_darboux_identity']=all(s.expand(v-(expected if k==0 else 0))==0 for k,v in defect.items())
checks['common_intermediate_heat_potential']=s.expand(2*s.diff(alpha-eta,x)-h*s.diff(w,x)/2)==0
assert all(checks.values()),checks
(HERE/'local_symbolic_validation.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(f'{len(checks)} exact local symbolic checks passed')
