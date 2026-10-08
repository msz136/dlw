"""Independent exact checks of DLW theory notebook; no notebook/proof mutation."""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import math
from functools import lru_cache
from pathlib import Path

import sympy as S

ROOT = Path("C:/Users/msz/aca")
OUT = Path(__file__).resolve().parent
NB_PATH = ROOT / "notebook/DLW理论.ipynb"
PROJECT = ROOT / "Workspaces/dlw_theory_notebook_20261008"
PROOFS = PROJECT / "proofs"
checks = []


def zero(name, expr, **context):
    reduced = S.factor(S.expand(expr))
    checks.append({"name": name, "passed": reduced == 0,
                   "residual": str(reduced), **context})
    if reduced != 0:
        raise AssertionError((name, reduced, context))


x, y, t, a, h = S.symbols("x y t a h", real=True, nonzero=True)
A, B = S.Function("A")(x, y, t), S.Function("B")(x, y, t)
dx = lambda z: S.diff(z, x)
dy = lambda z: S.diff(z, y)
dt = lambda z: S.diff(z, t)
u, v = 2*dx(B), 2*dx(dy(A))
R = dx(dx(A)) + dx(B)**2 + dt(B) + 2*a*dx(B)
T = dx(dx(dy(A))) - dx(dx(dy(B))) - dt(dy(A)) + dt(dy(B))
T -= 2*dx(B)*(dx(dy(A))-dx(dy(B)))
T -= 2*a*(dx(dy(A))-dx(dy(B)))
T += 4*dx(B)
C1 = dy(dt(u)) + dx(dx(v)) + dx((u+2*a)*dy(u))
C2 = dt(v) + dx(dx(dy(u))) + dx((u+2*a)*v-4*u)
zero("C1 normalized residual identity", C1 - 2*dx(dy(R)), cell=3, line=27)
zero("C2 normalized residual identity", C2 - (2*dx(dy(R))-2*dx(T)), cell=3, line=27)

# Generic differential functions at neighboring lattice sites.  These checks
# do not assume equations, boundary conditions, periodicity, or Gram data.
U = {k: S.Function(f"u{k+3}")(x,t) for k in range(-3,4)}
O = {k: S.Function(f"omega{k+3}")(x,t) for k in range(-3,4)}
d0 = lambda Z,j: (Z[j+1]-Z[j-1])/(2*h)
dm = lambda Z,j: (Z[j]-Z[j-1])/h
mm = lambda Z,j: (Z[j]+Z[j-1])/2
lap = lambda Z,j: (Z[j+1]-2*Z[j]+Z[j-1])/h**2
V = {k: 4*O[k]/h+d0(U,k) for k in range(-2,3)}
W = {k: V[k]-d0(U,k) for k in range(-2,3)}
H = {k: U[k]**2/2+2*a*U[k]+h**2*(W[k]**2/32-W[k]/4)
     for k in range(-2,3)}
UW = {k: (U[k]**2+O[k]**2)/2+2*a*U[k]-h*O[k]
      for k in range(-2,3)}
R7 = {k: dm({j:dt(U[j]) for j in U},k)+dx(dm(UW,k))
      +dx(dx(dm(U,k)+4*mm(O,k)/h)) for k in (0,1)}
Romega = dt(O[0])+dx((U[0]+2*a)*O[0]-h*U[0])-dx(dx(O[0]))
N81 = dm({j:dt(U[j]) for j in U},0)+dx(dm(H,0))
N81 += dx(dx(mm(V,0)-h**2*lap({k:dm(U,k) for k in (-1,0,1)},0)/4))
N82 = dt(V[0])+dx(d0(H,0)+(U[0]+2*a)*W[0]-4*U[0])
N82 += dx(dx(d0(U,0)+h**2*lap(W,0)/4))
zero("N8 first residual equals N7 first residual", N81-R7[0], cell=18, line=37)
zero("N8 second residual decomposition", N82-4*Romega/h-(R7[0]+R7[1])/2,
     identity="N8_2 = (4/h) N7_2 + M_plus N7_1", cell=18, line=37)
