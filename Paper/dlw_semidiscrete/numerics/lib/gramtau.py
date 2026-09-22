# -*- coding: utf-8 -*-
"""
gramtau.py -- finite-h Gram tau evaluation for arbitrary N.

Faithful, self-contained re-implementation of (G) in
GRAM_INTEGRABILITY_REASSESSMENT.md, written directly in log-space so that
large x/t do not overflow, and so that analytic x-derivatives are available
to all orders via the log-det identity

    d_x log det M = tr(M^{-1} M_x)
    d_x^2 log det M = tr(M^{-1}M_xx) - tr((M^{-1}M_x)^2)

Every block M, M_x, M_xx, M_t, M_xt is formed in closed form; no entry is
ever differenced numerically.
"""

import numpy as np

# ---------------------------------------------------------------------------


def lam(z, h):
    d = h / 2.0
    return (z + d) / (z - d)


class GramBlock:
    """One Gram matrix family M(n, j; s) with analytic derivatives.

    Entry:
        M_ik = delta_ik + A_ik * exp( (p_i+q_k) x + (q_k^2-p_i^2) t )
        A_ik = rho_i/(p_i+q_k) * (-(p_i-s)/(q_k+s))^n * chi_ik^j
        chi_ik = lam(p_i-a) lam(q_k+a)
    """

    def __init__(self, p, q, rho, a, h, n, j, s):
        self.p = np.asarray(p, dtype=float)
        self.q = np.asarray(q, dtype=float)
        self.rho = np.asarray(rho, dtype=float)
        self.a = float(a)
        self.h = float(h)
        self.n = n
        self.j = j
        self.s = float(s)
        self.N = len(self.p)
        P = self.p[:, None]
        Q = self.q[None, :]
        gam = (-(P - self.s) / (Q + self.s)) ** n
        chi = lam(P - self.a, self.h) * lam(Q + self.a, self.h)
        self.A = (self.rho[:, None] / (P + Q)) * gam * chi ** j
        self.pq = P + Q                      # d_x exponent rate
        self.pq2 = (self.q[None, :] ** 2 - self.p[:, None] ** 2)   # d_t rate
        self.pq3 = self.pq * self.pq2        # d_xt rate

    # -- powers of the exponent factor -----------------------------------
    def _E(self, x, t):
        """exp(rate), evaluated UNSHIFTED.

        The entries are A*exp(rate) + I, and the identity part does not carry
        any log-sum-exp shift, so the shift may NOT be factored out.  We
        therefore exponentiate the true rate and require callers to keep the
        region moderate (the report's baseline parameters do).  `max_exponent`
        is available as an overflow guard.
        """
        ex = self.pq * x + self.pq2 * t
        m = ex.max()
        if not np.isfinite(m):
            raise FloatingPointError("non-finite exponent in Gram block")
        return np.exp(ex), m

    def M(self, x, t):
        E, _ = self._E(x, t)
        return self.A * E + np.eye(self.N)

    def Mx(self, x, t):
        E, _ = self._E(x, t)
        return self.A * self.pq * E

    def Mxx(self, x, t):
        E, _ = self._E(x, t)
        return self.A * self.pq ** 2 * E

    def Mt(self, x, t):
        E, _ = self._E(x, t)
        return self.A * self.pq2 * E

    def Mxt(self, x, t):
        E, _ = self._E(x, t)
        return self.A * self.pq3 * E

    # -- log-derivatives --------------------------------------------------
    def logdet(self, x, t):
        """log det M  (includes the log-sum-exp shift so the value is correct)."""
        M = self.M(x, t)
        return float(np.linalg.slogdet(M)[1])

    def _shift(self, x, t):
        """Largest exponent rate (diagnostic only; not factored out of M)."""
        ex = self.pq * x + self.pq2 * t
        m = ex.max()
        if not np.isfinite(m):
            raise FloatingPointError("non-finite exponent in Gram block")
        return float(m)

    def max_exponent(self, x, t):
        """Largest actual exponent appearing in any entry (overflow guard)."""
        return self._shift(x, t)

    def dlog(self, x, t):
        """d_x log det M."""
        M = self.M(x, t)
        return float(np.trace(np.linalg.solve(M, self.Mx(x, t))))

    def d2log(self, x, t):
        """d_x^2 log det M.  Shift is piecewise linear in x => zero 2nd deriv."""
        M = self.M(x, t)
        A = np.linalg.solve(M, self.Mx(x, t))
        B = np.linalg.solve(M, self.Mxx(x, t))
        return float(np.trace(B) - np.trace(A @ A))

    def dt_logdet(self, x, t):
        M = self.M(x, t)
        return float(np.trace(np.linalg.solve(M, self.Mt(x, t))))

    def dt_dlog(self, x, t):
        """d_t d_x log det M  (needed for u_t)."""
        M = self.M(x, t)
        iM = np.linalg.inv(M)
        return float(np.trace(iM @ self.Mxt(x, t))
                     - np.trace((iM @ self.Mt(x, t)) @ (iM @ self.Mx(x, t))))


