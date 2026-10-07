"""Independent audit of Notebook SD tau midpoint and moving-grid ALE.

The raw bilinear residual below uses explicit NumPy stencils. It does not call
SDModel.matrix_for, scaled_operator, derivative_ratios, D1 or D2.
Only definition cells are loaded; no full report experiment is executed.
"""
from pathlib import Path
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MPLBACKEND', 'Agg')
import ast
import hashlib
import json
import time
import numpy as np
from sd_tau_cell import CELLS_SD
from dlw_numeric_cells import CELLS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NOTEBOOK = ROOT / 'notebook/DLW数值分析report.ipynb'
EVIDENCE = HERE / 'gsg_second_order'


def definitions():
    notebook = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
    cells = {c['id']: ''.join(c['source']) for c in notebook['cells']}
    ns = {'__name__': 'independent_tau_audit'}
    for name in ('dlw-imports', 'dlw-config', 'dlw-reference', 'dlw-spatial',
                 'dlw-sd_fd', 'dlw-sd2_lift', 'dlw-sd2_evolution', 'dlw-fd',
                 'dlw-sd', 'dlw-mesh'):
        assert cells[name].strip() == CELLS[name[4:]].strip(), name + ' is stale'
        exec(compile(cells[name], str(NOTEBOOK) + ':' + name, 'exec'), ns)
    return ns, cells


def dxi(f, spacing):
    return (np.roll(f, -1, axis=-1)-np.roll(f, 1, axis=-1))/(2*spacing)


def dxi2(f, spacing):
    return (np.roll(f, -1, axis=-1)-2*f+np.roll(f, 1, axis=-1))/spacing**2


def raw_bilinear_pair(a0, a1, b0, b1, spacing, jacobian, drift, dt, inside):
    # One constant scale per tau row, common to the old and new time levels.
    # Bilinear homogeneity permits this scaling without changing the equation.
    af = np.maximum(a0.max(axis=1), a1.max(axis=1))[:, None]
    bg = np.maximum(b0.max(axis=1), b1.max(axis=1))[:, None]
    f0, f1 = np.exp(a0-af), np.exp(a1-af)
    g0, g1 = np.exp(b0-bg), np.exp(b1-bg)
    fm, gm = (f0+f1)/2, (g0+g1)/2
    def dx(f):
        return dxi(f, spacing)/jacobian
    def dxx(f):
        return (dxi2(f, spacing)/jacobian**2
                - dxi(jacobian, spacing)*dxi(f, spacing)/jacobian**3)
    fx, gx = dx(fm), dx(gm)
    fxx, gxx = dxx(fm), dxx(gm)
    time_term = (f1*g0-f0*g1)/dt
    spatial = fxx*gm-2*fx*gx+fm*gxx+drift*(fx*gm-fm*gx)
    scale = f0*g0
    residual = (time_term+spatial)/scale
    size = (abs(time_term)+abs(fxx*gm)+2*abs(fx*gx)+abs(fm*gxx)
            +abs(drift*(fx*gm-fm*gx)))/scale
    result = {
        'maximum_B_divided_by_old_tau_product': float(abs(residual[:, inside]).max()),
        'maximum_B_relative_to_term_sum': float((abs(residual[:, inside]) /
            np.maximum(1., size[:, inside])).max()),
        'maximum_temporal_term_divided_by_old_tau_product': float(
            abs(time_term[:, inside]/scale[:, inside]).max()),
    }
    return result


