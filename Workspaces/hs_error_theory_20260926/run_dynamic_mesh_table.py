"""Complete continuously moving 2HS mesh comparison; reuse matching frozen runs."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
import run_designed_cases as engine

HERE=Path(__file__).resolve().parent
OUT=HERE/'out_dynamic_mesh'
PS=(3.,4.,5.,6.,8.,10.,11.,12.,14.,16.,18.,20.,22.)
ROUTES=('integrable_original','integrable_calibrated','difference_matched',
        'difference_rho','difference_rm','difference_fixed')
TIMES=(.25,.5)
SOURCES=(HERE/'out_v2/results.json',
         engine.BASE/'out/calibration_parameter_scan/results.json',
         engine.BASE/'out/euler_comparison/results.json')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def plan():
    plans={}
    for p in PS:
        for route in ROUTES:
            variants=[('rk4',400,.003125,4.,'rk4'),('euler',400,.003125,4.,'euler'),
                      ('rk4',800,.003125,4.,'space'),('rk4',800,.0015625,4.,'time'),
                      ('euler',400,.0015625,4.,'euler_half')]
            if p in (3.,8.,20.,22.):variants+=[('rk4',500,.003125,5.,'domain')]
            for method,n,dt,half,purpose in variants:
                spec=dict(p=p,route=route,method=method,n=n,dt=dt,halfwidth=half,purpose=purpose)
                plans[engine.case_key(spec)]=spec
    return plans

def source_catalog():
    catalog={}
    hashes=engine.source_hashes()
    for src in SOURCES:
        data=json.loads(src.read_text(encoding='utf-8'))
        assert all(data['source_hashes'][k]==v for k,v in hashes.items())
        for key,row in data['rows'].items():
            if key in catalog or row['status']!='completed':continue
            profile=Path(row['profile'])
            if not profile.is_absolute():profile=src.parent/profile
            if not profile.exists():raise FileNotFoundError(profile)
            catalog[key]=(row,profile.resolve(),src.resolve())
    return catalog

def analyze(spec,profile):
    sol,system,initial,a,C=engine.initialize(spec['p'],spec['route'],spec['n'],spec['halfwidth'])
    initial_data=engine.fields(sol,system,initial,0.)
    x0=initial_data[0];d0=np.diff(x0)
    rr=np.load(profile)
    snaps={}
    for t in TIMES:
        data=tuple(rr[f't{t}_{k}'] for k in ('x','u','rho_x','rho'))
        x=data[0]
        snaps[str(t)]={'errors':engine.measure(spec['p'],data,t,16001),
                       'eval_32001':engine.measure(spec['p'],data,t,32001),
                       'node_displacement_linf':float(np.max(abs(x-x0))),
                       'spacing_change_linf':float(np.max(abs(np.diff(x)-d0))),
                       'min_h':float(np.min(np.diff(x))),
                       'min_rho':float(np.min(data[3]))}
    return dict(a=a,C=C,snapshots=snaps,
                movement_025_to_05=float(np.max(abs(rr['t0.5_x']-rr['t0.25_x']))),
                profile_sha256=sha(profile))

def motion_audit():
    """Advance every accepted step and audit coupled mesh motion, not only output."""
    results=[]
    for method in ('euler','rk4'):
        for route in ROUTES:
            p,n,dt,half=14.,400,.003125,4.
            sol,system,state,a,C=engine.initialize(p,route,n,half)
            initial=engine.fields(sol,system,state,0.)[0].copy()
            previous=initial.copy();moving_steps=0;min_h=np.inf;v_error=0.;euler_error=0.
            for j in range(160):
                t=j*dt
                if system is not None:
                    fields=system.fields(t,state)
                    dz=system.rhs(t,state)
                    velocity=-fields['u']
                    v_error=max(v_error,float(np.max(abs(dz[n:2*n]+fields['v']))))
                    state,_,_=engine.original_advance(system,t,state,dt,method)
                else:
                    from run_mesh_comparison import rhs
                    x=state[0]
                    _,rho,u,R=engine.unpack(state,sol,t,-half,half)
                    velocity=np.zeros_like(x)
                    if route=='difference_rho':velocity[1:-1]=-u[1:-1]
                    if route=='difference_rm':velocity[1:-1]=-u[1:-1]-(rho[1:-1]-1)/(2*R[1:-1])
                    actual=rhs(state,sol,t,route.split('_')[-1],-half,half)[0]
                    v_error=max(v_error,float(np.max(abs(actual-velocity))))
                    state=engine.ale_step(state,sol,t,dt,route.split('_')[-1],-half,half,method)
                current=engine.fields(sol,system,state,(j+1)*dt)[0]
                moved=float(np.max(abs(current-previous)))
                moving_steps+=int(moved>1e-13)
                if method=='euler':euler_error=max(euler_error,float(np.max(abs(current-previous-dt*velocity))))
                previous=current.copy()
                min_h=min(min_h,float(np.min(np.diff(current))))
            expected=0 if route=='difference_fixed' else 160
            assert moving_steps==expected,(route,method,moving_steps)
            assert v_error<1e-12 and euler_error<1e-12 and min_h>0
            results.append(dict(p=p,method=method,route=route,steps=160,moving_steps=moving_steps,
                                mesh_rhs_residual=v_error,euler_position_update_residual=euler_error if method=='euler' else None,
                                node_displacement_linf=float(np.max(abs(previous-initial))),min_h=min_h))
    return results

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    catalog=source_catalog();plans=plan()
    hashes={**engine.source_hashes(),'run_designed_cases.py':sha(HERE/'run_designed_cases.py'),
            'run_dynamic_mesh_table.py':sha(__file__)}
    config=dict(p=list(PS),routes=list(ROUTES),times=list(TIMES),methods=['euler','rk4'],
                n=400,dt=.003125,halfwidth=4.,core=[-2.,2.],peak='|theta|<=1',
                evaluation_points=[16001,32001],c_phys=1.,
                mesh_protocol='mesh and fields advanced together at every time stage; no initial-only control',
                scope='deterministic full-method comparison; no new statistical inference')
    frozen=dict(plan=plans,source_hashes=hashes,configuration=config,
                source_results_sha256={str(p):sha(p) for p in SOURCES})
    manifest=OUT/'plan.json'
    if manifest.exists():assert json.loads(manifest.read_text(encoding='utf-8'))==frozen
    else:engine.dump(manifest,frozen)
    path=OUT/'results.json'
    saved=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {**frozen,'rows':{}}
    assert saved['plan']==plans and saved['source_hashes']==hashes
    engine.OUT=OUT
    for key,spec in plans.items():
        if key in saved['rows']:continue
        try:
            if key in catalog:
                source,profile,src=catalog[key]
                assert all(source['spec'][k]==spec[k] for k in ('p','route','method','n','dt','halfwidth'))
                row={k:source[k] for k in ('status','initial_state_sha256','min_h','min_rho')}
                provenance=dict(kind='reused',source_results=str(src),source_key=key)
            else:
                source=engine.run_one(spec)
                profile=(OUT/source['profile']).resolve()
                row={k:source[k] for k in ('status','initial_state_sha256','min_h','min_rho')}
                provenance=dict(kind='new',seconds=source['seconds'])
            row.update(analyze(spec,profile),profile=str(profile),provenance=provenance,spec=spec)
        except Exception as exc:
            row=dict(spec=spec,status='failed',error=f'{type(exc).__name__}: {exc}')
        saved['rows'][key]=row
        engine.dump(path,saved)
        if row['status']=='failed' or row['provenance']['kind']=='new':
            print(f"{len(saved['rows'])}/{len(plans)} {key}: {row['status']}",flush=True)
    engine.dump(OUT/'motion_audit.json',dict(rows=motion_audit()))
    print('Completed',len(saved['rows']),'records and 12 full-step mesh audits',flush=True)

if __name__=='__main__':main()
