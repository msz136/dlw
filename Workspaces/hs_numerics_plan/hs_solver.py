"""Open-chain semi-discrete 2-HS and ordinary moving-mesh solvers."""
from dataclasses import dataclass
import numpy as np
from scipy.integrate._ivp import dop853_coefficients


class StepFailure(RuntimeError):
    pass


@dataclass
class SolveResult:
    t: np.ndarray
    states: np.ndarray
    accepted: int
    rejected: int
    max_residual: float
    iterations: int
    status: str
    failure_reason: str = ''


class MovingSystem:
    def __init__(self, a, c, edges, left_u, kind='sd'):
        if a <= 0 or edges < 1 or kind not in ('sd','fd'):
            raise ValueError("Invalid lattice settings")
        self.a, self.c, self.edges = float(a),float(c),int(edges)
        self.left_u, self.kind = left_u,kind

    def exact_initial(self, reference, k0, t0):
        k=np.arange(k0,k0+self.edges+1)
        exact=reference.lattice_state(k,self.a,t0)
        return self.pack(exact['v'],exact['d'],exact['x'][0])

    def pack(self,v,d,x0):
        return np.r_[np.asarray(v),np.asarray(d),float(x0)]

    def fields(self,t,z):
        m=self.edges
        v=np.asarray(z[:m]); d=np.asarray(z[m:2*m]); x0=z[-1]
        if not np.all(np.isfinite(z)) or np.min(d) <= 0:
            raise StepFailure("Nonfinite state or nonpositive mesh edge")
        b=float(self.left_u(t))
        u=np.r_[b,b+np.cumsum(v)]
        x=np.r_[x0,x0+np.cumsum(d)]
        return {'v':v,'d':d,'x':x,'u':u,'rho':self.a/d,'w':v/d}

    def rhs(self,t,z):
        f=self.fields(t,z)
        v,d,u=f['v'],f['d'],f['u']
        if self.kind == 'sd':
            alpha=self.a*(self.a-self.c)
            dv=2*d*(u[1:]+u[:-1])+((d*d-alpha)**2-v*v)/(2*d)-self.c**2*d/2
        else:
            w=v/d
            dw=.5*w*w+2*(u[1:]+u[:-1])+.5*self.c**2*((self.a/d)**2-1)
            dv=d*dw-w*v
        return self.pack(dv,-v,-float(self.left_u(t)))


def advance(system,t,z,h,method,tol=1e-11,max_iter=70):
    f=system.rhs
    if method == 'euler':
        candidate=z+h*f(t,z); residual=0.; iters=0
    elif method == 'heun':
        k1=f(t,z)
        k2=f(t+h,z+h*k1)
        candidate=z+h*(k1+k2)/2; residual=0.; iters=0
    elif method == 'midpoint':
        k1=f(t,z)
        k2=f(t+h/2,z+h*k1/2)
        candidate=z+h*k2; residual=0.; iters=0
    elif method == 'rk4':
        k1=f(t,z); k2=f(t+h/2,z+h*k1/2)
        k3=f(t+h/2,z+h*k2/2); k4=f(t+h,z+h*k3)
        candidate=z+h*(k1+2*k2+2*k3+k4)/6; residual=0.; iters=0
    elif method == 'rk8':
        # Fixed-step 12-stage DOP853 order-8 main formula. No tolerance-based
        # adaptation; h is exactly the requested step except at output times.
        stages=[]
        for i in range(dop853_coefficients.N_STAGES):
            if i == 0:
                yi=z
            else:
                yi=z+h*sum(dop853_coefficients.A[i,j]*stages[j]
                            for j in range(i) if dop853_coefficients.A[i,j] != 0)
            stages.append(f(t+h*dop853_coefficients.C[i],yi))
        candidate=z+h*sum(dop853_coefficients.B[i]*stages[i]
                          for i in range(dop853_coefficients.N_STAGES)
                          if dop853_coefficients.B[i] != 0)
        residual=0.; iters=0
    elif method == 'trapezoid':
        f0=f(t,z); candidate=z+h*f0
        scale=max(1.,np.max(np.abs(z)))
        for iters in range(1,max_iter+1):
            new=z+h*(f0+f(t+h,candidate))/2
            residual=float(np.max(np.abs(new-candidate)))
            candidate=new
            if residual <= tol*scale:
                break
        else:
            raise StepFailure(f"Trapezoid iteration failed: residual={residual:g}")
        # Report the actual equation residual, not only the Picard increment.
        residual=float(np.max(np.abs(candidate-z-h*(f0+f(t+h,candidate))/2)))
    else:
        raise ValueError(method)
    system.fields(t+h,candidate)
    return candidate,residual,iters


def solve(system,z0,t0,t1,dt,method='rk4',outputs=None,tol=1e-11,
          min_dt=1e-10,max_rejections=40,strict=True):
    if not t1 > t0 or not dt > 0:
        raise ValueError("Require t1>t0 and dt>0")
    targets=np.unique(np.r_[t0, t1] if outputs is None else np.r_[t0,np.asarray(outputs),t1])
    if targets[0] < t0-1e-12 or targets[-1] > t1+1e-12:
        raise ValueError("Output times outside integration interval")
    t=float(t0); z=np.asarray(z0,dtype=float).copy(); states=[z.copy()]
    accepted=rejected=iterations=0; max_residual=0.
    for target in targets[1:]:
        while target-t > 1e-13*max(1,abs(target)):
            h=min(dt,target-t)
            try:
                trial,resid,iters=advance(system,t,z,h,method,tol)
                t+=h; z=trial; accepted+=1; iterations+=iters
                max_residual=max(max_residual,resid)
            except (StepFailure,FloatingPointError,OverflowError) as exc:
                rejected+=1; dt=h/2
                if dt < min_dt or rejected > max_rejections:
                    reason=f"Stopped at t={t:.12g}; {exc}"
                    if strict:
                        raise StepFailure(reason) from exc
                    if t > targets[len(states)-1]+1e-14:
                        return SolveResult(np.r_[targets[:len(states)],t],
                                           np.asarray(states+[z.copy()]),accepted,rejected,
                                           max_residual,iterations,'failed',reason)
                    return SolveResult(targets[:len(states)],np.asarray(states),
                                       accepted,rejected,max_residual,iterations,'failed',reason)
        t=float(target); states.append(z.copy())
    return SolveResult(targets,np.asarray(states),accepted,rejected,
                       max_residual,iterations,'completed')
