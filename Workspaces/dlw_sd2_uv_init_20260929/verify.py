import json
import numpy as np
from consistent_sd2 import Problem,ConsistentSD2,HERE,PRIOR
from reference import CASES,TwoExact
import run_experiments as old
from parametric import rk4

def main():
    init=[];seen=set()
    for s in old.make_plan():
        if s['model']!='SD2':continue
        key=tuple(s[k] for k in ('case','mesh','nx','L','h'))
        if key in seen:continue
        seen.add(key);p=Problem(s);z=p.initial()
        init.append(dict(spec=s,**p.m.lift_diagnostics))
    boundary=[]
    for case in CASES:
        for mesh in ('fixed','moving'):
            s=next(s for s in old.make_plan() if s['case']==case and s['mesh']==mesh and s['model']=='SD2' and s['variant']=='main')
            p=Problem(s);state=p.initial();m=p.m;s0=p.X.s.copy();t=.007
            velocity=.03*np.sin(2*np.pi*p.X.xi/p.X.L) if mesh=='moving' else np.zeros(p.X.n)
            velocity[0]=0.
            _,material=m.boundary_derivative(t,velocity)
            errs=[]
            for eps in (1e-4,5e-5):
                p.X.set_s(s0+eps*velocity);plus=m.boundary(t+eps)[0].copy()
                p.X.set_s(s0-eps*velocity);minus=m.boundary(t-eps)[0].copy()
                errs.append(float(abs((plus-minus)/(2*eps)-material[:-1]).max()))
            p.X.set_s(s0)
            assert errs[-1]<2e-6,(case,mesh,errs)
            for k in range(4):state=rk4(p.rhs,k*.000125,state,.000125)
            u,_=p.fields(state,.0005);exact=m.G.uv([m.js[0]],p.X.x,.0005)[0][0]
            be=float(abs(u[0]-exact).max());assert be<1e-10
            boundary.append(dict(case=case,mesh=mesh,directional_derivative_errors=errs,lower_u_error_after_four_RK4_steps=be))
    kernel=[]
    for case,c in CASES.items():
        for moving in (False,True):
            L=640. if case=='fig5' else 40.
            ns=(512,1024,2048) if case=='fig5' else (256,512,1024)
            for n in ns:
                m=ConsistentSD2(c,.125,n,L);g=TwoExact(c,.125,False)
                if moving:m.X.set_s(.15*np.sin(2*np.pi*m.X.xi/L))
                m.jump=np.expm1(sum(g.gammah-.5*g.chi));m.rjump=np.expm1(-sum(g.gammah-.5*g.chi))
                q,qt,r,rt=g.qr(m.js,m.X.x,.01)
                pq,pr=m.physical_arrays(q,r,m.dx(q,m.jump),m.dx(r,m.rjump),qt[0])
                mask=abs(m.X.x)<(100 if case=='fig5' else 10)
                kernel.append(dict(case=case,moving=moving,nx=n,q_rhs_error=float(abs(pq[:,mask]-qt[:,mask]).max()),r_rhs_error=float(abs(pr[:,mask]-rt[:,mask]).max())))
            for f in ('q_rhs_error','r_rhs_error'):
                order=float(np.log2(kernel[-2][f]/kernel[-1][f]));kernel[-1][f+'_order']=order
                assert 3.5<order<4.5
    result=dict(initial_configurations=init,boundary_checks=boundary,actual_kernel_finite_h_checks=kernel,
                sources={str(p):old.previous.sha(p) for p in (HERE/'consistent_sd2.py',HERE/'verify.py',PRIOR/'models.py',PRIOR/'reference.py')})
    old.previous.dump(HERE/'implementation_checks.json',result)
    print('PASS',len(init),'initial configurations;',len(boundary),'boundary checks;',len(kernel),'finite-h RHS checks')
    print('max initial errors',max(max(r['initial_field_errors'].values()) for r in init))
    print('max boundary derivative error',max(r['directional_derivative_errors'][-1] for r in boundary))

if __name__=='__main__':main()
