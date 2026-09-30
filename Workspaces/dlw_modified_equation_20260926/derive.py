"""Taylor identities for the physical-field DLW semidiscretization and matched FD."""
from pathlib import Path
import json
import sympy as s

x,y,t,h,a,c,kappa=s.symbols('x y t h a c kappa')
u=s.Function('u')(x,y,t)
v=s.Function('v')(x,y,t)
dx=lambda z:s.diff(z,x)
xx=lambda z:s.diff(z,x,2)
dy=lambda z:s.diff(z,y)
dt=lambda z:s.diff(z,t)
def jet(z,b,n=5):
    return sum(s.diff(z,y,k)*(s.Rational(b)*h)**k/s.factorial(k) for k in range(n+1))
checks=[]
def check(name,z):
    assert s.expand(z)==0, (name,s.simplify(z))
    checks.append(name)
    print('PASS:',name)
U=lambda j:jet(u,j)
V=lambda j:jet(v,j)
d0=lambda f,j:(f(j+1)-f(j-1))/(2*h)
W=lambda j:V(j)-d0(U,j)
H=lambda j:U(j)**2/2+2*a*U(j)+h*h*(W(j)**2/32-W(j)/4)
H0=lambda j:U(j)**2/2+2*a*U(j)
# First equation at y=0: its nodes j,j-1 are at +h/2,-h/2.
half=s.Rational(1,2)
e1=(dt(U(half)-U(-half))+dx(H(half)-H(-half)))/h+xx((U(half)-U(-half))/h+(W(half)+W(-half))/2)
e2=dt(V(0))+dx(d0(H,0)+(U(0)+2*a)*W(0)-4*U(0))+xx(d0(U,0)+(W(1)-2*W(0)+W(-1))/4)
f1=(dt(U(half)-U(-half))+dx(H0(half)-H0(-half)))/h+xx((V(half)+V(-half))/2)
f2=dt(v)+dx((u+2*a)*v-4*u)+xx(d0(U,0))
L1=s.diff(u,y,t)+xx(v)+dx((u+2*a)*dy(u))
L2=dt(v)+s.diff(u,x,2,y)+dx((u+2*a)*v-4*u)
K=(v-dy(u)-4)**2/32 # a constant offset is killed by x,y derivatives
R1=dx(dy(K))+s.diff(v,x,2,y,2)/12-s.diff(u,x,2,y,3)/4
R2=dx(dy(K))+dx(dy(u)*s.diff(u,y,2))/2+s.diff(v,x,2,y,2)/4-s.diff(u,x,2,y,3)/12
F1=s.diff(v,x,2,y,2)/12
F2=s.diff(u,x,2,y,3)/6
for name,expr,L,R,center in [('SD1',e1,L1,R1,True),('SD2',e2,L2,R2,False),('FD1',f1,L1,F1,True),('FD2',f2,L2,F2,False)]:
    expanded=s.expand(expr)
    check(name+' continuous term',expanded.coeff(h,0)-L)
    check(name+' no first order term',expanded.coeff(h,1))
    check(name+' second order term',expanded.coeff(h,2)-R-(s.diff(L1,y,2)/24 if center else 0))
    check(name+' no third order term',expanded.coeff(h,3))

check('SD-FD first additional defect',R1-F1-dx(dy(K))+s.diff(u,x,2,y,3)/4)
check('SD-FD second additional defect',R2-F2-dx(dy(K))-dx(dy(u)*s.diff(u,y,2))/2-s.diff(v,x,2,y,2)/4+s.diff(u,x,2,y,3)/4)
check('parameter-family first residual change',dy(dx(2*c*u))-2*c*s.diff(u,x,y))
check('parameter-family second residual change',dx(dy(2*c*u)+2*c*(v-dy(u))-4*kappa*u)-2*c*dx(v)+4*kappa*dx(u))

# Frechet derivatives govern the leading physical solution error, if a smooth
# matched solution expansion and suitable initial/boundary data exist.
eps=s.symbols('eps')
eu,ev=s.Function('eu')(x,y,t),s.Function('ev')(x,y,t)
linear1=s.diff(eu,y,t)+xx(ev)+dx((u+2*a)*dy(eu)+dy(u)*eu)
linear2=dt(ev)+s.diff(eu,x,2,y)+dx((u+2*a)*ev+(v-4)*eu)
check('first linearized physical equation',s.expand(L1.subs({u:u+eps*eu,v:v+eps*ev},simultaneous=True).doit()).coeff(eps,1)-linear1)
check('second linearized physical equation',s.expand(L2.subs({u:u+eps*eu,v:v+eps*ev},simultaneous=True).doit()).coeff(eps,1)-linear2)

# General tau perturbations separate extraction error from the change in tau.
alpha,beta,A2,B2=[s.Function(n)(x,y,t) for n in ('alpha','beta','A2','B2')]
uh=dx(2*(alpha+h*h*A2)-jet(beta+h*h*B2,-half)-jet(beta+h*h*B2,half))
wh=4*dx(jet(beta+h*h*B2,half)-jet(beta+h*h*B2,-half))/h
vh=wh+(jet(uh,1)-jet(uh,-1))/(2*h)
E_u=2*dx(A2-B2)-s.diff(beta,x,y,2)/4
E_v=2*s.diff(A2+B2,x,y)+s.diff(alpha,x,y,3)/3-5*s.diff(beta,x,y,3)/12
check('total physical u model coefficient',s.expand(uh).coeff(h,2)-E_u)
check('total physical v model coefficient',s.expand(vh).coeff(h,2)-E_v)

result={'checks':checks,'count':len(checks),'status':'passed',
        'R1_SD':s.latex(R1),'R2_SD':s.latex(R2),
        'R1_FD':s.latex(F1),'R2_FD':s.latex(F2),
        'first_equation_off_solution_extra':'h^2 * partial_y^2 L1 / 24',
        'meaning':'R is the h^2 residual on a continuous DLW solution, not its evolved field error.'}
Path(__file__).with_name('symbolic.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
