"""
certify.py -- independent certification battery for the semi-discretisation of
the DLW bilinear pair (6),(7) by the Feng-Sheng-Yu (generalised sine-Gordon)
method.

Run:  python -u certify.py
"""
import sympy as sp

from engine2 import Model, eadd, escale, emul, vanishes, rand_point

a, h, x, y, t = sp.symbols('a h x y t', real=True)
H = sp.Rational(1, 3)
OK = 'OK  '
BAD = 'FAIL'


def head(s):
    print()
    print('=' * 92)
    print(s)
    print('=' * 92)


def single(d):
    """the single coefficient of a one-monomial dict, or 0 for the empty dict."""
    if len(d) == 0:
        return sp.Integer(0)
    assert len(d) == 1, 'expected at most one monomial, got %d' % len(d)
    return list(d.values())[0]


# ---------------------------------------------------------------------------
head('A. continuum baseline:  (7) B_a f.g = 0  and  (6)|lam=-2  D_y B_a f.g = 4 D_x f.g')
for N in (1, 2, 3, 4, 5):
    ok7, _ = vanishes(lambda m: m.B(m.tau(1), m.tau(0)), N, trials=2)
    ok6, _ = vanishes(lambda m: eadd(m.bilin(m.tau(1), m.tau(0), ax=2, ay=1),
                                     m.bilin(m.tau(1), m.tau(0), at=1, ay=1),
                                     escale(m.bilin(m.tau(1), m.tau(0), ax=1, ay=1), 2 * m.a),
                                     escale(m.bilin(m.tau(1), m.tau(0), ax=1), -4)),
                      N, trials=2)
    print('   N=%d   (7) %s    (6)@lam=-2 %s' % (N, OK if ok7 else BAD, OK if ok6 else BAD))

# ---------------------------------------------------------------------------
head('B. (7) is exact at EVERY y-lattice site   lam(z) = (z+h/2)/(z-h/2)')
for N in (1, 2, 3, 4):
    res = []
    for j in (0, 1, 2, 3):
        ok7, _ = vanishes(lambda m, j=j: m.B(m.tau(1, j=j), m.tau(0, j=j)), N, trials=2, h=H)
        ok6, _ = vanishes(lambda m, j=j: m.B(m.tau(1, j=j, s=m.a - m.h / 2, mu=m.a),
                                             m.tau(0, j=j), s=m.a - m.h / 2), N, trials=2, h=H)
        res.append('%d:%s%s' % (j, '7=' + ('OK ' if ok7 else 'FAIL'), 'F=' + ('OK' if ok6 else 'FAIL')))
    print('   N=%d   site ' % N + '  '.join(res))

# ---------------------------------------------------------------------------
head('C. exact N=1 cross-site formula   B_a tau_1(p) . tau_0(q) = 2 c P E (chi^q - chi^p)')
m = Model(1, h=h)
m.subs_point(rand_point(m, seed=7))
p1, q1 = m.p[0], m.q[0]
P = p1 - m.a
Q = q1 + m.a
chi = m.lam(P) * m.lam(Q)
for (pp, qq) in [(0, 0), (1, 0), (0, 1), (1, 1), (2, 1), (3, 0)]:
    got = sp.simplify(single(m.B(m.tau(1, j=pp), m.tau(0, j=qq))))
    want = sp.simplify(2 * m.c[0] * P * (chi ** qq - chi ** pp))
    print('   (p,q)=(%d,%d)  B=%s   formula=%s   %s'
          % (pp, qq, sp.factor(got), sp.factor(want),
             OK if sp.simplify(got - want) == 0 else BAD))
print('   => B_a f_p.g_q is antisymmetric in (p,q) and vanishes iff p = q;')
print('      (7) is a purely POINTWISE identity, it carries no lattice information.')

# ---------------------------------------------------------------------------
head('D. naive lattice (6):   (1/h)[B f_{j+1}.g_j - B f_j.g_{j+1}] - 4 D_x f_j.g_j   != 0')
Dxfg = sp.simplify(single(m.bilin(m.tau(1), m.tau(0), ax=1)))
naive = sp.simplify(sp.expand(2 * P * (1 - chi) / m.h - 4 * Dxfg))
print('   D_x f_j.g_j                        =', sp.factor(Dxfg))
print('   (1/h)(Bf_{j+1}.g_j - Bf_j.g_{j+1}) =', sp.factor(sp.expand(2 * P * (1 - chi) / m.h)))
print('   residual                           =', sp.factor(naive))
print('   residual / h                       =', sp.factor(sp.simplify(naive / m.h)), ' (finite, nonzero at h=0)')
print('   => the naive two-site scheme is only FIRST order and never exact for h>0.')
for N in (1, 2, 3):
    def naive_op(mm):
        f, g = mm.tau(1), mm.tau(0)
        f1, g1 = mm.tau(1, j=1), mm.tau(0, j=1)
        return eadd(escale(eadd(mm.B(f1, g), escale(mm.B(f, g1), -1)), 1 / mm.h),
                    escale(mm.bilin(f, g, ax=1), -4))
    okz, _ = vanishes(naive_op, N, trials=2, h=H)
    print('   N=%d  naive residual identically zero? %s' % (N, 'YES' if okz else 'NO (as expected)'))

