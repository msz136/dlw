"""Check the intermediate lattice identity used to structure the Lean proof of C14.

Claim:   dm h Phi + lxG  ==  dm h (A + C)
with
  U = 2P - Q - R,  V = R - Q,
  Phi = U_t + (1/2)(U_x)^2 + (1/2)(V_x)^2 + 2a U_x - h V_x,
  lxG = (4/h) mm(V_xx) + mm(d0 h (U_xx)) - (h^2/4) lap h (dm h (U_xx)),
  A, C the normalized bilinear residuals (C13 forms).
Also check the n2 decomposition.
"""
import sympy as sp
from audit_c14 import J, D, dx, dxx, dt, dm, d0, mm, lap, P, Q, U, V, Av, Cv, a, h


def Phi(j):
    return dt(U(j)) + sp.Rational(1, 2) * dx(U(j)) ** 2 + sp.Rational(1, 2) * dx(V(j)) ** 2 \
        + 2 * a * dx(U(j)) - h * dx(V(j))


def O(z):
    """lxx as a lattice: site -> xx of z at that site"""
    return lambda j: dxx(z(j))


def lxG(j):
    OU = O(U)
    OV = O(V)
    return ((4 / h) * mm(OV, j) + mm(lambda i: d0(OU, i), j)
            - (h ** 2 / 4) * lap(lambda i: dm(OU, i), j))


S = lambda j: Av(j) + Cv(j)
for site in (0, 1, -1, 2):
    e = sp.simplify(sp.cancel(sp.expand(dm(Phi, site) + lxG(site) - dm(S, site))))
    print(f'conjunct1 structure, site {site}: {e}')
