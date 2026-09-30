"""Route 3: phase-tangent/normal defects and local N=2/N=3 dynamics.

Each time window starts afresh from the exact finite-h Gram state. Windows are
never concatenated or presented as a completed numerical collision.
"""
from pathlib import Path
import sys, json, hashlib, time
from fractions import Fraction
import numpy as np
from scipy.optimize import least_squares

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
from gramtau import GramRef
from parametric import Parameters, rk4
from parametric_open import OpenModel
from soliton_expansion import SolitonExpansion


class ManifoldModel(OpenModel):
    def __init__(self,p,q,rho,h=.25,nx=256,model='structure',L=20.,yhalf=1.5):
        super().__init__(Parameters(a=4.,p=p[0],q=q[0],rho=rho[0]),
                         h,nx,L=L,yhalf=yhalf,model=model)
        self.G=SolitonExpansion(p,q,rho,a=4.,h=h)


def inf(a):return float(np.max(np.abs(a)))


def scales(s,h=.25,nx=256):
    m=ManifoldModel(s.p,s.q,s.rho,h,nx)
    u,v=s.uv(m.js,m.X.x,0.)
    return (inf(u),inf(v))


def weight(m,uv,amps):
    c=np.sqrt(m.h*m.X.dx)
    return np.concatenate((c*np.asarray(uv[0]).ravel()/amps[0],
                           c*np.asarray(uv[1]).ravel()/amps[1]))


def projection(m,field,t,amps,mask=None):
    tangent=m.G.theta(m.js,m.X.x,t)
    def selected(pair):
        vec=weight(m,pair,amps)
        return vec if mask is None else vec[np.tile(mask.ravel(),2)]
    B=np.column_stack([selected((tangent[0][i],tangent[1][i]))
                       for i in range(m.G.n)])
    v=selected(field)
    lengths=np.linalg.norm(B,axis=0)
    if np.min(lengths)<1e-12:
        return {'identifiable':False,'reason':'vanishing tangent column'}
    normalized=B/lengths
    singular=np.linalg.svd(normalized,compute_uv=False)
    condition=float(singular[0]/singular[-1])
    if not np.isfinite(condition) or condition>1e6:
        return {'identifiable':False,'condition':condition,
                'reason':'phase tangent columns nearly dependent'}
    coeff_scaled=np.linalg.lstsq(normalized,v,rcond=1e-12)[0]
    parallel=normalized@coeff_scaled
    normal=v-parallel
    norm=float(np.linalg.norm(v))
    return {'identifiable':True,'condition':condition,
            'singular_values':singular.tolist(),
            'phase_rate_or_shift':(coeff_scaled/lengths).tolist(),
            'total_weighted_l2':norm,'tangent_weighted_l2':float(np.linalg.norm(parallel)),
            'normal_weighted_l2':float(np.linalg.norm(normal)),
            'normal_fraction':float(np.linalg.norm(normal)/max(norm,1e-30)),
            'orthogonality_inf':inf(normalized.T@normal)}


def defect(m,t,amps):
    z=m.exact(t)
    residual=m.rhs(t,z)-m.exact(t,True)
    du,dv=m.error_fields(residual)
    result=projection(m,(du,dv),t,amps)
    # Recompute the projection away from the x and open-chain boundaries.
    # This is a sensitivity check, not a replacement for the full-domain norm.
    core=(np.abs(m.y[:,None])<=1.0)&(np.abs(m.X.x[None,:])<=8.0)
    result['core_projection']=projection(m,(du,dv),t,amps,core)
    result['core_points']=int(np.sum(core))
    result.update({'u_inf':inf(du),'v_inf':inf(dv),'state_inf':inf(residual)})
    return result


