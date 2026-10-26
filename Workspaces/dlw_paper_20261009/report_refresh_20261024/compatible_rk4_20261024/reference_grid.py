"""Fast Cole--Hopf continuum reference for compatible Gaussian/sinusoidal data.

Physical y=z-2.  The analytic formula extends to every real y, including ghosts.
See REFERENCE_GRID.md and reference_certificate.json for all-node validation.
"""
from functools import lru_cache
import numpy as np

M = 32


def _parameters(case):
    if case.lower() in ('sinusoidal', 'sine'):
        return .03, np.pi/12, 0., 1, 8
    if case.lower() in ('gaussian',):
        return .05, np.pi/96, np.sqrt(np.pi)/32, 96, 1
    raise ValueError(case)


@lru_cache(maxsize=512)
def _coefficients(case, y):
    A, w, C, K, multiple = _parameters(case)
    kappa = np.pi/4
    angle = kappa*(y+2)
    s = -A*np.sin(angle)/2
    sz = -A*kappa*np.cos(angle)/2
    mu, muz = A*C*np.sin(angle), A*C*kappa*np.cos(angle)
    J = np.zeros(2*K+1, complex)
    for n in range(1,K+1):
        f = .5 if K==1 else C*np.exp(-9*(w*n)**2)
        J[K+n] = -1j*f/(w*n)
        J[K-n] = 1j*f/(w*n)
    term, termz = np.ones(1,complex), np.zeros(1,complex)
    Q, Qz = term.copy(), termz.copy()
    for m in range(1,M+1):
        termz = np.convolve(J,s*termz+sz*term)/m
        term = np.convolve(J,term)*(s/m)
        Q = np.pad(Q,(K,K))+term
        Qz = np.pad(Qz,(K,K))+termz
    n = np.arange(-M*K,M*K+1)
    return Q,Qz,w*n,n*multiple,mu,muz


def _jets(case,x,y,t,order=2):
    x,y = np.asarray(x,dtype=float), np.atleast_1d(y).astype(float)
    assert x.ndim==1 and np.isfinite(x).all()
    assert 0<=t<=.010000000000001
    N=len(x)
    uniform = N>1 and np.max(abs(x-(x[0]+np.arange(N)*192/N)))<1e-10
    out = []
    for yy in y:
        Q,Qz,freq,modes,mu,muz = _coefficients(case,float(yy))
        d = 1j*freq
        e = np.exp(-freq*freq*t+1j*freq*(x[0]-4*t-mu*t))
        coeff = [Q*e*d**j for j in range(order+1)]
        coeff += [Qz*e,Qz*e*d]
        if uniform:
            folded=np.zeros((len(coeff),N),complex)
            for row,c in zip(folded,coeff):
                np.add.at(row,modes%N,c)
            vals=(np.fft.ifft(folded,axis=1)*N).real
        else:
            phase=np.exp(1j*freq[:,None]*(x-x[0])[None,:])
            vals=np.asarray(coeff).dot(phase).real
        out.append((vals,mu,muz))
    return out


def evaluate_grid(case,x,y,t):
    """Return u,v arrays shaped (len(y),len(x))."""
    us,vs=[],[]
    for vals,mu,muz in _jets(case,x,y,t):
        H,Hx,Hxx,Hz,Hxz=vals
        u=mu-2*Hx/H
        uy=muz-2*((Hxz-muz*t*Hxx)/H-Hx*(Hz-muz*t*Hx)/(H*H))
        us.append(u);vs.append(4-uy)
    return np.asarray(us),np.asarray(vs)


def evaluate_ut(case,x,y,t):
    """Analytic u_t=u_xx-(u+4)u_x, including exterior ghost values."""
    uts=[]
    for vals,mu,muz in _jets(case,x,y,t,order=3):
        H,B,C,D,Hz,Hxz=vals
        u=mu-2*B/H
        ux=-2*(C/H-B*B/H**2)
        uxx=-2*(D/H-3*B*C/H**2+2*B**3/H**3)
        uts.append(uxx-(u+4)*ux)
    return np.asarray(uts)


def initial_data(case,x,y):
    """Analytic initial physical fields and time derivatives."""
    x,y=np.asarray(x,dtype=float),np.atleast_1d(y).astype(float)
    A,w,C,K,multiple=_parameters(case)
    if K==1:
        f=np.cos(w*x);fx=-w*np.sin(w*x);fxx=-w*w*f
    else:
        xx=x[None,:]+192*np.arange(-2,3)[:,None]
        g=np.exp(-(xx/6)**2)
        f=g.sum(0);fx=(-xx*g/18).sum(0)
        fxx=((xx*xx/324-1/18)*g).sum(0)
    s=np.sin(np.pi/4*(y+2))[:,None]
    sz=(np.pi/4*np.cos(np.pi/4*(y+2)))[:,None]
    u=A*s*f;uy=A*sz*f
    ux=A*s*fx;uxy=A*sz*fx;uxx=A*s*fxx;uxxy=A*sz*fxx
    ut=uxx-(u+4)*ux
    vt=-uxxy+uy*ux+(u+4)*uxy
    return dict(u=u,v=4-uy,uy=uy,ut=ut,vt=vt)
