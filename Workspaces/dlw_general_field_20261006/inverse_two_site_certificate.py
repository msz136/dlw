from pathlib import Path
import sympy as z
p,s,px,sx,c,eta,B=z.symbols('p s px sx c eta B',nonzero=True)
f=p/2-eta
a=f*(-sx/c+(1-s*s/c**2)*(p/2+eta))
d=B-p*s/c+px/(p-2*eta)
yl=f*(1+s/c);yh=-f*(1-s/c)
D=lambda q:z.diff(q,p)*px+z.diff(q,s)*sx
for name,y,lam in [('low',yl,B-2*eta),('high',yh,B+2*eta)]:
 residual=z.factor(D(y)-(y*y+(d-lam)*y-a));print(name,'Riccati residual:',residual);assert residual==0
print('p reconstruction:',z.factor(2*eta+yl-yh-p))
print('s reconstruction:',z.factor(c*(yl+yh)/(yl-yh)-s))
assert z.factor(2*eta+yl-yh-p)==0
assert z.factor(c*(yl+yh)/(yl-yh)-s)==0
for y,lam,target in [(yl,B-2*eta,p-2*eta*s/c+px/(p-2*eta)),(yh,B+2*eta,-p-2*eta*s/c+px/(p-2*eta))]:
 assert z.factor(2*y+d-lam-target)==0
# Conversely start from arbitrary Riccati data and their required derivatives.
l,r,lx,rx,aa,dd=z.symbols('yl yh ylx yhx a d')
pp=2*eta+l-r;ss=c*(l+r)/(l-r)
lxx=l*l+(dd-(B-2*eta))*l-aa
rxx=r*r+(dd-(B+2*eta))*r-aa
DD=lambda q:z.diff(q,l)*lxx+z.diff(q,r)*rxx
ff=pp/2-eta
arec=ff*(-DD(ss)/c+(1-ss*ss/c**2)*(pp/2+eta))
drec=B-pp*ss/c+DD(pp)/(pp-2*eta)
assert z.factor(arec-aa)==0
assert z.factor(drec-dd)==0
print('Converse reconstruction: both coefficients exactly recovered.')
# Uniform p=s=0: companion A at marked values has a nonzero nilpotent part.
for lam in [B-2*eta,B+2*eta]:
 A=z.Matrix([[0,1],[-eta**2,B-lam]])
 N=A-(B-lam)/2*z.eye(2)
 assert N*N==z.zeros(2)
 assert N!=z.zeros(2)
print('Both uniform-background marked monodromies are Jordan, not scalar.')
