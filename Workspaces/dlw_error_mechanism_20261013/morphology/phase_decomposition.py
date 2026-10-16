"""Frozen-protocol phase-only decomposition of stored physical DLW errors."""
from __future__ import annotations
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS","1")
os.environ.setdefault("OMP_NUM_THREADS","1")
from pathlib import Path
import csv,hashlib,importlib.util,json,sys,time
import numpy as np
import scipy
from scipy.special import logsumexp
from scipy.optimize import least_squares
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
STAGE1=HERE.parents[1]/"dlw_three_tracks_20261013"
SHARED=STAGE1/"shared"
assert (SHARED/"solver_cells.json").is_file(),"Frozen reference must already exist"
spec=importlib.util.spec_from_file_location("shared_generator",STAGE1/"generate_shared.py")
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
NS,BUNDLE=source.load_solver()
PROTOCOL_SHA=hashlib.sha256((HERE/"PROTOCOL.md").read_bytes()).hexdigest()
assert PROTOCOL_SHA=="0105d1aff5d9bbfa67449493f11803ecde71d8bdb4ca1314b4ad3e587c80228a"
CHECKS=[]

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as stream:
        for block in iter(lambda:stream.read(1024*1024),b""):h.update(block)
    return h.hexdigest()

def check(name,value,tolerance):
    v=float(value);ok=np.isfinite(v) and v<=tolerance
    CHECKS.append({"name":name,"value":v,"tolerance":tolerance,"passed":bool(ok)})
    if not ok:raise AssertionError((name,v,tolerance))

def csvwrite(name,rows):
    keys=list(dict.fromkeys(k for row in rows for k in row))
    with (HERE/name).open("w",newline="",encoding="utf-8-sig") as out:
        writer=csv.DictWriter(out,keys);writer.writeheader();writer.writerows(rows)

class PhaseExact(NS["Exact"]):
    """Change only additive subset phases, identically in f and g."""
    def __init__(self,case,h,a=2.):
        super().__init__(case,h,a)
        self.subsets=np.array([[0.],[1.]]) if len(self.coeff)==2 else np.array([[0.,0.],[1.,0.],[0.,1.],[1.,1.]])
        self.phase=np.zeros(self.subsets.shape[1])
    def set_phase(self,theta):
        self.phase=np.array(theta);self._key=None;self._cache={}
    def tau(self,js,x,t,is_f=False):
        y=(np.atleast_1d(js)+.5)*self.h
        logs=(np.log(self.coeff)[:,None,None]
            +self.rates[:,0,None,None]*np.atleast_1d(x)[None,None,:]
            +self.rates[:,1,None,None]*t+self.rates[:,2,None,None]*y[None,:,None]
            +(self.subsets@self.phase)[:,None,None])
        if is_f:logs=logs+self.gamma[:,None,None]
        total=logsumexp(logs,axis=0)
        return total,np.exp(logs-total[None,:,:])

