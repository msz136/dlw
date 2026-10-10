"""Run the existing notebook solver at the user-selected domain and spacings."""
from pathlib import Path
import json, shutil, hashlib, time, gc
import numpy as np
import matplotlib
matplotlib.use("Agg")
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'boundary_run'
OUT.mkdir(exist_ok=True)
BACK=OUT/'before'
BACK.mkdir(exist_ok=True)
nbpath=ROOT/'notebook/DLW数值分析report.ipynb'
for src in [nbpath,HERE/'manuscript.md',HERE/'tables.json',ROOT/'report/dlw_paper_draft.html']:
    dst=BACK/src.name
    if not dst.exists(): shutil.copy2(src,dst)
nb=json.loads((BACK/nbpath.name).read_text(encoding='utf-8'))
byid={c['id']:c for c in nb['cells']}
def source(key):return ''.join(byid['dlw-'+key]['source'])
def put(key,s):byid['dlw-'+key]['source']=s.splitlines(keepends=True)
put('config', """CASES = {'A': ((1.,), (2.,)), 'B': ((4.,), (-3.,)), 'C': ((6., 4.), (-5., -3.)), 'D': ((1.,4.), (2.,-3.))}
HALF_WIDTHS = {'A': 5., 'B': 10., 'C': 30., 'D': 30.}
CONFIG = dict(a=2., h=.1, dt=.0001, T=.01)
CASE_CONFIGS = {case: dict(CONFIG, L=2*half, nx=round(2*half/.1), yhalf=half,
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
time_source = source('time')
sampling = (HERE/'boundary_sampling.py').read_text(encoding='utf-8')
time_source = sampling + '\n\n' + time_source
time_source = time_source.replace("    native = p.fields(state, reached)\n    sampled = [CubicSpline(p.X.x, f, axis=-1)(xx) for f in native]",
    "    sampled, completed_x, completed_fields, native = sample_numerical_fields(p, state, reached, xx)")
time_source = time_source.replace("    nsteps = round(config['T']/config['dt'])",
    "    initial_x, initial_completed, _ = completed_numerical_fields(p, state, 0.)\n    initial_right_ref = p.m.G.uv(p.m.js, initial_x[-1:], 0.)\n    initial_endpoint_error = max(float(abs(f[:, -1:] - e).max()) for f, e in zip(initial_completed, initial_right_ref))\n    nsteps = round(config['T']/config['dt'])")
time_source = time_source.replace('initial_error=initial_error, x=xx',
    'initial_error=initial_error, initial_endpoint_error=initial_endpoint_error, state=state, completed_x=completed_x, completed_fields=completed_fields, x=xx')
put('time', time_source)
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
            s=s.replace(s.split('\n\n')[1], '四个算例的计算域依次为 $[-5,5]^2$、$[-10,10]^2$、$[-30,30]^2$、$[-30,30]^2$。取 $\\Delta x=h=0.1$，相应地每个方向依次为100、200、600、600个单元；x采用不重复右端点的网格，y场值取单元中点。',1)
        if c['id']=='dlw-time-text':
            s=s.replace('在 $x\\in[-20,20]$ 的 4001 个等距点及全部 $y$ 层上', '在各算例完整x区间上取间距0.01的等距评价点（依次1001、2001、6001、6001个），与全部y层组成评价网格')
        if c['id']=='dlw-field-text':
            s='## 8　物理场与误差分布\n\n四个算例依次在 $[-5,5]^2$、$[-10,10]^2$、$[-30,30]^2$、$[-30,30]^2$ 上计算和展示。固定网格、RK4，$\\Delta x=h=0.1$、$\\Delta t=0.0001$、$T=0.01$。场图与误差表采用同一组计算结果。\n'
        c['source']=s.splitlines(keepends=True)
nb['metadata']['boundary_rerun']={'status':'running','skipped':'Euler refinement study, which is not used in the paper'}
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
                r={k:result[k] for k in ['completed','reason','reached','max_errors','initial_error','min_J','cn_diagnostics','initial_endpoint_error']}
                r['completed']=bool(r['completed'])
                r.update(case=case,model=model,method=method,mesh=mesh,config=config,seconds=time.perf_counter()-t0)
                if result['completed'] and method=='RK4' and mesh=='fixed':
                    np.savez_compressed(OUT/(key+'.npz'),x=result['x'],y=result['y'],
                        u=result['fields'][0],v=result['fields'][1],exact_u=result['exact'][0],
                        exact_v=result['exact'][1],native_x=result['native_x'],
                        native_u=result['native_fields'][0],native_v=result['native_fields'][1],
                        completed_x=result['completed_x'],completed_u=result['completed_fields'][0],completed_v=result['completed_fields'][1],state=result['state'])
                np.savez_compressed(OUT/(key+'_state.npz'), state=result['state'], native_x=result['native_x'], native_u=result['native_fields'][0], native_v=result['native_fields'][1], completed_x=result['completed_x'], completed_u=result['completed_fields'][0], completed_v=result['completed_fields'][1])
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
nb['metadata']['boundary_rerun']['status']='completed_48_paper_runs'
nbpath.write_text(json.dumps(nb,ensure_ascii=False,indent=1),encoding='utf-8')
(OUT/'manifest.json').write_text(json.dumps({'configs':configs,'runs':len(records),'notebook':str(nbpath),'notebook_sha256':hashlib.sha256(nbpath.read_bytes()).hexdigest(),'all_completed':all(r['completed'] for r in records)},indent=2),encoding='utf-8')
print('ALL 48 RUNS COMPLETE',flush=True)
