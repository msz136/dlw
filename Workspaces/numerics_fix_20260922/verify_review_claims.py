"""Independent re-verification of the review's central claims.

Written BEFORE touching production code, so that the fixes are grounded
in my own measurement rather than in the review's text.

Run:  python -u Workspaces/numerics_fix_20260922/verify_review_claims.py
"""
import os
import sys

import numpy as np
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = os.path.abspath(os.path.join(HERE, "..", "..", "Paper", "dlw_semidiscrete", "numerics"))
sys.path.insert(0, os.path.join(NUM, "lib"))

A = 4.0


def banner(s):
    print("\n" + "=" * 72)
    print(s)
    print("=" * 72)


# ---------------------------------------------------------------- claim 1
banner("CLAIM 1: ContRef time phase should be q^2-p^2, not Q^2-P^2")

mp.mp.dps = 60


def cont_fields(p, q, rho, y, x, t, phase):
    """Continuous N=1 Gram fields, with a selectable time phase.

    phase='correct' -> exp((p+q)x + (q^2-p^2)t + y(1/P+1/Q))
    phase='current' -> exp((p+q)x + (Q^2-P^2)t + y(1/P+1/Q))
    """
    P = mp.mpf(p) - A
    Q = mp.mpf(q) + A
    gam = -(P) / (Q)                      # n=1, s=0
    base = mp.exp((p + q) * mp.mpf(x) + y * (1 / P + 1 / Q))

    def coeff(n):
        return mp.mpf(rho) / (P + Q) * (gam ** n)

    def det(n):
        if phase == "correct":
            ph = mp.exp((mp.mpf(q) ** 2 - mp.mpf(p) ** 2) * mp.mpf(t))
        else:
            ph = mp.exp((Q ** 2 - P ** 2) * mp.mpf(t))
        return 1 + coeff(n) * base * ph

    lg1, lg0 = mp.log(det(1)), mp.log(det(0))

    def dlx(n):
        c = coeff(n)
        ph = (mp.exp((mp.mpf(q) ** 2 - mp.mpf(p) ** 2) * mp.mpf(t)) if phase == "correct"
              else mp.exp((Q ** 2 - P ** 2) * mp.mpf(t)))
        num = c * base * ph * (p + q)
        return num / det(n)

    def dly(n):
        c = coeff(n)
        ph = (mp.exp((mp.mpf(q) ** 2 - mp.mpf(p) ** 2) * mp.mpf(t)) if phase == "correct"
              else mp.exp((Q ** 2 - P ** 2) * mp.mpf(t)))
        e = c * base * ph
        ey = e * (1 / P + 1 / Q)
        return ey / det(n)

    def dlxy(n):
        c = coeff(n)
        ph = (mp.exp((mp.mpf(q) ** 2 - mp.mpf(p) ** 2) * mp.mpf(t)) if phase == "correct"
              else mp.exp((Q ** 2 - P ** 2) * mp.mpf(t)))
        e = c * base * ph
        ey = e * (1 / P + 1 / Q)
        ex = e * (p + q)
        exy = e * (p + q) * (1 / P + 1 / Q)
        d = det(n)
        return exy / d - (ex / d) * (ey / d)

    u = 2 * (dlx(1) - dlx(0))
    v = 2 * (dlxy(1) + dlxy(0))
    return u, v


