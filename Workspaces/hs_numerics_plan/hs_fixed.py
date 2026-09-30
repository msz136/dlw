"""Fixed physical grid 2-HS comparison using m=u_xx+2 and C–N."""
import numpy as np
from scipy.linalg import solve_banded
from hs_solver import StepFailure


class FixedSystem:
    def __init__(self, x, c, reference):
        self.x=np.asarray(x,dtype=float)
        self.dx=float(self.x[1]-self.x[0]); self.c=float(c); self.reference=reference
        self.n=len(x)-2
        if self.n < 3 or not np.allclose(np.diff(x),self.dx):
            raise ValueError("Use a uniform physical grid with at least five points")
        ab=np.zeros((3,self.n))
        ab[0,1:]=1; ab[1]=-2; ab[2,:-1]=1
        self.poisson=ab

    def boundary(self,t):
        dx=self.dx; x=self.x
        extended=np.r_[x[0]-dx,x,x[-1]+dx]
        u,rho,_=self.reference.continuous_x(extended,t)
        # Match the same centered D2 operator used for interior m.
        m=u[2:]-2*u[1:-1]+u[:-2]
        m=m/dx**2+2
        return u[1:-1],rho[1:-1],m

    def initial(self,t0):
        _,rho,m=self.boundary(t0)
        return np.r_[m[1:-1],rho[1:-1]]

    def fields(self,t,z):
        if not np.all(np.isfinite(z)):
            raise StepFailure("Nonfinite fixed-grid state")
        n=self.n; uref,rr,mm=self.boundary(t)
        m=np.r_[mm[0],z[:n],mm[-1]]
        rho=np.r_[rr[0],z[n:],rr[-1]]
        if np.min(rho) <= 0:
            raise StepFailure("Nonpositive density")
        rhs=(m[1:-1]-2)*self.dx**2
        rhs[0]-=uref[0]; rhs[-1]-=uref[-1]
        ui=solve_banded((1,1),self.poisson,rhs,check_finite=False)
        u=np.r_[uref[0],ui,uref[-1]]
        return {'x':self.x,'u':u,'rho':rho,'m':m}

    def rhs(self,t,z):
        f=self.fields(t,z)
        dx=self.dx; u,rho,m=f['u'],f['rho'],f['m']
        ux=(u[2:]-u[:-2])/(2*dx)
        mx=(m[2:]-m[:-2])/(2*dx)
        rhor=(rho[2:]-rho[:-2])/(2*dx)
        mt=u[1:-1]*mx+2*ux*m[1:-1]+self.c**2*rho[1:-1]*rhor
        rt=((u*rho)[2:]-(u*rho)[:-2])/(2*dx)
        return np.r_[mt,rt]
