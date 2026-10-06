"""Independent algebra checks for DLW conserved adaptive-mesh densities.

No numerical PDE evolution, convergence certification or integrability claim.
"""
import json
from pathlib import Path
import sympy as s

x, t = s.symbols('x t')
a, h = s.symbols('a h', real=True)
u, v, w = [s.Function(z)(x, t) for z in ('u', 'v', 'w')]
dx = lambda z: s.diff(z, x)
dt = lambda z: s.diff(z, t)
checks = {}
rules = {dt(w): -dx((u+2*a)*w+dx(v)),
         dt(v): -dx((u+2*a)*v+dx(w)-4*u)}
for sigma in (-1, 1):
    r = 1-(v+sigma*w)/4
    q = (u+2*a)*r+sigma*dx(r)-2*a
    checks[f'continuum_r{sigma:+d}'] = s.expand((dt(r)+dx(q)).subs(rules))
r = 1-v/4
q = (u+2*a)*r-dx(w)/4-2*a
checks['continuum_r0'] = s.expand((dt(r)+dx(q)).subs(rules))

# Formal commuting x/y difference operators in interior sites. The symbols
# denote exact already differentiated flux pieces, no product rule assumption.
dxDH, dxBW, dxxDu, dxxV, dxxLW, dxDA, dxBV, dxxLv = s.symbols(
    'dxDH dxBW dxxDu dxxV dxxLW dxDA dxBV dxxLv')
sd_vt = -dxDH-dxBW-dxxDu-h**2*dxxLW/4
sd_Dut = -dxDH-dxxV-h**2*dxxLW/4
sd_Wt = sd_vt-sd_Dut
sd_qmx = -(dxBW-(dxxV-dxxDu))/4
sd_qpx = -(2*dxDH+dxBW+dxxV+dxxDu+h**2*dxxLW/2)/4
sd_q0x = -(dxDH+dxBW+dxxDu+h**2*dxxLW/4)/4
checks['SD_rminus'] = s.expand(-sd_Wt/4+sd_qmx)
checks['SD_rplus'] = s.expand(-(sd_vt+sd_Dut)/4+sd_qpx)
checks['SD_r0'] = s.expand(-sd_vt/4+sd_q0x)
checks['SD_flux_average'] = s.expand((sd_qmx+sd_qpx)/2-sd_q0x)
fd_vt = -dxBV-dxxDu
fd_Dut = -dxDA-dxxV-h**2*dxxLv/4
for sigma in (-1, 1):
    qx = -(dxBV+sigma*dxDA+dxxDu+sigma*(dxxV+h**2*dxxLv/4))/4
    checks[f'FD_r{sigma:+d}'] = s.expand(-(fd_vt+sigma*fd_Dut)/4+qx)
checks['FD_r0'] = s.expand(-fd_vt/4-(dxBV+dxxDu)/4)

# Full polynomial certificate of exact continuum positivity for original C.
A, B, c, L1, L2 = s.symbols('A B c L1 L2')
g = 1+A+B+c*A*B
Dx = lambda z: A*s.diff(z, A)+B*s.diff(z, B)
Dy = lambda z: L1*A*s.diff(z, A)+L2*B*s.diff(z, B)
xy_numerator = s.expand(g*Dy(Dx(g))-Dx(g)*Dy(g))
target = L1*A*(1+2*c*B+c*B**2)+L2*B*(1+2*c*A+c*A**2)
checks['N2_C_positive_density_polynomial'] = s.expand(xy_numerator-target)
K1, K2 = s.symbols('K1 K2')
Dx_general = lambda z: K1*A*s.diff(z,A)+K2*B*s.diff(z,B)
general_num = s.expand(g*Dy(Dx_general(g))-Dx_general(g)*Dy(g))
general_target = (K1*L1*A+K2*L2*B+c*K2*L2*A**2*B+c*K1*L1*A*B**2+
                  (c*(K1+K2)*(L1+L2)+(K1-K2)*(L1-L2))*A*B)
checks['N2_general_density_polynomial'] = s.expand(general_num-general_target)
positive_polynomials = {}
for case, data in {
    'D': (3,1,-s.Rational(3,4),-s.Rational(1,2),s.Rational(5,4)),
    'E': (s.Rational(1,12),s.Rational(1,5),-1,-s.Rational(1,6),s.Rational(39,38))
}.items():
    poly = s.Poly(general_num.subs(dict(zip((K1,K2,L1,L2,c),data))),A,B)
    positive_polynomials[case] = {str(powers):str(coef) for powers,coef in poly.terms()}
    assert all(coef < 0 for coef in poly.coeffs())

# Normalized finite-endpoint coordinate: F=theta*M,
# F_t=qL-qX, M_t=qL-qR, and dF/dt=F_t+R*V.
qL, qX, qR, R, theta = s.symbols('qL qX qR R theta')
velocity = (qX-qL-theta*(qR-qL))/R
checks['fixed_endpoint_mass_coordinate'] = s.expand(qL-qX+R*velocity-theta*(qL-qR))
checks['fixed_left_endpoint'] = s.simplify(velocity.subs({theta:0, qX:qL}))
checks['fixed_right_endpoint'] = s.simplify(velocity.subs({theta:1, qX:qR}))

result = {
    'kind': 'exact local algebra; no numerical evolution or global error bound',
    'passed': all(z == 0 for z in checks.values()),
    'residuals': {k: str(z) for k, z in checks.items()},
    'N2_D_E_logxy_numerator_coefficients': positive_polynomials,
    'positivity_scope': {
        'A': {'p':[1], 'q':[2], 'a':2, 'lower_bound':1, 'strict':True},
        'B': {'p':[4], 'q':[-3], 'a':2, 'lower_bound':1, 'strict':True},
        'C': {'p':[6,4], 'q':[-5,-3], 'a':2, 'lower_bound':1, 'strict':True},
        'D': {'p':[1,4], 'q':[2,-3], 'a':2, 'lower_bound':1, 'strict':True},
        'E': {'p':['7/4',1], 'q':['-5/3','-4/5'], 'a':2, 'lower_bound':1, 'strict':True},
        'meaning': 'exact continuum rminus/r0/rplus globally >1; numerical positivity monitored separately'
    }
}
Path(__file__).with_name('identity_checks.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
assert result['passed']
