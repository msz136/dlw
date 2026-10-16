"""Paper examples 5.1--5.5. Smooth solutions evaluated by monotone parametric inversion."""
import numpy as np


def invert_monotone(target, coordinate, scale=1.):
    target=np.asarray(target)
    lo=scale*target-80; hi=scale*target+80
    if np.any(coordinate(lo)>target) or np.any(coordinate(hi)<target):
        raise ValueError('Parametric bracket failed')
    for _ in range(58):
        mid=(lo+hi)/2
        test=coordinate(mid)<target
        lo=np.where(test,mid,lo); hi=np.where(test,hi,mid)
    return (lo+hi)/2


def profile(case,x,t=0.,alpha=.5,kappa=1.,c=1.):
    x=np.asarray(x)
    if case=='5.4':
        z=x-c*t; u=np.sqrt(1.5*c)*np.exp(-np.abs(z))
        return u,-np.sign(z)*u
    if case=='5.5':
        z=(x-c*t)%(2*np.pi)-np.pi
        amp=np.sqrt(3*c/(2*np.cosh(np.pi)**2+1))
        return amp*np.cosh(z),amp*np.sinh(z)
    if case=='5.1':
        a=1/np.sqrt(1-alpha**2); ct=2/(1-alpha**2); speed=ct+1
        z0=.5*np.log((1+alpha)/(1-alpha))
        A=np.sqrt(1-alpha); B=np.sqrt(1+alpha)
        def coord(z):
            # logaddexp avoids overflow in the parameter-to-physical map.
            return (z+z0)/alpha+2*(np.logaddexp(np.log(A)+z,np.log(B))-np.logaddexp(np.log(B)+z,np.log(A)))
        z=invert_monotone(x-speed*t,coord,alpha)
        ch=np.cosh(z); sh=np.sinh(z); factor=alpha**2*ct
        u=1+factor*(a*ch+1)/(ch+a)**2
        uz=factor*sh*(a*(ch+a)-2*(a*ch+1))/(ch+a)**3
        ez=np.exp(z)
        xz=1/alpha+2*(A*ez/(A*ez+B)-B*ez/(B*ez+A))
        return u,uz/xz
    if case=='5.2':
        b=kappa*alpha; speed=2*kappa*kappa/(1-b*b)
        def coord(z):
            th=np.tanh(z)
            return z/b+np.log1p(-b*th)-np.log1p(b*th)
        z=invert_monotone(x-speed*t,coord,b)
        ch=np.cosh(z); sh=np.sinh(z); den=np.cosh(2*z)+(1+b*b)/(1-b*b)
        factor=4*kappa*kappa*alpha/(1-b*b)**1.5
        u=factor*ch/den
        uz=factor*(sh*den-2*ch*np.sinh(2*z))/den**2
        xz=1/b-2*b/(ch*ch*(1-b*b*np.tanh(z)**2))
        return u,uz/xz
    if case=='5.3':
        aa=np.array([.7,.5]); rate=-2*aa*kappa**3/(1-(kappa*aa)**2)
        psi=.5*np.log((1+kappa*aa)/(1-kappa*aa)); coupling=((aa[0]-aa[1])/(aa[0]+aa[1]))**2
        def tau(y,sgn):
            e=np.exp(y[...,None]*aa+t*rate+sgn*psi)
            ab=e[...,0]*e[...,1]
            f=1+1j*e.sum(axis=-1)-coupling*ab
            fy=1j*(e*aa).sum(axis=-1)-coupling*aa.sum()*ab
            ft=1j*(e*rate).sum(axis=-1)-coupling*rate.sum()*ab
            fty=1j*(e*rate*aa).sum(axis=-1)-coupling*aa.sum()*rate.sum()*ab
            return f,fy,ft,fty
        def coord(y):
            f=tau(y,1)[0]; g=tau(y,-1)[0]
            return y/kappa+2*np.log(np.abs(g)/np.abs(f))
        y=invert_monotone(x,coord,kappa)
        f,fy,ft,fty=tau(y,1); g,gy,gt,gty=tau(y,-1)
        u=-np.imag(ft/f+gt/g)/kappa
        uy=-np.imag(fty/f-ft*fy/f**2+gty/g-gt*gy/g**2)/kappa
        xy=1/kappa+2*np.real(gy/g-fy/f)
        if np.any(xy<=0): raise ValueError('Nonmonotone two-soliton parametrization')
        return u,uy/xy
    raise ValueError(case)


def breakpoints(case,left,right,t=0.,c=1.):
    if case=='5.4': return [c*t]
    if case=='5.5':
        return [c*t+2*np.pi*j for j in range(int(np.floor((left-c*t)/(2*np.pi)))-1,int(np.ceil((right-c*t)/(2*np.pi)))+2)]
    return []
