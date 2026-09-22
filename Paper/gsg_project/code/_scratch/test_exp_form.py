"""
y-lattice: test the 'exponentiated' discretization of D_y B:
  D_y B f.g = d/de|0 B f(y+e).g(y-e)  ->  (1/h)[B f_{j+1}.g_{j-1} - B f_j.g_j]
Since B f_j.g_j = 0 site-wise, candidate (D6):
  (1/h) B f_{j+1}.g_{j-1} - 4 D_x f_j.g_j = 0
Also test the centred version and the unreduced form.
"""
import time
import sympy as sp
from engine import DLW, zero_at_points, e_add, e_scale

H = sp.Symbol('h', positive=True)


def cand_A(m):  # (1/h) B f1.g-1 - 4 Dx f.g
    f0, g0 = m.tau(1), m.tau(0)
    f1 = m.tau(1, jshift=1)
    gm = m.tau(0, jshift=-1)
    return e_add(e_scale(m.B(f1, gm), 1 / m.h), e_scale(m.Dx(f0, g0), -4))


def cand_B(m):  # (1/2h)[B f1.g-1 - B f-1.g1] - 4 Dx f.g
    f0, g0 = m.tau(1), m.tau(0)
    f1, fm = m.tau(1, jshift=1), m.tau(1, jshift=-1)
    g1, gm = m.tau(0, jshift=1), m.tau(0, jshift=-1)
    two = e_add(m.B(f1, gm), e_scale(m.B(fm, g1), -1))
    return e_add(e_scale(two, 1 / (2 * m.h)), e_scale(m.Dx(f0, g0), -4))


def cand_C(m):  # (1/h)[B f1.g-1 - B f.g] - 4 Dx f.g   (B f.g=0 anyway)
    f0, g0 = m.tau(1), m.tau(0)
    f1 = m.tau(1, jshift=1)
    gm = m.tau(0, jshift=-1)
    two = e_add(m.B(f1, gm), e_scale(m.B(f0, g0), -1))
    return e_add(e_scale(two, 1 / m.h), e_scale(m.Dx(f0, g0), -4))


for name, cand in [('A: (1/h) B f1.g-1 - 4Dx f.g', cand_A),
                   ('B: (1/2h)[B f1.g-1 - B f-1.g1] - 4Dx f.g', cand_B),
                   ('C: (1/h)[B f1.g-1 - B f.g] - 4Dx f.g', cand_C)]:
    t0 = time.time()
    ok, detail = zero_at_points(cand, 2, trials=3, kind='exp', h=H)
    print(f"{name}: {'OK' if ok else 'FAIL'}  [{time.time()-t0:.1f}s]", flush=True)
    if not ok:
        pt, d = detail
        print("   residual sample:", list(d.items())[:2])
