"""Merge this study into the existing DLW error topic and file index."""
from pathlib import Path

root=Path(__file__).resolve().parents[2]
log=root/'PROGRESS_LOG.md'
text=log.read_text(encoding='utf-8')
marker='2026-09-30（固定网格空间二阶系数上下界）'
entry='**'+marker+'：** 接受现有结果，仅新增纯y半离散解析估计；[报告](Workspaces/dlw_h2_bounds_20260930/REPORT.md)给原文A/B/C的SD（含相容SD2）/FD二阶残差全局上下界。单孤子用精确有理Sturm隔根与区间求值，显示区间宽1e−12；二孤子完整相互作用用精确有理Bernstein包围，宽<1e−6，见证点对每个t∈[0,.01]均在x∈[-10,10]/连续y∈[-1.5,1.5]内。A/B补有限h四阶残差余项界：h=.125时SD两式首项保证偏差分别≤.8213%/3.7515%、.3216%/.9129%。共同物理初值与y0=-1.5基值下，推导并包围场误差h²首项初始增长率；给有限时间系数的传播/缺陷及短时二阶时间余项条件界，尚未认证T=.01场误差系数。明确同谱孤子族系数需齐次初边值纠正、纯y相容SD/SD2同系数；未据残差排名推断总场排名。60位新有限h余项检查和包围引擎检查通过，未复核旧数据、未新增非线性PDE轨道、未改HTML或Lean。 '
if marker not in text:
    anchor='> **2026-09-29（同专题 DLW 三路线误差盘点）：**'
    assert anchor in text
    text=text.replace(anchor,'> '+entry+'**2026-09-29（同专题 DLW 三路线误差盘点）：**',1)
    log.write_text(text,encoding='utf-8')

index=root/'FILE_INDEX.md'
text=index.read_text(encoding='utf-8')
link='[固定网格空间二阶系数及上下界](Workspaces/dlw_h2_bounds_20260930/REPORT.md)'
if link not in text:
    anchor='**DLW 三路线误差现状复核（2026-09-29）：**'
    assert anchor in text
    replacement='**DLW 固定网格二阶系数与三路线误差（2026-09-30／29）：**\n\n'
    replacement+='- '+link+'（原文A/B/C；纯y残差、有限h余项、共同初值场误差首项初始增长率和传播条件界）\n'
    replacement+='- `Workspaces/dlw_h2_bounds_20260930/single_bounds.py`、`bernstein.py`、`two_coefficients.py`、`two_strip_bounds.py`（精确有理极值包围及二孤子物理见证）\n'
    replacement+='- `Workspaces/dlw_h2_bounds_20260930/velocity_bounds.py`、`remainder_bounds.py`（初始误差系数速度及有限h四阶余项）\n'
    replacement+='- `Workspaces/dlw_h2_bounds_20260930/single_bounds.json`、`two_bounds.json`、`two_strip_bounds.json`、`velocity_bounds.json`、`remainder_bounds.json`（系数、包围及精确有理见证）\n'
    replacement+='- `Workspaces/dlw_h2_bounds_20260930/validate_new_bounds.py`、`validation.json`、`make_report.py`（新界检查与报告生成）'
    text=text.replace(anchor,replacement,1)
    index.write_text(text,encoding='utf-8')
print('Merged existing progress topic and updated file index.')
