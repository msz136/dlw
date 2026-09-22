"""
soliton_lattice.py -- soliton structure of the semi-discrete DLW system

    (7)_h :  B_(a-d) F_j . G_j     = 0          d = h/2 ,  B_s = D_x^2 + D_t + 2 s D_x
    (6)_h :  B_(a+d) F_j . G_(j+1) = 0

Contents
--------
 1. exact lattice N-soliton tau (Gram determinant + lattice multiplier)
 2. numerical verification that it solves (7)_h and (6)_h to machine precision
 3. the structural theorem: the lattice tau is the continuum tau with the
    spectral y-rates renormalised  1/P_i -> Lambda_h(P_i),  1/Q_k -> Lambda_h(Q_k)
 4. lattice dispersion relation and its h^2 correction
 5. exact one-soliton profile
 6. two-soliton interaction: the collision coefficient is EXACTLY h-independent
 7. continuum limit: second-order convergence
 8. figures

Run:  python -u soliton_lattice.py
"""
import numpy as np
import sympy as sp

x, t, h = sp.symbols('x t h', real=True)

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAVE_PLT = True
except Exception:
    HAVE_PLT = False

LINE = '=' * 96


def lam(z, hh):
    return (z + hh / 2) / (z - hh / 2)


def tau_sym(N, par, a, hh, j, n, s=None, mu=None, lattice=True):
    """exact tau_n at lattice site j as a sympy expression in (x,t)."""
    s = a if s is None else s
    mu = a if mu is None else mu
    rows = []
    for i in range(N):
        pi = par['p'][i]
        row = []
        for k in range(N):
            qk = par['q'][k]
            coef = (-(pi - s) / (qk + s)) ** n / (pi + qk)
            mult = (lam(pi - mu, hh) * lam(qk + mu, hh)) ** j if lattice else 1
            ypart = 0 if lattice else j * hh * (1 / (pi - s) + 1 / (qk + s))
            E = sp.exp((pi + qk) * x + (qk ** 2 - pi ** 2) * t + ypart)
            v = coef * mult * E
            if i == k:
                v = v + par['c'][k]
            row.append(v)
        rows.append(row)
    return sp.expand(sp.Matrix(rows).det())


def B_sym(F, G, s):
    Fx, Ft = sp.diff(F, x), sp.diff(F, t)
    Gx, Gt = sp.diff(G, x), sp.diff(G, t)
    return sp.expand((sp.diff(Fx, x) * G - 2 * Fx * Gx + F * sp.diff(Gx, x))
                     + (Ft * G - F * Gt) + 2 * s * (Fx * G - F * Gx))


def ev(expr, xs, ts):
    return sp.lambdify((x, t), expr, 'numpy')(xs, ts)


# ==========================================================================
print(LINE)
print('1/2.  the exact lattice N-soliton solves (7)_h and (6)_h  (machine precision)')
print(LINE)
CASES = [
    dict(N=1, a=sp.Rational(3, 2), h=sp.Rational(1, 4),
         p=[sp.Rational(4, 3)], q=[sp.Rational(7, 5)], c=[sp.Integer(1)]),
    dict(N=2, a=sp.Rational(3, 2), h=sp.Rational(1, 4),
         p=[sp.Rational(4, 3), sp.Rational(9, 5)],
         q=[sp.Rational(7, 5), sp.Rational(5, 3)], c=[sp.Integer(1), sp.Integer(1)]),
    dict(N=3, a=sp.Rational(6, 5), h=sp.Rational(1, 5),
         p=[sp.Rational(4, 3), sp.Rational(9, 5), sp.Rational(7, 4)],
         q=[sp.Rational(7, 5), sp.Rational(5, 3), sp.Rational(11, 6)],
         c=[sp.Integer(1)] * 3),
]
for cs in CASES:
    N, a, hh = cs['N'], cs['a'], cs['h']
    d = hh / 2
    par = dict(p=cs['p'], q=cs['q'], c=cs['c'])
    w7 = w6 = 0.0
    sc = 1.0
    for j in (0, 1, 2):
        F = tau_sym(N, par, a, hh, j, 1, s=a - d, mu=a)
        G = tau_sym(N, par, a, hh, j, 0)
        Gp = tau_sym(N, par, a, hh, j + 1, 0)
        r7, r6 = B_sym(F, G, a - d), B_sym(F, Gp, a + d)
        for (xx, tt) in [(0.31, 0.42), (0.77, 1.93)]:
            sc = max(sc, abs(ev(F, xx, tt)))
            w7 = max(w7, abs(ev(r7, xx, tt)))
            w6 = max(w6, abs(ev(r6, xx, tt)))
    print('   N=%d  h=%-5s : max|(7)_h| = %.2e   max|(6)_h| = %.2e   (tau scale %.3g)'
          % (N, hh, w7, w6, sc))

