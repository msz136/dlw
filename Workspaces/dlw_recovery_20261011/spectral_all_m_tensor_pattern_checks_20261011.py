"""New symbolic tests of the candidate universal tensor inferred from M=3.

Finite tests supplement, and do not replace, a dimension-free proof.  No old
certificates or the preceding M=3 linear solve are rerun.
"""
import hashlib
import json
from pathlib import Path
import time
import sympy as sp


def comm(a, b):
    return a * b - b * a


started = time.monotonic()
a, b = sp.symbols("a b")
checks = []
for M in (4, 5):
    identity = sp.eye(M)
    units = {(i, j): sp.SparseMatrix(M, M, {(i, j): 1})
             for i in range(M) for j in range(M)}
    h = [units[i, i] - identity / M for i in range(M)]
    kron = sp.kronecker_product
    cartan = sum((kron(x, x) for x in h), sp.zeros(M * M))
    # Rden=(a-b)R avoids any rational-expression simplification in verification.
    Rden = (2 - a * a - b * b) / 2 * cartan
    for i in range(M):
        for j in range(M):
            if i == j:
                continue
            sign = 1 if j > i else -1
            Rden += (a - b) / 2 * (
                (b + sign) * kron(h[i], units[i, j])
                - (a + sign) * kron(units[i, j], h[i]))
            Rden += -(a + sign) * (b - sign) * kron(units[i, j], units[j, i])
    row = lambda i, parameter: sum(
        ((parameter + (0 if i == j else (1 if j > i else -1))) * units[i, j]
         for j in range(M)), sp.zeros(M))
    B = sum((kron(h[i], row(i, b)) + kron(row(i, a), h[i])
             for i in range(M)), sp.zeros(M * M))
    per_case = []
    # Canonical Delta,d fields.  Sum d=S; proving every individual row suffices.
    pairs = [(h[i], h[i], f"Cartan{i}") for i in range(M)]
    pairs += [(row(i, a), row(i, b), f"row{i}") for i in range(M)]
    for L1, L2, label in pairs:
        plus = kron(L1, identity) + kron(identity, L2)
        minus = kron(identity, L2) - kron(L1, identity)
        residual = comm(Rden, plus) - (a - b) / 2 * comm(B, minus)
        nonzero = []
        for index, value in enumerate(residual):
            reduced = sp.expand(value)
            if reduced != 0:
                nonzero.append((index, str(reduced)))
        per_case.append({"label": label, "verified": not nonzero,
                         "nonzero_first": nonzero[:2]})
        if nonzero:
            break
    checks.append({"M": M, "cases": per_case,
                   "all_verified": all(x["verified"] for x in per_case)})
    if not checks[-1]["all_verified"]:
        break
payload = {"script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           "parameter_domain": "Q(a,b), a=lambda/S,b=mu/S,S!=0",
           "checks": checks, "seconds": time.monotonic() - started,
           "all_verified": all(x["all_verified"] for x in checks)}
Path(__file__).with_suffix(".json").write_text(
    json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload))
