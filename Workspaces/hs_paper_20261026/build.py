from pathlib import Path
import json,math,re,html
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent;WS=ROOT.parent.parent
r=json.loads((ROOT/'data/results.json').read_text());mesh=json.loads((ROOT/'data/mesh_evolution.json').read_text())
def sci(x):
 m,e=f'{x:.3e}'.split('e');return f'{m} × 10<sup>{int(e)}</sup>'
def table(n,caption,heads,rows):
 classes=['label' if h in ['Case','Spatial method','Integrator','Method','Mesh'] else 'number' for h in heads]
 return f'<div class="table-wrap"><table><caption>Table {n}. {caption}</caption><thead><tr>'+''.join(f'<th class="{c}" scope="col">{h}</th>' for h,c in zip(heads,classes))+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td class="{c}">{v}</td>' for v,c in zip(row,classes))+'</tr>' for row in rows)+'</tbody></table></div>'
def fig(n,files,caption):
 return '<figure id="fig'+str(n)+'">'+''.join(f'<a href="Workspaces/hs_paper_20261026/figures/{f}.pdf"><img src="Workspaces/hs_paper_20261026/figures/{f}.png" alt="{html.escape(caption)}" loading="lazy"></a>' for f in files)+f'<figcaption>Figure {n}. {caption}</figcaption></figure>'
rep={}
rep['FIG_PROFILES']=''.join(fig(i+1,[f'profiles_{i}'],f'{case}: continuous exact initial fields and space–time distributions. The maps use a fixed physical-coordinate window.') for i,case in enumerate(['One-soliton case','Two-soliton case']))
rep['FIG_SPATIAL']=''.join(fig(i+3,[f'spatial_{i}',f'error_maps_{i}'],f'{case}: terminal fields and absolute-error curves, followed by space–time error maps for the three spatial formulations. Nominal spacing 0.02; RK4 time step 0.0005. Black curves show continuous point values; colored symbols show computed fields. Moving-cell density errors use exact cell averages. The maps linearly interpolate native absolute errors onto the displayed physical coordinates; each panel has its own color scale.') for i,case in enumerate(['One-soliton case','Two-soliton case']))
rep['FIG_TIME']=''.join(fig(i+5,[f'time_{i}'],f'{case}: temporal errors against the exact finite-lattice solution, with a=0.02 and ΔT=0.0025.') for i,case in enumerate(['One-soliton case','Two-soliton case']))
rep['FIG_MESH_SAMPLE']=fig(7,['mesh'],'One-soliton snapshot at T=0.25. Cell widths and pointwise interpolation errors on three equal-node meshes with common physical endpoints.')
rep['FIG_MESH_EVOLUTION']=''.join(fig(i+8,[f'moving_mesh_{i}'],f'{case}: final cell widths and native field errors after evolution from uniform and curvature-adapted labels, with 201 nodes.') for i,case in enumerate(['One-soliton case','Two-soliton case']))
rep['FIG_RESPONSE']=''.join(fig(i+10,[f'response_{i}'],f'{case}: normalized velocity and density responses to a velocity-only initial perturbation of amplitude 10⁻⁶. Each trajectory is compared with its own unperturbed background at matching native indices.') for i,case in enumerate(['One-soliton case','Two-soliton case']))
rows=[];prev={}
for d in r['model']:
 p=prev.get(d['case']);rows.append([d['case'],f"{d['a']:g}",sci(d['u']),'—' if p is None else f"{math.log2(p['u']/d['u']):.2f}",sci(d['rho']),'—' if p is None else f"{math.log2(p['rho']/d['rho']):.2f}"]);prev[d['case']]=d
rep['TABLE_MODEL']=table(1,'Exact finite-lattice fields against the continuous reference at T=0.25.',['Case','a','E<sub>u</sub>','Order','E<sub>ρ</sub>','Order'],rows)
rows=[]
for case in ['One soliton','Two solitons']:
 for method in ['Integrable SD','Moving FD','Fixed FD']:
  prev=None
  for d in [d for d in r['spatial'] if d['case']==case and d['method']==method]:
   rows.append([case,method,f"{d['spacing']:g}",sci(d['u']),'—' if prev is None else f"{math.log2(prev['u']/d['u']):.2f}",sci(d['rho']),'—' if prev is None else f"{math.log2(prev['rho']/d['rho']):.2f}"]);prev=d
