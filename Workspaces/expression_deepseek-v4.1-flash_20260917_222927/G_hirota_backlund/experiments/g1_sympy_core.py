"""Independent SymPy audit of the staggered y-semidiscrete DLW bilinear candidate.

Direction G (Hirota / Baecklund / hierarchy discretisation).
Written from scratch; it does NOT import or reuse lean-toda/check_dlw_staggered.py.

Conventions (see SHARED_MATH_SPEC.md section 3):
  B_s = D_x^2 + D_t + 2 s D_x,    s = a -+ h/2
  (B_{a-h/2}) F_j . G_j      = 0        G_j     at y = j h
  (B_{a+h/2}) F_j . G_{j+1}  = 0        F_j     at y = (j+1/2) h
  d = h/2, P_i = p_i - a, Q_i = q_i + a
  rho_i = ((P_i+d)(Q_i+d))/((P_i-d)(Q_i-d)),  r_i = -(P_i+d)/(Q_i-d)

Everything is exact (rationals / symbolic).  Run:  python -u g1_sympy_core.py
"""

import sympy as sp

p1, p2, q1, q2 = sp.symbols('p1 p2 q1 q2')
a, h = sp.symbols('a h')
E1, E2 = sp.symbols('E1 E2')
Gam = sp.symbols('Gamma')


def two_soliton_data(av, hv):
    """F/G coefficients of the staggered two-soliton tau pair (Gamma left free)."""
    dv = hv / 2
    P1, P2 = p1 - av, p2 - av
    Q1, Q2 = q1 + av, q2 + av
    r1 = -(P1 + dv) / (Q1 - dv)
    r2 = -(P2 + dv) / (Q2 - dv)
    Gam0 = ((p1 - p2) * (q1 - q2)) / ((p1 + q1) * (p1 + q2) * (p2 + q1) * (p2 + q2))
    G = 1 + E1 / (p1 + q1) + E2 / (p2 + q2) + Gam * E1 * E2
    F = 1 + r1 * E1 / (p1 + q1) + r2 * E2 / (p2 + q2) + Gam * r1 * r2 * E1 * E2
    return G, F, dict(d=dv, r1=r1, r2=r2, Gam0=Gam0)


def wave_pair(E1v=E1, E2v=E2):
    """mode -> (wavenumber k, frequency w) for the exponential part of tau."""
    k1, k2 = p1 + q1, p2 + q2
    w1, w2 = q1 ** 2 - p1 ** 2, q2 ** 2 - p2 ** 2
    out = {}
    for poly, tag in ((E1v, 1), (E2v, 2)):
        pass
    for m1 in range(3):
        for m2 in range(3):
            out[(m1, m2)] = (m1 * k1 + m2 * k2, m1 * w1 + m2 * w2)
    return out


def residuals(av, hv, Gamv=Gam):
    """dict s -> dict (m1,m2) -> coefficient of E1^m1 E2^m2 in B_s F_j . G_j."""
    G, F, dat = two_soliton_data(av, hv)
    F = F.subs(Gam, Gamv)
    G = G.subs(Gam, Gamv)
    k1, k2 = p1 + q1, p2 + q2
    w1, w2 = q1 ** 2 - p1 ** 2, q2 ** 2 - p2 ** 2
    pwF = sp.Poly(sp.expand(F), E1, E2)
    pwG = sp.Poly(sp.expand(G), E1, E2)
    Ft = {(m[0], m[1]): c for m, c in zip(pwF.monoms(), pwF.coeffs())}
    Gt = {(m[0], m[1]): c for m, c in zip(pwG.monoms(), pwG.coeffs())}
    out = {}
    for s_val in (av - hv / 2, av + hv / 2):
        acc = {}
        for (m1, m2), cF in Ft.items():
            for (M1, M2), cG in Gt.items():
                k, w = m1 * k1 + m2 * k2, m1 * w1 + m2 * w2
                kp, wp = M1 * k1 + M2 * k2, M1 * w1 + M2 * w2
                dk, dw = k - kp, w - wp
                key = (m1 + M1, m2 + M2)
                acc[key] = sp.expand(acc.get(key, sp.Integer(0))
                                     + cF * cG * (dk ** 2 + dw + 2 * s_val * dk))
        out[s_val] = acc
    return out


def test_general_two_soliton():
    print('=== T1: general-parameter two-soliton residual for BOTH staggered equations ===')
    ok = True
    for s_val, acc in residuals(a, h).items():
        for key in sorted(acc):
            v = sp.simplify(sp.together(acc[key]))
            if v != 0:
                print(f'  s={s_val} mode {key}: NONZERO {v}')
                ok = False
        print(f'  s = {s_val}: {len(acc)} modes, non-vanishing = '
              f'{sum(1 for v in acc.values() if sp.simplify(v) != 0)}')
    print('  PASS' if ok else '  FAIL')
    return ok


def test_Gamma_forced():
    print('=== T2: the interaction coefficient Gamma is forced (uniqueness) ===')
    ok = True
    for s_val, acc in residuals(a, h).items():
        for key in sorted(acc):
            e = sp.simplify(sp.together(acc[key]))
            if e != 0:
                sols = sp.solve(sp.Eq(sp.factor(sp.together(e)), 0), Gam)
                print(f'  s={s_val} mode {key}: forced condition Gamma in {sols}')
                for sol in sols:
                    diff = sp.simplify(sp.together(sol - two_soliton_data(a, h)[2]['Gam0']))
                    print(f'      candidate - Gamma_0 = {sp.factor(diff)}')
                    ok = ok and (diff == 0)
    print('  PASS (Gamma_0 is forced)' if ok else '  FAIL')
    return ok


