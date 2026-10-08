"""Self-contained code cells for the DLW numerical report."""
CELLS = {}
CELLS['imports'] = r'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import logsumexp
from scipy.interpolate import CubicSpline
from scipy.sparse import bmat, csc_matrix, coo_matrix, diags
from scipy.sparse.linalg import splu
from IPython.display import display

plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 11,
    'axes.linewidth': .7, 'axes.spines.top': False,
    'axes.spines.right': False, 'xtick.direction': 'in',
    'ytick.direction': 'in', 'figure.dpi': 110})
'''
CELLS['config'] = r'''CASES = {'A': ((1.,), (2.,)), 'B': ((4.,), (-3.,)),
         'C': ((6., 4.), (-5., -3.))}
# 计算域为 x∈[-L/2, L/2]；绘图区间须包含在评价区间内。
CONFIG = dict(
    a=2., h=.125, yhalf=1.5,       # 方程参数、y 格距、y 半宽
    L=40., nx=256,                 # x 计算域长度、网格点数
    dt=.000125, T=.01,             # 时间步长、终止时间
    eval_half=10., eval_points=4001,  # 误差评价区间 [-eval_half, eval_half]
    plot_xlim=(-5., 5.),           # 误差曲线的 x 范围
)
if not (0 < CONFIG['eval_half'] < CONFIG['L']/2):
    raise ValueError('评价区间须位于计算域 (-L/2, L/2) 内。')
if not np.isfinite(CONFIG['plot_xlim']).all() or not (
    -CONFIG['eval_half'] <= CONFIG['plot_xlim'][0] < CONFIG['plot_xlim'][1] <= CONFIG['eval_half']
):
    raise ValueError('plot_xlim 须递增且位于评价区间内；可调整 eval_half 和 L。')
MODELS = ('SD', 'SD2', 'FD')
COLORS = dict(SD='#1776bc', SD2='#d47b19', FD='#38965f')
pd.DataFrame([{'算例': k, 'p': p, 'q': q} for k, (p, q) in CASES.items()])
'''
CELLS['reference'] = r'''class Exact:
    def __init__(self, case, h, a=2.):
        p, q = map(np.asarray, CASES[case])
        self.h = h
        s, omega, ell = p+q, q*q-p*p, 1/(p-a)+1/(q+a)
        gamma = np.log(-(p-a)/(q+a))
        if len(p) == 1:
            self.coeff = np.array([1., 1/s[0]])
            subsets = np.array([[0.], [1.]])
        else:
            cross = ((p[0]-p[1])*(q[0]-q[1]) /
                ((p[0]+q[0])*(p[0]+q[1])*(p[1]+q[0])*(p[1]+q[1])))
            self.coeff = np.array([1., 1/s[0], 1/s[1], cross])
            subsets = np.array([[0., 0.], [1., 0.], [0., 1.], [1., 1.]])
        self.rates = subsets @ np.stack((s, omega, ell), axis=1)
        self.gamma = subsets @ gamma
        self._key, self._cache = None, {}

    def tau(self, js, x, t, is_f=False):
        y = (np.atleast_1d(js)+.5)*self.h
        logs = (np.log(self.coeff)[:, None, None]
            + self.rates[:, 0, None, None]*np.atleast_1d(x)[None, None, :]
            + self.rates[:, 1, None, None]*t
            + self.rates[:, 2, None, None]*y[None, :, None])
        if is_f:
            logs = logs + self.gamma[:, None, None]
        total = logsumexp(logs, axis=0)
        return total, np.exp(logs-total[None, :, :])

    def mean(self, w, k):
        return np.einsum('i,ijk->jk', self.rates[:, k], w)

    def cov(self, w, a, b):
        return (np.einsum('i,ijk->jk', self.rates[:, a]*self.rates[:, b], w)
                - self.mean(w, a)*self.mean(w, b))

    def uv(self, js, x, t):
        key = (float(t), np.asarray(x).tobytes())
        if key != self._key:
            self._key, self._cache = key, {}
        sub = tuple(np.atleast_1d(js))
        if sub not in self._cache:
            _, f = self.tau(js, x, t, True)
            _, g = self.tau(js, x, t)
            self._cache[sub] = (2*(self.mean(f, 0)-self.mean(g, 0)),
                2*(self.cov(f, 0, 2)+self.cov(g, 0, 2)))
        return tuple(v.copy() for v in self._cache[sub])
