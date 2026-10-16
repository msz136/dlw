"""Direct centered finite differences for original mCH, no LDG rewriting."""
import numpy as np


class DirectFD:
    def __init__(self,n,left,right,kappa=0.,order=2,offset=0.):
        self.n=n;self.left=left;self.right=right;self.kappa=kappa;self.order=order
        self.h=(right-left)/n;self.x=left+(np.arange(n)+offset)*self.h
        theta=2*np.pi*np.fft.fftfreq(n)
        if order==2:
            d2=-4*np.sin(theta/2)**2/self.h**2
        elif order==4:
            d2=(-2*np.cos(2*theta)+32*np.cos(theta)-30)/(12*self.h**2)
        else:raise ValueError(order)
        self.helmholtz_symbol=1-d2

    def d1(self,u):
        if self.order==2:return (np.roll(u,-1)-np.roll(u,1))/(2*self.h)
        return (-np.roll(u,-2)+8*np.roll(u,-1)-8*np.roll(u,1)+np.roll(u,2))/(12*self.h)

    def d2(self,u):
        if self.order==2:return (np.roll(u,-1)-2*u+np.roll(u,1))/self.h**2
        return (-np.roll(u,-2)+16*np.roll(u,-1)-30*u+16*np.roll(u,1)-np.roll(u,2))/(12*self.h**2)

    def helmholtz(self,m):
        return np.fft.irfft(np.fft.rfft(m)/self.helmholtz_symbol[:self.n//2+1],n=self.n)

    def momentum(self,u):return u-self.d2(u)

    def rhs(self,u):
        m=self.momentum(u);r=self.d1(u)
        flux=2*self.kappa**2*u+(u*u-r*r)*m
        return self.helmholtz(-self.d1(flux))

    def energy(self,u):return float(self.h*np.dot(u,self.momentum(u)))

    def energy_rate(self,u):return float(2*self.h*np.dot(self.momentum(u),self.rhs(u)))

    def mass(self,u):return float(self.h*np.sum(u))
