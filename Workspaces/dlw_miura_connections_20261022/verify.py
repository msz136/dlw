"""Exact differential identities; no numerical sampling."""
import sympy as s
from pathlib import Path
x,y,t=s.symbols('x y t')
h=s.symbols('h', nonzero=True)
q,r,m=[s.Function(z)(x,y,t) for z in ('q','r','m')]
D=lambda f,*args:s.diff(f,*args)
def evolve(expr, qt, rt):
    return s.simplify(s.expand(expr.subs({D(q,t):qt,D(r,t):rt}).doit()))
qt=-D(q,x,2)-2*D(m,x)*q
rt=D(r,x,2)+2*D(m,x)*r
u=2*D(q,x)/q
v=4*(1-q*r)+D(u,y)
e1=D(u,y,t)+D(v,x,2)+D(u*D(u,y),x)
e2=D(v,t)+D(u,x,2,y)+D(u*v-4*u,x)
results={}
for name,expr in [('continuous_DLW_1',e1),('continuous_DLW_2',e2)]:
    z=evolve(expr,qt,rt)
    z=s.simplify(z.subs(D(m,x,2,y),-D(q*r,x,2)))
    results[name]=z
# finite h: the two undifferenced physical evolution equations
S=s.Function('S')(x,t)  # M_j + M_{j+1}
omega=h*(1-q*r)
P=D(S,x)+h**2*(q**2*r**2-1)/4
qth=-D(q,x,2)-P*q
rth=D(r,x,2)+P*r
Z=u+2*S
results['finite_h_u']=evolve(D(u,t)+D((u*u+omega*omega)/2-h*omega,x)+D(Z,x,2),qth,rth)
results['finite_h_omega']=evolve(D(omega,t)+D(u*omega-h*u,x)-D(omega,x,2),qth,rth)
# Diagonal reduction of the continuous system: m_x=-qr.
qt1=-D(q,x,2)+2*q*q*r
rt1=D(r,x,2)-2*q*r*r
U=D(q,x)/q
H=-2*q*r+D(U,x)
results['Kaup_1']=evolve(D(U,t)+D(U*U+H,x),qt1,rt1)
results['Kaup_2']=evolve(D(H,t)+D(D(U,x,2)+2*U*H,x),qt1,rt1)
# Closed finite-h potential constraint, using M_{j+1}-M_j=h(1-s_j).
s0,s1,ds0,ds1,A=s.symbols('s0 s1 ds0 ds1 A')
V0=-A/2-h**2*(s0*s0-1)/8
V1=-(A-h*(ds0+ds1))/2-h**2*(s1*s1-1)/8
results['finite_h_potential_constraint']=s.simplify((V1-V0)/h-(ds0+ds1)/2+h*(s1*s1-s0*s0)/8)
theta,beta=[s.Function(z)(x,y,t) for z in ('theta','beta')]
B=D(theta,t)+D(theta,x,2)+D(theta,x)**2+2*D(beta,x,2)
J=D(beta,y,t)-D(beta,x,2,y)+2*D(theta,x)*(D(beta,x,y)-1)
H2=D(theta,x,2,y)+2*D(theta,x)*(D(theta,x,y)+2*D(beta,x,y))+D(theta,y)*B+D(theta,y,t)+2*D(beta,y,t)-4*D(theta,x)
results['bilinear_second_remainder']=s.simplify(H2-D(theta,y)*B-D(B,y)-2*J)
ss=1-D(beta,x,y)
results['three_tau_gauge_defect']=s.simplify(D(ss,t)-D(ss,x,2)+2*D(D(theta,x)*ss,x)+D(J,x))
output='\n'.join(f'{k}: {v}' for k,v in results.items())+'\n'
print(output)
assert all(v==0 for v in results.values())
Path(__file__).with_name('verification.txt').write_text(output,encoding='utf-8')
