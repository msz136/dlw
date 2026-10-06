"""Exact spectral generating identities and moments on the requested Gram benchmarks."""
from pathlib import Path
import json
import sympy as s

HERE = Path(__file__).resolve().parent
z, y1, y2, r = s.symbols('z y1 y2 r')
checks = []

def require(name, expr):
    num = s.cancel(expr).as_numer_denom()[0]
    assert s.expand(num) == 0, (name, num)
    checks.append(name)

def determinant_wave(p, q):
    ys = [y1, y2][:len(p)]
    k = [p[i]+q[i] for i in range(len(p))]
    speed = [p[i]-q[i] for i in range(len(p))]
    def Dx(f):
        return sum(k[i]*ys[i]*s.diff(f,ys[i]) for i in range(len(p)))
    def Dt(f):
        return -sum(k[i]*speed[i]*ys[i]*s.diff(f,ys[i]) for i in range(len(p)))
    t = [(z-p[i])/(z+q[i]) for i in range(len(p))]
    if len(p)==1:
        G, T = 1+y1, 1+t[0]*y1
    else:
        kap=s.Rational((p[0]-p[1])*(q[0]-q[1]),(p[0]+q[1])*(p[1]+q[0]))
        G=1+y1+y2+kap*y1*y2
        T=1+t[0]*y1+t[1]*y2+kap*t[0]*t[1]*y1*y2
    # B_z T.G=0 is equivalent to the complete heat generating identity,
    # not a finite coefficient sample.
    bil=Dx(Dx(T))*G-2*Dx(T)*Dx(G)+T*Dx(Dx(G))
    bil+=Dt(T)*G-T*Dt(G)+2*z*(Dx(T)*G-T*Dx(G))
    return G,T,Dx,Dt,bil

cases={'1a':([1],[2]),'1b':([4],[-3]),'two_soliton':([6,4],[-5,-3])}
moments={}
for name,(p,q) in cases.items():
    G,T,Dx,Dt,bil=determinant_wave(p,q)
    require(name+': all-order heat generating identity',bil)
    moments[name]=[str(sum(s.Rational((-q[i])**n-p[i]**n,n) for i in range(len(p)))) for n in range(1,9)]
    if len(p)==1:
        pp,qq=p[0],q[0]; kk=pp+qq; vv=pp-qq
        def Dr(f):return kk*r*(1-r)*s.diff(f,r)
        rho={n:-kk**2*r*(1-r)*(kk*r-qq)**(n-1) for n in range(1,9)}
        for n in range(1,8):
            flux=Dr(rho[n])+2*rho[n+1]+sum(rho[a]*rho[n-a] for a in range(1,n))
            require(name+f': coefficient conservation {n}',-vv*Dr(rho[n])+Dr(flux))
        for n in range(1,9):
            require(name+f': endpoint moment {n}',s.integrate(-kk*(kk*r-qq)**(n-1),(r,0,1))-s.Rational((-qq)**n-pp**n,n))

# The moment Jacobian is a Vandermonde, hence rank 2m if nodes differ.
rank_certificates={}
for name,(p,q) in cases.items():
    nodes=p+[-v for v in q]
    J=s.Matrix([[-s.Integer(v)**(n-1) for v in nodes] for n in range(1,2*len(p)+1)])
    rank_certificates[name]={'nodes':nodes,'rank':J.rank(),'determinant':str(J.det())}
    assert J.det()!=0
    checks.append(name+': spectral-parameter moment Jacobian')

result={'passed':len(checks),'checks':checks,'moments_1_to_8':moments,
        'spectral_family_rank':rank_certificates,
        'scope':'Exact Gram-family identities; no claim of general-state involution or finite total lattice integral.'}
(HERE/'benchmark_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
