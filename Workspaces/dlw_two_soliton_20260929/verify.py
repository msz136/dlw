"""Independent determinant reference, PDE identities and actual SD2 RHS checks."""
import json
from pathlib import Path
import mpmath as mp
import numpy as np
from reference import CASES,TwoExact
from models import TwoSD2,Problem,previous
HERE=Path(__file__).parent

def independent():
    mp.mp.dps=50;rows=[]
    for name,c in CASES.items():
        p,q=[[mp.mpf(str(v)) for v in vals] for vals in (c.p,c.q)];a=mp.mpf(c.a)
        def logtau(x,y,t,n):
            mat=mp.matrix(2)
            for i in range(2):
                for k in range(2):
                    exponent=(p[i]+q[k])*x+(q[k]**2-p[i]**2)*t+(1/(p[i]-a)+1/(q[k]+a))*y
                    mat[i,k]=int(i==k)+(-(p[i]-a)/(q[k]+a))**n*mp.exp(exponent)/(p[i]+q[k])
            return mp.log(mp.det(mat))
        ref=TwoExact(c,.125)
        for x,y,t in ((-.7,-.1875,0.),(.2,.3125,.02),(2.,1.0625,.01)):
            point=tuple(map(mp.mpf,(x,y,t)))
            def D(n,dx=0,dy=0,dt=0):return mp.diff(lambda xx,yy,tt:logtau(xx,yy,tt,n),point,(dx,dy,dt))
            u=2*(D(1,1)-D(0,1));v=2*(D(1,1,1)+D(0,1,1))
            ux=2*(D(1,2)-D(0,2));uy=2*(D(1,1,1)-D(0,1,1));uxy=2*(D(1,2,1)-D(0,2,1))
            uyt=2*(D(1,1,1,1)-D(0,1,1,1));vxx=2*(D(1,3,1)+D(0,3,1))
            vt=2*(D(1,1,1,1)+D(0,1,1,1));uxxy=2*(D(1,3,1)-D(0,3,1));vx=2*(D(1,2,1)+D(0,2,1))
            pde1=uyt+vxx+ux*uy+(u+2*a)*uxy
            pde2=vt+uxxy+ux*v+(u+2*a)*vx-4*ux
            uv=ref.uv([y/.125-.5],[x],t)
            er=max(abs(float(u)-uv[0][0,0]),abs(float(v)-uv[1][0,0]))
            assert er<1e-11 and max(abs(pde1),abs(pde2))<mp.mpf('1e-40')
            rows.append(dict(case=name,x=x,y=y,t=t,reference_error=float(er),pde_residual=float(max(abs(pde1),abs(pde2)))))
    return rows

def finite_rhs():
    rows=[]
    for name,c in CASES.items():
        for moving in (False,True):
            L=640. if name=='fig5' else 40.
            ns=(512,1024,2048) if name=='fig5' else (256,512,1024)
            for n in ns:
                m=TwoSD2(c,.125,n,L);m.G=TwoExact(c,.125,False)
                if moving:m.X.set_s(.15*np.sin(2*np.pi*m.X.xi/L))
                g=m.G;m.jump=np.expm1(sum(g.gammah-.5*g.chi));m.rjump=np.expm1(-sum(g.gammah-.5*g.chi))
                q,qt,r,rt=g.qr(m.js,m.X.x,.01)
                pq,pr,_,_=m.physical(.01,m.pack(q,r))
                mask=abs(m.X.x)<(100 if name=='fig5' else 10)
                row=dict(case=name,moving=moving,nx=n,q_error=float(abs(pq[:,mask]-qt[:,mask]).max()),r_error=float(abs(pr[:,mask]-rt[:,mask]).max()))
                rows.append(row)
            for f in ('q_error','r_error'):
                order=np.log2(rows[-2][f]/rows[-1][f]);rows[-1][f+'_order']=float(order)
                assert 3.5<order<4.5,(name,moving,f,order)
    return rows

def main():
    out=dict(independent_determinant_and_pde=independent(),finite_h_actual_rhs=finite_rhs())
    errs=[]
    for name in CASES:
        for model in ('SD','FD'):
            s=dict(case=name,model=model,mesh='moving',h=.125,nx=128,L=640. if name=='fig5' else 40.)
            p=Problem(s);z=p.initial();a=p.rhs(0.,z)
            b,c=p.p.rhs(0.,(z[:-p.X.n],z[-p.X.n:]),mesh_mode='moving')
            er=float(abs(a-np.r_[b,c]).max());assert er<1e-12;errs.append(er)
    out['legacy_wrapper_max_difference']=max(errs)
    previous.dump(HERE/'reference_checks.json',out)
    print('PASS: independent determinant/PDE, 18 finite-h SD2 RHS configurations, legacy wrapper')

if __name__=='__main__':main()
