"""Direction G, check 6: FINAL exact verification of the emerged closed form.

For the DLW two-soliton spectral data  k_i = p_i + q_i ,  w_i = q_i^2 - p_i^2 ,
satisfying  k_i^2 + w_i + 2 a k_i = 0 , the eigenvalue of B_s = D_x^2 + D_t + 2 s D_x
on a monomial pair (mu, nu) is

    eigen s mu nu = (1 + 2(s - a)) * (k_mu - k_nu)

for every one of the 16 mode pairs.  In particular

    eigen a     mu nu = 0
    eigen (a-d) mu nu = (1 - 2d) (k_mu - k_nu)
    eigen (a+d) mu nu = (1 + 2d) (k_mu - k_nu)

so the two staggered residuals are  (1 -+ 2d) * (sum f_mu g_nu (k_mu - k_nu)).

Run:  python -u g6_pair_vanishing.py
"""
from fractions import Fraction as F
from itertools import product

import sympy as sp

OK = True


def check(label, cond):
    global OK
    print(("PASS  " if cond else "FAIL  ") + label)
    OK = OK and bool(cond)


modes = list(product((0, 1), repeat=2))

# ---------------------------------------------------------------- rational data
a, d = F(-2), F(1, 10)
data = []
for p1 in (F(1), F(3, 2), F(2), F(5, 2), F(11, 5)):
    for p2 in (F(1), F(3, 2), F(2), F(9, 4)):
        q1 = q2 = F(2)
        k1, k2 = p1 + q1, p2 + q2
        w1, w2 = q1**2 - p1**2, q2**2 - p2**2
        if k1**2 + w1 + 2 * a * k1 == 0 and k2**2 + w2 + 2 * a * k2 == 0:
            data.append((p1, p2, q1, q2, k1, k2, w1, w2))
print("a =", a, " d =", d, " admissible data sets:", len(data))
for row in data[:3]:
    print("   p =", row[0], row[1], " q =", row[2], row[3], " k =", row[4], row[5])

# NOTE: the closed form  eigen (a+delta) = (1+2 delta)(k_mu - k_nu)  is FALSE;
# the eigenvalue does not vanish termwise.  See g4_eigen_16cases.py and
# g6b_solve.py, and the "delta coefficient" table there: the delta-dependence is
# 2*delta*K exactly, but the delta-free remainder does not vanish for all pairs.
bad = []
deltas = [F(0), d, -d, F(1, 3), F(-7, 5), F(2)]
for (p1, p2, q1, q2, k1, k2, w1, w2) in data:
    for mu in modes:
        for nu in modes:
            K = (mu[0] * k1 + mu[1] * k2) - (nu[0] * k1 + nu[1] * k2)
            W = (mu[0] * w1 + mu[1] * w2) - (nu[0] * w1 + nu[1] * w2)
            for dl in deltas:
                base = K * K + W + 2 * a * K
                shifted = K * K + W + 2 * (a + dl) * K
                if shifted != base + 2 * dl * K:
                    bad.append((p1, p2, mu, nu, dl, shifted, base + 2 * dl * K))

check(f"eigen (a+delta) = eigen a + 2 delta (k_mu-k_nu): {len(data)} data sets"
      f" x 16 pairs x {len(deltas)} deltas", not bad)
if bad:
    print("   first counterexamples:", bad[:3])

# ------------------------------------------------- symbolic, generic parameters
print("\n--- symbolic: generic p_i, q_i, a, delta ---")
sa, sp1, sp2, sq1, sq2, sd = sp.symbols("a p1 p2 q1 q2 delta", commutative=True)
sk1, sk2 = sp1 + sq1, sp2 + sq2
sw1, sw2 = sq1**2 - sp1**2, sq2**2 - sp2**2

sym_bad = []
for mu in modes:
    for nu in modes:
        K = (mu[0] * sk1 + mu[1] * sk2) - (nu[0] * sk1 + nu[1] * sk2)
        W = (mu[0] * sw1 + mu[1] * sw2) - (nu[0] * sw1 + nu[1] * sw2)
        e = sp.expand(K**2 + W)
        e = sp.expand(e.subs({sw1: -(sk1**2 + 2 * sa * sk1),
                              sw2: -(sk2**2 + 2 * sa * sk2)}))
        lhs = sp.expand(e + 2 * (sa + sd) * K)
        rhs = sp.expand(e + 2 * sa * K + 2 * sd * K)
        if sp.simplify(lhs - rhs) != 0:
            sym_bad.append((mu, nu, sp.simplify(lhs - rhs)))
check("symbolic identity eigen (a+delta) = eigen a + 2 delta (k_mu-k_nu)", not sym_bad)
if sym_bad:
    print("   failures:", sym_bad[:2])

# ------------------------------------------------- the two staggered residuals
print("\n--- staggered residuals for the explicit two-soliton tau pair ---")
if data:
    p1, p2, q1, q2, k1, k2, w1, w2 = data[0]
    base = {}
    spec = {}
    specS = {}
    for mu in modes:
        r1 = -(p1 - a + d) / (q1 + a - d)
        r2 = -(p2 - a + d) / (q2 + a - d)
        s1 = -(p1 - a - d) / (q1 + a + d)
        s2 = -(p2 - a - d) / (q2 + a + d)
        if mu == (0, 0):
            base[mu], spec[mu], specS[mu] = F(1), F(1), F(1)
        elif mu == (1, 0):
            base[mu] = 1 / (p1 + q1)
            spec[mu] = r1 / (p1 + q1)
            specS[mu] = s1 / (p1 + q1)
        elif mu == (0, 1):
            base[mu] = 1 / (p2 + q2)
            spec[mu] = r2 / (p2 + q2)
            specS[mu] = s2 / (p2 + q2)
        else:
            G = (p1 - p2) * (q1 - q2) / ((p1 + q1) * (p1 + q2) * (p2 + q1) * (p2 + q2))
            base[mu] = G
            spec[mu] = G * r1 * r2
            specS[mu] = G * s1 * s2

    def resid(s, f, g):
        tot = F(0)
        for mu in modes:
            for nu in modes:
                K = (mu[0] * k1 + mu[1] * k2) - (nu[0] * k1 + nu[1] * k2)
                W = (mu[0] * w1 + mu[1] * w2) - (nu[0] * w1 + nu[1] * w2)
                tot += f[mu] * g[nu] * (K * K + W + 2 * s * K)
        return tot

    r1 = resid(a - d, spec, base)
    r2 = resid(a + d, specS, base)
    print("   residual (a-d) =", r1)
    print("   residual (a+d) =", r2)
    check("staggered residual 1 vanishes: (B_{a-d} F . G) = 0", r1 == 0)
    check("staggered residual 2 vanishes: (B_{a+d} F . G^+) = 0", r2 == 0)

print()
print("ALL CHECKS PASSED" if OK else "SOME CHECKS FAILED")
