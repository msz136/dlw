"""New exact nonlinear physical/AKNS trace-vector identities."""
import hashlib, json
from pathlib import Path
import sympy as sp

x = sp.symbols("x", real=True)
S, lam, eta, rho, havg = sp.symbols("S lam eta rho havg", nonzero=True)
u,v,F,E,H = [sp.Function(n)(x) for n in ["u","v","F","E","H"]]
D = lambda f: sp.diff(f,x)
q = u-S
V = -2*u*v/S
A = (S*S/4-v*v)/(S*S)
r = A*(S+u)-D(v)/S
odes = {D(F):(V-lam)*F+2*r*H,
        D(E):(lam-V)*E-2*q*H,
        D(H):q*F-r*E}
rules = {}
for fun in [F,E,H]:
    for n in [1,2,3]:
        ex = sp.diff(odes[D(fun)],x,n-1)
        for _ in range(5): ex=ex.xreplace(odes)
        rules[sp.diff(fun,x,n)] = sp.expand(ex)

def reduce(ex):
    for _ in range(8): ex=sp.expand(ex.xreplace(rules))
    return sp.factor(ex)

checks=[]
def check(name,ex):
    result=reduce(ex)
    assert result==0,(name,result)
    checks.append(name)

# Mean-zero K adjoint gives -K(H_x) = -(H-havg).
guc = F+A*E+2*v*(H-havg)/S
gvc = (-2*v*(1+u/S)/S)*E+D(E)/S+2*u*(H-havg)/S
# fixed physical lambda: subtract F_zeta d_eta = h_avg*c.
gu = F+A*E+2*v*H/S
gv = (lam-2*v)*E/S+2*H
check("centered_source_gradient_v",gvc-(gv-2*u*havg/S))
check("fixed_lambda_holonomy_cancels_u",guc+2*v*havg/S-gu)
check("fixed_lambda_holonomy_cancels_v",gvc+2*u*havg/S-gv)
ut=-D(gv)/16
vt=-D(gu)/16
R=S*F+(lam*v/S-v*v/S-S/4)*E+(2*v-lam)*H
Vt=-2*(v*ut+u*vt)/S
check("local_V_t_is_total_derivative",Vt-D(R)/(8*S))
thetat=(R-rho)/(8*S)
# a_t/e^theta and b_t*e^theta, without exponentials.
at=ut+q*thetat
rt=A*ut-2*v*(1+u/S)*vt/S-D(vt)/S
bt=rt-r*thetat
w=(S*S-lam*lam)/(16*S)
check("physical_a_trace_vector",at-w*E+rho*q/(8*S))
check("physical_b_trace_vector",bt+w*F-rho*r/(8*S))
# Exact central triangular connection and canonical trace derivative.
Hmat=sp.diag(1,-1)
Emat=sp.Matrix([[0,1],[0,0]])
Fmat=sp.Matrix([[0,0],[1,0]])
Lchi=sp.Matrix([[u/2+lam*v/S,(S/2+v)*(1+lam/S)],
              [(S/2-v)*(lam/S-1),-u/2-lam*v/S]])
Lplus=(u/2+v)*Hmat+(S+2*v)*Emat
Lminus=(u/2-v)*Hmat-(S-2*v)*Fmat
for i,j in [(0,0),(0,1),(1,0),(1,1)]:
    check(f"central_triangular_plus_{i}{j}",Lchi.subs(lam,S)[i,j]-Lplus[i,j])
    check(f"central_triangular_minus_{i}{j}",Lchi.subs(lam,-S)[i,j]-Lminus[i,j])
check("spectral_trace_gradient_half_factor",
      sp.trace(sp.Matrix([[H,E],[F,-H]])*Hmat/2)-H)

here=Path(__file__)
out={"status":"all new nonlinear physical/AKNS trace identities passed",
     "check_count":len(checks),"checks":checks,
     "script_sha256":hashlib.sha256(here.read_bytes()).hexdigest(),
     "sympy_version":sp.__version__,
     "previous_certificate_scripts_rerun":False,
     "not_proved_by_script":["weighted Birkhoff inverse and action-only discriminant",
                             "infinite fiber tangent/gradient-closure theorem",
                             "strong coherent fiber tangent equality"]}
here.with_suffix(".json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf8")
print(json.dumps(out,ensure_ascii=False,indent=2))
