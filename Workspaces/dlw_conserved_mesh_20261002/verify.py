"""Independent checks against the paper tau functions, then experiment API checks.

This file belongs to the verification task. It does not import the numerical
implementation to construct its reference solution.
"""
from pathlib import Path
import importlib.util
import json
import math
import hashlib
import numpy as np
import mpmath as mp

HERE = Path(__file__).resolve().parent
mp.mp.dps = 60

PAPER_CASES = {
    "fig1a": ((1,), (2,)),
    "fig1b": ((4,), (-3,)),
    "fig3": ((6, 4), (-5, -3)),
    "fig4": ((1, 4), (2, -3)),
    "fig5": ((mp.mpf(7)/4, 1), (-mp.mpf(5)/3, -mp.mpf(4)/5)),
}


def partitions(items):
    """Set partitions of labelled derivative positions."""
    if not items:
        yield []
        return
    head, *tail = items
    for part in partitions(tail):
        yield [[head], *part]
        for i in range(len(part)):
            yield [b + [head] if j == i else b[:] for j, b in enumerate(part)]


class PaperExact:
    """Positive N=1/N=2 tau functions of Physica D Eqs. 13, 29--31.

    Axes are x,y,t. Derivatives of log(tau) are joint cumulants, evaluated
    independently in high precision by the set-partition formula.
    """
    def __init__(self, name):
        self.p, self.q = map(lambda z: tuple(map(mp.mpf, z)), PAPER_CASES[name])
        self.a = mp.mpf(2)
        n = len(self.p)
        s = [p+q for p, q in zip(self.p, self.q)]
        self.rates = [[mp.mpf(0)]*3]
        self.coef = [mp.mpf(1)]
        self.gamma = [mp.mpf(1)]
        gg = [-(p-self.a)/(q+self.a) for p, q in zip(self.p, self.q)]
        for i in range(n):
            self.rates.append([s[i], 1/(self.p[i]-self.a)+1/(self.q[i]+self.a), self.q[i]**2-self.p[i]**2])
            self.coef.append(1/s[i])
            self.gamma.append(gg[i])
        if n == 2:
            cross = (self.p[0]-self.p[1])*(self.q[0]-self.q[1])
            cross /= (self.p[0]+self.q[0])*(self.p[0]+self.q[1])*(self.p[1]+self.q[0])*(self.p[1]+self.q[1])
            self.rates.append([self.rates[1][k]+self.rates[2][k] for k in range(3)])
            self.coef.append(cross)
            self.gamma.append(gg[0]*gg[1])
        assert all(c > 0 for c in self.coef)
        assert all(g > 0 for g in self.gamma)

    def at(self, x, y, t):
        point = list(map(mp.mpf, (x, y, t)))
        eg = [c*mp.exp(sum(r[k]*point[k] for k in range(3))) for c, r in zip(self.coef, self.rates)]
        ef = [z*g for z, g in zip(eg, self.gamma)]
        self.weights = [tuple(z/sum(e) for z in e) for e in (eg, ef)]
        self.cache = {}
        return self

    def log_derivative(self, f, axes):
        key = (f, tuple(sorted(axes)))
        if key in self.cache:
            return self.cache[key]
        axes = tuple(axes)
        value = mp.mpf(0)
        for part in partitions(list(range(len(axes)))):
            term = mp.mpf((-1)**(len(part)-1)*math.factorial(len(part)-1))
            for block in part:
                moment = mp.mpf(0)
                for w, rate in zip(self.weights[int(f)], self.rates):
                    product = mp.mpf(1)
                    for j in block:
                        product *= rate[axes[j]]
                    moment += w*product
                term *= moment
            value += term
        self.cache[key] = value
        return value

    def u(self, axes=()):
        return 2*(self.log_derivative(True, (0,)+tuple(axes))-self.log_derivative(False, (0,)+tuple(axes)))

    def v(self, axes=()):
        return 2*(self.log_derivative(True, (0,1)+tuple(axes))+self.log_derivative(False, (0,1)+tuple(axes)))

    def pde_residual(self):
        u, v = self.u(), self.v()
        first = self.u((1,2))+self.v((0,0))+self.u((0,))*self.u((1,))+(u+2*self.a)*self.u((0,1))
        second = self.v((2,))+self.u((0,0,1))+self.u((0,))*v+(u+2*self.a)*self.v((0,))-4*self.u((0,))
        return first, second


