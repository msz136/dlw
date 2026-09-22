import sympy as sp
from engine import DLW, random_point

# 1) does my determinant expansion agree with sympy Matrix.det ?
for kind in ("none",):
    m = DLW(2, kind=kind)
    pt = random_point(m, seed=7)
    m.set_point(pt)
    p,q,a,c = m.p, m.q, m.a, m.c
    for n in (0,1):
        Ms = sp.zeros(2,2)
        for i in range(2):
            for j in range(2):
                off = (-(p[i]-a)/(q[j]+a))**n/(p[i]+q[j])   # E_ij coefficient
                Ms[i,j] = (c[j] if i==j else 0) + off
        # my tau: substitute coefficient product into E monomials
        t = m.tau(n)
        # reconstruct expression from dict by naming E symbols
        Es = {}
        expr = 0
        for key,coef in t.items():
            term = coef
            for (i,j) in key:
                Es.setdefault((i,j), sp.Symbol(f"E{i}{j}"))
                term *= Es[(i,j)]
            expr += term
        ref = Ms[0,0]*Ms[1,1] - Ms[0,1]*Ms[1,0]
        refsub = ref.subs({sp.Symbol(f"E{i}{j}"):1 for i in range(2) for j in range(2)})
        # E symbols are not in Ms; compare after projecting: tau should be
        # det with off-diagonals = coef*E
        Mine = 0
        for key,coef in t.items():
            term = coef
            for (i,j) in key:
                term *= sp.Symbol(f"E{i}{j}")
            Mine += term
        Ref = sp.expand(Ms[0,0]*Ms[1,1]-Ms[0,1]*Ms[1,0])
        # write Ref in the same form
        R2 = sp.expand(Ref.subs({Ms[0,1]: Ms[0,1], }))
        print("n=",n," my monomials:", sorted(t.keys()))
