"""Merge stage 2 into the existing research-topic progress entry."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
path=ROOT/'PROGRESS_LOG.md'
old=path.read_text(encoding='utf-8')
old_marker='（DLW 三项并行研究与方向评议）'
new_marker='（DLW 两阶段并行研究与方向评议）'
addition=(
    '**第二阶段完成：** 新增 [合法约化、辛保持与误差Lax报告](report/dlw_stage2_20261013.html)，'
    '完整材料在 `Workspaces/dlw_stage2_20261013/`。2A给出固定y切片不闭合的正则M3反例，'
    '转而在原M2周期结构、γ=0、零分量均值上构造显式椭圆行波辛环域，直接拉回原Ω得到dφ∧dP，'
    '证明一个自由度Liouville可积；给出c=−4,h=2,L=2π,0<m<1/20的解析非退化区间和twist极限5/(96π)。'
    '2B用原Hamilton网格56维固定Casimir叶，测实际Euler/RK4/中点切映射；T=.02、dt=.0025相对辛缺陷分别'
    '1.14e−3/1.65e−12/1.07e−15，物理场时间误差9.61e−5/1.73e−12/1.55e−7。'
    '完整传播有限Newton导数，揭示未解准时理想Cayley公式虚报保辛；40项核验、10张CSV、两组PNG/PDF完成。'
    '2C建立非线性误差PDE、热势残差到Darboux/单值化/谱量误差率的精确桥，保留物理采样h²修正、系数及算子两层Leibniz缺陷；'
    '有理见证的网格PDE/势残差为零而原矩阵Lax缺陷非零，38项158标量精确检查通过。'
    '综合命题给出同环域精确轨道action差恒定、提升角线性漂移、相位对齐误差一致界及条件强迫积分界。'
    '三代理交叉审读、root独立代数复核、18项交付检查通过，原Notebook/论文/第一阶段源哈希保持。'
    '固定y切片、du∧dx和自主误差Lax的直接猜想均作了必要修正；未声称多自由度完备、一般场长期稳定或原PE/PF已保辛。 '
    '**此前第一阶段：** '
)
if new_marker not in old:
    lines=old.splitlines(keepends=True)
    i=next(i for i,line in enumerate(lines) if old_marker in line)
    entry=lines.pop(i)
    head,body=entry.split('：** ',1)
    new=head.replace(old_marker,new_marker)+'：** '+addition+body
    revised=new.rstrip()+'\n\n'+''.join(lines).lstrip('\n')
    if path.read_text(encoding='utf-8')!=old:
        raise RuntimeError('Concurrent progress change; rerun merge.')
    path.write_text(revised,encoding='utf-8')

index=ROOT/'FILE_INDEX.md'
old=index.read_text(encoding='utf-8')
marker='<!-- DLW_STAGE2_20261013 -->'
block='''<!-- DLW_STAGE2_20261013 -->
**DLW 第二阶段：合法约化、辛保持与误差Lax（2026-10-13）：**

- [整合报告](report/dlw_stage2_20261013.html)、[主文源](Workspaces/dlw_stage2_20261013/manuscript.md)、[复现说明](Workspaces/dlw_stage2_20261013/README.md)、[独立审查总录](Workspaces/dlw_stage2_20261013/REVIEW.md)
- [2A完整定理](Workspaces/dlw_stage2_20261013/reduction/report.md)、[椭圆波验证脚本](Workspaces/dlw_stage2_20261013/reduction/verify_reduction.py)、[符号与数值证书](Workspaces/dlw_stage2_20261013/reduction/verification.json)、[五个椭圆波数值表](Workspaces/dlw_stage2_20261013/reduction/elliptic_family_checks.csv)、[2C独立审查](Workspaces/dlw_stage2_20261013/reduction/cross_review_error_lax.md)
- [2B方法与结果](Workspaces/dlw_stage2_20261013/symplectic/report.md)、[实际切映射实验](Workspaces/dlw_stage2_20261013/symplectic/symplectic_experiment.py)、[40项验证](Workspaces/dlw_stage2_20261013/symplectic/validation.json)、[切映射数据](Workspaces/dlw_stage2_20261013/symplectic/tangent_maps.npz)
- [辛缺陷图](Workspaces/dlw_stage2_20261013/symplectic/symplectic_defect.png)、[中点容差图](Workspaces/dlw_stage2_20261013/symplectic/midpoint_solver_tolerance.png)（均有同名PDF）
- [单步表](Workspaces/dlw_stage2_20261013/symplectic/single_step.csv)、[定时间表](Workspaces/dlw_stage2_20261013/symplectic/fixed_time.csv)、[累计缺陷](Workspaces/dlw_stage2_20261013/symplectic/defect_timeseries.csv)、[单步观测阶](Workspaces/dlw_stage2_20261013/symplectic/single_step_orders.csv)、[定时间观测阶](Workspaces/dlw_stage2_20261013/symplectic/fixed_time_orders.csv)
- [Newton容差扫描](Workspaces/dlw_stage2_20261013/symplectic/midpoint_tolerance.csv)、[至少两次Newton对照](Workspaces/dlw_stage2_20261013/symplectic/midpoint_min_two_iterations.csv)、[网格复查](Workspaces/dlw_stage2_20261013/symplectic/grid_checks.csv)、[物理辛形式拉回](Workspaces/dlw_stage2_20261013/symplectic/physical_pullback.csv)、[谐振子精确校准](Workspaces/dlw_stage2_20261013/symplectic/harmonic_calibration.csv)
- [2C完整误差Lax推导](Workspaces/dlw_stage2_20261013/error_lax/REPORT.md)、[精确验证脚本](Workspaces/dlw_stage2_20261013/error_lax/verify_error_lax.py)、[38项158条证书](Workspaces/dlw_stage2_20261013/error_lax/exact_checks.json)、[2B独立审查](Workspaces/dlw_stage2_20261013/error_lax/cross_review_symplectic.md)
- [相位/轨道/强迫误差证明](Workspaces/dlw_stage2_20261013/synthesis.md)、[root独立符号校准](Workspaces/dlw_stage2_20261013/verify_synthesis.py)、[校准记录](Workspaces/dlw_stage2_20261013/synthesis_validation.json)
- [HTML构建](Workspaces/dlw_stage2_20261013/build_report.py)、[交付核验](Workspaces/dlw_stage2_20261013/verify_delivery.py)、[18项结果](Workspaces/dlw_stage2_20261013/delivery_validation.json)、[输入哈希](Workspaces/dlw_stage2_20261013/baseline.json)、[记录合并器](Workspaces/dlw_stage2_20261013/update_records.py)

'''
if marker not in old:
    anchor='<!-- DLW_THREE_TRACKS_20261013 -->'
    if anchor not in old:
        raise RuntimeError('Stage-1 index anchor missing.')
    revised=old.replace(anchor,block+anchor,1)
    if index.read_text(encoding='utf-8')!=old:
        raise RuntimeError('Concurrent index change; rerun merge.')
    index.write_text(revised,encoding='utf-8')
print('Merged stage-2 progress and index into the existing topic.')
