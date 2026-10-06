"""Independent high-precision derivatives and alternate SD1 stencil identity.

This is a scientific implementation check, not a sampling proof of a norm bound.
The HTML cells execute JavaScript; this file is solely validation material.
"""
from pathlib import Path
from functools import lru_cache
import json
import mpmath as mp

HERE=Path(__file__).resolve().parent
mp.mp.dps=60
samples=json.loads((HERE/'independent_samples.json').read_text(encoding='utf-8'))
worst_coefficient=0.0
worst_residual=0.0
checked=0
for row in samples:
    a,p,q=(mp.mpf(v) for v in ((2,1,2) if row['name']=='A' else (2,4,-3)))
    k=p+q; ell=1/(p-a)+1/(q+a); gamma=-(p-a)/(q+a); omega=q*q-p*p
    z=mp.mpf(str(row['z'])); h=mp.mpf(str(row['h']))
    sig=lambda zz:1/(1+mp.exp(-zz))
    U=lambda zz:2*k*(sig(zz+mp.log(gamma))-sig(zz))
    V=lambda zz:2*k*ell*(mp.diff(sig,zz+mp.log(gamma))+mp.diff(sig,zz))
    w=lambda zz:4*k*ell*mp.diff(sig,zz)
    Bxy=k*ell*mp.diff(lambda zz:w(zz)**2/32-w(zz)/4,z,2)
    N=k*ell**3*mp.diff(lambda zz:mp.diff(U,zz)*mp.diff(U,zz,2),z)/2
    vterm=k*k*ell*ell*mp.diff(V,z,4); uterm=k*k*ell**3*mp.diff(U,z,5)
    coefficient={'FD':[vterm/12,uterm/6],
                 'SD':[vterm/12-uterm/4+Bxy,vterm/4-uterm/12+Bxy+N]}
    @lru_cache(None)
    def jet(j):
        zz=z+ell*h*j
        return ([mp.diff(U,zz,n) for n in range(4)],
                [mp.diff(V,zz,n) for n in range(3)])
    @lru_cache(None)
    def node(j):
        u,v=jet(j); plus,_=jet(j+1); minus,_=jet(j-1)
        D=[(plus[n]-minus[n])/(2*h) for n in range(3)]
        W=[v[n]-D[n] for n in range(3)]
        Ax=k*(u[0]+2*a)*u[1]
        Hx=Ax+h*h*k*(W[0]/16-mp.mpf(1)/4)*W[1]
        return u,v,D,W,Ax,Hx
    pp,mm=node(mp.mpf('.5')),node(mp.mpf('-.5'))
    uu,vv,dd,ww,_,_=node(0)
    for scheme in ('SD','FD'):
        r1=omega*(pp[0][1]-mm[0][1])/h+(pp[5 if scheme=='SD' else 4]-mm[5 if scheme=='SD' else 4])/h
        r1+=k*k*(pp[1][2]+mm[1][2])/2
        if scheme=='SD':
            # Alternate exact form M_-v_xx - h²/4 Δ_h δ_-u_xx.
            d3=(jet(mp.mpf('1.5'))[0][2]-3*pp[0][2]+3*mm[0][2]-jet(mp.mpf('-1.5'))[0][2])/h**3
            r1-=k*k*h*h*d3/4
            plus,minus=node(mp.mpf(1)),node(mp.mpf(-1))
            r2=omega*vv[1]+(plus[5]-minus[5])/(2*h)
            r2+=k*(uu[1]*ww[0]+(uu[0]+2*a)*ww[1]-4*uu[1])
            r2+=k*k*(dd[2]+(plus[3][2]-2*ww[2]+minus[3][2])/4)
        else:
            r2=omega*vv[1]+k*(uu[1]*vv[0]+(uu[0]+2*a)*vv[1]-4*uu[1])+k*k*dd[2]
        for i,value in enumerate((r1,r2)):
            coefficient_error=abs(mp.mpf(row['coefficient'][scheme][i])-coefficient[scheme][i])/(1+abs(coefficient[scheme][i]))
            residual_error=abs(mp.mpf(row[scheme][i])-value)/(1+abs(value))
            assert coefficient_error<mp.mpf('1e-12'), (row,scheme,i,coefficient_error)
            assert residual_error<mp.mpf('1e-11'), (row,scheme,i,residual_error)
            worst_coefficient=max(worst_coefficient,float(coefficient_error))
            worst_residual=max(worst_residual,float(residual_error)); checked+=1
result={'status':'passed','precision_digits':60,'coefficient_and_residual_comparisons':checked,
        'max_relative_coefficient_difference':worst_coefficient,
        'max_relative_finite_h_residual_difference':worst_residual,
        'method':'mpmath direct analytic differentiation; SD1 uses alternate Mv−h²Δδu/4 stencil',
        'scope':'Implementation sanity check at A/B, 7 phases, 3 grid sizes; analytic bounds are established by the theory, not by these samples.'}
(HERE/'independent_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
