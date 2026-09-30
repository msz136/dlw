"""Verify the full moving-mesh comparison and export canonical flat data."""
import csv
import json
import numpy as np
from run_dynamic_mesh_table import HERE,OUT,PS,ROUTES,TIMES,sha,engine

def main():
    saved=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
    rows=saved['rows'];assert len(rows)==len(saved['plan'])==414
    assert all(r['status']=='completed' for r in rows.values())
    for k,h in engine.source_hashes().items():assert saved['source_hashes'][k]==h
    for name in ('run_designed_cases.py','run_dynamic_mesh_table.py'):
        assert saved['source_hashes'][name]==sha(HERE/name)
    for path,h in saved['source_results_sha256'].items():assert sha(path)==h
    def get(p,r,purpose):
        hit=[row for row in rows.values() if row['spec']['p']==p and row['spec']['route']==r and row['spec']['purpose']==purpose]
        assert len(hit)==1
        return hit[0]
    def error(p,r,method,t,g,f,fine=False):
        return get(p,r,method)['snapshots'][str(t)]['eval_32001' if fine else 'errors'][g][f]
    flat=[]
    for row in rows.values():
        assert sha(row['profile'])==row['profile_sha256']
        assert row['min_h']>0 and row['min_rho']>0
        if row['spec']['route']=='difference_fixed':assert row['movement_025_to_05']==0
        else:assert row['movement_025_to_05']>1e-9
        for t in TIMES:
            for g in ('core','peak'):
                flat.append({**row['spec'],'time':t,'region':g,**row['snapshots'][str(t)]['errors'][g],
                             'provenance':row['provenance']['kind']})
    for p in PS:
        for purpose in ('rk4','euler','space','time','euler_half'):
            assert len({get(p,r,purpose)['initial_state_sha256'] for r in ROUTES[:3]})==1
    with (OUT/'all_errors.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
    pairs=(('integrable_calibrated','difference_matched'),('difference_rm','difference_fixed'),
           ('difference_rho','difference_fixed'),('difference_rm','difference_rho'))
    ratios=[]
    for a,b in pairs:
        for p in PS:
            for method in ('rk4','euler'):
                for t in TIMES:
                    for g in ('core','peak'):
                        ratios.append(dict(numerator=a,denominator=b,p=p,method=method,time=t,region=g,
                                      **{f:error(p,a,method,t,g,f)/error(p,b,method,t,g,f) for f in ('u','rho')}))
    controls={}
    for control,baseline,ps in [('space','rk4',PS),('time','space',PS),('euler_half','euler',PS),
                               ('domain','rk4',(3.,8.,20.,22.))]:
        changes=[];flips=[];orders={r:[] for r in ROUTES}
        for p in ps:
            for r in ROUTES:
                for t in TIMES:
                    for g in ('core','peak'):
                        for f in ('u','rho'):
                            a=error(p,r,control,t,g,f);b=error(p,r,baseline,t,g,f)
                            changes.append(abs(a/b-1))
                            if control=='space':orders[r].append(float(np.log2(b/a)))
            for a,b in pairs:
                for t in TIMES:
                    for g in ('core','peak'):
                        for f in ('u','rho'):
                            if (error(p,a,control,t,g,f)<error(p,b,control,t,g,f))!=(error(p,a,baseline,t,g,f)<error(p,b,baseline,t,g,f)):
                                flips.append(dict(p=p,numerator=a,denominator=b,time=t,region=g,field=f))
        controls[control]=dict(max_relative_error_change=max(changes),ranking_changes=flips)
        if control=='space':controls[control]['observed_orders']={k:[min(v),max(v)] for k,v in orders.items()}
    eval_changes=[];eval_flips=[]
    for row in rows.values():
        for t in TIMES:
            for g in ('core','peak'):
                for f in ('u','rho'):
                    snap=row['snapshots'][str(t)]
                    eval_changes.append(abs(snap['eval_32001'][g][f]/snap['errors'][g][f]-1))
    for a,b in pairs:
        for p in PS:
            for method in ('rk4','euler'):
                for t in TIMES:
                    for g in ('core','peak'):
                        for f in ('u','rho'):
                            if (error(p,a,method,t,g,f)<error(p,b,method,t,g,f))!=(error(p,a,method,t,g,f,True)<error(p,b,method,t,g,f,True)):
                                eval_flips.append(dict(p=p,method=method,numerator=a,denominator=b,time=t,region=g,field=f))
    motion=json.loads((OUT/'motion_audit.json').read_text(encoding='utf-8'))
    assert len(motion['rows'])==12
    for r in motion['rows']:
        assert r['moving_steps']==(0 if r['route']=='difference_fixed' else r['steps'])
    summary=dict(completed=len(rows),new=sum(r['provenance']['kind']=='new' for r in rows.values()),
                 reused=sum(r['provenance']['kind']=='reused' for r in rows.values()),
                 ratios=ratios,controls=controls,max_eval_relative_change=max(eval_changes),
                 evaluation_ranking_changes=eval_flips,full_step_audit=motion,
                 min_h=min(r['min_h'] for r in rows.values()),min_rho=min(r['min_rho'] for r in rows.values()))
    engine.dump(OUT/'summary.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k not in ('ratios','full_step_audit')},ensure_ascii=False,indent=2))
    for a,b in pairs:
        selected=[r for r in ratios if r['numerator']==a and r['denominator']==b and r['region']=='core']
        print(a,'/',b,'core u/rho wins:',sum(r['u']<1 for r in selected),sum(r['rho']<1 for r in selected),'/',len(selected))
    print('RK4 t=.5: p, Rm/fixed u/rho, rho/fixed u/rho')
    for p in PS:
        print(p,*[(r['u'],r['rho']) for r in ratios if r['p']==p and r['method']=='rk4' and r['time']==.5 and r['region']=='core' and r['denominator']=='difference_fixed'])

if __name__=='__main__':main()
