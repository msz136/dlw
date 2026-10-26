"""Validate constants, not continuum existence, using outward Arb arithmetic."""
import json
from pathlib import Path
from fractions import Fraction
from flint import arb, ctx

ctx.prec = 256
N, m = 901, 900
tq = Fraction(1801, 180200)
gq = Fraction(1, 180200)
aq = Fraction(9, 6494408)
assert tq - Fraction(9, N) == gq
assert Fraction(9, N - 1) - tq == gq
assert Fraction(1, 3604) * (9 - (N - 1) * tq) == aq
assert (N - 1) * gq / 2 > aq
assert Fraction(64, 31) + Fraction(1, 4) + Fraction(1, 2) < 4

def ball(q):
    return arb(q.numerator) / q.denominator

t, gamma, alpha = map(ball, [tq, gq, aq])
d = arb.pi() / 96
Z = 1 + (2 * arb.pi() / alpha).sqrt() / d
log_D = arb(4).log() + m * arb(64).log() + (1 + (N*m/alpha)**(m//2)).log() + N * Z.log()
log_C = -1 + arb(N).log() + N * (arb.pi()**3 / 2560**2).log()/2 - m * arb(2*N).log()
assert log_D > 25923 and log_D < 25924
assert log_C > -12265 and log_C < -12264
ell = 5000
K = d * N * ell
assert 1/K**2 < t
log_positive = log_C - m*K.log() + gamma*K**2
log_subtraction = log_D - gamma*K**2/2
assert log_positive > 97636
assert log_subtraction < -34000
# P - R > exp(97000); avoid forming huge absolute exponentials.
assert (log_positive-97000).exp() - (log_subtraction-97000).exp() > 1
result = {
    'kind': 'explicit constants for conditional transverse-jet obstruction',
    'precision_bits': ctx.prec, 'N': N, 'derivative_order_a_b': m,
    't_star_exact': str(tq), 'gamma_exact': str(gq), 'alpha_exact': str(aq),
    'log_D_enclosure': str(log_D), 'log_C_enclosure': str(log_C),
    'example_original_period_fourier_index': N*ell,
    'example_log_positive_enclosure': str(log_positive),
    'example_log_subtraction_enclosure': str(log_subtraction),
    'example_conditional_normalized_jet_coefficient_lower': 'exp(97000)',
    'scope': '900th normalized transverse boundary derivative of a, not physical u/v error',
    'independent_mathematical_review': False,
    'continuum_reference_certified': False, 'eta_u': None, 'eta_v': None,
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
