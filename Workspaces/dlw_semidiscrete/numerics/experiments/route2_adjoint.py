"""Discrete RK4 adjoint attribution for a smooth soliton-position target.

The tangent is the exact derivative of the actual RK4 step, including its
time-dependent boundary data. This is a short-time discrete target analysis,
not an adjoint of a continuum PDE or moving mesh.
"""
from pathlib import Path
import sys, json, hashlib
import numpy as np
from scipy.optimize import minimize_scalar

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
from parametric import Parameters, rk4
from parametric_open import OpenModel

OUT=ROOT/'out/route2'
OUT.mkdir(parents=True,exist_ok=True)
CASES={'P1':Parameters(),'P6':Parameters(p=1,q=3,rho=4)}


def inf(a):return float(np.max(np.abs(a)))


def jac(m,t,z,eye):
    return np.column_stack([m.delta(t,z,eye[:,i],True) for i in range(len(z))])


def step_data(m,t,z,dt,eye):
    f1=m.rhs(t,z);y2=z+dt*f1/2
    f2=m.rhs(t+dt/2,y2);y3=z+dt*f2/2
    f3=m.rhs(t+dt/2,y3);y4=z+dt*f3
    f4=m.rhs(t+dt,y4)
    step=z+dt*(f1+2*f2+2*f3+f4)/6
    matrices=(jac(m,t,z,eye),jac(m,t+dt/2,y2,eye),
              jac(m,t+dt/2,y3,eye),jac(m,t+dt,y4,eye))
    return step,matrices


def tangent_action(A,v,dt):
    A1,A2,A3,A4=A
    k1=A1@v
    k2=A2@(v+dt*k1/2)
    k3=A3@(v+dt*k2/2)
    k4=A4@(v+dt*k3)
    return v+dt*(k1+2*k2+2*k3+k4)/6


def adjoint_action(A,w,dt):
    A1,A2,A3,A4=A
    e=w.copy()
    b1=dt*w/6;b2=dt*w/3;b3=dt*w/3;b4=dt*w/6
    t4=A4.T@b4;e=e+t4;b3=b3+dt*t4
    t3=A3.T@b3;e=e+t3;b2=b2+dt*t3/2
    t2=A2.T@b2;e=e+t2;b1=b1+dt*t2/2
    return e+A1.T@b1


def position_target(m,T):
    j=int(np.argmin(abs(m.y)))
    site=int(m.js[j]);x=m.X.x
    ref=m.G.uv([site],x,T)[0][0]
    eps=1e-5
    ux=(m.G.uv([site],x+eps,T)[0][0]-m.G.uv([site],x-eps,T)[0][0])/(2*eps)
    curvature=float(ux@ux)
    if curvature<1e-8:raise RuntimeError('position fit is ill-conditioned')
    def proxy(e):
        eu=m.error_fields(e)[0][j]
        return float(-(eu@ux)/curvature)
    eye=np.eye(m.exact(0).size)
    grad=np.array([proxy(eye[:,i]) for i in range(len(eye))])
    def fit(z):
        u=m.fields(z,T)[0][j]
        opt=minimize_scalar(lambda s:float(np.sum((u-m.G.uv([site],x-s,T)[0][0])**2)),
                            bounds=(-.5,.5),method='bounded',options={'xatol':1e-11})
        return {'shift':float(opt.x),'rms_shape_after_shift':float(np.sqrt(opt.fun/len(x))),
                'fit_interior':bool(abs(opt.x)<.49)}
    return grad,proxy,fit,{'j':site,'y':float(m.y[j]),'curvature':curvature}


