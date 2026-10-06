# 逐段数值材料

此目录保存对既有 `error_material` 数值复算的逐段执行版本，不修改原数学实现或原结果。`hs_cells.json` 为 2HS 的 7 段，`cells.json` 为 DLW 的 7 段；`hs_intro.html` / `intro.html` 由主页面嵌入，单段源码同时另存为 `.js`。

每个 cell 含 `id,title,note,code,requires`。要求持久 Worker 维护共享 `lab`，逐次执行 AsyncFunction(lab, emit, 当前可见代码)；Run 当前段时不得拼接、重放前段。主页面须在编辑上游、上游执行失败或取消时，将后段标为过期并要求重新 Run；Run All 才按顺序逐段执行，遇错停止。

2HS 使用 `lab.hs`，DLW 使用 `lab.dlw`。每个定义段显式解构已运行前段的变量，再将本段函数/数据写回共享对象；`ready` 标记提供缺少前置的直接错误，并在重新运行上游段时撤销下游完成标记。输出只用既有 `emit` 的 text/table/series 接口。

准备段检查原生 Math 与 Float64Array；没有网络依赖，没有 Python 科学包 import。源码及运行标签必须表明 JavaScript。2HS 的实际演化在 `hs-evolve`，误差与图在 `hs-error`；DLW 的实际主系数计算在 `error-main`，有限 h 收敛与图在 `error-convergence`。

`build_material.py` 原样抽取旧代码中的公式，只增加单元边界、显式共享变量与前置标记。`validate_material.cjs` 逐段使用相同 AsyncFunction 执行方式，检验默认结果与旧版表格完全一致、缺少前置拒绝、不提前生成误差图、参数与算法编辑有效、上游重跑后过期、真实语法错误与修复。结果记录在 `validation.json`。

MIT 两份公开原 ipynb 保存于 `refs/`；原 notebook 的真实代码/叙述节奏与本页迁移理由见 `refs/MIT_NOTEBOOK_REVIEW.md`。这些文件只供来源审查，不参与页面执行。
