"""
final_test.py -- THE decisive integrability test.

For a genuine Lax pair the SPECTRAL CURVE must be an invariant of the flow:
for each fixed spectral parameter z,  tr T(z)  must be INDEPENDENT of (x,y,t).

  tr T(z)  independent of (x,y,t)  =>  conserved generating function
                                       => strong integrability
  tr T(z)  varies with (x,y,t)     =>  no conserved quantity
                                       => NOT strongly integrable
"""
import sys
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')
from tau4 import Tau

mp.mp.dps = 80
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2]
N = 3
T = Tau(N, A, H, PS, QS)


def trT_at(Xv, Yv, Tv, z):
    z = mp.mpf(z)
    TAU = {n: T.tau(n, xv=Xv, yv=Yv, tv=Tv) for n in range(-4, 8)}

    def psi(n):
        return T.tau(n, xv=Xv - 1 / z, yv=Yv, tv=Tv - mp.mpf(1) / 2 / z ** 2) / TAU[n]

    def AB(n):
        p1, p0, pm, p2 = psi(n + 1), psi(n), psi(n - 1), psi(n + 2)
        dd = p1 * pm - p0 * p0
        return ((-p2 * pm + p1 * p0) / dd, (p1 * (-p1) - p0 * (-p2)) / dd)

    prod = mp.eye(2)
    for n in (-1, 0, 1):
        An, Bn = AB(n)
        prod = mp.matrix([[-An, -Bn], [1, 0]]) * prod
    return prod[0, 0] + prod[1, 1]


pts = [
    (mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100),
    (mp.mpf(2) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100),
    (mp.mpf(1) / 100, mp.mpf(-2) / 100, mp.mpf(1) / 100),
    (mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(2) / 100),
    (mp.mpf(3) / 100, mp.mpf(-2) / 100, mp.mpf(35) / 1000),
]

print('=' * 98)
print('TEST: is tr T(z) independent of (x,y,t) for FIXED z?')
print('      (independence => conserved generating function => strong integrability)')
print('=' * 98)
for z in (mp.mpf(3), mp.mpf(10), mp.mpf(50), mp.mpf(500)):
    vals = [trT_at(X, Y, Tv, z) for (X, Y, Tv) in pts]
    mx, mn = max(vals), min(vals)
    spread = abs(mx - mn) / max(abs(mx), abs(mn))
    print('   z=%-8s  tr T: %s' % (mp.nstr(z, 5), '  '.join(mp.nstr(v, 12) for v in vals)))
    print('              rel.spread over (x,y,t) = %s' % mp.nstr(spread, 4))

print()
print('=' * 98)
print('CONTROL: the same test for the conserved quantity that DOES exist,')
print('         d_x ln tau_n  (which is a constant rate, independent of x,y,t,j)')
print('=' * 98)
for n in (0, 1):
    vals = []
    for (X, Y, Tv) in [(mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100),
                       (mp.mpf(1) / 50, mp.mpf(-1) / 100, mp.mpf(1) / 100)]:
        t0 = T.tau(n, xv=X, yv=Y, tv=Tv)
        B = T.Bmat(n, T.a, X, Y, Tv)
        import itertools
        from tau4 import det_exact
        tot = mp.mpf(0)
        for r in range(N + 1):
            for S in itertools.combinations(range(N), r):
                sub = mp.matrix(r, r)
                for a2, i in enumerate(S):
                    for b2, k in enumerate(S):
                        sub[a2, b2] = B[i, k] * (T.p[i] + T.q[k])
                tot += det_exact(sub)
        vals.append(tot / t0)
    print('   n=%d  d_x ln tau at two points: %s   equal = %s'
          % (n, ' '.join(mp.nstr(v, 14) for v in vals),
             abs(vals[0] / vals[1] - 1) < mp.mpf('1e-40')))