def independent_arrays(name, x, y, t):
    """Vectorized double precision evaluation of the independently defined taus."""
    ref = PaperExact(name)
    xx, yy = np.meshgrid(np.asarray(x), np.asarray(y))
    rr = np.asarray(ref.rates,dtype=float)
    cc = np.asarray(ref.coef,dtype=float)
    gg = np.asarray(ref.gamma,dtype=float)
    ex = rr[:,0,None,None]*xx+rr[:,1,None,None]*yy+rr[:,2,None,None]*t
    terms = cc[:,None,None]*np.exp(ex-ex.max(axis=0,keepdims=True))
    wf = terms*gg[:,None,None]
    wg = terms/terms.sum(axis=0,keepdims=True)
    wf = wf/wf.sum(axis=0,keepdims=True)
    cache = {}

    def cumulant(f, axes):
        key = (f,tuple(sorted(axes)))
        if key in cache:
            return cache[key]
        ww = wf if f else wg
        ans = np.zeros_like(xx)
        for part in partitions(list(range(len(axes)))):
            term = float((-1)**(len(part)-1)*math.factorial(len(part)-1))
            for block in part:
                rate = np.prod(rr[:,[axes[j] for j in block]],axis=1)
                term = term*np.sum(ww*rate[:,None,None],axis=0)
            ans += term
        cache[key] = ans
        return ans

    u = lambda axes: 2*(cumulant(True,(0,)+axes)-cumulant(False,(0,)+axes))
    v = lambda axes: 2*(cumulant(True,(0,1)+axes)+cumulant(False,(0,1)+axes))
    return dict(u=u(()),v=v(()),ut=u((2,)),vt=v((2,)),uy=u((1,)),
                ux=u((0,)),vx=v((0,)))


def verify_paper():
    checks = []
    max_residual = mp.mpf(0)
    max_density_residual = mp.mpf(0)
    # Physical coordinates; no old j+1/2 convention enters these evaluations.
    points = ((0,0,0), (mp.mpf("-.9"),mp.mpf(".7"),mp.mpf(".004")),
              (mp.mpf(".8"),mp.mpf("-.8"),mp.mpf(".013")))
    for name in PAPER_CASES:
        exact = PaperExact(name)
        for point in points:
            exact.at(*point)
            res = exact.pde_residual()
            max_residual = max(max_residual, *map(abs, res))
            density_residuals = {}
            u, uy, v = exact.u(), exact.u((1,)), exact.v()
            for sigma in (-1, 0, 1):
                rho = 1-(v+sigma*uy)/4
                rt = -(exact.v((2,))+sigma*exact.u((1,2)))/4
                rx = -(exact.v((0,))+sigma*exact.u((0,1)))/4
                if sigma == 0:
                    qx = exact.u((0,))*rho+(u+2*exact.a)*rx-exact.u((0,0,1))/4
                else:
                    rxx = -(exact.v((0,0))+sigma*exact.u((0,0,1)))/4
                    qx = exact.u((0,))*rho+(u+2*exact.a)*rx+sigma*rxx
                defect = rt+qx
                max_density_residual = max(max_density_residual, abs(defect))
                density_residuals[str(sigma)] = str(defect)
            checks.append(dict(case=name, point=list(map(str, point)), u=str(exact.u()),
                               v=str(exact.v()), residual=list(map(str,res)),
                               density_balance_residual=density_residuals))
    assert max_residual < mp.mpf("1e-50"), max_residual
    assert max_density_residual < mp.mpf("1e-50"), max_density_residual
    return dict(passed=True, precision_digits=mp.mp.dps,
                max_absolute_pde_residual=str(max_residual), point_checks=checks,
                max_density_balance_residual=str(max_density_residual),
                definition="u=2(log(f/g))_x, v=2(log(f*g))_xy; lambda=-2; a=2; c_i=1; all phases zero",
                source="Paper/sources/physd.txt Eqs.5,13,29-31 and captions Figs.1,3,4,5")


