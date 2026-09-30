"""Repeat only SD2, preserve every original integrator and baseline output."""
import json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
from consistent_sd2 import Problem,HERE,PRIOR
import run_experiments as old
from parametric import rk4
OUT=HERE/'out';OUT.mkdir(exist_ok=True)
SOURCES=[PRIOR/'out/results.json',PRIOR/'out/fine_time.json',HERE.parent/'dlw_two_soliton_euler_20260929/out/results.json']

def euler(fun,t,z,dt):return z+dt*fun(t,z)

def plan():
    pp=[]
    for p in SOURCES:
        d=json.loads(p.read_text(encoding='utf-8'))
        for r in d['runs']:
            if r['spec']['model']=='SD2':pp.append(dict(r['spec'],method='Euler' if 'euler' in str(p) else 'RK4'))
    return sorted(pp,key=lambda s:(s['variant']!='main',s['method'],s['case'],s['mesh'],s['variant']))

def one(s):
    old.OUT=OUT/s['method'];old.OUT.mkdir(exist_ok=True)
    old.rk4=euler if s['method']=='Euler' else rk4
    holder=[]
    def factory(spec):
        p=Problem(spec);holder.append(p);return p
    old.Problem=factory
    r=old.one(s);m=holder[0].m
    r['initialization']=m.lift_diagnostics
    r['boundary_solve_max_residual']=m.boundary_max_residual
    r['boundary_solves']=m.boundary_solves
    return r

def main():
    pp=plan();assert len(pp)==68
    sources={}
    for p in SOURCES:
        d=json.loads(p.read_text(encoding='utf-8'))
        sources.update(d['sources']);sources[str(p)]=old.previous.sha(p)
    sources.update({str(p):old.previous.sha(p) for p in (Path(__file__),HERE/'consistent_sd2.py',HERE/'implementation_checks.json')})
    for p,digest in sources.items():assert old.previous.sha(p)==digest,p
    dest=OUT/'results.json'
    d=json.loads(dest.read_text(encoding='utf-8')) if dest.exists() else dict(plan=pp,sources=sources,runs=[])
    assert d['plan']==pp and d['sources']==sources
    remaining=[s for s in pp if not any(r['spec']==s for r in d['runs'])]
    with ProcessPoolExecutor(max_workers=2) as pool:
        tasks={pool.submit(one,s):s for s in remaining}
        for f in as_completed(tasks):
            r=f.result();s=r['spec'];d['runs'].append(r);old.previous.dump(dest,d)
            print(len(d['runs']),s['method'],s['case'],s['mesh'],s['variant'],r['status'],r['reached'],r['history'][-1]['errors'],flush=True)
    print('DONE',len(d['runs']),flush=True)

if __name__=='__main__':main()
