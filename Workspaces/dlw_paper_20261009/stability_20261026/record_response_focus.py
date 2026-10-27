"""Record the user's final response-only scope without replacing other work slots."""
from pathlib import Path
import re
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

index = ROOT / 'FILE_INDEX.md'
original = index.read_bytes()
src = original.decode('utf-8')
line = next(line for line in src.splitlines() if line.startswith('| DLW 独立物理场扰动 |'))
replacement = '| DLW 独立物理场扰动 | A/D、高斯与正弦的独立 u/v 扰动响应及连续认证探索 | 正文聚焦6.1线性机制与6.2数值响应；连续认证暂缓，完整误差界未取得；高阶正则性与变换路线证明稿单独保留 | [主论文 Section 6](dlw-paper.html#section-6)；[扰动报告](report/dlw_independent_stability_20261026.html)；[认证进展](report/dlw_reference_certification_20261026.html)；[入口与目录](Workspaces/dlw_paper_20261009/stability_20261026/README.md) |'
assert index.read_bytes() == original
index.write_bytes(src.replace(line, replacement, 1).encode('utf-8'))

report = ROOT / 'report/dlw_independent_stability_20261026.html'
original = report.read_bytes()
src = original.decode('utf-8')
if 'dlw_reference_certification_20261026.html' not in src:
    note = '<p>连续参考认证的后续分析见<a href="dlw_reference_certification_20261026.html">专题报告</a>。主论文 Section 6 目前集中讨论线性机制与数值扰动响应。</p>'
    src, n = re.subn(r'(<h1\b[^>]*>.*?</h1>)', lambda m: m[0] + note, src, count=1, flags=re.S)
    assert n == 1 and report.read_bytes() == original
    report.write_bytes(src.encode('utf-8'))

progress = ROOT / 'PROGRESS_LOG.md'
original = progress.read_bytes()
src = original.decode('utf-8')
assert '## 本次工作｜DLW 独立扰动与 Section 6' in src
previous = src[src.index('## 上一次工作'):]
history = ROOT / 'Workspaces/workspace_catalog_audit_20261013/progress_history/2026-10.md'
entry = ('\n\n### 2026-10-26｜DLW 独立扰动：认证进展与正文聚焦\n\n'
         '整理实际正弦数据的横向Gevrey障碍、常背景形式级数发散及特定有限Laplace链非终止证明稿；完整连续误差界仍未取得。随后按用户要求暂缓认证，主论文仅保留6.1线性机制与6.2扰动响应，说明场间传递、横向区域及采样影响；撤下6.3，材料保留专题报告。29图7表及其他章节不变。证据：`report/dlw_reference_certification_20261026.html`；`Workspaces/dlw_paper_20261009/stability_20261026/response_focus_validation.json`。\n')
with history.open('a', encoding='utf-8', newline='') as f:
    f.write(entry)
current = ('# 当前工作与最近交接\n\n'
    '## 本次工作｜DLW 独立扰动与 Section 6（2026-10-26，聚焦响应；认证暂缓）\n\n'
    '主论文现只保留6.1线性机制与6.2独立扰动响应，撤下6.3，认证材料单独保留。A/D、高斯、正弦各独立扰动u或v，八条轨道到T=.01；h=Δx=.1、RK4 Δt=1e−4、ε=1e−6、κ=π/2。正文说明场间传递，D/A的v→u差异主要由横向积分及区域长度解释，高斯/正弦略低于初值的节点峰值包含平移采样效应。图表按规定ε归一化，不混用实测初峰增益。\n\n'
    '连续参考ηu/ηv仍未取得。新增实际正弦横向Gevrey障碍等为附条件证明稿，不是一般光滑解不存在定理。用户已暂缓认证，下一步仅按需润色6.1/6.2，不自行重启认证或对齐摘要、引言、结论。其他章节、29图7表保持原样并核验。入口：`dlw-paper.html#section-6`；`report/dlw_reference_certification_20261026.html`；`Workspaces/dlw_paper_20261009/stability_20261026/README.md`。\n\n')
updated = current + previous
assert len(updated) < 3000 and progress.read_bytes() == original
progress.write_bytes(updated.encode('utf-8'))

for path in [ROOT/'dlw-paper.html', report, ROOT/'report/dlw_reference_certification_20261026.html']:
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    assert not soup.select('.katex-error')
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'dlw-paper.html#section-6' in href:
            assert href.rsplit('#', 1)[1] in ['section-6','section-6.1','section-6.2']
print('Index, reports, history and two-slot progress updated. Main-paper Section 6 links and formula rendering verified.')
