import sympy as sp
P,Q,h = sp.symbols('P Q h', positive=True)
lam = ((P+h/2)/(P-h/2))*((Q+h/2)/(Q-h/2))
diff = sp.log(lam)/h - (1/P+1/Q)
print("h^0:", sp.simplify(diff.subs(h,0)))
print("h^1:", sp.simplify(sp.diff(diff,h).subs(h,0)))
print("h^2:", sp.simplify(sp.diff(diff,h,2).subs(h,0)/2))
print("h^3:", sp.simplify(sp.diff(diff,h,3).subs(h,0)/6))