class FrameReference:
    def __init__(self,case,x,y,t,h,a=2.):
        self.ref=PhaseExact(case,h,a);self.x=x;self.y=y;self.t=t
        self.js=np.rint(y/h-.5).astype(int)
        self.dim=self.ref.subsets.shape[1];self.n=len(x)*len(y)
        actual_y=(self.js+.5)*h
        check(f"{case} native y reconstruction",np.max(abs(actual_y-y)),5e-12)
        self.logs=(np.log(self.ref.coeff)[:,None,None]
            +self.ref.rates[:,0,None,None]*x[None,None,:]
            +self.ref.rates[:,1,None,None]*t
            +self.ref.rates[:,2,None,None]*actual_y[None,:,None])
        self._theta=None;self._value=None;self._derivative=None
    def evaluate(self,theta):
        if self._theta is not None and np.array_equal(theta,self._theta):
            return self._value,self._derivative
        s=self.ref.rates[:,0];ell=self.ref.rates[:,2];S=self.ref.subsets
        fields=[];derivs=[]
        phase=(S@theta)[:,None,None]
        for isf in (True,False):
            logs=self.logs+phase+(self.ref.gamma[:,None,None] if isf else 0)
            w=np.exp(logs-logsumexp(logs,axis=0)[None,:,:])
            mx=np.einsum("s,sij->ij",s,w);my=np.einsum("s,sij->ij",ell,w)
            mxy=np.einsum("s,sij->ij",s*ell,w)
            ms=np.einsum("sl,sij->lij",S,w)
            mxs=np.einsum("sl,sij->lij",S*s[:,None],w)
            mys=np.einsum("sl,sij->lij",S*ell[:,None],w)
            mxys=np.einsum("sl,sij->lij",S*(s*ell)[:,None],w)
            cx=mxs-mx[None,:,:]*ms;cy=mys-my[None,:,:]*ms
            dcov=mxys-mxy[None,:,:]*ms-my[None,:,:]*cx-mx[None,:,:]*cy
            fields.append((mx,mxy-mx*my));derivs.append((cx,dcov))
        value=np.stack((2*(fields[0][0]-fields[1][0]),2*(fields[0][1]+fields[1][1])))
        derivative=np.stack((2*(derivs[0][0]-derivs[1][0]),2*(derivs[0][1]+derivs[1][1])),axis=1)
        self._theta=np.array(theta);self._value=value;self._derivative=derivative
        return value,derivative
    def independent(self,theta):
        self.ref.set_phase(theta)
        return np.array(self.ref.uv(self.js,self.x,self.t))

