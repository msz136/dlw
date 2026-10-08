from pathlib import Path
import json,hashlib,shutil,re
import nbformat
from notebook_prose import revise
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
backup=HERE/'before_prose_revision'
backup.mkdir(exist_ok=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
paths=[ROOT/'notebook/DLW理论.ipynb',HERE/'DLW理论.executed.ipynb',HERE/'DLW理论.input.ipynb']
records=[]
for p in paths:
    saved=backup/p.name
    assert not saved.exists(),'Revision already applied'
    shutil.copy2(p,saved)
    n=nbformat.read(p,as_version=4)
    code_before={c.id:json.dumps(c,ensure_ascii=False,sort_keys=True) for c in n.cells if c.cell_type=='code'}
    original_count=len(n.cells)
    n.cells=revise(n.cells)
    code_after={c.id:json.dumps(c,ensure_ascii=False,sort_keys=True) for c in n.cells if c.cell_type=='code'}
    assert code_before==code_after
    nbformat.validate(n)
    nbformat.write(n,p)
    records.append({'path':str(p.relative_to(ROOT)),'before_sha256':digest(saved),'after_sha256':digest(p),'cells_before':original_count,'cells_after':len(n.cells),'code_cells_unchanged':len(code_after)})
assert paths[0].read_bytes()==paths[1].read_bytes()
source='\n'.join(c.source for c in n.cells if c.cell_type=='markdown')
tags=re.findall(r'\\tag\{([^}]+)\}',source)
refs=re.findall(r'（([A-Z]\d+)）',source)
assert len(tags)==len(set(tags))
assert set(refs)<=set(tags),set(refs)-set(tags)
assert source.index(r'\tag{T11}')<source.index(r'\tag{T13}')<source.index(r'\tag{T12}')<source.index(r'\tag{T7}')
for unwanted in ('**运行证明。**','明确列出','反向恢复 τ 函数','Lean 中 `PowBound','不是一般初值问题的通解','下面将此展开作为','下面展开任意 N 双线性链的 Lean','Mᵢₖ','P=diag','Hₓ='):
    assert unwanted not in source,unwanted
# Symmetric Taylor coefficients in the expanded S2 proof.
import sympy as s
x,h=s.symbols('x h')
v=s.symbols('v0:5')
poly=sum(v[i]*x**i/s.factorial(i) for i in range(5))
avg=s.expand((poly.subs(x,h/2)+poly.subs(x,-h/2))/2)
dif=s.expand((poly.subs(x,h/2)-poly.subs(x,-h/2))/h)
assert s.expand(avg-v[0]-h**2*v[2]/8-h**4*v[4]/384)==0
assert s.expand(dif-v[1]-h**2*v[3]/24)==0
record={'files':records,'code_and_saved_outputs_identical':True,'lean_reexecuted':False,'S2_coefficients':'exact symbolic check passed','equation_references':'all resolve','html_untouched_sha256':digest(ROOT/'report/dlw_theory.html')}
(HERE/'notebook_prose_validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ('execution_validation.json','delivery_validation.json'):
    p=HERE/name
    shutil.copy2(p,backup/name)
    r=json.loads(p.read_text(encoding='utf-8'))
    r['before_prose_revision_sha256']=r['sha256']
    r['sha256']=digest(paths[1])
    if 'delivery_sha256' in r:r['delivery_sha256']=digest(paths[0])
    r['prose_revision']='Only Markdown changed and independent interaction cell moved; all code cells, execution counts and outputs unchanged. No new Lean run.'
    p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(record,ensure_ascii=False))
