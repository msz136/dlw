"""Constant c,kappa optimization of analytic spatial residuals, without PDE evolution.

The objective fixes the physical N1/N2 representation and gives equal relative
L2 importance to both residuals and to each specified calibration profile.
"""
from pathlib import Path
import hashlib,json
import numpy as np
from numpy.polynomial import Polynomial
from scipy.special import expit
from scipy.integrate import simpson,quad_vec

ROOT=Path(__file__).parent
TRAIN={'P1':(4.,1.,2.),'B':(4.,2.,3.),'P6':(4.,1.,3.),'P10':(2.,1.5,2.)}
# Fixed beforehand: already-used independent spectra from the numerical study.
TRANSFER={'H1':(4.5,.9,2.6),'H2':(3.2,1.2,2.2),'H3':(2.3,1.65,2.4),'H4':(5.2,.65,1.2)}
POLY=[Polynomial([0,1])]
for _ in range(6):POLY.append(Polynomial([0,1,-1])*POLY[-1].deriv())

class Profile:
    def __init__(self,a,p,q):
        self.a,self.p,self.q=a,p,q
        self.k=p+q;self.omega=q*q-p*p
        self.P,self.Q=p-a,q+a
        self.L=1/self.P+1/self.Q
        self.loggamma=np.log(-self.P/self.Q)
    def derivs(self,z,n=5):
        # z is the centered phase: u(z), v(z) are even.
        f,g=expit(z+self.loggamma/2),expit(z-self.loggamma/2)
        u=[2*self.k*(POLY[i](f)-POLY[i](g)) for i in range(n+1)]
        v=[2*self.k*self.L*(POLY[i+1](f)+POLY[i+1](g)) for i in range(n+1)]
        return u,v
    def vectors(self,z):
        u,v=self.derivs(z)
        k,L=self.k,self.L
        w=[v[i]-L*u[i+1] for i in range(3)]
        square=k*L*(w[1]**2+(w[0]-4)*w[2])/16
        product=k*L**3*(u[2]**2+u[1]*u[3])/2
        vxxyy=k*k*L*L*v[4];uxxyyy=k*k*L**3*u[5]
        r1=square+vxxyy/12-uxxyyy/4
        r2=square+product+vxxyy/4-uxxyyy/12
        return r1,r2,2*k*L*u[2],2*k*v[1],-4*k*u[1]
    def finite_residual(self,z,h,c,kappa):
        k,L=self.k,self.L;A=self.a+c*h*h;r=1+kappa*h*h
        cache={}
        def at(j):
            if j not in cache:cache[j]=self.derivs(z+j*h*L,n=2)
            return cache[j]
        def node(j):
            u,v=at(j);up,_=at(j+1);um,_=at(j-1)
            d=[(up[i]-um[i])/(2*h) for i in range(3)]
            w=[v[i]-d[i] for i in range(3)]
            hx=(u[0]+2*A)*k*u[1]+h*h*(w[0]/16-r/4)*k*w[1]
            return u,v,d,w,hx
        p,m=node(.5),node(-.5)
        e1=self.omega*(p[0][1]-m[0][1])/h+(p[4]-m[4])/h
        e1+=k*k*((p[0][2]-m[0][2])/h+(p[3][2]+m[3][2])/2)
        u,v,d,w,hx=node(0);p,m=node(1),node(-1)
        e2=self.omega*v[1]+(p[4]-m[4])/(2*h)+k*(u[1]*w[0]+(u[0]+2*A)*w[1]-4*r*u[1])
        e2+=k*k*(d[2]+(p[3][2]-2*w[2]+m[3][2])/4)
        return e1,e2

def arrays(profile,z):
    r1,r2,A,B,C=profile.vectors(z)
    inner=lambda f,g:float(simpson(f*g,x=z))
    n1,n2=inner(r1,r1),inner(r2,r2)
    G=np.array([[inner(A,A)/n1+inner(B,B)/n2,inner(B,C)/n2],
                [inner(B,C)/n2,inner(C,C)/n2]])
    b=np.array([inner(A,r1)/n1+inner(B,r2)/n2,inner(C,r2)/n2])
    return (r1,r2,A,B,C),inner,(n1,n2),G,b

