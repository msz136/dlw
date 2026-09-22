"""Independent audit #3: clean, from-scratch mode computation for the staggered pair.

Definition used (the ONLY one):
  For a tau function T(j) = sum over subsets S of  C_S prod_{i in S} E_{i,j},
  with E_{i,j} = rho_i^j exp((p_i+q_i) x + (q_i^2-p_i^2) t + th_i),
  the Hirota bilinear form B_s F.G = D_x^2 F.G + D_t F.G + 2 s D_x F.G acts
  mode-by-mode:
     D_x^2 F.G : sum over (monomial a of F, monomial b of G) of (k_a-k_b)^2 * c_a c_b E^{a+b}
     D_t   F.G : ... (w_a-w_b)
     D_x   F.G : ... (k_a-k_b)
  where k_a = sum of (p_i+q_i) over a, w_a = sum over a of (q_i^2-p_i^2).

This is the standard bilinear-operator mode rule and it is what both the paper's
determinant identity and any direct differentiation must reproduce.  Here we
never assume the ansatz is right: we test it.
"""

import sympy as sp
from itertools import combinations

x, t = sp.symbols('x t')


def make_taus(n, av, hv, p, q, gam_override=None):
    """Return coefficient dicts for F and G (mode tuple -> symbol) and mode data."""
    dv = hv / 2
    cv = {}
    for k in range(n + 1):
        for S in combinations(range(n), k):
            c = sp.Integer(1)
            for i in S:
                c *= 1 / (p[i] + q[i])
            for idx, i in enumerate(S):
                for jdx in range(idx + 1, len(S)):
                    j = S[jdx]
                    c *= (p[i] - p[j]) * (q[i] - q[j]) / ((p[i] + q[j]) * (p[j] + q[i]))
            cv[S] = c
    # F coefficients: multiply by prod r_i
    rr = [-(p[i] - av + dv) / (q[i] + av - dv) for i in range(n)]
    Fc, Gc = {}, {}
    for S, c in cv.items():
        if gam_override is not None and len(S) > 1:
            c = gam_override
        Fc[S] = c * sp.prod([rr[i] for i in S]) if S else c
        Gc[S] = c
    return Fc, Gc, rr


def residual(Fc, Gc, n, p, q, av, hv, sv, shift_g=0):
    """Coefficient dict of B_s F_j . G_{j+shift_g} (mode -> exact value)."""
    dv = hv / 2
    rho = [((p[i] - av + dv) * (q[i] + av + dv))
           / ((p[i] - av - dv) * (q[i] + av - dv)) for i in range(n)]
    kw = {}
    for k in range(n + 1):
        for S in combinations(range(n), k):
            kw[S] = (sum(p[i] + q[i] for i in S), sum(q[i] ** 2 - p[i] ** 2 for i in S))
    acc = {}
    for Sa, ca in Fc.items():
        ka, wa = kw[Sa]
        for Sb, cb in Gc.items():
            kb, wb = kw[Sb]
            # lattice multiplier for G_{j+shift}
            mult = sp.prod([rho[i] for i in Sb]) ** shift_g
            # the monomial E^{Sa} . E^{Sb} is the exponential with multiplicity
            # tuple Sa+Sb (multiplicities add), which is an independent
            # exponential function of x, t; so coefficients are compared per
            # multiplicity tuple.
            key = tuple(sorted(list(Sa) + list(Sb)))
            dk, dw = ka - kb, wa - wb
            acc[key] = sp.expand(acc.get(key, sp.Integer(0))
                                 + ca * cb * mult * (dk ** 2 + dw + 2 * sv * dk))
    return acc


def check(n, av, hv, p, q, tag=''):
    dv = hv / 2
    Fc, Gc, rr = make_taus(n, av, hv, p, q)
    print(f'--- N={n} {tag}: a={av} h={hv} ---')
    print(f'    rho = {[sp.nsimplify(((p[i]-av+dv)*(q[i]+av+dv))/((p[i]-av-dv)*(q[i]+av-dv))) for i in range(n)]}')
    print(f'    r   = {[sp.nsimplify(v) for v in rr]}')
    out = {}
    for label, sv, shift in (('eq1  B_(a-d) F_j.G_j     ', av - dv, 0),
                             ('eq2  B_(a+d) F_j.G_(j+1) ', av + dv, 1)):
        acc = residual(Fc, Gc, n, p, q, av, hv, sv, shift)
        bad = {k: v for k, v in acc.items() if v != 0}
        print(f'    {label}: {len(acc)} modes, NONZERO = {len(bad)}')
        for k, v in sorted(bad.items(), key=str):
            print(f'        BAD {k} -> {sp.nsimplify(v)}')
        out[label] = bad
    return out


def main():
    print('### Test 1: N=2, exact rationals, several parameter sets (direct mode algebra)')
    sets = [([sp.Rational(7, 3), sp.Rational(13, 6)], [sp.Rational(3), sp.Rational(10, 3)],
             sp.Rational(2), sp.Rational(1, 10)),
            ([sp.Rational(1), sp.Rational(2)], [sp.Rational(5, 2), sp.Rational(-1, 3)],
             sp.Rational(2), sp.Rational(1, 7)),
            ([sp.Rational(-1, 2), sp.Rational(4, 5)], [sp.Rational(3, 2), sp.Rational(7, 4)],
             sp.Rational(-1, 3), sp.Rational(1, 5))]
    allok = True
    for p, q, av, hv in sets:
        o = check(2, av, hv, p, q)
        allok = allok and all(not v for v in o.values())
    print()
    print('### Test 2: N=1,2,3,4,5 with exact rationals (a=2, h=1/10)')
    av, hv = sp.Rational(2), sp.Rational(1, 10)
    for n in range(1, 6):
        p = [sp.Rational(3 + 2 * i, 2) for i in range(n)]
        q = [sp.Rational(7 + 3 * i, 3) for i in range(n)]
        o = check(n, av, hv, p, q)
        allok = allok and all(not v for v in o.values())
    print()
    print('### Test 3: does the ansatz require the canonical Gamma?  (N=2, gamma free)')
    p = [sp.Rational(7, 3), sp.Rational(13, 6)]
    q = [sp.Rational(3), sp.Rational(10, 3)]
    av, hv = sp.Rational(2), sp.Rational(1, 10)
    Fc, Gc, rr = make_taus(2, av, hv, p, q)
    dv = hv / 2
    print('    canonical interaction coefficient (2x2 minor of 1/(p_i+q_k)):')
    print('      Gamma_0 =', sp.nsimplify(Fc[(0, 1)] / sp.prod([rr[i] for i in (0, 1)])))
    print()
    print('### OVERALL:', 'ALL PASS' if allok else 'FAILURES PRESENT')
    return allok


if __name__ == '__main__':
    main()
