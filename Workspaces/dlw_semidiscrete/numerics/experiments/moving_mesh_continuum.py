"""Common continuous-DLW exact-field benchmark for both moving x models."""
from pathlib import Path
import sys,json,hashlib,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
sys.path.insert(0,str(ROOT/'experiments'))
from moving_mesh import MovingProblem
from moving_mesh_study import ALL,OUT,inf
import numpy as np


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    rows=[]
    for index,pars in enumerate(ALL):
        pid=f'P{index+1}'
        for model in ('structure','fd'):
            for mesh in ('uniform','static_adaptive','moving'):
                p=MovingProblem(pars,h=.125,nx=128,model=model,continuous=True)
                start=time.perf_counter()
                hist,status=p.evolve(.01,.000125,mesh_mode=mesh,balanced=False,
                                     observations=(.005,.01))
                tag=f'continuous_{pid}_{model}_{mesh}.npz'
                arrays={}
                for k,r in enumerate(hist):
                    arrays[f'x{k}']=r['x']
                    arrays[f'u{k}']=r['u_response']
                    arrays[f'v{k}']=r['v_response']
                np.savez_compressed(OUT/tag,**arrays)
                rows.append({'parameter_id':pid,'model':model,'mesh':mesh,
                             'pars':pars.__dict__,'seconds':time.perf_counter()-start,
                             'file':tag,
                             **status,'observations':[{'t':r['t'],
                                'u_inf':inf(r['u_response']),'v_inf':inf(r['v_response']),
                                'u_interior':inf(r['u_response'][abs(p.m.y)<=.75]),
                                'v_interior':inf(r['v_response'][abs(p.m.y)<=.75]),
                                'v_boundary':inf(r['v_response'][[0,-1]]),
                                'min_J':r['min_J'],'min_dx':r['min_dx']}
                                for r in hist]})
        data={'scope':{'target':'common exact continuous DLW field',
                       'parameter_count':16,'h':.125,'nx':128,'T':.01,
                       'dt':.000125,'x_length':20.,
                       'boundary':'common background-relative quadratic y extrapolation',
                       'mesh_initialization':'finite-h Gram density for both models'},
              'runs':rows}
        paths=[Path(__file__),ROOT/'lib/moving_mesh.py']
        data['source_sha256']={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest()
                               for f in paths}
        (OUT/'continuum.json').write_text(json.dumps(data,indent=2,allow_nan=False),encoding='utf-8')
        print(pid,'common-continuous runs',flush=True)


if __name__=='__main__':main()
