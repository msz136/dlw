# config
CASES = {'A': ((1.,), (2.,)), 'B': ((4.,), (-3.,)), 'C': ((6., 4.), (-5., -3.)), 'D': ((1., 4.), (2., -3.))}
HALF_WIDTHS = {'A': 5., 'B': 10., 'C': 30., 'D': 30.}
COMPUTE_HALF_WIDTHS = {'A': 10., 'B': 20., 'C': 40., 'D': 40.}
CONFIG = dict(a=2., h=.1, dt=.0001, T=.01)
CASE_CONFIGS = {case: dict(CONFIG, L=2*COMPUTE_HALF_WIDTHS[case], nx=round(2*COMPUTE_HALF_WIDTHS[case]/.1), yhalf=COMPUTE_HALF_WIDTHS[case], eval_yhalf=half,
                            eval_half=half, eval_points=round(2*half/.01)+1)
                for case, half in HALF_WIDTHS.items()}
def case_config(case):
    return dict(CASE_CONFIGS[case])
MODELS = ('SD', 'SD2', 'FD')
COLORS = dict(SD='#1776bc', SD2='#d47b19', FD='#38965f')
pd.DataFrame([{'case': k, 'p': p, 'q': q} for k, (p, q) in CASES.items()])


# reference
class Exact:
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

# spatial
class Grid:
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

# sd_fd
class PhysicalModel:
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

# sd
class SDModel(PhysicalModel):
    def initial(self):
        u, v = self.G.uv(self.js, self.X.x, 0.)
        ghosts = self.G.uv([self.js[0]-1, self.js[-1]+1], self.X.x, 0.)[0]
        # P = delta_- u, W = 4 omega / h = v - delta_0 u.
        return self.pack(np.diff(u, axis=0)/self.h,
                         v-delta0(u, ghosts, self.h))

    def fields(self, z, t):
        p, w = self.unpack(z)
        u = self.recover_u(p, t)
        ghosts = ghost_u(self.G, self.js, self.X.x, t, u)
        return u, w+delta0(u, ghosts, self.h)

    def rhs(self, t, z):
        p, w = self.unpack(z)
        u = self.recover_u(p, t)
        d1, d2, h, a = self.X.d1, self.X.d2, self.h, self.a
        # This is Report (7) after omega = h W / 4.
        H = u*u/2+2*a*u+h*h*(w*w/32-w/4)
        pt = -np.diff(d1(H), axis=0)/h-d2(p+(w[1:]+w[:-1])/2)
        wt = -d1((u+2*a)*w-4*u)+d2(w)
        return self.pack(pt, wt)

# fd
class FDModel(PhysicalModel):
    def rhs(self, t, z):
        p, v = self.unpack(z)
        u = self.recover_u(p, t)
        ghosts = ghost_u(self.G, self.js, self.X.x, t, u)
        uy = delta0(u, ghosts, self.h)
        d1, d2, h, a = self.X.d1, self.X.d2, self.h, self.a
        fp = -np.diff(d1(u*u/2+2*a*u), axis=0)/h-d2((v[1:]+v[:-1])/2)
        fv = -d1((u+2*a)*v)-d2(uy)+4*d1(u)
        return self.pack(fp, fv)

# time
def step(fun, t, state, dt, method):
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

def solve(case, model, method, mesh, config=None):
    config = case_config(case) if config is None else config
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
    margins = [float(xx[0]-p.X.x[0]), float(p.X.x[-1]-xx[-1])]
    assert min(margins) > 0, 'Evaluation region exceeds native numerical support'
    ymask = abs(p.m.y) < config['eval_yhalf']
    sampled = [CubicSpline(p.X.x, f[ymask], axis=-1, extrapolate=False)(xx) for f in native]
    assert all(np.isfinite(f).all() for f in sampled)
    exact = p.m.G.uv(p.m.js[ymask], xx, reached)
    errors = {f: abs(u-v) for f, u, v in zip(('u', 'v'), sampled, exact)}
    return dict(case=case, model=model, method=method, mesh=mesh,
        reached=reached, completed=not reason and np.isclose(reached, config['T']), reason=reason,
        initial_error=initial_error, x=xx, y=p.m.y[ymask], fields=sampled, exact=exact,
        errors=errors, max_errors={f: float(e.max()) for f, e in errors.items()},
        min_J=float(p.X.J.min()), native_x=p.X.x.copy(), native_fields=native,
        cn_diagnostics=cn_diagnostics, support_margins=margins, state=state.copy(), native_y=p.m.y.copy())

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