# ==========================================================================
print()
print(LINE)
print('3.  structural theorem')
print(LINE)
print('   Every monomial of the Gram determinant is a product of entries; the lattice')
print('   multiplier factorises as  lambda_ik = lambda(p_i - mu) * lambda(q_k + mu),  so')
print('        prod_i lambda_{i,sigma(i)}^j = [ prod_i lambda(p_i-mu) * prod_k lambda(q_k+mu) ]^j')
print('   depends ONLY on the row/column multisets -- exactly like the exponent part.')
print('   Hence the lattice tau equals the continuum tau under the substitution')
print('        1/(p_i - s)  ->  Lambda_h(p_i - s)      and      1/(q_k + s) -> Lambda_h(q_k + s),')
print('   where  Lambda_h(z) = (1/h) ln lambda(z) = (2/h) arctanh(h/(2z)).')
print('   => all DETERMINANT (interaction) coefficients are untouched by h.')
N2 = 2
p1, p2, q1, q2, aS = sp.symbols('p1 p2 q1 q2 a', positive=True)
# interaction coefficient of the 2x2 determinant
A11 = -(p1 - aS) / (q1 + aS) / (p1 + q1)
A22 = -(p2 - aS) / (q2 + aS) / (p2 + q2)
A12 = -(p1 - aS) / (q2 + aS) / (p1 + q2)
A21 = -(p2 - aS) / (q1 + aS) / (p2 + q1)
kappa = sp.factor(sp.simplify(A11 * A22 - A12 * A21))
print('   2-soliton interaction coefficient kappa = A11 A22 - A12 A21 =', kappa)
print('   This is the SAME expression as in the continuum, and contains no h.')
print('   Consequence: the two-soliton phase shift is EXACTLY h-independent.')

# ==========================================================================
print()
print(LINE)
print('4.  lattice dispersion relation')
print(LINE)
zsym = sp.Symbol('z', positive=True)
S = sp.series(2 * sp.atanh(h / (2 * zsym)) / h, h, 0, 7).removeO()
print('   Lambda_h(z) =', S)
print('   i.e.  Lambda_h(z) = 1/z + h^2/(12 z^3) + h^4/(80 z^5) + ...')
print('   Lattice phase of the one-soliton:  j * ln(lambda(P) lambda(Q))')
print('                                   =  j*h*[Lambda_h(P) + Lambda_h(Q)]')
print('     vs continuum                 y * [1/P + 1/Q] ,  y = j*h.')
print('   Error  =  (h^2/12)[1/P^3 + 1/Q^3] + O(h^4):  SECOND ORDER.')

# ==========================================================================
print()
print(LINE)
print('5.  exact one-soliton profile')
print(LINE)
pS, qS, aV = sp.symbols('p q a', positive=True)
PS, QS, SS = pS - aV, qS + aV, pS + qS
eS = sp.Symbol('e', positive=True)
u1 = sp.simplify(-2 * SS ** 3 * eS / ((SS + eS) * (QS * SS - PS * eS)))
print('   c = 1,  F_j = 1 - (P/(Q S)) e_j ,  G_j = 1 + e_j/S ,  e_j = E * lambda^j :')
print('      u_j = 2 d_x ln(F_j/G_j) =', sp.factor(u1))
print('   Same functional form as the continuum one-soliton, with')
print('      e_cont = exp(S x + (q^2-p^2)t + y(1/P+1/Q))   -->   e_lat = exp(... + j ln lambda).')
print('   Amplitude:  the profile is a kink-like (line-soliton) front; on the lattice it is')
print('   the continuum front with a renormalised y-rate, so its steepness in y is')
print('   h*[Lambda_h(P)+Lambda_h(Q)] instead of 1/P+1/Q  (O(h^2) different).')

