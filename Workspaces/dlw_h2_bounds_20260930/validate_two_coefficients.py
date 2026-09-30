"""Independent high-precision derivatives of the new two-soliton coefficients."""
from pathlib import Path
import json
import sympy as s
import mpmath as mp

HERE=Path(__file__).resolve().parent
mp.mp.dps=55
r,t=s.symbols('r t',real=True)
data=json.loads((HERE/'two_bounds.json').read_text(encoding='utf-8'))
func={name:s.lambdify((r,t),s.sympify(row['expression'],locals={'r':r,'t':t}),'mpmath') for name,row in data['bounds'].items()}
def alpha(x,y):
    a=mp.exp(x-y/12);b=mp.exp(x-y/2)
    return mp.log(1+mp.mpf(4)/3*a+2*b+mp.mpf(32)/9*a*b)
def beta(x,y):
    a=mp.exp(x-y/12);b=mp.exp(x-y/2)
    return mp.log(1+a+b+mp.mpf(4)/3*a*b)
def u(x,y):return 2*mp.diff(lambda xx:alpha(xx,y)-beta(xx,y),x)
def v(x,y):return 2*mp.diff(lambda xx,yy:alpha(xx,yy)+beta(xx,yy),(x,y),(1,1))
def w(x,y):return 4*mp.diff(beta,(x,y),(1,1))
def nonlinear(x,y):return (w(x,y)-4)**2/32
def product(x,y):return mp.diff(u,(x,y),(0,1))*mp.diff(u,(x,y),(0,2))
errors=[]
for xx,yy in (('.13','.37'),('-.43','-.81')):
    point=(mp.mpf(xx),mp.mpf(yy))
    dd=lambda f,i,j:mp.diff(f,point,(i,j))
    nl=dd(nonlinear,1,1)
    vt,ut=dd(v,2,2),dd(u,2,3)
    values={'SD_R1':nl+vt/12-ut/4,'SD_R2':nl+dd(product,1,0)/2+vt/4-ut/12,
            'FD_R1':vt/12,'FD_R2':ut/6}
    x,y=point
    rr=1/(1+mp.exp(-(x-y/12)));tt=1/(1+mp.exp(-(x-y/2)))
    for name,value in values.items():
        error=abs(value-func[name](rr,tt))
        assert error<mp.mpf('1e-45')
        errors.append({'point':[xx,yy],'coefficient':name,'absolute_difference':mp.nstr(error,8)})
    print('C independent derivative check at',xx,yy,'passed',flush=True)
validation=json.loads((HERE/'validation.json').read_text(encoding='utf-8'))
validation['two_soliton_independent_derivatives']={'precision_digits':55,'comparisons':errors}
(HERE/'validation.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
print('PASSED new C derivative checks',flush=True)
