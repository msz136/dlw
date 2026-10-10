"""Run the existing notebook solver at the user-selected domain and spacings."""
from pathlib import Path
import json, shutil, hashlib, time, gc
import numpy as np
import matplotlib
matplotlib.use("Agg")
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'unified_run'
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
put('config',source('config').replace('h=.125, yhalf=1.5','h=.1, yhalf=20.').replace('nx=256','nx=400').replace('dt=.000125','dt=.0001').replace('eval_half=10.','eval_half=20.').replace("CONFIG['eval_half'] < CONFIG['L']/2","CONFIG['eval_half'] <= CONFIG['L']/2"))
# Evaluate the initial mesh density in x blocks: identical y sums, bounded memory.
old="""            u, v = self.m.G.uv(self.m.js, x, 0.)
            gh = self.m.G.uv([self.m.js[0]-1, self.m.js[-1]+1], x, 0.)[0]
            density = 1-(v-delta0(u, gh, self.m.h)).mean(axis=0)/4"""
new="""            density_parts = []
            for xb in np.array_split(x, 40):
                u, v = self.m.G.uv(self.m.js, xb, 0.)
                gh = self.m.G.uv([self.m.js[0]-1, self.m.js[-1]+1], xb, 0.)[0]
                density_parts.append(1-(v-delta0(u, gh, self.m.h)).mean(axis=0)/4)
            density = np.concatenate(density_parts)"""
assert old in source('mesh')
put('mesh',source('mesh').replace(old,new))
put('field-data',source('field-data').replace("dict(CONFIG, L=80., nx=512, yhalf=30.,\n                    eval_half=30., eval_points=1201)","dict(CONFIG)").replace("FIELD_CONFIG['eval_half'] < FIELD_CONFIG['L']/2","FIELD_CONFIG['eval_half'] <= FIELD_CONFIG['L']/2"))
put('field-config',source('field-config').replace("(-3., 4.)","(-20., 20.)").replace("(-3., 3.)","(-20., 20.)").replace("(-30., 30.)","(-20., 20.)"))
for c in nb['cells']:
    if c['cell_type']=='code':
        c['outputs']=[];c['execution_count']=None
    else:
        s=''.join(c['source']).replace('0.000125','0.0001')
        if c['id']=='dlw-spatial-text':
            s=s.replace('$x\\in[-20,20)$ 分为 256 份，$\\Delta x=40/256=0.15625$；$y\\in[-1.5,1.5]$ 分为 24 份，$h=0.125$，场值取各份中点。',
                '$x\\in[-20,20)$ 分为 400 份，$\\Delta x=0.1$；$y\\in[-20,20]$ 分为 400 份，$h=0.1$，场值取各份中点。')
        if c['id']=='dlw-time-text':s=s.replace('[-10,10]','[-20,20]')
        if c['id']=='dlw-field-text':
            s='## 8　物理场与误差分布\n\n三个算例均在 $[-20,20]^2$ 上计算和展示。固定网格、RK4，$\\Delta x=h=0.1$、$\\Delta t=0.0001$、$T=0.01$。场图与误差表采用同一组计算结果。\n'
        c['source']=s.splitlines(keepends=True)
nb['metadata']['unified_rerun']={'status':'running','skipped':'Euler refinement study, which is not used in the paper'}
nbpath.write_text(json.dumps(nb,ensure_ascii=False,indent=1),encoding='utf-8')
ns={}
for i,name in enumerate(('imports','config','reference','spatial','sd_fd','sd','sd2_lift','sd2_evolution','fd','mesh','time'),1):
    exec(source(name).replace('from IPython.display import display','display = lambda *args, **kwargs: None'),ns)
    byid['dlw-'+name]['execution_count']=i
config=ns['CONFIG']
assert config==dict(a=2.,h=.1,yhalf=20.,L=40.,nx=400,dt=.0001,T=.01,eval_half=20.,eval_points=4001),config
records=[]
for method,mesh in [('RK4','fixed'),('Euler','fixed'),('CN','fixed'),('RK4','moving')]:
    for case in 'ABC':
        for model in ns['MODELS']:
            key=f'{case}_{model}_{method}_{mesh}'
            dest=OUT/(key+'.json')
            if dest.exists():
                r=json.loads(dest.read_text());assert r['config']==config
            else:
                print('START '+key,flush=True);t0=time.perf_counter()
                result=ns['solve'](case,model,method,mesh,config)
                r={k:result[k] for k in ['completed','reason','reached','max_errors','initial_error','min_J','cn_diagnostics']}
                r['completed']=bool(r['completed'])
                r.update(case=case,model=model,method=method,mesh=mesh,config=config,seconds=time.perf_counter()-t0)
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
nb['metadata']['unified_rerun']['status']='completed_36_paper_runs'
nbpath.write_text(json.dumps(nb,ensure_ascii=False,indent=1),encoding='utf-8')
(OUT/'manifest.json').write_text(json.dumps({'config':config,'runs':len(records),'notebook':str(nbpath),'notebook_sha256':hashlib.sha256(nbpath.read_bytes()).hexdigest(),'all_completed':all(r['completed'] for r in records)},indent=2),encoding='utf-8')
print('ALL 36 RUNS COMPLETE',flush=True)
