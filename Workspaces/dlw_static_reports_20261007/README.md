# DLW 两份主目录静态报告

交付：`dlw_numerical.html` 与 `dlw_integrability.html`，均为可离线双击阅读的单文件 HTML。Times New Roman／宋体正文、内嵌 KaTeX 字体和无需脚本的数学预渲染保持。

- `dlw_numerical.html`：由 `index.html` 直接改名，内容字节与改名前一致；5 段关键代码／27 行、6 张表、3 张原图。生成器仍在 `Workspaces/dlw_notebook_static_20261007/`，目标名已经更新。
- `dlw_integrability.html`：理论内容整合为五个阶段：方程与场空间 → 谱量与 Hamiltonian → 守恒与对易 → 泛型独立性 → 可积性结论。原来的 13 个小标题全部融入叙述，目录只保留五个入口；补充必要的段落过渡，修正旧节号引用。全部 88 处已渲染数学表达、原式（1）—（19）及末尾四行主定理代码保持。代码接口、编译输出、运行说明与完整代码附录继续不展示。形式 PDO 基础条件保留在谱族构造与结论中。

不编辑、不执行任何 notebook，也不编译 Lean。数值报告改名前字节及原记录保存在 `before/`；理论精简前材料保存在 `before_theory/`；五阶段整合前的 HTML、检查器、核验证据、截图、README 与根记录保存在 `before_flow/`。`before_flow/input_hashes.json` 记录本轮开始时的 notebook 与数值 HTML 哈希；可积性 notebook 已由主线程完成独立的文字修订，本轮按其当前版本核验，不恢复早期版本。`dlw_numerical.html` 内容未改变；原研究 HTML 留档继续在 `report/DLW数值分析_原HTML_20261007.html`。

## 构建与核验

```powershell
$reportPython = 'C:\Users\msz\aca\Workspaces\report_colab_20261006\.venv\Scripts\python.exe'
& $reportPython -X utf8 Workspaces/dlw_static_reports_20261007/restructure_integrability.py
& $reportPython -X utf8 Workspaces/dlw_static_reports_20261007/verify_reports.py
& node Workspaces/dlw_static_reports_20261007/check_reports.cjs
```

`restructure_integrability.py` 使用 `before_flow/dlw_integrability.html` 作为固定输入，整合现有数学正文，不重新读取或导出 notebook。`verify_reports.py` 逐项核对全部已渲染公式、样式与末尾代码保持，检查五个大节的内容归属、五个目录入口、仅八处衔接文字变化，以及本轮输入文件哈希。`check_reports.cjs` 在断网且禁用 JavaScript 的 Edge 中检查两页桌面、390px、打印视图；独立诊断页面确认实际使用的宋体与 KaTeX 字体。`build_integrability.py` 保留早期 notebook 导出的历史源码。

当前证据：`build_validation.json`、`content_validation.json`、`browser_validation.json`、`flow_revision.json`；6 张 PNG 为两页首页及可积性守恒／终点的真实预览。`theory_revision.json` 与 `registration.json` 保持此前理论精简和首次交付的历史登记，不用于核对本次整合结果；相应登记脚本也保持历史原样。