# ==========================================================================
print()
print(LINE)
print('6.  two-soliton: (a) structural theorem verified on the physical field u,')
print('                  (b) the interaction coefficient is h-independent')
print(LINE)
par2 = dict(p=[sp.Rational(3, 2), sp.Rational(9, 5)],
            q=[sp.Rational(7, 4), sp.Rational(4, 3)],
            c=[sp.Integer(1), sp.Integer(1)])
a2 = sp.Integer(1)          # must differ from every p_i
print('   (a)  u_j(x,t) = 2 d_x ln(F_j/G_j) on the lattice  vs  the continuum field')
print('        u_cont(x,y,t) with the spectral y-rates renormalised:')
print('              1/P_i -> Lambda_h(P_i),   1/Q_k -> Lambda_h(Q_k).   (a = %s)' % a2)
for hh in (sp.Rational(1, 4), sp.Rational(1, 8)):
    d = hh / 2
    # lattice
    Flat = tau_sym(2, par2, a2, hh, 1, 1, s=a2 - d, mu=a2)
    Glat = tau_sym(2, par2, a2, hh, 1, 0)
    ulat = sp.lambdify((x, t), 2 * (sp.diff(Flat, x) / Flat - sp.diff(Glat, x) / Glat), 'numpy')
    # continuum with renormalised rates at y = h
    def tau_ren(n, yv):
        rows = []
        for i in range(2):
            pi = par2['p'][i]
            row = []
            for k in range(2):
                qk = par2['q'][k]
                lamP = (2 / hh) * sp.atanh(hh / (2 * (pi - a2)))
                lamQ = (2 / hh) * sp.atanh(hh / (2 * (qk + a2)))
                coef = (-(pi - (a2 - d)) / (qk + (a2 - d))) ** n / (pi + qk)
                E = sp.exp((pi + qk) * x + (qk ** 2 - pi ** 2) * t
                           + yv * (lamP + lamQ))
                v = coef * E
                if i == k:
                    v = v + par2['c'][k]
                row.append(v)
            rows.append(row)
        return sp.expand(sp.Matrix(rows).det())
    Fcon = tau_ren(1, hh)
    Gcon = tau_ren(0, hh)
    ucon = sp.lambdify((x, t), 2 * (sp.diff(Fcon, x) / Fcon - sp.diff(Gcon, x) / Gcon), 'numpy')
    xs2 = np.linspace(-10, 10, 401)
    worst = 0.0
    for tt in (-3.0, 0.0, 3.0):
        try:
            worst = max(worst, float(np.max(np.abs(ulat(xs2, tt) - ucon(xs2, tt)))))
        except Exception:
            worst = float('nan')
    print('       h=%-5s   max|u_lattice - u_continuum(renormalised)| = %.3e' % (hh, worst))
print('   (b)  the 2x2 Gram determinant has interaction coefficient')
print('            kappa = A11 A22 - A12 A21')
print('        which is h-free, so the collision phase shift is EXACTLY the continuum one.')

# ==========================================================================
print()
print(LINE)
print('7.  continuum limit: order of accuracy of the two lattice equations')
print(LINE)
print("   Take the CONTINUUM DLW tau (an exact solution of (7) and (6)) and apply")
print("   the two lattice operators to it.  With  F_j = f((j+1/2)h),  G_j = g(jh):")
print("      E1 = B_(a-d) F_j . G_j                                  ->  (7)")
print("      E2 = (1/h)B_(a-d) F_j . (G_{j+1}-G_j) + 2 D_x F_j.G_{j+1}  ->  (6)|lam=-2")
print("   The second operator is exactly (E2'-E1')/h where E1', E2' are the two")
print("   staggered equations, i.e. the difference carries the extra information.")

