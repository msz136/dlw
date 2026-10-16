"""Reorganize the paper using completed buffered runs; no PDE time stepping."""
from pathlib import Path
import json, shutil, re, hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'results_revision';OUT.mkdir(exist_ok=True)
BEFORE=OUT/'before';BEFORE.mkdir(exist_ok=True)
FIG=HERE/'figures';DATA=HERE/'buffered_run'
for p in [HERE/'manuscript.md',ROOT/'report/dlw_paper_draft.html',ROOT/'PROGRESS_LOG.md',ROOT/'FILE_INDEX.md']:
    if not (BEFORE/p.name).exists():shutil.copy2(p,BEFORE/p.name)
nbpath=ROOT/'notebook/DLW数值分析report.ipynb'
protected={str(nbpath):hashlib.sha256(nbpath.read_bytes()).hexdigest()}
records=json.loads((DATA/'results.json').read_text(encoding='utf8'))
lookup={(r['case'],r['model'],r['method'],r['mesh']):r for r in records}
nb=json.loads(nbpath.read_text(encoding='utf8'));cells={c['id']:''.join(c['source']) for c in nb['cells']}
ns={}
for key in ['imports','config','reference','spatial','sd_fd','sd','sd2_lift','sd2_evolution','fd','mesh']:
    exec(cells['dlw-'+key].replace('from IPython.display import display','display=lambda *a,**k:None'),ns)

NAMES={'A':('One-soliton (1, 2)','单孤子 (1, 2)'), 'B':('One-soliton (4, −3)','单孤子 (4, −3)'),
       'C':('Two-soliton (6, −5; 4, −3)','二孤子 (6, −5; 4, −3)'), 'D':('Two-soliton (1, 2; 4, −3)','二孤子 (1, 2; 4, −3)')}
TITLES=['One-soliton\n$(1,2)$','One-soliton\n$(4,-3)$','Two-soliton\n$(6,-5;\\,4,-3)$','Two-soliton\n$(1,2;\\,4,-3)$']
checks=[];profiles={}
for case in 'ABCD':
    with np.load(DATA/f'{case}_SD_RK4_fixed.npz') as cache:
        x=cache['x'];y=cache['y'];exact=[cache['exact_u'],cache['exact_v']]
    out={'x':x}
    for method,mesh in [('Euler','fixed'),('RK4','fixed'),('CN','fixed'),('RK4','moving')]:
        r=lookup[case,'SD',method,mesh];p=ns['Problem'](case,'SD',mesh,r['config'])
        with np.load(DATA/f'{case}_SD_{method}_{mesh}_state.npz') as d:
            state=d['state'];savedx=d['x']
        native=p.fields(state,r['reached'])
        assert np.allclose(p.X.x,savedx,rtol=0,atol=1e-13)
        assert x[0]>=p.X.x[0] and x[-1]<=p.X.x[-1]
        mask=abs(p.m.y)<r['config']['eval_yhalf']
        assert np.array_equal(p.m.y[mask],y)
        for field,z,ex in zip('uv',native,exact):
            sampled=CubicSpline(p.X.x,z[mask],axis=-1,extrapolate=False)(x)
            envelope=np.max(abs(sampled-ex),axis=0)
            err=float(envelope.max());ref=r['max_errors'][field]
            assert np.isclose(err,ref,rtol=2e-10,atol=2e-13),(case,method,mesh,field,err,ref)
            out[f'{method}_{mesh}_{field}']=envelope
            checks.append(dict(case=case,method=method,mesh=mesh,field=field,max_error=err,saved_error=ref))
        if mesh=='moving':
            out['mesh_x']=(p.X.x[1:]+p.X.x[:-1])/2
            out['mesh_spacing']=np.diff(p.X.x)
        del native,state,p
    profiles[case]=out
    np.savez_compressed(OUT/f'{case}_profiles.npz',**out)
    print('Verified saved PE profiles: '+case,flush=True)

plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':11,
 'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.7,'savefig.facecolor':'white'})
def save(fig,stem):
    fig.savefig(FIG/(stem+'.png'),dpi=300,bbox_inches='tight')
    fig.savefig(FIG/(stem+'.pdf'),bbox_inches='tight')
    plt.close(fig)
    (FIG/(stem+'.py')).write_text("from pathlib import Path\nimport runpy\nrunpy.run_path(str(Path(__file__).resolve().parents[1]/'plot_result_profiles.py'),run_name='__main__')\n",encoding='utf8')

