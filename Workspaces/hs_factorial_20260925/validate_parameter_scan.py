"""Check completeness, provenance and numerical sanity of the selected-wave scan."""
import hashlib
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / 'out' / 'parameter_scan'
read = lambda name: json.loads((OUT / name).read_text(encoding='utf-8'))
main = read('evolution.json')
spatial = read('spatial_controls.json')
domain = read('domain_controls.json')
lattice = read('integrable_lattice_check.json')

ps = (3, 5, 12, 20)
spaces = ('integrable_moving', 'ordinary_moving', 'fixed_difference')
methods = ('euler', 'heun', 'rk4', 'rk8')
dts = (.05, .025, .0125, .00625)
assert main['status'] == 'completed'
assert len(main['rows']) == 192
assert {(r['p'], r['space'], r['method'], r['dt']) for r in main['rows']} == set(
    itertools.product(ps, spaces, methods, dts))
assert len(main['time_references']) == 12
assert {(r['p'], r['space']) for r in main['time_references']} == set(
    itertools.product(ps, spaces))
assert len(spatial['rows']) == 39
assert {(r['p'], r['space'], r['a_or_dx']) for r in spatial['rows']} == {
    (p, s, a) for p in ps for s in spaces
    for a in ((.04, .02, .01, .005) if p == 20 else (.04, .02, .01))}
assert len(domain['rows']) == 12
assert {(r['p'], r['space']) for r in domain['rows']} == set(
    itertools.product(ps, spaces))
assert len(lattice['rows']) == 4
assert {r['p'] for r in lattice['rows']} == set(ps)

for name, digest in main['source_sha256'].items():
    source = ROOT / name
    assert source.exists(), source
    assert hashlib.sha256(source.read_bytes()).hexdigest() == digest, source

max_floor_ratio = 0.0
final_floor_ratio = 0.0
floor_dominated = 0
for row in (main['rows'] + main['time_references'] +
            spatial['rows'] + domain['rows']):
    assert row['status'] == 'completed', row
    assert row['rejected'] == 0, row
    assert math.isclose(row['reached'], .25, abs_tol=1e-12), row
    for t in ('0.05', '0.1', '0.25') if row in main['rows'] or row in main['time_references'] else ('0.25',):
        obs = row['observations'][t]
        assert obs['mesh']['min_spacing'] > 0, row
        for window in ('legacy_core', 'wave_window'):
            v = obs['windows'][window]
            assert v['joint_scaled_linf'] >= 0
            for field in ('u', 'rho'):
                error = v[field + '_linf']
                floor = v[field + '_reconstruction_floor']
                assert all(math.isfinite(x) and x >= 0 for x in (error, floor))
                if error:
                    max_floor_ratio = max(max_floor_ratio, floor / error)
                    if floor >= error:
                        floor_dominated += 1
                    if row in main['rows'] and t == '0.25' and window == 'wave_window':
                        final_floor_ratio = max(final_floor_ratio, floor / error)
            assert math.isfinite(v['joint_scaled_linf'])

for row in main['rows']:
    assert math.isfinite(row['temporal_state_linf'])
for row in lattice['rows']:
    assert row['status'] == 'completed' and row['rejected'] == 0
    assert math.isclose(row['reached'], .25, abs_tol=1e-12)
    assert max(row[k] for k in ('u_solver_linf', 'rho_solver_linf',
                                'x_solver_linf')) < 1e-10
assert final_floor_ratio < 1, final_floor_ratio

print(f'PASS: 192 trajectories, 12 references, 39 spatial controls, '
      f'12 domain controls, 4 finite-a checks; max reconstruction-floor/error '
      f'ratio at main T=0.25 {final_floor_ratio:.3g}; '
      f'{floor_dominated} early/control field-window comparisons are floor-dominated; '
      f'source hashes match')
