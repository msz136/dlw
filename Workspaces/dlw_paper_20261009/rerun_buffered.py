"""Run the existing notebook solver at the user-selected domain and spacings."""
from pathlib import Path
import json, shutil, hashlib, time, gc
import numpy as np
import matplotlib
matplotlib.use("Agg")
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'buffered_run'
OUT.mkdir(exist_ok=True)
BACK=OUT/'before'
BACK.mkdir(exist_ok=True)
nbpath=ROOT/'notebook/DLW数值分析report.ipynb'
for src in [nbpath,HERE/'manuscript.md',HERE/'tables.json',ROOT/'report/dlw_paper_draft.html']:
    dst=BACK/src.name
    if not dst.exists(): shutil.copy2(src,dst)
nb=json.loads((HERE/'physd_domains_run/before'/nbpath.name).read_text(encoding='utf-8'))
byid={c['id']:c for c in nb['cells']}
def source(key):return ''.join(byid['dlw-'+key]['source'])
def put(key,s):byid['dlw-'+key]['source']=s.splitlines(keepends=True)
put('config', """CASES = {'A': ((1.,), (2.,)), 'B': ((4.,), (-3.,)), 'C': ((6., 4.), (-5., -3.)), 'D': ((1., 4.), (2., -3.))}
HALF_WIDTHS = {'A': 5., 'B': 10., 'C': 30., 'D': 30.}
COMPUTE_HALF_WIDTHS = {'A': 10., 'B': 20., 'C': 40., 'D': 40.}
CONFIG = dict(a=2., h=.1, dt=.0001, T=.01)
CASE_CONFIGS = {case: dict(CONFIG, L=2*COMPUTE_HALF_WIDTHS[case], nx=round(2*COMPUTE_HALF_WIDTHS[case]/.1), yhalf=COMPUTE_HALF_WIDTHS[case], eval_yhalf=half,
                            eval_half=half, eval_points=round(2*half/.01)+1)
                for case, half in HALF_WIDTHS.items()}
def case_config(case):
    return dict(CASE_CONFIGS[case])
MODELS = ('SD', 'SD2', 'FD')
COLORS = dict(SD='#1776bc', SD2='#d47b19', FD='#38965f')
pd.DataFrame([{'case': k, 'p': p, 'q': q} for k, (p, q) in CASES.items()])
""")
put('time', source('time').replace('def solve(case, model, method, mesh, config=CONFIG):',
    'def solve(case, model, method, mesh, config=None):\n    config = case_config(case) if config is None else config'))
sampling = source('time')
sampling = sampling.replace("    sampled = [CubicSpline(p.X.x, f, axis=-1)(xx) for f in native]\n    exact = p.m.G.uv(p.m.js, xx, reached)", """    margins = [float(xx[0]-p.X.x[0]), float(p.X.x[-1]-xx[-1])]
    assert min(margins) > 0, 'Evaluation region exceeds native numerical support'
    ymask = abs(p.m.y) < config['eval_yhalf']
    sampled = [CubicSpline(p.X.x, f[ymask], axis=-1, extrapolate=False)(xx) for f in native]
    assert all(np.isfinite(f).all() for f in sampled)
    exact = p.m.G.uv(p.m.js[ymask], xx, reached)""")
sampling = sampling.replace('y=p.m.y, fields=sampled', 'y=p.m.y[ymask], fields=sampled')
sampling = sampling.replace('cn_diagnostics=cn_diagnostics)', 'cn_diagnostics=cn_diagnostics, support_margins=margins, state=state.copy(), native_y=p.m.y.copy())')
put('time', sampling)
put('order',source('order').replace('dict(CONFIG,','dict(case_config(case),'))
put('field-data', """FIELD_MODEL, FIELD_METHOD, FIELD_MESH = 'SD2', 'RK4', 'fixed'
dlw_field_cache = {}
for field_case in CASES:
    key = (field_case, FIELD_MODEL, FIELD_METHOD, FIELD_MESH)
    record = results.get(key)
    if record is None or 'fields' not in record:
        record = solve(*key, config=case_config(field_case))
    if not record['completed']:
        raise RuntimeError(record['reason'])
    dlw_field_cache[field_case] = record
""")
put('field-config', """PLOT_CONFIG = dict(
    cases=('A', 'B', 'C', 'D'),
    windows={case: dict(xlim=(-half, half), ylim=(-half, half)) for case, half in HALF_WIDTHS.items()},
    cmap='jet', error_cmap='jet', map_style='contour', levels=11, contour_width=1.1,
    elev=28., azim=-62.,
)
""")
put('field-plots', """for field_case in PLOT_CONFIG['cases']:
    record = dlw_field_cache[field_case]
    drawing = dict(PLOT_CONFIG, **PLOT_CONFIG['windows'][field_case])
    draw_field_panels(record['x'], record['y'], record['fields'], record['exact'],
        f"DLW Case {field_case} | SD2 + RK4, fixed | t={record['reached']:g}",
        ('u','v'), drawing)
""")
for c in nb['cells']:
    if c['cell_type']=='code':
        c['outputs']=[];c['execution_count']=None
    else:
        s=''.join(c['source']).replace('0.000125','0.0001')
        if c['id']=='dlw-spatial-text':
            s=s.replace(s.split('\n\n')[1], '三个算例的计算域分别为 $[-5,5]^2$、$[-10,10]^2$、$[-30,30]^2$。取 $\\Delta x=h=0.1$，相应地每个方向分别为100、200、600个单元；x采用不重复右端点的网格，y场值取单元中点。',1)
        if c['id']=='dlw-time-text':
            s=s.replace('在 $x\\in[-20,20]$ 的 4001 个等距点及全部 $y$ 层上', '在各算例完整x区间上取间距0.01的等距评价点（分别1001、2001、6001个），与全部y层组成评价网格')
        if c['id']=='dlw-field-text':
            s='## 8　物理场与误差分布\n\n三个算例分别在 $[-5,5]^2$、$[-10,10]^2$、$[-30,30]^2$ 上计算和展示。固定网格、RK4，$\\Delta x=h=0.1$、$\\Delta t=0.0001$、$T=0.01$。场图与误差表采用同一组计算结果。\n'
        c['source']=s.splitlines(keepends=True)
