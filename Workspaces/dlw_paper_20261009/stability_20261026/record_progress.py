from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[3]
index=ROOT/'FILE_INDEX.md'
ib=index.read_bytes();it=ib.decode('utf-8')
row='| DLW 独立物理场扰动 | A/D、高斯与正弦的独立 u/v 扰动及连续误差认证 | 八条有限网格轨道、现行闭合线性机制与初值匹配证明稿；完整连续误差界待解 | [主论文 Section 6](dlw-paper.html#section-6)；[研究报告](report/dlw_independent_stability_20261026.html)；[入口与目录](Workspaces/dlw_paper_20261009/stability_20261026/README.md) |'
if '| DLW 独立物理场扰动 |' not in it:
    anchor=next(x for x in it.splitlines() if x.startswith('| DLW 非退化高斯／正弦基准 |'))
    it=it.replace(anchor,anchor+'\n'+row,1)
    assert index.read_bytes()==ib
    index.write_text(it,encoding='utf-8')

history=ROOT/'Workspaces/workspace_catalog_audit_20261013/progress_history/2026-10.md'
entry='\n\n### 2026-10-26｜DLW 独立扰动与 Section 6\n\n完成四背景独立 u/v 扰动八条 RK4 轨道及图表，核验现行 Centered-SD 常背景谱和双曲响应，D/A 的 v→u 差异主要由横向积分解释。混合问题、匹配导数和首修正尾界经独立复核；完整连续参考误差界仍未闭合。按用户要求全部集中主论文 Section 6，原结论正文不改、顺延 7，摘要与引言不对齐。证据：`Workspaces/dlw_paper_20261009/stability_20261026/README.md`、`section6_validation.json`；阅读：`report/dlw_independent_stability_20261026.html`。\n'
with history.open('a',encoding='utf-8') as f:f.write(entry)

progress=ROOT/'PROGRESS_LOG.md'
pb=progress.read_bytes();pt=pb.decode('utf-8')
current=re.search(r'## 本次工作[\s\S]*?(?=\n## 上一次工作|\Z)',pt).group(0).strip()
current=current.replace('## 本次工作','## 上一次工作',1)
new='''# 当前工作与最近交接

## 本次工作｜DLW 独立扰动与 Section 6（2026-10-26，图文已写入；连续认证待续）

当前采用 A/D、高斯、正弦四背景，各自独立扰动 u 或 v；八条轨道均到 T=.01，h=Δx=.1、RK4 Δt=1e−4、ε=1e−6、κ=π/2。已核验自然 Centered-SD 常背景谱、双曲响应及数值数据；D/A 的 v→u 差异主要来自横向积分长度。混合问题、非零匹配导数及首次高斯修正尾界已复核，完整独立扰动连续解的 ηu/ηv 仍未取得；下一步是全匹配逆尾和高阶修正，孤子还需域截断界。

按用户最新要求全部集中 Section 6（6.1 线性机制、6.2 独立扰动、6.3 连续参考认证）；移除旧 4.4/5.5，原结论仅顺延 Section 7。摘要、引言和结论正文保持原样，不做全篇对齐。29 图 7 表，旧数值小节与28图不变，公式渲染及链接检查通过。入口：`dlw-paper.html#section-6`；`report/dlw_independent_stability_20261026.html`；`Workspaces/dlw_paper_20261009/stability_20261026/README.md`。

'''+current+'\n'
assert len(new)<3000
assert progress.read_bytes()==pb, 'Concurrent progress update; reread before merging.'
progress.write_text(new,encoding='utf-8')
print('Updated project branch, appended history, and preserved the latest other-task progress in the previous slot.')
