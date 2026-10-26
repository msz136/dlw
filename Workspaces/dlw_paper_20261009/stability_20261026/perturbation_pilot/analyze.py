"""Read-only checks of saved sensitivity data; never a continuum certificate."""
from pathlib import Path
import csv,hashlib,json,sys
import numpy as np
from scipy.interpolate import CubicSpline
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from run_pilot import setup,measure

def record(name):
    p=HERE/(name+'.json');r=json.loads(p.read_text());q=p.with_suffix('.npz')
    assert hashlib.sha256(q.read_bytes()).hexdigest()==r['artifact_sha256']
    return r,np.load(q)

controls=[]
for c in ['u','v']:
    name=f'A_{c}_dx0.1_h0.1_dt0.0001'
    r,b=record(name);m,_,_,yv,_=setup('A',.1,.1,c)
    for label,nm in [('time_half',f'A_{c}_dx0.1_h0.1_dt5e-05'),('y_half',f'A_{c}_dx0.1_h0.05_dt0.0001')]:
        rr,f=record(nm)
        if label=='time_half':du=f['delta_u'];dv=f['delta_v'];interp=False
        else:
            assert np.max(abs(f['y'][::2]-b['y']))<2e-14
            du=f['delta_u'][::2]
            dv=CubicSpline(f['yv'],f['delta_v'],axis=0)(b['yv']);interp=True
        d=measure(m,du-b['delta_u'],dv-b['delta_v'],yv)
        controls.append(dict(component=c,control=label,terminal_perturbation_difference=d,midpoint_v_interpolation_used=interp,certified_error_bound=False))

r,f=record('A_u_dx0.05_h0.1_dt2.5e-05')
m,_,_,yv,_=setup('A',.05,.1,'u');t=float(f['t'][-1])
failed=dict(record='A_u_dx0.05_h0.1_dt2.5e-05',reached=t,status=r['status'],reason=r['reason'],background_max_global=[float(abs(f['u']).max()),float(abs(f['v']).max())],background_exact_error_in_region=measure(m,f['u']-m.profile(m.y,t)[0],f['v']-m.profile(yv,t)[1],yv),perturbation_max_global=[float(abs(f['delta_u']).max()),float(abs(f['delta_v']).max())],perturbation_max_region=measure(m,f['delta_u'],f['delta_v'],yv),comment='The unperturbed numerical baseline already loses accuracy under this x refinement. This is not a physical blow-up time or an error bound.')
summary=dict(controls=controls,x_refinement_stop=failed,certificate=False,eta_u=None,eta_v=None)
(HERE/'pilot_analysis.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))

records=[];suite=HERE/'four_case_kappa_pi_over_2'
for case in ['A','D','Gaussian','Sinusoidal']:
    path=suite/(case+'.json')
    if not path.exists():continue
    rec=json.loads(path.read_text());artifact=path.with_suffix('.npz')
    assert hashlib.sha256(artifact.read_bytes()).hexdigest()==rec['artifact_sha256']
    data=np.load(artifact)
    assert data['delta_max'].shape==(len(data['t']),2,2)
    assert np.all(np.isfinite(data['delta_max'])) and data['t'][0]==0
    assert rec['certificate'] is False and rec['reference_bound_u'] is None
    assert np.max(abs(np.asarray(rec['final_delta_max'])-data['delta_max'][-1]))==0
    records.append(rec)
with (suite/'summary.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['case','perturbed_field','kappa','epsilon','reached','initial_max_delta_u','initial_max_delta_v','final_max_delta_u','final_max_delta_v','gain_u','gain_v','certificate'])
    for r in records:
        for i,c in enumerate(['u','v']):w.writerow([r['case'],c,r['kappa'],r['epsilon'],r['reached'],*r['initial_delta_max'][i],*r['final_delta_max'][i],*r['gain_relative_to_initial_max'][i],False])
(suite/'validation.json').write_text(json.dumps(dict(completed_cases=[r['case'] for r in records],all_artifact_hashes_match=True,initial_field_mapping_max=max((max(r['initial_physical_v_map_errors']) for r in records),default=None),baseline_rk4_reproduction_max=max((r['baseline_reproduces_published_rk4_maxdiff'] for r in records),default=None),certificate=False,eta_u=None,eta_v=None),indent=2),encoding='utf-8')
