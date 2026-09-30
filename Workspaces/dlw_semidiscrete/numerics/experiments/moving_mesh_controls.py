"""Resolution, time-step, mode and long-time geometry controls."""
from pathlib import Path
import sys,json,hashlib,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
sys.path.insert(0,str(ROOT/'experiments'))
import numpy as np
from moving_mesh import MovingProblem,gram_mesh
from moving_mesh_study import OUT,ALL,compare,inf
from parametric_perturb import seed


def run_mode(pid,pars,model,mesh,mode,nx,dt,T=.01):
    p=MovingProblem(pars,h=.125,nx=nx,model=model)
    start=time.perf_counter()
    rows,status=p.evolve(T,dt,mesh_mode=mesh,balanced=True,
                         perturb=lambda m:seed(m,mode,.001),observations=(T/2,T))
    ident=f'ctrl_{pid}_{model}_{mesh}_{mode}_{nx}_{str(dt).replace(".","p")}'
    arrays={}
    for k,r in enumerate(rows):
        arrays[f'x{k}']=r['x'];arrays[f'u{k}']=r['u_response'];arrays[f'v{k}']=r['v_response']
    np.savez_compressed(OUT/(ident+'.npz'),**arrays)
    return {'parameter_id':pid,'model':model,'mesh':mesh,'mode':mode,
            'nx':nx,'dt':dt,'T':T,'file':ident+'.npz',**status,
            'seconds':time.perf_counter()-start,
            'observations':[{'t':r['t'],'min_dx':r['min_dx'],'min_J':r['min_J'],
                             'u_inf':inf(r['u_response']),'v_inf':inf(r['v_response'])}
                            for r in rows]}


def long_geometry(pid,pars,nx,T=2.,dt=.005):
    p=MovingProblem(pars,h=.125,nx=nx,model='structure')
    rows,status=p.evolve(T,dt,mesh_mode='moving',balanced=True,observations=(T,))
    return {'parameter_id':pid,'nx':nx,'T':T,'dt':dt,**status,
            'max_node_error':inf(p.X.x-gram_mesh(pars,.125,p.m.js,p.X.xi,T)),
            'min_dx':float(np.min(p.X.spacing())),
            'min_J':float(np.min(p.X.J))}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    result={'high_vonly':[],'x_dt_controls':[],'long_geometry':[]}
    for index in (0,1,9):
        pars=ALL[index];pid=f'P{index+1}'
        for model in ('structure','fd'):
            for mode in ('high','vonly'):
                ref=run_mode(pid,pars,model,'uniform',mode,384,.0000625)
                variants=[]
                for mesh in ('uniform','static_adaptive','moving'):
                    row=run_mode(pid,pars,model,mesh,mode,128,.000125)
                    row['own_model_fine_x_comparison']=compare(row,ref)
                    variants.append(row)
                result['high_vonly'].append({'parameter_id':pid,'model':model,
                                              'mode':mode,'reference':ref,
                                              'variants':variants})
        result['long_geometry'].append(long_geometry(pid,pars,128))
        print('modes and long geometry',pid,flush=True)
    # Controls check whether the nominal fine x reference is resolved, and
    # separate a time-step effect from x refinement at representative cases.
    for index in (0,1,9,15):
        pars=ALL[index];pid=f'P{index+1}'
        for model in ('structure','fd'):
            mid=run_mode(pid,pars,model,'uniform','low',256,.000125)
            fine=run_mode(pid,pars,model,'uniform','low',384,.0000625)
            finest=run_mode(pid,pars,model,'uniform','low',512,.0000625)
            half=run_mode(pid,pars,model,'uniform','low',384,.00003125)
            result['x_dt_controls'].append({'parameter_id':pid,'model':model,
                  'mid_vs_fine':compare(mid,fine),'fine_vs_finest':compare(fine,finest),
                  'time_step':compare(fine,half),'runs':[mid,fine,finest,half]})
        print('x/dt controls',pid,flush=True)
    paths=[Path(__file__),ROOT/'lib/moving_mesh.py',ROOT/'lib/parametric_open.py']
    result['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in paths}
    (OUT/'controls.json').write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')


if __name__=='__main__':main()
