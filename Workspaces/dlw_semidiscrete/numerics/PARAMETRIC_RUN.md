# 参数研究复现

2026-09-23。Python 运行时为应用依赖中的 Python 3.12；numpy 来自应用运行时，SciPy/mpmath、绘图及报告构建依赖安装于本目录 .research_deps。没有修改系统 Python。运行时版本在最终验收清单记录。

在本目录的 PowerShell 中设置：

```powershell
$researchPython = 'C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONPATH = "$PWD/.research_deps"
$env:OPENBLAS_NUM_THREADS = '1'
& $researchPython -u experiments/parametric_study.py
& $researchPython -u experiments/parametric_bounds.py
& $researchPython -u experiments/parametric_controls.py
& $researchPython -u experiments/parametric_perturb.py
& $researchPython -u experiments/parametric_reference.py
& $researchPython -u experiments/parametric_open_study.py
& $researchPython -u experiments/parametric_open_bounds.py
& $researchPython -u experiments/parametric_open_control.py
& $researchPython -u experiments/parametric_open_parameter_sweep.py
& $researchPython -u experiments/parametric_assess.py
& $researchPython -u experiments/parametric_cost.py
& $researchPython -u experiments/check_regressions.py
& $researchPython -u experiments/parametric_report.py
```

成本实验必须等其他实验完成后独立运行。背景求值包含在推进计时内，排除初始化、插值、输出和绘图；三次顺序重复并交替方案顺序。绝对耗时取决于机器。

报告构建：先执行 parametric_report.py，再从工作区根目录用上述 Python 执行 Workspaces/gsg_project/dlw_report/sync_numerical_results.py，最后执行既有 build_html.ps1 的数值页参数。构建后运行 parametric_validate.py。不要单独运行旧 dynamics_report.py 覆盖最新总报告；它只负责此前阶段，若运行须再次执行本轮报告生成。

结果源：PARAMETRIC_REPORT.md；理论推导：PARAMETRIC_THEORY.md；总报告：REPORT.md。先前总报告逐字保存在 PRE_PARAMETRIC_REPORT_20260923.md。所有失败及初版比较保留；当前扰动评估为 parametric_assessment.json，使用严格张量插值重新读取原始场。初版 parametric_perturbations.json 中比较字段因插值容差问题作废，原始轨道数据有效。

科学范围：正则单孤子参数族及其附近的短时非零扰动；新边界闭合改变了右端条件，不等价于原固定幽灵问题；没有证明长时间稳定或一般初值收敛。原生产 solver、Gram 与 Lean 未改。
