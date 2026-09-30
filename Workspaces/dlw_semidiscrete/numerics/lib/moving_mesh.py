"""Common x moving mesh for the open-chain DLW parameter study.

The y lattice and its closure are unchanged.  The physical x derivative is
J^{-1} D_xi, where x=xi+s(xi,t), J=1+D_xi s.  Periodic x is used, with
the left endpoint pinned by subtracting the left density flux.
"""
import numpy as np
from scipy.special import expit, logsumexp

from dynamics import Grid
from parametric_open import OpenModel
from parametric import rk4


class MovingGrid(Grid):
    def __init__(self, n, L):
        super().__init__(n, L)
        self.xi = self.x.copy()
        self.s = np.zeros(n)
        self.J = np.ones(n)

    def set_s(self, s):
        self.s = np.asarray(s).copy()
        self.x = self.xi + self.s
        self.J = 1 + super().d1(self.s)
        if not np.all(np.isfinite(self.J)) or np.min(self.J) <= 0:
            raise ValueError('nonpositive mesh Jacobian')
        if np.min(self.spacing()) <= 0:
            raise ValueError('crossed physical mesh nodes')

    def spacing(self):
        return np.diff(np.r_[self.x, self.x[0] + self.L])

    def d1(self, f):
        return super().d1(f) / self.J

    def d2(self, f):
        return self.d1(self.d1(f))


def gram_phi(pars, h, js, x, t):
    """Phi_j=h^-1 log(G_{j+1}/G_j) for the positive N=1 Gram family."""
    p, q, a = pars.p, pars.q, pars.a
    P, Q = p-a, q+a
    chi = np.log((P+h/2)/(P-h/2)) + np.log((Q+h/2)/(Q-h/2))
    z = (p+q)*np.asarray(x)[None, :] + (q*q-p*p)*t
    z = z + np.log(pars.rho/(p+q)) + np.asarray(js)[:, None]*chi
    return (np.logaddexp(0, z+chi)-np.logaddexp(0, z))/h


def gram_mesh(pars, h, js, xi, t=0., weights=None):
    """Invert the normalized Gram coordinate with fixed periodic endpoints."""
    xi = np.asarray(xi)
    L = xi[1]-xi[0]
    L *= len(xi)
    left, right = xi[0], xi[0]+L
    if weights is None:
        weights = np.full(len(js), 1/len(js))
    weights = np.asarray(weights)
    def phi(x):
        return weights @ gram_phi(pars, h, js, x, t)
    pl, pr = phi(np.array([left, right]))
    mass = L-(pr-pl)
    target = (xi-left)*mass/L
    x = xi.copy()
    for _ in range(12):
        ph = phi(x)
        # Analytic derivative of x-Phi(x) is the positive Gram density.
        pp = (pars.p+pars.q)*np.asarray(x)[None, :]
        pp = pp + (pars.q**2-pars.p**2)*t + np.log(pars.rho/(pars.p+pars.q))
        P,Q=pars.p-pars.a,pars.q+pars.a
        chi=np.log((P+h/2)/(P-h/2))+np.log((Q+h/2)/(Q-h/2))
        pp=pp+np.asarray(js)[:,None]*chi
        density=1-(pars.p+pars.q)/h*(weights @ (expit(pp+chi)-expit(pp)))
        x -= ((x-left)-(ph-pl)-target)/density
    x[0] = left
    return x


class MovingProblem:
    def __init__(self, pars, h=.125, nx=128, L=20., model='structure',
                 continuous=False, yhalf=1.5):
        self.m = OpenModel(pars, h, nx, L, yhalf, model=model,
                           continuous=continuous)
        self.X = MovingGrid(nx, L)
        self.m.X = self.X
        self.m.op.X = self.X
        self.weights = np.full(len(self.m.js), 1/len(self.m.js))

    def set_s(self, s):
        self.X.set_s(s)

    def mesh_density_flux(self, t, z):
        m = self.m
        P, Qstate = m.unpack(z)
        u, v = m.fields(z, t)
        rho = 1-(v-m.dy(u, m.state_ghosts(u,t)))/4
        R = self.weights @ rho
        q = (u+2*m.pars.a)*rho-self.X.d1(rho)-2*m.pars.a
        Q = self.weights @ q
        return R, Q

    def rhs(self, t, state, balanced=False, mesh_mode='moving'):
        z_or_e, s = state
        self.set_s(s)
        m = self.m
        bg = m.exact(t)
        z = bg+z_or_e if balanced else z_or_e
        R, Q = self.mesh_density_flux(t,z)
        if np.min(R) <= 0:
            raise ValueError('nonpositive monitor density')
        velocity = (Q-Q[0])/R if mesh_mode == 'moving' else np.zeros_like(R)
        if balanced:
            physical = m.delta(t,bg,z_or_e)
        else:
            physical = m.rhs(t,z)
        p,q=m.unpack(z_or_e)
        transport=m.pack(self.X.d1(p)*velocity,self.X.d1(q)*velocity)
        return physical+transport, velocity

    def initial(self, mesh_mode='uniform', balanced=False, perturb=None):
        if mesh_mode in ('moving','static_adaptive'):
            x=gram_mesh(self.m.pars,self.m.h,self.m.js,self.X.xi)
            self.set_s(x-self.X.xi)
        else:
            self.set_s(np.zeros(self.X.n))
        bg=self.m.exact(0.)
        e=np.zeros_like(bg) if perturb is None else perturb(self.m)
        return (e if balanced else bg+e),self.X.s.copy()

    def evolve(self, T, dt, mesh_mode='moving', balanced=False, perturb=None,
               observations=(.005,.01)):
        state=self.initial(mesh_mode,balanced,perturb)
        n=round(T/dt)
        rows=[]
        for i in range(n):
            t=i*dt
            z,s=state
            def fun(tt,zz):
                zz0=zz[:z.size];ss=zz[z.size:]
                dz,ds=self.rhs(tt,(zz0,ss),balanced,mesh_mode)
                return np.r_[dz,ds]
            try:
                zz=rk4(fun,t,np.r_[z,s],dt)
                state=zz[:z.size],zz[z.size:]
                self.set_s(state[1])
            except ValueError as exc:
                return rows,dict(complete=False,reason=str(exc),final_t=t)
            if not np.all(np.isfinite(zz)) or np.max(abs(zz[:z.size]))>1e3:
                return rows,dict(complete=False,reason='state diverged',final_t=t)
            now=(i+1)*dt
            if any(abs(now-obs)<dt/4 for obs in observations):
                e=state[0] if balanced else state[0]-self.m.exact(now)
                eu,ev=self.m.error_fields(e)
                R,Q=self.mesh_density_flux(now,self.m.exact(now)+e)
                rows.append(dict(t=now,x=self.X.x.copy(),u_response=eu.copy(),
                                 v_response=ev.copy(),min_J=float(np.min(self.X.J)),
                                 min_dx=float(np.min(self.X.spacing())),
                                 max_R=float(np.max(R)),min_R=float(np.min(R))))
        return rows,dict(complete=True,final_t=T)
