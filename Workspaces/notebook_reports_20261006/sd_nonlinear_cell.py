"""Notebook cell for the first nonlinear DLW semi-discrete system."""

CELLS_SD = r'''class SDModel(PhysicalModel):
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
'''
