"""Independent checks of moving-coordinate implementation and output metrics."""
from pathlib import Path
import json
import numpy as np
from model import BranchProblem, FamilyModel, Parameters, MovingGrid, evaluate

HERE = Path(__file__).resolve().parent
checks = {}

def record(name, error, tolerance):
    checks[name] = dict(error=float(error), tolerance=tolerance, passed=bool(error<tolerance))
    assert error<tolerance, (name, error, tolerance)

def norm(x): return np.max(abs(x))


def main():
    pars = Parameters(4, 1, 3, 4)
    for route in ('fd', 'sd'):
        p = BranchProblem(pars, route=route, branch='fixed', nx=128)
        z, s = p.initial()
        original = FamilyModel(pars, route=route, nx=128, L=40)
        record(route+'_fixed_reproduces_original_rhs', norm(p.rhs(0,z,s)[0]-original.rhs(0,z)), 1e-12)
        record(route+'_fixed_zero_velocity', norm(p.rhs(0,z,s)[1]), 1e-14)

    # Smooth periodic map x=xi+0.15 sin(xi); exact physical derivative of sin(2x).
    e1, e2 = [], []
    for n in (64, 128, 256):
        X = MovingGrid(n, 2*np.pi)
        X.set_s(.15*np.sin(X.xi))
        f = np.sin(2*X.x)
        e1.append(norm(X.d1(f)-2*np.cos(2*X.x)))
        e2.append(norm(X.d2(f)+4*np.sin(2*X.x)))
    for label, es in [('d1',e1),('d2',e2)]:
        order = np.log2(np.array(es[:-1])/es[1:])
        record(label+'_mapped_fourth_order', norm(order-4), .12)

    for branch in ('minus','plus'):
        p = BranchProblem(pars, branch=branch)
        z,s = p.initial()
        R,_ = p.density_flux(0,z)
        I,Ranalytic = p.initial_potential_density(p.X.x)
        record(branch+'_initial_density_matches_primitive', norm(R-Ranalytic), 2e-13)
        ends = p.initial_potential_density(np.array([-20.,20.]))[0]
        target = ends[0]+np.arange(p.X.n)/p.X.n*(ends[1]-ends[0])
        record(branch+'_equal_mass_initial_nodes', norm(I-target), 2e-12)
        for field,error in evaluate(p,z,s,0,reconstruction_factor=32).items():
            record(branch+'_initial_shared_output_'+field,error,2e-8)
        # An arbitrary smooth perturbation, not just an exact soliton, tests flux algebra.
        P,v = p.m.unpack(z)
        smooth = np.cos(2*np.pi*p.X.x/40)
        P = P+1e-4*np.arange(P.shape[0])[:,None]*smooth
        v = v+2e-4*np.arange(v.shape[0])[:,None]*smooth
        zz = p.m.pack(P,v)
        phys = p.m.rhs(0,zz)
        Rt = p.density_time_derivative(0,zz,phys)
        _,Q = p.density_flux(0,zz)
        record(branch+'_sd_discrete_flux_identity',norm(Rt+p.X.d1(Q)),2e-11)
        # Independent finite differentiation of the density along (t,z) at fixed x.
        eps = 1e-6
        rp = p.density_flux(eps,zz+eps*phys)[0]
        rm = p.density_flux(-eps,zz-eps*phys)[0]
        record(branch+'_density_time_chain_rule',norm((rp-rm)/(2*eps)-Rt),2e-8)
        # FD and SD start with exactly the same monitor and physical state.
        fd = BranchProblem(pars,route='fd',branch=branch)
        fz,fs = fd.initial()
        record(branch+'_matched_fd_sd_initial_state',max(norm(fz-z),norm(fs-s)),1e-14)
        record(branch+'_same_mesh_velocity_functional',norm(fd.rhs(0,fz,fs)[1]-p.rhs(0,z,s)[1]),1e-13)

    # Transport term independently checked against analytic x derivatives of P,v.
    errors=[]
    for n in (256,512,1024):
        p=BranchProblem(pars,branch='plus',nx=n)
        z,s=p.initial();dz,V=p.rhs(0,z,s)
        physical=p.m.rhs(0,z)
        # For this traveling exact profile, d_x = (p+q)/(q²-p²) d_t.
        zx=p.m.exact(0,True)*(pars.p+pars.q)/(pars.q**2-pars.p**2)
        ap,av=p.m.unpack(zx)
        exact_transport=p.m.pack(V*ap,V*av)
        errors.append(norm(dz-physical-exact_transport))
    record('ALE_transport_converges_order_four',abs(np.log2(errors[-2]/errors[-1])-4),.2)

    (HERE/'validation.json').write_text(json.dumps(dict(passed=True,checks=checks,
        mapped_d1_errors=e1,mapped_d2_errors=e2,ALE_transport_errors=errors),indent=2)+'\n',encoding='utf-8')
    print(f'{len(checks)} implementation checks passed')

if __name__=='__main__': main()
