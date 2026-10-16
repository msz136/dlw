"""Actual tangent-map tests of DLW Hamilton time integrators on a fixed leaf.

Uses the exact Stage-1A spatial Hamilton vector field and nonlinear initial data.
No artificial experiment fields are generated. A harmonic oscillator is used
only as a separately labeled analytic calibration. No packages are installed.
"""
from __future__ import annotations
from pathlib import Path
import csv
import hashlib
import importlib.util
import json
import sys
import time

import numpy as np
import scipy
from scipy.linalg import block_diag, helmert
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/"dlw_three_tracks_20261013/conservation/conservation_experiment.py"
spec=importlib.util.spec_from_file_location("stage1_dlw",SOURCE)
BASE=importlib.util.module_from_spec(spec);spec.loader.exec_module(BASE)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,
    "axes.spines.top":False,"axes.spines.right":False,"axes.linewidth":.75,
    "pdf.fonttype":42,"ps.fonttype":42,"figure.facecolor":"white"})
COLORS={"Euler":"#ba552a","RK4":"#2466a0","Midpoint":"#37916f"}
CHECKS=[]


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check(name,value,tolerance):
    value=float(value);ok=np.isfinite(value) and value<=tolerance
    CHECKS.append({"name":name,"value":value,"tolerance":tolerance,"passed":bool(ok)})
    if not ok:raise AssertionError((name,value,tolerance))


def write_csv(name,rows):
    columns=list(dict.fromkeys(k for r in rows for k in r))
    with (HERE/name).open("w",newline="",encoding="utf-8-sig") as stream:
        writer=csv.DictWriter(stream,columns);writer.writeheader();writer.writerows(rows)


class Leaf:
    def __init__(self,n=15):
        if n%2!=1:raise ValueError("Use odd Nx to exclude the centered Nyquist kernel")
        self.grid=BASE.Grid(n,"centered");self.n=n;self.m=BASE.M
        self.weight=BASE.H*self.grid.dx
        self.qy=helmert(self.m,full=False).T;self.qx=helmert(n,full=False).T
        self.q=np.kron(self.qy,self.qx)
        self.embed=block_diag(self.q,self.q)
        self.dim=self.embed.shape[1];self.eye=np.eye(self.dim)
        initial=BASE.initial(self.grid)
        self.center=np.broadcast_to(initial.mean(axis=2,keepdims=True),initial.shape).copy()
        self.z0=self.embed.T@(initial-self.center).ravel()
        dsmall=self.q.T@np.kron(np.eye(self.m),self.grid.D)@self.q
        zero=np.zeros_like(dsmall)
        self.B=-np.block([[zero,dsmall],[dsmall,zero]])/self.weight
        self.Omega=-np.linalg.inv(self.B)
        self.normOmega=np.linalg.norm(self.Omega,"fro")
        self.de=self.embed.reshape(2,self.m,n,self.dim)
        E=BASE.EMINUS.T  # (E f)_j=f_(j+1), matching the Stage-1C convention.
        self.C0=(E-E.T)/(2*BASE.H)
        py=np.kron(BASE.P0,np.eye(n));cy=np.kron(self.C0,np.eye(n))
        # Fixed inverse differential of the nonlinear physical embedding.
        self.physical_inverse=self.embed.T@np.block([[py,np.zeros_like(py)],[-cy@py,py]])

    def full(self,z):return self.center+(self.embed@z).reshape(2,self.m,self.n)

    def f(self,z):return self.embed.T@BASE.rhs(self.full(z),self.grid).ravel()

    def f_jac(self,z):
        """Exact analytic derivative of the Stage-1A polynomial vector field."""
        full=self.full(z);p,s=full;U,w=BASE.fields(full)
        dp,ds=self.de
        dU=dp-np.mean(dp*s[:,:,None]+p[:,:,None]*ds,axis=0,keepdims=True)/BASE.C
        dsx=np.einsum("ab,jbd->jad",self.grid.D,ds)
        dUx=np.einsum("ab,jbd->jad",self.grid.D,dU)
        df=dU*w[:,:,None]+U[:,:,None]*ds-dsx
        dk=U[:,:,None]*dU+2*BASE.BETA*w[:,:,None]*ds+dUx+np.einsum("ab,bid->aid",BASE.R,dsx)
        df=np.einsum("ab,bid->aid",BASE.P0,df)
        dk=np.einsum("ab,bid->aid",BASE.P0,dk)
        dF=-np.stack((np.einsum("ab,jbd->jad",self.grid.D,dk),
                     np.einsum("ab,jbd->jad",self.grid.D,df)))
        return self.f(z),self.embed.T@dF.reshape(2*self.m*self.n,self.dim)

    def jac(self,z):return self.f_jac(z)[1]

    def defect(self,tangent):
        return float(np.linalg.norm(tangent.T@self.Omega@tangent-self.Omega,"fro")/self.normOmega)

    def hamilton(self,z):return BASE.hamilton(self.full(z),self.grid)

    def physical(self,z):
        full=self.full(z);U,w=BASE.fields(full)
        # a=0 fixes the irrelevant constant shift in physical u=U-2a.
        return np.stack((U,w+self.C0@full[0]+4)).ravel()

    def physical_jac(self,z):
        p,s=self.full(z);dp,ds=self.de
        dU=dp-np.mean(dp*s[:,:,None]+p[:,:,None]*ds,axis=0,keepdims=True)/BASE.C
        dV=ds+np.einsum("ab,bid->aid",self.C0,dp)
        return np.stack((dU,dV)).reshape(2*self.m*self.n,self.dim)


