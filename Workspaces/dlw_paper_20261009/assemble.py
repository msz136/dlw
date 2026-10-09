from pathlib import Path
import re, json, shutil, hashlib

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
theory=(ROOT/'Workspaces/dlw_theory_notebook_20261008/paper.src.md').read_text(encoding='utf-8').split('## 参考文献')[0]
theory=theory.replace('# DLW 方程的半离散化、τ 函数与连续极限','# （2+1）维 DLW 方程的半离散化、Lax 表示与数值模拟',1)
abstract='''<div class="abstract"><span class="abstract-label">摘要</span> 对（2+1）维色散长波（DLW）方程构造交错格点半离散双线性系统。利用 Gram 行列式的秩一更新证明任意有限阶 τ 函数的精确性，并在正则谱域内建立物理场的二阶连续极限。通过消去或保留辅助势，导出 SD 与 SD2 两种非线性表示，给出两者的物理变量对应和 Darboux–Lax 相容性证明。数值计算进一步对保留连续的空间方向采用三点中心差分，并比较固定、动网格及不同时间算法。单孤子与二孤子试验表明，误差优势随算例和物理场变化；理论上的半离散二阶一致性与全离散计算的误差分别讨论。</div>'''
theory=re.sub(r'<div class="abstract">.*?</div>',lambda m:abstract,theory,count=1,flags=re.S)
theory=theory.replace('**关键词：** DLW 方程；半离散双线性系统；Gram 行列式；交错格点；连续极限','**关键词：** 色散长波方程；可积半离散化；Gram 行列式；Lax 对；连续极限；数值模拟\n\n## 引言')
intro='''Sheng–Yu [1] 通过双线性方法与 KP 层级约化研究连续 DLW 系统的行列式解，为本文的解构造及数值基准提供参照。Feng–Sheng–Yu [2] 将广义 sine–Gordon 方程的可积半离散化与自适应动网格计算结合，展示了从精确离散结构到数值方法的研究路径。本文采用相近的比较框架，但 DLW 具有两个空间方向：离散 $y$ 后仍保留 $x$ 导数，因此还需独立说明 $x$ 方向的差分与网格映射。文献 [2] 的（4.13）—（4.14）采用三点二阶差分的时间平均格式；本文据此对照差分记法，不将其一维算法直接视为 DLW 的数值格式。

离散系统的线性问题与非线性表示之间的联系，也见于二维 Toda 的直接线性化研究 [3] 和修正色散长波方程的 Darboux 构造 [4]。本文给出所构造半离散 DLW 系统自身的相容性计算，而不通过形式相似性移用其他方程的 Lax 对。

'''
theory=theory.replace('半离散化将一个空间方向',intro+'半离散化将一个空间方向',1)
theory=theory.replace('最后，分别考察方程的一致性与精确解族的连续极限，并明确两条非线性方程各自的空间评价位置。','随后考察方程的一致性与精确解族的连续极限，导出两种非线性形式及其 Lax 表示，最后将理论模型用于孤子数值比较。')
theory=theory.replace('## 5　正 τ 函数与非线性物理场','## 5　正则性与第一种非线性形式（SD）')
theory=theory.replace('## 附录　Q、R、M 的势表示','## 7　第二种非线性形式（SD2）及其物理场')
theory+=r'''

**命题 7.1（物理场的精确对应）。** 由同一正 τ 函数对构造 SD 和 SD2 时，两种形式恢复的 $u_j,v_j$ 在每个有限格距下完全相同。在定理 6.3 的固定谱条件下，SD2 恢复的物理场也满足（35）的一致二阶估计。

**证明。** 由（38），$2Q_{j,x}/Q_j=(2\alpha_j-\beta_j-\beta_{j+1})_x=u_j$；由（42），$4(1-Q_jR_j)=4\omega_j/h$。将二者代入（48），得到 SD 的物理场重构，故两者逐点相同。（35）因而同时适用于两种表示。□

'''
# Present the two treatments of Z consecutively, before the common limit theory.
prefix, rest=theory.split('## 6　二阶一致性与精确解族的连续极限',1)
limit, potential=rest.split('## 7　第二种非线性形式（SD2）及其物理场',1)
limit='## 7　二阶一致性与精确解族的连续极限'+limit
limit=re.sub(r'(?<=### )6\.', '7.', limit)
limit=re.sub(r'(命题 |定理 |第 )6\.',r'\g<1>7.',limit)
potential='## 6　势函数形式：保留并表示辅助势'+potential
potential=potential.replace('命题 7.1','命题 6.1').replace('定理 6.3','定理 7.3')
potential=potential.replace('设 $F_j,G_j$ 满足定理 5.2 的条件，沿用',
    '另一条非线性化路线从（29）出发，保留 $Z_j$，并用势函数表示它。设 $F_j,G_j$ 满足定理 5.2 的条件，沿用',1)
