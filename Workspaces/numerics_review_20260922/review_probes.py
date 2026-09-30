"""Read-only review probes. Production modules/results are never overwritten."""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[key]='1'
import ast, hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
NUM=ROOT/'Workspaces/dlw_semidiscrete/numerics'
sys.path.insert(0,str(NUM/'lib'))
import numpy as np
import mpmath as mp
from scipy.special import logsumexp
from gramtau import ContRef, GramRef, lam
from solver import XGrid, integrate

before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in NUM.rglob('*') if p.is_file() and '__pycache__' not in str(p)}
out={}

# Independent analytic N=1 reference with original p,q time rate.
mp.mp.dps=60
a,p,q=mp.mpf(4),mp.mpf(1),mp.mpf(2)
S=p+q; ry=1/(p-a)+1/(q+a); gam=-(p-a)/(q+a)
def fields(shift):
    def E(x,y,t): return mp.exp(S*x+(q*q-p*p+shift)*t+ry*y)
    def u(x,y,t):
        e=E(x,y,t); return 2*S*(gam*e/(1+gam*e)-e/(1+e))
    def v(x,y,t):
        e=E(x,y,t); return 2*S*ry*(gam*e/(1+gam*e)**2+e/(1+e)**2)
    return u,v
def residual(u,v,x,y,t):
    ux=mp.diff(lambda z:u(z,y,t),x)
    uy=mp.diff(lambda z:u(x,z,t),y)
    uxy=mp.diff(lambda z:mp.diff(lambda w:u(z,w,t),y),x)
    uyt=mp.diff(lambda z:mp.diff(lambda w:u(x,z,w),t),y)
    uxx_y=mp.diff(lambda z:mp.diff(lambda w:u(w,z,t),x,2),y)
    vx=mp.diff(lambda z:v(z,y,t),x)
    vxx=mp.diff(lambda z:v(z,y,t),x,2)
    vt=mp.diff(lambda z:v(x,y,z),t)
    return [float(uyt+vxx+ux*uy+u(x,y,t)*uxy+2*a*uxy),float(vt+ux*v(x,y,t)+u(x,y,t)*vx+uxx_y+2*a*vx-4*ux)]
points=[tuple(map(mp.mpf,z)) for z in [('0','0','0'),('0.3','0.2','0.1'),('-0.4','-0.3','0.2')]]
out['continuous_residual']={'correct': [residual(*fields(0),*z) for z in points], 'implemented_time_rate':[residual(*fields(2*a*S),*z) for z in points]}
C=ContRef([1],[2],[3],4)
phase=[]
for h in [1/4,1/8,1/16,1/32]:
    G=GramRef([1],[2],[3],4,h); x,t,y=-.3,.2,.5*h
    u,v=fields(0)
    phase.append({'h':h,'u_error_existing':abs(G.u(0,x,t)-C.u0(y,x,t)), 'u_error_correct':abs(G.u(0,x,t)-float(u(x,y,t)))})
out['nonzero_time_limit']=phase

# Same E1 finite-h fields, fixed physical y window; true quadrature weights.
xs=np.linspace(-1.5,1.5,25); wx=np.full(len(xs),xs[1]-xs[0]);wx[[0,-1]]*=.5
e1=[]
for h in [1/4,1/8,1/16,1/32]:
    js=np.arange(int(-1.5/h),int(1.5/h))
    G=GramRef([1],[2],[3],4,h)
    err=np.array([G.u_row(int(j),xs,0)-C.u0_row((j+.5)*h,xs,0) for j in js])
    e1.append({'h':h,'ny':len(js),'E2_fixed_domain':float(np.sqrt(h*np.sum(err**2*wx))),'Einf':float(np.max(abs(err)))})
out['E1_fixed_domain']=e1

# Load only function definitions from E7: no top-level experiment/JSON writes.
src=(NUM/'experiments/e7_fd_baseline.py').read_text(encoding='utf-8')
tree=ast.parse(src); funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
ns={'np':np,'A':4.0};ns['X']=XGrid(256,40,4)
ys=np.linspace(-6,6,241);ns['dy']=ys[1]-ys[0]
ns['U']=np.array([C.u0_row(y,ns['X'].x,0) for y in ys]);ns['V']=np.array([C.v0_row(y,ns['X'].x,0) for y in ys])
exec(compile(ast.Module(body=funcs,type_ignores=[]),'e7_extracted','exec'),ns)
run_old=ns['run']
run_node=next(n for n in funcs if n.name=='run')
fixed=ast.unparse(run_node).replace('t += h','u = u_from_w(w, U[0])\n        t += h')
assert fixed!=ast.unparse(run_node)
fixedns=ns.copy();exec(fixed,fixedns);run_fixed=fixedns['run']
curves={}
for name,run in [('original',run_old),('refresh_u_each_step',run_fixed)]:
    ur,vr,_=run(.01/128,.01); rows=[]
    for div in [2,4,8,16]:
        uu,vv,_=run(.01/div,.01)
        rows.append({'dt':.01/div,'Einf_u':float(np.max(abs(uu-ur))),'Einf_v':float(np.max(abs(vv-vr)))})
    for i in range(1,len(rows)):rows[i]['order_v']=float(np.log2(rows[i-1]['Einf_v']/rows[i]['Einf_v']))
    curves[name]=rows
out['E7_temporal_recheck']=curves

# A budget based on continuum k cannot be the spectrum of D1@D1 at Nyquist.
X=XGrid(256,60,4); nyq=(-1.0)**np.arange(256)
out['nyquist_symbol']={'k_nyquist':float(np.pi/X.dx),'D1_nyquist_max':float(np.max(abs(X.D1@nyq))), 'D2_nyquist_max':float(np.max(abs(X.D2@nyq)))}

# Trapezoid reports success even when fixed-point iteration did not converge.
_,_,info=integrate(lambda t,P,W:(10*P,10*W),0,1,np.ones((1,1)),np.ones((1,1)),1,method='trapezoid',maxit=2,tol=1e-12)
out['trapezoid_failure_handling']=info

# Stable positive four-term N=2 tau expansion, independently of inverse matrices.
pp=np.array([1.,2.]);qq=np.array([1.,3.]);rr=np.array([3.,4.]);h=.25
ss=pp+qq;ww=qq**2-pp**2;chi=lam(pp-4,h)*lam(qq+4,h);gamma=-(pp-4+h/2)/(qq+4-h/2)
A12=1/6
def dlog(n,j,x,t):
    e=np.log(rr/ss)+ss*x+ww*t+j*np.log(chi)+n*np.log(gamma)
    logs=np.array([0,e[0],e[1],np.log(A12)+sum(e)])
    return np.dot(np.exp(logs-logsumexp(logs)),[0,ss[0],ss[1],sum(ss)])
def stable_u(x,t):return 2*dlog(1,0,x,t)-dlog(0,0,x,t)-dlog(0,1,x,t)
G2=GramRef(pp,qq,rr,4,h)
out['E4_reference_conditioning']=[{'x':x,'t':t,'matrix_u':G2.u(0,x,t),'stable_expansion_u':stable_u(x,t)} for x,t in [(20.5367,-20),(10.5367,-10),(-19.8205,20)]]
assert before=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in NUM.rglob('*') if p.is_file() and '__pycache__' not in str(p)}
out['production_files_unchanged']=True
Path(__file__).with_name('probe_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
