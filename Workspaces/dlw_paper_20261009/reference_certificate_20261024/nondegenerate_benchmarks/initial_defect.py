"""Existing Endpoint-SD stencil on new pure initial fields, t=0 only."""
from pathlib import Path
import sys,json
import numpy as np
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
sys.path.insert(0,str(PROJECT/'spatial_audit_20261023'))
from run import Model

class NewData(Model):
    def __init__(self,case,h):
        super().__init__(case,'Endpoint-SD',.1,h);self.a=2.
    def jets(self,y,x=None):
        x=self.x if x is None else x;y=np.atleast_1d(y)
        k=np.pi/4;e=np.sin(k*(y+2))[:,None];ez=k*np.cos(k*(y+2))[:,None]
        if self.case=='Gaussian':
            A=.05;F=np.zeros_like(x);Fx=F.copy();Fxx=F.copy()
            for j in [-1,0,1]:
                q=x+192*j;g=np.exp(-(q/6)**2)
                F+=g;Fx+=-q/18*g;Fxx+=(q*q/324-1/18)*g
        else:
            A=.03;w=np.pi/12;F=np.cos(w*x);Fx=-w*np.sin(w*x);Fxx=-w*w*F
        return A*e*F,A*e*Fx,A*e*Fxx,A*ez*F,A*ez*Fx,A*ez*Fxx
    def profile(self,y,t=0.,x=None):
        assert t==0
        u,ux,uxx,p,px,pxx=self.jets(y,x)
        return np.array([u,4-3*p])
    def ut(self,y,t):
        assert t==0
        u,ux,uxx,p,px,pxx=self.jets(y)
        return 3*uxx-(u+4)*ux

rows=[]
for case in ['Sinusoidal','Gaussian']:
    for h in [.1,.05,.025,.0125]:
        m=NewData(case,h);ut,vt=m.rhs(0.,m.initial())
        u,ux,uxx,p,px,pxx=m.jets(m.yv)
        exact=-pxx+3*(ux*p+(u+4)*px)
        leading=-4*p*px
        mask=abs(m.yv)<=1.8+1e-12
        err=np.max(abs((vt-exact)[mask]));coef=np.max(abs(leading[mask]))
        rows.append({'case':case,'h':h,'vt_defect_max':float(err),'leading_coefficient_max':float(coef),
                     'defect_over_h':float(err/h),
                     'max_remainder_after_subtracting_hC':float(np.max(abs((vt-exact-h*leading)[mask])))})
    rr=rows[-4:]
    for a,b in zip(rr,rr[1:]):a['observed_order_to_next']=float(np.log2(a['vt_defect_max']/b['vt_defect_max']))
    assert rr[-2]['observed_order_to_next']>.9 and rr[-2]['observed_order_to_next']<1.1
out={'scope':'t=0 interior Endpoint v RHS defect, not terminal error or convergence of all methods','rows':rows}
(HERE/'initial_defect.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