def fit_frame(ref,target,archived_exact,common,validate_tangent=False):
    zero,derivative=ref.evaluate(np.zeros(ref.dim))
    check(f"{common['dataset']} {common['window']} t={ref.t:g} reference match",
          np.max(abs(zero-archived_exact)),3e-13)
    e=target-zero;total=float(np.mean(e[0]**2)+np.mean(e[1]**2))
    T=derivative.reshape(ref.dim,-1).T/np.sqrt(ref.n)
    ew=e.ravel()/np.sqrt(ref.n)
    gram=T.T@T;values=np.linalg.eigvalsh(gram)
    check("phase tangent full rank",float(values[-1]*1e-12/values[0]),1.)
    theta_linear=np.linalg.solve(gram,T.T@ew)
    parallel=(T@theta_linear).reshape(e.shape)*np.sqrt(ref.n)
    perpendicular=e-parallel
    Ephase=float(np.sum((T@theta_linear)**2))
    Eperp=float(np.sum((ew-T@theta_linear)**2))
    pyth=abs(total-Ephase-Eperp)/max(total,1e-300)
    orth=float(np.linalg.norm(T.T@(ew-T@theta_linear))/max(np.linalg.norm(T)*np.linalg.norm(ew),1e-300))
    check("Pythagoras budget",pyth,3e-13);check("phase orthogonality",orth,3e-13)
    if validate_tangent:
        for j in range(ref.dim):
            step=np.zeros(ref.dim);step[j]=1e-5
            fd=(ref.independent(step)-ref.independent(-step))/(2e-5)
            rel=np.linalg.norm(fd-derivative[j])/np.linalg.norm(derivative[j])
            check(f"{common['dataset']} {common['window']} tangent column {j}",rel,2e-7)
    floor=100*np.finfo(float).eps*max(1.,float(np.max(abs(zero))))
    signal=np.sqrt(total)>floor
    fit_records=[]
    if signal:
        def fun(theta):return (ref.evaluate(theta)[0]-target).ravel()/np.sqrt(ref.n)
        def jac(theta):return ref.evaluate(theta)[1].reshape(ref.dim,-1).T/np.sqrt(ref.n)
        for name,start in (("zero",np.zeros(ref.dim)),("linear",np.clip(theta_linear,-.249999,.249999))):
            opt=least_squares(fun,start,jac=jac,bounds=(-.25,.25),ftol=1e-12,xtol=1e-12,gtol=1e-14,max_nfev=40)
            fit_records.append({"start":name,"theta":opt.x,"energy":float(np.dot(opt.fun,opt.fun)),
                "success":bool(opt.success),"status":int(opt.status),"nfev":int(opt.nfev),
                "optimality":float(opt.optimality),"active_bound":bool(np.any(opt.active_mask)),
                "normalized_gradient":float(np.linalg.norm(opt.jac.T@opt.fun,np.inf)/max(np.linalg.norm(opt.jac)*np.linalg.norm(opt.fun),1e-300))})
        best=min(fit_records,key=lambda z:z["energy"]);theta=best["theta"]
        check("nonlinear objective not worse than zero",max(0.,best["energy"]/total-1),1e-9)
        if best["active_bound"] or not best["success"]:raise RuntimeError(("fit failed or hit bound",common,best))
        fit_field,_=ref.evaluate(theta);aligned=target-fit_field
        Efit=float(np.mean(aligned[0]**2)+np.mean(aligned[1]**2))
        fit_agree=abs(fit_records[0]["energy"]-fit_records[1]["energy"])/total
    else:
        theta=np.zeros(ref.dim);aligned=e.copy();Efit=total;fit_agree=0.
        best={"nfev":0,"success":True,"status":0,"optimality":None,"active_bound":False,"normalized_gradient":None}
    if validate_tangent:
        independent=ref.independent(theta)
        independent_energy=float(np.mean((target[0]-independent[0])**2)+np.mean((target[1]-independent[1])**2))
        check("independent inherited Exact objective",abs(independent_energy-Efit)/max(total,1e-30),2e-8)
    row={**common,"t":float(ref.t),"nodes":ref.n,"phase_dimension":ref.dim,"joint_rms_raw":np.sqrt(total),
        "joint_rms_aligned":np.sqrt(Efit),"total_squared_error":total,"linear_phase_squared_error":Ephase,
        "linear_nonphase_squared_error":Eperp,"nonlinear_residual_squared_error":Efit,
        "linear_phase_fraction":Ephase/total if signal else None,
        "nonlinear_explained_fraction":1-Efit/total if signal else None,
        "joint_rms_reduction_fraction":1-np.sqrt(Efit/total) if signal else None,
        "nonlinear_minus_linear_explained_fraction":1-Efit/total-Ephase/total if signal else None,
        "phase_tangent_condition":float(np.sqrt(values[-1]/values[0])),
        "phase_tangent_min_singular":float(np.sqrt(values[0])),"phase_tangent_max_singular":float(np.sqrt(values[-1])),
        "pythagoras_relative_residual":pyth,"orthogonality_relative_residual":orth,
        "signal_above_roundoff":bool(signal),"roundoff_floor":floor,"two_start_objective_difference_over_raw":fit_agree,
        "fit_nfev_best":best["nfev"],"fit_success":best["success"],"fit_status":best["status"],
        "fit_optimality":best["optimality"],"fit_normalized_gradient":best["normalized_gradient"],
        "fit_active_bound":best["active_bound"]}
    for j in range(ref.dim):
        row[f"theta{j+1}_linear"]=float(theta_linear[j]);row[f"theta{j+1}_fit"]=float(theta[j])
    for j,f in enumerate(("u","v")):
        row[f"{f}_rms_raw"]=float(np.sqrt(np.mean(e[j]**2)))
        row[f"{f}_rms_aligned_common_fit"]=float(np.sqrt(np.mean(aligned[j]**2)))
        row[f"{f}_rms_linear_phase"]=float(np.sqrt(np.mean(parallel[j]**2)))
        row[f"{f}_rms_linear_nonphase"]=float(np.sqrt(np.mean(perpendicular[j]**2)))
    if ref.dim==1:
        row["equivalent_x_feature_shift"]=-float(theta[0]/ref.ref.rates[1,0])
        row["equivalent_y_feature_shift"]=None
    else:
        rates=ref.ref.rates[1:3][:,[0,2]]
        translation=-np.linalg.solve(rates,theta)
        row["equivalent_x_feature_shift"]=float(translation[0])
        row["equivalent_y_feature_shift"]=float(translation[1])
    arrays={"error_raw":e,"error_linear_phase":parallel,"error_linear_nonphase":perpendicular,
        "error_nonlinear_aligned":aligned,"theta_linear":theta_linear,"theta_fit":theta,
        "phase_tangents":derivative,"gram_matrix":gram}
    return row,arrays,fit_records

