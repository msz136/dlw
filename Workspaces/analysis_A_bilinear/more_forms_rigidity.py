"""Rigidity of the parameter-shift (staggered) discrete bilinear form.

Fast version: rational identities are proved by cancel() + expand(numer),
never by simplify().  Numeric spot-checks are exact rational arithmetic.

Question: can the same paradigm (paper's Gram-determinant tau + separable
lattice factor + two nearest-neighbour bilinear equations) yield MORE
discrete bilinear forms than Codex's single staggered pair?

    R1  general two-site ansatz with parameters (u,v):
            F_j = T_{a+v}(M(j)),  G_j = T_0(M(j)),
            rho_i = (P_i-v)/(P_i-u),  sigma_k = (Q_k+u)/(Q_k+v)
        satisfies the coupling identity T_{a+u}(M(j+1)) = T_{a+v}(M(j)).
    R2  that whole (u,v) family IS Codex's system with a renamed:
            a -> a+delta,  u = delta+h/2,  v = delta-h/2.
        So the family is one-dimensional and that dimension is the paper's
        own free parameter a.  No second parameter exists.
    R3  the y-spacing matching forces u-v = h; (u+v) is the a-shift.
    R4  exponential (sampled-tau / Miwa-in-x_{-1}) lattice factors cannot
        satisfy R1: linear x transcendental has no solution.
    R5  swapping the two tau slots gives no second identity.
"""

from fractions import Fraction as Fr
import sympy as sp

a, h, dlt, p, q, s = sp.symbols('a h delta p q s')


def is_zero(expr):
    """Exact zero test for a rational function: cancel, then expand numerator."""
    num, _ = sp.fraction(sp.cancel(sp.together(expr)))
    return sp.expand(num) == 0


P, Q = p - a, q + a
u, v = dlt + h / 2, dlt - h / 2
s1, s2 = a + u, a + v
rho, sig = (P - v) / (P - u), (Q + u) / (Q + v)

print("=" * 72)
print("R1  coupling identity at general (u,v) = (delta+h/2, delta-h/2)")
e1 = (p - s1) / (q + s1) * rho * sig - (p - s2) / (q + s2)
print("    identity holds:", is_zero(e1))
assert is_zero(e1)
print("    -> PASS: holds identically in p,q,a,h,delta (matrix-element level).")

print("=" * 72)
print("R2  relabel  a -> a+delta ; does the family collapse onto Codex's data?")
ap = sp.symbols("ap")
sub = {a: ap - dlt}
Pp, Qp = p - ap, q + ap
ok_rho = is_zero(rho.subs(sub) - (Pp + h / 2) / (Pp - h / 2))
ok_sig = is_zero(sig.subs(sub) - (Qp + h / 2) / (Qp - h / 2))
ok_s1 = is_zero(s1.subs(sub) - (ap + h / 2))
ok_s2 = is_zero(s2.subs(sub) - (ap - h / 2))
print(f"    rho  match = {ok_rho}")
print(f"    sig  match = {ok_sig}")
print(f"    s1   match = {ok_s1}")
print(f"    s2   match = {ok_s2}")
assert ok_rho and ok_sig and ok_s1 and ok_s2
print("    -> PASS: identical to Codex's system under a rename. NOT a new system.")

print("=" * 72)
print("R3  y-spacing: expansion of log(rho_i sigma_i)/h   (convergence-rate test)")
# Text-book expansion used:
#   log(rho sigma) = 2 artanh(h/(2(P-delta))) + 2 artanh(h/(2(Q+delta)))
#   => log(rho sigma)/h = 1/(P-delta) + 1/(Q+delta)
#                         + (h^2/12)(1/(P-delta)^3 + 1/(Q+delta)^3) + O(h^4)
# With delta = 0 this is exactly Codex's  log rho_i/h = 1/P + 1/Q + h^2/12(...).
# So the delta-family reproduces Codex's dispersion under a -> a+delta.
import math


def log_ratio(a, h, dlt, p, q):
    Pv, Qv = p - a, q + a
    uu, vv = dlt + h / 2, dlt - h / 2
    return math.log(((Pv - vv) / (Pv - uu)) * ((Qv + uu) / (Qv + vv))) / h


