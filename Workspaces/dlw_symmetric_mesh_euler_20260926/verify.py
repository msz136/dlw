"""New identities and independent checks specific to the symmetric density."""
from pathlib import Path
import json
import numpy as np
from sym_model import SymmetricProblem,BranchProblem,Parameters,evaluate

HERE=Path(__file__).resolve().parent
checks={}
def norm(x):return float(np.max(abs(x)))
def record(name,value,tol):
    checks[name]=dict(error=float(value),tolerance=tol,passed=bool(value<tol))
    assert value<tol,(name,value,tol)

def main():
    pars=Parameters(4,1,3,4)
    for route in ('fd','sd'):
        p=SymmetricProblem(pars,route=route);z,s=p.initial()
        R,Q=p.density_flux(0,z)
        record(route+'_direct_finite_h_density',norm(R-p.direct_density(0,z)),1e-13)
        I,rr=p.initial_potential_density(p.X.x)
        ends=p.initial_potential_density(np.array([-20.,20.]))[0]
        target=ends[0]+np.arange(p.X.n)/p.X.n*(ends[1]-ends[0])
        record(route+'_equal_mass_inverse',norm(I-target),2e-12)
        record(route+'_primitive_density',norm(rr-R),2e-13)
        for f,error in evaluate(p,z,s,0,reconstruction_factor=32).items():
            record(route+'_initial_common_output_'+f,error,2e-8)
        # Independently take derivatives of the analytic primitive in physical x.
        eps=2e-5
        di=(p.initial_potential_density(p.X.x+eps)[0]-p.initial_potential_density(p.X.x-eps)[0])/(2*eps)
        record(route+'_primitive_differentiation',norm(di-R),5e-9)
        # Arbitrary smooth perturbations test the law beyond the exact initial profile.
        P,v=p.m.unpack(z);mode=np.cos(2*np.pi*p.X.x/40)
        zz=p.m.pack(P+1e-4*np.arange(P.shape[0])[:,None]*mode,
                    v+2e-4*np.arange(v.shape[0])[:,None]*mode)
        record(route+'_perturbed_direct_density',norm(p.density_flux(0,zz)[0]-p.direct_density(0,zz)),2e-13)
        rhs=p.m.rhs(0,zz);rt=p.density_time_derivative(0,zz,rhs)
        rp=p.density_flux(1e-6,zz+1e-6*rhs)[0];rm=p.density_flux(-1e-6,zz-1e-6*rhs)[0]
        record(route+'_density_time_chain_rule',norm((rp-rm)/2e-6-rt),2e-8)
        if route=='sd':record('sd_symmetric_local_conservation',norm(rt+p.X.d1(p.density_flux(0,zz)[1])),2e-11)

    fd=SymmetricProblem(pars,route='fd');sd=SymmetricProblem(pars,route='sd')
    fz,fs=fd.initial();sz,ss=sd.initial()
    record('fd_sd_matched_initial_fields_and_mesh',max(norm(fz-sz),norm(fs-ss)),1e-14)
    record('fd_sd_same_velocity_rule',norm(fd.rhs(0,fz,fs)[1]-sd.rhs(0,sz,ss)[1]),1e-13)
    # The symmetric velocity must divide the mixed flux by the mixed density.
    R,Q=sd.density_flux(0,sz);V=sd.rhs(0,sz,ss)[1]
    record('velocity_is_ratio_of_mixes',norm(V-(Q-Q[0])/R),1e-14)

    # Inherited fixed/minus/plus routes reproduce frozen implementation bit for bit.
    for branch in ('fixed','minus','plus'):
        old=BranchProblem(pars,branch=branch,nx=128)
        new=SymmetricProblem(pars,branch=branch,nx=128)
        oz,os=old.initial();nz,ns=new.initial()
        of,ov=old.rhs(0,oz,os);nf,nv=new.rhs(0,nz,ns)
        record('inherited_'+branch+'_unchanged',max(norm(oz-nz),norm(os-ns),norm(of-nf),norm(ov-nv)),1e-14)
    (HERE/'validation.json').write_text(json.dumps(dict(passed=True,checks=checks),indent=2)+'\n',encoding='utf-8')
    print(f'{len(checks)} symmetric-density checks passed')

if __name__=='__main__':main()
