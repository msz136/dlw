"""Positive finite-h Gram principal-minor expansion for N-soliton diagnostics.

Subset weights are evaluated by log-sum-exp. Exact time and phase tangents are
weighted covariances, so phase projection does not use finite differences.
This is a reference evaluator, not a replacement for the production solver.
"""
import numpy as np
from gramtau import lam


class SolitonExpansion:
    def __init__(self,p,q,rho,a=4.,h=.25):
        self.p=np.asarray(p,dtype=float)
        self.q=np.asarray(q,dtype=float)
        self.rho=np.asarray(rho,dtype=float)
        self.a,self.h=float(a),float(h)
        self.n=len(self.p)
        if not (1<=self.n<=6 and len(self.q)==self.n and len(self.rho)==self.n):
            raise ValueError('expected 1..6 spectral triples')
        self.s=self.p+self.q
        self.omega=self.q*self.q-self.p*self.p
        P,Q=self.p-self.a,self.q+self.a
        self.chi=lam(P,h)*lam(Q,h)
        self.gamma=-(P+h/2)/(Q-h/2)
        if not (np.all(self.s>0) and np.all(self.rho>0)
                and np.all(P < -h/2) and np.all(Q > h/2)
                and np.all(self.chi>0) and np.all(self.gamma>0)):
            raise ValueError('outside positive regular Gram sector')
        self.logchi=np.log(self.chi)
        self.loggamma=np.log(self.gamma)
        self.ind=np.asarray([[float(bool(mask & (1<<i))) for i in range(self.n)]
                             for mask in range(1<<self.n)])
        pair=[]
        self.A={}
        for i in range(self.n):
            for k in range(i+1,self.n):
                value=(self.p[i]-self.p[k])*(self.q[i]-self.q[k])/((self.p[i]+self.q[k])*(self.p[k]+self.q[i]))
                if not (0<value<1):
                    raise ValueError('pair interaction outside positive ordered sector')
                self.A[(i,k)]=float(value)
                pair.append((i,k,np.log(value)))
        self.pair_log=np.asarray([sum(self.ind[m,i]*self.ind[m,k]*v for i,k,v in pair)
                                  for m in range(1<<self.n)])
        self.subset_s=self.ind@self.s
        self.subset_omega=self.ind@self.omega

    def _dlog(self,j,x,t,is_f,kind):
        x=np.atleast_1d(np.asarray(x,dtype=float))
        phase=(np.log(self.rho/self.s)+self.omega*t+j*self.logchi
               +(self.loggamma if is_f else 0))
        logw=self.ind@(phase[:,None]+self.s[:,None]*x[None,:])+self.pair_log[:,None]
        m=np.max(logw,axis=0)
        weights=np.exp(logw-m)
        weights/=np.sum(weights,axis=0)
        rate=np.sum(weights*self.subset_s[:,None],axis=0)
        if kind=='value':return rate
        if kind=='time':
            omega=np.sum(weights*self.subset_omega[:,None],axis=0)
            return np.sum(weights*(self.subset_s*self.subset_omega)[:,None],axis=0)-rate*omega
        if kind=='theta':
            mean_i=self.ind.T@weights
            rate_i=self.ind.T@(weights*self.subset_s[:,None])
            return rate_i-rate[None,:]*mean_i
        raise ValueError(kind)

    def _fields(self,js,x,t,kind):
        js=np.asarray(js,dtype=int)
        if js.size==0:raise ValueError('empty lattice index')
        lo,hi=int(js.min())-1,int(js.max())+2
        F={j:self._dlog(j,x,t,True,kind) for j in range(lo,hi+1)}
        G={j:self._dlog(j,x,t,False,kind) for j in range(lo,hi+1)}
        u={j:2*F[j]-G[j]-G[j+1] for j in range(lo,hi)}
        # theta fields have a leading spectral-parameter axis.
        axis=1 if kind=='theta' else 0
        U=np.stack([u[int(j)] for j in js],axis=axis)
        V=np.stack([4/self.h*(G[int(j)+1]-G[int(j)])
                    +(u[int(j)+1]-u[int(j)-1])/(2*self.h) for j in js],axis=axis)
        if not (np.all(np.isfinite(U)) and np.all(np.isfinite(V))):
            raise FloatingPointError('nonfinite soliton expansion field')
        return U,V

    def uv(self,js,x,t,derivative=False):
        return self._fields(js,x,t,'time' if derivative else 'value')

    def theta(self,js,x,t):
        """Return d(u,v)/d log(rho_i), with leading parameter axis."""
        return self._fields(js,x,t,'theta')
