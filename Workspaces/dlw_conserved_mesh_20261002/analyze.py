"""Read saved fields, compare controls, and build the research report."""
from pathlib import Path
import json, csv, hashlib, base64, html
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import experiment

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE/'out'
OUTPUT = HERE/'short_time_report.html'
MESHES = ['fixed', 'minus', 'zero', 'plus']
LABEL = dict(fixed='均匀固定', minus='负支 r−', zero='平均 r₀', plus='正支 r+')
CASELABEL = dict(A='单孤子 · 图1(a)', B='单孤子 · 图1(b)', C='二孤子 · 图3', D='二孤子 · 图4', E='二孤子 · 图5')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
fmt = lambda x: f'{x:.3e}'
rat = lambda x: f'{x:.3f}'

def writecsv(name, rows):
    with (OUT/name).open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def key(r):
    return tuple(r['spec'][k] for k in ['case','model','mesh','motion','variant'])

def hist(r, t):
    return next((h for h in r['history'] if abs(h['t']-t)<1e-12), None)

def field(r, t, f):
    with np.load(r['profile']) as a:
        return a['y'].copy(), a['eval_x'].copy(), a[f't{t:g}_error_{f}'].copy()

def pic(path):
    return '<img src="data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode()+'" alt="'+html.escape(path.stem)+'">'

