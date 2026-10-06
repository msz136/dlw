"""Symbolic local remainder after skew transfer of every R term."""
import sympy as s
from pathlib import Path
import json
N=9
u=s.symbols('u0:'+str(N)); w=s.symbols('w0:'+str(N)); beta=s.symbols('beta')
def D(f): return s.expand(sum(s.diff(f,u[i])*u[i+1]+s.diff(f,w[i])*w[i+1] for i in range(N-1)))
B0=u[0]**2/2+beta*w[0]**2+u[1]
C=u[0]*w[0]-w[1]
QU=u[0]**2*w[0]+2*beta*w[0]**3/3-2*u[0]*w[1]+4*w[2]/3
QW=u[0]**3/3+2*beta*u[0]*w[0]**2+2*u[0]*u[1]+4*u[2]/3
F=s.expand(w[0]*D(B0)+u[0]*D(C)-D(QU)-D(D(u[0]*w[0])))
I0=s.expand(QU*D(B0)+QW*D(C))
def Euler(f,vs):
    out=0
    for i,v in enumerate(vs):
        p=s.diff(f,v)
        for _ in range(i):p=-D(p)
        out+=p
    return s.expand(out)
print('F=',F)
print('Euler(I0)=',Euler(I0,u),Euler(I0,w))
rem=s.expand(I0+4*beta*w[1]**3/3)
hom=0
for vs in [u,w]:
    for i in range(N-1):
        for k in range(i+1,N):
            term=s.diff(rem,vs[k])
            for _ in range(k-i-1):term=-D(term)
            hom+=vs[i]*term
hom=s.Poly(s.expand(hom),*u,*w)
G=sum(coef*s.prod(v**pow for v,pow in zip(u+w,mon))/sum(mon) for mon,coef in hom.terms() if sum(mon))
G=s.expand(G)
assert s.expand(D(G)-rem)==0
print('local primitive=',G)
out={'F':str(F),'I0':str(I0),'Euler_U':str(Euler(I0,u)),'Euler_w':str(Euler(I0,w)),'primitive_G':str(G),'primitive_check':True}
Path(__file__).with_name('weight4_structure.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
