"""Exact continuous linear tests and an independent current natural-SD audit.

The reference is ONLY for the continuous linearization at u=0, v=4.
It is not a nonlinear reference for perturbed solitons/Gaussian/sine data.
"""
from pathlib import Path
import sys, json, hashlib
import numpy as np
import sympy as sp
from flint import arb, ctx

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PROBE=HERE.parent/'spatial_audit_20261023/separated/reconstruction_probe'
sys.path.insert(0,str(PROBE))
from rerun_20261024 import rhs

def linear_value(which,x,y,t,mode=1,epsilon='0.000001',yL='-2',yR='2'):
    """Arb values, phi=sin²(pi*(y-yL)/(yR-yL)), kappa=mode*pi/2."""
    ctx.prec=160
    x,y,t,L,R,eps=map(arb,[str(x),str(y),str(t),str(yL),str(yR),epsilon])
    width=R-L;r=(y-L)/width;kappa=mode*arb.pi()/2
    phi=(arb.pi()*r).sin()**2
    phiy=arb.pi()/width*(2*arb.pi()*r).sin()
    primitive=(y-L)/2-width/(4*arb.pi())*(2*arb.pi()*r).sin()
    oscillation=(kappa*(x-4*t)).cos()
    growth=kappa*kappa*t
    if which=='u_only':return eps*phi*oscillation*growth.cosh(),eps*phiy*oscillation*growth.sinh()
    if which=='v_only':return eps*primitive*oscillation*growth.sinh(),eps*phi*oscillation*growth.cosh()
    raise ValueError(which)

def symbolic_checks():
    xi,h,d,c,l=sp.symbols('xi h d c l',real=True)
    B=sp.Matrix([[xi**2-sp.I*c*xi,xi**2*h/2-sp.I*xi*h*h*d/16],[-sp.I*xi*d,-xi**2-sp.I*c*xi]])
    polynomial=sp.expand((B-l*sp.eye(2)).det())
    eigs=[-sp.I*c*xi+sgn*(xi**2-sp.I*h*d*xi/4) for sgn in [1,-1]]
    eigen_remainders=[sp.simplify(polynomial.subs(l,e)) for e in eigs]
    x,y,t,k=sp.symbols('x y t k',real=True)
    phi=sp.Function('phi')(y);J=sp.Function('J')(y)
    phase=sp.cos(k*(x-4*t));C=sp.cosh(k*k*t);S=sp.sinh(k*k*t)
    checks=[]
    for u,v in [(phi*phase*C,sp.diff(phi,y)*phase*S),(J*phase*S,sp.diff(J,y)*phase*C)]:
        R1=sp.diff(u,y,t)+sp.diff(v,x,2)+4*sp.diff(u,y,x)
        R2=sp.diff(v,t)+sp.diff(u,y,x,2)+4*sp.diff(v,x)
        checks.extend([sp.simplify(R1),sp.simplify(R2)])
    assert eigen_remainders==[0,0] and checks==[0,0,0,0]
    return dict(characteristic_residuals=[str(x) for x in eigen_remainders],continuous_linear_PDE_residuals=[str(x) for x in checks])

class TestModel:
    def __init__(self,U,V):
        self.a=2.;self.h=.1;self.nx=32;self.ny=5
        self.x=np.arange(self.nx)*2*np.pi/self.nx;self.U=U;self.V=V
        self.k=np.fft.rfftfreq(self.nx,1/self.nx)
        self.m1=1j*self.k;self.m1[-1]=0;self.m2=-self.k*self.k
    def d1(self,z):return np.fft.irfft(np.fft.rfft(z,axis=-1)*self.m1,n=self.nx,axis=-1)
    def d2(self,z):return np.fft.irfft(np.fft.rfft(z,axis=-1)*self.m2,n=self.nx,axis=-1)
    def boundary(self,t):return np.zeros((6,self.nx)),np.zeros((6,self.nx))

