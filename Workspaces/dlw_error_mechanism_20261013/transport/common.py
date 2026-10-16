"""Common physical-coordinate step and exact analytic RK4 JVP for frozen solvers."""
from pathlib import Path
import importlib.util
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'Workspaces/dlw_three_tracks_20261013/generate_shared.py'
spec=importlib.util.spec_from_file_location('frozen_generate_shared',SOURCE)
frozen=importlib.util.module_from_spec(spec);spec.loader.exec_module(frozen)
NS,BUNDLE=frozen.load_solver()


def setup(case,kind,config=None):
    cfg=NS['case_config'](case) if config is None else config
    obj=NS['SDModel' if kind=='SD' else 'FDModel'](case,kind,cfg)
    return obj,cfg


def unpack(obj,z):
    z=np.asarray(z)
    shape=z.shape[:-1]
    return z[..., :obj.np].reshape(shape+(obj.shape[0]-1,obj.X.n)),z[...,obj.np:].reshape(shape+obj.shape)


def pack(p,v):
    return np.concatenate((p.reshape(p.shape[:-2]+(-1,)),v.reshape(v.shape[:-2]+(-1,))),axis=-1)


def delta_u(obj,dp):
    shape=dp.shape[:-2]+(1,obj.X.n)
    return np.concatenate((np.zeros(shape,dtype=dp.dtype),obj.h*np.cumsum(dp,axis=-2)),axis=-2)


def delta_y_reconstruction(obj,du):
    """Derivative of delta0(u,ghost_u): prescribed lower, extrapolated upper."""
    low=np.zeros(du.shape[:-2]+(1,obj.X.n),dtype=du.dtype)
    high=(3*du[...,-1,:]-3*du[...,-2,:]+du[...,-3,:])[...,None,:]
    ext=np.concatenate((low,du,high),axis=-2)
    return (ext[...,2:,:]-ext[...,:-2,:])/(2*obj.h)


def reference(obj,t):
    u,v=obj.G.uv(obj.js,obj.X.x,t)
    return pack(np.diff(u,axis=0)/obj.h,v)


def to_native(obj,z,t):
    if obj.kind=='FD':return z.copy()
    p,v=unpack(obj,z)
    u=obj.recover_u(p,t)
    ghosts=NS['ghost_u'](obj.G,obj.js,obj.X.x,t,u)
    return pack(p,v-NS['delta0'](u,ghosts,obj.h))


def from_native(obj,z,t):
    if obj.kind=='FD':return z.copy()
    p,w=unpack(obj,z)
    u=obj.recover_u(p,t)
    ghosts=NS['ghost_u'](obj.G,obj.js,obj.X.x,t,u)
    return pack(p,w+NS['delta0'](u,ghosts,obj.h))


def tangent_to_native(obj,dz):
    if obj.kind=='FD':return dz.copy()
    dp,dv=unpack(obj,dz)
    return pack(dp,dv-delta_y_reconstruction(obj,delta_u(obj,dp)))


def tangent_from_native(obj,dz):
    if obj.kind=='FD':return dz.copy()
    dp,dw=unpack(obj,dz)
    return pack(dp,dw+delta_y_reconstruction(obj,delta_u(obj,dp)))


def common_step(obj,t,z,dt):
    native=to_native(obj,z,t)
    advanced=NS['step'](obj.rhs,t,native,dt,'RK4')
    return from_native(obj,advanced,t+dt)


def native_rhs_jvp(obj,t,z,dz):
    """Jacobian-vector products; dz may have a leading direction batch axis."""
    p,w=unpack(obj,z);dp,dw=unpack(obj,dz)
    u=obj.recover_u(p,t);du=delta_u(obj,dp)
    D,D2,h,a=obj.X.d1,obj.X.d2,obj.h,obj.a
    if obj.kind=='SD':
        dH=(u+2*a)*du+h*h*(w/16-1/4)*dw
        rp=-np.diff(D(dH),axis=-2)/h-D2(dp+(dw[...,1:,:]+dw[...,:-1,:])/2)
        rw=-D((u+2*a)*dw+(w-4)*du)+D2(dw)
    else:
        rp=-np.diff(D((u+2*a)*du),axis=-2)/h-D2((dw[...,1:,:]+dw[...,:-1,:])/2)
        rw=-D((u+2*a)*dw+w*du)-D2(delta_y_reconstruction(obj,du))+4*D(du)
    return pack(rp,rw)


def step_and_jvp(obj,t,z,dz,dt):
    """Return Psi(z) and B(z)dz, differentiating every native RK4 stage."""
    y=to_native(obj,z,t);dy=tangent_to_native(obj,dz)
    k1=obj.rhs(t,y);j1=native_rhs_jvp(obj,t,y,dy)
    y2=y+dt*k1/2;dy2=dy+dt*j1/2
    k2=obj.rhs(t+dt/2,y2);j2=native_rhs_jvp(obj,t+dt/2,y2,dy2)
    y3=y+dt*k2/2;dy3=dy+dt*j2/2
    k3=obj.rhs(t+dt/2,y3);j3=native_rhs_jvp(obj,t+dt/2,y3,dy3)
    y4=y+dt*k3;dy4=dy+dt*j3
    k4=obj.rhs(t+dt,y4);j4=native_rhs_jvp(obj,t+dt,y4,dy4)
    value=y+dt*(k1+2*k2+2*k3+k4)/6
    tangent=dy+dt*(j1+2*j2+2*j3+j4)/6
    return from_native(obj,value,t+dt),tangent_from_native(obj,tangent)


def physical_error(obj,dz):
    dp,dv=unpack(obj,dz)
    return delta_u(obj,dp),dv


def masks(obj,cfg):
    return np.flatnonzero(abs(obj.y)<cfg['eval_yhalf']),np.flatnonzero(abs(obj.X.x)<=cfg['eval_half']+1e-10)


def cropped_error(obj,dz,mask=None):
    u,v=physical_error(obj,dz)
    if mask is not None:
        iy,ix=mask
        u=u[...,iy[:,None],ix];v=v[...,iy[:,None],ix]
    return np.stack((u,v),axis=-3)


def field_stats(fields):
    u,v=fields
    u2=float(np.mean(u*u));v2=float(np.mean(v*v))
    return dict(joint_rms=float(np.sqrt(u2+v2)),u_rms=float(np.sqrt(u2)),v_rms=float(np.sqrt(v2)),
                u_linf=float(np.max(abs(u))),v_linf=float(np.max(abs(v))))


def compare(fields,reference_fields):
    denom=np.sqrt(np.sum(reference_fields*reference_fields))
    norm=np.sqrt(np.sum(fields*fields))
    residual=np.sqrt(np.sum((fields-reference_fields)**2))
    cosine=float(np.sum(fields*reference_fields)/(norm*denom)) if norm*denom else np.nan
    return dict(relative_residual=float(residual/denom) if denom else np.nan,
                norm_ratio=float(norm/denom) if denom else np.nan,cosine=cosine)
