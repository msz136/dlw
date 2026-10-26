"""Arbitrary-precision nonlinear FD solve for sinusoidal data.

The exact discrete equations preserve period 24 on the original period-192
domain. Work on one fundamental period with the SAME dx and h. This is an
invariant-subspace computation, not a continuum tail certificate. Acb/arb radii
are discarded at specified points, so this is NOT validated interval evolution.
"""
from pathlib import Path
import sys,time,json
import numpy as np
from flint import arb,acb,ctx
HERE=Path(__file__).resolve().parent

def solve(dps, dtstr='0.0001', dxstr='0.05'):
    ctx.dps=dps
    tag=f'Sinusoidal_precision{dps}_dx{dxstr}_dt{dtstr}'
    if (HERE/(tag+'.json')).exists():
        print('cached',tag); return
    dt=arb(dtstr); dx=arb(dxstr); h=arb('0.1'); a=arb(2)
    nx=round(24/float(dx)); ny=41; steps=round(.01/float(dt))
    pi=arb.pi()
    x=[24*arb(i)/nx for i in range(nx)]
    y=[-2+arb(i)/10 for i in range(ny)]
    def prof(yy):
        e=(pi*(yy+2)/4).sin()
        return np.array([[arb('.03')*e*(pi*xx/12).cos() for xx in x],
                         [arb('.02')*e*(pi*xx/12).sin() for xx in x]],dtype=object)
    initial=np.array([prof(yy) for yy in y],dtype=object).transpose(1,0,2)
    z=np.vectorize(lambda t:t.mid(),otypes=[object])(initial)
    freq=[2*pi*(i if i<nx//2 else i-nx)/24 for i in range(nx)]
    m1=[acb(0,f) for f in freq]; m1[nx//2]=acb(0)
    m2=[-f*f for f in freq]
    def der(z,mul):
        return np.array([[v.real.mid() for v in acb.dft([v*m for v,m in zip(acb.dft(row),mul)],inverse=True)] for row in z],dtype=object)
    left=prof(-2-h)[0]
    bc=prof(2+h)[0]-3*initial[0,-1]+3*initial[0,-2]-initial[0,-3]
    zero=np.array([arb(0) for _ in x],dtype=object)
    def rhs(z):
        u,v=z
        H=u*u/2+2*a*u
        dv2=der(v,m2)
        dh=der(H,m1)
        integ=np.cumsum((dv2[1:]+dv2[:-1])*h/2,axis=0)
        ut=np.concatenate((zero[None],-dh[1:]+dh[0]-integ))
        right=bc+3*u[-1]-3*u[-2]+u[-3]
        ext=np.concatenate((left[None],u,right[None]))
        uy=(ext[2:]-ext[:-2])/(2*h)
        vt=-der((u+2*a)*v-4*u,m1)-der(uy,m2)
        return np.array([ut,vt],dtype=object)
    start=time.perf_counter()
    for i in range(steps):
        k1=rhs(z);k2=rhs(z+dt*k1/2);k3=rhs(z+dt*k2/2);k4=rhs(z+dt*k3)
        z=z+dt*(k1+2*k2+2*k3+k4)/6
        z=np.vectorize(lambda t:t.mid(),otypes=[object])(z)
        if (i+1)%20==0:
            print(tag,'step',i+1,'/',steps,'seconds',round(time.perf_counter()-start,1),flush=True)
    zfloat=np.vectorize(float)(z)
    np.savez_compressed(HERE/(tag+'.npz'),z=zfloat,x=np.array([float(xx) for xx in x]),y=np.array([float(yy) for yy in y]))
    # Preserve decimal midpoints beyond float64 for precision comparison.
    (HERE/(tag+'.txt')).write_text('\n'.join(t.str(dps, radius=False) for t in z.flat),encoding='utf8')
    rec=dict(case='Sinusoidal',dps=dps,dx=float(dx),h=.1,dt=float(dt),T=.01,
        domain=[0,24],original_domain=[-96,96],method='same nonlinear FD on period-24 invariant subspace',
        amplitude=[float(abs(zfloat[j]).max()) for j in range(2)],seconds=time.perf_counter()-start,
        certified=False,rounding='arb/acb midpoints retained; interval radii discarded')
    (HERE/(tag+'.json')).write_text(json.dumps(rec,indent=2),encoding='utf8')
    print(json.dumps(rec),flush=True)

if __name__=='__main__':
    solve(int(sys.argv[1]),sys.argv[2] if len(sys.argv)>2 else '0.0001',sys.argv[3] if len(sys.argv)>3 else '0.05')
