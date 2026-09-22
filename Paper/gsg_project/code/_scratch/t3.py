import sympy as sp, random, time
from engine import Lattice, e_add, e_scale, e_zero

def numeric_zero(d, trials=4):
    """True if every coefficient vanishes at random rational points."""
    if not d: return True, 0
    syms = set()
    for c in d.values(): syms |= c.free_symbols
    syms = sorted(syms, key=str)
    rng = random.Random(20260918)
    for t in range(trials):
        sub = {s: sp.Rational(rng.randint(2,17), rng.randint(1,13)) for s in syms}
        for k,c in d.items():
            v = complex(sp.N(c.subs(sub), 40))
            if abs(v) > 1e-25:
                return False, (k, sp.simplify(c.subs(sub)))
    return True, None

for N in (1,2,3):
    t0=time.time()
    L = Lattice(N, h=None, kind="none")
    f,g = L.tau(1), L.tau(0)
    r7 = L.B(f,g)
    ok,info = numeric_zero(r7)
    print(f"N={N} (7): mono={len(r7)}  exact_cancel_zero={e_zero(r7)}  numeric_zero={ok}  {info if not ok else ''}  [{time.time()-t0:.1f}s]")
    d = e_add(L.der(L.B(f,g),"y"), e_scale(L.Dx(f,g),-4))
    ok2,info2 = numeric_zero(d)
    print(f"     D_yB f.g-4D_x f.g: mono={len(d)} numeric_zero={ok2} {info2 if not ok2 else ''}")
