"""Independent, bounded numerical checks of the DLW notebook; never edits it."""
from __future__ import annotations

import contextlib
import io
import json
import pathlib
import time

import numpy as np

BASE = pathlib.Path(__file__).resolve().parent
NB = pathlib.Path(r"C:\Users\msz\aca\notebook\DLW数值分析report.ipynb")
notebook = json.loads(NB.read_text(encoding="utf-8"))
ns = {"__name__": "audited_notebook", "display": lambda *args, **kwargs: None}
for number in (2, 4, 6, 8, 9, 11, 13, 14, 16, 18, 20):
    source = "".join(notebook["cells"][number-1]["source"])
    # IPython supplies presentation only; retain every numerical source line.
    source = source.replace("from IPython.display import display", "# display stub supplied by audit")
    exec(compile(source, f"DLW.ipynb:cell{number}", "exec"), ns)

def json_float(value):
    return float(value)

checks = {}
config = ns["CONFIG"]
started = time.perf_counter()

# Distinguish exact tau quotient from a lift that only guarantees sampled u.
lift_checks = []
for case in ns["CASES"]:
    m = ns["SD2Model"](case, config)
    z = m.initial()
    q, r = m.unpack(z, 0.)
    u, v = m.G.uv(m.js, m.X.x, 0.)
    log_f, _ = m.G.tau(m.js, m.X.x, 0., True)
    log_g, _ = m.G.tau(m.js, m.X.x, 0.)
    ratio = np.exp(log_f-log_g)
    ratio /= ratio[:, :1]
    lift_checks.append(dict(case=case, min_q=float(q.min()), max_q=float(q.max()),
        lift_minus_tau_ratio=float(abs(q-ratio).max()),
        normalized_alternation=float(abs(np.diff(q-ratio, axis=1)).max()),
        lift_equation_residual=float(abs(m.dx(q,m.jump)-.5*u*q).max()),
        initial_fields_error=[float(abs(a-b).max()) for a,b in zip(m.fields(z,0.),(u,v))],
        endpoint_ratios=(1+np.asarray(m.jump).ravel()).tolist()))
checks["sd2_initial_lift"] = lift_checks

# Differentiate the lower lift independently in time, including a deformed mesh.
derivative_checks = []
for mesh in ("fixed", "moving"):
    p = ns["Problem"]("C", "SD2", mesh, config)
    state = p.initial()
    velocity = p.stage(0., state)[-p.X.n:]
    model = p.m
    physical_qt = model.boundary_derivative(0., velocity)
    qx = model.dx(model.boundary(0.)[0], model.boundary(0.)[1])
    material_qt = physical_qt + velocity*qx
    orig_s = p.X.s.copy()
    eps = 1e-7
    p.X.set_s(orig_s + eps*velocity)
    qp = model.boundary(eps)[0].copy()
    p.X.set_s(orig_s - eps*velocity)
    qm = model.boundary(-eps)[0].copy()
    p.X.set_s(orig_s)
    model.boundary(0.)
    derivative_checks.append(dict(mesh=mesh,
        independent_material_derivative_error=float(abs((qp-qm)/(2*eps)-material_qt).max()),
        material_derivative_size=float(abs(material_qt).max()), min_J=float(p.X.J.min())))
checks["sd2_boundary_derivative"] = derivative_checks

# The core RHS equals the equations printed in each scheme's markdown.
rhs_checks = []
for kind in ("SD", "FD"):
    p = ns["Problem"]("C", kind, "fixed", config)
    state = p.initial()
    m = p.m
    z = state[:-p.X.n]
    pp, ww = m.unpack(z)
    u = m.recover_u(pp, 0.)
    d1,d2,h,a = m.X.d1,m.X.d2,m.h,m.a
    if kind == "SD":
        H = .5*u**2 + 2*a*u + h**2*(ww**2/32-ww/4)
        fp = -np.diff(d1(H),axis=0)/h-d2(pp+.5*(ww[1:]+ww[:-1]))
        fw = -d1((u+2*a)*ww-4*u)+d2(ww)
    else:
        ghosts=ns["ghost_u"](m.G,m.js,m.X.x,0.,u)
        fp=-np.diff(d1(.5*u**2+2*a*u),axis=0)/h-d2(.5*(ww[1:]+ww[:-1]))
        fw=-d1((u+2*a)*ww-4*u)-d2(ns["delta0"](u,ghosts,h))
    reference=m.pack(fp,fw)
    rhs_checks.append(dict(model=kind, rhs_formula_difference=float(abs(reference-m.rhs(0.,z)).max())))
