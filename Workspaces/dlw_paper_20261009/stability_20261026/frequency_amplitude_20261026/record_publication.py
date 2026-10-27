"""Register the completed sweep without changing unrelated progress slots."""
from pathlib import Path
import json
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
status=json.loads((HERE/'publication_validation.json').read_text(encoding='utf-8'))
assert status['trajectories']==72 and status['all_reached_T']
summary=json.loads((HERE/'summary.json').read_text(encoding='utf-8'))
assert summary['completed_trajectories']==72 and len(summary['time_controls'])==8

readme=HERE/'README.md'
src=readme.read_text(encoding='utf-8') if readme.exists() else '# Wavenumber and amplitude dependence\n'
note=('\n\n## Published results\n\n'
      'All 72 main trajectories reached T=.01; all eight strongest-input time-step controls completed. '
      'The four case tables and their analysis are in `../../../../report/dlw_perturbation_sweep_20261026.html` '
      'and main manuscript Section 6.2 (`../../../../dlw-paper.html`). Each table has nine (kappa, epsilon) rows and both independent input fields. '
      'The existing Figure 29 is retained for kappa=pi/2 and epsilon=1e-6. The manuscript has 29 figures and 10 tables; the control table is renumbered 10. '
      'Only Section 6.2 and that caption number changed; abstract, introduction, conclusion and all figure bytes are preserved. '
      'See `publication_validation.json`, `audit/output_validation.json`, `summary.json`, and `terminal_rows.csv`. '
      'Continuous-reference certification is a separate research branch; these are nonlinear discrete trajectory responses.\n')
if '## Published results' not in src:src+=note
src=src.replace('The certification branch remains deferred; these are nonlinear discrete trajectory responses.', 'Continuous-reference certification is a separate research branch; these are nonlinear discrete trajectory responses.')
readme.write_text(src,encoding='utf-8')

parent=HERE.parent/'README.md'
src=parent.read_text(encoding='utf-8')
src=src.replace('- Numerical protocol/data: `perturbation_pilot/README.md`.',
    '- Current frequency/amplitude sweep: `frequency_amplitude_20261026/README.md`; reader report: `../../../report/dlw_perturbation_sweep_20261026.html`.\n- Original single-carrier protocol/data: `perturbation_pilot/README.md`.')
if 'The current sweep covers kappa=pi/2, pi, 2pi' not in src:src=src.replace('## Completed results\n',
    '## Completed results\n\nThe current sweep covers kappa=pi/2, pi, 2pi and epsilon=1e-7, 1e-6, 1e-5 for both independent inputs on all four backgrounds. All 72 trajectories reached T=.01. Each background has a nine-row table and a fieldwise amplitude-scaling analysis. Eight strongest-input time-step-halving controls and independent array audits passed. The normalizations remain max/epsilon and measured-initial-pair L2 gain.\n',1)
src=src.replace('Total: 29 figures, 7 tables. Current checksum and preservation checks: `response_focus_validation.json`; earlier checks: `section6_validation.json`.',
    'Current total: 29 figures, 10 tables. Section 6.2 now contains four frequency/amplitude tables and casewise analyses; the earlier two-subsection scope remains. Current checks: `frequency_amplitude_20261026/publication_validation.json`; previous scope checks: `response_focus_validation.json` and `section6_validation.json`.')
parent.write_text(src,encoding='utf-8')

index=ROOT/'FILE_INDEX.md';before=index.read_bytes();src=before.decode('utf-8')
line=next(v for v in src.splitlines() if v.startswith('| DLW 独立物理场扰动 |'))
new='| DLW 独立物理场扰动 | A/D、高斯与正弦的独立 u/v 扰动响应及连续认证探索 | 6.1线性机制、6.2波数/幅值扫描；72条轨道、四表及步长控制；连续参考认证与高频障碍另线研究 | [主论文 Section 6](dlw-paper.html#section-6)；[波数与幅值报告](report/dlw_perturbation_sweep_20261026.html)；[原扰动报告](report/dlw_independent_stability_20261026.html)；[最新认证goal](report/dlw_reference_goal_20261026.html)；[此前认证进展](report/dlw_reference_certification_20261026.html)；[入口与目录](Workspaces/dlw_paper_20261009/stability_20261026/README.md) |'
assert index.read_bytes()==before
index.write_bytes(src.replace(line,new,1).encode('utf-8'))

