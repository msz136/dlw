"""Execute the delivered notebook in a fresh project kernel and validate results."""
from pathlib import Path
import hashlib
import json
import os
import sys
import time
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PATH = ROOT/'notebook/DLW数值分析report.ipynb'
nb = nbformat.read(PATH, as_version=4)
source_hashes = {c.id:hashlib.sha256(c.source.encode()).hexdigest() for c in nb.cells}
backup = HERE/'before_dlw_execute.ipynb'
if not backup.exists():
    backup.write_bytes(PATH.read_bytes())
export = f'''from pathlib import Path
import json
rows = [dict(case=r['case'], model=r['model'], method=r['method'], mesh=r['mesh'],
    completed=bool(r['completed']), reached=float(r['reached']),
    errors=r['max_errors'], initial_error=r['initial_error'], min_J=r['min_J'])
    for r in results.values()]
Path({str(HERE/'dlw_numeric_results.json')!r}).write_text(
    json.dumps(dict(rows=rows, order_rows=order_rows, refinement_rows=refinement_rows,
        source_hashes={source_hashes!r}), indent=2), encoding='utf-8')
archive = {{}}
for key, r in results.items():
    label = '_'.join(key)
    archive[label+'_x'] = r['x']
    for field in ('u', 'v'):
        archive[label+'_'+field+'_curve'] = r['errors'][field].max(axis=0)
np.savez_compressed({str(HERE/'dlw_numeric_curves.npz')!r}, **archive)
'''
nb.cells.append(nbformat.v4.new_code_cell(export, id='dlw-validation-export'))
km = KernelManager(kernel_name='python3')
km.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
timings, starts = [], {}
def start_cell(cell, cell_index, **kwargs):
    if cell.cell_type == 'code':
        starts[cell.id] = time.perf_counter()
        print('Executing', cell.id, flush=True)
def end_cell(cell, cell_index, **kwargs):
    if cell.cell_type == 'code':
        seconds = round(time.perf_counter()-starts[cell.id], 3)
        timings.append(dict(cell=cell.id, seconds=seconds))
        print('Executed', cell.id, seconds, flush=True)
client = NotebookClient(nb, km=km, timeout=600, startup_timeout=60, allow_errors=False,
    resources={'metadata':{'path':str(PATH.parent)}}, on_cell_start=start_cell,
    on_cell_executed=end_cell)
began, failure = time.perf_counter(), None
try:
    client.execute(env={**os.environ, 'MPLBACKEND':'module://matplotlib_inline.backend_inline'})
except BaseException as error:
    failure = dict(type=type(error).__name__, message=str(error))
nb.cells.pop()
assert source_hashes == {c.id:hashlib.sha256(c.source.encode()).hexdigest() for c in nb.cells}
nbformat.validate(nb)
nbformat.write(nb, PATH)
codes = [c for c in nb.cells if c.cell_type == 'code']
errors = [{'cell':c.id,'name':o.ename,'message':o.evalue}
          for c in codes for o in c.outputs if o.output_type=='error']
validation = dict(notebook=str(PATH), notebook_sha256=hashlib.sha256(PATH.read_bytes()).hexdigest(),
    python=sys.executable, independent_native_kernel=True, code_cells=len(codes),
    executed_cells=sum(c.execution_count is not None for c in codes),
    seconds=round(time.perf_counter()-began, 3), success=failure is None and not errors,
    failure=failure, errors=errors, sources_unchanged=True, outputs_saved=True,
    image_outputs=sum('image/png' in o.get('data', {}) for c in codes for o in c.outputs),
    timings=timings, source_hashes=source_hashes,
    exported_results_sha256=hashlib.sha256((HERE/'dlw_numeric_results.json').read_bytes()).hexdigest() if failure is None else None,
    exported_curves_sha256=hashlib.sha256((HERE/'dlw_numeric_curves.npz').read_bytes()).hexdigest() if failure is None else None)
(HERE/'dlw_execution_validation.json').write_text(json.dumps(validation, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k:validation[k] for k in ('success','code_cells','seconds','image_outputs')}, ensure_ascii=False), flush=True)
if failure or errors:
    raise RuntimeError(failure or errors)
