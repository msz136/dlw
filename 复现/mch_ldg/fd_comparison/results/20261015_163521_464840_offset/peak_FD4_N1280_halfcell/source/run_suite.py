"""FD benchmark runner and paired LDG jobs; append-only output directories."""
import sys,json,time,hashlib,argparse
from pathlib import Path
from datetime import datetime
import numpy as np
from scipy.interpolate import CubicSpline
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from mch.exact import profile
from mch.experiment import run as run_ldg
from fd import DirectFD
from fd_rusanov import RusanovFD

HERE=Path(__file__).resolve().parent
def run_fd(config,folder):
    cfg=dict(config);out=folder/cfg['id'];out.mkdir(parents=True,exist_ok=False)
    cls=RusanovFD if cfg.get('variant')=='rusanov' else DirectFD
    start=time.perf_counter();d=cls(**{k:cfg[k] for k in ('n','left','right','kappa','order','offset')})
    exact=lambda x,t:profile(cfg['case'],x,t,alpha=cfg.get('alpha',.5),kappa=cfg['kappa'])[0]
    u=exact(d.x,0);t=0.;steps=0;failure=None;history=[];states=[];times=[]
    e0=d.energy(u);m0=d.mass(u)
    def save():
        err=u-exact(d.x,t)
        row=dict(t=t,energy=d.energy(u),energy_loss=e0-d.energy(u),energy_rate=d.energy_rate(u),mass_drift=d.mass(u)-m0,
                 native_l2=float(np.sqrt(d.h*np.sum(err*err))),native_linf=float(np.max(abs(err))))
        states.append(u.copy());times.append(t);history.append(row)
    source={p.name:p.read_bytes() for p in [Path(__file__),HERE/'fd.py',HERE/'fd_rusanov.py',ROOT/'mch/exact.py']}
    (out/'source').mkdir()
    for name,content in source.items():(out/'source'/name).write_bytes(content)
    (out/'config.json').write_text(json.dumps(cfg,indent=2),encoding='utf-8')
    targets=np.linspace(0,cfg['T'],21)
    with np.errstate(over='raise',invalid='raise',divide='raise'):
        save()
        try:
            for target in targets[1:]:
                while t<target-1e-13:
                    h=min(cfg['dt'],target-t)
                    k1=d.rhs(u);k2=d.rhs(u+h*k1/2);k3=d.rhs(u+h*k2/2);k4=d.rhs(u+h*k3)
                    candidate=u+h/6*(k1+2*k2+2*k3+k4)
                    if not np.all(np.isfinite(candidate)):raise FloatingPointError('Nonfinite candidate')
                    u=candidate;t+=h;steps+=1
                save()
        except FloatingPointError as exc:failure=str(exc)
    np.savez_compressed(out/'trajectory.npz',t=times,u=states,x=d.x,last_state=u,last_time=t)
    (out/'history.json').write_text(json.dumps(history,indent=2),encoding='utf-8')
    summary=dict(config=cfg,completed=failure is None,failure=failure,reached=t,last_diagnostic_time=times[-1],steps=steps,
                 evolution_and_diagnostic_seconds=time.perf_counter()-start,initial=history[0],final=history[-1],
                 source_hashes={p:hashlib.sha256(b).hexdigest() for p,b in source.items()})
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(dict(id=cfg['id'],completed=summary['completed'],reached=t,native_error=history[-1]['native_l2'],seconds=summary['evolution_and_diagnostic_seconds'])),flush=True)
    return dict(kind='FD',path=str(out),id=cfg['id'])

def configs(mode):
    base=dict(case='5.4',left=-20.,right=20.,kappa=0.,T=5.,dt=.00025,offset=0.,alpha=.5)
    if mode=='peak':
        for order in (2,4):
            for n in (320,640,1280,2560):
                yield dict(base,order=order,n=n,id=f'peak_FD{order}_N{n}')
    elif mode=='smooth':
        for order in (2,4):
            for n in (80,160,320,640,1280):
                yield dict(base,case='5.1',left=-40.,right=40.,T=.5,dt=.0005,order=order,n=n,id=f'smooth_FD{order}_N{n}')
    elif mode=='controls':
        for order in (2,4):
            yield dict(base,order=order,n=2560,dt=.000125,id=f'peak_FD{order}_N2560_halfdt')
            yield dict(base,order=order,n=2560,offset=.5,id=f'peak_FD{order}_N2560_halfcell')
    elif mode=='smoke':
        for order in (2,4):yield dict(base,order=order,n=160,T=.05,id=f'smoke_FD{order}_N160')
    elif mode=='rusanov':
        for n in (320,640,1280,2560):yield dict(base,variant='rusanov',order=2,n=n,id=f'peak_Rusanov_N{n}')
        for n in (80,160,320,640,1280):yield dict(base,variant='rusanov',case='5.1',left=-40.,right=40.,T=.5,dt=.0005,order=2,n=n,id=f'smooth_Rusanov_N{n}')
    elif mode=='offset':
        for order in (2,4):
            for n in (320,640,1280):yield dict(base,order=order,n=n,offset=.5,id=f'peak_FD{order}_N{n}_halfcell')
            yield dict(base,order=order,n=2560,offset=.5,dt=.000125,id=f'peak_FD{order}_N2560_halfcell_halfdt')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['peak','smooth','controls','ldg','smoke','rusanov','offset'],default='smoke');args=ap.parse_args()
    folder=HERE/'results'/f'{datetime.now():%Y%m%d_%H%M%S_%f}_{args.mode}';folder.mkdir(parents=True)
    manifest=[]
    if args.mode=='ldg':
        jobs=[]
        for flux in ('conservative','dissipative'):
            for n in (160,320):jobs.append(dict(case='5.4',left=-20.,right=20.,T=5.,dt=.00025,n=n,k=3,kappa=0.,alpha=.5,flux=flux,outputs=21,projection='radau'))
            for n in (80,160,320):jobs.append(dict(case='5.1',left=-40.,right=40.,T=.5,dt=.0005,n=n,k=3,kappa=0.,alpha=.5,flux=flux,outputs=21,projection='radau'))
        (folder/'planned_configs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
        for c in jobs:
            p,s=run_ldg(c,folder);manifest.append(dict(kind='LDG',path=p,id=Path(p).name))
            (folder/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    else:
        jobs=list(configs(args.mode));(folder/'planned_configs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
        for c in jobs:
            manifest.append(run_fd(c,folder));(folder/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
