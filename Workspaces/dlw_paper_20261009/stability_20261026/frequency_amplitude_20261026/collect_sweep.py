"""Validate saved trajectories and collect publication endpoint rows."""
from pathlib import Path
import csv,hashlib,json
import numpy as np
HERE=Path(__file__).resolve().parent
CASES=['A','D','Gaussian','Sinusoidal']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(tag):
    p=HERE/(tag+'.json');r=json.loads(p.read_text());assert sha(p.with_suffix('.npz'))==r['artifact_sha256']
    return r,np.load(p.with_suffix('.npz'))
rows=[];cases=[];controls=[]
for case in CASES:
    if not (HERE/(case+'.json')).exists():continue
    rec,data=load(case)
    assert rec['status']=='complete' and rec['reached']==.01
    assert len(rec['records'])==18
    assert data['max_normalized'].shape==(101,18,2)
    assert np.isfinite(data['normalized_final']).all()
    for q in rec['records']:
        rows.append(dict(case=case,kappa=q['kappa'],epsilon=q['epsilon'],component=q['component'],time=q['reached'],max_u_over_epsilon=q['final_max_normalized'][0],max_v_over_epsilon=q['final_max_normalized'][1],l2_pair_gain=q['l2_pair_gain'],amplitude_discrepancy_all_time=q['relative_pair_max_difference_all_time'],amplitude_discrepancy_terminal=q['relative_pair_max_difference_terminal']))
    cases.append(dict(case=case,complete_trajectories=len(rec['records']),max_amplitude_discrepancy_all_time=max(q['relative_pair_max_difference_all_time'] for q in rec['records']),max_amplitude_discrepancy_terminal=max(q['relative_pair_max_difference_terminal'] for q in rec['records']),baseline_reproduction_max=rec['baseline_reproduction_max'],legacy_physical_difference_max=max(max(q) for q in rec['legacy_pi_over_2_eps1e6_physical_differences']),map_residual=rec['initial_physical_map_max'],rhs_residual=rec['normalized_rhs_versus_existing_delta_rhs_max'],seconds=rec['seconds']))
    if (HERE/(case+'_half_step.json')).exists():
        cr,cd=load(case+'_half_step');assert cr['status']=='complete' and cr['reached']==.01
        y,yv,x=data['y'],data['yv'],data['x']
        if case in ['A','D']:
            R=5 if case=='A' else 30;mu,mv,ix=abs(y)<R,abs(yv)<R,abs(x)<=R
        else:mu,mv,ix=abs(y)<=1.8+1e-12,abs(yv)<=1.8+1e-12,np.ones(len(x),dtype=bool)
        def fields(d):return d[0],np.diff(d[0],axis=0)/.1+(d[1,1:]+d[1,:-1])/2
        for ci,component in enumerate(['u','v']):
            full=fields(data['normalized_final'][16+ci]);half=fields(cd['normalized_final'][ci])
            diffs=[float(abs((a-b)[mask][:,ix]).max()) for a,b,mask in zip(full,half,[mu,mv])]
            ref=max(float(abs(a[mask][:,ix]).max()) for a,mask in zip(half,[mu,mv]))
            controls.append(dict(case=case,component=component,kappa=float(2*np.pi),epsilon=1e-5,dt_main=1e-4,dt_control=5e-5,terminal_normalized_field_difference=diffs,terminal_physical_field_difference=[1e-5*d for d in diffs],relative_terminal_pair_max_difference=max(diffs)/ref,continuous_error_bound=False))

with (HERE/'terminal_rows.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
out=dict(completed_cases=[r['case'] for r in cases],completed_trajectories=len(rows),cases=cases,rows=rows,time_controls=controls,continuous_certificate=False,eta_u=None,eta_v=None)
(HERE/'summary.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
