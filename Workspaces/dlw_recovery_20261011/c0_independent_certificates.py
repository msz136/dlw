"""Fresh exact checks for the c=0 branch; no historical script is rerun.

All-M arguments are in c0_independent_review_20261011.md. These checks
audit the new principal-symbol and Hill quadratic-form calculations.
"""
from pathlib import Path
import hashlib
import json
import sympy as sp

records = {}
f, fx, fxx, alpha = sp.symbols('f fx fxx alpha', nonzero=True)
theta = fx / f
t = f/2-alpha/f
r = f/2+alpha/f
def Dx(expr):
    return sp.diff(expr, f)*fx + sp.diff(expr, fx)*fxx
q0 = Dx(t)-t*t-theta*t
r0 = -Dx(r)-r*r+theta*r
assert sp.factor(r0-q0+2*alpha) == 0
a = t+theta/2
hill = q0+Dx(theta)/2-theta**2/4
assert sp.factor(hill-Dx(a)+a*a) == 0
records['two_factor_pencil'] = {'R_minus_Q': '-2 alpha', 'periodic_Hill_gauge': True}

principal = []
for M in range(2, 11):
    P0 = sp.eye(M)-sp.ones(M)/M
    H = sp.Matrix(M, M, lambda i,j: int(int(i)>int(j)))
    R = P0*(H+sp.eye(M)/2)*P0
    E = sp.Matrix(M,M-1,lambda i,j: int(int(i)==int(j))-int(int(i)==M-1))
    Eleft = (E.T*E).inv()*E.T
    Re = Eleft*R*E
    G = E.T*E/M
    # An exact constant physical state with nonzero q.
    p = sp.Matrix([sp.Rational(j+1) for j in range(M-1)])
    s = sp.Matrix([sp.Rational((-1)**j*(j+2)) for j in range(M-1)])
    Gamma = (p.T*G*s)[0]
    if Gamma == 0:
        s = p
        Gamma = (p.T*G*s)[0]
    n = M-1
    A = (s.T*G).row_join(p.T*G)
    w = p.col_join(s)
    B = sp.eye(n).row_join(Re).col_join(sp.zeros(n).row_join(-sp.eye(n)))
    projection = sp.eye(2*n)-w*A/(2*Gamma)
    T = projection*B
    K = sp.Matrix.hstack(*A.nullspace())
    Kleft = (K.T*K).inv()*K.T
    Tw = sp.simplify(Kleft*T*K)
    assert A*T == sp.zeros(1,2*n)
    assert sp.simplify(Tw**3-Tw) == sp.zeros(2*n-1)
    multiplicities = {str(e): m for e,m in Tw.eigenvals().items()}
    expected = {'0': 1}
    if M>2:
        expected.update({'1':M-2, '-1':M-2})
    assert multiplicities == expected
    principal.append({'M':M, 'multiplicities':multiplicities, 'T_cubed_equals_T':True})
records['constrained_principal_symbol'] = principal

z, kappa = sp.symbols('z kappa', nonzero=True)
quadratic = []
for n in range(1, 13):
    exponent = 2*n-1
    divided = sp.Rational(2*n+1,2)*((z+kappa)**exponent-z**exponent)/(kappa*(2*z+kappa))
    coeff = sp.residue(divided,z,-kappa/2)
    target = sp.Rational(2*n+1,2**(2*n))*kappa**(2*n-2)
    assert sp.factor(coeff-target) == 0
    quadratic.append({'n':n, 'second_variation_residue':str(target)})
records['Hill_second_variation'] = quadratic

# f*=h=1, s*=4: a*=0, A=1. Each row has the common
# factor (1+k^2/4), leaving an exact Vandermonde in k^2.
vander = []
for N in range(1, 9):
    coeffs = [sp.Rational(-1,2)] + [sp.Rational((2*n+1)*(-1)**(n-1),2**(2*n+1)) for n in range(1,N)]
    mat = sp.Matrix(N,N,lambda n,j: coeffs[n]*(j+1)**(2*n)*(1+sp.Rational((j+1)**2,4)))
    target = sp.prod(coeffs)*sp.prod(1+sp.Rational(j*j,4) for j in range(1,N+1))*sp.prod(j*j-i*i for i in range(1,N+1) for j in range(i+1,N+1))
    det = mat.det()
    assert det == target and det != 0
    vander.append({'N':N,'quadratic_minor':str(det),'nonzero':True})
records['odd_trace_independence_minors'] = vander

output = {
    'status':'all fresh exact checks passed',
    'sympy':sp.__version__,
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'checks':records,
    'scope':'Finite certificates for new all-M proofs; no actual nonlinear flow or Liouville completeness claim.'
}
Path(__file__).with_name('c0_independent_certificates.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
print(output['status'])
