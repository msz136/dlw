# DLW 理论 Notebook

交付：`notebook/DLW理论.ipynb`；离线阅读：`report/dlw_theory.html`。

替代原 `notebook/非线性化report.ipynb`。原版的误差分析、数值比较与绘图按用户要求从新版移出，原件保存在 `before/` 和 `Trash/dlw_theory_notebook_20261008/`。保留两种非线性化路线，加入连续 DLW 起点、半离散双线性构造、任意 N τ 解证明、正性与二阶连续极限。

## 构建与执行

在现有 `Workspaces/report_colab_20261006/.venv/Scripts/python.exe` 下运行 `build.py`、`execute.py`、`export.py`。`build.py` 是新版的权威生成入口；旧 `build_nonlinear_notebook.py` 对应已留存的历史版本。

Notebook 使用 Colab 本地运行时或本地 Jupyter。Lean 4.34.0 与固定 Mathlib 来自 `_lean_shared/runtime.json`。没有为云端 Colab 安装运行时。

`proofs/` 收集 48 个既有 Lean 源文件，原始位置与 SHA-256 逐文件登记在 `proof_sources.json`；没有改动原证明库。每个 Lean 单元用已有来源／产物哈希审核运行器编译。新会话保存独立运行历史；证明缓存按精确源码与编译环境匹配后复用。

`execution_validation.json` 保存整本实际执行结果；`delivery_validation.json` 再核对逐单元源码与输入一致、执行编号完整、没有错误或 sorryAx、公理依赖仅标准逻辑公理。失败尝试留存在 `execution_attempts/`，不作成功记录使用。

离线 HTML 现以 `paper.src.md` 为独立正文源，`paper_revision.py` 记录从 Notebook 到纯理论稿的编辑。`export.py` 只导出该正文，不导出代码或执行输出；数学使用嵌入字体的 KaTeX HTML/MathML，正文使用思源宋体子集。每处公式均严格渲染；`check_layout.cjs` 检查 1440／390 像素布局、公式数量和零网络资源。`deliver.py` 在完整执行成功后交付并合并进度、索引及使用入口。

## Notebook 阅读修订

`notebook_prose.py` 由权威构建器调用：移除运行及防御性导读，展开 S2 的 Taylor 计算，以行列式定义和一般 N 证明为主线，再给子集展开及单／双孤子。`notebook_prose_validation.json` 核对14个代码单元及全部执行输出逐字保持，未新增Lean运行；记录246处LaTeX、CommonMark星号检查与S2精确系数核验。论文HTML的独立正文与交付未改。

## 主线精简

`focus_theory.py` 在构建器的文字修订后调用，使正文集中于一般 N Gram 精确解。连续表示只留起点，双孤子系数不单列推论，解族连续极限压为6.1。HTML以独立 `paper.src.md` 同步精简。最新证据为 `focus_validation.json`；全部14代码单元与保存输出保持，本轮未重跑Lean。


## 理论论文初稿重写

2026-10-09：以 `paper.src.md` 为理论正文唯一源，重写摘要、引言和六节理论主线，统一48个公式编号；保留一般N Gram证明、正则谱域、物理变量映射、二阶一致性与紧集上一致二阶极限，Q/R/M推导置于附录。未改Notebook、证明库或数值实现。`paper_revision.json` 记录本轮检查。

`export.py` 支持 Python Markdown 或 Pandoc，生成完全内联的 KaTeX HTML/MathML 与字体。在精简云端工作副本中可复用原HTML内嵌的KaTeX样式；完整仓库仍优先使用既有 `_assets`。可用 `DLW_KATEX_PATH`、`DLW_PAPER_FONT` 指定本机依赖。`check_layout.cjs` 支持 `DLW_PLAYWRIGHT_PATH` 与 `DLW_BROWSER_PATH`，并跟随新版章节定位。