def analyze_dataset(label,final_only=False):
    path=SHARED/f"{label}.npz";case=label[0]
    with np.load(path,allow_pickle=False) as npz:
        x=npz["x"];y=npz["y"];times=npz["t"];meta=json.loads(str(npz["metadata_json"]))
        u=npz["u"];v=npz["v"];eu=npz["exact_u"];ev=npz["exact_v"]
    rows=[];starts=[];half={"A":5.,"C":30.}[case]
    for window,fraction in (("full",1.),("central",.5)):
        ix=np.flatnonzero(abs(x)<=half*fraction+1e-10);iy=np.flatnonzero(abs(y)<half*fraction)
        selected=[len(times)-1] if final_only else range(len(times))
        for it in selected:
            t=times[it];reference=FrameReference(case,x[ix],y[iy],t,meta["config"]["h"],meta["config"]["a"])
            target=np.stack((u[it][np.ix_(iy,ix)],v[it][np.ix_(iy,ix)]))
            exact=np.stack((eu[it][np.ix_(iy,ix)],ev[it][np.ix_(iy,ix)]))
            common={"dataset":label,"case":case,"method":meta["model"],"window":window,"frame":it,
                "time_step":meta["config"]["dt"]}
            row,arrays,fit_records=fit_frame(reference,target,exact,common,it==len(times)-1)
            rows.append(row)
            for fit in fit_records:
                record={**common,"t":float(t),**{k:value for k,value in fit.items() if k!="theta"}}
                for j,q in enumerate(fit["theta"]):record[f"theta{j+1}"]=float(q)
                starts.append(record)
            if it==len(times)-1:
                np.savez_compressed(HERE/f"{label}_{window}_final_decomposition.npz",x=x[ix],y=y[iy],t=t,**arrays)
            if it%5==0 or it==len(times)-1:
                print(json.dumps({"dataset":label,"window":window,"frame":it,"fit_fraction":row["nonlinear_explained_fraction"]}),flush=True)
    return rows,starts,{"path":str(path),"sha256":sha(path),"frames_used":1 if final_only else len(times),
        "metadata":meta}

def plots(rows):
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"axes.spines.top":False,"axes.spines.right":False,
                         "pdf.fonttype":42,"ps.fonttype":42})
    fig,axes=plt.subplots(2,3,figsize=(11.8,6.8),layout="constrained")
    for r,case in enumerate(("A","C")):
        for method,color in (("SD","#2466a0"),("FD","#ba552a")):
            for window,style in (("full","-"),("central","--")):
                part=[q for q in rows if q["case"]==case and q["method"]==method and q["window"]==window and
                      q["signal_above_roundoff"] and "halfdt" not in q["dataset"]]
                t=[q["t"] for q in part];label=f"{method}, {window}"
                axes[r,0].plot(t,[100*q["nonlinear_explained_fraction"] for q in part],style,color=color,label=label)
                axes[r,1].semilogy(t,[q["joint_rms_raw"] for q in part],style,color=color,alpha=.35,lw=1)
                axes[r,1].semilogy(t,[q["joint_rms_aligned"] for q in part],style,color=color,lw=1.6,label=label)
                axes[r,2].plot(t,[q["phase_tangent_condition"] for q in part],style,color=color,label=label)
        for c,title in enumerate(("Phase-only explained squared error","Joint physical RMS: raw / aligned","Joint phase tangent condition")):
            axes[r,c].set_title(f"Case {case}: {title}",loc="left",fontsize=9)
            axes[r,c].set_xlabel("Time t");axes[r,c].grid(alpha=.15)
        axes[r,0].set_ylabel("Explained error energy [%]");axes[r,0].set_ylim(bottom=0)
        axes[r,1].set_ylabel(r"$\sqrt{\mathrm{RMS}_u^2+\mathrm{RMS}_v^2}$")
        axes[r,2].set_ylabel("Condition number")
        axes[r,0].legend(frameon=False,fontsize=7,ncol=2)
    fig.suptitle("Frozen joint phase fit | equal physical u/v weights | faint RMS curves: raw; dark curves: aligned",fontsize=10)
    fig.savefig(HERE/"phase_only_budget.png",dpi=300);fig.savefig(HERE/"phase_only_budget.pdf");plt.close(fig)

