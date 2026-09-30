"""Frozen experiments: two space methods, two moving branches, fixed baseline."""
from pathlib import Path
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from time import perf_counter
import argparse
import hashlib
import json
import numpy as np
from model import BranchProblem, Parameters, LIB, evaluate

HERE=Path(__file__).resolve().parent
OUT=HERE/'out'
CASES={
    'P1':Parameters(), 'P2':Parameters(p=2,q=3,rho=5),
    'P3':Parameters(a=3), 'P4':Parameters(a=6),
    'P5':Parameters(p=.5,q=1,rho=1.5), 'P6':Parameters(p=1,q=3,rho=4),
    'P7':Parameters(p=2,q=1,rho=3), 'P10':Parameters(a=2,p=1.5,q=2,rho=3.5)}
DT=.0000125

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def norm(a):return float(np.max(abs(a)))

def hashes():
    paths=[HERE/'model.py',Path(__file__),HERE.parent/'dlw_coefficient_euler_20260926/model.py']
    paths += [LIB/n for n in ('moving_mesh.py','parametric_open.py','parametric.py','dynamics.py','solver.py')]
    return {str(p):sha(p) for p in paths}

def plan(phase):
    ans={}
    for case in CASES:
        if phase=='pilot' and case not in ('P6','P10'):continue
        if phase=='space_y' and case not in ('P1','P2','P6','P10'):continue
        if phase=='domain_y' and case not in ('P2','P6','P10'):continue
        for route in ('fd','sd'):
            for branch in ('fixed','minus','plus'):
                h=.0625 if phase=='space_y' else .125
                nx=1024 if phase=='space_x' else 512
                dt=DT/2 if phase=='time_half' else DT
                yh=2. if phase=='domain_y' else 1.5
                key=f'{case}_{route}_{branch}_{phase}'
                ans[key]=dict(case=case,route=route,branch=branch,phase=phase,h=h,nx=nx,
                              L=40.,yhalf=yh,dt=dt,T=.01)
    return ans

