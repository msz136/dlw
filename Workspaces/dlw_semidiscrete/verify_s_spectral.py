"""Exact spectral wave family on the Gram solution sector; not an IST solver."""
from fractions import Fraction as F
import sympy as s
from verify_gram_reassessment import Gram,add,mul,scale,der

def sub(p,q): return add(p,scale(q,-1))
def triple(p,q,r): return mul(mul(p,q),r)

cases=0
for N in range(1,6):
    for hh in (F(1,2),F(1,4),F(1,8)):
        for off in (0,1):
            g=Gram(N,8,hh,off); a=g.a; d=hh/2
            for j in (-1,1):
                G=g.tau(0,j,a); Gp=g.tau(0,j+1,a); Ft=g.tau(1,j,a-d)
                Fx=der(Ft)
                for zz in (F(11),F(13,2),F(-17)):
                    T=g.tau(1,j,zz); Tp=g.tau(1,j+1,zz)
                    # Heat equation on e^(zx-z^2t) T/G.
                    # Bilinear residual B_z(T,G), computed independently by rates.
                    from verify_gram_reassessment import bil
                    assert bil(T,G,zz)=={}
                    # (D+z-w)T/G = [F*T_x - F_x*T + (z-s)*F*T]/(F*G).
                    right=add(mul(Ft,der(T)),scale(mul(Fx,T),-1),scale(mul(Ft,T),zz-a+d))
                    left=add(mul(Ft,der(Tp)),scale(mul(Fx,Tp),-1),scale(mul(Ft,Tp),zz-a-d))
                    ratio=(zz-a+d)/(zz-a-d)
                    assert sub(scale(mul(left,G),ratio),mul(right,Gp))=={}
                    cases+=1
    print('PASS: heat and lattice spectral wave, N=',N,flush=True)

# General-N proof: rank-one lattice update, proved entrywise for symbolic spectra.
p,q,a,h,z=s.symbols('p q a h z'); d=h/2
chi=(p-a+d)*(q+a+d)/((p-a-d)*(q+a-d))
assert s.factor((chi-1)/(p+q)-h/((p-a-d)*(q+a-d)))==0
lam=(z-a+d)/(z-a-d)
assert s.factor((q+a+d)/((q+a-d)*(q+z))-(1/lam)/(q+z)-(h/(z-a+d))/(q+a-d))==0
print('PASS: rank-one lattice update and spectral partial fractions')

# Woodbury reduction of the lattice wave function.
B,C,D,E=s.symbols('B C D E')
eta=1-B; ell=z-a-d; L=1+h*C; phi=eta/L
cz=1/lam; ez=h/(z-a+d)
m=1-D
mp=1-cz*D-ez*B-h*eta*(cz*E+ez*C)/L
Y=1/ell-E
assert s.factor(lam*mp-m-h*phi*Y)==0
print('PASS: all-N Woodbury wave update')

# Differential identities imply exact spatial intertwining, without sampling.
J=s.symbols('J')
Cx=J+B*(1-J)+h*C
assert s.factor(Cx-(L-eta*(1-J)))==0
wm_minus_wp=-h+h*Cx/L
assert s.factor(wm_minus_wp+h*phi*(1-J))==0
Yx=m*(1-J)-ell*Y
res=wm_minus_wp*m+h*phi*(ell*Y+Yx)
assert s.factor(res)==0
print('PASS: all-N spectral lattice compatibility scalar cancellation')

# Spectral normalization and a nonconstant transmission factor already for N=1.
trans=(z-p)/(z+q)
assert s.factor(s.diff(trans,z)-(p+q)/(z+q)**2)==0
print('PASS: normalized soliton transmission depends nontrivially on z')
print('ALL SPECTRAL CHECKS PASSED;',cases,'exact parameter/step/site/spectral cases')