def euler(leaf,z,h):
    f,A=leaf.f_jac(z)
    return z+h*f,leaf.eye+h*A,{"iterations":0,"nonlinear_residual":0.,"linear_residual":0.}


def rk4(leaf,z,h):
    f1,A1=leaf.f_jac(z);J1=A1
    f2,A2=leaf.f_jac(z+h*f1/2);J2=A2@(leaf.eye+h*J1/2)
    f3,A3=leaf.f_jac(z+h*f2/2);J3=A3@(leaf.eye+h*J2/2)
    f4,A4=leaf.f_jac(z+h*f3);J4=A4@(leaf.eye+h*J3)
    return z+h*(f1+2*f2+2*f3+f4)/6,leaf.eye+h*(J1+2*J2+2*J3+J4)/6,{
        "iterations":0,"nonlinear_residual":0.,"linear_residual":0.}


def midpoint(leaf,z,h,tolerance=1e-14,max_iter=12,min_iterations=0):
    """Differentiate the actual finite Newton iteration, including dJacobian.

    The returned tangent is NOT simply the formal implicit Cayley formula.
    Differentiation is within the locally fixed iteration-count branch.
    """
    f0,A0=leaf.f_jac(z);y=z+h*f0;Y=leaf.eye+h*A0
    previous=np.inf;linear_residual=0.
    for iteration in range(max_iter+1):
        m=(z+y)/2;f,A=leaf.f_jac(m)
        residual=y-z-h*f;norm=float(np.linalg.norm(residual,np.inf))
        J=leaf.eye-h*A/2
        if norm<=tolerance and iteration>=min_iterations:
            ideal=np.linalg.solve(J,leaf.eye+h*A/2)
            return y,Y,{"iterations":iteration,"nonlinear_residual":norm,
                "previous_nonlinear_residual":float(previous),"linear_residual":linear_residual,
                "formal_implicit_defect":leaf.defect(ideal),
                "actual_minus_formal_tangent_rel":float(np.linalg.norm(Y-ideal)/np.linalg.norm(ideal)),
                "stopping_ratio":norm/tolerance}
        if iteration==max_iter:raise RuntimeError(("Midpoint failed",h,tolerance,norm))
        delta=np.linalg.solve(J,residual)
        # Hessian contraction H_delta = D A(m)[delta]; polynomial complex step.
        H_delta=np.imag(leaf.jac(m+1j*1e-30*delta))/1e-30
        dres=Y-leaf.eye-h*A@(leaf.eye+Y)/2
        ddelta_rhs=dres+h*H_delta@(leaf.eye+Y)/4
        ddelta=np.linalg.solve(J,ddelta_rhs)
        linear_residual=max(linear_residual,float(np.linalg.norm(J@delta-residual,np.inf)),
            float(np.linalg.norm(J@ddelta-ddelta_rhs,np.inf)))
        y=y-delta;Y=Y-ddelta;previous=norm


