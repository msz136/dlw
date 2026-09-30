"""Exploratory 3x3x3 parameter boxes near P2/P6, with frozen numerical configurations."""
from pathlib import Path
import sys,json,hashlib
from itertools import product
from concurrent.futures import ProcessPoolExecutor,as_completed
import numpy as np
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'dlw_coefficient_euler_20260926'
sys.path.insert(0,str(OLD))
from model import FamilyModel,Parameters
from run import errors,THEORY,hashes as old_hashes
OUT=HERE/'out';OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def norm(x):return float(np.max(abs(x)))
def plans():
    ans={}
    for name,center in [('P2',(4.,2.,3.)),('P6',(4.,1.,3.))]:
        for offsets in product((-.1,0.,.1),repeat=3):
            pars=[v+dv for v,dv in zip(center,offsets)]
            point=name+'_'+''.join('m' if x<0 else 'p' if x>0 else '0' for x in offsets)
            for config,nx,dt in [('main',256,1.25e-5),('fine',512,6.25e-6)]:
                for method,route,c,kappa in [('fd','fd',0.,0.),('original','sd',0.,0.),('theory','sd',*THEORY)]:
                    key=f'{point}_{config}_{method}'
                    ans[key]=dict(point=point,center=name,parameters=pars,offsets=offsets,config=config,nx=nx,dt=dt,
                        h=.125,L=20.,yhalf=1.5,T=.01,method=method,route=route,c=c,kappa=kappa)
    return ans
def compute(spec):
    a,p,q=spec['parameters'];m=FamilyModel(Parameters(a,p,q,p+q),**{k:spec[k] for k in ('route','c','kappa','h','nx','L','yhalf')})
    z=m.exact(0);initial_sha=hashlib.sha256(z.tobytes()).hexdigest();dt=spec['dt']
    n=round(spec['T']/dt)
    for i in range(n):
        z+=dt*m.rhs(i*dt,z)
        if not np.all(np.isfinite(z)) or norm(z)>1e3:raise FloatingPointError(f'Failed at step {i+1}')
    uv=m.fields(z,spec['T']);err=errors(m,uv,spec['T'],4);doubled=errors(m,uv,spec['T'],8)
    path=OUT/(spec['point']+'_'+spec['config']+'_'+spec['method']+'.npz')
    np.savez_compressed(path,u=uv[0],v=uv[1],x=m.X.x,y=m.y,z=z)
    return dict(status='completed',errors=err,eval_double=doubled,profile=path.name,profile_sha256=sha(path),initial_sha256=initial_sha)
def main():
    plan=plans();path=OUT/'scan.json'
    # Round-trip plans before equality checks: JSON does not preserve tuples.
    plan=json.loads(json.dumps(plan))
    src={**old_hashes(),str(Path(__file__)):sha(__file__)}
    if path.exists():
        data=json.loads(path.read_text(encoding='utf-8'));assert data['plan']==plan and data['source_hashes']==src
    else:
        data=dict(plan=plan,source_hashes=src,scope='Exploratory grid of parameters, not interval certification or random sampling',rows={});dump(path,data)
    with ProcessPoolExecutor(max_workers=4) as pool:
        jobs={pool.submit(compute,s):(key,s) for key,s in plan.items() if key not in data['rows']}
        for job in as_completed(jobs):
            key,s=jobs[job]
            try:r=job.result()
            except Exception as e:r=dict(status='failed',error=str(e))
            data['rows'][key]=dict(spec=s,**r);dump(path,data)
            if len(data['rows'])%12==0:print(f'{len(data["rows"])}/{len(plan)}',flush=True)
if __name__=='__main__':main()
