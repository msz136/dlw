"""Selected 2HS wave parameters x 3 spatial x 4 temporal methods.

Every field run starts from the same continuous soliton sampled on its native grid.
The p values and physical evaluation widths were fixed by WAVE_PARAMETER_SELECTION.md
before reading any result from this scan.
"""
from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from pathlib import Path
from time import perf_counter

import numpy as np
import scipy
from scipy.interpolate import CubicSpline

HERE=Path(__file__).resolve().parent
HS=HERE.parent/'hs_numerics_plan'
sys.path.insert(0,str(HS))
from hs_exact import Soliton
from hs_fixed import FixedSystem
from hs_solver import MovingSystem,solve

OUT=HERE/'out'/'parameter_scan'
OUT.mkdir(parents=True,exist_ok=True)
PARAMETER_SELECTION=json.loads((HERE/'out'/'wave_selection'/'parameters.json').read_text(encoding='utf-8'))
CHOICES={int(r['p']):r for r in PARAMETER_SELECTION['selected']}
HALF_WIDTH={3:11.,5:6.5,12:5.,20:5.}
SPACES=('integrable_moving','ordinary_moving','fixed_difference')
METHODS=('euler','heun','rk4','rk8')
DTS=(.05,.025,.0125,.00625)
REF_DT=.000390625
TIMES=(.05,.10,.25)
A=.02


class RobustSoliton(Soliton):
    """Monotone, bracketed inverse of x(X) for the smooth p>2 branch."""

    def continuous_x(self,x,t,iterations=12):
        x=np.asarray(x,dtype=float)
        if self.p[0] < 18:
            return super().continuous_x(x,t,iterations)
        s=float(-self.omega[0])
        # In the existing tau gauge x=X-<omega>+shift and -<omega>∈[0,s].
        # A monotone lookup locates the steep transition before Newton steps.
        lower=float(np.min(x)-self.shift-s-1.)
        upper=float(np.max(x)-self.shift+1.)
        count=max(1001,int(np.ceil((upper-lower)/.01))+1)
        Xgrid=np.linspace(lower,upper,count)
        _,physical_grid,_=self.continuous_X(Xgrid,t)
        if np.any(np.diff(physical_grid)<=0):
            raise RuntimeError('Nonmonotone smooth-branch hodograph')
        X=np.interp(x,physical_grid,Xgrid)
        for _ in range(10):
            _,physical,rho=self.continuous_X(X,t)
            residual=physical-x
            if np.max(np.abs(residual))<2e-12:
                break
            X=X-residual*rho
        u,physical,rho=self.continuous_X(X,t)
        if np.max(np.abs(physical-x))>1e-10:
            raise RuntimeError('Bracketed hodograph inverse failed')
        return u,rho,X


def reference(p):
    wave=CHOICES[p]
    return RobustSoliton((float(p),),c=1.,phase=(0.,),shift=wave['initial_shift'])


def setup(p,space,half_width=None,a=A):
    ref=reference(p)
    half=HALF_WIDTH[p] if half_width is None else half_width
    edges=int(round(2*half/a))
    if abs(edges*a-2*half)>1e-10:
        raise ValueError('half width must be an integer number of intervals')
    X=np.linspace(-half,half,edges+1)
    if space=='fixed_difference':
        system=FixedSystem(X,1.,ref)
        return ref,system,system.initial(0.),X,edges
    u,x,_=ref.continuous_X(X,0.)
    left=float(X[0])
    b=lambda t:float(ref.continuous_X(np.array([left]),t)[0][0])
    system=MovingSystem(a,1.,edges,b,
                        'sd' if space=='integrable_moving' else 'fd')
    state=system.pack(np.diff(u),np.diff(x),float(x[0]))
    return ref,system,state,X,edges