def verify_implementation():
    path = HERE/"experiment.py"
    source_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    spec = importlib.util.spec_from_file_location("audited_dlw_experiment",path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    names = {"A":"fig1a", "B":"fig1b", "C":"fig3", "D":"fig4", "E":"fig5"}
    records = []
    max_initial = 0.
    max_reference = 0.
    min_density = np.inf
    min_jacobian = np.inf
    for case in module.CASES:
        for nx,h in ((33,.125),(65,.125),(33,.0625),(65,.0625)):
            for model in ("SD","FD"):
                for mesh in ("fixed","minus","zero","plus"):
                    plan = dict(case=case,model=model,mesh=mesh,motion="frozen",nx=nx,h=h,
                                dt=5e-6,T=.001,variant="independent_rhs")
                    problem = module.Problem(plan)
                    state = problem.initial()
                    P,Q,u,v,du,gh = problem.unpack(state,0.)
                    ref = independent_arrays(names[case],problem.X.x,problem.y,0.)
                    initial = {"u":float(abs(u-ref["u"]).max()),
                               "v":float(abs(v-ref["v"]).max())}
                    max_initial = max(max_initial,*initial.values())
                    rt = problem.G.uv(problem.y,problem.X.x,0.,derivative=True)
                    errref = max(float(abs(rt[i]-ref[k]).max()) for i,k in enumerate(("ut","vt")))
                    max_reference = max(max_reference,errref)
                    Pt,Qt = problem.physical_rhs(P,Q,u,v,du,gh)
                    base_t = ref["ut"][0]
                    ut = np.vstack((base_t,base_t[None,:]+h*np.cumsum(Pt,axis=0)))
                    if model == "SD":
                        outer_y = [problem.y[0]-h,problem.y[-1]+h]
                        ghost_t = independent_arrays(names[case],problem.X.x,outer_y,0.)["ut"]
                        error_top_t = ut[-3:]-ref["ut"][-3:]
                        ghost_t[1] += 3*error_top_t[-1]-3*error_top_t[-2]+error_top_t[-3]
                        vt = Qt+problem.dy(ut,ghost_t)
                    else:
                        vt = Qt
                    # Actual x Dirichlet endpoints are prescribed. These defects
                    # concern the evolved x interior, including upper/lower y rows.
                    defect = {"u":float(abs(ut[:,1:-1]-ref["ut"][:,1:-1]).max()),
                              "v":float(abs(vt[:,1:-1]-ref["vt"][:,1:-1]).max())}
                    source_core = {"u":float(abs(ut[1:-1,2:-2]-ref["ut"][1:-1,2:-2]).max()),
                                   "v":float(abs(vt[1:-1,2:-2]-ref["vt"][1:-1,2:-2]).max())}
                    R,F = problem.density_flux(P,Q,u,v,du)
                    min_density = min(min_density,float(R.min()))
                    min_jacobian = min(min_jacobian,float(problem.X.J.min()))
                    records.append(dict(case=case,model=model,mesh=mesh,nx=nx,h=h,
                                        initial_native_field_error=initial,
                                        initial_physical_rhs_defect=defect,
                                        interior_y_rhs_defect=source_core,
                                        min_R=float(R.min()),min_J=float(problem.X.J.min()),
                                        max_dx=float(problem.X.spacing().max()),
                                        endpoint_flux_difference=float(F[-1]-F[0])))
    assert max_initial < 2e-12,max_initial
    assert max_reference < 2e-11,max_reference
    assert min_density > 0 and min_jacobian > 0

    grid = module.Grid(33)
    no_wrap = bool(grid.D[0,-1] == 0 and grid.D[-1,0] == 0 and
                   (grid.D@grid.D)[0,-1] == 0 and (grid.D@grid.D)[-1,0] == 0)
    assert no_wrap
    x = grid.xi+.04*(1-grid.xi**2)*np.sin(np.pi*grid.xi)
    grid.set_x(x)
    const_error = float(abs(grid.d1(np.ones_like(x))).max())
    linear_error = float(abs(grid.d1(x)-1).max())
    assert max(const_error,linear_error) < 1e-11

    # The continuum normalized-mass formula is exact for this polynomial rho;
    # trapezoidal cumulative mass is then also exact, so a separate closed form
    # checks the right-endpoint flux correction rather than copying the code.
    rho = 2+x/5
    flux = np.sin(x)+.2*x*x
    eta = (2*(x+1)+(x*x-1)/10)/4
    expected = (flux-flux[0]-eta*(flux[-1]-flux[0]))/rho
    velocity = module.normalized_velocity(x,rho,flux)
    normalized_defect = float(abs(velocity-expected).max())
    assert normalized_defect < 2e-14
    assert velocity[0] == velocity[-1] == 0

    # Independent ALE check: reference field sampled on moving physical points
    # must satisfy dU/dt=u_t+V*u_x. No numerical field is reset in this check.
    eps = 2e-7
    reference = independent_arrays("fig1a",x,[-.6,.2,.7],0.)
    plus = independent_arrays("fig1a",x+eps*velocity,[-.6,.2,.7],eps)
    minus = independent_arrays("fig1a",x-eps*velocity,[-.6,.2,.7],-eps)
    ale_errors = {}
    for f in ("u","v"):
        fd = (plus[f]-minus[f])/(2*eps)
        analytic = reference[f+"t"]+velocity*reference[f+"x"]
        ale_errors[f] = float(abs(fd-analytic).max())
    assert max(ale_errors.values()) < 2e-7,ale_errors

    # Check the implemented ALE directional derivative of physical fields,
    # including the moving analytic lower-y base and moving analytic ghosts.
    # It need not equal V times the discrete derivative of the entire field:
    # those boundary values are analytic, so their derivatives are analytic too.
    plan = dict(case="A",model="SD",mesh="plus",motion="moving",nx=33,h=.125,
                dt=5e-6,T=.001,variant="independent_ale")
    problem = module.Problem(plan)
    state = problem.initial()
    P,Q,u,v,du,gh = problem.unpack(state,0.)
    Pt,Qt = problem.physical_rhs(P,Q,u,v,du,gh)
    R,F = problem.density_flux(P,Q,u,v,du)
    vel = problem.mesh_velocity(R,F)
    slope = problem.rhs(0.,state)
    own_ref = independent_arrays("fig1a",problem.X.x,problem.y,0.)
    outer_y = [problem.y[0]-problem.h,problem.y[-1]+problem.h]
    outer = independent_arrays("fig1a",problem.X.x,outer_y,0.)
    p_material = Pt+vel*problem.X.d1(P)
    q_material = Qt+vel*problem.X.d1(Q)
    base_material = own_ref["ut"][0]+vel*own_ref["ux"][0]
    material_u = np.vstack((base_material,base_material[None,:]+problem.h*np.cumsum(p_material,axis=0)))
    outer_material = outer["ut"]+vel*outer["ux"]
    reference_material_u = own_ref["ut"]+vel*own_ref["ux"]
    error_material_top = material_u[-3:]-reference_material_u[-3:]
    outer_material[1] += 3*error_material_top[-1]-3*error_material_top[-2]+error_material_top[-3]
    material_v = q_material+problem.dy(material_u,outer_material)
    xp = problem.fields(state+eps*slope,eps)
    xm = problem.fields(state-eps*slope,-eps)
    implemented_ale = {f:float(abs((a-b)[:,1:-1]/(2*eps)-expected[:,1:-1]).max())
                       for f,a,b,expected in zip(("u","v"),xp,xm,(material_u,material_v))}
    assert max(implemented_ale.values()) < 2e-7,implemented_ale

    assert hashlib.sha256(path.read_bytes()).hexdigest() == source_hash,"Source changed during audit"
    return dict(passed=True,source_sha256=source_hash,
                cases=list(module.CASES),number_of_initial_rhs_comparisons=len(records),
                max_initial_native_field_error=max_initial,max_exact_time_derivative_disagreement=max_reference,
                min_initial_density=min_density,min_initial_J=min_jacobian,
                nonperiodic_no_opposite_endpoint_support=no_wrap,
                mapped_derivative_constant_error=const_error,mapped_derivative_linear_error=linear_error,
                normalized_mass_velocity_error=normalized_defect,
                analytic_ALE_chain_rule_error=ale_errors,
                implemented_ALE_directional_error=implemented_ale,
                initial_rhs_defects=records,
                interpretation="RHS defects are initial Eulerian field error sources; no rigorous finite-time bound follows. Analytic finite-domain boundary data are common to all methods. No time integration was performed by this checker.")


def verify_boundary_source():
    spec = importlib.util.spec_from_file_location("audited_boundary_dlw",HERE/"experiment.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    records = []
    names = {"A":"fig1a", "B":"fig1b", "C":"fig3", "D":"fig4", "E":"fig5"}
    for case,name in names.items():
        for h in (.125,.0625):
            problem = module.Problem(dict(case=case,model="SD",mesh="fixed",motion="fixed",
                                          nx=65,h=h,dt=5e-6,T=.001,variant="boundary_diagnostic"))
            state = problem.initial()
            P,Q,u,v,du,gh = problem.unpack(state,0.)
            ref = independent_arrays(name,problem.X.x,problem.y,0.)
            Pt,Qt = problem.physical_rhs(P,Q,u,v,du,gh)
            ut = np.vstack((ref["ut"][0],ref["ut"][0,None,:]+h*np.cumsum(Pt,axis=0)))
            gt = independent_arrays(name,problem.X.x,[problem.y[0]-h,problem.y[-1]+h],0.)["ut"]
            intrinsic = Qt+problem.dy(ref["ut"],gt)-ref["vt"]
            error_ut = ut-ref["ut"]
            ghost_error_ut = np.zeros_like(gt)
            ghost_error_ut[1] = 3*error_ut[-1]-3*error_ut[-2]+error_ut[-3]
            propagation = problem.dy(error_ut,ghost_error_ut)
            total = intrinsic+propagation
            jy,jx = np.unravel_index(abs(total[:,1:-1]).argmax(),total[:,1:-1].shape)
            jx += 1
            error = float(abs(total-(Qt+problem.dy(ut,gt+ghost_error_ut)-ref["vt"])).max())
            assert error < 1e-12
            records.append(dict(case=case,h=h,max_y=float(problem.y[jy]),max_x=float(problem.X.x[jx]),
                                source=float(total[jy,jx]),intrinsic=float(intrinsic[jy,jx]),
                                reconstruction_ghost_contribution=float(propagation[jy,jx]),identity_error=error))
    return dict(records=records,
                explanation="The upper y ghost carries the quadratic extrapolation of the physical u perturbation. Its time derivative must carry the same extrapolation of u_t error; using the analytic ghost derivative alone incorrectly creates an O(h) boundary source. This decomposition includes the implemented extrapolation and separates the intrinsic source from reconstructed u_t transport.")


def verify_discrete_density_balance():
    """Check the implemented monitor flux against the actual Eulerian RHS."""
    spec = importlib.util.spec_from_file_location("audited_density_dlw",HERE/"experiment.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    names = {"A":"fig1a", "B":"fig1b", "C":"fig3", "D":"fig4", "E":"fig5"}
    records = []
    for case,name in names.items():
        for model in ("SD","FD"):
            problem = module.Problem(dict(case=case,model=model,mesh="fixed",motion="fixed",
                                          nx=33,h=.125,dt=5e-6,T=.001,variant="balance_diagnostic"))
            state = problem.initial()
            P,Q,u,v,du,gh = problem.unpack(state,0.)
            ref = independent_arrays(name,problem.X.x,problem.y,0.)
            Pt,Qt = problem.physical_rhs(P,Q,u,v,du,gh)
            h = problem.h
            ut = np.vstack((ref["ut"][0],ref["ut"][0,None,:]+h*np.cumsum(Pt,axis=0)))
            gt = independent_arrays(name,problem.X.x,[problem.y[0]-h,problem.y[-1]+h],0.)["ut"]
            etop = ut[-3:]-ref["ut"][-3:]
            gt[1] += 3*etop[-1]-3*etop[-2]+etop[-3]
            dut = problem.dy(ut,gt)
            vt = Qt+dut if model == "SD" else Qt
            for density_name,sigma in (("minus",-1),("zero",0),("plus",1)):
                R,F = problem.density_flux(P,Q,u,v,du,name=density_name)
                Rt = problem.monitor_weights @ (-(vt[1:-1]+sigma*dut[1:-1])/4)
                defect = Rt+problem.X.d1(F)
                records.append(dict(case=case,model=model,density=density_name,
                                    max_local_balance_error=float(abs(defect).max())))
    maximum = max(a["max_local_balance_error"] for a in records)
    assert maximum < 2e-11,maximum
    return dict(passed=True,max_local_balance_error=maximum,records=records,
                meaning="Algebraic local balances of the strong-form spatial RHS, evaluated before x Dirichlet endpoint overwrite. This is not an exact time-discrete conservation or exact quadrature mass-conservation result.")


def main():
    out = dict(analytic_reference=verify_paper())
    if (HERE/"experiment.py").exists():
        out["implementation"] = verify_implementation()
        out["boundary_source_decomposition"] = verify_boundary_source()
        out["discrete_density_balance"] = verify_discrete_density_balance()
    (HERE/"independent_validation.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    summary = dict(pde_residual=out["analytic_reference"]["max_absolute_pde_residual"], passed=True)
    if "implementation" in out:
        a = out["implementation"]
        summary.update(comparisons=a["number_of_initial_rhs_comparisons"],
                       max_initial_error=a["max_initial_native_field_error"],
                       implemented_ALE_error=a["implemented_ALE_directional_error"])
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
