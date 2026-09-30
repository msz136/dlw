"""Euler waveform atlas: frozen p scan, exact matching reuse, unchanged solvers."""
import sys
import json
import hashlib
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
PREVIOUS=HERE.parent/'hs_error_theory_20260926'
sys.path.insert(0,str(PREVIOUS))
import run_designed_cases as engine
OUT=HERE/'out'
PS=tuple(float(p) for p in np.arange(3.,22.01,.5))
REPRESENTATIVES=(5.,14.,22.)
ROUTES=('integrable_original','integrable_calibrated','difference_matched','difference_rm','difference_fixed')
TIMES=(.25,.5)
SOURCE=PREVIOUS/'out_dynamic_mesh/results.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def plan():
    result={}
    for p in PS:
        for route in ROUTES:
            variants=[(400,.003125,'main'),(400,.0015625,'time_half')]
            if p in REPRESENTATIVES:variants.append((800,.0015625,'space_time_half'))
            for n,dt,purpose in variants:
                spec=dict(p=p,route=route,n=n,dt=dt,method='euler',halfwidth=4.,purpose=purpose)
                result[engine.case_key(spec)]=spec
    return result

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    old=json.loads(SOURCE.read_text(encoding='utf-8'))
    hashes=engine.source_hashes()
    assert all(old['source_hashes'][k]==v for k,v in hashes.items())
    hashes.update({'run_designed_cases.py':sha(PREVIOUS/'run_designed_cases.py'),'run_experiments.py':sha(__file__)})
    frozen=dict(plan=plan(),source_hashes=hashes,source_results_sha256=sha(SOURCE),
                configuration=dict(p=PS,representatives=REPRESENTATIVES,routes=ROUTES,times=TIMES,
                    method='euler',n=400,dt=.003125,core=[-2,2],evaluation_points=[16001,32001],
                    mesh_protocol='continuous coupled updates; no initial-only mesh control',
                    y_definition='continuous mass coordinate X; p is the soliton parameter',
                    reference='same continuous c_phys=1 soliton; physical point comparison',
                    scope='deterministic half-unit parameter grid; descriptive, not statistical inference'))
    frozen=json.loads(json.dumps(frozen))
    manifest=OUT/'plan.json'
    if manifest.exists():assert json.loads(manifest.read_text(encoding='utf-8'))==frozen
    else:engine.dump(manifest,frozen)
    path=OUT/'results.json'
    saved=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {**frozen,'rows':{}}
    assert saved['plan']==frozen['plan'] and saved['source_hashes']==hashes
    engine.OUT=OUT
    for key,spec in frozen['plan'].items():
        if key in saved['rows']:continue
        try:
            if key in old['rows']:
                oldrow=old['rows'][key]
                assert oldrow['status']=='completed'
                assert all(oldrow['spec'][k]==spec[k] for k in ('p','route','n','dt','method','halfwidth'))
                profile=Path(oldrow['profile'])
                assert sha(profile)==oldrow['profile_sha256']
                row={k:oldrow[k] for k in ('status','snapshots','min_h','min_rho','initial_state_sha256')}
                origin='reused'
            else:
                outcome=engine.run_one(spec)
                profile=(OUT/outcome['profile']).resolve()
                row={k:outcome[k] for k in ('status','min_h','min_rho','initial_state_sha256')}
                row['snapshots']={str(t):outcome['snapshots'][str(t)] for t in TIMES}
                origin='new'
            row.update(spec=spec,profile=str(profile),profile_sha256=sha(profile),provenance=origin)
        except Exception as exc:
            row=dict(spec=spec,status='failed',error=f'{type(exc).__name__}: {exc}')
        saved['rows'][key]=row;engine.dump(path,saved)
        if len(saved['rows'])%20==0 or row['status']=='failed':
            print(f"{len(saved['rows'])}/{len(frozen['plan'])} {key}: {row['status']}",flush=True)
    print('Finished',len(saved['rows']),'cases',flush=True)

if __name__=='__main__':main()
