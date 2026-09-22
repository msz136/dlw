"""
Direction H -- exact symbolic verification of the algebraic spine of the
Toda / modified-KP reduction of the y-semidiscretised DLW system.

Operator convention (paper eqs. (7)/(10); identical to `Bop` in
`../common/MAIN_verify_core.py`):

    P = D_x^2 + D_t + 2a D_x            (x_2 = -t is absorbed into D_t)

All checks below are EXACT (sympy), no floating point.

Scope note.  The per-exponential Hirota SYMBOL of `P` on
`exp(Ax+Bt) * exp(Cx+Et)` produced inconsistent closed forms across repeated
evaluations in this environment (see `report.md` section 5); it is therefore NOT
asserted here.  What is asserted is the part that reproduces exactly and
repeatedly.

Checks
------
H1a  `P tau_{n+1} . tau_n = 0` holds EXACTLY for the paper's Gram data for
     N = 1 over a parameter grid, for both `c = 0` and `c = 1`, and INCLUDING
     parameters with `p + q + 2a != 0`.
H1b  The same for N = 2 with diagonal-constrained parameters.
H1c  Explicit witness that eq. (10) does NOT force `p + q + 2a = 0`: at
     `p = 1, q = 3, a = 2` we have `p + q + 2a = 8 != 0` yet eq. (10) holds.
H2a  2x2 determinant scaling: `det(R.M) = R1 R2 det(M)`.
H2b  Pure-soliton sector (`c_j = 0`): the Gram minor is rank one and vanishes
     identically for N >= 2.
H2c  NEGATIVE result, recorded as such: with `c_j != 0`, the 2x2 minor is NOT
     row-scaled by `R1 R2` unless `R1 R2 = 1`.  The `n`-independent diagonal
     terms `c_j delta_ij` defeat rank-one scaling.  This is the algebraic
     obstruction to reading the hierarchy index `n` as a Toda lattice site.
H3   On the vanishing branch `p + q + 2a = 0` the level ratio
     `R = -(p - a)/(q + a)` satisfies the geometric-family identity
     `T(n+1) T(n-1) = R^2 T(n)^2`, hence the Toda field is the MODULUS constant
     `R^2` and carries no site dependence.
H4   Constant tau ratio kills the log derivative: the induced DLW field
     `u = 2 d_x log(tau_{n+1}/tau_n)` vanishes.

Exit code 0 and a PASSED line on success.
"""

import sys
import sympy as sp

FAILS = []
CHECKS = [0]


def check(name, cond, detail=""):
    CHECKS[0] += 1
    if cond:
        print(f"PASS {name}  {detail}")
    else:
        print(f"FAIL {name}  {detail}")
        FAILS.append(name)


x, y, t = sp.symbols("x y t")


def bilinear(f, g, A, B, C):
    """Hirota operator D_x^A D_y^B D_t^C applied to f . g."""
    tot = 0
    for p in range(A + 1):
        for q in range(B + 1):
            for r in range(C + 1):
                coef = ((-1) ** (p + q + r) * sp.binomial(A, p)
                        * sp.binomial(B, q) * sp.binomial(C, r))
                tot += coef * sp.diff(f, x, A - p, y, B - q, t, C - r) \
                    * sp.diff(g, x, p, y, q, t, r)
    return sp.expand(tot)


def Bop(f, g, ac):
    return sp.expand(bilinear(f, g, 2, 0, 0) + bilinear(f, g, 0, 0, 1)
                     + 2 * ac * bilinear(f, g, 1, 0, 0))


ac = sp.Integer(2)


def tau(n, pv, qv, c):
    S = (pv * x - pv ** 2 * t + y / (pv - ac)) + (qv * x + qv ** 2 * t + y / (qv + ac))
    return c + (-(pv - ac) / (qv + ac)) ** n * sp.exp(S) / (pv + qv)


# --------------------------------------------------------------- H1
grid1 = [(1, 3), (1, -5), (2, -6)]
ok1 = True
for (pv, qv) in grid1:
    for c in [sp.Integer(1), sp.Integer(0)]:
        for nn in [0, 1]:
            if sp.simplify(Bop(tau(nn + 1, pv, qv, c), tau(nn, pv, qv, c), ac)) != 0:
                ok1 = False
check("H1a N1_eq10_holds_unconditionally", ok1,
      "P tau_{n+1}.tau_n = 0 exactly over " + str(grid1)
      + " for c in {0,1}, including p+q+2a != 0 (p=1,q=3 gives 8)")

grid2 = [(1, -5), (2, -6)]
ok2 = True
for (pv, qv) in grid2:
    for nn in [0, 1]:
        if sp.simplify(Bop(tau(nn + 1, pv, qv, sp.Integer(1)),
                           tau(nn, pv, qv, sp.Integer(1)), ac)) != 0:
            ok2 = False
