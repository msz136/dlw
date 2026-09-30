"""Route 1: long-distance sampling geometry, deliberately separate from PDE solves."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'lib'),str(ROOT/'experiments')]
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import brentq
from moving_mesh import gram_mesh
from moving_mesh_study import ALL,OUT,inf
from parametric import Exact


def exact_ux(exact,js,x,t):
    z=exact.S*np.asarray(x)[None,:]+exact.omega*t
    z=z+np.log(exact.pars.rho/exact.S)+np.asarray(js)[:,None]*exact.chi
    def deriv(v):
        a=np.exp(-np.logaddexp(0,-v))
        return a*(1-a)
    return exact.S**2*(2*deriv(z+exact.gamma)-deriv(z)-deriv(z+exact.chi))


def equidistribute(xfine,monitor,xi):
    cell=.5*(monitor[1:]+monitor[:-1])*np.diff(xfine)
    cumulative=np.r_[0,np.cumsum(cell)]
    target=np.arange(len(xi))*cumulative[-1]/len(xi)
    grid=np.interp(target,cumulative,xfine)
    grid[0]=xfine[0]
    return grid


def width(exact):
    x=np.linspace(-6,6,24001)
    u=abs(exact.uv([0],x,0)[0][0]);mask=u>=.5*np.max(u)
    return float(x[mask][-1]-x[mask][0])


def representation(exact,js,x,t,target_x):
    u,v=exact.uv(js,x,t)
    ut,vt=exact.uv(js,target_x,t)
    return {'u':inf(CubicSpline(x,u,axis=1,bc_type='natural')(target_x)-ut),
            'v':inf(CubicSpline(x,v,axis=1,bc_type='natural')(target_x)-vt)}


def main():
    cases=(0,1,6,9)
    xi=-10+np.arange(128)*20/128
    xfine=np.linspace(-10,10,12001)
    target_x=np.linspace(-8,8,1601)
    data={'scope':{'kind':'exact-field sampling geometry, no field evolution',
                   'cases':[f'P{i+1}' for i in cases],
                   'D_targets':[0,.25,.5,1,2],
                   'intermittent_refresh_interval':.25,
                   'x_points':128,'eval_interval':[-8,8],
                   'gradient_monitor':'1+alpha*GaussianSmooth(mean_j |u_x|), alpha matched to Gram minimum spacing at t=0'},
          'cases':[]}
    for index in cases:
        pars=ALL[index];pid=f'P{index+1}'
        exact=Exact(pars,.125)
        js=np.arange(-12,12)
        ell=width(exact);speed=abs(pars.p-pars.q)
        u0=exact.uv([0],xfine,0)[0][0]
        center0=float(xfine[np.argmax(abs(u0))])
        if speed==0:continue
        initial=gram_mesh(pars,.125,js,xi,0.)
        min_gram=np.min(np.diff(np.r_[initial,10.]))
        def grad_grid(t,alpha):
            grad=np.mean(abs(exact_ux(exact,js,xfine,t)),axis=0)
            grad=gaussian_filter1d(grad,0.08/(xfine[1]-xfine[0]))
            return equidistribute(xfine,1+alpha*grad,xi)
        def min_spacing(alpha):
            x=grad_grid(0,alpha)
            return np.min(np.diff(np.r_[x,10.]))
        alpha=brentq(lambda a:min_spacing(a)-min_gram,0,1e5)
        rows=[]
        for D in data['scope']['D_targets']:
            t=D*ell/speed
            last_refresh=np.floor((t+1e-12)/.25)*.25
            grids={'uniform':xi,'frozen_gram':initial,
                   'moving_gram_oracle':gram_mesh(pars,.125,js,xi,t),
                   'intermittent_gram_oracle':gram_mesh(pars,.125,js,xi,last_refresh),
                   'moving_gradient_oracle':grad_grid(t,alpha)}
            metrics={}
            for name,x in grids.items():
                spacing=np.diff(np.r_[x,10.])
                shape=representation(exact,js,x,t,target_x)
                metrics[name]={**shape,'min_dx':float(np.min(spacing)),
                               'max_dx':float(np.max(spacing)),
                               'node_count_near_pulse':int(np.sum(abs(x-(center0+(pars.p-pars.q)*t))<=ell/2))}
            rows.append({'D':D,'t':t,'last_refresh':last_refresh,'metrics':metrics})
        data['cases'].append({'parameter_id':pid,'pars':pars.__dict__,
                              'width':ell,'speed':speed,'gradient_alpha':alpha,
                              'initial_pulse_center':center0,
                              'initial_min_dx_gram':min_gram,
                              'initial_min_dx_gradient':min_spacing(alpha),
                              'rows':rows})
        print(pid,'width',ell,'alpha',alpha,flush=True)
    paths=[Path(__file__),ROOT/'lib/moving_mesh.py']
    data['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in paths}
    (OUT/'route1_geometry.json').write_text(json.dumps(data,indent=2,allow_nan=False),encoding='utf-8')


if __name__=='__main__':main()