def run_one(spec):
    p=BranchProblem(CASES[spec['case']],**{k:spec[k] for k in ('route','branch','h','nx','L','yhalf')})
    m,X=p.m,p.X
    z,s=p.initial();z0,s0=z.copy(),s.copy()
    start=perf_counter();n=round(spec['T']/spec['dt'])
    initial_hash=hashlib.sha256(z.tobytes()+s.tobytes()).hexdigest()
    u0,v0=m.fields(z,0)
    exact0=m.G.uv(m.js,X.x,0)
    initerr=max(norm(u0-exact0[0]),norm(v0-exact0[1]))
    assert initerr<2e-12
    e0=evaluate(p,z,s,0,reconstruction_factor=32)
    history=[dict(t=0.,**p.geometry(0,z,s,m.rhs(0,z)))]
    trajectory=[s.copy()];snapshots={};arrays={}
    steps_moving=0;maximum_velocity=0.;minimum_J=float(min(X.J));minimum_dx=float(min(X.spacing()))
    max_state=norm(z)
    observations={round(t/spec['dt']):t for t in (.005,.01)}
    for i in range(n):
        t=i*spec['dt']
        dz,V=p.rhs(t,z,s)
        maximum_velocity=max(maximum_velocity,norm(V))
        steps_moving += int(norm(V)>1e-12)
        z=z+spec['dt']*dz
        s=s+spec['dt']*V
        X.set_s(s)
        minimum_J=min(minimum_J,float(min(X.J)))
        minimum_dx=min(minimum_dx,float(min(X.spacing())))
        max_state=max(max_state,norm(z))
        if not np.all(np.isfinite(z)) or max_state>1000:
            raise FloatingPointError(f'state failure at t={(i+1)*spec["dt"]}')
        if (i+1) % (n//20)==0:
            now=(i+1)*spec['dt']
            history.append(dict(t=now,**p.geometry(now,z,s,m.rhs(now,z))))
            trajectory.append(s.copy())
        if i+1 in observations:
            now=observations[i+1]
            uv=m.fields(z,now);ref=m.G.uv(m.js,X.x,now)
            snapshots[str(now)]=dict(
                errors=evaluate(p,z,s,now),
                evaluation_double=evaluate(p,z,s,now,evaluation_factor=8),
                reconstruction_double=evaluate(p,z,s,now,reconstruction_factor=32),
                nodal_errors={f:norm(a-b) for f,a,b in zip(('u','v'),uv,ref)})
            arrays[f't{now}_z']=z.copy();arrays[f't{now}_s']=s.copy()
            arrays[f't{now}_u'],arrays[f't{now}_v']=uv
    output=OUT/'profiles'/f'{spec["case"]}_{spec["route"]}_{spec["branch"]}_{spec["phase"]}.npz'
    output.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(output,xi=X.xi,y=m.y,z0=z0,s0=s0,
        history_times=np.array([r['t'] for r in history]),mesh_history=np.array(trajectory),**arrays)
    # Bound analytic periodic-tail mismatch across endpoints at both observation times.
    tail=0.
    for tt in (0.,.005,.01):
        for derivative in (False,True):
            u,v=m.G.uv(np.r_[m.js[0]-1,m.js,m.js[-1]+1],np.array([-X.L/2,X.L/2]),tt,derivative)
            tail=max(tail,norm(u[:,1]-u[:,0]),norm(v[:,1]-v[:,0]))
    return dict(status='completed',steps=n,seconds=perf_counter()-start,snapshots=snapshots,
                initial_hash=initial_hash,initial_nodal_error=initerr,initial_output_error=e0,
                geometry=history,steps_with_nonzero_mesh_velocity=steps_moving,
                max_mesh_velocity=maximum_velocity,max_displacement_since_initial=norm(s-s0),
                minimum_J=minimum_J,minimum_spacing=minimum_dx,max_state=max_state,
                reference_endpoint_field_and_time_derivative_mismatch=tail,
                profile=str(output.relative_to(OUT)),profile_sha256=sha(output))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--phase',choices=['pilot','main','time_half','space_x','space_y','domain_y'],default='main')
    ap.add_argument('--workers',type=int,default=4)
    args=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/(args.phase+'.json');plans=plan(args.phase)
    header=dict(plan=plans,source_hashes=hashes(),configuration=dict(
        cases={k:asdict(v) for k,v in CASES.items()},integrator='explicit Euler for P,v and mesh simultaneously',
        moving_rule='same finite-h branch monitor and flux on FD/SD: X_t=(Q-Q_left)/R, every Euler step',
        initial_mesh='equal mass of same monitor on common continuous physical initial fields',
        density_strength=1.,spatial_coefficients=dict(c=0.,kappa=0.),
        mesh='all y layers share x=xi+s, fixed y; x endpoints pinned and periodic computational stencil',
        discretization='fourth-order mapped x D1=J^-1 Dxi, D2=D1(D1); second-order staggered y',
        reference='continuous u,v with unchanged a,p,q,rho; no finite-h exact reference',
        evaluation='common physical x in [-10,10), same y core |y|<1.5; mapped Fourier upsample and dense cubic evaluation',
        scope='deterministic short-time total physical-field errors; no long-time or population significance claim'))
    if path.exists():
        saved=json.loads(path.read_text(encoding='utf-8'))
        assert saved['plan']==plans and saved['source_hashes']==header['source_hashes']
    else:
        saved=dict(**header,rows={});dump(path,saved)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        jobs={pool.submit(run_one,spec):(key,spec) for key,spec in plans.items() if key not in saved['rows']}
        for fut in as_completed(jobs):
            key,spec=jobs[fut]
            try:row=fut.result()
            except Exception as exc:row=dict(status='failed',error=f'{type(exc).__name__}: {exc}')
            saved['rows'][key]=dict(spec=spec,**row);dump(path,saved)
            msg='' if row['status']!='completed' else ' '+str(row['snapshots']['0.01']['errors'])
            print(f'{len(saved["rows"])}/{len(plans)} {key}: {row["status"]}{msg}',flush=True)

if __name__=='__main__':main()
