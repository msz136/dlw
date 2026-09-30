from pathlib import Path
root=Path(__file__).resolve().parents[2]/'Workspaces/dlw_semidiscrete/numerics'
p=root/'experiments/check_regressions.py';s=p.read_text(encoding='utf-8')
a=s.index('# ---------------------------------------------------------------- defect 2');b=s.index('\nprint()\n',a)
s=s[:a]+'''# Live-source checks: no experiment top-level execution and no JSON writes.
import ast
from pathlib import Path
EXPDIR=Path(__file__).resolve().parent

def functions_from(name, scope):
    tree=ast.parse((EXPDIR/name).read_text(encoding="utf-8"))
    funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
    exec(compile(ast.Module(body=funcs,type_ignores=[]),name,"exec"),scope)
    return scope

print("\\n6. Live E7 temporal self-convergence (current source)")
X7=XGrid(256,40.,4); ys=np.linspace(-6,6,241)
scope={"np":np,"X":X7,"A":4.,"dy":ys[1]-ys[0],
       "U":np.array([cr.u0_row(y,X7.x,0) for y in ys]),
       "V":np.array([cr.v0_row(y,X7.x,0) for y in ys])}
run=functions_from("e7_fd_baseline.py",scope)["run"]
ur,vr,_=run(.01/128,.01); errs=[]
for div in [2,4,8,16]:
    u,v,n=run(.01/div,.01)
    check(f"E7 reaches {div} steps with finite fields",n==div and np.isfinite(u).all() and np.isfinite(v).all())
    errs.append(float(np.max(abs(v-vr))))
orders=np.log2(np.array(errs[:-1])/errs[1:])
check("live E7 RK4 order exceeds 3.5",np.isfinite(orders).all() and np.all(orders>3.5),str(orders))

print("\\n7. Live E1 quadrature and E5 initial/site checks")
xs=np.linspace(-1.5,1.5,25)
ns=functions_from("e1_continuum.py",{"np":np,"Y_LO":-1.5,"Y_HI":1.5,"DXW":.125})
unit=np.ones((12,25)); norm=ns["norms"](unit,unit,.25,xs)[2]
check("E1 constant integrates to rectangle area",abs(norm-3.)<1e-12,str(norm))
for h in [.25,.125]:
    js=ns["js_in_window"](h)
    check(f"E1 physical window h={h}",abs(len(js)*h-3)<1e-12)
from solver import Chain
C5=Chain(-2,2,.25,4.); X5=XGrid(8,8.,4)
class ZeroRHS:
    def b_fun(self,t): return np.full(8,10.)
    def __call__(self,t,P,W): return np.zeros_like(P),np.zeros_like(W)
scope={"np":np,"Cs":C5,"Xg":X5,"MID":0,"J_L":-2,"H_S":.25,"integrate":integrate}
record=functions_from("e5_conservation.py",scope)["integrate_full"]
P=np.repeat(np.arange(1,5)[:,None],8,axis=1).astype(float)
W=np.repeat(np.arange(5)[:,None],8,axis=1).astype(float)
cap,info,_=record(ZeroRHS(),P,W,.01,.005,"rk4")
check("E5 includes t=0",cap[0][0]==0 and len(cap)==3)
check("E5 selects correct u/W site",np.allclose(cap[0][1],10.75) and np.allclose(cap[0][3],2))
check("E5 reconstructs correct v site",np.allclose(cap[0][2],4.5))

print("\\n8. Live E6 Jacobian and eigenmode measured through the solver")
sys.path.insert(0,str(EXPDIR))
from e6_growth import eigenmode_check
from linearized import effective_k
for nx in [64,128]:
    result=eigenmode_check(nx)
    check(f"E6 live mode agrees nx={nx}",result["relative_error"]<1e-5 and result["jacobian_error"]<1e-8,str(result["relative_error"]))
    X6=XGrid(nx,60.,4); theta=2*np.pi*(nx//8)/60
    wave=np.exp(1j*theta*X6.x)
    check(f"E6 symbol matches actual D1 nx={nx}",np.max(abs(X6.D1@wave-1j*effective_k(theta,X6.dx)*wave))<1e-11)
'''+s[b:]
s=s.replace('Every check here FAILS on the pre-fix code and PASSES after the fix, so the','Live behavior checks exercise current source; JSON checks are supplementary. The')
s=s.replace('all("g_max_discrete" in g for g in e6.get("grid_gmax", []))','bool(e6.get("grid_gmax")) and all("g_max_discrete" in g for g in e6["grid_gmax"])')
s=s.replace('all("g_measured" in s for s in sg)','bool(sg) and all(s.get("finite") and s.get("relative_error",1)<1e-5 for s in sg)')
p.write_text(s,encoding='utf-8')
