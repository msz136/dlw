"""Merge this Report topic into the current shared progress and file index."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
build = json.loads((HERE / "build_manifest.json").read_text(encoding="utf-8"))
lean = json.loads((HERE / "lean_ui_validation.json").read_text(encoding="utf-8"))
browser = json.loads((HERE / "browser_validation.json").read_text(encoding="utf-8"))
assert build["originalDisplayMathBlocksPreserved"]
assert build["originalEquationTags"] == build["outputEquationTags"]
assert {c["route"] for c in lean["cases"]} == {"uw", "qrm"}
assert all(c["runResult"]["status"] == "PASSED" for c in lean["cases"])
assert not browser["errors"] and all(c["passed"] for c in browser["checks"])

description = (
    "**可运行报告改造：** 已将根目录[Report.html](Report.html)改为正文内可运行报告，"
    "沿用 local-learning-lab 的 MIT notebook 叙述—代码—输出节奏；原36显示公式块、34编号、两表四图和原CSS逐字保留。"
    "两条路线的起点/终点均显示Lean写法与原LaTeX源码，长证明折叠，中间原推导保留；"
    "只读端点调用与完整import闭包每次实际重编译，展示/执行/原研究模块哈希一致才允许运行。"
    "网页Run实际PASSED：UW5模块约89.9秒、QRM8模块约140.3秒，四端点仅标准三公理，"
    "范围每j全域正实联合解析F/G且h≠0（裸ContDiff ℝ ⊤为ω解析阶）。"
    "新增7可编辑JS单元：2HS单孤子按原N1600/a=.005/RK4/160步/32001点现场复算，"
    "四项终点误差与原表最大差1.14e−12，原保存场逐节点差≤1.33e−12；二孤子保留原图表。"
    "DLW纯y二阶主系数、全波形解析上界、有限h残差比较及减半收敛现场计算，"
    "168项60位独立核查、默认/参数/核心修改通过，收敛阶约2；不把采样峰值当连续上界或局部残差当总场误差。"
    "真实浏览器验证源码编辑生效、依赖失效、语法报错/修复、重置/恢复、重复运行、取消/15秒超时、"
    "1440/390无页面溢出和打印完整源码；静态运行无HTTP请求。"
    "[启动报告.cmd](启动报告.cmd)/[停止报告.cmd](停止报告.cmd)控制127.0.0.1:8766的本地Lean服务，"
    "服务错误请求、哈希不符、跨域、单作业限制与真实取消均核验。"
    "扩展生成入口、独立证明快照、数值源码/核验、浏览器/Lean证据及修改前页面统一在"
    "Workspaces/report_notebook_20261002/；原数学正文仍在既有Report.md，"
    "新可运行层权威源是本专题build_report.py+notebook.js/css及材料JSON。 **此前同日形式证明：** "
)

progress_path = ROOT / "PROGRESS_LOG.md"
progress = progress_path.read_text(encoding="utf-8")
blocks = re.split(r"\n\s*\n", progress)
topic = next((i for i,b in enumerate(blocks) if b.startswith("> **2026-10-02（Report两路非线性化Lean证明")),None)
heading = "> **2026-10-02（Report两路非线性化Lean证明与可运行报告）：** "
if topic is not None:
    old = blocks.pop(topic)
    body = old.split("）：** ",1)[1]
    if "**此前同日形式证明：** " in body:
        body = body.split("**此前同日形式证明：** ",1)[1]
    blocks.insert(0,heading+description+body)
else:
    blocks.insert(0,heading+description)
progress_path.write_text("\n\n".join(blocks).rstrip()+"\n",encoding="utf-8")

index_path = ROOT / "FILE_INDEX.md"
index = index_path.read_text(encoding="utf-8")
index = re.sub(r"^- \[Report\.html\]\(Report\.html\).*?$", "- [Report.html](Report.html)（保持原论文排版的可运行报告；两路LaTeX/Lean起终点、真实完整证明Run、2HS单孤子双方案现场复算、DLW空间误差估计）",index,count=1,flags=re.M)
index = index.replace("（权威正文／生成模板）","（基础数学正文／基础生成模板；可运行扩展见 report_notebook_20261002/build_report.py）",1)
begin = "<!-- REPORT_NOTEBOOK_INDEX_BEGIN -->"
end = "<!-- REPORT_NOTEBOOK_INDEX_END -->"
if begin in index:
    index = re.sub(re.escape(begin)+r"[\s\S]*?"+re.escape(end)+r"\n?","",index)
entries = [begin,"","**Report 可运行改造（2026-10-02）：**","",
    "- [启动报告.cmd](启动报告.cmd)、[停止报告.cmd](停止报告.cmd)（根目录双击入口）"]
files = {
    "README.md":"agent复现、生成与执行说明",
    "build_report.py":"在原报告上追加可运行单元；默认基础页为before/Report.html，可传新的无扩展基础页",
    "report.src.html":"当前完整可运行网页源码",
    "notebook.js":"可终止Worker、同作用域依赖重放、状态/错误/取消、真实Lean服务接入与输出渲染",
    "notebook.css":"代码与输出排版，原正文CSS保持，窄屏与打印支持",
    "build_manifest.json":"公式/编号保留及产物哈希",
    "check_notebook.cjs":"实际浏览器默认/修改/报错/恢复/取消/超时/宽窄屏/打印核验",
    "browser_validation.json":"浏览器核验记录",
    "check_lean_ui.cjs":"真实网页Run与实际编译记录校验",
    "lean_ui_validation.json":"UW/QRM网页运行，真实PASSED/耗时/哈希/端点公理",
    "register_records.py":"本专题合并登记入口",
    "registration.json":"当前报告/进度档/文件索引的登记哈希",
    "lean_material/manifest.json":"起终点Lean/LaTeX、真实条件、闭包与显示源码哈希",
    "lean_material/build_material.py":"从既有真实证明抽取并构建端点材料与固定验证入口",
    "lean_material/audit_validation.py":"已完成编译的逐源/端点公理审计",
    "lean_material/correct_regularity_metadata.py":"明确当前Mathlib裸⊤为ω解析阶的文字修订",
    "lean_material/README.md":"Lean数学范围与材料说明",
    "lean_material/validation.json":"全部实际编译与hash/公理核验",
    "lean_material/review.json":"独立科研含义、端点、公式/CSS与状态语义审查",
    "error_material/cells.json":"DLW三代码单元定义",
    "error_material/intro.html":"DLW残差/主系数/上界说明",
    "error_material/config.js":"DLW谱参数、格距、相位网格配置",
    "error_material/core.js":"DLW解析sigmoid导数、主系数、统一上界、有限h残差",
    "error_material/compare.js":"DLW采样峰值、上界、格距减半表与曲线",
    "error_material/prepare_and_validate.cjs":"DLW材料打包与默认/参数/核心修改验证",
    "error_material/validation.json":"DLW数值与修改行为证据",
    "error_material/validate_independent.py":"60位独立导数/有限h模板核查",
    "error_material/independent_samples.json":"独立核查采样数据",
    "error_material/independent_validation.json":"168项独立DLW核查",
    "error_material/hs_cells.json":"2HS四代码单元定义",
    "error_material/hs_intro.html":"2HS现场复算及默认条件说明",
    "error_material/hs_config.js":"2HS节点/格距/时间/评价网格配置",
    "error_material/hs_reference.js":"2HS解析单孤子与物理坐标反解",
    "error_material/hs_core.js":"2HS双方案场恢复、Thomas、RHS和RK4",
    "error_material/hs_compare.js":"真实2HS演化、插值误差、分段误差曲线及默认表回归",
    "error_material/prepare_hs.cjs":"2HS材料打包与参数/核心修改验证",
    "error_material/hs_validation.json":"2HS默认/加密/时间/核心修改证据",
    "error_material/hs_live_default_fields.json":"2HS默认现场终点场",
    "error_material/validate_hs_fields.py":"与原保存场及独立边界逐节点核对",
    "error_material/hs_independent_validation.json":"2HS逐节点/边界差值核验",
    "runtime/report_server.py":"回环地址可信固定Lean验证服务，完整重新编译/来源hash/公理检查/取消",
    "runtime/Start Report.cmd":"运行服务与浏览器启动入口",
    "runtime/Stop Report.cmd":"停止本地服务入口",
    "runtime/start-report.ps1":"隐藏启动、健康检查、重复启动复用",
    "runtime/stop-report.ps1":"随机令牌停止及作业终止",
    "runtime/verify_service.py":"服务请求拒绝/源码约束/单作业与真实取消验证",
    "runtime/README.md":"服务接口、固定编译语义与记录",
}
for rel, meaning in files.items():
    if not (HERE/rel).exists():raise ValueError(f"Index target missing: {rel}")
    target = f"Workspaces/report_notebook_20261002/{rel}"
    entries.append(f"- [{rel}]({target})（{meaning}）")
entries += [
    "- `Workspaces/report_notebook_20261002/lean_material/proofs/*.lean`（5/8模块固定验证闭包；ExampleUW/ExampleQRM与7份既有原样依赖）",
    "- `Workspaces/report_notebook_20261002/lean_material/*.txt`（起点、端点、变量及调用展示摘录）",
    "- `Workspaces/report_notebook_20261002/lean_material/proofs/.lean-runs/*/result.json`、`build.log`（每次独立真实编译结果与日志）",
    "- `Workspaces/report_notebook_20261002/runtime/service_verification_*.json`、`lifecycle_verification_*.json`（服务与启动停止核验）",
    "- `Workspaces/report_notebook_20261002/runtime/jobs/*/job.json`、`server-state.json`、`server_*.log`（运行/后台服务状态与日志，原样保留）",
    "- `Workspaces/report_notebook_20261002/preview/*.png`（真实1440/390截图、Lean网页OK）",
    "- `Workspaces/report_notebook_20261002/before/Report.html`、`PROGRESS_LOG.md`、`FILE_INDEX.md`（本次改造前副本）",
    "",end,"",
]
anchor = "- [Report.html](Report.html)"
line_end=index.index("\n",index.index(anchor))
index=index[:line_end+1]+"\n"+"\n".join(entries)+index[line_end+1:]
index_path.write_text(index,encoding="utf-8")
record={"reportSha256":hashlib.sha256((ROOT/'Report.html').read_bytes()).hexdigest(),"progressSha256":hashlib.sha256(progress_path.read_bytes()).hexdigest(),"indexSha256":hashlib.sha256(index_path.read_bytes()).hexdigest(),"mergedExistingReportTopic":topic is not None}
(HERE/"registration.json").write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(record,ensure_ascii=False))
