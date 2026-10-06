"""Exact support calculations for the specified DLW formal closure."""
from pathlib import Path
import json
import sympy as s

z, h, C, D = s.symbols('z h C D', nonzero=True)
checks = {}
cyclic = []
for n in range(3, 19):
    coefficients = [s.Integer(0)] + [h * (s.Rational(l,n)-s.Rational(1,2)) for l in range(1,n)]
    rr = sum(coefficients[l]*z**l for l in range(n))
    # Multiply dR=MP by hz, turning both sides into polynomials.
    pi = sum(z**l for l in range(n))/n
    residual = s.expand((z-1)*rr - h*(z+1)*(1-pi)/2)
    remainder = s.rem(residual, z**n-1, z)
    skew = all(s.simplify(coefficients[l]+coefficients[n-l]) == 0 for l in range(1,n))
    radius = max(min(l,n-l) for l in range(n) if coefficients[l] != 0)
    expected_radius = (n-1)//2
    ok = remainder == 0 and skew and radius == expected_radius
    cyclic.append({'N':n, 'inverse_identity':remainder == 0, 'skew':skew,
                   'exact_cyclic_radius':radius, 'pass':ok})
checks['cyclic_inverse_and_radius'] = cyclic

J = s.Matrix([[0,D],[D,0]])
T = s.Matrix([[1,0],[C,1]])
Tstar = s.Matrix([[1,-C],[0,1]])
checks['physical_coordinate_bracket_identity'] = T*J*Tstar == J

a,b,c,U,w,beta = s.symbols('a b c U w beta')
G0 = -U**2/2-beta*w**2
G1 = -U*w
q0,q1 = a*G0+b*G1, b*G0+c*G1
cross_difference = s.expand(s.diff(q0,w)-s.diff(q1,U))
checks['AD_quadratic_cross_difference'] = str(cross_difference)
checks['AD_after_diagonal_helmholtz_constraints'] = s.simplify(cross_difference.subs({a:0,c:0})) == 0

cmean, rho, qfield, rfield = s.symbols('cmean rho qfield rfield', nonzero=True)
constraint_pullback = s.Matrix([rfield+rho*rfield*cmean, qfield+rho*qfield*cmean])
checks['physical_constraint_covectors_annihilated'] = constraint_pullback.subs(rho,-1/cmean) == s.zeros(2,1)
skew_quadratic_checks = []
for n in range(3,9):
    shifts = s.zeros(n,n)
    for j in range(n):
        shifts[j,(j+1)%n] = 1
    cc = (shifts-shifts.T)/(2*h)
    qsymbols = s.Matrix(s.symbols('q0:'+str(n)))
    skew_quadratic_checks.append(s.expand((qsymbols.T*cc*qsymbols)[0]) == 0)
checks['cyclic_shear_quadratic_mean_zero'] = all(skew_quadratic_checks)
checks['all_pass'] = all(row['pass'] for row in cyclic) and all([
    checks['physical_coordinate_bracket_identity'],
    checks['AD_after_diagonal_helmholtz_constraints'],
    checks['physical_constraint_covectors_annihilated'],
    checks['cyclic_shear_quadratic_mean_zero'],
])
out = Path(__file__).with_name('algebra_checks.json')
out.write_text(json.dumps(checks, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
print(json.dumps({'all_pass':checks['all_pass'], 'cyclic_cases':len(cyclic), 'output':str(out)}, ensure_ascii=False))
if not checks['all_pass']:
    raise SystemExit(1)
