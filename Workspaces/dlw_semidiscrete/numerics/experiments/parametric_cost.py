"""Run only AFTER all other experiments finish: repeated sequential RHS timings."""
from parametric_study import PARAMS,save
from parametric import Model,rk4
from parametric_open import OpenModel
from parametric_perturb import seed
import time

def main():
    specs=[(mo,cl,b) for mo,cl in [('structure','original'),('structure','compatible'),('fd','original'),('structure','extrapolated'),('fd','extrapolated')] for b in (False,True)]
    rows=[{'model':m,'closure':c,'balanced':b,'seconds':[]} for m,c,b in specs]
    for repeat in range(3):
        order=range(len(rows)) if repeat%2==0 else reversed(range(len(rows)))
        for k in order:
            row=rows[k];cls=OpenModel if row['closure']=='extrapolated' else Model
            m=cls(PARAMS[0],.125,256,model=row['model'],closure=row['closure'],continuous=True)
            e=seed(m,'high',.001);z=e if row['balanced'] else m.exact(0)+e
            fun=(lambda t,z:m.delta(t,m.exact(t),z)) if row['balanced'] else m.rhs
            start=time.perf_counter()
            for i in range(80):z=rk4(fun,i*.000125,z,.000125)
            row['seconds'].append(time.perf_counter()-start)
    save('parametric_cost',rows);print('cost runs',30,flush=True)

if __name__=='__main__':main()
