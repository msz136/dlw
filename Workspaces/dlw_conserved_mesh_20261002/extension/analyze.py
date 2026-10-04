"""Report actual physical errors at shared times, keeping failed runs visible."""
from pathlib import Path
import json,csv,hashlib,base64,html
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import baseline

HERE=Path(__file__).resolve().parent
TOPIC=HERE.parent
ROOT=TOPIC.parents[1]
OUTPUT=ROOT/'report/dlw_conserved_mesh.html'
MESHES=['fixed','minus','zero','plus','mass','strong']
LABEL=dict(fixed='均匀固定',minus='负支',zero='平均密度',plus='正支',mass='无背景 −v/4',strong='增强 1−v')
CASES=dict(A='图1(a)',B='图1(b)',C='图3',D='图4',E='图5')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
fmt=lambda v:f'{v:.3e}'

def hist(r,t):return next((h for h in r['history'] if abs(h['t']-t)<1e-12),None)
def key(r):return tuple(r['spec'][k] for k in ['case','model','mesh','motion','variant'])
def motion(mesh):return 'fixed' if mesh=='fixed' else 'moving'
def field(r,t,f):
    with np.load(r['profile']) as a:return a['y'].copy(),a['eval_x'].copy(),a[f't{t:g}_error_{f}'].copy()