def run(case,model='structure',nx=32,h=.5,yhalf=.75,T=.01,dt=.0005):
    pars=CASES[case]
    m=OpenModel(pars,h,nx,yhalf=yhalf,model=model,continuous=True)
    zraw=m.exact(0);e_lin=np.zeros_like(zraw)
    steps=round(T/dt);assert abs(steps*dt-T)<1e-12
    eye=np.eye(zraw.size)
    records=[]
    for n in range(steps):
        t=n*dt;zbar=m.exact(t);zbar_next=m.exact(t+dt)
        step,A=step_data(m,t,zbar,dt,eye)
        b=step-zbar_next
        quadrature=(zbar+dt*(m.exact(t,True)+4*m.exact(t+dt/2,True)
                             +m.exact(t+dt,True))/6-zbar_next)
        spatial=b-quadrature
        e_before=zraw-zbar
        zraw_next=rk4(m.rhs,t,zraw,dt)
        nonlinear=zraw_next-zbar_next-tangent_action(A,e_before,dt)-b
        e_lin=tangent_action(A,e_lin,dt)+b
        records.append({'t':t,'A':A,'b':b,'spatial':spatial,'quadrature':quadrature,
                        'nonlinear':nonlinear,'r0':m.rhs(t,zbar)-m.exact(t,True),
                        'actual_error_before':e_before})
        zraw=zraw_next
        if not np.all(np.isfinite(zraw)) or inf(zraw)>1e3:
            raise RuntimeError(f'{case} raw RK4 stopped at {t}')
    zbarT=m.exact(T);e_actual=zraw-zbarT
    grad,proxy,fit,goal=position_target(m,T)
    # Independent transpose test on a deterministic vector, before attribution.
    rng=np.random.default_rng(20260923)
    v=rng.normal(size=len(grad));w=rng.normal(size=len(grad))
    trans_err=abs(w@tangent_action(records[0]['A'],v,dt)
                  -adjoint_action(records[0]['A'],w,dt)@v)
    assert trans_err<1e-10,trans_err
    # Independent finite-difference check of the full RK4 tangent, including
    # the time-dependent boundary. The direction is scaled to a physical size.
    v/=max(np.max(abs(v)),1.)
    z0=m.exact(0)
    fd_eps=1e-5
    fd_step=(rk4(m.rhs,0,z0+fd_eps*v,dt)-rk4(m.rhs,0,z0-fd_eps*v,dt))/(2*fd_eps)
    tangent_residual=inf(fd_step-tangent_action(records[0]['A'],v,dt))
    assert tangent_residual<2e-8,tangent_residual
    adj=grad.copy();totals={k:0. for k in ('spatial','quadrature','nonlinear')}
    absolute={k:0. for k in totals};by_time=[]
    spatial_cells=np.zeros_like(adj)
    boundary_abs=0.
    for r in reversed(records):
        contributions={k:float(adj@r[k]) for k in totals}
        for k in totals:
            totals[k]+=contributions[k]
            absolute[k]+=float(np.sum(abs(adj*r[k])))
        spatial_cells+=adj*r['spatial']
        p_cells,q_cells=m.unpack(adj*r['spatial'])
        boundary_abs+=float(np.sum(abs(p_cells[-1]))+np.sum(abs(q_cells[-1])))
        by_time.append({'t':r['t'],'defect_inf':inf(r['r0']),
                        'spatial_goal_signed':contributions['spatial'],
                        'spatial_goal_absolute_cells':float(np.sum(abs(adj*r['spatial'])))})
        adj=adjoint_action(r['A'],adj,dt)
    by_time.reverse()
    predicted=totals['spatial']+totals['quadrature']
    reconstructed=predicted+totals['nonlinear']
    assert abs(predicted-proxy(e_lin))<5e-11
    assert abs(reconstructed-proxy(e_actual))<5e-11
    P,Q=m.unpack(spatial_cells)
    denom=max(absolute['spatial'],1e-30)
    last_y_share=boundary_abs/denom
    top=np.argsort(abs(spatial_cells))[-8:][::-1]
    cells=[]
    for ix in top:
        if ix<m.np:
            row,col=np.unravel_index(ix,(len(m.js)-1,nx));kind='P';yy=float((m.js[row]+1)*h)
        else:
            row,col=np.unravel_index(ix-m.np,(len(m.js),nx));kind='Q';yy=float(m.y[row])
        cells.append({'kind':kind,'y':yy,'x':float(m.X.x[col]),'signed_contribution':float(spatial_cells[ix])})
    fit_actual=fit(zraw)
    synthetic=fit(m.exact(T)+.001*grad/max(np.linalg.norm(grad),1e-30))
    return {'case':case,'config':{'model':model,'h':h,'nx':nx,'yhalf':yhalf,'T':T,'dt':dt},
            'goal':goal,'target':{'linear_proxy_actual':proxy(e_actual),
                                 'linear_proxy_predicted':proxy(e_lin),
                                 'profile_fit_actual':fit_actual,
                                 'synthetic_gradient_direction_fit':synthetic},
            'adjoint_signed':totals,'adjoint_cellwise_absolute':absolute,
            'goal_reconstruction_residual':abs(reconstructed-proxy(e_actual)),
            'adjoint_transpose_residual':trans_err,
            'rk4_tangent_fd_residual':tangent_residual,
            'linear_prediction_difference':abs(predicted-proxy(e_actual)),
            'linear_absolute_bound':absolute['spatial']+absolute['quadrature'],
            'a_posteriori_nonlinear_bound':sum(absolute.values()),
            'spatial_boundary_last_y_absolute_share':last_y_share,
            'top_spatial_cells':cells,'by_time':by_time}


def main():
    rows=[]
    for case,model,dt in (('P1','structure',.0005),('P6','structure',.0005),
                          ('P6','fd',.0005),('P6','structure',.00025)):
        row=run(case,model=model,dt=dt)
        rows.append(row)
        print(case,model,dt,'fit',row['target']['profile_fit_actual'],
              'predicted',row['target']['linear_proxy_predicted'],
              'signed',row['adjoint_signed'],flush=True)
    paths=[Path(__file__),ROOT/'lib/parametric.py',ROOT/'lib/parametric_open.py']
    data={'scope':'fixed-grid discrete RK4 phase adjoint; open extrapolated boundary',
          'results':rows,'sources_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    (OUT/'adjoint.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('wrote route2/adjoint.json',flush=True)


if __name__=='__main__':main()
