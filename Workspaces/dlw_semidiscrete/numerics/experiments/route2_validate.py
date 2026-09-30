"""Check the stored route-two identities and provenance, without rerunning trajectories."""
from pathlib import Path
import hashlib
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out/route2'


def load(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))


def inf(a):
    return float(np.max(np.abs(a)))


def check_hashes(data):
    for path, expected in data['sources_sha256'].items():
        actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        assert actual == expected, (path, 'source changed after experiment')


def main():
    budget, adjoint, crossparam = load('budget.json'), load('adjoint.json'), load('crossparam.json')
    check_hashes(budget)
    check_hashes(adjoint)
    check_hashes(crossparam)
    checks = 0
    for row in budget['runs']:
        path = OUT / row['field_file']
        assert path.is_file(), path
        with np.load(path) as a:
            for f in ('u', 'v'):
                measured = row['errors'][f]['total_vs_continuous']
                assert abs(inf(a[f] - a['continuous_' + f]) - measured) < 2e-12
                if row['config']['initial'] == 'finite':
                    model = a['finite_' + f] - a['continuous_' + f]
                    solver = a[f] - a['finite_' + f]
                    assert inf((a[f] - a['continuous_' + f]) - model - solver) < 2e-12
                    assert abs(inf(model) - row['errors'][f]['model']) < 2e-12
                    assert abs(inf(solver) - row['errors'][f]['solver_vs_finite']) < 2e-12
                checks += 1
    for d in budget['prospective_balances']:
        pilot = d['pilot_solver']
        C = d['pilot_C']
        assert abs(d['predicted_h_balance']**2 * C - pilot) < 1e-12
        for held in d['held_out_h']:
            assert abs(held['predicted_model_to_pilot_solver'] - C*held['h']**2/pilot) < 1e-12
            checks += 1
    for d in budget['fd_same_h_fine_reference']:
        case = d['case']
        coarse = next(r for r in budget['runs'] if r['config']['case'] == case and
                      r['config']['model'] == 'fd' and r['config']['nx'] == 256)
        fine = next(r for r in budget['runs'] if r['config']['case'] == case and
                    r['config']['model'] == 'fd' and r['config']['nx'] == 512 and
                    r['config']['dt'] == .0000625)
        fine_dt = next(r for r in budget['runs'] if r['config']['case'] == case and
                       r['config']['model'] == 'fd' and r['config']['nx'] == 512 and
                       r['config']['dt'] == .000125)
        with np.load(OUT / coarse['field_file']) as c, np.load(OUT / fine['field_file']) as f, np.load(OUT / fine_dt['field_file']) as ft:
            assert inf(c['x'] - f['x'][::2]) < 1e-12
            for field in ('u', 'v'):
                assert abs(inf(c[field] - f[field][:, ::2]) - d['same_h_fd_coarse_minus_fine'][field]) < 2e-12
                assert abs(inf(f[field] - ft[field]) - d['fine_dt_halving'][field]) < 2e-12
                checks += 1
    for r in adjoint['results']:
        signed = r['adjoint_signed']
        proxy = r['target']['linear_proxy_actual']
        pred = r['target']['linear_proxy_predicted']
        assert abs(sum(signed.values()) - proxy) < 5e-11
        assert abs(signed['spatial'] + signed['quadrature'] - pred) < 5e-11
        assert r['adjoint_transpose_residual'] < 1e-10
        assert r['rk4_tangent_fd_residual'] < 2e-8
        assert abs(proxy) <= r['a_posteriori_nonlinear_bound'] + 1e-12
        assert abs(pred) <= r['linear_absolute_bound'] + 1e-12
        assert 0 <= r['spatial_boundary_last_y_absolute_share'] <= 1
        assert r['target']['profile_fit_actual']['fit_interior']
        checks += 1
    for field in ('u', 'v'):
        trained = [r['fields'][field]['observed_solver'] /
                   (crossparam['T']*r['fields'][field]['initial_output_defect'])
                   for r in crossparam['training']]
        assert abs(float(np.median(trained)) - crossparam['factors'][field]) < 1e-12
        for p in crossparam['predictions']:
            d=p['fields'][field]
            expected=crossparam['factors'][field]*crossparam['T']*d['initial_output_defect']
            assert abs(expected-d['predicted_solver_floor']) < 1e-12
            assert abs(d['pilot_h_model_C']*crossparam['h_test']**2/expected -
                       d['predicted_h_1_16_ratio']) < 1e-10
            actual=next(r for r in budget['runs'] if r['config']['case']==p['case'] and
                        r['config']['h']==crossparam['h_test'] and r['config']['nx']==256 and
                        r['config']['initial']=='finite')
            assert abs(d['observed_h_1_16_ratio']-actual['errors'][field]['dominance_ratio']) < 1e-12
            checks += 1
    print(f'route2 validation: {checks} checks passed; {len(budget["runs"])} budget runs, '
          f'{len(adjoint["results"])} adjoint runs, '
          f'{len(crossparam["training"])} cross-parameter calibration runs')


if __name__ == '__main__':
    main()
