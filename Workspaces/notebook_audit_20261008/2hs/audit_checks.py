import contextlib
import io
import json
from pathlib import Path

import numpy as np

ROOT = Path(r'C:\Users\msz\aca')
NOTEBOOK = ROOT / 'notebook' / '2HS数值分析report.ipynb'
OUT = Path(__file__).parent
nb = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
env = {'__name__': '__audit__'}
for number in (2, 4, 6, 8, 10, 12, 14, 16, 19, 22):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(''.join(nb['cells'][number-1]['source']), f'cell_{number}', 'exec'), env)
one_x, one_physical = env['hs_exact_X'], env['hs_exact_physical']
two_x, two_physical = env['hs_two_exact_X'], env['hs_two_exact_physical']
evidence = {}

def configure(n, kind, T=0.5, dt=0.003125):
    env.update(hs_N=n, hs_a=12/n, hs_Xleft=-6.0, hs_Xright=6.0,
               hs_T=T, hs_dt=dt, hs_steps=round(T/dt))
    env['hs_exact_X'] = one_x if kind == 'one' else two_x
    env['hs_exact_physical'] = one_physical if kind == 'one' else two_physical
    initial = env['hs_exact_X'](np.linspace(-6, 6, n+1), 0)
    left, right = initial['x'][[0, -1]]
    env.update(hs_initial=initial, hs_left=left, hs_right=right,
               hs_dx=(right-left)/n, hs_fixed_x=np.linspace(left, right, n+1))

def physical(x, t, kind):
    # The one-soliton inversion resolves its exact_X from this globals dict.
    env['hs_exact_X'] = one_x if kind == 'one' else two_x
    return (one_physical if kind == 'one' else two_physical)(x, t)

def derivative(values, h):
    return (values[0]-8*values[1]+8*values[3]-values[4])/(12*h)

def second(values, h):
    return (-values[0]+16*values[1]-30*values[2]+16*values[3]-values[4])/(12*h*h)

evidence['analytic_PDE_checks'] = []
for kind in ('one', 'two'):
    x = np.linspace(-2, 2, 101)
    t, h = .23, 1e-4
    fx = [physical(x+j*h, t, kind) for j in (-2,-1,0,1,2)]
    ft = [physical(x, t+j*h, kind) for j in (-2,-1,0,1,2)]
    u_x = derivative([f['u'] for f in fx], h)
    u_xx = second([f['u'] for f in fx], h)
    utx_parts = []
    for j in (-2,-1,0,1,2):
        space_at_time = [physical(x+k*h, t+j*h, kind)['u'] for k in (-2,-1,0,1,2)]
        utx_parts.append(derivative(space_at_time, h))
    u_tx = derivative(utx_parts, h)
    u, rho = fx[2]['u'], fx[2]['rho']
    R_u = u_tx-u*u_xx-.5*u_x*u_x-4*u-.5*(rho*rho-1)
    R_rho = derivative([f['rho'] for f in ft], h)-derivative([f['u']*f['rho'] for f in fx], h)
    evidence['analytic_PDE_checks'].append(dict(case=kind, h=h,
        max_first_equation_residual=float(abs(R_u).max()),
        max_density_equation_residual=float(abs(R_rho).max()),
        max_m_chain_rule_error=float(abs(fx[2]['m']-(u_xx+2)).max())))

# Independent dense Poisson solve versus Thomas recovery, with arbitrary state.
configure(40, 'one')
rng = np.random.default_rng(14)
m = 2+rng.normal(size=41)
left, right = -.013, .027
actual = env['hs_recover_u'](m, left, right)
matrix = np.diag(np.full(39,-2.0))+np.diag(np.ones(38),1)+np.diag(np.ones(38),-1)
rhs = env['hs_dx']**2*(m[1:-1]-2)
rhs[0] -= left
rhs[-1] -= right
expected = np.r_[left,np.linalg.solve(matrix,rhs),right]
evidence['Thomas_vs_dense'] = {'max_error':float(abs(actual-expected).max())}