'''
CELLS['spatial'] = r'''class Grid:
    def __init__(self, n, L):
        self.n, self.L, self.dx = n, L, L/n
        self.xi = -L/2 + np.arange(n)*self.dx
        ii = np.arange(n)
        self.Dxi = coo_matrix((np.concatenate([np.full(n, c/(2*self.dx))
            for c in (-1, 1)]), (np.tile(ii, 2),
            np.concatenate([(ii+k) % n for k in (-1, 1)]))),
            shape=(n, n)).tocsr()
        self.Dxxi = coo_matrix((np.concatenate([np.full(n, c/self.dx**2)
            for c in (1, -2, 1)]), (np.tile(ii, 3),
            np.concatenate([(ii+k) % n for k in (-1, 0, 1)]))),
            shape=(n, n)).tocsr()
        self.set_s(np.zeros(n))

    def neighbors(self, f, jump=0.):
        # f(xi+L)=f(xi)+jump；周期场取 jump=0。
        f = np.asarray(f, dtype=np.result_type(f, jump, float))
        left, right = np.roll(f, 1, axis=-1), np.roll(f, -1, axis=-1)
        left[..., :1] -= jump
        right[..., -1:] += jump
        return left, right

    def dxi(self, f, jump=0.):
        left, right = self.neighbors(f, jump)
        return (right-left)/(2*self.dx)

    def dxxi(self, f, jump=0.):
        left, right = self.neighbors(f, jump)
        return (right-2*f+left)/self.dx**2

    def set_s(self, s):
        self.s = np.asarray(s).copy()
        self.x, self.J = self.xi+self.s, 1+self.dxi(self.s)
        self.Jxi = self.dxi(self.J)
        if self.J.min() <= 0 or np.diff(np.r_[self.x, self.x[0]+self.L]).min() <= 0:
            raise ValueError('网格 Jacobian 非正或节点交叉')

    def d1(self, f, jump=0.):
        return self.dxi(f, jump)/self.J

    def d2(self, f, jump=0.):
        return (self.dxxi(f, jump)/self.J**2
                -self.Jxi*self.dxi(f, jump)/self.J**3)

def delta0(u, ghosts, h):
    ext = np.concatenate((ghosts[0][None, :], u, ghosts[1][None, :]))
    return (ext[2:]-ext[:-2])/(2*h)

def ghost_u(G, js, x, t, u):
    gl, gr = G.uv([js[0]-1, js[-1]+1], x, t)[0]
    # 上侧外推扰动；解析背景与内部数值解分开处理。
    e = u[-3:]-G.uv(js[-3:], x, t)[0]
    return gl, gr+3*e[-1]-3*e[-2]+e[-3]
'''
CELLS['sd_fd'] = r'''class PhysicalModel:
    def __init__(self, case, model, config):
        self.kind, self.h, self.a = model, config['h'], config['a']
        self.X = Grid(config['nx'], config['L'])
        self.G = Exact(case, self.h, self.a)
        n = round(config['yhalf']/self.h)
        self.js = np.arange(-n, n)
        self.y = (self.js+.5)*self.h
        self.shape = (len(self.js), self.X.n)
        self.np = (len(self.js)-1)*self.X.n

    def pack(self, p, w):
        return np.r_[p.ravel(), w.ravel()]

    def unpack(self, z):
        return z[:self.np].reshape(self.shape[0]-1, -1), z[self.np:].reshape(self.shape)

    def recover_u(self, p, t):
        base = self.G.uv([self.js[0]], self.X.x, t)[0][0]
        return np.vstack((base, base+self.h*np.cumsum(p, axis=0)))

    def initial(self):
        u, v = self.G.uv(self.js, self.X.x, 0.)
        ghosts = self.G.uv([self.js[0]-1, self.js[-1]+1], self.X.x, 0.)[0]
        w = v
        return self.pack(np.diff(u, axis=0)/self.h, w)

    def fields(self, z, t):
        p, w = self.unpack(z)
        u = self.recover_u(p, t)
        ghosts = ghost_u(self.G, self.js, self.X.x, t, u)
        return u, w