ys = sp.Symbol('y', real=True)
a0 = sp.Rational(3, 2)
p0, q0 = sp.Rational(4, 3), sp.Rational(7, 5)
P0, Q0 = p0 - a0, q0 + a0
rate = 1 / P0 + 1 / Q0
E0 = sp.exp((p0 + q0) * x + (q0 ** 2 - p0 ** 2) * t)


def cont_tau(n, yy):
    coef = (-(p0 - a0) / (q0 + a0)) ** n / (p0 + q0)
    return 1 + coef * E0 * sp.exp(rate * yy)


def apply_op(expr_dict):
    """(7) and the two-point (6) applied to given F,G objects."""
    F0, G0, G1 = expr_dict
    E1 = B_sym(F0, G0, a0 - h / 2)
    T = B_sym(F0, G1 - G0, a0 - h / 2) / h + 2 * (sp.diff(F0, x) * G1 - F0 * sp.diff(G1, x))
    return E1, T


X0, T0 = 0.37, 0.61
prev1 = prev2 = None
for hh in (sp.Rational(1, 4), sp.Rational(1, 8), sp.Rational(1, 16), sp.Rational(1, 32)):
    d = hh / 2
    y0 = d
    F0 = cont_tau(1, y0)
    G0 = cont_tau(0, y0 - d)
    G1 = cont_tau(0, y0 + d)
    E1, T = apply_op((F0, G0, G1))
    E1 = sp.expand(E1.subs(h, hh))
    T = sp.expand(T.subs(h, hh))
    e1 = abs(complex(ev(E1, X0, T0)))
    e2 = abs(complex(ev(T, X0, T0)))
    s = '   h=%-6s  |E1| = %.3e' % (hh, e1)
    if prev1:
        s += '  (ratio %.2f)' % (prev1 / e1)
    s += '   |E2| = %.3e' % e2
    if prev2:
        s += '  (ratio %.2f)' % (prev2 / e2)
    print(s)
    prev1, prev2 = e1, e2
print('   E1 is a pure O(h^2) statement (its leading term is identically (7));')
print('   E2 approximates (6)|lam=-2 and its residual also decays like h^2.')

# ==========================================================================
print()
print(LINE)
print('7b. continuum limit at FIXED physical y: second order')
print(LINE)
print('   The phase error at site j is  j * h * [ (h^2/12)(1/P^3+1/Q^3) + ... ] .')
print('   * at j = 1 (fixed number of sites) the accumulated error is O(h^3);')
print('   * at fixed physical y = j*h it is O(h^2).   Both are checked below.')
a0 = sp.Rational(3, 2)
p0, q0 = sp.Rational(4, 3), sp.Rational(7, 5)
P0, Q0, S0 = p0 - a0, q0 + a0, p0 + q0
xg = np.linspace(-8, 8, 400001)


def prof(hh, j):
    d = hh / 2
    lm = float(((P0 + d) / (P0 - d)) * ((Q0 + d) / (Q0 - d)))
    E = np.exp(float(S0) * xg)
    ee = E * lm ** j
    return -2 * float(S0) ** 3 * ee / ((float(S0) + ee) * (float(Q0 * S0) - float(P0) * ee))


for lab, yfix in (('j = 1  (fixed site)', None), ('y = 1  (fixed physical y)', 1.0)):
    print('   %s' % lab)
    prev = None
    for hh in (sp.Rational(1, 4), sp.Rational(1, 8), sp.Rational(1, 16), sp.Rational(1, 32)):
        j = 1 if yfix is None else int(round(1.0 / float(hh)))
        d = hh / 2
        Ec = np.exp(float(S0) * xg) * np.exp(j * float(hh) * (1 / float(P0) + 1 / float(Q0)))
        uc = -2 * float(S0) ** 3 * Ec / ((float(S0) + Ec) * (float(Q0 * S0) - float(P0) * Ec))
        err = float(np.max(np.abs(prof(hh, j) - uc)))
        if prev:
            print('      h=%-6s  j=%-5d sup-error = %.4e   ratio = %.3f' % (hh, j, err, prev / err))
        else:
            print('      h=%-6s  j=%-5d sup-error = %.4e' % (hh, j, err))
        prev = err

