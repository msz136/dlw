import sympy as sp
import engine as E
from engine import Lattice, e_add, e_scale, is_zero_exact

L = Lattice(1, h=None, kind="none")
f,g = L.tau(1), L.tau(0)
d = e_add(L.DyB(f,g), e_scale(L.Dx(f,g), -4))
print("monomials:", len(d))
for k,c in d.items():
    syms = sorted(c.free_symbols, key=str)
    print(" key",k," coeff-freesyms",syms)
    print("   coeff =", sp.factor(sp.cancel(c)))
