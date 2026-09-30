"""Frozen Euler factorial comparison: FD vs nine local integrable families."""
from pathlib import Path
from dataclasses import asdict
from time import perf_counter
import argparse,hashlib,json
from concurrent.futures import ProcessPoolExecutor,as_completed
import numpy as np
from scipy.signal import resample
from model import FamilyModel,Parameters,LIB

HERE=Path(__file__).resolve().parent
OUT=HERE/'out'
CASES={
 'P1':Parameters(), 'P2':Parameters(p=2,q=3,rho=5),
 'P3':Parameters(a=3), 'P4':Parameters(a=6),
 'P5':Parameters(p=.5,q=1,rho=1.5), 'P6':Parameters(p=1,q=3,rho=4),
 'P7':Parameters(p=2,q=1,rho=3), 'P10':Parameters(a=2,p=1.5,q=2,rho=3.5)}
COEFS=(-.125,0.,.125)
TIMES=(.005,.01)
DT=.0000125
THEORY=(.04248652711,.00844851896)

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(path,d):path.write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def norm(z):return float(np.max(abs(z)))
def hashes():
    return {str(p):sha(p) for p in [HERE/'model.py',Path(__file__),LIB/'parametric.py',
            LIB/'parametric_open.py',LIB/'dynamics.py',LIB/'solver.py']}

def plan(pilot=False):
    configs=[('fd',0.,0.)]+[('sd',c,k) for c in COEFS for k in COEFS]+[('sd',*THEORY)]
    ans={}
    for name in CASES:
        for route,c,kappa in configs:
            if pilot and (name not in ('P1','P10') or c!=0 or kappa!=0):continue
            variants=[('main',.125,256,DT,20.,1.5)]
            if not pilot:
                variants += [('time_half',.125,256,DT/2,20.,1.5),
                             ('space_y',.0625,256,DT,20.,1.5),
                             ('space_x',.125,512,DT,20.,1.5)]
                if name in ('P1','P5','P10'):
                    variants += [('domain_x',.125,512,DT,40.,1.5),
                                 ('domain_y',.125,256,DT,20.,2.)]
            for purpose,h,nx,dt,L,yhalf in variants:
                key=f'{name}_{route}_c{c:g}_k{kappa:g}_{purpose}'
                ans[key]=dict(case=name,route=route,c=c,kappa=kappa,purpose=purpose,h=h,nx=nx,dt=dt,L=L,yhalf=yhalf)
    return ans

def errors(m,uv,t,factor):
    # Compare at a shared core and actual y nodes; x output is trigonometric interpolation.
    xx=-m.X.L/2+np.arange(m.X.n*factor)*m.X.L/(m.X.n*factor)
    maskx=(xx>=-10)&(xx<10);masky=abs(m.y)<1.5
    ref=m.G.uv(m.js[masky],xx[maskx],t)
    values=[resample(v,m.X.n*factor,axis=-1)[masky][:,maskx] if factor>1 else v[masky][:,maskx] for v in uv]
    return {f:norm(a-b) for f,a,b in zip(('u','v'),values,ref)}

def run_one(spec):
    m=FamilyModel(CASES[spec['case']],**{k:spec[k] for k in ('route','c','kappa','h','nx','L','yhalf')})
    z=m.exact(0.);u0,v0=m.fields(z,0.)
    exact0=m.G.uv(m.js,m.X.x,0.)
    assert max(norm(u0-exact0[0]),norm(v0-exact0[1]))<2e-12
    initial_sha=hashlib.sha256(z.tobytes()).hexdigest()
    steps=round(.01/spec['dt']);snaps={};arrays={};max_state=norm(z)
    samples={round(t/spec['dt']):t for t in TIMES}
    start=perf_counter()
    for j in range(steps):
        z=z+spec['dt']*m.rhs(j*spec['dt'],z)
        if not np.all(np.isfinite(z)) or norm(z)>1000:
            raise FloatingPointError(f'Failed at step {j+1}, t={(j+1)*spec["dt"]}')
        max_state=max(max_state,norm(z))
        if j+1 in samples:
            t=samples[j+1];uv=m.fields(z,t)
            snaps[str(t)]={'errors':errors(m,uv,t,4),'eval_double':errors(m,uv,t,8),
                           'nodal_errors':errors(m,uv,t,1)}
            for f,val in zip(('u','v'),uv):arrays[f't{t}_{f}']=val
    key=f'{spec["case"]}_{spec["route"]}_c{spec["c"]:g}_k{spec["kappa"]:g}_{spec["purpose"]}'
    profile=OUT/'profiles'/(key+'.npz');profile.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(profile,x=m.X.x,y=m.y,z=z,**arrays)
    return dict(status='completed',snapshots=snaps,steps=steps,seconds=perf_counter()-start,
                initial_state_sha256=initial_sha,initial_field_error=max(norm(u0-exact0[0]),norm(v0-exact0[1])),
                A=m.A,r=m.r,sminus=m.sminus,splus=m.splus,max_state=max_state,
                profile=str(profile.relative_to(OUT)),profile_sha256=sha(profile))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',action='store_true');ap.add_argument('--workers',type=int,default=4);args=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True);plans=plan(args.pilot)
    path=OUT/('pilot.json' if args.pilot else 'results.json')
    manifest=dict(plan=plans,source_hashes=hashes(),configuration=dict(cases={k:asdict(v) for k,v in CASES.items()},
        coefs=list(COEFS),theory_coefficients=THEORY,theory_source='../dlw_modified_equation_20260926/PARAMETER_OPTIMIZATION.md',times=list(TIMES),dt=DT,integrator='explicit Euler in shared P,v state',
        x_stencil='fourth-order central D1, D2=D1 composed with D1',
        state='P=delta_minus u and physical v, identical initial state for all routes',
        reference='continuous exact solution, unchanged physical a and common boundary',
        boundary='analytic left base/ghost, right ghost extrapolates perturbation quadratically relative to common exact background',
        evaluation='Linf on fixed y nodes in (-1.5,1.5), x in [-10,10), x interpolation to 4nx checked against 8nx',
        scope='deterministic short-time comparison, no long-time or statistical claim'))
    if path.exists():
        saved=json.loads(path.read_text(encoding='utf-8'))
        assert saved['plan']==plans and saved['source_hashes']==manifest['source_hashes']
    else:
        saved={**manifest,'rows':{}};dump(path,saved)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        jobs={pool.submit(run_one,spec):(key,spec) for key,spec in plans.items() if key not in saved['rows']}
        for future in as_completed(jobs):
            key,spec=jobs[future]
            try:row=future.result()
            except Exception as exc:row=dict(status='failed',error=f'{type(exc).__name__}: {exc}')
            saved['rows'][key]={'spec':spec,**row};dump(path,saved)
            print(f'{len(saved["rows"])}/{len(plans)} {key}: {row["status"]}',flush=True)

if __name__=='__main__':main()
