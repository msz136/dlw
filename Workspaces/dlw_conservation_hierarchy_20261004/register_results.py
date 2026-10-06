"""Idempotent same-topic progress and exact file-inventory registration."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
backup=HERE/'before_registration'
backup.mkdir(exist_ok=True)
for name in ('PROGRESS_LOG.md','FILE_INDEX.md'):
    dst=backup/name
    if not dst.exists():
        dst.write_bytes((ROOT/name).read_bytes())

log_path=ROOT/'PROGRESS_LOG.md'
log=log_path.read_text(encoding='utf-8')
start=log.index('<!-- DLW_HAMILTON_BEGIN -->')
end=log.index('<!-- DLW_HAMILTON_END -->',start)+len('<!-- DLW_HAMILTON_END -->')
block=log[start:end]
old='> **2026-10-04（半离散 DLW Hamilton 结构）：** [论文式报告](dlw_hamilton.html)。'
new='''> **2026-10-04（半离散 DLW Hamilton 结构与守恒层级）：** [守恒生成式与对易量](report/dlw_conservation_hierarchy.html)。**最新形式守恒层级：** 固定周期平均叶c≠0,γ，显式V=RDw/2−hDw/4−Πe/c接原SD到完整交织，不需全局τ。P=∏(D−b)⁻¹(D−α)，G=Σhw/4≠0、T=ΣhUw/4为常数；L=−G(P−1)⁻¹−(G²−T)/(2G)，I_n=Tr res Lⁿ给无穷形式守恒递推。因子原常括号→raw Adler尺度1/8，trace梯度与P对易；共同U标量规范使ΣI_U=0，故整个族在既有Jred两两对易，无周期D零模反演。前五密度/通量显式；I1为旧K/P组合，I2与新Q4一般N等价，已用BCH至D⁻4去重。Q4=hΣ∫[U³w/3+2βUw³/3+2UwUx−4Uxwx/3+UwRDw]，Q5需减8hN/c∫(Πe)²才适配原周期流，裸Q5有−473181/256精确漂移反例。一般Q4/Q5red守恒由skewR和极化三线性trace恒等式直接证明。固定Casimir叶N3 G6 T12四cos模的四泛函Jacobian=411796986221479423/4426355198361600000≠0；h4简化可按g=hw/4延伸任意h，得K/Pmom/Q4/I3四独立对易量。N3指定G,T任意微分场证ρ3=−Q5red_density/128+3Q4_density/32−H0_density/2+228/5；一般N第五次桥未写，不另计Q5。连续二维Riccati递推至q5，β→0及固定Nh有序单值化极限相符；朴素two-boson第二括号Jacobiator1/4排除该候选。原文1a/1b/二孤子全部谱矩C_n=−Σ[p_iⁿ−(−q_i)ⁿ]/n精确，单站x值有限而全j和发散；谱族秩2/2/4。无限独立性、Liouville完备性、非周期relative单值化/对易延拓未证；旧Y不控制新梯度RD(Uw)，单格点第一扰动有ξ/θ域反例。25项PDO精确检查、36项原文基准检查、Q4/Q5结构/mean补正、固定叶与ρ3桥证书及两路独立审阅通过。用户报告26 MathML块、1440/390离线排版与链接通过；全部材料Workspaces/dlw_conservation_hierarchy_20261004/，无新PDE推进。 **此前Hamilton构造：** [论文式报告](dlw_hamilton.html)。'''
if old in block:
    block=block.replace(old,new,1)
elif '守恒生成式与对易量' not in block:
    raise RuntimeError('Missing expected same-topic entry')
remainder=(log[:start]+log[end:]).lstrip('\n')
log_path.write_text(block+'\n\n'+remainder,encoding='utf-8')

index_path=ROOT/'FILE_INDEX.md'
index=index_path.read_text(encoding='utf-8')
begin='<!-- DLW_CONSERVATION_INDEX_BEGIN -->'
finish='<!-- DLW_CONSERVATION_INDEX_END -->'
if begin in index:
    a=index.index(begin);b=index.index(finish,a)+len(finish)
    index=(index[:a]+index[b:]).lstrip('\n')
lines=[begin,'**半离散 DLW 守恒生成式与对易层级（2026-10-04）：**','',
       '- [dlw_conservation_hierarchy.html](report/dlw_conservation_hierarchy.html)（用户论文式报告；周期无穷形式对易族、Q4/Q5平均补正、四量独立、连续极限及原文三组谱矩）']
groups={}
for f in HERE.rglob('*'):
    if not f.is_file() or '__pycache__' in f.parts or 'before_registration' in f.parts:
        continue
    groups.setdefault(str(f.parent.relative_to(ROOT)).replace('\\','/'),[]).append(f.name)
for group,names in sorted(groups.items()):
    lines.append('- `'+group+'/`：'+ '、'.join('`'+name+'`' for name in sorted(names)))
lines.append('- `Workspaces/dlw_conservation_hierarchy_20261004/before_registration/PROGRESS_LOG.md`、`FILE_INDEX.md`（共享登记修改前保留）')
lines.append(finish)
index='\n'.join(lines)+'\n\n'+index
index=index.replace('当前用户报告共11个：主目录保留4个入口，7个专题页面位于 `report/`。','当前用户报告共12个：主目录保留4个入口，8个专题页面位于 `report/`。')
row='| [dlw_conservation_hierarchy.html](report/dlw_conservation_hierarchy.html) | 半离散DLW守恒生成式、形式对易族、四次/第五次密度及原文谱矩。 |'
if row not in index:
    anchor='| report 专题页面 | 内容与用途 |\n| --- | --- |'
    assert anchor in index
    index=index.replace(anchor,anchor+'\n'+row,1)
index_path.write_text(index,encoding='utf-8')
manifest={'report':'report/dlw_conservation_hierarchy.html',
          'sha256':hashlib.sha256((ROOT/'report/dlw_conservation_hierarchy.html').read_bytes()).hexdigest(),
          'progress_merged':True,'file_inventory_updated':True,
          'limitations':['Infinite independence and Liouville completeness unproved.','No transfer of periodic trace theorem to nonperiodic relative backgrounds.']}
(HERE/'registration.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False))