def metrics(vec,inner,norms,theta):
    r1,r2,A,B,C=vec;c,kappa=theta
    rr=(r1+c*A,r2+c*B+kappa*C)
    ratios=[np.sqrt(inner(rr[i],rr[i])/norms[i]) for i in (0,1)]
    maxratios=[float(np.max(np.abs(rr[i]))/np.max(np.abs((r1,r2)[i]))) for i in (0,1)]
    return {'relative_L2':list(map(float,ratios)),'relative_Linf_sampled':maxratios,
            'combined_relative_RMS':float(np.sqrt(sum(v*v for v in ratios)/2))}

def floors(vec,inner,norms):
    r1,r2,A,B,C=vec;n1,n2=norms
    c1=-inner(A,r1)/inner(A,A)
    G2=np.array([[inner(B,B),inner(B,C)],[inner(B,C),inner(C,C)]])
    b2=np.array([inner(B,r2),inner(C,r2)])
    theta2=-np.linalg.solve(G2,b2)
    res1=r1+c1*A;res2=r2+theta2[0]*B+theta2[1]*C
    return {'first_c_minimizer':c1,
            'individual_equation_L2_floors':[np.sqrt(inner(res1,res1)/n1),np.sqrt(inner(res2,res2)/n2)],
            'second_equation_minimizer':theta2.tolist(),
            'parity_L2_lower_bounds':[np.sqrt(inner((r1-r1[::-1])/2,(r1-r1[::-1])/2)/n1),
                                    np.sqrt(inner((r2+r2[::-1])/2,(r2+r2[::-1])/2)/n2)]}

z=np.linspace(-24,24,24577)
records={};Gsum=np.zeros((2,2));bsum=np.zeros(2)
for name,pars in TRAIN.items():
    p=Profile(*pars);vec,inner,norms,G,b=arrays(p,z)
    theta=-np.linalg.solve(G,b)
    assert min(np.linalg.eigvalsh(G))>0
    assert np.max(abs(G@theta+b))<1e-11
    records[name]={'parameters':dict(zip(('a','p','q'),pars)),
        'individual_optimum':theta.tolist(),'individual_metrics':metrics(vec,inner,norms,theta),
        'Gram_matrix':G.tolist(),'normal_rhs':b.tolist(),'floors':floors(vec,inner,norms)}
    Gsum+=G;bsum+=b
shared=-np.linalg.solve(Gsum,bsum)
shared_metrics={};transfer={};finite=[]
for name,pars in {**TRAIN,**TRANSFER}.items():
    p=Profile(*pars);vec,inner,norms,G,b=arrays(p,z)
    met=metrics(vec,inner,norms,shared)
    if name in TRAIN:
        shared_metrics[name]=met
        for h in (.25,.125,.0625,.03125):
            e0=p.finite_residual(z,h,0,0);e=p.finite_residual(z,h,*shared)
            lead=(vec[0]+shared[0]*vec[2],vec[1]+shared[0]*vec[3]+shared[1]*vec[4])
            pred=[e[i]-h*h*lead[i] for i in (0,1)]
            finite.append({'case':name,'h':h,
                'relative_L2':[np.sqrt(inner(e[i],e[i])/inner(e0[i],e0[i])) for i in (0,1)],
                'relative_Linf_sampled':[float(np.max(abs(e[i]))/np.max(abs(e0[i]))) for i in (0,1)],
                'relative_leading_prediction_L2_error':[np.sqrt(inner(pred[i],pred[i])/inner(e[i],e[i])) for i in (0,1)],
                'L2_minus_leading':[np.sqrt(inner(pred[i],pred[i])) for i in (0,1)]})
    else:transfer[name]={'parameters':dict(zip(('a','p','q'),pars)),**met}

