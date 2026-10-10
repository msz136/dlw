"""100 display cells per direction, T=.01; leave paper and notebook unchanged."""
from pathlib import Path
import json,hashlib,time,gc,shutil
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OUT=HERE/'trial_equal100';OUT.mkdir(exist_ok=True)
paths=[ROOT/'notebook/DLW数值分析report.ipynb',HERE/'manuscript.md',ROOT/'report/dlw_paper_draft.html']
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
nb=json.loads(paths[0].read_text(encoding='utf8'));cells={c['id']:''.join(c['source']) for c in nb['cells']};ns={}
for name in ['imports','config','reference','spatial','sd_fd','sd','sd2_lift','sd2_evolution','fd','mesh','time']:
    exec(cells['dlw-'+name].replace('from IPython.display import display','display=lambda *a,**k:None'),ns)
records=[]
for case in 'ABCD':
    half=dict(A=5.,B=10.,C=30.,D=30.)[case];h=2*half/100
    comp=dict(A=10.,B=20.,C=40.2,D=40.2)[case]
    cfg=dict(ns['case_config'](case),h=h,nx=round(2*comp/h),L=2*comp,yhalf=comp,T=.01)
    for model in ['SD','SD2','FD']:
        stem=f'{case}_{model}_RK4_fixed';dest=OUT/(stem+'.json')
        if dest.exists():
            record=json.loads(dest.read_text(encoding='utf8'));assert record['config']==cfg
        elif case=='A':
            record=json.loads((HERE/'buffered_run'/(stem+'.json')).read_text(encoding='utf8'));assert record['config']==cfg
            record['reused_identical_run']=True
            dest.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
        else:
            tic=time.perf_counter();print('START '+stem+' h='+str(h),flush=True)
            try:
                r=ns['solve'](case,model,'RK4','fixed',cfg)
                record={k:r[k] for k in ['completed','reason','reached','max_errors','initial_error','min_J','support_margins']}
                record['completed']=bool(record['completed'])
                assert len(r['y'])==100
                assert min(r['support_margins'])>0
                record['evaluation_y_cells']=len(r['y'])
                np.savez_compressed(OUT/(stem+'.npz'),x=r['x'],y=r['y'],u=r['fields'][0],v=r['fields'][1],exact_u=r['exact'][0],exact_v=r['exact'][1],state=r['state'],native_x=r['native_x'])
                del r;gc.collect()
            except (ValueError,FloatingPointError,OverflowError) as exc:
                record=dict(completed=False,reason=str(exc),reached=None,max_errors=None)
            record.update(case=case,model=model,method='RK4',mesh='fixed',config=cfg,seconds=time.perf_counter()-tic)
            dest.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
        records.append(record)
        (OUT/'results.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
        print('DONE '+stem+' '+json.dumps({k:record[k] for k in ['completed','reached','max_errors']}) ,flush=True)
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in hashes.items())
(OUT/'manifest.json').write_text(json.dumps(dict(runs=12,completed=sum(r['completed'] for r in records),display_cells_per_direction=100,protected_sha256=hashes,article_and_notebook_unchanged=True),indent=2),encoding='utf8')
print('ALL 12 GRID TRIALS FINISHED; PAPER AND NOTEBOOK UNCHANGED',flush=True)
