from pathlib import Path
import sys,json,shutil,os,time
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'Workspaces/notebook_reports_20261006'))
import static_field_plots as source
backup=HERE/'before_white_background'
backup.mkdir(exist_ok=True)
for name in ('DLW数值分析report.ipynb','2HS数值分析report.ipynb'):
    path=ROOT/'notebook'/name
    if not (backup/name).exists():shutil.copy2(path,backup/name)
if not (backup/'dlw_numerical.html').exists():shutil.copy2(ROOT/'dlw_numerical.html',backup/'dlw_numerical.html')
for name,prefix in [('DLW','dlw'),('2HS','hs')]:
    path=ROOT/f'notebook/{name}数值分析report.ipynb'
    nb=nbformat.read(path,4)
    for cell in nb.cells:
        if cell.id==prefix+'-field-config':cell.source=source.DLW_CONFIG.strip() if name=='DLW' else source.HS_CONFIG.strip()
        if cell.id==prefix+'-field-helpers':cell.source=source.PLOT_HELPERS.strip()
        if cell.id=='dlw-field-plots':cell.source=source.DLW_DRAW.strip()
        if cell.id=='dlw-field-text':
            fresh=source.apply_dlw(nbformat.v4.new_notebook(cells=[]))
            cell.source=next(c.source for c in fresh.cells if c.id=='dlw-field-text')
    nbformat.write(nb,path)

path=ROOT/'notebook/DLW数值分析report.ipynb'
nb=nbformat.read(path,4)
lookup={c.id:c for c in nb.cells}
# Unchanged numerical algorithms: caches are the same genuine wide-domain runs.
previous=nbformat.read(HERE/'before_notebook_integration/notebook/DLW数值分析report.ipynb',4)
for cell in previous.cells:
    if cell.cell_type=='code' and cell.id not in ('dlw-config','dlw-curves'):
        assert lookup[cell.id].source==cell.source,cell.id
bootstrap=f'''from pathlib import Path
import json
cache_dir=Path({str(HERE)!r})
FIELD_CONFIG=dict(CONFIG,L=80.,nx=512,yhalf=30.,eval_half=30.,eval_points=1201)
FIELD_MODEL,FIELD_METHOD,FIELD_MESH='SD2','RK4','fixed'
field_signature=(tuple(sorted(FIELD_CONFIG.items())),FIELD_MODEL,FIELD_METHOD,FIELD_MESH)
dlw_field_cache={{}}
for case in CASES:
    cached=np.load(cache_dir/f'case_{{case}}.npz')
    meta=json.loads((cache_dir/f'case_{{case}}.json').read_text())
    for key in FIELD_CONFIG:
        assert meta['config'][key]==FIELD_CONFIG[key],key
    dlw_field_cache[field_signature,case]=dict(x=cached['x'],y=cached['y'],
        fields=[cached['u'],cached['v']],exact=[cached['exact_u'],cached['exact_v']],
        model='SD2',method='RK4',mesh='fixed',reached=.01)
'''
ids=['dlw-field-config','dlw-field-helpers','dlw-field-plots']
temp=nbformat.v4.new_notebook(cells=[lookup['dlw-imports'],lookup['dlw-config'],nbformat.v4.new_code_cell(bootstrap,id='cache-bootstrap')]+[lookup[id] for id in ids])
km=KernelManager(kernel_name='python3')
km.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
started=time.perf_counter()
NotebookClient(temp,km=km,timeout=600,allow_errors=False,resources={'metadata':{'path':str(ROOT)}}).execute(env={**os.environ,'MPLBACKEND':'module://matplotlib_inline.backend_inline'})
for id in ids:
    updated=next(c for c in temp.cells if c.id==id)
    lookup[id].outputs=updated.outputs
    lookup[id].metadata=updated.metadata
nbformat.validate(nb);nbformat.write(nb,path)
(HERE/'style_execution.json').write_text(json.dumps({'success':True,'seconds':time.perf_counter()-started,'numerical_cache_reused':True,'unchanged_numerical_algorithms_checked':True,'updated_cells':ids},indent=2),encoding='utf-8')
print('DLW static images redrawn; numerical cache reused.',flush=True)
