"""Bounded exact M=3 constant tensor search in two symbolic spectral parameters.

S=1 is only dimensionless normalization.  A general nonzero S follows by
a=lambda/S, b=mu/S and scaling all free fields by S.  No older checks run.
"""
from __future__ import annotations
import hashlib
import json
import multiprocessing as mp
from pathlib import Path
import time
import sympy as sp


def comm(a, b):
    return a * b - b * a


def search(result_queue):
    started = time.monotonic()
    a, b = sp.symbols("a b")
    qs = sp.symbols("q0:2")
    ds = sp.symbols("d0:2")
    identity = sp.eye(3)
    d = [*ds, 1 - sum(ds)]
    delta = [qs[j] + 1 - sum(ds[:j]) + sum(ds[j + 1:]) for j in range(2)] + [0]

    def connection(parameter):
        return sp.Matrix(3, 3, lambda j, k:
            parameter * (d[j] - sp.Rational(1, 3))
            + delta[j] - sum(delta) / 3 if j == k
            else d[j] * (parameter + (1 if k > j else -1)))

    La, Lb = connection(a), connection(b)
    generators = []
    names = []
    for j in range(2):
        g = sp.zeros(3)
        g[j, j] = 1
        generators.append(g - identity / 3)
        names.append(f"H{j}")
    for j in range(3):
        for k in range(3):
            if j != k:
                g = sp.zeros(3)
                g[j, k] = 1
                generators.append(g)
                names.append(f"E{j}{k}")
    kron = sp.kronecker_product
    B = sp.zeros(9)
    for q, dfree in zip(qs, ds):
        B += kron(La.diff(q), Lb.diff(dfree)) + kron(La.diff(dfree), Lb.diff(q))
    unknowns = sp.symbols("r0:64")
    R = sp.zeros(9)
    tensor_basis = []
    for i, g in enumerate(generators):
        for j, h in enumerate(generators):
            tensor_basis.append(kron(g, h))
            R += unknowns[8 * i + j] * tensor_basis[-1]
    all_equations = []
    zero_source = dict.fromkeys([*qs, *ds], 0)
    field_pairs = [(La.subs(zero_source), Lb.subs(zero_source))]
    field_pairs += [(La.diff(f), Lb.diff(f)) for f in [*qs, *ds]]
    for l1, l2 in field_pairs:
        plus = kron(l1, identity) + kron(identity, l2)
        minus = kron(identity, l2) - kron(l1, identity)
        residual = comm(R, plus) - comm(B, minus) / 2
        all_equations.extend(list(residual))
    equations = [sp.expand(eq) for eq in all_equations if eq != 0]
    solution_set = sp.linsolve(equations, unknowns)
    result = {
        "M": 3,
        "parameter_domain": "Q(a,b), a=lambda/S, b=mu/S, S != 0",
        "equations_total": len(all_equations),
        "equations_nonzero": len(equations),
        "unknowns": len(unknowns),
        "solution_exists": solution_set != sp.EmptySet,
        "search_seconds": time.monotonic() - started,
    }
    if result["solution_exists"]:
        solution = next(iter(solution_set))
        subst = dict(zip(unknowns, solution))
        assert all(sp.cancel(eq.subs(subst)) == 0 for eq in all_equations)
        result["exact_identity_verified"] = True
        result["free_tensor_parameters"] = [str(x) for x in
            sorted(set().union(*(x.free_symbols for x in solution)) - {a, b}, key=str)]
        result["coefficients"] = {
            f"{names[i]} tensor {names[j]}": str(sp.factor(solution[8 * i + j]))
            for i in range(8) for j in range(8)
            if solution[8 * i + j] != 0
        }
    else:
        result["exact_identity_verified"] = False
    result_queue.put(result)


if __name__ == "__main__":
    queue = mp.Queue()
    process = mp.Process(target=search, args=(queue,))
    process.start()
    process.join(55)
    if process.is_alive():
        process.terminate()
        process.join(5)
        result = {"M": 3, "status": "bounded_search_timeout", "budget_seconds": 55}
    elif process.exitcode != 0:
        result = {"M": 3, "status": "worker_failed", "exitcode": process.exitcode}
    else:
        result = queue.get(timeout=2)
        result["status"] = "completed"
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(__file__).with_suffix(".json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False))
