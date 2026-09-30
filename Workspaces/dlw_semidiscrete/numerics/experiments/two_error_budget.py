"""Two-soliton u/v model, solver, reconstruction and total error budget.

Finite-h Gram and continuous Gram references are sampled at the same F sites.
An additional experiment starts both models from common continuous fields.
"""
from pathlib import Path
import sys, json, hashlib
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
from gramtau import ContRef
from multisoliton_study import TwoModel, advance, inf


class ContinuousTwo:
    def __init__(self,h):
        self.h=h
        self.ref=ContRef([1,2],[1,3],[3,4],4)

    def uv(self,js,x,t,derivative=False):
        if derivative:
            raise NotImplementedError('time derivative is not used by continuous-data runs')
        y=(np.asarray(js)+.5)*self.h
        return (np.asarray([self.ref.u0_row(float(yy),x,t) for yy in y]),
                np.asarray([self.ref.v0_row(float(yy),x,t) for yy in y]))


def norms(z,h,dx):
    return {'inf':inf(z),'l2':float(np.sqrt(h*dx*np.sum(z*z)))}


def fields(m,z,t):
    return m.fields(z,t)


def reference(m,t):
    return m.G.uv(m.js,m.X.x,t),ContinuousTwo(m.h).uv(m.js,m.X.x,t)


def budget(m,z,t):
    num=fields(m,z,t)
    finite,continuum=reference(m,t)
    row={'t':t,'model':m.model,'h':m.h,'nx':m.X.n,'fields':{}}
    errstate=z-m.exact(t)
    p,q=m.unpack(errstate)
    du,rec_v=m.error_fields(errstate)
    if m.model=='structure':
        reconstruction=rec_v-q
    else:
        reconstruction=np.zeros_like(q)
    assert inf(du-(num[0]-finite[0]))<5e-11
    assert inf(rec_v-(num[1]-finite[1]))<5e-11
    for i,name in enumerate(('u','v')):
        solver=num[i]-finite[i]
        model=finite[i]-continuum[i]
        total=num[i]-continuum[i]
        identity=inf(total-solver-model)
        assert identity<2e-12
        row['fields'][name]={'solver':norms(solver,m.h,m.X.dx),
                             'model':norms(model,m.h,m.X.dx),
                             'total':norms(total,m.h,m.X.dx),
                             'identity_inf':identity,
                             'triangle_ratio':inf(total)/max(inf(solver)+inf(model),1e-30)}
    row['v_reconstruction']={'q_error_inf':inf(q),
                             'dy_u_error_inf':inf(reconstruction),
                             'reconstructed_v_error_inf':inf(rec_v),
                             'right_q_error':inf(q[-1]),
                             'right_dy_u_error':inf(reconstruction[-1]),
                             'right_v_error':inf(rec_v[-1]),
                             'identity_inf':inf(rec_v-q-reconstruction)}
    return row


def model_scan():
    rows=[]
    for h in (.25,.125,.0625,.03125):
        m=TwoModel(h,256,'structure')
        for t in (0.,.005,.01):
            finite,continuum=reference(m,t)
            rows.append({'h':h,'t':t,'u':norms(finite[0]-continuum[0],h,m.X.dx),
                         'v':norms(finite[1]-continuum[1],h,m.X.dx)})
    return rows


def verify_common_reference():
    errs=[]
    for h in (.25,.125):
        c=ContinuousTwo(h)
        js=[-2,0,2];x=np.array([-.7,.2,1.1])
        for t in (0.,.01):
            u,v=c.uv(js,x,t)
            for k,j in enumerate(js):
                y=(j+.5)*h
                errs.extend([abs(u[k,i]-c.ref.u0(y,float(xx),t)) for i,xx in enumerate(x)])
                errs.extend([abs(v[k,i]-c.ref.v0(y,float(xx),t)) for i,xx in enumerate(x)])
    assert max(errs)<3e-12,max(errs)
    models=[]
    for model in ('structure','fd'):
        m=TwoModel(.25,64,model);m.G=ContinuousTwo(.25)
        models.append(m.fields(m.exact(0),0))
    common=max(inf(a-b) for a,b in zip(*models))
    assert common<2e-12,common
    return {'continuous_vector_scalar_inf':max(errs),'common_initial_uv_inf':common}


