import sympy as sp
x,t,y,h,a,lam = sp.symbols("x t y h a lam", real=True)
j = sp.symbols("j", integer=True)
def build_tau(N, nval, mode, cvals=None):
    p=[sp.Symbol(f"p{i+1}") for i in range(N)]
    q=[sp.Symbol(f"q{i+1}") for i in range(N)]
    xi0=[sp.Symbol(f"A{i+1}") for i in range(N)]
    et0=[sp.Symbol(f"B{i+1}") for i in range(N)]
    if cvals is None: cvals=[1]*N
    M=sp.zeros(N,N)
    for i in range(N):
        for k in range(N):
            Pi,Qk=p[i]-a,q[k]+a
            xi=-p[i]**2*t+xi0[i]; et=q[k]**2*t+et0[k]
            if mode=="cont":
                xi+=p[i]*x+y/Pi; et+=q[k]*x+y/Qk
            M[i,k]=(cvals[k] if i==k else 0)+sp.exp(xi+et)*(-Pi/Qk)**nval/(p[i]+q[k])
    return sp.expand(M.det()),p,q
f,_,_ = build_tau(1,1,"cont"); g,_,_ = build_tau(1,0,"cont")
print("f =",f); print("g =",g)
def Dx(F,G,v="x"): return sp.diff(F,v)*G-F*sp.diff(G,v)
def Bop(F,G,aa):
    return (sp.diff(F,x,2)*G-2*sp.diff(F,x)*sp.diff(G,x)+F*sp.diff(G,x,2))+Dx(F,G,"t")+2*aa*Dx(F,G)
e=sp.expand(Bop(f,g,a))
print("B f.g =",sp.simplify(e))
print("check A1:", sp.simplify(sp.diff(f,sp.Symbol("x"))))