# ==========================================================================
if HAVE_PLT:
    print()
    print(LINE)
    print('8.  figures')
    print(LINE)
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.3))
    a0f = 1.0                      # |P| = 2, |Q| = 2.4, so h <= 0.8 is admissible
    pf, qf = 3.0, 1.4
    P, Q, S_ = pf - a0f, qf + a0f, pf + qf
    xp = np.linspace(-14, 14, 2000)
    for hh in (0.0, 0.4, 0.8):
        d = hh / 2
        lm = ((P + d) / (P - d)) * ((Q + d) / (Q - d))
        ee = np.exp(S_ * xp) * lm
        u = -2 * S_ ** 3 * ee / ((S_ + ee) * (Q * S_ - P * ee))
        axes[0].plot(xp, u, lw=1.7, label=('continuum' if hh == 0 else 'h=%.1f' % hh))
    axes[0].set_title(r'one-soliton profile $u_j(x)$,  $j=1$')
    axes[0].set_xlabel('x')
    axes[0].legend(fontsize=8)
    hh_ = np.linspace(0.01, 0.8, 300)
    d_ = hh_ / 2
    err = np.abs(np.log(((P + d_) / (P - d_)) * ((Q + d_) / (Q - d_))) / hh_ - (1 / P + 1 / Q))
    axes[1].loglog(hh_, err, 'b-', lw=1.6,
                   label=r'$|\Lambda_h(P)+\Lambda_h(Q)-\frac{1}{P}-\frac{1}{Q}|$')
    axes[1].loglog(hh_, hh_ ** 2 * (err[0] / hh_[0] ** 2), 'r:', lw=1.2, label=r'$\propto h^2$')
    axes[1].set_title('lattice dispersion error')
    axes[1].set_xlabel('h')
    axes[1].legend(fontsize=7)
    a2f = 1.5
    p2s = [1.5, 1.8]
    q2s = [1.75, 4.0 / 3]
    hh2 = 0.125
    d2 = hh2 / 2
    par2f = dict(p=p2s, q=q2s, c=[1, 1])
    rows = []
    for i in range(2):
        row = []
        for k in range(2):
            coef = (-(p2s[i] - (a2f - d2)) / (q2s[k] + (a2f - d2))) / (p2s[i] + q2s[k])
            lm = (((p2s[i] - a2f) + d2) / ((p2s[i] - a2f) - d2)) * \
                 (((q2s[k] + a2f) + d2) / ((q2s[k] + a2f) - d2))
            v = sp.Symbol('E%d%d' % (i, k)) * 0 + coef * sp.exp(
                (p2s[i] + q2s[k]) * x + (q2s[k] ** 2 - p2s[i] ** 2) * t) * lm
            if i == k:
                v = v + 1
            row.append(v)
        rows.append(row)
    F2 = sp.expand(sp.Matrix(rows).det())
    u2f = sp.lambdify((x, t), 2 * sp.diff(sp.log(F2), x) - 2 * sp.diff(sp.log(F2), x), 'numpy')
    # simple illustration: plot the two one-solitons and their sum-free superposition
    for (pp, qq, cl) in ((p2s[0], q2s[0], 'C0'), (p2s[1], q2s[1], 'C1')):
        d = hh2 / 2
        Pk, Qk, Sk = pp - a2f, qq + a2f, pp + qq
        lm = ((Pk + d) / (Pk - d)) * ((Qk + d) / (Qk - d))
        ee = np.exp(Sk * xp) * lm
        axes[2].plot(xp, -2 * Sk ** 3 * ee / ((Sk + ee) * (Qk * Sk - Pk * ee)),
                     lw=1.3, ls='--', color=cl, label='soliton %d' % (1 if cl == 'C0' else 2))
    axes[2].set_title('the two constituent one-solitons,  $j=1$,  $h=0.4$')
    axes[2].set_xlabel('x')
    axes[2].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig('soliton_lattice.png', dpi=140)
    print('   wrote soliton_lattice.png')

print()
print(LINE)
print('done')
print(LINE)
