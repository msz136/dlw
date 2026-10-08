"""Revise report prose while preserving the executed notebook verbatim otherwise."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil

import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REVISION = HERE / "prose_revision"
NAME = "DLW刘维尔可积性report.ipynb"
BUILDER = HERE / "build_integrability_notebook.py"
DELIVERY = ROOT / "notebook" / NAME
MIRROR = HERE / NAME

REPLACEMENTS = [
    ("从真实光滑周期场和原 DLW 方程出发，构造同一个全阶谱族，依次证明守恒、对易和任意有限前缀的泛型独立性。关键定义与结论在下方写成 Lean 代码；系数递推、积分微分和长篇算子证明由已验证的证明库提供。",
     "从光滑周期场和 DLW 方程出发，构造全阶谱族，依次证明守恒性、对易性与有限前缀的泛型独立性。"),
    ("        本文使用显式的形式 PDO 基础参数 `FactorSpectralFoundation`。最终结论是带这一基础前提的周期场可积性结论；独立性针对每个有限前缀各自的开稠密集。\n\n", ""),
    ("\n\n        使用本地 Python 内核，先运行载入单元，再按阅读顺序点击 ▶。输出框保存 Lean 的原始声明类型与公理依赖。", ""),
    ("## 1. 周期格点与真实场", "## 1. 周期格点与物理场"),
    ("Adler 接口中的形式 PDO 元素，不是物理坐标", "Adler 接口中的形式 PDO 元素"),
    ("以下代码显示库中的参数、周期场与闭合物理场定义，并核验式（1）。", "以下代码显示参数、周期场与闭合物理场的定义，并给出式（1）中的闭合条件。"),
    ("是相同零均值场对的线性空间", "是由这类零均值场对组成的线性空间"),
    ("下面的 `U`、`w` 对应式（2），`rfl` 核对它们与原定义完全一致。重构定理说明任意满足式（1）的物理场都能恢复，没有额外缩小物理起点。",
     "`U`、`w` 对应式（2），`reconstruction` 给出物理场的坐标重构。"),
    ("本文保留一个显式基础参数：每个闭合场都有同一套形式 PDO 表示、所需逆元、循环留数迹、真实方向导数的系数源表示，以及自由一阶因子的标准 Adler 乘积／求逆规则。",
     "形式 PDO 的基础结构包括：每个闭合场的兼容表示、所需逆元、循环留数迹、场的方向导数的系数源表示，以及自由一阶因子的标准 Adler 乘积／求逆规则。"),
    ("守恒、对易、能量身份和独立性由后续定理推导，不是这些结构的目标假设。形式 $D^{-1}$ 不被解释为周期函数上的实际积分逆算子。",
     ""),
    ("以下代码显示准确的基础接口。后面出现的 `foundation.toActual` 是已证明的接口转换。",
     "以下代码展示基础接口，`foundation.toActual` 将其转换为后续定理使用的场接口。"),
    ("以下 `C` 正是实际场上的多项式积分定义", "以下 `C` 给出场上的多项式积分定义"),
    ("`traceIdentification` 核验式（7）", "`traceIdentification` 给出式（7）"),
    ("## 6. 实际 Hamiltonian 与最终族", "## 6. Hamiltonian 与最终族"),
    ("第一留数的真实系数计算给出", "第一留数的系数计算给出"),
    ("它们均与库定义核对。`energyIdentity` 是式（9）的结论，不需要把能量身份作为前提。",
     "`energyIdentity` 对应式（9）。"),
    ("实际约化演化由", "约化演化由"),
    ("使用真实变分配对", "使用变分配对"),
    ("`chargeDifferential` 说明 Euler 梯度确实表示实际场积分的方向导数：",
     "`chargeDifferential` 给出 Euler 梯度所表示的场积分方向导数："),
    ("这里 `gradientCovector` 是真实微分的线性形式", "这里 `gradientCovector` 是泛函微分的线性形式"),
    ("真实时空链式法则", "时空链式法则"),
    ("证明库将式（12）的积分微分与括号消去封装为已有定理；每个可见结论仍完整写出其条件和目标。",
     "证明库封装了式（12）中的积分微分与括号计算。"),
    ("已证明的因子坐标和投影变换将其传到真实约化括号", "因子坐标和投影变换将其传到约化括号"),
    ("把两个零括号结论完整写出", "分别给出两个零括号结论"),
    ("`topCoefficient` 显示式（15）的实际最高系数；该系数由正规乘法和求逆的二阶 jet 推导，未作为独立性的假设。",
     "`topCoefficient` 给出式（15）的最高系数，由正规乘法和求逆的二阶 jet 推导。"),
    ("## 11. 独立性：真实 Jacobian 非零", "## 11. 独立性：Jacobian 非零子式"),
    ("定义实际微分矩阵", "定义泛函微分矩阵"),
    ("真实行列式的首个可能系数", "行列式的首个可能系数"),
    ("以下定理的目标就是式（16），没有预先假设满秩或非零子式。", "`nonzeroJacobian` 对应式（16）。"),
    ("再加入真实 $s$ 方向", "再加入 $s$ 方向"),
    ("以下两个定理只保留形式 PDO 基础参数，见证、最高系数和非零 Jacobian 已由证明消去。",
     "`oddGeneric` 与 `familyGeneric` 分别对应式（17）和式（18）。"),
    ("包含实际物理 Hamiltonian 的最终族", "包含物理 Hamiltonian 的最终族"),
    ("最后的 `periodicIntegrability` 正是从基础前提到这一结论的主定理", "`periodicIntegrability` 给出主定理"),
    ("\n\n        此处没有进一步断言所有有限块在同一个稠密可数交上同时独立，也没有构造全局作用量—角变量或紧不变环面。`#print axioms` 显示 Lean 的原始公理依赖；数学基础前提始终保留在主定理类型中。", ""),
    ("。笔记本中的长证明来自同一套本地源码，当前可见定义与结论由各个代码单元分别核验。", "。"),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def math_expressions(notebook):
    return {
        c.id: re.findall(r"\$\$[\s\S]*?\$\$|(?<!\$)\$[^\n$]+\$(?!\$)", c.source)
        for c in notebook.cells if c.cell_type == "markdown"
    }


def main():
    assert not (REVISION / "validation.json").exists(), "Completed revision evidence already exists."
    assert DELIVERY.read_bytes() == MIRROR.read_bytes()
    before = nbformat.read(DELIVERY, 4)
    backup = REVISION / "before"
    original_builder = (backup / BUILDER.name if backup.exists() else BUILDER).read_text(encoding="utf-8")
    rewritten = original_builder
    for old, new in REPLACEMENTS:
        assert rewritten.count(old) == 1, repr(old)
        rewritten = rewritten.replace(old, new)

    backup.mkdir(parents=True, exist_ok=True)
    sources = {
        "delivery.ipynb": DELIVERY,
        "project_mirror.ipynb": MIRROR,
        "build_integrability_notebook.py": BUILDER,
        "README.md": HERE / "README.md",
        "PROGRESS_LOG.md": ROOT / "PROGRESS_LOG.md",
        "FILE_INDEX.md": ROOT / "FILE_INDEX.md",
    }
    old_hashes = {}
    for name, source in sources.items():
        archived = backup / name
        if not archived.exists():
            shutil.copy2(source, archived)
        old_hashes[str(source)] = sha(archived)
    BUILDER.write_text(rewritten, encoding="utf-8")

    spec = importlib.util.spec_from_file_location("report_builder", BUILDER)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.HERE = REVISION
    builder.DESTINATION = REVISION / "source_draft.ipynb"
    builder.build()
    draft = nbformat.read(builder.DESTINATION, 4)
    assert [(c.id, c.cell_type) for c in before.cells] == [(c.id, c.cell_type) for c in draft.cells]
    after = deepcopy(before)
    changed = []
    for current, source in zip(after.cells, draft.cells):
        if current.cell_type == "code":
            assert current.source == source.source, current.id
        elif current.source != source.source:
            current.source = source.source
            changed.append(current.id)
    nbformat.validate(after)
    old_math = math_expressions(before)
    assert old_math["foundation-text"].pop() == "$D^{-1}$"  # Inline symbol in the removed explanatory sentence.
    assert old_math == math_expressions(after)
    assert [c for c in before.cells if c.cell_type == "code"] == [c for c in after.cells if c.cell_type == "code"]
    assert before.metadata == after.metadata
    for old, new in zip(before.cells, after.cells):
        if old.cell_type == "markdown":
            assert {k: v for k, v in old.items() if k != "source"} == {k: v for k, v in new.items() if k != "source"}

    prose = "\n".join(c.source for c in after.cells if c.cell_type == "markdown")
    banned = ["没有", "不是", "未作为", "不需要", "未断言", "始终保留", "只保留", "仍完整", "确实"]
    assert not any(word in prose for word in banned)
    tags = re.findall(r"\\tag\{(\d+)\}", prose)
    assert tags == [str(n) for n in range(1, 20)]
    nbformat.write(after, DELIVERY)
    shutil.copy2(DELIVERY, MIRROR)
    result = {
        "success": True,
        "revision": "Chinese notebook prose cleanup",
        "changed_markdown_ids": changed,
        "markdown_cells": sum(c.cell_type == "markdown" for c in after.cells),
        "code_cells_preserved": sum(c.cell_type == "code" for c in after.cells),
        "all_code_objects_outputs_execution_counts_and_metadata_preserved": True,
        "all_display_formulas_and_retained_inline_math_preserved": True,
        "removed_inline_math_in_prose": {"foundation-text": "$D^{-1}$"},
        "numbered_formulas": tags,
        "generator_sources_match": all(a.source == b.source for a, b in zip(after.cells, draft.cells)),
        "delivery_and_mirror_match": DELIVERY.read_bytes() == MIRROR.read_bytes(),
        "before_sha256": old_hashes,
        "after_sha256": {str(p): sha(p) for p in (DELIVERY, MIRROR, BUILDER)},
    }
    (REVISION / "validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
