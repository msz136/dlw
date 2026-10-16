from pathlib import Path
import json
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
nb = json.loads((ROOT/'notebook'/'DLW数值分析report.ipynb').read_text(encoding='utf-8'))
ns = {'__name__': '__audit__'}
for cell in nb['cells'][:20]:
    if cell['cell_type'] == 'code':
        # The shell harness does not require the notebook-only display hook.
        source = ''.join(cell['source']).replace('from IPython.display import display',
                                                'display = lambda *args, **kwargs: None')
        exec(source, ns)
cfg = dict(ns['CONFIG'], L=80., nx=512, yhalf=30., eval_half=30., eval_points=1201)
windows = {'A': ((-3.,4.),(-3.,3.)), 'B': ((-30.,30.),(-30.,30.)),
           'C': ((-30.,30.),(-30.,30.))}
rows = []
for case, (xlim, ylim) in windows.items():
    start = time.perf_counter()
    r = ns['solve'](case,'SD2','RK4','fixed',cfg)
    xm = (r['x']>=xlim[0])&(r['x']<=xlim[1])
    ym = (r['y']>=ylim[0])&(r['y']<=ylim[1])
    mask = np.ix_(ym,xm)
    row = {'case':case,'completed':bool(r['completed']),'reached':r['reached'],
           'initial_error':r['initial_error'],'min_J':r['min_J'],
           'config':cfg,'window':{'x':xlim,'y':ylim},'fields':{},
           'seconds':time.perf_counter()-start}
    for i, field in enumerate(('u','v')):
        num, exact = r['fields'][i][mask], r['exact'][i][mask]
        row['fields'][field] = {'numerical_min':float(num.min()),'numerical_max':float(num.max()),
                                'exact_min':float(exact.min()),'exact_max':float(exact.max()),
                                'max_error':float(abs(num-exact).max())}
    rows.append(row)
    print(json.dumps(row,ensure_ascii=False),flush=True)
(OUT/'wide_field_evidence.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
