# -*- coding: utf-8 -*-
"""
solver.py -- open-chain time integrator for the closed nonlinear DLW system
(N1)(N2), following numerical_analysis.html section 5.

STATE CHOICE (report 5.1)
-------------------------
Rather than advancing (u_j, v_j) directly -- which is ill-posed for the pure
sum because the average mode is not recoverable -- we advance

    P_j = delta_- u_j        (staggered difference, j = j_L+1 .. j_R)
    W_j = v_j - delta_0 u_j  (the same W as in the report)

with the evolution equations

    P_{j,t} = -delta_- d_x H_j  - d_x^2 ( M_- v_j - (h^2/4) Delta_h P_j )
    W_{j,t} = -d_x [ (u_j + 2a) W_j - 4 u_j ] + d_x^2 W_j

and reconstruct, on the OPEN CHAIN, from a left base value b(x,t) = u_{j_L}:

    u_j = b + h * sum_{m=j_L+1}^{j} P_m          (exact telescoping)
    v_j = W_j + delta_0 u_j

This makes the missing average mode an EXPLICIT INPUT (the base value b), which
is exactly what the report demands: "average mode cannot be recovered from the
sum; either supply a compatible average-mode condition or use the open-chain
base value."

x-DIRECTION
-----------
Periodic high-order finite differences on the x-grid.  The report prefers a
high-order FD or Chebyshev collocation with analytic boundary closure; for the
benchmark we use a periodic window wide enough that the soliton and its tails
leave the boundary region below tolerance, and we record the boundary residual
so the reader can see the truncation level.  (An open/Chebyshev variant is left
to E7-style follow-up.)

TIME ALGORITHMS (report 5.2)
----------------------------
    'euler'     : first-order explicit baseline
    'rk4'       : classical RK4, small-step short-time reference
    'trapezoid' : implicit trapezoidal / Crank-Nicolson-like, second order,
                  solved by a fixed-point/Newton iteration with recorded
                  residual and iteration count
    'if_rk4'    : exponential (integrating-factor) RK4 on the linear part
"""

import numpy as np


# ---------------------------------------------------------------------------
# periodic finite-difference derivative operators
# ---------------------------------------------------------------------------

def periodic_diff_matrix(n, L, order=2):
    """Return the periodic first-derivative matrix on n uniform points, spacing
    L/n, at the requested order (2, 4 or 6).  Constructed as a dense matrix so
    that it can be applied to every lattice site at once."""
    dx = L / n
    D = np.zeros((n, n))
    if order == 2:
        # central difference (f[i+1]-f[i-1])/(2dx): coefficients +/-1/2, NOT +/-1.
        c = [(-1, -0.5), (1, 0.5)]
    elif order == 4:
        c = [(-2, 1 / 12), (-1, -2 / 3), (1, 2 / 3), (2, -1 / 12)]
    elif order == 6:
        c = [(-3, -1 / 60), (-2, 3 / 20), (-1, -3 / 4),
             (1, 3 / 4), (2, -3 / 20), (3, 1 / 60)]
    else:
        raise ValueError("order must be 2, 4 or 6")
    for k, coef in c:
        for i in range(n):
            D[i, (i + k) % n] += coef / dx
    return D


class XGrid:
    """Periodic uniform x-grid with high-order derivative operators."""

    def __init__(self, n, L, order=4):
        self.n = n
        self.L = L
        self.dx = L / n
        self.order = order
        self.x = -L / 2 + np.arange(n) * self.dx
        self.D1 = periodic_diff_matrix(n, L, order)
        self.D2 = self.D1 @ self.D1
        self.D3 = self.D2 @ self.D1
        self.D4 = self.D2 @ self.D2
        self.D5 = self.D4 @ self.D1
        self.D6 = self.D3 @ self.D3

    def d1(self, f):
        return self.D1 @ f

    def d2(self, f):
        return self.D2 @ f


# ---------------------------------------------------------------------------
# open-chain lattice state
# ---------------------------------------------------------------------------

