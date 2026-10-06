# Report 可运行改造（agent 文档）

最终入口：根目录 `C:\Users\msz\aca\Report.exe`，双击后自动打开同目录 `Report.html`。原启动/停止 CMD 已移到 `Trash/report_launchers_before_packaging_20261002/`。EXE 是本机工作区的单一入口；报告、服务、Python、Lean/Mathlib 仍沿用本机环境，不将其说成迁移到任意机器的独立安装包。页面 lease 与闲置回收自动管理后台服务，计算期间不退出，无需用户单独停止。

## 正文与生成

保留旧报告的 36 个显示公式块、34 个编号、原表图、两份 CSS，以及现有正文衬线字体与字号。实际查看用户给的 Colab 后，单元按短中文段前说明、紧凑代码、原始输出的顺序排列；Run 改为带中文可访问名称的 ▶ 按钮，支持鼠标与键盘。Lean 代码加克制的语法配色，字体不变。起点与终点只展示实际运行的 Lean 单元，不展示 LaTeX 源码；原排版公式和中间推导保留。起点完整定义 `StartPoint`，终点直接使用它，移除与理论起点无关的导数/变量定义核对。当前正文采用 UW 四点、QRM 三点阅读指南；每路线仅有一个默认折叠的关键证明摘录，去掉完整依赖巨块，完整证明仍由导入阶段编译。两路验证保留实际的 `h≠0`、正实解析函数与双线性假设。

`StepUWStart` 只定义并打印双线性起点，`section` 也不是证明步骤。终点单元中的 `(hsp : StartPoint ...)` 是输入假设，冒号后的类型是目标，`:=` 后调用已编译的完整证明项；短 `example` 是由 Lean 检查的普遍命题证明，不是一个数值样例。实际封装顺序是 `c15_proved` 先得到式（8）的非线性方程组，再由 `physical_v` 识别重构场；式（7）则使用这一结果、第一残差恒等式和 W 守恒桥。阅读指南与关键摘录显示这些连接，不重复完整证明库。此次仅精简展示，六份实际执行源码、证明源与运行逻辑均未修改。

基础数学正文仍由 `Workspaces/gsg_project/dlw_report/_src/Report.md`、`generate_submission_report.py` 与既有数学资源构建流程维护。当前可运行扩展的生成入口为 `build_report.py`，输出 `report.src.html` 与根目录 `Report.html`。默认基础页是 `before/Report.html` 的改造前完整快照；修改旧数学正文或图表后，先按旧流程生成一个无 notebook 的新完整 HTML，再执行：

```powershell
python -X utf8 Workspaces/report_notebook_20261002/build_report.py --base '新的基础报告绝对路径'
```

不要以已经含 `lean-manifest` 的增强页为基础再次嵌套。生成器会拒绝该情况。`before/` 中的原始页面、进度档、文件索引保持，不删除文件。

## 执行语义

- Lean：每路线三个只读可信单元：import、起点检查、终点调用。import 首次实际重编译证明库；后两段只编译当前薄单元，沿用同一会话的已检查 `.olean`。源码、当前显示单元、库产物逐项哈希核对，前置阶段缺失或会话重置会拒绝后段。终点还核验标准三公理；网页直接显示此次 Lean 编译器的 stdout/stderr，不追加 OK、汇总或运行记录路径，也不折叠输出。当前材料为 `lean_material/stage_manifest.json`、`steps/`，完整服务规则见 `runtime/README.md`。
- 2HS：七个可编辑 JavaScript 单元，准备、配置、解析参考、空间/恢复、RK4、实际演化、误差图。默认同报告参数，二孤子仍为原有图表结果。
- DLW：七个可编辑单元，准备、配置、解析剖面、主系数、有限 h 残差、主系数表、格距收敛图。相位采样最大值不当作连续上界，局部残差不当作终点总场误差。
- 每个数值 group 持有一个 Worker；共享对象 `lab.hs` / `lab.dlw` 保存已运行定义与数据。当前 textarea 的源码送入 AsyncFunction，仅执行眼前单元；不自动执行或重放前置。上游修改清除后段结果并取消其完成标记；漏跑前置显示具体单元，不发起计算。按用户要求移除运行全部操作；重置状态保留编辑，恢复示例同时重置源码，Shift+Enter 可运行当前单元。
- Worker 15 秒超时与手动取消均终止该数值环境，需要从准备段重新开始。语法错误不执行源码，保留此前有效状态；运行期错误可能部分修改共享对象，故重置本节环境，不把旧状态冒充有效。打印使用同步的完整 pre 源码与当前输出。
- 数值准备与定义段无输出时保持空白；计算段保留代码实际 emit 的参数/结果表、实测残差与图形，不另加完成提示或总结。

## 验证证据

- `build_manifest.json`：原始公式/编号保留、产物哈希。
- `browser_validation.json`、`preview/`：真实浏览器运行、代码修改、状态依赖、语法错误/修复、取消、超时、恢复、重复运行、1440/390 布局与打印。
- `lean_ui_validation.json`：网页 Run 触发的完整编译、运行耗时、实际 result.json 与端点公理。
- `lean_material/validation.json`、`review.json`：原证明与显示入口、复制源哈希、独立科学表述审查。
- `error_material/validation.json`、`independent_validation.json`：DLW 默认与参数/核心修改、60 位独立解析检查。
- `error_material/hs_validation.json`、`hs_independent_validation.json`：2HS 默认表回归、改变 N/T/RHS、与既有保存场逐节点核对。
- `runtime/service_verification_*.json`：服务拒绝错误请求、可信源码约束、真实取消与启动/停止。

当前验证另见 `stepwise_browser_validation.json`、`stepwise_lean_ui_validation.json`、`runtime/stepwise_validation_uw.json`、`step_material/validation.json` 和 `package/verification_*.json`、`upgrade_verification_*.json`。前一版证据留存为历史。默认浏览器打开入口的最后自动验证被审批拒绝（仅给出 blocked by policy）；EXE 自动启动/复用/安全升级/无窗口/闲置退出均通过无浏览器测试，页面在真实浏览器逐段验证。

前次原始输出修订的证据为 `raw_output_validation.json`、`raw_output_preview/` 与 `step_material/raw_output_validation.json`。旧逐段测试中的 OK、注释及说明位置断言仅代表旧界面，不再作为当前展示约定。`before_raw_output/` 保存那轮修改前源码与页面。

当前精简证明展示的证据为 `compact_proof_validation.json` 与 `compact_proof_preview/`，核验 UW 四点/QRM 三点阅读指南、默认折叠的单一关键摘录、原排版与运行入口。`before_compact_proof/` 保存修改前材料。六份实际执行源码与完整证明源均未改变，继续使用下述真实编译证据；本轮不重复编译或改变运行逻辑。

此前 Colab 编排修订证据为 `colab_style_validation.json`、`colab_style_preview/`、`step_material/colab_style_validation.json` 与 `lean_material/colab_start_validation.json`。六个当前 Lean 输入已真实编译通过，沿用只读的已检查证明库，未重新编库；当前源码 hash 与该证据逐份匹配。服务版本为 2.2.0。`before_colab_style/` 保存该轮修改前材料。更早的完整证明默认展开展示已被本轮精简展示替换，旧验证及页面继续保留。

MIT 两份实际 ipynb 源及逐单元结构在 `step_material/refs/`，网页运行无需联网。页面不请求外网，不安装新数学环境、库或在线字体。所有支撑代码、证明快照、运行记录与预览位于本 workspace。
