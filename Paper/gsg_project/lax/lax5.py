"""
lax5.py -- the decisive experiment.

Define the spectral tau
      TH_n(z) := tau_n with the rank-one spectral deformation
                  M_ik -> M_ik + z^{-1} u_i v_k
and the wave function
      psi_n(z) := TH_n(z) / tau_n .

Then test, EXACTLY, for a *spectral* (z-carrying) linear problem
      sum_k [ A_n^{(k)} psi_{n+1}(z) + B_n^{(k)} psi_n(z) + C_n^{(k)} psi_{n-1}(z) ] z^k = 0
with z-independent coefficients A,B,C built from tau and its x-derivatives.

Practically: evaluate psi_n at 1/z = 0,1,2,... and look for an exact linear
relation
      (c0 + c1/z + ... ) psi_{n+1} + (d0 + d1/z + ...) psi_n
       + (e0 + e1/z + ...) psi_{n-1} = 0 ,
i.e. a relation whose coefficients are polynomials in 1/z.  Solving an
overdetermined linear system in the unknown coefficients then either produces
a relation (integrability) or proves none exists in this class.
"""
import sys
import itertools

import sympy as sp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')

x, y, t = sp.symbols('x y t', real=True)
z = sp.Symbol('z')

A_VAL = sp.Rational(3, 2)
H_VAL = sp.Rational(1, 3)
P0 = {x: sp.Rational(1, 3), y: sp.Rational(-2, 5), t: sp.Rational(3, 7)}


class Tau:
    def __init__(self, N, a, h, p, q, c=None):
        self.N = int(N)
        self.a, self.h = sp.nsimplify(a), sp.nsimplify(h)
        self.p = [sp.nsimplify(v) for v in p]
        self.q = [sp.nsimplify(v) for v in q]
        self.c = [sp.Integer(1)] * self.N if c is None else [sp.nsimplify(v) for v in c]
        self.P = [self.p[i] - self.a for i in range(self.N)]
        self.Q = [self.q[k] + self.a for k in range(self.N)]

    def lam(self, v):
        return (v + self.h / 2) / (v - self.h / 2)

    def chi(self, i, k):
        return self.lam(self.P[i]) * self.lam(self.Q[k])

    def entry(self, n, j, i, k):
        p, q = self.p[i], self.q[k]
        P, Q = p - self.a, q + self.a
        coef = (-P / Q) ** n / (p + q)
        if j:
            coef *= self.chi(i, k) ** j
        xi = p * x - p ** 2 * t + y / P
        eta = q * x + q ** 2 * t + y / Q
        return coef * sp.exp(xi + eta)

    def M(self, n, j=0):
        return sp.Matrix(self.N, self.N, lambda i, k: self.entry(n, j, i, k))

    def tau(self, n, j=0):
        return sp.expand(self.M(n, j).det())


def ev(ex, extra=None):
    s = dict(P0)
    if extra:
        s.update(extra)
    v = complex(sp.sympify(ex).subs(s))
    assert abs(v.imag) < 1e-20, (ex, v)
    return v.real


class Lab:
    """exact rational values of tau, its derivatives, and psi_n(z)."""

    def __init__(self, N, p, q, j=0):
        self.T = Tau(N, A_VAL, H_VAL, p, q)
        self.N = N
        self.j = j

    # ---- tau with a rank-one spectral deformation in the (0,0) direction
    def tauhat(self, n, zinv):
        T = self.T
        N = self.N
        M = T.M(n, self.j)
        # fixed perturbation:  u_i = p_i, v_k = q_k
        u = [T.p[i] for i in range(N)]
        v = [T.q[k] for k in range(N)]
        if zinv != 0:
            for i in range(N):
                for k in range(N):
                    M[i, k] = M[i, k] + zinv * u[i] * v[k]
        return sp.expand(M.det())

    def psi(self, n, zinv):
        return ev(self.tauhat(n, zinv)) / ev(self.T.tau(n, self.j))

    def psid(self, n, zinv, var, order=1):
        """d^order/dvar^order of psi_n(z)."""
        T = self.T
        N = self.N
        M = T.M(n, self.j)
        u = [T.p[i] for i in range(N)]
        v = [T.q[k] for k in range(N)]
        # derivative of the determinant w.r.t. the continuous variable = same
        # determinant with each row differentiated (only off-diagonal entries dep.)
        raise NotImplementedError


# ---------------------------------------------------------------- experiment
def find_relation(N, p, q, n, zvals, deg=2, j=0):
    """Solve for coefficients a_m,b_m,c_m (m=0..deg) such that
       sum_m z^{-m} (a_m psi_{n+1} + b_m psi_n + c_m psi_{n-1}) = 0 .
       Gauge fix a_0 = 1 if possible."""
    L = Lab(N, p, q, j)
    rows = []
    for zi in zvals:
        row = []
        for m in range(deg + 1):
            row.append(zi ** (-m))          # coefficient of psi_{n+1}
        for m in range(deg + 1):
            row.append(zi ** (-m) * L.psi(n, zi))
        for m in range(deg + 1):
            row.append(zi ** (-m) * L.psi(n - 1, zi))
        rows.append(row)
    # unknowns: a_m (m>=1), b_m, c_m ; a_0 = 1 is subtracted off
    A = sp.Matrix([[r[0 + k] for k in range(1, deg + 1)] +
                   [r[deg + 1 + m] for m in range(deg + 1)] +
                   [r[2 * (deg + 1) + m] for m in range(deg + 1)] for r in rows])
    bvec = sp.Matrix([-r[0] for r in rows])
    # least-squares / exact solve
    sol = sp.linsolve((A, bvec))
    return sol


print('=' * 92)
print('2DTL bilinear probe on the y-lattice tau (N=2,3,4,5)')
print('=' * 92)


def bilin_2dtl(T, n, j=0):
    """ (1/2 Dx Dy - 1) t_n.t_n + t_{n+1} t_{n-1} """
    def DxDy(F, G):
        return sp.expand(sp.diff(F, x) * sp.diff(G, y) - sp.diff(F, y) * sp.diff(G, x))
    t0 = T.tau(n, j)
    t0x = sp.expand(sp.diff(t0, x))
    return None


for (N, p, q) in [(2, [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)]),
                  (3, [2, 3, sp.Rational(9, 2)], [sp.Rational(3, 2), 4, sp.Rational(11, 3)])]:
    T = Tau(N, A_VAL, H_VAL, p, q)
    for n in (0, 1):
        for j in (0, 1):
            t0 = T.tau(n, j)
            t1 = T.tau(n + 1, j)
            tm = T.tau(n - 1, j)
            lhs = sp.Rational(1, 2) * (sp.diff(t0, x, y) * t0 - sp.diff(t0, x) * sp.diff(t0, y)) - t0 * t0 \
                + t1 * tm
            print('  N=%d n=%d j=%d   2DTL residual = %.6g'
                  % (N, n, j, ev(lhs)))
