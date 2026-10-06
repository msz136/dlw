"""Independent T=.01 probes of the frozen original code; not new density runs."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import importlib.util
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

HERE=Path(__file__).resolve().parent
ORIGINAL=HERE.parent/'experiment.py'
sp=importlib.util.spec_from_file_location('original_mesh_experiment', ORIGINAL)
e=importlib.util.module_from_spec(sp)
sys.modules[sp.name]=e
sp.loader.exec_module(e)
e.TIMES=(0., .001, .002, .005, .01)
e.OUT=HERE/'out'

def one(s):
    return e.one(s)

if __name__=='__main__':
    specs=[]
    for model in ('SD','FD'):
        for nx in (33,65):
            for dt in (5e-6,2.5e-6):
                specs.append(dict(case='A',model=model,mesh='fixed',motion='fixed',
                    nx=nx,h=.125,dt=dt,T=.01,variant=f'nx{nx}_dt{dt:g}'))
    with ProcessPoolExecutor(max_workers=2) as pool:
        fs=[pool.submit(one,s) for s in specs]
        for f in as_completed(fs):
            r=f.result()
            print(e.spec_key(r['spec']),r['status'],r['reached'],r['history'][-1]['errors'],flush=True)
