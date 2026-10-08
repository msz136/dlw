from pathlib import Path
import time,json,hashlib
import shutil
import nbformat
from nbclient import NotebookClient
HERE=Path(__file__).resolve().parent
archive=HERE/'execution_attempts'/time.strftime('%Y%m%d_%H%M%S')
for name in ('DLW理论.executed.ipynb','execution_validation.json'):
    if (HERE/name).exists():
        archive.mkdir(parents=True,exist_ok=True)
        shutil.copy2(HERE/name,archive/name)
n=nbformat.read(HERE/'DLW理论.input.ipynb',as_version=4)
times=[]
start=time.monotonic()
def before(cell,cell_index,**kwargs):
    print('CELL',cell_index,cell.source.splitlines()[0],flush=True)
def after(cell,cell_index,**kwargs):
    print('FINISHED',cell_index,flush=True)
client=NotebookClient(n,timeout=3600,kernel_name='python3',resources={'metadata':{'path':str(HERE)}},on_cell_execute=before,on_cell_executed=after)
result={'success':False}
try:
    client.execute()
    result['success']=True
finally:
    out=HERE/'DLW理论.executed.ipynb'
    nbformat.write(n,out)
    result.update(seconds=time.monotonic()-start,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),code_cells=sum(c.cell_type=='code' for c in n.cells),errors=[o for c in n.cells if c.cell_type=='code' for o in c.outputs if o.output_type=='error'])
    (HERE/'execution_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False),flush=True)
