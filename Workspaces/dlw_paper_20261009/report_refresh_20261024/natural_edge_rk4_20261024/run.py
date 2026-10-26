"""Natural edge reconstruction: fixed-RK4 four-soliton comparison."""
from pathlib import Path
import sys, json, hashlib, time, csv
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=BASE.parents[2]
PROBE=BASE.parent/'spatial_audit_20261023/separated/reconstruction_probe'
sys.path.insert(0,str(PROBE))
from probe import Model, invert, transform, rates, HALF_WIDTHS
from rerun_20261024 import rhs, norms

def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def run(case):
    out=HERE/f'{case}.json'
    if out.exists():
        print('Retained',out.name,flush=True);return
    start=time.perf_counter()
    m=Model(case,'Centered-SD',.1,.1);m.gauge='local'
    u=m.initial()[0];yv=(m.y[1:]+m.y[:-1])/2
    v=m.profile(yv,0)[1]
    _,g=m.G.tau(m.y[:1]/m.h-.5,m.x,0,False)
    w,_,_=invert(m,u,v,4*m.G.cov(g,0,2)[0])
    z0=np.array([u,w]);z=z0.copy()
    initial=norms(m,u-m.profile(m.y,0)[0],transform(m,u,w)-v)
    assert max(initial)<1e-11
    # Reproduce the previously tested natural-edge initial vector field.
    ut,wt,vt=rates(m,u,w)
    assert np.max(abs(rhs(m,0,z0)-np.array([ut,wt])))<1e-12
    old=read(PROBE/f'{case}_0.1_local.json')
    defect_u=norms(m,ut-m.ut(m.y,0),np.zeros_like(v))[0]
    assert abs(defect_u-old['defects'][0])<1e-11
    dt=1e-4;T=.01
    with np.errstate(over='raise',invalid='raise',divide='raise'):
        for i in range(100):
            t=i*dt
            k1=rhs(m,t,z);k2=rhs(m,t+dt/2,z+dt*k1/2)
            k3=rhs(m,t+dt/2,z+dt*k2/2);k4=rhs(m,t+dt,z+dt*k3)
            z+=dt*(k1+2*k2+2*k3+k4)/6
            assert np.isfinite(z).all() and np.max(abs(z))<1e6
    v=transform(m,*z)
    error=norms(m,z[0]-m.profile(m.y,T)[0],v-m.profile(yv,T)[1])
    artifact=HERE/f'{case}.npz'
    np.savez_compressed(artifact,z=z,z0=z0,u=z[0],v=v,x=m.x,y=m.y,yv=yv)
    # Reload final fields and reconstruct without the helper map.
    saved=np.load(artifact)
    independent_v=np.diff(saved['z'][0],axis=0)/m.h+(saved['z'][1,1:]+saved['z'][1,:-1])/2
    map_error=float(np.max(abs(independent_v-saved['v'])))
    r=HALF_WIDTHS[case];mx=abs(saved['x'])<=r
    recomputed=[]
    for field,y in [(saved['u'],saved['y']),(saved['v'],saved['yv'])]:
        j=len(recomputed)
        diff=field-m.profile(y,T)[j]
        recomputed.append(float(np.max(abs(diff[abs(y)<r][:,mx]))))
    assert recomputed==error and map_error<1e-12
    sources=[Path(__file__),PROBE/'probe.py',PROBE/'rerun_20261024.py',PROBE.parents[1]/'run.py',PROBE.parent/'run_separated.py']
    record=dict(case=case,method='Centered-SD natural edge',h=.1,dx=.1,dt=dt,T=T,reached=T,
        integrator='RK4',status='complete',error=error,initial_error=initial,
        initial_u_defect_difference=abs(defect_u-old['defects'][0]),map_error=map_error,
        recomputed_error=recomputed,state='u,w; v=backward difference u + adjacent average w',
        boundary='Exact continuous lower u_t; lower w initialized as v-u_y and then evolved by w equation',
        artifact=str(artifact.relative_to(ROOT)),artifact_sha256=sha(artifact),
        sources=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in sources],seconds=time.perf_counter()-start)
    out.write_text(json.dumps(record,indent=2),encoding='utf-8')
    print(json.dumps(record),flush=True)

