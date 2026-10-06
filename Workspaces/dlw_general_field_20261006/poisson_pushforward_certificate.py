from pathlib import Path
import sympy as s
p=s.symbols('p:9');z=s.symbols('s:9');c,e,B=s.symbols('c eta B',nonzero=True)
def D(f):return s.expand(sum(s.diff(f,p[i])*p[i+1]+s.diff(f,z[i])*z[i+1] for i in range(8)))
def Dn(f,n):
 for _ in range(n):f=D(f)
 return f
def add(*ops):
 out={}
 for op in ops:
  for i,x in op.items():out[i]=out.get(i,0)+x
 return {i:s.factor(x) for i,x in out.items() if x!=0}
def mul(a,b):
 out={}
 for i,x in a.items():
  for j,y in b.items():
   for k in range(i+1):out[i+j-k]=out.get(i+j-k,0)+s.binomial(i,k)*x*Dn(y,k)
 return {i:s.factor(x) for i,x in out.items() if x!=0}
def adj(a):
 out={}
 for i,x in a.items():
  for k in range(i+1):out[i-k]=out.get(i-k,0)+(-1)**i*s.binomial(i,k)*Dn(x,k)
 return {i:s.factor(x) for i,x in out.items() if x!=0}
def scale(a,t):return {i:s.factor(t*x) for i,x in a.items()}
f=p[0]/2-e
alpha=f*(-z[1]/c+(1-z[0]**2/c**2)*(p[0]/2+e))
d=B-p[0]*z[0]/c+p[1]/(p[0]-2*e)
F=[[{i:s.diff(q,v[i]) for i in range(2) if s.diff(q,v[i])!=0} for v in [p,z]] for q in [alpha,d]]
J1=[[{}, {1:1}],[{1:1},{}]]
J2=[[{1:2*alpha,0:D(alpha)},{2:-1,1:d}],[{2:1,1:d,0:D(d)},{1:-2}]]
w=2*alpha*d-D(alpha)
J3=[[{1:2*w,0:D(w)},{3:1,2:-2*d,1:d*d-D(d)-4*alpha,0:-2*D(alpha)}], [{}, {1:-4*d,0:-2*D(d)}]]
J3[1][0]=scale(adj(J3[0][1]),-1)
for i in range(2):
 for j in range(2):
  computed=scale(add(mul(mul(F[i][0],{1:1}),adj(F[j][1])),mul(mul(F[i][1],{1:1}),adj(F[j][0]))),-1)
  expected=scale(add(J3[i][j],scale(J2[i][j],-2*B),scale(J1[i][j],B*B-4*e*e)),-1/(2*c))
  residual=add(computed,scale(expected,-1))
  assert all(s.factor(x)==0 for x in residual.values()),(i,j,residual)
  print('Pushforward matrix entry',i,j,'exactly matches pencil.')
print('Pushed bracket = -(J3 - 2B J2 +(B²-4 eta²) J1)/(2c)')
