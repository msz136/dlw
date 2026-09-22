import sympy as sp, random, os
OUT = r"C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\E_hamiltonian_poisson\experiments"
os.makedirs(OUT, exist_ok=True)

def mats(n, C, w, v, a, lam):
    u = C * w
    B = sp.diag(*[u[i] + 2*a for i in range(n)])
    W = sp.diag(*list(w))
    A = B + W * C
    E = sp.diag(*[v[i] + 2*lam for i in range(n)]) * C
    return A, B, E, W

def helm_solve(n, Cbuild, tag, symbolic=False, seed=7):
    w = sp.Matrix(sp.symbols(f'w0:{n}')); v = sp.Matrix(sp.symbols(f'v0:{n}'))
    a, lam = sp.symbols('a lam')
    C = Cbuild(n, w)
    A, B, E, W = mats(n, C, w, v, a, lam)
    P11 = sp.Matrix(n, n, lambda i, j: sp.Symbol(f'p{i}_{j}'))
    P12 = sp.Matrix(n, n, lambda i, j: sp.Symbol(f'r{i}_{j}'))
    eqs = list(A*P11 - P11*A.T) + list(P12 + P12.T) + list(A*P12 - P11*E.T - P12*B) + list(E*P12 + B*P11 + P12*E.T - P11*B)
    syms = list(P11) + list(P12)
    if symbolic:
        sol = sp.solve(eqs, syms, dict=True)
        print(f"  [{tag}] n={n} SYMBOLIC solution: {sol}")
        return
    random.seed(seed)
    sub = {a: sp.Rational(1), lam: sp.Rational(-2)}
    for i in range(n):
        sub[w[i]] = sp.Rational(random.randint(1, 9)); sub[v[i]] = sp.Rational(random.randint(1, 9))
    sol = sp.linsolve([sp.expand(e.subs(sub)) for e in eqs], syms)
    tup = list(sol)[0]
    Q11 = sp.Matrix(n, n, lambda i, j: tup[i*n+j])
    Q12 = sp.Matrix(n, n, lambda i, j: tup[n*n + i*n + j])
    Q = sp.Matrix(sp.BlockMatrix([[Q11, Q12],[Q12.T, Q11]]))
    print(f"  [{tag}] n={n} seed={seed} w={[sub[w[i]] for i in range(n)]} v={[sub[v[i]] for i in range(n)]}")
    print(f"       sol space dim (free params) = {sum(1 for e in tup if e.free_symbols)}  Q11={Q11.tolist()} Q12={Q12.tolist()}")
    print(f"       Q invertible? det={sp.simplify(Q.det())}   -> invertible = {sp.simplify(Q.det())!=0}")

circ = lambda n, w: sp.Matrix(n, n, lambda i, j: (1 if (j-i) % n == 1 else (-1 if (i-j) % n == 1 else 0)))
cum  = lambda n, w: sp.Matrix(n, n, lambda i, j: 1 if j < i else 0)
# general antisymmetric C with free entries (strict upper part free)
genasym = lambda n, w: sp.Matrix(n, n, lambda i, j: sp.Symbol(f'c{i}_{j}') if i < j else (-sp.Symbol(f'c{j}_{i}') if j < i else 0))

print("="*72); print("E5  antisymmetric discrete d_y^{-1} (periodic circulant)")
for n in (3, 4):
    helm_solve(n, circ, 'circulant-asym', seed=7)
    helm_solve(n, circ, 'circulant-asym', seed=11)

print("="*72); print("E6  general (free-entry) antisymmetric C, n=2 and n=3")
for n in (2, 3):
    helm_solve(n, genasym, 'general-asym', seed=7)

print("="*72); print("E7  cumsum convention: unique solution is SINGULAR")
for n in (3, 4):
    helm_solve(n, cum, 'cumsum', seed=7)

print("="*72); print("E8  fully symbolic check (n=2, general antisymmetric C, symbolic w,v,a,lam)")
helm_solve(2, genasym, 'general-asym-SYM', symbolic=True)
print("DONE")
