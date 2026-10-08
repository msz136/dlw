from pathlib import Path
import json,hashlib,shutil
import nbformat
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
paths=[HERE/'DLW理论.input.ipynb',HERE/'DLW理论.executed.ipynb',ROOT/'notebook/DLW理论.ipynb']
for i,p in enumerate(paths):
    backup=HERE/'before_metadata'/str(i)/p.name
    backup.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(p,backup)
    n=nbformat.read(p,as_version=4)
    original_cells=json.dumps(n.cells,ensure_ascii=False,sort_keys=True)
    n.metadata['title']='DLW 理论'
    n.metadata.setdefault('colab',{})['name']='DLW理论.ipynb'
    n.metadata['report_history']={k:n.metadata.pop(k) for k in ('report_conversion','report_split') if k in n.metadata}
    n.metadata['report_theory']={'title':'DLW 理论','scope':'Continuous DLW, exact semidiscrete Gram tau, nonlinear reconstruction and continuum limits','builder':'Workspaces/dlw_theory_notebook_20261008/build.py'}
    nbformat.write(n,p)
    assert json.dumps(nbformat.read(p,as_version=4).cells,ensure_ascii=False,sort_keys=True)==original_cells
digest=hashlib.sha256(paths[1].read_bytes()).hexdigest()
assert paths[1].read_bytes()==paths[2].read_bytes()
for name in ('execution_validation.json','delivery_validation.json'):
    p=HERE/name
    r=json.loads(p.read_text(encoding='utf-8'))
    r['executed_sha256_before_metadata']=r['sha256']
    r['sha256']=digest
    if 'delivery_sha256' in r:r['delivery_sha256']=digest
    r['metadata_revision']='Colab name and provenance updated; every cell, execution count and output unchanged'
    p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print('Colab title updated; all executed cells and outputs preserved:',digest)
