"""Open-chain zero-background modal growth; not a nonlinear stability bound."""
import sys, json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
from solver import XGrid, Chain, DLWChainRHS, integrate
from linearized import effective_k, open_block, spectral_max


def sigma_roots(k,l,h,a=4.):
    K=2/h*np.sin(l*h/2); C=np.cos(l*h/2)
    r=np.sqrt(complex(k**4+4*k**3*C/K-h*h*k*k))
    return -2j*a*k+r, -2j*a*k-r


def eigenmode_check(nx=64, seed=1e-6, steps=64):
    """Check the Jacobian against the nonlinear RHS, then evolve +/- an
    eigenmode and project its Fourier amplitude onto its initial eigenvector.
    Central odd differences cancel quadratic nonlinearity at t=0.
    """
    L,h,jL,jR=60.,.25,-12,12
    X=XGrid(nx,L,4); C=Chain(jL,jR,h,4.)
    rhs=DLWChainRHS(C,X,b_fun=lambda t:np.zeros(nx),
                    ghost_left=lambda t:np.zeros(nx),ghost_right=lambda t:np.zeros(nx))
    rhs.use_ext=True; rhs._ple=0.; rhs._pre=0.
    mode=nx//8; theta=2*np.pi*mode/L; k=effective_k(theta,X.dx)
    B=open_block(k,jL,jR,h)
    vals,vecs=np.linalg.eig(B); idx=int(np.argmax(vals.real)); lam=vals[idx]
    q=vecs[:,idx]; q=q/np.max(abs(q))
    def amplitude(z): return np.vdot(q,z)/np.vdot(q,q)
    wave=np.exp(1j*theta*(X.x-X.x[0]))
    base=np.real(q[:,None]*wave)
    nP=C.nj-1
    def call(z):
        p,w=rhs(0,z[:nP],z[nP:]);return np.concatenate((p,w))
    actual=(call(seed*base)-call(-seed*base))/(2*seed)
    predicted=np.real((B@q)[:,None]*wave)
    jacerr=float(np.max(abs(actual-predicted)))
    rng=np.random.default_rng(20260922)
    probe=rng.normal(size=len(q))+1j*rng.normal(size=len(q))
    direction=np.real(probe[:,None]*wave)
    jacerr=max(jacerr,float(np.max(abs(
        (call(seed*direction)-call(-seed*direction))/(2*seed)
        -np.real((B@probe)[:,None]*wave)))))
    T=.05/max(1.,lam.real); states=[]
    for sign in [1,-1]:
        z=sign*seed*base
        p,w,info=integrate(rhs,0,T,z[:nP],z[nP:],T/steps,method='rk4')
        assert info['stopped'] is None and abs(info['final_t']-T)<1e-12
        assert np.isfinite(p).all() and np.isfinite(w).all()
        states.append(np.concatenate((p,w)))
    z=(states[0]-states[1])/(2*seed)
    coeff=2*np.mean(z*wave.conj(),axis=1)
    initial=2*np.mean(base*wave.conj(),axis=1)
    ratio=amplitude(coeff)/amplitude(initial)
    measured=float(np.log(abs(ratio))/T)
    rel=float(abs(measured-lam.real)/max(1,abs(lam.real)))
    shape_error=float(np.max(abs(coeff-np.exp(lam*T)*initial)))
    assert jacerr<1e-8, jacerr
    assert rel<1e-5, rel
    assert shape_error<1e-7, shape_error
    return {'nx':nx,'mode':mode,'seed':seed,'steps':steps,'T_end':float(T),
            'k_pert_eff':float(k),'g_predicted':float(lam.real),
            'g_measured':measured,'relative_error':rel,'jacobian_error':jacerr,
            'eigen_residual':float(np.max(abs(B@q-lam*q))), 'mode_shape_error':shape_error,
            'finite':True,'background':'zero','boundary':'fixed zero base, ghosts, outer P',
            'observable':'projection onto initial right eigenvector; full mode shape also checked'}


def main():
    h=.25;l=2.;res={'experiment':'E6','a':4.,
       'spectrum_scope':'zero background; fixed zero perturbations of base, ghosts and outer P; j=-12..12',
       'budget_interpretation':'single-eigenmode amplification time only; not a nonlinear or nonnormal norm bound'}
    res['branch_table']=[]
    for k in [1,2,5,10,20,50,100,200,500,1000]:
        g,_=sigma_roots(k,l,h)
        res['branch_table'].append({'k':k,'Re_growing':g.real,'Re_over_k2':g.real/k**2,'Im_growing':g.imag})
    grids=[]
    for nx in [64,128,256,512,1024,2048]:
        s=spectral_max(nx,60,h)
        gc,_=sigma_roots(np.pi/(60/nx),l,h)
        grids.append({'nx':nx,'L':60.,'dx':60/nx,**s,'g_max_continuous_nyq':float(gc.real)})
        print('open-chain spectrum',grids[-1],flush=True)
    res['grid_gmax']=grids
    res['spectral_caveat']='Float64 eigenvalues of a nonnormal matrix are estimates; short-time eigenmode checks do not certify the full spectrum.'
    res['grid_budget']=[{**r,'T_budget':float(np.log(1e6)/r['g_max_discrete'])} for r in grids]
    res['linear_norm_times']=[{'nx':r['nx'], 'mu':r['linear_log_norm'],
        'T_sufficient':float(np.log(1e6)/r['linear_log_norm'])} for r in grids]
    X=XGrid(256,60,4); v=(-1.)**np.arange(256)
    res['nyquist_check']={'D1_action':float(max(abs(X.D1@v))),'D2_action':float(max(abs(X.D2@v)))}
    res['solver_growth']=[eigenmode_check(nx,seed,steps) for nx in [64,128]
                          for seed,steps in [(1e-6,32),(5e-7,64)]]
    print(json.dumps(res['solver_growth'],indent=2))
    (ROOT/'out/e6_growth.json').write_text(json.dumps(res,indent=2),encoding='utf-8')


if __name__=='__main__': main()
