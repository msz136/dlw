"""Direct staggered bilinear DLW: alternating linear implicit-midpoint solves.

The evolving unknowns are F_j and G_j, stored as logarithms for scaling.
Only the lower G and the x boundary strips are supplied analytically.
No P/W state or analytic interior time reset is used.
"""
from __future__ import annotations
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import time
import numpy as np
from scipy.special import logsumexp
from scipy.sparse import diags, eye
from scipy.sparse.linalg import spsolve

CASES = {'A': ((1.,), (2.,)), 'B': ((4.,), (-3.,)),
         'C': ((6., 4.), (-5., -3.))}

class GramTau:
    def __init__(self, case, h=.125, a=2.):
        self.case, self.h, self.a = case, h, a
        p, q = map(np.asarray, CASES[case])
        d = h/2
        chi = np.log((p-a+d)/(p-a-d)) + np.log((q+a+d)/(q+a-d))
        eta = np.log(-(p-a+d)/(q+a-d))
        if len(p) == 1:
            subsets = np.array([[0.], [1.]])
            coefficients = np.array([1., 1/(p[0]+q[0])])
        else:
            subsets = np.array([[0., 0.], [1., 0.], [0., 1.], [1., 1.]])
            cross = ((p[0]-p[1])*(q[0]-q[1])/
                ((p[0]+q[0])*(p[0]+q[1])*(p[1]+q[0])*(p[1]+q[1])))
            coefficients = np.array([1., 1/(p[0]+q[0]), 1/(p[1]+q[1]), cross])
        self.logcoef = np.log(coefficients)
        self.k = subsets@(p+q)
        self.omega = subsets@(q*q-p*p)
        self.chi = subsets@chi
        self.eta = subsets@eta

    def evaluate(self, js, x, t, f=False):
        js, x = np.atleast_1d(js), np.atleast_1d(x)
        terms = (self.logcoef[:, None, None]+self.k[:, None, None]*x[None, None, :]
                 +self.omega[:, None, None]*t+self.chi[:, None, None]*js[None, :, None])
        if f:
            terms = terms+self.eta[:, None, None]
        value = logsumexp(terms, axis=0)
        weights = np.exp(terms-value)
        dx = np.einsum('k,kji->ji', self.k, weights)
        dt = np.einsum('k,kji->ji', self.omega, weights)
        dxx = np.einsum('k,kji->ji', self.k*self.k, weights)-dx*dx
        return value, dx, dxx, dt

    def fields(self, js, x, t):
        js = np.asarray(js)
        def u(layers):
            return (2*self.evaluate(layers, x, t, True)[1]
                    -self.evaluate(layers, x, t)[1]-self.evaluate(layers+1, x, t)[1])
        uu = u(js)
        w = 4/self.h*(self.evaluate(js+1, x, t)[1]-self.evaluate(js, x, t)[1])
        return uu, w+(u(js+1)-u(js-1))/(2*self.h)

    def bilinear_residual(self, js, x, t):
        _, fx, fxx, ft = self.evaluate(js, x, t, True)
        residuals = []
        for offset, drift in ((0, 2*self.a-self.h), (1, 2*self.a+self.h)):
            _, gx, gxx, gt = self.evaluate(np.asarray(js)+offset, x, t)
            residuals.append(fxx+gxx+(fx-gx)**2+ft-gt+drift*(fx-gx))
        return max(float(abs(r).max()) for r in residuals)

@dataclass
class Config:
    intervals: int = 256
    L: float = 40.
    h: float = .125
    yhalf: float = 1.5
    dt: float = .000125
    T: float = .01
    boundary_width: int = 4

