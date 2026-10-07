"""Notebook code cell for the direct bilinear SD midpoint update."""

CELLS_SD = r'''from scipy.sparse import eye

class SDModel:
    def __init__(self, case, model='SD', config=None):
        if isinstance(model, dict):
            config, model = model, 'SD'
        config = CONFIG if config is None else config
        self.kind, self.h, self.a = 'SD', config['h'], config['a']
        self.X = Grid(config['nx'], config['L'])
        self.G = Exact(case, self.h, self.a)
        n = round(config['yhalf']/self.h)
        self.js = np.arange(-n, n)
        self.y = (self.js+.5)*self.h
        self.shape = (len(self.js), self.X.n)
        self.nalpha = np.prod(self.shape)
        nx = self.X.n
        self.Dxi, self.Dxxi = self.X.Dxi, self.X.Dxxi
        self.inside = np.arange(4, nx-4)
        self.outside = np.r_[np.arange(4), np.arange(nx-4, nx)]
        self.identity = eye(nx, format='csr')
        self._operator_key = None
        self.linear_solves = 0
        self.max_linear_residual = 0.
        self.minimum_tau_ratio = np.inf
        self.max_mesh_iterations = 0
        self.max_mesh_residual = 0.

    def operators(self):
        key = self.X.J.tobytes()
        if key != self._operator_key:
            self.D1 = (diags(1/self.X.J)@self.Dxi).tocsr()
            self.D2 = (diags(1/self.X.J**2)@self.Dxxi
                       -diags(self.X.Jxi/self.X.J**3)@self.Dxi).tocsr()
            self._operator_key = key
        return self.D1, self.D2

    def pack(self, alpha, beta):
        return np.r_[alpha.ravel(), beta.ravel()]

    def unpack(self, z):
        return (z[:self.nalpha].reshape(self.shape),
                z[self.nalpha:].reshape(self.shape[0]+1, self.shape[1]))

    def primitives(self, x, t):
        lf, wf = self.G.tau(self.js, x, t, True)
        lg, wg = self.G.tau(self.js, x, t)
        r = 2*(lf-lg)
        primitive_v = 2*(self.G.mean(wf, 2)+self.G.mean(wg, 2))
        ext_js = np.r_[self.js[0]-1, self.js, self.js[-1]+1]
        ext_r = 2*(self.G.tau(ext_js, x, t, True)[0]
                   -self.G.tau(ext_js, x, t)[0])
        d = self.h/4*(primitive_v-(ext_r[2:]-ext_r[:-2])/(2*self.h))
        beta0 = self.G.tau([self.js[0]-.5], x, t)[0]
        return r, d, beta0

    def analytic_tau(self, x, t):
        r, d, beta0 = self.primitives(x, t)
        beta = np.vstack((beta0, beta0+np.cumsum(d, axis=0)))
        return (r+beta[:-1]+beta[1:])/2, beta

    def initial(self):
        self.operators()
        r, d, beta0 = self.primitives(self.X.x, 0.)
        u, v = self.G.uv(self.js, self.X.x, 0.)
        ghosts = self.G.uv([self.js[0]-1, self.js[-1]+1], self.X.x, 0.)[0]
        w = v-delta0(u, ghosts, self.h)
        I, B = self.inside, self.outside
        lu = splu(self.D1[I][:, I].tocsc())
        boundary = self.D1[I][:, B]
        r[:, I] = lu.solve((u[:, I]-(boundary@r[:, B].T).T).T).T
        d[:, I] = lu.solve((self.h/4*w[:, I]-(boundary@d[:, B].T).T).T).T
        beta = np.vstack((beta0, beta0+np.cumsum(d, axis=0)))
        alpha = (r+beta[:-1]+beta[1:])/2
        return self.pack(alpha, beta)

    def fields(self, z, t):
        alpha, beta = self.unpack(z)
        u = self.X.d1(2*alpha-beta[:-1]-beta[1:])
        w = 4/self.h*self.X.d1(beta[1:]-beta[:-1])
        exact_boundary = self.G.uv(self.js, self.X.x[self.outside], t)
        u[:, self.outside] = exact_boundary[0]
        ghosts = ghost_u(self.G, self.js, self.X.x, t, u)
        v = w+delta0(u, ghosts, self.h)
        v[:, self.outside] = exact_boundary[1]
        return u, v

    def scaled_operator(self, matrix, logs):
        out = matrix.copy()
        rows = np.repeat(np.arange(self.X.n), np.diff(out.indptr))
        out.data *= np.exp(logs[out.indices]-logs[rows])
        return out

    def derivative_ratios(self, logs):
        c1 = self.scaled_operator(self.D1, logs)
        c2 = self.scaled_operator(self.D2, logs)
        return np.asarray(c1.sum(axis=1)).ravel(), np.asarray(c2.sum(axis=1)).ravel()

    def matrix_for(self, old_unknown, midpoint_known, s, solve_f):
        x1, x2 = self.derivative_ratios(midpoint_known)
        c1 = self.scaled_operator(self.D1, old_unknown)
        c2 = self.scaled_operator(self.D2, old_unknown)
        if solve_f:
            return c2+diags(2*s-2*x1)@c1+diags(x2-2*s*x1)
        return c2+diags(-2*s-2*x1)@c1+diags(x2+2*s*x1)

    def solve_one(self, old_unknown, old_known, new_known, boundary, s, solve_f, dt):
        midpoint_known = np.logaddexp(old_known, new_known)-np.log(2.)
        known_ratio = np.exp(new_known-old_known)
        midpoint_ratio = (1+known_ratio)/2
        spatial = self.matrix_for(old_unknown, midpoint_known, s, solve_f)
        signed = (1. if solve_f else -1.)*dt/2*(diags(midpoint_ratio)@spatial)
        matrix = self.identity+signed
        rhs = known_ratio-np.asarray(signed.sum(axis=1)).ravel()
        I, B = self.inside, self.outside
        ratio = np.empty(self.X.n)
        ratio[B] = np.exp(boundary-old_unknown[B])
        ratio[I] = splu(matrix[I][:, I].tocsc()).solve(rhs[I]-matrix[I][:, B]@ratio[B])
        if not np.isfinite(ratio).all() or ratio.min() <= 0:
            raise ValueError('SD 中点更新的 tau 比值非正或非有限')
        residual = np.asarray(matrix@ratio-rhs)[I]
        self.linear_solves += 1
        self.max_linear_residual = max(self.max_linear_residual, float(abs(residual).max()))
        self.minimum_tau_ratio = min(self.minimum_tau_ratio, float(ratio.min()))
        return old_unknown+np.log(ratio)

    def advance(self, alpha, beta, t, dt, velocity=None, new_x=None):
        self.operators()
        velocity = np.zeros(self.X.n) if velocity is None else velocity
        new_x = self.X.x if new_x is None else new_x
        boundary_a, boundary_b = self.analytic_tau(new_x, t+dt)
        newalpha, newbeta = np.empty_like(alpha), np.empty_like(beta)
        newbeta[0] = boundary_b[0]
        for j in range(len(self.js)):
            newalpha[j] = self.solve_one(alpha[j], beta[j], newbeta[j],
                boundary_a[j, self.outside], self.a-self.h/2-velocity/2, True, dt)
            newbeta[j+1] = self.solve_one(beta[j+1], alpha[j], newalpha[j],
                boundary_b[j+1, self.outside], self.a+self.h/2-velocity/2, False, dt)
        return newalpha, newbeta

    def mesh_velocity(self, z, t):
        u, v = self.fields(z, t)
        ghosts = ghost_u(self.G, self.js, self.X.x, t, u)
        rho = 1-(v-delta0(u, ghosts, self.h))/4
        density = rho.mean(axis=0)
        if density.min() <= 0:
            raise ValueError('动网格监测密度非正')
        flux = ((u+2*self.a)*rho-self.X.d1(rho)-2*self.a).mean(axis=0)
        return (flux-flux[0])/density

    def step(self, t, state, dt, mesh='fixed'):
        s0 = state[-self.X.n:].copy()
        z0 = state[:-self.X.n]
        alpha, beta = self.unpack(z0)
        self.X.set_s(s0)
        if mesh != 'moving':
            newalpha, newbeta = self.advance(alpha, beta, t, dt)
            return np.r_[self.pack(newalpha, newbeta), s0]
        v0 = self.mesh_velocity(z0, t)
        s1 = s0+dt*v0
        for iteration in range(1, 9):
            self.X.set_s((s0+s1)/2)
            newalpha, newbeta = self.advance(alpha, beta, t, dt,
                (s1-s0)/dt, self.X.xi+s1)
            z1 = self.pack(newalpha, newbeta)
            self.X.set_s(s1)
            v1 = self.mesh_velocity(z1, t+dt)
            target = s0+dt*(v0+v1)/2
            error = float(abs(target-s1).max())
            if error <= 2e-12:
                self.max_mesh_iterations = max(self.max_mesh_iterations, iteration)
                self.max_mesh_residual = max(self.max_mesh_residual, error)
                return np.r_[z1, s1]
            s1 = target
        raise ValueError('SD 动网格中点迭代未收敛')
'''
