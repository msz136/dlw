"""Exact checks for the accompanying all-M algebraic proof; no PDE numerics."""
from __future__ import annotations
import hashlib
import json
import platform
from pathlib import Path
import sympy as sp

z, W, eps = sp.symbols('z W eps')
checks = []

def require_zero(expr, label):
    residual = sp.cancel(expr)
    if residual != 0:
        raise AssertionError(f'{label}: {residual}')

for m in range(1, 8):
    basis = [(W+eps)**(m-j)*(W-eps)**j for j in range(m+1)]
    mat = sp.Matrix([[sp.expand(basis[j]-basis[m]).coeff(W, r)
                      for j in range(m)] for r in range(m)])
    expected = (2*eps)**(m*(m+1)//2)
    require_zero(mat.det(method='domain-ge')-expected, f'basis determinant m={m}')
    checks.append({'check':'basis determinant', 'M':m+1, 'symbolic':True, 'passed':True})

for M in range(2, 7):
    m = M-1
    for delta, kappa in [(sp.Rational(1,3), 2*sp.I), (sp.Rational(-2,5), 3*sp.I)]:
        aa = list(sp.symbols(f'a0:{m}'))
        bb = list(sp.symbols(f'b0:{m}'))
        alpha, beta = aa+[-sum(aa)], bb+[-sum(bb)]
        uv = z*z+kappa*z-delta*delta
        u, v = uv-kappa*delta, uv+kappa*delta
        numer = sp.expand(sum((delta*alpha[j]+z*beta[j])*v**(m-j)*u**j for j in range(M)))
        if sp.Poly(numer, z).degree() > 2*m-1:
            raise AssertionError('degree bound')
        matrix = sp.Matrix([[sp.diff(numer.coeff(z,r), x) for x in aa+bb]
                            for r in range(2*m)])
        expected = (-1)**(m*(m-1)//2)*delta**m*(2*kappa*delta)**(m*(m+1))
        require_zero(matrix.det(method='domain-ge')-expected, f'full determinant M={M}')
        ap = sum(alpha[j]*(W+kappa*delta)**(m-j)*(W-kappa*delta)**j for j in range(M))
        bp = sum(beta[j]*(W+kappa*delta)**(m-j)*(W-kappa*delta)**j for j in range(M))
        reflected = numer.subs(z, -kappa-z)
        qrecover = sp.cancel((numer-reflected)/(2*z+kappa))
        arecover = sp.cancel((numer+reflected+kappa*qrecover)/(2*delta))
        require_zero(qrecover-bp.subs(W,uv), f'beta reflection M={M}')
        require_zero(arecover-ap.subs(W,uv), f'alpha reflection M={M}')
        aval = [sp.Integer(j+1) for j in range(m)]
        bval = [sp.Integer((j+1)**2) for j in range(m)]
        aval += [-sum(aval)]
        bval += [-sum(bval)]
        t = lambda zz:(zz-delta)/(zz+delta)
        direct = sum(t(z+kappa)**(m-j)*(-2*(delta*aval[j]+z*bval[j]))
                     /((z+kappa+delta)*(z+delta))*t(z)**j for j in range(M))
        coeffs = dict(zip(aa+bb, aval[:m]+bval[:m]))
        formula = -2*numer.subs(coeffs)/((z+kappa+delta)**M*(z+delta)**M)
        require_zero(direct-formula, f'ordered product variation M={M}')
        checks.append({'check':'coefficient determinant, reflection and ordered variation',
                       'M':M, 'delta':str(delta), 'kappa':str(kappa),
                       'exact_arithmetic':True, 'passed':True})

script = Path(__file__)
result = {'status':'passed', 'python':platform.python_version(), 'sympy':sp.__version__,
          'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),
          'checks':checks,
          'scope':'Finite exact algebra checks; all-M proof in accompanying note. No inverse-spectral or completeness theorem certified.'}
out = script.with_name('scalar_monodromy_linearization_checks.json')
out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'PASS: {len(checks)} exact checks; output {out.name}')
