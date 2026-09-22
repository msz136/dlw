"""
lax11.py -- systematic search for the DISCRETE linear problem in the LATTICE
index j, i.e. for a Lax pair of the semidiscrete DLW system.

We take the exact staggered tau functions
      G_j = tau_0(j),   F_j = tau_1(j; a-d),   d = h/2,
form the natural wave-function candidates
      psi_j = F_j / G_j                     (the "u-field" potential)
      xi_j  = G_{j+1} / G_j ,   eta_j = F_{j+1}/F_j
and ask, by exact rational fitting, whether there is a firts-order /
second-order linear recursion
      psi_{j+1} = A_j psi_j + B_j psi_{j-1}
whose coefficients A_j, B_j are RATIONAL IN z with coefficients built from the
tau data (and whose monodromy is a nonconstant function of z).
"""
import sys
import sympy as sp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')

x, y, t = sp.symbols('x y t', real=True)
Z = sp.Symbol('z')
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
        self._c = {}

    def lam(self, v):
        return (v + self.h / 2) / (v - self.h / 2)

    def chi(self, i, k, s):
        return self.lam(self.p[i] - s) * self.lam(self.q[k] + s)

    def entry(self, n, j, i, k, s):
        p, q = self.p[i], self.q[k]
        P, Q = p - s, q + s
        coef = (-P / Q) ** n / (p + q)
        if j:
            coef *= self.chi(i, k, s) ** j
        return coef * sp.exp((p * x - p ** 2 * t + y / P) + (q * x + q ** 2 * t + y / Q))

    def M(self, n, j, s):
        return sp.Matrix(self.N, self.N, lambda i, k: self.entry(n, j, i, k, s))

    def tau(self, n, j, s=None):
        key = (n, j, s)
        if key not in self._c:
            self._c[key] = sp.expand(self.M(n, j, self.a if s is None else s).det())
        return self._c[key]


def ev(ex):
    v = complex(sp.sympify(ex).subs(P0))
    assert abs(v.imag) < 1e-16, v
    return v.real


N = 2
p = [1, sp.Rational(5, 2)]
q = [2, sp.Rational(7, 3)]
T = Tau(N, A_VAL, H_VAL, p, q)
d = T.h / 2
S_LO = T.a - d
S_HI = T.a + d

print('=' * 92)
print('structure of the staggered pair, N=%d' % N)
print('=' * 92)


def Gat(j):
    return T.tau(0, j, s=T.a)


def Fat(j):
    return T.tau(1, j, s=T.a - d)


for j in range(0, 3):
    print('  j=%d   G_j=%.10g  F_j=%.10g   F_j/G_j=%.10g  G_{j+1}/G_j=%.10g'
          % (j, ev(Gat(j)), ev(Fat(j)), ev(Fat(j)) / ev(Gat(j)),
             ev(Gat(j + 1)) / ev(Gat(j))))

print()
print('=' * 92)
print('search:  is  psi_j = F_j/G_j  a solution of a SPECTRAL recursion in j?')
print('  Test  psi_{j+1} = A psi_j + B psi_{j-1}  with A,B from the minimal')
print('  algebraic candidates built out of the tau data:')
print('=' * 92)

# tau-data candidates (all z-independent) at site j
def cands(j):
    G, Gm, Gp = Gat(j), Gat(j - 1), Gat(j + 1)
    F, Fm, Fp = Fat(j), Fat(j - 1), Fat(j + 1)
    return {
        'G': G, 'Gm': Gm, 'Gp': Gp, 'F': F, 'Fm': Fm, 'Fp': Fp,
        'Gp/G': Gp / G, 'G/Gm': G / Gm, 'Fp/F': Fp / F, 'F/Fm': F / Fm,
        'F/G': F / G, 'Fm/Gm': Fm / Gm, 'Fp/Gp': Fp / Gp,
    }


for j in (1, 2):
    C = cands(j)
    psi = [ev(Fat(k)) / ev(Gat(k)) for k in (j - 1, j, j + 1)]
    print('  j=%d  psi(j-1)=%.10g psi(j)=%.10g psi(j+1)=%.10g' % (j, *psi))
    print('        ratios psi(j+1)/psi(j)=%.10g   psi(j)/psi(j-1)=%.10g'
          % (psi[2] / psi[1], psi[1] / psi[0]))
    print('        Gp/G=%.10g  Fp/F=%.10g  (Fp/Gp)/(F/G)=%.10g'
          % (ev(C['Gp/G']), ev(C['Fp/F']), ev(C['Fp/Gp']) / ev(C['F/G'])))

print()
print('=' * 92)
print('Conclusion check: the two tau ratios that would be the Toda potentials:')
print('=' * 92)
for j in (1, 2):
    s_j = sp.simplify(Gat(j + 1) * Gat(j - 1) / Gat(j) ** 2)
    r_j = sp.simplify(Fat(j + 1) * Fat(j - 1) / Fat(j) ** 2)
    print('  j=%d   G: sigma_j = %.12g     F: sigma_j = %.12g' % (j, ev(s_j), ev(r_j)))
