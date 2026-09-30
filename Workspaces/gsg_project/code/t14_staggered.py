"""
Verify the GSG-style (spectral-shift / staggered) semi-discretisation of the DLW
bilinear pair (6),(7) independently, with the corrected exponential engine.

Objects (d = h/2, P_i = p_i - a, Q_k = q_k + a):
    G_j      = det( delta_ik + M_ik(j) )                   -- n = 0 tau
    F_j      = det( delta_ik - ((P_i+d)/(Q_k-d)) M_ik(j) ) -- n = 1 tau, a -> a-d
    M_ik(j)  = e^{xi_i+eta_k}/(p_i+q_k) ((P_i+d)/(P_i-d))^j ((Q_k+d)/(Q_k-d))^j

Identity (exact, entry-wise):
    F_{j+1} = T_{a+d}(M(j+1)) = T_{a-d}(M(j)) = F_j
where "T_{a+d}(M(j+1))" means the n=1 tau with a -> a+d at site j+1.
"""
import sympy as sp
from engine import DLW, e_add, e_scale, e_mul, zero_at_points, random_point

h = sp.Symbol('h', positive=True)


def mk(N, hval, kind='sym'):
    m = DLW(N, h=h, kind=kind)
    m.set_point(random_point(m, seed=11 + N))
    if hval is not None:
        m.h = hval
        m._xx = None
    return m


print("=" * 78)
print("C1  exact identity:  F_{j+1} = T_{a+d}(M(j+1)) = T_{a-d}(M(j)) = F_j")
print("=" * 78)
for N in (1, 2, 3):
    m = DLW(N, h=h, kind='sym')
    m.set_point(random_point(m, seed=5 + N))
    lhs = m.tau(1, jshift=1, a_shift=+m.h / 2)      # T_{a+d}(M(j+1))
    rhs = m.tau(1, jshift=0, a_shift=-m.h / 2)      # T_{a-d}(M(j))
    same = (lhs.keys() == rhs.keys()) and all(
        sp.simplify(lhs[k] - rhs[k]) == 0 for k in lhs)
    print(f"  N={N}:  F_(j+1) == F_j  ->  {'OK' if same else 'FAIL'}")

print()
print("=" * 78)
print("C2/C3  staggered lattice equations   (d = h/2)")
print("=" * 78)
hval = sp.Rational(1, 3)
for N in (1, 2, 3, 4):
    def E_minus(mm):
        F = mm.tau(1, jshift=0, a_shift=-mm.h / 2)
        G = mm.tau(0, jshift=0)
        return mm.B(F, G, s=mm.a - mm.h / 2)
    def E_plus(mm):
        F = mm.tau(1, jshift=0, a_shift=-mm.h / 2)
        G = mm.tau(0, jshift=1)
        return mm.B(F, G, s=mm.a + mm.h / 2)
    ok_m, dm = zero_at_points(E_minus, N, trials=2, h=hval, kind='sym')
    ok_p, dp = zero_at_points(E_plus, N, trials=2, h=hval, kind='sym')
    print(f"  N={N}:  B_(a-d)F_j.G_j=0 -> {'OK ' if ok_m else 'FAIL'}"
          f"   B_(a+d)F_j.G_(j+1)=0 -> {'OK ' if ok_p else 'FAIL'}", flush=True)

print()
print("=" * 78)
print("C4  what happens for the PLAIN two-site difference of B f.g ?  (kind='exp')")
print("=" * 78)
for kind in ('exp', 'expneg', 'sym'):
    for N in (1, 2):
        def naive(mm):
            f = mm.tau(1, jshift=0); g = mm.tau(0, jshift=0)
            f1 = mm.tau(1, jshift=1); g1 = mm.tau(0, jshift=1)
            d = e_scale(e_add(mm.B(f1, g), e_scale(mm.B(f, g1), -1)), 1 / mm.h)
            return e_add(d, e_scale(mm.Dx(f, g), -4))
        ok, det = zero_at_points(naive, N, trials=2, h=hval, kind=kind)
        print(f"  kind={kind:7s} N={N}:  (1/h)[B f_(j+1).g_j - B f_j.g_(j+1)] - 4 D_x f_j.g_j"
              f" -> {'ZERO' if ok else 'NONZERO'}", flush=True)
