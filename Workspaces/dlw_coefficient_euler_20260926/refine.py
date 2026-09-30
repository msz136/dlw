"""Targeted controls after x-refinement revealed competing spatial errors.

Keep all original output. Check dt-halving at nx=512 for FD/original/theory,
then joint x/y refinement. These are diagnostics, not a revised main table.
"""
import json
from concurrent.futures import ProcessPoolExecutor,as_completed
from run import HERE,OUT,CASES,THEORY,DT,run_one,dump,hashes,sha

def main():
    plans={}
    for case in CASES:
        for route,c,kappa in [('fd',0.,0.),('sd',0.,0.),('sd',*THEORY)]:
            for purpose,h in [('fine_time',.125),('fine_xy',.0625)]:
                key=f'{case}_{route}_c{c:g}_k{kappa:g}_{purpose}'
                plans[key]=dict(case=case,route=route,c=c,kappa=kappa,purpose=purpose,h=h,nx=512,dt=DT/2,L=20.,yhalf=1.5)
    path=OUT/'refinements.json';sources={**hashes(),str(HERE/'refine.py'):sha(HERE/'refine.py')}
    if path.exists():
        data=json.loads(path.read_text());assert data['plan']==plans and data['source_hashes']==sources
    else:
        data=dict(plan=plans,source_hashes=sources,reason=__doc__,rows={});dump(path,data)
    with ProcessPoolExecutor(max_workers=4) as pool:
        jobs={pool.submit(run_one,s):(k,s) for k,s in plans.items() if k not in data['rows']}
        for job in as_completed(jobs):
            k,s=jobs[job]
            try:r=job.result()
            except Exception as exc:r=dict(status='failed',error=f'{type(exc).__name__}: {exc}')
            data['rows'][k]={'spec':s,**r};dump(path,data)
            print(f'{len(data["rows"])}/{len(plans)} {k}: {r["status"]}',flush=True)
if __name__=='__main__':main()
