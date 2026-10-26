from run import *
import csv
methods=('Endpoint-SD','Centered-SD','FD')
ALIGNED='--a2' in sys.argv
PREFIX='a2_' if ALIGNED else ''
NAME='paper_table_a2' if ALIGNED else 'paper_table'
rows=[];checks={}
for case in CASES:
    rr=[]
    for method in methods:
        r=json.loads((HERE/f'{case}_{method}_main.json').read_text())
        assert r['T']==.01 and r['dx']==.1 and r['h']==.1 and r['dt']==.0001
        rr.append(r['errors'])
    rows.append(dict(case=case,errors=rr,reference='continuous exact solution'))
for case in ('Gaussian','Sinusoidal'):
    ref=np.load(HERE/f'{case}_FD_short_{PREFIX}ref8.npz')
    ref4=np.load(HERE/f'{case}_FD_short_{PREFIX}ref4.npz')
    reference_change=[]
    mask=abs(ref4['y'])<=1.8
    for j in range(2):reference_change.append(float(abs(ref4['z'][j,mask]-ref['z'][j,::2][mask]).max()))
    rr=[];timechecks=[];rank4=[]
    for method in methods:
        b=np.load(HERE/f'{case}_{method}_short_{PREFIX}main.npz')
        half=np.load(HERE/f'{case}_{method}_short_{PREFIX}halfdt.npz')
        err=[];dt=[];err4=[]
        for j,key in enumerate(('y','yv')):
            mask=(b[key]>=-1.8)&(b[key]<=1.8)
            fine=CubicSpline(ref['y'],ref['z'][j],axis=0)(b[key][mask])
            finer4=CubicSpline(ref4['y'],ref4['z'][j],axis=0)(b[key][mask])
            # Same x evaluation spacing (.02) as the exact-wave rows.
            xx=np.linspace(-96,95.9,9596)
            diff=CubicSpline(b['x'],b['z'][j,mask]-fine,axis=-1)(xx)
            diff4=CubicSpline(b['x'],b['z'][j,mask]-finer4,axis=-1)(xx)
            err.append(float(abs(diff).max()));err4.append(float(abs(diff4).max()))
            dt.append(float(abs(b['z'][j,mask]-half['z'][j,mask]).max()))
        rr.append(err);timechecks.append(dt);rank4.append(err4)
    rows.append(dict(case=case,errors=rr,reference='common FD reference: dx=.1,h=.0125,dt=.00005,T=.01'))
    checks[case]=dict(reference_refinement_difference=reference_change,time_halfstep_differences=timechecks,errors_against_h025=rank4,errors_against_h0125=rr)
    assert np.array_equal(np.argmin(rank4,axis=0),np.argmin(rr,axis=0)),'ranking changed with reference refinement'
(HERE/(NAME+'_results.json')).write_text(json.dumps(dict(rows=rows,checks=checks,common_a=2 if ALIGNED else None),indent=2))
with (HERE/(NAME+'.csv')).open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['case','method','e_u','e_v','reference'])
    for r in rows:
        for m,e in zip(methods,r['errors']):w.writerow([r['case'],m,*e,r['reference']])
labels={'A':'One-soliton (1, 2)','B':'One-soliton (4, −3)*','C':'Two-soliton (6, −5; 4, −3)*','D':'Two-soliton (1, 2; 4, −3)','Gaussian':'Gaussian†','Sinusoidal':'Sinusoidal†'}
def fmt(v):
    a,b=f'{v:.3e}'.split('e');return a+' × 10<sup>'+str(int(b)).replace('-','−')+'</sup>'
trs=[];md=['| Test | Endpoint-SD: e_u / e_v | Centered-SD: e_u / e_v | FD: e_u / e_v |','|---|---|---|---|']
for r in rows:
    ee=np.array(r['errors']);best=ee.argmin(axis=0);cells=[];mc=[]
    for i in range(3):
        nums=[('<strong>'+fmt(ee[i,j])+'</strong>') if i==best[j] else fmt(ee[i,j]) for j in range(2)]
        cells.append('<td>'+' / '.join(nums)+'</td>')
        mc.append(' / '.join(('**'+f'{ee[i,j]:.3e}'+'**') if i==best[j] else f'{ee[i,j]:.3e}' for j in range(2)))
    trs.append('<tr><th scope="row">'+labels[r['case']]+'</th>'+''.join(cells)+'</tr>')
    md.append('| '+labels[r['case']]+' | '+' | '.join(mc)+' |')
