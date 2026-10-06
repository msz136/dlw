"""Independent, lightweight checks of the current DLW Lax claims.

Does not import or modify the old Lax experiment engine.
"""
import json
from pathlib import Path
import sympy as s

x, t, a, h = s.symbols('x t a h', nonzero=True)
u, W, V = [s.Function(k)(x, t) for k in ('u', 'W', 'V')]
D = lambda q: s.diff(q, x)
wm = a + u/2 + h*(W-4)/8
wp = a + u/2 - h*(W-4)/8
Vp = V + h*D(W)/2
H = u*u/2 + 2*a*u + h*h*(W*W/32-W/4)
em = s.diff(wm,t) + D(D(wm)) + 2*wm*D(wm) + D(V)
ep = s.diff(wp,t) + D(D(wp)) + 2*wp*D(wp) + D(Vp)
rw = s.diff(W,t) - D(D(W)) + D((u+2*a)*W-4*u)
ru = s.diff(u,t) + D(H) + D(D(u)) + h*D(D(W))/2 + 2*D(V)
assert s.expand(em-ep-h*rw/4) == 0
assert s.expand(em+ep-ru) == 0

# The old rank-one scalar compatibility is an identity for arbitrary fields.
q, qp = [s.Function(k)(x,t) for k in ('q','qp')]
z = s.symbols('z')
ell = (z+qp)/(z+q)
mq = s.diff(q,t)/(z+q)
mp = s.diff(qp,t)/(z+qp)
assert s.cancel(s.diff(ell,t)+ell*mq-mp*ell) == 0

# A counterexample to claiming the bare rational heat/lattice pair is globally
# equivalent to the original SD equations without a nondegeneracy condition.
# h=1, a=0, W_j=4, u_j=j*x gives T_j^+=T_j^-, hence L_j=1.
j = s.symbols('j', integer=True)
uj = lambda k:k*x
wj = lambda k:s.Integer(4)
vj = lambda k:wj(k)+(uj(k+1)-uj(k-1))/2
hj = lambda k:uj(k)**2/2+wj(k)**2/32-wj(k)/4
dm = lambda f,k:f(k)-f(k-1)
d0 = lambda f,k:(f(k+1)-f(k-1))/2
lap = lambda f,k:f(k+1)-2*f(k)+f(k-1)
mm = lambda f,k:(f(k)+f(k-1))/2
n1 = D(dm(hj,j))+D(D(mm(vj,j)-lap(lambda k:dm(uj,k),j)/4))
n2 = D(d0(hj,j)+uj(j)*wj(j)-4*uj(j)) + D(D(d0(uj,j)+lap(wj,j)/4))
assert s.expand(n1-(2*j-1)*x) == 0
assert s.expand(n2-2*j*x) == 0
assert s.expand(wm-wp).subs(W,4) == 0

checks = {
    'Darboux_difference': 'Eminus-Eplus = h/4 * RW',
    'Darboux_sum': 'Eminus+Eplus = RU',
    'old_scalar_zero_curvature': 'identically zero for arbitrary q, qp',
    'bare_pair_degenerate_counterexample': {
        'h': 1, 'a': 0, 'u_j': 'j*x', 'W_j': 4, 'V_j': 0,
        'L_j': 1, 'N1_residual': str(s.expand(n1)),
        'N2_residual': str(s.expand(n2)),
    },
}
Path(__file__).with_name('lax_audit_checks.json').write_text(
    json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
for key in checks:
    print('PASS:',key)
print('ALL INDEPENDENT LAX AUDIT CHECKS PASSED')
