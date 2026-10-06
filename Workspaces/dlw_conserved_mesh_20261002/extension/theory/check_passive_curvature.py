"""Symbolic checks for passive initial-curvature weighting; no PDE runs."""
from pathlib import Path
import hashlib
import json

import sympy as s

HERE = Path(__file__).resolve().parent
x, t = s.symbols('x t')
R = s.Function('R_b')(x, t)
Q = s.Function('Q_b')(x, t)
mu = s.Function('mu')(x, t)
m = s.Function('m')(x, t)
M = s.Function('M')(t)
I = s.Function('I_left')(t)
QL = s.Function('Q_left')(t)
QR = s.Function('Q_right')(t)
V = s.Function('V')(x, t)

checks = {}

# R_mu conservation consists of the base conservation residual plus the
# passive transport residual. This identity also states the exact condition.
raw = s.diff(R*mu, t) + s.diff(Q*mu, x)
factorized = mu*(s.diff(R, t)+s.diff(Q, x)) + R*(s.diff(mu, t)+(Q/R)*s.diff(mu, x))
checks['weighted_residual_factorization'] = s.simplify(raw-factorized)
checks['weighted_conservation_given_base_and_passive_transport'] = s.simplify(
    raw.subs({s.diff(R, t): -s.diff(Q, x),
              s.diff(mu, t): -(Q/R)*s.diff(mu, x)}))

# On a finite fixed interval m = integral(left,x)R_b and I_left is the
# time integral of the LEFT endpoint flux. Normalized mass labels require
# a different derivative; they are not generally material labels.
finite_rules = {s.diff(m, x): R, s.diff(m, t): QL-Q,
                s.diff(M, t): QL-QR, s.diff(I, t): QL}
zeta = m-I
checks['absolute_label_x_is_density'] = s.simplify(s.diff(zeta, x).subs(finite_rules)-R)
checks['absolute_label_t_is_minus_flux'] = s.simplify(s.diff(zeta, t).subs(finite_rules)+Q)
checks['absolute_label_material_derivative_zero'] = s.simplify(
    (s.diff(zeta, t)+(Q/R)*s.diff(zeta, x)).subs(finite_rules))

eta = m/M
eta_material = s.simplify((s.diff(eta, t)+(Q/R)*s.diff(eta, x)).subs(finite_rules))
eta_expected = (QL+eta*(QR-QL))/M
checks['normalized_label_source_formula'] = s.simplify(eta_material-eta_expected)

# A fixed function of the absolute label obeys the needed passive transport.
f = s.Function('mu_initial')
mu_label = f(zeta)
label_residual = s.diff(R*mu_label, t)+s.diff(Q*mu_label, x)
checks['label_weighted_conservation'] = s.simplify(
    label_residual.subs(s.diff(R, t), -s.diff(Q, x)).subs(finite_rules))

# Derivative observed at moving ALE nodes: dot(mu)|xi = mu_t + V mu_x.
ale_from_chain_rule = s.diff(mu, t)+V*s.diff(mu, x)
ale_expected = (V-Q/R)*s.diff(mu, x)
checks['ALE_transport_velocity'] = s.simplify(
    ale_from_chain_rule.subs(s.diff(mu, t), -(Q/R)*s.diff(mu, x))-ale_expected)

# The endpoint-normalized mesh velocity makes eta stationary at mesh nodes.
# This is why eta is a mesh label but not a base-mass material label.
normalized_V = (Q-QL-eta*(QR-QL))/R
checks['normalized_label_stationary_at_normalized_mesh_nodes'] = s.simplify(
    (s.diff(eta, t)+normalized_V*s.diff(eta, x)).subs(finite_rules))

assert all(value == 0 for value in checks.values()), checks
assert eta_material != 0
record = {
    'date': '2026-10-02',
    'scope': 'Independent symbolic algebra only; no PDE evolution or precision claim',
    'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'passed': len(checks),
    'zero_residual_checks': {key: str(value) for key, value in checks.items()},
    'normalized_label_material_source': str(s.factor(eta_material)),
    'interpretation': {
        'base': 'R_b,t + Q_b,x = 0; R_b > 0',
        'passive_weight': 'mu_t + (Q_b/R_b) mu_x = 0',
        'weighted_pair': 'R_mu = mu R_b; Q_mu = mu Q_b',
        'absolute_label': 'zeta = integral_left^x R_b ds - integral_0^t Q_b(left,s) ds',
        'ALE': 'dot(mu)|xi = (V-Q_b/R_b) mu_x',
        'density_class': 'Conserved density of an augmented passive-transport system, not a new local function of current u,v alone',
        'limits': 'No DLW stability, error reduction, integrability, or full-discrete product rule follows from these identities',
    },
}
target = HERE/'passive_curvature_symbolic.json'
target.write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'passed': len(checks), 'normalized_label_material_source': str(s.factor(eta_material)),
                  'saved': str(target)}, ensure_ascii=False))
