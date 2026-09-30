"""Independent algebra and reference checks for the current Report.html."""
from pathlib import Path
import json
import sys
import hashlib
import sympy as s
import mpmath as mp
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
REPORT=ROOT/'Workspaces/gsg_project/dlw_report'
sys.path.insert(0,str(ROOT/'Workspaces/hs_numerics_plan'))
from hs_exact import Soliton

x,t,a,h=s.symbols('x t a h', nonzero=True)
A,B,C=[s.Function(n)(x,t) for n in ('A','B','C')]
u=s.diff(2*A-B-C,x);w=s.diff(C-B,x);Z=s.diff(2*A+B+C,x)
L=lambda f,g,k:s.diff(f+g,x,2)+s.diff(f-g,x)**2+s.diff(f-g,t)+2*k*s.diff(f-g,x)
wall0=L(A,B,a-h/2);wall1=L(A,C,a+h/2)
checks={}
def zero(name,v):
    result=s.simplify(s.expand(v))
    assert result==0,(name,result)
    checks[name]=True
flux=(u*u+w*w)/2+2*a*u-h*w
zero('eq6_sum',s.diff(u,t)+s.diff(flux,x)+s.diff(Z,x,2)-s.diff(wall0+wall1,x))
zero('eq6_difference',s.diff(w,t)+s.diff((u+2*a)*w-h*u,x)-s.diff(w,x,2)-s.diff(wall0-wall1,x))
um2,um1,u0,up1=s.symbols('um2 um1 u0 up1')
dm=lambda left,right:(right-left)/h
zero('eq8_first_spatial_identity',((up1-um1)+(u0-um2))/(4*h)-(u0-um1)/h-h*h/4*((up1-u0)-2*(u0-um1)+(um1-um2))/h**3)
wm,w0,wp=s.symbols('wm w0 wp')
zero('eq8_second_spatial_identity',(wm+2*w0+wp)/4-w0-h*h/4*(wp-2*w0+wm)/h**2)
Q=s.exp(A-(B+C)/2)
bracket=(s.diff(Q,t)+s.diff(Q,x,2)+2*a*s.diff(Q,x))/Q+s.diff(B+C,x,2)+w*w/4-h*w/2
zero('eq9e_bracket',bracket-(wall0+wall1)/2)
q,r=s.symbols('q r')
zero('eq9h',(h*(1-q*r))**2/4-h*h*(1-q*r)/2-h*h*(q*q*r*r-1)/4)
Qf,Rf=[s.Function(n)(x,t) for n in ('Q','R')]
zero('eq9j',-s.diff(Qf*Rf,x,2)+2*s.diff(s.diff(Qf,x)*Rf,x)-s.diff(Qf,x,2)*Rf+Qf*s.diff(Rf,x,2))
d,b,c,ur=s.symbols('d b c ur', nonzero=True)
z=(d-a)*(c-a-d)
paper=-b/d*(b+z)+(b+z)**2/(2*d)+4*ur*d-c*(b+z)-b*(2*d-c)
implemented=2*d*(2*ur-b)+((d*d-a*(a-c))**2-b*b)/(2*d)-c*c*d/2
zero('paper_2hs_eq100_vs_implemented',paper-implemented)

mp.mp.dps=55
residuals=[]
for kind in ('one','two'):
    def logtau(X,T):
        if kind=='one':
            return mp.log(1+mp.exp(mp.mpf('3.75')*X-mp.mpf('.6')*T))
        p1,p2,q1,q2=map(mp.mpf,('1.1','1.25','11','5'))
        E1=mp.exp((p1-q1)*X+(1/p1-1/q1)*T)*mp.mpf('6.5')
        E2=mp.exp((p2-q2)*X+(1/p2-1/q2)*T)*mp.mpf('6.5')
        return mp.log(1+E1+E2+mp.mpf(12)/507*E1*E2)
    U=lambda X,T:mp.diff(logtau,(X,T),(0,2))
    R=lambda X,T:1/(1-mp.diff(logtau,(X,T),(1,1)))
    for X,T in [(mp.mpf('-.3'),mp.mpf('0')),(mp.mpf('.2'),mp.mpf('.5'))]:
        uv,rv=U(X,T),R(X,T)
        ux=mp.diff(U,(X,T),(1,0))*rv
        first=mp.diff(U,(X,T),(1,1))*rv+ux**2/2-4*uv-(rv**2-1)/2
        second=mp.diff(R,(X,T),(0,1))-rv*ux
        assert max(abs(first),abs(second))<mp.mpf('1e-45')
        residuals.append(dict(case=kind,X=str(X),t=str(T),pde_u=str(first),pde_rho=str(second)))

grid=np.linspace(-1,1,32001)
one=json.loads((ROOT/'Workspaces/hs_four_schemes_20260927/paper_point/results.json').read_text())
two_dir=ROOT/'Workspaces/hs_two_soliton_short_20260928/main'
two=json.loads((two_dir/'results.json').read_text())
metrics=[]
for kind,sol in [('one',Soliton((5.,),phase=(0.,),shift=-.8)),('two',Soliton((1.1,1.25),phase=(np.log(6.5),)*2,shift=-(1/11+1/5)))]:
    refs=sol.continuous_x(grid,.5)[:2]
    saved=json.loads((REPORT/'submission_report'/('validation_data.json' if kind=='one' else 'two_soliton_summary.json')).read_text(encoding='utf-8'))['metrics']
    for scheme in ('S1','S4'):
        row=one['rows'][f'{scheme}_rk4_0.003125'] if kind=='one' else two['results'][scheme]
        path=Path(row['profile']) if kind=='one' else two_dir/row['profile']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256' if kind=='one' else 'profile_sha256']
        with np.load(path) as z:
            for i,field in enumerate(('u','rho')):
                coords=z['t0.5_'+('x' if field=='u' else 'rho_x')]
                error=float(abs(np.interp(grid,coords,z['t0.5_'+field])-refs[i]).max())
                expected=saved[scheme if kind=='one' else scheme+'_t0.5'][field]
                assert abs(error-expected)<5e-13
                metrics.append(dict(case=kind,scheme=scheme,field=field,error=error,difference=abs(error-expected)))
out=dict(symbolic=checks,continuous_pde_residuals=residuals,metrics=metrics,
         source_sha256=hashlib.sha256((REPORT/'_src/Report.md').read_bytes()).hexdigest(),
         html_sha256=hashlib.sha256((ROOT/'Report.html').read_bytes()).hexdigest())
(HERE/'checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
