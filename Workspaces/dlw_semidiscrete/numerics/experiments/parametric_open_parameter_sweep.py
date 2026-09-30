"""Extend the shared-boundary perturbation comparison to P3--P9.

Low physical frequency and epsilon=.001 are held fixed to isolate background
parameter variation; the P1/P2/P10 multi-mode experiments remain separate.
"""
from parametric_perturb import simulate,compare
from parametric_study import PARAMS,save
from parametric_open import OpenModel


def main():
    groups=[]
    for index in range(2,9):
        pars=PARAMS[index];mode='low';eps=.001
        def run(model,h,n,balanced=True,dt=.000125):
            return simulate(pars,model,'extrapolated',balanced,h,n,mode,eps,dt=dt,model_factory=OpenModel)
        variants=[run(m,.125,256,b) for m in ('structure','fd') for b in (False,True)]
        references=[run('fd',.03125,384),run('fd',.03125,512),
                    run('fd',.015625,512,dt=.000125),
                    run('fd',.015625,512,dt=.0000625),
                    run('structure',.015625,512,dt=.0000625)]
        controls={'x':compare(references[0],references[1]),
                  'y':compare(references[1],references[2]),
                  'dt':compare(references[2],references[3]),
                  'model':compare(references[4],references[3])}
        for row in variants:row['comparison']=compare(row,references[3])
        groups.append({'parameter_id':f'P{index+1}','pars':variants[0]['config']['pars'],
                       'mode':mode,'eps':eps,'variants':variants,
                       'references':references,'controls':controls})
        save('parametric_open_parameter_sweep',groups)
        print('parameter sweep',len(groups),'/7',flush=True)

if __name__=='__main__':main()
