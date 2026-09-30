"""Fine-scale perturbation: compare mesh modes to each model's own x reference."""
from pathlib import Path
import sys,json,hashlib

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'lib'),str(ROOT/'experiments')]
import numpy as np
from moving_mesh import MovingProblem
from moving_mesh_study import ALL
from moving_mesh_route1_coupled import remesh,periodic_interpolate,norm
from parametric_perturb import seed


def response_run(pars,model,mesh,T,nx,dt):
    p=MovingProblem(pars,h=.125,nx=nx,model=model)
    e,s=p.initial('uniform' if mesh=='uniform' else 'static_adaptive',
                  balanced=True,perturb=lambda m:seed(m,'high',.001))
    n=round(T/dt)
    status='complete';stop=T
    for i in range(n):
        t=i*dt
        try:
            if mesh=='moving':
                z=np.r_[e,s];ne=e.size
                def fun(tt,zz):
                    de,ds=p.rhs(tt,(zz[:ne],zz[ne:]),balanced=True,
                                mesh_mode='moving')
                    return np.r_[de,ds]
                k1=fun(t,z);k2=fun(t+dt/2,z+dt*k1/2)
                k3=fun(t+dt/2,z+dt*k2/2);k4=fun(t+dt,z+dt*k3)
                z=z+dt*(k1+2*k2+2*k3+k4)/6
                e,s=z[:ne],z[ne:]
                p.set_s(s)
            else:
                def fun(tt,ee):return p.m.delta(tt,p.m.exact(tt),ee)
                k1=fun(t,e);k2=fun(t+dt/2,e+dt*k1/2)
                k3=fun(t+dt/2,e+dt*k2/2);k4=fun(t+dt,e+dt*k3)
                e=e+dt*(k1+2*k2+2*k3+k4)/6
                if mesh=='intermittent' and (i+1)%round(.005/dt)==0:
                    old_x=p.X.x.copy()
                    z=p.m.exact((i+1)*dt)+e
                    remesh(p,z,(i+1)*dt)
                    e=p.m.pack(*[periodic_interpolate(old_x,f,p.X.x,20)
                                 for f in p.m.unpack(e)])
            if not np.all(np.isfinite(e)) or norm(e)>1e3:
                raise ValueError('response diverged')
        except ValueError as exc:
            status=str(exc);stop=t;break
    eu,ev=p.m.error_fields(e)
    target=np.linspace(-8,8,801)
    return {'status':status,'stop_t':stop,'x':p.X.x.copy(),
            'u':eu,'v':ev,'common_u':periodic_interpolate(p.X.x,eu,target,20),
            'common_v':periodic_interpolate(p.X.x,ev,target,20),
            'min_dx':float(min(p.X.spacing())),'min_J':float(min(p.X.J))}


def difference(a,b):
    if a['status']!='complete' or b['status']!='complete':return None
    return {k:{'absolute':norm(a['common_'+k]-b['common_'+k]),
               'reference_peak':norm(b['common_'+k]),
               'relative':norm(a['common_'+k]-b['common_'+k])/
                          max(norm(b['common_'+k]),1e-30)} for k in ('u','v')}


def main():
    result={'scope':{'cases':['P1','P7'],'models':['structure','fd'],
                     'T':[.01,.02],'h':.125,'coarse_nx':128,
                     'reference_nx':[384,512],
                     'mode':'high spatial frequency, amplitude .001',
                     'equations':'exact-background-balanced perturbation',
                     'common_x':[-8,8,801]},'rows':[]}
    for index in (0,6):
        for model in ('structure','fd'):
            for T in (.01,.02):
                ref=response_run(ALL[index],model,'uniform',T,384,.0000625)
                finer=response_run(ALL[index],model,'uniform',T,512,.0000625)
                variants={}
                for mesh in ('uniform','static_adaptive','moving','intermittent'):
                    a=response_run(ALL[index],model,mesh,T,128,.000125)
                    variants[mesh]={'status':a['status'],'stop_t':a['stop_t'],
                                    'min_dx':a['min_dx'],'min_J':a['min_J'],
                                    'vs_ref':difference(a,ref)}
                result['rows'].append({'parameter_id':f'P{index+1}',
                    'model':model,'T':T,'reference_status':ref['status'],
                    'finer_status':finer['status'],
                    'reference_check':difference(ref,finer),'variants':variants})
                print(f'P{index+1} {model} T={T}: {ref["status"]}, '
                      f'{finer["status"]}',flush=True)
    paths=[Path(__file__),ROOT/'experiments/moving_mesh_route1_coupled.py',
           ROOT/'lib/moving_mesh.py']
    result['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in paths}
    (ROOT/'out'/'moving_mesh'/'route1_perturb.json').write_text(
        json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')


if __name__=='__main__':main()
