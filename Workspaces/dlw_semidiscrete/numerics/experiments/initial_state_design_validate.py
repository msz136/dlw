"""Cross-check the frozen design against the existing finite-h Gram evaluator."""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "experiments"), str(ROOT / "lib")]

from initial_state_design import H_VALUES, field_at, initial_state, make_manifest
from parametric import Exact, Parameters


def main() -> None:
    path = ROOT / "design" / "manifest.json"
    saved = json.loads(path.read_text(encoding="utf-8"))
    expected = make_manifest()
    assert saved == expected, "manifest differs from frozen generator"
    assert (len(saved["construction"]), len(saved["holdout"]),
            len(saved["perturbation_backgrounds"]),
            len(saved["perturbations"])) == (123, 64, 6, 384)
    all_rows = (saved["construction"] + saved["holdout"]
                + saved["perturbation_backgrounds"])
    assert len({(r["S"], r["g"], r["nu"], r["x_c"])
                for r in saved["construction"] + saved["holdout"]}) == 187

    max_field_diff = 0.0
    max_init_density_gap = 0.0
    for row in all_rows:
        for h in H_VALUES:
            pars = Parameters(a=row["a"], p=row["p"], q=row["q"],
                              rho=row["rho_gram"])
            exact = Exact(pars, h)
            for j in (-2, 0, 2):
                for x in (row["x_c"] - 0.8, row["x_c"], row["x_c"] + 0.8):
                    u, v = field_at(row, h, j, x)
                    ue, ve = exact.uv([j], [x], 0)
                    max_field_diff = max(max_field_diff, abs(u - ue[0, 0]),
                                         abs(v - ve[0, 0]))
    assert max_field_diff < 2e-12, max_field_diff

    backgrounds = {r["id"]: r for r in saved["perturbation_backgrounds"]}
    for case in saved["perturbations"]:
        base = backgrounds[case["background_id"]]
        # Sampled check only; the analytic 0.99 bound is established in the
        # design report from ||B'|| <= 3 and the l1 coefficient constraint.
        state = initial_state(base, 0.125, list(range(-12, 12)),
                              [base["x_c"] - 0.5, base["x_c"],
                               base["x_c"] + 0.5], case["b"])
        for Wrow in state["W"]:
            for W in Wrow:
                density = 1 - W / 4
                max_init_density_gap = max(max_init_density_gap,
                                           max(0.0, 0.99 - density))
    assert max_init_density_gap == 0.0
    print(f"PASS: 187 distinct construction/holdout backgrounds; "
          f"3 h values, 384 perturbations; max Gram field difference "
          f"{max_field_diff:.3e}; sampled density >= 0.99")


if __name__ == "__main__":
    main()
