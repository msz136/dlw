"""Build the submission report from one published parameter point."""
from pathlib import Path
import base64,hashlib,html,json,re,subprocess,sys
import numpy as np
import markdown
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[2]/'Workspaces/hs_four_schemes_20260927/paper_point'
OUT=HERE/'submission_report';OUT.mkdir(exist_ok=True)

def exact(xx,t=.5):
    lo=xx+.5-.3;hi=xx+.5+.3
    for _ in range(60):
        X=(lo+hi)/2;z=np.tanh((3.75*X-.6*t)/2);v=X-.5+.3*z
        lo=np.where(v<xx,X,lo);hi=np.where(v>=xx,X,hi)
    z=np.tanh((3.75*(lo+hi)/2-.6*t)/2)
    return (.09*(1-z*z),16/(25-9*z*z))

def main():
    subprocess.run([sys.executable,str(HERE/'generate_two_soliton_section.py')],check=True)
    d=json.loads((SOURCE/'results.json').read_text());xx=np.linspace(-1,1,32001);t=.5
    ref=exact(xx,t)
    original_x=np.linspace(-2.5,1.5,32001);original_ref=exact(original_x,t)
    metrics={}
    plt.rcParams.update({'font.family':'DejaVu Serif','font.size':11})
    fig,ax=plt.subplots(figsize=(7.2,4.5),layout='constrained')
    table=['| 空间方案 | $E_u$ | $E_\\rho$ |','|---|---:|---:|'];maximum=0
    for scheme,title,label,color,style in [('S1','可积半离散（Integrable）','Integrable','#994455','--'),('S4','中心差分（FD）','FD','#276ba5',':')]:
        r=d['rows'][f'{scheme}_rk4_0.003125'];path=Path(r['profile']);assert hashlib.sha256(path.read_bytes()).hexdigest()==r['sha256']
        with np.load(path) as a:
            e={}
            for i,f in enumerate(('u','rho')):
                x=a['t0.5_'+('x' if f=='u' else 'rho_x')];value=np.interp(xx,x,a['t0.5_'+f]);err=abs(value-ref[i])
                old_error=float(abs(np.interp(original_x,x,a['t0.5_'+f])-original_ref[i]).max())
                delta=abs(old_error-r['metrics']['0.5']['32001'][f]);maximum=max(maximum,delta);assert delta<1e-12
                assert x[0]<=-1 and x[-1]>=1
                e[f]=float(err.max())
                if f=='rho':
                    # Plot local maxima, not densely connected reconstruction ripples.
                    # 100 disjoint bins cover [-1,1], preserving its maximum.
                    bins=np.minimum(np.floor((xx-xx[0])/.02).astype(int),99)
                    envelope=np.array([err[bins==k].max() for k in range(100)])
                    centers=xx[0]+(np.arange(100)+.5)*.02
                    assert envelope.max()==err.max()
                    ax.semilogy(centers,np.maximum(envelope,1e-16),color=color,ls=style,lw=.9,label=label)
            metrics[scheme]=e;table.append(f'| {title} | {e["u"]:.4e} | {e["rho"]:.4e} |')
    ax.set(xlabel='x',ylabel=r'Local maximum of $|\rho_h-\rho|$',xlim=(-1,1),ylim=(1e-10,1e-2))
    ax.grid(alpha=.15);ax.legend(fontsize=10)
    for ext in ('png','pdf'):fig.savefig(OUT/f'paper_point_rho.{ext}',dpi=200)
    plt.close(fig)
    src=(HERE/'_src/Report.md').read_text(encoding='utf-8').replace('<!-- POINT_TABLE -->','\n'.join(table))
    two=json.loads((OUT/'two_soliton_summary.json').read_text(encoding='utf-8'))
    src=src.replace('<!-- TWO_SOLITON_TABLE -->',two['table'])
    src=src.replace('<!-- TWO_SOLITON_COMPARISON -->',two['comparison'])
    two_b64=base64.b64encode((OUT/'two_soliton_error.png').read_bytes()).decode('ascii')
    src=src.replace('<!-- TWO_SOLITON_FIGURE -->',f'<figure><img src="data:image/png;base64,{two_b64}" alt="二孤子在t=0.5时的密度误差分布"><figcaption>图 2　二孤子在 t=0.5 时的密度误差分布，每段宽 0.02，取段内最大绝对误差。</figcaption></figure>')
    assert metrics['S4']['rho']<metrics['S1']['rho']
    assert metrics['S4']['u']<metrics['S1']['u']
    src=src.replace('<!-- POINT_COMPARISON -->',f'FD 的双场误差均较小；Integrable 的 $\\rho$ 误差为 FD 的 {metrics["S1"]["rho"]/metrics["S4"]["rho"]:.1f} 倍。')
    b64=base64.b64encode((OUT/'paper_point_rho.png').read_bytes()).decode('ascii')
    src=src.replace('<!-- POINT_FIGURE -->',f'<figure><img src="data:image/png;base64,{b64}" alt="单孤子在t=0.5时的密度误差分布"><figcaption>图 1　单孤子在 t=0.5 时的密度误差分布，每段宽 0.02，取段内最大绝对误差。</figcaption></figure>')
    subprocess.run([sys.executable,str(HERE/'generate_waveform_comparison.py')],check=True)
    wave_b64=base64.b64encode((OUT/'waveform_comparison.png').read_bytes()).decode('ascii')
    src=src.replace('<!-- WAVEFORM_COMPARISON -->',f'<figure><img src="data:image/png;base64,{wave_b64}" alt="t=0.5时单孤子和二孤子的u与rho波形，解析解为实线，Integrable为空心三角，FD为空心圆"><figcaption>图 3　t=0.5 时的单孤子（左）与二孤子（右）波形，上行为 u，下行为 ρ。实线为连续解析解，空心三角为 Integrable，空心圆为 FD；数值点抽稀显示。</figcaption></figure>')
    formulas=[]
    def protect(m):formulas.append(m[0]);return f'MATHPLACEHOLDER{len(formulas)-1}END'
    src=re.sub(r'\$\$[\s\S]*?\$\$|\$[^$\n]+\$',protect,src)
    body=markdown.markdown(src,extensions=['tables','md_in_html'])
    for i,f in enumerate(formulas):body=body.replace(f'MATHPLACEHOLDER{i}END',html.escape(html.unescape(f),quote=False))
    css='''*{box-sizing:border-box}body{margin:0;color:#111;background:#eee;font:12pt/1.8 "Times New Roman","SimSun",serif}main{max-width:900px;margin:28px auto;padding:65px 72px;background:#fff}h1{font-size:18pt;text-align:center;font-weight:bold;line-height:1.65;margin:0 0 36px}h2{font-size:14pt;line-height:1.5;margin:32px 0 18px}p{text-align:justify;margin:12px 0;text-indent:2em}table{width:100%;border-collapse:collapse;font-size:11pt;margin:12px 0 20px;border-top:1.5px solid;border-bottom:1.5px solid}th{border-bottom:1px solid}th,td{padding:8px;text-align:right}th:first-child,td:first-child{text-align:left}figure{margin:22px 0}img{width:100%;height:auto}figcaption,.caption{text-align:center;font-size:10.5pt;line-height:1.6}.katex-display{overflow-x:auto;overflow-y:hidden;font-size:.88em;padding:8px 0}a{color:#222}@page{size:A4;margin:22mm 20mm}@media print{body{background:white;font-size:11pt}main{margin:0;padding:0;max-width:none}h2{break-after:avoid}figure,table{break-inside:avoid}}@media(max-width:650px){main{padding:28px 18px;margin:0}h1{font-size:16pt}body{font-size:11pt}table{font-size:9pt}}'''
    page='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Report</title><style>@@KATEX_CSS@@</style><style>'+css+'</style></head><body><main>'+body+'</main><script>@@KATEX_JS@@</script><script>renderMathInElement(document.querySelector("main"),{delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}],throwOnError:false});</script></body></html>'
    (HERE/'_src/Report.src.html').write_text(page,encoding='utf-8')
    (OUT/'validation_data.json').write_text(json.dumps(dict(math_expressions=len(formulas),original_metric_difference=maximum,source_configuration=d['configuration'],evaluation_bounds=[-1,1],evaluation_points=32001,metrics=metrics,schemes=['S1','S4'],method='rk4',time=.5,dt=.003125),ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Report generated; {len(formulas)} formulas, two methods; metric difference {maximum}.')
if __name__=='__main__':main()
