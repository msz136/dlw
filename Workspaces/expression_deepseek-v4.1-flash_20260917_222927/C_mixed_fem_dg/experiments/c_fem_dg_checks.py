#!/usr/bin/env python
"""
Direction C (mixed FEM / DG discretisation in y for the DLW system).

Exact (SymPy) and numerical (NumPy) checks backing the report.

run:  python -u experiments/c_fem_dg_checks.py
"""
import sympy as sp
import numpy as np

I = sp.I
th, h, ell = sp.symbols('theta h ell', real=True)
k = sp.symbols('k', real=True)


def cz(e):
    return sp.simplify(sp.expand_complex(sp.expand(e)))


print("== A. exact symbols (SymPy) ==")
m_sym = h / 6 * (sp.exp(-I * th) + 4 + sp.exp(I * th))
a_sym = sp.Rational(1, 2) * (sp.exp(I * th) - sp.exp(-I * th))
print("A1  M symbol  - h(2+cos)/3      =", cz(m_sym - h * (2 + sp.cos(th)) / 3), " [0 = ok]")
print("A2  A^T symbol - i sin           =", cz(a_sym - I * sp.sin(th)), " [0 = ok]")
mu1 = a_sym / m_sym
d3 = cz(mu1 - 3 * I * sp.sin(th) / (h * (2 + sp.cos(th))))
print("A3  mu_P1 - 3 i sin/(h(2+cos))   =", d3)
print("A3b   ... numerically (th=0.7,h=0.3) =",
      complex(d3.subs({th: 0.7, h: 0.3})), " [~0 = ok]")
print("A4  R(theta) series              =", sp.series(3 * sp.sin(th) / (th * (2 + sp.cos(th))), th, 0, 9))
print("A5  numerator 3 sin - th(2+cos)  =", sp.series(3 * sp.sin(th) - th * (2 + sp.cos(th)), th, 0, 9))
print("A6  mu_P1 at Nyquist theta=pi    =", sp.simplify(cz(mu1).subs(th, sp.pi)), "  [0 = Nyquist zero]")
mu1l = 3 * I * sp.sin(ell * h) / (h * (2 + sp.cos(ell * h)))
print("A7  mu_P1 - i ell (series in ell)=", sp.series(mu1l - I * ell, ell, 0, 7))
muDG = (1 - sp.exp(-I * th)) / h
print("A8  mu_DG(P0 upwind)             =", muDG,
      " Re =", sp.simplify(sp.re(sp.expand(muDG))), " Im =", sp.simplify(sp.im(sp.expand(muDG))))
print("A9  mu_DG series in theta        =", sp.series(muDG, th, 0, 4))
print("A10 mu_DG at Nyquist             =", sp.simplify(muDG.subs(th, sp.pi)), " [2/h != 0]")
print("A11 mu_DG - i ell (series in ell)=", sp.series(muDG.subs(th, ell * h) - I * ell, ell, 0, 3))

print("== B. P1 DG upwind symbol (2 dofs per cell, upwind = left trace) ==")
# weak form  int (D_h u) phi = -int u phi' + [uhat phi],  uhat at an interface = left trace
# row phi_0^j : (a_j+b_j)/2 - b_{j-1} ;  row phi_1^j : -(a_j+b_j)/2 + b_j
Me = h / 6 * sp.Matrix([[2, 1], [1, 2]])
z = sp.exp(I * th)
B = sp.Matrix([[0, -1 / z], [0, 1]]) + sp.Matrix(
    [[sp.Rational(1, 2), sp.Rational(1, 2)], [-sp.Rational(1, 2), -sp.Rational(1, 2)]])
muv = sp.symbols('mu')
for e in sp.solve(sp.det(Me * muv - B), muv):
    e = sp.simplify(e)
    print("B1  branch:", e)
    print("      small theta:", sp.series(e, th, 0, 5),
          " at Nyquist:", sp.simplify(e.subs(th, sp.pi)))

print("== C. numerics ==")
N = 12
hh = 2 * np.pi / N
n = np.arange(N)
ths = 2 * np.pi * n / N
m = hh * (2 + np.cos(ths)) / 3
a = 1j * np.sin(ths)
mu = a / m

M = np.zeros((N, N))
for j in range(N):
    M[j, j] = 2 * hh / 3
    M[j, (j + 1) % N] += hh / 6
    M[j, (j - 1) % N] += hh / 6
Minv = np.linalg.inv(M)

# exact closed form of the periodic inverse: (M^-1)_{jk} = (sqrt3/h) sum_w r^|j-k+wN|
r = np.sqrt(3) - 2
K = np.zeros((N, N))
for j in range(N):
    for kk in range(N):
        K[j, kk] = np.sqrt(3) / hh * sum(r ** abs(j - kk + w * N) for w in range(-60, 61))
