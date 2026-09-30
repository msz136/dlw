"""Exact identities for the Miura/DLW choices review, without soliton sampling."""
import json
from pathlib import Path
import sympy as s

x, t, y = s.symbols('x t y')
h, a, c, kappa, P, Q = s.symbols('h a c kappa P Q', nonzero=True)
checks = []

def check(name, value):
    value = s.simplify(s.expand(value))
    assert value == 0, (name, value)
    checks.append(name)
    print('PASS:', name)

alpha = {j: s.Function(f'alpha{j}')(x,t) for j in range(-3,4)}
beta = {j: s.Function(f'beta{j}')(x,t) for j in range(-3,5)}
dx = lambda z: s.diff(z,x)
xx = lambda z: s.diff(z,x,2)
dt = lambda z: s.diff(z,t)
dm = lambda f,j: (f(j)-f(j-1))/h
d0 = lambda f,j: (f(j+1)-f(j-1))/(2*h)
u = lambda j: dx(2*alpha[j]-beta[j]-beta[j+1])
w = lambda j: 4*dx(beta[j+1]-beta[j])/h
v = lambda j: w(j)+d0(u,j)
z = lambda j: dx(2*alpha[j]+beta[j]+beta[j+1])

# Allow x-dependent parameters here to separate exact closure from integrability.
A = s.Function('A')(x)
r = s.Function('r')(x)
lower = lambda j: xx(alpha[j]+beta[j])+dx(alpha[j]-beta[j])**2+dt(alpha[j]-beta[j])+(2*A-h*r)*dx(alpha[j]-beta[j])
upper = lambda j: xx(alpha[j]+beta[j+1])+dx(alpha[j]-beta[j+1])**2+dt(alpha[j]-beta[j+1])+(2*A+h*r)*dx(alpha[j]-beta[j+1])
flux = lambda j: u(j)**2/2+2*A*u(j)+h**2*(w(j)**2/32-r*w(j)/4)
short1 = lambda j: dm(lambda k: dt(u(k))+dx(flux(k)),j)+xx(dm(u,j)+(w(j)+w(j-1))/2)
short2 = lambda j: dt(w(j))+dx((u(j)+2*A)*w(j)-4*r*u(j))-xx(w(j))
check('general parameter wall sum',dt(u(0))+dx(flux(0))+xx(z(0))-dx(lower(0)+upper(0)))
check('general parameter wall difference',short2(0)-4*dx(lower(0)-upper(0))/h)
check('auxiliary potential elimination',dm(z,0)-dm(u,0)-(w(0)+w(-1))/2)

# Fully displayed physical-field equations: no auxiliary unknowns or operators.
def displayed1(j):
    return (dt((u(j)-u(j-1))/h)
        + dx(((u(j)+u(j-1))/2+2*A)*(u(j)-u(j-1))/h
          +h*((v(j)-(u(j+1)-u(j-1))/(2*h)-4*r)**2
               -(v(j-1)-(u(j)-u(j-2))/(2*h)-4*r)**2)/32)
        +xx((v(j)+v(j-1))/2
          -(u(j+1)-3*u(j)+3*u(j-1)-u(j-2))/(4*h)))
check('explicit u,v first equation equals exact closure',displayed1(0)-short1(0))
# The square's j-independent offset cancels in equation 1 even for A(x),r(x).
factored2 = dt(v(0)-d0(u,0))+dx((u(0)+2*A)*(v(0)-d0(u,0)-4*r)-dx(v(0)-d0(u,0)))
check('factored second flux needs 8(Ar)_x for variable coefficients',factored2+8*dx(A*r)-short2(0))

# Fixed physical h, constant shifted midpoint and wall separation.
Ac, rc = a+c*h**2, 1+kappa*h**2
W, U = s.symbols('W U')
flux_base = U**2/2+2*a*U+h**2*(W**2/32-W/4)
flux_shift = U**2/2+2*Ac*U+h**2*(W**2/32-rc*W/4)
check('parameter changes first flux',flux_shift-flux_base-2*c*h**2*U+kappa*h**4*W/4)
check('parameter changes second flux',((U+2*Ac)*W-4*rc*U)-((U+2*a)*W-4*U)-h**2*(2*c*W-4*kappa*U))

# The Taylor errors in physical u,v, assuming exact samples of continuous tau.
f = s.Function('alpha')(x,y,t)
g = s.Function('beta')(x,y,t)
jet = lambda z,b: sum(s.diff(z,y,n)*(b*h)**n/s.factorial(n) for n in range(6))
uh = dx(2*f-jet(g,-s.Rational(1,2))-jet(g,s.Rational(1,2)))
wh = 4*dx(jet(g,s.Rational(1,2))-jet(g,-s.Rational(1,2)))/h
vh = wh+(jet(uh,1)-jet(uh,-1))/(2*h)
uc, vc = 2*dx(f-g), 2*s.diff(f+g,x,y)
check('physical u leading error',s.expand(uh-uc).coeff(h,2)-(s.diff(uc,y,2)-s.diff(vc,y))/16)
check('physical v leading error',s.expand(vh-vc).coeff(h,2)-(9*s.diff(uc,y,3)-s.diff(vc,y,2))/48)

# Logarithmic lattice phase; series are taken at nonzero fixed P,Q.
ell = h+kappa*h**3
logchi = (s.log(1+(-c*h**2+ell/2)/P)-s.log(1+(-c*h**2-ell/2)/P)
    +s.log(1+(c*h**2+ell/2)/Q)-s.log(1+(c*h**2-ell/2)/Q))
phase = s.expand(s.series(logchi,h,0,5).removeO()/h)
check('leading lattice phase',phase.coeff(h,0)-1/P-1/Q)
check('second order lattice phase',phase.coeff(h,2)-kappa*(1/P+1/Q)-c*(1/P**2-1/Q**2)-(1/P**3+1/Q**3)/12)
check('no universal fourth order within c,kappa family',phase.coeff(h,2).subs(Q,P)-2*kappa/P-1/(6*P**3))

# A varying parameter invalidates the naive fixed-s one-soliton identity.
p,q = s.symbols('p q')
b = s.Function('b')(x)
gamma = -(p-b)/(q+b)
E = s.exp((p+q)*x+(q*q-p*p)*t)
F,G = 1+gamma*E, 1+E
bilinear = xx(F)*G-2*dx(F)*dx(G)+F*xx(G)+dt(F)*G-F*dt(G)+2*b*(dx(F)*G-F*dx(G))
extra = E*((1+E)*xx(gamma)+2*(p+q)*dx(gamma)+2*b*(1+E)*dx(gamma))
check('variable parameter creates extra Gram residual',bilinear-extra)
check('variable parameter gamma derivative',dx(gamma)-(p+q)*dx(b)/(q+b)**2)

out = Path(__file__).with_name('miura_choices_checks.json')
out.write_text(json.dumps({'checks':checks,'count':len(checks),'status':'passed'},ensure_ascii=False,indent=2),encoding='utf-8')
