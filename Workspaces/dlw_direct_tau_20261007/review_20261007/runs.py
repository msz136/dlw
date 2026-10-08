"""Replay the live SD defaults and check moving-grid time refinement."""
from pathlib import Path
import os,sys,json,time,hashlib
os.environ.setdefault('MPLBACKEND','Agg')
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
nbpath=ROOT/'notebook/DLW数值分析report.ipynb'
nb=json.loads(nbpath.read_text('utf-8'))
cells={c['id']:''.join(c['source']) for c in nb['cells']}
ns={'__name__':'live_SD_replay'}
for key in ('imports','config','reference','spatial','sd_fd','sd2_lift','sd2_evolution','sd','fd','mesh','time'):
    exec(cells['dlw-'+key],ns)
saved=json.loads((ROOT/'Workspaces/notebook_reports_20261006/dlw_numeric_results.json').read_text('utf-8'))
saved={(r['case'],r['mesh']):r for r in saved['rows'] if r['model']=='SD'}
output={'notebook_sha256':hashlib.sha256(nbpath.read_bytes()).hexdigest(),'replays':[],'moving_time_order':[]}
target=Path(__file__).with_name('runs.json')
def save():
    target.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for case in ns['CASES']:
    for mesh in ('fixed','moving'):
        start=time.perf_counter()
        r=ns['solve'](case,'SD','Midpoint',mesh)
        difference=max(abs(r['max_errors'][f]-saved[case,mesh]['errors'][f]) for f in ('u','v'))
        row={k:r[k] for k in ('case','mesh','completed','reached','reason','initial_error','max_errors','min_J')}
        row['completed']=bool(row['completed'])
        row.update(saved_max_error_difference=difference,seconds=time.perf_counter()-start)
        output['replays'].append(row);save();print(json.dumps(row),flush=True)
fields=[]
for divisor in (1,2,4):
    r=ns['solve']('A','SD','Midpoint','moving',dict(ns['CONFIG'],T=.002,dt=.000125/divisor))
    assert r['completed'],r['reason']
    fields.append(r['fields'])
for k,f in enumerate(('u','v')):
    d1=float(abs(fields[0][k]-fields[1][k]).max())
    d2=float(abs(fields[1][k]-fields[2][k]).max())
    output['moving_time_order'].append(dict(case='A',T=.002,field=f,full_half=d1,half_quarter=d2,order=float(np.log2(d1/d2))))
save();print(json.dumps(output['moving_time_order']),flush=True)
