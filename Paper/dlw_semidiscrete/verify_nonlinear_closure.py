"""Exact symbolic verification of the conditional nonlinear closure.

No old tau engine, numerical zero tolerance, or soliton assumptions are used.
"""
import sympy as s
from fractions import Fraction

x, t, y, h, a = s.symbols('x t y h a', nonzero=True)
alpha = {j: s.Function(f'A{j}')(x, t) for j in range(-4, 5)}
beta = {j: s.Function(f'B{j}')(x, t) for j in range(-4, 6)}
dx = lambda f: s.diff(f, x)
xx = lambda f: s.diff(f, x, 2)
dt = lambda f: s.diff(f, t)
back = lambda f, j: (f(j)-f(j-1))/h
center = lambda f, j: (f(j+1)-f(j-1))/(2*h)
mean = lambda f, j: (f(j)+f(j-1))/2
lap = lambda f, j: (f(j+1)-2*f(j)+f(j-1))/h**2

def check(label, expression):
    assert s.expand(expression) == 0, label
    print('PASS:', label)

def A(j):
    p, q = alpha[j], beta[j]
    return xx(p+q)+dx(p-q)**2+dt(p-q)+(2*a-h)*dx(p-q)

def C(j):
    p, q = alpha[j], beta[j+1]
    return xx(p+q)+dx(p-q)**2+dt(p-q)+(2*a+h)*dx(p-q)

U = lambda j: dx(2*alpha[j]-beta[j]-beta[j+1])
R = lambda j: 2*dx(beta[j+1]-beta[j])/h
Q = lambda j: dx(2*alpha[j]+beta[j]+beta[j+1])
V = lambda j: 2*R(j)+center(U, j)
W = lambda j: V(j)-center(U, j)
H = lambda j: U(j)**2/2+2*a*U(j)+h**2*(W(j)**2/32-W(j)/4)
S = lambda j: dt(U(j))+dx(H(j))+xx(Q(j))
T = lambda j: dt(W(j))+dx((U(j)+2*a)*W(j)-4*U(j))-xx(W(j))
L1 = lambda j: back(lambda k: dt(U(k))+dx(H(k)), j)+xx(mean(V,j)-h**2*lap(lambda k: back(U,k),j)/4)
L2 = lambda j: dt(V(j))+dx(center(H,j)+(U(j)+2*a)*W(j)-4*U(j))+xx(center(U,j)+h**2*lap(W,j)/4)

check('averaged potential identity', S(0)-dx(A(0)+C(0)))
check('potential difference identity', T(0)-4*dx(A(0)-C(0))/h)
check('Q elimination identity', back(Q,0)-back(U,0)-R(0)-R(-1))
check('first closed residual', L1(0)-back(S,0))
check('second closed residual', L2(0)-T(0)-(L1(0)+L1(1))/2)

original_u = lambda j: 2*dx(alpha[j]-beta[j])
original_q = lambda j: 2*dx(alpha[j]+beta[j])
forward = lambda f,j: (f(j+1)-f(j))/h
avgforward = lambda f,j: (f(j+1)+f(j))/2
original_v = lambda j: forward(original_q,j)
f1 = lambda j: forward(lambda k:dt(original_u(k)),j)+dx((avgforward(original_u,j)+2*a-h)*forward(original_u,j))+xx(original_v(j))
f2 = lambda j: dt(original_v(j))+dx((avgforward(original_u,j)+2*a+h)*original_v(j)-h*(original_v(j)**2-forward(original_u,j)**2)/4-4*avgforward(original_u,j))+xx(forward(original_u,j))
check('original-variable first equation', f1(0)-2*forward(lambda j:dx(A(j)),0))
check('original-variable second equation', f2(0)-f1(0)-4*dx(A(0)-C(0))/h)

# Formal consistency with arbitrary smooth jets, as exact polynomials.
u = s.Function('u')(x,y,t)
v = s.Function('v')(x,y,t)
def jet(f, offset, order=5):
    return sum(s.diff(f,y,k)*(offset*h)**k/s.factorial(k) for k in range(order+1))
old_U, old_V = U, V
U = lambda j: jet(u,s.Rational(j))
V = lambda j: jet(v,s.Rational(j))
e1 = s.expand(L1(0))
e2 = s.expand(L2(0))
pde1 = s.diff(u,y,t)+dx((u+2*a)*s.diff(u,y))+xx(v)
pde2 = dt(v)+dx((u+2*a)*v-4*u)+s.diff(u,y,x,2)
check('first continuum equation', e1.coeff(h,0)-pde1)
check('first equation centered at y-h/2', e1.coeff(h,1)+s.diff(pde1,y)/2)
check('second continuum equation', e2.coeff(h,0)-pde2)
check('second equation has no first-order error', e2.coeff(h,1))

# Physical definitions: F at y, G at y +/- h/2.
f = s.Function('logf')(x,y,t)
g = s.Function('logg')(x,y,t)
uh = dx(2*f-jet(g,-s.Rational(1,2))-jet(g,s.Rational(1,2)))
rh = 2*dx(jet(g,s.Rational(1,2))-jet(g,-s.Rational(1,2)))/h
vh = 2*rh+(jet(uh,1)-jet(uh,-1))/(2*h)
check('u physical limit', s.expand(uh).coeff(h,0)-2*dx(f-g))
check('v physical limit', s.expand(vh).coeff(h,0)-2*s.diff(f+g,x,y))
check('u definition is second order', s.expand(uh).coeff(h,1))
check('v definition is second order', s.expand(vh).coeff(h,1))
check('u second-order coefficient', s.expand(uh).coeff(h,2)+s.diff(g,x,y,2)/4)
check('v second-order coefficient', s.expand(vh).coeff(h,2)-s.diff(f,x,y,3)/3+5*s.diff(g,x,y,3)/12)

# Exact rational h-scan: normalized truncation errors at multiple points.
poly_u = x*y**3+t*y**2+x**2*y
poly_v = x**2*y**2+t*y**3+x*y
subs = {u:poly_u,v:poly_v}
err1 = (e1-pde1+h*s.diff(pde1,y)/2-h**2*s.diff(pde1,y,2)/8).subs(subs).doit()
err2 = (e2-pde2).subs(subs).doit()
for point in [(1,2,3),(2,3,1),(3,1,2)]:
    vals=[]
    for den in (4,8,16,32,64):
        hv=Fraction(1,den)
        ev=[s.cancel(e.subs({x:point[0],y:point[1],t:point[2],a:s.Rational(3,2),h:s.Rational(hv.numerator,hv.denominator)})) for e in (err1,err2)]
        vals.append((str(hv),*[str(Fraction(int(z.p),int(z.q))/hv**2) for z in ev]))
    print('Exact h scan (h, error1/h^2, error2/h^2), point',point,':',vals)

# Correct continuous Hirota (6), N=1: compare independent exponential coefficients.
p,q = s.symbols('p q')
P,Qp = p-a,q+a
kx,kt,ky=p+q,q*q-p*p,1/P+1/Qp
cf,cg=-P/(Qp*(p+q)),1/(p+q)
bplus=kx*kx+kt+2*a*kx
bminus=kx*kx-kt-2*a*kx
assert s.factor(cf*bplus+cg*bminus)==0
assert s.factor(cf*ky*bplus-cg*ky*bminus-4*kx*(cf-cg))==0
assert s.factor(cg*ky*bminus+2*kx*(cf-cg))==0
print('PASS: true continuous Hirota (6), (7), and B(f,g_y)+2Dx(f,g), symbolic N=1')
print('ALL SYMBOLIC CHECKS PASSED')