def midpoint_fixed_iterations(leaf,z,h,iterations):
    """State-only fixed-branch program for independent complex-step checking."""
    y=z+h*leaf.f(z)
    for _ in range(iterations):
        m=(z+y)/2;f,A=leaf.f_jac(m)
        y=y-np.linalg.solve(leaf.eye-h*A/2,y-z-h*f)
    return y


METHODS={"Euler":euler,"RK4":rk4,"Midpoint":midpoint}


def integrate(leaf,method,T,steps,tolerance=1e-14,min_iterations=0):
    z=leaf.z0.copy();tangent=leaf.eye.copy();h=T/steps
    max_res=0.;max_linear=0.;max_newton=0;min_newton=99;states=[z.copy()]
    rows=[{"method":method,"steps":steps,"dt":h,"t":0.,"symplectic_defect":0.}]
    for step in range(steps):
        if method=="Midpoint":new,J,info=midpoint(leaf,z,h,tolerance,min_iterations=min_iterations)
        else:new,J,info=METHODS[method](leaf,z,h)
        z=new;tangent=J@tangent;states.append(z.copy())
        max_res=max(max_res,info["nonlinear_residual"]);max_linear=max(max_linear,info["linear_residual"])
        max_newton=max(max_newton,info["iterations"]);min_newton=min(min_newton,info["iterations"])
        rows.append({"method":method,"steps":steps,"dt":h,"t":(step+1)*h,
            "symplectic_defect":leaf.defect(tangent)})
    full=leaf.full(z);casimir=np.max(np.abs(full.mean(axis=2)-leaf.center.mean(axis=2)))
    summary={"method":method,"Nx":leaf.n,"leaf_dimension":leaf.dim,"steps":steps,"dt":h,"T":T,
        "symplectic_defect":leaf.defect(tangent),"nonlinear_residual_max":max_res,
        "linear_residual_max":max_linear,"newton_iterations_max":max_newton,
        "newton_iterations_min":min_newton,"casimir_mean_drift":float(casimir),
        "energy_drift_context_only":float(leaf.hamilton(z)-leaf.hamilton(leaf.z0)),
        "field_change_linf":float(np.max(np.abs(full-leaf.full(leaf.z0))))}
    return z,tangent,summary,rows,np.array(states)


def reference_flow(leaf,T,rtol=3e-13,atol=3e-15):
    n=leaf.dim
    def augmented(t,b):
        f,A=leaf.f_jac(b[:n])
        return np.r_[f,(A@b[n:].reshape(n,n)).ravel()]
    sol=solve_ivp(augmented,(0.,T),np.r_[leaf.z0,leaf.eye.ravel()],method="DOP853",
                  rtol=rtol,atol=atol)
    if not sol.success:raise RuntimeError(sol.message)
    z=sol.y[:n,-1];tangent=sol.y[n:,-1].reshape(n,n)
    return z,tangent,{"method":"DOP853 state and variational reference","rtol":rtol,"atol":atol,
        "nfev":sol.nfev,"accepted_steps":len(sol.t)-1,"symplectic_defect":leaf.defect(tangent)}


