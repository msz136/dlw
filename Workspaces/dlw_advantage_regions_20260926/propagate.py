"""Predict actual solution errors via forced linear error propagation, without fitting."""
from error_model import ErrorModel
from scan import HERE,OLD,OUT,Parameters,dump,sha,norm
from concurrent.futures import ProcessPoolExecutor,as_completed
import numpy as np
import json
from scipy.signal import resample
from run import THEORY

PARAMS={'P1':(4,1,2),'P2':(4,2,3),'P6':(4,1,3),'P10':(2,1.5,2)}
def compute(spec):
    case,config,method=spec['case'],spec['config'],spec['method'];a,p,q=PARAMS[case]
    nx=256 if config=='main' else 512;dt=1.25e-5 if config=='main' else 6.25e-6
    route='fd' if method=='fd' else 'sd';c,k=THEORY if method=='theory' else (0.,0.)
    m=ErrorModel(Parameters(a,p,q,p+q),nx=nx,route=route,c=c,kappa=k)
    components=[np.zeros_like(m.exact(0)) for _ in range(3)]
    for j in range(round(.01/dt)):
        t=j*dt;z=m.exact(t);zt=m.exact(t,True);zn=m.exact((j+1)*dt)
        fx=m.analytic_x_rhs(t);f=m.rhs(t,z)
        defects=[dt*(fx-zt),dt*(f-fx),z+dt*zt-zn] # y, x, Euler
        components=[e+dt*m.jac(t,z,e)+d for e,d in zip(components,defects)]
    # Use previously frozen actual trajectories for an independent endpoint comparison.
    purpose='main' if config=='main' else 'fine_time'
    manifest=OLD/'out'/('results.json' if config=='main' else 'refinements.json')
    data=json.loads(manifest.read_text(encoding='utf-8'))
    key=f'{case}_{route}_c{c:g}_k{k:g}_{purpose}';row=data['rows'][key]
    source=OLD/'out'/row['profile'];assert sha(source)==row['profile_sha256']
    actual=np.load(source)
    xx=-10+np.arange(nx*4)*20/(nx*4);ref=m.G.uv(m.js,xx,.01)
    actual_errors=[resample(actual['t0.01_'+f],nx*4,axis=-1)-rr for f,rr in zip(('u','v'),ref)]
    compuv=[]
    for e in components:
        ep,ev=m.unpack(e);compuv.append([resample(m.linear_u(ep),nx*4,axis=-1),resample(ev,nx*4,axis=-1)])
    ref_nodes=m.G.uv(m.js,m.X.x,.01)
    interp=[resample(rr,nx*4,axis=-1)-r for rr,r in zip(ref_nodes,ref)]
    pred=[sum(uv[i] for uv in compuv)+interp[i] for i in range(2)]
    metrics={};arrays={}
    for i,f in enumerate(('u','v')):
        act=actual_errors[i];pre=pred[i];index=np.unravel_index(np.argmax(abs(act)),act.shape)
        ex,ey=compuv[1][i],compuv[0][i]
        cosine=float(np.vdot(ex,ey).real/np.sqrt(np.vdot(ex,ex).real*np.vdot(ey,ey).real))
        metrics[f]=dict(actual=norm(act),predicted=norm(pre),relative_remainder=norm(pre-act)/norm(act),
            component_norms={label:norm(uv[i]) for label,uv in zip(('y','x','time'),compuv)},
            signed_components_at_actual_max={label:float(uv[i][index]) for label,uv in zip(('y','x','time'),compuv)},
            actual_at_max=float(act[index]),x_y_L2_cosine=cosine)
        arrays[f+'_actual']=act;arrays[f+'_predicted']=pre
        for label,uv in zip(('y','x','time'),compuv):arrays[f+'_'+label]=uv[i]
    path=OUT/f'propagation_{case}_{config}_{method}.npz';np.savez_compressed(path,**arrays)
    return dict(status='completed',metrics=metrics,profile=path.name,profile_sha256=sha(path),actual_source=str(source),actual_source_sha256=sha(source))
def main():
    specs={f'{case}_{config}_{method}':dict(case=case,config=config,method=method) for case in PARAMS for config in ('main','fine') for method in ('fd','original','theory')}
    path=OUT/'propagation.json';sources={str(p):sha(p) for p in [HERE/'error_model.py',Path(__file__),OLD/'model.py']}
    if path.exists():
        data=json.loads(path.read_text(encoding='utf-8'));assert data['plan']==specs and data['source_hashes']==sources
    else:
        data=dict(plan=specs,source_hashes=sources,rows={});dump(path,data)
    with ProcessPoolExecutor(max_workers=3) as pool:
        jobs={pool.submit(compute,s):(key,s) for key,s in specs.items() if key not in data['rows']}
        for job in as_completed(jobs):
            key,s=jobs[job]
            try:r=job.result()
            except Exception as e:r=dict(status='failed',error=str(e))
            data['rows'][key]=dict(spec=s,**r);dump(path,data)
            print(f'{len(data["rows"])}/24 {key}: {r["status"]}',flush=True)
if __name__=='__main__':
    from pathlib import Path
    main()
