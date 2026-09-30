"""Merge this completed experiment into the existing DLW topic and file index."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
summary=json.loads((HERE/'out/summary.json').read_text(encoding='utf-8'))
assert sum(d.get('completed',0) for d in summary['counts'].values())==481
addition=' **同日 Euler 系数族实际演化：** [比较报告](Workspaces/dlw_coefficient_euler_20260926/REPORT.md)固定网格与 Euler，8 组波形×FD/九组 c,κ 网格/理论共用系数；418 条主及控制轨道＋48 条加密补测＋15 条扩域复核共481条完成，另保留4条先导。所有方案统一连续物理初值、P/v时间状态与边界，比较T=.01的u/v总误差。新短闭合与旧长式、时变边界及60位精确孤子等18项核验通过，481个NPZ/源码哈希与误差回读通过。P2/P6的原式及理论系数在所测主/减步/分别及同时x/y加密中双场均胜FD；P6细x理论系数相对FD降40.1%/39.6%，扩x/y域后仍有优势。P1排序随x分辨率变化，P3/P7理论系数相对原式只加密y时u变差；P10仍为u差、v好。P5窄周期域尾部高频污染，保留原轨道并标记不可用于细微排序；扩域后理论系数改善原式但仍败FD。主表Euler减步误差变化≤.666%，160个FD比较有1个细小翻转；评价加密排除P5后最大.782%，含P5为24.224%。Miura报告的空间残差L2候选直接迁入演化但非普遍最优；不能把残差降幅当解误差降幅、不能宣称长期/一般初值稳定或统计显著性。完整三组系数表、加密表、CSV及冻结计划见新工作区；旧生产求解器、Lean及根HTML未改。'
p=ROOT/'PROGRESS_LOG.md';s=p.read_text(encoding='utf-8')
if '**同日 Euler 系数族实际演化：**' not in s:
    start=s.index('> **2026-09-26（双线性→非线性与 Miura 转化复梳）')
    end=s.index('\n\n',start)
    s=s[:end]+addition+s[end:]
    p.write_text(s,encoding='utf-8')
p=ROOT/'FILE_INDEX.md';s=p.read_text(encoding='utf-8')
needle='- `Workspaces/dlw_modified_equation_20260926/make_optimization_report.py`（数据生成参数优化推导与 HTML 第六部分）'
entries='''
- [DLW Euler 系数族比较报告](Workspaces/dlw_coefficient_euler_20260926/REPORT.md)（8波形×11方案、主/系数/加密表；Miura残差候选的实际演化检验，P5边界污染与扩域复核）
- `Workspaces/dlw_coefficient_euler_20260926/model.py`、`validate_model.py`、`model_validation.json`（统一P/v状态、固定物理h的c/κ族、18项独立/代数核验）
- `Workspaces/dlw_coefficient_euler_20260926/run.py`、`refine.py`、`boundary_control.py`（冻结418＋48＋15条Euler轨道；源码/初态哈希）
- `Workspaces/dlw_coefficient_euler_20260926/summarize.py`、`make_report.py`、`finish_docs.py`（误差回读、CSV/全表、报告与索引同步）
- `Workspaces/dlw_coefficient_euler_20260926/out/`（三份冻结JSON、481条物理场NPZ、errors.csv、summary.json、tables.md），`pilot_v1/`（4条先导与当时源码）'''
if 'DLW Euler 系数族比较报告' not in s:
    assert needle in s;s=s.replace(needle,needle+entries,1);p.write_text(s,encoding='utf-8')
print('Merged PROGRESS_LOG.md and FILE_INDEX.md')
