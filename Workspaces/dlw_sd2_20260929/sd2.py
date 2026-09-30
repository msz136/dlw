"""Report Eq.21: evolve Q,R; reconstruct Eq.22. No exact interior forcing."""
import sys
from pathlib import Path
import numpy as np
from scipy.special import expit
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'dlw_paper_cases_20260927'))
import run as previous
from moving_mesh import MovingGrid

class SD2:
    def __init__(self,pars,h=.125,nx=256,L=40.):
        self.pars,self.h=pars,h
        self.X=MovingGrid(nx,L)
        self.js=np.arange(-round(1.5/h),round(1.5/h))
        self.y=(self.js+.5)*h
        self.G=previous.PaperExact(pars,h,True)
        self.shape=(len(self.js),nx)
        self.jump=np.expm1(self.G.gamma0)
        self.rjump=np.expm1(-self.G.gamma0)

    def dx(self,f,jump=0.):
        # Affine-periodic extension: f(x+L)=f(x)+far-field jump.
        def shift(k):
            a=np.roll(f,k,axis=-1).copy()
            if k>0:a[...,:k]-=jump
            else:a[...,k:]+=jump
            return a
        return (shift(2)-8*shift(1)+8*shift(-1)-shift(-2))/(12*self.X.dx*self.X.J)

    def dy(self,u,ghost):
        e=np.concatenate((ghost[0][None,:],u,ghost[1][None,:]))
        return (e[2:]-e[:-2])/(2*self.h)

    def qexact(self,t):
        g=self.G
        z=g.S*self.X.x[None,:]+g.omega*t+np.log(self.pars.rho/g.S)+(self.js[:,None]+.5)*self.h*g.ry
        q=np.exp(np.logaddexp(0,z+g.gamma0)-np.logaddexp(0,z))
        qt=q*g.omega*(expit(z+g.gamma0)-expit(z))
        return q,qt

    def pack(self,q,r):return np.r_[q[1:].ravel(),r.ravel()]
    def unpack(self,z,t):
        n=(self.shape[0]-1)*self.shape[1]
        q=np.vstack((self.qexact(t)[0][0],z[:n].reshape(self.shape[0]-1,-1)))
        return q,z[n:].reshape(self.shape)

    def initial(self):
        q,_=self.qexact(0.)
        u,v=self.G.uv(self.js,self.X.x,0.)
        gh=self.G.uv([self.js[0]-1,self.js[-1]+1],self.X.x,0.)[0]
        w=1-(v-self.dy(u,gh))/4
        return self.pack(q,w/q)

    def fields(self,z,t):
        q,r=self.unpack(z,t)
        u=2*self.dx(q,self.jump)/q
        gh=self.G.uv([self.js[0]-1,self.js[-1]+1],self.X.x,t)[0]
        bg=self.G.uv(self.js[-3:],self.X.x,t)[0]
        e=u[-3:]-bg
        gh[1]+=3*e[-1]-3*e[-2]+e[-3]
        return u,4*(1-q*r)+self.dy(u,gh)

    def physical(self,t,z):
        q,r=self.unpack(z,t)
        qx,rx=self.dx(q,self.jump),self.dx(r,self.rjump)
        qxx,rxx=self.dx(qx),self.dx(rx)
        w=q*r;wx=self.dx(w)
        # Fix the y-integration constant by the prescribed lower Q boundary.
        # A=(M_j+M_{j+1})_x, M_{j+1,x}-M_{j,x}=-h*D_x(QR).
        H=self.h**2/4*(w*w-1)
        qt0=self.qexact(t)[1][0]
        A0=-(qt0+qxx[0]+2*self.pars.a*qx[0])/q[0]-H[0]
        mx0=(A0+self.h*wx[0])/2
        mx=mx0[None,:]-self.h*np.vstack((np.zeros(self.X.n),np.cumsum(wx,axis=0)))
        A=mx[:-1]+mx[1:]
        qt=-qxx-2*self.pars.a*qx-(A+H)*q
        rt=rxx-2*self.pars.a*rx+(A+H)*r
        return qt,rt,qx,rx

    def monitor(self,t,z):
        q,r=self.unpack(z,t);u=2*self.dx(q,self.jump)/q
        w=q*r
        return np.mean(w,axis=0),np.mean((u+2*self.pars.a)*w-self.dx(w)-2*self.pars.a,axis=0)

    def rhs(self,t,state,mesh):
        z=state[:-self.X.n];self.X.set_s(state[-self.X.n:])
        q,r=self.unpack(z,t)
        if np.min(q)<=0:raise ValueError('nonpositive Q')
        qt,rt,qx,rx=self.physical(t,z)
        vel=np.zeros(self.X.n)
        if mesh=='moving':
            den,flux=self.monitor(t,z)
            if np.min(den)<=0:raise ValueError('nonpositive mesh monitor')
            vel=(flux-flux[0])/den
        return np.r_[self.pack(qt+vel*qx,rt+vel*rx),vel]
