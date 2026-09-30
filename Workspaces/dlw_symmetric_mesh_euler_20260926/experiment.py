"""Matched symmetric-density experiments with full failure retention."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
from dataclasses import asdict
from time import perf_counter
import argparse,json,hashlib
import numpy as np
from sym_model import SymmetricProblem,BASE,evaluate
import run as baseline_run
from supplement import high_band

HERE=Path(__file__).resolve().parent
OUT=HERE/'out'
CASES=baseline_run.CASES
DT=baseline_run.DT
sha,dump,norm=baseline_run.sha,baseline_run.dump,baseline_run.norm

def plans():
    result={}
    groups=[('main',list(CASES),512,.125,DT),
            ('time_half',list(CASES),512,.125,DT/2),
            ('space_x',list(CASES),1024,.125,DT),
            ('space_y',['P1','P2','P6','P10'],512,.0625,DT),
            ('fine_half',['P1','P2','P6','P10'],1024,.125,DT/2),
            ('fine_quarter',['P6'],1024,.125,DT/4),
            ('main_quarter',['P5'],512,.125,DT/4),
            ('fine_seed',['P2','P10'],1024,.125,DT/2)]
    for phase,cases,nx,h,dt in groups:
        for case in cases:
            for route in ('fd','sd'):
                key=f'{case}_{route}_symmetric_{phase}'
                result[key]=dict(case=case,route=route,branch='symmetric',phase=phase,nx=nx,h=h,dt=dt,
                    L=40.,yhalf=1.5,T=.01,seed_amplitude=1e-12 if phase=='fine_seed' else 0.)
    return result

def one(spec):
    p=SymmetricProblem(CASES[spec['case']],**{k:spec[k] for k in ('route','branch','nx','h','L','yhalf')})
    z,s=p.initial();clean_z=z.copy();s0=s.copy()
    u,v=p.m.fields(z,0);ref=p.m.G.uv(p.m.js,p.X.x,0)
    initial_error=max(norm(u-ref[0]),norm(v-ref[1]));assert initial_error<2e-12
    output0=evaluate(p,z,s,0,reconstruction_factor=32)
    if spec['seed_amplitude']:
        P,v=p.m.unpack(z);mode=round(.28*p.X.n)
        v=v+spec['seed_amplitude']*np.sin(2*np.pi*mode*np.arange(p.X.n)/p.X.n)[None,:]
        z=p.m.pack(P,v)
    z0=z.copy();initial_hash=hashlib.sha256(z.tobytes()+s.tobytes()).hexdigest()
    n=round(spec['T']/spec['dt']);now=0.;status='completed';failure=None
    arrays={};snapshots={};start=perf_counter()
    traces=[dict(t=0.,geometry=p.geometry(0,z,s,p.m.rhs(0,z)),bands=high_band(p,z,s,0.))]
    meshes=[s.copy()];min_J=float(min(p.X.J));min_spacing=float(min(p.X.spacing()))
    min_R=traces[0]['geometry']['min_R'];moving=0;maximum_velocity=0.
    for i in range(n):
        try:
            dz,V=p.rhs(now,z,s)
            next_z=z+spec['dt']*dz;next_s=s+spec['dt']*V
            p.X.set_s(next_s)
            if not np.all(np.isfinite(next_z)) or norm(next_z)>1000:
                raise FloatingPointError('nonfinite or excessively large state')
            R,_=p.density_flux((i+1)*spec['dt'],next_z)
            if min(R)<=0:raise ValueError('nonpositive symmetric density')
        except Exception as exc:
            status='failed';failure=dict(attempted_t=(i+1)*spec['dt'],last_valid_t=now,reason=f'{type(exc).__name__}: {exc}')
            p.X.set_s(s);break
        z,s=next_z,next_s;now=(i+1)*spec['dt']
        moving+=int(norm(V)>1e-12);maximum_velocity=max(maximum_velocity,norm(V))
        min_J=min(min_J,float(min(p.X.J)));min_spacing=min(min_spacing,float(min(p.X.spacing())));min_R=min(min_R,float(min(R)))
        if (i+1)%(n//20)==0:
            traces.append(dict(t=now,geometry=p.geometry(now,z,s,p.m.rhs(now,z)),bands=high_band(p,z,s,now)))
            meshes.append(s.copy())
        if any(abs(now-tt)<spec['dt']/4 for tt in (.005,.01)):
            tt=min((.005,.01),key=lambda tt:abs(tt-now))
            uv=p.m.fields(z,tt);ref=p.m.G.uv(p.m.js,p.X.x,tt)
            snapshots[str(tt)]=dict(errors=evaluate(p,z,s,tt),
                evaluation_double=evaluate(p,z,s,tt,evaluation_factor=8),
                reconstruction_double=evaluate(p,z,s,tt,reconstruction_factor=32),
                nodal_errors={f:norm(a-b) for f,a,b in zip(('u','v'),uv,ref)})
            arrays[f't{tt}_z']=z.copy();arrays[f't{tt}_s']=s.copy()
            arrays[f't{tt}_u'],arrays[f't{tt}_v']=uv
    key=f'{spec["case"]}_{spec["route"]}_symmetric_{spec["phase"]}'
    file=OUT/'profiles'/(key+'.npz')
    np.savez_compressed(file,z0=z0,s0=s0,xi=p.X.xi,y=p.m.y,last_z=z,last_s=s,last_t=now,
        history_times=np.array([tr['t'] for tr in traces]),mesh_history=np.array(meshes),**arrays)
    return dict(spec=spec,status=status,failure=failure,completed_t=now,snapshots=snapshots,traces=traces,
        steps=round(now/spec['dt']),minimum_J=min_J,minimum_spacing=min_spacing,minimum_R=min_R,
        steps_with_nonzero_mesh_velocity=moving,max_mesh_velocity=maximum_velocity,initial_hash=initial_hash,
        initial_nodal_error=initial_error,initial_output_error=output0,initial_seed_norm=norm(z0-clean_z),
        max_displacement_since_initial=norm(s-s0),seconds=perf_counter()-start,
        profile=str(file.relative_to(OUT)),profile_sha256=sha(file))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--workers',type=int,default=4);args=ap.parse_args()
    (OUT/'profiles').mkdir(parents=True,exist_ok=True)
    pp=plans();path=OUT/'results.json';hh=baseline_run.hashes()
    for f in (HERE/'sym_model.py',Path(__file__),BASE/'supplement.py'):hh[str(f)]=sha(f)
    reuse={str(BASE/'out'/f):sha(BASE/'out'/f) for f in ('main.json','time_half.json','space_x.json','space_y.json','supplement.json')}
    if path.exists():
        d=json.loads(path.read_text(encoding='utf-8'));assert d['source_hashes']==hh and d['plan']==pp and d['comparison_manifests']==reuse
    else:
        d=dict(plan=pp,source_hashes=hh,comparison_manifests=reuse,configuration=dict(
            cases={k:asdict(v) for k,v in CASES.items()},density='arithmetic mean of aligned finite-h r_minus and r_plus',
            flux='same arithmetic mean of aligned branch fluxes; velocity formed AFTER mixing',
            beta=1.,c=0.,kappa=0.,integrator='Euler',reference='same continuous physical u,v',
            controls='matched to existing frozen branch experiments, unchanged initial rule, boundaries and error evaluation'),rows={})
        dump(path,d)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        jobs={pool.submit(one,spec):key for key,spec in pp.items() if key not in d['rows']}
        for fut in as_completed(jobs):
            key=jobs[fut]
            try:r=fut.result()
            except Exception as exc:r=dict(spec=pp[key],status='driver_failed',error=f'{type(exc).__name__}: {exc}')
            d['rows'][key]=r;dump(path,d)
            print(f'{len(d["rows"])}/{len(pp)} {key}: {r["status"]}, T={r.get("completed_t")}, errors={r.get("snapshots",{}).get("0.01",{}).get("errors")}',flush=True)

if __name__=='__main__':main()
