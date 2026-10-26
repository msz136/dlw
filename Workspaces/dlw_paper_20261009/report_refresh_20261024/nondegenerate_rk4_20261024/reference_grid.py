"""Full Laplace/heat continuum reference for v0=4-3*u0_y.

The relation between the initial fields is NOT imposed at positive time.
Analytic Fourier evaluation, including analytic time derivatives; no time stepping.
See REFERENCE_GRID.md and reference_certificate.json for enclosure scope.
"""
from functools import lru_cache
import numpy as np

M = 32


def _parameters(case):
    if case.lower() in ('sine', 'sinusoidal'):
        return .03, np.pi/12, 0., 1, 8
    if case.lower() == 'gaussian':
        return .05, np.pi/96, np.sqrt(np.pi)/32, 96, 1
    raise ValueError(case)


@lru_cache(maxsize=512)
def _initial(case, y):
    A,w,C,K,multiple = _parameters(case)
    angle=np.pi/4*(y+2)
    s=A*np.sin(angle)/2
    sz=A*np.pi/4*np.cos(angle)/2
    n=np.arange(-K,K+1)
    f=(np.abs(n)==1)*.5 if K==1 else C*np.exp(-9*(w*n)**2)
    J=np.zeros(2*K+1,complex)
    nz=n!=0
    J[nz]=f[nz]/(1j*w*n[nz])
    term=np.ones(1,complex);ts=np.zeros(1,complex);tss=ts.copy()
    Q=term.copy();Qs=ts.copy();Qss=tss.copy()
    for m in range(1,M+1):
        term,ts,tss=(-s*np.convolve(J,term)/m,
                    -np.convolve(J,term+s*ts)/m,
                    -np.convolve(J,2*ts+s*tss)/m)
        Q,Qs,Qss=(np.pad(Q,(K,K))+term,
                   np.pad(Qs,(K,K))+ts,
                   np.pad(Qss,(K,K))+tss)
    return s,sz,Q,Qs,Qss,f


