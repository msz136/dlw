# DLW notebook 的单文件静态报告

当前交付：根目录 `dlw_numerical.html`，来源为已重新执行的 `notebook/DLW数值分析report.ipynb`。空间差分已按 GSG 对照格式改为三点二阶；固定与动网格、SD 线性矩阵及 SD2 跃量延拓同步。SD（raw bilinear）直接推进原双线性方程中的 F、G，采用隐式中点时间递推；SD2、FD 使用 Euler／RK4。三种方案由共同连续 u、v 初值出发，在公共物理点比较误差。

当前报告保留第 1—7 节，结束于局部误差曲线；移除目录、第 8 节“结果”、参考资料与完整代码附录。共有 30 个展示单元、121 个数学表达式及 8 项保存输出，其中有 5 张表、3 张 PNG 图。正文仍显示 7 段关键源码，共 83 行；精确解摘录 `Exact.tau` 至 `uv`；SD 摘录 `SDModel.solve_one` 和 `advance`，其余为 SD2／FD 右端、Euler／RK4 与公共点误差代码。HTML 内嵌 KaTeX 公式及字体，可离线打开或发送单个文件。

静态生成器只读取 Notebook 的源码和保存输出。本次三点二阶版本的 Notebook SHA-256 为 `0a8bcb20201f13a35f64f36a75a4201f62d94af0afef4dd2f01858ce657fe00e`，HTML SHA-256 为 `fb875e43ac779f50e4089035531533c4000cd91b4dce8ab5b6c1e40552fd47ad`。17 个代码单元在新内核中执行 158.458 秒，24 组主试验与 12 组附加时间细化完成。公式、源码、表值与原图字节逐项核对；桌面／390px／打印的三线表及真实字体检查通过。最新登记见 [GSG 对齐记录](../notebook_reports_20261006/gsg_second_order/README.md)，四阶原件保存在 `../notebook_reports_20261006/before_gsg_second_order/`。此前三线表与正文精简登记分别保留为 `three_line_revision.json`、`trim_revision.json`。

开篇与第1.1节的叙述修订见 `intro_revision.json`；计算代码、执行计数和保存输出逐项保持，数值执行证据继续记录原始执行时的文件哈希。

## 生成与核验

在工作区根目录执行：

```powershell
$staticPython = 'C:\Users\msz\aca\Workspaces\report_colab_20261006\.venv\Scripts\python.exe'
& $staticPython -X utf8 Workspaces/dlw_notebook_static_20261007/build_static.py
& $staticPython -X utf8 Workspaces/dlw_notebook_static_20261007/verify_static.py
& node Workspaces/dlw_notebook_static_20261007/check_static.cjs
```

`build_static.py` 只转换内容，不执行 Notebook；SD 的完整核心方法通过 AST 摘录。`render_math.cjs` 使用已有本地 KaTeX 生成 HTML/MathML。`verify_static.py` 核对保留单元的关键摘录、正文（允许三项展示措辞替换）、公式源、表格数值、输出文本与原图字节，并确认目录与三个文末部分均已移除。各项计数读取当前 `build_validation.json`。`check_static.cjs` 用 Edge 在断网且禁用 JavaScript 的情况下检查桌面、390px 窄屏、打印样式，同时核对实际参与字形绘制的字体。

当前证据为 `build_validation.json`、`content_validation.json`、`browser_validation.json` 以及 `../notebook_reports_20261006/gsg_second_order/revision_manifest.json`。11 张 `report_*.png` 覆盖桌面与手机首页、SD 公式、SD 核心代码、比较表、误差图和打印样式；本轮截图哈希由 GSG 对齐记录登记。`three_line_revision.json` 与 `direct_tau_visual_validation.json` 保留此前版本的历史视觉记录。

## 字体与版式

五张表统一采用三线表：表顶线、整个表头下方的分隔线与表底线；单元格、数据行及表的左右边均无边框。双行表头与合并单元格沿用原结构，表内数值、加粗最小值及全部页面 DOM 保持。桌面、390px 与打印视图逐表检查实际边框，并复核了宽窄屏截图。修正前材料保存在 `before_three_lines/`。

中文／拉丁正文恢复旧 index 的 `Times New Roman, SimSun, serif`，版式沿用宋体论文正文、首行缩进与克制的标题字号。修复字体内嵌正则原先跨越 CSS 右花括号的问题，完整保留 20 条 KaTeX 字体注册及 `.katex` 基础样式；实际绘制证据确认正文使用 Times New Roman／SimSun，公式使用内嵌 KaTeX_Math-Italic，没有依赖 CSS 字体名称推断。输出中的打印文字随正文使用同一字体。

## 历史版本与登记

原 `index.html` 字节保存于 `before/index.html`；阅读留档为 `report/DLW数值分析_原HTML_20261007.html`，只加 `base href="../"` 保持相对链接。主入口随后按用户要求改名为 `dlw_numerical.html`。

此前完整展开版与代码精简版分别登记在本目录的 `registration.json`、`registration_compact.json`；两页改名阶段登记在 `Workspaces/dlw_static_reports_20261007/registration.json`。这些均为旧版记录，不代表当前 direct τ 主报告。旧 `register_static.py`、`register_compact.py` 不用于当前交付登记。

精简前的 HTML、源码、证据、截图和根记录保存于 `before_compact/`。direct τ 替换前的生成器、验证脚本与主 HTML 保存于 `before/direct_tau_generator_50a08adc630c4b929a9118e2a0a6a732/`。原先“5 段摘录／27 行／未重新执行 Notebook”及旧 Notebook 哈希 `10bd4b256d7ea80246d5cdd0dcf202a8f6bcec6e6cc41328f4b892bdc23a2cfe` 仅属于此前版本。