c=S.Function("c")(t)
constant_mode={**{z:c for z in U.values()},**{z:S.Integer(0) for z in O.values()}}
zero("N8 leaves a time-dependent lattice mean", N81.subs(constant_mode).doit(),
     cell=18,line=29,field="u_j=c(t), v_j=0",equation=1)
zero("N8 leaves a time-dependent lattice mean", N82.subs(constant_mode).doit(),
     cell=18,line=29,field="u_j=c(t), v_j=0",equation=2)

alpha, b0, b1 = [S.Function(z)(x,t) for z in ("alpha","beta0","beta1")]
Aj = dx(dx(alpha+b0))+dx(alpha-b0)**2+dt(alpha-b0)+(2*a-h)*dx(alpha-b0)
Cj = dx(dx(alpha+b1))+dx(alpha-b1)**2+dt(alpha-b1)+(2*a+h)*dx(alpha-b1)
pot = alpha-(b0+b1)/2
om = dx(b1-b0)
q_normalized = dt(pot)+dx(dx(pot))+dx(pot)**2+2*a*dx(pot)
q_normalized += dx(dx(b0+b1))+om**2/4-h*om/2
zero("Q residual over Q equals (A+C)/2", q_normalized-(Aj+Cj)/2, cell=28, line=35)
Q, Z = S.Function("Q")(x,t), S.Function("omega")(x,t)
RR = (1-Z/h)/Q
UU = 2*dx(Q)/Q
product_res = dt(Q*RR)-dx(dx(Q*RR))+2*a*dx(Q*RR)+2*dx(dx(Q)*RR)
omega_res = dt(Z)-dx(dx(Z))+dx((UU+2*a)*Z-h*UU)
zero("N18 product equation matches omega equation", S.cancel(product_res+omega_res/h),
     cell=28, line=66)
qf, rf, kf = [S.Function(z)(x,t) for z in ("Q","R","kappa")]
resq=dt(qf)+dx(dx(qf))+2*a*dx(qf)+kf*qf
resr=dt(rf)-dx(dx(rf))+2*a*dx(rf)-kf*rf
resprod=dt(qf*rf)-dx(dx(qf*rf))+2*a*dx(qf*rf)+2*dx(dx(qf)*rf)
zero("Q/R residual product split", resprod-rf*resq-qf*resr, cell=28, line=78)

# Taylor coefficients of the wall combinations are independent of Gram data.
coeff = S.symbols("P0:7")
Phi = lambda z: sum(coeff[k]*z**k/S.factorial(k) for k in range(7))
zero("S2 centered sum through fourth order",
     (Phi(h/2)+Phi(-h/2))/2-coeff[0]-h**2*coeff[2]/8-h**4*coeff[4]/384
     -h**6*coeff[6]/46080, cell=5, line=41)
zero("S2 centered difference through fourth order",
     (Phi(h/2)-Phi(-h/2))/h-coeff[1]-h**2*coeff[3]/24-h**4*coeff[5]/1920,
     cell=5, line=50)
p,q,z=S.symbols("p q z", real=True, nonzero=True)
lam=lambda zz: (zz+h/2)/(zz-h/2)
chi=lam(p-a)*lam(q+a)
gam=lambda s: -(p-s)/(q+s)
zero("T22 spectral wall shift", S.cancel(gam(a+h/2)*chi-gam(a-h/2)), cell=8, line=45)
kappa,mu,nu,eta1,eta2,ss,zeta=S.symbols("kappa mu nu eta1 eta2 s zeta")
kx=mu+nu-kappa**2
zetax=kappa*(1-zeta)-ss*zeta+eta1
eta1x=nu*(1-zeta)-ss*eta1+eta2
zetat=mu*(1-zeta)-ss*kappa+ss**2*zeta-eta2+eta1*kappa
zetaxx=kx*(1-zeta)-kappa*zetax-ss*zetax+eta1x
zero("T18 to T19 scalar cancellation",zetaxx+zetat+2*ss*zetax-2*kx*(1-zeta),
     cell=8,line=31)
