"""Independent audit #2: is the staggered pair non-degenerate?

B_s = D_x^2 + D_t + 2 s D_x,  d = h/2,  P_i = p_i - a,  Q_i = q_i + a.

Construction under audit (lean-toda/dlw_staggered_construction.md sec.3-5):
    rho_i = ((P_i+d)(Q_i+d))/((P_i-d)(Q_i-d)),   r_i = -(P_i+d)/(Q_i-d)
    G_j = 1 + E1/(p1+q1) + E2/(p2+q2) + Gam E1 E2
    F_j = 1 + r1 E1/(p1+q1) + r2 E2/(p2+q2) + Gam r1 r2 E1 E2
with E_i = rho_i^j * exp((p_i+q_i)x + (q_i^2-p_i^2)t).

Question 1: do both (B_{a-d})F_j.G_j = 0 and (B_{a+d})F_j.G_{j+1} = 0 hold?
Question 2: are F_j and G_j really j-dependent?  (degeneracy test)

Everything below is computed by direct partial differentiation of an explicit
rational-parameter expression - no mode bookkeeping, no reused prior code.
"""

import sympy as sp

x, t = sp.symbols('x t')


def build(av, hv, jv, pp, qq, gam=None):
    """Return F_j, G_j, G_{j+1} as explicit expressions in x, t."""
    dv = hv / 2
    rho = [((pp[i] - av + dv) * (qq[i] + av + dv))
           / ((pp[i] - av - dv) * (qq[i] + av - dv)) for i in range(2)]
    rr = [-(pp[i] - av + dv) / (qq[i] + av - dv) for i in range(2)]
    if gam is None:
        gam = ((pp[0] - pp[1]) * (qq[0] - qq[1])) / (
            (pp[0] + qq[0]) * (pp[0] + qq[1]) * (pp[1] + qq[0]) * (pp[1] + qq[1]))
    Ev = [rho[i] ** jv * sp.exp((pp[i] + qq[i]) * x + (qq[i] ** 2 - pp[i] ** 2) * t)
          for i in range(2)]
    G = 1 + Ev[0] / (pp[0] + qq[0]) + Ev[1] / (pp[1] + qq[1]) + gam * Ev[0] * Ev[1]
    F = (1 + rr[0] * Ev[0] / (pp[0] + qq[0]) + rr[1] * Ev[1] / (pp[1] + qq[1])
         + gam * rr[0] * rr[1] * Ev[0] * Ev[1])
    Ev1 = [Ev[i] * rho[i] for i in range(2)]
    G1 = (1 + Ev1[0] / (pp[0] + qq[0]) + Ev1[1] / (pp[1] + qq[1])
          + gam * Ev1[0] * Ev1[1])
    return F, G, G1, dict(rho=rho, rr=rr, gam=gam)


def hirotaB(sv, f, g):
    return (sp.diff(f, x, 2) * g - 2 * sp.diff(f, x) * sp.diff(g, x) + f * sp.diff(g, x, 2)
            + sp.diff(f, t) * g - f * sp.diff(g, t)
            + 2 * sv * (sp.diff(f, x) * g - f * sp.diff(g, x)))


def main():
    av, hv = sp.Rational(2), sp.Rational(1, 10)
    dv = hv / 2
    pp = [sp.Rational(7, 3), sp.Rational(13, 6)]
    qq = [sp.Rational(3), sp.Rational(10, 3)]
    print('parameters: a=%s h=%s p=%s q=%s' % (av, hv, pp, qq))
    print()
    print('--- Q1: do the two claimed equations hold? ---')
    for jv in [sp.Integer(0), sp.Integer(3)]:
        F, G, G1, dat = build(av, hv, jv, pp, qq)
        r_lo = sp.simplify(hirotaB(av - dv, F, G))
        r_hi = sp.simplify(hirotaB(av + dv, F, G1))
        print(f'  j={jv}:  (B_(a-d))F_j.G_j = {r_lo}   (B_(a+d))F_j.G_(j+1) = {r_hi}')
    print()
    print('--- Q2: degeneracy: is F_j / G_j actually j-dependent? ---')
    F0, G0, G10, dat = build(av, hv, sp.Integer(0), pp, qq)
    F1, G1, G11, _ = build(av, hv, sp.Integer(1), pp, qq)
    F2, G2, G12, _ = build(av, hv, sp.Integer(2), pp, qq)
    print('  F_1 - F_0 =', sp.simplify(F1 - F0))
    print('  F_2 - F_0 =', sp.simplify(F2 - F0))
    print('  G_1 - G_0 =', sp.simplify(G1 - G0))
    print('  G_2 - G_0 =', sp.simplify(G2 - G0))
    print()
    print('--- Q3: equivalently, is the matrix entry shift identity exact? ---')
    print('  rho_i*r_i  vs  r_i with s -> s+2d :')
    rho, rr = dat['rho'], dat['rr']
    for i in range(2):
        lhs = sp.simplify(rho[i] * rr[i])
        rhs = sp.simplify(-(pp[i] - av - dv) / (qq[i] + av + dv))
        print(f'    i={i}: rho_i r_i = {lhs}   -(P_i-d)/(Q_i+d) = {rhs}   equal: {sp.simplify(lhs-rhs)==0}')
    print()
    print('--- Q4: does the mean/difference pair carry independent information? ---')
    F, G, G1, _ = build(av, hv, sp.Integer(1), pp, qq)
    Ulo = hirotaB(av - dv, F, G)
    Uhi = hirotaB(av + dv, F, G1)
    print('  Ulo =', sp.simplify(Ulo), ' Uhi =', sp.simplify(Uhi))
    print('  (Uhi+Ulo)/2 =', sp.simplify((Uhi + Ulo) / 2), '  (Uhi-Ulo)/h =', sp.simplify((Uhi - Ulo) / hv))
    print()
    print('--- Q5: continuum check: F_j, G_j as functions of y=(j+1/2)h ---')
    # sample j = 0..4 and check F_j equals F_0 identically (for fixed x,t)
    subs = {x: sp.Rational(1, 5), t: sp.Rational(-1, 7)}
    vals = []
    for jv in range(5):
        Fj, Gj, _, _ = build(av, hv, sp.Integer(jv), pp, qq)
        vals.append((jv, sp.nsimplify(Fj.subs(subs)), sp.nsimplify(Gj.subs(subs))))
    for v in vals:
        print('   j=%d  F_j=%.12f  G_j=%.12f' % (v[0], float(v[1]), float(v[2])))


if __name__ == '__main__':
    main()