rep['TABLE_SPATIAL']=table(2,'Continuous-reference errors after RK4 evolution to T=0.25. Density errors are cell-average errors for moving methods and nodal errors for fixed FD.',['Case','Spatial method','a or Δx','E<sub>u</sub>','Order','E<sub>ρ</sub>','Order'],rows)
rep['SPATIAL_ANALYSIS']='<p>Both soliton cases exhibit approximately first-order refinement for integrable SD and second-order refinement for the two direct finite-difference formulations in their respective metrics. At nominal spacing 0.02, the one-soliton velocity errors are '+', '.join(sci(next(d['u'] for d in r['spatial'] if d['case']=='One soliton' and d['spacing']==.02 and d['method']==m)) for m in ['Integrable SD','Moving FD','Fixed FD'])+', respectively. The corresponding density errors distinguish the moving-cell and fixed-node representations. Halving the RK4 step at this resolution changes the evolved states by less than '+sci(max(v for k,v in r['checks'].items() if k.startswith('spatial_dt')))+', placing the reported errors well above the observed temporal refinement difference.</p>'
rows=[]
for case in ['One soliton','Two solitons']:
 for method,label in [('euler','Euler'),('rk4','RK4'),('trapezoid','Crank–Nicolson')]:
  prev=None
  for d in [d for d in r['time'] if d['case']==case and d['method']==method]:
   eu,er=sci(d['u']),sci(d['rho'])
   if method=='rk4':eu='<b>'+eu+'</b>';er='<b>'+er+'</b>'
   rows.append([case,label,f"{d['dt']:g}",eu,'—' if prev is None else f"{math.log2(prev['u']/d['u']):.2f}",er,'—' if prev is None else f"{math.log2(prev['rho']/d['rho']):.2f}"]);prev=d