amp2=S.cancel((gam(a-h/2)**2/chi)/(gam(a)**2))
zero("F interpolation normalized amplitude is even in h", amp2-amp2.subs(h,-h),
     cell=22, line=15)
phase_series=S.series(S.log((z+h/2)/(z-h/2))/h,h,0,5).removeO()
zero("lattice phase Taylor series", phase_series-1/z-h**2/(12*z**3)-h**4/(80*z**5),
     cell=22, line=15)

PS=tuple(map(S.Rational,["1/5","1/3","1/2","2/3"]))
QS=tuple(map(S.Rational,["1/4","2/5","3/5","4/5"]))
AA,HH=S.Integer(2),S.Rational(1,4)
RHOS=tuple(map(S.Rational,["3/2","4/3","5/4","6/5"]))


@lru_cache(None)
def jets(N,ss,n,j,rhos):
    K=S.Matrix(N,N,lambda i,k:rhos[i]/(PS[i]+QS[k])*
               (-(PS[i]-ss)/(QS[k]+ss))**n*
               (((PS[i]-AA+HH/2)/(PS[i]-AA-HH/2))*
                ((QS[k]+AA+HH/2)/(QS[k]+AA-HH/2)))**j)
    M=S.eye(N)+K
    Jx=S.Matrix(N,N,lambda i,k:(PS[i]+QS[k])*K[i,k])
    Jxx=S.Matrix(N,N,lambda i,k:(PS[i]+QS[k])**2*K[i,k])
    Jt=S.Matrix(N,N,lambda i,k:(QS[k]**2-PS[i]**2)*K[i,k])
    def det_cols(replacements):
        mat=M.copy()
        for col,vec in replacements.items():
            mat[:,col]=vec
        return mat.det()
    fx=sum(det_cols({k:Jx[:,k]}) for k in range(N))
    ft=sum(det_cols({k:Jt[:,k]}) for k in range(N))
    fxx=sum(det_cols({k:Jxx[:,k]}) for k in range(N))
    fxx+=2*sum(det_cols({i:Jx[:,i],k:Jx[:,k]}) for i,k in itertools.combinations(range(N),2))
    return M.det(),fx,fxx,ft


def bil(s,F,G):
    f,fx,fxx,ft=F
    g,gx,gxx,gt=G
    return fxx*g-2*fx*gx+f*gxx+ft*g-f*gt+2*s*(fx*g-f*gx)


for N in range(1,5):
    for ss in (AA-HH/2,AA+HH/2,S.Rational(7,5)):
        for n in (-2,0,1):
            for j in (-2,0,2):
                zero("T13 exact rational determinant jets",
                     bil(ss,jets(N,ss,n+1,j,RHOS[:N]),jets(N,ss,n,j,RHOS[:N])),
                     N=N,s=str(ss),n=n,j=j,cell=8,line=7)
    for j in (-2,0,2):
        fj=jets(N,AA-HH/2,1,j,RHOS[:N])
        gj=jets(N,AA,0,j,RHOS[:N])
        gp=jets(N,AA,0,j+1,RHOS[:N])
        zero("S1 minus wall determinant jets",bil(AA-HH/2,fj,gj),N=N,j=j,cell=7,line=18)
        zero("S1 plus wall determinant jets",bil(AA+HH/2,fj,gp),N=N,j=j,cell=7,line=18)
        if N<=2:
            E=[RHOS[i]/(PS[i]+QS[i])*
               (((PS[i]-AA+HH/2)/(PS[i]-AA-HH/2))*
                ((QS[i]+AA+HH/2)/(QS[i]+AA-HH/2)))**j for i in range(N)]
            gammas=[-(PS[i]-AA+HH/2)/(QS[i]+AA-HH/2) for i in range(N)]
            interaction=((PS[0]-PS[1])*(QS[0]-QS[1]))/((PS[0]+QS[1])*(PS[1]+QS[0]))
            Ge=1+sum(E)+(interaction*E[0]*E[1] if N==2 else 0)
            Fe=1+sum(gammas[i]*E[i] for i in range(N))
            if N==2:
                Fe+=interaction*gammas[0]*gammas[1]*E[0]*E[1]
            zero("T5/T6 G expansion",gj[0]-Ge,N=N,j=j,cell=10,line=43 if N==1 else 49)
            zero("T5/T6 F expansion",fj[0]-Fe,N=N,j=j,cell=10,line=43 if N==1 else 50)

