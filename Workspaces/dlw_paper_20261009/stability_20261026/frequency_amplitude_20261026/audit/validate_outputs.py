"""Independent read-only audit of sweep arrays and reported table metrics."""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
audits=[]
controls=[]
theory=json.loads((HERE/'constant_response.json').read_text())['rows']
ap=argparse.ArgumentParser();ap.add_argument('--cases',nargs='+',default=['A','D','Gaussian','Sinusoidal']);args=ap.parse_args()

for case in args.cases:
    path=BASE/(case+'.json')
    rec=json.loads(path.read_text())
    ap=path.with_suffix('.npz')
    assert hashlib.sha256(ap.read_bytes()).hexdigest()==rec['artifact_sha256']
    z=np.load(ap)
    initial_states=z['normalized_initial'];final_states=z['normalized_final']
    assert rec['status']=='complete' and abs(rec['reached']-.01)<1e-15
    assert len(rec['records'])==18 and len(z['t'])==101
    assert not rec['continuous_certificate'] and rec['eta_u'] is rec['eta_v'] is None
    x,y,yv=z['x'],z['y'],z['yv'];h,dx=rec['h'],rec['dx']
    if case in ['A','D']:
        R=5 if case=='A' else 30
        ix,mu,mv=abs(x)<=R,abs(y)<R,abs(yv)<R
    else:
        ix=np.ones(len(x),bool);mu,mv=abs(y)<=1.8+1e-12,abs(yv)<=1.8+1e-12
    def physical(state):
        u,w=state
        return u[mu],(np.diff(u,axis=0)/h+.5*(w[1:]+w[:-1]))[mv]
    maxima_error=0.;l2_error=0.;spread_error=0.
    ratios=[]
    for j,p in enumerate(rec['records']):
        assert p['status']=='complete' and abs(p['reached']-.01)<1e-15
        fields=physical(final_states[j]);initial=physical(initial_states[j])
        vals=np.array([abs(a[:,ix]).max() for a in fields])
        initvals=np.array([abs(a[:,ix]).max() for a in initial])
        maxima_error=max(maxima_error,float(abs(vals-np.array(p['final_max_normalized'])).max()),float(abs(initvals-p['initial_max_normalized']).max()))
        L0=np.array([np.sqrt(h*dx*np.sum(a*a)) for a in initial])
        LT=np.array([np.sqrt(h*dx*np.sum(a*a)) for a in fields])
        gain=np.linalg.norm(LT)/np.linalg.norm(L0)
        l2_error=max(l2_error,float(abs(gain-p['l2_pair_gain'])))
        ci=0 if p['component']=='u' else 1;ref=p['k_index']*6+2+ci
        rf=physical(final_states[ref])
        spread=np.array([abs((a-b)[:,ix]).max() for a,b in zip(fields,rf)])
        spread_error=max(spread_error,float(abs(spread-p['normalized_field_difference_from_eps1e6_terminal']).max()))
        if p['epsilon_index']==1:
            th=next(a for a in theory if a['case']==case and a['component']==p['component'] and a['kappa_factor_of_pi_over_2']==[1,2,4][p['k_index']])
            ratios.append(dict(component=p['component'],kappa=p['kappa'],maxima=vals.tolist(),
                constant_maxima=[th['terminal_u_over_epsilon'],th['terminal_v_over_epsilon']],
                ratio_to_constant=(vals/np.array([th['terminal_u_over_epsilon'],th['terminal_v_over_epsilon']])).tolist(),
                pair_gain=float(gain),constant_pair_gain=th['pair_L2_gain']))
    assert maxima_error<1e-12 and l2_error<1e-12 and spread_error<1e-12
    assert np.max(abs(z['amplitude_difference'][0]))==0
    amp=max(p['relative_pair_max_difference_all_time'] for p in rec['records'])
    audits.append(dict(case=case,record_count=18,artifact_hash_matches=True,maxima_recomputation_error=maxima_error,
        l2_gain_recomputation_error=l2_error,amplitude_spread_recomputation_error=spread_error,
        largest_relative_pair_amplitude_spread=amp,baseline_reproduction_max=rec['baseline_reproduction_max'],
        legacy_physical_difference_max=max(max(v) for v in rec['legacy_pi_over_2_eps1e6_physical_differences']),
        baseline_amplitude_theory_comparisons=ratios))
    control=BASE/(case+'_half_step.json')
    if control.exists():
        cr=json.loads(control.read_text());ca=control.with_suffix('.npz')
        assert hashlib.sha256(ca.read_bytes()).hexdigest()==cr['artifact_sha256']
        assert cr['status']=='complete' and cr['reached']==.01
        cz=np.load(ca)
        control_final=cz['normalized_final']
        for j,p in enumerate(cr['records']):
            assert p['k_index']==2 and p['epsilon_index']==2
            ref=16+(p['component']=='v')
            f=physical(control_final[j]);m=physical(final_states[ref])
            diff=np.array([abs((a-b)[:,ix]).max() for a,b in zip(f,m)])
            scale=max(abs(a[:,ix]).max() for a in m)
            controls.append(dict(case=case,component=p['component'],normalized_terminal_difference=diff.tolist(),
                physical_terminal_difference=(diff*p['epsilon']).tolist(),relative_pair_max_difference=float(diff.max()/scale)))

out=dict(independent_array_audit_passed=True,main_trajectories=18*len(audits),audits=audits,half_step_controls=controls,
    scope='Numerical reproducibility and metric audit; no continuous perturbed-reference certificate')
name='output_validation.json' if len(audits)==4 else 'output_validation_partial.json'
(HERE/name).write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(dict(main_trajectories=18*len(audits),audits=[{k:v for k,v in a.items() if k!='baseline_amplitude_theory_comparisons'} for a in audits],half_step_controls=controls),indent=2))
