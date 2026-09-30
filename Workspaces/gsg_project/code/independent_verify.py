"""
INDEPENDENT cross-check of the reported GSG-style y-lattice for the DLW bilinear
pair (6),(7).  Rewritten from scratch; imports NOTHING from engine.py.

Representation: a quantity is a dict  key -> sympy coefficient, where
    key = (n, m),   n = row multiplicities of the Gram index i,
                    m = column multiplicities of the Gram index k,
because E_ik = exp(xi_i + eta_k) obeys  E_00 E_11 = E_01 E_10, so a product of
atoms depends only on the multiplicities, not on the pairing.  This is the only
representation choice; everything else is a direct transcription of

    tau_n = det[ c_k d_ik + (-(p_i-a)/(q_k+a))^n e^{xi_i+eta_k}/(p_i+q_k) ]
    xi_i = p_i x - p_i^2 t (+ y/(p_i-a)),  eta_k = q_k x + q_k^2 t (+ y/(q_k+a))
    (7): B_a f.g = 0,   (6): D_y B_a f.g - 4 D_x f.g = 0,   f=tau_1, g=tau_0
    lattice multiplier:  (e^{y/P_i}, e^{y/Q_k})  ->  (lambda_i^j, lambda_k^j)
"""
import random
from itertools import permutations
from math import comb
import sympy as sp


# ----------------------------------------------------------------- monomials
def e_add(*ds):
    out = {}
    for d in ds:
        for k, v in d.items():
            v = sp.expand(v)
            if v == 0:
                continue
            if k in out:
                nv = sp.expand(out[k] + v)
                if nv == 0:
                    del out[k]
                else:
                    out[k] = nv
            else:
                out[k] = v
    return out


def e_scale(d, s):
    if s == 0:
        return {}
    out = {}
    for k, v in d.items():
        nv = sp.expand(v * s)
        if nv != 0:
            out[k] = nv
    return out


def e_mul(a, b):
    out = {}
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            k = (tuple(x + y for x, y in zip(k1[0], k2[0])),
                 tuple(x + y for x, y in zip(k1[1], k2[1])))
            nv = sp.expand(v1 * v2)
            if k in out:
                nv = sp.expand(out[k] + nv)
            if nv == 0:
                out.pop(k, None)
            else:
                out[k] = nv
    return out


