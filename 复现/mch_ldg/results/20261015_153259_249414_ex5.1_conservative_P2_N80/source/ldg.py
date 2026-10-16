"""Modal LDG, paper equations (2.4)-(2.5); periodic boundary baseline.

u[j,l] is the coefficient of P_l on cell j. Integrals are Gauss-exact
for every polynomial in the semidiscrete energy identity (no collocation aliasing).
"""
import numpy as np
from numpy.polynomial.legendre import leggauss, legvander, legder, legval
from scipy.sparse import coo_matrix, eye
from scipy.sparse.linalg import splu


class LDG:
    def __init__(self, n=80, k=3, left=-20., right=20., kappa=0., flux='conservative', nq=None):
        self.n, self.k = n, k
        self.left, self.right, self.kappa, self.flux = left, right, kappa, flux
        if flux not in ('conservative', 'dissipative'):
            raise ValueError(flux)
        self.h = (right-left)/n
        self.centers = left+(np.arange(n)+.5)*self.h
        self.z, self.w = leggauss(nq or max(2*k+2, 8))
        self.V = legvander(self.z,k)
        self.Vd = np.column_stack([legval(self.z,legder(np.eye(k+1)[l])) for l in range(k+1)])
        self.sign = (-1.)**np.arange(k+1)
        self.mass = self.h/(2*np.arange(k+1)+1)
        self.x = self.centers[:,None]+self.h/2*self.z
        self.K = self.V.T @ (self.w[:,None]*self.Vd)
        # Dminus uses u^- at every right interface; Dplus uses r^+.
        self.dm = self._derivative_matrix('minus')
        self.dp = self._derivative_matrix('plus')
        self.A = (eye(n*(k+1),format='csc')-self.dp@self.dm).tocsc()
        self.lu = splu(self.A)

    def _derivative_matrix(self, side):
        n,b=self.n,self.k+1
        rows=[]; cols=[]; data=[]
        block=-self.K.T
        if side=='minus':
            own=block+np.ones((b,b))
            nbr=-self.sign[:,None]*np.ones((1,b))
            shift=-1
        else:
            own=block-self.sign[:,None]*self.sign[None,:]
            nbr=np.ones((b,1))*self.sign[None,:]
            shift=1
        for j in range(n):
            for l in range(b):
                for m in range(b):
                    rows.extend([j*b+l,j*b+l]); cols.extend([j*b+m,((j+shift)%n)*b+m])
                    data.extend([own[l,m]/self.mass[l],nbr[l,m]/self.mass[l]])
        return coo_matrix((data,(rows,cols)),shape=(n*b,n*b)).tocsr()

    def derivative(self, values, right_flux):
        """Weak derivative of volume samples with one flux per right interface."""
        vol=values @ (self.w[:,None]*self.Vd)
        return (-vol+right_flux[:,None]-np.roll(right_flux,1)[:,None]*self.sign)/self.mass

    def traces(self,u):
        return u.sum(axis=1),np.roll(u@self.sign,-1)

    def deriv_minus(self,u):
        return (self.dm@u.ravel()).reshape(u.shape)

    def deriv_plus(self,u):
        return (self.dp@u.ravel()).reshape(u.shape)

    def project(self,fun,kind='radau',breakpoints=()):
        # Split integration at known cusps; no mollification of peakon initial data.
        z,w=leggauss(max(32,4*self.k+8))
        out=np.zeros((self.n,self.k+1))
        for j,c in enumerate(self.centers):
            a,b=c-self.h/2,c+self.h/2
            cuts=[a]+[p for p in breakpoints if a+1e-13<p<b-1e-13]+[b]
            for lo,hi in zip(cuts[:-1],cuts[1:]):
                xx=(lo+hi)/2+(hi-lo)/2*z
                out[j]+=(hi-lo)/2*(legvander((xx-c)*2/self.h,self.k).T@(w*fun(xx))) / self.mass
        if kind=='radau':
            # P_h^- matches the right endpoint, and moments through degree k-1.
            out[:,-1]=fun(self.centers+self.h/2)-out[:,:-1].sum(axis=1)
        elif kind!='l2':
            raise ValueError(kind)
        return out

    def rhs(self,u):
        r=self.deriv_minus(u)
        uq=u@self.V.T; rq=r@self.V.T
        um,up=self.traces(u); rm,rp=self.traces(r)
        ur=.5*(um*rm+up*rp)
        p=self.derivative(uq*uq*rq,ur*um)
        if self.flux=='conservative':
            ff=self.kappa**2*(um+up)+.25*(um+up)*(um*um+up*up)
            gg=(rm+rp)*(rm*rm+rp*rp)/12
        else:
            ff=2*self.kappa**2*um+um**3
            gg=rp**3/3
        ss=self.derivative(rq**3/3,gg)
        mt=(-self.derivative(2*self.kappa**2*uq+uq**3,ff)
            +self.deriv_plus(p)-self.derivative(rq*rq*uq,ur*rp)-self.deriv_plus(ss))
        return self.lu.solve(mt.ravel()).reshape(u.shape)

    def energy(self,u):
        r=self.deriv_minus(u)
        return float(np.sum((u*u+r*r)*self.mass))

    def mass_integral(self,u):
        return float(self.h*u[:,0].sum())

    def energy_rate(self,u,ut=None):
        if ut is None: ut=self.rhs(u)
        return float(2*np.sum((u*ut+self.deriv_minus(u)*self.deriv_minus(ut))*self.mass))

    def predicted_energy_rate(self,u):
        if self.flux=='conservative': return 0.
        r=self.deriv_minus(u)
        a,b=self.traces(u); c,d=self.traces(r)
        theta=(b-a)**2*(self.kappa**2+(b*b+2*a*b+3*a*a)/4)
        phi=-(d-c)**2*(c*c+2*c*d+3*d*d)/12
        return float(2*np.sum(-theta+phi))

    def sample(self,u,x):
        x=np.asarray(x); cells=np.clip(np.floor((x-self.left)/self.h).astype(int),0,self.n-1)
        z=2*(x-self.centers[cells])/self.h
        return np.sum(u[cells]*legvander(z,self.k),axis=-1)
