from pathlib import Path
import sympy as s
a=s.symbols('a:6');d=s.symbols('d:6');y,v,lam=s.symbols('y v lambda')
yx=y*y+(d[0]-lam)*y-a[0]
vx=-(2*y+d[0]-lam)*v-1
def D(f):return s.expand(s.diff(f,y)*yx+s.diff(f,v)*vx+sum(s.diff(f,a[i])*a[i+1]+s.diff(f,d[i])*d[i+1] for i in range(5)))
def Dn(f,n):
 for _ in range(n):f=D(f)
 return f
f=-v;g=y*v
j1=[D(g),D(f)]
j2=[2*a[0]*D(f)+a[1]*f-Dn(g,2)+d[0]*D(g),Dn(f,2)+d[0]*D(f)+d[1]*f-2*D(g)]
w=2*a[0]*d[0]-a[1]
# lower left = D^3+2dD²+(d²+3d_x-4a)D+2dd_x+d_xx-2a_x
j3=[2*w*D(f)+D(w)*f+Dn(g,3)-2*d[0]*Dn(g,2)+(d[0]**2-d[1]-4*a[0])*D(g)-2*a[1]*g,
Dn(f,3)+2*d[0]*Dn(f,2)+(d[0]**2+3*d[1]-4*a[0])*D(f)+(2*d[0]*d[1]+d[2]-2*a[1])*f-4*d[0]*D(g)-2*d[1]*g]
for i in range(2):
 r2=s.factor(j2[i]-lam*j1[i]);r3=s.factor(j3[i]-lam*j2[i]);print(i,r2,r3);assert r2==0;assert s.factor(r3-[a[1],d[1]][i])==0
print('All negative powers satisfy both Lenard identities; the third-tensor generating identity includes the translation constant.')
