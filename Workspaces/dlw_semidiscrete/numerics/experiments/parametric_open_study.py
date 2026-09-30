"""Controlled quadratic-ghost boundary experiment for BOTH models."""
from parametric_perturb import simulate,compare
from parametric_study import PARAMS,save,inf
from parametric_open import OpenModel
import numpy as np

def verify():
    rng=np.random.default_rng(12)
    for model in ('structure','fd'):
        m=OpenModel(nx=32,model=model,continuous=True)
        z=m.exact(.01);e=rng.normal(size=z.size)*.001
        assert inf(m.delta(.01,z,e)-(m.rhs(.01,z+e)-m.rhs(.01,z)))<1e-12
        assert inf(m.delta(.01,z,e,True)-(m.rhs(.01,z+e)-m.rhs(.01,z-e))/2)<1e-12
        if model=='structure':
            P,Q=m.unpack(e);u,v=m.error_fields(e)
            assert inf(v[-1]-Q[-1]-(1.5*P[-1]-.5*P[-2]))<1e-13
        assert inf(m.delta(.01,z,np.zeros_like(z)))==0
    save('parametric_open_verification',{'rhs_difference':True,'jacobian':True,'right_reconstruction_norm_2':True,'zero_perturbation':True})

def main():
    verify();groups=[]
    specs=[(p,mode,.001) for p in (PARAMS[0],PARAMS[1],PARAMS[-1]) for mode in ('low','high','vonly')]
    specs += [(PARAMS[0],mode,.0001) for mode in ('low','high')]
    for pars,mode,eps in specs:
        def run(model,h,n,balanced=True,dt=.000125):
            return simulate(pars,model,'extrapolated',balanced,h,n,mode,eps,dt=dt,model_factory=OpenModel)
        # Coarse variants; ref resolution controls keep x and y separate.
        rows=[run(m,.125,256,b) for m in ('structure','fd') for b in (False,True)]
        refs=[run('fd',.03125,384),run('fd',.03125,512),run('fd',.015625,512,dt=.0000625),
              run('structure',.015625,512,dt=.0000625)]
        controls={'x':compare(refs[0],refs[1]),'y_and_dt':compare(refs[1],refs[2]),'model':compare(refs[3],refs[2])}
        for r in rows:r['comparison']=compare(r,refs[2])
        groups.append({'pars':rows[0]['config']['pars'],'mode':mode,'eps':eps,'variants':rows,'references':refs,'controls':controls})
        save('parametric_open',groups);print('open-boundary groups',len(groups),'/11',flush=True)

if __name__=='__main__':main()
