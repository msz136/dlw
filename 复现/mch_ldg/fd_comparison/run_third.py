"""Fixed FD3 protocol, using the existing RK4 and output machinery."""
import argparse,json
from datetime import datetime
from run_suite import run_fd,HERE

ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['smooth','peak','controls'],default='smooth');args=ap.parse_args()
base=dict(case='5.4',left=-20.,right=20.,kappa=0.,T=5.,dt=.00025,offset=0.,alpha=.5,order=3,variant='lf3')
if args.mode=='smooth':
    jobs=[dict(base,case='5.1',left=-40.,right=40.,T=.5,dt=.0005,n=n,id=f'smooth_FD3_N{n}') for n in [80,160,320,640,1280]]
elif args.mode=='peak':
    jobs=[dict(base,n=n,offset=offset,id=f'peak_FD3_N{n}'+('_halfcell' if offset else '')) for offset in [0.,.5] for n in [320,640,1280,2560]]
else:
    jobs=[dict(base,n=2560,offset=offset,dt=.000125,id='peak_FD3_N2560_halfdt'+('_halfcell' if offset else '')) for offset in [0.,.5]]
    jobs.append(dict(base,case='5.1',left=-40.,right=40.,T=.5,dt=.00025,n=1280,id='smooth_FD3_N1280_halfdt'))
folder=HERE/'results'/f'{datetime.now():%Y%m%d_%H%M%S_%f}_third_{args.mode}';folder.mkdir(parents=True)
(folder/'planned_configs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
rows=[]
for c in jobs:
    rows.append(run_fd(c,folder));(folder/'manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
