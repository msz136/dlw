"""Reproducible DLW one-soliton parameter and initial-state design.

This creates inputs and checks algebraic admissibility. It does not evolve the
DLW solver or certify an error region. Run from any working directory.
"""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import math
import random


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "design"
SEED = 20260923
H_VALUES = (0.25, 0.125, 0.0625)
S_GRID = (F(3, 2), F(3), F(5))
G_GRID = (F(1, 2), F(1), F(2), F(3), F(5))
NU_GRID = (F(-1, 2), F(0), F(1, 2))
X_GRID = (F(-1), F(0), F(1))
PERTURB_BACKGROUNDS = (
    (4, 1, 2), (4, 2, 3), (6, 1, 2),
    (4, 2, 1), (2, 1.5, 2), (2, 0.375, 1.125),
)


def parameters(S: float, g: float, nu: float, x_c: float) -> dict:
    p = S * (1 + nu) / 2
    q = S * (1 - nu) / 2
    a = g + p
    return {"S": S, "g": g, "nu": nu, "x_c": x_c,
            "a": a, "p": p, "q": q,
            "rho_gram": S * math.exp(-S * x_c),
            "speed": p - q}


def admissible(row: dict, tolerance: float = 1e-11) -> bool:
    S, g, nu, x_c, a = (row[k] for k in ("S", "g", "nu", "x_c", "a"))
    return (1.5 - tolerance <= S <= 5 + tolerance
            and 0.5 - tolerance <= g <= 5 + tolerance
            and -0.5 - tolerance <= nu <= 0.5 + tolerance
            and -1 - tolerance <= x_c <= 1 + tolerance
            and 2 - tolerance <= a <= 6 + tolerance)


def exact_coefficients(row: dict, h: float) -> dict:
    """Coefficients in the repo's N=1 finite-h Gram formula."""
    S, g, x_c = (row[k] for k in ("S", "g", "x_c"))
    d = h / 2
    gamma = (g - d) / (S + g - d)
    chi = ((g - d) / (g + d)) * ((S + g + d) / (S + g - d))
    assert S > 0 and g > d and 0 < gamma < 1 and 0 < chi < 1
    return {"h": h, "gamma": gamma, "chi": chi,
            "log_gram_amplitude": math.log(row["rho_gram"]),
            "regular_margin_a_minus_p_minus_h_over_2": g - d}


def sigmoid(z: float) -> float:
    if z >= 0:
        return 1 / (1 + math.exp(-z))
    e = math.exp(z)
    return e / (1 + e)


def bump(s: float) -> float:
    return math.exp(1 - 1 / (1 - s * s)) if abs(s) < 1 else 0.0


def field_at(row: dict, h: float, j: int, x: float,
             b: list[float] | None = None) -> tuple[float, float]:
    """Physical (u,v) at t=0; b is an optional eight-direction perturbation."""
    c = exact_coefficients(row, h)
    S, chi, gamma = row["S"], c["chi"], c["gamma"]
    z = S * (x - row["x_c"]) + j * math.log(chi)

    def u_at(k: int) -> float:
        zk = z + (k - j) * math.log(chi)
        return S * (2 * sigmoid(zk + math.log(gamma))
                    - sigmoid(zk) - sigmoid(zk + math.log(chi)))

    u = u_at(j)
    W = 4 * S / h * (sigmoid(z + math.log(chi)) - sigmoid(z))
    v = W + (u_at(j + 1) - u_at(j - 1)) / (2 * h)
    if b is not None:
        assert len(b) == 8 and sum(abs(t) for t in b) <= 0.010000000001
        y, xx = (j + 0.5) * h, x - row["x_c"]
        A = bump(xx / 2) * bump(y)
        phi = (A * math.cos(xx), A * math.sin(xx),
               A * math.cos(4 * xx) * math.cos(math.pi * y),
               A * math.sin(4 * xx) * math.sin(math.pi * y))
        u_scales = (min(S, 4 / 3), min(S, 4 / 3),
                    min(S, 4 / (3 + math.pi)), min(S, 4 / (3 + math.pi)))
        u += sum(b[k] * u_scales[k] * phi[k] for k in range(4))
        v += 4 * sum(b[k + 4] * phi[k] for k in range(4))
    return u, v


def initial_state(row: dict, h: float, js: list[int], xs: list[float],
                  b: list[float] | None = None) -> dict:
    """Construct physical fields and compatible P,W on a common x grid.

    js must be consecutive. The first P row is a left ghost difference; a
    solver may instead store only P[1:]. The adjacent u values come from the
    same perturbed physical field, including the y ghost samples.
    """
    assert js and all(js[k] + 1 == js[k + 1] for k in range(len(js) - 1))
    u, v, P, W = [], [], [], []
    for j in js:
        ur, vr, pr, wr = [], [], [], []
        for x in xs:
            uj, vj = field_at(row, h, j, x, b)
            um = field_at(row, h, j - 1, x, b)[0]
            up = field_at(row, h, j + 1, x, b)[0]
            ur.append(uj)
            vr.append(vj)
            pr.append((uj - um) / h)
            wr.append(vj - (up - um) / (2 * h))
        u.append(ur)
        v.append(vr)
        P.append(pr)
        W.append(wr)
    return {"u": u, "v": v, "P": P, "W": W}


def background_row(case_id: str, group: str, coordinates) -> dict:
    row = {"id": case_id, "group": group,
           **parameters(*(float(v) for v in coordinates))}
    assert admissible(row)
    row["coefficients_by_h"] = [exact_coefficients(row, h) for h in H_VALUES]
    return row


