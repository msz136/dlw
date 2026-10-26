"""Independent diagnostics; all sampled differences, NOT continuum bounds."""
import json
import numpy as np
from numpy.polynomial import chebyshev as ch
from scipy.integrate import solve_ivp
from solve import Solver,HERE

PAIRS=[
 ('x','Sinusoidal_M16_Y16_dt1.0e-04','Sinusoidal_M32_Y16_dt1.0e-04'),
 ('y','Sinusoidal_M32_Y16_dt1.0e-04','Sinusoidal_M32_Y24_dt1.0e-04'),
 ('time','Sinusoidal_M32_Y24_dt1.0e-04','Sinusoidal_M32_Y24_dt5.0e-05'),
 ('x','Sinusoidal_M32_Y24_dt5.0e-05','Sinusoidal_M64_Y24_dt5.0e-05'),
 ('x','Gaussian_M64_Y16_dt1.0e-04','Gaussian_M96_Y16_dt1.0e-04'),
 ('x','Gaussian_M96_Y16_dt1.0e-04','Gaussian_M128_Y16_dt1.0e-04'),
 ('y','Gaussian_M128_Y16_dt1.0e-04','Gaussian_M128_Y24_dt1.0e-04'),
 ('time','Gaussian_M128_Y24_dt1.0e-04','Gaussian_M128_Y24_dt5.0e-05'),
 ('x','Gaussian_M128_Y24_dt5.0e-05','Gaussian_M192_Y24_dt5.0e-05')]

out={'continuum_certificate':False,'eta_u':None,'eta_v':None,'refinements':[],'candidates':[]}
for kind,a,b in PAIRS:
    qa=np.load(HERE/(a+'.npz'));qb=np.load(HERE/(b+'.npz'))
    diff=np.max(abs(qa['field']-qb['field']),axis=(1,2)).tolist()
    out['refinements'].append(dict(axis=kind,coarse=a,fine=b,max_difference_u_v=diff))

for case,M in [('Sinusoidal',32),('Gaussian',128)]:
    name=f'{case}_M{M}_Y24_dt5.0e-05'
    data=np.load(HERE/(name+'.npz'))
    s=Solver(case,M,24);x=data['x'];y=data['y']
    # Independent adaptive eighth-order RK calculation.
    alt=solve_ivp(s.rhs,(0,.01),s.initial().ravel(),method='DOP853',rtol=1e-13,atol=1e-16)
    assert alt.success
    alternate=s.sample(alt.y[:,-1],x,y)
    alt_diff=np.max(abs(alternate-data['field']),axis=(1,2)).tolist()
    interp=ch.chebvander(y/2,24)@s.C
    dy=interp@s.D
    expo=np.exp(1j*np.outer(s.xi,x))
    def ev(c,dx=0,yd=False):
        return (((dy if yd else interp)@c)*(1j*s.xi)**dx@expo).real
    max_r1=0.;max_r2=0.
    states=data['coefficients'];ts=data['times']
    for j in range(len(ts)-1):
        dt=ts[j+1]-ts[j];z0=states[j];z1=states[j+1]
        f0=s.rhs(ts[j],z0.ravel()).reshape(z0.shape)
        f1=s.rhs(ts[j+1],z1.ravel()).reshape(z0.shape)
        for q in [.25,.5,.75]:
            zz=(2*q**3-3*q*q+1)*z0+(q**3-2*q*q+q)*dt*f0+(-2*q**3+3*q*q)*z1+(q**3-q*q)*dt*f1
            zt=((6*q*q-6*q)*z0+(3*q*q-4*q+1)*dt*f0+(-6*q*q+6*q)*z1+(3*q*q-2*q)*dt*f1)/dt
            u,w=zz;ut,wt=zt
            u0=ev(u);ux=ev(u,1);uy=ev(u,yd=True)
            v=uy+ev(w);vx=ev(u,1,True)+ev(w,1)
            r1=ev(ut,yd=True)+uy*ux+(u0+4)*ev(u,1,True)+ev(u,2,True)+ev(w,2)
            r2=ev(ut,yd=True)+ev(wt)+ev(u,2,True)+ux*v+(u0+4)*vx-4*ux
            max_r1=max(max_r1,float(abs(r1).max()));max_r2=max(max_r2,float(abs(r2).max()))
    out['candidates'].append(dict(case=case,selected=name,
        independent_DOP853_difference_u_v=alt_diff,DOP853_rhs_calls=alt.nfev,
        sampled_full_physical_residuals=[max_r1,max_r2],
        residual_scope='Cubic-Hermite time interpolation; 30 time samples x 161 y x 768 x samples; exact polynomial derivatives; not an enclosure'))

(HERE/'validation.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
