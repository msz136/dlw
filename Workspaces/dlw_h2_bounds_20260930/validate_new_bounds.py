"""Checks of this new coefficient/bound computation, without reading old runs."""
from pathlib import Path
from fractions import Fraction
import json
import sympy as s
import mpmath as mp
from single_bounds import CASES,fields
from bernstein import abs_sup

HERE=Path(__file__).resolve().parent
mp.mp.dps=60
z=s.symbols('s',real=True)
checks=[]
x,y=s.symbols('x y')
b=abs_sup(16*x*(1-x)*y*(1-y),(x,y),tolerance=Fraction(1,10**7),seconds=20)
assert s.Rational(b['lower_exact'])<=1<=s.Rational(b['upper_exact'])
checks.append({'name':'Bernstein polynomial with exact interior maximum 1','gap':b['gap']})
b=abs_sup((1+x)/(2+x)+y/10,(x,y),tolerance=Fraction(1,10**6),seconds=20)
assert s.Rational(b['lower_exact'])<=s.Rational(23,30)<=s.Rational(b['upper_exact'])
checks.append({'name':'Bernstein rational function with exact corner maximum 23/30','gap':b['gap']})
remainders=json.loads((HERE/'remainder_bounds.json').read_text(encoding='utf-8'))
for name,pars in CASES.items():
    k,ell,gamma,residual,_,_=fields(*pars)
    a,p,q=map(lambda v:mp.mpf(str(v)),pars)
    k,ell,gamma=map(lambda v:mp.mpf(str(v)),(k,ell,gamma))
    om=q*q-p*p
    def derivative_polynomials(expr,n):
        out=[s.cancel(expr)]
        for _ in range(n):out.append(s.cancel(z*(1-z)*s.diff(out[-1],z)))
        return [s.lambdify(z,v,'mpmath') for v in out]
    fs=derivative_polynomials(s.Rational(str(gamma))*z/(1+(s.Rational(str(gamma))-1)*z),2)
    gs=derivative_polynomials(z,2)
    leading={key:s.lambdify(z,expr,'mpmath') for key,expr in residual.items()}
    maximum_ratio=0
    convergence=[]
    for hh in ('0.125','0.0625','0.03125'):
        h=mp.mpf(hh)
        max_remainders={key:mp.mpf(0) for key in leading}
        for zz in [mp.mpf(i)/4 for i in range(-32,33)]:
            ss=1/(1+mp.exp(-zz))
            cache={}
            def node(j):
                if j in cache:return cache[j]
                sj=1/(1+mp.exp(-(zz+ell*h*j)))
                sp=1/(1+mp.exp(-(zz+ell*h*(j+1))))
                sm=1/(1+mp.exp(-(zz+ell*h*(j-1))))
                U=[2*k*(ff(sj)-gg(sj)) for ff,gg in zip(fs,gs)]
                V=[2*k*ell*(fs[i+1](sj)+gs[i+1](sj)) for i in range(2)]
                # v phase second derivative uses independent analytic diff.
                vf=lambda z0:2*k*ell*(fs[1](1/(1+mp.exp(-z0)))+gs[1](1/(1+mp.exp(-z0))))
                V.append(mp.diff(vf,zz+ell*h*j,2))
                D=[2*k*((fs[i](sp)-gs[i](sp))-(fs[i](sm)-gs[i](sm)))/(2*h) for i in range(3)]
                W=[v0-d0 for v0,d0 in zip(V,D)]
                Hx=(U[0]+2*a)*k*U[1]
                cache[j]=(U,V,D,W,Hx)
                return cache[j]
            for model in ('SD','FD'):
                plus,minus=node(mp.mpf('.5')),node(mp.mpf('-.5'))
                def hx(n):
                    U,V,D,W,H0=n
                    return H0+(h*h*(W[0]/16-mp.mpf('.25'))*k*W[1] if model=='SD' else 0)
                r1=om*(plus[0][1]-minus[0][1])/h+(hx(plus)-hx(minus))/h
                if model=='SD':r1+=k*k*((plus[0][2]-minus[0][2])/h+(plus[3][2]+minus[3][2])/2)
                else:r1+=k*k*(plus[1][2]+minus[1][2])/2
                U,V,D,W,H0=node(0)
                if model=='SD':
                    pp,mm=node(1),node(-1)
                    r2=om*V[1]+(hx(pp)-hx(mm))/(2*h)+k*(U[1]*W[0]+(U[0]+2*a)*W[1]-4*U[1])
                    r2+=k*k*(D[2]+(pp[3][2]-2*W[2]+mm[3][2])/4)
                else:r2=om*V[1]+k*(U[1]*V[0]+(U[0]+2*a)*V[1]-4*U[1])+k*k*D[2]
                for i,value in enumerate((r1,r2),1):
                    key=model+'_R'+str(i)
                    rem=abs(value-h*h*leading[key](ss))
                    M=mp.mpf(remainders['cases'][name]['M'][key]['upper'])
                    ratio=rem/(M*h**4)
                    assert ratio<=1
                    maximum_ratio=max(maximum_ratio,ratio)
                    max_remainders[key]=max(max_remainders[key],rem)
        convergence.append({'h':hh,'max_remainder_over_h4':{key:float(v/h**4) for key,v in max_remainders.items()}})
    checks.append({'name':name+' finite-h analytic residuals inside derived h^4 bounds',
                   'max_fraction_of_bound':float(maximum_ratio),'sampled_h4_coefficients':convergence})
    print(name,'new finite-h remainder bound check',float(maximum_ratio),flush=True)

(HERE/'validation.json').write_text(json.dumps({'status':'passed','precision_digits':60,'checks':checks,
    'meaning':'New numerical sanity checks of the exact-arithmetic enclosure and analytic Taylor bound derivation; sampled checks are not the proof of the supremum.'},indent=2),encoding='utf-8')
print('PASSED new bound checks',flush=True)

