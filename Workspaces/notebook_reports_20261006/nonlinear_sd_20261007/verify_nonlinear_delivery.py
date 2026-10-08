"""Independent spatial and freshly executed nonlinear SD delivery checks.

Definitions are compiled from the final CELLS mapping used by the notebook.
This audit never executes the historical direct-tau checks or changes their
records. Main-result checks read the native-kernel JSON/NPZ exports and compare
unchanged SD2/FD runs with the pre-nonlinear snapshot.
"""
from pathlib import Path
import argparse
import base64
import hashlib
import itertools
import json
import runpy
import sys
import time

import nbformat
import numpy as np


EVIDENCE = Path(__file__).resolve().parent
HERE = EVIDENCE.parent
ROOT = HERE.parents[1]
NOTEBOOK = ROOT / "notebook/DLW数值分析report.ipynb"
PREVIOUS = HERE / "before_nonlinear_sd_20261007/Workspaces/notebook_reports_20261006"
sys.path.insert(0, str(HERE))


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


def digest_path(path):
    return digest_bytes(path.read_bytes())


def definitions():
    cells = runpy.run_path(str(HERE / "dlw_numeric_cells.py"))["CELLS"]
    ns = {}
    keys = ("imports", "config", "reference", "spatial", "sd_fd", "sd", "fd",
            "sd2_lift", "sd2_evolution", "mesh", "time")
    for key in keys:
        exec(compile(cells[key], "dlw-" + key, "exec"), ns)
    return ns, cells, {"dlw-" + key: digest_bytes(cells[key].strip().encode()) for key in keys}


def maximum(values):
    return float(np.max(np.abs(values)))


def relative_difference(actual, expected):
    return maximum(actual - expected) / max(1.0, maximum(expected))


def observed_orders(errors):
    return [float(np.log2(a / b)) for a, b in zip(errors[:-1], errors[1:])]


def explicit_derivatives(values, spacing, jacobian, jump=0.0):
    """Roll and ghost-value arithmetic, independent of sparse Grid matrices."""
    left = np.roll(values, 1, axis=-1).copy()
    right = np.roll(values, -1, axis=-1).copy()
    left[..., :1] -= jump
    right[..., -1:] += jump
    dxi = (right - left) / (2 * spacing)
    dxxi = (right - 2 * values + left) / spacing**2
    jxi = (np.roll(jacobian, -1) - np.roll(jacobian, 1)) / (2 * spacing)
    return dxi / jacobian, dxxi / jacobian**2 - jxi * dxi / jacobian**3


