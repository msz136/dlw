"""New direct original-PDE factor and ambient inverse-bubble checks."""
from pathlib import Path
import hashlib
import json
from math import comb
import sympy as sp

x = sp.Symbol("x")
count = 0
def check(expr):
    global count
    assert sp.simplify(expr) == 0
    count += 1

def compose(left, right):
    out = {}
    for i, a in left.items():
        for j, b in right.items():
            for k in range(i + 1):
                order = i + j - k
                out[order] = out.get(order, 0) + comb(i, k) * a * sp.diff(b, x, k)
    return out

a, b, nu = [sp.Function(n)(x) for n in ("a", "b", "nu")]
at = -sp.diff(nu, x) - sp.diff(a, x, 2) - sp.diff(b * a + a**2, x)
first = {1: sp.Integer(1), 0: -a}
right = {2: -sp.Integer(1), 1: -b, 0: -nu}
left = {2: -sp.Integer(1), 1: -b, 0: -nu - sp.diff(b, x) - 2 * sp.diff(a, x)}
av, wa = compose(first, right), compose(left, first)
for order in range(4):
    check(av.get(order, 0) - wa.get(order, 0) - (at if order == 0 else 0))

p, s, energy_mean, rsx = [sp.Function(n)(x) for n in ("p", "s", "energy_mean", "rsx")]
h = sp.Symbol("h", nonzero=True)
beta = h**2 / 32
plus = p / 2 + h * s / 8
minus = p / 2 - h * s / 8
nu_j = -energy_mean / 2 + rsx / 2 - h * sp.diff(s, x) / 4
nu_next = -energy_mean / 2 + rsx / 2 + h * sp.diff(s, x) / 4
plus_t = -sp.diff(nu_j, x) - sp.diff(plus, x, 2) - sp.diff(b * plus + plus**2, x)
minus_t = -sp.diff(nu_next, x) - sp.diff(minus, x, 2) - sp.diff(b * minus + minus**2, x)
expected_p = sp.diff(energy_mean, x) - sp.diff(rsx, x) - sp.diff(p, x, 2) - sp.diff(b * p + p**2 / 2 + beta * s**2, x)
expected_s = sp.diff(s, x, 2) - sp.diff(b * s + p * s, x)
check(plus_t + minus_t - expected_p)
check(4 * (plus_t - minus_t) / h - expected_s)

a0, a1, a2, b0, b1, b2, t10, t21, t20 = sp.symbols("a0 a1 a2 b0 b1 b2 theta10 theta21 theta20")
q_left, q_mid, q_right = b0 + t10 + t20, b1 + t21, b2
r_left, r_mid, r_right = a2 + t21 + t20, a1 + t10, a0
a2_tilde, b0_tilde = r_left - t20, q_left - t20
check(r_left - q_left - (a2 + t21 - b0 - t10))
check(r_mid - b0_tilde - (a1 - b0))
check(a2_tilde - q_mid - (a2 - b1))
recovered = [r_right, r_mid - t10, a2_tilde - t21, b0_tilde - t10, q_mid - t21, q_right]
for value, original in zip(recovered, [a0, a1, a2, b0, b1, b2]):
    check(value - original)

source = Path(__file__)
result = {"status": "all new independent original-PDE factor checks passed", "sympy": sp.__version__, "assert_count": count, "checks": {"first_order_intertwiner_coefficients": 4, "original_projected_p_s_equations": 2, "reverse_bubble_log_arguments": 3, "ambient_six_coefficients_recovered": 6}, "script_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "scope": "Direct factor bridge and generic ambient inverse bubble only. Floquet and actual flow proofs are in singular_m3_flow_independent_audit.md; no old scripts are imported or run."}
source.with_suffix(".json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
