"""Symbolic coefficient identities and independently integrated cell residuals."""
import json
from pathlib import Path
import numpy as np
import sympy as S
from numpy.polynomial.legendre import leggauss
from run_designed_cases import PS, initialize, safe_reference

HERE=Path(__file__).resolve().parent
checks={}
def check(name,expr):
    ans=S.factor(expr)
    assert ans==0,(name,ans)
    checks[name]=str(ans)

a,r,C,d,w,uL,uR=S.symbols('a r C d w uL uR',nonzero=True)
FI=w*w/2+2*(uL+uR)+((a/r+(C-a)*r)**2-C*C)/2
FD=w*w/2+2*(uL+uR)+(r*r-1)/2
delta=(C*C-2*a*C-1)*(r*r-1)/2+a*a*(1/r-r)**2/2
check('same_state_general_defect',FI-FD-delta)
check('original_defect',delta.subs(C,1)-a*(1-r*r)-a*a*(1/r-r)**2/2)
C0=a+S.sqrt(1+a*a)
check('calibrated_defect',delta.subs(C,C0)-a*a*(1/r-r)**2/2)
check('physical_spacing_defect',(a*a*(1/r-r)**2/2).subs(a,d*r)-d*d*(1-r*r)**2/2)
v=S.symbols('v')
dv=2*d*(uL+uR)+((d*d-a*(a-C))**2-v*v)/(2*d)-C*C*d/2
check('v_to_w_equation',(dv/d+v*v/d**2).subs(v,d*w).subs(d,a/r)-FI)

z,h=S.symbols('z h')
uc=S.symbols('u0:5'); rc=S.symbols('r0:4')
up=sum(uc[j]*z**j/S.factorial(j) for j in range(5))
rp=sum(rc[j]*z**j/S.factorial(j) for j in range(4))
avg=lambda f:S.integrate(f,(z,-h/2,h/2))/h
var=lambda f:avg(f*f)-avg(f)**2
TD=var(S.diff(up,z))/2+4*((up.subs(z,h/2)+up.subs(z,-h/2))/2-avg(up))-var(rp)/2
BD=uc[2]/3+uc[2]**2/24-rc[1]**2/24
check('cell_average_Taylor_coefficient',S.expand(TD).coeff(h,2)-BD)
check('no_odd_cell_powers',S.expand(TD).coeff(h,1)+S.expand(TD).coeff(h,3))

s=S.symbols('s',positive=True)
beta=4*s/(1-s*s)
u=s*s*(1-z*z)/4
rho=(1-s*s)/(1-s*s*z*z)
xz=2/(beta*(1-z*z))+s/2
Dx=lambda f:S.factor(S.diff(f,z)/xz)
ux=Dx(u);uxx=Dx(ux);rx=Dx(rho)
V=(1-s*s)/4
check('continuous_slope_equation',-(V+u)*uxx-ux**2/2-4*u-(rho*rho-1)/2)
check('continuous_mass_equation',-(V+u)*rx-rho*ux)
check('peak_curvature',uxx.subs(z,0)+2*s**4)
Bd=S.factor(uxx/3+uxx**2/24-rx**2/24)
Bc=S.factor(Bd+(1-rho*rho)**2/2)
Bd0=s**4*(s**4-4)/6
Bc0=S.Rational(2,3)*s**4*(1-s*s)*(2-s*s)
check('ordinary_peak_coefficient',Bd.subs(z,0)-Bd0)
check('calibrated_peak_coefficient',Bc.subs(z,0)-Bc0)
check('peak_absolute_ratio',-Bc0/Bd0-4*(1-s*s)/(2+s*s))
p=S.symbols('p',positive=True)
check('mass_coefficient_large_p',S.limit((Bc0/(1-s*s)**2).subs(s,1-2/p)/p,p,S.oo)-S.Rational(1,6))

rows=[]
g,wt=leggauss(100)
uxfn=S.lambdify((s,z),ux,'numpy')
for pv in PS:
    sv=1-2/pv; bv=pv-pv/(pv-1)
    sol,_,_,_,_=initialize(pv,'difference_matched',400)
    Bdf=float(Bd0.subs(s,sv)); Bcf=float(Bc0.subs(s,sv))
    for dh in (.02,.01,.005,.0025):
        xx=dh*g/2
        uu,rr,XX,inv=safe_reference(sol,xx,0.)
        slope=uxfn(sv,np.tanh(bv*XX/2))
        mean=lambda f:float(np.dot(wt,f)/2)
        vari=lambda f:mean((f-mean(f))**2)
        ends=safe_reference(sol,np.array([-dh/2,dh/2]),0.)[0]
        td=vari(slope)/2+4*(float(np.mean(ends))-mean(uu))-vari(rr)/2
        rb=mean(rr); actual_a=dh*rb
        tc=td+dh*dh*(1-rb*rb)**2/2
        ti=tc+actual_a*(1-rb*rb)
        rows.append(dict(p=pv,d=dh,a=actual_a,ordinary=td,calibrated=tc,original=ti,
                         BD=Bdf,BC=Bcf,ratio=abs(tc/td),theory_ratio=abs(Bcf/Bdf),
                         coefficient_relative_error=max(abs(td/dh**2/Bdf-1),abs(tc/dh**2/Bcf-1)),
                         inversion_residual=inv))
assert max(r['coefficient_relative_error'] for r in rows if r['d']==.0025)<.001
result=dict(symbolic_checks=checks,cell_quadrature=rows,
            formulas=dict(BD=str(Bd),BC=str(Bc)),
            p_threshold_improve=float(2/(1-S.sqrt(S.Rational(2,5)))),
            p_threshold_half=float(2/(1-S.sqrt(S.Rational(2,3)))))
(HERE/'theory_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'symbolic_checks':len(checks),'max_fine_coefficient_relerr':max(r['coefficient_relative_error'] for r in rows if r['d']==.0025),
                  'threshold':result['p_threshold_half']},indent=2))
