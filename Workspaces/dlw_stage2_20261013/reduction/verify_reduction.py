"""Exact algebra and numerical checks for an inherited DLW travelling-wave annulus.

All symbolic assertions below are exact SymPy identities. Floating-point
elliptic evaluations check implementations; they are not the existence,
Jacobi, or Liouville proof (see report.md).
"""
from pathlib import Path
import csv
import json
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.special import ellipj, ellipk

OUT = Path(__file__).resolve().parent


def symbolic_checks():
    p, r, A, b, q, c, nu = sp.symbols("p r A b q c nu", nonzero=True, real=True)
    s = c*(r-nu*p)/(p*p-q*q)
    rprime = 2*p**3-(A*A+b*b)*p
    R2=(A*A-p*p)*(b*b-p*p)
    V2=(q*q-A*A)*(q*q-b*b)/(q*q)
    def reduce(expr):
        num=sp.together(expr).as_numer_denom()[0]
        num=sp.rem(num,r*r-R2,r)
        num=sp.rem(num,nu*nu-V2,nu)
        return sp.factor(num)
    sprime=sp.diff(s,p)*r+sp.diff(s,r)*rprime
    p_res=sp.factor(r-(nu*p+(p*p-q*q)*s/c))
    s_res=reduce(sprime-(c*p-nu*s-p*s*s/c))
    G=nu*p*s+(p*p-q*q)*s*s/(2*c)-c*p*p/2
    energy_res=reduce(G+c*A*A*b*b/(2*q*q))
    grad_p=c*p-p*s*s/c-sprime
    grad_s=(q*q-p*p)*s/c+r
    hp_res=reduce(grad_p-nu*s)
    hs_res=sp.factor(grad_s-nu*p)
    momentum_res=sp.factor(p*s-c*nu*p*p/(q*q-p*p)-c*p*r/(p*p-q*q))
    assert p_res==s_res==energy_res==hp_res==hs_res==momentum_res==0

    # A regular (c != 0) M=3 counterexample to single-site dynamical closure.
    h, f, fx, fxx = sp.symbols("h f fx fxx", nonzero=True, real=True)
    beta=h*h/32
    P=sp.eye(3)-sp.ones(3)/3
    R=sp.Matrix([[0,-1,1],[1,0,-1],[-1,1,0]])*h/6
    sv=sp.Matrix([0,f,-f]); sx=sp.Matrix([0,fx,-fx]); sxx=sp.Matrix([0,fxx,-fxx])
    w=sp.ones(3,1)*c+sv
    pt=-P*(2*beta*sp.matrix_multiply_elementwise(w,sx)+R*sxx)
    mean_ut=-sp.simplify((pt.dot(sv))/(3*c))
    U0t=sp.factor(pt[0]+mean_ut)
    target=h*fxx/3+8*beta*f*fx/3
    assert sp.simplify(U0t-target)==0

    # Small-modulus frequency twist: K(m)=pi/2*(1+m/4+O(m^2)).
    k, hh, cc, L, v0 = sp.symbols("k hh cc L v0", nonzero=True, real=True)
    Pm0=hh*cc*L*v0*k*k/(q*q)
    vm0=-k*k*(3*q*q-2*k*k)/(4*q*q*v0)
    twist=sp.factor(k*k*vm0/Pm0)
    expected=-k*k*(3*q*q-2*k*k)/(4*hh*cc*L*v0*v0)
    assert sp.simplify(twist-expected)==0
    bound=sp.Rational(200,19)*(sp.Rational(1,75)+sp.Rational(1,56))
    assert bound==sp.Rational(131,399)<1
    return {
        "profile_p_equation_residual":str(p_res),
        "profile_s_equation_residual":str(s_res),
        "profile_Hamilton_level_residual":str(energy_res),
        "physical_K_gradient_minus_nu_P_gradient":[str(hp_res),str(hs_res)],
        "momentum_total_derivative_identity":str(momentum_res),
        "M3_fixed_slice_counterexample_U0_t":str(U0t),
        "M3_sin_x_at_pi_over_2":"-h/3",
        "twist_limit":str(expected),
        "concrete_nondegeneracy_upper_bound_abs_nu_log_derivative":str(bound),
        "concrete_lower_bound_J_log_derivative":"1/m >= 20 on 0<m<=1/20",
        "passed":True,
    }


C,H,L=-4.0,2.0,2*np.pi
BETA=H*H/32
Q=abs(H*C)/4
K0=2*np.pi/L


def family(m,x,phi=0.0):
    K=ellipk(m)
    b=4*K/L
    A=np.sqrt(m)*b
    nu=np.sqrt((Q*Q-A*A)*(Q*Q-b*b))/Q
    sn,cn,dn,_=ellipj(b*(x-phi),m)
    p=A*sn
    px=A*b*cn*dn
    s=C*(px-nu*p)/(p*p-Q*Q)
    sx=C*p-nu*s-p*s*s/C
    return p,s,px,sx,nu,b,A


