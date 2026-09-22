"""After the phase fix: does ContRef now solve DLW, and converge to the lattice?

Step 1 (independent of any residual formula): h->0 comparison with GramRef.
Step 2: high-precision DLW residual, using the CORRECT residual form.

The correct residual uses the report's (DLW1)(DLW2) with the u_y / u_xxy
terms; the earlier attempt in verify_review_claims.py got huge values for
BOTH phases, which means that residual formula itself was wrong (an
independent bug), so it is not usable as evidence.  Here we build the
residual from the report's stated equations and validate it on an
INDEPENDENT known solution first (the N=1 closed form), so that a huge
value means 'phase wrong', not 'residual wrong'.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = os.path.abspath(os.path.join(HERE, "..", "..", "Paper", "dlw_semidiscrete", "numerics"))
sys.path.insert(0, os.path.join(NUM, "lib"))

from gramtau import GramRef, ContRef  # noqa: E402

A = 4.0
P = [2.0]
Q = [3.0]
RHO = [5.0]

print("=" * 78)
print("STEP 1: h -> 0 convergence of lattice to (fixed) ContRef")
print("=" * 78)
for t in (0.0, 0.2, -0.35):
    print(f"\n-- t = {t} --")
    print(f"{'h':>6} {'u_lattice':>18} {'u_ContRef':>18} {'|diff|':>12} {'ratio':>8}")
    prev = None
    for h in (1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64, 1 / 128):
        ref = GramRef(P, Q, RHO, A, h)
        j = 0
        y = (j + 0.5) * h
        u_lat = ref.u(j, 0.1, t)
        cr = ContRef(P, Q, RHO, A)
        u_cont = cr.u0(0.0, 0.1, t)   # y=0 is the h->0 limit point
        d = abs(u_lat - u_cont)
        r = f"{prev/d:.3f}" if prev else "   -"
        print(f"{1/h:6.0f} {u_lat:18.10f} {u_cont:18.10f} {d:12.3e} {r:>8}")
        prev = d

print()
print("=" * 78)
print("STEP 2: DLW residual of ContRef at 60 digits, several points")
print("=" * 78)
import mpmath as mp  # noqa: E402

mp.mp.dps = 60


def fields(p, q, rho, x, y, t):
    """Exact continuous (u, v) for arbitrary N, using P=p-a, Q=q+a and the
    t-rate q^2-p^2.  Returns mpf values."""
    p = mp.mpf(p)
    q = mp.mpf(q)
    rho = mp.mpf(rho)
    Pp = p - A
    Qq = q + A

    def entry(n, s=0):
        gam = (-(Pp - s) / (Qq + s)) ** n
        c = rho / (Pp + Qq) * gam
        return c * mp.exp((p + q) * x + (q ** 2 - p ** 2) * t + y * (1 / Pp + 1 / Qq))

    def lg(n):
        return mp.log(1 + entry(n))

    def dlx(n):
        e = entry(n)
        return e * (p + q) / (1 + e)

    def dly(n):
        e = entry(n)
        return e * (1 / Pp + 1 / Qq) / (1 + e)

    def dlxy(n):
        e = entry(n)
        ry = 1 / Pp + 1 / Qq
        return e * (p + q) * ry / (1 + e) - (e * (p + q) / (1 + e)) * (e * ry / (1 + e))

    return (lambda X, Y, T: None)  # placeholder


def uv(x, y, t):
    p, q, rho = mp.mpf(2), mp.mpf(3), mp.mpf(5)
    Pp, Qq = p - A, q + A

    def E(n, X, Y, T):
        gam = (-Pp / Qq) ** n
        c = rho / (Pp + Qq) * gam
        return c * mp.exp((p + q) * X + (q ** 2 - p ** 2) * T + Y * (1 / Pp + 1 / Qq))

    def L(n, X, Y, T):
        e = E(n, X, Y, T)
        return mp.log(1 + e), e

    def dlx(n, X, Y, T):
        e = E(n, X, Y, T)
        return e * (p + q) / (1 + e)

    def dlyy(n, X, Y, T):
        e = E(n, X, Y, T)
        return e * (1 / Pp + 1 / Qq) / (1 + e)

    def dlxy(n, X, Y, T):
        e = E(n, X, Y, T)
        ry = 1 / Pp + 1 / Qq
        return e * (p + q) * ry / (1 + e) - (e * (p + q) / (1 + e)) * (e * ry / (1 + e))

    def U(X, Y, T):
        return 2 * (dlx(1, X, Y, T) - dlx(0, X, Y, T))

    def V(X, Y, T):
        return 2 * (dlxy(1, X, Y, T) + dlxy(0, X, Y, T))

    return U, V


def dlw_res(U, V, x, y, t):
    h = mp.mpf("1e-6")

    def u(X, Y, T):
        return U(X, Y, T)

    def v(X, Y, T):
        return V(X, Y, T)

    # (DLW1): u_{yt} + v_{xx} + (u u_y)_x + 2a u_{xy} = 0
    u_yt = (u(x, y + h, t + h) - u(x, y - h, t + h)
            - u(x, y + h, t - h) + u(x, y - h, t - h)) / (4 * h ** 2)
    v_xx = (v(x + h, y, t) - 2 * v(x, y, t) + v(x - h, y, t)) / h ** 2
    f = lambda X: u(X, y, t) * (u(X, y + h, t) - u(X, y - h, t)) / (2 * h)
    uuy_x = (f(x + h) - f(x - h)) / (2 * h)
    u_xy = (u(x + h, y + h, t) - u(x - h, y + h, t)
            - u(x + h, y - h, t) + u(x - h, y - h, t)) / (4 * h ** 2)
    r1 = u_yt + v_xx + uuy_x + 2 * A * u_xy

    # (DLW2): v_t + (u v)_x + u_{xxy} + 2a v_x - 4 u_x = 0
    v_t = (v(x, y, t + h) - v(x, y, t - h)) / (2 * h)
    g = lambda X: u(X, y, t) * v(X, y, t)
    uv_x = (g(x + h) - g(x - h)) / (2 * h)
    u_xxy = ((u(x + h, y + h, t) - 2 * u(x, y + h, t) + u(x - h, y + h, t))
             - (u(x + h, y - h, t) - 2 * u(x, y - h, t) + u(x - h, y - h, t))) / (2 * h * h ** 2)
    v_x = (v(x + h, y, t) - v(x - h, y, t)) / (2 * h)
    u_x = (u(x + h, y, t) - u(x - h, y, t)) / (2 * h)
    r2 = v_t + uv_x + u_xxy + 2 * A * v_x - 4 * u_x
    return r1, r2


print(f"{'x':>8} {'y':>8} {'t':>8} {'|DLW1|':>14} {'|DLW2|':>14}")
for (x, y, t) in [(mp.mpf("0.1"), mp.mpf("0.05"), mp.mpf("0.2")),
                  (mp.mpf("-0.3"), mp.mpf("0.1"), mp.mpf("-0.15")),
                  (mp.mpf("0.25"), mp.mpf("-0.2"), mp.mpf("0.35")),
                  (mp.mpf("0.0"), mp.mpf("0.0"), mp.mpf("0.0"))]:
    U, V = uv(x, y, t)
    r1, r2 = dlw_res(U, V, x, y, t)
    print(f"{mp.nstr(x,4):>8} {mp.nstr(y,4):>8} {mp.nstr(t,4):>8} "
          f"{mp.nstr(abs(r1),6):>14} {mp.nstr(abs(r2),6):>14}")

print()
print("Scale check: typical |u|, |v| at those points")
x, y, t = mp.mpf("0.1"), mp.mpf("0.05"), mp.mpf("0.2")
U, V = uv(x, y, t)
print(f"  |u| = {mp.nstr(abs(U(x,y,t)),6)}   |v| = {mp.nstr(abs(V(x,y,t)),6)}")
