import contextlib
import io
import json
from pathlib import Path
import numpy as np

ROOT=Path(r'C:\Users\msz\aca')
OUT=Path(__file__).parent
nb=json.loads((ROOT/'notebook'/'2HS数值分析report.ipynb').read_text(encoding='utf8'))
env={'__name__':'__audit__'}
for i in (2,4,6,8,10,12,14,16,19,22,33):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(''.join(nb['cells'][i-1]['source']),f'cell_{i}','exec'),env)
one_x,one_phys=env['hs_exact_X'],env['hs_exact_physical']
two_x,two_phys=env['hs_two_exact_X'],env['hs_two_exact_physical']

def configure(kind,n=2400,T=.5,dt=.003125):
    env.update(hs_N=n,hs_a=12/n,hs_T=T,hs_dt=dt,hs_steps=round(T/dt))
    env['hs_exact_X']=one_x if kind=='one' else two_x
    env['hs_exact_physical']=one_phys if kind=='one' else two_phys
    initial=env['hs_exact_X'](np.linspace(-6,6,n+1),0)
    left,right=initial['x'][[0,-1]]
    env.update(hs_initial=initial,hs_left=left,hs_right=right,
               hs_dx=(right-left)/n,hs_fixed_x=np.linspace(left,right,n+1))

evidence=json.loads((OUT/'evidence.json').read_text(encoding='utf8'))
evidence['integrable_time_refinement']=[]
for case in ('one','two'):
    base=None
    for dt in (.003125,.0015625,.00078125):
        configure(case,dt=dt)
        state,_=env['hs_initial_states']()
        for i in range(env['hs_steps']):
            state=env['hs_rk4_step'](env['hs_integrable_rhs'],i*dt,state,dt)
        f=env['hs_integrable_fields'](.5,state)
        xx=np.linspace(-5,5,32001)
        exact=env['hs_exact_physical'](xx,.5)
        u=env['hs_interpolate'](f['x'],f['u'],xx)
        rho=env['hs_interpolate'](f['rhoX'],f['rho'],xx)
        if base is None:
            base=(u.copy(),rho.copy())
        row=dict(case=case,N=2400,dt=dt,Eu=float(abs(u-exact['u']).max()),
                 Erho=float(abs(rho-exact['rho']).max()),
                 max_u_difference_to_default=float(abs(u-base[0]).max()),
                 max_rho_difference_to_default=float(abs(rho-base[1]).max()))
        print(json.dumps(row),flush=True)
        evidence['integrable_time_refinement'].append(row)

evidence['fd_domain_comparison']=[]
for case in ('one','two'):
    configure(case)
    _,state=env['hs_initial_states']()
    for i in range(env['hs_steps']):
        state=env['hs_rk4_step'](env['hs_fd_rhs'],i*env['hs_dt'],state,env['hs_dt'])
    f=env['hs_fd_fields'](.5,state)
    row=dict(case=case,N=2400,dt=.003125)
    for label,window in (('reported',(-1,1)),('wide',(-5,5))):
        xx=np.linspace(*window,32001)
        exact=env['hs_exact_physical'](xx,.5)
        u=env['hs_interpolate'](f['x'],f['u'],xx)
        rho=env['hs_interpolate'](f['rhoX'],f['rho'],xx)
        row[label+'_Eu']=float(abs(u-exact['u']).max())
        row[label+'_Erho']=float(abs(rho-exact['rho']).max())
    print(json.dumps(row),flush=True)
    evidence['fd_domain_comparison'].append(row)

# Demonstrate labels/reference when just the one-soliton solve cell is rerun
# after the sequential two-soliton section has changed the global case.
configure('two',n=40,T=.0125)
for i in (16,17):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(''.join(nb['cells'][i-1]['source']),env)
xx=np.linspace(-1,1,101)
rerun_reference=env['hs_histories']['one']['reference'](xx,0)
direct_two=two_phys(xx,0)
env['hs_exact_X']=one_x
direct_one=one_phys(xx,0)
evidence['rerun_single_cell_after_two']={
    'max_reference_vs_two_u':float(abs(rerun_reference['u']-direct_two['u']).max()),
    'max_reference_vs_one_u':float(abs(rerun_reference['u']-direct_one['u']).max()),
    'history_label':'one',
}

# T=0 passes the stated CONFIG guard, but plotting unconditionally rejects it.
configure('one',n=40,T=0)
for i in (16,17,32):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(''.join(nb['cells'][i-1]['source']),env)
try:
    env['checked_window'](env['PLOT_CONFIG']['tlim'],(0.0,0.0),'tlim')
except ValueError as exc:
    evidence['T_zero_plotting']={'config_time':0.0,'error':str(exc),
                                'record_count':len(env['hs_histories']['one']['records'])}
(OUT/'evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf8')