def burst(m,t0,amps,T=.005,dt=.00005):
    z=m.exact(t0)
    n=round(T/dt)
    stopped=None
    for k in range(n):
        t=t0+k*dt
        with np.errstate(over='ignore',invalid='ignore'):
            z=rk4(m.rhs,t,z,dt)
        if not np.all(np.isfinite(z)) or inf(z)>1e3:
            stopped={'t':t+dt,'reason':'nonfinite or state magnitude >1000'}
            break
    t1=t0+T if stopped is None else stopped['t']
    if stopped is not None:return {'complete':False,'stopped':stopped}
    num=m.fields(z,t1);exact=m.G.uv(m.js,m.X.x,t1)
    err=(num[0]-exact[0],num[1]-exact[1])
    proj=projection(m,err,t1,amps)
    result={'complete':True,'t0':t0,'t1':t1,'dt':dt,
            'u_inf':inf(err[0]),'v_inf':inf(err[1]),'linear_phase_projection':proj}
    if proj.get('identifiable'):
        # The nonlinear phase fit asks whether the evolved field is close to a
        # nearby member of the same fixed-spectral-parameter Gram family.
        def residual(theta):
            g=SolitonExpansion(m.G.p,m.G.q,m.G.rho*np.exp(theta),m.G.a,m.h)
            fit=g.uv(m.js,m.X.x,t1)
            return weight(m,(fit[0]-num[0],fit[1]-num[1]),amps)
        opt=least_squares(residual,np.asarray(proj['phase_rate_or_shift']),
                          bounds=(-.5,.5),max_nfev=20,xtol=1e-10,ftol=1e-10,gtol=1e-10)
        result['phase_fit']={'success':bool(opt.success),'theta':opt.x.tolist(),
                             'weighted_residual':float(np.linalg.norm(opt.fun)),
                             'weighted_initial_error':float(np.linalg.norm(weight(m,err,amps))),
                             'nfev':opt.nfev}
    return result


def full_window_gate(m,t0,amps,horizon=.5,dt=.00005,observe=.005):
    """Try a continuous collision trajectory; stop at the first 1% failure."""
    z=m.exact(t0)
    amp_u,amp_v=amps
    t=t0;history=[];failure=None
    blocks=round(horizon/observe);steps=round(observe/dt)
    for b in range(blocks):
        for k in range(steps):
            with np.errstate(over='ignore',invalid='ignore'):
                z=rk4(m.rhs,t,z,dt)
            t+=dt
            if not np.all(np.isfinite(z)) or inf(z)>1e3:
                failure={'t':t,'reason':'nonfinite or state magnitude >1000'}
                break
        if failure:break
        num=m.fields(z,t);exact=m.G.uv(m.js,m.X.x,t)
        eu,ev=inf(num[0]-exact[0])/amp_u,inf(num[1]-exact[1])/amp_v
        history.append({'t':t,'u_relative':eu,'v_relative':ev})
        if max(eu,ev)>.01:
            failure={'t':t,'reason':'first observed 1% two-field error failure'}
            break
    return {'start':t0,'target':t0+horizon,'last_t':t,'failure':failure,
            'observations':history}


def verify_expansion():
    cases=[([1.],[1.],[3.]),([1.,2.],[1.,3.],[3.,4.]),
           ([.5,1.5,2.5],[.5,2.,3.5],[1.,3.5,6.])]
    checks=[];x=np.linspace(-2,2,9);js=[-1,0,1]
    for p,q,rho in cases:
        g=SolitonExpansion(p,q,rho);slow=GramRef(p,q,rho,4.,.25)
        for t in (-.1,.1):
            u,v=g.uv(js,x,t)
            value=max(inf(u-slow.u_block(js,x,t)),inf(v-slow.v_block(js,x,t)))
            ut,vt=g.uv(js,x,t,True)
            eps=1e-5
            fwd=g.uv(js,x,t+eps);back=g.uv(js,x,t-eps)
            tangent_err=max(inf(ut-(fwd[0]-back[0])/(2*eps)),
                            inf(vt-(fwd[1]-back[1])/(2*eps)))
            theta=g.theta(js,x,t)
            hi=np.asarray(rho,dtype=float);hi[0]*=np.exp(eps)
            lo=np.asarray(rho,dtype=float);lo[0]*=np.exp(-eps)
            up=SolitonExpansion(p,q,hi).uv(js,x,t)
            um=SolitonExpansion(p,q,lo).uv(js,x,t)
            phase_err=max(inf(theta[0][0]-(up[0]-um[0])/(2*eps)),
                          inf(theta[1][0]-(up[1]-um[1])/(2*eps)))
            if max(value,tangent_err,phase_err)>2e-7:
                raise AssertionError((len(p),t,value,tangent_err,phase_err))
            checks.append({'N':len(p),'t':t,'gram_error':value,
                           'time_tangent_error':tangent_err,'phase_tangent_error':phase_err})
    return checks


