"""Exact polarized Fourier-symbol test for a bounded weight-four ansatz.

No numerical approximation: Fraction coefficients, r(l)=h/2*(s**l+1)/(s**l-1).
Only proper lattice-frequency subsets occur in R; samples avoid l=0 there.
The multilinear coloring removes self-products and gives polynomial identity tests.
"""
from fractions import Fraction as F
import random
import json
from pathlib import Path
import sympy as sp

BASE=Path(__file__).resolve().parent

class Poly:
    n=0; kval=[]; lval=[]; s=F(2); h=F(1)
    def __init__(self,a=None): self.a=a or {}
    def __add__(self,o):
        if not isinstance(o,Poly): o=Poly({0:F(o)})
        z=self.a.copy()
        for k,v in o.a.items(): z[k]=z.get(k,F(0))+v
        return Poly({k:v for k,v in z.items() if v})
    __radd__=__add__
    def __neg__(self): return Poly({k:-v for k,v in self.a.items()})
    def __sub__(self,o): return self+-o
    def __mul__(self,o):
        if not isinstance(o,Poly): return Poly({k:v*o for k,v in self.a.items() if v*o})
        z={}
        for k,v in self.a.items():
            for l,w in o.a.items():
                if not k&l: z[k|l]=z.get(k|l,F(0))+v*w
        return Poly({k:v for k,v in z.items() if v})
    __rmul__=__mul__
    def __pow__(self,n):
        z=Poly({0:F(1)})
        for _ in range(n): z=z*self
        return z
    def D(self): return Poly({k:v*self.kval[k] for k,v in self.a.items() if self.kval[k]})
    def R(self):
        z={}
        for k,v in self.a.items():
            if not self.lval[k]: raise ValueError('Undefined zero lattice mode inside R')
            q=self.s**self.lval[k]
            z[k]=v*self.h/2*(q+1)/(q-1)
        return Poly(z)
    def trace(self): return self.a.get((1<<self.n)-1,F(0))

class Dual:
    def __init__(self,a,b=None): self.a=a; self.b=b or Poly()
    def __add__(self,o):
        if not isinstance(o,Dual): o=Dual(Poly({0:F(o)}))
        return Dual(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self): return Dual(-self.a,-self.b)
    def __sub__(self,o): return self+-o
    def __mul__(self,o):
        if not isinstance(o,Dual): return Dual(self.a*o,self.b*o)
        return Dual(self.a*o.a,self.a*o.b+self.b*o.a)
    __rmul__=__mul__
    def __pow__(self,n):
        z=Dual(Poly({0:F(1)}))
        for _ in range(n): z=z*self
        return z
    def D(self): return Dual(self.a.D(),self.b.D())
    def R(self): return Dual(self.a.R(),self.b.R())

def basis(U,w):
    x=U.D(); y=w.D(); A=y.R(); B=x.R()
    return [U**4,U**3*w,U**2*w**2,U*w**3,w**4,
            U*w*x,w**2*x,x*x,x*y,y*y,
            U**2*A,U*w*A,w**2*A,A*A,x*A,
            U**2*B,U*w*B,w**2*B,A*B,B*B]

NAMES=['U^4','U^3 w','U^2 w^2','U w^3','w^4',
       'U w U_x','w^2 U_x','U_x^2','U_x w_x','w_x^2',
       'U^2 A','U w A','w^2 A','A^2','U_x A',
       'U^2 B','U w B','w^2 B','A B','B^2']

def row(n,rng):
    # Powers of two and a balancing final frequency avoid proper zero subsets.
    l=[2**i for i in range(n-1)]; l.append(-sum(l))
    rng.shuffle(l)
    k=[rng.randint(-3,4) for _ in range(n-1)]; k.append(-sum(k))
    Poly.n=n; Poly.s=F(rng.choice([2,3,5])); Poly.h=F(1)
    Poly.kval=[sum(k[i] for i in range(n) if m>>i&1) for m in range(1<<n)]
    Poly.lval=[sum(l[i] for i in range(n) if m>>i&1) for m in range(1<<n)]
    U=Poly({1<<i:F(rng.randint(-3,3)) for i in range(n)})
    w=Poly({1<<i:F(rng.randint(-3,3)) for i in range(n)})
    Ut=-(U*U*F(1,2)+w*w*F(1,32)+U.D()+w.D().R()).D()
    wt=-(U*w-w.D()).D()
    return [v.b.trace() for v in basis(Dual(U,Ut),Dual(w,wt))]

def main():
    rng=random.Random(20261004)
    rows=[row(n,rng) for n in [3,4,5] for _ in range(24)]
    mat=sp.Matrix([[sp.Rational(v.numerator,v.denominator) for v in r] for r in rows])
    null=mat.nullspace()
    out={'names':NAMES,'rows':mat.rows,'rank':mat.rank(),'nullspace':[[str(v) for v in c] for c in null],
         'scope':'weight4; x derivative <=1 representatives; R only on first derivatives; proper subset l!=0'}
    print(json.dumps(out,indent=2))
    (BASE/'weight4_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')

if __name__=='__main__': main()
