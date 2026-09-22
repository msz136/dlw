"""uni_identity.py -- explicit form of the extra UNIFORM-class lattice identity.

The h-scaling study (h_scaling.py, a = 5/2, h = 1/2 ... 1/20) shows that the
canonical uniform-class cross-site null vector has coefficients

    (1,0) block:  Dx^2 = Dt = -1/h^2 ,  Dx = -(2a-2h)/h^2 ,  id = -1
    (0,1) block:  Dx^2 = Dt = +1/h^2 ,  Dx = +(2a+2h)/h^2 ,  id = +1

so, multiplied by -h^2, it reads

    X := B_{a-h} F_{j+1}.G_j  -  B_{a+h} F_j.G_{j+1}
         + h^2 ( F_{j+1} G_j - F_j G_{j+1} )  = 0 ,      (uniform: F = tau_1^(a))

Here we test this claim directly, and also test the corresponding STAGGERED
version (F = tau_1^(a-d)), to contrast the two classes.
"""
import sympy as sp

from engine2 import Model, eadd, escale, rand_point

a = sp.symbols('a', real=True)
h = sp.symbols('h', positive=True)


def make(N, hh, stagger):
    m = Model(N, a=a, h=hh)
    m.p = [sp.Rational(4, 3), sp.Rational(9, 5), sp.Rational(7, 4),
           sp.Rational(11, 6), sp.Rational(13, 8), sp.Rational(16, 9)][:N]
    m.q = [sp.Rational(7, 5), sp.Rational(5, 3), sp.Rational(11, 7),
           sp.Rational(4, 3), sp.Rational(17, 10), sp.Rational(9, 5)][:N]
    m.a = sp.Rational(3, 2)
    if stagger:
        m._s = m.a - hh / 2
    else:
        m._s = m.a
    return m


def F(m, j):
    return m.tau(1, j=j, s=m._s, mu=m.a)


def X_uniform(m, hh, j):
    """B_{a-h}F_{j+1}.G_j - B_{a+h}F_j.G_{j+1} + h^2(F_{j+1}G_j - F_jG_{j+1})"""
    Fp, F0 = F(m, j + 1), F(m, j)
    Gp, G0 = m.tau(0, j=j + 1), m.tau(0, j=j)
    t1 = m.B(Fp, G0, s=m.a - hh)          # B_{a-h} F_{j+1}.G_j
    t2 = m.B(F0, Gp, s=m.a + hh)          # B_{a+h} F_j.G_{j+1}
    t3 = eadd(m.bilin(Fp, G0, ax=0), escale(m.bilin(F0, Gp, ax=0), -1))  # FpG0 - F0Gp
    return eadd(escale(t3, hh ** 2), t1, escale(t2, -1))


for stagger in (False, True):
    print('=' * 84)
    print('class: %s   (F = tau_1 with s = %s)'
          % ('STAGGERED' if stagger else 'UNIFORM',
             'a - h/2' if stagger else 'a'))
    for hh in (sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 4)):
        line = '   h=%-5s ' % hh
        for N in (1, 2, 3, 4):
            m = make(N, hh, stagger)
            tot, ok = 0, 0
            for j in (0, 1, 2):
                r = X_uniform(m, hh, j)
                tot += 1
                if len(r) == 0:
                    ok += 1
            line += ' N=%d:%d/%d' % (N, ok, tot)
        print(line, flush=True)
    print('   (X = 0 EXACTLY would mean the extra identity is genuine)')

print()
print('=' * 84)
print('leading continuum term of X (uniform), computed from the limits:')
print('   B_{a-h}F_{j+1}.G_j   ->  h B_a f_y.g - 2h D_x f.g + O(h^2)')
print('   B_{a+h}F_j.G_{j+1}   ->  h B_a f.g_y + 2h D_x f.g + O(h^2)')
print('   h^2(F_{j+1}G_j-F_jG_{j+1}) -> O(h^3)')
print('   X = h D_y B_a f.g - 4h D_x f.g + O(h^2) = O(h^2)   using (6): D_yB_a f.g = 4D_x f.g')
print('   => X is a HIGHER-ORDER lattice identity: it carries no O(h^0) continuum equation.')
print('   Contrast: the STAGGERED two-point form (star-prime) has leading term')
print('   B_a f.g_y + 2D_x f.g = (6)|lam=-2  at order h^0 after dividing by h.')
