"""Put 2HS formulas, parameters, and executable scheme code next to each other.

This transformation is used by both the maintained generator and the existing
executed notebook. It only splits and relocates the original Python functions;
the numerical statements, parameters, and later result cells stay unchanged.
"""
from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import uuid

import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
NOTEBOOK = ROOT / "notebook" / "2HS数值分析report.ipynb"

INTEGRABLE = r"""
## 2　空间离散

### 2.1　Integrable

原连续方程为

$$u_{tx}-uu_{xx}-\frac12u_x^2-4u-\frac12(\rho^2-1)=0,
\qquad \rho_t=(u\rho)_x.$$

将辅助坐标 $X\in[-4,4]$ 等分为 $N=1600$ 段，
$X_k=-4+ka$、$a=0.005$；式（2）将 $X=-4,4$ 映为初始物理端点，
区间约为 $[-4.8,\,3.8]$。

令 $d_k=x_{k+1}-x_k$、$b_k=u_{k+1}-u_k$。$c=1$ 时的半离散方程为

$$\begin{aligned}
\dot d_k&=-b_k,\qquad \dot x_0=-u_0(t),\\
\dot b_k&=2d_k(u_{k+1}+u_k)
+\frac{[d_k^2-a(a-1)]^2-b_k^2}{2d_k}-\frac{d_k}{2}.
\end{aligned}\tag{3}$$

取解析左端值 $u_0(t)$，节点及密度按下式递推：

$$u_{k+1}=u_k+b_k,\qquad x_{k+1}=x_k+d_k,\qquad
\rho_{k+1/2}=\frac a{d_k}.\tag{4}$$

参数：$c=1$、$a=0.005$、$N=1600$、$\Delta t=0.003125$、$T=0.5$。
以下代码实现式（4）的恢复与式（3）的右端；RK4 时间递推见第 3 节。
"""

FD = r"""
### 2.2　FD

对式（1）作 $x$ 微分，令 $m=u_{xx}+2$，原方程写成

$$m_t=um_x+2mu_x+\rho\rho_x,\qquad
\rho_t=u\rho_x+\rho u_x,\qquad u_{xx}=m-2.$$

在初始物理端点之间等分 1600 段，$x_i=x_L+i\Delta x$；
物理端点由解析坐标映射在 $X=-4,4$ 处给出，
单孤子、二孤子的区间分别约为 $[-4.8,\,3.8]$、$[-5.7,\,3.7]$。

中心差分及离散方程为

$$(D_1f)_i=\frac{f_{i+1}-f_{i-1}}{2\Delta x},\qquad
(D_2f)_i=\frac{f_{i+1}-2f_i+f_{i-1}}{\Delta x^2}.\tag{5}$$

$$\begin{aligned}
\dot m_i&=u_i(D_1m)_i+2m_i(D_1u)_i+\rho_i(D_1\rho)_i,\\
\dot\rho_i&=u_i(D_1\rho)_i+\rho_i(D_1u)_i,\\
u_{i+1}-2u_i+u_{i-1}&=\Delta x^2(m_i-2).
\end{aligned}\tag{6}$$

参数：$c=1$、$N=1600$、$\Delta t=0.003125$、$T=0.5$；
$\Delta x\approx0.005375$（单孤子）或 $\Delta x\approx0.005886$（二孤子）。
两端取解析值。以下代码先联立求出 $u$，再计算式（6）的时间导数。
"""

GRID = r"""
### 2.3　网格策略与初值

Integrable 的物理网格随 $\dot x=-u$ 运动，FD 保持初始物理节点固定。
两个算例均取 $N=1600$、$a=0.005$，初值为

$$b_k^0=u_{k+1}^0-u_k^0,\qquad d_k^0=x_{k+1}^0-x_k^0,
\qquad m_i^0=(D_2u^0)_i+2,\qquad \rho_i^0=\rho(x_i,0).$$
"""

TIME = r"""
## 3　时间推进

记空间系统为 $\dot z=\mathcal F(t,z)$，时间递推采用 RK4：

$$\begin{aligned}
K_1&=\mathcal F(t_n,z^n),&
K_2&=\mathcal F\!\left(t_n+\frac{\Delta t}{2},z^n+\frac{\Delta t}{2}K_1\right),\\
K_3&=\mathcal F\!\left(t_n+\frac{\Delta t}{2},z^n+\frac{\Delta t}{2}K_2\right),&
K_4&=\mathcal F(t_n+\Delta t,z^n+\Delta tK_3),\\
z^{n+1}&=z^n+\frac{\Delta t}{6}(K_1+2K_2+2K_3+K_4).
\end{aligned}\tag{7}$$

取 $\Delta t=0.003125$、$T=0.5$，共 160 步。每个阶段按式（4）或（6）恢复场值。
"""

ERROR = r"""
## 4　单孤子误差与波形

在 $x\in[-1,1]$ 的 32001 个等距点 $\mathcal G$ 上，线性插值后计算

$$E_u(t)=\max_{x\in\mathcal G}|u_h(x,t)-u(x,t)|,\qquad
E_\rho(t)=\max_{x\in\mathcal G}|\rho_h(x,t)-\rho(x,t)|.\tag{8}$$

以下代码实现插值与误差计算。误差图每段宽 $0.02$，取段内最大绝对误差。
"""


def _source(text: str) -> str:
    return text.strip() + "\n"


TWO_GRID = r"""辅助坐标 $X\in[-4,4]$ 等分 1600 段，$a=0.005$。由二孤子解析坐标映射在 $X=-4,4$ 处得到初始物理端点，区间约为 $[-5.7,\,3.7]$；FD 等分 1600 段，$\Delta x\approx0.005886$。"""


