import sympy as sp
p,q,a = sp.Integer(1), sp.Integer(2), sp.Integer(3)
for h in (sp.Integer(0), sp.Rational(1,4), sp.Rational(1,2), 1):
    d=h/2; P=p-a; Q=q+a
    E=sp.sqrt(-(Q-d)/(P+d))
    u=-2*E*(p+q)**2/((1+E)*((Q-d)-(P+d)*E))
    u0=-2*sp.sqrt(-Q/P)*(p+q)**2/((1+sp.sqrt(-Q/P))*(Q-P*sp.sqrt(-Q/P)))
    print(f"h={h}  E_cr={sp.N(E,10)}  u_max={sp.N(u,10)}  dev={sp.N((u-u0)/u0*100,4)}%")