def _coefficients(case,y,t):
    A,w,C,K,multiple=_parameters(case)
    s,sz,Q0,Qs0,Qss0,f0=_initial(case,y)
    n=np.arange(-K*M,K*M+1);d=1j*w*n-s*C
    E=np.exp(d*d*t)
    Es=-2*C*d*t*E
    Ess=(2*C*C*t+4*C*C*d*d*t*t)*E
    Q=Q0*E;Qs=Qs0*E+Q0*Es;Qss=Qss0*E+2*Qs0*Es+Q0*Ess
    Qt=d*d*Q;Qst=d*d*Qs-2*C*d*Q
    Qsst=d*d*Qss-4*C*d*Qs+2*C*C*Q
    H=np.asarray([-s*Q,-Q-s*Qs,-2*Qs-s*Qss])
    Ht=np.asarray([-s*Qt,-Qt-s*Qst,-2*Qst-s*Qsst])
    nf=np.arange(-K,K+1);freq=w*nf
    F=f0*np.exp(freq*freq*t);Ft=freq*freq*F
    P=np.asarray([np.convolve(F,q) for q in (Q,Qs,Qss)])
    Pt=np.asarray([np.convolve(Ft,q)+np.convolve(F,qt)
                   for q,qt in zip((Q,Qs,Qss),(Qt,Qst,Qsst))])
    np_=np.arange(-(M+1)*K,(M+1)*K+1)
    dp=1j*w*np_-s*C; nz=np_!=0
    a0=np.zeros(len(np_),complex);a1=a0.copy();a2=a0.copy()
    a0[nz]=-s/dp[nz]
    a1[nz]=-1/dp[nz]-s*C/dp[nz]**2
    a2[nz]=-2*C/dp[nz]**2-2*s*C*C/dp[nz]**3
    if C:
        a0[~nz]=1/C
    def product(P):
        return np.asarray([a0*P[0],a1*P[0]+a0*P[1],
                           a2*P[0]+2*a1*P[1]+a0*P[2]])
    psi,psit=product(P),product(Pt)
    if not C:
        center=K*M
        mean=np.asarray([Q0[center],Qs0[center],Qss0[center]])
        mean_t=np.zeros(3,complex)
        for n0 in (-1,1):
            j=center-n0
            hs0=np.asarray([-s*Q0[j],-Q0[j]-s*Qs0[j],-2*Qs0[j]-s*Qss0[j]])
            mean_t+=(-1j*w*n0)*hs0
        psi[:,len(np_)//2]=mean+t*mean_t
        psit[:,len(np_)//2]=mean_t
    return s,sz,H,Ht,psi,psit,F


def _values(polys,polyst,w,C,s,X0,N,multiple,t):
    """p,px,ps,psx,pss,pssx plus their physical time derivatives."""
    center=(polys.shape[1]-1)//2
    n=np.arange(-center,center+1);d=1j*w*n-s*C
    # Physical t at fixed x, including d_s=-C and X_t=-4.
    qt=polyst.copy()
    qt[0]-=4*d*polys[0]
    qt[1]+=-4*d*polys[1]+4*C*polys[0]
    qt[2]+=-4*d*polys[2]+8*C*polys[1]
    x=X0+np.arange(N)*192/N
    a=-C*x
    folded=np.zeros((12,N),complex)
    phase=np.exp(1j*w*n*X0)
    for offset,qq in ((0,polys),(6,qt)):
        for j in range(3):
            np.add.at(folded[offset+2*j],(n*multiple)%N,qq[j]*phase)
            np.add.at(folded[offset+2*j+1],(n*multiple)%N,d*qq[j]*phase)
    raw=(np.fft.ifft(folded,axis=1)*N).real
    result=[]
    factor=np.exp(-s*C*x)
    for b in (0,6):
        q,qx,qs,qsx,qss,qssx=raw[b:b+6]
        result.append(factor*np.asarray([q,qx,qs+a*q,qsx+a*qx-C*q,
                qss+2*a*qs+a*a*q,
                qssx+2*a*qsx+a*a*qx-2*C*(qs+a*q)]))
    return result


def _mul(a,b):
    return a[0]*b[0],a[1]*b[0]+a[0]*b[1]


def _div(a,b):
    return a[0]/b[0],(a[1]*b[0]-a[0]*b[1])/(b[0]*b[0])


def _sub(a,b):
    return a[0]-b[0],a[1]-b[1]


@lru_cache(maxsize=1024)
def _row(case,y,t,x0,N):
    A,w,C,K,multiple=_parameters(case)
    s,sz,H,Ht,P,Pt,F=_coefficients(case,y,t)
    p,pt=_values(P,Pt,w,C,s,x0-4*t,N,multiple,t)
    h,ht=_values(H,Ht,w,C,s,x0-4*t,N,multiple,t)
    # A pair stores a value and its exact physical time derivative.
    p,px,ps,psx,pss,pssx=list(zip(p,pt))
    h,hx,hs,hsx,hss,hssx=list(zip(h,ht))
    D=_sub(_mul(p,hs),_mul(h,ps))
    Dx=_sub(_mul(p,hsx),_mul(hx,ps))
    Ds=_sub(_mul(p,hss),_mul(h,pss))
    Dxs=_sub(_mul(p,hssx),_mul(hx,pss))
    u0,u1=_sub(_div(Dx,D),_div(px,p))
    u=(-2*u0,-2*u1)
    z0,z1=_sub(_div(_sub(_mul(Dxs,D),_mul(Dx,Ds)),_mul(D,D)),
               _div(_sub(_mul(psx,p),_mul(px,ps)),_mul(p,p)))
    us=(-2*z0,-2*z1)
    nf=np.arange(-K,K+1);freq=w*nf
    fc=np.zeros((2,N),complex)
    phase=np.exp(1j*freq*(x0-4*t))
    np.add.at(fc[0],(nf*multiple)%N,F*phase)
    np.add.at(fc[1],(nf*multiple)%N,F*phase*(freq*freq-4j*freq))
    f,ft=(np.fft.ifft(fc,axis=1)*N).real
    r,rt=_div(_mul((f,ft),D),_mul(p,p))
    v=4+4*sz*r-sz*us[0]
    vt=4*sz*rt-sz*us[1]
    return u[0],v,u[1],vt


def _grid(case,x,y,t):
    x=np.asarray(x,dtype=float);y=np.atleast_1d(y).astype(float)
    assert x.ndim==1 and len(x)>1
    assert np.max(abs(x-(x[0]+np.arange(len(x))*192/len(x))))<1e-10
    assert -.000000000001 <= t <= .010000000000001
    out=np.asarray([_row(case.lower(),float(yy),float(t),float(x[0]),len(x)) for yy in y])
    return tuple(out[:,j,:] for j in range(4))


def exact(case,x,y,t):
    return _grid(case,x,y,t)[:2]


def rates(case,x,y,t):
    return _grid(case,x,y,t)[2:]


evaluate_grid=exact


def evaluate_ut(case,x,y,t):
    return rates(case,x,y,t)[0]


def initial_data(case,x,y):
    x=np.asarray(x,dtype=float);y=np.atleast_1d(y).astype(float)
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
    u=A*s*f;uy=A*sz*f;ux=A*s*fx;uxy=A*sz*fx
    ut=3*A*s*fxx-(u+4)*ux
    vt=-A*sz*fxx+3*(uy*ux+(u+4)*uxy)
    return dict(u=u,v=4-3*uy,uy=uy,ut=ut,vt=vt)
