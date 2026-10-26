"""Evaluate saved approximate fields. This does not produce certified values."""
from functools import lru_cache
import numpy as np
from solve import Solver,HERE

@lru_cache(maxsize=2)
def _load(case):
    if case=='Sinusoidal':M=32
    elif case=='Gaussian':M=128
    else:raise ValueError('case must be Sinusoidal or Gaussian')
    data=np.load(HERE/f'{case}_M{M}_Y24_dt5.0e-05.npz')
    return Solver(case,M,24),data['times'],data['coefficients']

def evaluate(case,x,y,t=.01):
    """Return array [u,v] with shape (2,len(y),len(x)).

    x,y must be scalar or 1D. Periodic x evaluation uses the Fourier expansion.
    Stored times use saved RK4 states; other t use cubic-Hermite interpolation
    with the projected vector field as endpoint derivatives. Validity here is
    algebraic evaluation of the candidate, not an error guarantee.
    """
    s,times,states=_load(case)
    x=np.atleast_1d(x).astype(float);y=np.atleast_1d(y).astype(float)
    if np.any(abs(y)>2) or not 0<=t<=.01:
        raise ValueError('require -2<=y<=2 and 0<=t<=.01')
    exact=np.flatnonzero(abs(times-t)<1e-16)
    if len(exact):z=states[exact[0]]
    else:
        j=np.searchsorted(times,t)-1;dt=times[j+1]-times[j]
        q=(t-times[j])/dt;z0=states[j];z1=states[j+1]
        f0=s.rhs(times[j],z0.ravel()).reshape(z0.shape)
        f1=s.rhs(times[j+1],z1.ravel()).reshape(z1.shape)
        z=(2*q**3-3*q*q+1)*z0+(q**3-2*q*q+q)*dt*f0+(-2*q**3+3*q*q)*z1+(q**3-q*q)*dt*f1
    return s.sample(z,x,y)

if __name__=='__main__':
    import json
    result={case:dict(x=0,y=0,t=.01,u_v=evaluate(case,0,0).ravel().tolist(),eta=None,
        certified=False) for case in ['Sinusoidal','Gaussian']}
    print(json.dumps(result,indent=2))
