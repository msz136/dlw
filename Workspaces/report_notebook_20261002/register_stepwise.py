"""Merge single-entry and retained-cell execution into the existing Report topic."""
from pathlib import Path
import hashlib
import json
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
read=lambda rel:json.loads((HERE/rel).read_text(encoding="utf-8"))
browser=read("stepwise_browser_validation.json")
qrm=read("stepwise_lean_ui_validation.json")
uw=read("runtime/stepwise_validation_uw.json")
build=read("build_manifest.json")
raw=read("raw_output_validation.json")
colab=read("colab_style_validation.json")
compact=read("compact_proof_validation.json")
colab_lean=read("lean_material/colab_start_validation.json")
current_stages=read("lean_material/stage_manifest.json")
report_sha=hashlib.sha256((ROOT/"Report.html").read_bytes()).hexdigest()
assert not compact["errors"] and all(c["passed"] for c in compact["checks"])
assert compact["stageCodeUnchanged"] is True and compact["proofSourcesUnchanged"] is True
assert compact["reportSha256"]==report_sha
assert not colab["errors"] and all(c["passed"] for c in colab["checks"])
assert colab_lean["status"]=="PASSED" and colab_lean["proofSourcesUnchanged"]
for route in colab_lean["routes"]:
    assert [c["stage"] for c in route["cells"]]==["import","start","endpoint"]
    for cell in route["cells"]:
        assert cell["exitCode"]==0 and cell["sha256"]==current_stages["cases"][route["route"]][cell["stage"]]["sha256"]
assert not raw["errors"] and all(c["passed"] for c in raw["checks"])
assert [c["stage"] for c in raw["leanStages"]]==["import","start","endpoint"]
assert all(c["cellResult"]["status"]=="PASSED" for c in raw["leanStages"])
assert not browser["errors"] and all(c["passed"] for c in browser["checks"])
assert [c["stage"] for c in qrm["stages"]]==["import","start","endpoint"]
assert all(c["cellResult"]["status"]=="PASSED" for c in qrm["stages"])
assert all(c["status"]=="ok" and c["cellResult"]["status"]=="PASSED" for c in uw["stages"])
assert build["originalDisplayMathBlocksPreserved"] and build["originalEquationTags"]==build["outputEquationTags"]
exe_sha=hashlib.sha256((ROOT/"Report.exe").read_bytes()).hexdigest()
assert exe_sha==read("package/build.json")["sha256"]

