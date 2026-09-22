"""Independent Fraction-only Gram audit; no old tau engine is imported.

Exponential polynomials are grouped by their actual (x,t,y) rate vectors.
Identities are checked coefficientwise, never by floating point evaluation.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from math import factorial
import json
from pathlib import Path

ZERO=(F(0),)*3
def add(*polys):
    out={}
    for p in polys:
        for k,v in p.items():
            out[k]=out.get(k,F(0))+v
    return {k:v for k,v in out.items() if v}
def scale(p,c): return {k:v*c for k,v in p.items() if v*c}
def mul(p,q):
    out={}
    for k,c in p.items():
        for l,d in q.items():
            z=tuple(a+b for a,b in zip(k,l))
            out[z]=out.get(z,F(0))+c*d
    return {k:v for k,v in out.items() if v}
def der(p,axis=0): return {k:c*k[axis] for k,c in p.items() if k[axis]}
def bil(p,q,s):
    out={}
    for k,c in p.items():
        for l,d in q.items():
            dx=k[0]-l[0]
            z=tuple(a+b for a,b in zip(k,l))
            out[z]=out.get(z,F(0))+c*d*(dx*dx+k[1]-l[1]+2*s*dx)
    return {k:v for k,v in out.items() if v}
def det(matrix):
    n=len(matrix); total=F(0)
    for perm in permutations(range(n)):
        term=F((-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n)))
        for i in range(n): term*=matrix[i][perm[i]]
        total+=term
    return total

class Gram:
    def __init__(self,n,a,h,offset=0):
        self.n,self.a,self.h=n,F(a),F(h)
        # A globally positive real soliton sector: 0<p<a-h/2, q>0, ordered.
        self.p=[F(2*i+3+offset,3) for i in range(n)]
        self.q=[F(3*i+5+offset,4) for i in range(n)]
        self.rho=[F(i+2+offset,i+1) for i in range(n)]
        self.weights=[]
        for k in range(n+1):
            for subset in combinations(range(n),k):
                c=det([[1/(self.p[i]+self.q[j]) for j in subset] for i in subset])
                self.weights.append((subset,c))
    def lam(self,z): return (z+self.h/2)/(z-self.h/2)
    def tau(self,n,j,s,phase='none'):
        out={}
        for subset,c in self.weights:
            key=[F(0)]*3
            for i in subset:
                p,q=self.p[i],self.q[i]
                c*=self.rho[i]*(-(p-s)/(q+s))**n*(self.lam(p-self.a)*self.lam(q+self.a))**j
                key[0]+=p+q; key[1]+=q*q-p*p
                if phase!='none':
                    b=s if phase=='shifted' else self.a
                    key[2]+=1/(p-b)+1/(q+b)
            out[tuple(key)]=out.get(tuple(key),F(0))+c
        return {k:v for k,v in out.items() if v}
    def matrix_tau(self,n,j,s):
        # Independent determinant expansion of the actual Gram matrix.
        matrix=[]
        for i,p in enumerate(self.p):
            row=[]
            for k,q in enumerate(self.q):
                c=self.rho[i]/(p+q)*(-(p-s)/(q+s))**n*(self.lam(p-self.a)*self.lam(q+self.a))**j
                z=(p+q,q*q-p*p,F(0))
                row.append(add({z:c},{ZERO:F(1)} if i==k else {}))
            matrix.append(row)
        total={}
        for perm in permutations(range(self.n)):
            term={ZERO:F((-1)**sum(perm[i]>perm[k] for i in range(self.n) for k in range(i+1,self.n)))}
            for i in range(self.n): term=mul(term,matrix[i][perm[i]])
            total=add(total,term)
        return total

# Small exact Taylor jets for direct evaluation of nonlinear equations.
X,T=3,1
class Jet:
    def __init__(self,d=None): self.d={k:F(v) for k,v in (d or {}).items() if v}
    @staticmethod
    def lift(z): return z if isinstance(z,Jet) else Jet({(0,0):z})
    def __add__(self,z): return Jet(add(self.d,self.lift(z).d))
    __radd__=__add__
    def __neg__(self): return Jet(scale(self.d,-1))
    def __sub__(self,z): return self+-self.lift(z)
    def __rsub__(self,z): return self.lift(z)+-self
    def __mul__(self,z):
        d=mul(self.d,self.lift(z).d)
        return Jet({k:v for k,v in d.items() if k[0]<=X and k[1]<=T})
    __rmul__=__mul__
    def __truediv__(self,z): return self* (1/F(z))
    def dx(self): return Jet({(i-1,j):i*v for (i,j),v in self.d.items() if i})
    def dt(self): return Jet({(i,j-1):j*v for (i,j),v in self.d.items() if j})
    def val(self): return self.d.get((0,0),F(0))

def logjet(poly):
    d={(i,j):sum(c*k[0]**i*k[1]**j for k,c in poly.items())/F(factorial(i)*factorial(j)) for i in range(X+1) for j in range(T+1)}
    assert d[0,0]>0
    z=Jet(d)/d[0,0]-1
    power=Jet.lift(1); result=Jet()
    for k in range(1,X+T+1):
        power=power*z
        result+=power*F((-1)**(k+1),k)
    return result

def nonlinear_check(g,site):
    h,a=g.h,g.a
    logs_f={j:logjet(g.tau(1,j,a-h/2)) for j in range(site-3,site+4)}
    logs_g={j:logjet(g.tau(0,j,a)) for j in range(site-3,site+5)}
    u=lambda j:(2*logs_f[j]-logs_g[j]-logs_g[j+1]).dx()
    d0=lambda f,j:(f(j+1)-f(j-1))/(2*h)
    dm=lambda f,j:(f(j)-f(j-1))/h
    mm=lambda f,j:(f(j)+f(j-1))/2
    lap=lambda f,j:(f(j+1)-2*f(j)+f(j-1))/(h*h)
    v=lambda j:4*(logs_g[j+1]-logs_g[j]).dx()/h+d0(u,j)
    w=lambda j:v(j)-d0(u,j)
    H=lambda j:u(j)*u(j)/2+2*a*u(j)+h*h*(w(j)*w(j)/32-w(j)/4)
    n1=dm(lambda j:u(j).dt()+H(j).dx(),site)+(mm(v,site)-h*h*lap(lambda j:dm(u,j),site)/4).dx().dx()
    n2=v(site).dt()+(d0(H,site)+(u(site)+2*a)*w(site)-4*u(site)).dx()+(d0(u,site)+h*h*lap(w,site)/4).dx().dx()
    assert n1.val()==F(0) and n2.val()==F(0)
    return [str(n1.val()),str(n2.val())]

def run():
    result={'arithmetic':'fractions.Fraction; coefficientwise identities','bilinear':[],'nonlinear':[]}
    for N in range(1,6):
        count=0
        for offset in (0,1):
            for h in (F(1,2),F(1,3),F(1,4),F(1,8),F(1,16)):
                g=Gram(N,8,h,offset); a=g.a; d=h/2
                for j in (-2,0,1,3):
                    f=g.tau(1,j,a-d); z=g.tau(0,j,a); zp=g.tau(0,j+1,a)
                    assert bil(f,z,a-d)=={} and bil(f,zp,a+d)=={}
                    assert f==g.tau(1,j+1,a+d)
                    # Also valid with a shared independent spectator y phase.
                    assert bil(g.tau(1,j,a-d,'fixed'),g.tau(0,j,a,'fixed'),a-d)=={}
                    count+=1
                for n in (-2,-1,0,1,2):
                    assert bil(g.tau(n+1,0,a),g.tau(n,0,a),a)=={}
                    assert g.tau(n,0,a-d)==g.tau(n,n,a+d)
                if N<=3:
                    assert g.matrix_tau(1,1,a-d)==g.tau(1,1,a-d)
                    assert g.matrix_tau(0,1,a)==g.tau(0,1,a)
        result['bilinear'].append({'N':N,'parameter_step_site_cases':count,'both_residuals':'identically zero'})
        print('PASS Gram pair N=',N,'cases=',count,flush=True)
    for N in (1,2,3):
        for offset in (0,1):
            for h in (F(1,2),F(1,4),F(1,8)):
                for j in (-1,0,2):
                    g=Gram(N,8,h,offset)
                    result['nonlinear'].append({'N':N,'h':str(h),'offset':offset,'j':j,'residuals':nonlinear_check(g,j)})
        print('PASS direct nonlinear Gram solutions N=',N,flush=True)
    g=Gram(1,8,F(1,4)); a=g.a; d=g.h/2
    bad=bil(g.tau(1,0,a-d,'shifted'),g.tau(0,0,a,'shifted'),a-d)
    assert bad
    # This is a failure as a 3-variable identity, but vanishes identically on y=0.
    collapsed={}
    for (kx,kt,ky),c in bad.items(): collapsed=add(collapsed,{(kx,kt,F(0)):c})
    assert collapsed=={}
    result['hybrid_counterexample']=[{'rate':list(map(str,k)),'coefficient':str(c)} for k,c in bad.items()]
    print('PASS distinguishes invalid shifted-y hybrid from valid semidiscrete Gram',flush=True)
    dest=Path(__file__).with_name('gram_reassessment_results.json')
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('ALL CHECKS PASSED;',dest.name,flush=True)

if __name__=='__main__': run()
