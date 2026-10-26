"""Natural-edge reconstruction on the existing nondegenerate benchmarks."""
from pathlib import Path
import importlib.util,sys,json,time,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
REF=BASE/'nondegenerate_rk4_20261024'
ROOT=BASE.parents[2]
spec=importlib.util.spec_from_file_location('nondegenerate_run',REF/'run.py')
reference=importlib.util.module_from_spec(spec);spec.loader.exec_module(reference)
from probe import invert,transform
from rerun_20261024 import rhs

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def compute(case):
    dest=HERE/f'{case}.json'
    if dest.exists():
        print('Existing result retained',case,flush=True);return
    start=time.perf_counter()
    m=reference.NondegenerateModel(case,'Centered-SD');m.gauge='local'
    u0=m.profile(m.y,0)[0];yv=(m.y[1:]+m.y[:-1])/2
    v0=m.profile(yv,0)[1]
    data=reference.initial_data(case,m.x,m.y[:1])
    w,_,_=invert(m,u0,v0,(data['v']-data['uy'])[0])
    z0=np.array([u0,w]);z=z0.copy()
    initial_error=[float(np.max(abs(z[0]-u0))),float(np.max(abs(transform(m,*z)-v0)))]
    assert max(initial_error)<1e-12
    # Separate assembly from the displayed natural-edge u equation.
    rate=rhs(m,0,z0)
    H=u0*u0/2+4*u0
    Aw=w*w/32-w/4
    r=-np.diff(m.d1(H),axis=0)/m.h-m.d2(v0)-m.h*np.diff(m.d1(Aw),axis=0)
    lower=m.ut(m.y[:1],0)
    independent_ut=np.concatenate((lower,lower+m.h*np.cumsum(r,axis=0)))
    identity=float(np.max(abs(independent_ut-rate[0])))
    assert identity<1e-10
    with np.errstate(over='raise',invalid='raise',divide='raise'):
        for i in range(100):
            z=reference.rk4(lambda t,z:rhs(m,t,z),i*1e-4,z)
            assert np.isfinite(z).all() and np.max(abs(z))<1e6
            if (i+1)%25==0:print(case,'step',i+1,flush=True)
    v=transform(m,*z)
    error,pu,pv,ur,vr=reference.errors(m,z[0],v,yv,.01)
    prior_path=REF/f'{case}_Centered-SD_RK4.npz'
    prior_record=json.loads(prior_path.with_suffix('.json').read_text())
    cert=json.loads((REF/'reference_certificate.json').read_text())
    cert_case=next(c for c in cert['cases'] if c['case']==case)
    assert sha(prior_path)==prior_record['artifact_sha256']
    assert str(prior_path.resolve()) in cert_case['files']
    assert sha(prior_path)==cert_case['files'][str(prior_path.resolve())]
    prior=np.load(prior_path)
    for key,value in [('x',m.x),('y',m.y),('yv',yv),('u_ref',ur),('v_ref',vr)]:
        assert np.array_equal(prior[key],value),key
    artifact=dest.with_suffix('.npz')
    np.savez_compressed(artifact,x=m.x,y=m.y,yv=yv,z=z,z0=z0,u=z[0],v=v,u_ref=ur,v_ref=vr)
    saved=np.load(artifact)
    mapped=np.diff(saved['z'][0],axis=0)/m.h+(saved['z'][1,1:]+saved['z'][1,:-1])/2
    assert np.array_equal(mapped,saved['v'])
    check=[reference.measured(m,saved['u']-saved['u_ref'],m.y)[0],reference.measured(m,saved['v']-saved['v_ref'],yv)[0]]
    assert check==error
    src=[Path(__file__),REF/'run.py',REF/'reference_grid.py',reference.PROBE/'probe.py',reference.PROBE/'rerun_20261024.py',reference.PROJECT/'spatial_audit_20261023/run.py']
    record=dict(case=case,method='Centered-SD natural edge',integrator='RK4',h=.1,dx=.1,dt=1e-4,T=.01,reached=.01,status='complete',error=error,argmax_u=pu,argmax_v=pv,initial_error=initial_error,independent_initial_rhs_difference=identity,recomputed_error=check,reference_bound=cert['uniform_bound_each'],reference_values_identical_to_certified_artifact=str(prior_path.relative_to(ROOT)),certified_artifact_sha256=sha(prior_path),artifact=str(artifact.relative_to(ROOT)),artifact_sha256=sha(artifact),sources=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in src],boundary='Exact continuous lower u_t; all w nodes evolved; initial lower w=v-u_y',seconds=time.perf_counter()-start)
    dest.write_text(json.dumps(record,indent=2),encoding='utf-8')
    print(json.dumps(record),flush=True)

if __name__=='__main__':compute(sys.argv[1])
