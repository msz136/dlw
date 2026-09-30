import sympy as sp, time
from engine import DLW, residual_zero, e_is_zero, random_point

print("=== A. continuum regression  (7) B f.g = 0 ;  (6) D_yB f.g - 4D_x f.g = 0 ===")
for N in (1,2,3,4,5):
    t0=time.time()
    ok7,_ = residual_zero(lambda m: m.B(m.tau(1), m.tau(0)), N, trials=3, kind="none")
    ok6,_ = residual_zero(lambda m: __import__("engine").e_add(
        m.DyB(m.tau(1), m.tau(0)),
        __import__("engine").e_scale(m.Dx(m.tau(1), m.tau(0)), -4)), N, trials=3, kind="none")
    print(f"  N={N}:  (7)={'OK' if ok7 else 'FAIL'}   (6)@lam=-2={'OK' if ok6 else 'FAIL'}   [{time.time()-t0:.1f}s]", flush=True)
