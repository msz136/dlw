"""Read saved trajectories, verify algebra and independent integrations, summarize."""
from __future__ import annotations

import csv
import json

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

from run_parameter_calibration import (HERE, OUT, ROUTES, MOVING, PS, METHODS, DT,
    TIMES, Soliton, MovingSystem, original_advance, initialize, measure, source_hashes,
    case_key, specs, dump)


def main():
    data=json.loads((OUT/"results.json").read_text(encoding="utf-8"))
    assert data["source_hashes"]==source_hashes()
    assert set(data["rows"])==set(specs())
    rows=data["rows"]
    failures=[key for key,row in rows.items() if row["status"]!="completed"]
    if failures:
        raise RuntimeError(f"Failed trajectories retained: {failures}")
    def get(p,route,n=200,method="rk4",dt=DT,L=4.):
        return rows[case_key(dict(p=p,route=route,n=n,method=method,dt=dt,halfwidth=L))]
    def profile(row,t=.5):
        with np.load(OUT/row["profile"]) as archive:
            return tuple(archive[f"t{t}_{name}"].copy() for name in ("x","u","rho_x","rho"))

    a,c,r=sp.symbols("a c r",positive=True)
    C=a+sp.sqrt(c*c+a*a)
    defect=lambda cc: ((a/r+(cc-a)*r)**2-cc*cc-c*c*(r*r-1))/2
    assert sp.simplify(defect(c)-a*c*(1-r*r)-a*a*(1/r-r)**2/2)==0
    assert sp.simplify(defect(C)-a*a*(1/r-r)**2/2)==0

    rng=np.random.default_rng(20260926)
    residuals=[]
    for step in (.04,.02,.01):
        rr=rng.uniform(.25,1.5,31); w=rng.normal(0,.3,31)
        d=step/rr; v=d*w
        for corrected in (False,True):
            cc=step+np.hypot(1.,step) if corrected else 1.
            sd=MovingSystem(step,cc,len(d),lambda t:.012,"sd")
            fd=MovingSystem(step,1.,len(d),lambda t:.012,"fd")
            z=sd.pack(v,d,-4.)
            numerical=(sd.rhs(0,z)[:len(d)]-fd.rhs(0,z)[:len(d)])/d
            expected=.5*step**2*(1/rr-rr)**2
            if not corrected:
                expected+=step*(1-rr*rr)
            residuals.append(float(max(abs(numerical-expected))))
    assert max(residuals)<1e-12

    max_readback=0.; eval_changes=[]
    output_csv=[]
    for row in rows.values():
        spec=row["spec"]
        sol,_,_,a,cc=initialize(spec["p"],spec["route"],spec["n"],spec["halfwidth"])
        assert row["c_phys"]==1 and row["a"]==a and row["C"]==cc
        assert row["min_h"]>0 and row["min_rho"]>0
        if spec["route"]=="difference_rm":
            assert row["min_Rm"]>0
        for time in TIMES:
            saved=profile(row,time)
            assert np.all(np.diff(saved[0])>0) and np.min(saved[3])>0
            measured=measure(sol,saved,time)
            dense=measure(sol,saved,time,16001)
            for field in ("u","rho"):
                err=row["snapshots"][str(time)]["errors"][field]
                max_readback=max(max_readback,abs(measured[field]-err))
                assert np.isclose(measured[field],err,rtol=1e-12,atol=1e-15)
                assert np.isclose(dense[field],row["snapshots"][str(time)]["eval_16001"][field],
                                  rtol=1e-12,atol=1e-15)
                eval_changes.append(abs(dense[field]-err)/err)
            output_csv.append({**{k:v for k,v in spec.items() if k!="purposes"},"time":time,
                               "a":a,"C":cc,**measured})
    with (OUT/"all_errors.csv").open("w",newline="",encoding="utf-8-sig") as f:
        writer=csv.DictWriter(f,fieldnames=list(output_csv[0]))
        writer.writeheader();writer.writerows(output_csv)

    initial_checks=[]
    convergence=[]; improvements=[]; time_checks=[]; domain_checks=[]; temporal=[]
    for p in PS:
        for n in (200,400,800):
            initial_hashes=[get(p,route,n)["initial_state_sha256"] for route in MOVING]
            assert len(set(initial_hashes))==1
            initial_checks.append(dict(p=p,n=n,identical=True))
        for route in ROUTES:
            for time in TIMES:
                for field in ("u","rho"):
                    es=[get(p,route,n)["snapshots"][str(time)]["errors"][field]
                        for n in (200,400,800)]
                    orders=np.log2(np.array(es[:-1])/es[1:]).tolist()
                    convergence.append(dict(p=p,route=route,time=time,field=field,
                                            errors=es,orders=orders))
                    baseline=get(p,route,800)["snapshots"][str(time)]["errors"][field]
                    half=get(p,route,800,dt=DT/2)["snapshots"][str(time)]["errors"][field]
                    time_checks.append(dict(p=p,route=route,time=time,field=field,
                                            relative_change=abs(half-baseline)/baseline))
                    base=get(p,route,400)["snapshots"][str(time)]["errors"][field]
                    wide=get(p,route,500,L=5.)["snapshots"][str(time)]["errors"][field]
                    domain_checks.append(dict(p=p,route=route,time=time,field=field,
                                               base=base,wide=wide,relative_change=abs(wide-base)/base))
            fine=profile(get(p,route,method="rk8",dt=.00078125))
            grid=np.linspace(-2,2,8001)
            target=(np.interp(grid,fine[0],fine[1]),np.interp(grid,fine[2],fine[3]))
            for method in METHODS:
                errors=[]
                for dt in (.0125,.00625,DT):
                    candidate=profile(get(p,route,method=method,dt=dt))
                    errs=[float(max(abs(np.interp(grid,candidate[2*i],candidate[2*i+1])-target[i])))
                          for i in range(2)]
                    errors.append(errs)
                temporal.append(dict(p=p,route=route,method=method,errors=errors,
                                      fields=["u","rho"],dts=[.0125,.00625,DT]))
        for n in (200,400,800):
            for time in TIMES:
                for field in ("u","rho"):
                    er=lambda route: get(p,route,n)["snapshots"][str(time)]["errors"][field]
                    improvements.append(dict(p=p,n=n,time=time,field=field,
                        original_over_calibrated=er("integrable_original")/er("integrable_calibrated"),
                        calibrated_over_matched=er("integrable_calibrated")/er("difference_matched"),
                        calibrated_over_rm=er("integrable_calibrated")/er("difference_rm")))

    local_checks=[]
    for n,dt,L in ((200,DT,4.),(400,DT,4.),(800,DT,4.),(800,DT/2,4.),(500,DT,5.)):
        calibrated=get(12.,"integrable_calibrated",n,dt=dt,L=L)
        matched=get(12.,"difference_matched",n,dt=dt,L=L)
        for evaluation in ("errors","eval_16001"):
            ec=calibrated["snapshots"]["0.25"][evaluation]
            ed=matched["snapshots"]["0.25"][evaluation]
            ratios={field:ec[field]/ed[field] for field in ("u","rho")}
            assert ratios["u"]<.8 and ratios["rho"]>1
            local_checks.append(dict(n=n,dt=dt,halfwidth=L,evaluation=evaluation,ratios=ratios))

    # Independently form dw using the expanded identity and integrate with adaptive DOP853.
    independent=[]
    for p in PS:
        for route in MOVING:
            sol,system,z0,a,cc=initialize(p,route,200)
            m=200
            def rhs(t,z):
                v=z[:m]; d=z[m:2*m]; w=v/d; rr=a/d
                u=np.r_[system.left_u(t),system.left_u(t)+np.cumsum(v)]
                extra=np.zeros(m)
                if route!="difference_matched":
                    extra=.5*a*a*(1/rr-rr)**2
                    if route=="integrable_original":
                        extra+=a*(1-rr*rr)
                dw=.5*w*w+2*(u[1:]+u[:-1])+.5*(rr*rr-1)+extra
                return np.r_[d*dw-w*v,-v,-system.left_u(t)]
            solution=solve_ivp(rhs,(0.,.5),z0,method="DOP853",rtol=2e-12,atol=2e-14,max_step=.005)
            assert solution.success
            f=system.fields(.5,solution.y[:,-1])
            x,u,rx,rho=profile(get(p,route))
            diffs={"x":float(max(abs(f["x"]-x))),"u":float(max(abs(f["u"]-u))),
                   "rho":float(max(abs(f["rho"]-rho)))}
            assert max(diffs.values())<2e-8
            independent.append(dict(p=p,route=route,max_differences=diffs))

    # Separate exact-lattice test: this reference changes c and is NOT a PDE-error reference.
    lattice_checks=[]
    for p in PS:
        a=.04; C=a+np.hypot(1.,a); k=np.arange(-100,101)
        sol=Soliton((p,),c=C,shift=-(1-2/p)/2)
        left=lambda t: float(sol.lattice(np.array([k[0]]),a,t)[0][0])
        system=MovingSystem(a,C,200,left,"sd")
        z=system.exact_initial(sol,k[0],0.)
        for j in range(160):
            z,_,_=original_advance(system,j*DT,z,DT,"rk4")
        num=system.fields(.5,z); exact=sol.lattice_state(k,a,.5)
        delta={field:float(max(abs(num[field]-exact[field]))) for field in ("x","u","rho")}
        assert max(delta.values())<2e-8
        lattice_checks.append(dict(p=p,a=a,C=C,max_differences=delta))

    # Verify old frozen records' sources were not changed by adding this experiment.
    old_hash_checks={}
    for name in ("statistical_validation/frozen_manifest.json","time_methods/cohort_manifest.json"):
        manifest=json.loads((HERE/"out"/name).read_text(encoding="utf-8"))
        hashes=manifest.get("solver_hashes",manifest.get("solver_sha256",{}))
        checks=[]
        import hashlib
        for filename,digest in hashes.items():
            path=HERE/filename
            if not path.exists():path=HERE.parent/"hs_numerics_plan"/filename
            checks.append(hashlib.sha256(path.read_bytes()).hexdigest()==digest)
        assert checks and all(checks)
        old_hash_checks[name]=True

    audit={"status":"passed","trajectories":len(rows),"pilot_trajectories":18,
           "independent_integrations":len(independent),"exact_lattice_integrations":len(lattice_checks),
           "symbolic_identities":True,"numeric_rhs_identity_max_residual":max(residuals),
           "profile_readback_max_difference":max_readback,
           "evaluation_double_max_relative_change":max(eval_changes),
           "time_half_max_relative_change":max(v["relative_change"] for v in time_checks),
           "domain_max_relative_change":max(v["relative_change"] for v in domain_checks),
           "initial_states":initial_checks,"independent_checks":independent,
           "exact_lattice_checks":lattice_checks,"old_frozen_sources_match":old_hash_checks,
           "source_hashes":data["source_hashes"],"local_p12_t025_checks":local_checks}
    dump(OUT/"validation.json",audit)
    dump(OUT/"summary.json",dict(convergence=convergence,improvements=improvements,
         time_checks=time_checks,domain_checks=domain_checks,temporal=temporal))
    print(json.dumps({k:v for k,v in audit.items() if not isinstance(v,(list,dict))},indent=2))


if __name__=="__main__":
    main()
