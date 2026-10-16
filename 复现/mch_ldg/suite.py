import argparse,json
from pathlib import Path
from datetime import datetime
import numpy as np
from mch.experiment import run


def configs(mode):
    base=dict(left=-20.,right=20.,kappa=0.,alpha=.5,k=3,n=80,T=.5,dt=.001,projection='radau',outputs=11)
    if mode=='smoke':
        for flux in ('conservative','dissipative'):
            yield dict(base,case='5.4',flux=flux,n=80,T=.1,dt=.001)
    elif mode=='smooth':
        for k in (1,2,3):
            for n in (40,80,160):
                for flux in ('conservative','dissipative'):
                    yield dict(base,case='5.1',flux=flux,k=k,n=n,dt=.02*(40/n)/(2*k+1))
    elif mode=='peakon':
        for flux in ('conservative','dissipative'):
            yield dict(base,case='5.4',flux=flux,n=640,T=5.,dt=.0005,outputs=21,snapshots=[0,2,5])
    elif mode=='other':
        for case,n,kap,T in [('5.2',160,1.,5.),('5.3',1000,1.,5.),('5.5',1280,0.,5.)]:
            for flux in ('conservative','dissipative'):
                left,right=(-100.,100.) if case=='5.3' else ((-3*np.pi,3*np.pi) if case=='5.5' else (-20.,20.))
                yield dict(base,case=case,flux=flux,n=n,kappa=kap,T=T,left=left,right=right,dt=.0005,outputs=11)
    elif mode=='timecheck':
        for flux in ('conservative','dissipative'):
            yield dict(base,case='5.4',flux=flux,n=640,T=5.,dt=.00025,outputs=21)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['smoke','smooth','peakon','other','timecheck'],default='smoke');args=ap.parse_args()
    cp=Path('configs');cp.mkdir(exist_ok=True)
    records=[];index=Path('results')/('suite_'+args.mode+'_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.json')
    for j,c in enumerate(configs(args.mode)):
        (cp/f'{args.mode}_{j:02}.json').write_text(json.dumps(c,indent=2),encoding='utf-8')
        path,summary=run(c);records.append(dict(path=path,completed=summary['completed']))
        index.write_text(json.dumps(records,indent=2),encoding='utf-8')
