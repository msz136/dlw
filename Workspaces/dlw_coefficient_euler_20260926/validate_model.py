"""Independent long/short closure, boundary derivative and analytic soliton checks."""
import json
from pathlib import Path
import numpy as np
import mpmath as mp
from model import FamilyModel,Parameters,OpenModel

checks={}
def record(name,value,tol):
    value=float(value);checks[name]={'error':value,'tolerance':tol,'passed':value<tol}
    assert value<tol,(name,value,tol)
def norm(z):return np.max(np.abs(z))

rng=np.random.default_rng(20260926)
for route in ('fd','sd'):
    m=FamilyModel(Parameters(),nx=64,route=route)
    old=OpenModel(Parameters(),h=m.h,nx=64,model='fd' if route=='fd' else 'structure',continuous=True)
    t=.003;z=m.exact(t)+rng.normal(0,1e-4,m.exact(t).shape)
    P,v=m.unpack(z);u,_=m.fields(z,t)
    w=v-m.dy(u,m.state_ghosts(u,t))
    oldz=old.pack(P,v if route=='fd' else w)
    pt,qt=old.unpack(old.rhs(t,oldz))
    if route=='sd':
        bt=m.G.uv([m.js[0]],m.X.x,t,True)[0][0]
        ut=m.C.u_from_P(pt,bt)
        qt=qt+m.dy(ut,m.right_ghost_derivative(ut,t))
    record(route+'_old_long_vs_new_short_rhs',norm(m.rhs(t,z)-m.pack(pt,qt)),3e-11)

# Boundary time dependence checked by differentiating fields along an arbitrary state direction.
m=FamilyModel(Parameters(),nx=64);t=.003;z=m.exact(t)
dz=rng.normal(0,.01,z.shape);pt,_=m.unpack(dz)
bt=m.G.uv([m.js[0]],m.X.x,t,True)[0][0];ut=m.C.u_from_P(pt,bt)
eps=1e-5
up,_=m.fields(z+eps*dz,t+eps);um,_=m.fields(z-eps*dz,t-eps)
gp=m.state_ghosts(up,t+eps);gm=m.state_ghosts(um,t-eps)
actual=m.right_ghost_derivative(ut,t)
record('time_dependent_ghost_chain_rule',max(norm((a-b)/(2*eps)-d) for a,b,d in zip(gp,gm,actual)),2e-8)

# Exact coefficient flux differences at a common arbitrary state.
z=z+rng.normal(0,1e-4,z.shape);P,v=m.unpack(z);u,_=m.fields(z,t)
w=v-m.dy(u,m.state_ghosts(u,t));rhs0=m.rhs(t,z)
for c,k in [(-.125,.125),(.125,-.125),(.04248652711,.00844851896)]:
    n=FamilyModel(Parameters(),nx=64,c=c,kappa=k)
    dp=-np.diff(m.X.d1(2*c*m.h**2*u-k*m.h**4*w/4),axis=0)/m.h
    dw=-m.X.d1(m.h**2*(2*c*w-4*k*u))
    du=m.C.u_from_P(dp,np.zeros(m.X.n))
    dg=(np.zeros(m.X.n),3*du[-1]-3*du[-2]+du[-3])
    record(f'coefficient_flux_c{c}_k{k}',norm(n.rhs(t,z)-rhs0-m.pack(dp,dw+m.dy(du,dg))),4e-11)
    record(f'common_initial_c{c}_k{k}',norm(m.exact(0)-n.exact(0)),1e-14)

# 60-digit independent differentiation of the finite-h exact tau solution.
# No numerical x stencil or production boundary reconstruction enters this check.
mp.mp.dps=60
for a,p,q,c,k in [(4,1,2,0,0),(4,2,3,.125,-.125),(2,1.5,2,.04248652711,.00844851896)]:
    a,p,q,c,k=map(lambda v:mp.mpf(str(v)),(a,p,q,c,k));h=mp.mpf('.125')
    A=a+c*h*h;r=1+k*h*h;sm=A-h*r/2;sp=A+h*r/2
    chi=(p-sm)*(q+sp)/((p-sp)*(q+sm));gamma=-(p-sm)/(q+sm)
    S=p+q;om=q*q-p*p;rho=S
    sig=lambda z:1/(1+mp.exp(-z))
    def U(j,x,t):
        z=S*x+om*t+j*mp.log(chi)
        return S*(2*sig(z+mp.log(gamma))-sig(z)-sig(z+mp.log(chi)))
    def W(j,x,t):
        z=S*x+om*t+j*mp.log(chi)
        return 4*S/h*(sig(z+mp.log(chi))-sig(z))
    def F(j,x,t):return U(j,x,t)**2/2+2*A*U(j,x,t)+h*h*(W(j,x,t)**2/32-r*W(j,x,t)/4)
    worst=mp.mpf(0)
    for j,x,t in [(0,mp.mpf('.17'),mp.mpf('.003')),(-3,mp.mpf('-.31'),mp.mpf('.008'))]:
        e1=mp.diff(lambda tt:(U(j,x,tt)-U(j-1,x,tt))/h,t)
        e1+=mp.diff(lambda xx:(F(j,xx,t)-F(j-1,xx,t))/h,x)
        e1+=mp.diff(lambda xx:(U(j,xx,t)-U(j-1,xx,t))/h+(W(j,xx,t)+W(j-1,xx,t))/2,x,2)
        e2=mp.diff(lambda tt:W(j,x,tt),t)+mp.diff(lambda xx:(U(j,xx,t)+2*A)*W(j,xx,t)-4*r*U(j,xx,t),x)-mp.diff(lambda xx:W(j,xx,t),x,2)
        worst=max(worst,abs(e1),abs(e2))
        n=FamilyModel(Parameters(float(a),float(p),float(q),float(rho)),nx=64,c=float(c),kappa=float(k))
        un,vn=n.finite_fields([j],[float(x)],float(t))
        vv=W(j,x,t)+(U(j+1,x,t)-U(j-1,x,t))/(2*h)
        record(f'finite_tau_float_a{a}_p{p}_j{j}',max(abs(un[0,0]-float(U(j,x,t))),abs(vn[0,0]-float(vv))),4e-13)
    record(f'analytic_short_closure_a{a}_p{p}',worst,1e-50)

Path(__file__).with_name('model_validation.json').write_text(json.dumps(checks,indent=2)+'\n')
print(f'{len(checks)} checks passed; maximum scaled discrepancy {max(v["error"]/v["tolerance"] for v in checks.values()):.3g}')