# Same method colors and aligned small multiples, inspired by gallery
# oa-bio-plos-pcbi-1007396-f04; no decorative icons or aggregate score inset.
fig,axs=plt.subplots(2,4,figsize=(12,6.1),layout='constrained')
for col,case in enumerate('ABCD'):
    d=profiles[case]
    for row,field in enumerate('uv'):
        ax=axs[row,col]
        for method,color,ls in [('Euler','#d47b19','-'),('RK4','#1776bc','-'),('CN','#282828','--')]:
            ax.plot(d['x'],d[f'{method}_fixed_{field}'],color=color,ls=ls,lw=1.25,label=method.replace('CN','C–N'))
        ax.set_xlim(d['x'][[0,-1]]);ax.set_ylim(bottom=0)
        ax.ticklabel_format(axis='y',style='sci',scilimits=(0,0),useMathText=True)
        ax.set_ylabel(r'$\\max_j |e_'+field+r'(x,y_j,T)|$')
        ax.set_title(f'({chr(97+row*4+col)}) '+(TITLES[col] if row==0 else '$v$'))
        ax.set_xlabel('$x$');ax.grid(alpha=.15)
fig.legend(*axs[0,0].get_legend_handles_labels(),loc='outside upper center',ncol=3,frameon=False)
save(fig,'PE_time_profiles')

fig,axs=plt.subplots(3,4,figsize=(12,8.5),layout='constrained')
for col,case in enumerate('ABCD'):
    d=profiles[case];ax=axs[0,col]
    ax.axhline(.1,color='#777777',ls='--',lw=1.2,label='Fixed mesh')
    ax.plot(d['mesh_x'],d['mesh_spacing'],color='#1776bc',lw=1.4,label='Moving mesh')
    ax.set_ylabel(r'$x_{i+1}-x_i$');ax.set_title(f'({chr(97+col)}) '+TITLES[col]);ax.set_xlim(d['x'][[0,-1]])
    for row,field in enumerate('uv',1):
        ax=axs[row,col]
        for mesh,color,ls in [('fixed','#777777','--'),('moving','#1776bc','-')]:
            ax.plot(d['x'],d[f'RK4_{mesh}_{field}'],color=color,ls=ls,lw=1.3)
        ax.set_xlim(d['x'][[0,-1]]);ax.set_ylim(bottom=0)
        ax.ticklabel_format(axis='y',style='sci',scilimits=(0,0),useMathText=True)
        ax.set_ylabel(r'$\\max_j |e_'+field+r'(x,y_j,T)|$');ax.set_title(f'({chr(97+row*4+col)}) ${field}$')
    for ax in axs[:,col]:ax.set_xlabel('$x$');ax.grid(alpha=.15)
fig.legend(*axs[0,0].get_legend_handles_labels(),loc='outside upper center',ncol=2,frameon=False)
save(fig,'PE_mesh_profiles')

def err(case,model='SD',method='RK4',mesh='fixed',field='u'):
    return lookup[case,model,method,mesh]['max_errors'][field]
time_diff=max(abs(err(c,method='CN',field=f)/err(c,field=f)-1)*100 for c in 'ABCD' for f in 'uv')
reduction=[(1-err(c,mesh='moving',field=f)/err(c,field=f))*100 for c in 'ABCD' for f in 'uv']

def table(which,zh):
    heads=([('算例' if zh else 'Test'),'PE: U / V','PF: U / V','FD: U / V'] if which==1 else
           [('算例' if zh else 'Test'),'Euler: U / V','RK4: U / V','C–N: U / V'] if which==2 else
           [('算例' if zh else 'Test'),('固定网格：U / V' if zh else 'Fixed mesh: U / V'),('动网格：U / V' if zh else 'Moving mesh: U / V')])
    html='<div class="table-wrap"><table class="comparison compact-results"><thead><tr>'+''.join('<th>'+h+'</th>' for h in heads)+'</tr></thead><tbody>'
    for case in 'ABCD':
        values=([[err(case,model=m,field=f) for f in 'uv'] for m in ['SD','SD2','FD']] if which==1 else
                [[err(case,method=m,field=f) for f in 'uv'] for m in ['Euler','RK4','CN']] if which==2 else
                [[err(case,mesh=m,field=f) for f in 'uv'] for m in ['fixed','moving']])
        minima=np.min(values,axis=0)
        html+='<tr><th>'+NAMES[case][int(zh)]+'</th>'
        for pair in values:
            v=[('<strong>'+f'{val:.6e}'+'</strong>') if val==minima[i] else f'{val:.6e}' for i,val in enumerate(pair)]
            html+='<td>'+' / '.join(v)+'</td>'
        html+='</tr>'
    return html+'</tbody></table></div>'

