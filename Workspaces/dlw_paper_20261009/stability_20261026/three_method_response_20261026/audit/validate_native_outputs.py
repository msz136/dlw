"""Audit each method's own native physical response, without alignment/comparison."""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
NATIVE=BASE/'native'
CASES=['A','D','Gaussian','Sinusoidal']
METHODS=['Endpoint-SD','Centered-SD','FD']
KEYS=['endpoint','centered','fd']

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def audit(case):
    record=json.loads((NATIVE/(case+'.json')).read_text(encoding='utf-8'))
    source_path=Path(record['source_experiment'])
    source=json.loads(source_path.read_text(encoding='utf-8'))
    assert record['status']=='complete' and abs(record['reached']-.01)<1e-15
    assert record['methods']==METHODS and record['inputs']==['u','v']
    assert record['interpolation_used'] is False and record['method_pair_comparisons'] is False
    assert sha(NATIVE/(case+'.npz'))==record['artifact_sha256']
    assert sha(source_path.with_suffix('.npz'))==source['artifact_sha256']==record['source_artifact_sha256']
    for path,digest in record['source_files'].items():assert sha(Path(path))==digest
    output=[]
    with np.load(NATIVE/(case+'.npz')) as public, np.load(source_path.with_suffix('.npz')) as original:
        x,y=public['x'],public['y'];h=record['h'];dx=record['dx'];k=record['kappa']
        times=public['t'];curves=public['response_normalized']
        assert curves.shape==(101,3,2,2)
        assert np.max(abs(times-np.arange(101)*1e-4))<1e-15
        assert np.array_equal(curves,original['max_native_normalized'])
        assert np.isfinite(curves).all()
        ix=abs(x)<=(5 if case=='A' else 30) if case in ['A','D'] else np.ones(len(x),dtype=bool)
        mu=abs(y)<(5 if case=='A' else 30) if case in ['A','D'] else abs(y)<=1.8+1e-12
        carrier=np.cos(k*x)[None,:]
        for mi,(method,key) in enumerate(zip(METHODS,KEYS)):
            yv=public[key+'_v_y']
            expected_yv=y-h/2 if method=='Endpoint-SD' else ((y[1:]+y[:-1])/2 if method=='Centered-SD' else y)
            assert np.array_equal(yv,expected_yv)
            mv=abs(yv)<(5 if case=='A' else 30) if case in ['A','D'] else abs(yv)<=1.8+1e-12
            analytic_u=np.sin(np.pi*(y-y[0])/(y[-1]-y[0]))[:,None]**2*carrier
            analytic_v=np.sin(np.pi*(yv-y[0])/(y[-1]-y[0]))[:,None]**2*carrier
            arrays={}
            max_recompute=physical_export_error=0.
            for phase,ti in [('initial',0),('final',-1)]:
                u=public[key+'_delta_u_'+phase+'_normalized']
                v=public[key+'_delta_v_'+phase+'_normalized']
                state=original[key+'_delta_'+phase]
                physical_u=state[:,0]
                physical_v=np.diff(physical_u,axis=1)/h+(state[:,1,1:]+state[:,1,:-1])/2 if method=='Centered-SD' else state[:,1]
                physical_export_error=max(physical_export_error,float(abs(physical_u-u).max()),float(abs(physical_v-v).max()))
                assert physical_export_error==0
                expected=np.stack([abs(u[:,mu][:,:,ix]).max(axis=(1,2)),abs(v[:,mv][:,:,ix]).max(axis=(1,2))],axis=1)
                max_recompute=max(max_recompute,float(abs(expected-curves[ti,mi]).max()))
                assert max_recompute==0
                arrays[phase]=(u,v)
            iu,iv=arrays['initial'];fu,fv=arrays['final']
            initial_error=max(float(abs(iu[0]-analytic_u).max()),float(abs(iu[1]).max()),float(abs(iv[0]).max()),float(abs(iv[1]-analytic_v).max()))
            assert initial_error<2e-12
            l0=np.sqrt(h*dx*(np.sum(iu[:,mu][:,:,ix]**2,axis=(1,2))+np.sum(iv[:,mv][:,:,ix]**2,axis=(1,2))))
            lt=np.sqrt(h*dx*(np.sum(fu[:,mu][:,:,ix]**2,axis=(1,2))+np.sum(fv[:,mv][:,:,ix]**2,axis=(1,2))))
            for ci,component in enumerate(['u','v']):
                row=next(r for r in record['terminal'] if r['method']==method and r['input']==component)
                assert np.array_equal(np.array(row['initial_response_normalized']),curves[0,mi,ci])
                assert np.array_equal(np.array(row['terminal_response_normalized']),curves[-1,mi,ci])
                assert abs(row['native_pair_L2_gain']-lt[ci]/l0[ci])<1e-12
                output.append(dict(method=method,input=component,initial=curves[0,mi,ci].tolist(),terminal=curves[-1,mi,ci].tolist()))
            assert record['baseline_checks'][method]['baseline_reproduction_max']<2e-12
    return dict(case=case,native_histories_match_source_exactly=True,
        physical_export_reconstruction_error=0.,initial_terminal_max_recomputation_error=0.,
        initial_physical_functions_checked=True,baseline_reproduction_checked=True,
        interpolation_used=False,method_pair_comparisons=False,rows=output)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--partial',action='store_true');args=ap.parse_args()
    cases=[c for c in CASES if (NATIVE/(c+'.json')).exists()] if args.partial else CASES
    results=[audit(c) for c in cases]
    output=dict(independent_native_audit_passed=True,completed_cases=cases,trajectories=6*len(cases),results=results,
        interpretation='Each method own perturbed-minus-unperturbed native physical response; no spatial alignment or intermethod agreement metric.')
    path=HERE/('native_output_validation_partial.json' if args.partial else 'native_output_validation.json')
    path.write_text(json.dumps(output,indent=2),encoding='utf-8')
    print(json.dumps(output,indent=2))
