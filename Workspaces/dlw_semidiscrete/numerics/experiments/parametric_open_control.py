"""Separate y refinement from time-step refinement for the new closure."""
from parametric_perturb import simulate,compare
from parametric_study import save
from parametric_assess import read
from parametric import Parameters
from parametric_open import OpenModel

def main():
    out=[]
    for g in read('parametric_open'):
        r=simulate(Parameters(**g['pars']),'fd','extrapolated',True,.015625,512,g['mode'],g['eps'],model_factory=OpenModel)
        out.append({'pars':g['pars'],'mode':g['mode'],'eps':g['eps'],'run':r,
                    'y':compare(g['references'][1],r),'dt':compare(r,g['references'][2])})
        save('parametric_open_controls',out);print('open time/y controls',len(out),'/11',flush=True)

if __name__=='__main__':main()
