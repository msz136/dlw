"""Four spatial methods on nondegenerate Gaussian/sinusoidal continuous data.

Common RK4 parameters h=dx=.1, dt=1e-4, T=.01.  The initial relation
v=4-3*u_y is not imposed during either numerical or reference evolution.
"""
from pathlib import Path
import hashlib
import json
import sys
import time
import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ROOT = PROJECT.parents[1]
PROBE = PROJECT / 'spatial_audit_20261023/separated/reconstruction_probe'
sys.path.insert(0, str(PROBE))
from rerun_20261024 import rhs as centered_rhs, physical_rates
from probe import Model, transform
sys.path.insert(0, str(HERE.parent))
from initial_non_soliton import invert
sys.path.insert(0, str(HERE))

METHODS = ('Endpoint-SD', 'CSD0', 'Centered-SD', 'FD')
DX, H, DT, T = .1, .1, 1e-4, .01
BOUNDARIES = {}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sources():
    paths = [Path(__file__), HERE/'reference_grid.py', HERE.parent/'initial_non_soliton.py',
             PROBE/'rerun_20261024.py', PROBE/'probe.py',
             PROJECT/'spatial_audit_20261023/run.py',
             PROJECT/'spatial_audit_20261023/separated/run_separated.py']
    return [dict(path=p.relative_to(ROOT).as_posix(), sha256=sha(p)) for p in paths]


def initial_data(case, x, y):
    """Analytic initial jets and the original continuous DLW time derivatives."""
    x = np.asarray(x); y = np.asarray(y)
    kappa = np.pi/4
    e = np.sin(kappa*(y+2))[:, None]
    ey = (kappa*np.cos(kappa*(y+2)))[:, None]
    if case == 'Gaussian':
        a = .05
        shifts = x[None, :]+192*np.arange(-1, 2)[:, None]
        gg = np.exp(-(shifts/6)**2)
        f = np.sum(gg, axis=0)
        fx = np.sum(-shifts/18*gg, axis=0)
        fxx = np.sum((shifts*shifts/324-1/18)*gg, axis=0)
    else:
        a = .03; k = np.pi/12
        f = np.cos(k*x); fx = -k*np.sin(k*x); fxx = -k*k*f
    u, ux, uxx = a*e*f, a*e*fx, a*e*fxx
    uy, uxy, uxxy = a*ey*f, a*ey*fx, a*ey*fxx
    v = 4-3*uy
    ut = 3*uxx-(u+4)*ux
    vt = -uxxy+3*(ux*uy+(u+4)*uxy)
    return dict(u=u,v=v,ux=ux,uy=uy,uxx=uxx,uxy=uxy,uxxy=uxxy,ut=ut,vt=vt)


def ref_case(case):
    return 'gaussian' if case == 'Gaussian' else 'sine'


class NondegenerateModel(Model):
    def __init__(self, case, method):
        super().__init__(case, 'Centered-SD' if method == 'CSD0' else method, DX, H)
        self.label = method
        self.a = 2.
        self.gauge = 'mean'

    def profile(self, y, t=0., x=None):
        x = self.x if x is None else x
        if t == 0.:
            dat = initial_data(self.case, x, y)
            return np.array([dat['u'], dat['v']])
        from reference_grid import exact
        return np.array(exact(ref_case(self.case), x, y, t))

    def ut(self, y, t):
        if t == 0.:
            return initial_data(self.case, self.x, y)['ut']
        from reference_grid import rates
        return rates(ref_case(self.case), self.x, y, t)[0]

    def boundary(self, t):
        # RK4 stages lie on the common half-step grid. Share the exact boundary
        # values across the four methods without any state-dependent shortcut.
        tick = int(round(t/(DT/2)))
        assert abs(t-tick*(DT/2)) < 1e-15
        key = self.case, tick
        if key not in BOUNDARIES:
            yy = np.r_[self.y[0]-self.h,self.y[0],self.y[-3:],self.y[-1]+self.h]
            tt = tick*(DT/2)
            BOUNDARIES[key] = (self.profile(yy,tt)[0],self.ut(yy,tt))
        return BOUNDARIES[key]


def measured(m, defect, y):
    y = np.asarray(y)
    mask = abs(y) <= 1.8+1e-12
    values = abs(defect[mask])
    row, col = np.unravel_index(np.argmax(values), values.shape)
    return float(values[row, col]), [float(m.x[col]), float(y[mask][row])]


def errors(m, u, v, yv, t):
    uref = m.profile(m.y, t)[0]
    vref = m.profile(yv, t)[1]
    eu, pu = measured(m, u-uref, m.y)
    ev, pv = measured(m, v-vref, yv)
    return [eu, ev], pu, pv, uref, vref