def dlw_residual(u, v, x, t):
    """DLW residuals for (u,v) as functions of (x,y at fixed y),
    evaluated by finite differences in x with mpmath.

    (DLW1) u_{yt} + v_{xx} + (u u_y)_x + 2a u_{xy} = 0
    (DLW2) v_t + (u v)_x + u_{xxy} + 2a v_x - 4 u_x = 0

    We use u_y = 0 (N=1 fields are y-independent up to the exp(y(...))
    factor, which multiplies tau but drops out of u,v ratios only if
    it cancels -- so we compute at fixed y and treat y as a parameter).
    """
    h = mp.mpf("1e-8")
    ux = (u(x + h, t) - u(x - h, t)) / (2 * h)
    uxx = (u(x + h, t) - 2 * u(x, t) + u(x - h, t)) / h ** 2
    vx = (v(x + h, t) - v(x - h, t)) / (2 * h)
    vxx = (v(x + h, t) - 2 * v(x, t) + v(x - h, t)) / h ** 2
    ut = (u(x, t + h) - u(x, t - h)) / (2 * h)
    uxt = (u(x + h, t + h) - u(x - h, t + h) - u(x + h, t - h) + u(x - h, t - h)) / (4 * h ** 2)
    vt = (v(x, t + h) - v(x, t - h)) / (2 * h)
    # DLW2 has u_{xxy}: y-dependence.  For N=1 the y-part is exp(y(1/P+1/Q))
    # which DOES affect tau_1 vs tau_0 differently, so u carries y-dependence.
    # Use explicit y-derivative by evaluating at y +/- h.
    return dict(ux=ux, uxx=uxx, vx=vx, vxx=vxx, ut=ut, uxt=uxt, vt=vt)


# Evaluate the full 2-variable fields (y-dependence kept) so that
# y-derivatives are exact.
def cont_fields_xy(p, q, rho, x, y, t, phase):
    def mk(n):
        P = mp.mpf(p) - A
        Q = mp.mpf(q) + A
        gam = -(P / Q) ** n
        c = mp.mpf(rho) / (P + Q) * gam
        if phase == "correct":
            ph = mp.exp((mp.mpf(q) ** 2 - mp.mpf(p) ** 2) * mp.mpf(t))
        else:
            ph = mp.exp((Q ** 2 - P ** 2) * mp.mpf(t))
        return c * ph, P, Q

    def det(n, x, y):
        c, P, Q = mk(n)
        return 1 + c * mp.exp((mp.mpf(p) + mp.mpf(q)) * x + y * (1 / P + 1 / Q))

    def L(n, x, y):
        c, P, Q = mk(n)
        K = c * mp.exp((mp.mpf(p) + mp.mpf(q)) * x + y * (1 / P + 1 / Q))
        return mp.log(1 + K), K, P, Q

    def dlx(n, x, y):
        _, K, P, Q = L(n, x, y)
        return K * (mp.mpf(p) + mp.mpf(q)) / (1 + K)

    def dly(n, x, y):
        _, K, P, Q = L(n, x, y)
        return K * (1 / P + 1 / Q) / (1 + K)

    def dlxy(n, x, y):
        lg, K, P, Q = L(n, x, y)
        e = K
        ey = e * (1 / P + 1 / Q)
        ex = e * (mp.mpf(p) + mp.mpf(q))
        exy = e * (mp.mpf(p) + mp.mpf(q)) * (1 / P + 1 / Q)
        d = 1 + K
        return exy / d - (ex / d) * (ey / d)

    def u(x, y, t):
        return 2 * (dlx(1, x, y) - dlx(0, x, y))

    def v(x, y, t):
        return 2 * (dlxy(1, x, y) + dlxy(0, x, y))

    return u, v


def residual_full(u, v, x, y, t):
    h = mp.mpf("1e-6")

    def U(x, y, t):
        return u(x, y, t)

    def V(x, y, t):
        return v(x, y, t)

    # DLW1: u_{yt} + v_{xx} + (u u_y)_x + 2a u_{xy}
    u_yt = (U(x, y, t + h) - U(x, y, t - h)) / (2 * h)
    u_yt = (U(x, y + h, t + h) - U(x, y - h, t + h)
            - U(x, y + h, t - h) + U(x, y - h, t - h)) / (4 * h ** 2)
    v_xx = (V(x + h, y, t) - 2 * V(x, y, t) + V(x - h, y, t)) / h ** 2
    uu_y = U(x, y, t) * (U(x, y + h, t) - U(x, y - h, t)) / (2 * h)
    uu_y_x = ((U(x + h, y, t) * (U(x + h, y + h, t) - U(x + h, y - h, t)) / (2 * h))
              - (U(x - h, y, t) * (U(x - h, y + h, t) - U(x - h, y - h, t)) / (2 * h))) / (2 * h)
    u_xy = (U(x + h, y + h, t) - U(x - h, y + h, t)
            - U(x + h, y - h, t) + U(x - h, y - h, t)) / (4 * h ** 2)
    r1 = u_yt + v_xx + uu_y_x + 2 * A * u_xy

    # DLW2: v_t + (u v)_x + u_{xxy} + 2a v_x - 4 u_x
    v_t = (V(x, y, t + h) - V(x, y, t - h)) / (2 * h)
    uv = U(x, y, t) * V(x, y, t)
    uv_x = ((U(x + h, y, t) * V(x + h, y, t)) - (U(x - h, y, t) * V(x - h, y, t))) / (2 * h)
    u_xxy = ((U(x + h, y + h, t) - 2 * U(x, y + h, t) + U(x - h, y + h, t))
             - (U(x + h, y - h, t) - 2 * U(x, y - h, t) + U(x - h, y - h, t))) / (2 * h * h ** 2)
    v_x = (V(x + h, y, t) - V(x - h, y, t)) / (2 * h)
    u_x = (U(x + h, y, t) - U(x - h, y, t)) / (2 * h)
    r2 = v_t + uv_x + u_xxy + 2 * A * v_x - 4 * u_x

    return r1, r2


