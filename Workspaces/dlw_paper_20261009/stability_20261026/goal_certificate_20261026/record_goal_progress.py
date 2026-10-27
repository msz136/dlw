"""Record renewed certification scope, retaining the other progress slot."""
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
index=ROOT/'FILE_INDEX.md'
original=index.read_bytes();src=original.decode('utf-8')
line=next(x for x in src.splitlines() if x.startswith('| DLW 独立物理场扰动 |'))
new='| DLW 独立物理场扰动 | A/D、高斯与正弦的独立 u/v 扰动及连续认证goal | 正文6.1/6.2保留响应；认证goal重启，全非线性残差/有限采样无有限统一界及同包络初值邻域障碍已推导核验；固定单频初值的专门参考仍开放 | [主论文 Section 6](dlw-paper.html#section-6)；[最新goal报告](report/dlw_reference_goal_20261026.html)；[扰动报告](report/dlw_independent_stability_20261026.html)；[入口与目录](Workspaces/dlw_paper_20261009/stability_20261026/README.md) |'
assert index.read_bytes()==original
index.write_bytes(src.replace(line,new,1).encode('utf-8'))

progress=ROOT/'PROGRESS_LOG.md'
original=progress.read_bytes();src=original.decode('utf-8')
assert '## 本次工作｜DLW 独立扰动与 Section 6' in src
previous=src[src.index('## 上一次工作'):]
history=ROOT/'Workspaces/workspace_catalog_audit_20261013/progress_history/2026-10.md'
entry=('\n\n### 2026-10-26｜DLW 连续参考goal：高频认证障碍\n\n'
       '用户重启并设置goal。独立审计加强全非线性残差反例为任意r>0、M>0，保持精确初边值及有限采样而残差<r、终态v误差=M；解析候选也成立。新增同sin²包络的有限阶边界jet证明，排除普通初值不确定球上的统一光滑认证；256-bit参数例子及符号核验通过。固定单频受扰IVP的完整参考/绝对不可能性仍开放，goal保持active。主论文未改。证据：`report/dlw_reference_goal_20261026.html`；`Workspaces/dlw_paper_20261009/stability_20261026/goal_certificate_20261026/STATUS.json`。\n')
with history.open('a',encoding='utf-8',newline='') as f:f.write(entry)
current=('# 当前工作与最近交接\n\n'
 '## 本次工作｜DLW 连续参考goal与独立扰动（2026-10-26，active）\n\n'
 '用户撤销暂缓并显式设置goal：给当前独立u/v扰动的连续参考明确误差界，或严格证明高频导致哪类认证不可能。全非线性反例已独立复核并加强：任意残差r>0、终态v误差M>0，可保持精确初边值及有限采样；逐个解析候选亦成立，排除无统一导数/尾界的残差认证。256-bit例子做到残差<1e−30、误差=1。新增同sin²包络的初值邻域障碍，有限阶边界jet已足够；可保持有限初始采样完全相同。\n\n'
 '固定精确单载波受扰IVP仍无完整匹配或ηu/ηv；无所有方法均不可能的定理，goal保持active。实际正弦高阶导数必要下界已加强，不能据此排除任意C∞横向解。下一步需攻固定数据的弱横向类匹配/尾界或更强无解定理；不能把方法障碍当goal完成。主论文仍仅6.1/6.2，29图7表未改。入口：`report/dlw_reference_goal_20261026.html`；`Workspaces/dlw_paper_20261009/stability_20261026/goal_certificate_20261026/README.md`；`dlw-paper.html#section-6`。\n\n')
updated=current+previous
assert len(updated)<3000 and progress.read_bytes()==original
progress.write_bytes(updated.encode('utf-8'))
print('Renewed goal scope recorded; other progress slot preserved.')