# Vanishing tau is allowed for bilinear exactness, but not for log fields.
singular_rhos=(-(PS[0]+QS[0]),)
singF=jets(1,AA-HH/2,1,0,singular_rhos)
singG=jets(1,AA-HH/2,0,0,singular_rhos)
assert singG[0]==0
zero("T13 extends through tau_n=0",bil(AA-HH/2,singF,singG),cell=8,line=41)
zero("T13 nonnegative layer also permits p=s in a mathematical example",
     bil(PS[0],jets(1,PS[0],1,0,RHOS[:1]),jets(1,PS[0],0,0,RHOS[:1])),
     cell=7,line=22,n=0,s=str(PS[0]))

# Formal boundary hypotheses and correspondence audit, using runner's own
# import lexer but neither installing magic nor invoking any compiler.
spec=importlib.util.spec_from_file_location("audited_lean_runner",ROOT/"Workspaces/report_colab_20261006/lean_notebook.py")
runner=importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
nb=json.loads(NB_PATH.read_text(encoding="utf-8"))
local_sources={}
def closure(module):
    path=PROOFS.joinpath(*module.split(".")).with_suffix(".lean")
    if not path.is_file() or module in local_sources:
        return
    raw=path.read_text(encoding="utf-8-sig")
    visible=runner._visible_code(raw)
    local_sources[module]={"path":str(path),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                           "imports":runner._imports(raw),
                           "untrusted_axiom_or_placeholder": bool(__import__("re").search(r"\b(sorry|admit|axiom)\b",visible))}
    for dep in local_sources[module]["imports"]:
        closure(dep)

cell_sources=[]
latest_run=PROJECT/"runs/20261008_185555_78cde8d1"
history=json.loads((latest_run/"history.json").read_text(encoding="utf-8"))
for ci,cell in enumerate(nb["cells"],1):
    src="".join(cell["source"])
    if cell["cell_type"]=="code" and src.startswith("%%lean "):
        header,raw_body=src.split("\n",1)
        # Jupyter/IPython's cell input transformation terminates each input
        # line with a newline.  Seven notebook cells omit the final newline
        # in JSON; their saved compiler inputs differ by exactly that newline.
        body=raw_body if raw_body.endswith("\n") else raw_body+"\n"
        route,stage=header.split()[1:]
        for mod in runner._imports(body):
            closure(mod)
        module=("Theory"+route.title()+stage.title()) if route not in ("uw","qrm") else runner.MODULES[route][stage]
        path=latest_run/"cells"/(module+".lean")
        compile_records=[entry for entry in history if Path(entry["source"]).name==path.name]
        digest=hashlib.sha256(body.encode("utf-8")).hexdigest()
        artifact_records=[r for r in compile_records if r.get("passed") and r.get("exit_code")==0 and r.get("sha256")==digest]
        artifact_match=bool(artifact_records) and all(Path(r["artifact"]).is_file() and
             hashlib.sha256(Path(r["artifact"]).read_bytes()).hexdigest()==r.get("artifact_sha256") for r in artifact_records)
        cell_sources.append({"cell":ci,"module":module,"compiler_payload_sha256":digest,
                             "raw_notebook_body_sha256":hashlib.sha256(raw_body.encode("utf-8")).hexdigest(),
                             "normalization":"final newline only" if raw_body!=body else "none",
                             "saved_source_matches":path.is_file() and path.read_bytes()==body.encode("utf-8"),
                             "successful_compile_matches":bool(artifact_records),
                             "saved_artifact_matches":artifact_match})
