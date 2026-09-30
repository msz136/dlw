"""Forward Euler on the frozen two-soliton RHS and mesh implementation."""
import sys,json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parent/'dlw_two_soliton_20260929'
sys.path.insert(0,str(PRIOR))
import run_experiments as old
OUT=HERE/'out';OUT.mkdir(exist_ok=True)

def euler(fun,t,z,dt):return z+dt*fun(t,z)

def one(s):
    # Process-local time-step dispatch; historical source and output stay intact.
    old.OUT=OUT
    old.rk4=euler
    return old.one(s)

def plan():
    base=old.make_plan()
    result=[dict(s,method='Euler') for s in base]
    for s in base:
        if s['variant']=='main':result.append(dict(s,method='Euler',variant='time_quarter',dt=s['dt']/4))
        if s['variant']=='x_half' and s['case']=='fig4' and s['mesh']=='moving':
            result.append(dict(s,method='Euler',variant='x_half_time_half',dt=s['dt']/2))
    return result

def main():
    pp=plan();dest=OUT/'results.json'
    rk=json.loads((PRIOR/'out/results.json').read_text(encoding='utf-8'))
    sources=dict(rk['sources']);sources[str(Path(__file__))]=old.previous.sha(__file__)
    for p,digest in sources.items():assert old.previous.sha(p)==digest
    d=json.loads(dest.read_text(encoding='utf-8')) if dest.exists() else dict(plan=pp,parameters=rk['parameters'],sources=sources,runs=[])
    assert d['plan']==pp and d['sources']==sources
    remaining=[s for s in pp if not any(r['spec']==s for r in d['runs'])]
    with ProcessPoolExecutor(max_workers=2) as pool:
        tasks={pool.submit(one,s):s for s in remaining}
        for f in as_completed(tasks):
            r=f.result();s=r['spec'];d['runs'].append(r);old.previous.dump(dest,d)
            print(len(d['runs']),s['case'],s['model'],s['mesh'],s['variant'],r['status'],r['history'][-1]['errors'],flush=True)
    print('DONE',len(d['runs']),flush=True)

if __name__=='__main__':main()
