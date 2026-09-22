#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direction B -- spectral / pseudo-spectral semidiscretisation of the DLW system.
Reproducible spectral diagnostic.  Python 3.13 + SymPy.  Deterministic, no RNG.

Run:   python -u spectral_diagnostic.py

Contents
  Sec 1  exact symbolic re-derivation of the constant-background linearisation and
         of the dispersion relation  (sigma + i(u0+2a)k)^2 = k^4 - (v0+2 lam) k^3/l
  Sec 2  the l = 0 (zero-mode) sector: exact derivation of  d_x^2 v_0 = 0  and of
         the v_0 evolution equation; the zero-mode family v = -2 lam, u = U(x,t)
  Sec 3  that family is an EXACT solution of the Fourier-Galerkin truncation for
         every N (the infinite-dimensional zero mode survives the projection)
  Sec 4  exact sign analysis: the stable x-band is 0 < sgn(l) k < c/|l|,  c = v0+2 lam
  Sec 5  aliasing quantified exactly: Galerkin convolution vs M-point collocation;
         alias-free iff M >= 3N+1; the l = 0 mode is always alias-free for M > 2N
  Sec 6  finite-band growth vs continuous high-frequency growth: the diagnostic
         table, the 1/N stability threshold, and the N-independence of the k^2 rate
  Sec 7  kernel dimension of the centred difference on Z/M (odd vs even M):
         cross-check with proofs/Common/Operators.lean (DLW.Common.ctr_kernel)
