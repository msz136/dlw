from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
import re,json,hashlib
import numpy as np

HERE=Path(__file__).resolve().parent
old=(HERE/'before_full_comparison_revision/manuscript.md').read_text(encoding='utf-8')
new=(HERE/'manuscript.md').read_text(encoding='utf-8')
def equations(t):
    return {m[1]:re.sub(r'\\tag\{[^}]+\}','',m[0]) for m in re.finditer(r'\$\$[\s\S]*?\\tag\{([^}]+)\}[\s\S]*?\$\$',t)}
# Match each numbered math block independently, avoiding unnumbered blocks.
def numbered(t):
    return {re.search(r'\\tag\{([^}]+)\}',x)[1]:re.sub(r'\\tag\{[^}]+\}','',x) for x in re.findall(r'\$\$[\s\S]*?\$\$',t) if r'\tag{' in x}
oe,ne=numbered(old),numbered(new)
for k,v in oe.items():
    if k!='7':assert v in ne.values(),k
assert [int(t) for t in re.findall(r'\\tag\{(\d+)\}',new)]==list(range(1,76))
tables=json.loads((HERE/'tables.json').read_text(encoding='utf-8'))
out=BeautifulSoup(new,'html.parser').select('table.comparison')
assert len(out)==3
count=0
for key,t in zip(['space_table','time_table','mesh_table'],out):
    original=re.findall(r'\d+\.\d+e[+-]\d+',BeautifulSoup(tables[key],'html.parser').get_text())
    actual=re.findall(r'\d+\.\d+e[+-]\d+',t.get_text(' '))
    assert Counter(original)==Counter(actual),key
    count+=len(original)
assert count==108 and len(out[2].select('tbody tr'))==9
assert '## 附录' not in new and 'SD2' not in new
assert not any(ord(c)<32 and c not in '\r\n\t' for c in new)
manifest=json.loads((HERE/'comparison_fields/manifest.json').read_text(encoding='utf-8'))
stats=json.loads((HERE/'figures/plot_validation.json').read_text(encoding='utf-8'))
assert len(stats['stats'])==36
for r in manifest['records']:
    d=np.load(r['source'])
    assert all(np.isfinite(d[k]).all() for k in ['u','v','exact_u','exact_v'])
    assert d['u'].shape==d['v'].shape==(len(d['y']),len(d['x']))
for case in 'ABC':
    for kind in ['fields','errors']:
        for ext in ['png','pdf','py']:
            assert (HERE/f'figures/{case}_{kind}.{ext}').stat().st_size>0
result=dict(numbered_equations=75,prior_numbered_equations_preserved_except_inline_lambda=True,
    original_error_values_preserved=count,paired_mesh_table_rows=9,figures=6,panels_per_figure=12,
    methods=['PE','PF','FD'],PF_cached_runs_reused=3,missing_PE_FD_runs_computed=6,
    original_comparison_experiments_rerun=False,notebook_unchanged=manifest['notebook_unchanged'],
    source_sha256=hashlib.sha256(new.encode()).hexdigest())
(HERE/'full_comparison_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