def table(head, rows):
    return '<div class="tablewrap"><table><thead><tr>'+''.join('<th scope="col">'+h+'</th>' for h in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def main():
    d = json.loads((OUT/'results.json').read_text(encoding='utf-8'))
    runs = d['runs']; look = {key(r):r for r in runs}
    assert len(look)==len(runs)==len(d['expected_plan'])
    assert all(r['source_sha256']==sha(HERE/'experiment.py') and r['profile_sha256']==sha(r['profile']) for r in runs)
    primary = [r for r in runs if r['spec']['variant']=='main' and r['spec']['motion']!='frozen']
    pairs, controls, frozen, evaluation, inner = [], [], [], [], []
    for r in primary:
        s=r['spec']; case, model, mesh, motion = (s[k] for k in ['case','model','mesh','motion'])
        h=hist(r,.001)
        if not h: continue
        refs={m:hist(look[(case,m,'fixed','fixed','main')],.001) for m in ['SD','FD']}
        same=hist(look[(case,'FD',mesh,motion,'main')],.001)
        row=dict(case=case, model=model, mesh=mesh, motion=motion)
        for f in ['u','v']:
            row['E_'+f]=h['errors'][f]; row['node_'+f]=h['nodal_errors'][f]
            row['initial_'+f]=hist(r,0)['errors'][f]
            row['ratio_SD_uniform_'+f]=h['errors'][f]/refs['SD']['errors'][f]
            row['ratio_FD_uniform_'+f]=h['errors'][f]/refs['FD']['errors'][f]
            row['ratio_FD_same_mesh_'+f]=h['errors'][f]/same['errors'][f]
        pairs.append(row)
        with np.load(r['profile']) as a:
            xx=np.linspace(-1,1,801); exact=experiment.Exact(case).uv(a['y'],xx,.001)
            for f,b in zip(['u','v'],exact):
                values=CubicSpline(a['t0.001_x'],a[f't0.001_{f}'],axis=-1)(xx)
                err=float(abs(values-b).max()); old=h['errors'][f]
                evaluation.append(dict(case=case,model=model,mesh=mesh,field=f,E_401=old,E_801=err,relative_change=abs(err-old)/old))
                ey=a[f't0.001_error_{f}']; mask=abs(a['y'])<.75
                inner.append(dict(case=case,model=model,mesh=mesh,field=f,full_error=h['errors'][f],inner_error=float(abs(ey[mask]).max())))
        for t in [.0005,.001]:
            ht=hist(r,t)
            if not ht:continue
            for f in ['u','v']:
                yy,xx,coarse=field(r,t,f); values={}
                for variant in ['time_half','x_half','y_half','combined']:
                    rr=look[(case,model,mesh,motion,variant)]
                    if not hist(rr,t):values[variant]=None;continue
                    yf,xf,ef=field(rr,t,f)
                    if len(yf)!=len(yy):ef=CubicSpline(yf,ef,axis=0)(yy)
                    values[variant]=float(abs(coarse-ef).max())
                controls.append(dict(case=case,model=model,mesh=mesh,t=t,field=f,E=ht['errors'][f],
                    delta_dt=values['time_half'],delta_x=values['x_half'],delta_y=values['y_half'],delta_combined=values['combined'],
                    dt_fraction=values['time_half']/ht['errors'][f] if values['time_half'] is not None else None,
                    time_check_passed=values['time_half'] is not None and values['time_half']<=.05*ht['errors'][f]))
        if mesh!='fixed':
            fr=look[(case,model,mesh,'frozen','main')]; fh=hist(fr,.001)
            if fh:
                frozen.append(dict(case=case,model=model,mesh=mesh,moving_u=h['errors']['u'],moving_v=h['errors']['v'],
                    frozen_u=fh['errors']['u'],frozen_v=fh['errors']['v'],ratio_u=h['errors']['u']/fh['errors']['u'],ratio_v=h['errors']['v']/fh['errors']['v'],displacement=h['max_displacement']))
    for name,rows in [('paired_errors.csv',pairs),('control_differences.csv',controls),('moving_vs_frozen.csv',frozen),('evaluation_check.csv',evaluation),('inner_errors.csv',inner)]:writecsv(name,rows)
    summary=dict(runs=len(runs),expected=len(d['expected_plan']),completed=sum(r['status']=='completed' for r in runs),
        failures=[dict(spec=r['spec'],reached=r['reached'],reason=r['reason']) for r in runs if r['status']!='completed'],
        time_checks_passed=sum(c['time_check_passed'] for c in controls),time_checks_total=len(controls),
        max_dt_error_fraction=max(c['dt_fraction'] for c in controls if c['dt_fraction'] is not None),
        max_evaluation_change=max(e['relative_change'] for e in evaluation),
        min_R=min(r['min_R_all_stages'] for r in runs),min_J=min(r['min_J_all_stages'] for r in runs),
        max_mesh_displacement=max(v['displacement'] for v in frozen),
        max_moving_frozen_fractional_difference=max(abs(v['ratio_'+f]-1) for v in frozen for f in ['u','v']),
        comparisons=pairs,frozen=frozen,
        scope='Measured short-time physical-field errors, not a general nonlinear upper-bound theorem.',
        y_control='Only fine error interpolated to coarse y for paired diagnostics; no exact-background forcing in evolution.')
    (HERE/'analysis.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for case in d['parameters']:
        fig,axes=plt.subplots(4,4,figsize=(13,9),sharex=True,sharey=True,layout='constrained')
        data={}
        for mesh in MESHES:
            motion='fixed' if mesh=='fixed' else 'moving'
            for model in ['SD','FD']:
                r=look[(case,model,mesh,motion,'main')]
                if hist(r,.001):
                    for f in ['u','v']:data[(mesh,model,f)]=field(r,.001,f)
        scale={f:max(float(abs(a[2]).max()) for k,a in data.items() if k[2]==f) for f in ['u','v']}
        for i,mesh in enumerate(MESHES):
            for j,(model,f) in enumerate([('SD','u'),('FD','u'),('SD','v'),('FD','v')]):
                ax=axes[i,j]
                if (mesh,model,f) not in data:ax.text(.5,.5,'Stopped',transform=ax.transAxes);continue
                y,x,e=data[(mesh,model,f)]
                ax.pcolormesh(x,y,e,cmap='RdBu_r',vmin=-scale[f],vmax=scale[f],shading='auto',rasterized=True)
                ax.set_xlim(-1,1);ax.set_ylim(-1,1)
                if i==0:ax.set_title(f'{model}: numerical {f} - exact {f}')
                if j==0:ax.set_ylabel(f'{mesh}\ny')
                if i==3:ax.set_xlabel('x')
        for f,js in [('u',[0,1]),('v',[2,3])]:fig.colorbar(axes[0,js[0]].collections[0],ax=axes[:,js].ravel().tolist(),shrink=.85,label=f'{f} error')
        fig.suptitle(f'Original case {case}; t=0.001; same colour scale within each field')
        fig.savefig(HERE/f'error_fields_{case}.png',dpi=140);plt.close(fig)
        fig,axes=plt.subplots(2,3,figsize=(11,6),sharex=True,sharey=True,layout='constrained')
        for i,f in enumerate(['u','v']):
            with np.load(look[(case,'SD','zero','moving','main')]['profile']) as a:
                y,x=a['y'],a['eval_x']; ex=a[f't0.001_eval_exact_{f}'];sd=a[f't0.001_eval_{f}']
            with np.load(look[(case,'FD','zero','moving','main')]['profile']) as a:fd=a[f't0.001_eval_{f}']
            lo=min(b.min() for b in [ex,sd,fd]);hi=max(b.max() for b in [ex,sd,fd])
            for j,(b,title) in enumerate([(ex,'Exact'),(sd,'SD with r0'),(fd,'FD with r0')]):
                im=axes[i,j].pcolormesh(x,y,b,shading='auto',cmap='viridis',vmin=lo,vmax=hi)
                axes[i,j].set_title(title+' '+f);axes[i,j].set_xlabel('x');axes[i,j].set_ylabel('y')
            fig.colorbar(im,ax=axes[i,:].tolist(),shrink=.85)
        fig.suptitle(f'Original case {case}; t=0.001; identical colour scales')
        fig.savefig(HERE/f'physical_fields_{case}.png',dpi=140);plt.close(fig)
    fig,axes=plt.subplots(5,1,figsize=(10,8),sharex=True,layout='constrained')
    for ax,case in zip(axes,d['parameters']):
        for j,mesh in enumerate(MESHES):
            r=look[(case,'SD',mesh,'fixed' if mesh=='fixed' else 'moving','main')]
            with np.load(r['profile']) as z:ax.plot(z['t0_x'],np.zeros_like(z['t0_x'])+j,'|',markersize=11)
        ax.set_ylabel(case);ax.set_yticks(range(4),MESHES);ax.set_xlim(-1,1)
    axes[-1].set_xlabel('Physical x');fig.suptitle('Initial nodes: same count, different conserved densities')
    fig.savefig(HERE/'initial_meshes.png',dpi=140);plt.close(fig)
    body=['<h1>DLW：守恒密度网格的 u、v 误差</h1><p class="date">2026年10月2日</p>',
        '<p class="abstract">三种守恒密度均已实现并完成原文五组算例。当前短窗内没有得到跨分辨率的数量级双场改善：图1(a)、图4在主网格上有部分下降，但空间加密后收益消失或反转；其余三组对密度选择变化较小。持续移动相对同初始网格冻结的误差变化不超过0.24%，此次主要差异来自节点分配。以下直接列出物理u、v的实际误差。</p>',
        '<h2>比较对象</h2>',table(['算例','谱参数 p / q'],[[CASELABEL[k],str(v['p'])+' / '+str(v['q'])] for k,v in d['parameters'].items()]),
        '<p>全部 a=2、cᵢ=1、初相位为零。主网格为33个x节点、16个y中点层，Δy=1/8；RK4步长5×10⁻⁶，观察t=0.0005和0.001。两种方法使用相同物理初值、非周期x解析边界和相同y闭合。密度在固定y∈[−0.75,0.75]带内等权平均；全部y层参与误差评价。</p>',
        '<h2>三种守恒密度</h2>',table(['名称','连续公式','感知内容'],[['负支 r−','1−(v−uᵧ)/4','高度与横向斜率的一侧'],['平均 r₀','1−v/4','两支平均，直接响应高度'],['正支 r+','1−(v+uᵧ)/4','另一侧']]),
        '<p>三者均满足局部守恒律，在五组原文精确解上为正；平均密度是两支组合。实际计算采用δ₀u及各方法真实有限格距修正通量。密度越大，节点越密；节点速度由当前数值场计算。没有拟合密度强度或谱参数。</p>',
        '<p>GSG用√(1+uₓ²)及其守恒通量构造质量坐标。这里采用相同步骤，密度来自DLW方程。有限区间两端固定时，速度包含总质量变化的归一化修正。</p>',pic(HERE/'initial_meshes.png'),
        '<h2>最终物理场误差：t=0.001</h2><p>Eᵤ、Eᵥ分别是在同一401个物理x点、全部y层上的最大绝对误差。每格依次列u / v；比值小于1表示误差较小。</p>']
    for case in d['parameters']:
        rows=[]
        for mesh in MESHES:
            cs={m:next(c for c in pairs if c['case']==case and c['model']==m and c['mesh']==mesh) for m in ['SD','FD']}
            sd=cs['SD'];rows.append([LABEL[mesh]]+[fmt(cs[m]['E_u'])+' / '+fmt(cs[m]['E_v']) for m in ['SD','FD']]+[rat(sd['ratio_SD_uniform_u'])+' / '+rat(sd['ratio_SD_uniform_v']),rat(sd['ratio_FD_same_mesh_u'])+' / '+rat(sd['ratio_FD_same_mesh_v'])])
        body+=['<h3>'+CASELABEL[case]+'</h3>',table(['网格','SD误差 u / v','FD误差 u / v','SD / 固定SD','SD / 同密度FD'],rows)]
    body+=['<p>这些是指定网格与短时间的实测值。空间加密后的变化必须一起看；主表较小不构成跨分辨率优越性结论。</p>']
    refined=[]
    for case in d['parameters']:
        ref=hist(look[(case,'SD','fixed','fixed','combined')],.001)['errors']
        row=[CASELABEL[case],fmt(ref['u'])+' / '+fmt(ref['v'])]
        for mesh in ['minus','zero','plus']:
            e=hist(look[(case,'SD',mesh,'moving','combined')],.001)['errors']
            row.append(rat(e['u']/ref['u'])+' / '+rat(e['v']/ref['v']))
        refined.append(row)
    body+=['<h2>同时加密后，密度收益还在吗</h2><p>x节点增至65、Δy减至1/16、Δt减半。下表以同一细网格的固定SD为基准；没有一组密度在五个原文算例上持续改善两个场。</p>',table(['算例','固定SD误差 u / v','负支 / 固定','平均 / 固定','正支 / 固定'],refined)]
    body+=['<h2>初始评价误差与节点误差</h2><p>初态在节点上直接采样精确u、v，但共同物理评价点需插值，因此初始评价误差非零。以下将它与最终原生节点误差分开列出，避免把插值改善全算成演化改善。</p>']
    for case in d['parameters']:
        rows=[[LABEL[c['mesh']],fmt(c['initial_u'])+' / '+fmt(c['initial_v']),fmt(c['node_u'])+' / '+fmt(c['node_v'])] for c in pairs if c['case']==case and c['model']=='SD']
        body+=['<details><summary>'+CASELABEL[case]+'：SD初始评价与最终节点误差</summary>',table(['网格','t=0评价误差 u / v','t=0.001节点误差 u / v'],rows),'</details>']
    body+=[
        '<h2>可靠性与空间加密</h2>',f'<p>{summary["completed"]}/{summary["runs"]}条轨道完成；全阶段最小密度{summary["min_R"]:.6f}、最小J为{summary["min_J"]:.6f}。时间减半场差的最大占比为{100*summary["max_dt_error_fraction"]:.3g}%；{summary["time_checks_passed"]}/{summary["time_checks_total"]}项不超过主误差5%。评价点401→801时最大误差变化{100*summary["max_evaluation_change"]:.3g}%。</p>',
        '<p>下表δ为主计算与加密计算的实际场差。y加密时，把细网格误差插值到原y层用于对比。δ是分辨率诊断，不是精确误差的严格上界。</p>']
    for case in d['parameters']:
        rows=[]
        for model in ['SD','FD']:
            for mesh in MESHES:
                c={f:next(c for c in controls if c['case']==case and c['model']==model and c['mesh']==mesh and c['t']==.001 and c['field']==f) for f in ['u','v']}
                rows.append([model+' '+LABEL[mesh]]+[fmt(c['u'][k])+' / '+fmt(c['v'][k]) for k in ['delta_dt','delta_x','delta_y','delta_combined']])
        body+=['<details><summary>'+CASELABEL[case]+'：加密场差 u / v</summary>',table(['方法','减半Δt','加密x','加密y','同时加密'],rows),'</details>']
    body+=['<p>横向上边界采用相对解析背景的二次误差外推，使边界误差延拓保持平滑。x差分内点为四阶；单边一阶导数组合成二阶导数后，靠边部分为三阶，故全域四阶精度尚不能声称。</p>',
        '<h2>初始布点与持续移动</h2>',f'<p>与同一初始密度网格随后冻结配对，t=0.001的最大节点位移为{summary["max_mesh_displacement"]:.3e}，移动/冻结的最大误差比偏离1最多{100*summary["max_moving_frozen_fractional_difference"]:.3g}%。这直接检验持续运动的额外作用。初始插值误差另存数据，节点上初始物理场一致。</p>']
    for case in d['parameters']:
        rows=[[v['model']+' '+LABEL[v['mesh']],rat(v['ratio_u'])+' / '+rat(v['ratio_v']),fmt(v['displacement'])] for v in frozen if v['case']==case]
        body+=['<details><summary>'+CASELABEL[case]+'：移动 / 同初始网格冻结</summary>',table(['方法','误差比 u / v','最大位移'],rows),'</details>']
    body+=['<h2>精确场、数值场与误差场</h2><p>物理场图展示精确解及平均密度下的SD/FD解。误差图保留正负号，同一算例的同一场共用色标；数值大小以误差表为准。</p>']
    for case in d['parameters']:
        body+=['<details><summary>'+CASELABEL[case]+'：展开场图</summary>',pic(HERE/f'physical_fields_{case}.png'),pic(HERE/f'error_fields_{case}.png'),'</details>']
    body+=['<h2>如何建立误差估计</h2><p>共享坐标x=X(ξ,t)、J=Xξ&gt;0下，物理导数为J⁻¹∂ξ，数值场演化需加网格速度乘物理导数。误差源包括y离散、映射x差分、边界闭合及时间推进。密度调整改变x的分辨率，无法自动消除其余误差源。</p>',
        '<p>若在所用解类中已证明误差传播界G(t,s)，则可由‖e(t)‖≤G(t,0)‖e(0)‖+∫G(t,s)‖残差(s)‖ds给出物理场上界。本次交付直接可复算的精确解误差与加密诊断；一般非线性传播界仍需独立证明。正密度保障坐标可用，并不单独保障长期准确。</p>',
        '<h2>数据与推导</h2><p><a href="Workspaces/dlw_conserved_mesh_20261002/theory/THEORY.md">密度与修正通量推导</a>；<a href="Workspaces/dlw_conserved_mesh_20261002/out/errors.csv">全部时刻两场误差</a>；<a href="Workspaces/dlw_conserved_mesh_20261002/out/paired_errors.csv">固定网格与FD配对</a>；<a href="Workspaces/dlw_conserved_mesh_20261002/out/control_differences.csv">加密场差</a>；<a href="Workspaces/dlw_conserved_mesh_20261002/out/moving_vs_frozen.csv">移动与冻结</a>；<a href="Workspaces/dlw_conserved_mesh_20261002/independent_validation.json">独立核验</a>。</p>']
    style='''*{box-sizing:border-box}body{margin:0;background:#f3f2ef;color:#202020;font:17px/1.85 "Times New Roman","SimSun",serif}main{max-width:1100px;margin:30px auto;background:white;padding:48px 64px}h1{text-align:center;font-size:29px;line-height:1.5;font-weight:600;margin:0}h2{font-size:23px;line-height:1.5;margin:35px 0 12px}h3{font-size:19px;margin:26px 0 10px}.date{text-align:center;color:#666;font-size:14px}.abstract{border-block:1px solid #888;padding:16px 0}p{margin:12px 0}table{border-collapse:collapse;width:100%;font-size:14px;border-block:1.3px solid #555;margin:18px 0}th,td{text-align:left;padding:9px 10px;border-bottom:1px solid #ddd;font-variant-numeric:tabular-nums;white-space:nowrap}th{font-weight:600}tr:last-child td{border:0}.tablewrap{overflow-x:auto}img{display:block;width:100%;height:auto;margin:22px 0}details{border-top:1px solid #ccc;padding:12px 0;margin:12px 0}summary{cursor:pointer;font-weight:600}a{color:#28546f;text-underline-offset:3px}a:focus-visible,summary:focus-visible{outline:2px solid #28546f;outline-offset:4px}@media(max-width:700px){main{margin:0;padding:25px 19px}body{font-size:16px}h1{font-size:24px}h2{font-size:21px}table{font-size:13px}}@media print{body{background:white;font-size:11pt}main{margin:0;padding:0}a{color:inherit}}'''
    document='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="原文五组DLW孤子的守恒密度动网格、固定网格与FD物理u/v误差"><title>DLW：守恒密度网格的u/v误差</title><style>'+style+'</style></head><body><main>'+''.join(body)+'</main></body></html>'
    document=document.replace('href="Workspaces/', 'href="../../Workspaces/')
    (HERE/'report_source.html').write_text(document,encoding='utf-8');OUTPUT.write_text(document,encoding='utf-8')
    manifest=dict(date='2026-10-02',runs=len(runs),source_sha256=sha(HERE/'experiment.py'),analysis_sha256=sha(__file__),results_sha256=sha(OUT/'results.json'),report_sha256=sha(OUTPUT),new_pde_runs=len(runs),archived_prior_runs=230)
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:summary[k] for k in ['runs','completed','time_checks_passed','time_checks_total','max_dt_error_fraction','max_evaluation_change','min_R','min_J','max_mesh_displacement','max_moving_frozen_fractional_difference']},indent=2))

if __name__=='__main__':main()
