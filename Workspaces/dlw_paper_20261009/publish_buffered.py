"""Publish completed notebook runs into the bilingual manuscript."""
from pathlib import Path
import json,re,shutil
import numpy as np
HERE=Path(__file__).resolve().parent
OUT=HERE/'buffered_run'
rows=json.loads((OUT/'results.json').read_text())
assert len(rows)==48 and all(r['completed'] for r in rows)
R={(r['case'],r['model'],r['method'],r['mesh']):r for r in rows}
def err(c,m,t='RK4',mesh='fixed',f='u'):return R[c,m,t,mesh]['max_errors'][f]
models={'PE':'SD','PF':'SD2','FD':'FD'}
def name(c,zh):
    return {'A':'单孤子 (p=1, q=2)','B':'单孤子 (p=4, q=−3)','C':'二孤子 (6,−5; 4,−3)', 'D':'二孤子 (1,2; 4,−3)'}[c] if zh else {'A':'One-soliton (p=1, q=2)','B':'One-soliton (p=4, q=−3)','C':'Two-soliton (6,−5; 4,−3)', 'D':'Two-soliton (1,2; 4,−3)'}[c]
def td(value,best):
    v=f'{value:.6e}'
    return '<td>'+('<strong>'+v+'</strong>' if value==best else v)+'</td>'
def table(kind,zh):
    headers=({'space':['算例','场','PE','PF','FD'],'time':['算例','方法','场','Euler','RK4','C–N'],'mesh':['算例','方法','固定网格：u / v','动网格：u / v']} if zh else {'space':['Case','Field','PE','PF','FD'],'time':['Case','Method','Field','Euler','RK4','C–N'],'mesh':['Case','Method','Fixed mesh: u / v','Moving mesh: u / v']})[kind]
    s='<div class="table-wrap"><table class="comparison"><thead><tr>'+''.join('<th>'+h+'</th>' for h in headers)+'</tr></thead><tbody>'
    for c in 'ABCD':
        if kind=='space':
            for f in 'uv':
                vs=[err(c,m,f=f) for m in models.values()]
                s+='<tr><th>'+name(c,zh)+'</th><th>'+f+'</th>'+''.join(td(v,min(vs)) for v in vs)+'</tr>'
        elif kind=='time':
            for label,m in models.items():
                for f in 'uv':
                    vs=[err(c,m,t=t,f=f) for t in ['Euler','RK4','CN']]
                    s+='<tr><th>'+name(c,zh)+'</th><th>'+label+'</th><th>'+f+'</th>'+''.join(td(v,min(vs)) for v in vs)+'</tr>'
        else:
            for label,m in models.items():
                s+='<tr><th>'+name(c,zh)+'</th><th>'+label+'</th>'
                for mesh in ['fixed','moving']:
                    values=[]
                    for f in 'uv':
                        v=err(c,m,mesh=mesh,f=f);best=min(err(c,m,mesh=z,f=f) for z in ['fixed','moving'])
                        values.append(('<strong>'+f'{v:.6e}'+'</strong>') if v==best else f'{v:.6e}')
                    s+='<td>'+' / '.join(values)+'</td>'
                s+='</tr>'
    return s+'</tbody></table></div>'
