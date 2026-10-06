"""Exact algebra checks for a theory-only DLW factor-to-error model.

No PDE trajectories, floating point error tables, or fitted constants are used.
The output certifies the listed algebra identities, not a PDE convergence theorem.
"""
from pathlib import Path
import hashlib
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
s, gamma = sp.symbols('s gamma', real=True)
K, ell = sp.symbols('K ell', nonzero=True, real=True)
xi, eta, h, alpha, beta, a = sp.symbols('xi eta h alpha beta a', real=True)
I = sp.I
checks = []


def zero(name, expr):
    reduced = sp.cancel(expr)
    if reduced != 0:
        raise AssertionError(f'{name}: {reduced}')
    checks.append({'name': name, 'exact_residual': '0'})


def D(expr, n=1):
    for _ in range(n):
        expr = sp.cancel(s * (1-s) * sp.diff(expr, s))
    return expr


F = gamma*s/(1+(gamma-1)*s)
dp, cp = F-s, F+s
u, v = 2*K*dp, 2*K*ell*D(cp)
W = sp.cancel(v-ell*D(u))
zero('single soliton W equals 4 K ell sigmoid derivative', W-4*K*ell*D(s))
zeta = K*ell
nonlinear = K*ell*D(W**2/32-W/4, 2)
product = K*ell**3*D(D(u)*D(u, 2))/2
vterm = K**2*ell**2*D(v, 4)
uterm = K**2*ell**3*D(u, 5)
coefficients = {
    'FD1': vterm/12,
    'FD2': uterm/6,
    'SD1': nonlinear+vterm/12-uterm/4,
    'SD2': nonlinear+product+vterm/4-uterm/12,
}
profiles = {
    'FD1': zeta**3*D(cp, 5)/6,
    'FD2': zeta**3*D(dp, 5)/3,
    'SD1': zeta**3*((2*D(s, 5)-D(F, 5))/3+D(D(s)**2, 2)/2)-zeta**2*D(s, 3),
    'SD2': zeta**3*((D(F, 5)+2*D(s, 5))/3+D(D(s)**2, 2)/2
                   +2*D(D(dp)*D(dp, 2)))-zeta**2*D(s, 3),
}
for name in profiles:
    zero(f'universal residual profile {name}', coefficients[name]-profiles[name])
primitive_sd = zeta**3*((2*D(s, 4)-D(F, 4))/3+D(D(s)**2)/2)-zeta**2*D(s, 2)
primitive_fd = zeta**3*D(cp, 4)/6
zero('SD first residual primitive', D(primitive_sd)-profiles['SD1'])
zero('FD first residual primitive', D(primitive_fd)-profiles['FD1'])
zero('alpha response first equation', 2*K*ell*D(u, 2)-4*K*zeta*D(dp, 2))
zero('alpha response second equation', 2*K*D(v)-4*K*zeta*D(cp, 2))
zero('beta response second equation', -4*K*D(u)+8*K**2*D(dp))

pa, qa, aa = sp.symbols('p q a_parameter', real=True)
kp, pp, qq = pa+qa, pa-aa, qa+aa
zp, gp = kp**2/(pp*qq), -pp/qq
for parameter, expected_zeta, expected_gamma in (
        (aa, 1/pp-1/qq, -1/pp-1/qq),
        (pa, 2/kp-1/pp, 1/pp),
        (qa, 2/kp-1/qq, -1/qq)):
    zero(f'relative zeta parameter derivative {parameter}', sp.diff(zp,parameter)/zp-expected_zeta)
    zero(f'log gamma parameter derivative {parameter}', sp.diff(gp,parameter)/gp-expected_gamma)
zero('log gamma derivative is sigmoid phase shift derivative', gamma*sp.diff(F,gamma)-D(F))

# Sigmoid derivative suprema reduce to exact one-variable polynomials.
t = sp.symbols('t', real=True)
p2_squared = t**2*(1-4*t)
p3 = t*(1-6*t)
p5 = t*(1-30*t+120*t**2)
zero('second sigmoid derivative square reduction', D(s, 2)**2-p2_squared.subs(t, s*(1-s)))
zero('third sigmoid derivative reduction', D(s, 3)-p3.subs(t, s*(1-s)))
zero('fifth sigmoid derivative reduction', D(s, 5)-p5.subs(t, s*(1-s)))
suprema = {}
for name, polynomial, expected in (
        ('S2_squared', p2_squared, sp.Rational(1,108)),
        ('S3', p3, sp.Rational(1,8)),
        ('S5', p5, sp.Rational(1,4))):
    candidates = [sp.Integer(0), sp.Rational(1,4)]
    candidates += [r for r in sp.solve(sp.diff(polynomial,t),t)
                   if bool(r>=0) and bool(r<=sp.Rational(1,4))]
    values = [sp.simplify(abs(polynomial.subs(t,r))) for r in candidates]
    assert all(bool(sp.simplify(expected-v)>=0) for v in values)
    assert any(sp.simplify(expected-v)==0 for v in values)
    suprema[name] = {'critical_points': [str(r) for r in candidates],
                    'absolute_values': [str(v) for v in values], 'supremum': str(expected)}
    checks.append({'name': f'exact global sigmoid derivative bound {name}', 'passed': True})
