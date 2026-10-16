"""Split the nonlinear reading flow from the preserved combined report."""
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
DESTINATION = ROOT / "notebook" / "非线性化report.ipynb"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


UW_RESIDUAL_DEFINITIONS = """-- 式（7）的两个通量与两个残差，定义与证明库一致。
namespace DLWContract.ReportUW.NotebookDisplay

def fluxUW (a h : ℝ) (u w : Lattice) : Lattice :=
  (u ^ 2 + w ^ 2) / 2 + (2 * a) • u - h • w

def fluxOmega (a h : ℝ) (u w : Lattice) : Lattice :=
  (u + CC a) * w - h • u

def reportN1 (a h : ℝ) (u w : Lattice) : Lattice :=
  dm h (lt u) + lx (dm h (fluxUW a h u w)) +
    lxx (dm h u + (4 / h) • mm w)

def reportN2 (a h : ℝ) (u w : Lattice) : Lattice :=
  lt w + lx (fluxOmega a h u w) - lxx w

theorem reportN1_matches (a h : ℝ) (u w : Lattice) :
    reportN1 a h u w = DLWContract.ReportUW.reportN1 a h u w := rfl

theorem reportN2_matches (a h : ℝ) (u w : Lattice) :
    reportN2 a h u w = DLWContract.ReportUW.reportN2 a h u w := rfl

#print reportN1
#print reportN2

end DLWContract.ReportUW.NotebookDisplay

"""

UW_RESIDUAL_EXPLANATION = """\n\n下列代码先写出式（7）的两个通量和左端残差，再证明它们为零。`reportN1`、`reportN2` 分别对应式（7）的第一行、第二行；代码中的 `w` 即 $\\omega$。

| Lean 写法 | 公式中的含义 |
| --- | --- |
| `lt z`、`lx z`、`lxx z` | $\\partial_t z$、$\\partial_x z$、$\\partial_x^2 z$ |
| `dm h z`、`mm z` | $\\delta_-z$、$M_-z$ |
| `fluxUW a h u w` | $(u^2+\\omega^2)/2+2au-h\\omega$ |
| `fluxOmega a h u w` | $(u+2a)\\omega-hu$，其中 `CC a` 是常数场 $2a$ |
| `c • z` | 常数 $c$ 与格点场 $z$ 的乘积 |

显示定义置于 `NotebookDisplay` 命名空间；两条 `:= rfl` 等式核对它们与证明库中的原定义完全相同。`#print` 输出残差的定义，后面的 `example` 检查由 `StartPoint` 到两个残差为零的推论。"""


def add_uw_definitions(cells) -> None:
    """Expose the actual report (7) residuals without adding a runtime stage."""
    by_id = {cell.id: cell for cell in cells}
    code = by_id["lean-uw"]
    anchor = "-- 式（7）：u 与 ω 的两条演化方程。"
    if "namespace DLWContract.ReportUW.NotebookDisplay" not in code.source:
        assert anchor in code.source
        code.source = code.source.replace(anchor, UW_RESIDUAL_DEFINITIONS + anchor, 1)
    text = by_id["report-text-04"]
    if "显示定义置于 `NotebookDisplay`" not in text.source:
        text.source += UW_RESIDUAL_EXPLANATION