class GramRef:
    """The reference solution family: F_j = tau_1(j;a-d), G_j = tau_0(j)."""

    def __init__(self, p, q, rho, a, h):
        self.p = list(map(float, p))
        self.q = list(map(float, q))
        self.rho = list(map(float, rho))
        self.a = float(a)
        self.h = float(h)
        self.d = self.h / 2.0
        self.N = len(self.p)

    def _blk(self, n, j, s):
        return GramBlock(self.p, self.q, self.rho, self.a, self.h, n, j, s)

    # F lives on tau_1(.; a-d);  G on tau_0(.; a) which is s-independent
    def _F(self, j):
        return self._blk(1, j, self.a - self.d)

    def _G(self, j):
        return self._blk(0, j, self.a)

    # ---- field values ---------------------------------------------------
    def F(self, j, x, t):
        return float(np.exp(self.logF(j, x, t)))

    def G(self, j, x, t):
        return float(np.exp(self.logG(j, x, t)))

    def logF(self, j, x, t):
        return self._F(j).logdet(x, t)

    def logG(self, j, x, t):
        return self._G(j).logdet(x, t)

    def dlogF(self, j, x, t):
        return self._F(j).dlog(x, t)

    def dlogG(self, j, x, t):
        return self._G(j).dlog(x, t)

    def d2logF(self, j, x, t):
        return self._F(j).d2log(x, t)

    def d2logG(self, j, x, t):
        return self._G(j).d2log(x, t)

    def dtlogF(self, j, x, t):
        return self._F(j).dt_logdet(x, t)

    def dtlogG(self, j, x, t):
        return self._G(j).dt_logdet(x, t)

    # ---- u, v ------------------------------------------------------------
    def u(self, j, x, t):
        return 2.0 * self.dlogF(j, x, t) - self.dlogG(j, x, t) - self.dlogG(j + 1, x, t)

    def Wg(self, j, x, t):
        return 4.0 / self.h * (self.dlogG(j + 1, x, t) - self.dlogG(j, x, t))

    def v(self, j, x, t):
        d0u = (self.u(j + 1, x, t) - self.u(j - 1, x, t)) / (2.0 * self.h)
        return self.Wg(j, x, t) + d0u

    # ---- tangents (for exact time-advance comparisons) -------------------
    def u_t(self, j, x, t):
        return (2.0 * self._F(j).dt_dlog(x, t)
                - self._G(j).dt_dlog(x, t)
                - self._G(j + 1).dt_dlog(x, t))

    # ---- normalized bilinear residuals ----------------------------------
    def B_norm(self, j, sign, x, t):
        """Normalized Hirota residual of the two finite-h bilinear equations.

            sign = -1 :  R_B^- = B_{a-h/2} F_j . G_j      / (F_j G_j)
            sign = +1 :  R_B^+ = B_{a+h/2} F_j . G_{j+1}  / (F_j G_{j+1})

        with  B_s F.G = (D_x^2 + D_t + 2s D_x) F.G
                      = F_xx G - 2 F_x G_x + F G_xx + F_t G - F G_t
                        + 2s (F_x G - F G_x).

        Every derivative is analytic (log-det identities); no differencing.
        """
        if sign < 0:
            s = self.a - self.d
            bF, bG = self._F(j), self._G(j)
        else:
            s = self.a + self.d
            bF, bG = self._F(j), self._G(j + 1)
        lF, lG = bF.logdet(x, t), bG.logdet(x, t)
        dF, dG = bF.dlog(x, t), bG.dlog(x, t)
        ddF, ddG = bF.d2log(x, t), bG.d2log(x, t)
        tF, tG = bF.dt_logdet(x, t), bG.dt_logdet(x, t)
        # F_xx/F = d2log + (dlog)^2
        Fxx_F = ddF + dF * dF
        Gxx_G = ddG + dG * dG
        val = (Fxx_F - 2.0 * dF * dG + Gxx_G) + (tF - tG) + 2.0 * s * (dF - dG)
        return float(val)

    # ---- array helpers ---------------------------------------------------
    def u_series(self, js, xs, t):
        js = np.asarray(js)
        return np.array([[self.u(int(j), float(x), t) for x in xs] for j in js])

    def v_series(self, js, xs, t):
        js = np.asarray(js)
        return np.array([[self.v(int(j), float(x), t) for x in xs] for j in js])

    def sample(self, js, xs, t):
        return self.u_series(js, xs, t), self.v_series(js, xs, t)

    # ---- vectorized evaluation over an x-array --------------------------
    # u_j = 2 dlogF_j - dlogG_j - dlogG_{j+1} and v_j depends on u_{j+-1},
    # so a whole j-row can be produced from the dlogF/dlogG tables.

    def dlogF_x(self, j, xs, t):
        """d_x log F_j on an array of x values."""
        return self._vec(lambda xx: self._F(j).dlog(xx, t), xs)

    def dlogG_x(self, j, xs, t):
        return self._vec(lambda xx: self._G(j).dlog(xx, t), xs)

    def _vec(self, fn, xs):
        """Apply a scalar-x function over an array, returning NaN outside the
        numerically representable region instead of raising.

        The Gram exponentials genuinely overflow for large |x| at large |t|
        (e.g. |x| >~ 120 at |t| = 40 for the baseline parameters).  Callers
        that scan x must be able to see a NaN and decide, rather than having
        the whole sweep abort.
        """
        xs = np.asarray(xs, dtype=float)
        out = np.empty(xs.shape)
        for i, xx in enumerate(xs.ravel()):
            try:
                out.ravel()[i] = fn(float(xx))
            except (FloatingPointError, OverflowError, ValueError,
                    np.linalg.LinAlgError):
                out.ravel()[i] = np.nan
        return out

    def u_row(self, j, xs, t):
        return (2.0 * self.dlogF_x(j, xs, t)
                - self.dlogG_x(j, xs, t) - self.dlogG_x(j + 1, xs, t))

    def W_row(self, j, xs, t):
        return 4.0 / self.h * (self.dlogG_x(j + 1, xs, t) - self.dlogG_x(j, xs, t))

    def v_row(self, j, xs, t):
        """v_j = W_j + delta_0 u_j, vectorized over x."""
        d0u = (self.u_row(j + 1, xs, t) - self.u_row(j - 1, xs, t)) / (2.0 * self.h)
        return self.W_row(j, xs, t) + d0u

    def u_block(self, js, xs, t):
        js = list(js)
        return np.array([self.u_row(int(j), xs, t) for j in js])

    def v_block(self, js, xs, t):
        js = list(js)
        return np.array([self.v_row(int(j), xs, t) for j in js])


