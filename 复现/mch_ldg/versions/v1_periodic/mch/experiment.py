import json, time, hashlib, platform
from pathlib import Path
from datetime import datetime
import numpy as np
from numpy.polynomial.legendre import leggauss,legvander
from .ldg import LDG
from .exact import profile,breakpoints


def errors(solver,u,config,t):
    # Exact derivative has jumps: split error quadrature at their actual positions.
    z,w=leggauss(max(16,2*solver.k+4))
    cuts=breakpoints(config['case'],solver.left,solver.right,t,config.get('c',1))
    totals=np.zeros(2); linf=0.
    r=solver.deriv_minus(u)
    for j,center in enumerate(solver.centers):
        a,b=center-solver.h/2,center+solver.h/2
        bounds=[a]+sorted(p for p in cuts if a+1e-12<p<b-1e-12)+[b]
        for lo,hi in zip(bounds[:-1],bounds[1:]):
            xx=(lo+hi)/2+(hi-lo)/2*z
            V=legvander((xx-center)*2/solver.h,solver.k)
            ue,re=profile(config['case'],xx,t,alpha=config.get('alpha',.5),kappa=config['kappa'],c=config.get('c',1))
            eu=V@u[j]-ue; er=V@r[j]-re
            totals+=(hi-lo)/2*np.array([w@(eu*eu),w@(er*er)])
            linf=max(linf,float(np.max(np.abs(eu))))
    return dict(l2_u=float(np.sqrt(totals[0])),l2_r=float(np.sqrt(totals[1])),energy_error=float(np.sqrt(totals.sum())),sampled_linf_u=linf)


def run(config,base='results'):
    config=dict(config)
    start=time.perf_counter()
    solver=LDG(**{key:config[key] for key in ('n','k','left','right','kappa','flux')})
    fun=lambda x: profile(config['case'],x,0,alpha=config.get('alpha',.5),kappa=config['kappa'],c=config.get('c',1))[0]
    u=solver.project(fun,config.get('projection','radau'),breakpoints(config['case'],solver.left,solver.right))
    tag=f"ex{config['case']}_{config['flux']}_P{config['k']}_N{config['n']}"
    out=Path(base)/(datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'_'+tag)
    out.mkdir(parents=True,exist_ok=False)
    config['boundary']='periodic'  # deliberate first-version baseline
    config['boundary_alignment']='paper' if config['case']=='5.5' else 'periodic_truncation_approximation'
    config['quadrature_points']=len(solver.z)
    config['time_state']='u; Helmholtz solve for u_t at every RK4 stage'
    (out/'config.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
    times=[]; states=[]; history=[]; steps=0; t=0.; failed=None
    E0=solver.energy(u); mass0=solver.mass_integral(u)
    targets=np.unique(np.r_[np.linspace(0,config['T'],config.get('outputs',21)),config.get('snapshots',[])])
    def save():
        row=dict(t=float(t),energy=solver.energy(u),energy_loss=E0-solver.energy(u),mass=solver.mass_integral(u),mass_drift=solver.mass_integral(u)-mass0,
                 semidiscrete_energy_rate=solver.energy_rate(u),predicted_energy_rate=solver.predicted_energy_rate(u))
        row.update(errors(solver,u,config,t)); history.append(row)
        times.append(t); states.append(u.copy())
    save()
    try:
        with np.errstate(over='raise',invalid='raise',divide='raise'):
            for target in targets[1:]:
                while t<target-1e-13:
                    dt=min(config['dt'],target-t)
                    k1=solver.rhs(u);k2=solver.rhs(u+.5*dt*k1)
                    k3=solver.rhs(u+.5*dt*k2);k4=solver.rhs(u+dt*k3)
                    u=u+dt/6*(k1+2*k2+2*k3+k4);t+=dt;steps+=1
                    if not np.all(np.isfinite(u)): raise FloatingPointError('nonfinite state')
                save()
    except (FloatingPointError,ValueError) as exc:
        failed=str(exc)
    np.savez_compressed(out/'trajectory.npz',t=np.array(times),u=np.array(states),centers=solver.centers,last_state=u,last_time=t)
    summary=dict(completed=failed is None,reached=float(t),failure=failed,steps=steps,wall_seconds=time.perf_counter()-start,
                 initial=history[0],final=history[-1],config=config,python=platform.python_version(),numpy=np.__version__,
                 source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')})
    (out/'history.json').write_text(json.dumps(history,indent=2),encoding='utf-8')
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(dict(path=str(out),case=config['case'],flux=config['flux'],n=config['n'],k=config['k'],completed=summary['completed'],error=history[-1]['energy_error'],loss=history[-1]['energy_loss'],seconds=summary['wall_seconds']),ensure_ascii=True),flush=True)
    return str(out),summary
