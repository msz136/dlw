"""Review the live notebook without changing its cells or saved outputs."""
from pathlib import Path
import os
os.environ.setdefault('MPLBACKEND', 'Agg')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import sys, json, hashlib, time
import numpy as np
ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT/'Workspaces/notebook_reports_20261006'
sys.path.insert(0, str(SOURCE))
from verify_dlw_tau import audit_step
nbpath = ROOT/'notebook/DLW数值分析report.ipynb'
nb = json.loads(nbpath.read_text('utf-8'))
cells = {c['id']: ''.join(c['source']) for c in nb['cells']}
ns = {'__name__': 'review_live_notebook'}
for key in ('imports','config','reference','spatial','sd_fd','sd2_lift',
            'sd2_evolution','sd','fd','mesh','time'):
    exec(cells['dlw-'+key], ns)
from sd_tau_cell import CELLS_SD
result = {'notebook_sha256': hashlib.sha256(nbpath.read_bytes()).hexdigest(),
          'live_SD_matches_generator': cells['dlw-sd'].strip()==CELLS_SD.strip()}
result['one_step'] = [audit_step(ns,c,m) for c in ns['CASES'] for m in ('fixed','moving')]
from scipy.interpolate import CubicSpline
rows = []
for nx in (128,255,256,257,512):
    for case in ('A','B','C'):
        row = {'nx':nx,'case':case}
        try:
            p = ns['Problem'](case,'SD','fixed',dict(ns['CONFIG'],nx=nx))
            z = p.initial()
            u,v = p.fields(z,0.)
            eu,ev = p.m.G.uv(p.m.js,p.X.x,0.)
            mask = abs(p.X.x)<=10
            row['initial_node_error'] = max(float(abs(f[:,mask]-g[:,mask]).max()) for f,g in ((u,eu),(v,ev)))
            a,b = p.m.unpack(z[:-nx])
            aa,bb = p.m.analytic_tau(p.X.x,0.)
            row['lift_log_tau_correction'] = max(float(abs(a-aa).max()),float(abs(b-bb).max()))
            xx = np.linspace(-10,10,4001)
            e = p.m.G.uv(p.m.js,xx,0.)
            row['initial_interpolated_error'] = {k:float(abs(CubicSpline(p.X.x,f,axis=-1)(xx)-g).max()) for k,f,g in zip(('u','v'),(u,v),e)}
            q = p.m.step(0.,z,ns['CONFIG']['dt'],'fixed')
            row['one_step_finite'] = bool(np.isfinite(q).all())
            row['maximum_log_tau_state'] = float(abs(z[:-nx]).max())
        except Exception as exc:
            row['error'] = type(exc).__name__+': '+str(exc)
        rows.append(row)
result['initial_lift_grid_checks'] = rows
Path(__file__).with_name('audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'live_matches':result['live_SD_matches_generator'],'initial_lift_grid_checks':rows},ensure_ascii=False,indent=2),flush=True)