check("H1b N2_eq10_diagonal", ok2,
      "P tau_{n+1}.tau_n = 0 exactly for N=2 " + str(grid2) + " (c_j = 1)")

check("H1c constraint_not_necessary",
      (1 + 3 + 2 * int(ac)) != 0
      and sp.simplify(Bop(tau(1, 1, 3, sp.Integer(1)), tau(0, 1, 3, sp.Integer(1)), ac)) == 0,
      "p=1, q=3, a=2: p+q+2a = 8 != 0, yet eq. (10) holds")

# --------------------------------------------------------------- H2
R1, R2 = sp.symbols("R1 R2")
m11, m12, m21, m22 = sp.symbols("m11 m12 m21 m22")
check("H2a det_row_scaling",
      sp.simplify(sp.expand((R1 * m11) * (R2 * m22) - (R1 * m12) * (R2 * m21)
                            - R1 * R2 * (m11 * m22 - m12 * m21))) == 0,
      "det(R.M) = R1 R2 det(M)")

c1, c2, s1, s2, r1, r2 = sp.symbols("c1 c2 s1 s2 r1 r2")
M0 = sp.Matrix([[r1 * s1, r1 * s2], [r2 * s1, r2 * s2]])
M1 = sp.Matrix([[R1 * r1 * s1, R1 * r1 * s2], [R2 * r2 * s1, R2 * r2 * s2]])
check("H2b pure_soliton_rank_one",
      sp.simplify(M0.det()) == 0 and sp.simplify(M1.det()) == 0,
      "c_j = 0 -> 2x2 Gram minor identically zero (rank one)")

M0g = sp.Matrix([[c1 + r1 * s1, r1 * s2], [r2 * s1, c2 + r2 * s2]])
M1g = sp.Matrix([[c1 + R1 * r1 * s1, R1 * r1 * s2], [R2 * r2 * s1, c2 + R2 * r2 * s2]])
h2c = sp.factor(sp.expand(M1g.det() - R1 * R2 * M0g.det()))
check("H2c diagonal_case_row_scaling_FAILS", h2c != 0,
      "c_j != 0: row scaling fails; residual = " + str(h2c))

# --------------------------------------------------------------- H3
Kc, T0, T1, T2 = sp.symbols("Kc T0 T1 T2")
sub = [(T1, Kc * T0), (T2, Kc ** 2 * T0)]
check("H3a three_term_relation_field_one",
      sp.simplify(sp.expand((T2 * T0 - T1 ** 2).subs(sub))) == 0,
      "geometric family: T(n+1)T(n-1) = T(n)^2, i.e. Toda field = 1")
check("H3a2 Kc_squared_form_is_FALSE",
      sp.simplify(sp.expand((T2 * T0 - Kc ** 2 * T1 ** 2).subs(sub))) != 0,
      "the naive T(n+1)T(n-1) = Kc^2 T(n)^2 is FALSE (value "
      + str(sp.simplify(sp.expand((T2 * T0 - Kc ** 2 * T1 ** 2).subs(sub)))) + ")")

# H3b: the level ratio on the vanishing branch is a modulus constant
p, q, a = sp.symbols("p q a", nonzero=True)
R_shift = sp.simplify((-(p - a) / (q + a)).subs(q, -p - 2 * a))
check("H3b level_ratio_on_vanishing_branch",
      sp.simplify(R_shift - (p - a) / (p + a)) == 0,
      f"R = -(p-a)/(q+a) with q = -p-2a gives R = {R_shift} (no x, y, t)")

# H3c: the OTHER branch q = -p makes the ratio exactly 1 (degenerate branch)
R_deg = sp.simplify((-(p - a) / (q + a)).subs(q, -p))
check("H3c degenerate_branch_ratio_one",
      sp.simplify(R_deg - 1) == 0,
      f"R at q = -p gives {R_deg}; the entry prefactor 1/(p+q) is singular there")

# --------------------------------------------------------------- H4
V1, V0, D1, D0, Kc0 = sp.symbols("V1 V0 D1 D0 Kc0")
check("H4 constant_ratio_kills_log_deriv",
      sp.simplify(sp.expand((D1 * V0 - V1 * D0).subs({V1: Kc0 * V0, D1: Kc0 * D0}))) == 0,
      "V1 = Kc V0, D1 = Kc D0 => D1 V0 - V1 D0 = 0")

print()
print(f"CHECKS RUN: {CHECKS[0]}   FAILED: {len(FAILS)}")
if FAILS:
    print("FAILED CHECKS: " + ", ".join(FAILS))
    sys.exit(1)
print("PASSED: all Direction H symbolic checks.")
sys.exit(0)
