import sympy as sp
from engine import DLW, random_point

x,y,t = sp.symbols("x y t")

def tau_sympy(n, ps, qs, cs, a, xis, etas):
    N=len(ps); M=sp.zeros(N,N)
    for i in range(N):
        for j in range(N):
            xi = ps[i]*x - ps[i]**2*t + y/(ps[i]-a) + xis[i]
            eta = qs[j]*x + qs[j]**2*t + y/(qs[j]+a) + etas[j]
            M[i,j] = cs[j]*(1 if i==j else 0) + (-(ps[i]-a)/(qs[j]+a))**n*sp.exp(xi+eta)/(ps[i]+qs[j])
    return sp.expand(M.det())

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

for N in (1,2):
    ps=[sp.Integer(3),sp.Integer(5)][:N]; qs=[sp.Integer(2),sp.Integer(4)][:N]
    cs=[sp.Integer(1)]*N; a=sp.Integer(7)
    xis=[sp.Integer(1)]*N; etas=[sp.Integer(2)]*N
    f=tau_sympy(1,ps,qs,cs,a,xis,etas); g=tau_sympy(0,ps,qs,cs,a,xis,etas)
    e7=zero(Bop(f,g,a)); e6=zero(sp.expand(DyB(f,g,a)-4*bil(f,g,1,0,0)))
    print(f"N={N}  p={ps} q={qs} a={a}:  eq7={e7}  eq6(lam=-2)={e6}")
    if N==2 and not e7:
        r=sp.together(sp.expand(Bop(f,g,a)))
        num,den=sp.fraction(r)
        print("   numerator terms:", len(sp.Add.make_args(sp.expand(num))))
        print("   num=", sp.expand(num))