# Independent RK4 polynomial against y'=2*y, including time-dependent RHS stages.
rk = env['hs_rk4_step']
step = .125
actual = rk(lambda t,y: 2*y, 0.0, np.array([1.0]), step)[0]
z=2*step
expected = 1+z+z*z/2+z**3/6+z**4/24
actual_time = rk(lambda t,y: np.array([4*t**3]), .3, np.array([.3**4]), .2)[0]
evidence['RK4_checks'] = {'linear_polynomial_error':float(abs(actual-expected)),
                         'cubic_time_rhs_error':float(abs(actual_time-.5**4))}

# Broad-domain and reported-domain integrable error versus resolution.
evidence['integrable_refinement'] = []
for kind in ('one', 'two'):
    for n in (300,600,1200,2400,4800):
        configure(n,kind)
        state, _ = env['hs_initial_states']()
        initial_rhs = env['hs_integrable_rhs'](0,state)
        tail = env['hs_integrable_fields'](0,state)
        bg_state = np.r_[np.zeros(n), np.full(n,env['hs_a']), 0.0]
        # Zero background u requires zero left-boundary value.
        original_exact = env['hs_exact_X']
        env['hs_exact_X'] = lambda X,t: {'u':0.0}
        background_rhs = env['hs_integrable_rhs'](0,bg_state)
        env['hs_exact_X'] = original_exact
        for i in range(env['hs_steps']):
            state = rk(env['hs_integrable_rhs'], i*env['hs_dt'],state,env['hs_dt'])
        numerical = env['hs_integrable_fields'](.5,state)
        row = dict(case=kind,N=n,a=env['hs_a'],background_RHS_max=float(abs(background_rhs).max()))
        for label,extent in (('reported',(-1,1)),('wide',(-5,5))):
            xx=np.linspace(*extent,32001)
            exact=physical(xx,.5,kind)
            uu=env['hs_interpolate'](numerical['x'],numerical['u'],xx)
            rr=env['hs_interpolate'](numerical['rhoX'],numerical['rho'],xx)
            row[label+'_Eu']=float(abs(uu-exact['u']).max())
            row[label+'_Erho']=float(abs(rr-exact['rho']).max())
            row[label+'_u_at_right']=float(uu[-1])
            row[label+'_rho_at_right']=float(rr[-1])
        evidence['integrable_refinement'].append(row)
        print(json.dumps(row,ensure_ascii=False),flush=True)

evidence['initial_consistency_one'] = []
for n in (300,600,1200,2400,4800):
    configure(n,'one')
    state,_ = env['hs_initial_states']()
    rhs = env['hs_integrable_rhs'](0,state)
    X=np.linspace(-6,6,n+1)
    z=np.tanh(3.75*X/2)
    u_t=.054*z*(1-z*z)
    error=rhs[:n]-np.diff(u_t)
    midpoint=(X[:-1]+X[1:])/2
    z_mid=np.tanh(3.75*midpoint/2)
    J=1+.5625*(1-z_mid*z_mid)
    leading=env['hs_a']**2*(J*J-1)/J
    row=dict(N=n,a=env['hs_a'],max_db_residual=float(abs(error).max()),
             max_db_residual_over_a2=float(abs(error).max()/env['hs_a']**2),
             leading_expansion_mismatch=float(abs(error-leading).max()/env['hs_a']**2),
             cumulative_du_dt_residual_at_right=float(np.sum(error)))
    evidence['initial_consistency_one'].append(row)

# Default FD outputs independently recomputed without invoking plotting cells.
evidence['fd_default_recomputation'] = []
for kind in ('one','two'):
    configure(2400,kind)
    _,state=env['hs_initial_states']()
    for i in range(env['hs_steps']):
        state=rk(env['hs_fd_rhs'],i*env['hs_dt'],state,env['hs_dt'])
    fields=env['hs_fd_fields'](.5,state)
    xx=np.linspace(-1,1,32001)
    exact=physical(xx,.5,kind)
    uu=env['hs_interpolate'](fields['x'],fields['u'],xx)
    rr=env['hs_interpolate'](fields['rhoX'],fields['rho'],xx)
    row=dict(case=kind,N=2400,Eu=float(abs(uu-exact['u']).max()),Erho=float(abs(rr-exact['rho']).max()))
    evidence['fd_default_recomputation'].append(row)
    print(json.dumps(row),flush=True)

OUT.joinpath('evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
print('Evidence saved:',OUT / 'evidence.json')
