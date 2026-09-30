"""Independent x/y controls after the coupled finest grid proved unreliable.

This is an explicitly recorded follow-up, not replacement of failed trials.
"""
from parametric_perturb import simulate,compare
from parametric_study import PARAMS,save


def main():
    groups=[]
    for pars in (PARAMS[0],PARAMS[1],PARAMS[-1]):
        for mode in ('low','high','vonly'):
            for eps in (.001,.0001):
                # Same h for x comparison; same x grid for y comparison.
                specs=[('fd','original',.03125,256,.000125),
                       ('fd','original',.03125,384,.000125),
                       ('fd','original',.03125,512,.000125),
                       ('fd','original',.015625,512,.000125),
                       ('fd','original',.015625,512,.0000625),
                       ('structure','compatible',.015625,512,.0000625)]
                refs=[simulate(pars,mo,cl,True,h,n,mode,eps,dt=dt) for mo,cl,h,n,dt in specs]
                controls={'x_256_384':compare(refs[0],refs[1]),'x_384_512':compare(refs[1],refs[2]),
                          'y_003125_0015625':compare(refs[2],refs[3]),
                          'dt_halving':compare(refs[3],refs[4]),'model_agreement':compare(refs[5],refs[4])}
                groups.append({'pars':refs[0]['config']['pars'],'mode':mode,'eps':eps,'references':refs,'controls':controls})
                save('parametric_reference_controls',groups);print('independent references',len(groups),'/18',flush=True)

if __name__=='__main__':main()
