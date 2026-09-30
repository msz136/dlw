"""Analytic initial-profile diagnostics; no time integration or accuracy claims."""
from pathlib import Path
import sys,json
import numpy as np
from scipy.special import expit
from scipy.integrate import cumulative_trapezoid
from numpy.polynomial import Polynomial
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'dlw_coefficient_euler_20260926'))
from model import FamilyModel,Parameters

def fields(a,p,q,y,x):
    k=p+q;ell=-k/((a-p)*(a+q));gamma=(a-p)/(a+q)
    z=k*x[None,:]+ell*np.asarray(y)[:,None]
    f,g=expit(z+np.log(gamma)),expit(z)
    u=2*k*(f-g);v=2*k*ell*(f*(1-f)+g*(1-g));uy=2*k*ell*(f*(1-f)-g*(1-g))
    return u,v,uy

def main():
    x=np.linspace(-10,10,16385);h=.125;js=np.arange(-12,12);y=(js+.5)*h
    rows=[];shapes={}
    for name,(a,p,q) in {'P1':(4,1,2),'P2':(4,2,3),'P6':(4,1,3),'P10':(2,1.5,2)}.items():
        k=p+q;ell=-k/((a-p)*(a+q));gamma=(a-p)/(a+q)
        for label,c,kappa in [('original',0.,0.),('theory',.04248652711,.00844851896)]:
            mu=1+kappa*h*h
            uu,vv,_=fields(a,p,q,np.r_[y[0]-h,y,y[-1]+h],x)
            u,v=uu[1:-1],vv[1:-1];uyh=(uu[2:]-uu[:-2])/(2*h)
            w=v-uyh;P=np.diff(u,axis=0)/h;S=2*P+(w[1:]+w[:-1])/2
            rm=1-w/(4*mu);rp=1-S/(4*mu)
            # Work on the same 22 interior F layers, requiring no external plus layer.
            rmF=rm[1:-1];rpF=(rp[:-1]+rp[1:])/2
            raw={'minus':rmF.mean(axis=0),'plus':rpF.mean(axis=0),'symmetric':((rmF+rpF)/2).mean(axis=0)}
            raw['symmetric_strength4']=1+4*(raw['symmetric']-1)
            for density,R in raw.items():
                mass=cumulative_trapezoid(R,x,initial=0)
                mesh=np.interp(np.linspace(0,mass[-1],257),mass,x)
                rows.append(dict(case=name,coefficients=label,density=density,min_R=float(min(R)),max_R=float(max(R)),
                    min_spacing_ratio=float(min(np.diff(mesh))/(20/256)),max_spacing_ratio=float(max(np.diff(mesh))/(20/256)),
                    total_mass=float(mass[-1]),grid_nodes=mesh.tolist()))
            # Independent finite-h Gram identity for the new plus field.
            m=FamilyModel(Parameters(a,p,q,k),c=c,kappa=kappa)
            chi=(p-m.sminus)*(q+m.splus)/((p-m.splus)*(q+m.sminus));gam=-(p-m.sminus)/(q+m.sminus)
            assert 0<chi<1 and gam>0
            z=k*x[None,:]+js[:,None]*np.log(chi)
            wgram=4*k/h*(expit(z+np.log(chi))-expit(z))
            ugram=k*(2*expit(z+np.log(gam))-expit(z)-expit(z+np.log(chi)))
            s_from_u=2*np.diff(ugram,axis=0)/h+(wgram[1:]+wgram[:-1])/2
            s_tau=4*k/h*(expit(z[1:]+np.log(gam))-expit(z[:-1]+np.log(gam)))
            assert np.max(abs(s_from_u-s_tau))<5e-13
            assert (1-wgram/(4*mu)).min()>1-1e-12 and (1-s_tau/(4*mu)).min()>1-1e-12
        U,V,Uy=fields(a,p,q,[0],x)
        rm=1-(V[0]-Uy[0])/4;rp=1-(V[0]+Uy[0])/4
        shapes[name]=dict(a=a,p=p,q=q,k=k,ell=ell,gamma=gamma,u_center=-np.log(gamma)/(2*k),
            branch_peak=1-k*ell/4,symmetric_center=1-k*ell*np.sqrt(gamma)/(1+np.sqrt(gamma))**2,
            branch_peak_offset=abs(np.log(gamma))/(2*k))
        if name=='P6':np.savez_compressed(HERE/'p6_profiles.npz',x=x,u=U[0],v=V[0],minus=rm,plus=rp,symmetric=(rm+rp)/2)
    (HERE/'snapshots.json').write_text(json.dumps(dict(scope='Initial continuous physical fields at t=0; geometry only, no time integration',
        rows=rows,analytic_profiles=shapes,finite_gram_checks='8 parameter-family cases passed'),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(shapes,indent=2))
    for r in rows:
        if r['case']=='P6' and r['coefficients']=='original':print({k:v for k,v in r.items() if k!='grid_nodes'})
if __name__=='__main__':main()