(HERE/(NAME+'.md')).write_text('\n'.join(md),encoding='utf8')
body='''<h1>Spatial-discretization comparison</h1><p class="lead">统一终止时刻 T=0.01 · Δx=h=0.1 · RK4 · Δt=10⁻⁴</p>
<table><caption><b>Table 1.</b> Maximum final-time errors e<sub>u</sub> / e<sub>v</sub> on fixed grids; RK4, Δx=h=0.1, Δt=10<sup>−4</sup>, T=0.01. Bold values indicate the smallest error in each field within each test.</caption><thead><tr><th>Test</th><th>Endpoint-SD: e<sub>u</sub> / e<sub>v</sub></th><th>Centered-SD: e<sub>u</sub> / e<sub>v</sub></th><th>FD: e<sub>u</sub> / e<sub>v</sub></th></tr></thead><tbody>'''+''.join(trs)+'''</tbody></table>
<p class="note">† The Gaussian and sinusoidal rows use a common numerical reference computed with FD at Δx=0.1, h=0.0125 and Δt=5×10⁻⁵. These are reference-solution discrepancies, not errors against an exact solution. The reference is refined in y and time at fixed x resolution. The ordering is unchanged when h=0.025 is used instead.</p>
<p class="note">* The B test and the u field in C are sensitive to x resolution. Their entries are retained as measured; bold type denotes only the numerical minimum, not a verified convergence advantage.</p>
<h2>比较口径</h2><p>所有主计算均为 Fourier x 微分、固定网格、相同时间算法和步长。四孤子从连续精确解初始化并在 T=.01 与该解比较；非精确初值从共同物理剖面初始化，并与同一加密 FD 解比较。Endpoint-SD 的 v 位于 y 边中点，误差在其真实位置评价，其他两法两场共点。最大值的 y 采样点并非完全相同。</p>
<p>四孤子沿用原评价区域；Gaussian/正弦在 −1.8≤y≤1.8、全 x 节点覆盖区评价。六组均使用 x 方向三次样条及 .02 评价间距。a与区域尺寸为各算例的固有参数，三种方法在同一算例内一致；统一 T 不意味着不同算例使用相同物理解。</p>
<h2>参考解与时间步复核</h2>'''
for c,v in checks.items():
    body+='<p>'+c+'：参考 h=.025 → .0125 的共同节点最大场差为 '+ ' / '.join(fmt(x) for x in v['reference_refinement_difference'])+'；三种主计算时间步减半后的最大场差为 '+fmt(np.max(v['time_halfstep_differences']))+'。这些检查衡量参照与时间误差的敏感性，不是完整连续解误差界。</p>'
body+='''<p><a href="../Workspaces/dlw_paper_20261009/spatial_audit_20261023/paper_table.csv">下载表格数据 CSV</a> · <a href="../Workspaces/dlw_paper_20261009/spatial_audit_20261023/paper_table_results.json">完整数值与复核</a></p>'''
if ALIGNED:
    body=body.replace('T=0.01. Bold','T=0.01, a=2. Bold').replace('统一终止时刻 T=0.01','统一方程参数 a=2 · 终止时刻 T=0.01')
    body=body.replace('a与区域尺寸为各算例的固有参数，三种方法在同一算例内一致；统一 T 不意味着不同算例使用相同物理解。','六组方程参数a统一为2；不同初始波形保留各自的区域，三种方法在同一算例内使用相同区域与初边值。')
    body=body.replace('paper_table.csv','paper_table_a2.csv').replace('paper_table_results.json','paper_table_a2_results.json')
out=HERE.parents[2]/('report/dlw_spatial_table_T001_a2_20261023.html' if ALIGNED else 'report/dlw_spatial_table_T001_20261023.html')
out.write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><title>DLW spatial errors at T=.01</title><style>body{max-width:1280px;margin:48px auto;padding:0 30px;color:#111;font:17px/1.6 "Times New Roman","SimSun",serif}h1{font-size:27px}h2{font-size:20px;margin-top:30px}.lead{color:#444}table{border-collapse:collapse;width:100%;border-top:2px solid #111;border-bottom:2px solid #111;margin:30px 0 12px;font-size:15px;font-variant-numeric:tabular-nums}caption{text-align:left;padding-bottom:12px}thead{border-bottom:1px solid #111}th,td{padding:12px 8px;text-align:center;white-space:nowrap}tbody th{text-align:left;font-weight:normal}sup{font-size:75%}strong{font-weight:700}.note{font-size:14px;line-height:1.5}@media print{body{margin:0;font-size:11pt}h1,.lead,h2,h2~p{display:none}table{font-size:9pt;break-inside:avoid}th,td{padding:8px 4px}.note{font-size:9pt}}</style>'''+body+'</html>',encoding='utf8')
print('\n'.join(md));print(json.dumps(checks,indent=2))
