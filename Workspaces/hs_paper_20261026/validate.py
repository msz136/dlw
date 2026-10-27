from pathlib import Path
from urllib.parse import unquote,urlparse
import json,re
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent;WS=ROOT.parent.parent
p=WS/'2HS paper.html';s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
missing=[]
for tag in s.find_all(['img','a','link']):
 v=tag.get('src') or tag.get('href','')
 if v and not v.startswith(('#','http','mailto:')) and not (WS/unquote(v)).exists():missing.append(v)
ids=[t['id'] for t in s.find_all(id=True)];assert len(ids)==len(set(ids))
assert not missing,missing
assert not s.select('.katex-error')
assert len(s.find_all('figure'))==10
assert len(s.find_all('table'))==8
assert len(s.find_all('img'))==10
assert not s.find_all('details')
assert [int(re.match(r'Table (\d+)\.',t.caption.get_text()).group(1)) for t in s.find_all('table')]==list(range(1,9))
assert 'a or 螖x' not in s.get_text()
assert all(len(s.find_all('table')[i].select('tbody b'))==2 for i in [4,5])
assert all(len(s.find_all('table')[i].select('tbody b'))==6 for i in [0,1])
for t in s.find_all('table')[:2]:
 assert 'Moving FD' not in t.get_text() and 'Fixed FD' not in t.get_text()
for table in s.find_all('table'):
 headers=table.thead.find_all('th')
 occupied={}
 for row in table.tbody.find_all('tr'):
  col=0
  for cell in row.find_all('td',recursive=False):
   while occupied.get(col,0)>0:col+=1
   assert cell.get('class')==headers[col].get('class'),(col,cell.get_text())
   occupied[col]=int(cell.get('rowspan',1))
   col+=1
  assert all(occupied.get(i,0)>0 for i in range(len(headers)))
  occupied={i:n-1 for i,n in occupied.items() if n>1}
assert '{{' not in s.get_text()
r=json.loads((ROOT/'data/results.json').read_text())
assert len(r['spatial'])==18 and len(r['time'])==18 and len(r['response'])==6
assert all(d['min_rho']>0 for d in r['spatial'])
assert max(v for k,v in r['checks'].items() if k.startswith('rhs_'))<1e-8
assert max(v for k,v in r['checks'].items() if k.startswith('spatial_dt'))<1e-10
assert all(d['dt_halving_change']<1e-7 and d['epsilon_halving_change']<1e-5 for d in r['response'])
formula=json.loads((ROOT/'formula_checks.json').read_text());assert formula['symbolic_rhs_equivalence'] and formula['exact_rational_soliton_samples']==18
mesh=json.loads((ROOT/'data/conserved_mesh.json').read_text())
assert len(mesh)==4
assert all(d['min_h']>0 and d['min_rho']>0 and d['min_Rm']>0 and d['dt_halving_change']<1e-10 for d in mesh)
assert all(len(s.find_all('table')[i].select('tbody tr'))==2 for i in [4,5])
assert 'curvature-adapted' not in s.get_text().lower()
out={'file':str(p),'main_figures':10,'supplementary_time_maps':0,'image_assets':10,'tables':8,'consecutive_table_numbers':True,'spatial_and_mesh_bold_minima':True,'katex_formulas':len(s.select('.katex')),'missing_links':missing,'displayed_spatial_runs':12,'fd_mesh_comparisons':4,'time_refinement_runs':18,'response_configurations':6,'positive_terminal_densities':True,'formula_checks':formula,'passed':True}
(ROOT/'validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
