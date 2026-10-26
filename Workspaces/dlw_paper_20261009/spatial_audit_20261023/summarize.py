from pathlib import Path
import json,sys,html
import numpy as np
from scipy.interpolate import CubicSpline
from run import Model,CASES,HALF_WIDTHS,HERE

def load(case,method,variant):
    stem=HERE/f'{case}_{method}_{variant}'
    if not stem.with_suffix('.json').exists():return None,None
    rec=json.loads(stem.with_suffix('.json').read_text())
    return rec,np.load(stem.with_suffix('.npz')) if not rec['failed_at'] else None

rows=[]
for case in (*CASES,'Gaussian','Sinusoidal'):
    for method in ('Endpoint-SD','Centered-SD','FD'):
        r,b=load(case,method,'base')
        if r is None:continue
        row=dict(case=case,method=method,base=r)
        if b is not None:
            if case in CASES:
                m=Model(case,method,r['dx'],r['h'])
                node=[];interp=[]
                for j,key in enumerate(('y','yv')):
                    yy=b[key]; mask=abs(yy)<HALF_WIDTHS[case]; xm=abs(b['x'])<=HALF_WIDTHS[case]
                    ref=m.profile(yy[mask],r['T'])[j]
                    node.append(float(abs(b['z'][j,mask][:,xm]-ref[:,xm]).max()))
                    xx=np.linspace(-HALF_WIDTHS[case],HALF_WIDTHS[case],round(2*HALF_WIDTHS[case]/.02)+1)
                    interp.append(float(abs(CubicSpline(b['x'],ref,axis=-1)(xx)-m.profile(yy[mask],r['T'],xx)[j]).max()))
                row['nodal_errors']=node;row['reference_interpolation_error']=interp
            for variant in ('halfdt','x_refined','y_refined'):
                rr,f=load(case,method,variant)
                if rr is None:continue
                row[variant]=rr
                if f is None:continue
                dif=[]
                for j,key in enumerate(('y','yv')):
                    fine=f['z'][j]
                    if variant=='x_refined':fine=fine[:,::2]
                    if variant=='y_refined':fine=CubicSpline(f[key],fine,axis=0)(b[key])
                    ym=(abs(b[key])<HALF_WIDTHS[case]) if case in CASES else ((b[key]>=-1.8)&(b[key]<=1.8))
                    xm=(abs(b['x'])<=HALF_WIDTHS[case]) if case in CASES else np.ones(len(b['x']),bool)
                    dif.append(float(abs(fine[ym][:,xm]-b['z'][j,ym][:,xm]).max()))
                row[variant+'_difference']=dif
        rows.append(row)
