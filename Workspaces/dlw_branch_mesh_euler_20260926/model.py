"""Shared Euler/ALE driver for FD and the original DLW semidiscrete system.

The same two finite-h monitor/flux functionals are applied to both routes.
Their physical-x local conservation identities are exact for SD, not FD.
No reference forcing, filtering, or interior exact-state resetting is used.
"""
from pathlib import Path
import sys
import importlib.util
import numpy as np
from scipy.special import expit
from scipy.signal import resample
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('dlw_family_base', HERE.parent / 'dlw_coefficient_euler_20260926/model.py')
_base = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _base
_spec.loader.exec_module(_base)
FamilyModel, Parameters, LIB = _base.FamilyModel, _base.Parameters, _base.LIB
from moving_mesh import MovingGrid


class BranchProblem:
    def __init__(self, pars, route='sd', branch='minus', h=.125, nx=512,
                 L=40., yhalf=1.5):
        self.m = FamilyModel(pars, route=route, h=h, nx=nx, L=L, yhalf=yhalf)
        self.X = MovingGrid(nx, L)
        self.m.X = self.X
        self.m.op.X = self.X
        self.branch = branch
        self.weights = np.full(len(self.m.js)-2, 1/(len(self.m.js)-2))

    def density_flux(self, t, z):
        m = self.m
        P, v = m.unpack(z)
        u, _ = m.fields(z, t)
        w = v-m.dy(u, m.state_ghosts(u, t))
        if self.branch in ('minus', 'fixed'):
            r = 1-w/4
            q = (u+2*m.pars.a)*r-self.X.d1(r)-2*m.pars.a
            r, q = r[1:-1], q[1:-1]
        elif self.branch == 'plus':
            S = 2*P+(w[1:]+w[:-1])/2
            U = (u[1:]+u[:-1])/2+m.h*np.diff(w, axis=0)/8
            r = 1-S/4
            q = (U+2*m.pars.a)*r+self.X.d1(r)-2*m.pars.a
            r, q = (r[1:]+r[:-1])/2, (q[1:]+q[:-1])/2
        else:
            raise ValueError(self.branch)
        return np.einsum('j,jx->x', self.weights, r), np.einsum('j,jx->x', self.weights, q)

    def density_time_derivative(self, t, z, physical_rhs):
        """Differentiate this exact monitor functional along the physical RHS."""
        m = self.m
        Pt, vt = m.unpack(physical_rhs)
        bt = m.G.uv([m.js[0]], self.X.x, t, True)[0][0]
        ut = m.C.u_from_P(Pt, bt)
        wt = vt-m.dy(ut, m.right_ghost_derivative(ut, t))
        if self.branch in ('minus', 'fixed'):
            rt = -wt[1:-1]/4
        else:
            St = 2*Pt+(wt[1:]+wt[:-1])/2
            rt = -(St[1:]+St[:-1])/8
        return np.einsum('j,jx->x', self.weights, rt)

    def rhs(self, t, z, s):
        self.X.set_s(s)
        physical = self.m.rhs(t, z)
        R, Q = self.density_flux(t, z)
        if np.min(R) <= 0 or not np.all(np.isfinite(R)):
            raise ValueError('nonpositive or nonfinite branch density')
        # The computational x problem is periodic, so Q_R=Q_L exactly.
        # Analytic tail mismatch for the continuous reference is separately measured.
        V = np.zeros_like(R) if self.branch == 'fixed' else (Q-Q[0])/R
        P, v = self.m.unpack(z)
        transport = self.m.pack(V*self.X.d1(P), V*self.X.d1(v))
        return physical+transport, V

    def initial_potential_density(self, x):
        """Analytic x primitive and density of the SAME discrete initial monitor."""
        m = self.m
        k = m.pars.p+m.pars.q
        ell = 1/(m.pars.p-m.pars.a)+1/(m.pars.q+m.pars.a)
        lg = np.log((m.pars.a-m.pars.p)/(m.pars.a+m.pars.q))
        js = np.r_[m.js[0]-1, m.js, m.js[-1]+1]
        z = k*np.asarray(x)[None, :]+(js[:, None]+.5)*m.h*ell+np.log(m.pars.rho/k)
        f, g = expit(z+lg), expit(z)
        u = 2*k*(f-g)
        v = 2*k*ell*(f*(1-f)+g*(1-g))
        Iu = 2*(np.logaddexp(0, z+lg)-np.logaddexp(0, z))
        Iv = 2*ell*(f+g)

        def perturbation(uu, vv):
            w = vv[1:-1]-(uu[2:]-uu[:-2])/(2*m.h)
            if self.branch in ('minus', 'fixed'):
                return -self.weights @ w[1:-1]/4
            S = 2*np.diff(uu[1:-1], axis=0)/m.h+(w[1:]+w[:-1])/2
            return -self.weights @ ((S[1:]+S[:-1])/2)/4
        return np.asarray(x)+perturbation(Iu, Iv), 1+perturbation(u, v)

    def initial(self):
        x = self.X.xi.copy()
        if self.branch != 'fixed':
            endpoints = np.array([-self.X.L/2, self.X.L/2])
            ends, _ = self.initial_potential_density(endpoints)
            eta = np.arange(self.X.n)/self.X.n
            target = ends[0]+eta*(ends[1]-ends[0])
            for _ in range(24):
                potential, R = self.initial_potential_density(x)
                step = (potential-target)/R
                x -= step
                if np.max(abs(step)) < 2e-14:
                    break
            residual = np.max(abs(self.initial_potential_density(x)[0]-target))
            if residual > 2e-12:
                raise ValueError(f'initial inverse mass residual {residual}')
            x[0] = -self.X.L/2
        s = x-self.X.xi
        self.X.set_s(s)
        return self.m.exact(0), s

    def geometry(self, t, z, s, physical_rhs=None):
        self.X.set_s(s)
        R, Q = self.density_flux(t, z)
        JR = self.X.J*R
        mass = self.X.dx*np.sum(JR)
        answer = dict(min_J=float(min(self.X.J)), min_spacing=float(min(self.X.spacing())),
                      max_spacing=float(max(self.X.spacing())), min_R=float(min(R)),
                      max_R=float(max(R)), mass=float(mass),
                      relative_equidistribution_defect=float(np.max(abs(JR/JR.mean()-1))))
        if physical_rhs is not None:
            residual = self.density_time_derivative(t, z, physical_rhs)+self.X.d1(Q)
            answer['physical_conservation_residual'] = float(np.max(abs(residual)))
        return answer


