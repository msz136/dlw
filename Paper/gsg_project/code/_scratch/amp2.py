import sympy as sp
p,q,a = sp.Integer(1), sp.Integer(2), sp.Integer(3)
P,Q=p-a,q+a
E0=sp.sqrt(-Q/P); u0=-2*E0*(p+q)**2/((1+E0)*(Q-P*E0))
prev=None
for k in range(1,9):
    h=sp.Rational(1,2**k); d=h/2
    E=sp.sqrt(-(Q-d)/(P+d))
    u=-2*E*(p+q)**2/((1+E)*((Q-d)-(P+d)*E))
    dev=abs(float((u-u0)/u0))
    r = "" if prev is None else f"  ratio={dev/prev:.4f}"
    print(f"h=1/{2**k:<4d} dev={dev:.6e}{r}")
    prev=dev