def figure(stem,caption):
    url='../Workspaces/dlw_paper_20261009/figures/'+stem+'.png'
    return f'<figure><a href="{url}"><img src="{url}" alt="{stem.replace("_"," ")}" loading="lazy"></a><figcaption>{caption}</figcaption></figure>'

source=(BEFORE/'manuscript.md').read_text(encoding='utf8')
for lang in ['en','zh']:
    zh=lang=='zh';a=source.index('### 3.5 ',source.index('{#'+lang+'-tests}'));b=source.index('## 4. ',a)
    old=source[a:b];figs=re.findall(r'<figure>[\s\S]*?</figure>',old);assert len(figs)==8
    chunks=['### 3.5 '+('数值结果' if zh else 'Numerical results')+' {#'+lang+'-results}']
    chunks += [
     '本节依次考察空间离散、时间推进与网格配置对计算结果的影响。首先在固定网格上比较 PE、PF 与 FD 的波形和误差；随后以 PE 为统一空间方法，分别改变时间算法与网格配置。后一安排使两组比较共享同一非线性表示，便于区分时间推进和节点重分布的作用。各表每格按 U / V 列出两个物理场的最大绝对误差，并分别加粗同一算例、同一物理场的最小值。' if zh else
     'We examine the effects of spatial discretization, time integration and mesh placement in turn. The fixed-grid study first compares the profiles and errors of PE, PF and FD. We then use PE throughout the time-integration and mesh studies, so that these comparisons share a common nonlinear formulation. In every table, each entry lists the maximum absolute errors as U / V; minima are bold separately for each field and test.',
     '#### 3.5.1 '+('空间离散的比较' if zh else 'Comparison of spatial discretizations')+' {#'+lang+'-spatial-results}',
     '在四组孤子算例中，我们用相同的固定网格与 RK4 推进三种空间离散，考察非线性表示及其实现对物理场的影响。取 $\\Delta x=h=0.1$、$\\Delta t=10^{-4}$、$T=0.01$。表 1 概括最大绝对误差，图 1—8 展示对应波形与误差分布；同一物理量在三种方法中采用共同色阶与高度范围。' if zh else
     'For each of the four soliton tests, we advance all three spatial discretizations on the same fixed grid with RK4. This comparison examines how the nonlinear formulation and its implementation affect the reconstructed fields. We use $\\Delta x=h=0.1$, $\\Delta t=10^{-4}$ and $T=0.01$. Table 1 summarizes the maximum absolute errors, while Figures 1–8 show the corresponding profiles and error distributions with common colour and height scales across methods.',
     '**'+('表 1　固定网格上三种空间离散的最大绝对误差（U / V），RK4。' if zh else 'Table 1. Maximum absolute errors (U / V) for the three spatial discretizations on the fixed grid, using RK4.')+'**',table(1,zh),
     'PE 与 FD 的相对精度随物理场及孤子参数而变：PE 在第二组单孤子和第一组二孤子的 U 场上误差较小，FD 在其余比较中较小。PF 在四组算例中的 U、V 误差均高于 PE。这说明，由相同半离散结构得到的非线性表示，在进一步作空间与时间离散后仍可产生不同的误差；选择演化变量也是数值实现的一部分。下面的场图用于查看这些差异在空间中的分布。' if zh else
     'The relative accuracy of PE and FD depends on the field and soliton parameters: PE gives the smaller U error for the second one-soliton and first two-soliton tests, while FD gives the smaller error in the remaining comparisons. PF has larger U and V errors than PE in all four tests. Thus, nonlinear formulations derived from the same semi-discrete structure can produce different errors after further spatial and temporal discretization. The choice of evolution variables matters in the numerical implementation. The following plots locate these differences within the physical fields.'
    ]
    texts_zh=['第一组单孤子的两个场均为斜向负脉冲。图 1、2 将波形再现与局部误差并列展示，便于判断可见波形的一致程度是否反映实际精度。',
    '第二组单孤子的 U 为正脉冲、V 为负脉冲。图 3、4 分别显示数值波形和误差；这一算例中 PF 的 V 误差明显高于另外两种方法，说明仅观察数值曲面不足以区分重构精度。',
    '第一组二孤子包含两条不同取向的波带。图 5、6 同时覆盖相互作用区和分离分支，用于检查三种方法在二维波形不同区域中的误差分布。',
    '第二组二孤子组合了一正一负的 U 波带。图 7、8 将该复合结构纳入相同的比较，使单孤子观察能够与更复杂的波形相对照。']
    texts_en=['Both fields in the first one-soliton test are negative oblique pulses. Figures 1 and 2 show the profiles and local errors together, allowing visual agreement of the profiles to be assessed against their actual accuracy.',
    'The second one-soliton test has a positive U pulse and a negative V pulse. Figures 3 and 4 show the profiles and errors, respectively. The larger V error of PF in this test illustrates why field surfaces alone do not distinguish reconstruction accuracy.',
    'The first two-soliton test contains two differently oriented wave bands. Figures 5 and 6 include both their interaction region and separated branches, showing how the errors are distributed over different parts of the two-dimensional profile.',
    'The second two-soliton test combines positive and negative U wave bands. Figures 7 and 8 extend the same comparison to this composite structure, providing a counterpart to the one-soliton observations.']
    for i,c in enumerate('ABCD'):
        chunks+=['**'+NAMES[c][int(zh)]+'**',(texts_zh if zh else texts_en)[i],figs[2*i],figs[2*i+1]]
    chunks += [
     '综合表 1 与图 1—8，三种实现的差别需要在物理场重构后的误差中判断，单个波形图或单个场的排名都不足以代表整个方法。当前网格上，PE 相比 PF 给出一致较小的误差，并在部分 U 场比较中优于 FD；因此后续采用 PE 研究时间推进与网格配置，同时保留 FD 作为空间精度的参照。' if zh else
     'Taken together, Table 1 and Figures 1–8 show that the implementations should be assessed through errors in the reconstructed physical fields; neither a profile plot nor a ranking for one field represents the whole method. At the present resolution, PE consistently improves on PF and outperforms FD in some U comparisons. We therefore retain PE for the time-integration and mesh studies, with FD serving as a spatial-accuracy reference.',
     '#### 3.5.2 '+('PE 的时间推进比较' if zh else 'Time integration of PE')+' {#'+lang+'-time-results}',
     '为考察时间推进对同一空间离散的影响，我们在固定网格上用 Euler、RK4 和 C–N 推进 PE。四组算例均保持 $\\Delta x=h=0.1$、$\\Delta t=10^{-4}$、$T=0.01$。表 2 给出两个场的终止误差，图 9 沿 x 展示各位置上对内部 y 层取最大值的绝对误差，即 $\\max_j|e_U(x,y_j,T)|$ 和 $\\max_j|e_V(x,y_j,T)|$。该剖面保留局部误差的位置，其全局最大值与表中误差一致。' if zh else
     'To examine time integration with the spatial discretization held fixed, we advance PE with Euler, RK4 and C–N on the fixed grid. All four tests use $\\Delta x=h=0.1$, $\\Delta t=10^{-4}$ and $T=0.01$. Table 2 gives the terminal errors in both fields. Figure 9 plots the absolute-error envelopes $\\max_j|e_U(x,y_j,T)|$ and $\\max_j|e_V(x,y_j,T)|$ over the interior y layers. These profiles retain the locations of local errors, and their global maxima equal the tabulated errors.',
     '**'+('表 2　固定 PE 空间离散的时间算法比较：最大绝对误差（U / V）。' if zh else 'Table 2. Time-integrator comparison for the fixed PE spatial discretization: maximum absolute errors (U / V).')+'**',table(2,zh),
     figure('PE_time_profiles',('图 9　PE 时间算法的绝对误差剖面。四列依次为两组单孤子和两组二孤子，上、下行为 U、V。对每个 x 取内部 y 层的最大绝对误差。固定网格，Δx=h=0.1，Δt=10⁻⁴，T=0.01；RK4 与 C–N 曲线几乎重合。' if zh else 'Figure 9. Absolute-error envelopes for PE time integration. Columns show the two one-soliton tests followed by the two two-soliton tests; rows show U and V. Each envelope takes the maximum over interior y layers at each x. Fixed grid, Δx=h=0.1, Δt=10⁻⁴, T=0.01. RK4 and C–N nearly overlap.')),
     (f'RK4 与 C–N 的误差剖面几乎重合，八项最大误差的相对差异均不超过 {time_diff:.4f}%（以 RK4 为基准）。Euler 在第二组单孤子和第一组二孤子的 V 场上产生较明显的误差增加，但在另外一些比较中终止误差略小。这里度量的是相对于连续精确解的总误差，空间与时间误差可能相互抵消，因此某个终点误差较小不能单独说明时间方法更准确。' if zh else
     f'The RK4 and C–N error profiles nearly coincide, and their eight maximum errors differ by at most {time_diff:.4f}% relative to RK4. Euler increases the V error more noticeably in the second one-soliton and first two-soliton tests, but gives a slightly smaller terminal error in some other comparisons. These are total errors relative to the continuous exact solution, so spatial and temporal contributions may offset one another; a smaller terminal error alone does not establish a more accurate time integrator.'),
     '该比较表明，在当前步长与时间区间内，用 C–N 替换 RK4 对 PE 的观测精度影响很小。后续网格实验统一采用 RK4，以保持时间推进不变，将比较集中于节点配置的作用。' if zh else
     'At the present step sizes and time interval, replacing RK4 by C–N has little effect on the observed PE accuracy. We use RK4 throughout the mesh experiment to keep time integration unchanged and focus the comparison on node placement.',
     '#### 3.5.3 '+('PE 的固定网格与动网格比较' if zh else 'Fixed and moving meshes for PE')+' {#'+lang+'-mesh-results}',
     '本组实验考察在节点数不变时，沿 x 重分布节点能否改善 PE 的计算精度。固定与动网格分别使用 200、400、800、800 个 x 节点和相同数量的 y 层；四组算例的计算域依次为 $[-10,10]^2$、$[-20,20]^2$、$[-40,40]^2$、$[-40,40]^2$。y 间距保持 $h=0.1$，两种网格均用 RK4、$\\Delta t=10^{-4}$ 推进到 $T=0.01$。误差区域依次为 $[-5,5]^2$、$[-10,10]^2$、$[-30,30]^2$、$[-30,30]^2$。动网格由守恒密度的 y 平均值控制，各 y 层共享同一组 x 节点。' if zh else
     'We next examine whether redistributing x nodes improves PE accuracy without increasing their number. The four tests use 200, 400, 800 and 800 x nodes, with the same respective numbers of y layers, on $[-10,10]^2$, $[-20,20]^2$, $[-40,40]^2$ and $[-40,40]^2$. The y spacing remains $h=0.1$. Both mesh configurations use RK4 with $\\Delta t=10^{-4}$ up to $T=0.01$. Errors are evaluated on $[-5,5]^2$, $[-10,10]^2$, $[-30,30]^2$ and $[-30,30]^2$, respectively. The moving mesh is driven by the y-averaged conservation density, with a common set of x nodes for all y layers.',
     '**'+('表 3　PE 在固定与动网格上的最大绝对误差（U / V），RK4。' if zh else 'Table 3. Maximum absolute errors (U / V) of PE on fixed and moving meshes, using RK4.')+'**',table(3,zh),
     figure('PE_mesh_profiles',('图 10　PE 的节点间距与误差剖面。四列的算例顺序与图 9 相同；第一行给出 T=0.01 时的实际 x 节点间距，以相邻节点中点为横坐标，虚线为固定间距 0.1；第二、三行分别为 U、V 的最大 y 向绝对误差剖面。两种网格使用相同节点数、RK4 和 Δt=10⁻⁴。' if zh else 'Figure 10. Node spacings and error envelopes for PE. Test ordering is the same as in Figure 9. The first row shows physical x spacings at T=0.01, located at cell midpoints; the dashed line is the fixed spacing 0.1. The next two rows show U and V absolute errors maximized over interior y layers. Both meshes use the same node counts, RK4 and Δt=10⁻⁴.')),
     (f'图 10 将节点配置与误差放在同一 x 坐标下比较。动网格在保持 y 分辨率和总节点数不变的同时调整 x 分辨率，使四组算例的两个场均得到较小的最大误差；相对降幅为 {min(reduction):.2f}%—{max(reduction):.2f}%。这一改善来自所采用的初始非均匀配置及其后续运动的共同作用。由于监测密度经过 y 平均，所选方法沿 x 分配分辨率，而不对每条孤子波带独立加密。' if zh else
     f'Figure 10 places node spacing and error on the same x coordinate. The moving mesh adjusts x resolution while retaining the y resolution and total node count, reducing both field errors in all four tests by {min(reduction):.2f}%–{max(reduction):.2f}%. This gain reflects the combined effect of the initial nonuniform mesh and its subsequent motion. Because the monitor is averaged over y, the method allocates resolution along x rather than refining each soliton band independently.'),
     '因此，节点重分布在这些算例中提供了提高 PE 精度的另一种途径，其收益随波形和物理场而变。综合三组比较，空间表示、时间推进和节点配置应分别评价：前者决定当前分辨率下的主要方法差异，RK4 与 C–N 给出接近的结果，而密度驱动的 x 节点重分布在相同自由度下进一步降低误差。这些观察为本节所采用的 PE–RK4 动网格实现提供了数值依据。' if zh else
     'Node redistribution therefore provides an additional way to improve PE accuracy in these tests, with gains that depend on the profile and physical field. Across the three studies, the spatial formulation, time integrator and mesh placement have distinct effects: the formulation produces the larger method differences at the current resolution, RK4 and C–N give similar results, and density-driven x-node redistribution further reduces errors at the same number of degrees of freedom. These observations support the PE–RK4 moving-mesh implementation used here.'
    ]
    source=source[:a]+'\n\n'.join(chunks)+'\n\n'+source[b:]

