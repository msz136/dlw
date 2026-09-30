"""Independent saved-field audit and semantic CSV checks; never run evolution."""
from pathlib import Path
from functools import lru_cache
import csv
import json
import hashlib
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=ROOT/'Workspaces/hs_table_data_20260927'
DEST=HERE/'table_handoff_review'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

@lru_cache(None)
def exact(p,t):
    x=np.linspace(-2,2,32001)
    s=1-2/p; beta=p-p/(p-1)
    lo=x-s/2;hi=x+s/2
    for _ in range(58):
        X=(lo+hi)/2
        mapped=X+s/2*np.tanh((beta*X-s*t)/2)
        lo=np.where(mapped<x,X,lo);hi=np.where(mapped>=x,X,hi)
    X=(lo+hi)/2; z=np.tanh((beta*X-s*t)/2)
    assert np.max(np.abs(X+s/2*z-x))<2e-14
    return x,s*s/4*(1-z*z),(1-s*s)/(1-s*s*z*z)

def main():
    DEST.mkdir(exist_ok=True)
    d=json.loads((SOURCE/'out/results.json').read_text(encoding='utf-8'))
    assert len(d['rows'])==len(d['plan'])==368
    assert sha(SOURCE/'run_tables.py')==d['driver_sha256']
    for name,h in d['source_hashes'].items():assert sha(ROOT/'Workspaces'/name)==h
    for name,h in d['source_results_sha256'].items():assert sha(name)==h
    maximum=0.;metric_checks=0; specs={}; provenance={}
    for key,r in d['rows'].items():
        assert r['status']=='completed' and r['spec']==d['plan'][key]
        assert sha(r['profile'])==r['profile_sha256']
        spec=r['spec'];assert spec['route'] in ('difference_rm','difference_fixed')
        sk=(spec['p'],spec['route'],spec['method'],spec['n'],spec['dt'])
        assert sk not in specs;specs[sk]=r
        provenance[r['provenance']]=provenance.get(r['provenance'],0)+1
        with np.load(r['profile']) as z:
            for t in (.25,.5):
                x,u,rx,rho=(z[f't{t}_{v}'] for v in ('x','u','rho_x','rho'))
                assert all(np.isfinite(v).all() for v in (x,u,rx,rho))
                assert np.min(np.diff(x))>0 and np.min(np.diff(rx))>0 and np.min(rho)>0
                assert x[0]<=-2 and x[-1]>=2 and rx[0]<=-2 and rx[-1]>=2
                if spec['route']=='difference_fixed':assert np.allclose(x,np.linspace(-4,4,spec['n']+1),rtol=0,atol=1e-13)
                xx,ue,re=exact(spec['p'],t)
                errors=(np.abs(np.interp(xx,x,u)-ue),np.abs(np.interp(xx,rx,rho)-re))
                for size,stride in ((8001,4),(16001,2),(32001,1)):
                    for field,e in zip(('u','rho'),errors):
                        delta=abs(float(e[::stride].max())-r['snapshots'][str(t)][str(size)][field])
                        maximum=max(maximum,delta);metric_checks+=1
                        assert delta<5e-13,(key,t,size,field,delta)
    with (SOURCE/'out/expanded_cells.csv').open(encoding='utf-8-sig',newline='') as f:cells=list(csv.DictReader(f))
    numeric=0;empty=0;seen=set()
    for c in cells:
        signature=tuple(c[k] for k in ('p','t','method','N','dt','scheme'))
        assert signature not in seen;seen.add(signature)
        if c['scheme'] in ('S1','S2','S3','S4'):
            assert c['status']=='model_not_constructed' and not c['u_error'] and not c['rho_error'];empty+=1
        else:
            route={'S5':'difference_rm','S6':'difference_fixed'}[c['scheme']]
            r=specs[(float(c['p']),route,c['method'],int(c['N']),float(c['dt']))]
            e=r['snapshots'][str(float(c['t']))][c['evaluation_points']]
            assert c['status']=='completed'
            for field in ('u','rho'):assert float(c[field+'_error'])==e[field]
            numeric+=1
    assert numeric==640 and empty==1280
    counts={};flips=[];eval_change=0
    for n,dt,size in ((400,.003125,16001),(200,.0125,8001)):
        for method in ('euler','heun','rk4','rk8'):
            for t in (.25,.5):
                count={'u':0,'rho':0}
                for p in range(3,23):
                    rows=[specs[(p,route,method,n,dt)] for route in ('difference_rm','difference_fixed')]
                    for f in count:
                        win=rows[0]['snapshots'][str(t)][str(size)][f]<rows[1]['snapshots'][str(t)][str(size)][f]
                        count[f]+=int(win)
                        if p in (5,12,22):
                            half=[specs[(p,route,method,n,dt/2)]['snapshots'][str(t)][str(size)][f] for route in ('difference_rm','difference_fixed')]
                            if win!=(half[0]<half[1]):flips.append([p,n,method,t,f])
                counts[f'N{n}_{method}_t{t}']=count
    for r in specs.values():
        for e in r['snapshots'].values():
            for f in ('u','rho'):eval_change=max(eval_change,abs(e['32001'][f]/e['16001'][f]-1))
    reported=json.loads((SOURCE/'out/summary.json').read_text(encoding='utf-8'))
    assert counts==reported['s5_better_counts_out_of_20'] and flips==reported['time_half_ranking_flips']
    assert abs(eval_change-reported['max_relative_eval16001_to32001'])<1e-15
    result=dict(status='passed',profiles=368,provenance=provenance,independent_metric_checks=metric_checks,
        max_absolute_metric_difference=maximum,numeric_cells=numeric,undefined_cells=empty,
        counts=counts,time_half_flips=flips,max_relative_eval_change=eval_change,
        results_sha256=sha(SOURCE/'out/results.json'),expanded_csv_sha256=sha(SOURCE/'out/expanded_cells.csv'))
    (DEST/'review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='counts'}))

if __name__=='__main__':main()
