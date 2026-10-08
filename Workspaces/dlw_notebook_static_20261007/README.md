# DLW notebook 的单文件静态报告

## 当前静态场图（2026-10-08）

当前第7节改为物理场与误差分布：A/B/C 各一张数值三维曲面、数值二维场、解析二维场及一张三维/二维误差图，共6张内嵌PNG。A显示 x=[-3,4]、y=[-3,3]，B/C显示 x/y=[-30,30]，T=.01。零值为白色，负值蓝、正值红，误差用白到红；混合正负场保持同幅值色强。Notebook末尾分别设置各算例窗口，静态报告不显示配置与代码。原比较表数值保持，宽域场为SD2/RK4固定网格另行计算。最新合并核验见 `../dlw_precision_surface_20261008/notebook_integration_validation.json` 与本目录 `content_validation.json`；本页以下为原构建与历史记录。

当前交付：根目录 `dlw_numerical.html`，来源为 `notebook/DLW数值分析report.ipynb`。SD 推进非线性化报告式（7）的 $(u,\omega)$ 系统，保存 $P=\delta_-u$、$W=4\omega/h$，恢复 $u,v$ 后在公共物理点计算误差。空间差分为三点二阶 $D_1$ 与直接三点 $D_2$；固定／动网格及 SD2 跃量延拓沿用同一差分。SD、SD2、FD 均由共同连续物理初值出发，采用 Euler／RK4。

报告保留第 1—7 节，结束于局部误差曲线；无目录、第 8 节、参考资料和代码附录。HTML 全部代码块与实现名称说明已移除，精确解由单／二孤子的 $f,g$ 闭式及解析对数导数计算，SD／SD2／FD 及 Euler／RK4 的递推用 LaTeX 展示。36 组主试验覆盖三种方法、三种算例、两种时间算法与两种网格；SD 与 SD2 的 Euler 时间细化另有 12 条轨道。固定网格空间误差表与动网格比较表使用 RK4，局部误差曲线使用 Euler。五张三线表与三张 PNG 图取自 Notebook 保存输出。HTML 内嵌 KaTeX 公式及字体，可离线打开或发送单个文件。

静态生成器只读取 Notebook 的正文和保存输出，主方法递推公式、表格数值和 PNG 字节由 `verify_static.py` 逐项核对。当前源码与数值核验材料见 `../notebook_reports_20261006/`，非线性 SD 核验材料见其 `nonlinear_sd_20261007/`；运行、内容与浏览器核验的计数和交付哈希由各自的 JSON 证据保存。

本轮 Notebook 的 17 个代码单元完整执行，用时 36.895 秒；36 组主试验和 12 条细化轨道全部到达 $T=0.01$。静态报告包含 30 个展示单元、107 个数学表达式、五张三线表与三张 PNG 图。正文、公式、72 项误差及原图字节核对通过；桌面／390px／打印的无代码内容、三线表与真实字体检查通过。当前 Notebook SHA-256 为 `03d051287aad5bbe9af167081466d54e7142107c0eb412053d5f0796c73ef473`，HTML SHA-256 为 `0e8dea4f857464ecaa1d13af541cc397497d6dbf4169c414998c2cc9279f949d`。

本轮按用户要求先保存在本地，未提交或推送。

## 生成与核验

在工作区根目录执行：

```powershell
$staticPython = 'C:\Users\msz\aca\Workspaces\report_colab_20261006\.venv\Scripts\python.exe'
& $staticPython -X utf8 Workspaces/dlw_notebook_static_20261007/build_static.py
& $staticPython -X utf8 Workspaces/dlw_notebook_static_20261007/verify_static.py
& node Workspaces/dlw_notebook_static_20261007/check_static.cjs
```

`build_static.py` 只转换内容，不执行 Notebook；代码单元只导出保存的表格、文字和图片，正文的实现说明改为数学叙述。`render_math.cjs` 使用已有本地 KaTeX 生成 HTML/MathML。`verify_static.py` 核对正文、公式源、表格数值和原图字节，并确认源码块、函数名说明、目录及三个文末部分均已移除。各项计数读取当前 `build_validation.json`。`check_static.cjs` 用 Edge 在断网且禁用 JavaScript 的情况下检查桌面、390px 窄屏、打印样式，同时核对实际参与字形绘制的字体。

当前静态生成与核验证据为 `build_validation.json`、`content_validation.json`、`browser_validation.json`。`report_*.png` 覆盖桌面与手机首页、精确解、SD 公式、时间递推、比较表、误差图和打印样式。`no_code_revision.json`、原代码截图、`three_line_revision.json` 与 `direct_tau_visual_validation.json` 保留此前版本的历史视觉记录。

## 字体与版式

五张表统一采用三线表：表顶线、整个表头下方的分隔线与表底线；单元格、数据行及表的左右边均无边框。双行表头与合并单元格沿用原结构，表内数值、加粗最小值及全部页面 DOM 保持。桌面、390px 与打印视图逐表检查实际边框，并复核了宽窄屏截图。修正前材料保存在 `before_three_lines/`。

中文／拉丁正文恢复旧 index 的 `Times New Roman, SimSun, serif`，版式沿用宋体论文正文、首行缩进与克制的标题字号。修复字体内嵌正则原先跨越 CSS 右花括号的问题，完整保留 20 条 KaTeX 字体注册及 `.katex` 基础样式；实际绘制证据确认正文使用 Times New Roman／SimSun，公式使用内嵌 KaTeX_Math-Italic，没有依赖 CSS 字体名称推断。输出中的打印文字随正文使用同一字体。

## 历史版本与登记

原 `index.html` 字节保存于 `before/index.html`；阅读留档为 `report/DLW数值分析_原HTML_20261007.html`，只加 `base href="../"` 保持相对链接。主入口随后按用户要求改名为 `dlw_numerical.html`。

此前完整展开版与代码精简版分别登记在本目录的 `registration.json`、`registration_compact.json`；两页改名阶段登记在 `Workspaces/dlw_static_reports_20261007/registration.json`。这些均为旧版记录。旧 `register_static.py`、`register_compact.py` 不用于当前交付登记。

精简前的 HTML、源码、证据、截图和根记录保存于 `before_compact/`。direct τ 替换前的生成器、验证脚本与主 HTML 保存于 `before/direct_tau_generator_50a08adc630c4b929a9118e2a0a6a732/`。原先“5 段摘录／27 行／未重新执行 Notebook”及旧 Notebook 哈希 `10bd4b256d7ea80246d5cdd0dcf202a8f6bcec6e6cc41328f4b892bdc23a2cfe` 仅属于此前版本。

本轮改回非线性 SD 前的完整材料保存在 `../notebook_reports_20261006/before_nonlinear_sd_20261007/`。当时 SD 使用原始双线性 $\tau$ 隐式中点；三点二阶计算来源见 [GSG 对齐历史记录](../notebook_reports_20261006/gsg_second_order/README.md)。该阶段无代码 HTML 的 Notebook SHA-256 为 `d73afce61ea07e523be2bb8a365f72546f91e684d5974e234f5f1cf461d6c1c2`，HTML SHA-256 为 `90df160d1d1e9eab74b771e2e36e2918146cb9372dc83bf3b9430b9312985870`，曾展示 30 个单元、122 个数学表达式与 8 项输出。`simple_exact_revision.json`、`explicit_xyt_revision.json`、`no_code_revision.json`、`intro_revision.json` 分别保留闭式简化、变量补全、移除代码与开篇代码说明的历史。此前含代码版本保存在 `before_no_code/`；三线表与正文精简登记为 `three_line_revision.json`、`trim_revision.json`。