def check_uniform(ns):
    rows, symbols = [], []
    for n in (64, 128, 256):
        grid = ns["Grid"](n, 2 * np.pi)
        for mode in (1, 3, n // 2):
            theta = 2 * np.pi * mode / n
            values = ((-1.0)**np.arange(n) if mode == n // 2 else
                      np.exp(1j * theta * np.arange(n)))
            expected_first = 1j * np.sin(theta) / grid.dx * values
            expected_second = -4 * np.sin(theta / 2)**2 / grid.dx**2 * values
            first = relative_difference(grid.d1(values), expected_first)
            second = relative_difference(grid.d2(values), expected_second)
            assert max(first, second) < 3e-12, (n, mode, first, second)
            symbols.append(dict(nx=n, mode=mode,
                D1_symbol_scaled_error=first, D2_symbol_scaled_error=second))
            if mode == n // 2:
                direct = maximum(grid.d2(values))
                composed = maximum(grid.d1(grid.d1(values)))
                assert direct > 1 and composed < 1e-20
        values = np.sin(3 * grid.xi)
        rows.append(dict(nx=n,
            D1_error=maximum(grid.d1(values) - 3 * np.cos(3 * grid.xi)),
            D2_error=maximum(grid.d2(values) + 9 * values)))
    orders = {key: observed_orders([r[key] for r in rows])
              for key in ("D1_error", "D2_error")}
    assert all(1.9 < p < 2.1 for values in orders.values() for p in values), orders
    return dict(rows=rows, observed_orders=orders, symbols=symbols,
        D1_symbol="i sin(theta)/d", D2_symbol="-4 sin(theta/2)^2/d^2",
        Nyquist_distinguishes_direct_D2_from_composed_D1=True)


def check_moving(ns):
    rows = []
    for n in (64, 128, 256):
        grid = ns["Grid"](n, 2 * np.pi)
        grid.set_s(0.16 * np.sin(grid.xi) + 0.05 * np.sin(2 * grid.xi))
        exact_j = 1 + 0.16 * np.cos(grid.xi) + 0.1 * np.cos(2 * grid.xi)
        values = np.sin(2 * grid.x) + 0.2 * np.cos(3 * grid.x)
        exact_first = 2 * np.cos(2 * grid.x) - 0.6 * np.sin(3 * grid.x)
        exact_second = -4 * np.sin(2 * grid.x) - 1.8 * np.cos(3 * grid.x)
        independent = explicit_derivatives(values, grid.dx, grid.J)
        first_difference = relative_difference(grid.d1(values), independent[0])
        second_difference = relative_difference(grid.d2(values), independent[1])
        assert max(first_difference, second_difference) < 3e-12
        # The SD2 additive endpoint jump uses the same direct three-point D2.
        lifted = np.stack((values + 0.2 * grid.xi, 2 * values - 0.1 * grid.xi))
        jumps = np.array([[0.2 * grid.L], [-0.1 * grid.L]])
        lift_expected = explicit_derivatives(lifted, grid.dx, grid.J, jumps)
        lift_first = relative_difference(grid.d1(lifted, jumps), lift_expected[0])
        lift_second = relative_difference(grid.d2(lifted, jumps), lift_expected[1])
        assert max(lift_first, lift_second) < 3e-12
        rows.append(dict(nx=n, min_J=float(grid.J.min()),
            J_error=maximum(grid.J - exact_j),
            D1_error=maximum(grid.d1(values) - exact_first),
            D2_error=maximum(grid.d2(values) - exact_second),
            D1_explicit_scaled_error=first_difference,
            D2_explicit_scaled_error=second_difference,
            jump_D1_explicit_scaled_error=lift_first,
            jump_D2_explicit_scaled_error=lift_second))
    orders = {key: observed_orders([r[key] for r in rows])
              for key in ("J_error", "D1_error", "D2_error")}
    assert all(1.85 < p < 2.15 for values in orders.values() for p in values), orders
    return dict(rows=rows, observed_orders=orders,
        mapping="x=xi+0.16 sin(xi)+0.05 sin(2xi)",
        field="sin(2x)+0.2 cos(3x)")


def spatial_validation(ns, source_hashes):
    record = dict(success=True, uniform=check_uniform(ns), moving=check_moving(ns),
        namespace_source="final dlw_numeric_cells.CELLS",
        independent_ghost_arithmetic=True,
        notebook_definition_sources_sha256=source_hashes)
    path = EVIDENCE / "spatial_validation.json"
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return record


def check_delivery(ns, cells, definition_hashes, spatial):
    results_path = HERE / "dlw_numeric_results.json"
    curves_path = HERE / "dlw_numeric_curves.npz"
    execution_path = HERE / "dlw_execution_validation.json"
    data = json.loads(results_path.read_text("utf-8"))
    key_of = lambda r: tuple(r[k] for k in ("case", "model", "method", "mesh"))
    rows = {key_of(r): r for r in data["rows"]}
    expected = set(itertools.product(ns["CASES"], ns["MODELS"],
                                     ("Euler", "RK4"), ("fixed", "moving")))
    assert len(data["rows"]) == len(rows) == 36 and set(rows) == expected
    end = ns["CONFIG"]["T"]
    assert all(r["completed"] and abs(r["reached"] - end) < 1e-13 for r in rows.values())
    assert all(r["min_J"] > 0 and set(r["errors"]) == {"u", "v"}
        and np.isfinite(list(r["errors"].values())).all()
        and min(r["errors"].values()) >= 0 for r in rows.values())
    assert max(r["initial_error"] for r in rows.values()) < 1e-9

    refinements = data["refinement_rows"]
    refinement_keys = {(r["case"], r["model"], r["method"], r["mesh"], r["dt"])
                       for r in refinements}
    expected_refinements = {(case, model, "Euler", "fixed", ns["CONFIG"]["dt"] / divisor)
        for case, model, divisor in itertools.product(ns["CASES"], ("SD", "SD2"), (2, 4))}
    assert len(refinements) == len(refinement_keys) == 12
    assert refinement_keys == expected_refinements
    assert all(r["completed"] and abs(r["reached"] - end) < 1e-13 and r["min_J"] > 0
               for r in refinements)
    orders = data["order_rows"]
    order_keys = {(r["算例"], r["方案"], r["场"]) for r in orders}
    assert len(orders) == len(order_keys) == 12
    assert order_keys == set(itertools.product(ns["CASES"], ("SD", "SD2"), ("u", "v")))
    for r in orders:
        assert r.get("时间算法", "Euler") == "Euler"
        first, second = r["dt 与 dt/2 场差"], r["dt/2 与 dt/4 场差"]
        assert first > 0 and second > 0
        assert np.isclose(r["观测阶"], np.log2(first / second), rtol=0, atol=1e-12)
    order_ranges = {}
    for model in ("SD", "SD2"):
        values = [r["观测阶"] for r in orders if r["方案"] == model]
        assert all(0.85 < p < 1.15 for p in values), (model, values)
        order_ranges[model] = [min(values), max(values)]

    curve_comparisons = []
    with np.load(curves_path) as curves:
        expected_keys, reference_x = set(), None
        for key, row in rows.items():
            label = "_".join(key)
            expected_keys.update(label + suffix for suffix in ("_x", "_u_curve", "_v_curve"))
            x = curves[label + "_x"]
            assert x.shape == (ns["CONFIG"]["eval_points"],)
            assert np.isfinite(x).all() and np.diff(x).min() > 0
            assert x[0] == -ns["CONFIG"]["eval_half"] and x[-1] == ns["CONFIG"]["eval_half"]
            if reference_x is None:
                reference_x = x.copy()
            assert np.array_equal(x, reference_x)
            for field in ("u", "v"):
                curve = curves[label + "_" + field + "_curve"]
                assert curve.shape == x.shape and np.isfinite(curve).all() and curve.min() >= 0
                maximum_value = float(curve.max())
                difference = abs(maximum_value - row["errors"][field])
                assert maximum_value == row["errors"][field], (key, field, difference)
                curve_comparisons.append(difference)
        assert set(curves.files) == expected_keys

        previous = json.loads((PREVIOUS / "dlw_numeric_results.json").read_text("utf-8"))
        old_rows = {key_of(r): r for r in previous["rows"] if r["model"] in ("SD2", "FD")}
        common_keys = set(old_rows) & set(rows)
        assert len(common_keys) == 18
        unchanged = []
        with np.load(PREVIOUS / "dlw_numeric_curves.npz") as old_curves:
            for key in sorted(common_keys):
                current, old = rows[key], old_rows[key]
                scalar_difference = max(abs(current["errors"][f] - old["errors"][f]) for f in ("u", "v"))
                assert current["errors"] == old["errors"], (key, scalar_difference)
                assert current["initial_error"] == old["initial_error"]
                assert current["min_J"] == old["min_J"]
                label = "_".join(key)
                curve_difference = 0.0
                for suffix in ("_x", "_u_curve", "_v_curve"):
                    current_curve, old_curve = curves[label + suffix], old_curves[label + suffix]
                    curve_difference = max(curve_difference, maximum(current_curve - old_curve))
                    assert np.array_equal(current_curve, old_curve), (key, suffix, curve_difference)
                unchanged.append(dict(key=key, maximum_scalar_difference=scalar_difference,
                                      maximum_curve_difference=curve_difference))

    notebook = nbformat.read(NOTEBOOK, as_version=4)
    nbformat.validate(notebook)
    by_id = {c.id: c for c in notebook.cells}
    code_hashes = {}
    for name, source in cells.items():
        cell = by_id["dlw-" + name]
        assert cell.cell_type == "code" and cell.source.strip() == source.strip(), name + " is stale"
        code_hashes[cell.id] = digest_bytes(cell.source.encode())
    assert all(code_hashes[name] == digest for name, digest in definition_hashes.items())
    all_hashes = {c.id: digest_bytes(c.source.encode()) for c in notebook.cells}
    execution = json.loads(execution_path.read_text("utf-8"))
    notebook_hash = digest_path(NOTEBOOK)
    results_hash, curves_hash = digest_path(results_path), digest_path(curves_path)
    assert execution["success"] and execution["sources_unchanged"] and execution["outputs_saved"]
    assert execution["independent_native_kernel"]
    assert execution["notebook_sha256"] == notebook_hash
    assert execution["source_hashes"] == data["source_hashes"] == all_hashes
    assert execution["exported_results_sha256"] == results_hash
    assert execution["exported_curves_sha256"] == curves_hash
    assert any(r["cell"] == "dlw-validation-export" for r in execution["timings"])
    assert "class SDModel(PhysicalModel)" in by_id["dlw-sd"].source
    assert "def rhs" in by_id["dlw-sd"].source
    assert "candidate = step(p.stage" in by_id["dlw-time"].source
    assert "Midpoint" not in "\n".join(c.source for c in notebook.cells)
    assert "for model in ('SD', 'SD2')" in by_id["dlw-order"].source
    assert "calculate('Euler', 'moving')" in by_id["dlw-curves"].source

    figures = []
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        assert cell.execution_count is not None
        assert not any(o.output_type == "error" for o in cell.outputs)
        for out in cell.outputs:
            if "image/png" in out.get("data", {}):
                blob = base64.b64decode(out.data["image/png"])
                assert blob.startswith(b"\x89PNG\r\n\x1a\n")
                path = EVIDENCE / ("dlw_notebook_figure_%d.png" % (len(figures) + 1))
                path.write_bytes(blob)
                figures.append(dict(path=str(path), sha256=digest_bytes(blob), cell=cell.id))
    assert len(figures) == execution["image_outputs"] == 3
    modules = ("dlw_numeric_cells.py", "sd_nonlinear_cell.py", "execute_dlw_notebook.py",
               "build_dlw_numerics_notebook.py", "revise_dlw_structure.py")
    return dict(success=True, primary_runs=len(rows), temporal_refinement_runs=len(refinements),
        initial_maximum_evaluation_node_error=max(r["initial_error"] for r in rows.values()),
        scalar_curve_maxima_comparisons=len(curve_comparisons),
        maximum_scalar_curve_difference=max(curve_comparisons),
        euler_order_ranges=order_ranges, diagrams=len(figures),
        code_cells=sum(c.cell_type == "code" for c in notebook.cells), all_code_executed=True,
        minimum_final_J=min(r["min_J"] for r in rows.values()),
        sd_results=[r for r in data["rows"] if r["model"] == "SD"],
        unchanged_SD2_FD_runs=unchanged,
        notebook_sha256=notebook_hash, notebook_code_sources_sha256=code_hashes,
        exported_results_sha256=results_hash, exported_curves_sha256=curves_hash,
        native_execution_sha256=digest_path(execution_path),
        independent_spatial_audit_sha256=digest_path(EVIDENCE / "spatial_validation.json"),
        uniform_orders=spatial["uniform"]["observed_orders"],
        moving_orders=spatial["moving"]["observed_orders"],
        source_modules_sha256={name: digest_path(HERE / name) for name in modules},
        fresh_native_exports_checked=True, figures=figures)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spatial-only", action="store_true")
    args = parser.parse_args()
    start = time.perf_counter()
    ns, cells, hashes = definitions()
    spatial = spatial_validation(ns, hashes)
    if args.spatial_only:
        print(json.dumps(dict(success=True, uniform_orders=spatial["uniform"]["observed_orders"],
            moving_orders=spatial["moving"]["observed_orders"], seconds=time.perf_counter()-start)))
        return
    record = check_delivery(ns, cells, hashes, spatial)
    record["seconds"] = time.perf_counter() - start
    path = EVIDENCE / "delivery_validation.json"
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: record[key] for key in ("success", "primary_runs", "temporal_refinement_runs",
        "maximum_scalar_curve_difference", "euler_order_ranges", "minimum_final_J", "seconds")},
        ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