def exact_n3_factorization():
    # Rational Cauchy principal minors check the triple coefficient without
    # relying on the floating-point subset expansion itself.
    p=list(map(Fraction,['0.5','1.5','2.5']))
    q=list(map(Fraction,['0.5','2','3.5']))
    def det3(a):
        return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
                -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
                +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
    c=[[1/(p[i]+q[j]) for j in range(3)] for i in range(3)]
    ratio=det3(c)/(c[0][0]*c[1][1]*c[2][2])
    pair={(i,j):(p[i]-p[j])*(q[i]-q[j])/((p[i]+q[j])*(p[j]+q[i]))
          for i in range(3) for j in range(i+1,3)}
    prod=np.prod([float(z) for z in pair.values()])
    assert ratio==np.prod(list(pair.values()))
    return {'pair_factors':{f'{i+1}{j+1}':str(v) for (i,j),v in pair.items()},
            'triple_coefficient':str(ratio),'float_product':float(prod)}


def main():
    verified=verify_expansion()
    cases=[]
    p2,q2,r2=[1.,2.],[1.,3.],[3.,4.]
    for h,nx,stages in ((.25,256,[-4.,-2.,0.,2.,4.]),
                        (.25,512,[-4.,0.,4.]),(.125,256,[-4.,0.,4.])):
        s=SolitonExpansion(p2,q2,r2,h=h)
        amp=scales(s,h,nx)
        for t in stages:
            for model in ('structure','fd'):
                m=ManifoldModel(p2,q2,r2,h,nx,model)
                row={'kind':'N2','h':h,'nx':nx,'t':t,'model':model,
                     'amplitude_scale':amp,'defect':defect(m,t,amp)}
                if h==.25 and ((nx==256 and t in (-4.,0.,4.)) or
                               (nx==512 and t==0.)):
                    row['burst']=burst(m,t,amp)
                    if nx==256 and t==0.:
                        row['burst_half_dt']=burst(m,t,amp,dt=.000025)
                cases.append(row)
                print('N2',h,nx,t,model,'normal',row['defect'].get('normal_fraction'),flush=True)
    # Asymptotic single-component controls. The faster soliton is dressed by
    # A12 before crossing; the stationary one is dressed after crossing.
    A12=s.A[(0,1)]
    singles=[]
    for t in (-4.,4.):
        for i in (0,1):
            factor=(A12 if (t<0 and i==1) or (t>0 and i==0) else 1.)
            pp,qq,rr=[p2[i]],[q2[i]],[r2[i]*factor]
            sol=SolitonExpansion(pp,qq,rr)
            amp=scales(sol)
            for model in ('structure','fd'):
                m=ManifoldModel(pp,qq,rr,model=model)
                row={'kind':'matched_N1','component':i+1,'t':t,
                     'dressing':factor,'model':model,'defect':defect(m,t,amp),
                     'burst':burst(m,t,amp)}
                singles.append(row)
                print('N1 control',t,i+1,model,row['defect'].get('normal_fraction'),flush=True)
    gate=[]
    for model in ('structure','fd'):
        m=ManifoldModel(p2,q2,r2,.25,256,model)
        gate.append({'model':model,**full_window_gate(m,-4.,scales(m.G))})
        print('continuous window gate',model,gate[-1]['failure'],flush=True)
    n3=exact_n3_factorization()
    p3,q3=[.5,1.5,2.5],[.5,2.,3.5]
    s3=np.asarray(p3)+np.asarray(q3)
    configs=[('concentrated',[0.,0.,0.],[0.]),
             ('staggered',[0.,2.,8.],[4.,8.,12.])]
    n3rows=[]
    for label,intercepts,stages in configs:
        rho=(s3*np.exp(-s3*np.asarray(intercepts))).tolist()
        sol=SolitonExpansion(p3,q3,rho)
        amp=scales(sol)
        for t in stages:
            for model in ('structure','fd'):
                m=ManifoldModel(p3,q3,rho,model=model)
                row={'kind':'N3','configuration':label,'intercepts':intercepts,
                     't':t,'model':model,'amplitude_scale':amp,
                     'defect':defect(m,t,amp)}
                if (label=='concentrated' and t==0.) or (label=='staggered' and t==8.):
                    row['burst']=burst(m,t,amp)
                n3rows.append(row)
                print('N3',label,t,model,row['defect'].get('normal_fraction'),flush=True)
    source=[Path(__file__),ROOT/'lib/soliton_expansion.py',ROOT/'lib/parametric.py',
            ROOT/'lib/parametric_open.py',ROOT/'lib/gramtau.py']
    result={'scope':'fixed-spectral phase manifold; local windows are independent',
            'validation':verified,'projection_condition_limit':1e6,
            'n2':cases,'matched_singles':singles,'continuous_gate':gate,
            'n3_factorization':n3,'n3_local':n3rows,
            'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source}}
    out=ROOT/'out/manifold_scattering.json'
    out.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('wrote',out,flush=True)


if __name__=='__main__':main()
