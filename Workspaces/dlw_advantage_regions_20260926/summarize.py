"""Audit all neighborhood trajectories and collect data-driven claims."""
from scan import HERE,OUT,FamilyModel,Parameters,sha,dump,errors
import json,csv
import numpy as np

def main():
    d=json.loads((OUT/'scan.json').read_text(encoding='utf-8'));assert len(d['rows'])==324
    prop=json.loads((OUT/'propagation.json').read_text(encoding='utf-8'));assert len(prop['rows'])==24
    for dataset in (d,prop):
        for path,digest in dataset['source_hashes'].items():assert sha(path)==digest,path
        for r in dataset['rows'].values():assert r['status']=='completed',r
    idx={(r['spec']['point'],r['spec']['config'],r['spec']['method']):r for r in d['rows'].values()}
    initial={};readback=0.;evaldiff=0.;flat=[]
    for r in d['rows'].values():
        s=r['spec'];path=OUT/r['profile'];assert sha(path)==r['profile_sha256']
        initial.setdefault((s['point'],s['config']),set()).add(r['initial_sha256'])
        a,p,q=s['parameters'];m=FamilyModel(Parameters(a,p,q,p+q),**{k:s[k] for k in ('route','c','kappa','h','nx','L','yhalf')})
        z=np.load(path);ee=errors(m,(z['u'],z['v']),.01,4)
        for f in ('u','v'):
            readback=max(readback,abs(ee[f]-r['errors'][f]));evaldiff=max(evaldiff,abs(r['eval_double'][f]/r['errors'][f]-1))
        if s['method']=='fd':continue
        fd=idx[(s['point'],s['config'],'fd')]
        ratios=[r['errors'][f]/fd['errors'][f] for f in ('u','v')]
        ratio8=[r['eval_double'][f]/fd['eval_double'][f] for f in ('u','v')]
        flat.append(dict(center=s['center'],point=s['point'],a=a,p=p,q=q,d=a-p,k=p+q,
            config=s['config'],method=s['method'],u_ratio=ratios[0],v_ratio=ratios[1],
            both_better=max(ratios)<1,both_better_eval8=max(ratio8)<1))
    assert all(len(x)==1 for x in initial.values());assert readback<1e-14
    groups=[]
    for center in ('P2','P6'):
        for config in ('main','fine'):
            for method in ('original','theory'):
                group=[r for r in flat if r['center']==center and r['config']==config and r['method']==method]
                assert len(group)==27
                groups.append(dict(center=center,config=config,method=method,both_better=sum(r['both_better'] for r in group),
                    u_min=min(r['u_ratio'] for r in group),u_max=max(r['u_ratio'] for r in group),
                    v_min=min(r['v_ratio'] for r in group),v_max=max(r['v_ratio'] for r in group),
                    failures=[r for r in group if not r['both_better']]))
    remainder=max(r['metrics'][f]['relative_remainder'] for r in prop['rows'].values() for f in ('u','v'))
    rank_agree=0;rank_total=0;paired=[]
    for case in ('P1','P2','P6','P10'):
        for config in ('main','fine'):
            fd=prop['rows'][f'{case}_{config}_fd']
            for method in ('original','theory'):
                r=prop['rows'][f'{case}_{config}_{method}']
                entry=dict(case=case,config=config,method=method)
                for f in ('u','v'):
                    actual=r['metrics'][f]['actual']/fd['metrics'][f]['actual']
                    pred=r['metrics'][f]['predicted']/fd['metrics'][f]['predicted']
                    rank_agree+=(actual<1)==(pred<1);rank_total+=1
                    entry[f+'_actual_ratio']=actual;entry[f+'_predicted_ratio']=pred
                paired.append(entry)
    for r in prop['rows'].values():assert sha(OUT/r['profile'])==r['profile_sha256']
    with (OUT/'neighborhood_ratios.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
    output=dict(groups=groups,scan_count=324,linear_response_count=24,profile_hashes_verified=348,
        readback_error=readback,common_initial_hashes=True,evaluation_max_relative_change=evaldiff,
        evaluation_classification_flips=sum(r['both_better']!=r['both_better_eval8'] for r in flat),
        max_relative_linear_remainder=remainder,linear_rank_agreement=[rank_agree,rank_total],paired_predictions=paired)
    dump(OUT/'summary.json',output)
    print(json.dumps(output,ensure_ascii=True,indent=2))
if __name__=='__main__':main()