'''
CELLS['sd2_lift'] = r'''class SD2Lift(PhysicalModel):
    def __init__(self, case, config):
        super().__init__(case, 'SD2', config)
        n, dx = self.X.n, self.X.dx
        self.D = self.X.Dxi.tocsc()
        self.b = np.zeros(n)
        self.b[0] = self.b[-1] = 1/(2*dx)
        self.norm = csc_matrix(([1.], ([0], [0])), shape=(1, n))
        self.initial_right, self._boundary_key = None, None
        self.jump = self.rjump = 0.

    def dx(self, f, jump=0.):
        return self.X.d1(f, jump)

    def lift(self, u):
        A = bmat([[self.D-diags(.5*self.X.J*u), csc_matrix(self.b[:, None])],
                  [self.norm, csc_matrix((1, 1))]], format='csc')
        lu = splu(A)
        sol = lu.solve(np.r_[np.zeros(self.X.n), 1.])
        q, jump = sol[:-1], sol[-1]
        if q.min() <= 0 or 1+jump <= 0:
            raise ValueError('SD2 提升后的 Q 或端点比值非正')
        return q, jump, lu

    def boundary(self, t):
        key = (float(t), self.X.x.tobytes(), self.X.J.tobytes())
        if key != self._boundary_key:
            _, f = self.G.tau([self.js[0]], self.X.x, t, True)
            _, g = self.G.tau([self.js[0]], self.X.x, t)
            u = 2*(self.G.mean(f, 0)-self.G.mean(g, 0))[0]
            ut = 2*(self.G.cov(f, 0, 1)-self.G.cov(g, 0, 1))[0]
            ux = 2*(self.G.cov(f, 0, 0)-self.G.cov(g, 0, 0))[0]
            q, jump, lu = self.lift(u)
            self._boundary_key = key
            self._boundary_value = q, jump, lu, u, ut, ux
        q, jump, lu, u, ut, ux = self._boundary_value
        if self.initial_right is not None:
            right = self.initial_right*(1+jump)/self.initial_right[0]
            self.jump, self.rjump = (right-1)[:, None], (1/right-1)[:, None]
        return self._boundary_value

    def boundary_derivative(self, t, velocity):
        q, jump, lu, u, ut, ux = self.boundary(t)
        rhs = .5*(self.D@velocity*u+self.X.J*(ut+velocity*ux))*q
        material_qt = lu.solve(np.r_[rhs, 0.])[:-1]
        qx = (self.D@q+self.b*jump)/self.X.J
        return material_qt-velocity*qx

    def pack(self, q, r):
        return np.r_[q[1:].ravel(), r.ravel()]

    def unpack(self, z, t):
        q = np.vstack((self.boundary(t)[0], z[:self.np].reshape(self.shape[0]-1, -1)))
        return q, z[self.np:].reshape(self.shape)

    def initial(self):
        u, v = self.G.uv(self.js, self.X.x, 0.)
        lifted = [self.lift(row) for row in u]
        q = np.array([v[0] for v in lifted])
        self.initial_right = 1+np.array([v[1] for v in lifted])
        self._boundary_key = None
        self.boundary(0.)
        ghosts = self.G.uv([self.js[0]-1, self.js[-1]+1], self.X.x, 0.)[0]
        r = (1-(v-delta0(u, ghosts, self.h))/4)/q
        return self.pack(q, r)
'''
CELLS['sd2_evolution'] = r'''class SD2Model(SD2Lift):
    def fields(self, z, t):
        q, r = self.unpack(z, t)
        u = 2*self.dx(q, self.jump)/q
        ghosts = ghost_u(self.G, self.js, self.X.x, t, u)
        return u, 4*(1-q*r)+delta0(u, ghosts, self.h)

    def stage(self, t, state, mesh):
        self.X.set_s(state[-self.X.n:])
        q, r = self.unpack(state[:-self.X.n], t)
        if q.min() <= 0:
            raise ValueError('演化后的 Q 非正')
        qx, rx = self.dx(q, self.jump), self.dx(r, self.rjump)
        w = q*r
        velocity = np.zeros(self.X.n)
        if mesh == 'moving':
            density = w.mean(axis=0)
            flux = ((2*qx/q+2*self.a)*w-self.dx(w)-2*self.a).mean(axis=0)
            if density.min() <= 0:
                raise ValueError('动网格监测密度非正')
            velocity = (flux-flux[0])/density
        qt0 = self.boundary_derivative(t, velocity)
        qxx = self.X.d2(q, self.jump)
        rxx, wx = self.X.d2(r, self.rjump), self.dx(w)
        H = self.h**2/4*(w*w-1)
        A0 = -(qt0+qxx[0]+2*self.a*qx[0])/q[0]-H[0]
        mx0 = (A0+self.h*wx[0])/2
        mx = mx0-self.h*np.vstack((np.zeros(self.X.n), np.cumsum(wx, axis=0)))
        A = mx[:-1]+mx[1:]
        qt = -qxx-2*self.a*qx-(A+H)*q
        rt = rxx-2*self.a*rx+(A+H)*r
        return np.r_[self.pack(qt+velocity*qx, rt+velocity*rx), velocity]