summary=(
    "**关键证明精简与阅读指南（当前）：** UW正文按四点、QRM按三点组织，"
    "每路线仅保留一个默认折叠的关键证明摘录，完整证明与依赖巨块移出正文。"
    "StartPoint单元仅定义/打印双线性起点；终点的hsp是输入，冒号后的类型是目标，"
    ":=后调用由Lean检查的完整证明项，短example为普遍命题证明。"
    "实际c15先给出式（8），physical_v识别重构场；式（7）通过第一残差恒等式和W守恒桥得到。"
    "原字体/公式、六份实际执行源码、证明源及逐段运行逻辑均未修改，沿用既有真实编译证据；"
    "当前浏览器验证与截图在compact_proof_validation.json、compact_proof_preview/，"
    "修改前材料保存在before_compact_proof/。"
    " **此前Colab编排修订（证明展示已由本次精简）：** 实际打开用户指定的MIT Colab，采用短中文正文→代码→原始输出的节奏。"
    "20个单元均有简洁中文段前说明，流程解释移出代码，保留局部数学注释，减少空行；"
    "Lean只读代码加克制语法配色，沿用原正文/代码字体字号。"
    "全部Run按钮换为▶，含中文可访问名称及键盘运行；原逐段状态和原始输出规则保留。"
    "两路线起点改为完整双线性StartPoint定义，删去导数/变量rfl核对；终点实际直接接收StartPoint。"
    "六薄单元逐份重新编译为0/PASSED，显示源码/hash与真实输入一致，原证明库及其产物未改。"
    "14数值单元仅说明/注释变化，默认与参数/算法编辑回归通过；真实浏览器验证中文说明、三角按钮、"
    "键盘/鼠标逐段运行、前段不重放、字体/公式无误；预览在colab_style_preview/。"
    "服务2.2.0保留现有会话、原始编译器输出与后台管理；最终Report.html/Report.exe入口不变。"
    " **此前原始输出修订（起点及说明位置已被本次替换）：** 取消逐段OK与完成总结；"
    "起点/终点仅保留精确Lean源码，移除LaTeX源码但保留排版公式与中间推导。"
    "当时每路线完整证明与依赖合成默认展开的源码块（历史展示，已被当前关键摘录替换）；"
    "模块边界和当前Run编译example/公理查询、import重编证明库的关系写入注释。"
    "Lean 2.1.0服务新增独立compilerOutput通道，显示真实编译器stdout/stderr，"
    "不混入checker的CHECK/PASSED/REPORT记录，输出无需展开。"
    "Windows禁止第二服务共享已有端口，实际核验绑定拒绝且原实例/PID状态文件保留。"
    "数值定义/准备段无输出则空白，保留真实参数、演化、误差表、图与实测连续方程残差。"
    "新真实浏览器核验14数值段默认结果、六份可见Lean输入、UW三阶段编译与原始输出逐字吻合，"
    "以及1440/390排版与打印；旧数学结果和原公式保留。"
    "**单入口与逐段会话修订：** 根目录只保留[Report.exe](Report.exe)作为打开入口，"
    "旧启动/停止CMD移至Trash/report_launchers_before_packaging_20261002/；"
    "18KB Windows GUI入口自动隐藏启动服务、复用同工作区实例，并用页面lease/闲置回收管理后台。"
    "它依赖本机现有Workspaces/Python/Lean，不冒称可跨机器独立安装包。"
    "已真实读取MIT两份ipynb（共65单元），按持久对象、定义与推进分开的节奏改造[Report.html](Report.html)。"
    "取消运行全部与自动前置重放，数值两组各7段（准备/配置/定义/计算），"
    "当前可见源码经AsyncFunction只运行眼前段，持久Worker中lab.hs/lab.dlw保存定义和数据；"
    "漏前置不计算、修改上游后段失效、重跑只替换本段输出，运行期错误/取消/15秒超时重置该环境，"
    "语法错保留未被执行修改的有效前置。"
    "Lean两路线各import→起点→终点三段；首次import真实重编证明库，后两段只编当前固定薄单元，"
    "复用同会话已检查且hash吻合的库/产物，不提前执行终点调用。UW实际三段约77.4/14.9/15.3秒；"
    "QRM网页三次独立点击约128.1/14.6/15.5秒，真实PASSED、四端点只标准三公理，"
    "前置/旧会话/重置与显示单元hash均校验。"
    "此前14项逐段浏览器检查通过：单段状态、未演化无图、前置不重放、参数/核心编辑生效、错误/恢复、"
    "取消/超时、2HS原默认数值回归、1440/390排版与打印、离线无HTTP。"
    "入口并发启动复用、无可见终端、闲置退出、活动任务保护及空闲升级已通过；"
    "正常打开默认浏览器的最终自动验证被审批拦截（仅给出blocked by policy），已采用本地服务和浏览器核验页面。"
    "原36公式块/34编号/表图/正文CSS继续保留。"
    "当前源码、refs、验证及入口构建均在Workspaces/report_notebook_20261002/；"
    "新数值材料step_material/、Lean steps/stage_manifest、服务stepwise_lean.py、package/ReportLauncher.cs。"
    " **此前可运行改造（前置重放与多CMD已被本次替代）：** "
)
progress_path=ROOT/"PROGRESS_LOG.md"
blocks=re.split(r"\n\s*\n",progress_path.read_text(encoding="utf-8"))
i=next(i for i,b in enumerate(blocks) if b.startswith("> **2026-10-02（Report两路非线性化Lean证明"))
old=blocks.pop(i).split("）：** ",1)[1]
if "**此前可运行改造（前置重放与多CMD已被本次替代）：** " in old:
    old=old.split("**此前可运行改造（前置重放与多CMD已被本次替代）：** ",1)[1]
blocks.insert(0,"> **2026-10-02（Report两路非线性化Lean证明与可运行报告）：** "+summary+old)
progress_path.write_text("\n\n".join(blocks).rstrip()+"\n",encoding="utf-8")

index_path=ROOT/"FILE_INDEX.md"
index=index_path.read_text(encoding="utf-8")
index=re.sub(r"^- \[Report\.html\]\(Report\.html\).*?$","- [Report.html](Report.html)（论文排版；中文说明→代码→原始输出，▶逐段运行，UW四点/QRM三点指南与默认折叠的关键证明摘录）",index,count=1,flags=re.M)
begin="<!-- REPORT_NOTEBOOK_INDEX_BEGIN -->";end="<!-- REPORT_NOTEBOOK_INDEX_END -->"
new=[begin,"","**Report 单入口与逐段运行（2026-10-02）：**","",
     "- [Report.exe](Report.exe)（单一用户入口；自动后台服务与打开报告，现有本机环境）"]
