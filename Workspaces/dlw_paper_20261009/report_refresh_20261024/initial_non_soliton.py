"""Initial physical-rate defects, with explicit analytic continuum references.

No positive-time continuous solution is assumed or approximated.  The current
full-potential Centered-SD is imported from the existing experiment code.
"""
from pathlib import Path
import sys, json, time
import numpy as np

HERE = Path(__file__).resolve().parent
PROBE = HERE.parent / 'spatial_audit_20261023/separated/reconstruction_probe'
sys.path.insert(0, str(PROBE))
from rerun_20261024 import rhs as centered_rhs, physical_rates
from probe import Model, transform, primitive, A


def invert(m,u,V,w0):
    """Same inverse iteration as probe.invert, with a larger iteration cap.

    The period-192 primitive requires more than the soliton code's 200 steps.
    Mapping, initial iterate, damping, branch and residual tolerance are unchanged.
    """
    w=np.empty_like(u);w[0]=w0;maxit=0;maxres=0
    for k in range(1,len(u)):
        rhs=2*(V[k-1]-(u[k]-u[k-1])/m.h)-w[k-1]+2*m.h*primitive(m,A(w[k-1]))
        cand=w[k-1].copy()
        for it in range(1000):
            nxt=rhs-2*m.h*primitive(m,A(cand))
            res=float(np.max(abs(nxt-cand)))
            if res<2e-12:break
            cand=.5*cand+.5*nxt
            if not np.isfinite(cand).all() or np.max(abs(cand))>1e5:raise ValueError('inverse diverged')
        else:raise ValueError(f'inverse did not converge at row {k}, residual {res}')
        w[k]=cand;maxit=max(maxit,it+1);maxres=max(maxres,res)
    return w,maxit,maxres


def xjets(case, x):
    if case == 'Gaussian':
        s = x[None, :] + 192*np.arange(-1, 2)[:, None]
        g = np.exp(-(s/6)**2)
        f = np.sum(g, axis=0)
        fx = np.sum(-s/18*g, axis=0)
        fxx = np.sum((s*s/324-1/18)*g, axis=0)
        return .05*f, .05*fx, .05*fxx, .03*f, .03*fx, .03*fxx
    k = np.pi/12
    c, s = np.cos(k*x), np.sin(k*x)
    return .03*c, -.03*k*s, -.03*k*k*c, .02*s, .02*k*c, -.02*k*k*s


def exact_data(case, x, y):
    p, px, pxx, q, qx, qxx = xjets(case, x)
    angle = np.pi*(np.asarray(y)+2)/4
    e = np.sin(angle)[:, None]
    ey = (np.pi/4*np.cos(angle))[:, None]
    E = (4/np.pi*(1-np.cos(angle)))[:, None]
    u, v, ux, uy = e*p, e*q, e*px, ey*p
    ut = -E*qxx-(u+4)*ux
    vt = -ey*pxx-ux*v-(u+4)*e*qx+4*ux
    return dict(u=u, v=v, uy=uy, ut=ut, vt=vt)


class InitialModel(Model):
    def __init__(self, case, method, dx=.1, h=.1):
        super().__init__(case, method, dx, h)
        self.a = 2.
        self.gauge = 'mean'

    def profile(self, y, t=0., x=None):
        assert t == 0, 'Only initial data are defined here.'
        dat = exact_data(self.case, self.x if x is None else x, y)
        return np.array([dat['u'], dat['v']])

    def ut(self, y, t):
        assert t == 0
        return exact_data(self.case, self.x, y)['ut']


def measured(m, defect, yy):
    mask = abs(yy) <= 1.8+1e-12
    a = abs(defect[mask])
    index = np.unravel_index(np.argmax(a), a.shape)
    return float(a[index]), [float(m.x[index[1]]), float(yy[mask][index[0]])]


def compute(case, method):
    m = InitialModel(case, method)
    u = m.profile(m.y)[0]
    checks = {}
    if method == 'Centered-SD':
        yv = (m.y[1:]+m.y[:-1])/2
        v = m.profile(yv)[1]
        bd = exact_data(case, m.x, m.y[:1])
        w0 = (bd['v']-bd['uy'])[0]
        w, it, res = invert(m, u, v, w0)
        z = np.array([u, w])
        dz = centered_rhs(m, 0., z)
        ut, vt = physical_rates(m, z, dz)
        reconstructed = transform(m, *z)
        expected = -np.diff(m.d1(u*u/2+4*u), axis=0)/m.h-m.d2(v)
        eps=1e-6
        fd=(transform(m, *(z+eps*dz))-transform(m, *(z-eps*dz)))/(2*eps)
        checks = dict(inverse_iterations=it, inverse_residual=res,
                      map_residual=float(np.max(abs(reconstructed-v))),
                      first_equation_identity=float(np.max(abs(np.diff(ut, axis=0)/m.h-expected))),
                      chain_rule_difference=float(np.max(abs(fd-vt))))
        assert checks['map_residual'] < 1e-10
        assert checks['first_equation_identity'] < 1e-7
        assert checks['chain_rule_difference'] < 1e-7
    else:
        yv = m.yv
        v = m.profile(yv)[1]
        ut, vt = m.rhs(0., np.array([u, v]))
    eu, at_u = measured(m, ut-exact_data(case, m.x, m.y)['ut'], m.y)
    ev, at_v = measured(m, vt-exact_data(case, m.x, yv)['vt'], yv)
    row = dict(case=case, method=method, dx=m.dx, h=m.h, t=0., a=2.,
               total=[eu, ev], argmax_ut=at_u, argmax_vt=at_v, checks=checks,
               region='all periodic x grid nodes in [-96,96); field sites |y|<=1.8',
               reference='analytic continuous initial time derivatives',
               status='complete')
    np.savez_compressed(HERE/f'initial_{case}_{method}.npz', x=m.x, y=m.y, yv=yv,
                        ut=ut, vt=vt, ut_ref=exact_data(case,m.x,m.y)['ut'],
                        vt_ref=exact_data(case,m.x,yv)['vt'])
    print(json.dumps(row), flush=True)
    return row


