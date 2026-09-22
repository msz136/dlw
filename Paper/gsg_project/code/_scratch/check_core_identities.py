"""
Core identity test:  GSG-style y-discretization of the DLW bilinear system.

  continuous:   (7)  B f.g = 0 ,                B = D_x^2 + D_t + 2a D_x
                (6)  D_y B f.g + 2 lam D_x f.g = 0 ,   lam = -2

  GSG device:   e^{y/P} -> (1 - h/P)^{-j}  (row),  e^{y/Q} -> (1 - h/Q)^{-j} (col)

  candidates:
    (D7)  B f_j . g_j = 0                                    (site-wise)
    (D6)  (1/h)[ B f_{j+1}.g_j - B f_j.g_{j+1} ] - 4 D_x f_j.g_j = 0
"""
import time
import sympy as sp
from engine import DLW, zero_at_points, e_add, e_scale


def make_D7(m):
    f, g = m.tau(1), m.tau(0)
    return m.B(f, g)


def make_D6(m):
    f, g = m.tau(1), m.tau(0)
    f1, g1 = m.tau(1, jshift=1), m.tau(0, jshift=1)
    two_site = e_add(m.B(f1, g), e_scale(m.B(f, g1), -1))
    two_site = e_scale(two_site, 1 / m.h)
    return e_add(two_site, e_scale(m.Dx(f, g), -4))


def make_D6_shifted(m):
    """Same identity centered at j+1 (translation invariance check)."""
    f, g = m.tau(1, jshift=1), m.tau(0, jshift=1)
    f1, g1 = m.tau(1, jshift=2), m.tau(0, jshift=2)
    two_site = e_add(m.B(f1, g), e_scale(m.B(f, g1), -1))
    two_site = e_scale(two_site, 1 / m.h)
    return e_add(two_site, e_scale(m.Dx(f, g), -4))


def make_D6_generic_lam(m):
    lam = sp.Symbol('lam')
    f, g = m.tau(1), m.tau(0)
    f1, g1 = m.tau(1, jshift=1), m.tau(0, jshift=1)
    two_site = e_scale(e_add(m.B(f1, g), e_scale(m.B(f, g1), -1)), 1 / m.h)
    return e_add(two_site, e_scale(m.Dx(f, g), 2 * lam))


if __name__ == '__main__':
    H = sp.Symbol('h', positive=True)
    for N in (1, 2, 3):
        t0 = time.time()
        ok7, d7 = zero_at_points(make_D7, N, trials=3, kind='exp', h=H)
        ok6, d6 = zero_at_points(make_D6, N, trials=3, kind='exp', h=H)
        ok6s, _ = zero_at_points(make_D6_shifted, N, trials=2, kind='exp', h=H)
        ok6g, _ = zero_at_points(make_D6_generic_lam, N, trials=1, kind='exp', h=H)
        print(f"N={N}:  (D7) site-wise = {'OK' if ok7 else 'FAIL'}"
              f"   (D6) two-site lam=-2 = {'OK' if ok6 else 'FAIL'}"
              f"   (D6)@j+1 = {'OK' if ok6s else 'FAIL'}"
              f"   (D6) generic lam = {'zero (unexpected!)' if ok6g else 'nonzero (expected)'}"
              f"   [{time.time()-t0:.1f}s]", flush=True)
        if not ok7:
            print("   D7 residual sample:", list(d7[1].items())[:2])
        if not ok6:
            print("   D6 residual sample:", list(d6[1].items())[:2])