class M:
    def __init__(self, N, p, q, a, h=None, kind='none', c=None):
        self.N, self.p, self.q, self.a, self.h, self.kind = N, list(p), list(q), a, h, kind
        self.c = list(c) if c is not None else [sp.Integer(1)] * N
        self.P = [self.p[i] - a for i in range(N)]
        self.Q = [self.q[k] + a for k in range(N)]

    def chi(self):
        N, h = self.N, self.h
        if self.kind == 'none':
            return [sp.Integer(1)] * N, [sp.Integer(1)] * N
        d = h / 2
        if self.kind == 'sym':      # staggered / central:  (P+d)/(P-d)
            return ([ (self.P[i] + d) / (self.P[i] - d) for i in range(N)],
                    [ (self.Q[k] + d) / (self.Q[k] - d) for k in range(N)])
        if self.kind == 'exp':      # literal GSG (1 - h/P)^-1
            return ([ self.P[i] / (self.P[i] - h) for i in range(N)],
                    [ self.Q[k] / (self.Q[k] - h) for k in range(N)])
        if self.kind == 'expneg':   # (P+h)/P
            return ([ (self.P[i] + h) / self.P[i] for i in range(N)],
                    [ (self.Q[k] + h) / self.Q[k] for k in range(N)])
        raise ValueError(self.kind)

    def tau(self, n, j=0, aoff=0):
        N = self.N
        aa = self.a + aoff
        Pn = [self.p[i] - aa for i in range(N)]
        Qn = [self.q[k] + aa for k in range(N)]
        r, cc = self.chi()
        zk = ((0,) * N, (0,) * N)
        ent = {}
        for i in range(N):
            for k in range(N):
                coef = (-Pn[i] / Qn[k]) ** n / (self.p[i] + self.q[k])
                if self.h is not None and self.kind != 'none':
                    coef = coef * (r[i] * cc[k]) ** j
                ki = (tuple(1 if x == i else 0 for x in range(N)),
                      tuple(1 if y == k else 0 for y in range(N)))
                e = {ki: sp.expand(coef)}
                if i == k:
                    e = e_add(e, {zk: self.c[k]})
                ent[(i, k)] = e
        tot = {}
        for perm in permutations(range(N)):
            pl = list(perm)
            sgn = 1
            for ii in range(N):
                for jj in range(ii + 1, N):
                    if pl[ii] > pl[jj]:
                        sgn = -sgn
            term = {zk: sp.Integer(sgn)}
            for i in range(N):
                term = e_mul(term, ent[(i, pl[i])])
            tot = e_add(tot, term)
        return tot

    def rate(self, key, var):
        n, m = key
        if var == 'x':
            return sum(n[i] * self.p[i] for i in range(self.N)) + \
                   sum(m[k] * self.q[k] for k in range(self.N))
        if var == 't':
            return sum(-n[i] * self.p[i] ** 2 for i in range(self.N)) + \
                   sum(m[k] * self.q[k] ** 2 for k in range(self.N))
        if var == 'y':
            return sum(n[i] / self.P[i] for i in range(self.N)) + \
                   sum(m[k] / self.Q[k] for k in range(self.N))
        raise ValueError(var)

    def der(self, d, var):
        out = {}
        for k, v in d.items():
            rr = self.rate(k, var)
            if rr != 0:
                out[k] = sp.expand(out.get(k, 0) + v * rr)
        return {k: v for k, v in out.items() if v != 0}

    def dn(self, d, var, k):
        for _ in range(k):
            d = self.der(d, var)
        return d

    def bil(self, F, G, ax=0, ay=0, at=0):
        out = {}
        for pp in range(ax + 1):
            for qq in range(ay + 1):
                for rr in range(at + 1):
                    co = (-1) ** (pp + qq + rr) * comb(ax, pp) * comb(ay, qq) * comb(at, rr)
                    A = self.dn(self.dn(self.dn(F, 'x', ax - pp), 'y', ay - qq), 't', at - rr)
                    B = self.dn(self.dn(self.dn(G, 'x', pp), 'y', qq), 't', rr)
                    out = e_add(out, e_scale(e_mul(A, B), co))
        return out

    def B(self, F, G, s):
        """(D_x^2 + D_t + 2s D_x) F.G"""
        return e_add(self.bil(F, G, ax=2), self.bil(F, G, at=1),
                     e_scale(self.bil(F, G, ax=1), 2 * s))

    def DyB(self, F, G, s):
        return e_add(self.bil(F, G, ax=2, ay=1), self.bil(F, G, at=1, ay=1),
                     e_scale(self.bil(F, G, ax=1, ay=1), 2 * s))

    def Dx(self, F, G):
        return self.bil(F, G, ax=1)


# ----------------------------------------------------------------- helpers
def random_pt(model, seed, lo=2, hi=41):
    rng = random.Random(seed)
    syms = list(model.p) + list(model.q) + [model.a]
    if model.h is not None:
        syms.append(model.h)
    pt, used = {}, set()
    for s in syms:
        for _ in range(200):
            v = sp.Rational(rng.randint(lo, hi), rng.randint(lo, 7))
            if v not in used:
                used.add(v); pt[s] = v; break
    for _ in range(50):
        if all(pt[model.a] != pt[x] for x in model.p) and \
           all(pt[model.a] != -pt[x] for x in model.q):
            break
        pt[model.a] += sp.Rational(1, 7)
    return pt


def vanishes_symbolic(res):
    """True iff every coefficient of the monomial dict is identically zero."""
    for k, v in res.items():
        if sp.simplify(sp.together(v)) != 0:
            return False, (k, sp.factor(sp.together(v)))
    return True, None


