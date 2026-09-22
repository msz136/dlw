"""Symbolic (jet-variable) check of the C14 residual identity.

We model P_j(x,t) = log F_j, Q_j(x,t) = log G_j as free functions of (x,t)
indexed by site j, with all derivatives treated as independent symbols
(a "jet algebra").  Every quantity in Contracts.C14 is a polynomial in these
jets with coefficients in Q(a,h), so the identity is checked exactly:
the difference must be the literal sympy expression 0.

No floating point is used anywhere.
"""
import sympy as sp

a, h = sp.symbols('a h', nonzero=True)

_jets = {}


def J(name, j, nx, nt):
    key = (name, j, nx, nt)
    if key not in _jets:
        _jets[key] = sp.Symbol(f'{name}[{j}]_x{nx}t{nt}')
    return _jets[key]


def _parsed(s):
    """('P', j, nx, nt) for a jet symbol name, else None."""
    if '[' not in s or '_x' not in s:
        return None
    name = s.split('[')[0]
    j = int(s.split('[')[1].split(']')[0])
    nx = int(s.split('_x')[1].split('t')[0])
    nt = int(s.split('_x')[1].split('t')[1])
    return (name, j, nx, nt)


def D(e, axis):
    """Differentiate a jet expression w.r.t. x ('x') or t ('t')."""
    if e.is_Symbol:
        p = _parsed(e.name)
        if p is None:
            return sp.S.Zero
        name, j, nx, nt = p
        return J(name, j, nx + (1 if axis == 'x' else 0), nt + (1 if axis == 't' else 0))
    if not any(_parsed(s.name) is not None for s in e.free_symbols):
        return sp.S.Zero
    if e.is_Add:
        return sp.Add(*[D(arg, axis) for arg in e.args])
    if e.is_Mul:
        terms = []
        for i, arg in enumerate(e.args):
            rest = sp.Mul(*[x for k, x in enumerate(e.args) if k != i])
            terms.append(D(arg, axis) * rest)
        return sp.Add(*terms)
    if e.is_Pow:
        base, exp = e.args
        if not any(_parsed(s.name) is not None for s in base.free_symbols):
            return sp.S.Zero
        return exp * base ** (exp - 1) * D(base, axis)
    raise RuntimeError(f'unhandled node {e} ({sp.srepr(e)})')


def P(j):
    return J('P', j, 0, 0)


def Q(j):
    return J('Q', j, 0, 0)


def dx(e):
    return D(e, 'x')


def dxx(e):
    return D(D(e, 'x'), 'x')


def dt(e):
    return D(e, 't')


# ---- lattice operators (Contracts.lean definitions), as functions of site ----
def dm(z, j):
    return (z(j) - z(j - 1)) / h


def d0(z, j):
    return (z(j + 1) - z(j - 1)) / (2 * h)


def mm(z, j):
    return (z(j) + z(j - 1)) / 2


def lap(z, j):
    return (z(j + 1) - 2 * z(j) + z(j - 1)) / h ** 2


# ---- physical fields ----
def U(j):
    return 2 * P(j) - Q(j) - Q(j + 1)


def u(j):
    return dx(U(j))


def V(j):
    return Q(j + 1) - Q(j)


def Wf(j):
    return (4 / h) * dx(V(j))


# v = (4/h) lx(R-Q) + d0 h u  (so that W = v - d0 u)
def v(j):
    return Wf(j) + d0(u, j)


def H(j):
    return u(j) ** 2 / 2 + (2 * a) * u(j) + h ** 2 * (Wf(j) ** 2 / 32 - Wf(j) / 4)


# ---- normalized bilinear residuals ----
def Av(j):
    return (dxx(P(j) + Q(j)) + dx(P(j) - Q(j)) ** 2 + dt(P(j) - Q(j))
            + (2 * a - h) * dx(P(j) - Q(j)))


def Cv(j):
    return (dxx(P(j) + Q(j) + 0) + dx(P(j) - Q(j + 1)) ** 2 + dt(P(j) - Q(j + 1))
            + (2 * a + h) * dx(P(j) - Q(j + 1)))


# fix Cv: second derivative is of P + R with R = Q(j+1)
def Cv(j):
    return (dxx(P(j) + Q(j + 1)) + dx(P(j) - Q(j + 1)) ** 2 + dt(P(j) - Q(j + 1))
            + (2 * a + h) * dx(P(j) - Q(j + 1)))


# ---- LHS of C14 ----
def n1(j):
    t1 = dm(lambda i: dt(u(i)) + dx(H(i)), j)
    G = lambda i: mm(v, i) - (h ** 2 / 4) * lap(lambda k: dm(u, k), i)
    return t1 + dxx(G(j))


def n2(j):
    t1 = dt(v(j))
    inner = lambda i: d0(H, i) + (u(i) + 2 * a) * Wf(i) - 4 * u(i)
    t2 = dx(inner(j))
    G = lambda i: d0(u, i) + (h ** 2 / 4) * lap(Wf, i)
    return t1 + t2 + dxx(G(j))


def rhs1(j):
    return dm(lambda i: dx(Av(i) + Cv(i)), j)


def rhs2(j):
    return d0(lambda i: dx(Av(i) + Cv(i)), j) + (4 / h) * dx(Av(j) - Cv(j))


for name, lhs, rhs in (('n1', n1, rhs1), ('n2', n2, rhs2)):
    for site in (0, 1, -1):
        e = sp.simplify(sp.together(sp.expand(lhs(site) - rhs(site))))
        e = sp.simplify(sp.cancel(sp.expand(e)))
        print(f'{name} at site {site}: difference = {e}')
