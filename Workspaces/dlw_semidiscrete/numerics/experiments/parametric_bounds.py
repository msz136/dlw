"""Defect sweeps and small-grid Jacobian norm checks for the derived bounds."""
from parametric_study import PARAMS,save,inf,OUT
from parametric import Model,Parameters
from dataclasses import asdict
import numpy as np
from scipy.linalg import expm


def constants(m,t):
    z=m.exact(t);u,v=m.fields(z,t);P,Q=m.unpack(z)
    ell=(len(m.js)-1)*m.h;s=max(1,(len(m.js)-2)/2);d=1.5/m.X.dx;b=inf(u)+2*abs(m.pars.a)
    if m.model=='structure':
        H=b*ell+m.h*m.h*(inf(Q)/16+.25)
        c=1+(ell/(4*m.h) if m.closure=='compatible' else 0)
        K=max(2*d/m.h*H+d*d*(1+s+c),d*(b+(inf(Q)+4)*ell)+d*d)
        C=max(d*ell*ell/m.h+d*m.h/16,d*ell)
    else:
        K=max(2*d/m.h*b*ell+d*d,d*(b+inf(Q)*ell)+d*d*s+4*d*ell)
        C=max(d*ell*ell/m.h,d*ell)
    return K,C


def main():
    defects=[]
    for pars in PARAMS:
        for h in (.25,.125,.0625):
            for nx in (128,256,512):
                for model in ('structure','fd'):
                    for cont in (False,True):
                        m=Model(pars,h,nx,model=model,continuous=cont)
                        z=m.exact(0);r=m.rhs(0,z)-m.exact(0,True);ru,rv=m.error_fields(r)
                        defects.append({'pars':asdict(pars),'h':h,'nx':nx,'model':model,'continuous_background':cont,
                                        'state_defect':inf(r),'u_defect':inf(ru),'v_defect':inf(rv),
                                        'v_boundary_defect':inf(rv[[0,-1]]),'v_interior_defect':inf(rv[1:-1]),'K_C':constants(m,0)})
    save('parametric_defects',defects)
    rng=np.random.default_rng(1234);norms=[]
    for pars in (PARAMS[0],PARAMS[1],PARAMS[-1]):
        for model,closure in [('structure','original'),('structure','compatible'),('fd','original')]:
            m=Model(pars,.25,16,model=model,closure=closure,yhalf=.75,continuous=True)
            z=m.exact(0);eye=np.eye(z.size)
            A=np.column_stack([m.delta(0,z,e,True) for e in eye]);K,C=constants(m,0)
            rownorm=np.sum(abs(A),axis=1);mu=float(np.max(np.diag(A)+rownorm-abs(np.diag(A))))
            assert np.max(rownorm)<=K*(1+1e-12)
            for _ in range(5):
                e=rng.normal(size=z.size)*.001
                rem=m.delta(0,z,e)-m.delta(0,z,e,True)
                assert inf(rem)<=C*inf(e)**2+1e-14
            # Frozen-time propagator only: not the nonautonomous soliton propagator.
            norm=float(np.max(np.sum(abs(expm(.02*A)),axis=1)))
            assert norm<=np.exp(.02*mu)*(1+1e-12)
            norms.append({'pars':asdict(pars),'model':model,'closure':closure,'nx':16,'yhalf':.75,
                          'K':K,'C':C,'matrix_inf_norm':float(max(rownorm)),'mu_inf':mu,
                          'frozen_exp_norm_T002':norm,'spectral_abscissa':float(max(np.linalg.eigvals(A).real))})
    save('parametric_bounds',norms);print('defects',len(defects),'norm checks',len(norms),flush=True)

if __name__=='__main__':main()