meaning={
    "README.md":"当前关键证明阅读指南、生成、持久单元和单入口说明",
    "build_report.py":"保持原排版生成逐段增强页与精简关键证明展示",
    "notebook.js":"持久Worker、显式前置检查、仅当前段执行、Lean三阶段与页面lease",
    "notebook.css":"沿用正文的代码/结果与窄屏/打印排版",
    "report.src.html":"当前增强页源码，UW四点/QRM三点指南与单一折叠关键摘录",
    "build_manifest.json":"原公式/编号/产物哈希",
    "check_stepwise.cjs":"实际数值单段执行与持久状态/编辑/错误/取消/超时/窄屏/打印核验",
    "stepwise_browser_validation.json":"14项新浏览器检查证据",
    "stepwise_max_points_validation.json":"最大10001个空间点的逐段演化与两幅绘图核验",
    "check_raw_output.cjs":"原始输出、单块Lean展示、注释与当前UW真实三阶段的浏览器核验",
    "raw_output_validation.json":"前次原始输出逐字核对与数值默认结果/排版证据",
    "colab_style_validation.json":"此前中文段前说明/三角按钮/键盘及鼠标逐段运行/精确Lean输入的浏览器核验",
    "compact_proof_validation.json":"当前阅读指南/单一默认折叠关键摘录/排版核验与执行、证明源不变证据",
    "check_stepwise_lean_ui.cjs":"QRM网页import/起点/终点三段及重置验证",
    "stepwise_lean_ui_validation.json":"三次独立点击、同会话真实cell PASSED与公理",
    "register_stepwise.py":"本专题合并登记入口",
    "stepwise_registration.json":"当前报告/入口/共享记录哈希",
    "step_material/build_material.py":"从旧数值实现拆分显式共享状态的当前单元",
    "step_material/cells.json":"DLW七段当前代码与前置关系",
    "step_material/hs_cells.json":"2HS七段当前代码与前置关系",
    "step_material/intro.html":"DLW残差/主系数/全波形上界说明",
    "step_material/hs_intro.html":"2HS单孤子逐段演化与误差说明",
    "step_material/README.md":"当前数值单元共享接口和说明",
    "step_material/validate_material.cjs":"逐cell真实执行、同原默认回归、缺前置/编辑/语法核验",
    "step_material/validation.json":"当前数值实现核验",
    "step_material/raw_output_validation.json":"去除人为输出、注释修订后的数学结果与单元核验",
    "step_material/colab_style_validation.json":"中文lead/局部注释/空行修改后可执行数学不变与默认/编辑回归",
    "step_material/fetch_mit_refs.py":"公开参考ipynb源快照读取",
    "step_material/refs/MIT_NOTEBOOK_REVIEW.md":"两份MIT参考实际单元节奏分析",
    "step_material/refs/notebook_structure.json":"65单元结构、来源及源码SHA",
    "lean_material/stage_manifest.json":"六个可信Lean单元的精确显示源码与hash",
    "lean_material/raw_output_semantic_validation.json":"上一版六Lean单元仅注释变化的历史核验",
    "lean_material/colab_start_validation.json":"当前StartPoint与终点实际衔接、六精确单元真实编译为0的完整证据",
    "runtime/report_server.py":"2.2同源可信服务、独立原始编译器通道、会话/lease/自动回收",
    "runtime/stepwise_lean.py":"import一次检查库、后段实际编当前cell、源/产物hash校验",
    "runtime/stepwise_validation_uw.json":"UW三阶段真实PASSED与前置/重置核验",
    "runtime/raw_compiler_validation.json":"真实Lean成功、类型错误、stderr及Unicode原始输出传输核验",
    "runtime/exclusive_binding_validation.json":"Windows第二服务绑定被拒绝且原服务身份/状态文件保留的实际验证",
    "runtime/README.md":"当前2.0接口与执行语义",
    "package/ReportLauncher.cs":"Windows GUI单入口、隐藏启动、版本/实例检查与安全升级",
    "package/build-launcher.ps1":"使用已有.NET编译器构建入口",
    "package/build.json":"EXE当前构建/hash记录",
    "package/Report.exe":"已构建根入口的工作副本",
    "package/README.md":"真实本机单入口范围与验证说明",
    "package/verify-launcher.ps1":"并发启动/复用/无窗口/自动退出测试",
    "package/verify-upgrade.py":"隔离fixture中的活动任务保护与空闲升级",
    "package/verification_20261002_125350_504.json":"单入口真实并发/无窗口/闲置退出证据",
    "package/upgrade_verification_20261002_125409_661959.json":"空闲升级/任务保护/中文提示证据",
}
for rel,description in meaning.items():
    if rel!="stepwise_registration.json":assert (HERE/rel).exists(),rel
    new.append(f"- [{rel}](Workspaces/report_notebook_20261002/{rel})（{description}）")
