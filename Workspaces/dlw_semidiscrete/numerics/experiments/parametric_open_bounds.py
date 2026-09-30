"""Check the sharper h-uniform bounds and unchanged background zero state."""
from parametric_study import PARAMS,save,inf
from parametric_open import OpenModel
from parametric_bounds import constants
import numpy as np

def sharp(m):
    z=m.exact(0);P,Q=m.unpack(z);u,v=m.fields(z,0)
    ell=(len(m.js)-1)*m.h;d=1.5/m.X.dx;b=inf(u)+2*abs(m.pars.a)
    if m.model=='structure':
        kp=d*(b+inf(P)*ell+m.h*(inf(Q)/8+.5))+4*d*d
        kq=d*(b+(inf(Q)+4)*ell)+d*d;C=d*ell+d*m.h/16
    else:
        kp=d*(b+inf(P)*ell)+d*d
        kq=d*(b+inf(Q)*ell)+2*d*d+4*d*ell;C=d*ell
    return max(kp,kq),C

def main():
    rows=[];rng=np.random.default_rng(42)
    for pars in (PARAMS[0],PARAMS[1],PARAMS[-1]):
        for model in ('structure','fd'):
            for h in (.25,.125,.0625):
                m=OpenModel(pars,h,16,model=model,yhalf=.75,continuous=True)
                z=m.exact(0);K,C=sharp(m)
                A=np.column_stack([m.delta(0,z,e,True) for e in np.eye(len(z))])
                norm=float(np.max(np.sum(abs(A),axis=1)));assert norm<=K*(1+1e-12)
                for _ in range(3):
                    e=rng.normal(size=z.size)*.001
                    assert inf(m.delta(0,z,e)-m.delta(0,z,e,True))<=C*inf(e)**2+1e-12
                rows.append({'a':pars.a,'p':pars.p,'q':pars.q,'model':model,'h':h,'K':K,'C':C,'actual_J_inf':norm})
    save('parametric_open_bounds',rows);print('sharp bounds',len(rows),flush=True)

if __name__=='__main__':main()