def build() -> dict:
    original = nbformat.read(SOURCE, as_version=4)
    cells = deepcopy(original.cells[:14])
    cells[0].source = (
        "# DLW 半离散系统的非线性化\n\n"
        "从交错格点上的双线性方程出发，分别得到消去辅助势的两场形式与保留势的比值形式。"
        "中间的恒等变换以公式展开，Lean 中的起点和终点对应两条推导路线。"
        "最后将连续单孤子代入半离散方程，比较空间残差、二阶主系数及格距收敛。\n\n"
        "证明所需的定义与定理来自已有的本地 Lean 证明库。"
    )
    cells[1].source = cells[1].source.replace(
        "# @title 载入本地 Lean 证明库", "# 载入非线性化证明所需的本地 Lean 环境。"
    )
    cleanup = (
        "`def StartPoint` 写出式（1）的两条双线性假设；`#print StartPoint` 将这一定义输出。"
        "起点到终点的证明在后面的终点代码块中调用。\n\n"
        "`namespace` 组织名称，`section` 管理作用域，`noncomputable section` 允许使用精确实数函数；"
        "这些声明负责组织代码。\n\n"
    )
    for cell in cells:
        if cell.cell_type == "markdown":
            cell.source = cell.source.replace(cleanup, "")
            cell.source = cell.source.replace(
                "将理论的双线性起点写为 StartPoint，供下一段定理调用使用。",
                "在 Lean 中，两条双线性假设合并为 `StartPoint`：",
            )
            cell.source = cell.source.replace(
                "在 h≠0、F/G 严格为正且联合实解析的条件下，从 StartPoint 推出式 (7)、(8)，并显示原始公理依赖。",
                "假设 $h\\ne0$，$F,G$ 严格为正且关于 $(x,t)$ 联合实解析。"
                "`StartPoint` 与证明库中的 `SemiPair` 具有相同定义，由此得到式（7）、（8）。",
            )
            cell.source = cell.source.replace(
                "在 h≠0、F/G 严格为正且联合实解析的条件下，从 StartPoint 推出式 (21)，给出式 (22) 的重构恒等式，并显示原始公理依赖。",
                "沿用相同的正则性、正性与 $h\\ne0$ 假设，式（21）由双线性起点推出；"
                "式（22）给出物理场的重构恒等式。",
            )
        else:
            cell.source = cell.source.replace("-- (7): equations for u and ω.", "-- 式（7）：u 与 ω 的两条演化方程。")
            cell.source = cell.source.replace("-- (8): the reconstructed pair (u, v).", "-- 式（8）：重构后的物理场 (u, v)。")
            cell.source = cell.source.replace(
                "-- (21): equations for Q and R, and the lattice constraint.",
                "-- 式（21）：Q、R 的演化方程与格点约束。",
            )
            cell.source = cell.source.replace("-- (22): reconstruction of u, ω and v.", "-- 式（22）：由 Q、R、M 重构 u、ω、v。")

    add_uw_definitions(cells)

    bridge = deepcopy(original.cells[14])
    bridge.source = bridge.source.split("## 2　2HS", 1)[0].strip()
    cells.append(bridge)

    consistency = deepcopy(original.cells[28])
    consistency.id = "nonlinear-consistency-intro"
    consistency.metadata.id = consistency.id
    consistency.source = "## 2　DLW 空间残差与一致性\n\n" + consistency.source.split(
        "## 3　DLW 空间误差估计的现场计算\n\n", 1
    )[1]
    consistency.source = consistency.source.replace(
        "这里现场计算 DLW 的纵向空间截断误差：",
        "考察 DLW 的纵向空间截断误差：",
    ).replace(
        "*计算对象是方程残差，不是第 2 节 2HS 演化至终点的总场误差。*",
        "这里的残差衡量连续解对离散方程的相容程度，演化误差还取决于时间离散与稳定性。",
    )
    consistency.source = consistency.source.split("先准备数值环境", 1)[0].rstrip()
    consistency.source += (
        "\n\n采样最大值取自指定的相位区间，解析上界覆盖整个实相位轴。"
        "减半格距时，$\\|\\mathcal R_h/h^2-\\tau_y\\|$ 应约缩小至四分之一。"
        "推导见 [DLW 误差理论](../report/dlw_error_theory.html)。"
    )
    cells.append(consistency)
    cells.extend(deepcopy(original.cells[29:]))

    leads = {
        "report-text-16": "取原文参数 A：$(a,p,q)=(2,1,2)$，相位区间为 $[-10,10]$。"
        "纵向格距从 $h=1/8$ 开始逐次减半，横向和时间导数保持解析。",
        "report-text-17": "sigmoid 的各阶导数写成 $s(1-s)$ 与多项式的乘积。"
        "这一递推同时给出连续剖面和残差主系数所需的解析导数。",
        "report-text-18": "将连续剖面代入截断展开，得到 SD 与 FD 的二阶主系数。"
        "下列上界使用 sigmoid 导数在全部实相位上的极值。",
        "report-text-19": "有限格距残差直接由离散方程左端求值。"
        "第一条方程取交错中点，第二条取原节点；每个偏移节点均按 $W=v-\\delta_0u$ 重构。",
        "report-text-20": "比较采样主系数与全波形解析上界，并检查同一剖面对连续 DLW 方程的残差。",
        "report-text-21": "逐次减半格距，比较 $\\mathcal R_h/h^2$ 与 $\\tau_y$。"
        "表中的收敛阶来自相邻格距的差值，曲线展示最细格距下的缩放残差与主系数。",
    }
    for cell in cells:
        if cell.id in leads:
            cell.source = leads[cell.id]
        if cell.cell_type == "code":
            cell.execution_count = None
            cell.outputs = []

    cells.append(nbformat.v4.new_markdown_cell(
        "式（7）、（8）与式（21）、（22）给出同一双线性起点的两种非线性表示。"
        "空间残差比较反映这些方程在连续单孤子上的二阶相容性；"
        "不同参数下的系数大小与演化至有限时间后的场误差需要分别考察。\n\n"
        "孤子演化的数值比较见 [DLW 数值分析](DLW数值分析report.ipynb)。",
        id="nonlinear-conclusion",
    ))
    metadata = deepcopy(original.metadata)
    metadata.colab = {"name": DESTINATION.name, "provenance": []}
    metadata.report_split = {
        "source": str(SOURCE), "source_sha256": sha256(SOURCE.read_bytes()),
        "title": "非线性化 report", "numerical_scope": "DLW longitudinal consistency residuals",
    }
    notebook = nbformat.v4.new_notebook(cells=cells, metadata=metadata)
    nbformat.validate(notebook)
    DESTINATION.parent.mkdir(exist_ok=True)
    nbformat.write(notebook, DESTINATION)

    text = "\n".join(c.source for c in cells if c.cell_type == "markdown")
    expected = set(str(i) for i in range(1, 23))
    equation_tags = set(re.findall(r"\\tag\{(\d+)\}", text))
    assert equation_tags == expected, equation_tags
    assert "2HS 单孤子" not in text
    assert "现场" not in text
    assert not any(c.id.startswith("hs-") for c in cells)
    assert sum(c.cell_type == "code" for c in cells) == 14
    original_numerical = {c.id: c.source for c in original.cells if c.id.startswith("error-")}
    assert original_numerical == {c.id: c.source for c in cells if c.id.startswith("error-")}
    validation = {
        "notebook": str(DESTINATION), "source": str(SOURCE),
        "source_sha256": sha256(SOURCE.read_bytes()),
        "built_sha256": sha256(DESTINATION.read_bytes()),
        "cells": len(cells), "code_cells": 14, "lean_cells": 6,
        "numbered_equations_preserved": sorted(equation_tags, key=int),
        "original_dlw_numeric_sources_preserved": True,
        "two_hs_removed": True, "schema_valid": True,
    }
    (HERE / "nonlinear_build_validation.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return validation


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2))
