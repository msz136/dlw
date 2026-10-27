"""Record native response publication while preserving the parallel certification state."""
from pathlib import Path
import json,re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
status=json.loads((HERE/'publication_validation.json').read_text(encoding='utf-8'))
assert status['trajectories']==24 and status['main_section']=='5.5'
local=HERE/'README.md'
s=local.read_text(encoding='utf-8')
if '## Manuscript and reader report' not in s:
    s+=('\n\n## Manuscript and reader report\n\n'
        'Current main text is Section 5.5, "Evolution of independent physical-field perturbations", in `../../../../dlw-paper.html`. '
        'The standalone reader report is `../../../../report/dlw_native_perturbation_responses_20261026.html`. '
        'Figures29/30 present u-only/v-only native-site histories, each with four cases and three method styles. '
        'The report contains three separate methodwise endpoint tables and an optional overview layout. '
        'No common-grid interpolation, intermethod field difference, or agreement threshold enters the published material. '
        'Previous Section6 and the72-trajectory frequency sweep remain in snapshots and separate reports. '
        'Main totals:30figures,6tables; conclusion renumbered6 with body preserved. '
        'Checks: `publication_validation.json`, `audit/native_output_validation.json`, `figures/figure_validation.json`.\n')
    local.write_text(s,encoding='utf-8')

parent=HERE.parent/'README.md';before=parent.read_bytes();s=before.decode('utf-8')
s=s.replace('The manuscript currently retains only the response study in Sections 6.1/6.2; certification research is reported separately.',
            'The manuscript now includes native within-method response histories in Section 5.5 (Numerical Experiments); certification research is reported separately.')
s=s.replace('- Main manuscript: `../../../dlw-paper.html`, Section 6, “Response to initial perturbations” (6.1 linearized response; 6.2 independent-field experiments).',
            '- Main manuscript: `../../../dlw-paper.html`, Section 5.5, “Evolution of independent physical-field perturbations”.\n- Current reader report: `../../../report/dlw_native_perturbation_responses_20261026.html`; data and plots: `three_method_response_20261026/README.md`.')
s=s.replace('- Current frequency/amplitude sweep:', '- Retained frequency/amplitude sweep:')
s=s.replace('The current sweep covers kappa=pi/2, pi, 2pi', 'The retained single-method sweep covers kappa=pi/2, pi, 2pi')
intro=('The current publication follows24 native-site trajectories (four backgrounds, three spatial methods, independentu/v inputs), '
       'all reachingT=.01 with epsilon=1e-6,kappa=pi/2,h=dx=.1 and RK4dt=1e-4. '
       'Each curve subtracts its own method\'s unperturbed trajectory. The user explicitly declined alignment and intermethod comparisons; '
       'common-grid diagnostics are superseded. All12 background arrays reproduce production RK4 results exactly. '
       'Independent native-data and figure audits passed.\n\n')
if 'The current publication follows24 native-site trajectories' not in s:s=re.sub(r'## Completed results\r?\n\r?\n',lambda m:m[0]+intro,s,count=1)
manuscript=('## Manuscript state and preservation\n\n'
    'The user moved the response study into Numerical Experiments as Section5.5. The main text describes each method\'s own response and coupling on native physical-field sites; it uses no intermethod error or agreement-time metric. '
    'The standalone Section6, its linear derivation and the four frequency/amplitude tables have been retained in reports/snapshots. '
    'Two new eight-panel figures showu-only andv-only inputs. Original figures1–28 and Sections1–4 are unchanged. '
    'Section5 gains a roadmap sentence and5.5; the conclusion is renumbered6 without changing its body. Current total:30figures,6tables. '
    'Current checks: `three_method_response_20261026/publication_validation.json`.\n\n'
    'Old publishers, `section6.html`, and earlier validation files document historical states. Do not rerun them to overwrite current scope. '
    'Current subsection source is `three_method_response_20261026/section55.html`; edit the main paper locally while preserving newer user edits. '
    'Earlier proofs, datasets and snapshots are retained.\n\n')
