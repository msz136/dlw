from pathlib import Path
import sympy as z
import json
p=z.symbols('p:9');s=z.symbols('s:9'); c,g,be=z.symbols('c gamma beta',nonzero=True)
vars=p+s
def D(f):
 return z.expand(sum(z.diff(f,p[i])*p[i+1]+z.diff(f,s[i])*s[i+1] for i in range(8)))
def powerD(f,n):
 for _ in range(n):f=D(f)
 return f
def eu(f,v):
 return z.factor(sum((-1)**i*powerD(z.diff(f,v[i]),i) for i in range(6)))
b=(g-p[0]*s[0])/c
K=c*p[0]**2/2-(g-p[0]*s[0])**2/(2*c)+be*c*s[0]**2+s[0]*p[1]
q4=0
for sign in [1,-1]:
 U=b+sign*p[0];w=c+sign*s[0]
 q4+= (U**3*w/3+2*be*U*w**3/3+2*U*w*D(U)-z.Rational(4,3)*D(U)*D(w))/2
q4=z.expand(q4)
# Divide out overall constant 2h in all charges; bracket normalized accordingly
KP,KS=eu(K,p),eu(K,s)
pt,st=-D(KS),-D(KP)
checks={}
for name,rho in [('mass_p',p[0]),('mass_s',s[0]),('momentum',p[0]*s[0]),('Hamiltonian',K),('Q4',q4)]:
 rate=z.expand(eu(rho,p)*pt+eu(rho,s)*st)
 checks[name]=[str(eu(rate,p)),str(eu(rate,s))]
 assert checks[name]==['0','0'],(name,checks[name])
print('p_t=',z.factor(pt));print('s_t=',z.factor(st));print('Q4 density=',z.collect(q4,[p[1],s[1]]));print(json.dumps(checks,indent=2))
open(str(Path(__file__).resolve().parent / 'two_site_exact_result.json'),'w').write(json.dumps(checks,indent=2))
eta=z.symbols('eta',nonzero=True)
pt=pt.subs(be,2*eta**2/c**2);st=st.subs(be,2*eta**2/c**2)
def dt(f):return z.expand(sum(z.diff(f,p[i])*powerD(pt,i)+z.diff(f,s[i])*powerD(st,i) for i in range(6)))
C=g/(2*c)-p[0]*s[0]/c
f=p[0]/2-eta
r=-s[1]/c+(1-s[0]**2/c**2)*(p[0]/2+eta)
v=[r]
for i in range(1,4):v.append(z.expand(C*v[-1]-D(v[-1])))
ell=[0]+[-f*vi for vi in v]
for n in [1,2]:
 # [-(D²+2 ell1), L] at D^-n
 rhs=-D(D(ell[n]))-2*D(ell[n+1])
 for j in range(1,n):rhs+=2*ell[j]*z.binomial(-j,n-j)*powerD(ell[1],n-j)
 # coefficient order n: [multiplication,-] term +2 ell_j binomial(-j,k) D^k ell1
 residual=z.factor(dt(ell[n])-rhs)
 print('Lax coefficient',n,':',residual)
A=z.factor(-(dt(f)+D(D(f))+2*C*D(f)+(D(C)+C*C)*f-2*f*f*r)/f)
print('sigma_t=',A)
for label,expr in [('gauge_compatibility',dt(C)-D(A)),('adjoint_heat',dt(r)-A*r-D(D(r))+2*C*D(r)-(C*C-D(C))*r+2*f*r*r)]:
 res=z.factor(expr);print(label,res);assert res==0
k,lam=z.symbols('k lambda',real=True)
mat=z.Matrix([[k*k-z.I*k*g/c,-4*z.I*eta**2*k/c],[-z.I*c*k,-k*k-z.I*k*g/c]])
char=z.factor((lam*z.eye(2)-mat).det())
assert z.expand(char-((lam+z.I*k*g/c)**2-k**4+4*eta**2*k**2))==0
print('linearized characteristic:',char)
# All-order scalar gauge intertwining identities avoid any inverse of f.
assert z.factor(dt(f)+A*f+D(D(f))+2*C*D(f)+(D(C)+C*C)*f-2*f*f*r)==0
print('All polynomial gauge identities certified for arbitrary jets and parameters.')
# Direct Miura evolution into the two-field Kaup--Broer-type system.
aa=f*r;dd=C+D(f)/f
for label,expr in [('a_miura',dt(aa)-D(D(aa))+2*D(aa*dd)),('d_miura',dt(dd)+D(D(dd))+D(dd*dd)-2*D(aa))]:
 residual=z.factor(expr);print(label,residual);assert residual==0
