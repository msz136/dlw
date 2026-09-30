"""Read-back checks, comparison tables and sensitivity of the frozen cases."""
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
from run_designed_cases import (OUT, HERE, PS, TIMES, ROUTES, MOVING, case_key,
    source_hashes, safe_reference, initialize)

def main():
    saved=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
    rows=saved['rows']
    assert len(rows)==len(saved['plan'])==135
    assert all(r['status']=='completed' for r in rows.values())
    for file,hash_ in source_hashes().items():
        assert saved['source_hashes'][file]==hash_
    assert saved['source_hashes']['run_designed_cases.py']==hashlib.sha256((HERE/'run_designed_cases.py').read_bytes()).hexdigest()
    def get(p,route,purpose='main'):
        hits=[r for r in rows.values() if r['spec']['p']==p and r['spec']['route']==route and r['spec']['purpose']==purpose]
        assert len(hits)==1
        return hits[0]
    def err(row,t,region,field,fine=False):
        return row['snapshots'][str(t)]['eval_32001' if fine else 'errors'][region][field]
    for p in PS:
        assert len({get(p,r)['initial_state_sha256'] for r in MOVING})==1
    flat=[]; ratios=[]
    for row in rows.values():
        spec=row['spec']
        assert row['min_h']>0 and row['min_rho']>0
        profile=np.load(OUT/row['profile'])
        for t in TIMES:
            for name in ('x','u','rho_x','rho'):
                assert np.all(np.isfinite(profile[f't{t}_{name}']))
            for region in ('core','peak'):
                flat.append({**spec,'time':t,'region':region,**row['snapshots'][str(t)]['errors'][region]})
    with (OUT/'all_errors.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
    for p in PS:
        s=1-2/p
        for purpose in ('main','space_control','time_control','euler','euler_half'):
            for t in TIMES[1:]:
                for region in ('core','peak'):
                    ca,di=get(p,'integrable_calibrated',purpose),get(p,'difference_matched',purpose)
                    ratios.append(dict(p=p,purpose=purpose,time=t,region=region,
                        theory_ratio=4*(1-s*s)/(2+s*s),
                        u=err(ca,t,region,'u')/err(di,t,region,'u'),
                        rho=err(ca,t,region,'rho')/err(di,t,region,'rho')))
    controls={};orders={r:[] for r in ROUTES};changes=[]
    max_eval=max(abs(err(r,t,g,f,True)/err(r,t,g,f)-1) for r in rows.values()
                 for t in TIMES[1:] for g in ('core','peak') for f in ('u','rho'))
    for control in ('space_control','time_control','euler','euler_half','domain_control'):
        effects=[]; flip=[]
        for p in PS:
            if control=='domain_control' and p not in (8.,22.):continue
            for route in ROUTES:
                base=get(p,route,'space_control' if control=='time_control' else 'main')
                test=get(p,route,control)
                for t in TIMES[1:]:
                    for region in ('core','peak'):
                        for field in ('u','rho'):
                            effects.append(abs(err(test,t,region,field)/err(base,t,region,field)-1))
                            if control=='space_control':
                                orders[route].append(np.log2(err(base,t,region,field)/err(test,t,region,field)))
            for t in TIMES[1:]:
                for g in ('core','peak'):
                    for f in ('u','rho'):
                        basewin=err(get(p,'integrable_calibrated'),t,g,f)<err(get(p,'difference_matched'),t,g,f)
                        testwin=err(get(p,'integrable_calibrated',control),t,g,f)<err(get(p,'difference_matched',control),t,g,f)
                        if basewin!=testwin:flip.append(dict(p=p,time=t,region=g,field=f))
        controls[control]=dict(max_relative_error_change=max(effects),ranking_changes=flip)
    fine_eval_flips=[]
    for p in PS:
        for t in TIMES[1:]:
            for g in ('core','peak'):
                for f in ('u','rho'):
                    a,b=get(p,'integrable_calibrated'),get(p,'difference_matched')
                    if (err(a,t,g,f)<err(b,t,g,f)) != (err(a,t,g,f,True)<err(b,t,g,f,True)):
                        fine_eval_flips.append([p,t,g,f])
    # Parametric forward map is independent of inversion; check round trips.
    inverse_residual=0.;exact_field_difference=0.
    for p in PS:
        sol,_,_,_,_=initialize(p,'difference_matched',400)
        for t in TIMES:
            X=np.linspace(-3,3,10001)
            u,x,rho=sol.continuous_X(X,t)
            ue,re,back,res=safe_reference(sol,x,t)
            inverse_residual=max(inverse_residual,res,float(np.max(abs(back-X))))
            exact_field_difference=max(exact_field_difference,float(np.max(abs(ue-u))),float(np.max(abs(re-rho))))
    previous=json.loads((HERE/'out/results.json').read_text(encoding='utf-8'))['rows']
    ref_change=0.
    for key,old in previous.items():
        if old['status']!='completed':continue
        for t in TIMES:
            for g in ('core','peak'):
                for f in ('u','rho'):
                    ref_change=max(ref_change,abs(err(rows[key],t,g,f)-err(old,t,g,f)))
    # Exact same-region field discrepancy for half-time-step control.
    time_field_difference=0.
    for p in PS:
        for route in ROUTES:
            aa=np.load(OUT/get(p,route,'space_control')['profile'])
            bb=np.load(OUT/get(p,route,'time_control')['profile'])
            for t in TIMES[1:]:
                xx=np.linspace(-2,2,32001)
                for f,xkey in [('u','x'),('rho','rho_x')]:
                    time_field_difference=max(time_field_difference,float(np.max(abs(
                        np.interp(xx,aa[f't{t}_{xkey}'],aa[f't{t}_{f}'])-
                        np.interp(xx,bb[f't{t}_{xkey}'],bb[f't{t}_{f}'])))))
    result=dict(completed=len(rows),ratios=ratios,controls=controls,
                spatial_order_ranges={k:[float(min(v)),float(max(v))] for k,v in orders.items()},
                max_evaluation_relative_change=max_eval,evaluation_ranking_changes=fine_eval_flips,
                reference_round_trip_max=inverse_residual,reference_field_max=exact_field_difference,
                previous_successful_reference_max_change=ref_change,
                rk4_half_step_field_linf=time_field_difference,
                min_h=min(r['min_h'] for r in rows.values()),min_rho=min(r['min_rho'] for r in rows.values()))
    (OUT/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='ratios'},ensure_ascii=False,indent=2))
    print('MAIN RATIOS (u/rho):')
    for r in ratios:
        if r['purpose']=='main':print(r['p'],r['time'],r['region'],round(r['u'],4),round(r['rho'],4))

if __name__=='__main__':main()
