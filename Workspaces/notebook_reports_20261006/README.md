# 非线性化、2HS 与 DLW：三份独立笔记本

2026-10-07 当前 DLW：SD 回到非线性化报告式（7）的 $(u,\omega)$ 半离散系统，保存 $P=\delta_-u$、$W=4\omega/h$，由 $P$ 与下边界恢复 $u$，再由 $v=W+\delta_0u$ 恢复 $v$。空间差分使用三点二阶 $D_1$ 与直接三点 $D_2$；固定／动网格沿用同一计算坐标差分和坐标链式法则，SD2 端点跃量延拓同步。SD、SD2、FD 均采用 Euler／RK4，从共同连续物理初值出发。

主试验覆盖 A／B／C、三种方法、Euler／RK4 与固定／动网格的 36 个组合；SD 与 SD2 的 Euler 时间细化各增加 6 条轨道，共 12 条。固定网格空间误差表和动网格比较表均使用 RK4，局部误差曲线均使用 Euler。主 HTML 为 [dlw_numerical.html](../../dlw_numerical.html)，由同一 Notebook 的保存输出生成，正文用数学公式展示方案；可执行代码保存在 Notebook。

当前源码为 `sd_nonlinear_cell.py`、`dlw_numeric_cells.py`、`revise_dlw_structure.py`、`build_dlw_numerics_notebook.py`，执行入口为 `execute_dlw_notebook.py`。非线性 SD 的独立核验与证据位于 `nonlinear_sd_20261007/`：原始 $\omega$ 方程、缩放后的 $(P,W)$ 方程、展开的 $y$ 差分形式、ALE 输运以及固定／动网格初值均逐项核对。

本轮在新 Python 内核中完整执行 17 个代码单元，用时 36.895 秒；36 组主试验与 12 条细化轨道均到达 $T=0.01$，三张图及全部输出已保存。72 项误差标量与对应曲线最大值完全一致，18 组共同配置下的 SD2／FD 结果与替换前逐位一致。SD 的 Euler 观测阶为 0.997137–1.000294，SD2 为 0.994819–1.000083；最小网格 Jacobian 为 0.676281，初始评价区间物理场节点差最大为 $1.975\times10^{-13}$。Notebook SHA-256 为 `03d051287aad5bbe9af167081466d54e7142107c0eb412053d5f0796c73ef473`。

<!-- HS_FIGURE_README_BEGIN -->
2HS 当前展示（2026-10-07）：五张图统一使用 STIX 数学与文字字体，单孤子／二孤子的初始物理区间分别简写为约 [-4.8,3.8]／[-5.7,3.7]；实际节点由原解析坐标映射计算。16 个单元已完整重跑，八个误差范数与此前输出一致。字体与显示精度源为 `hs_presentation.py`，生成器同步调用；实际字形核对、执行与新图见 [展示修订](hs_plot_fonts_20261007/validation.json)。
<!-- HS_FIGURE_README_END -->

本目录维护根目录 `notebook/` 中的三份标准 Jupyter 笔记本。原 `notebook/Report.ipynb` 拆为非线性化与 2HS 两份；根目录 `index.html` 的 DLW 数值内容另转为独立笔记本。正文按数学叙述、代码、输出顺序组织，保留分段执行，不为无输出的定义单元补造结果。

| 主交付 | 内容 |
| --- | --- |
| [非线性化report.ipynb](../../notebook/非线性化report.ipynb) | DLW 两套非线性化、Lean 起点和终点，以及相关空间残差估计。 |
| [2HS数值分析report.ipynb](../../notebook/2HS数值分析report.ipynb) | 2HS 精确参照、数值推进、误差评价和图。 |
| [DLW数值分析report.ipynb](../../notebook/DLW数值分析report.ipynb) | DLW 孤子算例、SD／SD2／FD 空间离散、Euler／RK4 时间推进和误差比较。 |
| [使用说明](../../report/notebook_usage.html) | 用户运行步骤。 |

## 运行

VS Code 打开对应 `.ipynb`，选择现有 Python 内核：

```text
C:/Users/msz/aca/Workspaces/report_colab_20261006/.venv/Scripts/python.exe
```

从首个代码单元开始，依次点击原生播放按钮或按 `Shift+Enter`。修改配置后，从配置单元向下重跑。已有输出可直接阅读；保存后保留本次编辑与输出。

Colab 中上传对应 `.ipynb`。两份数值笔记本自包含，使用 NumPy、pandas、Matplotlib，DLW 另用 SciPy；直接连接 Colab 云端 Python 即可逐段运行，也可以选择本地运行时。它们不导入工作区路径或 Lean。

