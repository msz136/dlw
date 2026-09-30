"""Paper Eqs.29-31: positive four-term two-soliton tau, log-sum evaluation."""
from dataclasses import dataclass,asdict
import numpy as np
from scipy.special import logsumexp

@dataclass(frozen=True)
class Case:
    p:tuple
    q:tuple
    a:float=2.
    c:tuple=(1.,1.)
    phases:tuple=(0.,0.)

CASES={'fig3':Case((6.,4.),(-5.,-3.)),
       'fig4':Case((1.,4.),(2.,-3.)),
       'fig5':Case((7/4,1.),(-5/3,-4/5))}

class TwoExact:
    def __init__(self,case,h,continuous=True):
        self.case,self.h,self.continuous=case,h,continuous
        p,q=np.array(case.p),np.array(case.q);a=case.a
        self.S=p+q;self.T=q*q-p*p;self.Y=1/(p-a)+1/(q+a)
        cross=(p[0]-p[1])*(q[0]-q[1])/((p[0]+q[0])*(p[0]+q[1])*(p[1]+q[0])*(p[1]+q[1]))
        self.coeff=np.array([1.,1/self.S[0],1/self.S[1],cross])
        assert np.min(self.coeff)>0 and case.c==(1.,1.) and case.phases==(0.,0.)
        ratio=-(p-a)/(q+a)
        self.gamma=np.log(ratio)
        self.chi=np.log((p-a+h/2)/(p-a-h/2))+np.log((q+a+h/2)/(q+a-h/2))
        self.gammah=np.log(-(p-a+h/2)/(q+a-h/2))
        self.rates=np.array([[0,0,0],[self.S[0],self.T[0],self.Y[0]],
                             [self.S[1],self.T[1],self.Y[1]],
                             [sum(self.S),sum(self.T),sum(self.Y)]])
        self.qjump=np.expm1(sum(self.gamma))
        self.rjump=np.expm1(-sum(self.gamma))
        self._cache_key=None;self._cache={}

    def tau(self,js,x,t,is_f=False):
        js=np.atleast_1d(js);x=np.atleast_1d(x)
        phase=(js[:,None]+.5)*self.h*self.Y[None,:] if self.continuous else js[:,None]*self.chi[None,:]
        z=phase[:,:,None]+self.S[None,:,None]*x[None,None,:]+self.T[None,:,None]*t
        e=np.stack((np.zeros_like(z[:,0]),z[:,0],z[:,1],z[:,0]+z[:,1]),axis=0)
        coef=np.log(self.coeff).copy()
        if is_f:
            gg=self.gamma if self.continuous else self.gammah
            coef+=np.array([0.,gg[0],gg[1],sum(gg)])
        e+=coef[:,None,None]
        l=logsumexp(e,axis=0);w=np.exp(e-l[None,:,:])
        return l,w

    def mean(self,w,k):return np.einsum('i,ijk->jk',self.rates[:,k],w)
    def cov(self,w,a,b):
        return np.einsum('i,ijk->jk',self.rates[:,a]*self.rates[:,b],w)-self.mean(w,a)*self.mean(w,b)
    def third(self,w,a,b,c):
        aa=self.mean(w,a);bb=self.mean(w,b);cc=self.mean(w,c)
        return np.sum(w*(self.rates[:,a,None,None]-aa)*(self.rates[:,b,None,None]-bb)*(self.rates[:,c,None,None]-cc),axis=0)

    def uv(self,js,x,t,derivative=False):
        key=(float(t),np.asarray(x).tobytes())
        if self._cache_key!=key:self._cache_key=key;self._cache={}
        sub=(tuple(np.atleast_1d(js)),bool(derivative))
        if sub in self._cache:return tuple(a.copy() for a in self._cache[sub])
        js=np.atleast_1d(js)
        if self.continuous:
            _,f=self.tau(js,x,t,True);_,g=self.tau(js,x,t)
            if derivative:
                uv=(2*(self.cov(f,0,1)-self.cov(g,0,1)),2*(self.third(f,0,2,1)+self.third(g,0,2,1)))
            else:uv=(2*(self.mean(f,0)-self.mean(g,0)),2*(self.cov(f,0,2)+self.cov(g,0,2)))
        else:
            def gx(j,f=False):
                _,w=self.tau(j,x,t,f)
                return self.cov(w,0,1) if derivative else self.mean(w,0)
            def u(j):return 2*gx(j,True)-gx(j)-gx(j+1)
            uv=(u(js),4/self.h*(gx(js+1)-gx(js))+(u(js+1)-u(js-1))/(2*self.h))
        if len(self._cache)<16:self._cache[sub]=tuple(a.copy() for a in uv)
        return uv

    def qr(self,js,x,t):
        lf,f=self.tau(js,x,t,True);lg,g=self.tau(js,x,t)
        if self.continuous:
            q=np.exp(lf-lg);qt=q*(self.mean(f,1)-self.mean(g,1))
            return q,qt
        lg1,g1=self.tau(np.asarray(js)+1,x,t)
        q=np.exp(lf-.5*(lg+lg1))
        qt=q*(self.mean(f,1)-.5*(self.mean(g,1)+self.mean(g1,1)))
        w=1-(self.mean(g1,0)-self.mean(g,0))/self.h
        wt=-(self.cov(g1,0,1)-self.cov(g,0,1))/self.h
        r=w/q;rt=wt/q-w*qt/q**2
        return q,qt,r,rt