def collect():
    natural=[read(HERE/f'{c}.json') for c in 'ABCD']
    allrows=read(BASE/'rk4_spatial/results.json')+read(BASE/'csd0_rk4_20261024/results.json')+natural
    assert len(allrows)==20 and all(r['status']=='complete' for r in allrows)
    methods=['Endpoint-SD','CSD0','Centered-SD natural edge','Centered-SD','FD']
    labels=['Endpoint-SD','CSD0（旧节点）','Centered-SD（自然边场）','Centered-SD（完整势）','FD']
    (HERE/'results.json').write_text(json.dumps(allrows,indent=2),encoding='utf-8')
    with (HERE/'comparison.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f);writer.writerow(['case','method','h','dx','dt','T','error_u','error_v'])
        for r in allrows:writer.writerow([r['case'],r['method'],.1,.1,1e-4,.01,*r['error']])
    trs=[];markdown=[];bold=0
    for c in 'ABCD':
        values=[next(r for r in allrows if r['case']==c and r['method']==m)['error'] for m in methods]
        for j,field in enumerate(['u','v']):
            minimum=min(v[j] for v in values);cells=[];md=[]
            for value in values:
                val=value[j];s=f'{val:.4e}';best=s==f'{minimum:.4e}';bold+=best
                cells.append(f'<td data-value="{val:.17g}">'+(f'<strong>{s}</strong>' if best else s)+'</td>')
                md.append(f'**{s}**' if best else s)
            head=f'<th rowspan="2" scope="rowgroup">{c}</th>' if j==0 else ''
            trs.append(f'<tr>{head}<th>{field}</th>'+''.join(cells)+'</tr>')
            markdown.append('| '+c+' | '+field+' | '+' | '.join(md)+' |')
    html='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>自然边场重构的空间格式比较</title>
<style>body{max-width:1200px;margin:40px auto;padding:0 24px;color:#202020;font:17px/1.8 Georgia,"Microsoft YaHei",serif}h1{font-size:27px}table{border-collapse:collapse;width:100%;border-top:2px solid;border-bottom:2px solid;font-size:14px;font-variant-numeric:tabular-nums}thead{border-bottom:1px solid}td,th{padding:12px 10px;text-align:right}th{text-align:center}tbody tr:nth-child(2n){border-bottom:1px solid #ddd}td{white-space:nowrap}.table-wrap{overflow-x:auto}a{color:#345}caption{text-align:left;margin-bottom:12px}</style>
<h1>自然边场重构的空间格式比较</h1>
<p>四个孤子算例统一采用 RK4，h = Δx = 0.1，Δt = 10⁻⁴，T = 0.01；x 方向采用 Fourier 微分。误差为指定区域内各物理场采样点上，相对于连续精确解的最大绝对误差。</p>
<p>自然边场采用 v = Δₕu + (wₖ + wₖ₋₁)/2，保留 u 方程中的 h²A(w) 通量。CSD0 采用旧节点重构 v = w + δ₀u；完整势形式额外包含 h²JΔₕA(w)。两种边场形式均推进 (u,w)，其余三种格式推进 (u,v)。</p>
<div class="table-wrap"><table><caption>T = 0.01 的物理场误差。粗体表示每个算例、每个分量的最小值。</caption><thead><tr><th>算例</th><th>分量</th>'''+''.join(f'<th>{l}</th>' for l in labels)+'</tr></thead><tbody>'+''.join(trs)+'''</tbody></table></div>
<p>A、B 为单孤子；C、D 为双孤子。测量区域分别为 |x| ≤ R、|y| &lt; R，R = 5、10、30、30。各格式使用自身物理场采样位置及既有边界闭合。</p>
<p><a href="../Workspaces/dlw_paper_20261009/report_refresh_20261024/natural_edge_rk4_20261024/comparison.csv">下载数据 CSV</a></p></html>'''
    from bs4 import BeautifulSoup
    soup=BeautifulSoup(html,'html.parser')
    assert len(soup.select('td'))==40 and len(soup.select('strong'))==bold
    for tr,md in zip(soup.select('tbody tr'),markdown):
        cells=tr.select('td');minimum=min(float(x['data-value']) for x in cells)
        for cell in cells:assert bool(cell.strong)==(f"{float(cell['data-value']):.4e}"==f'{minimum:.4e}')
    report=ROOT/'report/dlw_natural_edge_comparison_20261024.html'
    report.write_text(html,encoding='utf-8')
    (HERE/'table.md').write_text('\n'.join(markdown),encoding='utf-8')
    (HERE/'validation.json').write_text(json.dumps(dict(complete=4,cells=40,bold=bold,max_map_error=max(r['map_error'] for r in natural),max_initial_error=max(max(r['initial_error']) for r in natural)),indent=2))
    print('\n'.join(markdown),flush=True)

if __name__=='__main__':
    if sys.argv[1]=='collect':collect()
    else:run(sys.argv[1])