ratios={f:[err(c,'SD2',f=f)/err(c,'SD',f=f) for c in 'ABCD'] for f in 'uv'}
cn=max(abs(err(c,m,t='CN',f=f)/err(c,m,f=f)-1)*100 for c in 'ABCD' for m in models.values() for f in 'uv')
reductions=[(1-err(c,m,mesh='moving',f=f)/err(c,m,f=f))*100 for c in 'ABCD' for m in models.values() for f in 'uv']
improved=sum(v>0 for v in reductions)
summary={}
summary['en']=f"The fixed-grid comparison gives PF-to-PE u-error ratios of {', '.join(f'{v:.3g}' for v in ratios['u'])} for the four tests, respectively. The largest relative difference between RK4 and C–N terminal errors is {cn:.3g}%. The moving mesh lowers {improved} of the twenty-four field errors; the percentage changes, measured as reductions relative to the corresponding fixed-grid errors, range from {min(reductions):.3g}% to {max(reductions):.3g}%."
summary['zh']=f"固定网格下，两组单孤子和两组二孤子的 PF 与 PE 的 u 误差比分别为 {'、'.join(f'{v:.3g}' for v in ratios['u'])}。RK4 与 C–N 终止误差的最大相对差异为 {cn:.3g}%。动网格使二十四组物理场比较中的 {improved} 组误差降低；以对应固定网格误差为基准，降幅范围为 {min(reductions):.3g}% 至 {max(reductions):.3g}%。"
source=(OUT/'before/manuscript.md').read_text(encoding='utf-8')
for lang in ['en','zh']:
    zh=lang=='zh'
    a=source.index('### 3.5 ',source.index('{#'+lang+'-tests}'))
    b=source.index('## 4. ',a)
    old=source[a:b]
    figures=re.findall(r'<figure>[\s\S]*?</figure>',old)
    assert len(figures)==6
    figures[4:6]=[f.replace('Two-soliton:', 'Two-soliton (6,−5; 4,−3):').replace('二孤子的', '二孤子（6,−5；4,−3）的') for f in figures[4:6]]
    for error in [False, True]:
        stem='D_errors' if error else 'D_fields'
        caption=('图 ' if zh else 'Figure ')+str(8 if error else 7)+'. '+name('D',zh)+('：绝对误差。' if error and zh else '：数值解。' if zh else ': absolute errors.' if error else ': numerical fields.')+(' 列为 PE、PF、FD；行依次为 u 曲面、u 等高线、v 曲面、v 等高线；误差图显示相应绝对误差。固定网格，RK4，T=0.01。' if zh else ' Columns: PE, PF, FD. Rows: u surface, u contours, v surface, v contours; error plots show the corresponding absolute errors. Fixed mesh, RK4, T=0.01.')
        figures.append('<figure><img src="../Workspaces/dlw_paper_20261009/figures/'+stem+'.png" alt="'+caption+'" loading="lazy"><figcaption>'+caption+'</figcaption></figure>')
    section='### 3.5 '+('数值结果' if zh else 'Numerical results')+' {#'+lang+'-results}\n\n'
    section+=('**空间方法比较。** 表 1 在各算例相同的计算域、网格与 RK4 时间积分下比较三种方法的最大绝对误差。所有误差均在第 3.4 节给出的共同评价网格上计算。\n\n' if zh else '**Spatial-method comparison.** Table 1 compares maximum absolute errors on the same domain and fixed grid with RK4. All errors use the common evaluation grid specified in Section 3.4.\n\n')
    section+=('**表 1　固定网格、RK4 的最大绝对误差；每行最小值加粗。**' if zh else '**Table 1. Maximum absolute errors on the fixed grid with RK4; row minima are bold.**')+'\n\n'+table('space',zh)+'\n\n'
    for c in 'ABCD':
        winners={f:min(models,key=lambda m:err(c,models[m],f=f)) for f in 'uv'}
        section+=(f"{name(c,True)}中，u 与 v 的最小误差分别由 {winners['u']} 和 {winners['v']} 给出。 " if zh else f"For {name(c,False).lower()}, the smallest u and v errors are obtained by {winners['u']} and {winners['v']}, respectively. ")
    section+='\n\n'+(f"四组算例中 PF 与 PE 的 u 误差比分别为 {'、'.join(f'{v:.3g}' for v in ratios['u'])}，v 误差比分别为 {'、'.join(f'{v:.3g}' for v in ratios['v'])}。共同的半离散起点在采用不同非线性变量进行数值演化时，给出不同的物理场误差。\n\n" if zh else f"The PF-to-PE error ratios are {', '.join(f'{v:.3g}' for v in ratios['u'])} for u and {', '.join(f'{v:.3g}' for v in ratios['v'])} for v, in case order. Thus the choice of nonlinear variables affects the physical-field errors obtained from the common semi-discrete construction.\n\n")
    section+=('**时间算法比较。** 保持空间网格与时间步长相同，比较 Euler、RK4 和 C–N。\n\n**表 2　固定网格下各时间算法的最大绝对误差；每行最小值加粗。**' if zh else '**Time-integrator comparison.** Euler, RK4 and C–N are compared at the same spatial resolution and time step.\n\n**Table 2. Maximum absolute errors of the time integrators on the fixed grid; row minima are bold.**')+'\n\n'+table('time',zh)+'\n\n'
    section+=(f"RK4 与 C–N 终止误差的最大相对差异为 {cn:.3g}%。" if zh else f"The largest relative difference between RK4 and C–N terminal errors is {cn:.3g}%. ")
    for label,m in models.items():
        changes=[100*(1-err(c,m,f=f)/err(c,m,t='Euler',f=f)) for c in 'ABCD' for f in 'uv']
        section+=(f"对 {label}，从 Euler 改为 RK4 的误差降幅为 {min(changes):.3g}% 至 {max(changes):.3g}%。" if zh else f"For {label}, replacing Euler by RK4 changes the errors by reductions ranging from {min(changes):.3g}% to {max(changes):.3g}%. ")
    section+=('负值表示误差增加。后续网格比较与场图均采用 RK4。\n\n' if zh else 'Negative reductions denote increases. RK4 is used for the mesh comparison and field plots.\n\n')
    section+=('**固定网格与动网格。** 表 3 保持节点数、时间步长和终止时间相同，每格依次列出 u、v 的误差。\n\n**表 3　固定与动网格的最大绝对误差；各物理场的较小值加粗。**' if zh else '**Fixed and moving meshes.** Table 3 keeps the node counts, time step and final time identical. Each cell lists the u and v errors in that order.\n\n**Table 3. Maximum absolute errors on fixed and moving meshes; the smaller value for each field is bold.**')+'\n\n'+table('mesh',zh)+'\n\n'
    section+=(f"动网格使二十四组比较中的 {improved} 组误差降低。相对于对应固定网格结果，误差降幅为 {min(reductions):.3g}% 至 {max(reductions):.3g}%。" if zh else f"The moving mesh lowers {improved} of the twenty-four field errors. Reductions relative to the corresponding fixed-grid errors range from {min(reductions):.3g}% to {max(reductions):.3g}%. ")
    for label,m in models.items():
        rr=[100*(1-err(c,m,mesh='moving',f=f)/err(c,m,f=f)) for c in 'ABCD' for f in 'uv']
        section+=(f"{label} 的降幅范围为 {min(rr):.3g}% 至 {max(rr):.3g}%。" if zh else f"For {label}, the range is {min(rr):.3g}% to {max(rr):.3g}%. ")
    section+='\n\n'
    section+=('**数值物理场与误差分布。** 图 1—8 与表 1—3 使用相同的内部评价区域，分别展示 $[-5,5]^2$、$[-10,10]^2$ 和 $[-30,30]^2$ 上的结果。每幅图的三列依次为 PE、PF、FD，四行依次为 u 曲面、u 等高线、v 曲面和 v 等高线；误差图按相同布局展示绝对误差。同一物理量在三种方法中采用共同色阶和高度范围。\n\n' if zh else '**Numerical fields and error distributions.** Figures 1–8 use the same interior evaluation regions as Tables 1–3: $[-5,5]^2$, $[-10,10]^2$ and $[-30,30]^2$, respectively. The columns are PE, PF and FD; the rows show the u surface, u contours, v surface and v contours. Absolute-error plots follow the same arrangement. Each physical quantity uses common colour and height scales across methods.\n\n')
    descriptions=([
        '第一组单孤子的两个物理场均为沿斜向波带分布的负脉冲。图 1、2 分别展示数值波形及其绝对误差。',
        '第二组单孤子的 u 为正脉冲，v 为负脉冲。图 3、4 展示三种方法对同一波带的再现及误差分布。',
        '二孤子包含两条不同取向的波带。图 5 展示相互作用区与远离相互作用区的分支，图 6 给出对应误差。'
    ] if zh else [
        'Both fields of the first one-soliton solution are negative pulses along an oblique wave band. Figures 1 and 2 show the numerical profiles and their absolute errors.',
        'The second one-soliton solution has a positive u pulse and a negative v pulse. Figures 3 and 4 compare the wave profiles and error distributions of the three methods.',
        'The two-soliton solution has two differently oriented wave bands. Figure 5 shows the interaction region and the separated branches; Figure 6 gives the corresponding errors.'
    ])
    descriptions.append('第二组二孤子含一正一负的 u 波带，图 7、8 展示其数值解与绝对误差。' if zh else 'The second two-soliton test combines positive and negative u pulses. Figures 7 and 8 show the numerical fields and absolute errors.')
    for i,c in enumerate('ABCD'):
        section+='**'+name(c,zh)+'**\n\n'+descriptions[i]+'\n\n'+figures[2*i]+'\n\n'+figures[2*i+1]+'\n\n'
    section=section.replace('[−20,20]', '[−30,30]')
    source=source[:a]+section+source[b:]
    a=source.index('**计算设置与误差度量。**' if zh else '**Computational settings and error measures.**')
    b=source.index('<a id="'+lang+'-eq-110">',a)
    settings=(r"""**计算设置与误差度量。**

四组算例分别在 $[-10,10]^2$、$[-20,20]^2$、$[-40,40]^2$ 和 $[-40,40]^2$ 上计算；展示与误差评价分别限制于内部区域 $[-5,5]^2$、$[-10,10]^2$、$[-30,30]^2$ 和 $[-30,30]^2$。展示范围对应 Physica D 文献中的图 1(a)、图 1(b)、图 3 和图 4。各算例均取 $\Delta x=h=0.1$，每个方向的计算单元数分别为 200、400、800、800。动网格重新分配 $x$ 节点，保持节点数与 $y$ 层不变。初值取 $t=0$，以 $\Delta t=10^{-4}$ 推进 100 步至 $T=0.01$。

共同评价网格 $\mathcal G$ 在内部 $x$ 区间上取间距 $0.01$ 的等距点，并保留内部 $y$ 单元中点。数值物理场由实际 $x$ 节点作三次样条插值，全部评价点均位于这些节点覆盖的区间内。表格与场图使用相同的内部区域与数值解，定义

""" if zh else r"""**Computational settings and error measures.**

The four tests are computed on $[-10,10]^2$, $[-20,20]^2$, $[-40,40]^2$ and $[-40,40]^2$, respectively. Plots and error evaluation use the interior squares $[-5,5]^2$, $[-10,10]^2$, $[-30,30]^2$ and $[-30,30]^2$, matching the display ranges of Figures 1(a), 1(b), 3 and 4 in the Physica D reference. All tests use $\Delta x=h=0.1$, giving 200, 400, 800 and 800 computational cells in each direction. The moving mesh redistributes x nodes while retaining the node counts and y layers. Starting at $t=0$, each run advances 100 steps with $\Delta t=10^{-4}$ to $T=0.01$.

The common evaluation grid $\mathcal G$ consists of x points spaced by $0.01$ over the interior interval and the interior y-cell centres. Numerical fields are interpolated by cubic splines on the actual x nodes, whose support contains every evaluation point. Tables and field plots use these same interior regions and numerical solutions. Define

""")
    source=source[:a]+settings+source[b:]
    if zh:
        source=re.sub(r'在固定网格算例中，差分消势形式[\s\S]*?(?=\n\n)',summary['zh'],source,count=1)
        source=re.sub(r'进一步用于计算时，表示方式[\s\S]*?(?=\n\n)',summary['zh']+' 非线性表示、时间算法和节点分布共同影响最终物理场误差。',source,count=1)
    else:
        source=re.sub(r'In the fixed-grid tests, the potential-elimination formulation[\s\S]*?(?=\n\n)',summary['en'],source,count=1)
        source=re.sub(r'In numerical computation, the choice of formulation[\s\S]*?(?=\n\n)',summary['en']+' The nonlinear representation, time integrator and node distribution jointly influence the terminal physical-field errors.',source,count=1)
