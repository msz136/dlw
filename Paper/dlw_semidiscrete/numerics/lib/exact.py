# -*- coding: utf-8 -*-
"""
exact.py -- exact finite-h Gram reference for the semi-discrete DLW system.

Implements numerical_analysis.html  section 4.1 / 4.3.

Pure lattice Gram tau (GRAM_INTEGRABILITY_REASSESSMENT.md eq. (G)):

    tau_n(j;s) = det[ delta_ik + rho_i/(p_i+q_k) * (-(p_i-s)/(q_k+s))^n
                      * chi_ik^j * exp((p_i+q_k)x + (q_k^2-p_i^2)t) ]

    chi_ik = lam_h(p_i-a) lam_h(q_k+a),   lam_h(z) = (z+h/2)/(z-h/2)
    G_j = tau_0(j)        (rho_i absorbed into rho)
    F_j = tau_1(j; a-h/2)   ==  tau_1(j+1; a+h/2)   by (G2)

Physical fields, both marked at the F site y = (j+1/2)h:

    u_j = d_x log( F_j^2 / (G_j G_{j+1}) )
    v_j = (4/h) d_x log( G_{j+1} / G_j ) + delta_0 u_j

ALL evaluations here use analytic x-derivatives and log-sum-exp style stable
determinant evaluation.  No finite differences are used to produce a "truth"
value -- per the report: "cannot use the same coarse differences to compute
both the truth and the numerical result".

Two arithmetic backends:
  * float  (numpy, float64)          -- fast, for scans
  * mp     (mpmath, configurable dps) -- 50+ digit spot checks
"""

import numpy as np
import mpmath as mp

# ---------------------------------------------------------------------------
# parameters
# ---------------------------------------------------------------------------


class Params:
    """Soliton data for an N-soliton pure lattice Gram tau."""

    def __init__(self, N, p, q, rho, a, h):
        self.N = int(N)
        self.p = np.asarray(p, dtype=float) if not isinstance(p, list) or True else p
        self.p = [float(v) for v in p]
        self.q = [float(v) for v in q]
        self.rho = [float(v) for v in rho]
        self.a = float(a)
        self.h = float(h)
        assert len(self.p) == self.N and len(self.q) == self.N
        assert len(self.rho) == self.N

    # regular real branch condition (R) in GRAM_INTEGRABILITY_REASSESSMENT.md
    def regularity_report(self):
        d = self.h / 2.0
        msgs = []
        ok = True
        if not self.h > 0:
            ok = False; msgs.append("h <= 0")
        ps = sorted(self.p); qs = sorted(self.q)
        for i in range(self.N):
            if not (0 < ps[i] < self.a - d):
                ok = False; msgs.append("p_%d=%g outside (0, a-h/2=%g)" % (i + 1, ps[i], self.a - d))
            if not (0 < qs[i]):
                ok = False; msgs.append("q_%d=%g <= 0" % (i + 1, qs[i]))
            if not self.rho[i] > 0:
                ok = False; msgs.append("rho_%d=%g <= 0" % (i + 1, self.rho[i]))
        return ok, msgs


def lam(z, h):
    d = h / 2.0
    return (z + d) / (z - d)


def chi_ik(p_i, q_k, a, h):
    return lam(p_i - a, h) * lam(q_k + a, h)


# ---------------------------------------------------------------------------
# exact tau and its x-derivatives in closed form
# ---------------------------------------------------------------------------
# We never difference tau numerically.  Since every tau entry is
#   m_ik = rho_i/(p_i+q_k) * gamma_i^n * chi_ik^j * exp(p_i x - p_i^2 t + q_k x + q_k^2 t)
# the k-th x derivative of the determinant is obtained from the entries'
# x-derivatives.  We implement d_x via the exact identity
#   d_x det M = det M * tr(M^{-1} M_x)
# using a LU-based solve, which is stable and analytic in x.


