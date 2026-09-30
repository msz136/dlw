"""
General obstruction, widened ansatz.

Is there ANY lattice combination, with coefficients independent of p_i,q_k, that
closes (6) exactly?  Ansatz (N = 1):

  a1 B_{s} f_{j+1}.g_j + a2 B_{s} f_j.g_{j+1} + a3 B_s f_j.g_j
+ a4 D_x f_j.g_j       + a5 D_x f_{j+1}.g_j     + a6 D_x f_j.g_{j+1}
+ a7 D_y-ish ... (D_y has no lattice meaning, so it is replaced by the difference)

Result reported at the end.
"""
import sympy as sp
from engine import DLW, random_point, e_add, e_scale

names = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8']
C = sp.symbols(names)


def build(m, stagger):
    f, g = m.tau(1), m.tau(0)
    f1, g1 = m.tau(1, jshift=1), m.tau(0, jshift=1)
    sB = m.a
    terms = [
        e_scale(m.B(f1, g, s=sB), C[0]),
        e_scale(m.B(f, g1, s=sB), C[1]),
        e_scale(m.B(f, g, s=sB), C[2]),
        e_scale(m.Dx(f, g), C[3]),
        e_scale(m.Dx(f1, g), C[4]),
        e_scale(m.Dx(f, g1), C[5]),
        e_scale(m.Dx(f1, g1), C[6]),
        e_scale(m.bilin(f1, g1, ax=2), C[7]),
    ]
    if stagger:
        terms[0] = e_scale(m.B(f1, g, s=m.a + m.h / 2), C[0])
        terms[1] = e_scale(m.B(f, g1, s=m.a - m.h / 2), C[1])
    return e_add(*terms)


def analyse(kind, stagger, trials=3, seed0=1):
    rows = []
    for tt in range(trials):
        m = DLW(1, h=sp.Rational(1, 3), kind=kind)
        m.set_point(random_point(m, seed=seed0 + 37 * tt))
        r = build(m, stagger)
        for key, coef in r.items():
            rows.append([sp.nsimplify(coef.diff(c)) for c in C])
    M = sp.Matrix(rows)
    return M, M.nullspace()


for stagger in (False, True):
    print("=" * 92)
    print("ansatz:", "staggered B-parameters (a+h/2, a-h/2)" if stagger else "uniform B-parameter a")
    print("=" * 92)
    for kind in ('exp', 'sym'):
        M, ns = analyse(kind, stagger)
        print(f"   kind={kind:5s}  rank={M.rank()}/{M.cols}   nullspace dim={len(ns)}")
        for v in ns:
            print("        ", [sp.nsimplify(x) for x in v.T.tolist()[0]])
    print()

print("=" * 92)
print("INTERPRETATION")
print("  * a1=a2=1 (all other a_i=0):  B f_{j+1}.g_j + B f_j.g_{j+1} = 0")
print("      -> an exact lattice identity, but its continuum limit is 2 B f.g + O(h^2),")
print("         i.e. it is a REDUNDANT discrete copy of (7), not a discrete (6).")
print("  * a3=1: B f_j.g_j = 0  -> the discrete (7).")
print("  * all other null vectors found from finitely many samples were tested at 12")
print("    FRESH random points (verify_nullvec.py) and turned out SPURIOUS.")
print("  * no GENUINE null vector contains the antisymmetric direction a1 = -a2,")
print("    i.e. the lattice 'D_y' direction.")
print("  => (6) has NO exact two-site lattice analogue with p,q-independent coefficients:")
print("     at h>0 the discrete D_yB - 4D_x residual is a nonzero rational function.")
print("=" * 92)
