"""Sequential repeated cost comparison, excluding diagnostics and setup."""
from dynamics_study import Problem, integrate, norm, write
import time
import numpy as np


def main():
    rows=[]
    for case in ('A','B'):
        for h in (.25,.125):
            for nx in (128,256):
                pair={model:[] for model in ('structure','fd')}
                errors={}
                for repeat in range(3):
                    # Alternate order so one method is not always first.
                    for model in (('structure','fd') if repeat%2==0 else ('fd','structure')):
                        p=Problem(case,h,nx,model=model,continuous_data=True)
                        P,Q=p.initial()
                        p.rhs(0,P,Q) # warm up, outside timing / call count
                        p.calls=0
                        start=time.perf_counter()
                        P,Q,info=integrate(p.rhs,0,.005,P,Q,.00025)
                        pair[model].append(time.perf_counter()-start)
                        assert info['stopped'] is None and p.calls==80
                        errors[model]={k:norm(a-b,p.X.dx,h) for k,a,b in
                                       zip(('u','v'),p.fields(P,Q,.005),p.G.uv(p.js,p.X.x,.005))}
                for model in pair:
                    rows.append(dict(case=case,h=h,nx=nx,model=model,T=.005,dt=.00025,
                                     seconds=pair[model],median_seconds=float(np.median(pair[model])),
                                     errors=errors[model],steps=20,rhs_calls=80))
    write('dynamics_cost',rows)
    print('Sequential cost benchmark:',len(rows),'configurations x 3 repeats')


if __name__=='__main__':main()