def evaluate(problem, z, s, t, evaluation_factor=4, reconstruction_factor=16):
    """Compare both fields on the same physical x core using mapped Fourier output.

    Fourier upsampling takes place in the uniform computational coordinate.
    Cubic interpolation of the densely sampled physical curve evaluates a shared
    physical grid. Both evaluation and reconstruction resolutions are checked.
    """
    m, X = problem.m, problem.X
    X.set_s(s)
    uv = m.fields(z, t)
    nup = X.n*reconstruction_factor
    xup = -X.L/2+np.arange(nup)*X.L/nup+resample(s, nup)
    if np.min(np.diff(xup)) <= 0:
        raise ValueError('nonmonotone reconstructed coordinate')
    xx = -X.L/2+np.arange(X.n*evaluation_factor)*X.L/(X.n*evaluation_factor)
    xx = xx[(xx >= -10) & (xx < 10)]
    my = abs(m.y) < 1.5
    ref = m.G.uv(m.js[my], xx, t)
    fields = []
    for a in uv:
        aup = resample(a[my], nup, axis=-1)
        fields.append(CubicSpline(xup, aup, axis=-1)(xx))
    errors = {f:float(np.max(abs(a-b))) for f, a, b in zip(('u', 'v'), fields, ref)}
    return errors