progress=ROOT/'PROGRESS_LOG.md';before=progress.read_bytes();src=before.decode('utf-8')
assert '## 本次工作｜DLW ' in src
previous=src[src.index('## 上一次工作'):]
history=ROOT/'Workspaces/workspace_catalog_audit_20261013/progress_history/2026-10.md'
entry=('\n\n### 2026-10-26｜DLW 独立扰动：波数与幅值扫描\n\n'
       '完成A/D、高斯、正弦的κ=π/2、π、2π及ε=1e−7、1e−6、1e−5独立u/v扰动，共72条轨道至T=.01；另做8条时间步减半控制。归一化响应随幅值近似重合，场间传递随波数增强；孤子背景的两个传递方向呈现不同频率依赖。主论文6.2写入四个算例表及分析，原图保留；连续认证另线推进，本轮未改变其科学状态。证据：`report/dlw_perturbation_sweep_20261026.html`；`Workspaces/dlw_paper_20261009/stability_20261026/frequency_amplitude_20261026/summary.json`及`audit/output_validation.json`。\n')
with history.open('a',encoding='utf-8',newline='') as f:f.write(entry)
current=('# 当前工作与最近交接\n\n'
         '## 本次工作｜DLW 独立扰动与 Section 6（2026-10-26，波数/幅值扫描完成）\n\n'
         '四背景A/D、高斯、正弦，κ=π/2、π、2π，ε=1e−7、1e−6、1e−5，分别扰动u或v。72条轨道均到T=.01，h=Δx=.1、RK4 Δt=1e−4；8条最高波数/幅值的时间步减半控制完成，独立核对原生最大值、配对范数和全场幅值差。响应近似按ε缩放，短波加强场间传递；孤子反向传递体现明显背景作用。\n\n'
         '主论文6.2更新为每算例一表及分析，原Figure29保留，现29图10表。6.1、摘要、引言、结论及其他正文不变，仅控制表号顺延10。连续参考认证仍暂缓且未取得完整ηu/ηv；不把此次离散响应当作连续稳定性认证。下一步按用户意见调整表格呈现或继续稳定性机制比较，不自动重启认证。入口：`dlw-paper.html#section-6.2`；`report/dlw_perturbation_sweep_20261026.html`；`Workspaces/dlw_paper_20261009/stability_20261026/frequency_amplitude_20261026/README.md`。\n\n')
if '## 本次工作｜DLW 连续参考goal与独立扰动' in src:
    active=src[:src.index('## 上一次工作')]
    active=active.replace('主论文仍仅6.1/6.2，29图7表未改。','主论文仅6.1/6.2，数值分支已扩展为29图10表。')
    active+=('同项目数值分支已完成波数/幅值扫描：四背景、κ=π/2/π/2π、ε=1e−7/1e−6/1e−5、独立u/v，共72条轨道与8条步长控制。6.2现为四张算例表及分析；归一化场对幅值的最大相对差异7.81e−6，双孤子短波自身响应明显增强。既有图及其他正文保持；本轮不改变上面的认证goal状态。数值入口：`report/dlw_perturbation_sweep_20261026.html`；`Workspaces/dlw_paper_20261009/stability_20261026/frequency_amplitude_20261026/README.md`。\n\n')
    updated=active+previous
else:
    updated=current+previous
assert len(updated)<3000 and progress.read_bytes()==before
progress.write_bytes(updated.encode('utf-8'))
print('Registered four-case sweep, report, manuscript update, history and current progress.')