checks["printed_rhs_checks"] = rhs_checks

# Self convergence on one representative two-soliton case, fixed x/y discretization.
order_checks = []
for kind in ("SD", "SD2", "FD"):
    records=[]
    for divisor in (1,2,4):
        records.append(ns["solve"]("C", kind, "Euler", "fixed", dict(config,dt=config['dt']/divisor)))
    first=records[0]
    differences=[]
    orders=[]
    for fi in range(2):
        d1=float(abs(records[0]['fields'][fi]-records[1]['fields'][fi]).max())
        d2=float(abs(records[1]['fields'][fi]-records[2]['fields'][fi]).max())
        differences.append([d1,d2]); orders.append(float(np.log2(d1/d2)))
    order_checks.append(dict(case="C", model=kind, method="Euler",
        completed=[bool(r['completed']) for r in records], reached=[r['reached'] for r in records],
        field_differences=differences, observed_orders=orders,
        max_errors=[r['max_errors'] for r in records]))
checks['bounded_time_self_convergence']=order_checks

# Compare frozen mesh transport against its exact, independent discrete identity.
ale_checks=[]
for kind in ("SD", "FD"):
    p=ns['Problem']('B',kind,'moving',config)
    state=p.initial(); m=p.m; z=state[:-p.X.n]
    full=p.stage(0.,state); vel=full[-p.X.n:]; phys=m.rhs(0.,z)
    pp,ww=m.unpack(z)
    expected=phys+m.pack(m.X.d1(pp)*vel,m.X.d1(ww)*vel)
    ale_checks.append(dict(model=kind, transport_difference=float(abs(expected-full[:-p.X.n]).max()),
        min_J=float(m.X.J.min()), fixed_left_velocity=float(vel[0]),
        velocity_max=float(abs(vel).max())))
checks['ale_discrete_identity']=ale_checks

# Quantify the assumed isolated-soliton tails at the artificial x boundaries.
tails=[]
for case in ns['CASES']:
    for label,cfg in (('main',config),('field',dict(config,L=80.,nx=512,yhalf=30.))):
        model=ns['SD2Model'](case,cfg)
        endpoints=np.array([-cfg['L']/2,cfg['L']/2])
        fields=model.G.uv(model.js,endpoints,cfg['T'])
        tails.append(dict(case=case,configuration=label, endpoint_nonperiodicity={name:float(abs(f[:,1]-f[:,0]).max()) for name,f in zip(('u','v'),fields)},
            endpoint_field_size={name:float(abs(f).max()) for name,f in zip(('u','v'),fields)}))
checks['exact_boundary_tails']=tails

# An x checkerboard is a genuine growing semidiscrete mode, not a time-step artefact.
from types import SimpleNamespace
growth=[]
for nx in (256,512,1024):
    cfg=dict(config,nx=nx)
    m=ns['SDModel']('A','SD',cfg)
    m.G=SimpleNamespace(uv=lambda js,x,t:(np.zeros((len(np.atleast_1d(js)),len(np.atleast_1d(x)))),)*2)
    pp=np.tile((-1.)**np.arange(nx),(m.shape[0]-1,1))
    ww=np.zeros(m.shape)
    z=m.pack(pp,ww)
    actual=m.rhs(0.,z)
    rate=4/m.X.dx**2
    growth.append(dict(nx=nx,dx=m.X.dx, positive_eigenvalue=rate,
        eigenmode_residual=float(abs(actual-rate*z).max()),
        exact_amplification_at_T=float(np.exp(rate*cfg['T'])),
        euler_amplification_at_T=float((1+cfg['dt']*rate)**round(cfg['T']/cfg['dt']))))
checks['sd_backward_heat_mode']=growth

# Independent cumulants evaluate the continuous PDE, without finite differences.
def cumulant(w,rates,indices):
    mean=np.einsum('i,ijk->jk',rates[:,indices[0]],w)
    centered=[rates[:,index,None,None]-np.einsum('i,ijk->jk',rates[:,index],w)[None,:,:] for index in indices]
    if len(indices)==2:
        return np.sum(w*centered[0]*centered[1],axis=0)
    if len(indices)==3:
        return np.sum(w*centered[0]*centered[1]*centered[2],axis=0)
    total=np.sum(w*np.prod(centered,axis=0),axis=0)
    for a,b,c,d in ((0,1,2,3),(0,2,1,3),(0,3,1,2)):
        total-=np.sum(w*centered[a]*centered[b],axis=0)*np.sum(w*centered[c]*centered[d],axis=0)
    return total