def rk4(fun, t, z):
    k1 = fun(t, z)
    k2 = fun(t+DT/2, z+DT*k1/2)
    k3 = fun(t+DT/2, z+DT*k2/2)
    k4 = fun(t+DT, z+DT*k3)
    return z+DT*(k1+2*k2+2*k3+k4)/6


def setup(case, method):
    m = NondegenerateModel(case, method)
    u0 = m.profile(m.y,0.)[0]
    checks = {}
    if method == 'Centered-SD':
        yv = (m.y[1:]+m.y[:-1])/2
        v0 = m.profile(yv,0.)[1]
        bd = initial_data(case,m.x,m.y[:1])
        w0 = (bd['v']-bd['uy'])[0]
        w,it,res = invert(m,u0,v0,w0)
        z0 = np.array([u0,w]); fun = lambda t,z: centered_rhs(m,t,z)
        dz = fun(0.,z0); ut,vt = physical_rates(m,z0,dz)
        reconstructed = transform(m,*z0)
        expected = -np.diff(m.d1(u0*u0/2+4*u0),axis=0)/H-m.d2(v0)
        eps=1e-6
        push=(transform(m,*(z0+eps*dz))-transform(m,*(z0-eps*dz)))/(2*eps)
        checks.update(inverse_iterations=it,inverse_residual=res,
                      map_residual=float(np.max(abs(reconstructed-v0))),
                      first_equation_identity=float(np.max(abs(np.diff(ut,axis=0)/H-expected))),
                      chain_rule_difference=float(np.max(abs(push-vt))))
        assert checks['map_residual']<1e-10,checks
        assert checks['first_equation_identity']<1e-7,checks
        assert checks['chain_rule_difference']<1e-7,checks
        v0=reconstructed
        state='u,w; physical v from current full-potential edge map'
        closure='Exact continuous lower u_t; all w nodes evolved by their equation; no upper y ghost.'
    else:
        yv=m.yv;v0=m.profile(yv,0.)[1];z0=np.array([u0,v0]);fun=m.rhs
        ut,vt=fun(0.,z0)
        state='u,v; both physical fields evolved directly'
        closure=('Exact continuous lower u_t and lower ghost u; backward/open chain; no upper y ghost.'
                 if method=='Endpoint-SD' else
                 'Exact continuous lower u_t and lower ghost u; upper ghost uses exact continuous background plus quadratic perturbation extrapolation; its time derivative uses the same closure.')
    checks['initial_lower_ut_difference']=float(np.max(abs(ut[0]-m.ut(m.y[:1],0.)[0])))
    initial_error,_,_,u0ref,v0ref=errors(m,u0,v0,yv,0.)
    checks['initial_physical_error']=initial_error
    assert max(initial_error)<1e-9,checks
    utref=initial_data(case,m.x,m.y)['ut'];vtref=initial_data(case,m.x,yv)['vt']
    eut,put=measured(m,ut-utref,m.y);evt,pvt=measured(m,vt-vtref,yv)
    ini=dict(case=case,method=method,dx=m.dx,h=H,t=0.,a=2.,total=[eut,evt],
             argmax_ut=put,argmax_vt=pvt,checks=checks,
             region='all periodic x nodes in [-96,96); native field sites |y|<=1.8',
             reference='analytic nondegenerate continuous initial time derivatives',status='complete')
    np.savez_compressed(HERE/f'initial_{case}_{method}.npz',x=m.x,y=m.y,yv=yv,z0=z0,u0=u0,v0=v0,
                        u0_ref=u0ref,v0_ref=v0ref,ut=ut,vt=vt,ut_ref=utref,vt_ref=vtref)
    (HERE/f'initial_{case}_{method}.json').write_text(json.dumps(ini,indent=2),encoding='utf8')
    print(json.dumps(dict(case=case,method=method,initial_error=ini['total'],checks=checks)),flush=True)
    return m,z0,fun,yv,u0,v0,u0ref,v0ref,initial_error,state,closure,checks


