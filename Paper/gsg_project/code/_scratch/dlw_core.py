"""
Shared symbolic core for the GSG-style semi-discretization of the DLW bilinear system.

Sources
-------
[SY]  H.-H. Sheng, G.-F. Yu, "Solitons, breathers and rational solutions for a
      (2+1)-dimensional dispersive long wave system", Physica D 432 (2022) 133140.
      Bilinear system (lambda = -2 throughout):
          (7)  B f.g = 0,                B = D_x^2 + D_t + 2a D_x
          (6)  [ D_y B + 2 lam D_x ] f.g = 0
      Gram tau:  m_ij^(n) = c_j d_ij + 1/(p_i+q_j) * (-P_i/Q_j)^n * exp(xi_i+eta_j)
          P_i = p_i - a,  Q_j = q_j + a
          xi_i = p_i x - p_i^2 t + y/P_i + xi_i0
          eta_j = q_j x + q_j^2 t + y/Q_j + eta_j0
          f = tau_{n+1}, g = tau_n
      Dependent variable transformation (5):
          u = 2 (ln(f/g))_x ,   v = 2 (ln f g)_{xy}

[GSG] B.-F. Feng, H.-H. Sheng, G.-F. Yu, "Integrable semi-discretizations and
      self-adaptive moving mesh method for a generalized sine-Gordon equation",
      Numerical Algorithms 94 (2023) 351-370.
      The discretization device used here:
        (i)   replace the continuous plane wave e^{p z} of the tau function by the
              DISCRETE exponential (1 - h p)^{-k} in the new lattice index k,
              equivalently:  e^{z/c} -> (1 - h/c)^{-k};
        (ii)  the lattice therefore acts on the tau as a RANK-ONE (row x column)
              scaling, which shifts the effective spectral parameters by h;
        (iii) the derivative in the *other* variable is kept continuous, giving a
              TWO-SITE bilinear relation (Backlund/lattice form) at each site;
        (iv)  the physical coordinate is reconstructed by a discrete hodograph
              transformation (moving mesh).
"""
import sympy as sp

# ---------------------------------------------------------------- symbols
x, t, y, h, a, lam = sp.symbols('x t y h a lam', real=True)
n = sp.symbols('n', integer=True)          # mKP hierarchy index (0 -> g, 1 -> f)
j = sp.symbols('j', integer=True)          # y-lattice index


def P_of(p):
    return p - a


def Q_of(q):
    return q + a


# ---------------------------------------------------------------- bilinear ops
def Dx(F, G, v='x'):
    return sp.diff(F, v) * G - F * sp.diff(G, v)


def Dx2(F, G):
    return sp.diff(F, x, 2) * G - 2 * sp.diff(F, x) * sp.diff(G, x) + F * sp.diff(G, x, 2)


def Bop(F, G, aa=None):
    """B f.g = (D_x^2 + D_t + 2a D_x) f.g .  `aa` overrides the parameter a."""
    if aa is None:
        aa = a
    return Dx2(F, G) + Dx(F, G, 't') + 2 * aa * Dx(F, G)


# ---------------------------------------------------------------- continuous tau
def gram_tau(N, nval, cvals=None, pvals=None, qvals=None, xivals=None, etavals=None,
             aa=None, hh=None, lat=None, disc=False):
    """
    Return (tau, info) where tau = det(M) for the DLW Gram matrix.

    disc=False : continuous tau, m_ij = c_j d_ij + 1/(p_i+q_j)(-P_i/Q_j)^n e^{xi_i+eta_j}
    disc=True  : GSG-style y-lattice tau, the y-exponentials replaced by the
                 discrete exponentials (1-h/P_i)^{-j}, (1-h/Q_j)^{-j}
    """
    if aa is None:
        aa = a
    if pvals is None:
        pvals = [sp.Symbol(f'p{i+1}') for i in range(N)]
    if qvals is None:
        qvals = [sp.Symbol(f'q{i+1}') for i in range(N)]
    if cvals is None:
        cvals = [1] * N
    if xivals is None:
        xivals = [sp.Symbol(f'xi{i+1}0') for i in range(N)]
    if etavals is None:
        etavals = [sp.Symbol(f'eta{i+1}0') for i in range(N)]

    rows = []
    for i in range(N):
        row = []
        for k in range(N):
            Pi, Qk = pvals[i] - aa, qvals[k] + aa
            xi = pvals[i] * x - pvals[i] ** 2 * t + xivals[i]
            et = qvals[k] * x + qvals[k] ** 2 * t + etavals[k]
            if disc:
                # y -> lattice index j ;  e^{y/P} -> (1 - h/P)^{-j}
                xi = xi + sp.log(1 - hh / Pi) * (-j)
                et = et + sp.log(1 - hh / Qk) * (-j)
            else:
                xi = xi + y / Pi
                et = et + y / Qk
            e = sp.exp(xi + et)
            entry = cvals[k] * sp.KroneckerDelta(0) if False else None
            m = (-Pi / Qk) ** nval * e / (pvals[i] + qvals[k])
            row.append((cvals[k] if i == k else 0, m))
        rows.append(row)
    M = sp.Matrix(N, N, lambda i, k: rows[i][k][0] + rows[i][k][1])
    return sp.expand(M.det()), dict(p=pvals, q=qvals, c=cvals, M=M)
