"""
GSG-style semi-discretization of the DLW bilinear system (6),(7)  --  exploration.

Question 1:  with the GSG discrete exponential  e^{y/P} -> (1-h/P)^{-k},
             which two-site bilinear relation replaces  (6)  [D_y B + 2 lam D_x] f.g = 0 ?

We test every natural candidate exactly, for N = 1 and N = 2 with generic parameters.
"""
import sympy as sp
from itertools import product

x, t, y, h, a, lam = sp.symbols('x t y h a lam', real=True)
j = sp.symbols('j', integer=True)


def Dx(F, G, v='x'):
    return sp.diff(F, v) * G - F * sp.diff(G, v)


def Bop(F, G, aa):
    return (sp.diff(F, x, 2) * G - 2 * sp.diff(F, x) * sp.diff(G, x) + F * sp.diff(G, x, 2)) \
        + Dx(F, G, 't') + 2 * aa * Dx(F, G)


def build_tau(N, nval, mode, cvals=None):
    """mode='cont' | 'disc_y' | 'disc_x' """
    p = [sp.Symbol(f'p{i+1}') for i in range(N)]
    q = [sp.Symbol(f'q{i+1}') for i in range(N)]
    xi0 = [sp.Symbol(f'A{i+1}') for i in range(N)]
    et0 = [sp.Symbol(f'B{i+1}') for i in range(N)]
    if cvals is None:
        cvals = [1] * N
    M = sp.zeros(N, N)
    for i in range(N):
        for k in range(N):
            Pi, Qk = p[i] - a, q[k] + a
            xi = -p[i] ** 2 * t + xi0[i]
            et = q[k] ** 2 * t + et0[k]
            if mode == 'cont':
                xi += p[i] * x + y / Pi
                et += q[k] * x + y / Qk
            elif mode == 'disc_y':
                xi += p[i] * x + sp.log(1 - h / Pi) * (-j)
                et += q[k] * x + sp.log(1 - h / Qk) * (-j)
            elif mode == 'disc_x':
                xi += sp.log(1 - h * p[i]) * (-j) + y / Pi
                et += sp.log(1 - h * q[k]) * (-j) + y / Qk
            M[i, k] = (cvals[k] if i == k else 0) + sp.exp(xi + et) * (-Pi / Qk) ** nval / (p[i] + q[k])
    return sp.expand(M.det()), p, q


def is_zero(e):
    if e == 0:
        return True
    try:
        return sp.simplify(sp.expand(sp.log(sp.expand(e)) if False else e)) == 0
    except Exception:
        return False


def report(name, e):
    s = sp.simplify(sp.expand(e))
    ok = (s == 0)
    print(f"  [{'OK  ' if ok else 'FAIL'}] {name}")
    if not ok:
        print(f"          residual = {s}")
    return ok


print("=" * 84)
print("TEST A : continuum regression  --  (7) B f.g = 0  and  (6) [D_y B + 2lam D_x] f.g = 0")
print("=" * 84)
for N in (1, 2):
    tau0, p, q = build_tau(N, 0, 'cont')
    tau1, _, _ = build_tau(N, 1, 'cont')
    f, g = tau1, tau0
    report(f"N={N}  (7)  B f.g = 0", Bop(f, g, a))
    e6 = Dx(Bop(f, g, a), 'y') + 2 * lam * Dx(f, g)
    report(f"N={N}  (6)  [D_y B + 2lam D_x] f.g = 0   (every lam)", e6)

print()
print("=" * 84)
print("TEST B : GSG discrete exponential in y,  tau_n(j)")
print("=" * 84)


def make_pair(N, mode):
    t0, p, q = build_tau(N, 0, mode)
    t1, _, _ = build_tau(N, 1, mode)
    # shift helpers:  tau(j+s).  We build them by direct substitution.
    return t0, t1, p, q


def shift(e, s):
    return e.subs(j, j + s)


for N in (1, 2):
    t0, t1, p, q = make_pair(N, 'disc_y')
    f, g = t1, t0
    print(f"-- N = {N}")
    report(f"(7) site-wise  B f_j.g_j = 0", Bop(f, g, a))
    # candidate discrete (6)
    d1 = (Bop(shift(f, 1), g, a) - Bop(f, shift(g, 1), a)) / h
    report("(6a) forward two-site  (1/h)[B f_{j+1}.g_j - B f_j.g_{j+1}] + 2lam D_x f_j.g_j",
           d1 + 2 * lam * Dx(f, g))
    d2 = (Bop(shift(f, 1), shift(g, -1), a) - Bop(shift(f, -1), shift(g, 1), a)) / (2 * h)
    report("(6b) centred         (1/2h)[B f_{j+1}.g_{j-1} - B f_{j-1}.g_{j+1}] + 2lam D_x f_j.g_j",
           d2 + 2 * lam * Dx(f, g))
    # what IS the forward two-site difference equal to ?
    print(f"     info:  (1/h)[B f_{j+1}.g_j - B f_j.g_{j+1}] / (f_j g_j) = "
          f"{sp.simplify(d1/(f*g))}")
    print(f"     info:  D_x f_j.g_j / (f_j g_j) = {sp.simplify(Dx(f, g)/(f*g))}")
