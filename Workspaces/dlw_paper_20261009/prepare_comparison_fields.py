"""Reuse PF cache; compute only six missing PE/FD wide-domain fields."""
from pathlib import Path
import json,hashlib,time
import numpy as np
import matplotlib
matplotlib.use('Agg')

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'comparison_fields';OUT.mkdir(exist_ok=True)
nbpath=ROOT/'notebook/DLW数值分析report.ipynb'
before=hashlib.sha256(nbpath.read_bytes()).hexdigest()
nb=json.loads(nbpath.read_text(encoding='utf-8'))
cells={c['id']:''.join(c['source']) for c in nb['cells']}
ns={}
for name in ('imports','config','reference','spatial','sd_fd','sd','sd2_lift','sd2_evolution','fd','mesh','time'):
    exec(cells['dlw-'+name].replace('from IPython.display import display', 'display = lambda *args, **kwargs: None'),ns)
config=dict(ns['CONFIG'],L=80.,nx=512,yhalf=30.,eval_half=30.,eval_points=1201)
records=[]
for case in 'ABC':
    cache=ROOT/f'Workspaces/dlw_precision_surface_20261008/case_{case}.npz'
    meta=json.loads(cache.with_suffix('.json').read_text(encoding='utf-8'))
    data=np.load(cache)
    for k in ['a','h','yhalf','L','nx','dt','T','eval_half','eval_points']:assert meta['config'][k]==config[k]
    exact=ns['Exact'](case,config['h'],config['a']).uv(data['y']/config['h']-.5,data['x'],config['T'])
    assert all(np.allclose(x,data['exact_'+f],rtol=1e-12,atol=1e-13) for x,f in zip(exact,['u','v']))
    records.append(dict(case=case,method='PF',source=str(cache),reused=True,metadata=meta))
    for method,model in [('PE','SD'),('FD','FD')]:
        dest=OUT/f'{case}_{method}.npz';mp=dest.with_suffix('.json')
        if dest.exists():
            info=json.loads(mp.read_text());assert info['config']==config and info['source_sha256']==before
        else:
            print(f'Computing {case} {method}',flush=True);started=time.perf_counter()
            r=ns['solve'](case,model,'RK4','fixed',config)
            assert r['completed'] and np.isclose(r['reached'],config['T']),r['reason']
            assert np.allclose(r['x'],data['x']) and np.allclose(r['y'],data['y'])
            assert all(np.allclose(x,e,rtol=1e-12,atol=1e-13) for x,e in zip(r['exact'],exact))
            assert all(np.isfinite(x).all() for x in r['fields'])
            np.savez_compressed(dest,x=r['x'],y=r['y'],u=r['fields'][0],v=r['fields'][1],exact_u=exact[0],exact_v=exact[1])
            info=dict(case=case,method=method,model=model,config=config,source_sha256=before,
                completed=True,reached=r['reached'],elapsed_seconds=time.perf_counter()-started,
                max_errors=r['max_errors'],initial_error=r['initial_error'])
            mp.write_text(json.dumps(info,indent=2),encoding='utf-8')
        records.append(dict(case=case,method=method,source=str(dest),reused=False,metadata=info))
        print(f'Finished {case} {method}',flush=True)
assert hashlib.sha256(nbpath.read_bytes()).hexdigest()==before
(OUT/'manifest.json').write_text(json.dumps(dict(config=config,records=records,notebook_unchanged=True,original_tables_rerun=False),ensure_ascii=False,indent=2),encoding='utf-8')
