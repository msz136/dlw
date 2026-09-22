"""Exact structural checks, separate from the Gram/nonlinear test battery."""
import sympy as s
from fractions import Fraction as F
from verify_gram_reassessment import Gram,add,mul,scale,der

# 2D Toda identity on an auxiliary continuous negative-flow coordinate eta.
# It is not the assertion that an eta derivative equals a physical j difference.
count=0
for N in range(1,6):
    for hh in (F(1,2),F(1,4),F(1,8)):
        g=Gram(N,8,hh)
        for nn in (-1,0,1):
            z=g.tau(nn,2,g.a,'shifted')
            res=add(mul(z,der(der(z,0),2)),scale(mul(der(z,0),der(z,2)),-1),scale(mul(z,z),-1),mul(g.tau(nn+1,2,g.a,'shifted'),g.tau(nn-1,2,g.a,'shifted')))
            assert res=={}
            count+=1
print('PASS: exact 2D Toda identities,',count,'cases, N=1..5')

x,t,a,h=s.symbols('x t a h')
w,V,psi=[s.Function(z)(x,t) for z in ('w','V','psi')]
D=lambda z:s.diff(z,x)
H0=lambda z:s.diff(z,t)+D(D(z))+V*z
H1=lambda z:s.diff(z,t)+D(D(z))+(V+2*D(w))*z
T=lambda z:D(z)-w*z
obstruction=s.diff(w,t)+D(D(w))+2*w*D(w)+D(V)
assert s.expand(H1(T(psi))-T(H0(psi))+obstruction*psi)==0
print('PASS: Darboux operator identity on arbitrary wave function')

al,be,bp=[s.Function(z)(x,t) for z in ('alpha','beta','beta_next')]
def pot(q,par): return D(D(al+q))+D(al-q)**2+s.diff(al-q,t)+2*par*D(al-q)
for q,par in ((be,a-h/2),(bp,a+h/2)):
    ww=par+D(al-q); vv=2*D(D(q))
    assert s.expand(s.diff(ww,t)+D(D(ww))+2*ww*D(ww)+D(vv)-D(pot(q,par)))==0
    assert s.expand(vv+2*D(ww)-2*D(D(al)))==0
print('PASS: both Darboux links have the same intermediate potential')
u=D(2*al-be-bp); r=2*D(bp-be)/h
assert s.expand(a-h/2+D(al-be)-(a+u/2+h*(r-2)/4))==0
assert s.expand(a+h/2+D(al-bp)-(a+u/2-h*(r-2)/4))==0
print('PASS: Darboux shift coefficients expressed in physical fields')
W=2*r
HH=u*u/2+2*a*u+h*h*(W*W/32-W/4)
S=s.diff(u,t)+D(HH)+D(D(D(2*al+be+bp)))
assert s.expand(D(2*D(D(be)))+(s.diff(u,t)+D(HH)+D(D(u))+h*D(D(W))/2)/2-S/2)==0
assert s.expand(2*D(D(bp-be))-h*D(W)/2)==0
print('PASS: physical-field reconstruction of heat potentials')

P,Q,d=s.symbols('P Q d',nonzero=True)
chi=(P+d)*(Q+d)/((P-d)*(Q-d))
gm=-(P+d)/(Q-d); gp=-(P-d)/(Q+d)
assert s.factor(gp*chi-gm)==0
assert s.factor(gm**2/chi-(P**2-d**2)/(Q**2-d**2))==0
print('PASS: structural entry identity and exact soliton mass factor')

p1,p2,q1,q2=s.symbols('p1 p2 q1 q2')
interaction=1-(p1+q1)*(p2+q2)/((p1+q2)*(p2+q1))
assert s.factor(interaction-(p1-p2)*(q1-q2)/((p1+q2)*(p2+q1)))==0
print('PASS: normalized pair interaction is independent of h and tau shift')

# Show why the old projective-matrix product is not the fixed-z scalar transfer.
z=F(5); q0,q1,q2=F(1),F(2),F(3)
scalar=(z+q1)/(z+q0)*(z+q2)/(z+q1)
first=(z+q1)/(z+q0)
composition=(first+q2)/(first+q1)
assert scalar==F(4,3) and composition==F(25,19) and scalar!=composition
print('PASS: old transfer identification fails; scalar=',scalar,'Mobius composition=',composition)

# Exact linear dispersion using the nearest-edge equivalent physical variables.
sigma,k,K,C=s.symbols('sigma k K C',nonzero=True,real=True)
ii=s.I
mat=s.Matrix([[ii*K*(sigma+ii*k*(2*a-h)),-k**2],[-ii*k*(4*C+K*k),sigma+ii*k*(2*a+h)]])
expected=ii*K*((sigma+2*a*ii*k)**2+h*h*k*k-k**4-4*k**3*C/K)
assert s.expand(mat.det()-expected)==0
print('PASS: dispersion (sigma+2a*i*k)^2=k^4+4*k^3*C/K-h^2*k^2')

# Audit the all-N determinant lemma's scalar contraction cancellation.
kap,mq,nu,zeta,eta,eta2,ss=s.symbols('kap mq nu zeta eta eta2 ss')
kapx=mq+nu-kap**2
zetax=kap*(1-zeta)-ss*zeta+eta
etax=nu*(1-zeta)-ss*eta+eta2
zetaxx=kapx*(1-zeta)-(kap+ss)*zetax+etax
zetat=mq*(1-zeta)-ss*kap+ss**2*zeta-eta2+eta*kap
assert s.expand(zetat+zetaxx+2*ss*zetax-2*kapx*(1-zeta))==0
print('PASS: all-N Gram determinant lemma scalar cancellation')
print('ALL STRUCTURAL CHECKS PASSED')