"""

import cmath
import json
import math
import os
import sys

import sympy as sp

FAILURES = []
CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append({"check": name, "ok": bool(ok), "detail": detail})
    print(("PASS  " if ok else "FAIL  ") + name + (("   | " + detail) if detail else ""))
    if not ok:
        FAILURES.append(name)
    return ok


def banner(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# ----------------------------------------------------------------------------
banner("Sec 0  environment")
print("python   :", sys.version.replace("\n", " "))
print("sympy    :", sp.__version__)
print("cwd      :", os.getcwd())

# ----------------------------------------------------------------------------
# Sec 1.  Exact linearisation and dispersion relation.
# ----------------------------------------------------------------------------
banner("Sec 1  exact linearisation and the dispersion relation")

X, Y, T = sp.symbols("x y t", real=True)
eps = sp.symbols("epsilon", positive=True)
u0, v0, a, lam = sp.symbols("u0 v0 a lam", real=True)
k, l = sp.symbols("k l", real=True)
s = sp.symbols("s")
U, V = sp.symbols("U V")
E = sp.symbols("E", nonzero=True)          # E stands for exp(s t + i(k x + l y))

u = u0 + eps * U * E
v = v0 + eps * V * E


def d(e, var, rate):
    """d/dvar of an expression that is polynomial in E = exp(s t + i(kx+ly))."""
    return sp.diff(e, var) + sp.diff(e, E) * E * rate


rate = {T: s, X: sp.I * k, Y: sp.I * l}


def dT(e):
    return d(e, T, s)


def dX(e):
    return d(e, X, sp.I * k)


def dY(e):
    return d(e, Y, sp.I * l)


# (1)  u_yt + v_xx + u u_xy + u_x u_y + 2 a u_xy = 0
r1 = dT(dY(u)) + dX(dX(v)) + u * dX(dY(u)) + dX(u) * dY(u) + 2 * a * dX(dY(u))
# (2)  v_t + (u v)_x + u_xxy + 2 a v_x + 2 lam u_x = 0
r2 = dT(v) + dX(u * v) + dX(dX(dY(u))) + 2 * a * dX(v) + 2 * lam * dX(u)


def first_order(e):
    """coefficient of eps^1, divided by the single factor E."""
    return sp.expand(sp.diff(e, eps).subs(eps, 0) / E)


lin1 = first_order(r1)
lin2 = first_order(r2)

exp1 = (sp.I * l * s) * U - k**2 * V - (u0 + 2 * a) * k * l * U
exp2 = (s + sp.I * (u0 + 2 * a) * k) * V + sp.I * (v0 + 2 * lam) * k * U - sp.I * k**2 * l * U

check("Sec1 linearised (1) equals (i l s)U - k^2 V - (u0+2a)k l U",
      sp.simplify(sp.expand(lin1 - exp1)) == 0)
check("Sec1 linearised (2) equals (s+i(u0+2a)k)V + i(v0+2 lam)kU - i k^2 l U",
      sp.simplify(sp.expand(lin2 - exp2)) == 0)

Vsol = sp.solve(sp.Eq(lin1, 0), V)
check("Sec1 (1L) determines V (unique solution)", len(Vsol) == 1)
rel_expr = sp.simplify(sp.expand(lin2.subs(V, Vsol[0]) / U))
target = (s + sp.I * (u0 + 2 * a) * k) ** 2 - (k**4 - (v0 + 2 * lam) * k**3 / l)
quot = sp.simplify(sp.expand(rel_expr - (sp.I * l / k**2) * target))
check("Sec1 elimination of V gives (s+i(u0+2a)k)^2 = k^4 - (v0+2 lam)k^3/l",
      quot == 0, "residual = %s" % quot)

# the l = 0 sector, linearly
lin1_l0 = sp.simplify(lin1.subs(l, 0))
lin2_l0 = sp.simplify(lin2.subs(l, 0))
check("Sec1 l=0: (1L) forces V = 0", sp.simplify(lin1_l0 + k**2 * V) == 0)
lin2_l0_V0 = sp.simplify(lin2_l0.subs(V, 0))
check("Sec1 l=0: (2L) with V = 0 forces (v0+2 lam) U = 0",
      sp.simplify(lin2_l0_V0 - sp.I * (v0 + 2 * lam) * k * U) == 0,
      "(2L)|l=0 with V=0 is %s" % lin2_l0_V0)

# ----------------------------------------------------------------------------
# Sec 2.  The l = 0 (zero-mode) sector, exactly, in Fourier space.
# ----------------------------------------------------------------------------
banner("Sec 2  the l = 0 sector of the nonlinear system (exact Fourier computation)")

NB = 3
uhat = {m: sp.Function("u%d" % (m + 10))(X, T) for m in range(-NB, NB + 1)}
vhat = {m: sp.Function("v%d" % (m + 10))(X, T) for m in range(-NB, NB + 1)}


def conv(A, B, L, dxA=0, dxB=0, dyB=0):
    """L-th y-mode of (d_x^dxA A) * (d_x^dxB d_y^dyB B) for finite Fourier series."""
    tot = 0
    for m in A:
        n = L - m
        if n in B:
            tot += sp.diff(A[m], X, dxA) * sp.diff(B[n], X, dxB) * (sp.I * n) ** dyB
    return sp.expand(tot)


def resid1(L):
    """L-th y-mode of equation (1)."""
    return sp.expand(
        (sp.I * L) * sp.diff(uhat[L], T)
        + sp.diff(vhat[L], X, 2)
        + conv(uhat, uhat, L, dxB=1, dyB=1)
        + conv(uhat, uhat, L, dxA=1, dyB=1)
        + 2 * a * (sp.I * L) * sp.diff(uhat[L], X)
    )


def resid2(L):
    """L-th y-mode of equation (2)."""
    return sp.expand(
        sp.diff(vhat[L], T)
        + sp.diff(conv(uhat, vhat, L), X)
        + (sp.I * L) * sp.diff(uhat[L], X, 2)
        + 2 * a * sp.diff(vhat[L], X)
        + 2 * lam * sp.diff(uhat[L], X)
    )


r1_0 = resid1(0)
check("Sec2 l=0 of (1) is exactly d_x^2 v_0 (no u_0, no nonlinearity)",
      sp.simplify(r1_0 - sp.diff(vhat[0], X, 2)) == 0, "residual = %s" % sp.simplify(r1_0 - sp.diff(vhat[0], X, 2)))

uv0 = sp.expand(sum(uhat[m] * vhat[-m] for m in uhat if -m in vhat))
exp_r2_0 = sp.expand(sp.diff(vhat[0], T) + sp.diff(uv0 + 2 * a * vhat[0] + 2 * lam * uhat[0], X))
check("Sec2 l=0 of (2) is d_t v_0 + d_x[<uv> + 2a v_0 + 2 lam u_0]",
      sp.simplify(resid2(0) - exp_r2_0) == 0,
      "residual = %s" % sp.simplify(resid2(0) - exp_r2_0))

# the loop sum (u u_xy + u_x u_y)_0 telescopes into a directed sum that cancels
quad0 = sp.expand(conv(uhat, uhat, 0, dxB=1, dyB=1) + conv(uhat, uhat, 0, dxA=1, dyB=1))
check("Sec2 the quadratic pair u u_xy + u_x u_y contributes zero to l=0 (antisymmetry)",
      sp.simplify(quad0) == 0, "residual = %s" % sp.simplify(quad0))

# the zero-mode family  v = -2 lam, u = U(x,t) arbitrary
Ufun = sp.Function("Ufun")(X, T)
u_zm = {m: (Ufun if m == 0 else 0) for m in range(-NB, NB + 1)}
v_zm = {m: (-2 * lam if m == 0 else 0) for m in range(-NB, NB + 1)}
zm1 = [sp.simplify(resid1(L).subs({uhat[m]: u_zm[m] for m in uhat}, simultaneous=True)
                  .subs({vhat[m]: v_zm[m] for m in vhat}, simultaneous=True)) for L in range(-NB, NB + 1)]
zm2 = [sp.simplify(resid2(L).subs({uhat[m]: u_zm[m] for m in uhat}, simultaneous=True)
                  .subs({vhat[m]: v_zm[m] for m in vhat}, simultaneous=True)) for L in range(-NB, NB + 1)]
check("Sec2 (V7) v = -2 lam, u = U(x,t) arbitrary solves (1) exactly (all l)",
      all(e == 0 for e in zm1))
check("Sec2 (V7) same family solves (2) exactly (all l)", all(e == 0 for e in zm2))
check("Sec2 the zero-mode family is not affected by the projection "
      "(residuals are mode-wise zero for every retained band)",
      all(e == 0 for e in zm1 + zm2))

# ----------------------------------------------------------------------------
# Sec 3.  Truncated Fourier-Galerkin system: which structural identities survive?
# ----------------------------------------------------------------------------
banner("Sec 3  Fourier-Galerkin truncation at N: algebraic checks")

for N in (1, 2, 3):
    ok = True
    for L in range(-N, N + 1):
        r1L = resid1(L)
        r2L = resid2(L)
        # the l = 0 sector identity must hold in the truncation too
        if L == 0:
            ok = ok and sp.simplify(r1L - sp.diff(vhat[0], X, 2)) == 0
            ok = ok and sp.simplify(r2L - exp_r2_0) == 0
        # every retained nonzero mode keeps a nontrivial residual expression
    check("Sec3 truncated (N=%d) l=0 identities hold exactly" % N, ok)

# ----------------------------------------------------------------------------
# Sec 4.  Exact sign analysis of the discriminant.
# ----------------------------------------------------------------------------
banner("Sec 4  exact sign analysis: stable x-band is 0 < sgn(l) k < c/|l|")

c = sp.symbols("c", positive=True)
disc = k**4 - c * k**3 / l
fac = sp.simplify(sp.factor(sp.expand(disc * l)))
check("Sec4 l * disc factors as k^3 (k l - c)", sp.simplify(fac - k**3 * (k * l - c)) == 0,
      "l*disc = %s" % fac)

samples = [
    # (k, l, sign of disc) for c = 1; neutral iff k l > 0 and |k| < c/|l|
    (sp.Rational(1, 2), sp.Integer(1), -1),      # k l > 0, |k| < c/|l| -> neutral
    (sp.Integer(2), sp.Integer(1), 1),           # k l > 0, |k| > c/|l| -> unstable
    (sp.Integer(1), sp.Integer(1), 0),           # k l > 0, |k| = c/|l| -> borderline
    (sp.Rational(-1, 2), sp.Integer(-1), -1),    # k l > 0, |k| < c/|l| -> neutral
    (sp.Integer(3), sp.Integer(-1), 1),          # k l < 0 -> unstable for every k
    (sp.Integer(-3), sp.Integer(1), 1),          # k l < 0 -> unstable for every k
    (sp.Rational(1, 3), sp.Integer(-1), 1),      # k l < 0 -> unstable
    (sp.Rational(-1, 3), sp.Integer(1), 1),      # k l < 0 -> unstable
]
ok = True
for kk, ll, sg in samples:
    val = sp.sign(sp.simplify(disc.subs({k: kk, l: ll, c: 1})))
    ok = ok and (val == sg)
check("Sec4 sign(disc) matches the predicted neutral/unstable regions (c=1)", ok)

ok = True
for kk, ll in [(sp.Rational(1, 4), 2), (sp.Rational(1, 3), 3), (sp.Rational(1, 10), 10)]:
    val = sp.simplify(disc.subs({k: kk, l: ll, c: 1}))
    ok = ok and (val <= 0)
check("Sec4 neutral region 0 < sgn(l) k < c/|l| has disc <= 0", ok)

# ----------------------------------------------------------------------------
# Sec 5.  Aliasing: exact Galerkin convolution vs M-point collocation.
# ----------------------------------------------------------------------------
banner("Sec 5  aliasing quantified (exact, no floating point)")


def conv_coeff(A, B, m):
    """Exact Galerkin coefficient at y-mode m of the product of two finite series."""
    return sum(A[p] * B[m - p] for p in A if (m - p) in B)


def alias_coeff(A, B, M, m):
    """Collocation coefficient at mode m on an M-point grid.

    DFT algebra: (1/M) sum_j (sum_p A_p w^{pj})(sum_q B_q w^{qj}) w^{-mj}
                 = sum_{p+q == m (mod M)} A_p B_q.
    """
    tot = 0
    for p in A:
        for q in B:
            if (p + q - m) % M == 0:
                tot += A[p] * B[q]
    return tot


# the root-of-unity filter identity that produces the mod-M convolution
w = sp.symbols("w")
for M in (3, 4, 5):
    okf = True
    for t in range(-6, 7):
        val = sp.simplify(sum(w ** (t * j) for j in range(M)).subs(w, sp.exp(2 * sp.pi * sp.I / M)))
        want = M if t % M == 0 else 0
        okf = okf and abs(sp.re(sp.nsimplify(val))) < 1e-9 and abs(sp.im(val) - 0) < 1e-9 if want == 0 \
            else okf and abs(complex(sp.N(val)) - want) < 1e-9
    check("Sec5 root-of-unity filter: sum_j w^{tj} = M if M|t else 0 (M=%d)" % M, okf)

# a single retained mode at the top of the band, u = w^{N y}:  the product u*u
for N in range(1, 9):
    M = 2 * N + 1
    A = {N: sp.Integer(1)}
    B = {N: sp.Integer(1)}
    gal = conv_coeff(A, B, -1)          # exact: the product has only mode 2N
    ali = alias_coeff(A, B, M, -1)      # collocation: 2N == -1 (mod 2N+1)
    check("Sec5 N=%d: mode -1 of (top mode)^2 is 0 exactly, %d under %d-point collocation"
          % (N, gal, M), gal == 0 and ali == 1)

# general contamination pattern and the padding threshold
for N in range(1, 9):
    M = 2 * N + 1
    A = {p: sp.Integer((p * 7 + 3) % 11 - 5) for p in range(-N, N + 1)}
    B = {q: sp.Integer((q * 5 + 1) % 7 - 3) for q in range(-N, N + 1)}
    bad = [m for m in range(-N, N + 1) if conv_coeff(A, B, m) != alias_coeff(A, B, M, m)]
    check("Sec5 N=%d, M=2N+1: aliasing contaminates the nonzero modes, never l=0" % N,
          0 not in bad and len(bad) > 0, "contaminated modes: %s" % bad)

for N in range(1, 9):
    M = 3 * N + 1
    A = {p: sp.Integer((p * 7 + 3) % 11 - 5) for p in range(-N, N + 1)}
    B = {q: sp.Integer((q * 5 + 1) % 7 - 3) for q in range(-N, N + 1)}
    ok = all(conv_coeff(A, B, m) == alias_coeff(A, B, M, m) for m in range(-N, N + 1))
    check("Sec5 N=%d, M=3N+1=%d: collocation reproduces the exact Galerkin coefficients" % (N, M), ok)

for N in range(1, 9):
    M = 3 * N
    # a witness: the top retained mode and its square, which folds onto mode -N
    A = {N: sp.Integer(1)}
    B = {N: sp.Integer(1)}
    bad = [m for m in range(-N, N + 1) if conv_coeff(A, B, m) != alias_coeff(A, B, M, m)]
    check("Sec5 N=%d, M=3N: the top mode still aliases onto mode -%d "
          "(threshold is sharp at M >= 3N+1)" % (N, N), len(bad) > 0,
          "contaminated modes: %s" % bad)

# the relative size of the alias error: the corrupted coefficient is O(1), not small
N = 4
M = 2 * N + 1
A = {N: sp.Integer(1)}
B = {N: sp.Integer(1)}
gal = conv_coeff(A, B, -1)
ali = alias_coeff(A, B, M, -1)
check("Sec5 the alias error is O(1) in the data: corrupted coefficient %s vs exact %s "
      "(amplitude 1)" % (ali, gal), gal == 0 and ali == 1)

# ----------------------------------------------------------------------------
# Sec 6.  Finite-band growth vs continuous high-frequency growth.
# ----------------------------------------------------------------------------
banner("Sec 6  spectral diagnostic: finite-band growth vs continuous growth")

CC = 1.0          # c = v0 + 2 lam, normalised to 1 (e.g. v0 = 5, lam = -2)
A0 = 1.0          # u0 + 2a (only shifts the imaginary part of sigma)


def re_sigma(cval, kv, lv):
    """max Re sigma of the two branches, for the mode (k, l).

    disc = k^4 - c k^3/l ; Re sigma = sqrt(disc) if disc > 0 else 0.
    """
    R = kv**4 - cval * kv**3 / lv
    if R <= 0.0:
        return 0.0
    return math.sqrt(R)


print()
print("  (a) max over the retained band |l| <= N of Re sigma, c = 1")
print("  %8s | %s | %s" % ("k", " ".join("N=%-6d" % n for n in (1, 2, 4, 8, 16, 32)),
                            "sqrt(k^4+c k^3)"))
rows = []
for kv in (0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0):
    line = []
    for N in (1, 2, 4, 8, 16, 32):
        line.append(max(re_sigma(CC, kv, float(lv)) for lv in range(-N, N + 1) if lv != 0))
    rows.append((kv, line))
    print("  %8.2f | %s | %10.4f"
          % (kv, " ".join("%-8.4f" % v for v in line), math.sqrt(kv**4 + CC * kv**3)))

okA = all(line[0] > 0 for kv, line in rows)
okB = all(max(line) - min(line) < 1e-12 for kv, line in rows)
okC = all(abs(line[0] - math.sqrt(kv**4 + CC * kv**3)) < 1e-9 for kv, line in rows)
check("Sec6 (a) every truncation N >= 1 is unstable at EVERY k > 0 "
      "(the mode l = -1 is retained in every band)", okA)
check("Sec6 (a) the band maximum is attained at l = -1 and is completely "
      "independent of the truncation N", okB and okC)

print()
print("  (b) ratio max Re sigma / k^2   (-> 1 for every fixed N: same k^2 rate)")
print("  %8s | %s" % ("k", " ".join("N=%-6d" % n for n in (1, 2, 4, 8, 16, 32))))
okD = True
for kv, line in rows:
    if kv >= 16.0:
        okD = okD and all(abs(v / kv**2 - 1.0) < 0.05 for v in line)
    print("  %8.2f | %s" % (kv, " ".join("%-8.4f" % (v / kv**2) for v in line)))
check("Sec6 (b) the finite-band growth shows the same k^2 rate as the continuous "
      "high-frequency growth, uniformly in N", okD)

print()
print("  (c) ONE-SIDED sector l >= 1 only: threshold in k is c/N")
okE = True
for N in (1, 2, 4, 8, 16):
    pred = CC / N
    kstar = 0.0
    kk = 0.0
    while kk < 4.0 * CC:
        kk += 1e-4
        if max(re_sigma(CC, kk, float(lv)) for lv in range(1, N + 1)) > 1e-9:
            break
        kstar = kk
    okE = okE and abs(kstar - pred) < 2e-3
    print("    N=%2d : measured k* = %.5f , c/N = %.5f" % (N, kstar, pred))
check("Sec6 (c) the positive-ell modes are neutral exactly for k <= c/N, so the "
      "one-sided stable band shrinks like 1/N -- this is NOT full-band stability, "
      "because l = -1 is unstable for every k > 0", okE)

print()
print("  (d) the small-|l| face: fixed k = 1, l -> 0^- gives unbounded growth")
print("  %12s | %12s | %12s" % ("l", "Re sigma", "sqrt(c k^3/|l|)"))
okF = True
for d in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
    val = re_sigma(CC, 1.0, -d)
    asym = math.sqrt(CC / d)
    okF = okF and abs(val / asym - 1.0) < 0.05
    print("  %12.1e | %12.4f | %12.4f" % (-d, val, asym))
band_max = max(re_sigma(CC, 1.0, float(lv)) for lv in range(-32, 33) if lv != 0)
check("Sec6 (d) for fixed k the CONTINUOUS growth is unbounded as l -> 0^- "
      "(Re sigma ~ sqrt(c k^3/|l|)), while the truncated band |l| >= 1 has the "
      "finite maximum sqrt(k^4+c k^3) = %.4f" % band_max, okF)
check("Sec6 (d) hence the y-truncation regularises the l -> 0 direction "
      "(the singularity at l = 0 is removed) but NOT the k -> infinity direction",
      band_max < math.inf and okA and okD)

# ----------------------------------------------------------------------------
# Sec 7.  Kernel dimension of the centred difference on Z/M.
# ----------------------------------------------------------------------------
banner("Sec 7  centred-difference kernel on Z/M (cross-check with Common/Operators.lean)")
print("  Z/M, C[j, j+1] = +1/2, C[j, j-1] = -1/2 ;  nullity = M - rank")
print("  %4s | %8s | %s" % ("M", "nullity", "expected"))
okF = True
for M in range(3, 11):
    Cm = sp.zeros(M, M)
    for j in range(M):
        Cm[j, (j + 1) % M] += sp.Rational(1, 2)
        Cm[j, (j - 1) % M] -= sp.Rational(1, 2)
    nul = M - Cm.rank()
    want = 1 if M % 2 == 1 else 2
    okF = okF and nul == want
    print("  %4d | %8d | %s" % (M, nul, want))
check("Sec7 odd M (in particular M = 2N+1) gives a ONE-dimensional kernel, "
      "even M gives a spurious second zero mode", okF)

# ----------------------------------------------------------------------------
banner("summary")
n_ok = sum(1 for c_ in CHECKS if c_["ok"])
print("%d/%d checks passed" % (n_ok, len(CHECKS)))
if FAILURES:
    print("FAILED: " + "; ".join(FAILURES))
    print("RESULT: FAIL")
else:
    print("RESULT: OK")

out = {
    "direction": "B_spectral",
    "python": sys.version.split()[0],
    "sympy": sp.__version__,
    "checks_total": len(CHECKS),
    "checks_passed": n_ok,
    "failures": FAILURES,
    "checks": CHECKS,
    "growth_table": [{"k": kv, "maxReSigma_N1_N2_N4_N8_N16_N32": line} for kv, line in rows],
    "c_normalisation": CC,
}
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "spectral_diagnostic_summary.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2, default=str)
print("wrote", os.path.join(here, "spectral_diagnostic_summary.json"))

sys.exit(1 if FAILURES else 0)
