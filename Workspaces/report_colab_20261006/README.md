# 共用本地运行时与混合版迁移历史

当前可运行报告已拆分为 [DLW理论](../../notebook/DLW理论.ipynb)、[2HS数值分析](../../notebook/2HS数值分析report.ipynb) 与 [DLW数值分析](../../notebook/DLW数值分析report.ipynb)。运行步骤见 [用户使用说明](../../report/notebook_usage.html)，构建与本轮验证见 [新项目说明](../notebook_reports_20261006/README.md)。

本目录继续提供共用 Python、Colab 本地 Jupyter 服务、Lean 与 Mathlib 的 import 辅助器及证明缓存。运行时和证明源沿用已核验环境。旧 [Report.ipynb](Report.ipynb) 保留混合版项目镜像；原根目录混合本保存为 [before_split/Report.ipynb](../notebook_reports_20261006/before_split/Report.ipynb)。下文 42 个单元、21 段执行与对应输出核验属于拆分前混合版历史，当前三份报告的执行证据见新项目。

原 [Report.html](../../Report.html) 保留，另有 [综合报告 HTML 留档](../../report/Report_原HTML_20261006.html)；数值 HTML 见 [DLW HTML 留档](../../report/DLW数值分析_原HTML_20261006.html)。

## 在 Colab 中运行

1. 在 Colab 上传并打开根目录 `notebook/` 中所需的笔记本。2HS 与 DLW 数值笔记本自包含，直接连接云端 Python 就可以执行。
2. 非线性化笔记本需要本机 Lean：双击根目录 notebook 中的 [启动Colab本地运行时.pyw](../../notebook/启动Colab本地运行时.pyw)，点击 Colab 右上角“连接”的菜单，选择“连接到本地运行时”，粘贴弹窗中的地址。数值笔记本若选择本地，也使用同一入口。
3. 先运行准备单元，再按正文顺序点击各单元的原生运行按钮。两条 Lean 路线各从自己的 import 单元开始；数值路线各从自己的准备与配置开始。