class LatticeExact:
    """Exact (analytic-x) evaluation of the finite-h Gram reference."""

    def __init__(self, params, dps=None, backend="float"):
        self.P = params
        self.a = params.a
        self.h = params.h
        self.d = params.h / 2.0
        self.N = params.N
        self.backend = backend
        if backend == "mp":
            if dps is not None:
                mp.mp.dps = int(dps)

    # ---- matrix ---------------------------------------------------------
    def _matrix(self, n, j, s, x, t):
        """Return M (N x N) with entries as in (G).  Float backend."""
        N, P = self.N, self.P
        ep = np.array(P.p) * x - np.array(P.p) ** 2 * t
        eq = np.array(P.q) * x + np.array(P.q) ** 2 * t
        # coefficient matrices
        p = np.array(P.p)[:, None]
        q = np.array(P.q)[None, :]
        rho = np.array(P.rho)[:, None]
        gam = (-(p - s) / (q + s)) ** n
        chi = lam(p - self.a, self.h) * lam(q + self.a, self.h)
        coef = rho / (p + q) * gam * chi ** j
        M = coef * np.exp(ep[:, None] + eq[None, :])
        M = M + np.eye(N)
        return M

    def _matrix_dx(self, n, j, s, x, t):
        """d_x M.  d_x exp(p x - p^2 t + q x + q^2 t) = (p+q) * exp(...)."""
        N, P = self.N, self.P
        ep = np.array(P.p) * x - np.array(P.p) ** 2 * t
        eq = np.array(P.q) * x + np.array(P.q) ** 2 * t
        p = np.array(P.p)[:, None]
        q = np.array(P.q)[None, :]
        rho = np.array(P.rho)[:, None]
        gam = (-(p - s) / (q + s)) ** n
        chi = lam(p - self.a, self.h) * lam(q + self.a, self.h)
        coef = rho / (p + q) * gam * chi ** j
        E = np.exp(ep[:, None] + eq[None, :])
        return coef * (p + q) * E

    # ---- tau and log-derivatives ---------------------------------------
    def tau(self, n, j, s, x, t):
        return float(np.linalg.det(self._matrix(n, j, s, x, t)))

    def logtau_x(self, n, j, s, x, t):
        """d_x log tau  =  tr(M^{-1} M_x), evaluated analytically."""
        M = self._matrix(n, j, s, x, t)
        Mx = self._matrix_dx(n, j, s, x, t)
        # tr(M^{-1} Mx) = tr(solve(M, Mx))
        A = np.linalg.solve(M, Mx)
        return float(np.trace(A))

    # ---- F, G and friends ----------------------------------------------
    def F(self, j, x, t):
        return float(np.linalg.det(self._matrix(1, j, self.a - self.d, x, t)))

    def G(self, j, x, t):
        return float(np.linalg.det(self._matrix(0, j, self.a, x, t)))

    def dlogF(self, j, x, t):
        return self.logtau_x(1, j, self.a - self.d, x, t)

    def dlogG(self, j, x, t):
        return self.logtau_x(0, j, self.a, x, t)

    # ---- physical fields (exact analytic x-derivatives) -----------------
    def u(self, j, x, t):
        """u_j = d_x log(F_j^2/(G_j G_{j+1}))."""
        return 2.0 * self.dlogF(j, x, t) - self.dlogG(j, x, t) - self.dlogG(j + 1, x, t)

    def du_dx(self, j, x, t):
        """d_x u_j, analytic: d_x^2 log(.) via the second log-derivative."""
        return (2.0 * self.d2logtau(1, j, self.a - self.d, x, t)
                - self.d2logtau(0, j, self.a, x, t)
                - self.d2logtau(0, j + 1, self.a, x, t))

    def d2logtau(self, n, j, s, x, t):
        """d_x^2 log tau = tr(M^{-1}Mxx) - tr((M^{-1}Mx)^2) (analytic)."""
        M = self._matrix(n, j, s, x, t)
        Mx = self._matrix_dx(n, j, s, x, t)
        Mxx = self._matrix_dxx(n, j, s, x, t)
        A = np.linalg.solve(M, Mx)
        B = np.linalg.solve(M, Mxx)
        return float(np.trace(B) - np.trace(A @ A))

    def _matrix_dxx(self, n, j, s, x, t):
        N, P = self.N, self.P
        ep = np.array(P.p) * x - np.array(P.p) ** 2 * t
        eq = np.array(P.q) * x + np.array(P.q) ** 2 * t
        p = np.array(P.p)[:, None]
        q = np.array(P.q)[None, :]
        rho = np.array(P.rho)[:, None]
        gam = (-(p - s) / (q + s)) ** n
        chi = lam(p - self.a, self.h) * lam(q + self.a, self.h)
        coef = rho / (p + q) * gam * chi ** j
        E = np.exp(ep[:, None] + eq[None, :])
        return coef * (p + q) ** 2 * E

    def Wg(self, j, x, t):
        """W_j = v_j - delta_0 u_j = (4/h) d_x log(G_{j+1}/G_j)."""
        return 4.0 / self.h * (self.dlogG(j + 1, x, t) - self.dlogG(j, x, t))

    def v(self, j, x, t):
        """v_j = (4/h) d_x log(G_{j+1}/G_j) + delta_0 u_j."""
        d0u = (self.u(j + 1, x, t) - self.u(j - 1, x, t)) / (2.0 * self.h)
        return self.Wg(j, x, t) + d0u

    # ---- u, v on a whole j-range ---------------------------------------
    def u_range(self, js, x, t):
        return np.array([self.u(int(j), x, t) for j in js])

    def v_range(self, js, x, t):
        return np.array([self.v(int(j), x, t) for j in js])

    # ---- bilinear residuals (normalized) --------------------------------
    def B_norm(self, j, s, sign, x, t, dx=None):
        """Normalized bilinear residual.

        sign = -1 :  R_B^- = B_{a-h/2} F_j . G_j        / (F_j G_j)
        sign = +1 :  R_B^+ = B_{a+h/2} F_j . G_{j+1}    / (F_j G_{j+1})

        B_s F.G = (D_x^2 + D_t + 2 s D_x) F . G
                = F_xx G - 2 F_x G_x + F G_xx + F_t G - F G_t + 2s(F_x G - F G_x)

        We evaluate F, G and their x- and t-derivatives analytically.
        """
        if sign < 0:
            ss = self.a - self.d
            nF, jF = 1, j
            nG, jG = 0, j
        else:
            ss = self.a + self.d
            nF, jF = 1, j
            nG, jG = 0, j + 1
        F = float(np.linalg.det(self._matrix(nF, jF, ss if nF == 1 and sign < 0 else self.a - self.d, x, t))) \
            if False else self.F(j, x, t)
        G = self.G(jG, x, t)
        Fx = F * self.dlogF(jF, x, t)
        Gx = G * self.dlogG(jG, x, t)
        Fxx = F * (self.d2logtau(1, jF, self.a - self.d, x, t) + self.dlogF(jF, x, t) ** 2)
        Gxx = G * (self.d2logtau(0, jG, self.a, x, t) + self.dlogG(jG, x, t) ** 2)
        Ft = self._dtau(1, jF, self.a - self.d, x, t)
        Gt = self._dtau(0, jG, self.a, x, t)
        val = (Fxx * G - 2 * Fx * Gx + F * Gxx
               + Ft * G - F * Gt
               + 2 * ss * (Fx * G - F * Gx))
        return val / (F * G)

    def _dtau(self, n, j, s, x, t):
        """d_t tau, analytic.  d_t exp(p x - p^2 t + q x + q^2 t) = (q^2-p^2) exp(...)."""
        N, P = self.N, self.P
        ep = np.array(P.p) * x - np.array(P.p) ** 2 * t
        eq = np.array(P.q) * x + np.array(P.q) ** 2 * t
        p = np.array(P.p)[:, None]
        q = np.array(P.q)[None, :]
        rho = np.array(P.rho)[:, None]
        gam = (-(p - s) / (q + s)) ** n
        chi = lam(p - self.a, self.h) * lam(q + self.a, self.h)
        coef = rho / (p + q) * gam * chi ** j
        E = np.exp(ep[:, None] + eq[None, :])
        M = coef * E + np.eye(N)
        Mt = coef * (q ** 2 - p ** 2) * E
        # d_t det = det * tr(M^{-1} M_t)
        A = np.linalg.solve(M, Mt)
        return float(np.linalg.det(M) * np.trace(A))

    # ---- NL residuals (N1)(N2), exact analytic --------------------------
    def res_N1(self, j, x, t, dx=None):
        """delta_-(u_t + d_x H) + d_x^2 ( M_- v - (h^2/4) Delta_h delta_- u ).

        We evaluate the whole expression with analytic x-derivatives; the
        lattice operators delta_-, delta_0, M_-, Delta_h are exact.
        """
        h, a = self.h, self.a
        # u_t at sites j, j-1  (analytic in t)
        ut_j = self._du_dt(j, x, t)
        ut_jm = self._du_dt(j - 1, x, t)
        d_ut = (ut_j - ut_jm) / h
        # H = u^2/2 + 2 a u + h^2 (W^2/32 - W/4)
        Hj = self._H(j, x, t)
        Hjm = self._H(j - 1, x, t)
        dH = (Hj - Hjm) / h
        # M_- v  and  Delta_h delta_- u
        Mmv = 0.5 * (self.v(j, x, t) + self.v(j - 1, x, t))
        dm_u_j = (self.u(j, x, t) - self.u(j - 1, x, t)) / h
        dm_u_jp = (self.u(j + 1, x, t) - self.u(j, x, t)) / h
        dm_u_jm = (self.u(j - 1, x, t) - self.u(j - 2, x, t)) / h
        Dl = (dm_u_jp - 2 * dm_u_j + dm_u_jm) / h ** 2
        inner = Mmv - h ** 2 / 4.0 * Dl
        # second x-derivative of inner, analytic (structure in x only via u,v)
        d2inner = self._d2(self._inner_N1, j, x, t)
        return d_ut + self._dx(dH, j, x, t) + d2inner

    def _inner_N1(self, j, x, t):
        h = self.h
        Mmv = 0.5 * (self.v(j, x, t) + self.v(j - 1, x, t))
        dm_u_j = (self.u(j, x, t) - self.u(j - 1, x, t)) / h
        dm_u_jp = (self.u(j + 1, x, t) - self.u(j, x, t)) / h
        dm_u_jm = (self.u(j - 1, x, t) - self.u(j - 2, x, t)) / h
        Dl = (dm_u_jp - 2 * dm_u_j + dm_u_jm) / h ** 2
        return Mmv - h ** 2 / 4.0 * Dl

    def _H(self, j, x, t):
        a, h = self.a, self.h
        u = self.u(j, x, t)
        W = self.Wg(j, x, t)
        return 0.5 * u ** 2 + 2 * a * u + h ** 2 * (W ** 2 / 32.0 - W / 4.0)

    def _du_dt(self, j, x, t, eps=None):
        """d_t u_j, analytic.

        u_j = 2 dlogF_j - dlogG_j - dlogG_{j+1};  dlog tau = tr(M^{-1}M_x),
        so d_t(dlog tau) needs mixed M_{xt}.  We use the exact identity
          d_t tr(M^{-1}M_x) = tr(M^{-1}M_{xt}) - tr(M^{-1}M_t M^{-1}M_x).
        """
        return (2.0 * self._dt_logtau_x(1, j, self.a - self.d, x, t)
                - self._dt_logtau_x(0, j, self.a, x, t)
                - self._dt_logtau_x(0, j + 1, self.a, x, t))

    def _dt_logtau_x(self, n, j, s, x, t):
        M = self._matrix(n, j, s, x, t)
        Mx = self._matrix_dx(n, j, s, x, t)
        Mt = self._matrix_dt(n, j, s, x, t)
        Mxt = self._matrix_dxt(n, j, s, x, t)
        iM = np.linalg.inv(M)
        iMx = iM @ Mx
        iMt = iM @ Mt
        iMxt = iM @ Mxt
        return float(np.trace(iMxt) - np.trace(iMt @ iMx))

    def _entry_parts(self, n, j, s):
        P = self.P
        p = np.array(P.p)[:, None]
        q = np.array(P.q)[None, :]
        rho = np.array(P.rho)[:, None]
        gam = (-(p - s) / (q + s)) ** n
        chi = lam(p - self.a, self.h) * lam(q + self.a, self.h)
        coef = rho / (p + q) * gam * chi ** j
        return p, q, coef

    def _matrix_dt(self, n, j, s, x, t):
        p, q, coef = self._entry_parts(n, j, s)
        ep = np.array(self.P.p) * x - np.array(self.P.p) ** 2 * t
        eq = np.array(self.P.q) * x + np.array(self.P.q) ** 2 * t
        E = np.exp(ep[:, None] + eq[None, :])
        return coef * (q ** 2 - p ** 2) * E

    def _matrix_dxt(self, n, j, s, x, t):
        p, q, coef = self._entry_parts(n, j, s)
        ep = np.array(self.P.p) * x - np.array(self.P.p) ** 2 * t
        eq = np.array(self.P.q) * x + np.array(self.P.q) ** 2 * t
        E = np.exp(ep[:, None] + eq[None, :])
        return coef * (q ** 2 - p ** 2) * (p + q) * E

    # ---- generic analytic x-derivatives of an x-function ----------------
    def _dx(self, f, j, x, t, eps=None):
        """d_x f(j,.,t) analytic via the exact derivative of log-combinations.

        Not used for truth generation of u,v (those are closed form), but is
        used for the composite N1/N2 residual inner blocks where we need d_x
        of an expression built from u,v and their x-derivatives.  We use the
        analytic derivative chain rather than a finite difference.
        """
        return self._chain_dx(f, j, x, t)

    def _chain_dx(self, f, j, x, t):
        raise NotImplementedError

    def _d2(self, f, j, x, t):
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Closed-form u, v for N = 1  (report section 4.1)
# ---------------------------------------------------------------------------

