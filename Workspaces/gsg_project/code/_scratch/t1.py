import sympy as sp
from engine import DLWModel

# ---- continuum regression: (7) and (6) for N=1,2,3
for N in (1,2,3):
    m = DLWModel(N, h=None, lattice="none")
    f, g = m.tau(1), m.tau(0)
    r7 = m.clean(m.B(f,g))
    r6 = m.clean(m.deriv(m.B(f,g),"y") + 2*sp.Symbol("lam", real=True)*m.Dx(f,g))
    print(f"N={N}  (7) B f.g -> {r7}     (6) D_yB f.g + 2lam D_x f.g -> {r6}")

# ---- is D_yB f.g = 4 D_x f.g at lam=-2 ?
for N in (1,2,3):
    m = DLWModel(N, h=None, lattice="none")
    f, g = m.tau(1), m.tau(0)
    d = m.clean(m.deriv(m.B(f,g),"y") - 4*m.Dx(f,g))
    print(f"N={N}  D_yB f.g - 4D_x f.g -> {d}")
