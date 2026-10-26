from fine_grid import *
import csv
methods=('Endpoint-SD','Centered-SD','FD')
labels={'A':'One-soliton (1, 2)','B':'One-soliton (4, −3)','C':'Two-soliton (6, −5; 4, −3)','D':'Two-soliton (1, 2; 4, −3)','Gaussian':'Gaussian','Sinusoidal':'Sinusoidal'}
records=[];rows=[];stops=[]
for case in labels:
    rr=[json.loads((OUT/f'{case}_{m}_dt0.0001.json').read_text()) for m in methods]
    assert all(r['failed_at'] is not None for r in rr),'Completed run needs final-error evaluation'
    records.extend(rr)
    rows.append('<tr><th>'+labels[case]+'</th>'+''.join('<td>— / —</td>' for _ in rr)+'</tr>')
    stops.append('<tr><th>'+labels[case]+'</th>'+''.join('<td>'+f"{r['failed_at']:.4f}"+'</td>' for r in rr)+'</tr>')
with (OUT/'table.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['case','method','dx','h','dt','target_T','e_u','e_v','stop_time'])
    for r in records:w.writerow([r['case'],r['method'],.01,.01,.0001,.01,'NA','NA',r['failed_at']])
(OUT/'results.json').write_text(json.dumps(records,indent=2),encoding='utf8')
head='<thead><tr><th>Test</th>'+''.join('<th>'+m+'</th>' for m in methods)+'</tr></thead>'
body='''<h1>Spatial-discretization comparison: Δx=h=0.01</h1><table><caption><b>Table 1.</b> Final-time maximum errors e<sub>u</sub> / e<sub>v</sub>; RK4, Δx=h=0.01, Δt=10<sup>−4</sup>, T=0.01.</caption>'''+head+'<tbody>'+''.join(rows)+'''</tbody></table><p class="note">—: the computation triggered the stopping criterion before T=0.01, so no final-time error is reported. No minimum is highlighted because no method supplied a valid final-time result.</p><table><caption><b>Diagnostic table.</b> First detected stopping times for the same runs.</caption>'''+head+'<tbody>'+''.join(stops)+'''</tbody></table>
<p class="note">Stopping criterion: a nonfinite field or max(|u|,|v|)&gt;10⁶. Times are step-end detection times, not analytical blow-up times. The original domains, parameters, initial and boundary profiles, Fourier derivatives and lack of filtering are retained.</p>
<h2>本轮说明</h2><p>六算例的三种方法均实际重跑至首次触发判据；没有用旧网格误差外推，也没有将中途场变化填成终止误差。新分块实现与原实现的小网格一阶导数右端差异&lt;9×10⁻¹⁵，RK4一步差异&lt;3×10⁻¹⁶。最大算例采用磁盘工作数组逐块计算。</p>
<p>dx=.01 时最高普通模态的 dt·ξ² 接近9.87，而经典RK4在负实轴的稳定区间约到−2.785。原 dt=10⁻⁴ 已不能稳定推进这样的衰减模态；Endpoint-SD 还具有此前推导的正增长分支。因此本表不能解释为单纯的空间截断误差比较。</p>'''
control=OUT/'control/A_Endpoint-SD_dt1e-05.json'
if control.exists():
    c=json.loads(control.read_text());body+='<p>补充控制：单孤子A的Endpoint-SD改用dt=10⁻⁵（dt·ξ²≈.987）后，仍于 t='+str(c['failed_at'])+' 触发停止判据。该检查表明仅减小时间步尚未恢复到T=.01的有效结果，不将其冒充三法共同参数主表。</p>'
body+='''<p><a href="dlw_spatial_table_T001_20261023.html">保留的 Δx=h=.1 表</a> · <a href="../Workspaces/dlw_paper_20261009/spatial_audit_20261023/fine_dx001/table.csv">本表CSV</a> · <a href="../Workspaces/dlw_paper_20261009/spatial_audit_20261023/fine_dx001/results.json">逐步峰值及运行记录</a></p>'''
out=HERE.parents[2]/'report/dlw_spatial_table_dx001_20261023.html'
out.write_text('''<!doctype html><html><meta charset="utf-8"><title>DLW Δx=h=.01</title><style>body{max-width:1100px;margin:48px auto;padding:0 28px;font:17px/1.6 "Times New Roman","SimSun",serif;color:#111}table{border-collapse:collapse;width:100%;border-top:2px solid;border-bottom:2px solid;margin:28px 0 12px}thead{border-bottom:1px solid}th,td{padding:10px 12px;text-align:center}tbody th{text-align:left;font-weight:normal}caption{text-align:left;padding-bottom:12px}.note{font-size:14px}h1{font-size:26px}h2{font-size:20px}@media print{body{margin:0;font-size:11pt}table{break-inside:avoid}}</style>'''+body+'</html>',encoding='utf8')
for c in labels:print(c,[r['failed_at'] for r in records if r['case']==c])
