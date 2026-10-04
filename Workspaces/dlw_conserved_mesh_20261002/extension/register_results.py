"""Merge the long-time extension into this topic's workspace records."""
from pathlib import Path
import hashlib,json,re

HERE=Path(__file__).resolve().parent
TOPIC=HERE.parent
ROOT=TOPIC.parents[1]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

progress=ROOT/'PROGRESS_LOG.md'
s=progress.read_text(encoding='utf-8')
marker='> **2026-10-02（DLW守恒密度动网格：原文五算例、物理小域）：** '
assert s.count(marker)==1
start=s.index(marker);end=s.find('\n\n',start)
if end<0:end=len(s)
old=s[start:end]
previous=old.split(' **此前T=.001：** ',1)[-1] if ' **此前T=.001：** ' in old else old[len(marker):]
current=(
    '**T=.01延长（当前）：** [完整物理u/v报告](report/dlw_conserved_mesh.html)已更新，原T=.001页面保留于专题short_time_report.html。'
    '原文五参数组、x/y[-1,1]、初边值及原SD/FD方程不变；主33x、h=.125、RK4 dt2.5e−5，记录.001/.002/.005/.01并保留时间/x/y/联合加密和相同初态冻结对照。'
    '追加mass=平均(−v/4)、strong=平均(1−v)，通量分别Q0/4Q0；两者只是同一守恒律的背景强度变体，系数预先固定。'
    '未得到数量级双场收益。A固定SD误差.001786/.001292，strong .033315/.031125，分别恶化18.65/24.08倍；mass FD .536837/.651166，恶化282.78/201.45倍，mass SD在.009025停止。'
    'A strong SD从.001的相对误差.616/.849转为终点18.65/24.08；mass初始最大单元长.39232 vs固定.0625，初始样条误差.002244/.004796，节点初值仍精确。'
    '全部新增x加密停止，联合加密仅E strong两方法到终点但误差巨大；主格完成不等于准确。可配对减步差≤原误差1.52e−6，评价点加倍变化≤.469%；移动相对同初始冻结最大降低约23%，未抵消集中损失。'
    '独立A原求解器减步复核与初始场Jacobian谱支持空间高频增长机制（粗约590/细约2250），不是严格非线性上界；需继续分辨边界闭合与体内截断激发。'
    '40新增初态/通量身份、350轨道1735快照/225初值配对独立读回通过，92停止均无伪终点，源/场哈希一致。'
    '新增初态双场曲率被动权重守恒构造R=μRb,Q=μQb、μt+(Qb/Rb)μx=0；9符号检查通过，尚未运行演化或证明可积性/收益。'
    '新报告6图19表、宽窄屏/链接检查通过。新源码/协议/原始场/CSV/报告/复核分别在extension/与extension_diagnostics/。'
)
entry=marker+current+' **此前T=.001：** '+previous
s=entry+'\n\n'+(s[:start]+s[end:]).lstrip('\r\n')
progress.write_text(s,encoding='utf-8')

index=ROOT/'FILE_INDEX.md'
s=index.read_text(encoding='utf-8')
s=s.replace('**DLW守恒密度动网格：原文五算例小域实验（2026-10-02）：**','**DLW守恒密度动网格：原文五算例小域实验及T=.01延长（2026-10-02）：**',1)
old='- [物理u/v误差、精确场与数值场](report/dlw_conserved_mesh.html)（x/y[-1,1]、T=.001，三密度、固定SD/FD、同初态冻结、联合细化；11图23表）'
new='- [物理u/v误差与T=.01密度比较](report/dlw_conserved_mesh.html)（原文五组、x/y[-1,1]、五密度、固定SD/FD、同初态冻结；6图19表，初态重构与演化增长分开）；[此前T=.001完整报告](Workspaces/dlw_conserved_mesh_20261002/short_time_report.html)（11图23表）'
assert old in s or new in s
s=s.replace(old,new,1)
new_index='''- `Workspaces/dlw_conserved_mesh_20261002/extension/baseline.py`、`candidates.py`、`BASELINE_PROTOCOL.json`、`CANDIDATE_PROTOCOL.json`（T=.01冻结源与先验协议；mass/strong通量和初始布点对应）
- `Workspaces/dlw_conserved_mesh_20261002/extension/baseline_out/`、`candidate_out/`（230+120条完整/停止运行，results.json、原始节点/精确场/误差/网格NPZ、源码与场哈希）
- `Workspaces/dlw_conserved_mesh_20261002/extension/errors.csv`、`paired_errors.csv`、`controls.csv`、`moving_vs_frozen.csv`、`evaluation.csv`、`analysis.json`（同物理时刻双场差、空间/时间控制、评价与冻结配对）
- `Workspaces/dlw_conserved_mesh_20261002/extension/theory/NEW_DENSITIES.md`、`density_checks.json`、`check_new_density.py`、`new_density_validation.json`、`source_snapshot/`（背景/强度密度、先验形状预测、40组合独立通量初态检查）
- `Workspaces/dlw_conserved_mesh_20261002/extension/theory/PASSIVE_CURVATURE_DIRECTION.md`、`check_passive_curvature.py`、`passive_curvature_symbolic.json`（μRb守恒构造、绝对/归一标签、ALE关系9符号核验；未做演化）
- `Workspaces/dlw_conserved_mesh_20261002/extension/audit/`（350轨道1735快照、225初值配对、92停止目标时刻完整性核验与停止CSV）
- `Workspaces/dlw_conserved_mesh_20261002/extension_diagnostics/NOTES.md`、`FINAL_INTERPRETATION.md`、`probe_original.py`、`frozen_growth.py`、`growth.json`、`out/`（独立八轨道减步诊断、初始场增长谱、初态重构/演化分离解释）
- `Workspaces/dlw_conserved_mesh_20261002/extension/analyze.py`、`report_source.html`、`manifest.json`、`check_report.cjs`、`html_validation.json`、`report_*.png`、`error_fields_*.png`、`growth_time_controls.png`（T=.01论文式报告、宽窄屏/链接验证和科学图）；`register_results.py`、`registration.json`（同专题记录合并）
'''
if new_index not in s:
    loc=s.index(new)+len(new)
    s=s[:loc]+'\n'+new_index.rstrip('\n')+s[loc:]