def test_physical_nonlinear_two_soliton():
    """Independent check with PHYSICAL parameters and a lattice site j.

    Builds G_j, F_j with rho_i^j, differentiates in x and t symbolically, and
    checks the two staggered bilinear equations by direct differentiation.
    """
    print('=== T3: direct differentiation check at physical rational parameters ===')
    av, hv = sp.Rational(2), sp.Rational(1, 10)
    jv = sp.Integer(3)
    pp = [sp.Rational(7, 3), sp.Rational(13, 6)]
    qq = [sp.Rational(3), sp.Rational(10, 3)]
    dv = hv / 2
    rho = [((pp[i] - av + dv) * (qq[i] + av + dv))
           / ((pp[i] - av - dv) * (qq[i] + av - dv)) for i in range(2)]
    rr = [-(pp[i] - av + dv) / (qq[i] + av - dv) for i in range(2)]
    Gam0 = ((pp[0] - pp[1]) * (qq[0] - qq[1])) / ((pp[0] + qq[0]) * (pp[0] + qq[1])
                                                  * (pp[1] + qq[0]) * (pp[1] + qq[1]))
    Ev = [rho[i] ** jv * sp.exp((pp[i] + qq[i]) * sp.Symbol('x')
                                + (qq[i] ** 2 - pp[i] ** 2) * sp.Symbol('t'))
          for i in range(2)]
    X, T = sp.symbols('x t')
    G = 1 + Ev[0] / (pp[0] + qq[0]) + Ev[1] / (pp[1] + qq[1]) + Gam0 * Ev[0] * Ev[1]
    F = (1 + rr[0] * Ev[0] / (pp[0] + qq[0]) + rr[1] * Ev[1] / (pp[1] + qq[1])
         + Gam0 * rr[0] * rr[1] * Ev[0] * Ev[1])
    # G_{j+1}: multiply each E_i by rho_i
    Ev1 = [Ev[i] * rho[i] for i in range(2)]
    G1 = (1 + Ev1[0] / (pp[0] + qq[0]) + Ev1[1] / (pp[1] + qq[1])
          + Gam0 * Ev1[0] * Ev1[1])

    def hirotaB(s_val, f, g):
        return (sp.diff(f, X, 2) * g - 2 * sp.diff(f, X) * sp.diff(g, X) + f * sp.diff(g, X, 2)
                + sp.diff(f, T) * g - f * sp.diff(g, T)
                + 2 * s_val * (sp.diff(f, X) * g - f * sp.diff(g, X)))

    res_low = sp.simplify(sp.expand(hirotaB(av - dv, F, G)))
    res_high = sp.simplify(sp.expand(hirotaB(av + dv, F, G1)))
    print(f'  (B_(a-d)) F_j.G_j      = {res_low}')
    print(f'  (B_(a+d)) F_j.G_(j+1)  = {res_high}')
    ok = (res_low == 0) and (res_high == 0)
    print('  PASS' if ok else '  FAIL')
    return ok


def test_VT_local_nonlinear():
    """The pointwise nonlinear variable transformation, checked exactly.

    phi = ln(F/G), psi = ln(F G).  Claim:
      (D_x^2 + D_t + 2sD_x) F . G  =  F G [ W + (V + 2s u)_x ],
      u = phi_x,  V = psi_xx,  W = psi_t,
      and, for the swapped pair,
      (D_x^2 + D_t + 2s D_x) G . F  = -F G [ V_t + (W V)_x + W_xxx + 2s V_x ].
    """
    print('=== T4: pointwise bilinear -> nonlinear identity (VT) ===')
    X, T = sp.symbols('x t')
    F = sp.Function('F')(X, T)
    G = sp.Function('G')(X, T)
    s = sp.symbols('s')
    phi = sp.log(F / G)
    psi = sp.log(F * G)
    u = sp.diff(phi, X)
    V = sp.diff(psi, X, 2)
    W = sp.diff(psi, T)
    lhs = (sp.diff(F, X, 2) * G - 2 * sp.diff(F, X) * sp.diff(G, X) + F * sp.diff(G, X, 2)
           + sp.diff(F, T) * G - F * sp.diff(G, T)
           + 2 * s * (sp.diff(F, X) * G - F * sp.diff(G, X)))
    rhs = F * G * (W + sp.diff(V + 2 * s * u, X))
    d1 = sp.simplify(sp.expand(lhs - rhs))
    print(f'  (B_s F.G) - F G [W + (V+2s u)_x] = {d1}')
    lhs2 = (sp.diff(G, X, 2) * F - 2 * sp.diff(G, X) * sp.diff(F, X) + G * sp.diff(F, X, 2)
            + sp.diff(G, T) * F - G * sp.diff(F, T)
            + 2 * s * (sp.diff(G, X) * F - G * sp.diff(F, X)))
    rhs2 = -F * G * (sp.diff(V, T) + sp.diff(W * V, X) + sp.diff(W, X, 3) + 2 * s * sp.diff(V, X))
    d2 = sp.simplify(sp.expand(lhs2 - rhs2))
    print(f'  (B_s G.F) + F G [V_t + (WV)_x + W_xxx + 2s V_x] = {d2}')
    ok = (d1 == 0) and (d2 == 0)
    print('  PASS' if ok else '  FAIL')
    return ok


if __name__ == '__main__':
    res = [test_general_two_soliton(), test_Gamma_forced(),
           test_physical_nonlinear_two_soliton(), test_VT_local_nonlinear()]
    print()
    print('SUMMARY:', 'ALL PASS' if all(res) else 'FAILURES PRESENT')