qbound = sp.Rational(1,108)+sp.Rational(1,4)*sp.Rational(1,8)
zero('SD1 universal bound coefficient', sp.Rational(1,4)+qbound-sp.Rational(251,864))
zero('SD2 universal bound coefficient', sp.Rational(1,4)+9*qbound-sp.Rational(59,96))

# Exact linear matrices, followed by a formal fixed-wave-number expansion.
d, m, r, A, lam = sp.symbols('d m r A lam')
M_fd = sp.Matrix([[-2*I*a*xi, -I*xi**2*m/d],
                  [I*(xi**2*d*m+4*xi), -2*I*a*xi]])
M_uw = sp.Matrix([[xi**2-2*I*A*xi, I*xi*h**2*r/4-I*xi**2*m/d],
                  [4*I*r*xi, -xi**2-2*I*A*xi]])
T = sp.Matrix([[1,0],[I*d*m,1]])
M_sd = T*M_uw*T.inv()
Dfd = xi**4*m**2+4*xi**3*m/d
Dsd = xi**4+4*r*xi**3*m/d-r**2*xi**2*h**2
zero('FD exact linear characteristic polynomial', (lam*sp.eye(2)-M_fd).det()-((lam+2*I*a*xi)**2-Dfd))
zero('SD exact linear characteristic polynomial', (lam*sp.eye(2)-M_sd).det()-((lam+2*I*A*xi)**2-Dsd))
substitutions = {d: eta-eta**3*h**2/24, m:1-eta**2*h**2/8,
                 A:a+alpha*h**2, r:1+beta*h**2}
M0 = sp.Matrix([[-2*I*a*xi, -I*xi**2/eta],
                [I*(xi**2*eta+4*xi), -2*I*a*xi]])
L = (xi**2*eta**2+xi*eta)/4
M2sd = sp.Matrix([[L-2*I*alpha*xi, I*(xi/4+xi**2*eta/12)],
                  [I*(xi**2*eta**3/12+xi*eta**2/4+4*beta*xi), -L-2*I*alpha*xi]])
M2fd = sp.Matrix([[0,I*xi**2*eta/12],[-I*xi**2*eta**3/6,0]])
for name, mat, expected in (('SD',M_sd,M2sd),('FD',M_fd,M2fd)):
    expanded = mat.subs(substitutions, simultaneous=True).applyfunc(lambda e: sp.series(e,h,0,3).removeO())
    for row in range(2):
        for col in range(2):
            zero(f'{name} physical Fourier matrix coefficient {row}{col}', expanded[row,col]-M0[row,col]-h**2*expected[row,col])
cf = -xi**4*eta**2/4-xi**3*eta/3
cs = -xi**3*eta/3-xi**2+4*beta*xi**3/eta
zero('FD discriminant second coefficient', sp.series(Dfd.subs(substitutions,simultaneous=True),h,0,3).removeO()-xi**4-4*xi**3/eta-h**2*cf)
zero('SD discriminant second coefficient', sp.series(Dsd.subs(substitutions,simultaneous=True),h,0,3).removeO()-xi**4-4*xi**3/eta-h**2*cs)
b = sp.symbols('b', real=True)
factor = (b**2/4-1)*(b**2/4+2*b/3+1)
zero('frequency advantage factorization', (cf**2-cs.subs(beta,0)**2)/xi**4-factor.subs(b,xi*eta))

# Time coefficients come from stability polynomials, not measured error curves.
z = sp.symbols('z')
rk = 1+z+z**2/2+z**3/6+z**4/24
zero('Euler leading logarithmic time defect', sp.series(sp.log(1+z),z,0,3).removeO()-z+z**2/2)
zero('RK4 leading logarithmic time defect', sp.series(sp.log(rk),z,0,6).removeO()-z+z**5/120)

out = {
    'status': 'passed', 'method': 'exact symbolic rational identities and algebraic extrema',
    'scope': 'listed algebra identities only; no PDE stability or convergence certification',
    'uses_observed_error_data': False, 'PDE_simulations': 0,
    'checks': checks, 'sigmoid_bounds': suprema,
    'fourier_M2_SD': str(M2sd), 'fourier_M2_FD': str(M2fd),
    'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(HERE/'symbolic_validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':out['status'],'checks':len(checks),'PDE_simulations':0},ensure_ascii=False))
