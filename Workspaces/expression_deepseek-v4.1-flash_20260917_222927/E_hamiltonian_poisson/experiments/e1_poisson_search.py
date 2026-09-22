import sympy as sp, random, os
OUT = r"C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\E_hamiltonian_poisson\experiments"
os.makedirs(OUT, exist_ok=True)

def build(n):
    w = sp.Matrix(sp.symbols(f'w0:{n}'))
    v = sp.Matrix(sp.symbols(f'v0:{n}'))
    a, lam = sp.symbols('a lam')
    C = sp.Matrix(n, n, lambda i, j: 1 if j < i else 0)   # discrete d_y^{-1}: cumsum
    u = C * w
    B = sp.diag(*[u[i] + 2*a for i in range(n)])
    W = sp.diag(*list(w))
    A = B + W * C
    E = sp.diag(*[v[i] + 2*lam for i in range(n)]) * C
    return w, v, a, lam, C, A, B, E, W

print("="*72)
print("E1  general CONSTANT symmetric Q (2n x 2n) : Helmholtz blocks")
print("    S1: A Q11 = Q11 A^T     S2: Q12^T = -Q12    S3: Q22 = Q11")
print("    S4: A Q12 = Q11 E^T + Q12 B    S5: E Q12 + B Q11 + Q12 E^T - Q11 B = 0")
for n in (2, 3):
    w, v, a, lam, C, A, B, E, W = build(n)
    P11 = sp.Matrix(n, n, lambda i, j: sp.Symbol(f'p{i}_{j}'))
    P12 = sp.Matrix(n, n, lambda i, j: sp.Symbol(f'r{i}_{j}'))
    eqs = list(A*P11 - P11*A.T) + list(P12 + P12.T) + list(A*P12 - P11*E.T - P12*B) + list(E*P12 + B*P11 + P12*E.T - P11*B)
    syms = list(P11) + list(P12)
    for seed in (7, 11):
        random.seed(seed)
        sub = {a: sp.Rational(1), lam: sp.Rational(-2)}
        for i in range(n):
            sub[w[i]] = sp.Rational(random.randint(1, 9))
            sub[v[i]] = sp.Rational(random.randint(1, 9))
        eqsn = [sp.expand(e.subs(sub)) for e in eqs]
        sol = sp.linsolve(eqsn, syms)
        print(f"  n={n} seed={seed}: Q11={dict(sub)}")
        print(f"       solution set = {sol}")

print("="*72)
print("E2  Theta := diag(w)C - C^T diag(w) = A - A^T ; skew + entry formula")
for n in (2, 3, 4):
    w, v, a, lam, C, A, B, E, W = build(n)
    Th = W*C - C.T*W
    print(f"  n={n}: Theta == A - A^T : {sp.simplify(Th - (A - A.T)) == sp.zeros(n,n)}",
          f"| skew: {sp.simplify(Th + Th.T) == sp.zeros(n,n)}",
          f"| entry w_i C_ij - w_j C_ji: {all(sp.simplify(Th[i,j]-(w[i]*C[i,j]-w[j]*C[j,i]))==0 for i in range(n) for j in range(n))}")
    Thsub = Th.subs({w[i]: sp.Rational(1+i) for i in range(n)})
    print(f"       Theta at w=(1,2,..): {Thsub.tolist()}  nonzero={Thsub != sp.zeros(n,n)}")

print("="*72)
print("E3  class Q = q*I_n : D_x^0 / D_x^1 coefficient matching")
for n in (2, 3):
    w, v, a, lam, C, A, B, E, W = build(n)
    q11, q12, q22 = sp.symbols('q11 q12 q22')
    print(f"  n={n}: A - A^T != 0 : {sp.simplify(A - A.T) != sp.zeros(n,n)}")
    print(f"       E - E^T != 0 : {sp.simplify(E - E.T) != sp.zeros(n,n)}")
    print(f"       A - A^T = diag(w)C + C diag(w) : {sp.simplify((A-A.T) - (W*C + C*W)) == sp.zeros(n,n)}")

print("="*72)
print("E4  zero-mode locus v_j = -2*lam : E - E^T vanishes, Theta does not")
for n in (3,):
    w, v, a, lam, C, A, B, E, W = build(n)
    sub = {v[i]: -2*lam for i in range(n)}
    print(f"  n={n}: (E - E^T) at zero mode == 0 : {sp.simplify((E-E.T).subs(sub)) == sp.zeros(n,n)}")
    print(f"       Theta at zero mode != 0 (w=(1,2,3)) : {sp.simplify((A-A.T).subs({w[i]: sp.Rational(1+i) for i in range(n)})) != sp.zeros(n,n)}")
    print(f"       Theta at w==0 : {sp.simplify((A-A.T).subs({w[i]: 0 for i in range(n)})) == sp.zeros(n,n)}")
print("DONE")