potential=potential.replace('代入（29），得到',
    '因此，$Z_j$ 被写成物理场 $u_j$ 与相邻辅助势 $M_j,M_{j+1}$ 的组合。将此表示直接代入（29），得到',1)
prefix=prefix.replace('## 5　正则性与第一种非线性形式（SD）','## 5　正则性与差分消势形式')
prefix=prefix.replace('### 5.2　物理变量重构与势的消去','### 5.2　物理变量与共同的辅助势方程')
needle='式（27）、（28）给出'
prefix=prefix.replace(needle,
    '式（29）是两种非线性化的共同起点。第一种对 $Z_j$ 作格点差分，利用相邻格点关系消去该势；第二种引入势函数表示 $Z_j$，保留其局部结构，见第 6 节。\n\n### 5.3　对辅助势作差分并消元\n\n'+needle,1)
source=prefix+potential+'\n'+limit+'\n'+(HERE/'lax_bridge.md').read_text(encoding='utf-8')+'\n'+(HERE/'numerics.md').read_text(encoding='utf-8')
source=source.replace('第 7 节所写的 SD2','第 6 节所写的 SD2').replace('第 7 节的势变量形式','第 6 节的势变量形式')
# Update remaining references in the numerical section to the relocated limit theorem.
source=source.replace('定理 6.3','定理 7.3')
tables=json.loads((HERE/'tables.json').read_text(encoding='utf-8'))
for key,name in [('SPACE','space_table'),('TIME','time_table'),('ORDER','order_table'),('MESH','mesh_table')]:
    table=tables[name].replace('<table ','<table aria-label="数值比较表" ')
    source=source.replace('TABLE_'+key,'<div class="table-wrap">'+table+'</div>')
