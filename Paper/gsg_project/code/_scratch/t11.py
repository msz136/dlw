import sympy as sp, random
x,y,t = sp.symbols("x y t")
def bil(f,g,ax=0,ay=0,at=0):
    from math import comb
    tot=0
    for p in range(ax+1):
        for q in range(ay+1):
            for r in range(at+1):
                co=(-1)**(p+q+r)*comb(ax,p)*comb(ay,q)*comb(at,r)
                tot += co*sp.diff(f,x,ax-p,y,ay-q,t,at-r)*sp.diff(g,x,p,y,q,t,r)
    return sp.expand(tot)
def Bop(f,g,a): return sp.expand(bil(f,g,2,0,0)+bil(f,g,0,0,1)+2*a*bil(f,g,1,0,0))
def DyB(f,g,a): return sp.expand(bil(f,g,2,1,0)+bil(f,g,0,1,1)+2*a*bil(f,g,1,1,0))
def zero(e):
    e=sp.together(sp.expand(e)); num,den=sp.fraction(e); return sp.expand(num)==0
def tau(n,ps,qs,cs,a,xis,etas):
    N=len(ps); M=sp.zeros(N,N)
    for i in range(N):
        for j in range(N):
            xi=ps[i]*x-ps[i]**2*t+y/(ps[i]-a)+xis[i]
            eta=qs[j]*x+qs[j]**2*t+y/(qs[j]+a)+etas[j]
            M[i,j]=cs[j]*(1 if i==j else 0)+(-(ps[i]-a)/(qs[j]+a))**n*sp.exp(xi+eta)/(ps[i]+qs[j])
    return sp.expand(M.det())
tests=[([3,5],[2,4],7),([4,1],[14,8],18),([6,9],[1,3],4),([2,8],[5,7],11)]
for ps,qs,a in tests:
    ps=[sp.Integer(v) for v in ps]; qs=[sp.Integer(v) for v in qs]; a=sp.Integer(a)
    cs=[sp.Integer(1)]*2; xis=[sp.Integer(1)]*2; etas=[sp.Integer(2)]*2
    f=tau(1,ps,qs,cs,a,xis,etas); g=tau(0,ps,qs,cs,a,xis,etas)
    print(f"p={ps} q={qs} a={a}: eq7={zero(Bop(f,g,a))}  eq6(lam=-2)={zero(sp.expand(DyB(f,g,a)-4*bil(f,g,1,0,0)))}", flush=True)