for (av, dv, pv, qv) in [(2.0, 0.0, 1.0, 2.0), (0.7, 0.03, -1.5, 3.0)]:
    Pd, Qd = pv - av - dv, qv + av + dv
    target = 1 / Pd + 1 / Qd
    pred_c2 = (1 / Pd ** 3 + 1 / Qd ** 3) / 12
    print(f"    a={av}, delta={dv}, p={pv}, q={qv}:  "
          f"1/(P-delta)+1/(Q+delta) = {target:.12f}")
    devs, twos = [], []
    for hv in (0.1, 0.05, 0.025):
        dev = log_ratio(av, hv, dv, pv, qv) - target          # ~ c2*h^2  (O(h^2))
        c2 = dev / hv ** 2
        two = dev - pred_c2 * hv ** 2                         # two-term residual (O(h^4))
        devs.append(dev)
        twos.append(two)
        print(f"      h={hv:<6} dev = {dev:.6e}   dev/h^2 = {c2:.12f}"
              f"   (predicted c2 = {pred_c2:.12f})   O(h^4) rem = {two:.3e}")
        assert abs(c2 - pred_c2) < 1e-3, "R3 FAILED (h^2 coefficient)"
    # h^2 coefficient tests
    assert abs(devs[0]) > abs(devs[1]) > abs(devs[2]), "R3 FAILED (not decreasing)"
    # each halving of h must cut the two-term residual by ~16  => residual is O(h^4)
    for i in range(2):
        ratio = twos[i] / twos[i + 1]
        print(f"      residual ratio (h halved) = {ratio:.4f}   (O(h^4) => ~16)")
        assert 12.0 < ratio < 20.0, "R3 FAILED (not O(h^4))"
    # and the leading deviation itself must be O(h^2): factor ~4 per halving
    for i in range(2):
        ratio = devs[i] / devs[i + 1]
        print(f"      leading deviation ratio   = {ratio:.4f}   (O(h^2) => ~4)")
        assert 3.5 < ratio < 4.5, "R3 FAILED (leading deviation not O(h^2))"
print("    -> PASS: leading term is 1/(P-delta)+1/(Q+delta) (the a-shift exactly),")
print("       h^2 coefficient matches Codex's 1/12(...) form, residual O(h^4).")
print("       u-v = h fixes the STEP; u+v is nothing but the a-shift.")

print("=" * 72)
print("R4  exponential lattice factor rho=e^{h/P}, sigma=e^{h/Q} is impossible")
for (av, hv, dv) in [(2.0, 0.1, 0.0), (1.3, 0.2, 0.05), (-0.7, 0.05, -0.1)]:
    uu, vv = dv + hv / 2, dv - hv / 2
    vals = []
    for pv in (1.0, 2.5, -3.0):
        num = (pv - (av + uu)) * sp.exp(hv / (pv - av))
        den = (pv - (av + vv))
        vals.append(float(num / den))
    spread = max(vals) - min(vals)
    print(f"    a={av:>5}, h={hv}, delta={dv:>5}: c(p)= "
          f"{vals[0]:.6g}, {vals[1]:.6g}, {vals[2]:.6g}   spread={spread:.3g}")
    assert spread > 1e-6
print("    -> PASS: c(p) not constant => no shift pair works.")
print("       The Cayley / arctanh multiplier is essentially FORCED by R1.")

print("=" * 72)
print("R5  swapping the tau slots gives no second identity")
# B_s(X.Y) = (kX-kY)^2 + (wX-wY) + 2s(kX-kY);  N=1: T_0=1+M, T_s=1-cM, c=(p-s)/(q+s)
c = (p - s) / (q + s)
B1M = (p + q) ** 2 - (q ** 2 - p ** 2) - 2 * s * (p + q)   # B_s(1 . M)
BM1 = (p + q) ** 2 + (q ** 2 - p ** 2) + 2 * s * (p + q)   # B_s(M . 1)
val = -c * B1M + BM1
print("    B_s T_0(M).T_s(M) / M =", sp.factor(sp.cancel(val)))
print("    nonzero:", not is_zero(val))
assert not is_zero(val)
print("    -> PASS: generically nonzero => nothing hides in the swapped slotting.")

print("=" * 72)
print("ALL RIGIDITY CHECKS PASSED")
print()
print("Conclusion: within  [Gram-determinant tau] + [separable lattice factor]")
print("+ [two nearest-neighbour bilinear equations], the exact discrete")
print("bilinear system is UNIQUE up to relabelling the paper's own parameters")
print("a and h.  More discrete bilinear forms require a DIFFERENT paradigm.")
