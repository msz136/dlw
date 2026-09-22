"""
verify_structure.py -- robust (mpmath, 60 digits) verification of the core
structural facts about the GSG semidiscrete DLW tau function.

Points used are generic (non-resonant).
"""
import sys
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')
from mpt import MP

mp.mp.dps = 60
X = mp.mpf(1) / 3
Y = mp.mpf(-2) / 5
T = mp.mpf(3) / 7
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
# generic spectral data
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7), mp.mpf(31) / 4]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2, mp.mpf(13) / 3]
CV = [mp.mpf(1), mp.mpf(3) / 2, mp.mpf(2) / 3, mp.mpf(5) / 4]


def rel(x, y):
    return abs(x - y) / max(abs(x), abs(y), mp.mpf(1))


print('=' * 92)
print('1. sigma_n = tau_{n+1} tau_{n-1}/tau_n^2  and  sigma_j = tau(j+1)tau(j-1)/tau_j^2')
print('=' * 92)
for N in (1, 2, 3, 4):
    M = MP(N, A, H, PS[:N], QS[:N], CV[:N])
    for j in (0, 1, 2):
        sn = M.tau(1, j, xv=X, yv=Y, tv=T) * M.tau(-1, j, xv=X, yv=Y, tv=T) / \
            M.tau(0, j, xv=X, yv=Y, tv=T) ** 2
        print('   N=%d j=%d  sigma_n = %s' % (N, j, mp.nstr(sn, 25)))
    for n in (0, 1):
        sj = M.tau(n, 1, xv=X, yv=Y, tv=T) * M.tau(n, -1, xv=X, yv=Y, tv=T) / \
            M.tau(n, 0, xv=X, yv=Y, tv=T) ** 2
        print('   N=%d n=%d  sigma_j = %s' % (N, n, mp.nstr(sj, 25)))

print()
print('=' * 92)
print('2. is tau_n / C^n n-independent?   (C = tau_1/tau_0)')
print('=' * 92)
for N in (2, 3, 4):
    for j in (0, 1):
        M = MP(N, A, H, PS[:N], QS[:N], CV[:N])
        t0 = M.tau(0, j, xv=X, yv=Y, tv=T)
        t1 = M.tau(1, j, xv=X, yv=Y, tv=T)
        tm = M.tau(-1, j, xv=X, yv=Y, tv=T)
        C = t1 / t0
        print('   N=%d j=%d  C=%s   tau_{-1}*C^2/tau_1 = %s   tau_0*C/tau_1 = %s'
              % (N, j, mp.nstr(C, 18),
                 mp.nstr(tm * C ** 2 / t1, 18), mp.nstr(t0 * C / t1, 18)))

print()
print('=' * 92)
print('3. the 2DTL bilinear equation  (1/2 Dx Dy - 1) tau_n.tau_n + tau_{n+1}tau_{n-1} = 0')
print('=' * 92)
for N in (2, 3, 4):
    M = MP(N, A, H, PS[:N], QS[:N], CV[:N])
    for n in (-1, 0, 1):
        for j in (0, 1):
            t0 = M.tau(n, j, xv=X, yv=Y, tv=T)
            txy = M.dtau(n, j, M.a, X, Y, T, {'x': 1, 'y': 1})
            tx = M.dtau(n, j, M.a, X, Y, T, {'x': 1})
            ty = M.dtau(n, j, M.a, X, Y, T, {'y': 1})
            t1 = M.tau(n + 1, j, xv=X, yv=Y, tv=T)
            tm = M.tau(n - 1, j, xv=X, yv=Y, tv=T)
            res = mp.mpf(1) / 2 * (txy * t0 - tx * ty) - t0 * t0 + t1 * tm
            scale = abs(t0 * t0) + abs(t1 * tm) + abs(txy * t0)
            print('   N=%d n=%d j=%d   2DTL rel.resid = %s' % (N, n, j, mp.nstr(res / scale, 12)))

print()
print('=' * 92)
print('4. the semidiscrete bilinear pair (7)_h and (6)_h  [staggered]')
print('    (7)_h: B_{a-d} F_j . G_j = 0,   (6)_h: B_{a+d} F_j . G_{j+1} = 0')
print('=' * 92)
d = H / 2


def B(M, F, G, s):
    """B_s F.G = D_x^2 F.G + D_t F.G + 2 s D_x F.G, exact via rates."""
    out = mp.mpf(0)
    # in our monomial representation F.G derivative is a product of two
    # independent permutations; use the bilinear expansion
    return out


# do it with the standard bilinear expansion on the monomial dictionaries
def btau(M, n1, j1, s1, n2, j2, s2, ax=0, at=0):
    """D_x^ax D_t^at tau_{n1}(j1;s1) . tau_{n2}(j2;s2) evaluated at (X,Y,T)."""
    from math import comb
    tot = mp.mpf(0)
    for p_ in range(ax + 1):
        for r_ in range(at + 1):
            co = (-1) ** (p_ + r_) * comb(ax, p_) * comb(at, r_)
            A_ = M.dtau(n1, j1, s1, X, Y, T, {'x': ax - p_, 't': at - r_})
            B_ = M.dtau(n2, j2, s2, X, Y, T, {'x': p_, 't': r_})
            tot += co * A_ * B_
    return tot


for N in (1, 2, 3, 4):
    M = MP(N, A, H, PS[:N], QS[:N], CV[:N])
    for j in (0, 1, 2):
        # (7)_h
        r7 = btau(M, 1, j, A - d, 0, j, A, ax=2) + btau(M, 1, j, A - d, 0, j, A, at=1) \
            + 2 * (A - d) * btau(M, 1, j, A - d, 0, j, A, ax=1)
        # (6)_h  : F_j . G_{j+1} with operator parameter a+d
        r6 = btau(M, 1, j, A - d, 0, j + 1, A, ax=2) + btau(M, 1, j, A - d, 0, j + 1, A, at=1) \
            + 2 * (A + d) * btau(M, 1, j, A - d, 0, j + 1, A, ax=1)
        # scale: F*G magnitude
        Fv = M.tau(1, j, s=A - d, xv=X, yv=Y, tv=T)
        Gv = M.tau(0, j + 1, s=A, xv=X, yv=Y, tv=T)
        sc = abs(Fv * Gv) + mp.mpf('1e-300')
        print('   N=%d j=%d   (7)_h = %s   (6)_h = %s'
              % (N, j, mp.nstr(r7 / sc, 10), mp.nstr(r6 / sc, 10)))