(HERE/'summary.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
def pair(a):return ' / '.join(f'{v:.3e}' for v in a) if a else '—'
def table(header,data):return '<table><thead><tr>'+''.join('<th>'+h+'</th>' for h in header)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in data)+'</tbody></table>'
intro='''<h1>DLW 六算例空间离散复核</h1><p>2026-10-23 · Endpoint-SD / Centered-SD / FD · 固定网格，物理场 u,v，Fourier x 微分，RK4，无滤波。</p>
<h2>已有实验与本轮区别</h2><p>2026-10-22 的四孤子 Endpoint-SD/PE/FD 比较已完成，但 x 方向采用中心差分，PE 推进 P,W。附件 PDF 第12–13页有 Endpoint-SD 的 Fourier 孤子及 Gaussian/正弦结果。本轮新写 u,v 推进器，所有三种格式统一 Fourier 算子；旧结果未覆盖、未冒充本轮数据。</p>
<p>保留全部四组孤子：A=(1,2)，B=(4,−3)，C=(6,−5;4,−3)，D=(1,2;4,−3)。a=2，h=.1，T=.01，dt=.0001；基准 dx=.2，x加密 dx=.1，y加密 h=.05。计算半宽10/20/40/40，评价半宽5/10/30/30。Gaussian/正弦使用 a=1/3，x∈[−96,96)，y∈[−2,2]，h=.1，Nx=384，T=.1，dt=.001；x加密 Nx=768。</p>
<h2>位置与边界</h2><p>Endpoint-SD 的 u 位于 y_k，v 位于 y_k−h/2；另两种格式的 u,v 共点。精确误差在各自真实场位置计算，表中最大值的 y 采样点不完全相同。三种格式从相同连续物理剖面取样。</p>
<p>Endpoint-SD 使用向后格点差，无右端边界。Centered-SD/FD 的上侧 u 虚点采用“给定背景＋内部扰动二次外推”；下侧数据由背景给定。孤子背景为连续精确解；非精确背景为初始剖面，左端 u=0。Centered-SD 的 v_t 中对虚点规则也作相同时间微分。这不是两端固定 u,v，也不能直接套用 Endpoint-SD 的谱结论。</p>
<p>非精确数据采用 e(y)=sin[π(y+2)/4] 的共同物理剖面；Endpoint-SD 在边中点对 v 取样。故并非附件按同一 k 指定两场振幅的逐项复现。Gaussian 振幅 .05/.03，宽度6；正弦振幅 .03/.02，波长24。</p>'''
sol=[r for r in rows if r['case'] in CASES]
body=intro+'<h2>孤子：连续精确解误差（u / v）</h2><p>基准与 x 加密误差均用 x 方向三次样条在 .02 间距上评价。额外列出基准节点误差和对精确样本作同样插值的误差，以辨识插值影响；后者不是求解器误差。</p>'
body+=table(['算例','方法','基准总误差','节点误差','精确样本插值误差','x加密总误差','y加密总误差'],[[r['case'],r['method'],pair(r['base'].get('errors')),pair(r.get('nodal_errors')),pair(r.get('reference_interpolation_error')),pair(r.get('x_refined',{}).get('errors')),pair(r.get('y_refined',{}).get('errors'))] for r in sol])
body+='<h2>非精确初值：加密差异（u / v）</h2><p>以下是两次计算之差，不是精确解误差。x比较取共同节点；y比较将细格插值至粗格，评价 −1.8≤y≤1.8。y加密时 Endpoint-SD 的边中点随 h 改变，差异也包含位置对齐插值。</p>'
body+=table(['初值','方法','时间步减半差异','x加密差异','y加密差异'],[[r['case'],r['method'],pair(r.get('halfdt_difference')),pair(r.get('x_refined_difference')),pair(r.get('y_refined_difference'))] for r in rows if r['case'] not in CASES])
body+='<h2>孤子：时间步减半与空间加密差异</h2>'+table(['算例','方法','时间步减半差异','x加密差异','y加密差异'],[[r['case'],r['method'],pair(r.get('halfdt_difference')),pair(r.get('x_refined_difference')),pair(r.get('y_refined_difference'))] for r in sol])
body+='<h2>数据用途</h2><p>本轮是六算例数据审计，未筛除不利结果。有限时刻的误差排序与加密差异分别报告；没有精确参考的两组不能据此宣称某方法更准确。Fourier 的高频增长、周期截断与 x 插值都会影响加密结果，不能把所有变化归因于 y 离散阶。</p><p>完整参数、72次运行记录、状态数组、实现和验证结果：<a href="../Workspaces/dlw_paper_20261009/spatial_audit_20261023/summary.json">summary.json</a>；<a href="../Workspaces/dlw_paper_20261009/spatial_audit_20261023/run.py">实验实现</a>。</p>'
out=HERE.parents[2]/'report/dlw_spatial_diagnostics_20261023.html'
out.write_text('<!doctype html><html lang="zh"><meta charset="utf-8"><title>DLW 六算例空间离散复核</title><style>body{font:16px/1.7 Georgia,"Microsoft YaHei",serif;max-width:1450px;margin:40px auto;padding:0 28px;color:#24303b}h1,h2{color:#17364d}table{border-collapse:collapse;width:100%;font-size:13px;margin:20px 0}td,th{padding:10px;border-bottom:1px solid #cbd5df;text-align:left}th{background:#edf2f6}p{max-width:1100px}</style>'+body+'</html>',encoding='utf8')
print('rows',len(rows),'complete variants',sum(1+sum(v in r for v in ('halfdt','x_refined','y_refined')) for r in rows))
for r in rows: print(r['case'],r['method'],'base',pair(r['base'].get('errors')),'x_refined',pair(r.get('x_refined',{}).get('errors')),'dt',pair(r.get('halfdt_difference')))
