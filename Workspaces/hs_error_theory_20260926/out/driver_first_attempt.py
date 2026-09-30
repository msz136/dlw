"""Theory-guided, deterministic cases. Frozen solvers are imported unchanged."""
from __future__ import annotations
import hashlib
import json
import sys
from functools import lru_cache
from pathlib import Path
from time import perf_counter
import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'hs_conserved_mesh_20260925'
sys.path.insert(0, str(BASE))
from run_parameter_calibration import (initialize, fields, original_advance, ale_step,
    unpack, reference, case_key, source_hashes, dump, MOVING)

OUT = HERE / 'out'
PS = (8., 11., 14., 18., 22.)
TIMES = (0., .0625, .125, .25, .5)
ROUTES = MOVING + ('difference_fixed', 'difference_rm')

@lru_cache(None)
def exact_grid(p, t, size, region):
    sol, _, _, _, _ = initialize(p, 'difference_matched', 400)
    s = 1 - 2/p
    beta = p - p/(p-1)
    center = (1-s*s)*t/4
    width = 1/beta + s/2*np.tanh(.5)
    bounds = (-2., 2.) if region == 'core' else (center-width, center+width)
    xx = np.linspace(*bounds, size)
    ue, re, _, _ = reference(sol, xx, t)
    return xx, ue, re

def measure(p, data, t, size):
    x, u, rx, rho = data
    out = {}
    for region in ('core', 'peak'):
        grid, ue, re = exact_grid(p,t,size,region)
        if grid[0] < max(x[0],rx[0]) or grid[-1] > min(x[-1],rx[-1]):
            raise ValueError('Evaluation window not covered')
        out[region] = {'u':float(np.max(abs(np.interp(grid,x,u)-ue))),
                       'rho':float(np.max(abs(np.interp(grid,rx,rho)-re)))}
    return out

def plan():
    plans = {}
    for p in PS:
        for route in ROUTES:
            variants = [('rk4',400,.003125,4.,'main'),
                        ('rk4',800,.003125,4.,'space_control'),
                        ('rk4',800,.0015625,4.,'time_control'),
                        ('euler',400,.003125,4.,'euler'),
                        ('euler',400,.0015625,4.,'euler_half')]
            if p in (8.,22.):
                variants += [('rk4',500,.003125,5.,'domain_control')]
            for method,n,dt,half,purpose in variants:
                spec = dict(p=p,route=route,method=method,n=n,dt=dt,
                            halfwidth=half,purpose=purpose)
                plans[case_key(spec)] = spec
    return plans

def run_one(spec):
    p,route,n,method,dt,half = (spec[k] for k in ('p','route','n','method','dt','halfwidth'))
    sol,system,state,a,C = initialize(p,route,n,half)
    mode = route.split('_')[-1]
    start = perf_counter()
    arrays, snapshots = {}, {}
    def save(t):
        data = fields(sol,system,state,t)
        snapshots[str(t)] = {'errors':measure(p,data,t,16001),
                            'eval_32001':measure(p,data,t,32001)}
        for name,arr in zip(('x','u','rho_x','rho'),data):
            arrays[f't{t}_{name}'] = arr.copy()
    init_hash = hashlib.sha256(b''.join(np.asarray(v).tobytes() for v in
                 (state if system is None else (state,)))).hexdigest()
    save(0.)
    samples = {int(round(t/dt)):t for t in TIMES[1:]}
    assert all(abs(j*dt-t)<1e-12 for j,t in samples.items())
    min_h,min_rho = np.inf,np.inf
    for j in range(1,int(round(.5/dt))+1):
        t = (j-1)*dt
        if system is not None:
            state,_,_ = original_advance(system,t,state,dt,method)
        else:
            state = ale_step(state,sol,t,dt,mode,-half,half,method)
            _,rr,_,_ = unpack(state,sol,j*dt,-half,half)
            min_h = min(min_h,float(np.min(np.diff(state[0]))))
            min_rho = min(min_rho,float(np.min(rr)))
        if j in samples:
            save(samples[j])
    if system is not None:
        min_h,min_rho = system.min_h,system.min_rho
    assert min_h > 0 and min_rho > 0
    profile = OUT/'profiles'/(case_key(spec)+'.npz')
    profile.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(profile,**arrays)
    return dict(status='completed',a=a,C=C,snapshots=snapshots,
                min_h=min_h,min_rho=min_rho,initial_state_sha256=init_hash,
                seconds=perf_counter()-start,profile=str(profile.relative_to(OUT)))

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    path = OUT/'results.json'
    plans = plan()
    hashes = {**source_hashes(), 'run_designed_cases.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    config = dict(p=list(PS),times=list(TIMES),routes=list(ROUTES),
                  primary_region='peak',peak_definition='|theta| <= 1',core=[-2,2],
                  primary_method='rk4',primary_n=400,primary_dt=.003125,
                  evaluation_points=[16001,32001],c_phys=1.,lambda_adjustment=False,
                  hypothesis='p >= 10.89898 gives peak RHS coefficient ratio <= 0.5; solution errors tested separately',
                  scope='deterministic theory-guided extension, no statistical inference')
    frozen = dict(configuration=config,plan=plans,source_hashes=hashes)
    manifest = OUT/'plan.json'
    if manifest.exists():
        assert json.loads(manifest.read_text(encoding='utf-8')) == frozen
    else:
        dump(manifest,frozen)
    saved = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {**frozen,'rows':{}}
    assert saved['source_hashes']==hashes and saved['plan']==plans
    for key,spec in plans.items():
        if key in saved['rows']:
            continue
        try:
            result=run_one(spec)
        except Exception as exc:
            result=dict(status='failed',error=f'{type(exc).__name__}: {exc}')
        saved['rows'][key]={'spec':spec,**result}
        dump(path,saved)
        print(f"{len(saved['rows'])}/{len(plans)} {key}: {result['status']}",flush=True)

if __name__=='__main__':
    main()
