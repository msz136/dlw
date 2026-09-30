"""Targeted expanded-domain checks prompted by P5's slowly decaying tails."""
import json
from concurrent.futures import ProcessPoolExecutor,as_completed
from run import HERE,OUT,THEORY,DT,run_one,dump,hashes,sha

def main():
    plans={}
    variants=[('P5','wide_fine',.125,1024,40.,1.5),('P5','wide_fine_xy',.0625,1024,40.,1.5),
              ('P6','wide_fine',.125,1024,40.,1.5),('P6','tall_fine',.125,512,20.,2.),
              ('P1','tall_fine',.125,512,20.,2.)]
    for case,purpose,h,nx,L,yhalf in variants:
        for route,c,kappa in [('fd',0.,0.),('sd',0.,0.),('sd',*THEORY)]:
            key=f'{case}_{route}_c{c:g}_k{kappa:g}_{purpose}'
            plans[key]=dict(case=case,route=route,c=c,kappa=kappa,purpose=purpose,h=h,nx=nx,dt=DT/2,L=L,yhalf=yhalf)
    path=OUT/'boundary_controls.json';sources={**hashes(),str(HERE/'boundary_control.py'):sha(HERE/'boundary_control.py')}
    if path.exists():
        data=json.loads(path.read_text());assert data['plan']==plans and data['source_hashes']==sources
    else:
        data=dict(plan=plans,source_hashes=sources,reason=__doc__,rows={});dump(path,data)
    with ProcessPoolExecutor(max_workers=3) as pool:
        jobs={pool.submit(run_one,s):(k,s) for k,s in plans.items() if k not in data['rows']}
        for job in as_completed(jobs):
            k,s=jobs[job]
            try:r=job.result()
            except Exception as exc:r=dict(status='failed',error=f'{type(exc).__name__}: {exc}')
            data['rows'][k]={'spec':s,**r};dump(path,data)
            print(f'{len(data["rows"])}/{len(plans)} {k}: {r["status"]}',flush=True)
if __name__=='__main__':main()
