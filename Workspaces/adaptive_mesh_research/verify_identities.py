"""Symbolic conservation-law checks; no time evolution or Lean claims."""
import json
from pathlib import Path
import sympy as s

x, t = s.symbols('x t')
a, c, b, alpha = s.symbols('a c b alpha', real=True)
u, rho, w, v = [s.Function(n)(x, t) for n in ('u', 'rho', 'w', 'v')]
dx = lambda f: s.diff(f, x)
checks = {}

# 2-HS: w=u_x, w_t=u w_x+w^2/2+4u+c^2(rho^2-1)/2.
hs = {s.diff(w,t): u*dx(w)+w**2/2+4*u+c**2*(rho**2-1)/2,
      s.diff(rho,t): dx(u*rho)}
def hs_reduce(f):
    return s.simplify(s.expand(f.subs(hs)).subs(dx(u), w))
checks['hs_mass'] = hs_reduce(s.diff(rho,t)-dx(u*rho))
R = b+alpha*rho
checks['hs_affine_mass'] = hs_reduce(s.diff(R,t)-dx(alpha*u*rho))
e = w**2-c**2*(rho**2-1)
checks['hs_signed_energy'] = hs_reduce(s.diff(e,t)-dx(u*e+4*u**2-2*c**2*u))
mu = s.Function('mu')(x,t)
checks['hs_passive_weight'] = hs_reduce(
    (s.diff(rho*mu,t)-dx(u*rho*mu)).subs(s.diff(mu,t),u*dx(mu)))

# DLW: w=u_y; lambda=-2, zero (u,v) background.
dlw = {s.diff(w,t): -dx((u+2*a)*w+dx(v)),
       s.diff(v,t): -dx((u+2*a)*v+dx(w)-4*u)}
def dlw_reduce(f):
    return s.simplify(s.expand(f.subs(dlw)))
for sign in (-1,1):
    r = 1-(v+sign*w)/4
    q = (u+2*a)*r+sign*dx(r)-2*a
    checks[f'dlw_r_{sign:+d}'] = dlw_reduce(s.diff(r,t)+dx(q))
r0 = 1-v/4
q0 = (u+2*a)*r0-dx(w)/4-2*a
checks['dlw_r0'] = dlw_reduce(s.diff(r0,t)+dx(q0))
rminus = 1-(v-w)/4
qminus = (u+2*a)*rminus-dx(rminus)-2*a
checks['dlw_affine'] = dlw_reduce(s.diff(b+alpha*rminus,t)+dx(alpha*qminus))

# Exact existing semi-discrete W equation: W_t=-[(u+2a)W-4u]_x+W_xx.
W = s.Function('W')(x,t)
r = 1-W/4
q = (u+2*a)*r-dx(r)-2*a
checks['dlw_semidiscrete_rminus'] = s.simplify((s.diff(r,t)+dx(q)).subs(
    s.diff(W,t), -dx((u+2*a)*W-4*u)+s.diff(W,x,2)))
result = {'kind':'symbolic identities only; no PDE evolution',
          'residuals':{k:str(z) for k,z in checks.items()},
          'passed':all(z == 0 for z in checks.values())}
Path(__file__).with_name('identity_checks.json').write_text(
    json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2,ensure_ascii=False))
assert result['passed']