source=source.replace('The computational boundaries are placed where the soliton tails approach their backgrounds. ','').replace('计算域边界选在孤子尾部接近背景的位置。','')
for lang in ['en','zh']:
    marker='**初值与边界数据。**' if lang=='zh' else '**Initial and boundary data.**'
    description=('第二组二孤子取 $(p_1,q_1)=(1,2)$、$(p_2,q_2)=(4,-3)$，此时 $c_1=1/4$、$c_2=2$、$A_{12}=5/4$，相位为 $\\theta_1=3x+3t-3y/4$ 和 $\\theta_2=x-7t-y/2$，其 $u$ 场包含正、负两条波带。' if lang=='zh' else 'The second two-soliton test takes $(p_1,q_1)=(1,2)$ and $(p_2,q_2)=(4,-3)$, with $c_1=1/4$, $c_2=2$ and $A_{12}=5/4$. Its phases are $\\theta_1=3x+3t-3y/4$ and $\\theta_2=x-7t-y/2$, producing positive and negative wave bands in u.')
    caption=('二孤子精确解' if lang=='zh' else 'Exact two-soliton solution')+': (1,2; 4,-3), t=0; u / v; [-30,30]².'
    extra=description+'\n\n<figure><img src="../Workspaces/dlw_paper_20261009/figures/exact_two_soliton_mixed.png" alt="'+caption+'" loading="lazy"><figcaption>'+caption+'</figcaption></figure>\n\n'
    assert marker in source, marker
    source=source.replace(marker,extra+marker,1)
