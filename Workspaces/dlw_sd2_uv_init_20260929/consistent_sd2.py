"""Discrete u,v lift and compatible Dirichlet u boundary for SD2 Eq.21.

Only initial interior Q/R are lifted. During evolution, lift only the lowest
y boundary; interior Q/R are evolved by Eq.21, with no exact interior reset.
"""
import sys
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix,bmat,csc_matrix,diags
from scipy.sparse.linalg import splu
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parent/'dlw_two_soliton_20260929'
sys.path.insert(0,str(PRIOR))
from models import TwoSD2,Problem as OriginalProblem

class ConsistentSD2(TwoSD2):
    def __init__(self,case,h,nx,L):
        super().__init__(case,h,nx,L)
        ii=np.arange(nx)
        self.D=coo_matrix((np.concatenate([np.full(nx,c/(12*self.X.dx)) for c in (1,-8,8,-1)]),
                         (np.tile(ii,4),np.concatenate([(ii+k)%nx for k in (-2,-1,1,2)]))),shape=(nx,nx)).tocsc()
        self.b=np.zeros(nx);self.b[:2]=[7,-1];self.b[-2:]=[-1,7];self.b/=12*self.X.dx
        self.norm=csc_matrix(([1.],([0],[0])),shape=(1,nx))
        self.initial_right=None;self._boundary_key=None;self._boundary_value=None
        self.lift_diagnostics={}
        self.boundary_max_residual=0.;self.boundary_solves=0

    def lift(self,u):
        n=self.X.n
        A=bmat([[self.D-diags(.5*self.X.J*u),csc_matrix(self.b[:,None])],
                [self.norm,csc_matrix((1,1))]],format='csc')
        lu=splu(A);sol=lu.solve(np.r_[np.zeros(n),1.])
        q,jump=sol[:-1],sol[-1]
        if np.min(q)<=0 or 1+jump<=0:raise ValueError('discrete lift produced nonpositive Q or far field')
        residual=float(np.max(abs(2*(self.D@q+self.b*jump)/self.X.J/q-u)))
        if residual>1e-10:raise ValueError(f'discrete lift residual {residual}')
        return q,float(jump),lu,residual

    def boundary(self,t):
        key=(float(t),self.X.x.tobytes(),self.X.J.tobytes())
        if key!=self._boundary_key:
            js=[self.js[0]]
            _,f=self.G.tau(js,self.X.x,t,True);_,g=self.G.tau(js,self.X.x,t)
            u=2*(self.G.mean(f,0)-self.G.mean(g,0))[0]
            ut=2*(self.G.cov(f,0,1)-self.G.cov(g,0,1))[0]
            ux=2*(self.G.cov(f,0,0)-self.G.cov(g,0,0))[0]
            q,jump,lu,residual=self.lift(u)
            self.boundary_max_residual=max(self.boundary_max_residual,residual);self.boundary_solves+=1
            self._boundary_key=key;self._boundary_value=(q,jump,lu,u,ut,ux,residual)
        q,jump,lu,u,ut,ux,residual=self._boundary_value
        if self.initial_right is not None:
            # All right far fields share the lower-boundary gauge evolution.
            right=self.initial_right*(1+jump)/self.initial_right[0]
            self.jump=(right-1)[:,None];self.rjump=(1/right-1)[:,None]
        return self._boundary_value

    def boundary_derivative(self,t,velocity):
        q,jump,lu,u,ut,ux,residual=self.boundary(t)
        jdot=self.D@velocity
        material_u=ut+velocity*ux
        rhs=.5*(jdot*u+self.X.J*material_u)*q
        sol=lu.solve(np.r_[rhs,0.])
        # This is the derivative along the changing numerical mesh. Subtract
        # the SAME discrete ALE term used by the interior equations.
        qx=(self.D@q+self.b*jump)/self.X.J
        return sol[:-1]-velocity*qx,sol

    def qexact(self,t):
        q=self.boundary(t)[0]
        # Compatibility only: unpack is overridden, no interior exact Q used.
        return q[None,:],self.boundary_derivative(t,np.zeros(self.X.n))[0][None,:]

    def unpack(self,z,t):
        n=(self.shape[0]-1)*self.X.n
        q=np.vstack((self.boundary(t)[0],z[:n].reshape(self.shape[0]-1,-1)))
        return q,z[n:].reshape(self.shape)

    def initial(self):
        u,v=self.G.uv(self.js,self.X.x,0.)
        lifted=[self.lift(row) for row in u]
        q=np.array([a[0] for a in lifted]);self.initial_right=1+np.array([a[1] for a in lifted])
        self._boundary_key=None;self.boundary(0.)
        gh=self.G.uv([self.js[0]-1,self.js[-1]+1],self.X.x,0.)[0]
        r=(1-(v-self.dy(u,gh))/4)/q
        z=self.pack(q,r);actual=self.fields(z,0.)
        errors={f:float(abs(x-y).max()) for f,x,y in zip(('u','v'),actual,(u,v))}
        if max(errors.values())>1e-10:raise ValueError(f'initial physical fields not matched: {errors}')
        self.lift_diagnostics=dict(max_lift_residual=max(a[3] for a in lifted),initial_field_errors=errors,
                                   min_Q=float(q.min()),max_Q=float(q.max()),
                                   far_jump_range=[float(min(self.initial_right-1)),float(max(self.initial_right-1))],
                                   analytic_jump=float(self.G.qjump))
        return z

    def physical_arrays(self,q,r,qx,rx,qt0):
        qxx,rxx=self.dx(qx),self.dx(rx)
        w=q*r;wx=self.dx(w);H=self.h**2/4*(w*w-1)
        A0=-(qt0+qxx[0]+2*self.pars.a*qx[0])/q[0]-H[0]
        mx0=(A0+self.h*wx[0])/2
        mx=mx0[None,:]-self.h*np.vstack((np.zeros(self.X.n),np.cumsum(wx,axis=0)))
        A=mx[:-1]+mx[1:]
        return -qxx-2*self.pars.a*qx-(A+H)*q,rxx-2*self.pars.a*rx+(A+H)*r

    def rhs(self,t,state,mesh):
        z=state[:-self.X.n];self.X.set_s(state[-self.X.n:])
        q,r=self.unpack(z,t)
        if q.min()<=0:raise ValueError('nonpositive evolved Q')
        qx,rx=self.dx(q,self.jump),self.dx(r,self.rjump)
        vel=np.zeros(self.X.n)
        if mesh=='moving':
            w=q*r;den=w.mean(axis=0)
            if den.min()<=0:raise ValueError('nonpositive mesh monitor')
            flux=((2*qx/q+2*self.pars.a)*w-self.dx(w)-2*self.pars.a).mean(axis=0)
            vel=(flux-flux[0])/den
        qt0,_=self.boundary_derivative(t,vel)
        qt,rt=self.physical_arrays(q,r,qx,rx,qt0)
        return np.r_[self.pack(qt+vel*qx,rt+vel*rx),vel]

class Problem(OriginalProblem):
    def __init__(self,s):
        super().__init__(s)
        if self.sd2:
            self.m=ConsistentSD2(self.m.G.case,s['h'],s['nx'],s['L']);self.X=self.m.X
