"""Check fine-x time error and jointly refine x,y; preserve primary records."""
import json
from pathlib import Path
from run_sd2 import one,OUT,HERE,previous

def main():
    variants={'x_half_time_half':(512,.125,.00003125),'xy_half':(512,.0625,.0000625)}
    plan=[dict(case=c,model='SD2',mesh=mesh,variant=k,nx=n,L=40.,h=h,dt=dt,T=.02) for c in previous.CASES for mesh in ('fixed','moving') for k,(n,h,dt) in variants.items()]
    dest=OUT/'controls.json';sources={str(p):previous.sha(p) for p in (Path(__file__),HERE/'sd2.py',HERE/'run_sd2.py')}
    d=json.loads(dest.read_text()) if dest.exists() else dict(plan=plan,sources=sources,runs=[])
    assert d['plan']==plan and d['sources']==sources
    for s in plan:
        if any(r['spec']==s for r in d['runs']):continue
        r=one(s);d['runs'].append(r);previous.dump(dest,d)
        print(len(d['runs']),s['case'],s['mesh'],s['variant'],r['status'],r['history'][-1]['errors'],flush=True)

if __name__=='__main__':main()
