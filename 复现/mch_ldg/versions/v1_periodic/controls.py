"""Prespecified controls after observing the first baseline, not paper settings."""
import argparse,json
from datetime import datetime
from pathlib import Path
from mch.experiment import run

ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['domain','projection','rk4'],default='domain');args=ap.parse_args()
configs=[]
base=dict(case='5.1',left=-40.,right=40.,kappa=0.,alpha=.5,k=3,n=80,T=.5,dt=.001,projection='radau',outputs=3,flux='conservative')
if args.mode=='domain':
    for k in (1,2,3):
        for n in (80,160,320):
            for flux in ('conservative','dissipative'):
                configs.append(dict(base,k=k,n=n,flux=flux,dt=.02*(80/n)/(2*k+1)))
elif args.mode=='projection':
    for flux in ('conservative','dissipative'):
        configs.append(dict(base,case='5.4',left=-20.,right=20.,n=640,T=5,dt=.0005,projection='l2',outputs=21))
        configs[-1]['flux']=flux
else:
    for dt in (.02,.01,.005,.0025,.00125):
        configs.append(dict(base,n=40,T=.5,dt=dt,outputs=2))
rows=[];out=Path('results')/f"control_{args.mode}_{datetime.now():%Y%m%d_%H%M%S}.json"
for i,c in enumerate(configs):
    Path(f'configs/control_{args.mode}_{i:02}.json').write_text(json.dumps(c,indent=2),encoding='utf-8')
    p,s=run(c);rows.append(dict(path=p,completed=s['completed']))
    out.write_text(json.dumps(rows,indent=2),encoding='utf-8')
