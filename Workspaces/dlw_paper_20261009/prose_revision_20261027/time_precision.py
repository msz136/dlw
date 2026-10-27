from pathlib import Path
from bs4 import BeautifulSoup
import json,re
R=Path('C:/Users/msz/aca');H=Path(__file__).parent;P=R/'dlw-paper.html';raw=P.read_bytes();s=raw.decode('utf-8')
assert 'id="table-time-precision"' not in s
(H/'before_time_precision.html').write_bytes(raw)
cases=[('A','One-soliton'),('D','Two-soliton'),('Gaussian','Gaussian'),('Sinusoidal','Sinusoidal')]
B=R/'Workspaces/dlw_paper_20261009/time_samm_20261025/time'
rows=[];records=[]
def sci(x,d=11):
 a,b=f'{x:.{d}e}'.split('e');return a+' &times; 10<sup>'+str(int(b))+'</sup>'
for case,label in cases:
 data=json.loads((B/(case+'_time.json')).read_text())['integrators']
 controls=json.loads((B/(case+'_controls.json')).read_text())['controls']
 rk=data['RK4']['error'];cn=data['CN']['error']
 half=next(x for x in controls if x['integrator']=='RK4')['error'];tight=next(x for x in controls if x['control']=='tight_solve')['error']
 for i,q in enumerate(['u','v']):
  delta=cn[i]-rk[i];winner='RK4' if delta>0 else 'C–N' if delta<0 else 'Equal'
  records.append(dict(case=case,field=q,rk4=rk[i],cn=cn[i],cn_minus_rk4=delta,smaller=winner,rk4_half_step_change=half[i]-rk[i],cn_tolerance_change=tight[i]-cn[i]))
  cells=('<td rowspan="2">'+label+'</td>') if i==0 else ''
  rows.append('<tr>'+cells+'<td><i>'+q+'</i></td><td>'+sci(rk[i])+'</td><td>'+sci(cn[i])+'</td><td>'+sci(delta,5)+'</td><td>'+winner+'</td></tr>')
note=' Values are rounded to four significant digits; some RK4 and Crank–Nicolson entries therefore coincide. Additional digits, signed differences and the smaller recorded error are given in <a href="#table-time-precision">Appendix D, Table 8</a>.'
pat=r'(<table id="table-time"><caption>)(.*?)(</caption>)'
s,n=re.subn(pat,lambda m:m[1]+m[2]+note+m[3],s,count=1,flags=re.S);assert n==1
s=s.replace('RK4 and Crank–Nicolson lie on top of each other throughout the entire evolution', 'RK4 and Crank–Nicolson are nearly superposed at the scale of the plots')
text='''<h4>Resolving the RK4 and Crank–Nicolson differences</h4>
<p>Table 8 resolves the entries that coincide after rounding in Table 4. It lists twelve significant digits from the saved terminal error norms and their signed difference, C–N minus RK4. A positive difference means that RK4 has the smaller recorded error. Both methods advance the same spatial system with a small time step, so their total physical-field errors are close even though their temporal approximations differ. The extra digits resolve this difference at the parameters used in the main experiment.</p>
<div class="table-wrap"><table id="table-time-precision"><caption>Table 8. Terminal RK4 and Crank–Nicolson error norms at T = 0.01, with h = Δx = 0.1 and Δt = 10⁻⁴. The last column compares the two saved main runs.</caption><thead><tr><th>Case</th><th>Field</th><th>RK4</th><th>Crank–Nicolson</th><th>C–N − RK4</th><th>Smaller error</th></tr></thead><tbody>'''+''.join(rows)+'''</tbody></table></div>
<p>For the one-soliton case, Crank–Nicolson gives the smaller <i>u</i> error by 1.442999 × 10<sup>−10</sup>, while RK4 gives the smaller <i>v</i> error by 1.838085 × 10<sup>−11</sup>. In the two-soliton case, RK4 is smaller in both components, by 1.310683 × 10<sup>−6</sup> and 4.263798 × 10<sup>−8</sup>, respectively. These differences exceed the changes observed in the corresponding RK4 half-step and C–N tighter-tolerance controls, and the recorded ordering is retained under those controls.</p>
<p>The Gaussian main runs favor Crank–Nicolson in <i>u</i> and RK4 in <i>v</i>; the sinusoidal main runs favor Crank–Nicolson in both components. Their differences range from approximately 1.6 × 10<sup>−13</sup> to 1.8 × 10<sup>−12</sup>. The saved step-size controls show how sensitive these small differences are to temporal resolution. Halving the RK4 time step changes its Gaussian <i>v</i> error to 6.969132826384 × 10<sup>−9</sup> and its sinusoidal <i>v</i> error to 4.704773459707 × 10<sup>−9</sup>, reversing their ordering relative to the main C–N runs. Thus Table 8 distinguishes the methods at the stated time step, while the controls show that the closest comparisons depend on that step. The displayed digits report the computed norms; they are not a certification of twelve-digit accuracy of the continuous reference.</p>
'''
pat=r'(<section\b[^>]*id="appendix-D"[^>]*>)(.*?)(</section>)'
s,n=re.subn(pat,lambda m:m[1]+m[2]+text+m[3],s,count=1,flags=re.S);assert n==1
a=BeautifulSoup(raw.decode('utf-8'),'html.parser');b=BeautifulSoup(s,'html.parser')
assert [str(x) for x in a.find_all('figure')]==[str(x) for x in b.find_all('figure')]
for t in a.find_all('table'):
 if t.get('id')!='table-time':assert str(t)==str(b.find(id=t['id'])) if t.get('id') else True
assert len(b.find_all('table'))==8
P.write_bytes(s.encode('utf-8'))
(H/'time_precision.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
with (R/'Workspaces/workspace_catalog_audit_20261013/progress_history/2026-10.md').open('a',encoding='utf-8') as f:f.write('\n2026-10-27 同轮补充：核对四算例RK4/C–N保存全精度误差及控制实验；主表说明四位有效数字舍入，Appendix D新增Table 8列12位有效数字、差值及较小者。说明非孤子v微小排序随RK4步长减半改变；曲线改称图示尺度近乎重合。未重跑，现14图8表。证据：prose_revision_20261027/time_precision.json。\n')
p=R/'PROGRESS_LOG.md';t=p.read_text(encoding='utf-8');t=t.replace('下一步按用户选择继续审稿，其他图布局暂不调整。','已核对时间法全精度数据，Table 4增加舍入说明，Appendix D新增Table 8及控制解释；现14图8表，细小排序按固定步长报告。下一步继续审稿，其他图布局暂不调整。');p.write_text(t,encoding='utf-8')
print(json.dumps(records,indent=2))
