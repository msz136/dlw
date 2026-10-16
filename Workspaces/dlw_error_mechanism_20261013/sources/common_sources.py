"""Exact Gram-reference source decomposition for the FROZEN paper solver.

source_parts(obj, t) returns physical pack(p=delta_-u, v) vectors.
y_model: analytic-x semidiscrete physical RHS minus exact time derivative.
x_stencil: true exterior-reference centered stencil minus analytic-x RHS.
x_wrap: actual periodic-x RHS minus true-exterior stencil RHS.
This diagnostic changes no solver and retains the time-dependent y closure.
"""
from pathlib import Path
import importlib.util
import numpy as np

ROOT = Path(__file__).resolve().parents[3]


def load_solver():
    path = ROOT / 'Workspaces/dlw_three_tracks_20261013/generate_shared.py'
    spec = importlib.util.spec_from_file_location('source_frozen_solver', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.load_solver()


def exact_jets(obj, t, x=None, js=None):
    """Analytic u,v, first/second x derivatives and exact first t derivative.

    Derivatives of log(tau) are joint cumulants of its fixed exponential rates.
    All fields use the original continuous Gram reference, not a new soliton.
    """
    x = obj.X.x if x is None else np.asarray(x)
    js = obj.js if js is None else np.asarray(js)
    rates = obj.G.rates
    out = {k: np.zeros((len(js), len(x))) for k in
           ('u', 'v', 'ux', 'vx', 'uxx', 'vxx', 'ut', 'vt')}
    for is_f in (False, True):
        _, weights = obj.G.tau(js, x, t, is_f)
        means = [np.einsum('a,ajk->jk', rates[:, k], weights) for k in range(3)]
        centered = [rates[:, k, None, None] - means[k] for k in range(3)]

        def moment(*ks):
            val = weights.copy()
            for k in ks:
                val *= centered[k]
            return val.sum(axis=0)

        xx = moment(0, 0)
        xy = moment(0, 2)
        sign = 1 if is_f else -1
        out['u'] += 2 * sign * means[0]
        out['ux'] += 2 * sign * xx
        out['uxx'] += 2 * sign * moment(0, 0, 0)
        out['ut'] += 2 * sign * moment(0, 1)
        out['v'] += 2 * xy
        out['vx'] += 2 * moment(0, 0, 2)
        out['vxx'] += 2 * (moment(0, 0, 0, 2) - 3 * xx * xy)
        out['vt'] += 2 * moment(0, 2, 1)
    return out


def _delta0_from_full(full, h):
    return (full[2:] - full[:-2]) / (2 * h)


def _ut_from_pt(obj, pt, exact_ut):
    return np.vstack((exact_ut[0], exact_ut[0] + obj.h * np.cumsum(pt, axis=0)))


def physical_qt(obj, ut, exact_ut, exact_ghost_ut):
    """Derivative of frozen ghost_u: exact lower, extrapolated upper error."""
    e = ut[-3:] - exact_ut[-3:]
    gl = exact_ghost_ut[0]
    gr = exact_ghost_ut[1] + 3 * e[-1] - 3 * e[-2] + e[-3]
    return _delta0_from_full(np.vstack((gl, ut, gr)), obj.h)


def _backend_rhs(obj, t, jets_full, backend, kind):
    """Same physical point, same y closure; only x differentiation changes."""
    h, a, dx = obj.h, obj.a, obj.X.dx
    # jets_full includes one true reference ghost on each x and y side.
    u = jets_full['u'][1:-1]
    v = jets_full['v'][1:-1]
    p = np.diff(u, axis=0) / h
    q = _delta0_from_full(jets_full['u'], h)
    w = v - q
    U = u + 2 * a
    H0 = u * u / 2 + 2 * a * u
    Hc = h * h * (w * w / 32 - w / 4)
    M = lambda f: (f[1:] + f[:-1]) / 2
    exact_ut = jets_full['ut'][1:-1, 1:-1]
    exact_ghost_ut = jets_full['ut'][[0, -1], 1:-1]

    if backend == 'analytic':
        ux = jets_full['ux'][1:-1, 1:-1]
        vx = jets_full['vx'][1:-1, 1:-1]
        vxx = jets_full['vxx'][1:-1, 1:-1]
        qx = _delta0_from_full(jets_full['ux'], h)[:, 1:-1]
        qxx = _delta0_from_full(jets_full['uxx'], h)[:, 1:-1]
        pxx = np.diff(jets_full['uxx'][1:-1, 1:-1], axis=0) / h
        u, v, q, w, U = [z[:, 1:-1] for z in (u, v, q, w, U)]
        wx, wxx = vx - qx, vxx - qxx
        H0x = U * ux
        N = -np.diff(h * h * (w / 16 - 1 / 4) * wx, axis=0) / h
        G = -(pxx - M(qxx))
        pt_fd = -np.diff(H0x, axis=0) / h - M(vxx)
        vt_fd = -(ux * v + U * vx) - qxx + 4 * ux
        pt_sd = pt_fd + N + G
        wt_sd = -(ux * w + U * wx - 4 * ux) + wxx
        compatibility_flux = ux * q + U * qx + vxx
    else:
        if backend == 'extended':
            d1 = lambda f: (f[:, 2:] - f[:, :-2]) / (2 * dx)
            d2 = lambda f: (f[:, 2:] - 2 * f[:, 1:-1] + f[:, :-2]) / (dx * dx)
        elif backend == 'periodic':
            d1 = lambda f: obj.X.d1(f[:, 1:-1])
            d2 = lambda f: obj.X.d2(f[:, 1:-1])
        else:
            raise ValueError(backend)
        N = -np.diff(d1(Hc), axis=0) / h
        G = -d2(p - M(q))
        pt_fd = -np.diff(d1(H0), axis=0) / h - d2(M(v))
        vt_fd = -d1(U * v) - d2(q) + 4 * d1(u)
        pt_sd = -np.diff(d1(H0 + Hc), axis=0) / h - d2(p + M(w))
        wt_sd = -d1(U * w - 4 * u) + d2(w)
        compatibility_flux = d1(U * q) + d2(v)

    ut_sd = _ut_from_pt(obj, pt_sd, exact_ut)
    qt_sd = physical_qt(obj, ut_sd, exact_ut, exact_ghost_ut)
    vt_sd = wt_sd + qt_sd
    ut_fd = _ut_from_pt(obj, pt_fd, exact_ut)
    qt_fd = physical_qt(obj, ut_fd, exact_ut, exact_ghost_ut)
    # Exact SD-FD algebra: delta pt=N+G, delta vt=C+homogeneous_qt(N+G).
    C = qt_fd + compatibility_flux
    if kind == 'SD':
        pt, ut, vt = pt_sd, ut_sd, vt_sd
    elif kind == 'FD':
        pt, ut, vt = pt_fd, ut_fd, vt_fd
    else:
        raise ValueError(kind)
    return {'p': pt, 'u': ut, 'v': vt, 'N': N, 'G': G, 'C': C,
            'sd_minus_fd_p': pt_sd - pt_fd,
            'sd_minus_fd_u': ut_sd - ut_fd,
            'sd_minus_fd_v': vt_sd - vt_fd,
            'qt_difference': qt_sd - qt_fd}


def source_parts(obj, t, details=False):
    """Source vectors in physical pack(p,v), directly usable in tangent transport.

    total = F_actual(t,z_ref)-z_ref_t = y_model+x_stencil+x_wrap.
    z_ref is physical (p,v), native_ref is solver (p,w) for SD.
    Three components are added at the same reference point and same h/dx.
    y_model includes the prescribed physical y closure, not a periodic model.
    """
    if not np.allclose(obj.X.J, 1) or not np.allclose(obj.X.s, 0):
        raise ValueError('Decomposition currently requires the frozen fixed uniform x grid.')
    kind = 'SD' if obj.kind == 'SD' else 'FD' if obj.kind == 'FD' else None
    if kind is None:
        raise ValueError('Only frozen SD and FD are supported.')
    xext = np.r_[obj.X.x[0] - obj.X.dx, obj.X.x, obj.X.x[-1] + obj.X.dx]
    jext = np.r_[obj.js[0] - 1, obj.js, obj.js[-1] + 1]
    jets = exact_jets(obj, t, xext, jext)
    ref = {k: jets[k][1:-1, 1:-1] for k in ('u', 'v', 'ut', 'vt')}
    ref['p'] = np.diff(ref['u'], axis=0) / obj.h
    ref['pt'] = np.diff(ref['ut'], axis=0) / obj.h
    rhs = {b: _backend_rhs(obj, t, jets, b, kind)
           for b in ('analytic', 'extended', 'periodic')}
    source = {}
    for name, pos, neg in (('y_model', rhs['analytic'], {'p': ref['pt'], 'u': ref['ut'], 'v': ref['vt']}),
                           ('x_stencil', rhs['extended'], rhs['analytic']),
                           ('x_wrap', rhs['periodic'], rhs['extended'])):
        source[name] = {k: pos[k] - neg[k] for k in ('p', 'u', 'v')}
    source['total'] = {k: rhs['periodic'][k] - ref[{'p': 'pt', 'u': 'ut', 'v': 'vt'}[k]]
                       for k in ('p', 'u', 'v')}
    pack = lambda fields: obj.pack(fields['p'], fields['v'])
    ans = {k: pack(v) for k, v in source.items()}
    ans['z_ref'] = obj.pack(ref['p'], ref['v'])
    ans['z_ref_t'] = obj.pack(ref['pt'], ref['vt'])
    q = _delta0_from_full(jets['u'], obj.h)[:, 1:-1]
    ans['native_ref'] = obj.pack(ref['p'], ref['v'] - q if kind == 'SD' else ref['v'])
    # Independent call to the frozen native RHS and exact output-map derivative.
    native_p, native_second = obj.unpack(obj.rhs(t, ans['native_ref']))
    native_ut = _ut_from_pt(obj, native_p, ref['ut'])
    native_vt = native_second
    if kind == 'SD':
        native_vt = native_vt + physical_qt(obj, native_ut, ref['ut'], jets['ut'][[0, -1], 1:-1])
    actual = obj.pack(native_p, native_vt)
    ans['checks'] = {
        'actual_rhs_max_difference': float(np.max(np.abs(actual - pack(rhs['periodic'])))),
        'sum_source_max_difference': float(np.max(np.abs(ans['total'] - ans['y_model'] - ans['x_stencil'] - ans['x_wrap']))),
        'sd_fd_p_algebra_max_difference': float(max(np.max(np.abs(v['sd_minus_fd_p'] - v['N'] - v['G'])) for v in rhs.values())),
        'sd_fd_v_algebra_max_difference': float(max(np.max(np.abs(v['sd_minus_fd_v'] - v['C'] - v['qt_difference'])) for v in rhs.values())),
    }
    if details:
        ans.update(fields=source, reference=ref, backend_rhs=rhs)
    return ans