index.write_text(s,encoding='utf-8')

notes=TOPIC/'RESEARCH_NOTES.md'
s=notes.read_text(encoding='utf-8')
tag='# 2026-10-02：T=.01延长与新增密度最终结果'
if tag in s:s=s[s.index('\n# ',s.index(tag)+len(tag))+1:]
new_notes='''# 2026-10-02：T=.01延长与新增密度最终结果

## 已完成的范围

extension/baseline.py复制此前最终闭合，不改原experiment.py/out；extension/candidates.py引入mass/strong，分别R0−1与1+4(R0−1)，Q0与4Q0。原论文五组a2、ci1、phase0、x/y[-1,1]保持。主nx33/h.125/dt2.5e-5，T=.01；time_half、x_half、y_half、combined及moving/frozen在运行前冻结。baseline230、candidate120均处理完，其中258到终点、92真实停止；主移动/均匀60组有59到终点。停止原因及最后快照保留，不能把不同终点做排名。独立诊断另用A固定nx33/65、dt5e-6/2.5e-6八条轨道，验证时间污染不是主因。

## 科学结论

没有数量级双场收益。A固定SD .001786/.001292；strong SD .033315/.031125；mass FD .536837/.651166；mass SD .009025停止。strong SD .001的收益比.616/.849随时间反转到.01的18.65/24.08倍损失。B/C变化较小；E mass两模型约翻倍，不能算有效优化。

分清两种损失：A mass dxmax=.39232 vs固定.0625，初始共同评价样条误差.002244/.004796 vs固定4.36e-5/2.13e-5；节点初值仍为精确解。样条仅用于评价，没有回灌演化。晚期A mass FD节点误差.523/.648证明损失亦进入演化。A strong初始u重构略小但终点明显变坏，需要传播机制解释。

全部20个新增x_half停止；联合加密仅E strong SD/FD到终点，u/v .858/.835及.0422/.0357，远高主格。原固定FD的B x_half虽完成，误差58.8/64.8，说明完成不代表准确。独立初始场Jacobian正增长谱约590→2250；常背景PDE含k²增长分支。它支持机制诊断，不是非线性误差上界，未排除端点闭合激发。当前不宣称T=.01空间收敛或任何自适应算法普遍失效。

可配对时间减半最大场差/原误差1.517e-6；401→801物理评价点误差最大变化.4685%。移动相同初始冻结对照误差比最低.7697，最高1.000018，最大位移.01756。短窗的.231%结论不适用于此长窗；约23%移动收益仍未抵消强集中损失。D1²端点附近三阶限定保留。

## 新的密度方向

已推导初态双场曲率被动加权：Rb,t+Qb,x=0，μt+(Qb/Rb)μx=0，则R=μRb、Q=μQb守恒。它需增广被动状态，不是仅当前u/v的新独立密度。初态μ从固定物理初值导数/幅值设定；不使用未来精确场。有限端点用绝对质量标签，归一η通常非被动标签；实际差分需兼容通量。9项独立符号零残差通过，尚未做演化、精度收益或可积性证明。

下一步先分辨体内截断与端点闭合如何激发增长，建立明确时间/分辨率范围，再检验导数加权密度是否同时减小残差和传播放大；不继续无控制地增大同一质量密度强度。

## 核验与复现

theory/check_new_density.py独立40组合初值/有限h通量身份；audit/verify_saved_fields.py读回350轨道1735快照、225初态配对、端点和各类误差，无问题。初值独立差≤7.11e-15、配对≤1.78e-15、端点≤7.99e-15；92停止没有目标时间伪填。原报告按源码report_source保留为short_time_report，调整相对链接；原短窗全部数据不变。

运行：在extension中执行 `python baseline.py --stage all --workers 4`、`python candidates.py --workers 2`。复核：`python theory/check_new_density.py`、`python theory/check_passive_curvature.py`、`python audit/verify_saved_fields.py`。报告：`python analyze.py`、`node check_report.cjs`。不得边运行边改冻结源。专题报告report/dlw_conserved_mesh.html为T=.01结果，6图19表；短窗11图23表另有链接。先前已有数据可续读，源/场hash不匹配会拒绝复用。

'''
notes.write_text(new_notes+s,encoding='utf-8')
record=dict(date='2026-10-02',topic='DLW conserved density mesh T=.01 extension',
    registered={str(p.relative_to(ROOT)):sha(p) for p in [progress,index,notes,ROOT/'report/dlw_conserved_mesh.html',HERE/'manifest.json',HERE/'html_validation.json']})
(HERE/'registration.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Merged progress, file index and research notes.')