class DirectBilinear:
    def __init__(self, case, cfg=Config()):
        self.cfg = cfg
        self.exact = GramTau(case, cfg.h)
        self.x = np.linspace(-cfg.L/2, cfg.L/2, cfg.intervals+1)
        self.dx = cfg.L/cfg.intervals
        n = round(cfg.yhalf/cfg.h)
        self.js = np.arange(-n, n)
        self.gs = np.r_[self.js, self.js[-1]+1]
        self.N = len(self.x)
        self.d1 = diags([np.full(self.N, c/(12*self.dx)) for c in (1, -8, 8, -1)],
                        (-2, -1, 1, 2), shape=(self.N, self.N), format='csr')
        self.d2 = (self.d1@self.d1).tocsr()
        b = cfg.boundary_width
        self.inside = np.arange(b, self.N-b)
        self.outside = np.r_[np.arange(b), np.arange(self.N-b, self.N)]
        self.initial = (self.exact.evaluate(self.js, self.x, 0., True)[0],
                        self.exact.evaluate(self.gs, self.x, 0.)[0])
        self.max_residual = 0.
        self.linear_solves = 0
        self.min_ratio = np.inf

    def scaled_operator(self, matrix, logs):
        out = matrix.copy()
        rows = np.repeat(np.arange(self.N), np.diff(out.indptr))
        out.data *= np.exp(logs[out.indices]-logs[rows])
        return out

    def derivative_ratios(self, logs):
        c1 = self.scaled_operator(self.d1, logs)
        c2 = self.scaled_operator(self.d2, logs)
        return np.asarray(c1.sum(axis=1)).ravel(), np.asarray(c2.sum(axis=1)).ravel()

    def matrix_for(self, old_unknown, midpoint_known, s, solve_f):
        x1, x2 = self.derivative_ratios(midpoint_known)
        c1 = self.scaled_operator(self.d1, old_unknown)
        c2 = self.scaled_operator(self.d2, old_unknown)
        if solve_f:
            return c2+diags(2*s-2*x1)@c1+diags(x2-2*s*x1)
        return c2+diags(-2*s-2*x1)@c1+diags(x2+2*s*x1)

    def solve_one(self, old_unknown, old_known, new_known, exact_boundary, s, solve_f, dt):
        midpoint_known = np.logaddexp(old_known, new_known)-np.log(2.)
        known_ratio = np.exp(new_known-old_known)
        midpoint_ratio = (1+known_ratio)/2
        spatial = self.matrix_for(old_unknown, midpoint_known, s, solve_f)
        signed = (1. if solve_f else -1.)*dt/2*(diags(midpoint_ratio)@spatial)
        matrix = eye(self.N, format='csr')+signed
        rhs = known_ratio-np.asarray(signed.sum(axis=1)).ravel()
        ratio = np.empty(self.N)
        ratio[self.outside] = np.exp(exact_boundary-old_unknown[self.outside])
        reduced_rhs = rhs[self.inside]-matrix[self.inside][:, self.outside]@ratio[self.outside]
        ratio[self.inside] = spsolve(matrix[self.inside][:, self.inside].tocsc(), reduced_rhs)
        self.linear_solves += 1
        self.min_ratio = min(self.min_ratio, float(ratio.min()))
        residual = np.asarray(matrix@ratio-rhs)[self.inside]
        self.max_residual = max(self.max_residual, float(abs(residual).max()))
        if not np.isfinite(ratio).all() or ratio.min() <= 0:
            raise FloatingPointError('direct midpoint produced a nonpositive or nonfinite tau ratio')
        return old_unknown+np.log(ratio)

    def advance(self, alpha, beta, t, dt):
        newalpha, newbeta = np.empty_like(alpha), np.empty_like(beta)
        newbeta[0] = self.exact.evaluate([self.gs[0]], self.x, t+dt)[0][0]
        fb = self.exact.evaluate(self.js, self.x[self.outside], t+dt, True)[0]
        gb = self.exact.evaluate(self.gs, self.x[self.outside], t+dt)[0]
        for k in range(len(self.js)):
            newalpha[k] = self.solve_one(alpha[k], beta[k], newbeta[k], fb[k],
                                         self.exact.a-self.cfg.h/2, True, dt)
            newbeta[k+1] = self.solve_one(beta[k+1], alpha[k], newalpha[k], gb[k+1],
                                          self.exact.a+self.cfg.h/2, False, dt)
        return newalpha, newbeta

    def recover(self, alpha, beta, t):
        # u uses the log derivative, the same continuum definition as the reference.
        ax, bx = alpha@self.d1.T, beta@self.d1.T
        u = 2*ax-bx[:-1]-bx[1:]
        w = 4/self.cfg.h*(bx[1:]-bx[:-1])
        lower, upper = self.exact.fields([self.js[0]-1, self.js[-1]+1], self.x, t)[0]
        ext = np.vstack((lower, u, upper))
        return u, w+(ext[2:]-ext[:-2])/(2*self.cfg.h)

    def run(self):
        started = time.perf_counter()
        alpha, beta = (x.copy() for x in self.initial)
        cfg = self.cfg
        steps = round(cfg.T/cfg.dt)
        assert np.isclose(steps*cfg.dt, cfg.T)
        reached, reason = 0., ''
        checkpoints = []
        for n in range(steps):
            try:
                candidate_a, candidate_b = self.advance(alpha, beta, n*cfg.dt, cfg.dt)
                if max(abs(candidate_a).max(), abs(candidate_b).max()) > 1e4:
                    raise FloatingPointError('log tau amplitude exceeded 10000')
                alpha, beta = candidate_a, candidate_b
                reached = (n+1)*cfg.dt
            except (FloatingPointError, ValueError, RuntimeError) as error:
                reason = str(error)
                break
            if n+1 in {1, steps//4, steps//2, steps}:
                checkpoints.append(self.errors(alpha, beta, reached))
        final = self.errors(alpha, beta, reached)
        record = dict(case=self.exact.case, config=asdict(cfg), completed=not reason and reached >= cfg.T-1e-14,
            reached=reached, reason=reason, seconds=time.perf_counter()-started,
            linear_solves=self.linear_solves, normalized_linear_residual=self.max_residual,
            minimum_step_tau_ratio=self.min_ratio, checkpoints=checkpoints, final=final,
            exact_bilinear_residual=self.exact.bilinear_residual(self.js, self.x, reached),
            reference='Finite-h staggered Gram tau, not continuous DLW tau',
            boundaries='Analytic lowest G; analytic 4-node strips at each x boundary',
            initial=self.errors(*self.initial, 0.))
        return record, dict(x=self.x, js=self.js, alpha=alpha, beta=beta,
                           u=self.recover(alpha, beta, reached)[0], v=self.recover(alpha, beta, reached)[1])

    def errors(self, alpha, beta, t):
        exact_a = self.exact.evaluate(self.js, self.x, t, True)[0]
        exact_b = self.exact.evaluate(self.gs, self.x, t)[0]
        u, v = self.recover(alpha, beta, t)
        ue, ve = self.exact.fields(self.js, self.x, t)
        projected_u, projected_v = self.recover(exact_a, exact_b, t)
        mask = abs(self.x) <= 10
        return dict(t=float(t), logF=float(abs(alpha[:, mask]-exact_a[:, mask]).max()),
            logG=float(abs(beta[:, mask]-exact_b[:, mask]).max()),
            u=float(abs(u[:, mask]-ue[:, mask]).max()), v=float(abs(v[:, mask]-ve[:, mask]).max()),
            propagated_u=float(abs(u[:, mask]-projected_u[:, mask]).max()),
            propagated_v=float(abs(v[:, mask]-projected_v[:, mask]).max()))

def main():
    here = Path(__file__).resolve().parent
    output = here/'out'
    output.mkdir(exist_ok=True)
    records = []
    for case in CASES:
        for intervals, divisor in ((256, 1), (256, 2), (256, 4), (512, 1)):
            cfg = Config(intervals=intervals, dt=.000125/divisor)
            solver = DirectBilinear(case, cfg)
            record, arrays = solver.run()
            label = f'{case}_n{intervals}_dt{divisor}'
            np.savez_compressed(output/(label+'.npz'), **arrays)
            (output/(label+'.json')).write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
            records.append(record)
            (output/'results.json').write_text(json.dumps(records, indent=2)+'\n', encoding='utf-8')
            print(label, record['completed'], record['reached'], record['final'], flush=True)
    print('DONE', len(records), flush=True)

if __name__ == '__main__':
    main()
