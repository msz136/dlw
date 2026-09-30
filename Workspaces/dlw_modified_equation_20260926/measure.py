"""Pure y-model defects and exact Gram field errors; no time or x discretization."""
from pathlib import Path
import json, hashlib
import numpy as np
import mpmath as mp
from scipy.special import expit
from numpy.polynomial import Polynomial

ROOT=Path(__file__).parent
CASES={'P1':(4.,1.,2.,3.),'B':(4.,2.,3.,5.),
       'P6':(4.,1.,3.,4.),'P10':(2.,1.5,2.,3.5)}
HS=[.25,.125,.0625,.03125,.015625]
polys=[Polynomial([0,1])]
for _ in range(7):
    polys.append(Polynomial([0,1,-1])*polys[-1].deriv())

class Wave:
    def __init__(self,pars):
        self.a,self.p,self.q,self.rho=pars
        self.k=self.p+self.q
        self.omega=self.q**2-self.p**2
        self.P,self.Q=self.p-self.a,self.q+self.a
        self.L=1/self.P+1/self.Q
        self.gamma=-self.P/self.Q
        self.C=(self.P**-3+self.Q**-3)/12
        self.D=(self.Q**-2-self.P**-2)/8
    def phase(self,x,y,t=0.):
        return self.k*x+self.omega*t+np.log(self.rho/self.k)+self.L*y
    def derivatives(self,z,n=5):
        f,g=expit(z+np.log(self.gamma)),expit(z)
        uu=[2*self.k*(polys[i](f)-polys[i](g)) for i in range(n+1)]
        vv=[2*self.k*self.L*(polys[i+1](f)+polys[i+1](g)) for i in range(n+1)]
        return uu,vv
    def coefficient_parts(self,z,y):
        f,g=expit(z+np.log(self.gamma)),expit(z)
        f1,f2,f3=[polys[i](f) for i in (1,2,3)]
        g1,g2,g3=[polys[i](g) for i in (1,2,3)]
        k,L,C,D=self.k,self.L,self.C,self.D
        return {'phase':(2*k*y*C*(f1-g1),2*k*C*(f1+g1)+2*k*L*y*C*(f2+g2)),
                'F_coefficient':(2*k*D*f1,2*k*L*D*f2),
                'field_extraction':(-k*L*L*g2/4,k*L**3*(f3/3-5*g3/12))}
    def exact_fields(self,x,y,h,t=0.):
        P,Q=self.P,self.Q
        logchi=(np.log1p(h/(2*P))-np.log1p(-h/(2*P))
                +np.log1p(h/(2*Q))-np.log1p(-h/(2*Q)))
        centered_loggamma=np.log(self.gamma)+.5*np.log1p(-h*h/(4*P*P))-.5*np.log1p(-h*h/(4*Q*Q))
        z=self.k*x+self.omega*t+np.log(self.rho/self.k)+y*(logchi/h)
        def U(z):
            return self.k*(2*expit(z+centered_loggamma)-expit(z-logchi/2)-expit(z+logchi/2))
        u=U(z)
        v=4*self.k/h*(expit(z+logchi/2)-expit(z-logchi/2))+(U(z+logchi)-U(z-logchi))/(2*h)
        return u,v
    def leading_residual(self,z):
        u,v=self.derivatives(z)
        k,L=self.k,self.L
        w=[v[i]-L*u[i+1] for i in range(3)]
        nonlinear=k*L*(w[1]**2+(w[0]-4)*w[2])/16
        product=k*L**3*(u[2]**2+u[1]*u[3])/2
        vterm=k*k*L*L*v[4]
        uterm=k*k*L**3*u[5]
        return {'SD':(nonlinear+vterm/12-uterm/4,nonlinear+product+vterm/4-uterm/12),
                'FD':(vterm/12,uterm/6),
                'terms':{'nonlinear':nonlinear,'product':product,'v_xxyy':vterm,'u_xxyyy':uterm}}
    def residual(self,z,h,model):
        k,a,L,om=self.k,self.a,self.L,self.omega
        cache={}
        def get(j):
            if j not in cache:
                U,V=self.derivatives(z+L*h*j,n=2)
                cache[j]=(U,V)
            return cache[j]
        def node(j):
            U,V=get(j)
            Up,_=get(j+1); Um,_=get(j-1)
            d=[(Up[i]-Um[i])/(2*h) for i in range(3)]
            w=[V[i]-d[i] for i in range(3)]
            hx=(U[0]+2*a)*k*U[1]
            if model=='SD':hx+=h*h*(w[0]/16-.25)*k*w[1]
            return U,V,w,d,hx
        plus,minus=node(.5),node(-.5)
        R1=om*(plus[0][1]-minus[0][1])/h+(plus[4]-minus[4])/h
        if model=='SD':
            R1+=k*k*((plus[0][2]-minus[0][2])/h+(plus[2][2]+minus[2][2])/2)
        else:R1+=k*k*(plus[1][2]+minus[1][2])/2
        U,V,w,d,hx=node(0)
        if model=='SD':
            pp,mm=node(1),node(-1)
            R2=om*V[1]+(pp[4]-mm[4])/(2*h)+k*(U[1]*w[0]+(U[0]+2*a)*w[1]-4*U[1])
            R2+=k*k*(d[2]+(pp[2][2]-2*w[2]+mm[2][2])/4)
        else:
            R2=om*V[1]+k*(U[1]*V[0]+(U[0]+2*a)*V[1]-4*U[1])+k*k*d[2]
        return R1,R2

