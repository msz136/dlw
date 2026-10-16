# 非线性化 notebook 的式（7）定义补充

交付文件：`C:\Users\msz\aca\notebook\非线性化report.ipynb`。

仅修改既有单元 `report-text-04` 与 `lean-uw`。后者增加与原证明源逐字一致的 `fluxUW`、`fluxOmega`、`reportN1`、`reportN2`，放入显示命名空间，并由两条 `rfl` 定理核对与库定义相同。原有 `StartPoint` 到式（7）、（8）的终点证明仍原样调用。说明表对照导数、差分、平均和通量的 LaTeX 含义。

## 执行与保留

- `revise_and_verify.py` 在原生项目 Python kernel 中运行初始化、UW 导入、起点及修订后的终点四个单元，实际编译通过，总计 53.203 秒；终点单元 17.497 秒。
- `targeted_lean.executed.ipynb` 与 `targeted_lean.stdout.txt` 保存该次真实输出，`revision_validation.json` 保存 SHA-256、逐定义源匹配、单元计时及保留检查。
- 其余 13 个代码单元连同执行编号、保存输出与元数据保持相同；数值单元未重新计算。原证明源没有修改。
- `before_revision` 保存此前 notebook、权威 builder 和全执行证据。
- 权威 builder `Workspaces\notebook_reports_20261006\build_nonlinear_notebook.py` 已包含 `add_uw_definitions`，重新生成不会丢失定义补充。
- `update_execution_evidence.py` 保留原全执行 SHA-256 和耗时，另登记本次局部执行及交付文件当前 SHA-256。没有把局部重跑记成整本重跑。

当前 notebook SHA-256：`601be1d52d8379fdb330399a0039ea17911ec09127fd085c8040d87eb35e4b33`。

根进度及索引由本任务主 agent 登记。本次未修改讲稿、HTML、Lean 库源或运行器。