def verify_leaf(leaf):
    Q=leaf.embed;z=leaf.z0;f,A=leaf.f_jac(z)
    check("leaf orthonormal embedding",np.linalg.norm(Q.T@Q-leaf.eye),2e-13)
    check("leaf initial reconstruction",np.max(np.abs(leaf.full(z)-BASE.initial(leaf.grid))),2e-14)
    check("leaf B skew",np.linalg.norm(leaf.B+leaf.B.T),2e-13)
    check("leaf inverse Omega",np.linalg.norm(leaf.Omega@leaf.B+leaf.eye),2e-13)
    check("leaf Omega skew",np.linalg.norm(leaf.Omega+leaf.Omega.T),2e-13)
    check("infinitesimal Hamilton identity",np.linalg.norm(A.T@leaf.Omega+leaf.Omega@A)/leaf.normOmega,2e-13)
    grad=leaf.weight*Q.T@np.stack(BASE.gradients(leaf.full(z),leaf.grid)).ravel()
    check("Poisson times Euclidean Hamilton gradient",np.linalg.norm(f-leaf.B@grad),2e-13)
    rng=np.random.default_rng(417)
    for j in range(3):
        v=rng.normal(size=leaf.dim);v/=np.linalg.norm(v)
        exact=np.imag(leaf.f(z+1j*1e-30*v))/1e-30
        check(f"analytic Jacobian complex step direction {j}",np.linalg.norm(A@v-exact),2e-13)
    Ephys=leaf.physical_jac(z);L=leaf.physical_inverse
    check("physical inverse differential",np.linalg.norm(L@Ephys-leaf.eye),3e-13)
    v=rng.normal(size=leaf.dim)
    check("physical differential complex step",np.linalg.norm(Ephys@v-np.imag(leaf.physical(z+1j*1e-30*v))/1e-30),3e-13)
    Ophys=L.T@leaf.Omega@L
    check("physical Omega pullback",np.linalg.norm(Ephys.T@Ophys@Ephys-leaf.Omega)/leaf.normOmega,3e-13)
    # Euler's exact single-step defect identity (no asymptotic approximation).
    h=.02;_,Je,_=euler(leaf,z,h)
    check("Euler exact h^2 defect identity",np.linalg.norm(Je.T@leaf.Omega@Je-leaf.Omega-h*h*A.T@leaf.Omega@A)/leaf.normOmega,3e-14)
    for tol in (1e-2,1e-4,1e-8,1e-14):
        out,J,info=midpoint(leaf,z,h,tol)
        for j in range(2):
            v=rng.normal(size=leaf.dim);v/=np.linalg.norm(v)
            direct=np.imag(midpoint_fixed_iterations(leaf,z+1j*1e-30*v,h,info["iterations"]))/1e-30
            check(f"actual Newton tangent tol={tol:g} direction {j}",np.linalg.norm(J@v-direct),3e-12)
    # Independent complex-step derivatives of explicit RK4, with all stages.
    _,J,_=rk4(leaf,z,h)
    v=rng.normal(size=leaf.dim);v/=np.linalg.norm(v)
    def state_rk4(z):
        a=leaf.f(z);b=leaf.f(z+h*a/2);c=leaf.f(z+h*b/2);d=leaf.f(z+h*c)
        return z+h*(a+2*b+2*c+d)/6
    check("RK4 tangent complex step",np.linalg.norm(J@v-np.imag(state_rk4(z+1j*1e-30*v))/1e-30),3e-12)
    return {"dimension":leaf.dim,"Nx":leaf.n,"M":leaf.m,"weight_h_dx":leaf.weight,
        "B_condition_number":float(np.linalg.cond(leaf.B)),"Omega_frobenius_norm":leaf.normOmega,
        "casimir_x_means":leaf.center.mean(axis=2).tolist()}


