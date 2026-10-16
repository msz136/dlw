"""Test a preregistered follow-up source-cancellation prediction in actual C flow."""
from pathlib import Path
import argparse
import csv
import importlib.util
import json
import time
import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('mechanism_intervention', HERE/'homotopy.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
NS = base.NS
OUT = HERE / 'refinement'
OUT.mkdir(exist_ok=True)


def run(kind, half=False):
    cfg = NS['case_config']('C')
    cfg.update(nx=3200, T=.001, dt=.0000125 if half else .000025)
    tag = f'C_{kind}_dx0025' + ('_halfdt' if half else '')
    dest = OUT/(tag+'.json')
    if dest.exists():
        print('EXISTS',tag,flush=True)
        return
    obj = NS['SDModel' if kind=='SD' else 'FDModel']('C',kind,cfg)
    state = obj.initial()
    iy = np.flatnonzero(abs(obj.y)<cfg['eval_yhalf'])
    ix = np.flatnonzero(abs(obj.X.x)<=cfg['eval_half']+1e-10)
    nsteps = round(cfg['T']/cfg['dt'])
    start = time.perf_counter()
    print('START',tag,nsteps,flush=True)
    for n in range(nsteps):
        with np.errstate(over='raise',invalid='raise',divide='raise'):
            state = NS['step'](obj.rhs,n*cfg['dt'],state,cfg['dt'],'RK4')
        assert np.isfinite(state).all() and np.max(abs(state))<1000
    uv = obj.fields(state,cfg['T'])
    exact = obj.G.uv(obj.js[iy],obj.X.x[ix],cfg['T'])
    errors = [v[np.ix_(iy,ix)]-e for v,e in zip(uv,exact)]
    result = dict(case='C',model=kind,config=cfg,dx=obj.X.dx,seconds=time.perf_counter()-start,
                  u_rms=float(np.sqrt(np.mean(errors[0]**2))),
                  v_rms=float(np.sqrt(np.mean(errors[1]**2))),
                  u_linf=float(np.max(abs(errors[0]))),v_linf=float(np.max(abs(errors[1]))))
    np.savez_compressed(OUT/(tag+'.npz'),x=obj.X.x[ix],y=obj.y[iy],error_u=errors[0],error_v=errors[1])
    dest.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('DONE',tag,result,flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--kind',choices=['SD','FD'],required=True)
    parser.add_argument('--halfdt',action='store_true')
    args=parser.parse_args()
    run(args.kind,args.halfdt)