# ---------------------------------------------------------------------------
# Continuous reference (h -> 0), report 4.3
# ---------------------------------------------------------------------------

class ContRef:
    """Continuous f,g obtained by chi^j -> exp(y(1/P + 1/Q)), gamma -> -P/Q.

    The x-rate is (p+q) and the t-rate is (q^2-p^2): BOTH are inherited
    unchanged from the lattice Gram block (eq. (G)).  Only the lattice
    phase chi^j is replaced.  See the comment in __init__.
    """

    def __init__(self, p, q, rho, a):
        self.p = list(map(float, p))
        self.q = list(map(float, q))
        self.rho = list(map(float, rho))
        self.a = float(a)
        self.P = [pi - self.a for pi in self.p]
        self.Q = [qk + self.a for qk in self.q]
        self.N = len(self.p)
        # The time rate is q^2 - p^2 in the ORIGINAL spectral parameters.
        # The lattice construction (GramBlock, eq. (G)) carries the raw
        # q^2 - p^2 rate, and this continuous reference is its h -> 0 limit,
        # so it must carry the same rate.  Using Q^2 - P^2 here instead
        # would amount to an extra x -> x + 2at translation, which makes the
        # reference fail to converge to the lattice solution as h -> 0
        # (measured: error stalls at O(1) instead of falling like h).
        # See Workspaces/numerics_fix_20260922/decide_phase.py.
        pv = np.array(self.p)[:, None]
        qv = np.array(self.q)[None, :]
        self._trate = qv ** 2 - pv ** 2

    def _blk(self, n, y, s):
        # entry: delta + rho/(p+q) (-(p-s)/(q+s))^n exp((p+q)x+(q^2-p^2)t + y(1/P+1/Q))
        return GramBlock(
            self.p, self.q, self.rho, self.a, 1e300,  # placeholder h; unused
            n, 0, s)

    def _entry_matrix(self, n, y, s, x, t):
        """Return (E, m) with E = exp(rate) UNSHIFTED.

        Continuous limit of (G): the lattice phase chi^j is replaced by
        exp(y (1/P + 1/Q)) with P = p - a, Q = q + a, and gamma by -P/Q
        (report 4.3).  The x/t rates are unchanged: (p+q) and (q^2-p^2).

        The identity part of the matrix does not carry any shift, so the
        exponential is not rescaled; callers keep the region moderate and
        `max_exponent` is available as an overflow guard.
        """
        P = np.array(self.P)[:, None]          # P = p - a
        Q = np.array(self.Q)[None, :]          # Q = q + a
        rho = np.array(self.rho)[:, None]
        gam = (-(P - s) / (Q + s)) ** n
        coef = rho / (P + Q) * gam
        rate = (P + Q) * x + self._trate * t + y * (1.0 / P + 1.0 / Q)
        return coef * np.exp(rate), 0.0

    def max_exponent(self, n, y, s, x, t):
        P = np.array(self.P)[:, None]
        Q = np.array(self.Q)[None, :]
        rate = (P + Q) * x + self._trate * t + y * (1.0 / P + 1.0 / Q)
        return float(rate.max())

    def M(self, n, y, s, x, t):
        E, m = self._entry_matrix(n, y, s, x, t)
        return E + np.eye(self.N)

    def logdet(self, n, y, s, x, t):
        E, _ = self._entry_matrix(n, y, s, x, t)
        M = E + np.eye(self.N)
        return float(np.linalg.slogdet(M)[1])

    def dlog_x(self, n, y, s, x, t):
        E, _ = self._entry_matrix(n, y, s, x, t)
        M = E + np.eye(self.N)
        iM = np.linalg.inv(M)
        pq = np.array(self.P)[:, None] + np.array(self.Q)[None, :]   # = p + q
        return float(np.trace(iM @ (E * pq)))

    def dlog_y(self, n, y, s, x, t):
        E, _ = self._entry_matrix(n, y, s, x, t)
        M = E + np.eye(self.N)
        iM = np.linalg.inv(M)
        P = np.array(self.P)[:, None]
        Q = np.array(self.Q)[None, :]
        rate_y = 1.0 / P + 1.0 / Q
        return float(np.trace(iM @ (E * rate_y)))

    def dlog_xy(self, n, y, s, x, t):
        """d_y d_x log det M  (mixed; both rates are exact)."""
        E, _ = self._entry_matrix(n, y, s, x, t)
        M = E + np.eye(self.N)
        iM = np.linalg.inv(M)
        P = np.array(self.P)[:, None]
        Q = np.array(self.Q)[None, :]
        pq = P + Q
        rate_y = 1.0 / P + 1.0 / Q
        A = E * pq
        B = E * rate_y
        AB = E * pq * rate_y
        return float(np.trace(iM @ AB) - np.trace((iM @ A) @ (iM @ B)))

    # f = tau_1(y; s=0) -> continuous gamma = -P/Q  (report 4.3)
    def f(self, y, x, t):
        return self.logdet(1, y, 0.0, x, t)

    def g(self, y, x, t):
        return self.logdet(0, y, 0.0, x, t)

    # u^0 = 2 (log f/g)_x ;  v^0 = 2 (log f g)_{xy}
    def u0(self, y, x, t):
        return 2.0 * (self.dlog_x(1, y, 0.0, x, t) - self.dlog_x(0, y, 0.0, x, t))

    def v0(self, y, x, t):
        return 2.0 * (self.dlog_xy(1, y, 0.0, x, t) + self.dlog_xy(0, y, 0.0, x, t))

    # ---- vectorised in x (for grid-based experiments such as E7) ----------
    def _vec_entry(self, n, y, s, xv, t):
        """Entry matrices for an ARRAY of x.  Returns E with shape (N,N,len(xv))."""
        P = np.array(self.P)[:, None, None]
        Q = np.array(self.Q)[None, :, None]
        rho = np.array(self.rho)[:, None, None]
        xv = np.asarray(xv, dtype=float)[None, None, :]
        gam = (-(P - s) / (Q + s)) ** n
        coef = rho / (P + Q) * gam
        rate = (P + Q) * xv + self._trate[:, :, None] * t + y * (1.0 / P + 1.0 / Q)
        return coef * np.exp(rate)

    def _vec_dlog_x(self, n, y, s, xv, t):
        E = self._vec_entry(n, y, s, xv, t)
        Nb = E.shape[0]
        M = E + np.eye(Nb)[:, :, None]
        iM = np.linalg.inv(np.moveaxis(M, 2, 0))          # (nx,N,N)
        pq = (np.array(self.P)[:, None] + np.array(self.Q)[None, :])
        A = np.moveaxis(E * pq[:, :, None], 2, 0)
        return np.trace(iM @ A, axis1=1, axis2=2)

    def _vec_dlog_xy(self, n, y, s, xv, t):
        E = self._vec_entry(n, y, s, xv, t)
        Nb = E.shape[0]
        M = E + np.eye(Nb)[:, :, None]
        iM = np.linalg.inv(np.moveaxis(M, 2, 0))
        P = np.array(self.P)[:, None, None]
        Q = np.array(self.Q)[None, :, None]
        pq = P + Q
        ry = 1.0 / P + 1.0 / Q
        A = np.moveaxis(E * pq, 2, 0)
        B = np.moveaxis(E * ry, 2, 0)
        AB = np.moveaxis(E * pq * ry, 2, 0)
        t1 = np.trace(iM @ AB, axis1=1, axis2=2)
        t2 = np.trace((iM @ A) @ (iM @ B), axis1=1, axis2=2)
        return t1 - t2

    def u0_row(self, y, xv, t):
        """u^0 on an array of x (continuous reference)."""
        return 2.0 * (self._vec_dlog_x(1, y, 0.0, xv, t)
                      - self._vec_dlog_x(0, y, 0.0, xv, t))

    def v0_row(self, y, xv, t):
        """v^0 on an array of x (continuous reference)."""
        return 2.0 * (self._vec_dlog_xy(1, y, 0.0, xv, t)
                      + self._vec_dlog_xy(0, y, 0.0, xv, t))
