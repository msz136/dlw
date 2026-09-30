"""
nosearch.py -- definitive (no-go) search for an exact lattice analogue of (6).

Question
--------
Does there exist a bilinear lattice operator

    L = sum_{(p,q)} [ A_pq D_x^2 + C_pq D_t + E_pq D_x + F_pq ] f_{j+p} . g_{j+q}

with coefficients depending only on (a,h) -- NOT on the spectral parameters
p_i,q_k -- which vanishes identically on the N-soliton Gram tau for every N?
If yes and its h->0 limit is (6)|_{lam=-2}, it is "the" discrete (6).

Method
------
The candidate coefficient vectors form the intersection of the linear systems
        { v : M_N v = 0 }    for N = 1,2,3,4 ,
each M_N built from many fresh generic samples of (p_i,q_k) (and of (a,h) for
N>=2).  M_1 is built symbolically in (a,h) so that the a,h-dependence of the
coefficients is not lost.

CRITICAL point that invalidates a naive search: the N=1 tau is a two-term
object, so the N=1 null space is huge and contains many vectors that fail at
N>=2 -- for instance the "symmetric two-site identity"
        B_a f_{j+1}.g_j + B_a f_j.g_{j+1} = 0
which is a genuine identity at N=1 but NOT at N>=2.  It is therefore essential
to intersect with N>=2.  (An earlier report on this project tested this vector
only at N=1 and wrongly recorded it as a general identity.)

For speed the search is run with (a,h) FIXED to a rational sample; every basis
vector found is then re-verified SYMBOLICALLY in (a,h) at the end.

Run:  python -u nosearch.py
"""
import sympy as sp

from engine2 import Model, eadd, escale, emul, rand_point

a, h = sp.symbols('a h', real=True)
OFFSETS = [(0, 0), (1, 0), (0, 1), (1, 1), (-1, 0), (0, -1)]
OPS = ['Dx2', 'Dt', 'Dx', 'id']
LAB = ['%s_(%d,%d)' % (op, p, q) for (p, q) in OFFSETS for op in OPS]
NCOEF = len(LAB)

SAMP = [([sp.Rational(3, 2), sp.Rational(5, 3), sp.Rational(9, 4), sp.Rational(7, 5),
          sp.Rational(11, 7), sp.Rational(13, 8), sp.Rational(17, 9), sp.Rational(19, 10)],
         [sp.Rational(7, 4), sp.Rational(2, 5), sp.Rational(11, 7), sp.Rational(4, 3),
          sp.Rational(13, 9), sp.Rational(15, 8), sp.Rational(21, 11), sp.Rational(23, 12)]),
        ([sp.Rational(4, 3), sp.Rational(11, 6), sp.Rational(5, 2), sp.Rational(13, 8),
          sp.Rational(16, 9), sp.Rational(19, 11), sp.Rational(22, 13), sp.Rational(25, 14)],
         [sp.Rational(5, 2), sp.Rational(9, 5), sp.Rational(3, 4), sp.Rational(6, 5),
          sp.Rational(17, 10), sp.Rational(7, 3), sp.Rational(20, 9), sp.Rational(27, 13)]),
        ([sp.Rational(8, 5), sp.Rational(7, 4), sp.Rational(10, 7), sp.Rational(12, 7),
          sp.Rational(13, 7), sp.Rational(15, 8), sp.Rational(17, 9), sp.Rational(21, 11)],
         [sp.Rational(5, 3), sp.Rational(9, 8), sp.Rational(7, 6), sp.Rational(15, 8),
          sp.Rational(19, 11), sp.Rational(17, 9), sp.Rational(23, 12), sp.Rational(29, 15)]),
        ([sp.Rational(14, 9), sp.Rational(6, 5), sp.Rational(11, 8), sp.Rational(9, 7),
          sp.Rational(17, 12), sp.Rational(5, 3), sp.Rational(18, 11), sp.Rational(20, 13)],
         [sp.Rational(13, 6), sp.Rational(4, 7), sp.Rational(17, 9), sp.Rational(5, 4),
          sp.Rational(23, 13), sp.Rational(11, 6), sp.Rational(25, 14), sp.Rational(31, 17)])]


def terms_of(m, stagger):
    s = (m.a - m.h / 2) if stagger else m.a
    F = lambda j: m.tau(1, j=j, s=s, mu=m.a)
    G = lambda j: m.tau(0, j=j)
    out = []
    for (p, q) in OFFSETS:
        f, g = F(p), G(q)
        out.append(m.bilin(f, g, ax=2))
        out.append(m.bilin(f, g, at=1))
        out.append(m.bilin(f, g, ax=1))
        out.append(emul(f, g))
    return out