pts = [(mp.mpf("0.1"), mp.mpf("0.05"), mp.mpf("0.2")),
       (mp.mpf("-0.3"), mp.mpf("0.1"), mp.mpf("-0.15")),
       (mp.mpf("0.25"), mp.mpf("-0.2"), mp.mpf("0.35"))]

print(f"{'phase':>9} {'point':>5} {'|DLW1|':>14} {'|DLW2|':>14}")
for phase in ("correct", "current"):
    for i, (x, y, t) in enumerate(pts):
        u, v = cont_fields_xy(2.0, 3.0, 5.0, x, y, t, phase)
        r1, r2 = residual_full(u, v, x, y, t)
        print(f"{phase:>9} {i:>5} {mp.nstr(abs(r1), 6):>14} {mp.nstr(abs(r2), 6):>14}")

banner("CLAIM 6: order=2 central difference missing 1/2")


def periodic_diff_matrix(x, order=4):
    """Copy of the production builder, for the sine test."""
    n = len(x)
    dx = x[1] - x[0]
    D = np.zeros((n, n))
    if order == 2:
        for i in range(n):
            D[i, (i + 1) % n] = 1.0 / dx
            D[i, (i - 1) % n] = -1.0 / dx
    elif order == 4:
        for i in range(n):
            D[i, (i + 1) % n] = 2.0 / (3 * dx)
            D[i, (i - 1) % n] = -2.0 / (3 * dx)
            D[i, (i + 2) % n] = -1.0 / (6 * dx)
            D[i, (i - 2) % n] = 1.0 / (6 * dx)
    return D


n = 128
x = np.linspace(0, 2 * np.pi, n, endpoint=False)
D2 = periodic_diff_matrix(x, 2)
f = np.sin(x)
print(f"order=2 D1@sin at x=0 : {D2 @ f [0]:.10f}   (true 1.0)")

banner("CLAIM 5: trapezoid accepts a non-converged step")


def trapezoid_bad(z0, dt, maxit, tol, fz=lambda z: 10 * z):
    z = z0
    for it in range(maxit):
        znew = z + 0.5 * dt * (fz(z) + fz(z))
        if abs(znew - z) < tol:
            return znew, it + 1, True
        z = znew
    return z, maxit, False


z, iters, ok = trapezoid_bad(1.0, 1.0, 2, 1e-12)
print(f"returned z={z}, iters={iters}, converged={ok}")

banner("CLAIM 3: E1 L2 exponent comes from shrinking integration region")

from fractions import Fraction  # noqa


def l2_region_fixed(h, ylo=-1.5, yhi=1.5):
    """L2 over a FIXED physical y-window, with all quadrature weights."""
    js = []
    j = -200
    while j <= 200:
        y = (j + 0.5) * h
        if ylo <= y <= yhi:
            js.append(j)
        j += 1
    return js


for h in (1 / 4, 1 / 8, 1 / 16, 1 / 32):
    js = l2_region_fixed(h)
    print(f"h={h:.5f}  #points in fixed window = {len(js)}")
