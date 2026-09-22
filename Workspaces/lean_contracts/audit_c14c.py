"""Check the n2-side lattice structure for the Lean proof of C14.

Claim:  n2 = lx Psi  with
  Psi = (4/h) V_t + d0 h (U_t) + lx(d0 h H + (u+2a)W - 4u) + lx(d0 h u + (h^2/4) lap h W)
and      Psi = d0 h (A + C) + (4/h) (A - C).
"""
import sympy as sp
from audit_c14 import (J, D, dx, dxx, dt, dm, d0, mm, lap, P, Q, U, V, Av, Cv, a, h,
                       u, Wf, H, v)


def Psi(j):
    t1 = (4 / h) * dt(V(j))
    t2 = d0(lambda i: dt(U(i)), j)
    inner1 = lambda i: d0(H, i) + (u(i) + 2 * a) * Wf(i) - 4 * u(i)
    t3 = inner1(j)
    inner2 = lambda i: d0(u, i) + (h ** 2 / 4) * lap(Wf, i)
    t4 = dx(inner2(j))
    return t1 + t2 + t3 + t4


S = lambda j: Av(j) + Cv(j)
for site in (0, 1, -1, 2):
    e = sp.simplify(sp.cancel(sp.expand(
        Psi(site) - (d0(S, site) + (4 / h) * (Av(site) - Cv(site))))))
    print(f'Psi - [d0(A+C) + (4/h)(A-C)] at site {site}: {e}')
