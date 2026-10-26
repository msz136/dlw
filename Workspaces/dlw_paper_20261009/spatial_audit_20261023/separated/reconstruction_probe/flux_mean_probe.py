"""Local nonlinear flux-matching mean; retain exact transformed dynamics."""
from probe import *

def from_uw(m,u,w):
    rad=(u+2*m.a)**2+2*m.h*m.h*A(w)
    if np.min(rad)<=0:raise ValueError('nonpositive flux root')
    return -2*m.a+np.sqrt(rad),np.diff(u,axis=0)/m.h+(w[1:]+w[:-1])/2

def test_flux(case,h):
    m=Model(case,'Centered-SD',.1,h);target=m.initial()[0];ye=(m.y[1:]+m.y[:-1])/2;V=m.profile(ye)[1]
    _,g=m.G.tau(m.y[:1]/h-.5,m.x,0,False);w=np.empty_like(target);w[0]=4*m.G.cov(g,0,2)[0]
    u=np.empty_like(target)
    def recover(k,wk):
        rad=(target[k]+2*m.a)**2-2*h*h*A(wk)
        if np.min(rad)<=0:raise ValueError('nonpositive inverse root')
        return -2*m.a+np.sqrt(rad)
    u[0]=recover(0,w[0]);maxres=0;maxit=0
    for k in range(1,len(u)):
        cand=w[k-1].copy()
        for it in range(100):
            uk=recover(k,cand)
            nxt=2*(V[k-1]-(uk-u[k-1])/h)-w[k-1]
            err=float(np.max(abs(nxt-cand)))
            if err<2e-12:break
            cand=nxt
        else:raise ValueError('inverse failed')
        w[k]=cand;u[k]=recover(k,cand);maxres=max(maxres,err);maxit=max(maxit,it+1)
    wt=m.d2(w)-m.d1((u+2*m.a)*w-4*u)
    target_t=m.ut(m.y,0)
    base=((target[0]+2*m.a)*target_t[0]-h*h*Ap(w[0])*wt[0])/(u[0]+2*m.a)
    r=-np.diff(m.d1(u*u/2+2*m.a*u+h*h*A(w)),axis=0)/h-m.d2(np.diff(u,axis=0)/h+(w[1:]+w[:-1])/2)
    ut=np.concatenate((base[None],base[None]+h*np.cumsum(r,axis=0)))
    Ut=((u+2*m.a)*ut+h*h*Ap(w)*wt)/(target+2*m.a)
    Vt=np.diff(ut,axis=0)/h+(wt[1:]+wt[:-1])/2
    ev=np.concatenate([fields(m,ye[i:i+64])[2][1] for i in range(0,len(ye),64)])
    mx=abs(m.x)<=HALF_WIDTHS[case];mu=abs(m.y)<HALF_WIDTHS[case];mv=abs(ye)<HALF_WIDTHS[case]
    Ucheck,Vcheck=from_uw(m,u,w)
    eps=1e-6;up,vp=from_uw(m,u+eps*ut,w+eps*wt);um,vm=from_uw(m,u-eps*ut,w-eps*wt)
    row=dict(case=case,h=h,dx=.1,status='complete',inverse_max_iterations=maxit,inverse_residual=maxres,map_residual=max(float(np.max(abs(Ucheck-target))),float(np.max(abs(Vcheck-V)))),defects=[float(np.max(abs(Ut-target_t)[mu][:,mx])),float(np.max(abs(Vt-ev)[mv][:,mx]))],pushforward_check=max(float(np.max(abs((up-um)/(2*eps)-Ut))),float(np.max(abs((vp-vm)/(2*eps)-Vt)))))
    (HERE/f'{case}_{h:g}_fluxmean.json').write_text(json.dumps(row,indent=2));print(json.dumps(row),flush=True)

if __name__=='__main__':
    for c in 'ABCD':
        for h in [.1,.05,.025]:test_flux(c,h)
