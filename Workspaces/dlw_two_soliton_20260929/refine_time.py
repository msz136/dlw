"""Additional fine-x time check for Fig4 moving-grid spatial sensitivity."""
import json
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
from run_experiments import make_plan,one,OUT,HERE,previous

def main():
    plan=[]
    for s in make_plan():
        if s['case']=='fig4' and s['mesh']=='moving' and s['variant']=='x_half':
            s=dict(s,variant='x_half_time_half',dt=s['dt']/2);plan.append(s)
    dest=OUT/'fine_time.json'
    sources={str(p):previous.sha(p) for p in (Path(__file__),HERE/'run_experiments.py',HERE/'reference.py',HERE/'models.py',HERE.parent/'dlw_sd2_20260929/sd2.py')}
    d=json.loads(dest.read_text(encoding='utf-8')) if dest.exists() else dict(plan=plan,sources=sources,runs=[])
    assert d['plan']==plan and d['sources']==sources
    for s in plan:
        if any(r['spec']==s for r in d['runs']):continue
        r=one(s);d['runs'].append(r);previous.dump(dest,d)
        print(s['model'],r['status'],r['history'][-1]['errors'],flush=True)

if __name__=='__main__':main()
