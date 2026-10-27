"""Independent reconstruction and metric checks of the three-method responses."""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
from scipy.interpolate import CubicSpline

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
CASES=['A','D','Gaussian','Sinusoidal']
METHODS=['Endpoint-SD','Centered-SD','FD']
KEYS=['endpoint','centered','fd']
PAIRS=[(0,1),(0,2),(1,2)]

def audit(case):
    record=json.loads((BASE/(case+'.json')).read_text(encoding='utf-8'))
    path=BASE/(case+'.npz')
    assert hashlib.sha256(path.read_bytes()).hexdigest()==record['artifact_sha256']
    assert record['status']=='complete' and abs(record['reached']-.01)<1e-15
    assert record['methods']==METHODS and record['inputs']==['u','v']
    with np.load(path) as archive:
        x,y,ye=archive['x'],archive['y'],archive['common_v_y']
        h=record['h']; eps=record['epsilon']; k=record['kappa']
        mx=abs(x)<=(5 if case=='A' else 30) if case in ['A','D'] else np.ones(len(x),dtype=bool)
        mu=abs(y)<(5 if case=='A' else 30) if case in ['A','D'] else abs(y)<=1.8+1e-12
        mv=abs(ye)<(5 if case=='A' else 30) if case in ['A','D'] else abs(ye)<=1.8+1e-12
        yvs=[y-h/2,ye,y]
        t=archive['t']; maxima=archive['max_common_normalized']; pairs=archive['pairwise_absolute_normalized']; relative=archive['pairwise_relative']
        snapshot_t=archive['snapshot_t'];su=archive['common_u_snapshots'];sv=archive['common_v_snapshots']
        assert len(t)==101 and np.max(abs(t-np.arange(101)*1e-4))<1e-15
        assert np.isfinite(maxima).all() and np.isfinite(relative).all()
        def physical(state,method):
            u=state[:,0]
            v=np.diff(u,axis=1)/h+(state[:,1,1:]+state[:,1,:-1])/2 if method=='Centered-SD' else state[:,1]
            return u,v
        common_initial=[];common_final=[];raw_init_error=0.;map_grid_error=0.
        for mi,method in enumerate(METHODS):
            init=archive[KEYS[mi]+'_delta_initial']; final=archive[KEYS[mi]+'_delta_final']
            u0,v0=physical(init,method)
            carrier=np.cos(k*x)[None,:]
            u_exact=np.sin(np.pi*(y-y[0])/(y[-1]-y[0]))[:,None]**2*carrier
            v_exact=np.sin(np.pi*(yvs[mi]-y[0])/(y[-1]-y[0]))[:,None]**2*carrier
            raw_init_error=max(raw_init_error,float(abs(u0[0]-u_exact).max()),float(abs(u0[1]).max()),float(abs(v0[0]).max()),float(abs(v0[1]-v_exact).max()))
            for state,container in [(init,common_initial),(final,common_final)]:
                u,v=physical(state,method)
                if method=='Endpoint-SD':v=v[:,1:]
                elif method=='FD':v=CubicSpline(y,v,axis=1)(ye)
                container.append((u[:,mu][:,:,mx],v[:,mv][:,:,mx]))
            if method=='Endpoint-SD':map_grid_error=float(abs(yvs[0][1:]-ye).max())
        assert raw_init_error<2e-12
        def sample_metrics(uu,vv):
            maxs=np.stack((abs(uu).max(axis=(2,3)),abs(vv).max(axis=(2,3))),axis=-1)
            diff=[]
            for i,j in PAIRS:diff.append(np.stack((abs(uu[i]-uu[j]).max(axis=(1,2)),abs(vv[i]-vv[j]).max(axis=(1,2))),axis=-1))
            diff=np.array(diff)
            denom=np.maximum(1.,maxs.max(axis=(0,2)))
            return maxs,diff,diff.max(axis=-1)/denom
        worst_max=worst_pair=worst_relative=0.
        for ti,(us,vs) in enumerate(zip(su,sv)):
            idx=int(round(snapshot_t[ti]/1e-4))
            a,b,c=sample_metrics(us,vs)
            worst_max=max(worst_max,float(abs(a-maxima[idx]).max()))
            worst_pair=max(worst_pair,float(abs(b-pairs[idx]).max()))
            worst_relative=max(worst_relative,float(abs(c-relative[idx]).max()))
        endpoints=[]
        for idx,common in [(0,common_initial),(-1,common_final)]:
            us=np.array([r[0] for r in common]);vs=np.array([r[1] for r in common])
            a,b,c=sample_metrics(us,vs)
            worst_max=max(worst_max,float(abs(a-maxima[idx]).max()))
            worst_pair=max(worst_pair,float(abs(b-pairs[idx]).max()))
            worst_relative=max(worst_relative,float(abs(c-relative[idx]).max()))
            endpoints.append((us,vs))
        assert max(worst_max,worst_pair,worst_relative)<1e-12
        assert np.max(abs(maxima[0]-record['initial_response_normalized']))<1e-12
        assert np.max(abs(maxima[-1]-record['terminal_response_normalized']))<1e-12
        assert np.max(abs(relative[-1]-record['terminal_pairwise_relative']))<1e-12
        window_checks=[]
        for ci,component in enumerate(['u','v']):
            discrepancy=relative[:,:,ci].max(axis=1)
            for tolerance in [.01,.05,.1]:
                above=np.where(discrepancy>tolerance)[0]
                first=None if not len(above) else float(t[above[0]])
                last=float(t[-1]) if first is None else float(t[max(0,above[0]-1)])
                stored=next(r for r in record['agreement_windows'] if r['input']==component and r['threshold']==tolerance)
                assert stored['first_exceedance']==first and stored['last_prefix_time_within']==last
                assert stored['right_censored']==(first is None)
                window_checks.append(dict(input=component,threshold=tolerance,first_exceedance=first,last_within=last))
        floor=float(pairs[0].max());assert abs(floor-record['initial_interpolation_floor_normalized'])<1e-12
        l2_initial=np.sqrt(h*record['dx']*(np.sum(endpoints[0][0]**2,axis=(2,3))+np.sum(endpoints[0][1]**2,axis=(2,3))))
        l2_final=np.sqrt(h*record['dx']*(np.sum(endpoints[1][0]**2,axis=(2,3))+np.sum(endpoints[1][1]**2,axis=(2,3))))
        l2_error=float(abs(l2_final/l2_initial-record['terminal_l2_gain_common_observation']).max());assert l2_error<1e-12
        baseline_max=max(v['baseline_reproduction_max'] for v in record['checkpoints'].values())
        assert baseline_max<2e-12
        out=dict(case=case,complete=True,methods=3,independent_inputs=2,artifact_hash_matches=True,
            raw_native_initial_physical_function_error_normalized=raw_init_error,
            endpoint_centered_v_grid_difference=map_grid_error,
            initial_cubic_interpolation_floor_normalized=floor,
            max_curve_recomputation_error=worst_max,pair_distance_recomputation_error=worst_pair,
            relative_distance_recomputation_error=worst_relative,l2_recomputation_error=l2_error,
            baseline_reproduction_max=baseline_max,windows=window_checks,
            terminal_response=record['terminal_response_normalized'],terminal_pairwise_relative=record['terminal_pairwise_relative'])
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--partial',action='store_true');args=ap.parse_args()
    cases=[c for c in CASES if (BASE/(c+'.json')).exists()] if args.partial else CASES
    results=[audit(c) for c in cases]
    output=dict(independent_audit_passed=True,completed_cases=cases,trajectories=6*len(cases),results=results,
        interpretation='Common-grid numerical response consistency and first-threshold crossings; not a continuous reference error certificate.')
    path=HERE/('output_validation_partial.json' if args.partial else 'output_validation.json')
    path.write_text(json.dumps(output,indent=2),encoding='utf-8')
    print(json.dumps(output,indent=2))