def compute(case, method, initial_only=False):
    dest=HERE/f'{case}_{method}_RK4.json'
    if dest.exists() and not initial_only:
        print('Existing record retained: '+dest.name,flush=True);return
    started=time.perf_counter()
    m,z0,fun,yv,u0,v0,u0ref,v0ref,initial_error,state,closure,checks=setup(case,method)
    if initial_only:return
    z=z0.copy();reached=0.;status='complete';evolution_started=time.perf_counter()
    with np.errstate(over='raise',invalid='raise',divide='raise'):
        try:
            for i in range(round(T/DT)):
                new=rk4(fun,i*DT,z)
                if not np.isfinite(new).all() or np.max(abs(new))>1e6:
                    raise RuntimeError('nonfinite_or_amplitude_threshold')
                z=new;reached=(i+1)*DT
                if (i+1)%25==0:print(json.dumps(dict(case=case,method=method,step=i+1)),flush=True)
        except (FloatingPointError,RuntimeError) as exc:
            status='failed: '+str(exc)
    evolution_seconds=time.perf_counter()-evolution_started
    u=z[0];v=transform(m,*z) if method=='Centered-SD' else z[1]
    err,pu,pv,uref,vref=errors(m,u,v,yv,reached)
    state_path=dest.with_suffix('.npz')
    np.savez_compressed(state_path,x=m.x,y=m.y,yv=yv,z=z,z0=z0,u=u,v=v,u0=u0,v0=v0,
                        u_ref=uref,v_ref=vref,u0_ref=u0ref,v0_ref=v0ref,reached=reached)
    record=dict(case=case,method=method,integrator='RK4',h=H,dx=m.dx,dt=DT,T=T,reached=reached,
                status=status,error=err,argmax_u=pu,argmax_v=pv,state=state,nx=m.nx,ny=len(m.y),a=m.a,
                computational_x_interval=[-96,96],computational_y_interval=[-2,2],evaluation_y_interval=[-1.8,1.8],
                initial_error=initial_error,metric='Absolute sampled maximum at native field positions.',
                reference='Nondegenerate continuous two-heat/Laplace-transform reference; v=4-3*u_y only initially.',
                spatial_x='Fourier differentiation; first-derivative Nyquist zero; no filtering or dealiasing.',
                boundary=closure,checks=checks,evolution_seconds=evolution_seconds,
                processing_seconds=time.perf_counter()-started,artifact=state_path.relative_to(ROOT).as_posix(),
                artifact_sha256=sha(state_path),sources=sources())
    dest.write_text(json.dumps(record,indent=2),encoding='utf8')
    print(json.dumps({k:record[k] for k in ('case','method','status','reached','error','evolution_seconds')}),flush=True)


def collect():
    rows=[];initial_rows=[];audit=[]
    for case in ('Gaussian','Sinusoidal'):
        for method in METHODS:
            path=HERE/f'{case}_{method}_RK4.json'
            row=json.loads(path.read_text(encoding='utf8'))
            ini=json.loads((HERE/f'initial_{case}_{method}.json').read_text(encoding='utf8'))
            data=np.load(path.with_suffix('.npz'));initial=np.load(HERE/f'initial_{case}_{method}.npz')
            m=NondegenerateModel(case,method)
            mapped=transform(m,*data['z']) if method=='Centered-SD' else data['z'][1]
            md=float(np.max(abs(mapped-data['v'])))
            err,_,_,ur,vr=errors(m,data['u'],data['v'],data['yv'],row['reached'])
            ed=max(abs(a-b) for a,b in zip(err,row['error']))
            rd=max(float(np.max(abs(ur-data['u_ref']))),float(np.max(abs(vr-data['v_ref']))))
            e0=[measured(m,initial['ut']-initial_data(case,m.x,m.y)['ut'],m.y)[0],
                measured(m,initial['vt']-initial_data(case,m.x,data['yv'])['vt'],data['yv'])[0]]
            idiff=max(abs(a-b) for a,b in zip(e0,ini['total']))
            assert max(md,ed,rd,idiff)<1e-13
            assert sha(path.with_suffix('.npz'))==row['artifact_sha256']
            audit.append(dict(case=case,method=method,recomputed_error=err,record_difference=ed,
                              initial_record_difference=idiff,stored_reference_difference=rd,
                              stored_physical_map_difference=md,checks=row['checks']))
            rows.append(row);initial_rows.append(ini)
    (HERE/'results.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
    (HERE/'initial_results.json').write_text(json.dumps(initial_rows,indent=2),encoding='utf8')
    validation=dict(records=len(rows),complete=sum(r['status']=='complete' for r in rows),
                    max_record_difference=max(r['record_difference'] for r in audit),
                    max_initial_record_difference=max(r['initial_record_difference'] for r in audit),audit=audit)
    (HERE/'validation.json').write_text(json.dumps(validation,indent=2),encoding='utf8')
    print(json.dumps({k:validation[k] for k in ('records','complete','max_record_difference','max_initial_record_difference')}),flush=True)


if __name__=='__main__':
    if sys.argv[1]=='collect':collect()
    elif sys.argv[1]=='initial':
        for case in ('Gaussian','Sinusoidal'):
            for method in METHODS:compute(case,method,True)
    else:
        for method in ([sys.argv[2]] if len(sys.argv)>2 else METHODS):compute(sys.argv[1],method)
