"""Audit already completed source data without rerunning the experiment."""
from pathlib import Path
import csv
import hashlib
import json
import math

HERE = Path(__file__).resolve().parent


def rows(name):
    with (HERE / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def main():
    tests = []
    add = lambda name, ok, value: tests.append(dict(name=name, passed=bool(ok), value=value))
    direction_ranges = []
    for case in ('A', 'C'):
        identities = rows(f'identity_checks_{case}.csv')
        keys = [(r['scan'], float(r['value']), r['model']) for r in identities]
        add(case + '_complete_unique_26_states', len(keys) == len(set(keys)) == 26, len(keys))
        add(case + '_624_source_metric_rows', len(rows(f'source_metrics_{case}.csv')) == 624,
            len(rows(f'source_metrics_{case}.csv')))
        for name, bound in [('actual_rhs_max_difference', 5e-10),
                            ('sum_source_max_difference', 1e-15),
                            ('sd_fd_p_algebra_max_difference', 5e-11),
                            ('sd_fd_v_algebra_max_difference', 5e-11)]:
            value = max(float(r[name]) for r in identities)
            add(case + '_' + name, value < bound, value)
        correlations = rows(f'source_correlations_{case}.csv')
        for model in ('SD', 'FD'):
            for field in ('u', 'v'):
                selected = [r for r in correlations if r['scan'] == 'snapshot'
                            and r['model'] == model and r['field'] == field
                            and r['region'] == 'observation']
                cosines = [float(r['cosine_y_x']) for r in selected]
                direction_ranges.append(dict(case=case, model=model, field=field,
                                             cosine_min=min(cosines), cosine_max=max(cosines)))
                add(f'{case}_{model}_{field}_zero_instantaneous_inner_wrap',
                    all(float(r['rms_wrap']) == 0 for r in selected),
                    max(float(r['rms_wrap']) for r in selected))
    ind = json.loads((HERE / 'independent_validation.json').read_text())
    for key, bound in [('native_map_max_relative_at_smallest_epsilon', 1e-7),
                       ('jet_x1_max_relative_at_smallest_epsilon', 2e-6),
                       ('jet_x2_max_relative_at_smallest_epsilon', 2e-6),
                       ('y_buffer_u_change_max_y_variation', 1e-12),
                       ('y_buffer_v_change_max_abs', 1e-12),
                       ('x_buffer_max_source_difference', 1e-9)]:
        add(key, ind[key] < bound, ind[key])
    jets = rows('jet_validation.csv')
    for case in ('A', 'C'):
        for field in ('u', 'v'):
            ts = sorted([r for r in jets if r['case'] == case and r['check'] == 't1'],
                        key=lambda r: float(r['epsilon']), reverse=True)
            orders = [math.log(float(a[field]) / float(b[field]), 2) for a, b in zip(ts, ts[1:])]
            add(case + '_' + field + '_time_jet_second_order_difference',
                all(1.98 < p < 2.02 for p in orders), orders)
    fine = [float(r['order']) for r in rows('source_refinement_orders.csv') if float(r['fine']) == .025]
    add('fine_source_refinement_near_second_order', all(1.99 < x < 2.01 for x in fine),
        [min(fine), max(fine)])
    budgets = rows('baseline_source_budget.csv')
    res = max(float(r['energy_budget_relative_residual']) for r in budgets)
    add('source_squared_norm_budget', res < 1e-12, res)
    paths = [p for p in HERE.iterdir() if p.suffix in ('.py', '.csv', '.json', '.md')
             and p.name != 'validation.json']
    report = dict(passed=all(x['passed'] for x in tests), checks=tests,
                  source_direction_ranges_t_0_to_001=direction_ranges,
                  sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)})
    (HERE / 'validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'sha256'}, indent=2))
    assert report['passed']


if __name__ == '__main__':
    main()
