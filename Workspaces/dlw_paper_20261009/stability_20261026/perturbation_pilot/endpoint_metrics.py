"""Endpoint L2 norms and finite-grid Fourier interpolation diagnostics.

These are diagnostics of the stored numerical perturbations, not continuum
enclosures. The original NPZ files are only read and hash-checked.
"""
from pathlib import Path
import csv,hashlib,json
import numpy as np
from scipy.signal import resample
HERE=Path(__file__).resolve().parent/'four_case_kappa_pi_over_2'

records=[]
for case in ['A','D','Gaussian','Sinusoidal']:
    path=HERE/(case+'.json')
    if not path.exists():continue
    rec=json.loads(path.read_text());artifact=path.with_suffix('.npz')
    digest=hashlib.sha256(artifact.read_bytes()).hexdigest()
    assert digest==rec['artifact_sha256']
    d=np.load(artifact);h,dx=rec['h'],rec['dx'];x=d['x'];nx=len(x)
    y,yv=d['y'],d['yv']
    if case in ['A','D']:
        R=5 if case=='A' else 30
        mu,mv=abs(y)<R,abs(yv)<R
    else:
        R=1.8;mu,mv=abs(y)<=R+1e-12,abs(yv)<=R+1e-12
    def fields(state):
        u,w=state;v=np.diff(u,axis=0)/h+(w[1:]+w[:-1])/2
        return u[mu],v[mv]
    for i,c in enumerate(['u','v'],start=1):
        f0=fields(d['z0'][i]);ft=fields(d['final_state'][i])
        L0=np.array([np.sqrt(h*dx*np.sum(q*q)) for q in f0]);Lt=np.array([np.sqrt(h*dx*np.sum(q*q)) for q in ft])
        r=dict(case=case,perturbed_field=c,time=rec['reached'],L2_definition='sqrt(h*dx*sum(field^2)) over all periodic x nodes and the native y evaluation region',L2_initial=L0.tolist(),L2_final=Lt.tolist(),L2_gain_relative_to_initial_pair=(Lt/np.linalg.norm(L0)).tolist(),L2_pair_gain=float(np.linalg.norm(Lt)/np.linalg.norm(L0)),native_full_period_max_initial=[float(abs(q).max()) for q in f0],native_full_period_max_final=[float(abs(q).max()) for q in ft],fourier_interpolant_max={},source_sha256=digest,continuous_certificate=False)
        for factor in [4,8]:
            initial=[];terminal=[]
            for arr,dest in [(f0,initial),(ft,terminal)]:
                for q in arr:dest.append(float(abs(resample(q,nx*factor,axis=-1)).max()))
            scale=max(initial)
            r['fourier_interpolant_max'][str(factor)]=dict(initial=initial,final=terminal,gain_relative_to_initial_max=[v/scale for v in terminal],scope='finite-grid trigonometric interpolant evaluated on '+str(factor)+'x denser x nodes; y rows unchanged')
        records.append(r)
    assert hashlib.sha256(artifact.read_bytes()).hexdigest()==digest

out=dict(records=records,all_source_hashes_unchanged=True,continuous_certificate=False)
(HERE/'endpoint_norms.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
with (HERE/'endpoint_norms.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['case','perturbed_field','L2u_initial','L2v_initial','L2u_final','L2v_final','L2pair_gain','x8_max_u','x8_max_v','x8_gain_u','x8_gain_v'])
    for r in records:
        q=r['fourier_interpolant_max']['8'];w.writerow([r['case'],r['perturbed_field'],*r['L2_initial'],*r['L2_final'],r['L2_pair_gain'],*q['final'],*q['gain_relative_to_initial_max']])
for r in records:print(r['case'],r['perturbed_field'],'L2pair gain',r['L2_pair_gain'],'x8 peak gain',r['fourier_interpolant_max']['8']['gain_relative_to_initial_max'])