def audit_step(ns, case, mesh):
    cfg = dict(ns['CONFIG'])
    p = ns['Problem'](case, 'SD', mesh, cfg)
    old = p.initial()
    m, n, dt = p.m, p.X.n, cfg['dt']
    a0, b0 = (x.copy() for x in m.unpack(old[:-n]))
    s0 = old[-n:].copy()
    initial_fields = p.fields(old, 0.)
    exact_initial = m.G.uv(m.js, p.X.x, 0.)
    initial_error = max(float(abs(u-v).max()) for u, v in zip(initial_fields, exact_initial))
    x0 = p.X.x.copy()
    references = {}
    for scheme in ('SD2', 'FD'):
        other = ns['Problem'](case, scheme, mesh, cfg)
        other_state = other.initial()
        assert np.allclose(other.X.x, x0, rtol=0, atol=1e-13)
        f = other.fields(other_state, 0.)
        references[scheme] = max(float(abs(u-v).max()) for u, v in zip(initial_fields, f))
    new = m.step(0., old, dt, mesh)
    a1, b1 = (x.copy() for x in m.unpack(new[:-n]))
    s1 = new[-n:].copy()
    velocity = (s1-s0)/dt
    midpoint_jacobian = 1+dxi((s0+s1)/2, p.X.dx)
    pairs = []
    for offset, sign in ((0, -1), (1, 1)):
        drift = 2*m.a+sign*m.h-velocity
        pair = raw_bilinear_pair(a0, a1, b0[offset:offset+len(m.js)],
            b1[offset:offset+len(m.js)], p.X.dx, midpoint_jacobian,
            drift, dt, m.inside)
        pair['pair'] = 'F_j,G_j' if offset == 0 else 'F_j,G_(j+1)'
        pair['passed'] = pair['maximum_B_relative_to_term_sum'] < 2e-8
        pairs.append(pair)
    boundary_a, boundary_b = m.analytic_tau(p.X.xi+s1, dt)
    boundary_errors = {
        'lowest_G_log_error': float(abs(b1[0]-boundary_b[0]).max()),
        'F_boundary_strip_log_error': float(abs(a1[:, m.outside]-boundary_a[:, m.outside]).max()),
        'G_boundary_strip_log_error': float(abs(b1[:, m.outside]-boundary_b[:, m.outside]).max()),
    }
    wrong_ale = []
    old_metric = 1+dxi(s0, p.X.dx)
    old_metric_results = []
    if mesh == 'moving':
        for offset, sign in ((0, -1), (1, 1)):
            wrong_ale.append(raw_bilinear_pair(a0, a1,
                b0[offset:offset+len(m.js)], b1[offset:offset+len(m.js)],
                p.X.dx, midpoint_jacobian, 2*m.a+sign*m.h+velocity,
                dt, m.inside)['maximum_B_divided_by_old_tau_product'])
            old_metric_results.append(raw_bilinear_pair(a0, a1,
                b0[offset:offset+len(m.js)], b1[offset:offset+len(m.js)],
                p.X.dx, old_metric, 2*m.a+sign*m.h-velocity,
                dt, m.inside)['maximum_B_divided_by_old_tau_product'])
    p.X.set_s(s0)
    v0 = m.mesh_velocity(old[:-n], 0.)
    p.X.set_s(s1)
    v1 = m.mesh_velocity(new[:-n], dt)
    mesh_equation_error = float(abs(s1-s0-dt*(v0+v1)/2).max()) if mesh == 'moving' else float(abs(s1-s0).max())
    # A small perturbation only changes interior F and an interior G layer.
    # The lowest G and the prescribed boundary strips are left unchanged.
    perturbed = old.copy()
    pa, pb = m.unpack(perturbed[:-n])
    bump = 1e-7*np.exp(-((x0-.3)/.8)**2)
    bump[m.outside] = 0
    row = len(m.js)//2
    pa[row] += bump
    pb[row+1] -= .4*bump
    before_delta = max(float(abs(pa-a0).max()), float(abs(pb-b0).max()))
    p.X.set_s(s0)
    perturbed_new = m.step(0., perturbed, dt, mesh)
    aa, bb = m.unpack(perturbed_new[:-n])
    after_delta = max(float(abs(aa[:, m.inside]-a1[:, m.inside]).max()),
                      float(abs(bb[:, m.inside]-b1[:, m.inside]).max()))
    correct_maximum = max(p['maximum_B_divided_by_old_tau_product'] for p in pairs)
    negative_threshold = max(1e-7, 20*correct_maximum)
    negative_controls_detected = (mesh != 'moving' or
        min(wrong_ale+old_metric_results) > negative_threshold)
    return {
        'case': case, 'mesh': mesh, 'dt': dt, 'raw_bilinear_pairs': pairs,
        'shared_initial_u_v_max_error': initial_error,
        'initial_u_v_difference_from_other_schemes': references,
        'prescribed_boundary_checks': boundary_errors,
        'midpoint_mesh_equation_max_error': mesh_equation_error,
        'minimum_midpoint_J': float(midpoint_jacobian.min()),
        'maximum_mesh_velocity': float(abs(velocity).max()),
        'wrong_ALE_plus_velocity_B_residual': wrong_ale,
        'using_old_instead_of_midpoint_J_B_residual': old_metric_results,
        'negative_control_detection_threshold': negative_threshold,
        'ALE_and_midpoint_metric_negative_controls_detected': negative_controls_detected,
        'initial_tau_perturbation_max': before_delta,
        'propagated_tau_perturbation_max': after_delta,
        'perturbation_remains_in_evolved_interior': after_delta > 1e-10,
        'linear_solves_including_perturbed_step': m.linear_solves,
        'maximum_mesh_iterations': m.max_mesh_iterations,
    }