for key in ['spatial-text','time-text','field-text']:
    put(key, {'spatial-text': '## Spatial grid\n\nCompute on [-10,10]^2, [-20,20]^2, [-40,40]^2, [-40,40]^2 for A, B, C, D. Use dx=h=0.1. The moving mesh redistributes x nodes; y cell centres remain fixed.\n', 'time-text': '## Time integration and errors\n\nEuler, RK4 and Crank–Nicolson use dt=0.0001 up to T=0.01. Evaluate only on the interior target squares with half-widths 5, 10, 30, 30. Interpolate in x with spacing 0.01 within native node support; retain interior y cell centres. No extrapolation is used.\n', 'field-text': '## Physical fields and errors\n\nDisplay the same interior regions used for error evaluation, from the fixed-mesh RK4 runs.\n'}[key])
nb['metadata']['buffered_rerun']={'status':'running','skipped':'Euler refinement study, which is not used in the paper'}
nbpath.write_text(json.dumps(nb,ensure_ascii=False,indent=1),encoding='utf-8')
ns={}
for i,name in enumerate(('imports','config','reference','spatial','sd_fd','sd','sd2_lift','sd2_evolution','fd','mesh','time'),1):
    exec(source(name).replace('from IPython.display import display','display = lambda *args, **kwargs: None'),ns)
    byid['dlw-'+name]['execution_count']=i
configs=ns['CASE_CONFIGS']
records=[]
for method,mesh in [('RK4','fixed'),('Euler','fixed'),('CN','fixed'),('RK4','moving')]:
    for case in 'ABCD':
        config=configs[case]
        for model in ns['MODELS']:
            key=f'{case}_{model}_{method}_{mesh}'
            dest=OUT/(key+'.json')
            if dest.exists():
                r=json.loads(dest.read_text());assert r['config']==config
            else:
                print('START '+key,flush=True);t0=time.perf_counter()
                result=ns['solve'](case,model,method,mesh,config)
                r={k:result[k] for k in ['completed','reason','reached','max_errors','initial_error','min_J','cn_diagnostics','support_margins']}
                r['completed']=bool(r['completed'])
                r.update(case=case,model=model,method=method,mesh=mesh,config=config,seconds=time.perf_counter()-t0)
                np.savez_compressed(OUT/(key+'_state.npz'), state=result['state'], x=result['native_x'], y=result['native_y'])
                if result['completed'] and method=='RK4' and mesh=='fixed':
                    np.savez_compressed(OUT/(key+'.npz'),x=result['x'],y=result['y'],
                        u=result['fields'][0],v=result['fields'][1],exact_u=result['exact'][0],
                        exact_v=result['exact'][1],native_x=result['native_x'],
                        native_u=result['native_fields'][0],native_v=result['native_fields'][1])
                dest.write_text(json.dumps(r,indent=2),encoding='utf-8')
                del result;gc.collect()
            records.append(r)
            ns['results'][case,model,method,mesh]=r
            (OUT/'results.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
            print('DONE '+key+' '+json.dumps({k:r[k] for k in ['completed','max_errors']})+' seconds='+str(round(r.get('seconds',0),1)),flush=True)
            if not r['completed']:raise RuntimeError(key+': '+r['reason'])
tables={}
for idx,(name,var) in enumerate([('space_experiment','space_table'),('time_experiment','time_table'),('mesh_experiment','mesh_table')],20):
    exec(source(name),ns)
    df=ns[var];tables[var]=df.to_html(float_format=lambda x:f'{x:.6e}')
    cell=byid['dlw-'+name];cell['execution_count']=idx
    cell['outputs']=[{'output_type':'execute_result','execution_count':idx,
        'metadata':{},'data':{'text/html':[df.style.format('{:.6e}').highlight_min(axis=1,props='font-weight: bold').to_html()],'text/plain':[df.to_string()]}}]
(OUT/'tables.json').write_text(json.dumps(tables,ensure_ascii=False,indent=2),encoding='utf-8')
nb['metadata']['buffered_rerun']['status']='completed_48_paper_runs'
nbpath.write_text(json.dumps(nb,ensure_ascii=False,indent=1),encoding='utf-8')
(OUT/'manifest.json').write_text(json.dumps({'configs':configs,'runs':len(records),'notebook':str(nbpath),'notebook_sha256':hashlib.sha256(nbpath.read_bytes()).hexdigest(),'all_completed':all(r['completed'] for r in records)},indent=2),encoding='utf-8')
print('ALL 48 RUNS COMPLETE',flush=True)
