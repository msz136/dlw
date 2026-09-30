import sys
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'dlw_sd2_20260929'))
from sd2 import SD2,previous
from moving_mesh import MovingProblem
from reference import TwoExact,CASES

class TwoSD2(SD2):
    def __init__(self,case,h,nx,L):
        super().__init__(previous.pm.Parameters(a=case.a,p=1.,q=2.,rho=1.),h,nx,L)
        self.G=TwoExact(case,h)
        self.jump,self.rjump=self.G.qjump,self.G.rjump
    def qexact(self,t):return self.G.qr(self.js,self.X.x,t)[:2]

class Problem:
    def __init__(self,s):
        self.spec=s;self.sd2=s['model']=='SD2'
        case=CASES[s['case']]
        if self.sd2:
            self.m=TwoSD2(case,s['h'],s['nx'],s['L']);self.X=self.m.X
        else:
            self.p=MovingProblem(previous.pm.Parameters(a=case.a,p=1.,q=2.,rho=1.),h=s['h'],nx=s['nx'],L=s['L'],model='structure' if s['model']=='SD' else 'fd',continuous=True)
            self.m=self.p.m;self.m.G=TwoExact(case,s['h']);self.X=self.p.X

    def initial(self):
        if self.spec['mesh']=='moving':
            x=np.linspace(-self.X.L/2,self.X.L/2,40001)
            u,v=self.m.G.uv(self.m.js,x,0.);gh=self.m.G.uv([self.m.js[0]-1,self.m.js[-1]+1],x,0.)[0]
            den=1-np.mean(v-self.m.dy(u,gh),axis=0)/4
            if den.min()<=0:raise ValueError('initial monitor not positive')
            mass=np.r_[0,np.cumsum((den[:-1]+den[1:])*np.diff(x)/2)]
            xx=np.interp(np.arange(self.X.n)/self.X.n*mass[-1],mass,x)
            self.X.set_s(xx-self.X.xi)
        z=self.m.initial() if self.sd2 else self.m.exact(0.)
        return np.r_[z,self.X.s]

    def fields(self,state,t):
        self.X.set_s(state[-self.X.n:])
        return self.m.fields(state[:-self.X.n],t)

    def monitor(self,t,z):
        return self.m.monitor(t,z) if self.sd2 else self.p.mesh_density_flux(t,z)

    def rhs(self,t,state):
        if self.sd2:return self.m.rhs(t,state,self.spec['mesh'])
        z=state[:-self.X.n];self.X.set_s(state[-self.X.n:])
        phys=self.m.rhs(t,z)
        if self.spec['mesh']=='fixed':return np.r_[phys,np.zeros(self.X.n)]
        den,flux=self.monitor(t,z)
        if den.min()<=0:raise ValueError('nonpositive monitor')
        vel=(flux-flux[0])/den
        p,q=self.m.unpack(z)
        return np.r_[phys+self.m.pack(self.X.d1(p)*vel,self.X.d1(q)*vel),vel]