def production_check(U,V,mode=3):
    m=TestModel(U,V);xi=float(mode)
    # Lower u is prescribed and is therefore not a perturbation state variable.
    indices=[(1,0)]+[(field,j) for j in range(1,m.ny) for field in [0,1]]
    z0=np.empty((2,m.ny,m.nx));z0[0]=U;z0[1]=V
    epsilon=1e-4;c,s=np.cos(xi*m.x),np.sin(xi*m.x)
    projection=np.exp(-1j*xi*m.x)/m.nx
    actual=np.zeros((len(indices),len(indices)),dtype=complex)
    for j,(field,layer) in enumerate(indices):
        directional=np.zeros_like(z0,dtype=complex)
        for function,weight in [(c,1.),(s,1j)]:
            plus=z0.copy();minus=z0.copy()
            plus[field,layer]+=epsilon*function;minus[field,layer]-=epsilon*function
            directional+=weight*(rhs(m,0.,plus)-rhs(m,0.,minus))/(2*epsilon)
        for i,index in enumerate(indices):actual[i,j]=np.sum(directional[index]*projection)
    expected=np.zeros_like(actual);advection=U+4;d=V-4
    expected[0,0]=-xi*xi-1j*advection*xi
    block=np.array([[xi*xi-1j*advection*xi,xi*xi*m.h/2-1j*xi*m.h*m.h*d/16],[-1j*xi*d,-xi*xi-1j*advection*xi]])
    for j in range(1,m.ny):
        start=2*j-1;expected[start:start+2,start:start+2]=block
        expected[start,0]=xi*xi*m.h/2+1j*xi*m.h*m.h*d/16
        for r in range(1,j):expected[start,2*r]=xi*xi*m.h
    discrepancy=float(np.max(abs(actual-expected)))
    assert discrepancy<2e-8,discrepancy
    return dict(U=U,V=V,xi=xi,h=m.h,ny=m.ny,nx=m.nx,matrix_discrepancy=discrepancy,
        block=[[str(v) for v in row] for row in block],
        predicted_eigenvalues=[str(-1j*advection*xi+sgn*(xi*xi-1j*m.h*d*xi/4)) for sgn in [1,-1]],
        first_lower_u_excluded=True)

def main():
    ctx.prec=160
    factors=[]
    for mode in [1,2,4,8,16]:
        k=mode*arb.pi()/2;r=k*k/100
        factors.append(dict(mode=mode,kappa=str(k),cosh=str(r.cosh()),sinh=str(r.sinh())))
    samples=[]
    for which in ['u_only','v_only']:
        for mode in [1,2,4,8,16]:
            u,v=linear_value(which,'.3','.5','.01',mode)
            assert u.rad()<arb('1e-40') and v.rad()<arb('1e-40')
            samples.append(dict(which=which,mode=mode,x='.3',y='.5',t='.01',epsilon='1e-6',
                u_enclosure=str(u),v_enclosure=str(v),radius_upper_bound='1e-40'))
    result=dict(scope='Continuous linearization at u=0,v=4 only; not a nonlinear perturbed-wave certificate',
        precision_bits=160,amplification_factors=factors,samples=samples,symbolic=symbolic_checks(),
        production_natural_blocks=[production_check(0.,0.),production_check(0.,4.),production_check(.2,1.3)],
        production_source=str(PROBE/'rerun_20261024.py'),production_source_sha256=hashlib.sha256((PROBE/'rerun_20261024.py').read_bytes()).hexdigest(),
        full_strip_note='Block lower triangular with repeated eigenvalues; no propagator upper bound is inferred from eigenvalues alone.')
    (HERE/'audit_linear_reference.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(dict(symbolic=result['symbolic'],matrix_discrepancies=[r['matrix_discrepancy'] for r in result['production_natural_blocks']],samples=len(samples)),indent=2))

if __name__=='__main__':main()