'''
CELLS['mesh'] = r'''class Problem:
    def __init__(self, case, model, mesh, config=CONFIG):
        self.mesh, self.model = mesh, model
        self.m = SD2Model(case, config) if model == 'SD2' else (SDModel if model == 'SD' else FDModel)(case, model, config)
        self.X = self.m.X

    def initial(self):
        if self.mesh == 'moving':
            x = np.linspace(-self.X.L/2, self.X.L/2, 40001)
            u, v = self.m.G.uv(self.m.js, x, 0.)
            gh = self.m.G.uv([self.m.js[0]-1, self.m.js[-1]+1], x, 0.)[0]
            density = 1-(v-delta0(u, gh, self.m.h)).mean(axis=0)/4
            if density.min() <= 0:
                raise ValueError('初始监测密度非正')
            mass = np.r_[0, np.cumsum((density[:-1]+density[1:])*np.diff(x)/2)]
            nodes = np.interp(np.arange(self.X.n)/self.X.n*mass[-1], mass, x)
            self.X.set_s(nodes-self.X.xi)
        return np.r_[self.m.initial(), self.X.s]

    def fields(self, state, t):
        self.X.set_s(state[-self.X.n:])
        return self.m.fields(state[:-self.X.n], t)

    def stage(self, t, state):
        if self.model == 'SD2':
            return self.m.stage(t, state, self.mesh)
        z = state[:-self.X.n]
        self.X.set_s(state[-self.X.n:])
        physical = self.m.rhs(t, z)
        velocity = np.zeros(self.X.n)
        if self.mesh == 'moving':
            u, v = self.m.fields(z, t)
            ghosts = ghost_u(self.m.G, self.m.js, self.X.x, t, u)
            rho = 1-(v-delta0(u, ghosts, self.m.h))/4
            density = rho.mean(axis=0)
            flux = ((u+2*self.m.a)*rho-self.X.d1(rho)-2*self.m.a).mean(axis=0)
            if density.min() <= 0:
                raise ValueError('动网格监测密度非正')
            velocity = (flux-flux[0])/density
            p, w = self.m.unpack(z)
            physical += self.m.pack(self.X.d1(p)*velocity, self.X.d1(w)*velocity)
        return np.r_[physical, velocity]
'''
CELLS['time'] = r'''def step(fun, t, state, dt, method):
    if method == 'Euler':
        return state+dt*fun(t, state)
    if method == 'CN':
        # 隐式梯形法：两端右端的平均，不是中点状态的右端。
        f0 = fun(t, state)
        candidate = state+dt*f0
        tolerance = 1e-12+1e-11*max(1., float(np.max(abs(state))))
        for iteration in range(1, 81):
            residual = candidate-state-dt*(f0+fun(t+dt, candidate))/2
            residual_max = float(np.max(abs(residual)))
            if residual_max <= tolerance:
                step.cn_last = dict(iterations=iteration, residual=residual_max, tolerance=tolerance)
                return candidate
            candidate = candidate-residual
        raise ValueError(f'Crank–Nicolson 隐式迭代未收敛：残差 {residual_max:.3e}')
    if method != 'RK4':
        raise ValueError('时间算法应为 Euler、RK4 或 CN')
    k1 = fun(t, state)
    k2 = fun(t+dt/2, state+dt*k1/2)
    k3 = fun(t+dt/2, state+dt*k2/2)
    k4 = fun(t+dt, state+dt*k3)
    return state+dt*(k1+2*k2+2*k3+k4)/6

