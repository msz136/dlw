"""Lock a parameter-only interval rule, then evaluate unseen solitons.

The model is deliberately simple and fixed before the holdout trajectories
are run.  It predicts an interval in units of pulse widths, for the
controlled transport test at h=1/8 and nx=128.  It is not a DLW theorem.
"""
from dataclasses import asdict
from pathlib import Path
import argparse
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'lib'), str(ROOT / 'experiments')]
import numpy as np

from moving_mesh_interval_study import transport_run, INTERVALS_D
from moving_mesh_route1_geometry import width
from parametric import Exact, Parameters

BASE = ROOT / 'out' / 'moving_mesh'
LOCK = BASE / 'interval_parameter_model_lock.json'
RESULT = BASE / 'interval_parameter_model_holdout.json'

# These have new (a,p,q) triples, not phase variants of P1--P16.
HOLDOUT = (
    ('H01', 4., 1.25, 2.4), ('H02', 3.25, .8, 2.2),
    ('H03', 5., 1.2, 2.6), ('H04', 4.5, 2., 3.1),
    ('H05', 3.5, 2.1, 1.1), ('H06', 4.5, 2.7, 1.5),
    ('H07', 3., 1.9, 1.), ('H08', 5., 3., 1.8),
    ('H09', 2.2, 1.65, 2.1), ('H10', 2., 1.4, 2.6),
    ('H11', 2.6, 2., 2.8), ('H12', 1.9, 1.4, 1.9),
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contrast(pars, h=.125, layers=24):
    """Exact max(R)-1 for the symmetric 24-layer N=1 Gram monitor.

    R=1-S/(layers*h)*(sigmoid(z+n*chi)-sigmoid(z-n*chi)), n=layers/2.
    The maximum occurs at z=0; the minimum far away is 1.
    """
    exact = Exact(pars, h)
    return exact.S / (layers*h) * np.tanh(layers*abs(exact.chi)/4)


def predict(pars):
    c = contrast(pars)
    if pars.p > pars.q:
        return .0625
    if c >= .6:
        return .5
    return .25


def lock():
    training = (BASE / 'interval_study.json', BASE / 'interval_extended.json')
    planned = []
    for name, a, p, q in HOLDOUT:
        pars = Parameters(a=a, p=p, q=q, rho=p+q)
        exact = Exact(pars, .125)
        planned.append({'id': name, 'parameters': asdict(pars),
                        'monitor_contrast': contrast(pars),
                        'width': width(exact), 'selected_interval_D': predict(pars)})
    data = {'locked_rule': 'if p>q: 1/16; elif C>=0.6: 1/2; else: 1/4',
            'C_formula': '(p+q)/(24h)*tanh(6*abs(chi)), h=1/8',
            'objective': 'minimize max(u_common_error/u_frozen, v_common_error/v_frozen)',
            'test_equation': 'controlled transport, not DLW',
            'test_h': .125, 'test_nx': 128, 'test_dt': .001,
            'test_D_final': 2, 'comparison': 'always 1/4 pulse width',
            'holdout': planned,
            'source_sha256': sha(Path(__file__)),
            'training_sha256': {p.name: sha(p) for p in training}}
    LOCK.write_text(json.dumps(data, indent=2, allow_nan=False), encoding='utf-8')
    print('locked', len(planned), 'unseen parameter triples; source', data['source_sha256'])


def evaluate():
    plan = json.loads(LOCK.read_text(encoding='utf-8'))
    assert plan['source_sha256'] == sha(Path(__file__)), 'source changed after lock'
    for name, digest in plan['training_sha256'].items():
        assert sha(BASE / name) == digest, f'training data changed after lock: {name}'
    result = {'lock_sha256': sha(LOCK), 'scope': {'equation': 'controlled transport, not DLW',
              'holdout_count': len(plan['holdout']), 'intervals_D': INTERVALS_D},
              'cases': []}
    for item in plan['holdout']:
        pars = Parameters(**item['parameters'])
        rows = []
        for interval in INTERVALS_D:
            row = transport_run(pars, item['width'], 128, .001, interval)
            rows.append(row)
            print(item['id'], interval, row['status'], flush=True)
        result['cases'].append({'id': item['id'], 'parameters': item['parameters'],
                                'monitor_contrast': item['monitor_contrast'],
                                'width': item['width'],
                                'selected_interval_D': item['selected_interval_D'],
                                'runs': rows})
    result['source_sha256'] = {str(Path(__file__).relative_to(ROOT)): sha(Path(__file__)),
                               'experiments/moving_mesh_interval_study.py':
                               sha(ROOT / 'experiments/moving_mesh_interval_study.py')}
    RESULT.write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=('lock', 'evaluate'))
    args = parser.parse_args()
    {'lock': lock, 'evaluate': evaluate}[args.stage]()


if __name__ == '__main__':
    main()
