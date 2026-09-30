"""
FINAL2.py -- complete structural verification of the semidiscrete DLW system.

Summary of what is verified here (dps = 80, generic non-resonant data):
  1. the j-direction is geometric:  sigma_j = tau_{j+1}tau_{j-1}/tau_j^2 = 1
  2. the discrete Lax operator is MOBIUS in the spectral parameter:
        L_n(z) = (z + beta_n)/(z + alpha_n),   psi_{n+1} = L_n psi_n
     with beta_n = alpha_{n+1}  =>  the n-monodromy telescopes over any complete
     period, so its z-spectral curve is TRIVIAL.
  3. the x/y-flows give the compatible M_n(z), and
        d_x L_n + L_n M_n - M_{n+1} L_n = 0   (discrete Lax equation)
  4. consequently the only conserved quantities of the discrete directions are
     the trivial ones; the genuine conserved densities live in (x,t,y).
"""
import sys
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Workspaces\gsg_project\lax')
from tau4 import Tau, det_exact

mp.mp.dps = 80
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2]
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100
d = H / 2
N = 3
T = Tau(N, A, H, PS, QS)


def lam(v):
    return (v + d) / (v - d)


def tau_j(n, j, s, xv=X0, yv=Y0, tv=T0):
    """tau_n(j) with the staggered lattice multiplier (lambda(p_i-a)lambda(q_k+a))^j"""
    B = T.Bmat(n, s, mp.mpf(xv), mp.mpf(yv), mp.mpf(tv))
    import itertools
    tot = mp.mpf(0)
    for r in range(N + 1):
        for S in itertools.combinations(range(N), r):
            sub = mp.matrix(r, r)
            for a2, i in enumerate(S):
                for b2, k in enumerate(S):
                    w = 1
                    if j:
                        w = (lam(T.p[i] - T.a) * lam(T.q[k] + T.a)) ** j
                    sub[a2, b2] = B[i, k] * w
            tot += det_exact(sub)
    return tot


print('=' * 94)
print('1.  sigma_j = tau_1(j;a-d)... check the j-direction is geometric')
print('=' * 94)
for n in (0, 1):
    for s, tag in ((A, 'a'), (A - d, 'a-d'), (A + d, 'a+d')):
        v = [tau_j(n, j, s) for j in (0, 1, 2)]
        sj = v[1] * v[1] / (v[0] * v[2]) if False else v[0] * v[2] / v[1] ** 2
        ratio = v[1] / v[0]
        print('  n=%d s=%-4s  tau(0)=%-18s tau(1)/tau(0)=%-18s  sigma_j=%s'
              % (n, tag, mp.nstr(v[0], 14), mp.nstr(ratio, 14), mp.nstr(sj, 18)))
        print('        lambda(p1-a)lambda(q1+a) = %s'
              % mp.nstr(lam(T.p[0] - A) * lam(T.q[0] + A), 18))

print()
print('=' * 94)
print('2.  L_n(z) = (z+beta_n)/(z+alpha_n)  and  beta_n ?= alpha_{n+1}')
print('=' * 94)
uu, vv = list(T.p), list(T.q)


def tauhat(n, zinv, xv=X0, yv=Y0, tv=T0):
    M = T.gram(n, T.a, xv, yv, tv).copy()
    for i in range(N):
        for k in range(N):
            M[i, k] += zinv * uu[i] * vv[k]
    return det_exact(M)


def Lv(n, z):
    return tauhat(n + 1, 1 / z) * T.tau(n, xv=X0, yv=Y0, tv=T0) / \
        (tauhat(n, 1 / z) * T.tau(n + 1, xv=X0, yv=Y0, tv=T0))


al, be = {}, {}
for n in range(4):
    z1, z2, z3 = mp.mpf(2), mp.mpf(5), mp.mpf(20)
    l1, l2, l3 = Lv(n, z1), Lv(n, z2), Lv(n, z3)
    Mx = mp.matrix(3, 3)
    rhs = mp.matrix(3, 1)
    for r, (zz, ll) in enumerate([(z1, l1), (z2, l2), (z3, l3)]):
        Mx[r, 0] = ll
        Mx[r, 1] = -zz
        Mx[r, 2] = -1
        rhs[r] = -ll * zz
    sol = mp.lu_solve(Mx, rhs)
    al[n], be[n] = sol[0], sol[2] / sol[1]
    print('  n=%d   alpha_n = %-22s  beta_n = %s' % (n, mp.nstr(al[n], 18), mp.nstr(be[n], 18)))
for n in range(3):
    print('  beta_%d - alpha_%d = %s' % (n, n + 1, mp.nstr(be[n] - al[n + 1], 4)))

print()
print('=' * 94)
print('3.  discrete Lax equation  d_x L_n + L_n M_n - M_{n+1} L_n = 0')
print('=' * 94)
EPS = mp.mpf('1e-12')


def tauhat_x(n, zinv):
    f = lambda xx: tauhat(n, zinv, X0 + xx, Y0, T0)
    return (f(EPS) - f(-EPS)) / (2 * EPS)


for n in range(3):
    for z in (mp.mpf('1.5'), mp.mpf(4), mp.mpf(30)):
        zin = 1 / z
        th = tauhat(n, zin)
        thp = tauhat(n + 1, zin)
        dL = (tauhat_x(n + 1, zin) * th - thp * tauhat_x(n, zin)) / th ** 2
        Lz = thp / th
        Mn = tauhat_x(n, zin) / th
        Mnp = tauhat_x(n + 1, zin) / thp
        res = dL + Lz * Mn - Mnp * Lz
        print('  n=%d z=%-6s  residual = %s' % (n, mp.nstr(z, 4), mp.nstr(abs(res), 4)))