def no_old_pw_check(ns):
    base = ns['PhysicalModel']
    names = ('pack', 'unpack', 'recover_u', 'initial', 'fields')
    original = {name: getattr(base, name) for name in names}
    def forbidden(*args, **kwargs):
        raise AssertionError('Old P/W PhysicalModel method was used by SD')
    try:
        for name in names:
            setattr(base, name, forbidden)
        p = ns['Problem']('A', 'SD', 'fixed', ns['CONFIG'])
        initial = p.initial()
        end = p.m.step(0., initial, ns['CONFIG']['dt'], 'fixed')
        p.fields(end, ns['CONFIG']['dt'])
    finally:
        for name, method in original.items():
            setattr(base, name, method)
    tree = ast.parse(CELLS_SD)
    node = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'SDModel')
    assert not node.bases
    return {'old_PhysicalModel_methods_disabled_during_SD_test': True,
            'SDModel_has_no_PhysicalModel_base': True,
            'state_components': ['log_F_all_24_layers', 'log_G_all_25_layers', 'mesh_shift'],
            'old_P_W_state_used': False}


def main():
    started = time.perf_counter()
    ns, cells = definitions()
    rows = [audit_step(ns, case, mesh) for case in ns['CASES'] for mesh in ('fixed', 'moving')]
    independence = no_old_pw_check(ns)
    report_matches = {
        'first_linear_equation_has_plus_LHS_minus_RHS': r'G_j^nF_j^{n+1}+\frac{\Delta t}{2}' in cells['dlw-sd-text'],
        'second_linear_equation_has_minus_LHS_plus_RHS': r'F_j^nG_{j+1}^{n+1}-\frac{\Delta t}{2}' in cells['dlw-sd-text'],
        'ALE_report_has_minus_V_over_2': r's_\pm-V/2' in cells['dlw-mesh-text'],
        'solve_dispatches_SD_direct_midpoint': "if model == 'SD' else" in cells['dlw-time'],
    }
    passed = all(all(p['passed'] for p in r['raw_bilinear_pairs'])
        and r['shared_initial_u_v_max_error'] < 1e-10
        and max(r['initial_u_v_difference_from_other_schemes'].values()) < 1e-10
        and max(r['prescribed_boundary_checks'].values()) < 1e-10
        and r['midpoint_mesh_equation_max_error'] < 2e-12
        and r['minimum_midpoint_J'] > 0
        and r['ALE_and_midpoint_metric_negative_controls_detected']
        and r['perturbation_remains_in_evolved_interior'] for r in rows)
    passed = passed and all(report_matches.values())
    summary = {'passed': bool(passed), 'seconds': time.perf_counter()-started,
        'scope': 'Six independent one-step A/B/C fixed/moving audits; not a full-time completion test',
        'residual_formula': 'delta_t(F)*Gbar-Fbar*delta_t(G)+D2(Fbar)*Gbar-2*D1(Fbar)*D1(Gbar)+Fbar*D2(Gbar)+(2s-V)*(D1(Fbar)*Gbar-Fbar*D1(Gbar))',
        'independent_stencils': True,
        'time_sign': 'Same Fnew*Gold-Fold*Gnew sign for both B equations',
        'space_metric': 'J=1+Dxi((s_old+s_new)/2); D1=J^-1 Dxi; D2=J^-2 Dxi2-(Dxi J)J^-3 Dxi',
        'stencils': 'Dxi=(f[i+1]-f[i-1])/(2d); Dxi2=(f[i+1]-2f[i]+f[i-1])/d^2',
        'recurrence': 'G_j(new) -> F_j(new) -> G_(j+1)(new)',
        'report_matches': report_matches,
        'notebook_definition_sources_sha256': {k: hashlib.sha256(v.encode()).hexdigest()
            for k, v in cells.items() if k.startswith('dlw-') and k[4:] in CELLS},
        'old_P_W_independence': independence, 'rows': rows}
    EVIDENCE.mkdir(exist_ok=True)
    target = EVIDENCE / 'verify_dlw_tau.json'
    target.write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'passed': passed, 'seconds': summary['seconds'], 'file': str(target),
        'max_raw_relative_residual': max(p['maximum_B_relative_to_term_sum'] for r in rows for p in r['raw_bilinear_pairs']),
        'max_initial_error': max(r['shared_initial_u_v_max_error'] for r in rows)}, ensure_ascii=False), flush=True)
    if not passed:
        raise AssertionError('Independent tau audit failed; inspect verify_dlw_tau.json')


if __name__ == '__main__':
    main()