def harmonic_calibration():
    """R4(i h) modulus defect is exactly -h^6/72 + h^8/576."""
    A=np.array([[0.,1.],[-1.,0.]]);O=A.copy();I=np.eye(2)
    rows=[]
    for h in (.8,.4,.2,.1):
        R=I+h*A+h*h*(A@A)/2+h**3*np.linalg.matrix_power(A,3)/6+h**4*np.linalg.matrix_power(A,4)/24
        eulerJ=I+h*A;mid=np.linalg.solve(I-h*A/2,I+h*A/2)
        scalar=-h**6/72+h**8/576
        check(f"harmonic RK4 exact polynomial h={h}",np.linalg.norm(R.T@O@R-O-scalar*O),2e-15)
        check(f"harmonic Euler exact polynomial h={h}",np.linalg.norm(eulerJ.T@O@eulerJ-O-h*h*O),2e-15)
        check(f"harmonic midpoint Cayley h={h}",np.linalg.norm(mid.T@O@mid-O),2e-15)
        rows.append({"dt":h,"RK4_measured_relative_defect":float(np.linalg.norm(R.T@O@R-O)/np.linalg.norm(O)),
            "RK4_exact_relative_defect":abs(scalar),"Euler_exact_relative_defect":h*h,
            "Midpoint_measured_relative_defect":float(np.linalg.norm(mid.T@O@mid-O)/np.linalg.norm(O))})
    write_csv("harmonic_calibration.csv",rows)
    return rows


def observed_orders(rows,group_key="method",value_key="symplectic_defect",floor=1e-12):
    out=[]
    for group in dict.fromkeys(r[group_key] for r in rows):
        sub=sorted([r for r in rows if r[group_key]==group],key=lambda r:r["dt"],reverse=True)
        for a,b in zip(sub[:-1],sub[1:]):
            da,db=a[value_key],b[value_key]
            out.append({group_key:group,"dt_coarse":a["dt"],"dt_fine":b["dt"],
                "coarse_defect":da,"fine_defect":db,"above_fit_floor":da>floor and db>floor,
                "observed_order":float(np.log(da/db)/np.log(a["dt"]/b["dt"])) if da>floor and db>floor else None})
    return out


def physical_check(leaf,zfinal,tangent,method):
    L=leaf.physical_inverse;A0=leaf.physical_jac(leaf.z0);A1=leaf.physical_jac(zfinal)
    Ophys=L.T@leaf.Omega@L
    Dphys=A1@tangent@L
    actual=A0.T@(Dphys.T@Ophys@Dphys-Ophys)@A0
    reduced=tangent.T@leaf.Omega@tangent-leaf.Omega
    residual=np.linalg.norm(actual-reduced)/leaf.normOmega
    check(f"finite physical-map pullback {method}",residual,3e-13)
    return {"method":method,"reduced_defect":leaf.defect(tangent),
        "physical_restricted_defect":float(np.linalg.norm(actual)/leaf.normOmega),
        "matrix_equivalence_relative_residual":float(residual),
        "physical_coordinates":"u=U-2a with a=0; v=w+C0 p+4; restricted to the nonlinear fixed-Casimir leaf"}


def savefig(fig,name):
    fig.savefig(HERE/f"{name}.png",dpi=300);fig.savefig(HERE/f"{name}.pdf");plt.close(fig)