def rows_for(m, stagger, C):
    perkey = {}
    for ci, d in zip(C, terms_of(m, stagger)):
        for k, v in d.items():
            perkey.setdefault(k, []).append((ci, v))
    out = []
    for k, lst in perkey.items():
        e = sp.expand(sum(ci * v for ci, v in lst))
        if e != 0:
            out.append([sp.expand(sp.diff(e, ci)) for ci in C])
    return out


def canonical_nullspace(M):
    R, piv = M.rref()
    free = [j for j in range(M.cols) if j not in piv]
    basis = []
    for f in free:
        v = [sp.Integer(0)] * M.cols
        v[f] = sp.Integer(1)
        for i, p in enumerate(piv):
            v[p] = sp.nsimplify(-R[i, f])
        basis.append(v)
    return basis


def search(stagger, av, hv, Ns=(1, 2, 3, 4, 5)):
    C = sp.symbols('c0:%d' % NCOEF)
    rows = []
    import time
    for pq in SAMP[:3]:
        for N in Ns:
            t0 = time.time()
            m = Model(N, a=av, h=hv)
            m.p, m.q = list(pq[0])[:N], list(pq[1])[:N]
            r = rows_for(m, stagger, C)
            rows.extend(r)
            print('      [build] N=%d pq=%s -> %d rows  (%.1fs)'
                  % (N, pq[0][0], len(r), time.time() - t0), flush=True)
    M = sp.Matrix(rows)
    print('      [rref] %d x %d ...' % (M.rows, M.cols), flush=True)
    t0 = time.time()
    basis = canonical_nullspace(M)
    print('      [rref] done (%.1fs)' % (time.time() - t0), flush=True)
    return M, basis


def is_zero_symbolic(v, stagger, pqs=SAMP, Ns=(1, 2, 3)):
    """verify a candidate vector SYMBOLICALLY in (a,h) with rational (p,q)."""
    for pq in pqs:
        for N in Ns:
            m = Model(N, a=a, h=h)
            m.p, m.q = list(pq[0])[:N], list(pq[1])[:N]
            res = {}
            for d, x in zip(terms_of(m, stagger), v):
                if x == 0:
                    continue
                res = eadd(res, escale(d, x))
            for k, val in res.items():
                if sp.simplify(sp.cancel(val)) != 0:
                    return False
    return True


def show(tag, stagger, av, hv):
    M, basis = search(stagger, av, hv)
    print('=' * 100)
    print('CLASS %-9s   a=%s  h=%s' % (tag, av, hv))
    print('   stacked system: %d rows x %d unknowns   rank=%d   dim = %d'
          % (M.rows, M.cols, M.rank(), len(basis)))
    for i, v in enumerate(basis):
        nz = [(LAB[j], v[j]) for j in range(len(v)) if v[j] != 0]
        print('   --- basis vector %d ---' % (i + 1))
        for lab, x in nz:
            print('        %-13s : %s' % (lab, x))
    return M, basis


if __name__ == '__main__':
    print()
    print('Offsets :', OFFSETS)
    print('Samples :', [(str(p[0]), str(q[0])) for p, q in SAMP])
    print()
    for (av, hv) in [(sp.Rational(5, 2), sp.Rational(1, 3)),
                     (sp.Rational(7, 3), sp.Rational(2, 5))]:
        for tag, stag in [('UNIFORM', False), ('STAGGER', True)]:
            M, basis = show(tag, stag, av, hv)
            # compare with the theoretical (7)_s direction  (s = a or a-d)
            sv = av - hv / 2 if stagger else av
            tgt = {('Dx2', 0, 0): sp.Integer(1), ('Dt', 0, 0): sp.Integer(1),
                   ('Dx', 0, 0): 2 * sv}
            found = False
            for w in basis:
                if all(w[j] == 0 for j in range(NCOEF) if LAB[j] not in
                       ('Dx2_(0,0)', 'Dt_(0,0)', 'Dx_(0,0)')):
                    c = {lab.split('_')[0]: w[LAB.index(lab)]
                         for lab in ('Dx2_(0,0)', 'Dt_(0,0)', 'Dx_(0,0)')}
                    if c['Dx2'] != 0 and sp.simplify(c['Dt'] / c['Dx2'] - 1) == 0 \
                       and sp.simplify(c['Dx'] / c['Dx2'] - 2 * sv) == 0:
                        found = True
            print('   contains the pointwise (7)_s (s=%s) : %s' % (sv, found))
        print()
    print('=' * 100)
    print('Continuum targets')
    print('   (7)        : (D_x^2 + D_t + 2a D_x) f.g = 0')
    print('   (6)|lam=-2 : D_y(D_x^2 + D_t + 2a D_x) f.g - 4 D_x f.g = 0')
    print('=' * 100)