class Chain:
    """Open chain of lattice sites j = jL .. jR, carrying P_j and W_j.

    P is defined for j = jL+1 .. jR   (one fewer than the number of sites)
    W is defined for j = jL   .. jR
    u is defined for j = jL   .. jR   (base value pinned at jL)
    v follows from W + delta_0 u.
    """

    def __init__(self, jL, jR, h, a):
        assert jR > jL
        self.jL, self.jR = int(jL), int(jR)
        self.h, self.a = float(h), float(a)
        self.nj = self.jR - self.jL + 1
        self.P = None      # shape (nj-1, nx)
        self.W = None      # shape (nj,   nx)
        self.b = None      # base value u_{jL}, shape (nx,)

    # ---- reconstruction --------------------------------------------------
    def u_from_P(self, P, b):
        """u_j = b + h * cumsum(P)  (exact telescoping of delta_- u = P)."""
        out = np.empty((self.nj, P.shape[1]))
        out[0] = b
        if self.nj > 1:
            out[1:] = b[None, :] + self.h * np.cumsum(P, axis=0)
        return out

    def v_from_Wu(self, W, u):
        """v_j = W_j + delta_0 u_j."""
        v = W.copy()
        v[1:-1] += (u[2:] - u[:-2]) / (2 * self.h)
        # one-sided at the chain ends (ghost values are supplied by the caller
        # through the exact solution when running the benchmark)
        v[0] += (u[1] - self.ghost_left) / (2 * self.h)
        v[-1] += (self.ghost_right - u[-2]) / (2 * self.h)
        return v

    ghost_left = None
    ghost_right = None


# ---------------------------------------------------------------------------
# the nonlinear right-hand side
# ---------------------------------------------------------------------------

class DLWChainRHS:
    """Right-hand side of the (P, W) evolution on an open chain.

    Given the left base value b(x,t) (and the two ghost columns needed for
    delta_0 at the chain ends), compute dP/dt and dW/dt.
    """

    def __init__(self, chain, X, b_fun=None, ghost_left=None, ghost_right=None):
        self.C = chain
        self.X = X
        self.b_fun = b_fun              # callable (x, t) -> array, or None
        self.gl = ghost_left            # callable (x, t) -> array or array
        self.gr = ghost_right

    # -- helpers ----------------------------------------------------------
    def _u(self, P, b):
        return self.C.u_from_P(P, b)

    def _tv(self, f):
        """d_x of an (nj, nx) field."""
        return f @ self.X.D1.T

    def _tv2(self, f):
        return f @ self.X.D2.T

    def base(self, t):
        if self.b_fun is None:
            raise ValueError("base value b(x,t) must be supplied")
        return self.b_fun(t)

    def ghosts(self, t):
        gl = self.gl(t) if callable(self.gl) else self.gl
        gr = self.gr(t) if callable(self.gr) else self.gr
        return gl, gr

    # -- W equation -------------------------------------------------------
    def W_rhs(self, W, u, a):
        """W_t = -d_x[ (u+2a) W - 4 u ] + d_x^2 W."""
        flux = (u + 2.0 * a) * W - 4.0 * u
        return -self._tv(flux) + self._tv2(W)

    # -- P equation -------------------------------------------------------
    def P_rhs(self, P, W, u, v, a):
        """P_t = -delta_- d_x H - d_x^2 ( M_- v - (h^2/4) Delta_h P ).

        All lattice operators are applied exactly on the open chain; the
        chain-end values needed by delta_- and Delta_h use the reconstructed
        u,v and the supplied ghost columns / outer P values.
        """
        C, h = self.C, self.C.h
        H = 0.5 * u ** 2 + 2.0 * a * u + h ** 2 * (W ** 2 / 32.0 - W / 4.0)
        dH = self.d1(H)

        # delta_- d_x H
        dm_dH = (dH[1:] - dH[:-1]) / h

        # M_- v
        Mmv = 0.5 * (v[1:] + v[:-1])

        # Delta_h P (second difference of the staggered state)
        Dl = np.empty_like(P)
        Dl[1:-1] = (P[2:] - 2 * P[1:-1] + P[:-2]) / h ** 2
        Dl[0] = (P[1] - 2 * P[0] + self.P_left_ext) / h ** 2
        Dl[-1] = (self.P_right_ext - 2 * P[-1] + P[-2]) / h ** 2

        inner = Mmv - h ** 2 / 4.0 * Dl
        return -dm_dH - self.d2(inner)

    # external P values just outside the chain; in benchmark mode these come
    # from the exact solution, otherwise from a user-supplied closure.
    P_left_ext = 0.0
    P_right_ext = 0.0
    use_ext = False

    def d1(self, f):
        return f @ self.X.D1.T

    def d2(self, f):
        return f @ self.X.D2.T

    # -- full RHS ---------------------------------------------------------
    def rhs(self, t, P, W, gl=None, gr=None):
        C, a = self.C, self.C.a
        b = self.base(t)
        if gl is None or gr is None:
            gl, gr = self.ghosts(t)
        if self.use_ext:
            self.P_left_ext = self._eval_ext(self._ple, t)
            self.P_right_ext = self._eval_ext(self._pre, t)
        # reconstruct u with one ghost on each side so delta_0 is central
        u_ext = np.empty((C.nj + 2, P.shape[1]))
        u_ext[0] = gl
        u_ext[1:-1] = self._u(P, b)
        u_ext[-1] = gr
        u = u_ext[1:-1]
        v = W + (u_ext[2:] - u_ext[:-2]) / (2 * C.h)
        if not self.use_ext:
            self.P_left_ext = (u[0] - gl) / C.h
            self.P_right_ext = (gr - u[-1]) / C.h
        dP = self.P_rhs(P, W, u, v, a)
        dW = self.W_rhs(W, u, a)
        return dP, dW

    _ple = None
    _pre = None

    def _eval_ext(self, f, t):
        if f is None:
            return 0.0
        return f(t) if callable(f) else f

    def __call__(self, t, P, W):
        """Allow the RHS to be passed straight to `integrate`."""
        return self.rhs(t, P, W)