def solve(case, model, method, mesh, config=CONFIG):
    if method not in ('Euler', 'RK4', 'CN'):
        raise ValueError('时间算法应为 Euler、RK4 或 CN')
    p = Problem(case, model, mesh, config)
    state = p.initial()
    initial = p.fields(state, 0.)
    initial_ref = p.m.G.uv(p.m.js, p.X.x, 0.)
    mask = abs(p.X.x) <= config['eval_half']
    initial_error = max(float(abs(u[:, mask]-v[:, mask]).max())
                        for u, v in zip(initial, initial_ref))
    nsteps = round(config['T']/config['dt'])
    if not np.isclose(nsteps*config['dt'], config['T'], rtol=0, atol=1e-13):
        raise ValueError('T 必须是 dt 的整数倍')
    reached, reason = 0., ''
    cn_diagnostics = []
    for n in range(nsteps):
        try:
            with np.errstate(over='raise', invalid='raise', divide='raise'):
                candidate = step(p.stage, n*config['dt'], state, config['dt'], method)
                if method == 'CN':
                    cn_diagnostics.append(dict(step.cn_last))
                if not np.all(np.isfinite(candidate)) or abs(candidate).max() > 1000:
                    raise ValueError('状态非有限或绝对值超过 1000')
                p.X.set_s(candidate[-p.X.n:])
        except (ValueError, FloatingPointError, OverflowError) as e:
            reason = str(e)
            break
        state, reached = candidate, (n+1)*config['dt']
    xx = np.linspace(-config['eval_half'], config['eval_half'], config['eval_points'])
    native = p.fields(state, reached)
    sampled = [CubicSpline(p.X.x, f, axis=-1)(xx) for f in native]
    exact = p.m.G.uv(p.m.js, xx, reached)
    errors = {f: abs(u-v) for f, u, v in zip(('u', 'v'), sampled, exact)}
    return dict(case=case, model=model, method=method, mesh=mesh,
        reached=reached, completed=not reason and np.isclose(reached, config['T']), reason=reason,
        initial_error=initial_error, x=xx, y=p.m.y, fields=sampled, exact=exact,
        errors=errors, max_errors={f: float(e.max()) for f, e in errors.items()},
        min_J=float(p.X.J.min()), native_x=p.X.x.copy(), native_fields=native,
        cn_diagnostics=cn_diagnostics)

results = {}
def calculate(method, mesh):
    for case in CASES:
        for model in MODELS:
            key = case, model, method, mesh
            if key not in results:
                results[key] = solve(case, model, method, mesh)
    failed = [r for r in results.values() if not r['completed']]
    if failed:
        display(pd.DataFrame([{k: r[k] for k in ('case', 'model', 'method', 'mesh', 'reached', 'reason')}
                             for r in failed]))
        raise RuntimeError('未到达共同终点，停止配对比较')

def error_table(method, mesh):
    return pd.DataFrame([{'算例': case, '场': field,
        **{m: results[case, m, method, mesh]['max_errors'][field] for m in MODELS}}
        for case in CASES for field in ('u', 'v')]).set_index(['算例', '场'])
'''
CELLS['space_experiment'] = r'''calculate('RK4', 'fixed')
space_table = error_table('RK4', 'fixed')
space_table.style.format('{:.3e}').highlight_min(axis=1, props='font-weight: bold')
'''
CELLS['time_experiment'] = r'''calculate('Euler', 'fixed')
calculate('CN', 'fixed')
time_table = pd.DataFrame([{'算例': case, '方案': model, '场': field,
    **{('Crank–Nicolson' if method == 'CN' else method): results[case, model, method, 'fixed']['max_errors'][field]
       for method in ('Euler', 'RK4', 'CN')}}
    for case in CASES for model in MODELS for field in ('u', 'v')]).set_index(['算例', '方案', '场'])
time_table.style.format('{:.3e}').highlight_min(axis=1, props='font-weight: bold')
'''
CELLS['mesh_experiment'] = r'''calculate('RK4', 'moving')
mesh_table = pd.DataFrame([{'算例': case, '方案': model, '场': field,
    **{mesh: results[case, model, 'RK4', mesh]['max_errors'][field]
       for mesh in ('fixed', 'moving')}}
    for case in CASES for model in MODELS for field in ('u', 'v')]).set_index(['算例', '方案', '场'])
mesh_table.style.format('{:.3e}').highlight_min(axis=1, props='font-weight: bold')
'''
CELLS['order'] = r'''order_rows = []
refinement_rows = []
for case in CASES:
    for model in ('SD', 'SD2'):
        fields = [results[case, model, 'Euler', 'fixed']['fields']]
        for divisor in (2, 4):
            refined = solve(case, model, 'Euler', 'fixed',
                            dict(CONFIG, dt=CONFIG['dt']/divisor))
            if not refined['completed']:
                raise RuntimeError(refined['reason'])
            fields.append(refined['fields'])
            refinement_rows.append(dict(case=case, model=model, method='Euler',
                mesh='fixed', dt=CONFIG['dt']/divisor, reached=refined['reached'],
                completed=bool(refined['completed']), min_J=refined['min_J']))
        for i, field in enumerate(('u', 'v')):
            d1 = np.max(abs(fields[0][i]-fields[1][i]))
            d2 = np.max(abs(fields[1][i]-fields[2][i]))
            order_rows.append({'算例': case, '方案': model, '场': field,
                              'dt 与 dt/2 场差': d1, 'dt/2 与 dt/4 场差': d2,
                              '观测阶': np.log2(d1/d2)})
