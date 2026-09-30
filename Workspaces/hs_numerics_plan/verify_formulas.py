"""Exact algebra checks for the proposal; no time integration is performed."""
from fractions import Fraction as Q
import json
from pathlib import Path
import sympy as s

d, v, a, c, ur = s.symbols('d v a c ur', nonzero=True)
alpha = a*(a-c)
A = (d-a)*(c-a-d)
original = -v*(v+A)/d+(v+A)**2/(2*d)+4*ur*d-c*(v+A)-v*(2*d-c)
compact = 2*d*(2*ur-v)+((d*d-alpha)**2-v*v)/(2*d)-c*c*d/2
assert s.factor(original-compact) == 0

def tau(p, q, z, order=3, g=False):
    n = len(p)
    interaction = Q(1) if n == 1 else (p[1]-p[0])*(q[1]-q[0])/((q[1]-p[0])*(p[1]-q[0]))
    out = [Q(0)]*(order+1)
    for mask in range(1 << n):
        coeff = interaction if mask == 3 else Q(1)
        omega = Q(0)
        for i in range(n):
            if mask & (1 << i):
                coeff *= z[i]
                omega += 1/p[i]-1/q[i]
                if g:
                    coeff *= p[i]/q[i]
        for j in range(order+1):
            out[j] += coeff*omega**j
    return out

def logs(f):
    L1 = f[1]/f[0]
    L2 = f[2]/f[0]-L1**2
    L3 = f[3]/f[0]-3*f[2]*f[1]/f[0]**2+2*L1**3
    return L1, L2, L3

def bilinear(g, f, b):
    return g[2]*f[0]-2*g[1]*f[1]+g[0]*f[2]+b*(g[1]*f[0]-g[0]*f[1])

count = 0
for p in ([Q(5)], [Q(11,10), Q(5,4)]):
    c0 = Q(1)
    q = [r/(c0*r-1) for r in p]
    for a0 in (Q(1,100), Q(1,200), Q(1,400)):
        ratio = [(1-a0*q[i])/(1-a0*p[i]) for i in range(len(p))]
        for seed in (Q(1,7), Q(1), Q(9)):
            z = [seed**(i+1) for i in range(len(p))]
            prev = [z[i]/ratio[i] for i in range(len(p))]
            f, fm, g = tau(p,q,z), tau(p,q,prev), tau(p,q,z,g=True)
            l1,u,ut = logs(f)
            lm1,um,umt = logs(fm)
            delta = a0-l1+lm1
            jump = u-um
            al = a0*(a0-c0)
            rhs = 2*delta*(u+um)+((delta**2-al)**2-jump**2)/(2*delta)-c0**2*delta/2
            assert ut-umt == rhs
            assert delta > 0
            assert bilinear(g,f,c0) == 0
            assert bilinear(g,fm,c0-2*a0) == 0
            count += 1

result = {'symbolic_rhs_equivalence': True, 'exact_rational_soliton_samples': count,
          'bilinear_and_compact_rhs_residuals': 'exactly zero',
          'time_integration_performed': False,
          'scope': 'Algebra identity plus finite N=1,2 samples; not stability or convergence proof.'}
Path(__file__).with_name('formula_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