def construction() -> tuple[list[dict], dict]:
    grid = {(S, g, nu, x_c) for S, g, nu, x_c
            in product(S_GRID, G_GRID, NU_GRID, X_GRID)
            if 2 <= g + S * (1 + nu) / 2 <= 6}
    edges = {(S, F(a) - S * (1 + nu) / 2, nu, x_c)
             for S, a, nu, x_c in product(S_GRID, (2, 6), NU_GRID, X_GRID)
             if F(1, 2) <= F(a) - S * (1 + nu) / 2 <= 5}
    extra = edges - grid
    assert (len(grid), len(extra), len(grid | edges)) == (90, 33, 123)
    rows = [background_row(f"C{i:03}", "grid", item)
            for i, item in enumerate(sorted(grid), 1)]
    rows += [background_row(f"C{i:03}", "a_boundary", item)
             for i, item in enumerate(sorted(extra), len(rows) + 1)]
    return rows, {"grid": len(grid), "new_a_boundary": len(extra)}


def holdout(construction_rows: list[dict]) -> list[dict]:
    # Precommitted independent draw in (S, log g, nu, x_c), followed by
    # rejection on a. No solver result is consulted by this function.
    rng = random.Random(SEED)
    known = {(r["S"], r["g"], r["nu"], r["x_c"])
             for r in construction_rows}
    rows = []
    while len(rows) < 64:
        S = round(rng.uniform(1.5, 5), 12)
        g = round(math.exp(rng.uniform(math.log(0.5), math.log(5))), 12)
        nu = round(rng.uniform(-0.5, 0.5), 12)
        x_c = round(rng.uniform(-1, 1), 12)
        row = parameters(S, g, nu, x_c)
        key = (S, g, nu, x_c)
        if admissible(row) and key not in known:
            rows.append(background_row(f"H{len(rows)+1:03}", "holdout", key))
            known.add(key)
    return rows


def perturbations() -> tuple[list[dict], list[dict]]:
    backgrounds = []
    for i, (a, p, q) in enumerate(PERTURB_BACKGROUNDS, 1):
        S = p + q
        coords = (S, a - p, (p - q) / S, 0.0)
        backgrounds.append(background_row(f"B{i:02}", "perturbation_base", coords))
    rng = random.Random(SEED + 1)
    rows = []
    for base in backgrounds:
        for axis in range(8):
            for sign, amplitude in product((-1, 1), (1e-4, 1e-3, 1e-2)):
                b = [0.0] * 8
                b[axis] = sign * amplitude
                rows.append({"id": f"Q{len(rows)+1:03}", "background_id": base["id"],
                             "kind": "axis", "b": b})
        for _ in range(16):
            raw = [rng.gauss(0, 1) for _ in range(8)]
            norm = sum(abs(value) for value in raw)
            b = [0.01 * value / norm for value in raw]
            rows.append({"id": f"Q{len(rows)+1:03}", "background_id": base["id"],
                         "kind": "mixed", "b": b})
    assert len(rows) == 384
    assert all(sum(abs(v) for v in row["b"]) <= 0.010000000001 for row in rows)
    return backgrounds, rows


def make_manifest() -> dict:
    construction_rows, counts = construction()
    holdout_rows = holdout(construction_rows)
    bases, perturbed = perturbations()
    assert all(admissible(row) for row in construction_rows + holdout_rows + bases)
    assert min(row["p"] for row in construction_rows + holdout_rows + bases) >= 0.375 - 1e-10
    assert min(row["q"] for row in construction_rows + holdout_rows + bases) >= 0.375 - 1e-10
    return {
        "schema": "dlw-initial-state-design-v1", "random_seed": SEED,
        "scope": "lambda=-2, regular N=1 finite-h DLW; input design only",
        "parameter_domain": {"S": [1.5, 5], "g": [0.5, 5],
                             "nu": [-0.5, 0.5], "x_c": [-1, 1], "a": [2, 6]},
        "h_values": list(H_VALUES), "construction_counts": counts,
        "construction": construction_rows, "holdout": holdout_rows,
        "perturbation_backgrounds": bases, "perturbations": perturbed,
        "perturbation_definition": {
            "b_l1_max": 0.01,
            "B": "exp(1-1/(1-s^2)) for |s|<1; 0 otherwise",
            "A": "B((x-x_c)/2)*B(y)",
            "scalar_shapes": ["A*cos(x-x_c)", "A*sin(x-x_c)",
                              "A*cos(4*(x-x_c))*cos(pi*y)",
                              "A*sin(4*(x-x_c))*sin(pi*y)"],
            "directions": "u scales: min(S,4/3) for low, min(S,4/(3+pi)) for high; v scales: 4",
            "initialization": "form physical u,v, then P=delta_minus(u), W=v-delta_zero(u)",
            "uniform_initial_density_lower_bound": 0.99},
        "planned_finite_domain": {"x": "[-20,20)", "y": "[-1.5,1.5]",
                                  "h_main": 0.125, "nx_main": 512,
                                  "times": [0.0025, 0.005, 0.01],
                                  "later_times_separate": [0.02, 0.05, 0.1],
                                  "boundary": "periodic x; background-relative quadratic y ghost extrapolation and left base"},
        "status": "no field time evolution or regional error certification performed"
    }


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = make_manifest()
    target = OUTPUT / "manifest.json"
    data = json.dumps(manifest, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    target.write_bytes(data.encode("utf-8"))
    digest = sha256(target.read_bytes()).hexdigest()
    print(f"{target}: 123 construction, 64 holdout, 6 perturbation backgrounds, "
          f"384 perturbations; SHA-256 {digest}")


if __name__ == "__main__":
    main()