def main():
    start=time.perf_counter();allrows=[];starts=[];inputs=[]
    for case in ("A","C"):
        for method in ("SD","FD"):
            rows,s,meta=analyze_dataset(f"{case}_{method}_RK4")
            allrows.extend(rows);starts.extend(s);inputs.append(meta)
            csvwrite("fit_timeseries.csv",allrows);csvwrite("fit_start_diagnostics.csv",starts)
        rows,s,meta=analyze_dataset(f"{case}_SD_RK4_halfdt",final_only=True)
        allrows.extend(rows);starts.extend(s);inputs.append(meta)
    csvwrite("fit_timeseries.csv",allrows);csvwrite("fit_start_diagnostics.csv",starts)
    endpoints=[r for r in allrows if r["frame"]==20];csvwrite("endpoint_summary.csv",endpoints)
    comparisons=[]
    for case in ("A","C"):
        for window in ("full","central"):
            sd=next(r for r in endpoints if r["dataset"]==f"{case}_SD_RK4" and r["window"]==window)
            fd=next(r for r in endpoints if r["dataset"]==f"{case}_FD_RK4" and r["window"]==window)
            half=next(r for r in endpoints if r["dataset"]==f"{case}_SD_RK4_halfdt" and r["window"]==window)
            comparisons.append({"case":case,"window":window,"raw_SD_over_FD_joint_RMS":sd["joint_rms_raw"]/fd["joint_rms_raw"],
                "aligned_SD_over_FD_joint_RMS":sd["joint_rms_aligned"]/fd["joint_rms_aligned"],
                "SD_phase_explained_fraction":sd["nonlinear_explained_fraction"],"FD_phase_explained_fraction":fd["nonlinear_explained_fraction"],
                "halfdt_change_SD_explained_fraction":half["nonlinear_explained_fraction"]-sd["nonlinear_explained_fraction"],
                "halfdt_relative_aligned_RMS_change":half["joint_rms_aligned"]/sd["joint_rms_aligned"]-1})
    csvwrite("method_comparison.csv",comparisons);plots(allrows)
    validation={"passed":all(q["passed"] for q in CHECKS),"protocol_sha256":PROTOCOL_SHA,"script_sha256":sha(__file__),
        "frozen_solver_sha256":sha(SHARED/"solver_cells.json"),"inputs":inputs,"checks":CHECKS,
        "versions":{"python":sys.version,"numpy":np.__version__,"scipy":scipy.__version__,"matplotlib":matplotlib.__version__},
        "rows":len(allrows),"fits_at_roundoff_skipped":sum(not r["signal_above_roundoff"] for r in allrows),
        "all_fit_success":all(r["fit_success"] for r in allrows),"any_bound_contact":any(r["fit_active_bound"] for r in allrows),
        "max_tangent_condition":max(r["phase_tangent_condition"] for r in allrows),
        "max_pythagoras_residual":max(r["pythagoras_relative_residual"] for r in allrows),
        "max_two_start_objective_difference_over_raw":max(r["two_start_objective_difference_over_raw"] for r in allrows),
        "max_nonlinear_minus_linear_fraction":max(abs(r["nonlinear_minus_linear_explained_fraction"]) for r in allrows if r["signal_above_roundoff"]),
        "method_comparison":comparisons,"elapsed_seconds":time.perf_counter()-start}
    (HERE/"validation.json").write_text(json.dumps(validation,indent=2,ensure_ascii=False,allow_nan=False),encoding="utf-8")
    print(json.dumps({"done":True,"seconds":validation["elapsed_seconds"],"comparisons":comparisons},indent=2),flush=True)

if __name__=="__main__":main()
