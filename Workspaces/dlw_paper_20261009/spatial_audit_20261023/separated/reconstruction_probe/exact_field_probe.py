"""Matched Gram fields, independent of time stepping. Fixed left primitive."""
from pathlib import Path
import itertools,json
import numpy as np
from scipy.integrate import cumulative_trapezoid

HERE=Path(__file__).resolve().parent
CASES={'A':([1],[2],5),'B':([4],[-3],10),'C':([6,4],[-5,-3],30),'D':([1,4],[2,-3],30)}

def logjets(p,q,n,x,y,t,h=0):
    P=p-2;Q=q+2
    gamma=(1/P+1/Q) if h==0 else (np.log1p(h/(2*P))-np.log1p(-h/(2*P))+np.log1p(h/(2*Q))-np.log1p(-h/(2*Q)))/h
    C=1/(p[:,None]+q[None,:])
    if n:
        factor=-P[:,None]/Q[None,:]
        if h:factor=factor*np.sqrt((1-h*h/(4*P[:,None]**2))/(1-h*h/(4*Q[None,:]**2)))
        C=C*factor
    exps=[];ks=[];gs=[]
    for size in range(len(p)+1):
        for ids in itertools.combinations(range(len(p)),size):
            ii=list(ids);coeff=1. if not ii else float(np.linalg.det(C[np.ix_(ii,ii)]))
            assert coeff>0,(p,q,n,coeff)
            k=np.sum((p+q)[ii]);g=np.sum(gamma[ii]);omega=np.sum((q*q-p*p)[ii])
            exps.append(np.log(coeff)+k*x+g*y+omega*t);ks.append(k);gs.append(g)
    exps=np.stack(np.broadcast_arrays(*exps));exps-=exps.max(axis=0)
    weights=np.exp(exps);weights/=weights.sum(axis=0)
    ks=np.array(ks)[:,None,None];gs=np.array(gs)[:,None,None]
    lx=np.sum(weights*ks,axis=0)
    lxy=np.sum(weights*ks*gs,axis=0)-lx*np.sum(weights*gs,axis=0)
    return lx,lxy

def aux(p,q,x,y,t,h):
    fx=logjets(p,q,1,x,y,t,h)[0]
    gm=logjets(p,q,0,x,y-h/2,t,h)[0];gp=logjets(p,q,0,x,y+h/2,t,h)[0]
    return 2*fx-gm-gp,2*fx+gm+gp,4*(gp-gm)/h

def run(dx=.02):
    out=[]
    for case,(pl,ql,R) in CASES.items():
        p=np.array(pl,dtype=float);q=np.array(ql,dtype=float)
        x=np.linspace(-R,R,round(2*R/dx)+1)[None,:]
        # Fixed observation coordinates; the Gram formula defines smooth lattice extensions.
        y=np.linspace(-R,R,101)[:,None]
        for t in [0.,.01]:
            fx,fxy=logjets(p,q,1,x,y,t);gx,gxy=logjets(p,q,0,x,y,t)
            u=2*(fx-gx);v=2*(fxy+gxy)
            for h in [.1,.05,.025]:
                U=aux(p,q,x,y,t,h)[0]
                _,zp,wp=aux(p,q,x,y+h/2,t,h);_,zm,wm=aux(p,q,x,y-h/2,t,h)
                a=lambda w:w*w/32-w/4
                integral=cumulative_trapezoid((a(wp)-a(wm))/h,x.ravel(),axis=1,initial=0)
                V=(zp-zm)/h+h*h*integral
                out.append(dict(case=case,t=t,h=h,U=float(np.max(abs(U-u))),V=float(np.max(abs(V-v)))))
    return out

if __name__=='__main__':
    rows=run();fine=run(.01)
    result=dict(meaning='Exact matched Gram field errors, not RHS defects or evolved numerical errors',primitive='Integral from fixed x=-R; trapezoidal quadrature',rows=rows,max_relative_V_change_on_quadrature_refinement=max(abs(a['V']-b['V'])/b['V'] for a,b in zip(rows,fine)))
    (HERE/'exact_field_validation.json').write_text(json.dumps(result,indent=2))
    for c in CASES:
        rr=[r for r in rows if r['case']==c and r['t']==0]
        print(c,[(r['h'],r['U'],r['V']) for r in rr], 'orders', [[float(np.log2(rr[i][key]/rr[i+1][key])) for i in [0,1]] for key in ['U','V']])
    print('quadrature relative change',result['max_relative_V_change_on_quadrature_refinement'])
