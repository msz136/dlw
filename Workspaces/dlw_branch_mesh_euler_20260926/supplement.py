"""Adaptive follow-up to observed fine-x growth, retaining incomplete trajectories."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
from time import perf_counter
import argparse,json,hashlib
import numpy as np
from model import BranchProblem,evaluate
from run import CASES,DT,OUT,hashes,dump,norm,sha

HERE=Path(__file__).resolve().parent

def plans():
    ans={}
    groups=[('fine_half',['P1','P2','P6','P10'],1024,DT/2),
            ('fine_quarter',['P6'],1024,DT/4),
            ('main_quarter',['P5'],512,DT/4),
            ('fine_seed',['P2','P10'],1024,DT/2)]
    for phase,cases,nx,dt in groups:
        for case in cases:
            for route in ('fd','sd'):
                for branch in (('plus',) if phase=='fine_seed' else ('fixed','minus','plus')):
                    key=f'{case}_{route}_{branch}_{phase}'
                    ans[key]=dict(case=case,route=route,branch=branch,phase=phase,nx=nx,dt=dt,
                        L=40.,h=.125,yhalf=1.5,T=.01,seed_amplitude=1e-12 if phase=='fine_seed' else 0.)
    return ans

def high_band(p,z,s,t):
    p.X.set_s(s);uv=p.m.fields(z,t);ref=p.m.G.uv(p.m.js,p.X.x,t)
    result={}
    for f,a,b in zip(('u','v'),uv,ref):
        e=a-b;c=np.fft.rfft(e,axis=-1)
        # Above 40% of the computational Nyquist frequency: diagnostic, no filtering in evolution.
        c[:,:int(.4*(p.X.n//2))]=0
        hi=np.fft.irfft(c,n=p.X.n,axis=-1)
        result[f]=dict(total_nodal=norm(e),high_band_nodal=norm(hi))
    return result

def one(spec):
    p=BranchProblem(CASES[spec['case']],**{k:spec[k] for k in ('route','branch','nx','h','L','yhalf')})
    z,s=p.initial();initial_z=z.copy();s0=s.copy()
    if spec['seed_amplitude']:
        P,v=p.m.unpack(z)
        mode=round(.28*p.X.n)
        v=v+spec['seed_amplitude']*np.sin(2*np.pi*mode*np.arange(p.X.n)/p.X.n)[None,:]
        z=p.m.pack(P,v)
    z0=z.copy();n=round(spec['T']/spec['dt']);now=0.;status='completed';failure=None
    arrays={};snaps={};traces=[];start=perf_counter()
    min_J=float(min(p.X.J));min_spacing=float(min(p.X.spacing()));moving=0
    for i in range(n):
        try:
            dz,V=p.rhs(now,z,s)
            next_z=z+spec['dt']*dz;next_s=s+spec['dt']*V
            p.X.set_s(next_s)
            if not np.all(np.isfinite(next_z)) or norm(next_z)>1000:
                raise FloatingPointError('nonfinite or excessively large state')
            r,_=p.density_flux((i+1)*spec['dt'],next_z)
            if min(r)<=0: raise ValueError('nonpositive monitor density')
        except Exception as exc:
            status='failed';failure=dict(attempted_t=(i+1)*spec['dt'],last_valid_t=now,reason=f'{type(exc).__name__}: {exc}')
            p.X.set_s(s)
            break
        z,s=next_z,next_s;now=(i+1)*spec['dt']
        moving+=int(norm(V)>1e-12)
        min_J=min(min_J,float(min(p.X.J)));min_spacing=min(min_spacing,float(min(p.X.spacing())))
        if (i+1)%(n//20)==0:
            traces.append(dict(t=now,geometry=p.geometry(now,z,s),bands=high_band(p,z,s,now)))
        if any(abs(now-tt)<spec['dt']/4 for tt in (.005,.01)):
            tt=min((.005,.01),key=lambda tt:abs(tt-now))
            snaps[str(tt)]=dict(errors=evaluate(p,z,s,tt),
                evaluation_double=evaluate(p,z,s,tt,evaluation_factor=8),
                reconstruction_double=evaluate(p,z,s,tt,reconstruction_factor=32))
            arrays[f't{tt}_z']=z.copy();arrays[f't{tt}_s']=s.copy()
    key=f'{spec["case"]}_{spec["route"]}_{spec["branch"]}_{spec["phase"]}'
    file=OUT/'profiles'/(key+'.npz')
    np.savez_compressed(file,z0=z0,s0=s0,xi=p.X.xi,y=p.m.y,last_z=z,last_s=s,last_t=now,**arrays)
    return dict(spec=spec,status=status,failure=failure,completed_t=now,snapshots=snaps,traces=traces,
        minimum_J=min_J,minimum_spacing=min_spacing,steps_with_nonzero_mesh_velocity=moving,
        initial_seed_norm=norm(z0-initial_z),max_displacement_since_initial=norm(s-s0),
        seconds=perf_counter()-start,profile=str(file.relative_to(OUT)),profile_sha256=sha(file))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--workers',type=int,default=4);args=ap.parse_args()
    pp=plans();path=OUT/'supplement.json'
    hh=hashes();hh[str(Path(__file__))]=sha(__file__)
    if path.exists():
        d=json.loads(path.read_text());assert d['source_hashes']==hh and d['plan']==pp
    else:
        d=dict(plan=pp,source_hashes=hh,reason='Fine-x P2 showed large errors and P10 moving meshes failed; halve time step and retain pre-failure traces. P6 fine-quarter and P5 main-quarter check delicate small-error comparisons. Four seeded runs probe high-frequency sensitivity.',rows={})
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