# ---------------------------------------------------------------------------
head('E. structural identity   tau_1(j=1 ; coeff param a+d) = tau_1(j=0 ; coeff param a-d)')
for N in (1, 2, 3, 4):
    mm = Model(N, h=h)
    mm.subs_point(rand_point(mm, seed=21 + N))
    d = mm.h / 2                       # NOTE: must use the SUBSTITUTED h
    lhs = mm.tau(1, j=1, s=mm.a + d, mu=mm.a)
    rhs = mm.tau(1, j=0, s=mm.a - d, mu=mm.a)
    same = lhs.keys() == rhs.keys() and all(sp.simplify(lhs[k] - rhs[k]) == 0 for k in lhs)
    print('   N=%d   %s' % (N, OK if same else BAD))
print('   (equivalently:  -((P-d)/(Q+d)) * chi_ik  =  -((P+d)/(Q-d)) , chi_ik = lam(P)lam(Q))')

# ---------------------------------------------------------------------------
head('F. staggered lattice pair   d = h/2,   F_j = tau_1(j ; coeff param a-d),  G_j = tau_0(j)\n'
     '     (7)_h :  B_(a-d) F_j . G_j     = 0\n'
     '     (6)_h :  B_(a+d) F_j . G_(j+1) = 0')
for N in (1, 2, 3, 4, 5):
    row = []
    for j in (0, 1, 2, 3):
        def p7(mm, j=j):
            return mm.B(mm.tau(1, j=j, s=mm.a - mm.h / 2, mu=mm.a), mm.tau(0, j=j),
                        s=mm.a - mm.h / 2)

        def p6(mm, j=j):
            return mm.B(mm.tau(1, j=j, s=mm.a - mm.h / 2, mu=mm.a), mm.tau(0, j=j + 1),
                        s=mm.a + mm.h / 2)
        ok7, _ = vanishes(p7, N, trials=2, h=H, seed0=31 + j + 7 * N)
        ok6, _ = vanishes(p6, N, trials=2, h=H, seed0=71 + j + 7 * N)
        row.append('%d:(%s,%s)' % (j, 'OK' if ok7 else 'FL', 'OK' if ok6 else 'FL'))
    print('   N=%d   site ' % N + '  '.join(row))

# ---------------------------------------------------------------------------
head('G. equivalent two-point form   (1/h) B_(a-d) F_j . (G_{j+1} - G_j) + 2 D_x F_j . G_{j+1} = 0')
for N in (1, 2, 3, 4):
    row = []
    for j in (0, 1, 2):
        def tp(mm, j=j):
            F = mm.tau(1, j=j, s=mm.a - mm.h / 2, mu=mm.a)
            G = mm.tau(0, j=j)
            Gp = mm.tau(0, j=j + 1)
            return eadd(escale(mm.B(F, eadd(Gp, escale(G, -1)), s=mm.a - mm.h / 2), 1 / mm.h),
                        escale(mm.bilin(F, Gp, ax=1), 2))
        ok, _ = vanishes(tp, N, trials=2, h=H, seed0=53 + j + 5 * N)
        row.append('%d:%s' % (j, 'OK' if ok else 'FAIL'))
    print('   N=%d   site ' % N + '  '.join(row))

# ---------------------------------------------------------------------------
head('H. probes for extra structure')
N = 2


def probe(name, fn, hh=None):
    ok, _ = vanishes(fn, N, trials=2, h=hh)
    print('   N=2  %-58s %s' % (name, 'HOLDS' if ok else 'no'))


probe('2DTL:  (1/2 D_y D_x - 1) t_n.t_n + t_{n+1} t_{n-1} = 0',
      lambda m: eadd(escale(m.bilin(m.tau(0), m.tau(0), ax=1, ay=1), sp.Rational(1, 2)),
                     escale(emul(m.tau(0), m.tau(0)), -1),
                     emul(m.tau(1), m.tau(-1))))
probe('symmetric 2-site:  B_a f_{j+1}.g_j + B_a f_j.g_{j+1} = 0  [lattice]',
      lambda m: eadd(m.B(m.tau(1, j=1), m.tau(0)), m.B(m.tau(1), m.tau(0, j=1))), hh=H)
probe('symmetric 2-site:  B_a f_{j+1}.g_j + B_a f_j.g_{j+1} = 2 B_a f.g ?  [continuum]',
      lambda m: eadd(m.B(m.tau(1, j=1), m.tau(0)), m.B(m.tau(1), m.tau(0, j=1)),
                     escale(m.B(m.tau(1), m.tau(0)), -2)))

