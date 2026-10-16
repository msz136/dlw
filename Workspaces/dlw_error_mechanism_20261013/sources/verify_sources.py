"""Independent numerical checks of analytic jets, coordinate derivatives and buffers."""
from pathlib import Path
import csv
import json
import numpy as np
from common_sources import load_solver, exact_jets, source_parts

HERE = Path(__file__).resolve().parent


def crop(obj, cfg, fields):
    iy = np.flatnonzero(abs(obj.y) < cfg['eval_yhalf'])
    ix = np.flatnonzero(abs(obj.X.x) <= cfg['eval_half'] + 1e-10)
    return {name: {field: values[field][np.ix_(iy, ix)] for field in ('u', 'v')}
            for name, values in fields.items()}


def main():
    ns, _ = load_solver()
    rows, bounds = [], []
    for case in ('A', 'C'):
        cfg = ns['case_config'](case)
        small = dict(cfg, h=.2, nx=round(cfg['L']/.2))
        for kind in ('SD', 'FD'):
            obj = ns[kind + 'Model'](case, kind, small)
            t = .004
            result = source_parts(obj, t, details=True)
            z = result['native_ref']
            zd = obj.rhs(t, z)
            expected = result['backend_rhs']['periodic']
            for eps in (4e-5, 2e-5, 1e-5):
                plus = obj.fields(z+eps*zd, t+eps)
                minus = obj.fields(z-eps*zd, t-eps)
                for j, field in enumerate(('u', 'v')):
                    measured = (plus[j]-minus[j])/(2*eps)
                    rows.append(dict(case=case, model=kind, check='native_output_time_derivative', field=field,
                                     epsilon=eps, max_abs=float(abs(measured-expected[field]).max()),
                                     relative_l2=float(np.linalg.norm(measured-expected[field])/np.linalg.norm(expected[field]))))
        obj = ns['SDModel'](case, 'SD', small)
        xs = np.linspace(-cfg['eval_half'], cfg['eval_half'], 31)
        js = obj.js[::max(1, len(obj.js)//17)]
        jets = exact_jets(obj, .004, xs, js)
        base = obj.G.uv(js, xs, .004)
        for eps in (.04, .02, .01):
            vals = {j: obj.G.uv(js, xs+j*eps, .004) for j in (-2, -1, 1, 2)}
            for j, field in enumerate(('u', 'v')):
                first = (vals[-2][j]-8*vals[-1][j]+8*vals[1][j]-vals[2][j])/(12*eps)
                second = (-vals[-2][j]+16*vals[-1][j]-30*base[j]+16*vals[1][j]-vals[2][j])/(12*eps**2)
                for tag, measured, key in [('fivepoint_x1', first, field+'x'), ('fivepoint_x2', second, field+'xx')]:
                    rows.append(dict(case=case, model='reference', check=tag, field=field, epsilon=eps,
                                     max_abs=float(abs(measured-jets[key]).max()),
                                     relative_l2=float(np.linalg.norm(measured-jets[key])/np.linalg.norm(jets[key]))))
        for kind in ('SD', 'FD'):
            obj = ns[kind+'Model'](case, kind, cfg)
            base = crop(obj, cfg, source_parts(obj, 0., details=True)['fields'])
            for axis in ('x', 'y'):
                expanded = dict(cfg)
                if axis == 'x':
                    expanded.update(L=cfg['L']+20, nx=round((cfg['L']+20)/.1))
                else:
                    expanded.update(yhalf=cfg['yhalf']+10)
                obj2 = ns[kind+'Model'](case, kind, expanded)
                comp = crop(obj2, expanded, source_parts(obj2, 0., details=True)['fields'])
                for source in base:
                    for field in ('u','v'):
                        diff = comp[source][field]-base[source][field]
                        bounds.append(dict(case=case, model=kind, buffer_axis=axis, extra=10, source=source, field=field,
                                           max_abs_difference=float(abs(diff).max()), rms_difference=float(np.sqrt(np.mean(diff*diff))),
                                           max_y_variation=float(abs(diff-diff.mean(axis=0,keepdims=True)).max())))
    for name, data in [('independent_validation.csv', rows), ('buffer_field_validation.csv', bounds)]:
        with (HERE/name).open('w', encoding='utf-8-sig', newline='') as f:
            writer=csv.DictWriter(f, fieldnames=list(data[0]));writer.writeheader();writer.writerows(data)
    checks = {
        'native_map_max_relative_at_smallest_epsilon': max(r['relative_l2'] for r in rows if r['check']=='native_output_time_derivative' and r['epsilon']==1e-5),
        'jet_x1_max_relative_at_smallest_epsilon': max(r['relative_l2'] for r in rows if r['check']=='fivepoint_x1' and r['epsilon']==.01),
        'jet_x2_max_relative_at_smallest_epsilon': max(r['relative_l2'] for r in rows if r['check']=='fivepoint_x2' and r['epsilon']==.01),
        'observation_buffer_max_source_difference':max(r['max_abs_difference'] for r in bounds),
        'y_buffer_u_change_max_y_variation':max(r['max_y_variation'] for r in bounds if r['buffer_axis']=='y' and r['field']=='u'),
        'y_buffer_v_change_max_abs':max(r['max_abs_difference'] for r in bounds if r['buffer_axis']=='y' and r['field']=='v'),
        'x_buffer_max_source_difference':max(r['max_abs_difference'] for r in bounds if r['buffer_axis']=='x'),
    }
    assert checks['native_map_max_relative_at_smallest_epsilon'] < 1e-7
    assert checks['jet_x1_max_relative_at_smallest_epsilon'] < 2e-6
    assert checks['jet_x2_max_relative_at_smallest_epsilon'] < 2e-6
    (HERE/'independent_validation.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
    print(json.dumps(checks,indent=2))


if __name__=='__main__':
    main()