print("C1  max|M^-1 - (sqrt3/h) sum_w r^|j-k+wN|| =", np.max(np.abs(Minv - K)),
      "  r = sqrt3-2 =", r)
print("C2  |M^-1| decay ratios: |c1/c0| =", abs(Minv[0, 1] / Minv[0, 0]),
      " |c3/c2| =", abs(Minv[0, 3] / Minv[0, 2]), " (theory 0.267949)")

for nn in [1, 2, N // 2 - 1, N // 2]:
    col = np.exp(2j * np.pi * nn * n / N)
    r1 = (M @ col)[0] / col[0]
    r2 = ((0.5 * np.roll(col, -1) - 0.5 * np.roll(col, 1)))[0] / col[0]
    print("C3  mode n=%2d : M-symbol %s (closed %s) ; A^T-symbol %s (closed %s)"
          % (nn, np.round(r1, 12), np.round(m[nn], 12), np.round(r2, 12), np.round(a[nn], 12)))

u0, a0, v0, lam = 0.4, 0.7, 1.1, -2.0
A = u0 + 2 * a0
c = v0 + 2 * lam
print("C4  A = u0+2a =", A, " ; v0+2lam =", c, " (standing zero-mode background v0 = -2lam = 4)")
for kx in [0.7, 1.3, 2.5]:
    errs = []
    for nn in range(N):
        if nn in (0, N // 2):
            continue  # mu = 0 : y-constant mode and Nyquist, pencil degenerate
        mun = mu[nn]
        P2 = np.array([[mun, 0], [0, 1]], dtype=complex)
        Q2 = np.array([[-1j * kx * A * mun, kx ** 2],
                       [kx ** 2 * mun - 1j * kx * c, -1j * kx * A]], dtype=complex)
        ev = np.linalg.eigvals(np.linalg.solve(P2, Q2))
        e0 = -1j * kx * A + np.sqrt(kx ** 4 - 1j * kx ** 3 * c / mun)
        e1 = -1j * kx * A - np.sqrt(kx ** 4 - 1j * kx ** 3 * c / mun)
        # compare as multisets (both roots are often purely imaginary, so sorting
        # by real part is numerically ambiguous)
        errs.append(min(max(abs(ev[0] - e0), abs(ev[1] - e1)),
                        max(abs(ev[0] - e1), abs(ev[1] - e0))))
    print("C5  k=%4.1f  max |discrete sigma - analytic sigma| over non-degenerate modes = %.3e"
          % (kx, max(errs)))
print("C6  analytic formula used: (sigma + i A k)^2 = k^4 - i (v0+2lam) k^3 / mu_h(ell)")
for cc, lab in [(c, "v0=1.1 (c=%s)" % c), (0.0, "v0=4 (c=0, zero-mode background)")]:
    print("C7  degenerate modes (mu=0): roots of sigma^2 + i A k sigma + i c k^3 = 0, %s ->" % lab,
          np.roots([1, 1j * 1.3 * A, 1j * 1.3 ** 3 * cc]))

ell0 = 1.7
print("C8  order study, ell = 1.7 (P1 consistent vs DG P0 upwind)")
prev = None
for h_ in [0.4, 0.2, 0.1, 0.05]:
    e1 = abs(3j * np.sin(ell0 * h_) / (h_ * (2 + np.cos(ell0 * h_))) - 1j * ell0)
    e2 = abs((1 - np.exp(-1j * ell0 * h_)) / h_ - 1j * ell0)
    print("      h=%.3f  P1-consistent err=%.6e (ratio %s)   DG-P0-upwind err=%.6e"
          % (h_, e1, "-" if prev is None else round(prev / e1, 4), e2))
    prev = e1

Mf = 4096
tt = 2 * np.pi * np.arange(Mf) / Mf
cf = np.fft.fft(1 / (2 + np.cos(tt))) / Mf
print("C9  Fourier coefficients of 1/(2+cos): c0 =", cf[0].real, " (1/sqrt3 =", 1 / np.sqrt(3), ")")
print("      c_n / r^n for n=1..5:", [round((cf[n].real) / r ** n, 10) for n in range(1, 6)],
      " (1/sqrt3 =", round(1 / np.sqrt(3), 10), ")")

hh2 = 0.37
Mel = hh2 / 6 * np.array([[2, 1], [1, 2]])
Kel = 1 / hh2 * np.array([[1, -1], [-1, 1]])
print("C10 det(element mass) - h^2/12 =", np.linalg.det(Mel) - hh2 ** 2 / 12,
      " ; stiffness * (1,1) =", Kel @ np.ones(2))
