"""Exact checks supporting the general proofs in ../../dlw_liouville_integrability.md.
Finite checks are not a substitute for the arbitrary-N proofs in that report.
"""
from fractions import Fraction as F
import sympy as s
S,c,d,P,Q,gamma,chi=s.symbols('S c d P Q gamma chi')
p=(S+c)/2;q=(S-c)/2
Cs=[s.expand((p**k-(-q)**k)/k) for k in range(1,5)]
assert Cs==[S,S*c/2,S**3/12+S*c*c/4,S*c*(S*S+c*c)/8] or all(s.expand(x-y)==0 for x,y in zip(Cs,[S,S*c/2,S**3/12+S*c*c/4,S*c*(S*S+c*c)/8]))
assert s.expand(2*Cs[2]-S**3/6-S*c*c/2)==0
print('PASS first four spectral coefficients and Hamiltonian identification')
gam=-(P+d)/(Q-d);ch=(P+d)*(Q+d)/((P-d)*(Q-d))
Pr=d*(chi+1-2*gamma)/(chi-1)
Qr=d*(gamma*chi+gamma-2*chi)/(gamma*(chi-1))
assert s.factor(Pr.subs({gamma:gam,chi:ch})-P)==0
assert s.factor(Qr.subs({gamma:gam,chi:ch})-Q)==0
print('PASS spectral inverse from gamma,chi')
for n in range(1,7):
 nodes=[s.Integer(4+2*i) for i in range(n)]+[s.Integer(3+2*i) for i in range(n)]
 V=s.Matrix([[x**k for x in nodes] for k in range(2*n)])
 expected=s.prod(nodes[j]-nodes[i] for i in range(2*n) for j in range(i+1,2*n))
 assert V.det()==expected!=0
print('PASS nonzero exact full spectral Vandermonde checks N=1..6')
def add(v,w):return(v[0]+w[0],v[1]*w[1])
def recover(vs):
 known={(F(0),F(1))}
 for v in vs:
  more={add(v,w) for w in known};assert not(more & known);known|=more
 remaining=set(known);remaining.remove((F(0),F(1)))
 built={(F(0),F(1))};out=[]
 while remaining:
  v=min(remaining);out.append(v);more={add(v,w) for w in built}
  assert more<=remaining;remaining-=more;built|=more
 return out
for n in range(1,7):
 vs=[]
 for i in range(n):
  cc=F(7+4*i);pp=(1+cc)/2;qq=(1-cc)/2;dd=F(1,16)
  chh=(pp-2+dd)*(qq+2+dd)/((pp-2-dd)*(qq+2-dd));vs.append((F(1),chh))
 assert set(recover(vs))==set(vs)
print('PASS exact exponential subset support recovery N=1..6')
print('General scope: nonresonant positive subset sums; proof is in the report, not the finite loop.')
