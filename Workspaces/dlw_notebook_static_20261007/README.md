# DLW notebook 的单文件静态报告

当前交付：根目录 `dlw_numerical.html`，来源为已重新执行的 `notebook/DLW数值分析report.ipynb`。SD（raw bilinear）直接推进原双线性方程中的 F、G，采用隐式中点时间递推；SD2、FD 使用 Euler／RK4。三种方案由共同连续 u、v 初值出发，在公共物理点比较误差。

当前报告保留第 1—7 节，结束于局部误差曲线；移除目录、第 8 节“结果”、参考资料与完整代码附录。共有 30 个展示单元、112 个数学表达式及 8 项保存输出，其中有 5 张表、3 张 PNG 图。正文仍显示 6 段关键源码，共 54 行；SD 摘录 `SDModel.solve_one` 和 `advance`，其余为 SD2／FD 右端、Euler／RK4 与公共点误差代码。HTML 内嵌 KaTeX 公式及字体，可离线打开或发送单个文件。

静态生成器只读取 Notebook 的源码和保存输出。Notebook SHA-256 为 `831fad81459e614dfffc3b890c4c6dcbda4b7ee386dfa471826f781a9042bb8b`，HTML SHA-256 为 `25087fdada5a52387911782bcf203f8e5796acf0606cb0d5e072a43562c7d5c0`。本轮选取的 30 个单元 DOM 与精简前逐项相同，全部 112 个数学表达式保持；Notebook 文件字节保持。最新登记为 `trim_revision.json`，精简前 HTML、脚本、共享记录、核验证据与截图保存在 `before_trim/`。

## 生成与核验

在工作区根目录执行：

```powershell
$staticPython = 'C:\Users\msz\aca\Workspaces\report_colab_20261006\.venv\Scripts\python.exe'
& $staticPython -X utf8 Workspaces/dlw_notebook_static_20261007/build_static.py
& $staticPython -X utf8 Workspaces/dlw_notebook_static_20261007/verify_static.py
& node Workspaces/dlw_notebook_static_20261007/check_static.cjs
```

`build_static.py` 只转换内容，不执行 Notebook；SD 的完整核心方法通过 AST 摘录。`render_math.cjs` 使用已有本地 KaTeX 生成 HTML/MathML。`verify_static.py` 核对保留单元的关键摘录、正文（允许三项展示措辞替换）、公式源、表格数值、输出文本与原图字节，并确认目录与三个文末部分均已移除。各项计数读取当前 `build_validation.json`。`check_static.cjs` 用 Edge 在断网且禁用 JavaScript 的情况下检查桌面、390px 窄屏、打印样式，同时核对实际参与字形绘制的字体。

当前证据为 `build_validation.json`、`content_validation.json`、`browser_validation.json`、`trim_revision.json`。11 张 `report_*.png` 覆盖桌面与手机首页、SD 公式、SD 核心代码、比较表、误差图和打印样式；本轮截图哈希由 `trim_revision.json` 登记。`direct_tau_visual_validation.json` 保留此前完整报告的历史视觉记录。

## 字体与版式

中文／拉丁正文恢复旧 index 的 `Times New Roman, SimSun, serif`，版式沿用宋体论文正文、首行缩进与克制的标题字号。修复字体内嵌正则原先跨越 CSS 右花括号的问题，完整保留 20 条 KaTeX 字体注册及 `.katex` 基础样式；实际绘制证据确认正文使用 Times New Roman／SimSun，公式使用内嵌 KaTeX_Math-Italic，没有依赖 CSS 字体名称推断。输出中的打印文字随正文使用同一字体。

## 历史版本与登记

原 `index.html` 字节保存于 `before/index.html`；阅读留档为 `report/DLW数值分析_原HTML_20261007.html`，只加 `base href="../"` 保持相对链接。主入口随后按用户要求改名为 `dlw_numerical.html`。

此前完整展开版与代码精简版分别登记在本目录的 `registration.json`、`registration_compact.json`；两页改名阶段登记在 `Workspaces/dlw_static_reports_20261007/registration.json`。这些均为旧版记录，不代表当前 direct τ 主报告。旧 `register_static.py`、`register_compact.py` 不用于当前交付登记。

精简前的 HTML、源码、证据、截图和根记录保存于 `before_compact/`。direct τ 替换前的生成器、验证脚本与主 HTML 保存于 `before/direct_tau_generator_50a08adc630c4b929a9118e2a0a6a732/`。原先“5 段摘录／27 行／未重新执行 Notebook”及旧 Notebook 哈希 `10bd4b256d7ea80246d5cdd0dcf202a8f6bcec6e6cc41328f4b892bdc23a2cfe` 仅属于此前版本。