def transform(notebook):
    """Idempotently reorganize an nbformat notebook without executing it."""
    notebook = deepcopy(notebook)
    if any(cell.id == "hs-fd-spatial" for cell in notebook.cells):
        for cell in notebook.cells:
            if cell.id == "hs-space-model":
                cell.source = _source(INTEGRABLE)
            elif cell.id == "hs-fd-model":
                cell.source = _source(FD)
            elif cell.id == "hs-two-grid":
                cell.source = _source(TWO_GRID)
        nbformat.validate(notebook)
        return notebook
    by_id = {cell.id: cell for cell in notebook.cells}
    original = by_id["hs-spatial"]
    tree = ast.parse(original.source)
    lines = original.source.splitlines(keepends=True)
    functions = {
        node.name: "".join(lines[node.lineno - 1:node.end_lineno]).rstrip() + "\n"
        for node in tree.body
    }
    assert set(functions) == {
        "hs_integrable_fields", "hs_integrable_rhs", "hs_recover_u",
        "hs_fd_fields", "hs_fd_rhs", "hs_initial_states", "hs_interpolate",
    }

    def piece(cid, names, inherit=False):
        cell = deepcopy(original) if inherit else nbformat.v4.new_code_cell(id=cid)
        cell.id = cid
        cell.source = "\n".join(functions[name] for name in names)
        return cell

    integrable_code = piece("hs-spatial", ["hs_integrable_fields", "hs_integrable_rhs"], True)
    fd_code = piece("hs-fd-spatial", ["hs_recover_u", "hs_fd_fields", "hs_fd_rhs"])
    initial_code = piece("hs-initial-state", ["hs_initial_states"])
    interpolation_code = piece("hs-interpolation", ["hs_interpolate"])
    updates = {
        "hs-title": "# 2HS 数值分析\n\n比较可积半离散格式（Integrable）与固定网格中心差分（FD）的单孤子、二孤子计算。\n",
        "hs-space-model": _source(INTEGRABLE),
        "hs-time-model": _source(TIME),
        "hs-evolve-lead": "按式（7）从解析初值推进到 $T=0.5$。\n",
        "hs-error-model": _source(ERROR),
        "hs-single-reference": "以下代码给出式（2）的解析场、初始物理节点及 FD 端点。\n",
        "hs-two-grid": _source(TWO_GRID),
        "hs-two-time": "沿用式（3）—（7）的空间系统和 RK4；初值与边界取二孤子解析值。"
                       "取 $\\Delta t=0.003125$、$T=0.5$，共 160 步。\n",
        "hs-two-discussion": "上表比较同一终点、同一物理评价网格上的最大绝对误差。\n",
    }
    single = by_id["hs-single-model"].source
    single = single.split("其中 $\\rho$", 1)[0].rstrip()
    updates["hs-single-model"] = single + "\n\n取 $N=1600$、$a=0.005$；具体空间格式见第 2 节。\n"

    result = []
    for cell in notebook.cells:
        if cell.id in updates:
            cell.source = updates[cell.id]
        if cell.id == "hs-spatial":
            result.extend([
                integrable_code,
                nbformat.v4.new_markdown_cell(_source(FD), id="hs-fd-model"),
                fd_code,
                nbformat.v4.new_markdown_cell(_source(GRID), id="hs-grid-model"),
                initial_code,
            ])
        elif cell.id == "hs-error":
            result.extend([interpolation_code, cell])
        else:
            result.append(cell)
    notebook.cells = result
    notebook.metadata["report_structure"] = {
        "revision": "2026-10-06 formulas-parameters-executable-code",
        "transform": str(Path(__file__).resolve()),
        "numerical_algorithms_unchanged": True,
    }
    nbformat.validate(notebook)
    return notebook


def ast_sequence(notebook):
    return [ast.dump(node, include_attributes=False)
            for cell in notebook.cells if cell.cell_type == "code"
            for node in ast.parse(cell.source).body]


def revise_existing():
    before = nbformat.read(NOTEBOOK, 4)
    after = transform(before)
    before_statements = ast_sequence(before)
    after_statements = ast_sequence(after)
    # Only independent function definitions are moved to their relevant sections.
    assert sorted(before_statements) == sorted(after_statements)
    assert len(before_statements) == len(after_statements)
    before_results = {
        cell.id: (cell.get("execution_count"), cell.get("outputs", []))
        for cell in before.cells if cell.cell_type == "code" and cell.id != "hs-spatial"
    }
    after_results = {
        cell.id: (cell.get("execution_count"), cell.get("outputs", []))
        for cell in after.cells if cell.id in before_results
    }
    assert before_results == after_results
    for cell in after.cells:
        if cell.cell_type == "code":
            compile(cell.source, cell.id, "exec")
    backup = HERE / "before_hs_structure" / (uuid.uuid4().hex + ".ipynb")
    backup.parent.mkdir(exist_ok=True)
    backup.write_bytes(NOTEBOOK.read_bytes())
    nbformat.write(after, NOTEBOOK)
    record = {
        "success": True,
        "notebook": str(NOTEBOOK),
        "backup": str(backup),
        "notebook_sha256": hashlib.sha256(NOTEBOOK.read_bytes()).hexdigest(),
        "cell_count": len(after.cells),
        "code_cell_count": sum(cell.cell_type == "code" for cell in after.cells),
        "python_statements_unchanged": True,
        "existing_result_outputs_preserved": True,
        "schema_and_python_syntax_valid": True,
        "spatial_sections": ["2.1 Integrable", "2.2 FD", "2.3 网格策略与初值"],
    }
    (HERE / "hs_structure_validation.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return record


if __name__ == "__main__":
    revise_existing()
