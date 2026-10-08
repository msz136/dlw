from pathlib import Path
import sys, shutil, json
import nbformat
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'Workspaces/notebook_reports_20261006'))
from static_field_plots import apply_dlw, apply_hs
backup=HERE/'before_notebook_integration'
backup.mkdir(exist_ok=True)
files=['notebook/DLW数值分析report.ipynb','notebook/2HS数值分析report.ipynb','dlw_numerical.html',
       'Workspaces/notebook_reports_20261006/build_dlw_numerics_notebook.py',
       'Workspaces/notebook_reports_20261006/build_hs_notebook.py',
       'Workspaces/dlw_notebook_static_20261007/build_static.py',
       'Workspaces/dlw_notebook_static_20261007/verify_static.py']
for name in files:
    source=ROOT/name;target=backup/name
    if not target.exists():
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
for name,transform in [('DLW',apply_dlw),('2HS',apply_hs)]:
    path=ROOT/f'notebook/{name}数值分析report.ipynb'
    nb=transform(nbformat.read(path,4))
    for c in nb.cells:
        if c.cell_type=='code':
            compile(c.source,c.id,'exec')
            c.outputs=[];c.execution_count=None
    nbformat.validate(nb);nbformat.write(nb,path)
    print(name,len(nb.cells))
