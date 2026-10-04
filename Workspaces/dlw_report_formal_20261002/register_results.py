"""Register the verified two-route proof delivery in the shared index and progress log."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
evidence = json.loads((HERE / 'lean_validation.json').read_text(encoding='utf-8'))
html_check = json.loads((HERE / 'html_validation.json').read_text(encoding='utf-8'))
assert evidence['status'] == 'passed' and html_check['status'] == 'passed'
run = evidence['run_id']
modules = evidence['local_module_count']
topic = 'Report两路非线性化Lean证明'

progress_entry = (
    f'> **2026-10-02（{topic}）：** 新增report目录[双线性到两套非线性形式的Lean证明]'
    '(report/dlw_bilinear_nonlinear_lean.html)，严格从Report式（1）的SemiPair出发，'
    '第一路推出式（7）的u/未缩放omega闭合系统，第二路推出式（21）的Q/R演化与M势差约束，'
    '并证明式（22）全部u/omega/v重构及Q=F/sqrt(G_j G_{j+1})。'
    '统一入口Workspaces/lean_contracts/proofs/ReportEndpoints.lean，'
    '主定理bilinear_to_report7、bilinear_to_report21_22、bilinear_to_both；'
    f'标准核验run {run}，退出0、PASSED {modules}本地模块，当前全部源码SHA-256吻合。'
    '所有4个合并端点仅依赖propext/Classical.choice/Quot.sound，无sorry或新公理。'
    '真实Real.exp/商与Mathlib deriv；Q方程用E_Q=Q(A+C)/2直接从双线性信息取得，'
    '乘积残差E_P=−E_omega/h=R E_Q+Q E_R仅取消Q，允许R为零或变号，无零积分常数前提。'
    '范围h≠0、每j全(x,t)域正实联合解析F/G；当前Mathlib中SmoothL的裸ContDiff ℝ ⊤为ω解析阶，'
    '不冒充普通C∞或局部任意非零/复分支定理。'
    'Contracts与历史Main哈希保持；现有Report/index公式未改。'
    '新证据、页面生成、标准复核入口与宽窄屏检查在Workspaces/dlw_report_formal_20261002/。'
)
index_entry = f'''**{topic}（2026-10-02）：**

- [双线性到两套非线性形式的Lean证明](report/dlw_bilinear_nonlinear_lean.html)（共同起点Report式1；式7与式21/22两路完整终点、证明恒等式及核验证据）
- [ReportEndpoints.lean](Workspaces/lean_contracts/proofs/ReportEndpoints.lean)（统一入口；bilinear_to_report7、bilinear_to_report21_22、bilinear_to_both及中心sqrt比值）
- Workspaces/lean_contracts/proofs/ReportNonlinearUW.lean（真实未缩放omega、式7两条方程与物理v桥）
- Workspaces/lean_contracts/proofs/ReportNonlinearQRM.lean（实际Q/R/M构造、式21三条约束、式22全部重构与残差恒等式）
- Workspaces/lean_contracts/proofs/ReportQRMCalculus.lean、ReportQRatio.lean（指数/乘积真实微分、正规化Hirota恒等式与正实sqrt中心比值）
- Workspaces/lean_contracts/proofs/.lean-runs/{run}/result.json、build.log（{modules}模块统一PASSED，逐端点标准3公理审计）
- Workspaces/dlw_report_formal_20261002/lean_validation.json、verify_delivery.py、Check-Proofs.ps1（源码/冻结入口哈希与起终点范围核对、标准复核入口）
- Workspaces/dlw_report_formal_20261002/build_report.py、report.source.html、manifest.json（自包含论文式报告源与生成记录）
- Workspaces/dlw_report_formal_20261002/check_report.cjs、html_validation.json、report_1440.png、report_route2.png、report_390.png（数学/本地链接与宽窄屏核验）
- Workspaces/dlw_report_formal_20261002/register_results.py、registration.json（共享进度与索引登记记录）
'''

changes = []
for filename, addition in [('PROGRESS_LOG.md', progress_entry), ('FILE_INDEX.md', index_entry)]:
    file = ROOT / filename
    before = file.read_bytes()
    text = before.decode('utf-8-sig')
    newline = '\r\n' if b'\r\n' in before else '\n'
    text = text.replace('\r\n', '\n')
    if filename == 'PROGRESS_LOG.md':
        pattern = r'^> \*\*2026-10-02（' + re.escape(topic) + r'）：\*\*.*$'
        if re.search(pattern, text, re.M):
            text = re.sub(pattern, lambda _: addition, text, count=1, flags=re.M)
        else:
            text = addition + '\n\n' + text
    else:
        pattern = r'^\*\*' + re.escape(topic) + r'（2026-10-02）：\*\*\n\n(?:- .*\n)+'
        if re.search(pattern, text, re.M):
            text = re.sub(pattern, lambda _: addition, text, count=1, flags=re.M)
        else:
            first, rest = text.split('\n\n', 1)
            text = first + '\n\n' + addition + '\n' + rest
    after = text.replace('\n', newline).encode('utf-8')
    if before.startswith(b'\xef\xbb\xbf'):
        after = b'\xef\xbb\xbf' + after
    file.write_bytes(after)
    changes.append({'file': filename, 'before_sha256': hashlib.sha256(before).hexdigest(),
                    'after_sha256': hashlib.sha256(after).hexdigest()})
(HERE / 'registration.json').write_text(json.dumps({'status': 'registered', 'run_id': run,
    'changes': changes}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': 'registered', 'run_id': run, 'files': [v['file'] for v in changes]}))
