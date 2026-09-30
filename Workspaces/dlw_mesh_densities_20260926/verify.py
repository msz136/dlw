"""Local conservation identities for both finite-h DLW walls and shared meshes."""
from pathlib import Path
import json
import sympy as s
HERE=Path(__file__).resolve().parent
x,t=s.symbols('x t',real=True)
a,A,h,mu,beta,theta=s.symbols('a A h mu beta theta',real=True,nonzero=True)
u,v,g=[s.Function(name)(x,t) for name in ('u','v','g')]
checks={}
def check(name,expr):
    res=s.simplify(s.expand(expr));checks[name]=str(res);assert res==0,(name,res)
gt=-s.diff((u+2*a)*g+s.diff(v,x),x)
vt=-s.diff((u+2*a)*v+s.diff(g,x)-4*u,x)
for sig in (-1,1):
    R=1-(v+sig*g)/4;Q=(u+2*a)*R+sig*s.diff(R,x)-2*a
    check(f'continuous_branch_{sig}',-(vt+sig*gt)/4+s.diff(Q,x))
R0=1-v/4;Q0=(u+2*a)*R0-s.diff(g,x)/4-2*a
check('continuous_symmetric',-vt/4+s.diff(Q0,x))

u0,um,w0,wm=[s.Function(name)(x,t) for name in ('u0','um','w0','wm')]
P=(u0-um)/h;Mw=(w0+wm)/2
H=lambda u,w:u*u/2+2*A*u+h*h*(w*w/32-mu*w/4)
F=lambda u,w:(u+2*A)*w-4*mu*u
Pt=-s.diff((H(u0,w0)-H(um,wm))/h,x)-s.diff(P+Mw,x,2)
w0t=-s.diff(F(u0,w0),x)+s.diff(w0,x,2)
wmt=-s.diff(F(um,wm),x)+s.diff(wm,x,2)
S=2*P+Mw;St=2*Pt+(w0t+wmt)/2
ut=(u0+um)/2+h*(w0-wm)/8
Jp=(ut+2*A)*S-4*mu*ut+s.diff(S,x)
check('finite_plus_field_flux',St+s.diff(Jp,x))
Rm=1-w0/(4*mu);Qm=(u0+2*A)*Rm-s.diff(Rm,x)-2*A
Rp=1-S/(4*mu);Qp=(ut+2*A)*Rp+s.diff(Rp,x)-2*A
check('finite_minus_density',-w0t/(4*mu)+s.diff(Qm,x))
check('finite_plus_density',-St/(4*mu)+s.diff(Qp,x))
check('same_monitor_without_mu_normalization',-w0t/4+s.diff((u0+2*A)*(1-w0/4)-s.diff(1-w0/4,x)-2*A+(mu-1)*u0,x))
check('constant_affine_strength',beta*(-w0t/(4*mu))+s.diff(beta*Qm,x))
check('constant_convex_mix',(1-theta)*(-w0t/(4*mu))+theta*(-St/(4*mu))+s.diff((1-theta)*Qm+theta*Qp,x))

up,wp=s.symbols('up wp')
Sp=2*(up-u0)/h+(wp+w0)/2
Rplus_center=1-(S+Sp)/(8*mu)
Ravg=(Rm+Rplus_center)/2
v0=w0+(up-um)/(2*h)
check('symmetric_density_physical_formula',Ravg-(1-v0/(4*mu)-(wp-2*w0+wm)/(32*mu)))

# Tau identity for the staggered plus field, independent of evolution.
aj,am,bp,b0,bm=s.symbols('aj am bp b0 bm')
uj=2*aj-b0-bp;ujm=2*am-bm-b0
wj=4*(bp-b0)/h;wjm=4*(b0-bm)/h
check('plus_tau_log_slope',2*(uj-ujm)/h+(wj+wjm)/2-4*(aj-am)/h)

# Full finite interval normalization: q at the left endpoint is not enough
# unless the left and right fluxes agree.
R,Q,QL,QR,eta=s.symbols('R Q QL QR eta',real=True)
vel=(Q-QL-eta*(QR-QL))/R
check('normalized_mass_mesh_velocity',-(Q-QL)+R*vel-eta*(QL-QR))

# Reciprocal/ALE density balance: d/dt(R(X,t) X_xi)=0 for V=Q/R.
Rx,Qx,Xxi=s.symbols('Rx Qx Xxi')
check('moving_cell_mass',(-Qx+(Q/R)*Rx)*Xxi+R*(Qx*R-Q*Rx)/R**2*Xxi)

# Do not turn an arbitrary nonlinear function of a density into a conservation law.
r=s.Function('r')(x,t);q=s.Function('q')(x,t)
nonlinear_defect=s.simplify((-2*r*s.diff(q,x))+s.diff(2*r*q,x))
check('square_density_extra_source',nonlinear_defect-2*q*s.diff(r,x))
out=dict(passed=True,identities=checks,number=len(checks),
    scope='Finite-h identities use A=a+c*h^2 and mu=1+kappa*h^2 as constants. No moving-mesh PDE evolution performed.',
    nonlinear_square_warning=str(nonlinear_defect))
(HERE/'identity_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(f'{len(checks)} symbolic identities passed')
