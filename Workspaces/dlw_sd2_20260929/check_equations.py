"""Independent smooth-data check: Eq.21 -> Eq.7 as x stencils refine."""
import numpy as np
from scipy.special import expit
from sd2 import SD2,previous
from pathlib import Path

def check(n,moving):
    m=SD2(previous.CASES['fig1a'],nx=n,L=2*np.pi)
    if moving:m.X.set_s(.12*np.sin(m.X.xi))
    x=m.X.x[None,:];j=np.arange(6)[:,None];h=m.h;a=m.pars.a
    q=1+.12*np.sin(x+.2*j)+.03*np.cos(2*x-.1*j)
    r=1+.08*np.cos(x-.3*j)
    D=m.dx
    w=q*r;omega=h*(1-w)
    mx=.04*np.sin(m.X.x)[None,:]-h*np.vstack((np.zeros(n),np.cumsum(D(w),axis=0)))
    A=mx[:-1]+mx[1:];H=h*h/4*(w*w-1)
    qt=-D(D(q))-2*a*D(q)-(A+H)*q
    rt=D(D(r))-2*a*D(r)+(A+H)*r
    u=2*D(q)/q
    ut=2*(D(qt)/q-D(q)*qt/q**2)
    ot=-h*(qt*r+q*rt)
    f=.5*(u*u+omega*omega)+2*a*u-h*omega
    residual1=np.diff(ut+D(f),axis=0)/h+D(D(np.diff(u,axis=0)/h+2/h*(omega[1:]+omega[:-1])))
    residual2=ot+D((u+2*a)*omega-h*u)-D(D(omega))
    return dict(nx=n,moving=moving,eq7_first=float(abs(residual1).max()),eq7_second=float(abs(residual2).max()))

def main():
    rows=[check(n,m) for m in (False,True) for n in (64,128,256)]
    for moving in (False,True):
        rr=[r for r in rows if r['moving']==moving]
        for f in ('eq7_first','eq7_second'):
            order=np.log2(rr[-2][f]/rr[-1][f]);assert 3.8<order<4.2,(moving,f,order)
            rr[-1][f+'_order']=float(order)
    exact_rows=[]
    for case,pars in previous.CASES.items():
        for moving in (False,True):
            for n in (256,512,1024):
                m=SD2(pars,nx=n);g=m.G;t=.01
                if moving:m.X.set_s(.15*np.sin(2*np.pi*m.X.xi/m.X.L))
                z=g.S*m.X.x[None,:]+g.omega*t+np.log(pars.rho/g.S)+m.js[:,None]*g.chi
                q=np.exp(np.logaddexp(0,z+g.gamma)-.5*np.logaddexp(0,z)-.5*np.logaddexp(0,z+g.chi))
                qt=q*g.omega*(expit(z+g.gamma)-.5*expit(z)-.5*expit(z+g.chi))
                w=1-g.S/m.h*(expit(z+g.chi)-expit(z))
                ds=lambda a:expit(a)*(1-expit(a))
                wt=-g.S*g.omega/m.h*(ds(z+g.chi)-ds(z))
                r=w/q;rt=wt/q-w*qt/q**2
                m.qexact=lambda unused:(q,qt)
                m.jump=np.expm1(g.gamma-.5*g.chi);m.rjump=np.expm1(-g.gamma+.5*g.chi)
                gotq,gotr,_,_=m.physical(t,m.pack(q,r))
                mask=abs(m.X.x)<10
                exact_rows.append(dict(case=case,moving=moving,nx=n,q_rhs_error=float(abs(gotq[:,mask]-qt[:,mask]).max()),r_rhs_error=float(abs(gotr[:,mask]-rt[:,mask]).max())))
            rr=exact_rows[-3:]
            for f in ('q_rhs_error','r_rhs_error'):
                order=np.log2(rr[-2][f]/rr[-1][f]);assert 3.7<order<4.3,(case,moving,f,order)
                rr[-1][f+'_order']=float(order)
    previous.dump(Path(__file__).parent/'equation_checks.json',dict(description='Eq21 -> Eq7 manufactured-field check, and actual SD2 RHS against finite-h exact tau Q/R derivatives. Four-order x residual decay; not a proof of integrability of the fully discrete scheme.',rows=rows,finite_h_exact_rhs=exact_rows))
    print('Passed manufactured and actual finite-h exact RHS checks:',len(rows)+len(exact_rows))

if __name__=='__main__':main()
