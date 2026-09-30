"""Exact-coefficient checks for ALTERNATIVE_DISCRETIZATIONS.md.

This checks finite examples only. The arbitrary-N statement follows from the
fixed-parameter Gram chain and the entrywise parameter-site identity.
"""
from fractions import Fraction as Q
from verify_gram_reassessment import Gram, bil, logjet


def alternative_tau(g, n, j, s, s_minus, s_plus):
    out = {}
    for subset, minor in g.weights:
        coefficient = minor
        rates = [Q(0), Q(0), Q(0)]
        for i in subset:
            p, q = g.p[i], g.q[i]
            gamma = -(p - s) / (q + s)
            chi = (p - s_minus) * (q + s_plus) / ((p - s_plus) * (q + s_minus))
            coefficient *= g.rho[i] * gamma**n * chi**j
            rates[0] += p + q
            rates[1] += q*q - p*p
        key = tuple(rates)
        out[key] = out.get(key, Q(0)) + coefficient
    return {key: value for key, value in out.items() if value}


def continuous_second(f, g, a):
    out = {}
    for k, ck in f.items():
        for l, cl in g.items():
            dx, dt, dy = (k[i] - l[i] for i in range(3))
            rate = tuple(k[i] + l[i] for i in range(3))
            value = ck * cl * (dy * (dx*dx + dt + 2*a*dx) - 4*dx)
            out[rate] = out.get(rate, Q(0)) + value
    return {key: value for key, value in out.items() if value}


def nonlinear_physical_h_check(g, h, c, kappa, site=0):
    """Check both closed equations in the common physical-h field variables."""
    center = g.a + Q(c)*h*h
    span = h + Q(kappa)*h*h*h
    ratio = span/h
    s_minus, s_plus = center - span/2, center + span/2
    logs_f = {j: logjet(alternative_tau(g, 1, j, s_minus, s_minus, s_plus))
              for j in range(site-3, site+4)}
    logs_g = {j: logjet(alternative_tau(g, 0, j, g.a, s_minus, s_plus))
              for j in range(site-3, site+5)}
    u = lambda j: (2*logs_f[j]-logs_g[j]-logs_g[j+1]).dx()
    d0 = lambda f,j: (f(j+1)-f(j-1))/(2*h)
    dm = lambda f,j: (f(j)-f(j-1))/h
    mm = lambda f,j: (f(j)+f(j-1))/2
    lap = lambda f,j: (f(j+1)-2*f(j)+f(j-1))/(h*h)
    v = lambda j: 4*(logs_g[j+1]-logs_g[j]).dx()/h+d0(u,j)
    w = lambda j: v(j)-d0(u,j)
    flux = lambda j: u(j)*u(j)/2+2*center*u(j)+h*h*(w(j)*w(j)/32-ratio*w(j)/4)
    n1 = dm(lambda j: u(j).dt()+flux(j).dx(),site) + (
        mm(v,site)-h*h*lap(lambda j: dm(u,j),site)/4
    ).dx().dx()
    n2 = v(site).dt() + (
        d0(flux,site)+(u(site)+2*center)*w(site)-4*ratio*u(site)
    ).dx() + (
        d0(u,site)+h*h*lap(w,site)/4
    ).dx().dx()
    assert n1.val() == Q(0) and n2.val() == Q(0)


def main():
    count = 0
    for nsol in range(1, 5):
        for h in (Q(1, 2), Q(1, 3)):
            for c, kappa in ((0, 0), (1, 0), (0, 1), (-1, 1)):
                g = Gram(nsol, 8, h)
                center = g.a + Q(c)*h*h
                span = h + Q(kappa)*h*h*h
                s_minus, s_plus = center - span/2, center + span/2
                for j in (-1, 0, 2):
                    f = alternative_tau(g, 1, j, s_minus, s_minus, s_plus)
                    low = alternative_tau(g, 0, j, g.a, s_minus, s_plus)
                    high = alternative_tau(g, 0, j+1, g.a, s_minus, s_plus)
                    assert not bil(f, low, s_minus)
                    assert not bil(f, high, s_plus)
                    for n in (-1, 0, 1, 2):
                        assert alternative_tau(g, n, j, s_minus, s_minus, s_plus) == alternative_tau(
                            g, n, j+n, s_plus, s_minus, s_plus
                        )
                    count += 1
        g = Gram(nsol, 8, Q(1, 2))
        f = g.tau(1, 0, g.a, 'fixed')
        low = g.tau(0, 0, g.a, 'fixed')
        assert not bil(f, low, g.a)
        assert not continuous_second(f, low, g.a)
        if nsol <= 3:
            for h in (Q(1, 2), Q(1, 3)):
                for c, kappa in ((0, 0), (1, 0), (0, 1), (-1, 1)):
                    nonlinear_physical_h_check(Gram(nsol, 8, h), h, c, kappa)
        print(f'PASS N={nsol}: local family and continuous logarithmic-shift pair')
    print(f'PASS {count} exact local family cases')
    print('PASS 24 exact nonlinear physical-h cases (N=1..3)')


if __name__ == '__main__':
    main()