s,n=re.subn(r'## Manuscript state and preservation\r?\n.*?(?=The older `linear_spectrum)',lambda _:manuscript,s,flags=re.S);assert n==1
assert parent.read_bytes()==before;parent.write_bytes(s.encode('utf-8'))

index=ROOT/'FILE_INDEX.md';before=index.read_bytes();s=before.decode('utf-8')
line=next(q for q in s.splitlines() if q.startswith('| DLW 独立物理场扰动 |'))
new=line.replace('6.1线性机制、6.2波数/幅值扫描；72条轨道、四表及步长控制；',
                 '5.5原生格点扰动响应；24条轨道、两张时间曲线大图，分别叙述各方法；旧波数/幅值扫描另存；')
new=new.replace('[主论文 Section 6](dlw-paper.html#section-6)',
                '[主论文 Section 5.5](dlw-paper.html#section-5.5)；[原生响应图文](report/dlw_native_perturbation_responses_20261026.html)')
assert new!=line and index.read_bytes()==before
index.write_bytes(s.replace(line,new,1).encode('utf-8'))

progress=ROOT/'PROGRESS_LOG.md';before=progress.read_bytes();s=before.decode('utf-8')
assert '## 本次工作' in s and '## 上一次工作' in s
previous=s[s.index('## 上一次工作'):];active=s[:s.index('## 上一次工作')]
active=active.replace('主论文仅6.1/6.2，数值分支29图10表。','主论文扰动内容已并入5.5，现30图6表。')
active=active.replace('`dlw-paper.html#section-6`','`dlw-paper.html#section-5.5`')
paragraph=('同项目数值分支按用户更正完成：三种空间方法各自计算受扰减未扰动响应，保留原生格点，不对齐、不做方法间差或一致性阈值。四背景各u/v独立扰动共24条轨道至T=.01；初值、差分方程、背景复现、原生响应及图均核验。主论文5.5写入两张4×2时间曲线大图和逐方法分析，独立Section6撤下，结论顺延为6。旧72条波数/幅值扫描及理论材料另存；认证goal状态不变。数值入口：`report/dlw_native_perturbation_responses_20261026.html`；`Workspaces/dlw_paper_20261009/stability_20261026/three_method_response_20261026/README.md`。')
active,n=re.subn(r'同项目数值分支已完成波数/幅值扫描：.*?(?=\r?\n\r?\n)',lambda _:paragraph,active,count=1,flags=re.S)
if not n:active+=paragraph+'\n\n'
updated=active+previous;assert len(updated)<3000 and progress.read_bytes()==before
history=ROOT/'Workspaces/workspace_catalog_audit_20261013/progress_history/2026-10.md'
with history.open('a',encoding='utf-8',newline='') as f:
    f.write('\n\n### 2026-10-26｜DLW 三方法原生扰动响应并入5.5\n\n完成四背景×三方法×独立u/v共24条轨道至T=.01，各自受扰减未扰动；按用户更正使用原生格点，不对齐、不作方法间差或一致性阈值。两张4×2时间曲线图与逐方法分析并入主论文5.5；原Section6和波数扫描另存，正文现30图6表。背景复现、非线性差分及原生数据/图独立核验通过。证据：`report/dlw_native_perturbation_responses_20261026.html`；`Workspaces/dlw_paper_20261009/stability_20261026/three_method_response_20261026/publication_validation.json`。\n')
progress.write_bytes(updated.encode('utf-8'))

taste=Path('C:/Users/msz/.codex/skills/plot-is-all-you-need/taste.md')
with taste.open('a',encoding='utf-8',newline='') as f:
    f.write('\n2026-10-26 | DLW期刊正文 | 用户指定同一时间面板叠加三种空间方法，蓝/橙/绿与实/虚/点划线；分别展示u-only、v-only输入的两场响应 | 各方法使用自身原生格点，不做对齐或方法间差值 | 四算例4×2大图并入数值实验\n')
print('Native response publication recorded; parallel certification state and previous progress slot preserved.')
