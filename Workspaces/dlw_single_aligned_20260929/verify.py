"""Verify single-soliton adapter, common lift, boundary derivative and Eq.21."""
from experiment import *


def main():
    refs=[]; initial=[]; boundaries=[]; kernels=[]
    for name,c in CASES.items():
        for continuous in (False,True):
            g=SingleExact(c,.125,continuous)
            js=np.arange(-12,12); x=np.linspace(-12,12,521)
            # Independently evaluate the inherited tau-moment field formulas.
            for derivative in (False,True):
                a=TwoExact.uv(g,js,x,.007,derivative)
                b=g.uv(js,x,.007,derivative)
                e=max(float(abs(v-w).max()) for v,w in zip(a,b))
                assert e<1e-11,(name,continuous,derivative,e)
                refs.append(dict(case=name,continuous=continuous,derivative=derivative,error=e))
    seen=set()
    for s in plan():
        if s['model']!='SD2': continue
        key=tuple(s[k] for k in ('case','mesh','nx','L','h'))
        if key in seen: continue
        seen.add(key); p=Problem(s); z=p.initial()
        b=Problem(dict(s,model='SD')); zb=b.initial()
        fs=p.fields(z,0.); bs=b.fields(zb,0.)
        err=max(float(abs(v-w).max()) for v,w in zip(fs,bs))
        nodes=float(abs(p.X.x-b.X.x).max())
        assert max(err,nodes)<1e-10
        initial.append(dict(spec=s,physical_field_difference=err,node_difference=nodes,**p.m.lift_diagnostics))
        if s['variant']!='main': continue
        m=p.m; s0=p.X.s.copy(); t=.007
        vel=.03*np.sin(2*np.pi*p.X.xi/p.X.L) if s['mesh']=='moving' else np.zeros(p.X.n)
        vel[0]=0.
        _,material=m.boundary_derivative(t,vel); errors=[]
        for eps in (1e-4,5e-5):
            p.X.set_s(s0+eps*vel); plus=m.boundary(t+eps)[0].copy()
            p.X.set_s(s0-eps*vel); minus=m.boundary(t-eps)[0].copy()
            errors.append(float(abs((plus-minus)/(2*eps)-material[:-1]).max()))
        p.X.set_s(s0)
        assert errors[-1]<2e-6,errors
        for k in range(4): z=rk4(p.rhs,k*.000125,z,.000125)
        u,_=p.fields(z,.0005)
        be=float(abs(u[0]-m.G.uv([m.js[0]],p.X.x,.0005)[0][0]).max())
        assert be<1e-10
        boundaries.append(dict(case=s['case'],mesh=s['mesh'],derivative_errors=errors,lower_u_error=be))
    for name,c in CASES.items():
        for moving in (False,True):
            for n in (256,512,1024):
                m=consistent.ConsistentSD2(c,.125,n,40.); g=SingleExact(c,.125,False)
                if moving: m.X.set_s(.15*np.sin(2*np.pi*m.X.xi/40.))
                m.jump=np.expm1(sum(g.gammah-.5*g.chi)); m.rjump=np.expm1(-sum(g.gammah-.5*g.chi))
                q,qt,r,rt=g.qr(m.js,m.X.x,.01)
                pq,pr=m.physical_arrays(q,r,m.dx(q,m.jump),m.dx(r,m.rjump),qt[0])
                mask=abs(m.X.x)<10
                kernels.append(dict(case=name,moving=moving,nx=n,Q=float(abs(pq[:,mask]-qt[:,mask]).max()),R=float(abs(pr[:,mask]-rt[:,mask]).max())))
            for f in ('Q','R'):
                order=float(np.log2(kernels[-2][f]/kernels[-1][f]))
                kernels[-1][f+'_order']=order
                assert 3.5<order<4.5,(name,moving,f,order)
    io.dump(HERE/'implementation_checks.json',dict(reference_checks=refs,initial_checks=initial,boundary_checks=boundaries,kernel_checks=kernels))
    print('PASS',len(refs),'references',len(initial),'initial configurations',len(boundaries),'boundaries',len(kernels),'RHS checks')


if __name__=='__main__': main()
