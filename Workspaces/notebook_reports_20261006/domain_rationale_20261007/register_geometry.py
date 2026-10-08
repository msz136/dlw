"""Record the analytic domain rationale without changing the numerical report."""
from pathlib import Path
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
check = json.loads((HERE/'exact_geometry.json').read_text('utf-8'))
assert check['success']
for name in ('PROGRESS_LOG.md','FILE_INDEX.md'):
    path = ROOT/name
    backup = HERE/'before_records'/name
    backup.parent.mkdir(exist_ok=True)
    if not backup.exists():
        backup.write_bytes(path.read_bytes())

path = ROOT/'PROGRESS_LOG.md'
source = path.read_text('utf-8')
start,end = '<!-- DLW_DOMAIN_RATIONALE_BEGIN -->','<!-- DLW_DOMAIN_RATIONALE_END -->'
source = re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\s*','',source,flags=re.S)
anchor = '> **2026-10-06（DLW数值分析笔记本）：** '
assert source.count(anchor) == 1
note = (start+'**计算域解析说明（2026-10-07）：** '
    '针对用户询问现有 x∈[-20,20)、y∈[-1.5,1.5] 的选取理由，核对连续孤子解析几何，未重跑 PDE。'
    'A/B 的峰位在当前 y/t 窗口约为 [0.212,0.972]/[-1.097,0.473]；独立解析采样 C 的 u/v 峰位约 '
    '[-0.964,0.198]/[-1.057,0.240]、半高宽约 3.3–3.5。50 位解析采样 x=±20 的 B/C 双场绝对值最大约 '
    '1.4e-8，A 约 1.8e-24，支持远场计算边界加核心评价窗口的说明。'
    'C 的相位差为 5y/12−4t，等相位线 y=9.6t∈[0,0.096]；条带内 E1/E2∈[0.514,1.868]。'
    '可将指数项相差不超过两倍作为中央相位交叠条带的充分准则，得到 Y≤(12/5)(ln2−4T)≈1.568；'
    'h=.125 下最大整格半宽为 1.5，对应 24 个中点层。此为现有配置的可核验解释，未追溯成原始选域步骤，'
    '也未用解析边界场值替代数值解扩域验证；Notebook、HTML 与已有数值输出保持。'
    '依据见 [解析几何核对](Workspaces/notebook_reports_20261006/domain_rationale_20261007/exact_geometry.json)。'+end+' ')
path.write_text(source.replace(anchor,anchor+note,1),'utf-8')

path = ROOT/'FILE_INDEX.md'
source = path.read_text('utf-8')
start,end = '<!-- DLW_DOMAIN_RATIONALE_INDEX_BEGIN -->','<!-- DLW_DOMAIN_RATIONALE_INDEX_END -->'
source = re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\n*','',source,flags=re.S)
files = sorted(p for p in HERE.rglob('*') if p.is_file())
section = start+'\n**DLW 计算域的解析几何依据（未重跑数值演化）：**\n\n'
section += '\n'.join(f'- [{p.relative_to(ROOT).as_posix()}]({p.relative_to(ROOT).as_posix()})' for p in files)
section += '\n'+end+'\n\n'
anchor = '<!-- NOTEBOOK_REPORTS_INDEX_BEGIN -->\n'
assert anchor in source
path.write_text(source.replace(anchor,anchor+section,1),'utf-8')
print('Analytic domain rationale recorded; numerical deliverables unchanged.')