for rel in sorted((HERE/"step_material").glob("*.js")):
    new.append(f"- [{rel.name}](Workspaces/report_notebook_20261002/step_material/{rel.name})（对应可见单元源码）")
for rel in sorted((HERE/"lean_material/steps").glob("*.lean")):
    new.append(f"- [{rel.name}](Workspaces/report_notebook_20261002/lean_material/steps/{rel.name})（固定可信分段编译源码）")
new += [
    "- `Workspaces/report_notebook_20261002/step_material/refs/*.ipynb`（MIT两份公开参考原快照，不在运行时加载）",
    "- `Workspaces/report_notebook_20261002/stepwise_preview/*.png`（1440/390布局、QRM三阶段真实OK）",
    "- `Workspaces/report_notebook_20261002/raw_output_preview/*.png`（当前单块源码/编译原始输出/数值结果的1440与390布局）",
    "- `Workspaces/report_notebook_20261002/compact_proof_preview/*.jpg`（当前UW四点/QRM三点阅读指南与单一折叠关键证明摘录的实际页面预览）",
    "- `Workspaces/report_notebook_20261002/colab_style_preview/*.jpg`（此前中文说明、Lean起点及三角运行按钮的实际页面预览）",
    "- `Workspaces/report_notebook_20261002/lean_material/colab_validation_runs/*/`（六个当前精确薄单元的新编译产物与真实输出，既有库只读）",
    "- `Workspaces/report_notebook_20261002/before_compact_proof/`（精简完整证明展示并加入阅读指南前的源码与页面备份）",
    "- `Workspaces/report_notebook_20261002/before_colab_style/`（中文段前说明/StartPoint/三角按钮修订前源码与页面备份）",
    "- `Workspaces/report_notebook_20261002/before_raw_output/`（本轮输出/源码展示修订前材料备份）",
    "- `Workspaces/report_notebook_20261002/before_stepwise/`（本轮修改前页面、代码与证据；旧首次EXE构建保留）",
    "- `Trash/report_launchers_before_packaging_20261002/启动报告.cmd`、`停止报告.cmd`（旧根入口存档，当前不用）",
    "- `Workspaces/report_notebook_20261002/lean_material/proofs/`、`error_material/`（原可信证明快照与原数值实现/独立核查，未改数学内容）",
    "- `Workspaces/report_notebook_20261002/runtime/jobs/*/job.json`、`cell-result.json`、`lib/lean/*.olean`（每会话真实编译/产物记录）",
    "- `Workspaces/report_notebook_20261002/lean_material/proofs/.lean-runs/*`（标准证明库重编记录与源码hash）",
    "- `Workspaces/report_notebook_20261002/package/logs/`、`verification_*.json`、`upgrade_verification_*.json`（全部入口/测试历史记录）",
    "- `Workspaces/report_notebook_20261002/check_notebook.cjs`、`check_lean_ui.cjs`、`browser_validation.json`、`lean_ui_validation.json`、`register_records.py`、`registration.json`、`preview/`、`before/`（前一版完整证据与基础页，保留为历史，不作为新版再测试入口）",
    "",end,""
]
index=re.sub(re.escape(begin)+r"[\s\S]*?"+re.escape(end),"\n".join(new).rstrip(),index,count=1)
index_path.write_text(index,encoding="utf-8")
record={"reportSha256":report_sha,"exeSha256":exe_sha,"progressSha256":hashlib.sha256(progress_path.read_bytes()).hexdigest(),"indexSha256":hashlib.sha256(index_path.read_bytes()).hexdigest(),"rootCmdFiles":len(list(ROOT.glob("*.cmd"))),"actualBrowserChecks":len(compact["checks"]),"previousColabBrowserChecks":len(colab["checks"]),"previousRawOutputBrowserChecks":len(raw["checks"]),"previousStepwiseBrowserChecks":len(browser["checks"]),"defaultBrowserLaunchTest":"automatic approval rejected: blocked by policy"}
(HERE/"stepwise_registration.json").write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(record,ensure_ascii=False))
