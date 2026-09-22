import sympy as sp
from engine import DLW, random_point, e_is_zero

for N in (2,3):
    for trial in range(4):
        m = DLW(N, kind="none")
        pt = random_point(m, seed=1+97*trial)
        m.set_point(pt)
        f,g = m.tau(1), m.tau(0)
        d7 = m.B(f,g)
        raw = {k:v for k,v in d7.items()}
        nonfinite = any(not v.is_finite for v in raw.values())
        canc = {k: sp.cancel(v) for k,v in raw.items()}
        canc = {k:v for k,v in canc.items() if v!=0}
        print(f"N={N} trial={trial} pt={pt}")
        print(f"   raw monomials={len(raw)} nonfinite={nonfinite}  after cancel={len(canc)}")
        if canc: print("    sample:", list(canc.items())[:1])
