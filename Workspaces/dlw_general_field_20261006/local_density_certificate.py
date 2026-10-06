from pathlib import Path
import sympy as z
A=z.symbols('a:12');V=z.symbols('d:12')
def D(f):return z.expand(sum(z.diff(f,A[i])*A[i+1]+z.diff(f,V[i])*V[i+1] for i in range(11)))
def Dn(f,n):
 for _ in range(n):f=D(f)
 return f
at=D(D(A[0]))-2*D(A[0]*V[0]);vt=-D(D(V[0]))-D(V[0]**2)+2*D(A[0])
def dt(f):return z.expand(sum(z.diff(f,A[i])*Dn(at,i)+z.diff(f,V[i])*Dn(vt,i) for i in range(9)))
r=[0,-A[0]]
for n in range(1,7):r.append(z.expand(V[0]*r[n]-D(r[n])+sum(r[i]*r[n-i] for i in range(1,n))))
for n in range(1,7):
 res=z.expand(dt(r[n])+D(r[n+1]+V[0]*r[n]));assert res==0
 print('density',n,'exact conservation residual:',res)
print('first density:',r[1]);print('second density:',r[2]);print('third density:',r[3])
def euler(f,v):return z.expand(sum((-1)**i*Dn(z.diff(f,v[i]),i) for i in range(8)))
def J1(grad):f,g=grad;return [D(g),D(f)]
def J2(grad):
 f,g=grad
 return [2*A[0]*D(f)+A[1]*f-Dn(g,2)+V[0]*D(g),Dn(f,2)+V[0]*D(f)+V[1]*f-2*D(g)]
for n in range(1,5):
 lhs=J2([euler(r[n],A),euler(r[n],V)])
 rhs=J1([euler(r[n+1],A),euler(r[n+1],V)])
 assert all(z.expand(a-b)==0 for a,b in zip(lhs,rhs))
 print('Lenard direct Euler check',n,'passed')