# ---------------------------------------------------------------------------
head('I. UNIQUENESS of the staggered pair  (see nosearch.py, nosearch_uniform.py,\n'
     '   h_scaling.py, uni_identity.py, stag_h.py)')
print('   Search space: all 24 bilinear combinations')
print('        {D_x^2, D_t, D_x, id}  x  {(0,0),(1,0),(0,1),(1,1),(-1,0),(0,-1)}')
print('   with coefficients in Q(a,h) (no dependence on the spectral parameters),')
print('   intersected over N = 1,2,3,4,5 and several generic (p,q) samples.')
print()
print('   CAVEAT (found in this work): the intersection matrix is assembled at a FIXED')
print('   (a,h), so its null space may contain vectors that vanish only at that h.')
print()
print('   STAGGERED class  (f = tau_1 with coefficient parameter a-d, d = h/2):')
print('        dim = 4 for EVERY tested h in {1/2, 3/7, 1/3, 1/5, 1/10}, and the span is')
print('        always exactly')
print('             (7)_h at site j ,  (7)_h at site j+1 ,')
print('             (6)_h at (j,j+1) , (6)_h at (j-1,j)')
print('        i.e. by the two equations of the system taken at neighbouring sites.')
print('        => the staggered pair is the UNIQUE exact lattice system in this stencil,')
print('           robustly in h.   [stag_h.py]')
print()
print('   UNIFORM class    (f = tau_1 with coefficient parameter a):')
print('        dim = 4 at the fixed value h = 1/3 (up to N = 7, 8748 rows), with two extra')
print('        cross-site vectors whose coefficients diverge like h^-2.  Their structure is')
print('             X = B_{a-h}F_{j+1}.G_j - B_{a+h}F_j.G_{j+1} + h^2(F_{j+1}G_j-F_jG_{j+1})')
print('        and X IS NOT AN IDENTITY: it vanishes for h = 1/3 and 1/4 but NOT for')
print('        h = 1/2 (N = 3,4)   [uni_identity.py].  So the extra vectors are artifacts')
print('        of fixing h.')
print('        Structurally: as h -> 0 every site collapses to one point, so the leading')
print('        operator of ANY uniform-class identity is a SINGLE-POINT operator')
print('        annihilating the continuum tau, hence proportional to B_a -- i.e. its h^0')
print('        content can only be (7), never (6).  And the leading term of X is indeed')
print('             X = h D_y B_a f.g - 4h D_x f.g + O(h^2) = O(h^2)   using (6).')
print('        => a "lattice (6)" with an unshifted B-parameter does NOT exist.')

# ---------------------------------------------------------------------------
head('J. COUNTEREXAMPLE to the old claim (5.2a) of OUT_GSG_DLW_report.md:\n'
     '   "the lattice one-soliton profile equals the continuum profile with a -> a - h/2"')
Es, ps, qs, asy = sp.symbols('E p q a', positive=True)
hs = sp.Symbol('h', positive=True)
ds = hs / 2
Ss = ps + qs
Ps = ps - asy
Qs = qs + asy
lams = ((Ps + ds) / (Ps - ds)) * ((Qs + ds) / (Qs - ds))
u_lat = -2 * Ss ** 3 * (Es * lams) / ((Ss + Es * lams) * (Qs * Ss - Ps * Es * lams))
a2 = asy - hs / 2
P2, Q2 = ps - a2, qs + a2
u_con = -2 * Ss ** 3 * Es / ((Ss + Es) * (Q2 * Ss - P2 * Es))
num = sp.factor(sp.numer(sp.cancel(sp.together(u_lat - u_con))))
sub = {ps: sp.Rational(5, 3), qs: sp.Rational(7, 4), asy: sp.Rational(3, 2),
       hs: sp.Rational(1, 4), Es: sp.Integer(2)}
val = complex((u_lat - u_con).subs(sub))
print('   symbolic numerator of  u_lat - u_con(a-h/2)  has an overall factor  E*h : %s'
      % ('yes' if sp.simplify(num / (Es * hs)).is_polynomial(ps, qs, asy, hs) else '?'))
print('   at (p,q,a,h,E) = (5/3, 7/4, 3/2, 1/4, 2):  u_lat - u_con = %s' % sp.nsimplify(val.real))
print('   => the claim is FALSE.  The correct statement is the RATE renormalisation')
print('        exp(y(1/P + 1/Q))  ->  lambda^j ,   i.e.  1/P -> Lambda_h(P) = ln(lam(P))/h ,')
print('      which reproduces the lattice profile EXACTLY (see REPORT.md section 8.3).')

print()
print('=' * 92)
print('certify.py finished.')
print('=' * 92)
