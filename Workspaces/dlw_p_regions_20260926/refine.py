"""Targeted confirmation around the observed r-minus SD/FD crossover."""
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
import json,argparse
from scan import OUT,SYM,BASE,make_spec,key_of,one,source_hashes,sha,dump,old_rows

def plans():
    result={}
    for p in (.9,.95,1.05,1.1):
        for phase in ('main','time_half','fine_half'):
            for route in ('fd','sd'):
                for branch in ('fixed','minus'):
                    s=make_spec(p,route,branch,phase);result[key_of(s)]=s
    for p in (.9,1.,1.1):
        for route in ('fd','sd'):
            for branch in ('fixed','minus'):
                s=make_spec(p,route,branch,'fine_half');s.update(config='fine_quarter',dt=3.125e-6)
                result[key_of(s)]=s
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--workers',type=int,default=4);args=ap.parse_args()
    path=OUT/'refinement.json';pp=plans();hh=source_hashes();hh[str(Path(__file__))]=sha(__file__)
    old,refs=old_rows()
    if path.exists():
        d=json.loads(path.read_text(encoding='utf-8'));assert d['plan']==pp and d['source_hashes']==hh
    else:
        d=dict(plan=pp,source_hashes=hh,comparison_manifests=refs,
               rationale='Coarse scan showed r-minus SD/FD trade-offs at p=.75 and 1.25 but double-field advantage at p=1. Confirm p=.9:.05:1.1 with both space/time settings, plus smaller fine-grid time step at endpoints and center.',rows={})
        for key,s in pp.items():
            if s['p']==1.:
                oldkey=f'P6_{s["route"]}_{s["branch"]}_fine_quarter';r,_,root=old[oldkey];file=root/r['profile']
                assert sha(file)==r['profile_sha256']
                # Source supplement stores both 4Nx and 8Nx physical evaluations.
                d['rows'][key]=dict(spec=s,status='completed',reused=True,completed_t=.01,snapshots=r['snapshots'],
                    profile=str(file),profile_sha256=r['profile_sha256'],source_key=oldkey,minimum_J=r['minimum_J'],failure=None)
        dump(path,d)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        jobs={pool.submit(one,spec):key for key,spec in pp.items() if key not in d['rows']}
        for fut in as_completed(jobs):
            key=jobs[fut]
            try:r=fut.result()
            except Exception as exc:r=dict(spec=pp[key],status='driver_failed',error=f'{type(exc).__name__}: {exc}')
            d['rows'][key]=r;dump(path,d);print(f'{len(d["rows"])}/{len(pp)} {key}: {r["status"]}',flush=True)

if __name__=='__main__':main()
