"""Independent audit: scalar inverse reference, SciPy time integration, metrics,
original-paper RHS identity, and a matched-boundary mesh-placement control.
Does not modify the scanned solvers or recorded scan data.
"""
import hashlib,json
from pathlib import Path
import numpy as np
import sympy as sy
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline,PchipInterpolator
from run_parameter_scan import setup,SPACES,CHOICES,HALF_WIDTH,OUT,evaluate
from local_advantage_study import NonuniformMovingSystem

HERE=Path(__file__).resolve().parent
DEST=HERE/'out'/'independent_review'
DEST.mkdir(parents=True,exist_ok=True)
saved=json.loads((OUT/'evolution.json').read_text(encoding='utf-8'))

def independent(p,x,t):
    """Traveling wave inversion using scalar bracketing, no tau/inverse code."""
    s=1-2/p; beta=p-p/(p-1); speed=(1-s*s)/4
    y=np.asarray(x)-speed*t
    th=np.array([brentq(lambda z:z/beta+s/2*np.tanh(z/2)-v,
                       beta*(v-s/2)-1e-10,beta*(v+s/2)+1e-10,
                       xtol=5e-15) for v in y.ravel()]).reshape(y.shape)
    sech2=1/np.cosh(th/2)**2
    u=s*s/4*sech2
    rho=1/(1+s*s/(1-s*s)*sech2)
    # theta=beta X-s t, hence X=(theta+s t)/beta.
    return u,rho,(th+s*t)/beta

# Algebra against original paper (81), not just the already simplified RHS.
a,c,d,v,u0=sy.symbols('a c d v u0')
u1=u0+v
B=v+(d-a)*(c-a-d)
original=-v*B/d+B**2/(2*d)+4*u1*d-c*B-v*(2*d-c)
simplified=2*d*(u1+u0)+((d*d-a*(a-c))**2-v*v)/(2*d)-c*c*d/2
paper_residual=sy.factor(original-simplified)
assert paper_residual==0

rows=[];placement=[]
for p in (3,5,12,20):
    for space in SPACES:
        print('audit',p,space,flush=True)
        ref,sys,z0,X,n=setup(p,space)
        f0=sys.fields(0,z0)
        ue,re,xe=independent(p,f0['x'],0)
        init_u=float(np.max(abs(f0['u']-ue)))
        if space=='fixed_difference':
            init_rho=float(np.max(abs(f0['rho']-re)))
        else:
            init_rho=float(np.max(abs(f0['rho']-np.diff(xe)/np.diff(f0['x']))))
        sol=solve_ivp(sys.rhs,(0,.25),z0,method='DOP853',rtol=2e-12,atol=2e-14,
                      max_step=.00625,t_eval=[.25])
        assert sol.success
        f=sys.fields(.25,sol.y[:,-1])
        x=f['x']; rx=x if space=='fixed_difference' else (x[:-1]+x[1:])/2
        rho=f['rho']
        rp=rho if space=='fixed_difference' else rho-np.diff(x)**2*CubicSpline(rx,rho)(rx,2)/24
        old=next(r for r in saved['rows'] if (r['p'],r['space'],r['method'],r['dt'])==(p,space,'rk4',.00625))
        obs=old['observations']['0.25']['windows']['wave_window']
        L=3*CHOICES[p]['u_fwhm'];grids={}
        for ng in (1201,9601):
            xx=np.linspace(-L,L,ng)
            ur,rr,_=independent(p,xx,.25)
            un=CubicSpline(x,f['u'])(xx);rn=CubicSpline(rx,rp)(xx)
            eu=un-ur;er=rn-rr
            iu=int(np.argmax(abs(eu)));ir=int(np.argmax(abs(er)))
            grids[str(ng)]={'u_linf':float(max(abs(eu))),'rho_linf':float(max(abs(er))),
                'u_max_location':float(xx[iu]),'rho_max_location':float(xx[ir]),
                'u_at_max_error_exact':float(ur[iu]),
                'u_signed_error':float(eu[iu]),
                'u_pchip_linf':float(max(abs(PchipInterpolator(x,f['u'])(xx)-ur))),
                'rho_pchip_linf':float(max(abs(PchipInterpolator(rx,rp)(xx)-rr))),
                'u_scaled_linf':float(max(abs(eu))/CHOICES[p]['u_peak']),
                'rho_scaled_linf':float(max(abs(er))/(1-CHOICES[p]['rho_min']))}
        ur,rr,xr=independent(p,x,.25)
        if space=='fixed_difference':
            rnative=rr
        else:
            rnative=np.diff(xr)/np.diff(x)
        oldprofile=np.load(OUT/f'profile_p{p}_{space}.npz')
        rows.append(dict(p=p,space=space,init_u=init_u,init_rho_native=init_rho,
            integrator_nfev=sol.nfev,
            saved_profile_difference={k:float(max(abs(f[k]-oldprofile[k]))) for k in ('u','rho','x')},
            independent_native_u=float(max(abs(f['u']-ur))),
            independent_native_rho=float(max(abs(rho-rnative))),
            saved_metrics={k:obs[k] for k in ('u_linf','rho_linf')},metrics=grids,
            left_u_error=float(f['u'][0]-ur[0]),right_u_error=float(f['u'][-1]-ur[-1]),
            exact_inverse_difference=float(max(abs(ref.continuous_x(x,.25)[1]-rr)))))

    # Same moving method and identical endpoint labels; only initial node allocation changes.
    print('matched-placement',p,flush=True)
    ref,sys,z0,X,n=setup(p,'ordinary_moving')
    f0=sys.fields(0,z0)
    xx=np.linspace(f0['x'][0],f0['x'][-1],n+1)
    u0,r0,X0=independent(p,xx,0)
    mass=np.diff(X0)
    alt=NonuniformMovingSystem(mass,1,sys.left_u)
    state=alt.pack(np.diff(u0),np.diff(xx),xx[0])
    sol=solve_ivp(alt.rhs,(0,.25),state,method='DOP853',rtol=2e-12,atol=2e-14,
                  max_step=.00625,t_eval=[.25])
    assert sol.success
    metrics=evaluate(ref,alt,'ordinary_moving',p,.25,sol.y[:,-1])
    base=next(r for r in rows if r['p']==p and r['space']=='ordinary_moving')['metrics']['9601']
    altm=metrics['windows']['wave_window']
    placement.append(dict(p=p,definition='initial uniform physical nodes, then same x_t=-u; not fixed-grid evolution',
        endpoint_label_difference=float(max(abs(X0[[0,-1]]-X[[0,-1]]))),
        natural_mass=base,uniform_initial_physical=altm,
        ratio_uniform_to_natural={k:altm[k]/base[k] for k in ('u_linf','rho_linf')}))

out=dict(scope='audit only; original solver and scan files untouched',
    paper81_simplification_residual=str(paper_residual),rows=rows,
    matched_placement_controls=placement,
    hashes={str(f.relative_to(HERE)):hashlib.sha256(f.read_bytes()).hexdigest()
            for f in (Path(__file__),HERE/'run_parameter_scan.py',OUT/'evolution.json',
                      OUT/'spatial_controls.json',OUT/'domain_controls.json',OUT/'integrable_lattice_check.json')})
(DEST/'audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
for r in rows:
    m=r['metrics']['9601']
    print(r['p'],r['space'],'u/rho',m['u_linf'],m['rho_linf'],'u max x',m['u_max_location'])
print('PLACEMENT',json.dumps([{ 'p':r['p'],**r['ratio_uniform_to_natural']} for r in placement]))