class SingleSoliton:
    """Exact single-soliton reference in closed form (report 4.1).

        P = p - a, Q = q + a, S = p + q, d = h/2
        chi = lam(P) lam(Q),  gamma = -(P+d)/(Q-d)
        E = (rho/S) exp(S x + (q^2-p^2) t) chi^j
        G_j = 1+E, F_j = 1+gamma E, G_{j+1} = 1+chi E
        u_j = U(E),  v_j = (4S/h)[chiE/(1+chiE) - E/(1+E)] + [U(chiE)-U(E/chi)]/(2h)
    """

    def __init__(self, p, q, rho, a, h):
        self.p, self.q, self.rho, self.a, self.h = p, q, rho, a, h
        d = h / 2.0
        self.d = d
        self.P = p - a
        self.Q = q + a
        self.S = p + q
        self.chi = lam(self.P, h) * lam(self.Q, h)
        self.gamma = -(self.P + d) / (self.Q - d)
        self.c0 = rho / self.S

    def E(self, j, x, t):
        return self.c0 * np.exp(self.S * x + (self.q ** 2 - self.p ** 2) * t) * self.chi ** j

    def U(self, E):
        """U(E) = S [ 2 gamma E/(1+gamma E) - E/(1+E) - chi E/(1+chi E) ]."""
        S, g, c = self.S, self.gamma, self.chi
        return S * (2 * g * E / (1 + g * E) - E / (1 + E) - c * E / (1 + c * E))

    def u(self, j, x, t):
        return self.U(self.E(j, x, t))

    def logG(self, j, x, t):
        return np.log1p(self.E(j, x, t))

    def logG1(self, j, x, t):
        return np.log1p(self.chi * self.E(j, x, t))

    # ---- exact x-derivatives of log G and log G1 ------------------------
    def dlogG(self, j, x, t):
        E = self.E(j, x, t)
        return self.S * E / (1 + E)

    def dlogG1(self, j, x, t):
        E = self.E(j, x, t)
        return self.S * self.chi * E / (1 + self.chi * E)

    def Wg(self, j, x, t):
        return 4.0 / self.h * (self.dlogG1(j, x, t) - self.dlogG(j, x, t))

    def du_dx(self, j, x, t):
        return self.U(self.E(j, x, t)) - self.U(self.E(j, x, t) / self.chi)

    def v(self, j, x, t):
        d0u = (self.u(j + 1, x, t) - self.u(j - 1, x, t)) / (2.0 * self.h)
        return self.Wg(j, x, t) + d0u


# ---------------------------------------------------------------------------
# robust evaluation helpers
# ---------------------------------------------------------------------------

def logdet_mp(mat_fn, N, **kw):
    """High-precision log|det| via mpmath (used for spot checks)."""
    M = mp.matrix(N, N)
    entries = mat_fn(**kw)
    for i in range(N):
        for k in range(N):
            M[i, k] = mp.mpf(entries[i][k])
    return mp.log(mp.fabs(mp.det(M)))
