"""Export each method's own native-grid perturbation response.

The earlier common-grid metrics are superseded and are not publication data.
No interpolation or pairwise method comparison enters this export.
"""
from pathlib import Path
import argparse,csv,hashlib,json
import numpy as np

HERE=Path(__file__).resolve().parent
OUT=HERE/'native';OUT.mkdir(exist_ok=True)
METHODS=['Endpoint-SD','Centered-SD','FD']
KEYS=['endpoint','centered','fd']
CASES=['A','D','Gaussian','Sinusoidal']
PROJECT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def export(case):
    source=HERE/(case+'.json')
    if not source.exists():source=HERE/'superseded_common_grid'/(case+'.json')
    artifact=source.with_suffix('.npz')
    if not source.exists():return
    rec=json.loads(source.read_text(encoding='utf-8'));assert sha(artifact)==rec['artifact_sha256']
    data=np.load(artifact);x,y=data['x'],data['y'];h=rec['h'];dx=rec['dx'];eps=rec['epsilon']
    response=data['max_native_normalized']
    result=dict(t=data['t'],response_normalized=response,x=x,y=y)
    metrics=[]
    for i,(method,key) in enumerate(zip(METHODS,KEYS)):
        yv=y-h/2 if method=='Endpoint-SD' else ((y[1:]+y[:-1])/2 if method=='Centered-SD' else y.copy())
        result[key+'_v_y']=yv
        if case in ['A','D']:
            R=5 if case=='A' else 30;ix=abs(x)<=R;mu=abs(y)<R;mv=abs(yv)<R
        else:ix=np.ones(len(x),bool);mu=abs(y)<=1.8+1e-12;mv=abs(yv)<=1.8+1e-12
        def physical(state):
            # State shape input(2),statefield(2),nativey,x.
            u=state[:,0]
            v=np.diff(u,axis=1)/h+(state[:,1,1:]+state[:,1,:-1])/2 if method=='Centered-SD' else state[:,1]
            return u,v
        for phase in ['initial','final']:
            u,v=physical(data[key+'_delta_'+phase])
            result[key+'_delta_u_'+phase+'_normalized']=u
            result[key+'_delta_v_'+phase+'_normalized']=v
            vals=np.stack([np.max(abs(u[:,mu][:,:,ix]),axis=(1,2)),np.max(abs(v[:,mv][:,:,ix]),axis=(1,2))],axis=1)
            np.testing.assert_allclose(vals,response[0 if phase=='initial' else -1,i],rtol=0,atol=0)
        u0=result[key+'_delta_u_initial_normalized'];v0=result[key+'_delta_v_initial_normalized']
        ut=result[key+'_delta_u_final_normalized'];vt=result[key+'_delta_v_final_normalized']
        l0=np.sqrt(h*dx*(np.sum(u0[:,mu][:,:,ix]**2,axis=(1,2))+np.sum(v0[:,mv][:,:,ix]**2,axis=(1,2))))
        lt=np.sqrt(h*dx*(np.sum(ut[:,mu][:,:,ix]**2,axis=(1,2))+np.sum(vt[:,mv][:,:,ix]**2,axis=(1,2))))
        for ci,component in enumerate(['u','v']):
            metrics.append(dict(method=method,input=component,initial_response_normalized=response[0,i,ci].tolist(),terminal_response_normalized=response[-1,i,ci].tolist(),native_pair_L2_gain=float(lt[ci]/l0[ci])))
    dest=OUT/(case+'.npz');np.savez_compressed(dest,**result)
    sources=[HERE/'run_comparison.py',PROJECT/'spatial_audit_20261023/run.py',PROJECT/'spatial_audit_20261023/separated/reconstruction_probe/rerun_20261024.py',PROJECT/'spatial_audit_20261023/separated/reconstruction_probe/probe.py',PROJECT/'time_samm_20261025/time/run_time.py',PROJECT/'report_refresh_20261024/nondegenerate_rk4_20261024/run.py']
    final=dict(case=case,methods=METHODS,inputs=['u','v'],outputs=['u','v'],status=rec['status'],reason=rec['reason'],T=rec['T'],reached=rec['reached'],dt=rec['dt'],dx=dx,h=h,epsilon=eps,kappa=rec['kappa'],samples=len(data['t']),
        response_definition='For each method independently: maximum absolute numerical perturbed-minus-own-unperturbed physical field at its native sites, divided by prescribed epsilon.',
        observation=rec['observation'],initial_condition='Same analytic physical initial background and epsilon*sin^2(pi*(y-yL)/(yR-yL))*cos(kappa*x) sampled at each native physical-field location; one physical field perturbed at a time.',
        interpolation_used=False,method_pair_comparisons=False,terminal=metrics,initial_checks=rec['initial_checks'],baseline_checks=rec['checkpoints'],boundary=rec['boundary'],
        native_L2_scope='h*dx sum on each field own native sites and the same per-case observation window; terminal divided by own initial paired norm.',
        continuous_certificate=False,artifact_sha256=sha(dest),source_experiment=str(source),source_artifact_sha256=rec['artifact_sha256'],source_files={str(p):sha(p) for p in sources},export_source_sha256=sha(Path(__file__)))
    dest.with_suffix('.json').write_text(json.dumps(final,indent=2),encoding='utf-8')
    with (OUT/(case+'_history.csv')).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['case','method','input','time','native_u_response_over_epsilon','native_v_response_over_epsilon'])
        for ti,t in enumerate(data['t']):
            for mi,method in enumerate(METHODS):
                for ci,component in enumerate(['u','v']):w.writerow([case,method,component,t,*response[ti,mi,ci]])
    print('EXPORTED',case,'native only',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('case',nargs='?',choices=CASES);a=ap.parse_args()
    for c in ([a.case] if a.case else CASES):export(c)
