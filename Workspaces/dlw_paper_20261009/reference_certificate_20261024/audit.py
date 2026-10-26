"""Reproducible feasibility audit, NOT a validated continuum error certificate.
Uses the frozen nonlinear FD implementation with its documented open-y closure.
No filtering, no new boundary conditions, no change to initial data.
"""
from pathlib import Path
import sys, json, time
import numpy as np
from scipy import fft as sfft

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'spatial_audit_20261023'
sys.path.insert(0, str(OLD))
from run import Model, step

def run(case, dx, dt, extended=False):
    tag = f'{case}_dx{dx:g}_dt{dt:g}' + ('_extended' if extended else '')
    out = HERE / (tag + '.json')
    if out.exists():
        print('cached', tag, flush=True)
        return
    m = Model(case, 'FD', dx=dx, h=.1)
    m.a = 2.
    if extended:
        # scipy.fft preserves longdouble; numpy.fft does not on all platforms.
        # This is a roundoff sensitivity experiment, not interval validation.
        if np.finfo(np.longdouble).eps >= np.finfo(float).eps:
            raise RuntimeError('extended precision is unavailable on this platform')
        pi = np.arccos(np.longdouble(-1))
        m.x = -np.longdouble(96) + np.arange(m.nx, dtype=np.longdouble)*(np.longdouble(192)/m.nx)
        m.y = -np.longdouble(2) + np.arange(41, dtype=np.longdouble)/10
        m.yv = m.y.copy()
        freq = 2*pi*np.arange(m.nx//2+1, dtype=np.longdouble)/192
        m.m1 = 1j*freq; m.m1[-1]=0
        m.m2 = -freq**2
        m.d1 = lambda f: sfft.irfft(sfft.rfft(f,axis=-1)*m.m1,n=m.nx,axis=-1)
        m.d2 = lambda f: sfft.irfft(sfft.rfft(f,axis=-1)*m.m2,n=m.nx,axis=-1)
        def profile(y,t=0.,x=None):
            xx=m.x if x is None else np.asarray(x,dtype=np.longdouble)
            e=np.sin(pi*(np.asarray(y,dtype=np.longdouble)+2)/4)[:,None]
            if case=='Gaussian':
                return np.array([np.longdouble('.05')*e*np.exp(-(xx/6)**2),np.longdouble('.03')*e*np.exp(-(xx/6)**2)])
            return np.array([np.longdouble('.03')*e*np.cos(2*pi*xx/24),np.longdouble('.02')*e*np.sin(2*pi*xx/24)])
        m.profile=profile
    z = m.initial()
    start = time.perf_counter()
    rec = dict(case=case, method='FD', dx=dx, h=.1, dt=dt, T=.01,
               a=2, norm='max over both fields and all native grid points',
               certified=False, precision='longdouble/scipy FFT' if extended else 'float64/numpy FFT',
               machine_epsilon=float(np.finfo(z.dtype).eps), diagnostics=[], residual_kind='sampled Hermite ODE defect; not an enclosure')
    max_residual = 0.
    # Cubic Hermite interpolation at each step; midpoint residual diagnoses
    # only time reconstruction on this grid, not continuous PDE truncation.
    for i in range(round(.01/dt)):
        t = i*dt
        with np.errstate(over='ignore', invalid='ignore'):
            f0 = m.rhs(t, z)
            zn = step(m, t, z, dt)
            if not np.isfinite(zn).all() or abs(zn).max() > 1e6:
                rec.update(status='threshold_stop', stopped_at=t+dt)
                break
            f1 = m.rhs(t+dt, zn)
            zm = (z+zn)/2 + dt*(f0-f1)/8
            dm = 1.5*(zn-z)/dt - (f0+f1)/4
            residual = float(abs(dm-m.rhs(t+dt/2, zm)).max())
        max_residual = max(max_residual, residual)
        z = zn
        if (i+1) % max(1, round(.001/dt)) == 0:
            spec = np.fft.rfft(z, axis=-1)/m.nx
            rec['diagnostics'].append(dict(t=t+dt,
                amplitude=[float(abs(z[j]).max()) for j in range(2)],
                high_frequency_l1=[float(2*abs(spec[j,:,int(.8*spec.shape[-1]):]).sum(axis=-1).max()) for j in range(2)]))
    else:
        rec.update(status='complete', amplitude=[float(abs(z[j]).max()) for j in range(2)])
        np.savez_compressed(HERE/(tag+'.npz'), z=z, x=m.x, y=m.y)
    rec.update(sampled_ode_residual_max=max_residual, seconds=time.perf_counter()-start)
    out.write_text(json.dumps(rec, indent=2), encoding='utf8')
    print(json.dumps({k:v for k,v in rec.items() if k!='diagnostics'}), flush=True)

if __name__ == '__main__':
    case = sys.argv[1]
    if len(sys.argv)>2 and sys.argv[2]=='extended':
        run(case,.05,5e-5,extended=True)
        sys.exit()
    for dx,dt in [(.1,1e-4),(.05,1e-4),(.05,5e-5),(.025,1e-4)]:
        run(case, dx, dt)