pd.DataFrame(order_rows).set_index(['算例', '方案', '场']).style.format({
    'dt 与 dt/2 场差': '{:.3e}', 'dt/2 与 dt/4 场差': '{:.3e}', '观测阶': '{:.4f}'})
'''
CELLS['curves'] = r'''plot_lo, plot_hi = CONFIG['plot_xlim']
if not np.isfinite([plot_lo, plot_hi]).all() or plot_lo >= plot_hi:
    raise ValueError('plot_xlim 须为有限且递增的 (左端, 右端)。')
calculate('Euler', 'moving')
for case in CASES:
    for model in MODELS:
        for mesh in ('fixed', 'moving'):
            xx = results[case, model, 'Euler', mesh]['x']
            if plot_lo < xx[0] or plot_hi > xx[-1] or np.count_nonzero((xx >= plot_lo) & (xx <= plot_hi)) < 2:
                raise ValueError('plot_xlim 须位于已计算的评价区间内且包含至少两点；扩大 eval_half 后需重新计算。')
for case in CASES:
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7), layout='constrained')
    for i, field in enumerate(('u', 'v')):
        upper = max(results[case, model, 'Euler', mesh]['errors'][field][:,
            (results[case, model, 'Euler', mesh]['x'] >= plot_lo) &
            (results[case, model, 'Euler', mesh]['x'] <= plot_hi)].max()
            for model in MODELS for mesh in ('fixed', 'moving'))
        for j, mesh in enumerate(('fixed', 'moving')):
            ax = axes[i, j]
            for model, style in zip(MODELS, ('-', '--', ':')):
                r = results[case, model, 'Euler', mesh]
                take = (r['x'] >= plot_lo) & (r['x'] <= plot_hi)
                curve = r['errors'][field].max(axis=0)
                ax.plot(r['x'][take], curve[take], color=COLORS[model], ls=style,
                        lw=1.3, label=model)
            ax.set(xlabel='$x$', ylabel=f'$e_{field}(x)$', xlim=(plot_lo, plot_hi),
                   ylim=(0, upper*1.06), title=f'{field}: {mesh}')
            ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
            ax.grid(alpha=.16, lw=.5)
            ax.legend(frameon=False)
    fig.suptitle(f'Case {case} | Euler | T={CONFIG["T"]:g}')
    plt.show()
'''
CELLS['summary'] = r'''for case in CASES:
    best_u = space_table.loc[(case, 'u')].idxmin()
    best_v = space_table.loc[(case, 'v')].idxmin()
    print(f'算例 {case}：RK4 固定网格下，u / v 的最小误差方案为 {best_u} / {best_v}。')
mesh_ratios = mesh_table['moving']/mesh_table['fixed']
ratio_table = mesh_ratios.unstack('场').rename(columns={'u': 'u 动格/固定', 'v': 'v 动格/固定'})
display(ratio_table.style.format('{:.3f}'))
print(f'全部 {len(results)} 组主试验到达 T={CONFIG["T"]:g}；'
      f'初始物理场的最大节点差为 {max(r["initial_error"] for r in results.values()):.3e}。')
'''
from sd_nonlinear_cell import CELLS_SD
CELLS['sd'] = CELLS_SD

CELLS['fd'] = r'''class FDModel(PhysicalModel):
    def rhs(self, t, z):
        p, v = self.unpack(z)
        u = self.recover_u(p, t)
        ghosts = ghost_u(self.G, self.js, self.X.x, t, u)
        uy = delta0(u, ghosts, self.h)
        d1, d2, h, a = self.X.d1, self.X.d2, self.h, self.a
        fp = -np.diff(d1(u*u/2+2*a*u), axis=0)/h-d2((v[1:]+v[:-1])/2)
        fv = -d1((u+2*a)*v)-d2(uy)+4*d1(u)
        return self.pack(fp, fv)
'''
