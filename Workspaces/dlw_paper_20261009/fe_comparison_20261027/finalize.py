from pathlib import Path
import json,subprocess,copy,hashlib
import numpy as np
from PIL import Image
from bs4 import BeautifulSoup
from run_fe import model,norms
R=Path('C:/Users/msz/aca');H=Path(__file__).parent;path=R/'dlw-paper.html'
s=BeautifulSoup(path.read_text(encoding='utf8'),'html.parser')
a=next(a for a in s.find(id='fe-formulation').select('annotation') if 'B_i' in a.get_text())
tex=a.get_text().replace(r'\bigr],dy',r'\bigr]\,dy')
js="const k=require(process.argv[1]);process.stdout.write(k.renderToString(process.argv[2],{displayMode:true,throwOnError:true}));"
r=subprocess.run(['node','-e',js,str(R/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js'),tex],capture_output=True,text=True,encoding='utf8',check=True)
a.find_parent(class_='katex-display').replace_with(BeautifulSoup(r.stdout,'html.parser'))
for node in list(s.find_all(string=True)):
 if node.parent.name in ['annotation','style','script']:continue
 text=str(node).replace('nonlinear products are evaluated at the grid points','nonlinear terms are evaluated at the x grid points')
 text=text.replace('while Centered-SD gives smaller terminal errors in both fields in the soliton tests.','while Centered-SD gives smaller terminal errors than Endpoint-SD in both fields in the soliton tests. FE gives the smallest second-field error throughout the comparison, and its common first equation with FD makes the influence of the second-field approximation visible in their subsequent evolution.')
 if text!=str(node):node.replace_with(text)
for i,f in enumerate(s.find_all('figure'),1):
 if 5<=i<=8:continue
 for a in f.find_all('a'):
  if a.get('href','').endswith('.pdf'):a['href']=f'pdf/dlw/images/figure-{i:02}.pdf'
style=s.new_tag('style');style['id']='fe-table-layout';style.string='#table-initial td,#table-final td{white-space:nowrap} #table-initial,#table-final{font-size:13px} @media print{#table-initial,#table-final{font-size:8pt} #table-initial td,#table-final td,#table-initial th,#table-final th{padding:5pt 3pt}}';s.head.append(style)
# Reuse the print-row refresh, independent of publication text/table edits.
code=(H/'publish.py').read_text(encoding='utf8');part=code[code.index("rows=H/'print_rows'"):code.index("(H/'publication.json')")];exec(part)
checks=[]
for c in ['A','D','Gaussian','Sinusoidal']:
 d=np.load(H/f'{c}.npz');d2=np.load(H/f'{c}_halfdt.npz');m=model(c);rec=json.loads((H/f'{c}.json').read_text())
 err=norms(m,d['z']-d['ref']);diff=norms(m,d['z']-d2['z'])
 assert np.allclose(err,rec['error'],rtol=0,atol=1e-15)
 baseline=H.parent/'report_refresh_20261024'/('rk4_spatial' if c in ['A','D'] else 'nondegenerate_rk4_20261024')/f'{c}_FD_RK4.npz'
 fd=np.load(baseline);assert np.array_equal(d['x'],fd['x']) and np.array_equal(d['y'],fd['y']) and np.max(abs(d['z0']-fd['z0']))<1e-13
 checks.append(dict(case=c,recomputed_error=err,half_dt_field_difference=diff,half_dt_relative_to_error=(np.array(diff)/err).tolist(),FD_same_nodes_and_initial_fields=True))
for name in ['table-initial','table-final']:
 tb=s.find(id=name)
 for tr in tb.tbody.find_all('tr'):
  td=tr.find_all('td');assert len(td)==8
  for j in [0,1]:
   vals=[float(td[k]['data-value']) for k in range(j,8,2)];best=np.argmin(vals)
   assert [k for k in range(4) if td[2*k+j].strong]==[best]
assert len(s.find_all('figure'))==14 and len(s.find_all('table'))==8
assert hashlib.sha256((R/'pdf/dlw/main.tex').read_bytes()).digest()==hashlib.sha256((H/'tex_sync_source.tex').read_bytes()).digest()
manifest=dict(checks=checks,figures=14,tables=8,tex_unchanged=True,assembly=json.loads((H/'assembly_validation.json').read_text()),sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [H/'run_fe.py',H/'check_fe.py',H/'tex_sync_source.tex']})
(H/'validation.json').write_text(json.dumps(manifest,indent=2),encoding='utf8');print(json.dumps(checks,indent=2))
# Focused reading copy: algorithm + full spatial experiment, same content as paper.
preview=BeautifulSoup('<!doctype html><html lang="en"><head></head><body></body></html>','html.parser')
preview.head.replace_with(copy.deepcopy(s.head));preview.title.string='DLW: finite-element comparison'
title=preview.new_tag('h1');title.string='DLW: finite-element spatial comparison';preview.body.append(title)
for id in ['section-4.1','section-5.2']:preview.body.append(copy.deepcopy(s.find(id=id)))
for tag in preview.find_all(['img','a','link']):
 key='src' if tag.name=='img' else 'href';v=tag.get(key,'')
 if v and not v.startswith(('http','#','/','data:')):tag[key]='../'+v
(R/'report/dlw_fe_comparison_20261027.html').write_text(str(preview),encoding='utf8')
