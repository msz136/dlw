import sympy as sp
x,t,y,a = sp.symbols("x t y a", real=True)
p,q = sp.symbols("p q")
A,B = sp.symbols("A B")
P,Q = p-a, q+a
th = (p+q)*x + (q**2-p**2)*t + y/P + y/Q + A + B
A1 = -(P/Q)/(p+q); A0 = 1/(p+q)
f = 1 + A1*sp.exp(th); g = 1 + A0*sp.exp(th)
def Dx(F,G): 
    return sp.diff(F,x)*G - F*sp.diff(G,x)
def Dt(F,G):
    return sp.diff(F,t)*G - F*sp.diff(G,t)
def Dx2(F,G):
    return sp.diff(F,x,2)*G - 2*sp.diff(F,x)*sp.diff(G,x) + F*sp.diff(G,x,2)
Bfg = sp.expand(Dx2(f,g) + Dt(f,g) + 2*a*Dx(f,g))
print("B f.g =", sp.simplify(Bfg))
print("A1 =",sp.simplify(A1)," A0 =",sp.simplify(A0))
print("A1+A0 =",sp.simplify(A1+A0)," A1-A0 =",sp.simplify(A1-A0))
print("Dx2 =",sp.simplify(Dx2(f,g)))
print("Dt  =",sp.simplify(Dt(f,g)))
print("2aDx=",sp.simplify(2*a*Dx(f,g)))