figures=[]
for i in range(1,7):
    case='ABC'[(i-1)//2]
    what='数值物理场与解析场对照' if i%2 else '绝对误差分布'
    figures.append(f'<figure><img src="../Workspaces/dlw_paper_20261009/figure_{i}.png" alt="算例{case}：{what}" loading="lazy"><figcaption>图 {i}　算例 {case} 的{what}。SD2，RK4，固定网格，T = 0.01。</figcaption></figure>')
source=source.replace('FIGURES','\n\n'.join(figures))
source=source.replace('SD2','势函数形式').replace('SD','差分消势形式')
source=source.replace('（差分消势形式）','').replace('（势函数形式）','')
source=source.replace('差分消势形式','PE').replace('势函数形式','PF')
source=source.replace('PE 与 PF 两种非线性表示',
    '差分消势形式（potential-elimination formulation，PE）与势函数形式（potential formulation，PF）',1)
source=source.replace('## 5　正则性与PE','## 5　正则性与 PE 形式')
source=source.replace('## 6　PF：','## 6　PF 形式：')
tags=re.findall(r'\\tag\{([^}]+)\}',source)
assert len(tags)==len(set(tags))
mapping={tag:str(i+1) for i,tag in enumerate(tags)}
source=re.sub(r'\\tag\{([^}]+)\}',lambda m:r'\tag{'+mapping[m[1]]+'}',source)
source=re.sub(r'（([LN]?\d+)）',lambda m:'（'+mapping.get(m[1],m[1])+'）',source)
assert not any(ord(c)<32 and c not in '\n\t\r' for c in source)
from editorial import revise
source,prose_changes=revise(source)
from determinant_only import revise as retain_determinants
source=retain_determinants(source)
from methods_revision import revise as revise_methods
source=revise_methods(source)
from narrative_revision import revise as revise_narrative
source=revise_narrative(source)
from structure_revision import revise as revise_structure
source=revise_structure(source)
from full_comparison_revision import revise as revise_full_comparison
source=revise_full_comparison(source)
tags=re.findall(r'\\tag\{([^}]+)\}',source)
(HERE/'style_revision/prose_changes.json').write_text(json.dumps(prose_changes,ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'manuscript.md').write_text(source,encoding='utf-8')
# Reuse the already established offline paper renderer and CSS.
build=(ROOT/'Workspaces/dlw_lax_derivation_20261009/build.py').read_text(encoding='utf-8')
build=build.replace("'compact_manuscript.md'","'manuscript.md'").replace('半离散 DLW 的 Lax 对','（2+1）维 DLW 方程的半离散化、Lax 表示与数值模拟')
build=build.replace("'report/dlw_lax_derivation.html'","'report/dlw_paper_draft.html'")
build=build.replace('原半离散 DLW 方程、所需条件、辅助线性对及其相容性证明。','DLW 方程的交错半离散化、Gram 行列式解、两种非线性形式、连续极限与孤子数值比较。')
start=build.index('assert tags ==')
end=build.index("assert 'MATHSLOT'",start)
build=build[:start]+f'assert tags == list(range(1,{len(tags)+1})), tags\n'+build[end:]
build=build.replace("    assert (dest.parent / link).exists(), link","    if not link.startswith(('https://','http://')): assert (dest.parent / link).exists(), link")
build=build.replace("count = 0",'''css += """
.abstract{font-size:16px;margin:24px 0;padding:0 20px}.abstract-label{font-weight:bold;margin-right:1em}figure{margin:32px 0;break-inside:avoid}figure img{display:block;width:100%;height:auto}figcaption{font-size:14px;text-align:center;line-height:1.65;margin:12px 0}table{font-variant-numeric:tabular-nums;font-size:13px;white-space:nowrap}th,td{padding:7px 10px}.table-wrap{overflow-x:auto;max-width:100%}tbody tr:nth-child(even){background:#fafafa}nav{border-top:1px solid #ccc;border-bottom:1px solid #ccc;padding:12px 0}h1{max-width:820px;margin-left:auto;margin-right:auto}h3{font-size:19px}@media print{.table-wrap{overflow:visible}table{font-size:8pt}th,td{padding:4px}figure{max-height:240mm}nav{display:none}}@media(max-width:600px){.abstract{padding:0;font-size:15px}figure{margin-left:-8px;margin-right:-8px}figcaption{padding:0 8px}}
"""
count = 0''')
build='\n'.join(line for line in build.split('\n') if not line.startswith("body = body.replace('</h1>'"))
build=build.replace('tbody tr:nth-child(even){background:#fafafa}','')
build=build.replace('count = 0', 'css += "table.comparison th,table.comparison td{text-align:center;vertical-align:middle;background:white}table.comparison tbody th{font-weight:normal}table.comparison thead th{font-weight:600}table.comparison strong{font-weight:800}table.comparison tbody tr:has(th[rowspan=\\\"6\\\"]){border-top:1px solid #ddd}"\ncount = 0')
(HERE/'build.py').write_text(build,encoding='utf-8')
shutil.copy2(ROOT/'Workspaces/dlw_lax_derivation_20261009/render.cjs',HERE/'render.cjs')
print(json.dumps({'equations':len(tags),'source_characters':len(source)},ensure_ascii=False))