norm=lambda z:float(np.max(np.abs(z)))
result={'scope':'Analytic x,t derivatives; no PDE time integration. Residual components have different units and are not summed.',
        'model_error_domain':'x in [-10,10], y=(j+1/2)h in [-1.5,1.5], t=0',
        'x_samples':4001,'residual_phase_domain':[-16,16],'residual_phase_samples':8193,'cases':{}}
for name,pars in CASES.items():
    wave=Wave(pars)
    z=np.linspace(-16,16,8193)
    leading=wave.leading_residual(z)
    rec={'parameters':dict(zip(['a','p','q','rho'],pars)),
         'phase_h2_coefficient':wave.C,'centered_F_h2_coefficient':wave.D,
         'residual_h2_norm':{m:[norm(e) for e in leading[m]] for m in ('SD','FD')},
         'residual_scans':[],'field_scans':[]}
    for h in HS:
        defects={}
        for model in ('SD','FD'):
            exact=wave.residual(z,h,model)
            err=[exact[i]-h*h*leading[model][i] for i in range(2)]
            defects[model]={'norm':[norm(e) for e in exact],
                'minus_leading_norm':[norm(e) for e in err],
                'relative_prediction_error':[norm(err[i])/norm(exact[i]) for i in range(2)]}
        rec['residual_scans'].append({'h':h,**defects})
        x=np.linspace(-10,10,4001)[None,:]
        ny=int(round(1.5/h))
        y=((np.arange(-ny,ny)+.5)*h)[:,None]
        phase=wave.phase(x,y)
        U,V=wave.derivatives(phase,n=0)
        exact=wave.exact_fields(x,y,h)
        errors=[exact[0]-U[0],exact[1]-V[0]]
        parts=wave.coefficient_parts(phase,y)
        coeff=[sum(p[i] for p in parts.values()) for i in range(2)]
        rem=[errors[i]-h*h*coeff[i] for i in range(2)]
        rec['field_scans'].append({'h':h,'norm':[norm(e) for e in errors],
            'relative_norm':[norm(errors[i])/norm((U[0],V[0])[i]) for i in range(2)],
            'predicted_norm':[h*h*norm(e) for e in coeff],
            'minus_leading_norm':[norm(e) for e in rem],
            'relative_prediction_error':[norm(rem[i])/norm(errors[i]) for i in range(2)],
            'coefficient_parts_norm':{key:[norm(e) for e in val] for key,val in parts.items()}})
    for rows in (rec['field_scans'],):
        for i in range(1,len(rows)):
            for key in ('norm','minus_leading_norm'):
                rows[i][key+'_order']=[float(np.log2(rows[i-1][key][j]/rows[i][key][j])) for j in range(2)]
    result['cases'][name]=rec
    print(name,'residual coefficients',rec['residual_h2_norm'],'h=1/8 model errors',rec['field_scans'][1]['norm'])

