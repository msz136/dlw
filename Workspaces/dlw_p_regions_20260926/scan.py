"""Frozen one-parameter slice: a=4, q=3, rho=p+q; same Euler/ALE methods."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
from time import perf_counter
import sys,json,argparse,hashlib
import numpy as np

HERE=Path(__file__).resolve().parent
SYM=HERE.parent/'dlw_symmetric_mesh_euler_20260926'
sys.path.insert(0,str(SYM))
from sym_model import SymmetricProblem,Parameters,BASE,evaluate
from supplement import high_band
import run as baseline_run
OUT=HERE/'out'
sha,dump,norm=baseline_run.sha,baseline_run.dump,baseline_run.norm
PVALUES=[.5,.75,1.,1.25,1.5,1.75,2.,2.25,2.5]
CONFIGS={'main':(512,1.25e-5),'time_half':(512,6.25e-6),'fine_half':(1024,6.25e-6)}

def source_hashes():
    hh=baseline_run.hashes()
    for path in (Path(__file__),SYM/'sym_model.py',BASE/'supplement.py'):hh[str(path)]=sha(path)
    return hh

def make_spec(p,route,branch,config):
    nx,dt=CONFIGS[config]
    return dict(p=float(p),a=4.,q=3.,rho=float(p)+3.,route=route,branch=branch,config=config,
                nx=nx,dt=dt,h=.125,L=40.,yhalf=1.5,T=.01)

def key_of(s):return f'p{s["p"]:.6f}_{s["route"]}_{s["branch"]}_{s["config"]}'

def plans():
    return {key_of(s):s for p in PVALUES for config in CONFIGS for route in ('fd','sd')
            for branch in ('fixed','minus','plus','symmetric')
            for s in [make_spec(p,route,branch,config)]}

def old_rows():
    result={};manifest={}
    for name in ('main','time_half','space_x','space_y','supplement'):
        file=BASE/'out'/f'{name}.json';d=json.loads(file.read_text(encoding='utf-8'))
        result.update({key:(row,file,BASE/'out') for key,row in d['rows'].items()});manifest[str(file)]=sha(file)
    file=SYM/'out/results.json';d=json.loads(file.read_text(encoding='utf-8'))
    result.update({key:(row,file,SYM/'out') for key,row in d['rows'].items()});manifest[str(file)]=sha(file)
    return result,manifest

def reuse(spec):
    if spec['p'] not in (1.,2.):return None
    case='P6' if spec['p']==1 else 'P2'
    saved,_,root=old_rows()[0][f'{case}_{spec["route"]}_{spec["branch"]}_{spec["config"]}']
    for k in ('h','nx','L','yhalf','dt','T'):assert saved['spec'][k]==spec[k],k
    assert saved['status']=='completed'
    file=root/saved['profile'];assert sha(file)==saved['profile_sha256']
    aa=np.load(file);p=SymmetricProblem(Parameters(spec['a'],spec['p'],spec['q'],spec['rho']),
        **{k:spec[k] for k in ('route','branch','nx','h','L','yhalf')})
    snaps={}
    for ts,snap in saved['snapshots'].items():
        snaps[ts]={**snap,'bands':high_band(p,aa[f't{ts}_z'],aa[f't{ts}_s'],float(ts))}
    ih=hashlib.sha256(aa['z0'].tobytes()+aa['s0'].tobytes()).hexdigest()
    return dict(spec=spec,status=saved['status'],reused=True,completed_t=.01,
        snapshots=snaps,profile=str(file),profile_sha256=saved['profile_sha256'],initial_hash=ih,
        source_key=f'{case}_{spec["route"]}_{spec["branch"]}_{spec["config"]}',
        minimum_J=saved['minimum_J'],failure=None)

def one(spec):
    m=SymmetricProblem(Parameters(spec['a'],spec['p'],spec['q'],spec['rho']),
        **{k:spec[k] for k in ('route','branch','nx','h','L','yhalf')})
    z,s=m.initial();z0,s0=z.copy(),s.copy();ih=hashlib.sha256(z.tobytes()+s.tobytes()).hexdigest()
    n=round(spec['T']/spec['dt']);now=0.;status='completed';failure=None;snaps={};arrays={}
    traces=[];start=perf_counter();min_J=float(min(m.X.J));moving=0
    for i in range(n):
        try:
            dz,V=m.rhs(now,z,s);nz=z+spec['dt']*dz;ns=s+spec['dt']*V;m.X.set_s(ns)
            if not np.all(np.isfinite(nz)) or norm(nz)>1000:raise FloatingPointError('nonfinite or excessively large state')
            R,_=m.density_flux((i+1)*spec['dt'],nz)
            if min(R)<=0:raise ValueError('nonpositive monitor')
        except Exception as exc:
            status='failed';failure=dict(attempted_t=(i+1)*spec['dt'],last_valid_t=now,reason=f'{type(exc).__name__}: {exc}')
            m.X.set_s(s);break
        z,s=nz,ns;now=(i+1)*spec['dt'];min_J=min(min_J,float(min(m.X.J)));moving+=int(norm(V)>1e-12)
        if (i+1)%(n//10)==0:
            traces.append(dict(t=now,geometry=m.geometry(now,z,s),bands=high_band(m,z,s,now)))
        if any(abs(now-tt)<spec['dt']/4 for tt in (.005,.01)):
            tt=min((.005,.01),key=lambda tt:abs(tt-now))
            snaps[str(tt)]=dict(errors=evaluate(m,z,s,tt),
                evaluation_double=evaluate(m,z,s,tt,evaluation_factor=8),
                reconstruction_double=evaluate(m,z,s,tt,reconstruction_factor=32),bands=high_band(m,z,s,tt))
            arrays[f't{tt}_z']=z.copy();arrays[f't{tt}_s']=s.copy()
    file=OUT/'profiles'/(key_of(spec)+'.npz');file.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(file,z0=z0,s0=s0,xi=m.X.xi,y=m.m.y,last_z=z,last_s=s,last_t=now,**arrays)
    return dict(spec=spec,status=status,failure=failure,reused=False,completed_t=now,snapshots=snaps,traces=traces,
        initial_hash=ih,minimum_J=min_J,steps=round(now/spec['dt']),steps_with_nonzero_mesh_velocity=moving,
        max_displacement_since_initial=norm(s-s0),seconds=perf_counter()-start,
        profile=str(file),profile_sha256=sha(file))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--workers',type=int,default=4);args=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True);path=OUT/'scan.json';pp=plans();hh=source_hashes();_,refs=old_rows()
    if path.exists():
        d=json.loads(path.read_text(encoding='utf-8'));assert d['plan']==pp and d['source_hashes']==hh and d['comparison_manifests']==refs
    else:
        d=dict(plan=pp,source_hashes=hh,comparison_manifests=refs,configuration=dict(
            slice='a=4, q=3, rho=p+q; p=0.5:0.25:2.5',c=0.,kappa=0.,beta=1.,T=.01,
            integrator='Euler',density='fixed, minus, plus, symmetric',reference='common continuous u/v',
            ranking='Separate u and v errors; use common physical 8Nx evaluation. Pareto comparisons, no fitted scalar score.',
            interpretation='Sampled candidate regions, not a proof over continuous intervals.',
            diagnostic='High-band error above 40% of computational Nyquist; fraction>=0.1 flagged for sensitivity, not silently excluded.'),rows={})
        for key,spec in pp.items():
            r=reuse(spec)
            if r is not None:d['rows'][key]=r
        dump(path,d);print(f'Reused {len(d["rows"])} matching frozen runs',flush=True)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        jobs={pool.submit(one,spec):key for key,spec in pp.items() if key not in d['rows']}
        for fut in as_completed(jobs):
            key=jobs[fut]
            try:r=fut.result()
            except Exception as exc:r=dict(spec=pp[key],status='driver_failed',error=f'{type(exc).__name__}: {exc}')
            d['rows'][key]=r;dump(path,d)
            print(f'{len(d["rows"])}/{len(pp)} {key}: {r["status"]}, T={r.get("completed_t")}',flush=True)

if __name__=='__main__':main()