# ---------------------------------------------------------------------------
# time integrators
# ---------------------------------------------------------------------------

def integrate(rhs, t0, T, P0, W0, dt, method="rk4", tol=1e-12, maxit=50,
              record=None, stop_fn=None):
    """Advance (P, W) from t0 to T.

    Returns (P, W, info).  info records steps, iteration counts and the
    implicit residual for the trapezoidal method (report 5.1/5.2: record the
    nonlinear iteration tolerance, residual and iteration count).

    If method="trapezoid" and a step's fixed-point iteration fails to reach
    tol within maxit, that step is REFUSED: the returned state is the last
    accepted one, info["stopped"] explains the failure, info["final_t"] is
    the last accepted time, and info["trap_converged"] is False.  A
    non-converged implicit step is never silently accepted.
    """
    t = t0
    P, W = P0.copy(), W0.copy()
    nsteps = 0
    iters = []
    resids = []
    stopped = None
    while t < T - 1e-15:
        h_ = min(dt, T - t)
        if method == "euler":
            dP, dW = rhs(t, P, W)
            P = P + h_ * dP
            W = W + h_ * dW
        elif method == "rk4":
            k1P, k1W = rhs(t, P, W)
            k2P, k2W = rhs(t + h_ / 2, P + h_ / 2 * k1P, W + h_ / 2 * k1W)
            k3P, k3W = rhs(t + h_ / 2, P + h_ / 2 * k2P, W + h_ / 2 * k2W)
            k4P, k4W = rhs(t + h_, P + h_ * k3P, W + h_ * k3W)
            P = P + h_ / 6 * (k1P + 2 * k2P + 2 * k3P + k4P)
            W = W + h_ / 6 * (k1W + 2 * k2W + 2 * k3W + k4W)
        elif method == "trapezoid":
            Pn, Wn = P.copy(), W.copy()
            f0P, f0W = rhs(t, Pn, Wn)
            Pi, Wi = Pn + h_ * f0P, Wn + h_ * f0W      # explicit predictor
            it = 0
            res = np.inf
            converged = False
            for it in range(1, maxit + 1):
                fP, fW = rhs(t + h_, Pi, Wi)
                Pnew = Pn + h_ / 2 * (f0P + fP)
                Wnew = Wn + h_ / 2 * (f0W + fW)
                res = max(np.max(np.abs(Pnew - Pi)), np.max(np.abs(Wnew - Wi)))
                Pi, Wi = Pnew, Wnew
                if res < tol:
                    converged = True
                    break
            if not converged:
                # Do NOT accept a step whose fixed-point iteration did not
                # converge: the accepted value would be an arbitrary iterate.
                # Refuse it and report, so that callers cannot mistake it for
                # a successful implicit step.
                stopped = ("trapezoid iteration failed to converge at t=%.6g "
                           "(h=%.3g, iters=%d, last iter diff=%.3e > tol=%.3e)"
                           % (t, h_, it, res, tol))
                info_fail = {"steps": nsteps, "final_t": t, "stopped": stopped,
                             "trap_converged": False}
                if iters:
                    info_fail["trap_mean_iters"] = float(np.mean(iters))
                    info_fail["trap_max_iters"] = int(np.max(iters))
                    info_fail["trap_max_resid"] = float(np.max(resids))
                info_fail["trap_fail_t"] = float(t)
                info_fail["trap_fail_iter_diff"] = float(res)
                return P, W, info_fail
            P, W = Pi, Wi
            iters.append(it)
            resids.append(res)
        else:
            raise ValueError("unknown method %r" % method)
        t += h_
        nsteps += 1
        if record is not None:
            record(t, P, W)
        if stop_fn is not None:
            msg = stop_fn(t, P, W)
            if msg:
                stopped = msg
                break
    info = {"steps": nsteps, "final_t": t, "stopped": stopped}
    if iters:
        info["trap_mean_iters"] = float(np.mean(iters))
        info["trap_max_iters"] = int(np.max(iters))
        info["trap_max_resid"] = float(np.max(resids))
    return P, W, info