pde_checks=[]
for case in ns['CASES']:
    G=ns['Exact'](case,config['h'],config['a'])
    js=np.arange(-12,12); x=np.linspace(-5,5,101); t=.01
    _,f=G.tau(js,x,t,True); _,g=G.tau(js,x,t)
    def both(inds,plus=False):
        a=cumulant(f,G.rates,inds); b=cumulant(g,G.rates,inds)
        return 2*(a+b if plus else a-b)
    u,v=G.uv(js,x,t)
    ux=both((0,0)); uy=both((0,2)); uxy=both((0,0,2)); uyt=both((0,1,2))
    vxx=both((0,0,0,2),True); vt=both((0,1,2),True); vx=both((0,0,2),True); uxxy=both((0,0,0,2))
    pde_checks.append(dict(case=case,first_pde_residual=float(abs(uyt+ux*uy+(u+2*config['a'])*uxy+vxx).max()),
        second_pde_residual=float(abs(vt+ux*v+(u+2*config['a'])*vx-4*ux+uxxy).max())))
checks['continuous_exact_pde_residual']=pde_checks

# The 27 main solves are short, so verify every saved numerical comparison.
import re
main=[]
records={}
for method,mesh in (('RK4','fixed'),('Euler','fixed'),('RK4','moving')):
    for case in ns['CASES']:
        for kind in ns['MODELS']:
            result=ns['solve'](case,kind,method,mesh,config)
            records[case,kind,method,mesh]=result
            main.append({key:result[key] for key in ('case','model','method','mesh','completed','reached','reason','initial_error','max_errors','min_J')})
            main[-1]['completed']=bool(main[-1]['completed'])
checks['main_27_runs']=main

def saved_table(number):
    outputs=notebook['cells'][number-1]['outputs']
    html=next(''.join(output['data']['text/html']) for output in outputs if 'text/html' in output.get('data',{}))
    return {(int(row),int(col)):value.strip() for row,col,value in re.findall(r'<td\s+id="[^"]*_row(\d+)_col(\d+)"[^>]*>([^<]+)</td>',html)}

comparisons=[]
for number in (22,24,28,30):
    actual={}
    if number==22:
        for row,(case,field) in enumerate((case,field) for case in ns['CASES'] for field in ('u','v')):
            for col,kind in enumerate(ns['MODELS']):
                actual[row,col]=f"{records[case,kind,'RK4','fixed']['max_errors'][field]:.3e}"
    elif number in (24,28):
        for row,(case,kind,field) in enumerate((case,kind,field) for case in ns['CASES'] for kind in ns['MODELS'] for field in ('u','v')):
            for col,param in enumerate(('Euler','RK4') if number==24 else ('fixed','moving')):
                result=records[case,kind,param,'fixed'] if number==24 else records[case,kind,'RK4',param]
                actual[row,col]=f"{result['max_errors'][field]:.3e}"
    else:
        # pandas unstack sorts the model level alphabetically in this table.
        for row,(case,kind) in enumerate((case,kind) for case in ns['CASES'] for kind in sorted(ns['MODELS'])):
            for col,field in enumerate(('u','v')):
                ratio=records[case,kind,'RK4','moving']['max_errors'][field]/records[case,kind,'RK4','fixed']['max_errors'][field]
                actual[row,col]=f"{ratio:.3f}"
    stored=saved_table(number)
    differences=[dict(row=key[0],column=key[1],saved=value,recomputed=actual.get(key)) for key,value in stored.items() if actual.get(key)!=value]
    comparisons.append(dict(cell=number,numeric_entries=len(stored),mismatches=differences))
checks['saved_tables_against_recomputed']=comparisons
checks['recomputed_winners']=[dict(case=case,field=field,winner=min(ns['MODELS'],key=lambda kind:records[case,kind,'RK4','fixed']['max_errors'][field])) for case in ns['CASES'] for field in ('u','v')]

checks['elapsed_seconds']=time.perf_counter()-started
out=BASE/'numerical_checks.json'
out.write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False,indent=2))