def certify_references():
    """Arb validates every floating-point analytic reference actually used.

    Coordinates are their exact binary64 values, i.e. the solver's sample sites.
    Gaussian omitted m tails are bounded uniformly, including derivatives.
    This does not enclose the FFT implementation or nonlinear inverse.
    """
    from flint import arb, ctx
    ctx.dps=80
    pi=arb.pi(); one=arb(1)
    d=arb(288); ratio=arb(25)/9*(-arb(4096)).exp()
    tail0=2*(-arb(2304)).exp()/(1-ratio)
    tail1=2*(d/18)*(-arb(2304)).exp()/(1-ratio)
    tail2=2*(d*d/324+one/18)*(-arb(2304)).exp()/(1-ratio)
    total_rate_tail=100*(tail0+tail1+tail2)
    assert total_rate_tail < arb('1e-990')
    result=[]
    for case in ['Gaussian','Sinusoidal']:
        files=[np.load(HERE/f'initial_{case}_{meth}.npz') for meth in ['Endpoint-SD','Centered-SD','FD']]
        xx=files[0]['x']
        # Include every unique reference sample, including those outside measured region.
        yy=np.unique(np.concatenate([a[k] for a in files for k in ['y','yv']]))
        xr=[]
        for xd in xx:
            x=arb(float(xd))
            if case=='Gaussian':
                terms=[x+192*m for m in [-1,0,1]]
                gg=[(-(s/6)**2).exp() for s in terms]
                f=sum(gg);fx=sum(-s/18*g for s,g in zip(terms,gg))
                fxx=sum((s*s/324-one/18)*g for s,g in zip(terms,gg))
                xr.append((arb('.05')*f,arb('.05')*fx,arb('.05')*fxx,arb('.03')*f,arb('.03')*fx,arb('.03')*fxx))
            else:
                k=pi/12;c=(k*x).cos();s=(k*x).sin()
                xr.append((arb('.03')*c,-arb('.03')*k*s,-arb('.03')*k*k*c,arb('.02')*s,arb('.02')*k*c,-arb('.02')*k*k*s))
        numerical=exact_data(case,xx,yy)
        upper=[arb(0),arb(0)]
        for j,yd in enumerate(yy):
            y=arb(float(yd));angle=pi*(y+2)/4
            e=angle.sin();ey=pi/4*angle.cos();E=4/pi*(1-angle.cos())
            for i,(p,px,pxx,q,qx,qxx) in enumerate(xr):
                ut=-E*qxx-(e*p+4)*e*px
                vt=-ey*pxx-e*px*e*q-(e*p+4)*e*qx+4*e*px
                for n,(val,key) in enumerate([(ut,'ut'),(vt,'vt')]):
                    err=abs(val-arb(float(numerical[key][j,i])))
                    if case=='Gaussian':err+=total_rate_tail
                    assert err < arb('1e-14')
                    if err.upper()>upper[n]:upper[n]=err.upper()
        # This explicitly verified simple bound is what the report may quote.
        assert all(v<arb('1e-14') for v in upper)
        result.append(dict(case=case, nx=len(xx), distinct_y_sites=len(yy),
                           sampled_rates_checked=2*len(xx)*len(yy),
                           arb_precision_digits=80,
                           observed_outward_upper_strings=[v.str(12) for v in upper],
                           rigorous_uniform_sample_bound_ut='1e-14',
                           rigorous_uniform_sample_bound_vt='1e-14',
                           gaussian_omitted_rate_tail_bound='1e-990' if case=='Gaussian' else '0',
                           scope='analytic reference evaluation at every tabulated grid sample; not discrete solver roundoff'))
        print(json.dumps(result[-1]),flush=True)
    return result


if __name__=='__main__':
    start=time.perf_counter()
    rows=[compute(case,method) for case in ['Gaussian','Sinusoidal']
          for method in ['Endpoint-SD','Centered-SD','FD']]
    (HERE/'initial_nonsoliton.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
    cert=certify_references()
    (HERE/'initial_non_soliton_reference_certificate.json').write_text(json.dumps(cert,indent=2),encoding='utf8')
    print('seconds',time.perf_counter()-start,flush=True)
