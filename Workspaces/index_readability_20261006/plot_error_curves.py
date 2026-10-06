"""Render Euler error curves from the saved 24-layer error archive."""
from pathlib import Path
import csv
import hashlib
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import MaxNLocator, ScalarFormatter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "Workspaces/dlw_waveform_fields_20261001/revision_euler_crop"
FIG = HERE / "figures"
CASES = {"fig1a": "A", "fig1b": "B", "fig3": "C"}
MESHES = {"fixed": "固定网格", "moving": "移动网格"}
MODELS = ("SD", "SD2", "FD")
FIELDS = ("u", "v")
COLORS = {"SD": "#2676bd", "SD2": "#e68a22", "FD": "#299760"}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return path.relative_to(ROOT).as_posix()


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    font_path = Path("C:/Windows/Fonts/msyh.ttc")
    font_manager.fontManager.addfont(font_path)
    chinese_family = font_manager.FontProperties(fname=font_path).get_name()
    plt.rcParams.update({
        "font.family": chinese_family,
        "font.size": 12,
        "mathtext.fontset": "stix",
        "axes.unicode_minus": False,
        "axes.linewidth": .8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "pdf.fonttype": 42,
        "savefig.facecolor": "white",
    })
    source_archive = SOURCE / "euler_cropped_errors.npz"
    source_csv = SOURCE / "euler_cropped_errors.csv"
    source_json = SOURCE / "euler_plot_validation.json"
    with source_csv.open(encoding="utf-8-sig", newline="") as handle:
        prior_records = list(csv.DictReader(handle))
    prior = {
        (r["case"], r["mesh"], r["model"], r["field"]): r
        for r in prior_records
    }
    assert len(prior) == 36
    curves, curve_records = {}, []
    with np.load(source_archive, allow_pickle=False) as archive:
        x, y = archive["x"], archive["y"]
        assert x.shape == (401,) and y.shape == (24,)
        assert x[0] == -1 and x[-1] == 1 and np.all(np.diff(x) > 0)
        for case in CASES:
            for mesh in MESHES:
                for field in FIELDS:
                    for model in MODELS:
                        key = (case, mesh, model, field)
                        error_key = f"{case}_Euler_{mesh}_{model}_abs_error_{field}"
                        error = archive[error_key]
                        assert error.shape == (24, 401)
                        assert np.all(np.isfinite(error)) and np.all(error >= 0)
                        curve = np.max(error, axis=0)
                        window_peak = float(error.max())
                        curve_peak = float(curve.max())
                        csv_peak = float(prior[key]["cropped_max"])
                        assert curve.shape == (401,)
                        assert curve_peak == window_peak == csv_peak
                        curves[key] = curve
                        curve_records.append({
                            "case": case, "case_label": CASES[case],
                            "method": "Euler", "mesh": mesh,
                            "model": model, "field": field,
                            "source_key": error_key, "points": len(curve),
                            "source_shape": list(error.shape),
                            "curve_peak": curve_peak,
                            "original_window_peak": csv_peak,
                            "peak_difference": abs(curve_peak - csv_peak),
                            "color": COLORS[model], "line_style": "solid",
                        })
    axis_limits = {
        (case, field): max(
            curves[(case, mesh, model, field)].max()
            for mesh in MESHES for model in MODELS
        ) * 1.08
        for case in CASES for field in FIELDS
    }
    figures, fragments = [], []
    for case, label in CASES.items():
        fragments.append(f'<h3>算例 {label}</h3>')
        for mesh, mesh_label in MESHES.items():
            fragments.append('<div class="error-curve-pair">')
            for field in FIELDS:
                fig, ax = plt.subplots(figsize=(8, 4.8))
                fig.subplots_adjust(left=.14, right=.975, bottom=.145, top=.78)
                fig.suptitle(f"算例 {label} · {mesh_label} · {field}", fontsize=15, y=.975)
                for model in MODELS:
                    curve = curves[(case, mesh, model, field)]
                    line, = ax.plot(x, curve, color=COLORS[model],
                                    lw=1.85, ls="-", label=model)
                    assert np.array_equal(line.get_ydata(), curve)
                    assert np.array_equal(line.get_xdata(), x)
                ax.set(xlim=(-1, 1), ylim=(0, axis_limits[(case, field)]),
                       xlabel=r"横坐标 $x$",
                       ylabel=rf"最大绝对误差 $\max_y |{field}_h-{field}_\mathrm{{exact}}|$")
                ax.set_xticks([-1, -.5, 0, .5, 1])
                ax.yaxis.set_major_locator(MaxNLocator(nbins=5, min_n_ticks=4))
                formatter = ScalarFormatter(useMathText=True)
                formatter.set_powerlimits((0, 0))
                formatter.set_useOffset(False)
                ax.yaxis.set_major_formatter(formatter)
                ax.grid(color="#d7dde3", alpha=.72, lw=.6)
                ax.set_axisbelow(True)
                ax.legend(loc="lower center", bbox_to_anchor=(.5, 1.055),
                          ncol=3, frameon=False, fontsize=11,
                          handlelength=2.4, columnspacing=2.4)
                assert len(fig.axes) == 1 and len(ax.lines) == 3
                stem = f"{case}_euler_{mesh}_{field}_error_curve"
                paths = {}
                for ext in ("png", "pdf"):
                    path = FIG / f"{stem}.{ext}"
                    fig.savefig(path, dpi=240)
                    paths[ext] = relative(path)
                plt.close(fig)
                caption = f"算例 {label}，{mesh_label}：{field} 的绝对误差随 x 的变化。"
                fragment = (
                    '<figure class="error-curve">\n'
                    f'  <img src="{paths["png"]}" alt="{caption}" loading="lazy" decoding="async">\n'
                    f'  <figcaption>{caption}</figcaption>\n'
                    '</figure>'
                )
                fragments.append(fragment)
                figures.append({
                    "case": case, "case_label": label, "mesh": mesh,
                    "mesh_label": mesh_label, "field": field,
                    **paths, "caption": caption,
                    "y_limits": [0., float(axis_limits[(case, field)])],
                    "curves": list(MODELS), "axes": 1,
                })
            fragments.append('</div>')
    np.savez_compressed(HERE / "error_curves.npz", x=x,
        **{f"{case}_Euler_{mesh}_{model}_{field}": curve
           for (case, mesh, model, field), curve in curves.items()})
    fragment_header = (
        '<p>在 t = 0.01 时，对每个 x 取 24 个 y 层上的最大绝对误差。'
        '蓝、橙、绿曲线分别表示 SD、SD2、FD；同一算例同一物理场的两种网格共用纵轴尺度。</p>'
    )
    (HERE / "error_curves.fragment.html").write_text(
        fragment_header + "\n" + "\n".join(fragments) + "\n", encoding="utf-8")
    summaries = []
    for case, label in CASES.items():
        for mesh, mesh_label in MESHES.items():
            peak_sets = {}
            for field in FIELDS:
                peaks = {model: float(curves[(case, mesh, model, field)].max())
                         for model in MODELS}
                winner = min(peaks, key=peaks.get)
                peak_sets[field] = {"peak_errors": peaks, "smallest_peak_model": winner}
            summaries.append({"case": case, "case_label": label,
                              "mesh": mesh, "mesh_label": mesh_label,
                              "fields": peak_sets})
    validation = {
        "time": .01, "method": "Euler", "x_interval": [-1., 1.],
        "x_points": 401, "y_layers": 24,
        "definition": "max_y |f_h - f_exact| at each stored x",
        "ordinate_scale": "linear", "curves": 36,
        "png_figures": 12, "pdf_figures": 12,
        "maximum_peak_difference": max(r["peak_difference"] for r in curve_records),
        "source_files": [
            {"path": relative(path), "sha256": sha(path),
             "size_bytes": path.stat().st_size}
            for path in (source_archive, source_csv, source_json)
        ],
        "font": {"family": chinese_family, "path": str(font_path)},
        "curve_records": curve_records, "figures": figures,
        "peak_summary": summaries,
    }
    (HERE / "curve_validation.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "png_figures": 12, "pdf_figures": 12, "curves": 36,
        "points_per_curve": 401,
        "maximum_peak_difference": validation["maximum_peak_difference"],
        "source_sha256": sha(source_archive),
        "peak_summary": summaries,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