def charges(m,n=4096):
    x=np.arange(n)*L/n
    p,s,px,sx,nu,b,A=family(m,x)
    mom=2*H*L*np.mean(p*s)
    # Physical Hamiltonian minus its fixed background constant.
    kappa=C*p*p/2-p*p*s*s/(2*C)+BETA*C*s*s+s*px
    energy=2*H*L*np.mean(kappa)
    nn=A*A/(Q*Q)
    Pi=quad(lambda theta: 1/((1-nn*np.sin(theta)**2)*np.sqrt(1-m*np.sin(theta)**2)),0,np.pi/2,epsabs=2e-13,epsrel=2e-13)[0]
    closed_mom=8*H*C*nu/b*(Pi-ellipk(m))
    return mom,energy,closed_mom


def derivative5(fun,m,eps=2e-5):
    return (fun(m-2*eps)-8*fun(m-eps)+8*fun(m+eps)-fun(m+2*eps))/(12*eps)


def numerical_checks():
    n=1024
    x=np.arange(n)*L/n
    kk=2*np.pi*np.fft.fftfreq(n,d=L/n)
    kk[n//2]=0
    def D(a):return np.fft.ifft(1j*kk*np.fft.fft(a,axis=-1),axis=-1).real
    def invD(a):
        mul=np.zeros(n,dtype=complex)
        mask=kk!=0
        mul[mask]=1/(1j*kk[mask])
        return np.fft.ifft(mul*np.fft.fft(a,axis=-1),axis=-1).real
    Eminus=np.array([[0,1],[1,0]])
    d=(np.eye(2)-Eminus)/H
    avg=(np.eye(2)+Eminus)/2
    rows=[]
    for m in [.002,.005,.01,.02,.05]:
        p,s,px,sx,nu,b,A=family(m,x)
        U=np.stack((p-p*s/C,-p-p*s/C))
        w=np.stack((C+s,C-s))
        Ux=np.stack((px-(px*s+p*sx)/C,-px-(px*s+p*sx)/C))
        wx=np.stack((sx,-sx))
        Ut,wt=-nu*Ux,-nu*wx
        original1=d@(Ut+D(U*U/2+BETA*w*w))+D(D(d@U+avg@w))
        original2=wt+D(U*w)-D(D(w))
        mom,energy,closed=charges(m)
        Pm=derivative5(lambda z:charges(z)[0],m)
        Hm=derivative5(lambda z:charges(z)[1],m)
        eps=min(2e-5,m/1000)
        tangent_m=derivative5(lambda modulus:np.array(family(modulus,x)[:2]),m,eps)
        tangent_phi=-np.stack((px,sx))
        # i_X omega=dH convention; original normalized J=-offdiag(D).
        omega_phi_m=-2*H*L*np.mean(invD(tangent_phi[1])*tangent_m[0]+invD(tangent_phi[0])*tangent_m[1])
        omega_expected=2*H*L*np.mean(s*tangent_m[0]+p*tangent_m[1])
        numu=derivative5(lambda z:family(z,np.array([0.0]))[4],m)
        row={"m":m,"amplitude_A":float(A),"b":float(b),"velocity":float(nu),
             "momentum_full":float(mom),"relative_K_full":float(energy),
             "momentum_closed_formula_error":float(abs(mom-closed)),
             "P_derivative_m":float(Pm),"K_derivative_minus_velocity_P_derivative":float(Hm-nu*Pm),
             "original_eq1_linf":float(np.max(np.abs(original1))),
             "original_eq2_linf":float(np.max(np.abs(original2))),
             "mean_p":float(np.mean(p)),"mean_s":float(np.mean(s)),
             "omega_phi_m":float(omega_phi_m),"omega_pullback_error":float(abs(omega_phi_m-omega_expected)),
             "omega_minus_momentum_derivative":float(omega_phi_m-Pm),
             "twist_dOmega_dI":float(K0*K0*numu/Pm),
             "min_abs_w":float(np.min(np.abs(w)))}
        rows.append(row)
        assert abs(mom-closed)<2e-11
        assert abs(Hm-nu*Pm)<2e-7
        assert max(row["original_eq1_linf"],row["original_eq2_linf"])<2e-8
        assert row["omega_pullback_error"]<2e-11
        assert Pm<0
    return rows


def main():
    symbolic=symbolic_checks()
    numeric=numerical_checks()
    with (OUT/"elliptic_family_checks.csv").open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(numeric[0]));writer.writeheader();writer.writerows(numeric)
    result={"symbolic":symbolic,"numerical":numeric,
            "concrete_parameters":{"c":C,"h":H,"L":L,"q":Q,"m_domain":"0<m<=1/20", "mean_p":0,"mean_s":0,"gamma":0},
            "twist_limit_concrete":"5/(96*pi)",
            "interpretation":"Exact inherited one-degree-of-freedom physical-time annulus. The proof is in report.md; floating samples are only implementation checks."}
    (OUT/"verification.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":main()