lines=source.splitlines()
for i,line in enumerate(lines):
    if '<figure>' in line and 'exact_single_' in line:
        lines[i]=line.replace('[−20,20]','[−5,5]') if 'exact_single_1_2' in line else line.replace('[−5,5]','[−10,10]').replace('[−20,20]','[−10,10]')
    elif '<figure>' in line and 'exact_two_soliton' in line:
        lines[i]=line.replace('[−20,20]','[−30,30]')
source='\n'.join(lines)+'\n'
source=re.sub(r'The fixed-grid comparison gives[\s\S]*?(?=\n\n)',summary['en'],source)
source=re.sub(r'固定网格下，两组单孤子[\s\S]*?(?=\n\n)',summary['zh'],source)
source=source.replace('**Two-soliton solution.**', '**Two-soliton solutions.**')
source=source.replace('For the two-soliton solution, we take', 'For the first two-soliton test, we take')
source=source.replace('prepare_comparison_fields.py','rerun_unified.py').replace('plot_comparison_fields.py','plot_unified_fields.py').replace('宽域场图','数值场图').replace('expanded-domain','common-domain')
source=source.replace('rerun_unified.py','rerun_buffered.py').replace('plot_unified_fields.py','plot_buffered_fields.py')
(HERE/'manuscript.md').write_text(source,encoding='utf-8')
shutil.copy2(OUT/'tables.json',HERE/'tables.json')
(OUT/'analysis.json').write_text(json.dumps(dict(pf_pe_ratios=ratios,cn_rk4_max_relative_percent=cn,moving_improved=improved,moving_reductions_percent=reductions,summary=summary),ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