def plots(single,fixed,tolerance,times):
    fig,axes=plt.subplots(1,3,figsize=(11.6,3.8),layout="constrained")
    for method in METHODS:
        for ax,table,title in ((axes[0],single,"(a) One step from the same state"),
                               (axes[1],fixed,"(b) Fixed total time T = 0.02")):
            part=[r for r in table if r["method"]==method]
            ax.loglog([r["dt"] for r in part],[r["symplectic_defect"] for r in part],"o-",ms=3.5,lw=1.25,color=COLORS[method],label=method)
            ax.set_xlabel(r"Time step $\Delta t$");ax.set_title(title,loc="left")
            ax.axhspan(1e-17,1e-12,color=".94",zorder=0);ax.set_ylim(bottom=1e-17)
            ax.text(.03,.025,"Order fits omitted below 1e-12",transform=ax.transAxes,fontsize=7,color=".4")
        part=[r for r in times if r["method"]==method and r["steps"]==8 and r["t"]>0]
        axes[2].semilogy([r["t"] for r in part],[r["symplectic_defect"] for r in part],"o-",ms=3.5,lw=1.25,color=COLORS[method],label=method)
    axes[0].set_ylabel(r"$\|D\Phi^T\Omega D\Phi-\Omega\|_F / \|\Omega\|_F$")
    axes[2].set_xlabel("Time t");axes[2].set_title("(c) Accumulation; dt = 0.0025",loc="left")
    axes[2].xaxis.set_major_locator(MaxNLocator(4))
    for ax in axes:ax.grid(alpha=.18);ax.legend(frameon=False,fontsize=8)
    fig.suptitle("Actual tangent-map symplecticity | DLW centered Hamilton grid, M = 3, Nx = 15, leaf dimension = 56",fontsize=10)
    savefig(fig,"symplectic_defect")
    fig,axes=plt.subplots(1,3,figsize=(11.6,3.8),layout="constrained")
    t=[r["tolerance"] for r in tolerance]
    axes[0].loglog(t,[r["symplectic_defect"] for r in tolerance],"o-",color="#2466a0",label="Actual Newton program")
    axes[0].loglog(t,[r["formal_implicit_defect"] for r in tolerance],"s--",color="#37916f",label="Formal implicit formula")
    axes[0].set(ylabel="Relative symplectic defect",title="(a) Actual versus formal tangent")
    axes[0].legend(frameon=False,fontsize=7.5)
    axes[1].loglog(t,[r["nonlinear_residual"] for r in tolerance],"o-",color="#ba552a",label="Equation residual")
    axes[1].loglog(t,t,":",color=".5",label="Requested tolerance")
    axes[1].set(ylabel="Residual infinity norm",title="(b) Nonlinear equation solve")
    axes[1].legend(frameon=False,fontsize=7.5)
    axes[2].semilogx(t,[r["iterations"] for r in tolerance],"o-",color="#2466a0")
    axes[2].set(ylabel="Newton corrections",title="(c) Finite iteration branches")
    axes[2].set_yticks([0,1,2])
    for ax in axes:ax.set_xlabel("Absolute Newton tolerance");ax.grid(alpha=.18)
    fig.suptitle("Implicit midpoint, one DLW step dt = 0.02 | Euler predictor; differentiate the implemented iterations",fontsize=10)
    savefig(fig,"midpoint_solver_tolerance")


