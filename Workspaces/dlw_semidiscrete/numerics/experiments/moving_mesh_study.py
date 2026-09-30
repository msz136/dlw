"""Coupled common-x mesh comparisons on regular one-soliton backgrounds.

All models use the SAME background-relative quadratic right y ghost.  The
unbalanced Gram experiment measures solver error against an exact finite-h
field.  The perturbed experiment uses balanced equations and compares each
model with its OWN finer x reference at the same h; it is not a truth claim
about arbitrary perturbed continuous DLW solutions.
"""
from pathlib import Path
import sys, json, hashlib, argparse, time
from dataclasses import asdict

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
sys.path.insert(0,str(ROOT/'experiments'))
import numpy as np
from scipy.interpolate import CubicSpline
from moving_mesh import MovingProblem, gram_mesh, gram_phi
from parametric import Parameters
from parametric_study import PARAMS
from parametric_perturb import seed

OUT=ROOT/'out'/'moving_mesh'
EXTRA=[
    Parameters(a=4,p=.75,q=1.5,rho=2),
    Parameters(a=4,p=1.5,q=2.5,rho=4),
    Parameters(a=3.5,p=1,q=2,rho=3),
    Parameters(a=5,p=1.5,q=2,rho=3),
    Parameters(a=4,p=.75,q=3,rho=2),
    Parameters(a=2.5,p=1,q=1.5,rho=1),
]
ALL=PARAMS+EXTRA


def inf(a):return float(np.max(np.abs(a)))


def run(pid, pars, model, mesh, balanced, nx, dt, T, perturb=False):
    p=MovingProblem(pars,h=.125,nx=nx,model=model,continuous=False)
    pulse=(lambda m:seed(m,'low',.001)) if perturb else None
    start=time.perf_counter()
    rows,status=p.evolve(T,dt,mesh_mode=mesh,balanced=balanced,
                         perturb=pulse,observations=(T/2,T))
    elapsed=time.perf_counter()-start
    tag=f'{pid}_{model}_{mesh}_{"pert" if perturb else "gram"}_{nx}_{str(dt).replace(".","p")}'
    data={}
    for k,r in enumerate(rows):
        data[f'x{k}']=r['x'];data[f'u{k}']=r['u_response'];data[f'v{k}']=r['v_response']
    np.savez_compressed(OUT/(tag+'.npz'),**data)
    info={'parameter_id':pid,'pars':asdict(pars),'model':model,'mesh':mesh,
          'balanced':balanced,'perturbation':'low_0.001' if perturb else None,
          'h':.125,'nx':nx,'dt':dt,'T':T,'seconds':elapsed,'file':tag+'.npz',
          **status,'observations':[]}
    for r in rows:
        info['observations'].append({'t':r['t'],'u_inf':inf(r['u_response']),
                                     'v_inf':inf(r['v_response']),
                                     'min_J':r['min_J'],'min_dx':r['min_dx'],
                                     'max_R':r['max_R'],'min_R':r['min_R']})
    return info


def compare(row,ref):
    if not row['complete'] or not ref['complete']:
        return []
    a=np.load(OUT/row['file']);b=np.load(OUT/ref['file']);L=20.
    result=[]
    for k,ob in enumerate(row['observations']):
        xr=b[f'x{k}'];x=a[f'x{k}']
        out={'t':ob['t']}
        for field in ('u','v'):
            vf=b[f'{field}{k}']
            spline=CubicSpline(np.r_[xr,xr[0]+L],
                               np.concatenate((vf,vf[:,:1]),axis=1),
                               axis=1,bc_type='periodic')
            target=spline(x)
            difference=a[f'{field}{k}']-target
            out[field]={'absolute_difference':inf(difference),
                        'relative_response_difference':inf(difference)/max(inf(target),1e-30),
                        'reference_peak':inf(target),
                        'interior_difference':inf(difference[np.abs(np.arange(vf.shape[0])
                            -vf.shape[0]/2)<vf.shape[0]/4]),
                        'boundary_difference':inf(difference[[0,-1]])}
        result.append(out)
    return result


def geometry(pid,pars,nx,dt,T):
    p=MovingProblem(pars,h=.125,nx=nx,model='structure')
    rows,status=p.evolve(T,dt,mesh_mode='moving',balanced=True)
    exact=gram_mesh(pars,.125,p.m.js,p.X.xi,T)
    # Exact weighted cell masses from the Gram coordinate potential.
    x=p.X.x
    phi=p.weights @ gram_phi(pars,.125,p.m.js,np.r_[x,x[0]+p.X.L],T)
    cell=np.diff(np.r_[x,x[0]+p.X.L]-phi)
    return {'parameter_id':pid,'nx':nx,'dt':dt,'T':T,**status,
            'max_node_error':inf(x-exact),
            'cell_mass_spread':float(np.max(cell)-np.min(cell)),
            'min_spacing':float(np.min(p.X.spacing())),
            'min_J':float(np.min(p.X.J))}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--quick',action='store_true')
    args=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    params=ALL[:3] if args.quick else ALL
    T=.005 if args.quick else .01
    dt=.000125
    data={'scope':{'parameter_count':len(params),'existing_count':min(10,len(params)),
                   'new_count':max(0,len(params)-10),'h':.125,'T':T,
                   'coarse_nx':128,'reference_nx':384,'periodic_x_L':20,
                   'boundary':'background-relative quadratic y extrapolation',
                   'reference_kind':'within-model x-refinement, not certified truth'},
          'geometry':[],'gram':[],'perturbation':[],'references':[]}
    for i,pars in enumerate(params):
        pid=f'P{i+1}'
        data['geometry'].append(geometry(pid,pars,128,dt,T))
        for model in ('structure','fd'):
            for mesh in ('uniform','static_adaptive','moving'):
                row=run(pid,pars,model,mesh,False,128,dt,T)
                data['gram'].append(row)
            ref=run(pid,pars,model,'uniform',True,384,dt/2,T,perturb=True)
            data['references'].append(ref)
            for mesh in ('uniform','static_adaptive','moving'):
                row=run(pid,pars,model,mesh,True,128,dt,T,perturb=True)
                row['own_model_fine_x_comparison']=compare(row,ref)
                data['perturbation'].append(row)
        sources=[Path(__file__),ROOT/'lib/moving_mesh.py',ROOT/'lib/parametric.py',
                 ROOT/'lib/parametric_open.py']
        data['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sources}
        (OUT/'study.json').write_text(json.dumps(data,indent=2,allow_nan=False),encoding='utf-8')
        print(f'{pid}: geometry + 2 models x 3 meshes, exact and perturbation',flush=True)


if __name__=='__main__':main()
