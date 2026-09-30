"""
conserved.py -- THE decisive test.

tr T(z) = sum_k I_k / z^k  gives candidate conserved densities I_k.
Being nonzero is not enough -- they must be CONSTANT along the (x,y,t) flow.

We compute I_1, I_2, I_3 by fitting tr T(z) at large z, at SEVERAL distinct
(x,y,t) points, and check whether each I_k is independent of x, y, t.
"""
import sys
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Workspaces\gsg_project\lax')
from tau4 import Tau

mp.mp.dps = 80
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2]
N = 3
T = Tau(N, A, H, PS, QS)


def make(Xv, Yv, Tv):
    TAU = {n: T.tau(n, xv=Xv, yv=Yv, tv=Tv) for n in range(-4, 8)}

    def psi(n, z):
        z = mp.mpf(z)
        return T.tau(n, xv=Xv - 1 / z, yv=Yv, tv=Tv - mp.mpf(1) / 2 / z ** 2) / TAU[n]

    def AB(n, z):
        p1, p0, pm, p2 = psi(n + 1, z), psi(n, z), psi(n - 1, z), psi(n + 2, z)
        dd = p1 * pm - p0 * p0
        return ((-p2 * pm + p1 * p0) / dd, (p1 * (-p1) - p0 * (-p2)) / dd)

    def trT(z):
        prod = mp.eye(2)
        for n in (-1, 0, 1):
            An, Bn = AB(n, z)
            prod = mp.matrix([[-An, -Bn], [1, 0]]) * prod
        return prod[0, 0] + prod[1, 1]
    return trT


def fit_I(trT, zs, nord=4):
    Mx = mp.matrix(nord, nord)
    rhs = mp.matrix(nord, 1)
    for r, zz in enumerate(zs):
        for c in range(nord):
            Mx[r, c] = 1 / mp.mpf(zz) ** c
        rhs[r] = trT(mp.mpf(zz))
    return mp.lu_solve(Mx, rhs)


zs = [mp.mpf(10) ** 4, mp.mpf(10) ** 5, mp.mpf(10) ** 6, mp.mpf(10) ** 7]

print('=' * 96)
print('I_k from  tr T(z) = I_0 + I_1/z + I_2/z^2 + I_3/z^3  at various (x,y,t)')
print('=' * 96)
pts = [
    (mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100),
    (mp.mpf(1) / 50, mp.mpf(-1) / 100, mp.mpf(1) / 100),
    (mp.mpf(1) / 100, mp.mpf(-1) / 50, mp.mpf(1) / 100),
    (mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 50),
    (mp.mpf(3) / 100, mp.mpf(-2) / 100, mp.mpf(7) / 200),
]
rows = []
for (Xv, Yv, Tv) in pts:
    trT = make(Xv, Yv, Tv)
    sol = fit_I(trT, zs)
    rows.append((Xv, Yv, Tv, sol))
    print('   (x,y,t)=(%-8s,%-8s,%-8s)  I0=%-20s I1=%-20s I2=%-20s I3=%s'
          % (mp.nstr(Xv, 5), mp.nstr(Yv, 5), mp.nstr(Tv, 5),
             mp.nstr(sol[0], 14), mp.nstr(sol[1], 14), mp.nstr(sol[2], 14), mp.nstr(sol[3], 14)))

print()
print('=' * 96)
print('Are the I_k CONSTANT (conserved)?   relative spread over the 5 points')
print('=' * 96)
for k in range(4):
    vals = [r[3][k] for r in rows]
    mx = max(vals)
    mn = min(vals)
    spread = abs(mx - mn) / max(abs(mx), abs(mn), mp.mpf('1e-40'))
    print('   I_%d :  min=%-22s max=%-22s   rel.spread=%s' % (k, mp.nstr(mn, 16), mp.nstr(mx, 16), mp.nstr(spread, 4)))