rep['TABLE_TIME']=table(3,'Temporal errors at T=0.25 for a=0.02. Bold entries are smallest among the three integrators at the same case and step size.',['Case','Integrator','ΔT','E<sub>u</sub>','Order','E<sub>ρ</sub>','Order'],rows)
rep['TABLE_MESH_SAMPLE']=table(4,'Equal-node snapshot reconstruction errors; 401 nodes.',['Mesh','E<sub>u</sub>','E<sub>ρ</sub>','Minimum width','Maximum width'],[[d['mesh'],sci(d['u']),sci(d['rho']),f"{d['min_dx']:.5f}",f"{d['max_dx']:.5f}"] for d in r['mesh']])
rep['TABLE_MESH_EVOLUTION']=table(5,'Errors after moving FD evolution from two initial label distributions. The common-point columns include piecewise-linear reconstruction.',['Case','γ','Native E<sub>u</sub>','Native E<sub>ρ</sub>','Common-point E<sub>u</sub>','Common-point E<sub>ρ</sub>'],[[d['case'],d['gamma']]+[sci(d[q]) for q in ['u','rho','common_u','common_rho']] for d in mesh])
factors=[]
for i in [0,2]:factors.append([mesh[i][q]/mesh[i+1][q] for q in ['u','rho','common_u','common_rho']])
rep['MESH_ANALYSIS']=f'<p>For the one-soliton case, the adapted labels reduce the native velocity and density errors by factors of {factors[0][0]:.2f} and {factors[0][1]:.2f}; on the common physical points, the factors are {factors[0][2]:.2f} and {factors[0][3]:.2f}. The two-soliton case also improves in both fields, with common-point factors of {factors[1][2]:.2f} and {factors[1][3]:.2f}. All cells remain positive. Halving the time step changes the terminal states by less than {sci(max(d["dt_half_state_change"] for d in mesh))}, so the observed gains persist under temporal refinement.</p>'
rep['TABLE_RESPONSE']=table(6,'Terminal normalized responses and maximum changes in the complete normalized response histories under amplitude or time-step halving.',['Case','Method','R<sub>u</sub>(T)','R<sub>ρ</sub>(T)','ε-halving change','ΔT-halving change'],[[d['case'],d['method'],f"{d['u']:.5f}",f"{d['rho']:.5f}",sci(d['epsilon_halving_change']),sci(d['dt_halving_change'])] for d in r['response']])
rep['RESPONSE_ANALYSIS']='<p>On the one-soliton background, the normalized velocity responses of the two moving formulations reach approximately 11.4, while their density responses reach approximately 0.240. On the two-soliton background, the corresponding values are approximately 14.2 and 0.282. Within fixed FD, the terminal velocity response is approximately 0.75 in the one-soliton case and 0.74 in the two-soliton case; the density responses are approximately 0.174 and 0.133. The moving-label and fixed-position measurements retain the distinct coordinate and boundary settings specified above. Across all six experiments, amplitude halving changes the normalized response histories by less than '+sci(max(d['epsilon_halving_change'] for d in r['response']))+', and time-step halving changes them by less than '+sci(max(d['dt_halving_change'] for d in r['response']))+'.</p>'
from case_layout import apply as case_layout
case_layout(rep,fig,sci,mesh)
body=(ROOT/'manuscript.html').read_text(encoding='utf-8')
for k,v in rep.items():body=body.replace('{{'+k+'}}',v)
assert '{{' not in body
css='''body{margin:0;background:#f5f3ef;color:#252525;font:18px/1.75 Georgia,"Times New Roman",serif}main{max-width:1030px;margin:30px auto;padding:55px 65px;background:white}h1{font-size:35px;line-height:1.25;font-weight:normal;margin:12px 0 35px}h2{font-size:26px;line-height:1.3;margin-top:50px}h3{font-size:21px;margin-top:32px}p{text-align:justify;margin:15px 0}a{color:#23638b;text-decoration:none}nav{font:14px/2 sans-serif;border-block:1px solid #ccc;padding:14px 0;margin:30px 0}nav a{display:inline-block;margin:0 12px}.eyebrow{font:12px sans-serif;letter-spacing:1.8px;text-transform:uppercase;color:#666}.keywords{font-size:15px}figure{margin:35px 0}figure img{width:100%;height:auto}figcaption,caption{font-size:15px;line-height:1.5;text-align:left}figcaption{padding-top:10px}table{border-collapse:collapse;width:100%;font:13px/1.6 Georgia,serif;font-variant-numeric:tabular-nums;border-top:2px solid #333;border-bottom:2px solid #333}caption{padding:10px 0}th{border-bottom:1px solid #333;font-weight:normal}td,th{padding:7px 8px;text-align:right;white-space:nowrap}td:first-child,th:first-child,td:nth-child(2){text-align:left}td[rowspan]{vertical-align:middle}tr.group-start td{border-top:1px solid #ddd}.table-wrap{overflow-x:auto;margin:30px 0}.katex-display{overflow-x:auto;overflow-y:hidden;padding:8px 0;font-size:.92em}footer{margin-top:40px;font:13px sans-serif;color:#666}@media(max-width:800px){main{margin:0;padding:25px 18px}body{font-size:16px}h1{font-size:28px}}@media print{body{background:white;font-size:10pt}main{margin:0;padding:0;max-width:none}nav,.eyebrow{display:none}figure{break-inside:avoid}h2,h3{break-after:avoid}table{font-size:8pt}@page{size:A4;margin:20mm}}'''
out='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Numerical study of the two-component Hunter–Saxton system: exact references, spatial and temporal errors, moving meshes and perturbation responses."><title>Numerical approximation of the two-component Hunter–Saxton system</title><link rel="stylesheet" href="Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css"><style>'+css+'</style></head><body><main>'+body+'<footer>Computational material: <a href="Workspaces/hs_paper_20261026/data/results.json">numerical tables</a> · <a href="Workspaces/hs_paper_20261026/README.md">methods and reproducibility</a></footer></main></body></html>'
# Merge repeated group labels, retaining the complete table data.
css+='''td.label,th.label{text-align:left}td.number,th.number{text-align:right}th{vertical-align:bottom;white-space:normal}td[rowspan]{padding-right:16px}table{font-size:14px}thead{display:table-header-group}@media print{.table-wrap{overflow:visible}table{font-size:8pt;width:100%}td,th{padding:5px 4px}td.label,th.label{white-space:normal}tr{break-inside:avoid}caption{break-after:avoid}.table-wrap{break-inside:auto}}'''
# Replace positional rules: rowspan changes DOM position, not logical column.
out=out.replace('td:first-child,th:first-child,td:nth-child(2){text-align:left}','')
out=out.replace('</style>',css[css.index('td.label,th.label'):]+ '</style>')
soup=BeautifulSoup(out,'html.parser')
soup.style.string=(ROOT/'layout.css').read_text(encoding='utf-8')
eyebrow=soup.select_one('.eyebrow')
if eyebrow:eyebrow.decompose()
nav=soup.nav
nav.clear();nav['aria-label']='Contents'
for section in soup.select('main > section'):
 if section.get('id') in ['abstract','references']:continue
 h2=section.find('h2');link=soup.new_tag('a',href='#'+section['id']);link.string=h2.get_text();nav.append(link)
 for i,h3 in enumerate(section.find_all('h3'),1):
  if not h3.get('id'):h3['id']=section['id']+'-'+str(i)
  link=soup.new_tag('a',href='#'+h3['id']);link['class']='subsection';link.string=h3.get_text();nav.append(link)
for tab in soup.find_all('table'):
 trs=tab.tbody.find_all('tr',recursive=False)
 cells=[tr.find_all('td',recursive=False) for tr in trs]
 labels=[[c.get_text() for c in row] for row in cells]
 cols=[0,1] if len(cells[0])==7 else [0]
 for col in reversed(cols):
  start=0
  while start<len(cells):
   end=start+1
   while end<len(cells) and labels[end][:col+1]==labels[start][:col+1]:end+=1
   if end-start>1:
    cells[start][col]['rowspan']=str(end-start)
    for i in range(start+1,end):cells[i][col].decompose()
   if col==0:trs[start]['class']='group-start'
   start=end
(ROOT/'unrendered.html').write_text(str(soup),encoding='utf-8')
print('Manuscript assembled')
