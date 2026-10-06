"""Exact local identities for Q5 after R transfer and mixed cubic trace."""
import sympy as s
import json
from pathlib import Path
N=10
u=s.symbols('u0:'+str(N));w=s.symbols('w0:'+str(N));beta=s.symbols('beta')
def D(f):return s.expand(sum(s.diff(f,u[i])*u[i+1]+s.diff(f,w[i])*w[i+1] for i in range(N-1)))
def Euler(f,vs):
    out=0
    for i,v in enumerate(vs):
        a=s.diff(f,v)
        for _ in range(i):a=-D(a)
        out+=a
    return s.expand(out)
qloc=u[0]**4*w[0]+12*u[0]**2*w[0]*u[1]-4*w[0]*u[1]**2-16*u[0]*u[1]*w[1]+8*u[1]*w[2]
qloc+=4*beta*u[0]**2*w[0]**3+4*beta**2*w[0]**5/5+8*beta*w[0]**3*u[1]/3-8*beta*w[0]*w[1]**2
LU=Euler(qloc,u);LW=Euler(qloc,w)
B=u[0]**2/2+beta*w[0]**2+u[1];C=u[0]*w[0]-w[1]
F0=u[0]**2*w[0]+w[0]*u[1]-u[0]*w[1]+2*beta*w[0]**3/3
T1=s.expand(-D(LU)+8*C*D(B)+(4*u[0]**2+8*u[1]+8*beta*w[0]**2)*D(C)+4*D(w[0]*D(B))-4*D(u[0]*D(C))+D(D(8*D(C)-4*F0)))
I0=s.expand(LU*D(B)+LW*D(C)+16*beta*w[1]**2*D(u[0]*w[0]))
print('T1=',T1)
print('Euler residual local=',Euler(I0,u),Euler(I0,w))
assert T1==0
assert Euler(I0,u)==0 and Euler(I0,w)==0
hom=0
for vs in [u,w]:
    for i in range(N-1):
        for k in range(i+1,N):
            term=s.diff(I0,vs[k])
            for _ in range(k-i-1):term=-D(term)
            hom+=vs[i]*term
hom=s.Poly(s.expand(hom),*u,*w)
G=sum(coef*s.prod(v**power for v,power in zip(u+w,mon))/sum(mon) for mon,coef in hom.terms() if sum(mon))
G=s.expand(G)
assert s.expand(D(G)-I0)==0
print('primitive G5=',G)
out={'LU':str(LU),'LW':str(LW),'T1':str(T1),'I0_corrected':str(I0),'Euler_U':str(Euler(I0,u)),'Euler_w':str(Euler(I0,w)),
     'G5':str(G),'primitive_verified':True}
Path(__file__).with_name('q5_structure.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