def evolve_budget(h,nx,model,continuous_data=False,T=.01,dt=.00005):
    m=TwoModel(h,nx,model)
    if continuous_data:
        m.G=ContinuousTwo(h)
    z0=m.exact(0)
    _,trajectory,complete=advance(m.rhs,z0,dt,round(T/dt))
    if not complete or len(trajectory)!=round(T/.005):
        raise RuntimeError(f'incomplete trajectory h={h}, nx={nx}, model={model}')
    if continuous_data:
        observations=[]
        for t,z in trajectory:
            observed=fields(m,z,t);exact=m.G.uv(m.js,m.X.x,t)
            observations.append({'t':t,'u':norms(observed[0]-exact[0],h,m.X.dx),
                                 'v':norms(observed[1]-exact[1],h,m.X.dx)})
        return {'h':h,'nx':nx,'model':model,'T':T,'dt':dt,
                'initial_data':'continuous','observations':observations}
    return {'h':h,'nx':nx,'model':model,'T':T,'dt':dt,
            'initial_data':'finite_h_Gram','observations':[budget(m,z,t) for t,z in trajectory]}


def main():
    verification=verify_common_reference()
    scan=model_scan()
    for t in (0.,.005,.01):
        a=[r for r in scan if r['t']==t]
        for field in ('u','v'):
            ratios=[a[i][field]['inf']/a[i+1][field]['inf'] for i in range(3)]
            print('exact model limit',t,field,'ratios',ratios,flush=True)
    runs=[]
    for h,nx,T,dt in ((.25,256,.01,.00005),(.125,256,.01,.00005),
                      (.0625,256,.01,.00005),
                      (.25,512,.005,.000025)):
        for model in ('structure','fd'):
            row=evolve_budget(h,nx,model,T=T,dt=dt)
            runs.append(row)
            print('finite initial',h,nx,model,row['observations'][-1]['fields'],flush=True)
    continuous_runs=[]
    for h in (.25,.125):
        for model in ('structure','fd'):
            row=evolve_budget(h,256,model,continuous_data=True)
            continuous_runs.append(row)
            print('continuous initial',h,model,row['observations'][-1],flush=True)
    time_controls=[]
    for model in ('structure','fd'):
        coarse=next(r for r in runs if r['h']==.25 and r['nx']==256 and r['model']==model)
        fine=evolve_budget(.25,256,model,dt=.000025)
        diffs={field:{kind:abs(coarse['observations'][-1]['fields'][field][kind]['inf']
                                -fine['observations'][-1]['fields'][field][kind]['inf'])
                      for kind in ('solver','total')} for field in ('u','v')}
        time_controls.append({'model':model,'coarse_dt':.00005,'fine_dt':.000025,
                              'error_norm_differences':diffs})
        print('time control',model,diffs,flush=True)
    sources=[Path(__file__),ROOT/'experiments/multisoliton_study.py',
             ROOT/'lib/multigram.py',ROOT/'lib/gramtau.py',ROOT/'lib/parametric.py',
             ROOT/'lib/parametric_open.py']
    result={'sample_y':'(j+1/2)h','domain':{'x':[-10,10],'y_half':1.5},
            'verification':verification,
            'exact_model_scan':scan,'finite_initial_runs':runs,
            'continuous_initial_runs':continuous_runs,'time_controls':time_controls,
            'sources_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    path=ROOT/'out/two_error_budget.json'
    path.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('wrote',path,flush=True)


if __name__=='__main__':main()
