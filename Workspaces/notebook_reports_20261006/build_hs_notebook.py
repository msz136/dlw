"""Build an independent 2HS report from the preserved mathematical source."""
from __future__ import annotations
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = HERE / "before_split" / "Report.ipynb"
DESTINATION = ROOT / "notebook" / "2HS数值分析report.ipynb"


def renumber(text: str) -> str:
    text = re.sub(r"\\tag\{(\d+)\}", lambda m: "\\tag{" + str(int(m[1])-22) + "}", text)
    return re.sub(r"（(\d+)）", lambda m: "（" + str(int(m[1])-22) + "）"
                  if 23 <= int(m[1]) <= 34 else m[0], text)


def markdown(source: str, cell_id: str):
    return nbformat.v4.new_markdown_cell(renumber(source.strip()), id=cell_id)


def code(source: str, cell_id: str):
    return nbformat.v4.new_code_cell(renumber(source), id=cell_id)


def build(include_two: bool = True) -> dict:
    original = nbformat.read(SOURCE, 4)
    source = original.cells[14].source.split("## 2　2HS", 1)[1]
    single = source.split("考虑 $c=1$", 1)[1].split("表 1", 1)[0]
    single = "考虑 $c=1$" + single
    reference, spatial = single.split("**Integrable。**", 1)
    spatial, time = spatial.split("两种系统均用 RK4", 1)
    time, evaluation = time.split("在 $x\\in[-1,1]$", 1)
    specs = {c.id: c.source for c in original.cells if c.id.startswith("hs-")}
    cells = [markdown(
        "# 2HS 数值分析\n\n"
        "以连续单孤子和二孤子为参考，比较可积半离散格式（Integrable）与固定网格中心差分（FD）。"
        "两种空间系统采用相同的 RK4 时间步长，场值在公共物理网格上重构后评价误差。",
        "hs-title",
    ), code(specs["hs-prepare"], "hs-prepare"),
        markdown("## 1　单孤子与初始网格\n\n" + reference, "hs-single-model"),
        code(specs["hs-config"], "hs-config"),
        markdown("辅助坐标 $X$ 到物理坐标 $x$ 的映射严格单调。由 $J=\\partial_Xx>0$ "
                 "反解物理坐标，并用链式法则得到 FD 边界所需的 $m=u_{xx}+2$。", "hs-single-reference"),
        code(specs["hs-reference"], "hs-reference"),
        markdown("## 2　空间离散\n\n**Integrable。**" + spatial, "hs-space-model"),
        code(specs["hs-spatial"], "hs-spatial"),
        markdown("## 3　时间推进\n\n两种系统均用 RK4" + time, "hs-time-model"),
        code(specs["hs-rk4"], "hs-rk4"),
        markdown("两种方案从各自的解析初值推进到同一时刻 $T$。"
                 "Integrable 的物理网格随 $\\dot x=-u$ 运动，FD 的节点位置保持固定。", "hs-evolve-lead"),
        code(specs["hs-evolve"], "hs-evolve"),
        markdown("## 4　单孤子误差与波形\n\n在 $x\\in[-1,1]$" + evaluation +
                 "\n\n密度分别位于 Integrable 的胞元中点与 FD 的节点。"
                 "误差图每段宽 $0.02$，取段内评价点的最大绝对误差；对数图的显示下限不改变误差范数。",
                 "hs-error-model"),
    ]
    error = specs["hs-error"].split("# 仅原配置与原表核对", 1)[0].rstrip()
    error += "\n\nhs_single_summary = {name: dict(Eu=float(r['Eu']), Erho=float(r['Erho']))\n                     for name, r in hs_results.items()}\n"
    cells.append(code(error, "hs-error"))
    cells.append(markdown("在同一物理区间比较数值场与连续解，误差曲线对应上表的最大绝对误差。", "hs-waveform-lead"))
    cells.append(code('''def hs_plot_waveforms(fields, reference, title):
    fig, axes = plt.subplots(2, 2, figsize=(9, 5.5), sharex=True, sharey="row")
    for column, (name, values) in enumerate(fields.items()):
        for row, key in enumerate(("u", "rho")):
            ax = axes[row, column]
            coordinates = values["x"] if key == "u" else values["rhoX"]
            ax.plot(hs_xx, reference[key], "-", color="firebrick", label="Exact")
            mask = (coordinates >= hs_xmin) & (coordinates <= hs_xmax)
            # 稀疏显示数值节点，完整节点仍参与误差评价。
            ids = np.flatnonzero(mask)[::max(1, int(mask.sum()) // 100)]
            ax.plot(coordinates[ids], values[key][ids], ".", markersize=3,
                    label=name, color="royalblue")
            ax.set_title(name if row == 0 else "")
            ax.set_ylabel(r"$u$" if key == "u" else r"$\\rho$")
            if row == 1:
                ax.set_xlabel(r"Physical coordinate $x$")
            ax.grid(alpha=.2)
            ax.legend()
    fig.suptitle(title)
    fig.tight_layout()
    plt.show()

hs_plot_waveforms(hs_live_fields, hs_reference, f"2HS one soliton, t={hs_T:g}")
''', "hs-waveforms"))
    if include_two:
        from hs_two_soliton_cells import build_two_soliton_cells
        cells.extend(build_two_soliton_cells())
    metadata = deepcopy(original.metadata)
    metadata.colab = {"name": DESTINATION.name, "provenance": []}
    metadata.pop("report_conversion", None)
    metadata.report_split = {"source": str(SOURCE), "scope": "2HS numerical analysis"}
    notebook = nbformat.v4.new_notebook(cells=cells, metadata=metadata)
    from revise_hs_structure import transform
    notebook = transform(notebook)
    from hs_presentation import apply_presentation
    notebook = apply_presentation(notebook)
    from plot_range_config import apply_hs_plot_range
    notebook = apply_hs_plot_range(notebook)
    from static_field_plots import apply_hs
    notebook = apply_hs(notebook)
    cells = notebook.cells
    nbformat.validate(notebook)
    nbformat.write(notebook, DESTINATION)
    validation = {"notebook": str(DESTINATION), "cells": len(cells),
                  "code_cells": sum(c.cell_type == "code" for c in cells),
                  "sha256": hashlib.sha256(DESTINATION.read_bytes()).hexdigest(),
                  "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  "native_schema_valid": True, "two_soliton_included": include_two}
    (HERE / "hs_build_validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return validation


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2))
