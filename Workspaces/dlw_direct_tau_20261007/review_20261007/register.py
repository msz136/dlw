from pathlib import Path
import hashlib,json,shutil
from html.parser import HTMLParser
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
report=ROOT/'report/dlw_sd_implementation_review.html'
class Links(HTMLParser):
    def __init__(self): super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a': self.links += [v for k,v in attrs if k=='href']
parser=Links();parser.feed(report.read_text('utf-8'))
assert all((report.parent/link).resolve().exists() for link in parser.links)
audit=json.loads((HERE/'audit.json').read_text('utf-8'))
runs=json.loads((HERE/'runs.json').read_text('utf-8'))
notebook=ROOT/'notebook/DLW数值分析report.ipynb'
current=hashlib.sha256(notebook.read_bytes()).hexdigest()
assert current==audit['notebook_sha256']==runs['notebook_sha256']
assert len(runs['replays'])==6 and all(r['completed'] and r['saved_max_error_difference']==0 for r in runs['replays'])
backup=HERE/'before_registration';backup.mkdir(exist_ok=True)
for name in ('PROGRESS_LOG.md','FILE_INDEX.md'):
    if not (backup/name).exists(): shutil.copy2(ROOT/name,backup/name)
p=ROOT/'PROGRESS_LOG.md';text=p.read_text('utf-8')
marker='> **2026-10-06（DLW数值分析笔记本）：** '
addition='**2026-10-07实现审查：** [SD审查报告](report/dlw_sd_implementation_review.html)核对当前实际notebook；六组默认SD轨道复跑至T=.01，终点误差与保存值逐值一致，六组独立单步双线性相对残差最大1.03e-10，A动格T=.002减步阶2.0005/2.0020。确认两个未修接口问题：初值提升反演奇数阶反对称差分块，nx=257奇异、nx=255可先产生巨大伪解；solve请求SD/Euler仍执行中点而保存Euler标签。默认nx256/Midpoint不受影响。另核对T=0公共点样条误差，A为u2.2282e-4/v9.6117e-5，区别节点初值差约1e-12；比较含不同边界闭合。未改实现、notebook或主数值HTML；核验与复跑材料在Workspaces/dlw_direct_tau_20261007/review_20261007/。 '
assert marker in text
if '[SD审查报告]' not in text: p.write_text(text.replace(marker,marker+addition,1),encoding='utf-8')
p=ROOT/'FILE_INDEX.md';text=p.read_text('utf-8')
if 'report/dlw_sd_implementation_review.html' not in text:
    text+='\n**DLW SD递推实现审查（2026-10-07）：**\n\n- [SD审查报告](report/dlw_sd_implementation_review.html)（当前递推、奇数节点提升奇异、方法标签与初始插值误差）。\n- `Workspaces/dlw_direct_tau_20261007/review_20261007/audit.py`、`audit.json`（当前notebook六组独立单步与15组初值网格检查）。\n- `Workspaces/dlw_direct_tau_20261007/review_20261007/runs.py`、`runs.json`（六组默认SD复跑及A组动网格时间细化）。\n- `Workspaces/dlw_direct_tau_20261007/review_20261007/method_check.json`（Euler请求实际执行中点的复现）。\n- `Workspaces/dlw_direct_tau_20261007/review_20261007/register.py`、`registration.json`、`before_registration/`（登记、交付核验及旧记录备份）。\n'
    p.write_text(text,encoding='utf-8')
registration={'notebook_unchanged_sha256':current,'six_default_replays_identical':True,'report_local_links_valid':True,
              'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [report,HERE/'audit.json',HERE/'runs.json',HERE/'method_check.json']}}
(HERE/'registration.json').write_text(json.dumps(registration,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Review registered; all local links valid; live notebook unchanged; six default replays identical.')
