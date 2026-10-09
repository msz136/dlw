from pathlib import Path
import json, hashlib, re, base64
from bs4 import BeautifulSoup
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
path=ROOT/'notebook/DLW数值分析report.ipynb'
nb=json.loads(path.read_text(encoding='utf-8'))
ns={'display':lambda *args,**kwargs:None}
for i,c in enumerate(nb['cells']):
    if c['cell_type']=='code' and i<=27:
        source=''.join(c['source']).replace('from IPython.display import display','')
        exec(compile(source,f'notebook-cell-{i}','exec'),ns)
rows=[]
for k,r in ns['results'].items():
    assert r['completed']
    rows.append({v:r[v] for v in ('case','model','method','mesh','reached','initial_error','min_J','max_errors')})
tables={}
for name in ('space_table','time_table','mesh_table'):
    tables[name]=ns[name].to_html(float_format=lambda x:f'{x:.6e}',border=0)
tables['order_table']=ns['pd'].DataFrame(ns['order_rows']).to_html(index=False,float_format=lambda x:f'{x:.6e}',border=0)
(HERE/'tables.json').write_text(json.dumps(tables,ensure_ascii=False,indent=2),encoding='utf-8')
# Compare saved display values with fresh evaluations, retaining the notebook untouched.
comparisons=[]
for cell,name in [(21,'space_table'),(23,'time_table'),(27,'mesh_table')]:
    output=next(o for o in nb['cells'][cell]['outputs'] if 'text/html' in o.get('data',{}))
    soup=BeautifulSoup(''.join(output['data']['text/html']),'html.parser')
    values=[float(td.get_text()) for td in soup.select('td.data')]
    actual=ns[name].to_numpy().ravel()
    assert len(values)==len(actual)
    assert np.allclose(values,actual,rtol=5.1e-4,atol=1e-12)
    comparisons.append({'cell':cell,'numeric_values':len(values),'matches_saved_4_significant_digits':True})
figures=[]
for i,o in enumerate(nb['cells'][36].get('outputs',[])):
    data=o.get('data',{}).get('image/png')
    if data:
        p=HERE/f'figure_{len(figures)+1}.png'
        p.write_bytes(base64.b64decode(''.join(data)))
        figures.append(p.name)
record={'source':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'runs':rows,'main_count':len(rows),'refinement_runs':ns['refinement_rows'],'orders':ns['order_rows'],'saved_table_comparison':comparisons,'figures_from_saved_notebook':figures}
(HERE/'numerical_validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'main_runs':len(rows),'refinement_runs':len(ns['refinement_rows']),'saved_comparison':comparisons,'figures':len(figures)}))