def main():
    start=time.perf_counter();leaf=Leaf(15);leaf_info=verify_leaf(leaf);calibration=harmonic_calibration()
    coarse_z,coarse_J,coarse_info=reference_flow(leaf,.02)
    reference_z,reference_J,reference_info=reference_flow(leaf,.02,rtol=3e-14,atol=3e-16)
    reference_info["coarser_solve"]=coarse_info
    reference_info["refinement_leaf_state_linf"]=float(np.max(np.abs(reference_z-coarse_z)))
    reference_info["refinement_physical_field_linf"]=float(np.max(np.abs(leaf.physical(reference_z)-leaf.physical(coarse_z))))
    reference_info["refinement_tangent_relative"]=float(np.linalg.norm(reference_J-coarse_J)/np.linalg.norm(reference_J))
    check("DOP853 physical-field reference refinement",reference_info["refinement_physical_field_linf"],2e-13)
    check("DOP853 tangent reference refinement",reference_info["refinement_tangent_relative"],2e-13)
    single=[];fixed=[];times=[];saved={};physical=[]
    for method in METHODS:
        print(f"Running {method}",flush=True)
        for h in [.02/2**k for k in range(7)]:
            z,J,info=METHODS[method](leaf,leaf.z0,h)
            single.append({"method":method,"dt":h,"symplectic_defect":leaf.defect(J),**info})
        for steps in (1,2,4,8,16,32,64):
            z,J,row,trajectory,states=integrate(leaf,method,.02,steps)
            row["reduced_leaf_state_error_vs_DOP853_linf"]=float(np.max(np.abs(z-reference_z)))
            pdiff=(leaf.physical(z)-leaf.physical(reference_z)).reshape(2,leaf.m,leaf.n)
            row["physical_u_error_vs_DOP853_linf"]=float(np.max(np.abs(pdiff[0])))
            row["physical_v_error_vs_DOP853_linf"]=float(np.max(np.abs(pdiff[1])))
            row["physical_field_error_vs_DOP853_linf"]=float(np.max(np.abs(pdiff)))
            row["tangent_error_vs_DOP853_relative"]=float(np.linalg.norm(J-reference_J)/np.linalg.norm(reference_J))
            fixed.append(row);times.extend(trajectory)
            if steps==8:
                physical.append(physical_check(leaf,z,J,method))
                saved[method+"_states"]=states;saved[method+"_final_tangent"]=J
        print(f"Completed {method}",flush=True)
    tolerance=[]
    for tol in (1e-2,1e-3,1e-4,1e-5,1e-6,1e-7,1e-8,1e-10,1e-12,1e-14):
        z,J,info=midpoint(leaf,leaf.z0,.02,tol)
        tolerance.append({"tolerance":tol,"dt":.02,"symplectic_defect":leaf.defect(J),**info})
    min_two=[]
    for steps in (1,2,4,8,16,32,64):
        _,_,row,_,_=integrate(leaf,"Midpoint",.02,steps,min_iterations=2)
        row["minimum_Newton_corrections_requested"]=2;min_two.append(row)
    grid_checks=[]
    for n in (9,25):
        other=Leaf(n)
        for method in METHODS:
            z,J,row,_,_=integrate(other,method,.02,8)
            grid_checks.append(row)
    single_order=observed_orders(single);fixed_order=observed_orders(fixed)
    write_csv("single_step.csv",single);write_csv("fixed_time.csv",fixed)
    write_csv("defect_timeseries.csv",times);write_csv("midpoint_tolerance.csv",tolerance)
    write_csv("grid_checks.csv",grid_checks);write_csv("single_step_orders.csv",single_order)
    write_csv("midpoint_min_two_iterations.csv",min_two)
    write_csv("fixed_time_orders.csv",fixed_order);write_csv("physical_pullback.csv",physical)
    np.savez_compressed(HERE/"tangent_maps.npz",Omega=leaf.Omega,B=leaf.B,embedding=leaf.embed,
        leaf_center=leaf.center,z0=leaf.z0,reference_z=reference_z,reference_tangent=reference_J,**saved)
    plots(single,fixed,tolerance,times)
    validation={"passed":all(c["passed"] for c in CHECKS),"checks":CHECKS,"leaf":leaf_info,
        "parameters":{"M":3,"h_y":4.,"c":2.,"gamma":4.,"a":0.,"Lx":2*np.pi,"Nx":15,
            "T":.02,"time_steps":[.02/2**k for k in range(7)],"midpoint_default_absolute_tolerance":1e-14,
            "initial_data":"exact Stage-1A nonlinear Fourier witness, no new random initial state",
            "Omega_convention":"Omega=-B_leaf^{-1}; i_X omega = dH; matches the Stage-2A convention"},
        "sources":{"stage1_code":str(SOURCE),"stage1_sha256":sha(SOURCE),"script_sha256":sha(__file__)},
        "versions":{"python":sys.version,"numpy":np.__version__,"scipy":scipy.__version__,"matplotlib":matplotlib.__version__},
        "reference":reference_info,"harmonic_calibration":calibration,"single_step_orders":single_order,
        "midpoint_min_two_control":min_two,
        "fixed_time_orders":fixed_order,"physical_pullback":physical,"elapsed_seconds":time.perf_counter()-start,
        "interpretation":"No spatial convergence, full discrete integrability or long-time error claim. Energy drift is context only; the tested observable is the full tangent-map two-form defect."}
    def clean(o):
        if isinstance(o,dict):return {k:clean(v) for k,v in o.items()}
        if isinstance(o,list):return [clean(v) for v in o]
        if isinstance(o,float) and not np.isfinite(o):return None
        return o
    (HERE/"validation.json").write_text(json.dumps(clean(validation),indent=2,ensure_ascii=False,allow_nan=False),encoding="utf-8")
    print(json.dumps({"passed":validation["passed"],"seconds":validation["elapsed_seconds"],
        "fixed_time":fixed,"tolerance":tolerance},indent=2,ensure_ascii=False),flush=True)


if __name__=="__main__":main()
