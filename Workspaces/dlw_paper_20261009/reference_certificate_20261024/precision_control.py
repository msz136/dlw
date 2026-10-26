"""Independent float64 controls for arbitrary-precision implementation."""
from pathlib import Path
import sys,json,numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'spatial_audit_20261023'))
from run import Model,step

def advance(m):
    z=m.initial()
    for i in range(100): z=step(m,i*1e-4,z,1e-4)
    return z

m=Model('Sinusoidal','FD',.05,.1);m.a=2
m.nx=480;m.x=np.arange(480)*.05
m.freq=2*np.pi*np.fft.rfftfreq(m.nx,.05)
m.m1=1j*m.freq;m.m1[-1]=0;m.m2=-m.freq**2
z=advance(m)
ref=np.load(HERE/'Sinusoidal_precision80_dx0.05_dt0.0001.npz')['z']
r=dict(case='Sinusoidal',domain=[0,24],dx=.05,h=.1,dt=.0001,T=.01,
       precision='float64',amplitude=[float(abs(v).max()) for v in z],
       difference_to_80digit=[float(abs(z[j]-ref[j]).max()) for j in range(2)],certified=False)
(HERE/'fundamental_float64_control.json').write_text(json.dumps(r,indent=2),encoding='utf8')
coarse=Model('Sinusoidal','FD',.5,.1);coarse.a=2
zc=advance(coarse)
rc=np.load(HERE/'Sinusoidal_precision30_dx0.5_dt0.0001.npz')['z']
err=float(abs(zc-np.tile(rc,(1,1,8))).max())
assert err<1e-13
(HERE/'implementation_control.json').write_text(json.dumps(dict(coarse_full_domain_vs_precision30=err,passed=True),indent=2))
print(r);print('coarse implementation control',err)