非线性化笔记本复用本机 Lean：双击 [启动Colab本地运行时.pyw](../../notebook/启动Colab本地运行时.pyw)，在“连接”菜单选择“连接到本地运行时”，粘贴启动窗口中的连接地址。数值笔记本若选本地，也使用同一启动器与项目 Python，无新增启动脚本。

非线性化首单元通过 `report_runtime.load_lean` 复用本机 Lean 4.34.0、Mathlib 及已经编译的证明缓存。它沿用 `Workspaces/report_colab_20261006/report_runtime.py`、`lean_notebook.py`；本轮不改共用服务、证明源或 Lean 环境。

## 保留与登记

原混合笔记本保存为 `before_split/Report.ipynb`，`Workspaces/report_colab_20261006/Report.ipynb` 仍保留迁移历史。原 `Report.html` 和 `index.html` 保留；另在 `report/` 保存 [原综合 HTML](../../report/Report_原HTML_20261006.html) 与 [原 DLW 数值 HTML](../../report/DLW数值分析_原HTML_20261006.html)。归档页保留原相对资源和链接，原始字节副本在 `before_split/Report.html`、`before_split/index.html`，构建与核验见 `archive_source_html.py`、`html_archive_validation.json`。

共用运行时项目的旧 `README.md` 已更新当前入口，原稿保存在 `before_split/report_colab_README.md`；其 42 单元／21 段执行记录明确作为旧混合版历史保留。

本目录的构建、执行与科学核验材料逐文件登记在根 `FILE_INDEX.md`。最终运行证据与交付哈希由 `registration_summary.json` 汇总，`register_notebook_split.py` 在所有报告核验完成后合并根 `PROGRESS_LOG.md` 的既有 Report 和 Index 条目，更新 `FILE_INDEX.md`，并保存登记前副本及 `registration.json`。验证证据标明实际覆盖范围；复用的早期浏览器记录不能当作本轮 Colab 页面执行证据。

## 初版执行证据（保留）

三份报告均在新的原生 Python 内核中完整执行，42 个代码单元全部通过，实际输出保存在对应笔记本中。

| 报告 | 单元／代码 | 完整执行 | 证据 |
| --- | --- | --- | --- |
| 非线性化 | 30／14 | 95.87 秒 | `nonlinear_execution_validation.json` |
| 2HS | 27／13 | 10.936 秒 | `hs_execution_validation.json`、`hs_numerical_validation.json` |
| DLW | 31／15 | 27.629 秒 | `dlw_execution_validation.json` |

非线性化保留 22 个原编号，DLW 空间残差图为 2 张。2HS 包含单孤子与二孤子参考、推进及 5 张图，8 个打印误差范数与原结果最大差约 `1.10e-12`；二孤子解析导数、正 Jacobian 和坐标反解另有独立核对。DLW 的 36 条主轨道与 6 条 SD2 Euler 减步轨道全部推进至指定终点，原 90 个表值最大绝对差为 `6.44e-13`，36 条 Euler 曲线最大差为 `1.93e-13`；3 张图包含 12 个子图。`delivery_validation.json` 核对三份交付哈希、代码输出、22＋12 个原编号、10 张生成图及 HTML 归档。

## DLW 双线性推进阶段（历史）

非线性 SD 重算前的 Notebook、HTML、源码、结果和验证材料已保存于 `before_nonlinear_sd_20261007/`。该阶段 SD 使用原始双线性 $\tau$ 隐式中点，按 $G_j^{n+1}\to F_j^{n+1}\to G_{j+1}^{n+1}$ 逐层求解；SD2、FD 使用 Euler／RK4。三点二阶版本曾执行 24 组主试验及 12 组附加时间细化，33 个单元中的 17 个代码单元全部完成（158.458 秒），保存 6 张表和 3 张图。

该阶段的空间观测阶约 2，SD 中点时间阶为 1.995–2.000，SD2 Euler 时间阶为 0.995–1.000，初始评价区间物理场节点差为 $7.764\times10^{-13}$。记录见 [GSG 对齐记录](gsg_second_order/README.md)。`sd_tau_cell.py`、`tau_report_cells.py`、`verify_dlw_tau.py`、`verify_direct_tau_delivery.py`、`gsg_second_order/` 及 `direct_tau_main_manifest.json` 保留双线性阶段的实现与证据。四阶原件仍在 `before_gsg_second_order/`；更早的替换记录在 `before_direct_tau/`。
