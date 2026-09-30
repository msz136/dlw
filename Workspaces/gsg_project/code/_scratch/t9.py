import sympy as sp
from engine import DLW

x,y,t = sp.symbols("x y t")
ps=[sp.Integer(3),sp.Integer(5)]; qs=[sp.Integer(2),sp.Integer(4)]; a=sp.Integer(7)
cs=[sp.Integer(1)]*2; xis=[sp.Integer(1)]*2; etas=[sp.Integer(2)]*2
N=2
m = DLW(N, kind="none")
m.set_point({m.p[0]:ps[0], m.p[1]:ps[1], m.q[0]:qs[0], m.q[1]:qs[1], m.a:a})
for n in (0,1):
    t_ = m.tau(n)
    print("engine tau n=",n, "monomials", len(t_), "coeffs")
    for k,c in t_.items(): print("   ", k, "->", c)

def eval_dict(d, xv, yv, tv):
    tot=0
    for key,coef in d.items():
        term=coef
        for (i,j) in key:
            xi = ps[i]*xv - ps[i]**2*tv + yv/(ps[i]-a) + xis[i]
            eta= qs[j]*xv + qs[j]**2*tv + yv/(qs[j]+a) + etas[j]
            term *= sp.exp(xi+eta)
        tot += term
    return sp.nsimplify(sp.expand(tot))

f_e = m.tau(1); g_e = m.tau(0)
B_e = m.B(f_e, g_e)
DyB_e = m.DyB(f_e, g_e)
Dx_e = m.Dx(f_e, g_e)
xv,yv,tv = sp.Rational(1,3), sp.Rational(1,5), sp.Rational(1,7)
print("engine   B f.g @pt =", sp.N(eval_dict(B_e,xv,yv,tv),30))
print("engine  DyB f.g @pt =", sp.N(eval_dict(DyB_e,xv,yv,tv),30))
print("engine   Dx f.g @pt =", sp.N(eval_dict(Dx_e,xv,yv,tv),30))
print("engine  DyB-4Dx @pt =", sp.N(eval_dict(DyB_e,xv,yv,tv)-4*eval_dict(Dx_e,xv,yv,tv),30))