def table(head,rows):
    return '<div class="tablewrap"><table><thead><tr>'+''.join('<th scope="col">'+v+'</th>' for v in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def pic(p):
    alt='图1(a)：减半时间步与加密x后的物理u、v误差随时间变化' if p.stem=='growth_time_controls' else f'{CASES[p.stem[-1]]}：T=0.01，固定、无背景、增强密度下SD与FD的u、v有符号误差'
    return '<img src="data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()+'" alt="'+html.escape(alt)+'">'
def status(r,t):
    h=hist(r,t)
    return fmt(h['errors']['u'])+' / '+fmt(h['errors']['v']) if h else f'停止于 {r["reached"]:.5f}'
def csvwrite(name,rows):
    with (HERE/name).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    b=json.loads((HERE/'baseline_out/results.json').read_text(encoding='utf-8'))
    n=json.loads((HERE/'candidate_out/results.json').read_text(encoding='utf-8'))
    runs=b['runs']+n['runs'];look={key(r):r for r in runs}
    assert len(look)==len(runs)==len(b['expected_plan'])+len(n['expected_plan'])
    assert all(r['source_sha256']==sha(HERE/'baseline.py') and r['profile_sha256']==sha(r['profile']) for r in runs)
    assert all(r['candidate_sha256']==sha(HERE/'candidates.py') for r in n['runs'])
    primary=[r for r in runs if r['spec']['variant']=='main' and r['spec']['motion']!='frozen']
    errors,paired,controls,frozen,evaluation=[],[],[],[],[]
    for r in runs:
        for h in r['history']:
            for f in ['u','v']:
                errors.append({**r['spec'],'status':r['status'],'reached':r['reached'],'t':h['t'],'field':f,'max_error':h['errors'][f],'rms_error':h['rms_errors'][f],'nodal_error':h['nodal_errors'][f],'relative_initial_peak':h['relative_initial_peaks'][f]})
    for r in primary:
        s=r['spec'];case,model,mesh,mo=(s[k] for k in ['case','model','mesh','motion'])
        for t in [.001,.002,.005,.01]:
            h=hist(r,t)
            if not h:continue
            fixed=hist(look[(case,model,'fixed','fixed','main')],t)
            fd=hist(look[(case,'FD',mesh,mo,'main')],t)
            for f in ['u','v']:
                E=h['errors'][f]
                paired.append(dict(case=case,model=model,mesh=mesh,t=t,field=f,E=E,ratio_own_uniform=E/fixed['errors'][f] if fixed else None,ratio_same_mesh_FD=E/fd['errors'][f] if fd else None))
                yy,xx,coarse=field(r,t,f)
                for variant in ['time_half','x_half','y_half','combined']:
                    rr=look[(case,model,mesh,mo,variant)];hh=hist(rr,t)
                    delta=None
                    if hh:
                        yf,xf,ef=field(rr,t,f)
                        if len(yf)!=len(yy):ef=CubicSpline(yf,ef,axis=0)(yy)
                        delta=float(abs(coarse-ef).max())
                    controls.append(dict(case=case,model=model,mesh=mesh,t=t,field=f,variant=variant,E=E,delta=delta,fraction=delta/E if delta is not None else None,refined_error=hh['errors'][f] if hh else None,control_status=rr['status'],control_reached=rr['reached']))
            if mesh!='fixed':
                fr=look[(case,model,mesh,'frozen','main')];fh=hist(fr,t)
                if fh:frozen.append(dict(case=case,model=model,mesh=mesh,t=t,moving_u=h['errors']['u'],moving_v=h['errors']['v'],frozen_u=fh['errors']['u'],frozen_v=fh['errors']['v'],ratio_u=h['errors']['u']/fh['errors']['u'],ratio_v=h['errors']['v']/fh['errors']['v'],displacement=h['max_displacement']))
        h=hist(r,.01)
        if h:
            with np.load(r['profile']) as a:
                xx=np.linspace(-1,1,801);ref=baseline.Exact(case).uv(a['y'],xx,.01)
                for f,refa in zip(['u','v'],ref):
                    aup=CubicSpline(a['t0.01_x'],a[f't0.01_{f}'],axis=-1)(xx)
                    E=float(abs(aup-refa).max())
                    evaluation.append(dict(case=case,model=model,mesh=mesh,field=f,E_401=h['errors'][f],E_801=E,relative_change=abs(E-h['errors'][f])/h['errors'][f]))
    for name,rows in [('errors.csv',errors),('paired_errors.csv',paired),('controls.csv',controls),('moving_vs_frozen.csv',frozen),('evaluation.csv',evaluation)]:csvwrite(name,rows)
    summary=dict(total_runs=len(runs),completed=sum(r['status']=='completed' for r in runs),main_total=len(primary),main_completed=sum(hist(r,.01) is not None for r in primary),
        failures=[dict(spec=r['spec'],reached=r['reached'],reason=r['reason']) for r in runs if r['status']!='completed'],
        max_time_fraction=max(c['fraction'] for c in controls if c['variant']=='time_half' and c['fraction'] is not None),
        max_evaluation_change=max(e['relative_change'] for e in evaluation),
        paired=paired,frozen=frozen,source_sha256=sha(HERE/'baseline.py'),candidate_sha256=sha(HERE/'candidates.py'))
    (HERE/'analysis.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # New density errors at the same requested terminal time; stops have no terminal image.
    for case in CASES:
        fig,axes=plt.subplots(3,4,figsize=(13,8),sharex=True,sharey=True,layout='constrained')
        data={}
        for mesh in ['fixed','mass','strong']:
            for model in ['SD','FD']:
                r=look[(case,model,mesh,motion(mesh),'main')]
                if hist(r,.01):
                    for f in ['u','v']:data[(mesh,model,f)]=field(r,.01,f)
        scale={f:max([float(abs(a[2]).max()) for k,a in data.items() if k[2]==f]+[1e-15]) for f in ['u','v']}
        for i,mesh in enumerate(['fixed','mass','strong']):
            for j,(model,f) in enumerate([('SD','u'),('FD','u'),('SD','v'),('FD','v')]):
                ax=axes[i,j];r=look[(case,model,mesh,motion(mesh),'main')]
                if (mesh,model,f) in data:
                    y,x,e=data[(mesh,model,f)]
                    ax.pcolormesh(x,y,e,cmap='RdBu_r',vmin=-scale[f],vmax=scale[f],shading='auto',rasterized=True)
                else:ax.text(.5,.5,f'Stopped at t={r["reached"]:.5f}',ha='center',transform=ax.transAxes)
                ax.set_xlim(-1,1);ax.set_ylim(-1,1)
                if i==0:ax.set_title(f'{model}: {f} error')
                if j==0:ax.set_ylabel(mesh+'\ny')
                if i==2:ax.set_xlabel('x')
        for f,js in [('u',[0,1]),('v',[2,3])]:
            plot=next((ax.collections[0] for ax in axes[:,js].ravel() if ax.collections),None)
            if plot:fig.colorbar(plot,ax=axes[:,js].ravel().tolist(),label=f'{f} error',shrink=.85)
        fig.suptitle(f'Original case {case}; t=0.01; stopped runs are not compared at other times')
        fig.savefig(HERE/f'error_fields_{case}.png',dpi=140);plt.close(fig)
    # An error trajectory contrasts increased spatial resolution with decreased time step.
    fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
    for ax,f in zip(axes,['u','v']):
        for variant,style in [('main','-'),('time_half','--'),('x_half',':')]:
            for model in ['SD','FD']:
                r=look[('A',model,'fixed','fixed',variant)]
                hs=[h for h in r['history'] if h['t']>0]
                ax.semilogy([h['t'] for h in hs],[h['errors'][f] for h in hs],style,marker='o',label=model+' '+variant)
        ax.set_xlabel('t');ax.set_ylabel(f'Max absolute {f} error');ax.grid(alpha=.2);ax.legend(fontsize=8)
    fig.suptitle('Case A: halving time step vs doubling x resolution')
    fig.savefig(HERE/'growth_time_controls.png',dpi=150);plt.close(fig)
    body=['<h1>DLW守恒密度网格：延长到 T=0.01</h1><p class="date">2026年10月2日</p>',
        '<p class="abstract">原文五组参数、x与y均为[−1,1]，时间延长到0.01。追加−v/4与1−v两种守恒密度，未得到数量级的双场改善。图1(a)中，1−v使SD的u、v误差分别增大约19倍、24倍；−v/4使FD误差增大约283倍、201倍。时间步减半几乎不改变结果，而加密x后误差显著增长或运行停止。因此，当前问题已不只是节点分配不足，更是密集网格上的误差放大。</p>',
        '<h2>追加了什么密度</h2>',table(['密度','实际共同网格公式','对应通量','预期作用'],[['原平均','R₀=平均(1−v/4)','Q₀','背景保持均匀分配'],['无背景','R=R₀−1=平均(−v/4)','Q₀','将节点更集中到波区'],['增强','R=1+4(R₀−1)=平均(1−v)','4Q₀','保留正背景，同时增强波区集中']]),
        '<p>它们是同一物理质量守恒律的不同背景与强度选择，不是新的独立守恒量。无背景没有自由系数；增强采用固定公式1−v，在所有算例与网格中共用。实际有限Δy通量分别从SD、FD方程推导，未依据终点误差调参。</p>',
        '<p>实验前初态分析显示：无背景密度的最大/最小值之比，图1(a)为20.65、图4为4.49；其余三组为1.20–1.68。因此预期布点变化主要出现在图1(a)、图4，同时必须检验较小网格间距引入的高频增长。</p>',
        '<h2>比较设置</h2><p>原文图1(a)、图1(b)、图3、图4、图5，全部a=2、cᵢ=1、初相位零，谱参数保持原文。主格33个x节点、Δy=1/8，RK4步长2.5×10⁻⁵；检查时刻0.001、0.002、0.005、0.01。控制包括减半时间步、65个x节点、Δy=1/16及联合加密。各密度另有相同初始网格冻结对照。初值、边界及误差评价沿用短窗实验。</p>',
        table(['原文算例','p','q'],[['图1(a)','1','2'],['图1(b)','4','−3'],['图3','6, 4','−5, −3'],['图4','1, 4','2, −3'],['图5','7/4, 1','−5/3, −4/5']]),
        '<p>x微分采用D₁，二阶微分采用D₁²；内点为四阶，靠近端点的D₁²闭合为三阶。SD与FD使用相同物理初值、固定x端点及y边界闭合；连续精确解只提供初边值与误差参照。</p>',
        '<h2>T=0.01：精确解与数值解的实际差值</h2><p>每格依次列u / v的最大绝对误差，同一401个物理x点及全部y层。数值场通过三次样条重构到这些共同位置，误差包含重构与演化两部分；原始节点误差另行保存。未到0.01的运行显示停止时间，不把较早时刻误差当作终点结果。</p>']
    for case in CASES:
        rows=[]
        for mesh in MESHES:
            rs={m:look[(case,m,mesh,motion(mesh),'main')] for m in ['SD','FD']}
            h=hist(rs['SD'],.01);fixed=hist(look[(case,'SD','fixed','fixed','main')],.01)
            ratio='—' if not h or not fixed else f'{h["errors"]["u"]/fixed["errors"]["u"]:.3f} / {h["errors"]["v"]/fixed["errors"]["v"]:.3f}'
            rows.append([LABEL[mesh],status(rs['SD'],.01),status(rs['FD'],.01),ratio])
        body+=['<h3>'+CASES[case]+'</h3>',table(['网格','SD误差 u / v','FD误差 u / v','SD / 固定SD'],rows)]
    body+=['<p>新增密度在任何一组原文参数上均未实现u、v同时十倍改善。图1(b)、图3的变化较小；图5中无背景密度使两种方法的双场误差约翻倍。图1(a)、图4的强集中则明显增大长期误差。</p>']
    initial=[]
    for mesh in ['fixed','zero','strong','mass']:
        r=look[('A','SD',mesh,motion(mesh),'main')];h=hist(r,0)
        with np.load(r['profile']) as a:dx=np.diff(a['t0_x'])
        initial.append([LABEL[mesh],f'{dx.min():.4f} / {dx.max():.4f}',fmt(h['errors']['u'])+' / '+fmt(h['errors']['v'])])
    body+=['<h2>初始布点损失与演化增长要分开</h2><p>图1(a)的所有初始节点值均匹配同一精确解，误差在舍入量级；但节点之间的场重构已有差别。无背景密度让波尾过稀，初始重构误差已比固定网格大约52倍、225倍。</p>',
        table(['图1(a)初始网格','最小 / 最大单元长','初始重构误差 u / v'],initial),
        '<p>这一损失不能全部归因于后续高频增长。另一方面，无背景FD到0.01的原始节点误差仍达0.523 / 0.648，说明终点失准也不是单纯的样条插值假象。</p>']
    reversal=[]
    for t in [.001,.005,.01]:
        f=hist(look[('A','SD','fixed','fixed','main')],t);s=hist(look[('A','SD','strong','moving','main')],t)
        reversal.append([f'{t:g}',fmt(f['errors']['u'])+' / '+fmt(f['errors']['v']),fmt(s['errors']['u'])+' / '+fmt(s['errors']['v']),f'{s["errors"]["u"]/f["errors"]["u"]:.3f} / {s["errors"]["v"]/f["errors"]["v"]:.3f}'])
    body+=[table(['图1(a)时间','固定SD误差 u / v','增强SD误差 u / v','增强 / 固定'],reversal),
        '<p>增强密度在0.001的短时改善，随后反转为大幅损失。这比终点上的小幅排序更有判断力：减小一部分初始误差，仍可能被更快的演化放大抵消。</p>']
    body+=['<h2>空间加密是否支持终点结论</h2><p>下面列同一密度在65个x节点及同时加密x、y下的结果。停止或误差放大本身是结果；时间减半不能替代空间核验。</p>']
    for case in CASES:
        rows=[]
        for model in ['SD','FD']:
            for mesh in MESHES:
                rows.append([model+' '+LABEL[mesh],status(look[(case,model,mesh,motion(mesh),'x_half')],.01),status(look[(case,model,mesh,motion(mesh),'combined')],.01)])
        body+=['<details><summary>'+CASES[case]+'：加密后的u / v误差及停止时间</summary>',table(['方法','只加密x','同时加密x、y'],rows),'</details>']
    body+=['<p>两种新增密度的全部x加密运行均未到达0.01。联合加密仅图5的增强密度SD/FD到达终点，但其u / v误差分别为0.858 / 0.835及0.0422 / 0.0357，远高于主格。原密度与固定格也出现同类增长；“运行完成”本身不能证明准确。</p>',
        '<h2>为什么较密的网格反而更快失准</h2><p>缩小网格间距能减小差分残差，同时会放行更高的空间频率。当前DLW分支的常背景线性化具有正增长率约κ²的高频模态；它们会将差分截断、舍入和边界闭合产生的小误差指数放大。密度守恒与网格正性没有排除这种放大。</p>',
        '<p>独立线性化检查在图1(a)上给出：固定粗格正增长率约590，加密x后约2250。更小时间步能更准确地解析增长，却不能去掉增长分支。这是支持误差传播机制的诊断，不是对每条非线性轨道的严格误差上界；端点闭合的贡献仍需分开研究。</p>',pic(HERE/'growth_time_controls.png'),
        '<p>独立减步核验中，图1(a)固定粗格T=0.01的误差几乎不变；加密x到T=0.005时u、v误差已接近0.1。这个现象阻止将粗格上的密度排序解释成收敛的长期精度收益。</p>',
        f'<p>全部可配对的时间减半控制中，双场差值不超过原误差的{summary["max_time_fraction"]:.2e}；将物理评价x点由401增至801，最大误差变化不超过{100*summary["max_evaluation_change"]:.3f}%。当前主要失准不能归因于所用时间步或评价点过稀。</p>',
        '<h2>持续移动与初始分配</h2>']
    for case in CASES:
        rows=[]
        for v in frozen:
            if v['case']==case and v['t']==.01:rows.append([v['model']+' '+LABEL[v['mesh']],f'{v["ratio_u"]:.3f} / {v["ratio_v"]:.3f}',fmt(v['displacement'])])
        body+=['<details><summary>'+CASES[case]+'：可配对的移动 / 同初始网格冻结</summary>',table(['方法','误差比 u / v','最大位移'],rows),'</details>']
    body+=['<p>到0.01，持续移动相对于同初始布点冻结的最大降幅约23%，出现在图1(a)的无背景FD；但该运行的终点误差仍为0.537 / 0.651。运动有可观测影响，未抵消初始强集中带来的失准。</p>']
    body+=['<h2>终点误差场</h2><p>下图比较固定、无背景及增强密度的有符号误差，同一算例同一场共用色标。</p>']
    for case in CASES:body+=['<details><summary>'+CASES[case]+'：展开误差场</summary>',pic(HERE/f'error_fields_{case}.png'),'</details>']
    body+=['<h2>还有什么密度值得继续</h2><p>下一条有数学依据的选择，是按初始u、v的曲率给质量加权：让节点感知两场弯曲的位置，而不只感知v的幅值。这个权重随后随质量流动，不逐时按观测误差重选。</p>',
        '<p>若基密度满足R<sub>b,t</sub>+Q<sub>b,x</sub>=0，令c=Q<sub>b</sub>/R<sub>b</sub>，并输运正权重μ：μ<sub>t</sub>+cμ<sub>x</sub>=0。则R=μR<sub>b</sub>、Q=μQ<sub>b</sub>严格满足R<sub>t</sub>+Q<sub>x</sub>=0。初始μ可由两场曲率与各自初态幅值构造，以同一规则用于全部原文算例。</p>',
        '<p>它增加一个被动权重变量，属于扩展系统中的守恒构造；并非仅由当前u、v得到的新独立守恒量。该构造已完成推导与符号核验，尚未做演化实验，也未证明最优性或保留原可积结构。有限端点需要处理权重流入，实际差分需要兼容的守恒通量。直接把当前曲率乘上旧密度、沿用旧通量，不满足这个守恒关系。</p>',
        '<p>下一次实验的关键，是同时检验它是否减小物理场的离散残差、是否增大高频误差传播。固定SD/FD在0.01的空间加密已经失准；须先分清内点增长与端点闭合的贡献，才能判断新密度有无可迁移收益。仅继续提高集中强度没有得到本轮证据支持。</p>',
        '<h2>完整结果与依据</h2><p><a href="Paper/sources/physd.txt">DLW原文</a>；<a href="Paper/sources/gsg.txt">GSG参考文献</a>；<a href="Workspaces/dlw_conserved_mesh_20261002/extension/errors.csv">各时刻实际误差</a>；<a href="Workspaces/dlw_conserved_mesh_20261002/extension/paired_errors.csv">固定网格与FD配对</a>；<a href="Workspaces/dlw_conserved_mesh_20261002/extension/controls.csv">时间与空间控制</a>；<a href="Workspaces/dlw_conserved_mesh_20261002/extension/moving_vs_frozen.csv">移动与冻结</a>；<a href="Workspaces/dlw_conserved_mesh_20261002/extension/theory/NEW_DENSITIES.md">新密度与被动权重推导</a>；<a href="Workspaces/dlw_conserved_mesh_20261002/extension/theory/new_density_validation.json">新增密度独立核验</a>；<a href="Workspaces/dlw_conserved_mesh_20261002/extension/theory/passive_curvature_symbolic.json">被动权重守恒关系核验</a>；<a href="Workspaces/dlw_conserved_mesh_20261002/extension/audit/saved_field_validation.json">原始物理场独立读回</a>；<a href="Workspaces/dlw_conserved_mesh_20261002/extension_diagnostics/NOTES.md">独立高频增长诊断</a>；<a href="Workspaces/dlw_conserved_mesh_20261002/short_time_report.html">先前T=0.001完整报告</a>。</p>']
    style='''*{box-sizing:border-box}body{margin:0;background:#f3f2ef;color:#202020;font:17px/1.85 "Times New Roman","SimSun",serif}main{max-width:1100px;margin:30px auto;background:white;padding:48px 64px}h1{text-align:center;font-size:29px;line-height:1.5;font-weight:600;margin:0}h2{font-size:23px;line-height:1.5;margin:35px 0 12px}h3{font-size:19px;margin:26px 0 10px}.date{text-align:center;color:#666;font-size:14px}.abstract{border-block:1px solid #888;padding:16px 0}p{margin:12px 0}table{border-collapse:collapse;width:100%;font-size:14px;border-block:1.3px solid #555;margin:18px 0}th,td{text-align:left;padding:9px 10px;border-bottom:1px solid #ddd;font-variant-numeric:tabular-nums;white-space:nowrap}th{font-weight:600}tr:last-child td{border:0}.tablewrap{overflow-x:auto}img{display:block;width:100%;height:auto;margin:22px 0}details{border-top:1px solid #ccc;padding:12px 0;margin:12px 0}summary{cursor:pointer;font-weight:600}a{color:#28546f;text-underline-offset:3px}a:focus-visible,summary:focus-visible{outline:2px solid #28546f;outline-offset:4px}@media(max-width:700px){main{margin:0;padding:25px 19px}body{font-size:16px}h1{font-size:24px}h2{font-size:21px}table{font-size:13px}}'''
    doc='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="DLW原文五算例延长到T=.01，新增守恒密度，误差场、失败时间及加密检验"><title>DLW守恒密度网格：T=0.01</title><style>'+style+'</style></head><body><main>'+''.join(body)+'</main></body></html>'
    doc=doc.replace('href="Workspaces/', 'href="../Workspaces/').replace('href="Paper/', 'href="../Paper/')
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    (HERE/'report_source.html').write_text(doc,encoding='utf-8');OUTPUT.write_text(doc,encoding='utf-8')
    manifest=dict(date='2026-10-02',extension_runs=len(runs),baseline_source_sha256=sha(HERE/'baseline.py'),candidate_source_sha256=sha(HERE/'candidates.py'),html_sha256=sha(OUTPUT),analysis_sha256=sha(__file__),
        input_sha256={str(p.relative_to(HERE)):sha(p) for p in [HERE/'baseline_out/results.json',HERE/'candidate_out/results.json',HERE/'BASELINE_PROTOCOL.json',HERE/'CANDIDATE_PROTOCOL.json',HERE/'audit/saved_field_validation.json',HERE/'theory/new_density_validation.json',HERE/'theory/passive_curvature_symbolic.json']},
        outputs_sha256={p.name:sha(p) for p in [HERE/'errors.csv',HERE/'paired_errors.csv',HERE/'controls.csv',HERE/'moving_vs_frozen.csv',HERE/'evaluation.csv',HERE/'analysis.json']})
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:summary[k] for k in ['total_runs','completed','main_total','main_completed','max_time_fraction','max_evaluation_change']},indent=2))

if __name__=='__main__':main()
