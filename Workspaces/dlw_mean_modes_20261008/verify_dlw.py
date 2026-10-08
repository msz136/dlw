"""Exact finite-jet certificates. General proofs and scope are in the HTML report."""
from pathlib import Path
import json
import hashlib
import sympy as S

x, t = S.symbols('x t', real=True)
checks = []

def check(name, expression):
    terms = list(expression) if isinstance(expression, S.MatrixBase) else [expression]
    errors = [S.cancel(e) for e in terms]
    ok = all(e == 0 for e in errors)
    checks.append({'name': name, 'passed': ok})
    if not ok:
        raise AssertionError((name, [str(e) for e in errors if e != 0][:2]))

def matrices(n, h):
    E = S.zeros(n)
    for j in range(n):
        E[j, (j+1) % n] = 1
    Pi = S.ones(n)/n
    P = S.eye(n)-Pi
    dm = (S.eye(n)-E.T)/h
    mm = (S.eye(n)+E.T)/2
    R = S.zeros(n)
    for ell in range(1, n):
        R += h*(S.Rational(ell,n)-S.Rational(1,2))*E**ell
    return Pi, P, dm, mm, R

def prod(a,b):
    return a.multiply_elementwise(b)

def avg(a):
    return sum(a)/len(a)

for n in range(2,7):
    h = S.Rational(2,3)
    beta = h*h/32
    Pi,P,dm,mm,R = matrices(n,h)
    check(f'M={n}: lattice inverse and skew', (dm*R-mm*P).col_join(R+R.T))
    p = P*S.Matrix([S.Rational(j+1,n+2)*x + S.Rational(j*j+1,n+1) for j in range(n)])
    s = P*S.Matrix([S.Rational(2*j-1,n+3)*x + S.Rational(j%3-1,n+2) for j in range(n)])
    one = S.ones(n,1)
    r = avg(prod(p,s))
    for label,m,q in [('arbitrary-time-flux',S.Rational(-4),3+t+t*t),
                       ('nonperiodic-affine-mean',2+t+x/7,-x+3+t*t)]:
        b = (q-r)/m
        U = p+b*one
        w = s+m*one
        F = prod(U,U)/2+beta*prod(w,w)
        pt = -P*F.diff(x)-p.diff(x,2)-R*s.diff(x,2)
        st = -P*prod(U,w).diff(x)+s.diff(x,2)
        rt = avg(prod(pt,s)+prod(p,st))
        bt = (S.diff(q,t)-rt)/m-(q-r)*S.diff(m,t)/m**2
        Ut = pt+bt*one
        wt = st+S.diff(m,t)*one
        check(f'M={n}, {label}: physical mean',Pi*prod(U,w)-q*one)
        check(f'M={n}, {label}: first original residual',dm*(Ut+F.diff(x))+(dm*U+mm*w).diff(x,2))
        check(f'M={n}, {label}: second original residual',wt+prod(U,w).diff(x)-w.diff(x,2))
        lam = q-S.diff(m,x)
        collective = m*b*b/2+b*r-lam*b+m*S.diff(b,x)
        check(f'M={n}, {label}: bulk Hamilton density',collective+(q-r)**2/(2*m)-S.diff(m*b,x))
    b = x*x + S.Rational(3,7)*x
    U = p+b*one
    w = s
    F = prod(U,U)/2+beta*prod(w,w)
    pt = -P*F.diff(x)-p.diff(x,2)-R*s.diff(x,2)
    st = -prod(U,w).diff(x)+avg(prod(U,w).diff(x))*one+s.diff(x,2)
    rt = avg(prod(pt,s)+prod(p,st))
    T = avg(prod(prod(p,p),s)+2*beta*prod(prod(s,s),s)/3+
            prod(s,p.diff(x))-prod(p,s.diff(x))+prod(s,R*s.diff(x)))
    check(f'M={n}: zero-c secondary constraint identity',rt+S.diff(T,x)+2*r*S.diff(b,x)+b*S.diff(r,x))

c,g,r = S.symbols('c g r', nonzero=True, real=True)
bb = (g-r)/c
check('energy split for arbitrary gamma',c*bb**2/2+bb*r-g*bb+r**2/(2*c)-g*r/c+g*g/(2*c))
B = S.symbols('B')
charges = S.symbols('I1:11')
normalized = {}
for n in range(1,11):
    normalized[n] = sum(S.binomial(n-1,k-1)*B**(n-k)*charges[k-1] for k in range(1,n+1))
    restored = sum(S.binomial(n-1,k-1)*(-B)**(n-k)*normalized[k] for k in range(1,n+1))
    check(f'spectral triangular inverse n={n}',restored-charges[n-1])
    if n>1:
        check(f'normalized spectral drift n={n}',S.diff(normalized[n],B)-(n-1)*normalized[n-1])

h,g,a = S.symbols('h g a', nonzero=True, real=True)
f = 1+x+x*x
ss = g/f
b = a-S.diff(f,x)/f
p = S.Matrix([f,-f]); s = S.Matrix([ss,-ss]); U = p+b*S.ones(2,1)
_,P,dm,mm,R = matrices(2,h)
F = prod(U,U)/2+h*h*prod(s,s)/32
check('M=2 zero-c branch: first original residual',dm*(-a*p.diff(x)+F.diff(x))+(dm*U+mm*s).diff(x,2))
check('M=2 zero-c branch: second original residual',-a*s.diff(x)+prod(U,s).diff(x)-s.diff(x,2))
d = h*g/(8*f)
ell = S.diff(f,x)/f
v = f/2-d
gauge = b/2+ell/2
u1 = b/2+v+ell-gauge
u2 = b/2-v-gauge
ff = v+ell/2
check('M=2 order-two root: first-order coefficient',-u1-u2)
check('M=2 order-two root: potential',u1*u2-S.diff(u2,x)-(S.diff(ff,x)-ff**2))

# Exact first-order factor identities prove the monodromy factorization:
# T1*T0-I = -2 A1^{-1} p A0^{-1} d.
A0 = (b+f)/2-d
B0 = (b+f)/2+d
A1 = (b-f)/2+d
B1 = (b-f)/2-d
check('M=2 monodromy factor: B0-A0=-2d as operators',-B0+A0+2*d)
check('M=2 monodromy factor: B1-A1=2d as operators',-B1+A1-2*d)
check('M=2 monodromy factor: A0-B1=-p as operators',-A0+B1+f)
check('M=2 monodromy root normalization',f*d-h*g/8)

result = {'passed':all(q['passed'] for q in checks), 'count':len(checks),
          'scope':'Exact symbolic checks at M=2,...,6 and spectral orders 1,...,10; all-order Jacobi, trace involution and independence are analytic claims, not inferred from these finite checks.',
          'checks':checks, 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':result['passed'],'count':result['count']}))
