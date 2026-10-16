"""Merge this topic into the workspace progress and artifact index."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
progress = ROOT / 'PROGRESS_LOG.md'
old = progress.read_text(encoding='utf-8')
lines = old.splitlines(keepends=True)
marker = '（DLW 下阶段研究方向评议）'
newmarker = '（DLW 三项并行研究与方向评议）'
addition = (
    '**三项实施完成：** 新增 [三项整合报告](report/dlw_three_tracks_20261013.html) 与 '
    '`Workspaces/dlw_three_tracks_20261013/`。1A采用周期平均约束流形，明确前三个逆单值化谱积分的固定密度离散版，'
    '完成中心差分24/48/96及Fourier24/48、81时刻漂移、空间/时间分离和CSV；中心漂移约二阶，'
    'Hamilton量漂移≤2.3e−13，ΔI₁=−ΔK/48+ΔP/24残差<7e−15，中心三轨迹缺陷积分与实测差<7.5e−13。'
    '1B重算论文A/C的PE/FD及PE半步长共六条21帧轨道，四个主终态与原存档逐值相同；'
    '完成二维Fourier、共同y=−0.05截面Morlet小波、格点极值/连通分量/阈值敏感性，9组PNG/PDF和4个GIF。'
    '授权后PyWavelets隔离安装，252场帧Parseval最大残差1.39e−15；加窗影响显著，未发现可认定新增孤子的谱证据，'
    '当前结果不支持PE普遍更准确。1C给出原物理场括号、一般坐标推前Jacobi证明、Casimir和秩；'
    '1596个全符号三元组及66项精确检查通过，有理反例K点=0、P点=169/12936，说明连续时间Hamilton空间离散仍可破坏平移动量。'
    '三代理交叉审读；26项交付检查通过，289处严格离线数学渲染，原Notebook哈希保持，未修改论文。'
    '周期守恒试验与论文孤子试验的边界条件明确区分，未声称有限维Liouville可积或长期误差定理。 '
    '**此前方向评议：** '
)
if newmarker not in old:
    target = next(i for i, line in enumerate(lines) if marker in line)
    previous = lines.pop(target)
    prefix, body = previous.split('：** ', 1)
    updated = prefix.replace(marker, newmarker) + '：** ' + addition + body
    revised = updated.rstrip() + '\n\n' + ''.join(lines).lstrip('\n')
    # Avoid overwriting concurrent updates to this shared log.
    if progress.read_text(encoding='utf-8') != old:
        raise RuntimeError('Progress changed during merge; rerun against the latest file.')
    progress.write_text(revised, encoding='utf-8')

index = ROOT / 'FILE_INDEX.md'
old_index = index.read_text(encoding='utf-8')
index_marker = '<!-- DLW_THREE_TRACKS_20261013 -->'
block = '''<!-- DLW_THREE_TRACKS_20261013 -->
**DLW 三项并行研究：守恒量、频谱与Poisson（2026-10-13）：**

- [三项整合报告](report/dlw_three_tracks_20261013.html)（1A/1C周期平均约束实验与1B论文孤子轨道分开解释；图、动画、表与完整推导）
- [复现入口](Workspaces/dlw_three_tracks_20261013/README.md)、[报告生成器](Workspaces/dlw_three_tracks_20261013/build_report.py)、[交付检查](Workspaces/dlw_three_tracks_20261013/verify_delivery.py)、[核验结果](Workspaces/dlw_three_tracks_20261013/delivery_validation.json)、[进度索引更新器](Workspaces/dlw_three_tracks_20261013/update_records.py)
- [原轨道生成器](Workspaces/dlw_three_tracks_20261013/generate_shared.py)、[冻结Notebook代码单元](Workspaces/dlw_three_tracks_20261013/shared/solver_cells.json)；shared/ 下 A/C×SD/FD 与 SD_halfdt 的6份NPZ、JSON和端点NPZ（21实际时刻；四主终态与论文存档逐值一致）
- [1A脚本](Workspaces/dlw_three_tracks_20261013/conservation/conservation_experiment.py)、[1A推导](Workspaces/dlw_three_tracks_20261013/conservation/DERIVATION_AND_RESULTS.md)、[1A核验](Workspaces/dlw_three_tracks_20261013/conservation/validation.json)
- [1A汇总](Workspaces/dlw_three_tracks_20261013/conservation/invariant_summary.csv)、[1A逐时表](Workspaces/dlw_three_tracks_20261013/conservation/invariant_timeseries.csv)、[空间精化](Workspaces/dlw_three_tracks_20261013/conservation/space_refinement.csv)、[时间精化](Workspaces/dlw_three_tracks_20261013/conservation/time_refinement.csv)；conservation/ 下5主轨道、时间精化和试运行NPZ保留
- [守恒量漂移](Workspaces/dlw_three_tracks_20261013/conservation/invariant_drift_absolute.png)、[相对漂移](Workspaces/dlw_three_tracks_20261013/conservation/invariant_drift.png)、[空间/时间分离](Workspaces/dlw_three_tracks_20261013/conservation/error_separation.png)（均有同名PDF）
- [1B脚本](Workspaces/dlw_three_tracks_20261013/spectrum/analyze_error_fields.py)、[完整方法](Workspaces/dlw_three_tracks_20261013/spectrum/README.md)、[数值结论](Workspaces/dlw_three_tracks_20261013/spectrum/FINDINGS.md)、[结论生成器](Workspaces/dlw_three_tracks_20261013/spectrum/build_findings.py)、[哈希与校准](Workspaces/dlw_three_tracks_20261013/spectrum/out/manifest.json)；spectrum/vendor/ 为已获授权的隔离PyWavelets
- [1B终态汇总](Workspaces/dlw_three_tracks_20261013/spectrum/out/endpoint_summary.csv)、[252场帧表](Workspaces/dlw_three_tracks_20261013/spectrum/out/spectral_metrics.csv)、[局域极值](Workspaces/dlw_three_tracks_20261013/spectrum/out/local_extrema.csv)、[连通分量](Workspaces/dlw_three_tracks_20261013/spectrum/out/excursion_components.csv)、[阈值敏感性](Workspaces/dlw_three_tracks_20261013/spectrum/out/threshold_sensitivity.csv)、[时间步对照](Workspaces/dlw_three_tracks_20261013/spectrum/out/dt_refinement.csv)
- [1B时序总览](Workspaces/dlw_three_tracks_20261013/spectrum/out/error_diagnostics_summary.png)；spectrum/out/ 下 A/C×SD/FD 的 *_fourier.png/pdf、*_wavelet.png/pdf、*_error_evolution.gif（4动画均21帧）及12个终态谱/CWT数据包；C_SD_RK4_animation_frame10.png为目视检查帧
- [1C完整推导](Workspaces/dlw_three_tracks_20261013/poisson/report.md)、[精确符号脚本](Workspaces/dlw_three_tracks_20261013/poisson/verify_poisson.py)、[66项与1596三元组证书](Workspaces/dlw_three_tracks_20261013/poisson/exact_checks.json)、[1B独立交叉审查](Workspaces/dlw_three_tracks_20261013/poisson/cross_review_spectrum.md)

'''
if index_marker not in old_index:
    anchor = '**DLW 研究 pipeline：理论驱动的命题调研（2026-10-01）：**'
    if anchor not in old_index:
        raise RuntimeError('Index topic anchor missing.')
    new_index = old_index.replace(anchor, block + anchor, 1)
    if index.read_text(encoding='utf-8') != old_index:
        raise RuntimeError('Index changed during merge; rerun against the latest file.')
    index.write_text(new_index, encoding='utf-8')
print('Merged topic into PROGRESS_LOG.md and FILE_INDEX.md.')