def vanishes_at_points(build, N, kind='none', h=None, trials=3, seed0=11):
    for att in range(1, 60):
        m = M(N, [sp.Symbol(f'p{i+1}') for i in range(N)],
                 [sp.Symbol(f'q{k+1}') for k in range(N)], sp.Symbol('a'), h=h, kind=kind)
        pt = random_pt(m, seed=seed0 + 91 * att)
        m = M(N, [pt[sp.Symbol(f'p{i+1}')] for i in range(N)],
                 [pt[sp.Symbol(f'q{k+1}')] for k in range(N)], pt[sp.Symbol('a')],
                 h=(pt[sp.Symbol('h')] if h is not None else None), kind=kind)
        ok, bad = vanishes_symbolic(build(m))
        if not ok:
            return False, (pt, bad)
    return True, None


if __name__ == '__main__':
    hp, hq, ha, hh = (sp.Symbol('p', positive=True), sp.Symbol('q', positive=True),
                      sp.Symbol('a'), sp.Symbol('h', positive=True))
    H = sp.Rational(1, 3)

    print("=" * 88)
    print("A. CONTINUUM baseline:   f=tau_1, g=tau_0")
    print("=" * 88)
    for N in (1, 2):
        m = M(N, [sp.Symbol(f'p{i+1}') for i in range(N)],
              [sp.Symbol(f'q{k+1}') for k in range(N)], ha, kind='none')
        ok7, b7 = vanishes_symbolic(m.B(m.tau(1), m.tau(0), m.a))
        ok6, b6 = vanishes_symbolic(e_add(m.DyB(m.tau(1), m.tau(0), m.a),
                                          e_scale(m.Dx(m.tau(1), m.tau(0)), -4)))
        print(f"   N={N} [ALL-SYMBOLIC]: (7) {'OK' if ok7 else 'FAIL ' + str(b7)}"
              f"   (6)|lam=-2 {'OK' if ok6 else 'FAIL ' + str(b6)}", flush=True)
    for N in (3, 4, 5, 6):
        ok7, _ = vanishes_at_points(lambda m: m.B(m.tau(1), m.tau(0), m.a), N)
        ok6, _ = vanishes_at_points(lambda m: e_add(m.DyB(m.tau(1), m.tau(0), m.a),
                                                    e_scale(m.Dx(m.tau(1), m.tau(0)), -4)), N)
        print(f"   N={N} [exact random rational pts]: (7) {'OK' if ok7 else 'FAIL'}"
              f"   (6)|lam=-2 {'OK' if ok6 else 'FAIL'}", flush=True)

    print()
    print("=" * 88)
    print("D. ELEMENTWISE identity   T_{a+d}(j+1) == T_{a-d}(j),  d=h/2,  n=1")
    print("=" * 88)
    for N in (1, 2, 3):
        m = M(N, [sp.Symbol(f'p{i+1}') for i in range(N)],
              [sp.Symbol(f'q{k+1}') for k in range(N)], ha, h=hh, kind='sym')
        if N == 3:
            pt = random_pt(m, seed=7)
            m = M(N, [pt[sp.Symbol(f'p{i+1}')] for i in range(N)],
                  [pt[sp.Symbol(f'q{k+1}')] for k in range(N)], pt[sp.Symbol('a')],
                  h=pt[sp.Symbol('h')], kind='sym')
        L = m.tau(1, j=1, aoff=+m.h / 2)
        R = m.tau(1, j=0, aoff=-m.h / 2)
        same = (L.keys() == R.keys()) and all(
            sp.simplify(sp.together(L[k] - R[k])) == 0 for k in L)
        print(f"   N={N}: {'IDENTICAL' if same else 'DIFFERENT'}"
              f"   ({'symbolic' if N < 3 else 'exact rational point'})")

    print()
    print("=" * 88)
    print("E. STAGGERED LATTICE pair (the reported answer)")
    print("   (7)_h: B_(a-d) F_j . G_j = 0    F_j=tau_1(j;a-d), G_j=tau_0(j)")
    print("   (6)_h: B_(a+d) F_j . G_(j+1) = 0")
    print("=" * 88)
    for kind in ('sym', 'exp', 'expneg'):
        for N in (1, 2):
            m = M(N, [sp.Symbol(f'p{i+1}') for i in range(N)],
                  [sp.Symbol(f'q{k+1}') for k in range(N)], ha, h=hh, kind=kind)
            okm, bm = vanishes_symbolic(m.B(m.tau(1, 0, -m.h / 2), m.tau(0), m.a - m.h / 2))
            okp, bp = vanishes_symbolic(m.B(m.tau(1, 0, -m.h / 2), m.tau(0, 1), m.a + m.h / 2))
            print(f"   kind={kind:7s} N={N} [ALL-SYMBOLIC]:"
                  f" (7)_h {'OK' if okm else 'FAIL ' + str(bm)}"
                  f"   (6)_h {'OK' if okp else 'FAIL ' + str(bp)}", flush=True)
        for N in (3, 4, 5):
            okm, _ = vanishes_at_points(
                lambda m: m.B(m.tau(1, 0, -m.h / 2), m.tau(0), m.a - m.h / 2),
                N, kind=kind, h=H)
            okp, _ = vanishes_at_points(
                lambda m: m.B(m.tau(1, 0, -m.h / 2), m.tau(0, 1), m.a + m.h / 2),
                N, kind=kind, h=H)
            print(f"   kind={kind:7s} N={N} [exact pts]:"
                  f" (7)_h {'OK' if okm else 'FAIL'}   (6)_h {'OK' if okp else 'FAIL'}", flush=True)

    print()
    print("=" * 88)
    print("F. NAIVE two-point difference for (6)  (N=1, closed form in p,q,a,h)")
    print("   R = (1/h)[ B f_{j+1}.g_j - B f_j.g_{j+1} ] - 4 D_x f_j.g_j,")
    print("   f_j = tau_1(j) at base a (no a-shift),  g_j = tau_0(j)")
    print("=" * 88)
    for kind, chi in (('exp', hp * hq / ((hp - ha - hh) * (hq + ha - hh))),
                      ('sym', ((hp - ha + hh / 2) / (hp - ha - hh / 2)) *
                              ((hq + ha + hh / 2) / (hq + ha - hh / 2)))):
        m = M(1, [hp], [hq], ha, h=hh, kind=kind)
        f0, g0 = m.tau(1, 0), m.tau(0, 0)
        f1, g1 = m.tau(1, 1), m.tau(0, 1)
        R = e_add(e_scale(e_add(m.B(f1, g0, m.a), e_scale(m.B(f0, g1, m.a), -1)), 1 / hh),
                  e_scale(m.Dx(f0, g0), -4))
        # divide by the common monomial factor 4*chi^j*e^{theta}  ->  Delta
        keys = list(R.keys())
        Delta = None
        if len(keys) == 1:
            coef = sp.factor(sp.simplify(R[keys[0]] / (4 * chi)))
            Delta = coef
        print(f"   kind={kind}:  #monomials={len(keys)}")
        if Delta is not None:
            print(f"      R/(4 chi^j) = {Delta}")
            print(f"      limit h->0 : {sp.simplify(sp.limit(Delta, hh, 0, dir='+'))}")
            print(f"      R/(4 chi^j)/h at h=1/3 : {sp.factor(sp.simplify((Delta/hh)))}")

    print()
    print("=" * 88)
    print("G. lattice dispersion:  ln(lambda_i)/h  vs  1/P_i")
    print("=" * 88)
    lam = ((hp - ha + hh / 2) / (hp - ha - hh / 2))
    s = sp.series(sp.log(lam) / hh, hh, 0, 5).removeO()
    print("   (1/h) ln[(P+h/2)/(P-h/2)] =", sp.nsimplify(sp.expand(s)))
    print("   = 1/P + h^2/(12P^3) + h^4/(80P^5) + ...  check:",
          sp.simplify(sp.expand(s) - 1 / (hp - ha) - hh ** 2 / (12 * (hp - ha) ** 3)))
