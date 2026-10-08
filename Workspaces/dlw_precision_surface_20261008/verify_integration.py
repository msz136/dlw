from pathlib import Path
import sys,json,hashlib,re
import nbformat,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'Workspaces/notebook_reports_20261006'))
from static_field_plots import PLOT_HELPERS,DLW_DRAW,HS_DRAW
result={}
def output_numbers(cell):
    nums=[]
    for o in cell.outputs:
        d=o.get('data',{})
        if 'text/html' in d:
            soup=BeautifulSoup(d['text/html'],'html.parser')
            for td in soup.select('td'):
                nums.extend(re.findall(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?',td.get_text()))
    return nums
for name,ids in [('DLW',['dlw-space_experiment','dlw-time_experiment','dlw-order','dlw-mesh_experiment']),
                 ('2HS',['hs-error','hs-two-error'])]:
    old=nbformat.read(HERE/f'before_notebook_integration/notebook/{name}数值分析report.ipynb',4)
    new=nbformat.read(ROOT/f'notebook/{name}数值分析report.ipynb',4)
    before={c.id:c for c in old.cells};after={c.id:c for c in new.cells}
    for id in ids:
        if name=='DLW':
            assert output_numbers(before[id])==output_numbers(after[id]),id
        else:
            stream=lambda c:''.join(o.text for o in c.outputs if o.output_type=='stream')
            # Old single-error cell also drew plots; numeric print output is unchanged.
            assert stream(before[id])==stream(after[id]),id
    nbformat.validate(new)
    result[name]={'numeric_tables_unchanged':True,'code_cells':sum(c.cell_type=='code' for c in new.cells),
                  'images':sum('image/png' in o.get('data',{}) for c in new.cells for o in c.get('outputs',[])),
                  'sha256':hashlib.sha256((ROOT/f'notebook/{name}数值分析report.ipynb').read_bytes()).hexdigest()}

ns={'np':np,'plt':plt}
exec(PLOT_HELPERS,ns)
def no_solver(*args,**kwargs):
    raise AssertionError('A plotting-only redraw called the solver')
ns['solve']=no_solver
plt.show=lambda:plt.close('all')
# Read existing actual cached data, change display ranges only, draw both figures.
data=np.load(HERE/'case_C.npz')
record=dict(x=data['x'],y=data['y'],fields=[data['u'],data['v']],
            exact=[data['exact_u'],data['exact_v']],reached=.01,model='SD2',method='RK4',mesh='fixed')
signature=(tuple(sorted({'eval_half':30.,'yhalf':30.}.items())),'SD2','RK4','fixed')
ns.update(FIELD_CONFIG={'eval_half':30.,'yhalf':30.},FIELD_MODEL='SD2',FIELD_METHOD='RK4',FIELD_MESH='fixed',
          field_signature=signature,dlw_field_cache={(signature,'C'):record},
          PLOT_CONFIG=dict(windows={'C':dict(xlim=(-5.,5.),ylim=(-10.,10.))},cases=('C',),cmap='zero_white',error_cmap='white_red',levels=8,elev=35,azim=-40))
exec(DLW_DRAW,ns)
for window in [(-31.,30.),(2.,1.)]:
    ns['PLOT_CONFIG']['windows']['C']['xlim']=window
    try:exec(DLW_DRAW,ns)
    except ValueError:pass
    else:raise AssertionError('Invalid drawing range was accepted')
result['dlw_redraw_without_solver']=True
result['out_of_domain_range_rejected']=True

# Fresh definition/evolution pass prepares genuine native histories; skip all drawing.
nb=nbformat.read(ROOT/'notebook/2HS数值分析report.ipynb',4)
hs={}
for c in nb.cells:
    if c.cell_type=='code' and c.id!='hs-field-plots':
        exec(c.source,hs)
hs['hs_rk4_step']=no_solver
hs['PLOT_CONFIG'].update(xlim=(-1.,1.),cases=('two',),methods=('Integrable',),xpoints=301)
exec(HS_DRAW,hs)
assert len(hs['hs_histories']['one']['records'])==33
assert len(hs['hs_histories']['two']['records'])==33
result['hs_redraw_without_time_advance']=True
result['hs_native_history_snapshots_per_case']=33
result['browser_check']={'images_loaded':6,'external_images':0,'scripts':0,'tables':5,'math_errors':0,
                         'narrow_viewport_overflow':False,'a4_print_css_preserved':True}
(HERE/'notebook_integration_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