# Independent adaptive quadrature of the nine inner products over all real phase.
quad_checks=[];qGsum=np.zeros((2,2));qbsum=np.zeros(2)
for name,pars in TRAIN.items():
    p=Profile(*pars)
    def integrand(s):
        r1,r2,A,B,C=p.vectors(float(s))
        return np.array([r1*r1,r2*r2,A*A,B*B,B*C,C*C,A*r1,B*r2,C*r2])
    vals,err=quad_vec(integrand,-np.inf,np.inf,epsabs=1e-11,epsrel=2e-11)
    n1,n2,aa,bb,bc,cc,ar,br,cr=vals
    G=np.array([[aa/n1+bb/n2,bc/n2],[bc/n2,cc/n2]])
    b=np.array([ar/n1+br/n2,cr/n2])
    theta=-np.linalg.solve(G,b);qGsum+=G;qbsum+=b
    old=np.array(records[name]['individual_optimum'])
    assert np.max(abs(theta-old))<1e-8
    quad_checks.append({'case':name,'independent_optimum':theta.tolist(),
                        'max_absolute_coefficient_change':float(np.max(abs(theta-old))),
                        'quadrature_error_estimate':float(err)})
quad_shared=-np.linalg.solve(qGsum,qbsum)
assert np.max(abs(shared-quad_shared))<1e-9

# Expanded interval + refined sample grid checks both tails and maxima.
refinements=[]
for name,pars in TRAIN.items():
    vec,inner,norms,G,b=arrays(Profile(*pars),np.linspace(-32,32,65537))
    mm=metrics(vec,inner,norms,shared)
    refinements.append({'case':name,
        'max_L2_ratio_change':float(np.max(abs(np.array(mm['relative_L2'])-shared_metrics[name]['relative_L2']))),
        'max_Linf_ratio_change':float(np.max(abs(np.array(mm['relative_Linf_sampled'])-shared_metrics[name]['relative_Linf_sampled']))),
        'refined_metrics':mm})

for name in TRAIN:
    rows=[r for r in finite if r['case']==name]
    for i in range(1,len(rows)):
        rows[i]['remainder_orders']=[float(np.log2(rows[i-1]['L2_minus_leading'][j]/rows[i]['L2_minus_leading'][j])) for j in (0,1)]

c,kappa=shared
# A sufficient uniform positive-Gram condition for every listed spectrum and 0<h<=1/4.
gmin=min(a-p for a,p,q in {**TRAIN,**TRANSFER}.values())
assert c-kappa*.25/2>0 and gmin-.25/2>0 and kappa>0
result={'scope':'Only analytic spatial residuals and function quadrature. No x finite differences or time integrator.',
        'objective':'Sum of squared residual L2 norms normalized separately by each original equation norm; equal weights per equation and calibration profile.',
        'calibration':records,'shared_optimum':shared.tolist(),'shared_metrics':shared_metrics,
        'shared_combined_RMS':float(np.sqrt(np.mean([x*x for m in shared_metrics.values() for x in m['relative_L2']]))),
        'transfer_without_refit':transfer,'finite_h_checks':finite,
        'independent_quadrature':quad_checks,'independent_shared_optimum':quad_shared.tolist(),
        'sampling_refinements':refinements,
        'regularity':{'h_max':.25,'minimum_a_minus_p':gmin,'uniform_lower_s_minus_minus_p':gmin-.125,
                      'c_minus_kappa_hmax_over_2':float(c-kappa*.125)},
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(ROOT/'optimization.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Shared c,kappa:',shared,'combined RMS:',result['shared_combined_RMS'])
for name in TRAIN:print(name,'shared',shared_metrics[name],'floors',records[name]['floors']['individual_equation_L2_floors'])
for name,m in transfer.items():print('Transfer',name,m)
print('Independent coefficient change:',np.max(abs(shared-quad_shared)))
