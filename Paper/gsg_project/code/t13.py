import sympy as sp, time
from engine import DLW, zero_at_points, e_add, e_scale

print("=== A. continuum regression:  (7) B f.g = 0  and  (6) D_yB f.g - 4D_x f.g = 0 ===")
for N in (1,2,3,4,5,6):
    t0=time.time()
    def mk7(m): return m.B(m.tau(1), m.tau(0))
    def mk6(m): return e_add(m.DyB(m.tau(1), m.tau(0)), e_scale(m.Dx(m.tau(1), m.tau(0)), -4))
    def mk6gen(m):
        lam = sp.Symbol("lam")
        return e_add(m.DyB(m.tau(1), m.tau(0)), e_scale(m.Dx(m.tau(1), m.tau(0)), 2*lam))
    ok7,_ = zero_at_points(mk7, N, trials=3, kind="none")
    ok6,_ = zero_at_points(mk6, N, trials=3, kind="none")
    ok6g,_ = zero_at_points(mk6gen, N, trials=2, kind="none")
    print(f"  N={N}:  (7)={'OK' if ok7 else 'FAIL'}   (6)@lam=-2={'OK' if ok6 else 'FAIL'}"
          f"   (6) generic lam={'OK(unexpected)' if ok6g else 'nonzero (expected)'}   [{time.time()-t0:.1f}s]", flush=True)
