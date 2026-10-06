"""Bounded weight-five conservation ansatz, exact Fourier polarization."""
from search_weight4 import Poly,Dual,F
import random
import sympy as s
import json
from pathlib import Path
BASE=Path(__file__).resolve().parent

def basis(U,w):
    x=U.D(); y=w.D(); A=y.R(); B=x.R()
    items=[]
    def add(name,value):items.append((name,value))
    for i in range(6):add(f'U^{5-i} w^{i}',U**(5-i)*w**i)
    for i in range(3):add(f'U^{2-i} w^{i+1} U_x',U**(2-i)*w**(i+1)*x)
    for v,vname in [(U,'U'),(w,'w')]:
        for q,qname in [(x*x,'U_x²'),(x*y,'U_x w_x'),(y*y,'w_x²')]:add(vname+' '+qname,v*q)
    add('U_x w_xx',x*y.D())
    for q,qname in [(A,'A'),(B,'B')]:
        for i in range(4):add(f'U^{3-i} w^{i} '+qname,U**(3-i)*w**i*q)
        for v,vname in [(U,'U'),(w,'w')]:
            for der,dname in [(x,'U_x'),(y,'w_x')]:add(vname+' '+dname+' '+qname,v*der*q)
    for q,qname in [(A*A,'A²'),(A*B,'A B'),(B*B,'B²')]:
        for v,vname in [(U,'U'),(w,'w')]:add(vname+' '+qname,v*q)
    add('U_x A_x',x*A.D());add('w_x A_x',y*A.D());add('U_x B_x',x*B.D())
    quad=[(U*U,'U²'),(U*w,'Uw'),(w*w,'w²')]
    for i,(f,fn) in enumerate(quad):
        for g,gn in quad[i:]:add(fn+' K('+gn+')',f*g.D().R())
    return items

def sample(n,rng,h=F(1),time=True):
    l=[2**i for i in range(n-1)];l.append(-sum(l));rng.shuffle(l)
    k=[rng.randint(-3,4) for _ in range(n-1)];k.append(-sum(k))
    Poly.n=n; Poly.s=F(rng.choice([2,3,5]));Poly.h=h
    Poly.kval=[sum(k[i] for i in range(n) if m>>i&1) for m in range(1<<n)]
    Poly.lval=[sum(l[i] for i in range(n) if m>>i&1) for m in range(1<<n)]
    U=Poly({1<<i:F(rng.randint(-3,3)) for i in range(n)})
    w=Poly({1<<i:F(rng.randint(-3,3)) for i in range(n)})
    if time:
        Ut=-(U*U*F(1,2)+w*w*(h*h/32)+U.D()+w.D().R()).D()
        wt=-(U*w-w.D()).D()
        vals=basis(Dual(U,Ut),Dual(w,wt))
        return [v.b.trace() for _,v in vals],[n for n,_ in vals]
    vals=basis(U,w)
    return [v.trace() for _,v in vals],[n for n,_ in vals]

def main():
    rng=random.Random(20261005)
    rows=[];tracerows=[]
    for n in range(2,7):
        for _ in range(48):
            row,names=sample(n,rng);rows.append(row)
        if n<=5:
            for _ in range(64):
                row,_=sample(n,rng,time=False);tracerows.append(row)
    prime=2305843009213693951
    def modular_null(rr):
        a=[[v.numerator*pow(v.denominator,-1,prime)%prime for v in row] for row in rr]
        rank=0;piv=[]
        for j in range(len(a[0])):
            pick=next((i for i in range(rank,len(a)) if a[i][j]),None)
            if pick is None:continue
            a[rank],a[pick]=a[pick],a[rank]
            inv=pow(a[rank][j],-1,prime);a[rank]=[v*inv%prime for v in a[rank]]
            for i in range(len(a)):
                if i!=rank and a[i][j]:
                    f=a[i][j];a[i]=[(x-f*y)%prime for x,y in zip(a[i],a[rank])]
            piv.append(j);rank+=1
        null=[]
        from math import isqrt
        bound=isqrt(prime//2)
        def reconstruct(v):
            r0,r1=prime,v;t0,t1=0,1
            while abs(r1)>bound:
                q=r0//r1;r0,r1=r1,r0-q*r1;t0,t1=t1,t0-q*t1
            if not t1 or abs(t1)>bound:raise ValueError('reconstruction failed')
            return F(r1,t1)
        for j in range(len(a[0])):
            if j in piv:continue
            vec=[F(0)]*len(a[0]);vec[j]=F(1)
            for i,k in enumerate(piv):vec[k]=reconstruct(-a[i][j]%prime)
            assert all(sum(x*y for x,y in zip(row,vec))==0 for row in rr), 'exact verification failed'
            null.append(s.Matrix([s.Rational(v.numerator,v.denominator) for v in vec]))
        return rank,null
    rank,conserved=modular_null(rows);trank,zero=modular_null(tracerows)
    span=zero.copy();new=[]
    for v in conserved:
        if s.Matrix.hstack(*(span+[v])).rank()>len(span):span.append(v);new.append(v)
    out={'names':names,'rows':len(rows),'rank':rank,'trace_rank':trank,
         'null_dim':len(conserved),'zero_trace_dim':len(zero),
         'new_charges':[[str(v) for v in c] for c in new],
         'scope':'weight5; x derivative <=2 representatives; R only on D(linear/quadratic); at most 2 R factors'}
    print(json.dumps(out,indent=2))
    (BASE/'weight5_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')

if __name__=='__main__':main()
