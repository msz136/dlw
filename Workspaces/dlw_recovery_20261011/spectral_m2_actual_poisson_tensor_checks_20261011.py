"""Exact search for a constant two-spectral-parameter total-derivative tensor.

Uses the actual M=2 traceless rank-one connection and physical free bracket.
No old certificates are rerun.  A successful identity alone does not prove
nonlinear spectral completeness.
"""
import hashlib
import json
from pathlib import Path
import sympy as sp


def comm(a, b):
    return a * b - b * a


S, la, mu = sp.symbols("S la mu", nonzero=True)
H = sp.diag(1, -1)
E = sp.Matrix([[0, 1], [0, 0]])
F = sp.Matrix([[0, 0], [1, 0]])
I = sp.eye(2)
basis = [H, E, F]
K = lambda t: t / S * H + (1 + t / S) * E + (1 - t / S) * F
L0 = lambda t: S / 2 * (E - F) + t / 2 * (E + F)
kron = sp.kronecker_product
B = kron(H / 2, K(mu)) + kron(K(la), H / 2)
rs = sp.symbols("r0:9")
R = sp.zeros(4)
for i, a in enumerate(basis):
    for j, b in enumerate(basis):
        R += rs[3 * i + j] * kron(a, b)
eqs = []
for Ll, Lm in [(H / 2, H / 2), (K(la), K(mu)), (L0(la), L0(mu))]:
    plus = kron(Ll, I) + kron(I, Lm)
    minus = kron(I, Lm) - kron(Ll, I)
    residual = comm(R, plus) - comm(B, minus) / 2
    eqs.extend(list(residual))
solution = sp.linsolve(eqs, rs)
payload = {
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "equations": len(eqs),
    "unknowns": len(rs),
    "solution": str(solution),
}
if solution != sp.EmptySet:
    sol = next(iter(solution))
    subst = dict(zip(rs, sol))
    verified = all(sp.cancel(x.subs(subst)) == 0 for x in eqs)
    payload["exact_tensor_identity_verified"] = verified
    assert verified
    u, v = sp.symbols("u v")
    d0, d1 = S / 2 + v, S / 2 - v
    b1 = -d0 * u / S
    b0 = b1 + u
    raw = sp.Matrix([[la * d0 / S + b0, d0 * (la / S + 1)],
                     [d1 * (la / S - 1), la * d1 / S + b1]])
    traceless = raw - sp.trace(raw) * I / 2
    exact_connection = L0(la) + u * H / 2 + v * K(la)
    payload["actual_physical_traceless_connection_verified"] = all(
        sp.cancel(x) == 0 for x in traceless - exact_connection
    )
    assert payload["actual_physical_traceless_connection_verified"]
    payload["actual_trace_verified"] = sp.cancel(
        sp.trace(raw) - (la - 2 * u * v / S)
    ) == 0
    assert payload["actual_trace_verified"]
    Rsol = R.subs(subst)
    flipped = sp.zeros(4)
    for i, a in enumerate(basis):
        for j, b in enumerate(basis):
            coefficient = sol[3 * i + j].subs({la: mu, mu: la}, simultaneous=True)
            flipped += coefficient * kron(b, a)
    payload["spectral_flip_antisymmetry_verified"] = all(
        sp.cancel(x) == 0 for x in Rsol + flipped
    )
    assert payload["spectral_flip_antisymmetry_verified"]
else:
    payload["exact_tensor_identity_verified"] = False
Path(__file__).with_suffix(".json").write_text(
    json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)
print(json.dumps(payload, ensure_ascii=False))
