"""Exact algebra checks supporting the analytic Hamilton proof; no PDE simulation.

Run with the existing Python313 + SymPy installation. The report proves the
general statements; finite matrices/polynomial jets here independently check
normalizations, signs, constraint lift, and both original SD residuals.
"""
from pathlib import Path
import hashlib
import json
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
x = s.symbols('x', real=True)
checks = []

def zero(name, expr):
    items = list(expr) if isinstance(expr, s.MatrixBase) else [expr]
    reduced = [s.cancel(s.expand(e)) for e in items]
    ok = all(e == 0 for e in reduced)
    checks.append({'name': name, 'passed': ok})
    if not ok:
        raise AssertionError((name, [str(e) for e in reduced if e != 0][:3]))

def mat(n, h):
    I = s.eye(n)
    E = s.zeros(n)
    for j in range(n):
        E[j, (j+1) % n] = 1
    Pi = s.ones(n)/n
    P = I-Pi
    d = (I-E.T)/h
    M = (I+E.T)/2
    C0 = (E-E.T)/(2*h)
    R = s.zeros(n)
    for ell in range(1, n):
        R += h*(s.Rational(ell,n)-s.Rational(1,2))*(E**ell)
    return E, Pi, P, d, M, C0, R

for n in [3,4,5,6,7]:
    h = s.Rational(2,3)
    E, Pi, P, d, M, C0, R = mat(n,h)
    zero(f'N={n}: R skew', R+R.T)
    zero(f'N={n}: d R = M P', d*R-M*P)
    zero(f'N={n}: R annihilates mean', R*Pi)
    zero(f'N={n}: central difference skew', C0+C0.T)
    zero(f'N={n}: R delta0 = P M- M+', R*C0-P*M*M.T)

    q = P*s.Matrix([s.Rational(j+1,n+2)*x**2 + (j%3-1)*x
                     +s.Rational(j*j+1,n+1) for j in range(n)])
    r = P*s.Matrix([s.Rational(2*j-1,n+3)*x**2 + (j%2)*x
                     +s.Rational(3*j+2,n+2) for j in range(n)])
    one = s.ones(n,1)
    for c, flux in [(s.Integer(-4),s.Rational(-40,7)),
                    (s.Rational(2,3),s.Rational(9,5))]:
        a = s.Rational(5,7)
        rho = -1/c
        mean_u = flux/c-2*a + rho*(q.T*r)[0]/n
        u = q+mean_u*one
        v = r+(c+4)*one
        U = u+2*a*one
        w = v-C0*u-4*one
        mul = lambda b,z: s.diag(*b)*z
        b = h*h/s.Integer(32)
        F = mul(U,U)/2+b*mul(w,w)
        gU = mul(U,w)-w.diff(x)-flux*one
        gw = F+U.diff(x)+R*w.diff(x)
        gu = gU+C0*gw
        gv = gw
        prefix = f'N={n}, c={c}'
        zero(prefix+': mean w', Pi*w-c*one)
        zero(prefix+': mean U w', Pi*mul(U,w)-flux*one)
        zero(prefix+': physical constraint', Pi*mul(u,v-4*one)
             -(flux-2*a*c)*one)
        zero(prefix+': mean ambient u gradient', Pi*gu)

        # A*: pull back the physical covector to the meanzero chart (q,r).
        gq = P*(gu+rho*mul(r,Pi*gu))
        gr = P*(gv+rho*mul(q,Pi*gu))
        qt = -P*gr.diff(x)
        rt = -P*gq.diff(x)
        # A: push forward chart velocity to physical u,v.
        ut = qt+rho*Pi*(mul(r,qt)+mul(q,rt))
        vt = rt
        wt = vt-C0*ut
        zero(prefix+': SD first residual',
             d*(ut+F.diff(x))+(d*u+M*w).diff(x,2))
        zero(prefix+': SD w residual',
             wt+mul(U,w).diff(x)-w.diff(x,2))
        zero(prefix+': derivative of physical constraints',
             Pi*(mul(ut,v-4*one)+mul(u,vt)))
        zero(prefix+': v mean tangent',Pi*vt)
        # Original physical N2 is w equation plus M+ times N1.
        Wh = w+4*one
        Hphysical=mul(u,u)/2+2*a*u+h*h*(mul(Wh,Wh)/32-Wh/4)
        Delta=(E+E.T-2*s.eye(n))/(h*h)
        n2=vt+(C0*Hphysical+mul(U,Wh)-4*u).diff(x)
        n2+=(C0*u+h*h*Delta*Wh/4).diff(x,2)
        zero(prefix+': original physical N2',n2)

# The reduced functional's scalar collective term and its two derivatives.
m, flux, sigma = s.symbols('m flux sigma', nonzero=True)
A=(flux-sigma)/m
collective=m*A*A/2+A*sigma-flux*A
zero('eliminated mean energy',collective+(flux-sigma)**2/(2*m))
zero('collective derivative',s.diff(collective,sigma)-(flux-sigma)/m)

# Bounded-locality obstruction: evaluation at zeta=1 is nonzero.
zeta,h=s.symbols('zeta h', nonzero=True)
for radius in [0,1,2,3]:
    coeff=s.symbols(f'b0:{2*radius+1}')
    B=sum(coeff[j]*zeta**(j-radius) for j in range(2*radius+1))
    obstruction=s.expand((zeta-1)*zeta**radius*B
                         -h*zeta**radius*(zeta+1)/2)
    zero(f'locality r={radius}: pole witness',obstruction.subs(zeta,1)+h)
    assert s.Poly(obstruction,zeta).degree() <= 2*radius+1

sources = [ROOT/'Workspaces/dlw_semidiscrete/NONLINEAR_CLOSURE.md',
           ROOT/'Workspaces/dlw_factor_model_20260930/_src/equations_and_estimates.md',
           Path(__file__)]
result={'scope':'Exact finite matrix / polynomial jet checks. General skew, Jacobi, '
        'equivalence and locality proofs are analytic in the report.',
        'passed':all(c['passed'] for c in checks), 'count':len(checks),
        'checks':checks,
        'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sources}}
(HERE/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':result['passed'],'count':len(checks)},ensure_ascii=False))
