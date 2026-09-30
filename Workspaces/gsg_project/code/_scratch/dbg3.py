import sympy as sp
x,t,y,a=sp.symbols("x t y a",real=True)
p1,q1,A1s,B1s=sp.symbols("p1 q1 A1 B1")
Pi,Qk=p1-a,q1+a
th=(p1+q1)*x+(q1**2-p1**2)*t+y/Pi+y/Qk+A1s+B1s
A1=-(Pi/Qk)/(p1+q1); A0=1/(p1+q1)
raw = 1 + sp.exp(th)*(-Pi/Qk)/(p1+q1)
g_raw = 1 + sp.exp(th)/(p1+q1)
f_raw = sp.expand(raw); g_raw=sp.expand(g_raw)
def Dx(F,G,v="x"): return sp.diff(F,v)*G-F*sp.diff(G,v)
def Bop(F,G):
    return (sp.diff(F,x,2)*G-2*sp.diff(F,x)*sp.diff(G,x)+F*sp.diff(G,x,2))+Dx(F,G,"t")+2*a*Dx(F,G)
for tag,(F,G) in {"no-expand":(raw,g_raw),"expanded":(sp.expand(raw),sp.expand(g_raw))}.items():
    e=sp.expand(Bop(F,G))
    print(tag,"->", sp.simplify(e))
    vals={x:sp.Rational(3,7),t:sp.Rational(2,5),y:sp.Rational(1,3),a:sp.Rational(1,4),
          p1:sp.Rational(6,5),q1:sp.Rational(7,10),A1s:sp.Rational(1,9),B1s:sp.Rational(2,11)}
    print("   numeric:", sp.N(e.subs(vals),20))
