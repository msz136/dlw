import sympy as sp

x, y, t, a = sp.symbols('x y t a')
# random-ish smooth A, B
A = sp.Integer(3)*x**3*y + 2*x*y**2*t + sp.Integer(5)*y*t**2 + x*t + 7*y + 2
B = sp.Integer(2)*x**2*y**2 + 3*x*y*t + t**3 + x**2 + 4*y**2 + 3*t

d = lambda F, *v: sp.diff(F, *v)
R = d(A, x, 2) + d(B, x)**2 + d(B, t) + 2*a*d(B, x)
S_mine = (d(A, x, 2, y) - d(B, x, 2, y) - d(A, y, t) + d(B, y, t)
          - 2*d(B, x)*(d(A, x, y) - d(B, x, y))
          - 2*a*(d(A, x, y) - d(B, x, y)) + 4*d(B, x))
E2_mine = (d(A, y) - d(B, y))*R + S_mine

beta_y = (d(A, y) - d(B, y))/2
alpha = (A + B)/2
So = alpha + beta_y
Do = alpha - beta_y
E2_old = beta_y*(d(So, x, 2) + d(Do, x)**2 + d(Do, t) + 2*a*d(Do, x)) + 2*d(B, x)

diff = sp.simplify(E2_mine - E2_old)
print("E2_mine - E2_old simplifed ->", sp.factor(sp.expand(diff)))
print("is zero?", sp.simplify(diff) == 0)

# also: the fully honest identity for the second hypothesis, at the cbil level
# 2*S_mine = 2*(2*q_y*R + 2*e + 4*B_x) check: c02S = 2e + 4 B_x with e as below
q_y = (d(A, y) - d(B, y))/2
e = (d(A, x, 2, y) - d(B, x, 2, y) - d(A, y, t) + d(B, y, t))/2 \
    - d(B, x)*(d(A, x, y) - d(B, x, y)) - a*(d(A, x, y) - d(B, x, y))
print("S_mine - (2e + 4 B_x) =", sp.simplify(S_mine - (2*e + 4*d(B, x))))
print("E2_mine - 2*(q_y*R + e + 2*B_x) =",
      sp.simplify(E2_mine - 2*(q_y*R + e + 2*d(B, x))))
