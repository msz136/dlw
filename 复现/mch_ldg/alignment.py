"""Post-baseline checks; these parameter choices are not attributed to authors."""
import argparse,json
from pathlib import Path
from datetime import datetime
from mch.experiment import run

ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['boundary','periodic_time','initialization'],default='boundary');args=ap.parse_args()
base=dict(case='5.4',left=-20.,right=20.,kappa=0.,alpha=.5,k=3,n=640,T=5.,dt=.0005,projection='radau',outputs=11,flux='conservative')
configs=[]
if args.mode=='boundary':
    for flux in ('conservative','dissipative'):
        configs.append(dict(base,boundary='dirichlet',boundary_value=0.,flux=flux))
    for k in (1,2,3):
        for n in (40,80,160):
            configs.append(dict(base,case='5.1',T=.5,n=n,k=k,dt=.001,boundary='dirichlet',boundary_value=1.,outputs=3))
elif args.mode=='periodic_time':
    import numpy as np
    configs=[dict(base,case='5.5',n=1280,left=-3*np.pi,right=3*np.pi,dt=.000125)]
else:
    configs=[dict(base,projection='l2',flux=f) for f in ('conservative','dissipative')]
out=Path('results')/f"alignment_{args.mode}_{datetime.now():%Y%m%d_%H%M%S}.json";rows=[]
for i,c in enumerate(configs):
    Path(f'configs/alignment_{args.mode}_{i:02}.json').write_text(json.dumps(c,indent=2),encoding='utf-8')
    p,s=run(c);rows.append(dict(path=p,completed=s['completed']))
    out.write_text(json.dumps(rows,indent=2),encoding='utf-8')