def evaluate(ref,system,space,p,t,state):
    field=system.fields(t,state)
    x,u,rho=field['x'],field['u'],field['rho']
    u_ref_node,_,_=ref.continuous_x(x,t)
    if space=='fixed_difference':
        rx=x; rho_point=rho
        rho_ref_native=ref.continuous_x(x,t)[1]
        rho_ref_point=rho_ref_native
        spacing=np.diff(x)
    else:
        spacing=field['d']
        rx=.5*(x[:-1]+x[1:])
        rho_ref_native=ref.continuous_density_cell_mean(x[:-1],x[1:],t)
        rho_point=rho-spacing**2*CubicSpline(rx,rho)(rx,2)/24
        rho_ref_point=(rho_ref_native
            -spacing**2*CubicSpline(rx,rho_ref_native)(rx,2)/24)
    su=CubicSpline(x,u)
    sru=CubicSpline(x,u_ref_node)
    sr=CubicSpline(rx,rho_point)
    srr=CubicSpline(rx,rho_ref_point)
    fwhm=CHOICES[p]['u_fwhm']
    windows={'legacy_core':np.linspace(-2,2,801),
             'wave_window':np.linspace(-3*fwhm,3*fwhm,1201)}
    result={'native':{'u_linf':float(np.max(abs(u-u_ref_node))),
                      'rho_linf':float(np.max(abs(rho-rho_ref_native)))},
            'mesh':{'left':float(x[0]),'right':float(x[-1]),
                    'min_spacing':float(np.min(spacing)),
                    'max_spacing':float(np.max(spacing)),
                    'min_rho':float(np.min(rho)),
                    'max_rho':float(np.max(rho))},'windows':{}}
    for name,grid in windows.items():
        if grid[0]<max(x[0],rx[0]) or grid[-1]>min(x[-1],rx[-1]):
            result['windows'][name]={'status':'not covered'}
            continue
        ur,rr,_=ref.continuous_x(grid,t)
        eu=su(grid)-ur; er=sr(grid)-rr
        Au=CHOICES[p]['u_peak'];Ar=1-CHOICES[p]['rho_min']
        result['windows'][name]={
            'u_linf':float(np.max(abs(eu))),'rho_linf':float(np.max(abs(er))),
            'u_l2':float(np.sqrt(np.trapezoid(eu**2,grid)/(grid[-1]-grid[0]))),
            'rho_l2':float(np.sqrt(np.trapezoid(er**2,grid)/(grid[-1]-grid[0]))),
            'u_scaled_linf':float(np.max(abs(eu))/Au),
            'rho_scaled_linf':float(np.max(abs(er))/Ar),
            'joint_scaled_linf':float(max(np.max(abs(eu))/Au,np.max(abs(er))/Ar)),
            'u_reconstruction_floor':float(np.max(abs(sru(grid)-ur))),
            'rho_reconstruction_floor':float(np.max(abs(srr(grid)-rr))),
        }
    return result


def run_one(p,space,method,dt,half_width=None,a=A,outputs=TIMES,
            save_profile=False):
    ref,system,z0,X,edges=setup(p,space,half_width,a)
    tic=perf_counter()
    r=solve(system,z0,0.,max(outputs),dt,method,outputs=(0.,*outputs),strict=False)
    seconds=perf_counter()-tic
    f0=system.fields(0.,z0)
    node_count_half=int(np.sum(np.abs(f0['x'])<=CHOICES[p]['u_fwhm']/2))
    row={'p':p,'space':space,'method':method,'dt':dt,'a_or_dx':a,
         'half_width':HALF_WIDTH[p] if half_width is None else half_width,
         'edges':edges,'initial_x_left':float(f0['x'][0]),
         'initial_x_right':float(f0['x'][-1]),
         'initial_nodes_in_fwhm':node_count_half,
         'status':r.status,'reached':float(r.t[-1]),'seconds':seconds,
         'accepted':r.accepted,'rejected':r.rejected,
         'failure_reason':r.failure_reason,'observations':{}}
    for t,z in zip(r.t[1:],r.states[1:]):
        row['observations'][str(float(t))]=evaluate(ref,system,space,p,float(t),z)
    if save_profile and r.status=='completed':
        f=system.fields(float(r.t[-1]),r.states[-1])
        np.savez_compressed(OUT/f'profile_p{p}_{space}.npz',
                            t=float(r.t[-1]),x=f['x'],u=f['u'],rho=f['rho'])
    return row,(r.states[-1].copy() if r.status=='completed' else None)


def write_partial(out):
    (OUT/'evolution.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def main():
    out={'scope':'p=3,5,12 main and p=20 stress; 3 space x 4 time methods',
         'status':'running','selected_file':'../wave_selection/parameters.json',
         'fixed':{'c':1,'a_or_dx':A,'phase':0,'initial_peak_x':0,
                  'times':TIMES,'dts':DTS,'time_reference_dt':REF_DT,
                  'space_by_p':HALF_WIDTH,
                  'initial':'same continuous exact profile sampled on each native grid',
                  'fixed_boundary':'two exact time-dependent endpoints and ghosts',
                  'moving_boundary':'exact time-dependent left u',
                  'evaluation':'legacy [-2,2] and per-p [-3 FWHM,3 FWHM]'},
         'waves':{str(p):CHOICES[p] for p in (3,5,12,20)},
         'time_references':[],'rows':[],
         'runtime':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__}}
    files=[Path(__file__),HS/'hs_exact.py',HS/'hs_solver.py',HS/'hs_fixed.py',
           HERE/'select_wave_parameters.py']
    out['source_sha256']={str(f.relative_to(HERE.parent)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    for p in (3,5,12,20):
        refs={}
        for space in SPACES:
            print('reference',p,space,flush=True)
            rr,z=run_one(p,space,'rk8',REF_DT)
            out['time_references'].append(rr)
            refs[space]=z
            write_partial(out)
        for space in SPACES:
            for method in METHODS:
                for dt in DTS:
                    print('run',p,space,method,dt,flush=True)
                    row,z=run_one(p,space,method,dt,
                        save_profile=(method=='rk4' and dt==DTS[-1]))
                    if z is not None and refs[space] is not None:
                        row['temporal_state_linf']=float(np.max(abs(z-refs[space])))
                    else:
                        row['temporal_state_linf']=None
                    out['rows'].append(row)
                    write_partial(out)
    out['status']='completed'
    write_partial(out)
    print('completed',len(out['rows']),'runs',flush=True)


if __name__=='__main__':
    main()
