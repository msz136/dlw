from pathlib import Path
import shutil
import datetime
import json

workspace = Path(r'C:\Users\msz\aca')
project = workspace / 'Workspaces' / 'dlw_integrability_lean_20261006'
records = []
for result_path in (project / '.lean-runs').glob('*/result.json'):
    result = json.loads(result_path.read_text(encoding='utf-8-sig'))
    if result.get('status') == 'PASSED' and Path(result['target']).name == 'FinalEndpoint.lean':
        records.append(result)
if not records:
    raise SystemExit('FinalEndpoint has not passed; final registration was not changed.')
final_result = max(records, key=lambda result: result['run_id'])
run_id = final_result['run_id']
module_count = len(final_result['files'])
date = datetime.date.today().isoformat()
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
backup = project / 'registration_before' / stamp
backup.mkdir(parents=True, exist_ok=True)

progress_path = workspace / 'PROGRESS_LOG.md'
index_path = workspace / 'FILE_INDEX.md'
for source in (progress_path, index_path):
    shutil.copy2(source, backup / source.name)

progress = progress_path.read_text(encoding='utf-8-sig')
begin = progress.index('<!-- DLW_HAMILTON_BEGIN -->')
end = progress.index('<!-- DLW_HAMILTON_END -->', begin)
block = progress[begin:end]
marker_begin = '<!-- DLW_LEAN_PROGRESS_BEGIN -->'
marker_end = '<!-- DLW_LEAN_PROGRESS_END -->'
update = f'''<!-- DLW_LEAN_PROGRESS_BEGIN -->
> **同专题 Lean 形式化（{date}，带显式基础前提的最终定理已通过）：** [证明报告](Workspaces/dlw_integrability_lean_20261006/LEAN_PROOF_REPORT.md)与 [FinalEndpoint.lean](Workspaces/dlw_integrability_lean_20261006/FinalEndpoint.lean) 位于 `Workspaces/dlw_integrability_lean_20261006/`，按用户要求仅交付 Markdown。Lean/Mathlib 4.34.0 的完整最终入口 `{module_count}` 个本地依赖模块重新编译全部 PASS，记录为 [result.json](Workspaces/dlw_integrability_lean_20261006/.lean-runs/{run_id}/result.json)。已证明一般闭合周期场的实际全阶谱量身份、正整数阶谱对易、沿给定光滑原 PDE 解的普通时间守恒、实际 K=-8G C1+(γ/c)P+常数及其真实时间生成性质；奇数谱族和最终 K,P,C3,C5,… 的每个有限前缀在实际 compact-jet C∞ 拓扑中有开稠密独立集。真实幅度二次系数、全阶最高 Fourier 项、非零 Vandermonde 子式和动量补充方向均已构造；见证和目标性质不再是最终输入。标准自由一阶因子 Adler 定理到 DLW 的切/余切坐标、1/8归一化、P0源与Ward投影修正均在 Lean 内证明。主定理保留 `FactorSpectralFoundation`：用户已允许循环留数迹和标准 Adler 乘积/求逆理论；具体正规 PDO 环、形式逆元与源代入表示的存在仍显式提供，这项额外基础范围的询问尚未答复，因此不宣称已从定义完成全部 PDO 基础。没有证明全局解存在、Baire 可数交强化或全局作用量—角变量。入口及关键定理只列出 propext/Classical.choice/Quot.sound，检查闭包无 sorry/admit/新 axiom；显式结构前提仍须按报告审阅。
<!-- DLW_LEAN_PROGRESS_END -->

'''
if marker_begin in block:
    p = block.index(marker_begin)
    q = block.index(marker_end, p) + len(marker_end)
    block = block[:p] + update.rstrip() + block[q:]
else:
    first_paragraph_end = block.index('\n\n', block.index('> **2026-10-06'))
    block = block[:first_paragraph_end + 2] + update + block[first_paragraph_end + 2:]
block = block.replace('> **2026-10-06（一般周期物理场',
    f'> **{date}（一般周期物理场', 1)
topic_end = '<!-- DLW_HAMILTON_END -->'
other_progress = (progress[:begin] + progress[end + len(topic_end):]).lstrip('\r\n')
progress_path.write_text(block.rstrip() + '\n' + topic_end + '\n\n' + other_progress,
    encoding='utf-8')

index = index_path.read_text(encoding='utf-8-sig')
begin = index.index('<!-- DLW_HAMILTON_INDEX_BEGIN -->')
end = index.index('<!-- DLW_HAMILTON_INDEX_END -->', begin)
block = index[begin:end]
marker_begin = '<!-- DLW_LEAN_INDEX_BEGIN -->'
marker_end = '<!-- DLW_LEAN_INDEX_END -->'
sources = sorted(project.glob('*.lean'))
source_lines = '\n'.join(f'- `Workspaces/dlw_integrability_lean_20261006/{p.name}`' for p in sources)
update = f'''<!-- DLW_LEAN_INDEX_BEGIN -->
**一般周期 DLW 的 Lean 形式化（带显式基础前提的最终定理已通过）：**

- [LEAN_PROOF_REPORT.md](Workspaces/dlw_integrability_lean_20261006/LEAN_PROOF_REPORT.md)（真实 Lean/LaTeX 起点与终点、全部外部基础前提、最终统一验证）
{source_lines}
- `Workspaces/dlw_integrability_lean_20261006/register_progress.py`（合并专题进度及逐文件索引）
- `Workspaces/dlw_integrability_lean_20261006/update_final_report.py`（根据最终 PASS 记录与源码哈希生成 Markdown 报告）
- `Workspaces/dlw_integrability_lean_20261006/BALANCED_COEFFICIENT_DERIVATION.md`（二阶系数计算的中间推导记录）
- `Workspaces/dlw_integrability_lean_20261006/.lean-runs/`（每次实际编译的源码哈希、日志与结果）
- `Workspaces/dlw_integrability_lean_20261006/registration_before/`（共享记录修改前备份）
<!-- DLW_LEAN_INDEX_END -->

'''
if marker_begin in block:
    p = block.index(marker_begin)
    q = block.index(marker_end, p) + len(marker_end)
    block = block[:p] + update.rstrip() + block[q:]
else:
    p = len('<!-- DLW_HAMILTON_INDEX_BEGIN -->')
    block = block[:p] + '\n' + update + block[p:]
index_path.write_text(index[:begin] + block + index[end:], encoding='utf-8')
print(f'Merged current Lean progress and {len(sources)} source files into existing DLW topic.')
print(f'Backup: {backup}')
