"""Original DLW examples on a bounded, nonperiodic physical rectangle.

P=delta_-u is advanced with SD W=v-delta_0u or FD v. Only physical
boundary data are supplied analytically; all interior fields and mesh nodes
are advanced together by RK4. No exact interior correction or filtering.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
import argparse
import csv
import hashlib
import json
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
from scipy.special import logsumexp
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
OUT = HERE / 'out'
CASES = {
    'A': {'a': 2., 'p': [1.], 'q': [2.], 'c': [1.], 'phases': [0.]},
    'B': {'a': 2., 'p': [4.], 'q': [-3.], 'c': [1.], 'phases': [0.]},
    'C': {'a': 2., 'p': [6., 4.], 'q': [-5., -3.],
          'c': [1., 1.], 'phases': [0., 0.]},
    'D': {'a': 2., 'p': [1., 4.], 'q': [2., -3.],
          'c': [1., 1.], 'phases': [0., 0.]},
    'E': {'a': 2., 'p': [7/4, 1.], 'q': [-5/3, -4/5],
          'c': [1., 1.], 'phases': [0., 0.]},
}
TIMES = (0., .0005, .001)
EVAL_X = np.linspace(-1., 1., 401)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False,
                                    allow_nan=False) + '\n', encoding='utf-8')


class Exact:
    """Continuous positive Gram tau, evaluated at physical y and x."""
    def __init__(self, case='A'):
        self.case = CASES[case] if isinstance(case, str) else case
        p, q = np.array(self.case['p']), np.array(self.case['q'])
        a = self.case['a']
        self.S, self.T = p + q, q*q - p*p
        self.Y = 1/(p-a) + 1/(q+a)
        gamma = -(p-a)/(q+a)
        if len(p) == 1:
            self.rates = np.array([[0., 0., 0.],
                                  [self.S[0], self.T[0], self.Y[0]]])
            self.coeff = np.array([1., 1/self.S[0]])
            self.fcoef = self.coeff * np.array([1., gamma[0]])
        else:
            cross = ((p[0]-p[1])*(q[0]-q[1]) /
                     ((p[0]+q[0])*(p[0]+q[1])*(p[1]+q[0])*(p[1]+q[1])))
            self.rates = np.array([[0., 0., 0.],
                                  [self.S[0], self.T[0], self.Y[0]],
                                  [self.S[1], self.T[1], self.Y[1]],
                                  [sum(self.S), sum(self.T), sum(self.Y)]])
            self.coeff = np.array([1., 1/self.S[0], 1/self.S[1], cross])
            self.fcoef = self.coeff * np.array([1., gamma[0], gamma[1], np.prod(gamma)])
        if min(self.coeff.min(), self.fcoef.min()) <= 0:
            raise ValueError('nonpositive tau coefficient')

    def weights(self, y, x, t, is_f=False):
        y = np.atleast_1d(y)
        x = np.atleast_1d(x)
        e = (self.rates[:, 0, None, None]*x[None, None, :] +
             self.rates[:, 2, None, None]*y[None, :, None] +
             self.rates[:, 1, None, None]*t)
        e = e + np.log(self.fcoef if is_f else self.coeff)[:, None, None]
        return np.exp(e - logsumexp(e, axis=0)[None, :, :])

    def mean(self, w, k):
        return np.einsum('i,ijk->jk', self.rates[:, k], w)

    def cov(self, w, a, b):
        return (np.einsum('i,ijk->jk', self.rates[:, a]*self.rates[:, b], w) -
                self.mean(w, a)*self.mean(w, b))

    def third(self, w, a, b, c):
        aa, bb, cc = (self.mean(w, k) for k in (a, b, c))
        return np.sum(w*(self.rates[:, a, None, None]-aa)*
                      (self.rates[:, b, None, None]-bb)*
                      (self.rates[:, c, None, None]-cc), axis=0)

    def uv(self, y, x, t, derivative=False):
        f, g = self.weights(y, x, t, True), self.weights(y, x, t)
        if derivative:
            return (2*(self.cov(f, 0, 1)-self.cov(g, 0, 1)),
                    2*(self.third(f, 0, 2, 1)+self.third(g, 0, 2, 1)))
        return (2*(self.mean(f, 0)-self.mean(g, 0)),
                2*(self.cov(f, 0, 2)+self.cov(g, 0, 2)))


def derivative_matrix(n):
    """Five-point first derivative; one-sided end rows never wrap."""
    xi = np.linspace(-1., 1., n)
    dxi = xi[1]-xi[0]
    D = np.zeros((n, n))
    for i in range(n):
        ids = np.arange(min(max(i-2, 0), n-5), min(max(i-2, 0), n-5)+5)
        offsets = (xi[ids]-xi[i])/dxi
        V = np.vstack([offsets**k for k in range(5)])
        b = np.zeros(5); b[1] = 1.
        D[i, ids] = np.linalg.solve(V, b)/dxi
    return xi, D


class Grid:
    def __init__(self, nx):
        self.n = nx
        self.xi, self.D = derivative_matrix(nx)
        self.set_x(self.xi)

    def set_x(self, x):
        self.x = np.asarray(x).copy()
        self.J = self.D @ self.x
        if not np.all(np.isfinite(self.x)) or self.spacing().min() <= 0 or self.J.min() <= 0:
            raise ValueError('crossed nodes or nonpositive Jacobian')

    def spacing(self):
        return np.diff(self.x)

    def d1(self, f):
        return np.asarray(f) @ self.D.T / self.J

    def d2(self, f):
        return self.d1(self.d1(f))


def normalized_velocity(x, density, flux):
    """Finite-interval equidistribution including unequal endpoint fluxes."""
    mass = np.r_[0., np.cumsum(.5*(density[1:]+density[:-1])*np.diff(x))]
    if density.min() <= 0 or mass[-1] <= 0:
        raise ValueError('nonpositive mesh density')
    eta = mass/mass[-1]
    vel = (flux-flux[0]-eta*(flux[-1]-flux[0]))/density
    vel[0] = vel[-1] = 0.
    return vel


class Problem:
    def __init__(self, spec):
        self.spec = dict(spec)
        self.a = CASES[spec['case']]['a']
        self.h = spec['h']
        ny = int(round(2/self.h))
        self.y = -1. + (np.arange(ny)+.5)*self.h
        self.X = Grid(spec['nx'])
        self.G = Exact(spec['case'])
        self.np = (ny-1)*(self.X.n-2)
        self.nq = ny*(self.X.n-2)
        self.model = spec['model']
        self.monitor_weights = (abs(self.y[1:-1]) < .75+1e-12).astype(float)
        self.monitor_weights /= self.monitor_weights.sum()
        self.rhs_calls = 0
        self.minimum_density = np.inf
        self.minimum_jacobian = np.inf
        self.minimum_spacing = np.inf
        self._boundary_key = None
        self._boundary_value = None

    def dy(self, u, ghosts):
        ext = np.vstack((ghosts[0], u, ghosts[1]))
        return (ext[2:]-ext[:-2])/(2*self.h)

    def boundary(self, t):
        key = (float(t), self.X.x.tobytes())
        if self._boundary_key != key:
            xb = np.array([-1., 1.])
            ub, vb = self.G.uv(self.y, xb, t)
            gb = self.G.uv([self.y[0]-self.h, self.y[-1]+self.h], xb, t)[0]
            pb = np.diff(ub, axis=0)/self.h
            qb = vb-self.dy(ub, gb) if self.model == 'SD' else vb
            base = self.G.uv([self.y[0]], self.X.x, t)[0][0]
            gh = self.G.uv([self.y[0]-self.h, self.y[-1]+self.h], self.X.x, t)[0]
            self._boundary_key = key
            self._boundary_value = base, gh, pb, qb
        return self._boundary_value

    def pack(self, P, Q, x):
        return np.r_[P[:, 1:-1].ravel(), Q[:, 1:-1].ravel(), x[1:-1]]

    def unpack(self, state, t):
        self.X.set_x(np.r_[-1., state[self.np+self.nq:], 1.])
        base, gh, pb, qb = self.boundary(t)
        P = np.empty((len(self.y)-1, self.X.n))
        Q = np.empty((len(self.y), self.X.n))
        P[:, 1:-1] = state[:self.np].reshape(len(self.y)-1, -1)
        Q[:, 1:-1] = state[self.np:self.np+self.nq].reshape(len(self.y), -1)
        P[:, [0, -1]], Q[:, [0, -1]] = pb, qb
        u = np.vstack((base, base[None, :]+self.h*np.cumsum(P, axis=0)))
        # Same upper-y closure for both methods: extend the numerical perturbation
        # quadratically around the analytic boundary background. This avoids
        # an O(h^2) interior u error jumping to a zero ghost error over one cell.
        reference_top = self.G.uv(self.y[-3:], self.X.x, t)[0]
        error_top = u[-3:]-reference_top
        gh = gh.copy()
        gh[1] += 3*error_top[-1]-3*error_top[-2]+error_top[-3]
        du = self.dy(u, gh)
        v = Q+du if self.model == 'SD' else Q
        return P, Q, u, v, du, gh

    def fields(self, state, t):
        return self.unpack(state, t)[2:4]

    def initial(self):
        density_name = self.spec['mesh']
        if density_name == 'fixed':
            x = self.X.xi.copy()
        else:
            fine = np.linspace(-1., 1., 20001)
            u, v = self.G.uv(self.y, fine, 0.)
            gh = self.G.uv([self.y[0]-self.h, self.y[-1]+self.h], fine, 0.)[0]
            du = self.dy(u, gh)
            sigma = {'minus': -1, 'zero': 0, 'plus': 1}[density_name]
            den = self.monitor_weights @ (1-(v[1:-1]+sigma*du[1:-1])/4)
            if den.min() <= 0:
                raise ValueError('initial density not positive')
            mass = np.r_[0., np.cumsum(.5*(den[1:]+den[:-1])*np.diff(fine))]
            x = np.interp(np.linspace(0., mass[-1], self.X.n), mass, fine)
            x[0], x[-1] = -1., 1.
        self.X.set_x(x)
        u, v = self.G.uv(self.y, x, 0.)
        gh = self.G.uv([self.y[0]-self.h, self.y[-1]+self.h], x, 0.)[0]
        P = np.diff(u, axis=0)/self.h
        Q = v-self.dy(u, gh) if self.model == 'SD' else v
        return self.pack(P, Q, x)

    def physical_rhs(self, P, Q, u, v, du, gh):
        dx, dxx, h = self.X.d1, self.X.d2, self.h
        A = .5*u*u+2*self.a*u
        if self.model == 'SD':
            W = Q
            H = A+h*h*(W*W/32-W/4)
            pe = np.vstack(((u[0]-gh[0])/h, P, (gh[1]-u[-1])/h))
            lapP = (pe[2:]-2*pe[1:-1]+pe[:-2])/(h*h)
            Pt = -np.diff(dx(H), axis=0)/h-dxx(.5*(v[1:]+v[:-1])-h*h*lapP/4)
            Qt = -dx((u+2*self.a)*W-4*u)+dxx(W)
        else:
            Pt = -np.diff(dx(A), axis=0)/h-dxx(.5*(v[1:]+v[:-1]))
            Qt = -dx((u+2*self.a)*v-4*u)-dxx(du)
        return Pt, Qt

    def density_flux(self, P, Q, u, v, du, name=None):
        """Matched finite-h local flux, aggregated on a fixed interior y band."""
        name = name or self.spec['mesh']
        name = 'minus' if name == 'fixed' else name
        sigma = {'minus': -1, 'zero': 0, 'plus': 1}[name]
        dx, h = self.X.d1, self.h
        b, A = u+2*self.a, .5*u*u+2*self.a*u
        density = 1-(v[1:-1]+sigma*du[1:-1])/4
        if self.model == 'SD':
            W = Q
            H = A+h*h*(W*W/32-W/4)
            dh = (H[2:]-H[:-2])/(2*h)
            lapW = (W[2:]-2*W[1:-1]+W[:-2])/(h*h)
            rminus = 1-W[1:-1]/4
            qminus = b[1:-1]*rminus-dx(rminus)-2*self.a
            zplus = v[1:-1]+du[1:-1]
            qplus = -(2*dh+b[1:-1]*W[1:-1]-4*u[1:-1] +
                      dx(zplus+h*h*lapW/2))/4
            flux = qminus if sigma == -1 else qplus if sigma == 1 else .5*(qminus+qplus)
        else:
            dA = (A[2:]-A[:-2])/(2*h)
            lapv = (v[2:]-2*v[1:-1]+v[:-2])/(h*h)
            flux = -(b[1:-1]*v[1:-1]-4*u[1:-1]+sigma*dA +
                     dx(du[1:-1]+sigma*(v[1:-1]+h*h*lapv/4)))/4
        return self.monitor_weights @ density, self.monitor_weights @ flux

    def mesh_velocity(self, R, Q):
        if self.spec.get('motion', 'moving') in ('fixed', 'frozen'):
            return np.zeros(self.X.n)
        return normalized_velocity(self.X.x, R, Q)

    def rhs(self, t, state):
        self.rhs_calls += 1
        P, Q, u, v, du, gh = self.unpack(state, t)
        Pt, Qt = self.physical_rhs(P, Q, u, v, du, gh)
        R, flux = self.density_flux(P, Q, u, v, du)
        if R.min() <= 0:
            raise ValueError('evolved mesh density not positive')
        vel = self.mesh_velocity(R, flux)
        self.minimum_density = min(self.minimum_density, float(R.min()))
        self.minimum_jacobian = min(self.minimum_jacobian, float(self.X.J.min()))
        self.minimum_spacing = min(self.minimum_spacing, float(self.X.spacing().min()))
        return self.pack(Pt+vel*self.X.d1(P), Qt+vel*self.X.d1(Q), vel)


def rk4(fun, t, z, dt):
    k1 = fun(t, z)
    k2 = fun(t+dt/2, z+dt*k1/2)
    k3 = fun(t+dt/2, z+dt*k2/2)
    k4 = fun(t+dt, z+dt*k3)
    return z+dt*(k1+2*k2+2*k3+k4)/6


def spec_key(s):
    return '_'.join(str(s[k]) for k in ('case', 'model', 'mesh', 'motion', 'variant'))


def main_specs():
    specs = []
    for case in CASES:
        for model in ('SD', 'FD'):
            for mesh in ('fixed', 'minus', 'zero', 'plus'):
                motions = ['fixed'] if mesh == 'fixed' else ['moving', 'frozen']
                for motion in motions:
                    specs.append(dict(case=case, model=model, mesh=mesh, motion=motion,
                                      variant='main', nx=33, h=.125, dt=5e-6, T=.001))
    return specs


def control_specs():
    specs = []
    for main in main_specs():
        if main['motion'] == 'frozen':
            continue
        for variant in ('time_half', 'x_half', 'y_half', 'combined'):
            s = dict(main, variant=variant)
            if variant in ('time_half', 'x_half', 'combined'):
                s['dt'] /= 2
            if variant in ('x_half', 'combined'):
                s['nx'] = 65
            if variant in ('y_half', 'combined'):
                s['h'] /= 2
            specs.append(s)
    return specs


def one(s):
    start = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    p = Problem(s)
    state = p.initial()
    initial_x = p.X.x.copy()
    reference0 = p.G.uv(p.y, EVAL_X, 0.)
    peaks = {f: float(abs(a).max()) for f, a in zip(('u', 'v'), reference0)}
    arrays = {'y': p.y.copy(), 'eval_x': EVAL_X.copy(), 'monitor_y': p.y[1:-1],
              'monitor_weights': p.monitor_weights.copy()}
    history = []
    reached = 0.
    status, reason = 'completed', ''

    def sample(t):
        P, Q, u, v, du, gh = p.unpack(state, t)
        nodal_exact = p.G.uv(p.y, p.X.x, t)
        dense_exact = p.G.uv(p.y, EVAL_X, t)
        dense = [CubicSpline(p.X.x, field, axis=-1)(EVAL_X) for field in (u, v)]
        R, flux = p.density_flux(P, Q, u, v, du)
        errors, rms, nodal = {}, {}, {}
        for f, a, b, na, nb in zip(('u', 'v'), dense, dense_exact, (u, v), nodal_exact):
            err = a-b
            errors[f] = float(abs(err).max())
            rms[f] = float(np.sqrt(p.h*np.sum(np.trapezoid(err*err, EVAL_X, axis=-1))/4))
            nodal[f] = float(abs(na-nb).max())
            arrays[f't{t:g}_eval_{f}'] = a.copy()
            arrays[f't{t:g}_eval_exact_{f}'] = b.copy()
            arrays[f't{t:g}_error_{f}'] = err.copy()
            arrays[f't{t:g}_{f}'] = na.copy()
            arrays[f't{t:g}_exact_{f}'] = nb.copy()
        arrays[f't{t:g}_x'] = p.X.x.copy()
        arrays[f't{t:g}_R'] = R.copy()
        arrays[f't{t:g}_flux'] = flux.copy()
        history.append(dict(t=float(t), errors=errors, rms_errors=rms, nodal_errors=nodal,
                            relative_initial_peaks={f: errors[f]/peaks[f] for f in errors},
                            min_R=float(R.min()), max_R=float(R.max()), min_J=float(p.X.J.min()),
                            min_dx=float(p.X.spacing().min()), max_dx=float(p.X.spacing().max()),
                            max_displacement=float(abs(p.X.x-initial_x).max()),
                            endpoint_flux_difference=float(flux[-1]-flux[0])))

    sample(0.)
    steps = round(s['T']/s['dt'])
    samples = {round(t/s['dt']): t for t in TIMES[1:] if t <= s['T']+1e-15}
    for j in range(1, steps+1):
        try:
            with np.errstate(over='raise', invalid='raise', divide='raise'):
                cand = rk4(p.rhs, (j-1)*s['dt'], state, s['dt'])
                if not np.all(np.isfinite(cand)) or abs(cand[:p.np+p.nq]).max() > 1000:
                    raise ValueError('nonfinite state or magnitude exceeded 1000')
                p.unpack(cand, j*s['dt'])
        except (ValueError, FloatingPointError, OverflowError) as exc:
            status, reason = 'stopped', str(exc)
            break
        state = cand
        reached = j*s['dt']
        if j in samples:
            sample(samples[j])
    if abs(history[-1]['t']-reached) > 1e-12:
        sample(reached)
    path = OUT/(spec_key(s)+'.npz')
    np.savez_compressed(path, **arrays)
    result = dict(spec=s, status=status, reason=reason, reached=float(reached), history=history,
                  initial_peaks=peaks, rhs_calls=p.rhs_calls,
                  min_R_all_stages=float(p.minimum_density), min_J_all_stages=float(p.minimum_jacobian),
                  min_dx_all_stages=float(p.minimum_spacing),
                  elapsed_seconds=time.perf_counter()-start,
                  profile=str(path.resolve()), profile_sha256=sha(path), source_sha256=sha(__file__))
    dump(OUT/(spec_key(s)+'.json'), result)
    return result


def consolidate():
    runs = [json.loads(path.read_text(encoding='utf-8')) for path in sorted(OUT.glob('*.json'))
            if path.name != 'results.json']
    runs = [r for r in runs if 'spec' in r]
    for r in runs:
        if r['source_sha256'] != sha(__file__) or sha(r['profile']) != r['profile_sha256']:
            raise ValueError('run source or field hash mismatch')
    dump(OUT/'results.json', dict(parameters=CASES, domain={'x': [-1, 1], 'y': [-1, 1]},
                                 times=TIMES, expected_plan=main_specs()+control_specs(),
                                 source_sha256=sha(__file__), runs=runs))
    rows = []
    for r in runs:
        for h in r['history']:
            for f in ('u', 'v'):
                rows.append({**r['spec'], 'status': r['status'], 't': h['t'], 'field': f,
                             'max_error': h['errors'][f], 'rms_error': h['rms_errors'][f],
                             'nodal_max_error': h['nodal_errors'][f],
                             'relative_initial_peak': h['relative_initial_peaks'][f],
                             'min_R': h['min_R'], 'min_J': h['min_J'], 'min_dx': h['min_dx'],
                             'max_displacement': h['max_displacement']})
    if rows:
        with (OUT/'errors.csv').open('w', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0]))
            writer.writeheader(); writer.writerows(rows)
    return runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', choices=('main', 'controls', 'all', 'smoke'), default='main')
    ap.add_argument('--workers', type=int, default=2)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    specs = main_specs() if args.stage == 'main' else control_specs()
    if args.stage == 'all':
        specs = main_specs()+control_specs()
    if args.stage == 'smoke':
        specs = [main_specs()[0], next(s for s in main_specs() if s['model'] == 'SD' and s['mesh'] == 'plus'),
                 next(s for s in main_specs() if s['model'] == 'FD' and s['mesh'] == 'plus')]
    todo = []
    for s in specs:
        dest = OUT/(spec_key(s)+'.json')
        if dest.exists():
            saved = json.loads(dest.read_text(encoding='utf-8'))
            if saved['spec'] != s or saved['source_sha256'] != sha(__file__) or sha(saved['profile']) != saved['profile_sha256']:
                raise ValueError('existing run differs from frozen implementation')
        else:
            todo.append(s)
    if args.workers == 1:
        for s in todo:
            r = one(s)
            print(spec_key(s), r['status'], r['reached'], r['history'][-1]['errors'], flush=True)
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            fs = {pool.submit(one, s): s for s in todo}
            for f in as_completed(fs):
                r = f.result()
                print(spec_key(r['spec']), r['status'], r['reached'], r['history'][-1]['errors'], flush=True)
    runs = consolidate()
    print('SAVED', len(runs), 'of', len(main_specs()+control_specs()), flush=True)


if __name__ == '__main__':
    main()
