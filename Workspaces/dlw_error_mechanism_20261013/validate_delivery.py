"""Aggregate existing scientific checks and verify the delivered assets."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from PIL import Image

HERE = Path(__file__).resolve().parent


def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))


def main():
    checks = []

    def check(name, passed):
        checks.append({'name': name, 'passed': bool(passed)})
        assert passed, name

    for file in ('sources/validation.json',
                 'transport/common_validation.json', 'morphology/validation.json', 'validation.json'):
        d = read(file)
        check(file, d['passed'])
    independent = read('sources/independent_validation.json')
    check('independent_source_derivatives', max(independent[k] for k in (
        'native_map_max_relative_at_smallest_epsilon', 'jet_x1_max_relative_at_smallest_epsilon',
        'jet_x2_max_relative_at_smallest_epsilon')) < 1e-6)
    d = read('transport/analysis_validation.json')
    check('all_transport_closure_and_time_controls', d['all_completed_checks_passed'])
    check('13_complete_field_closures', len(d['checks']) == 13 and all(x['passed'] for x in d['checks']))
    check('16_time_step_controls', len(d['time_refinement']) == 16 and all(x['passed'] for x in d['time_refinement']))
    for kind in ('SD', 'FD'):
        b = read(f'boundary/A_{kind}_validation.json')
        check(f'boundary_{kind}_matched_grid_time_reference', b['target_grid_identical'] and b['target_times_identical'] and b['exact_reference_max_difference'] == 0)
    r = read('refinement/validation.json')
    check('frozen_prediction_confirmed', r['prediction_confirmed'] and r['ratios']['dx0.1_u'] < 1 < r['ratios']['dx0.025_u'])
    check('refinement_PE_time_control', all(v['relative_vector_difference'] < 1e-5 for k, v in r['checks'].items() if 'time_refinement' in k))
    mix = pd.read_csv(HERE / 'intervention/summary.csv')
    base = mix[~mix.halfdt]
    check('all_ten_intervention_endpoints', len(base) == 10)
    for case, sign in [('A', 1), ('C', -1)]:
        values = base[base.case == case].sort_values('lam').joint_rms.to_numpy()
        check(f'{case}_prespecified_mixture_trend', np.all(sign * np.diff(values) > 0))
    half = mix[(mix.case == 'A') & mix.halfdt].iloc[0].joint_rms
    original = base[(base.case == 'A') & (base.lam == .5)].iloc[0].joint_rms
    check('mixture_midpoint_time_control', abs(half / original - 1) < 1e-6)
    solver = HERE.parent / 'dlw_three_tracks_20261013/shared/solver_cells.json'
    sha = hashlib.sha256(solver.read_bytes()).hexdigest()
    check('frozen_solver_unchanged', sha == '4323fa90ef051a88de371c4da1f642711e5ccb128fa4e1d79be5fd6e80c30db0')
    figures = []
    for stem in ('source_propagator_exchange', 'transported_source_budget', 'refinement_reversal',
                 'update_intervention', 'error_evolution', 'error_fields'):
        png, pdf = HERE / 'figures' / (stem + '.png'), HERE / 'figures' / (stem + '.pdf')
        with Image.open(png) as im:
            info = {'name': stem, 'pixels': list(im.size), 'dpi': list(im.info.get('dpi', (0, 0)))}
        check(stem + '_PNG300_PDF', min(info['dpi']) > 299 and min(info['pixels']) > 800 and pdf.read_bytes()[:4] == b'%PDF')
        figures.append(info)
    result = {'passed': True, 'checks': checks, 'figures': figures,
              'frozen_solver_sha256': sha, 'figure_visual_review': 'All six PNGs inspected; refinement labels separated and colored.',
              'browser_preview': 'Not executed: application browser policy blocks local file URLs. No bypass attempted. Static HTML, math, links, and image files checked.'}
    (HERE / 'delivery_validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'passed': True, 'checks': len(checks), 'figures': len(figures)}))


if __name__ == '__main__':
    main()
