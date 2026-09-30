"""Merge this completed scan into the existing DLW topic and file index."""
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MARK=' **同日 p 参数优势带扫描：** '
ENTRY=(MARK+'[受控 p 扫描报告](Workspaces/dlw_p_regions_20260926/REPORT.md)固定 a=4、q=3、ρ=p+q、c=κ=0、β=1、Euler，'
       '9个p×FD/SD×固定/负支/正支/对称×主/减步/细x配置，加局部确认，共276条记录（224新＋52匹配复用），全部完成。'
       '主Nx512中p=.75/1/1.25/1.5的SD正支u最小、对称v最小；p=2/2.25/2.5则对称u最小、正支v最小，减半时间步保持。'
       '对称SD主网格9/9双场改善固定，细网格优势缩小或反转。p=.9/.95/1/1.05/1.1在T=.01的三配置中SD负支均双场胜同密度FD，'
       '细x比u=.896–.952、v=.834–.969，端点与中心再减步仍胜；但T=.005细网格u全部反败，故仅为条件性采样候选带。'
       'p≥1.75细网格逐步出现增长，p=2.5对称SD误差约.545/.876，不能把完成当稳定。GSG原文只有三代表p的精度比较，波形分区非全区间误差定理。'
       '276个NPZ、18个源码/清单哈希、138组同初态配对与552快照误差回读通过，误差回读差0；候选32Nx评价变化≤.149%，'
       '主Euler减步最大变化2.415%。输出完整u/v同格表、CSV、2张PNG/PDF和条件连续性邻域论证；未做统计显著性、区间认证、全时间或跨分辨率统一最优声明。')

path=ROOT/'PROGRESS_LOG.md'
txt=path.read_text(encoding='utf-8')
lines=txt.splitlines()
index=next(i for i,line in enumerate(lines) if line.startswith('> **2026-09-26（双线性'))
if MARK in lines[index]:
    lines[index]=re.sub(re.escape(MARK)+r'.*?(?= \*\*同日 |$)',lambda _:ENTRY,lines[index])
else:lines[index]+=ENTRY
path.write_text('\n'.join(lines)+'\n',encoding='utf-8')

block='''- [DLW p 参数优势带扫描](Workspaces/dlw_p_regions_20260926/REPORT.md)（a=4/q=3固定切片、条件密度排名、SD/FD候选带、时刻反转与大p增长）
- `Workspaces/dlw_p_regions_20260926/scan.py`、`refine.py`（216主扫描＋60局部确认记录，224新演化＋52匹配旧轨道，Euler）
- `Workspaces/dlw_p_regions_20260926/analyze.py`、`make_report.py`、`finish_docs.py`（276哈希/初态/误差审计、稠密评价、双场表/科学图与文档同步）
- `Workspaces/dlw_p_regions_20260926/out/`（scan/refinement冻结JSON、224新NPZ、summary.json、errors.csv、ratios.csv、full_tables.md；复用文件路径与哈希明确记录）
- `Workspaces/dlw_p_regions_20260926/sd_fd_regions.png/pdf`、`symmetric_regions.png/pdf`（同网格SD/FD比与对称/固定误差比随p变化）

'''
path=ROOT/'FILE_INDEX.md';txt=path.read_text(encoding='utf-8')
if '- [DLW p 参数优势带扫描]' not in txt:
    anchor='**2HS 守恒密度动网格参数总体检验（2026-09-26）：**'
    assert anchor in txt
    txt=txt.replace(anchor,block+anchor,1)
    path.write_text(txt,encoding='utf-8')
print('Merged into existing DLW progress entry; file index updated.')