地址包含本次本地会话的认证 token，由启动器保存到 `.local_runtime/Colab连接地址.txt`。该目录只供当前 Windows 用户与 SYSTEM 访问；公共日志与验证文件不保存 token。Jupyter 仅监听 `127.0.0.1`，允许 Colab 来源并保留认证。此连接方式按 [Google 官方本地运行时说明](https://research.google.com/colaboratory/local-runtimes.html) 实现，使用直接 Jupyter 连接。

浏览器负责显示和编辑；Python、Lean 和 Mathlib 的计算发生在本机。云端 Python 运行时不能读取本机目录；准备单元只调用本机环境，不包含下载步骤。

## 在 VS Code／Jupyter 中运行

打开根目录 `notebook/` 中所需的笔记本，选择 `C:/Users/msz/aca/Workspaces/report_colab_20261006/.venv/Scripts/python.exe` 内核。运行顺序与 Colab 相同。已有实际输出可以直接阅读；编辑参数或算法后重新运行当前段，再逐段更新后段。

## 笔记本与 Lean 的结构

此前混合版笔记本有 42 个标准单元：21 Markdown，1 个准备单元、6 个 Lean 单元、14 个 Python 单元。每段代码之前有中文说明。37 个显示公式、34 个编号、两张静态表和四张原图与 `Report.html` 的内容及顺序核对。

两条 Lean 路线各分为 import、双线性起点、终点三段，可见 Lean 源码通过 `%%lean` 交给本机编译器。准备单元读取 `_lean_shared/runtime.json`；当前 Lean 为 4.34.0，Mathlib 为 `v4.34.0`，commit 为 `5ed2965256430c3649e86755f9576b54eca72435`。

原证明源位于 `Workspaces/report_notebook_20261002/lean_material/proofs/`，持久缓存在本项目 `proof_cache/`。import 复用经哈希核对的编译证明；缓存同时记录传递依赖源、编译器及 Mathlib 身份，源或环境不一致时重新检查。当前可见单元每次实际编译，编译器输出保留在该单元下方。上游源码改变会使后段失效，须重新从 import 开始。

此前混合版中，2HS 与 DLW 各有七个可编辑 Python 单元，使用 NumPy、pandas、Matplotlib。定义、参数、推进与评价分开，在同一个 Python 内核内保留对象；运行当前段不会自动补算前段。无程序输出的准备、定义段保持空白，误差表、图与残差来自实际计算。

## 当前文件

| 文件 | 用途 |
| --- | --- |
| [三份当前报告](../notebook_reports_20261006/README.md) | 非线性化、2HS 与 DLW 独立笔记本。 |
| `Report.ipynb` | 此前混合版项目镜像。 |
| [启动Colab本地运行时.pyw](../../notebook/启动Colab本地运行时.pyw)、`local_runtime.py` | 本地 Jupyter 启动入口与 Colab 连接服务。 |
| `local_runtime_validation.json` | 认证、Colab 来源、真实 Python 内核与 WebSocket Lean 编译验证。 |
| `report_runtime.py`、`lean_notebook.py` | 六行准备入口、Lean 单元编译与证明缓存。 |
| `validate_local_lean.py`、`local_lean_validation.json`、`proof_cache/`、`local_lean_runs/` | 本地证明复用、六阶段编译、失效检查及缓存证据。 |
| `validate_lean_seed_chronology.py`、`lean_seed_chronology_validation.json`、`seed_guard_cache/` | 历史编译依赖次序与陈旧依赖产物的拒绝核验。 |
| `build_lean_bootstrap.py`、`bootstrap_source.txt`、`local_import_manifest.json` | 本地 import 准备单元及工具／证明源哈希。 |
| `smoke_local_import.py`、`local_import_smoke.ipynb`、`local_import_smoke_validation.json` | 最终辅助器在新内核中的准备及两路线 import 核验。 |
| `build_notebook.py`、`build_validation.json` | 正文转换、单元组装、公式／表图与格式核对。 |
| `execute_notebook.py`、`execution_validation.json` | 项目原生内核的完整执行与输出记录。 |
| `verify_local_delivery.py`、`local_delivery_validation.json` | 根目录交付与项目镜像、六行准备、21 段源码及实际输出核对。 |
| `local_reuse_summary.json`、`register_local_reuse.py`、`local_reuse_registration.json` | 当前本地复用版汇总与 Report 同专题合并登记。 |
| `hs_cells.py`、`hs_cells.json`、`validate_hs.py`、`hs_validation.json` | 2HS 七段源码、说明与默认／编辑回归。 |
| `dlw_cells.py`、`dlw_cells.json`、`build_dlw_cells.py`、`validate_dlw.py`、`dlw_validation.json` | DLW 七段源码、说明与系数／残差／曲线／收敛核验。 |
| `before_local_reuse/` | 本次修改前的 notebook、辅助器生成材料、说明与共享记录。 |
| `refs/colab_local_runtimes_official.html` | 本次核对的 Google 官方连接说明。 |

重建此前混合版时，在本目录依次运行 `python build_lean_bootstrap.py`、`python build_notebook.py`；完整执行使用 `python execute_notebook.py`。此处的 `python` 指项目 `.venv/Scripts/python.exe`。

## 数值与证明证据

拆分前混合版交付已由项目原生 Python 内核实际执行全部 21 个代码单元，约 110.91 秒，零错误；表、图和 Lean 输出已保存。`local_delivery_validation.json` 记录拆分前根目录交付与项目镜像字节一致，21 段源码及实际输出与完整运行记录逐段吻合，原 `Report.html` 字节保持。

`local_lean_validation.json` 通过本轮六阶段真实编译与八项缓存／失效检查。新内核的 UW、QRM import 分别约 16.10、15.76 秒，历史中只新增两个可见单元的编译，没有重编证明源；修改传递依赖、失败编译、损坏产物与并发构建均已核验，自动下载被禁用。

最终辅助器另由 `lean_seed_chronology_validation.json` 核对三项历史依赖次序检查：有效旧产物接受，依赖改动后的陈旧子模块拒绝，三个实际 QRM 旧产物重新核验通过。`local_import_smoke_validation.json` 在新内核实际运行六行准备与两路线 import，只有两个显示单元编译、11 次证明缓存读取全部复用，零证明源重编。

`local_runtime_validation.json` 通过真实 Jupyter API 与 WebSocket 执行：无认证请求被拒绝，Colab 来源正确，唯一内核使用项目 Python，NumPy／pandas／Matplotlib 可导入，本机 Lean 与 Mathlib 的实际 example 编译退出 0。
此项验证覆盖服务与内核，Colab 浏览器连接尚未实测。

本次数值端口的实际本地环境为 Python 3.13.3、NumPy 2.2.5、pandas 2.3.3、Matplotlib 3.10.1。

`hs_validation.json` 核对默认 N=1600、a=.005、T=.5、RK4 160 步、32001 评价点，四项误差与原报告最大差 1.139e−12；编辑 T 后推进步数和终点误差改变，缺少前置时不自动补算。

`dlw_validation.json` 核对七段依序执行、默认及原文参数 B 的主系数、有限 h 残差、收敛表和逐条绘图数据。参数及算法编辑会改变结果，缺失前置、配置失效与语法错误／修复有记录。采样最大值与全波形解析上界分别标注；局部方程残差不作为演化场总误差。

旧 `lean_validation.json`、`lean_bytes_validation.json` 保留六个阶段的真实编译、五项前置／编辑／失败检查及 UTF-8 源码核对。四个终点公理查询仅有 `propext`、`Classical.choice`、`Quot.sound`；九份原证明源逐文件一致。

## 历史迁移记录

此前完整本地执行约 578 秒，全部 21 个代码单元零错误；随后单独核验过准备单元的字节保真补正。相关稿件和记录保存在 `before_execute/`、`before_final_bootstrap/`、`bootstrap_final_run.ipynb`、`bootstrap_integration_validation.json`。此前准备单元曾内嵌辅助器、证明闭包并提供 Linux 首次安装路径；现已改为本机短 import。旧 `lean_bundle_manifest.json`、`report_lean/` 与 `finalize_bootstrap.py` 仅说明此前版本。

更早的云端副本已上传并核对 42 个迁移单元源码，见 `cloud_copy_metadata.json`、`cloud_sync_validation.json`、`colab_cell_mapping.json`、`mcp_control/`。旧云端副本为 [Report.ipynb](https://colab.research.google.com/drive/1s2B_cGFByM_0d29CJzAlIxCvTlSjAlkx)。当时未在云端执行报告代码，Linux 下载与缓存也未远程核验；该副本不代表当前本地 import 版本。

`colab_server.py`、`colab_client.py`、`sync_colab.py` 与 `refs/` 中的官方 `colab-mcp` 1.0.1 参考源保留为迁移历史。旧 `final_summary.json`、`registration.json`、`register_results.py` 和 `before_records/` 对应首次本地交付及登记。