# Check the sampling resolution behind the displayed maxima, not a new solver.
sampling=[]
for name,pars in CASES.items():
    wave=Wave(pars); h=.125
    x=np.linspace(-10,10,8001)[None,:]
    y=((np.arange(-12,12)+.5)*h)[:,None]
    u,v=wave.derivatives(wave.phase(x,y),n=0)
    uh,vh=wave.exact_fields(x,y,h)
    dense_fields=[norm(uh-u[0]),norm(vh-v[0])]
    old=result['cases'][name]['field_scans'][1]['norm']
    leading=wave.leading_residual(np.linspace(-16,16,16385))
    residual_change={model:[abs(norm(leading[model][i])/result['cases'][name]['residual_h2_norm'][model][i]-1) for i in range(2)] for model in ('SD','FD')}
    sampling.append({'case':name,'field_max_relative_change':[abs(dense_fields[i]/old[i]-1) for i in range(2)],
                     'residual_coefficient_max_relative_change':residual_change})
result['sampling_refinement']=sampling

# Independent high precision differentiation: the predicted exact-family error
# must solve the forced linearized DLW equations, not merely fit h-scans.
mp.mp.dps=65
mpchecks=[]
for name,pars in CASES.items():
    a,p,q,rho=map(mp.mpf,map(str,pars)); k=p+q; om=q*q-p*p
    P,Q=p-a,q+a; L=1/P+1/Q; C=(P**-3+Q**-3)/12; D=(Q**-2-P**-2)/8
    gamma=-P/Q
    def poly(i,z):
        return sum(mp.mpf(int(co))*z**n for n,co in enumerate(polys[i].coef))
    def allfields(x,y,t):
        phase=k*x+om*t+mp.log(rho/k)+L*y
        f=1/(1+mp.exp(-phase)/gamma); g=1/(1+mp.exp(-phase))
        fs=[poly(i,f) for i in range(4)]; gs=[poly(i,g) for i in range(4)]
        u=2*k*(f-g); v=2*k*L*(fs[1]+gs[1])
        eu=2*k*((y*C+D)*fs[1]-y*C*gs[1])-k*L*L*gs[2]/4
        ev=2*k*C*(fs[1]+gs[1])+2*k*L*((y*C+D)*fs[2]+y*C*gs[2])+k*L**3*(fs[3]/3-5*gs[3]/12)
        return u,v,eu,ev
    fields=[lambda x,y,t,i=i:allfields(x,y,t)[i] for i in range(4)]
    point=tuple(map(mp.mpf,('.13','.37','.02')))
    dd=lambda f,orders:mp.diff(f,point,orders)
    uf,vf,ef,gf=fields
    Kfun=lambda x,y,t:(vf(x,y,t)-mp.diff(uf,(x,y,t),(0,1,0))-4)**2/32
    r1=dd(Kfun,(1,1,0))+dd(vf,(2,2,0))/12-dd(uf,(2,3,0))/4
    product=lambda x,y,t:mp.diff(uf,(x,y,t),(0,1,0))*mp.diff(uf,(x,y,t),(0,2,0))
    r2=dd(Kfun,(1,1,0))+dd(product,(1,0,0))/2+dd(vf,(2,2,0))/4-dd(uf,(2,3,0))/12
    linflux1=lambda x,y,t:(uf(x,y,t)+2*a)*mp.diff(ef,(x,y,t),(0,1,0))+mp.diff(uf,(x,y,t),(0,1,0))*ef(x,y,t)
    linflux2=lambda x,y,t:(uf(x,y,t)+2*a)*gf(x,y,t)+(vf(x,y,t)-4)*ef(x,y,t)
    residuals=[dd(ef,(0,1,1))+dd(gf,(2,0,0))+dd(linflux1,(1,0,0))+r1,
               dd(gf,(0,0,1))+dd(ef,(2,1,0))+dd(linflux2,(1,0,0))+r2]
    assert max(map(abs,residuals))<mp.mpf('1e-50'),(name,residuals)
    mpchecks.append({'case':name,'forced_error_equation_residual':[mp.nstr(z,8) for z in residuals]})
result['high_precision_checks']=mpchecks
result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(ROOT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('High precision forced-error identities verified for all four cases.')
