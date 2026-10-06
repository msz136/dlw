"""Independent readback of both frozen DLW extension batches; no evolution."""
from pathlib import Path
import csv
import hashlib
import json
import re
import sys
import numpy as np
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAPER_CASES = {
    'A': (2., (1.,), (2.,)),
    'B': (2., (4.,), (-3.,)),
    'C': (2., (6., 4.), (-5., -3.)),
    'D': (2., (1., 4.), (2., -3.)),
    'E': (2., (7/4, 1.), (-5/3, -4/5)),
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def paper_uv(case, y, x, t):
    """Direct positive tau sums in extended precision, independent of solver."""
    aa, pp, qq = PAPER_CASES[case]
    p, q = np.asarray(pp, dtype=np.longdouble), np.asarray(qq, dtype=np.longdouble)
    y = np.asarray(y, dtype=np.longdouble)[:, None]
    x = np.asarray(x, dtype=np.longdouble)[None, :]
    K = p+q
    L = 1/(p-aa)+1/(q+aa)
    gamma = -(p-aa)/(q+aa)
    exponents = [K[i]*x+L[i]*y+(q[i]**2-p[i]**2)*np.longdouble(t) for i in range(len(p))]
    E = [np.exp(z) for z in exponents]
    zero = np.zeros_like(E[0])
    if len(p) == 1:
        tau_terms = np.stack((np.ones_like(E[0]), E[0]/K[0]))
        rates_x, rates_y = np.array([0., K[0]], dtype=np.longdouble), np.array([0., L[0]], dtype=np.longdouble)
        factor = np.array([1., gamma[0]], dtype=np.longdouble)
    else:
        cross = ((p[0]-p[1])*(q[0]-q[1])/
                 ((p[0]+q[0])*(p[0]+q[1])*(p[1]+q[0])*(p[1]+q[1])))
        tau_terms = np.stack((np.ones_like(E[0]), E[0]/K[0], E[1]/K[1], cross*E[0]*E[1]))
        rates_x = np.array([0., K[0], K[1], sum(K)], dtype=np.longdouble)
        rates_y = np.array([0., L[0], L[1], sum(L)], dtype=np.longdouble)
        factor = np.array([1., gamma[0], gamma[1], np.prod(gamma)], dtype=np.longdouble)
    f_terms = tau_terms*factor[:, None, None]
    def logarithmic_derivatives(terms):
        tau = terms.sum(axis=0)
        tx = (terms*rates_x[:, None, None]).sum(axis=0)
        ty = (terms*rates_y[:, None, None]).sum(axis=0)
        txy = (terms*(rates_x*rates_y)[:, None, None]).sum(axis=0)
        return tx/tau, txy/tau-tx*ty/(tau*tau)
    fx, fxy = logarithmic_derivatives(f_terms)
    gx, gxy = logarithmic_derivatives(tau_terms)
    return np.asarray(2*(fx-gx), float), np.asarray(2*(fxy+gxy), float)


def close(label, value, tolerance):
    if not np.isfinite(value) or value > tolerance:
        raise AssertionError(f'{label}: {value} > {tolerance}')


def main():
    hashes = {'baseline': sha(ROOT/'baseline.py'), 'candidate': sha(ROOT/'candidates.py')}
    records, pairs, initial, stopped = [], [], {}, []
    maxima = dict(initial_native_field=0., independent_exact_reference=0.,
                  physical_endpoint=0., saved_spline_reconstruction=0.,
                  error_field_readback=0., scalar_max_error_readback=0.,
                  scalar_rms_error_readback=0., nodal_max_error_readback=0.)
    totals = {}
    snapshot_count = 0
    for batch, subdir in (('baseline', 'baseline_out'), ('candidate', 'candidate_out')):
        metadata = json.loads((ROOT/subdir/'results.json').read_text(encoding='utf-8'))
        runs = metadata['runs']
        expected = metadata['expected_plan']
        assert len(runs) == len(expected)
        assert len({json.dumps(r['spec'], sort_keys=True) for r in runs}) == len(expected)
        assert {json.dumps(r['spec'], sort_keys=True) for r in runs} == {json.dumps(s, sort_keys=True) for s in expected}
        if batch == 'baseline':
            assert metadata['source_sha256'] == hashes['baseline']
        else:
            assert metadata['base_source_sha256'] == hashes['baseline']
            assert metadata['candidate_sha256'] == hashes['candidate']
        totals[batch] = dict(runs=len(runs), completed=0, stopped=0)
        for r in runs:
            s = r['spec']
            assert r['source_sha256'] == hashes['baseline']
            if batch == 'candidate':
                assert r['candidate_sha256'] == hashes['candidate']
                assert r['base_source_sha256'] == hashes['baseline']
            assert sha(r['profile']) == r['profile_sha256']
            a, p, q = PAPER_CASES[s['case']]
            declared = metadata['parameters'][s['case']]
            assert declared['a'] == a and tuple(declared['p']) == p and tuple(declared['q']) == q
            assert declared['c'] == [1.]*len(p) and declared['phases'] == [0.]*len(p)
            ts = [h['t'] for h in r['history']]
            assert ts[0] == 0. and all(t2 > t1 for t1, t2 in zip(ts, ts[1:]))
            close('last snapshot time vs reached', abs(ts[-1]-r['reached']), 1e-12)
            assert all(t <= r['reached']+1e-12 for t in ts)
            if r['status'] == 'completed':
                close('completed target time', abs(r['reached']-s['T']), 1e-12)
            elif r['status'] == 'stopped':
                assert r['reached'] < s['T']-1e-12 and r['reason']
                assert not any(abs(t-s['T']) < 1e-12 for t in ts)
                stopped.append(dict(batch=batch, spec=s, reached=r['reached'], reason=r['reason'],
                                    recorded_times=ts, has_target_snapshot=False))
            else:
                raise AssertionError('unknown status')
            totals[batch][r['status']] += 1
            local = {k: 0. for k in maxima}
            with np.load(r['profile']) as z:
                y = z['y']; xx = z['eval_x']
                ny = round(2/s['h'])
                close('physical midpoint y', float(abs(y-(-1+(np.arange(ny)+.5)*s['h'])).max()), 1e-12)
                close('physical common x', float(abs(xx-np.linspace(-1, 1, 401)).max()), 1e-12)
                file_times = sorted(float(re.fullmatch(r't(.+)_x', k).group(1)) for k in z.files if re.fullmatch(r't(.+)_x', k))
                assert len(file_times) == len(ts)
                assert max(abs(t1-t2) for t1, t2 in zip(file_times, ts)) < 1e-12
                if r['status'] == 'stopped':
                    assert not any(abs(t-s['T']) < 1e-12 for t in file_times)
                for h in r['history']:
                    snapshot_count += 1
                    prefix = 't'+format(h['t'], 'g')
                    x = z[prefix+'_x']
                    close('fixed physical mesh endpoints', abs(x[0]+1)+abs(x[-1]-1), 1e-13)
                    assert np.all(np.isfinite(x)) and np.diff(x).min() > 0
                    exact_native = paper_uv(s['case'], y, x, h['t'])
                    exact_dense = paper_uv(s['case'], y, xx, h['t'])
                    for f, en, ed in zip(('u', 'v'), exact_native, exact_dense):
                        raw, dense = z[prefix+'_'+f], z[prefix+'_eval_'+f]
                        assert raw.shape == (ny, s['nx']) and dense.shape == (ny, len(xx))
                        assert np.all(np.isfinite(raw)) and np.all(np.isfinite(dense))
                        exact_difference = max(float(abs(z[prefix+'_exact_'+f]-en).max()), float(abs(z[prefix+'_eval_exact_'+f]-ed).max()))
                        local['independent_exact_reference'] = max(local['independent_exact_reference'], exact_difference)
                        local['physical_endpoint'] = max(local['physical_endpoint'], float(abs((raw-en)[:, [0, -1]]).max()))
                        if h['t'] == 0:
                            local['initial_native_field'] = max(local['initial_native_field'], float(abs(raw-en).max()))
                        spline = CubicSpline(x, raw, axis=-1)(xx)
                        local['saved_spline_reconstruction'] = max(local['saved_spline_reconstruction'], float(abs(spline-dense).max()))
                        error = dense-z[prefix+'_eval_exact_'+f]
                        local['error_field_readback'] = max(local['error_field_readback'], float(abs(error-z[prefix+'_error_'+f]).max()))
                        local['scalar_max_error_readback'] = max(local['scalar_max_error_readback'], abs(float(abs(error).max())-h['errors'][f]))
                        rms = np.sqrt(s['h']*np.sum(np.trapezoid(error*error, xx, axis=-1))/4)
                        local['scalar_rms_error_readback'] = max(local['scalar_rms_error_readback'], abs(float(rms)-h['rms_errors'][f]))
                        native_error = float(abs(raw-z[prefix+'_exact_'+f]).max())
                        local['nodal_max_error_readback'] = max(local['nodal_max_error_readback'], abs(native_error-h['nodal_errors'][f]))
                    assert np.all(np.isfinite(z[prefix+'_R'])) and np.all(np.isfinite(z[prefix+'_flux']))
                key = (batch,)+tuple(s[k] for k in ('case', 'mesh', 'motion', 'variant', 'nx', 'h', 'dt'))
                initial[(key, s['model'])] = tuple(z['t0_'+f].copy() for f in ('x', 'u', 'v'))
            for name, value in local.items():
                close(name, value, 5e-11 if name == 'saved_spline_reconstruction' else 1e-11)
                maxima[name] = max(maxima[name], value)
            records.append(dict(batch=batch, spec=s, status=r['status'], reached=r['reached'],
                                snapshots=len(ts), checks=local, source_hash_passed=True,
                                profile_hash_passed=True, target_snapshot_present=any(abs(t-s['T']) < 1e-12 for t in ts)))
    for (key, model), fields in initial.items():
        if model == 'SD' and (key, 'FD') in initial:
            other = initial[(key, 'FD')]
            diff = max(float(abs(a-b).max()) for a, b in zip(fields, other))
            close('same density SD/FD initial fields', diff, 1e-11)
            pairs.append(dict(type='SD_vs_FD', key=key, difference=diff))
        if key[3] == 'moving':
            frozen = list(key); frozen[3] = 'frozen'; frozen = tuple(frozen)
            if (frozen, model) in initial:
                other = initial[(frozen, model)]
                diff = max(float(abs(a-b).max()) for a, b in zip(fields, other))
                close('moving/frozen initial fields', diff, 1e-11)
                pairs.append(dict(type='moving_vs_frozen', key=key, model=model, difference=diff))
    result = dict(passed=True, audit_scope='Readback only; no PDE rerun or finite-time mathematical bound.',
                  source_sha256=hashes, audit_sha256=sha(__file__), batch_counts=totals,
                  run_count=len(records), snapshot_count=snapshot_count, independent_maxima=maxima,
                  pair_count=len(pairs), max_initial_pair_difference=max(p['difference'] for p in pairs),
                  stopped_count=len(stopped), stopped_runs_with_false_target=0,
                  records=records, initial_pairs=pairs, stopped_runs=stopped)
    (HERE/'saved_field_validation.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    with (HERE/'stopped_runs.csv').open('w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=('batch', 'case', 'model', 'mesh', 'motion', 'variant', 'reached', 'reason', 'has_target_snapshot'))
        writer.writeheader()
        for r in stopped:
            writer.writerow(dict(batch=r['batch'], **{k: r['spec'][k] for k in ('case', 'model', 'mesh', 'motion', 'variant')},
                                 reached=r['reached'], reason=r['reason'], has_target_snapshot=False))
    text = f'''# 延长时间两批保存场的独立审核

共审核 {len(records)} 条轨道、{snapshot_count} 个保存快照，全部通过原始场与冻结源码哈希、原论文直接 τ 公式、端点与误差读回检查。

- 基准批：{totals['baseline']['completed']} 条到达 T=.01，{totals['baseline']['stopped']} 条停止。
- 候选批：{totals['candidate']['completed']} 条到达 T=.01，{totals['candidate']['stopped']} 条停止。
- 共 {len(stopped)} 条停止轨道都只保存到实际 reached，没有把最后有效状态标为 T=.01。
- 原物理初值最大偏差 {maxima['initial_native_field']:.6e}；同网格 SD/FD 与 moving/frozen 的 {len(pairs)} 组初值配对最大差 {result['max_initial_pair_difference']:.6e}。
- 物理 x 端点场误差最大 {maxima['physical_endpoint']:.6e}；独立直接 τ 参照与保存精确解的最大差 {maxima['independent_exact_reference']:.6e}。
- 保存样条场、误差场、最大误差、RMS 和节点误差均从原始场重新核验。

本审核只确认数据与声明一致。达到目标时间不代表数值精度通过；停止轨道不能参与 T=.01 的误差排名。完整逐轨道记录见 saved_field_validation.json，停止清单见 stopped_runs.csv。
'''
    (HERE/'READBACK_REVIEW.md').write_text(text, encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('records', 'initial_pairs', 'stopped_runs')}, indent=2))


if __name__ == '__main__':
    main()