# Replace result inventories in the abstract/conclusion by the scoped findings now presented.
old_en='The fixed-grid comparison gives PF-to-PE u-error ratios of 4.78, 5.68, 2.11, 6.48 for the four tests, respectively. The largest relative difference between RK4 and C–N terminal errors is 0.0599%. The moving mesh lowers 24 of the twenty-four field errors; the percentage changes, measured as reductions relative to the corresponding fixed-grid errors, range from 0.469% to 20.7%.'
new_en='At the tested resolution, PE gives smaller physical-field errors than PF, while its relative accuracy against direct differences depends on the field and soliton parameters. For PE, RK4 and C–N give nearly identical terminal errors, and density-driven redistribution of x nodes reduces both field errors in all four tests at unchanged node counts.'
old_zh='固定网格下，两组单孤子和两组二孤子的 PF 与 PE 的 u 误差比分别为 4.78、5.68、2.11、6.48。RK4 与 C–N 终止误差的最大相对差异为 0.0599%。动网格使二十四组物理场比较中的 24 组误差降低；以对应固定网格误差为基准，降幅范围为 0.469% 至 20.7%。'
new_zh='在所测试的分辨率下，PE 的物理场误差小于 PF，而其与直接差分的相对精度随物理场及孤子参数而变。对 PE，RK4 与 C–N 给出几乎一致的终止误差；密度驱动的 x 节点重分布在保持节点数不变时，降低了四组算例中两个物理场的误差。'
assert source.count(old_en)==2 and source.count(old_zh)==2
source=source.replace(old_en,new_en).replace(old_zh,new_zh)
source=source.replace('The common-domain comparisons additionally use the [field preparation script]', 'The PE time and mesh profiles are reproduced by the [profile plotting script](../Workspaces/dlw_paper_20261009/plot_result_profiles.py). The common-domain comparisons additionally use the [field preparation script]')
source=source.replace('三种方法的数值场图另附','PE 时间算法与网格比较图另附[误差剖面绘图程序](../Workspaces/dlw_paper_20261009/plot_result_profiles.py)。三种方法的数值场图另附')
(HERE/'manuscript.md').write_text(source,encoding='utf8')
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in protected.items())
(OUT/'validation.json').write_text(json.dumps(dict(no_time_stepping=True,checks=checks,pe_time_max_relative_percent=time_diff,pe_mesh_reduction_percent=reduction,protected_sha256=protected,plot_design='Aligned small multiples; fixed method colours and line styles; source gallery oa-bio-plos-pcbi-1007396-f04; no simulated data'),indent=2),encoding='utf8')
print('Reorganized bilingual results; PE time difference',time_diff,'mesh reductions',reduction)
