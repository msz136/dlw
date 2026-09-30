"""
Search for a lattice equation that plays the role of (6) on the y-lattice.

(6)  at lam=-2  is  D_y B f.g = 4 D_x f.g .
On the lattice D_y must become a difference.  We test every natural stencil
against the lattice tau, exactly, at generic rational points.
"""
import sympy as sp
from engine import DLW, e_add, e_scale, zero_at_points

H = sp.Rational(1, 3)


def shift(m, d, s):
    return m.shift(d, s)


CANDIDATES = {}


def cand(name):
    def deco(fn):
        CANDIDATES[name] = fn
        return fn
    return deco


@cand("forward two-site   (1/h)[B f_{j+1}.g_j - B f_j.g_{j+1}] - 4D_x f_j.g_j")
def c1(m):
    f, g = m.tau(1), m.tau(0)
    f1, g1 = m.tau(1, jshift=1), m.tau(0, jshift=1)
    return e_add(e_scale(e_add(m.B(f1, g), e_scale(m.B(f, g1), -1)), 1 / m.h),
                 e_scale(m.Dx(f, g), -4))


@cand("backward two-site  (1/h)[B f_j.g_{j-1} - B f_{j-1}.g_j] - 4D_x f_j.g_j")
def c2(m):
    f, g = m.tau(1), m.tau(0)
    fm, gm = m.tau(1, jshift=-1), m.tau(0, jshift=-1)
    return e_add(e_scale(e_add(m.B(f, gm), e_scale(m.B(fm, g), -1)), 1 / m.h),
                 e_scale(m.Dx(f, g), -4))


@cand("centred 3-site     (1/2h)[B f_{j+1}.g_{j-1} - B f_{j-1}.g_{j+1}] - 4D_x f_j.g_j")
def c3(m):
    f, g = m.tau(1), m.tau(0)
    fp, gp = m.tau(1, jshift=1), m.tau(0, jshift=1)
    fm, gm = m.tau(1, jshift=-1), m.tau(0, jshift=-1)
    return e_add(e_scale(e_add(m.B(fp, gm), e_scale(m.B(fm, gp), -1)), 1 / (2 * m.h)),
                 e_scale(m.Dx(f, g), -4))


@cand("centred diagonal   (1/2h)[B f_{j+1}.g_j - B f_{j-1}.g_{j-1}... ]")
def c4(m):
    f, g = m.tau(1), m.tau(0)
    fp, gp = m.tau(1, jshift=1), m.tau(0, jshift=1)
    fm, gm = m.tau(1, jshift=-1), m.tau(0, jshift=-1)
    return e_add(e_scale(e_add(m.B(fp, g), e_scale(m.B(fm, g), -1)), 1 / (2 * m.h)),
                 e_scale(m.Dx(f, g), -4))


@cand("mixed             (1/2h)[B f_{j+1}.g_j - B f_j.g_{j+1} + B f_j.g_{j-1} - B f_{j-1}.g_j] - 4D_x")
def c5(m):
    f, g = m.tau(1), m.tau(0)
    fp, gp = m.tau(1, jshift=1), m.tau(0, jshift=1)
    fm, gm = m.tau(1, jshift=-1), m.tau(0, jshift=-1)
    a1 = e_add(m.B(fp, g), e_scale(m.B(f, gp), -1))
    a2 = e_add(m.B(f, gm), e_scale(m.B(fm, g), -1))
    return e_add(e_scale(e_add(a1, a2), 1 / (2 * m.h)), e_scale(m.Dx(f, g), -4))


@cand("staggered         (1/h)[B_(a+d) f_j.g_{j+1} - B_(a-d) f_j.g_j] - 4D_x f_j.g_j   [f=T_{a-d}]")
def c6(m):
    F = m.tau(1, a_shift=-m.h / 2)
    G = m.tau(0)
    Gp = m.tau(0, jshift=1)
    Em = m.B(F, G, s=m.a - m.h / 2)
    Ep = m.B(F, Gp, s=m.a + m.h / 2)
    return e_add(e_scale(e_add(Ep, e_scale(Em, -1)), 1 / m.h),
                 e_scale(m.Dx(F, G), -4))


print("=" * 100)
print("candidate lattice replacements for (6)   (kind = lattice multiplier)")
print("=" * 100)
for kind in ('exp', 'expneg', 'sym'):
    print(f"\n--- kind = {kind} ---")
    for name, fn in CANDIDATES.items():
        row = []
        for N in (1, 2):
            try:
                ok, det = zero_at_points(fn, N, trials=2, h=H, kind=kind)
            except Exception as ex:
                ok = f"ERR:{type(ex).__name__}"
            row.append(f"N={N}:{'ZERO   ' if ok is True else ('nonzero' if ok is False else ok)}")
        print(f"   {name}\n        " + "   ".join(row), flush=True)
