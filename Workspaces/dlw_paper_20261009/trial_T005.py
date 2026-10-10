"""Read-only notebook reuse: continue the 12 fixed RK4 states to T=0.05."""
from pathlib import Path
import json,time,gc,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'trial_T005';OUT.mkdir(exist_ok=True)
protected=[ROOT/'notebook/DLW数值分析report.ipynb',HERE/'manuscript.md',ROOT/'report/dlw_paper_draft.html']
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
nb=json.loads(protected[0].read_text(encoding='utf8'))
source={c['id']:''.join(c['source']) for c in nb['cells']}
ns={}
for name in ['imports','config','reference','spatial','sd_fd','sd','sd2_lift','sd2_evolution','fd','mesh','time']:
    exec(source['dlw-'+name].replace('from IPython.display import display','display=lambda *a,**k:None'),ns)
records=[]
for case in 'ABCD':
 for model in ['SD','SD2','FD']:
    stem=f'{case}_{model}_RK4_fixed';dest=OUT/(stem+'.json')
    if dest.exists():
        record=json.loads(dest.read_text(encoding='utf8'))
    else:
        print('START '+stem,flush=True);tic=time.perf_counter()
        cfg=dict(ns['case_config'](case),T=.05)
        problem=ns['Problem'](case,model,'fixed',cfg)
        initial=problem.initial();del initial
        with np.load(HERE/'buffered_run'/(stem+'_state.npz')) as cached:state=cached['state'].copy()
        restored=problem.fields(state,.01)
        with np.load(HERE/'buffered_run'/(stem+'.npz')) as cached:
            restart_error=max(float(abs(restored[i]-cached['native_'+f]).max()) for i,f in enumerate(['u','v']))
        assert restart_error<1e-12,(stem,restart_error)
        reached=.01;reason='';trace=[]
        for n in range(100,500):
            try:
                with np.errstate(over='raise',invalid='raise',divide='raise'):
                    candidate=ns['step'](problem.stage,n*cfg['dt'],state,cfg['dt'],'RK4')
                    if not np.isfinite(candidate).all() or abs(candidate).max()>1000:
                        raise ValueError('State nonfinite or absolute value exceeds the existing 1000 threshold')
                    problem.X.set_s(candidate[-problem.X.n:])
            except (ValueError,FloatingPointError,OverflowError) as exc:
                reason=str(exc);break
            state=candidate;reached=(n+1)*cfg['dt']
            if (n+1)%50==0:
                trace.append(dict(t=reached,max_abs_state=float(abs(state).max())))
                print(f'  {stem} t={reached:.3f} max_state={abs(state).max():.6g}',flush=True)
        native=problem.fields(state,reached);mask=abs(problem.m.y)<cfg['eval_yhalf']
        xx=np.linspace(-cfg['eval_half'],cfg['eval_half'],cfg['eval_points'])
        margins=[float(xx[0]-problem.X.x[0]),float(problem.X.x[-1]-xx[-1])];assert min(margins)>0
        sampled=[ns['CubicSpline'](problem.X.x,f[mask],axis=-1,extrapolate=False)(xx) for f in native]
        exact=problem.m.G.uv(problem.m.js[mask],xx,reached)
        errors={f:float(abs(a-b).max()) for f,a,b in zip(['u','v'],sampled,exact)}
        record=dict(case=case,model=model,method='RK4',mesh='fixed',config=cfg,reached=reached,completed=bool(not reason and np.isclose(reached,.05)),reason=reason,max_errors=errors,restart_field_difference=restart_error,support_margins=margins,trace=trace,seconds=time.perf_counter()-tic)
        np.savez_compressed(OUT/(stem+'_state.npz'),state=state,x=problem.X.x,y=problem.m.y)
        dest.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
        del problem,state,native,sampled,exact;gc.collect()
    records.append(record)
    (OUT/'results.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
    print('DONE '+stem+' '+json.dumps({k:record[k] for k in ['completed','reached','reason','max_errors']},ensure_ascii=False),flush=True)
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in hashes.items())
(OUT/'manifest.json').write_text(json.dumps(dict(runs=len(records),completed=sum(r['completed'] for r in records),target_T=.05,resumed_from=.01,protected_sha256=hashes,article_and_notebook_unchanged=True),indent=2),encoding='utf8')
print('ALL 12 TRIALS FINISHED; PAPER AND NOTEBOOK UNCHANGED',flush=True)
