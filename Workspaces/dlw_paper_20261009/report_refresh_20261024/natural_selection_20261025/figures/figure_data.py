"""Physical data API for the selected three-method numerical figures.

Arrays are y-by-x. All interpolated sections use physical numerical fields
without adding or subtracting an exact-solution correction.
"""
from pathlib import Path
from functools import lru_cache
from types import SimpleNamespace
import importlib.util
import sys
import numpy as np

HERE=Path(__file__).resolve().parent
DATA=HERE/'data'
SELECTION=HERE.parent
BASE=SELECTION.parent
PROJECT=BASE.parent
ROOT=BASE.parents[2]
PROBE=PROJECT/'spatial_audit_20261023/separated/reconstruction_probe'
sys.path.insert(0,str(PROBE))
from probe import Model,fields,HALF_WIDTHS,transform
from rerun_20261024 import rhs,physical_rates
spec=importlib.util.spec_from_file_location('figure_nondegenerate_runner',BASE/'nondegenerate_rk4_20261024/run.py')
reference=importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
sys.path.insert(0,str(BASE/'nondegenerate_rk4_20261024'))
import reference_grid as continuous

CASES=['A','B','C','D','Gaussian','Sinusoidal']
METHODS={'endpoint':'Endpoint-SD','centered':'Centered-SD','fd':'FD'}

@lru_cache(maxsize=6)
def model(case):
    return Model(case,'FD',.1,.1) if case in ('A','B','C','D') else reference.NondegenerateModel(case,'FD')

def display_limits(case):
    if case in ('A','B','C','D'):
        r=HALF_WIDTHS[case];return (-r,r),(-r,r)
    return (-24.,24.),(-1.8,1.8)

def _direct_values(polys,polyst,w,C,s,X):
    """Evaluate finite Laurent polynomials at arbitrary x, with time jets."""
    center=(polys.shape[1]-1)//2
    n=np.arange(-center,center+1);d=1j*w*n-s*C
    qt=polyst.copy()
    qt[0]-=4*d*polys[0]
    qt[1]+=-4*d*polys[1]+4*C*polys[0]
    qt[2]+=-4*d*polys[2]+8*C*polys[1]
    z=np.exp(1j*w*X);phase=np.exp(-1j*w*center*X)
    a=-C*X;factor=np.exp(-s*C*X)
    result=[]
    for qq in (polys,qt):
        raw=[]
        for q in qq:
            raw.extend([(np.polynomial.polynomial.polyval(z,q)*phase).real,
                        (np.polynomial.polynomial.polyval(z,d*q)*phase).real])
        q,qx,qs,qsx,qss,qssx=raw
        result.append(factor*np.asarray([q,qx,qs+a*q,qsx+a*qx-C*q,
            qss+2*a*qs+a*a*q,qssx+2*a*qsx+a*a*qx-2*C*(qs+a*q)]))
    return result

def _direct_row(case,x,y,t):
    name='gaussian' if case=='Gaussian' else 'sine'
    A,w,C,K,multiple=continuous._parameters(name)
    s,sz,H,Ht,P,Pt,F=continuous._coefficients(name,float(y),float(t))
    X=x-4*t
    p,pt=_direct_values(P,Pt,w,C,s,X)
    h,ht=_direct_values(H,Ht,w,C,s,X)
    p,px,ps,psx,pss,pssx=list(zip(p,pt))
    h,hx,hs,hsx,hss,hssx=list(zip(h,ht))
    mul,sub,div=continuous._mul,continuous._sub,continuous._div
    D=sub(mul(p,hs),mul(h,ps));Dx=sub(mul(p,hsx),mul(hx,ps))
    Ds=sub(mul(p,hss),mul(h,pss));Dxs=sub(mul(p,hssx),mul(hx,pss))
    u0,u1=sub(div(Dx,D),div(px,p));u=(-2*u0,-2*u1)
    z0,z1=sub(div(sub(mul(Dxs,D),mul(Dx,Ds)),mul(D,D)),
              div(sub(mul(psx,p),mul(px,ps)),mul(p,p)))
    us=(-2*z0,-2*z1)
    nf=np.arange(-K,K+1);freq=w*nf
    phase=np.exp(-1j*w*K*X);z=np.exp(1j*w*X)
    f=(np.polynomial.polynomial.polyval(z,F)*phase).real
    ft=(np.polynomial.polynomial.polyval(z,F*(freq*freq-4j*freq))*phase).real
    r,rt=div(mul((f,ft),D),mul(p,p))
    return u[0],4+4*sz*r-sz*us[0],u[1],4*sz*rt-sz*us[1]

def exact_fields(case,x,y,t=0.):
    """Continuous physical u,v on arbitrary supplied x,y coordinates."""
    x=np.asarray(x,dtype=float);y=np.atleast_1d(y).astype(float)
    if case in ('A','B','C','D'):
        return tuple(model(case).profile(y,t,x))
    if t==0.:
        d=reference.initial_data(case,x,y);return d['u'],d['v']
    rows=np.asarray([_direct_row(case,x,float(yy),t) for yy in y])
    return rows[:,0],rows[:,1]

def exact_rates(case,x,y,t=0.):
    """Analytic continuous u_t,v_t; no finite time differences."""
    x=np.asarray(x,dtype=float);y=np.atleast_1d(y).astype(float)
    if case in ('A','B','C','D'):
        m=model(case);stub=SimpleNamespace(x=x,G=m.G,h=m.h)
        return tuple(fields(stub,y,t)[2])
    if t==0.:
        d=reference.initial_data(case,x,y);return d['ut'],d['vt']
    rows=np.asarray([_direct_row(case,x,float(yy),t) for yy in y])
    return rows[:,2],rows[:,3]

def load_case(case):
    """Read the prepared, cropped physical arrays and y=0 sections."""
    with np.load(DATA/f'{case}.npz') as d:return {k:d[k] for k in d.files}

def section_at_zero(y,values,degree=11):
    """Local barycentric evaluation of numerical physical fields at y=0."""
    y=np.asarray(y);values=np.asarray(values)
    close=np.flatnonzero(abs(y)<=1e-12)
    if len(close):return values[close[np.argmin(abs(y[close]))]].copy(),dict(mode='native',degree=0)
    number=min(degree+1,len(y))
    indices=np.sort(np.argsort(abs(y),kind='stable')[:number])
    nodes=y[indices]
    scaled=(nodes-nodes.mean())/(nodes.max()-nodes.min())
    weights=np.array([1/np.prod(scaled[j]-np.delete(scaled,j)) for j in range(number)])
    weights/=np.max(abs(weights))
    terms=weights/(-nodes)
    bary=terms/terms.sum()
    result=np.tensordot(bary,values[indices],axes=(0,0))
    return result,dict(mode='barycentric',degree=number-1,indices=indices.tolist(),nodes=nodes.tolist(),
                       lebesgue_at_zero=float(np.sum(abs(bary))))
