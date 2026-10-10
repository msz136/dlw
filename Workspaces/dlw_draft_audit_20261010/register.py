from pathlib import Path
import shutil,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
prior=HERE/'registration_before'
prior.mkdir(exist_ok=True)
for name in ('PROGRESS_LOG.md','FILE_INDEX.md'):
    if not (prior/name).exists():shutil.copy2(ROOT/name,prior/name)
begin='<!-- DLW_PAPER_DRAFT_BEGIN -->'
p=ROOT/'PROGRESS_LOG.md';s=p.read_text(encoding='utf-8')
entry='> **2026-10-10（论文草稿完整推导审查）：** 新增 [审查报告](report/dlw_draft_audit_20261010.html)，独立重推全部理论链：连续双线性、交错构造、任意有限阶Gram、PE/PF、连续极限与Lax。590处HTML公式与源一致；主验证2415项及Taylor/谱/正性补验8项，共2423项精确检查通过。未发现第1—6节主命题的致命代数错误；记录3项P2（高频增长条件、PF增广跳跃初始化未写明、半离散守恒与实际网格律范围）及2项P3（B/C超出既定谱域但已独立补证正性、CN固定容差限制）。当前Notebook九组初态最大场差1.77e-13，补核PE节点通量缺陷与总质量区别，并复现CN接受Euler预测的标量反例。表内百分比核对一致；未重跑整批PDE轨道。审查页282处严格KaTeX、1440/390px无溢出或公式错误，已目视检查。原稿、正文源与Notebook均保持原样；源码、快照及证据在 Workspaces/dlw_draft_audit_20261010/。'
assert begin in s
if entry not in s:s=s.replace(begin,begin+'\n'+entry+'\n',1)
p.write_text(s,encoding='utf-8')
p=ROOT/'FILE_INDEX.md';s=p.read_text(encoding='utf-8')
tag='<!-- DLW_DRAFT_AUDIT_FILES_BEGIN -->'
entries=[('report/dlw_draft_audit_20261010.html','完整重推与适用范围审查报告')]
for path in sorted(HERE.rglob('*')):
    if path.is_file():
        rel=path.relative_to(ROOT).as_posix()
        desc=('登记前原件备份' if 'registration_before' in rel else
              '独立推导、符号/初始化核验、报告构建或排版证据')
        entries.append((rel,desc))
entries.append(('Workspaces/dlw_draft_audit_20261010/final_validation.json','交付时哈希与核验汇总'))
block=tag+'\n**DLW 草稿推导审查（2026-10-10）：**\n\n'+'\n'.join(f'- [{path}]({path})：{desc}。' for path,desc in entries)+'\n<!-- DLW_DRAFT_AUDIT_FILES_END -->\n\n'
if tag not in s:
    anchor='<!-- DLW_PAPER_DRAFT_INDEX_BEGIN -->'
    assert anchor in s
    s=s.replace(anchor,block+anchor,1)
p.write_text(s,encoding='utf-8')
verification=json.loads((HERE/'verification.json').read_text(encoding='utf-8'))
probe=json.loads((HERE/'numerical_probe.json').read_text(encoding='utf-8'))
for path,key in [(ROOT/'report/dlw_paper_draft.html','html_sha256'),(ROOT/'Workspaces/dlw_paper_20261009/manuscript.md','source_sha256')]:
    assert hashlib.sha256(path.read_bytes()).hexdigest()==verification[key]
assert hashlib.sha256((ROOT/'notebook/DLW数值分析report.ipynb').read_bytes()).hexdigest()==probe['notebook_sha256']
result={'original_html_source_notebook_unchanged':True,'symbolic_checks':2423,'initialization_cases':9,'new_PDE_trajectories':0,
        'build':json.loads((HERE/'build_validation.json').read_text(encoding='utf-8')),
        'layout':json.loads((HERE/'layout_validation.json').read_text(encoding='utf-8'))}
(HERE/'final_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