events=json.loads((latest_run/"cache_events.json").read_text(encoding="utf-8"))
cache_evidence=[]
for module,record in local_sources.items():
    if module.startswith("Step"):
        continue  # Notebook-defined earlier cells, not proof modules.
    relevant=[ev for ev in events if ev["module"]==module]
    manifests=[]
    for ev in relevant:
        entry=Path(ev["entry"])
        manifest=json.loads((entry/"ready.json").read_text(encoding="utf-8"))
        artifact_matches=all(hashlib.sha256((entry/"lib/lean"/rel).read_bytes()).hexdigest()==sha
                             for rel,sha in manifest["artifacts"].items())
        source_matches=all(hashlib.sha256((PROOFS/rr["path"]).read_bytes()).hexdigest()==rr["sha256"]
                           for rr in manifest["descriptor"]["sources"].values())
        manifests.append({"entry":str(entry),"artifact_matches":artifact_matches,"transitive_sources_match":source_matches})
    cache_evidence.append({"module":module,"source_sha256":record["sha256"],
                           "cached_source_matches":bool(relevant) and all(ev["source_sha256"]==record["sha256"] for ev in relevant),
                           "manifests":manifests})
mathlib_def=ROOT/"_lean_shared/mathlib/Mathlib/Analysis/Calculus/ContDiff/Defs.lean"
scope_notes=[
    {"cell":18,"line":1,"classification":"domain wording","priority":"P3",
     "text":"非零区域不足以定义实值 log F、log G；本节后文以及全部 Lean 终点实际采用 F,G>0。改为严格为正的区域，或明确使用 log|F|, log|G| 并另证局部版本。",
     "invalidates_current_theorems":False},
    {"cell":7,"line":22,"classification":"formal coverage wording","priority":"P3",
     "text":"正文仅在 n<0 时要求 p_i-s≠0；C07 实际通过 LayerOK 对所有 n 要求 p_i-s≠0。正文通用辅助层引理在 n≥0 的退化参数情形比当前 Lean 定理更宽。F/G 采用 s=a±h/2，Admissible 已排除这些退化，故主定理无缺口。",
     "proof_file":str(PROOFS/"Contracts.lean"),"proof_lines":[104,105,134,135],
     "invalidates_current_theorems":False},
    {"cell":18,"line":29,"classification":"boundary caveat for numerical consumers","priority":"note",
     "text":"N7/N8 为两场封闭残差系统，但 δ_-u_t 留有格点常数模态。若解释为时间推进系统，还须给均值/边界规范。u_j=c(t),v_j=0 为任意 c 的残差解。此处未断言适定性，因此不作为理论错误。"}
]
evidence={"notebook":str(NB_PATH),"notebook_sha256":hashlib.sha256(NB_PATH.read_bytes()).hexdigest(),
          "scope":"31 cells of DLW theory; only directly imported local proof closure and runner",
          "symbolic_checks":checks,"symbolic_check_count":len(checks),
          "all_symbolic_checks_passed":all(c["passed"] for c in checks),
          "cell_compile_correspondence":cell_sources,"local_proof_sources":local_sources,
          "proof_source_cache_correspondence":cache_evidence,
          "contdiff_top_semantics":{"path":str(mathlib_def),"lines":[91,1196],
                                     "meaning":"ContDiff real top is real analytic (omega), not the infinite smoothness index."},
          "scope_notes":scope_notes,"lean_recompiled":False,
          "limitations":"Finite-N exact spot checks supplement endpoint/source audit; they do not independently prove arbitrary-N theorems or uniform compact rates."}
(OUT/"evidence.json").write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"checks":len(checks),"all_symbolic_checks_passed":True,
                  "local_proof_modules":len(local_sources),
                  "cell_sources_match":all(c["saved_source_matches"] for c in cell_sources),
                  "cell_compile_records_match":all(c["successful_compile_matches"] for c in cell_sources),
                  "cell_artifacts_match":all(c["saved_artifact_matches"] for c in cell_sources),
                  "cache_sources_match":all(c["cached_source_matches"] for c in cache_evidence),
                  "no_custom_axioms_or_placeholders":not any(c["untrusted_axiom_or_placeholder"] for c in local_sources.values())},ensure_ascii=False))
