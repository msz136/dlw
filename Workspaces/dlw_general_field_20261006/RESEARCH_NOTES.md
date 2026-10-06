# General periodic DLW field: direct verification and analytic boundary

Date: 2026-10-06. Research notes, not an independent-reviewed theorem. 

## Scope

Period M>=2 in j, period L in x, h>0. U=u+2a, w=v-delta0 u-4, beta=h²/32. Fix lattice averages Pi w=c !=0 and Pi(Uw)=gamma. Write p=P0 U, s=w-c, b=(gamma-Pi(ps))/c, U=b+p. p,s are arbitrary smooth periodic fields with zero lattice averages; x means may be fixed as Casimirs. Pair variational gradients using h sum_j integral.

R=(delta_- restricted to P0)^-1 M_-P0 is a finite skew matrix. Define
H0=h sum integral e,
e=U²w/2+beta w³/3+w U_x+w R w_x/2,
K=H0-gamma h sum integral U.
Jred=-[[0,P0 D],[P0 D,0]].

Direct chain rule, using Pi(Uw-w_x-gamma)=0, gives
K_p=Uw-gamma-w_x,
K_s=P0(U²/2+beta w²+U_x+R w_x).
Thus
p_t=-D P0(U²/2+beta w²+U_x+R w_x),
s_t=-D(Uw-w_x).
This fixes the actual mean closure and reproduces the implicit physical equations. Jred is constant skew, hence Poisson; its component x means are Casimirs. The momentum Pmom=h sum integral ps generates negative x translation, so it commutes with every translation-invariant differential functional, including K.

## Explicit two-site system and fresh exact certificate

For M=2, use p0=p,p1=-p,s0=s,s1=-s. R=0. Let b=(gamma-ps)/c, U0=b+p,U1=b-p,w0=c+s,w1=c-s. K/(2h), up to a constant, has density
kappa = c p²/2 -(gamma-ps)²/(2c)+beta c s²+s p_x.
Use the normalized scalar bracket -D swap with this normalized K. Then
p_t=-p_xx-(gamma/c)p_x+(p²s/c)_x-2 beta c s_x,
s_t= s_xx-(gamma/c)s_x-c p_x+(ps²/c)_x.
No soliton ansatz is imposed.

two_site_exact.py verifies by identically vanishing Euler derivatives that integral p, integral s, integral ps, integral kappa and the restriction of Q4 are conserved. Parameters and all jets remain symbolic. Q4 in full fields is
h sum integral [U³w/3+(2 beta/3)Uw³+2UwU_x-(4/3)U_xw_x+UwR w_x].

## New explicit rational Lax form on the full two-site field space

eta=hc/8, B=gamma/(2c), C=B-ps/c,
f=p/2-eta,
g=-s_x/c+(1-s²/c²)(p/2+eta).
Let the original transfer factors be T_j=(D-U_j/2+hw_j/8)^-1(D-U_j/2-hw_j/8), M=T1 T0. An exact first-order-factor inversion gives
L=(-4eta)(M-I)^-1+(B-2eta)I = D-f(D-C)^-1 g.
This is valid as a formal PDO for c!=0 and arbitrary p,s. It extends the earlier s=0 independence witness to the whole two-field chart.

For clarity, set sigma_x=C and
sigma_t=A=-[8c²eta²-2c²p²+4c p s_x-4c p_x s-8eta²s²+gamma²-4gamma ps+6p²s²]/(4c²).
Exact jet calculations give C_t=A_x. Define q=f exp(sigma), r=g exp(-sigma). They satisfy
q_t=-q_xx+2q²r,
r_t= r_xx-2qr².
This follows from three polynomial identities in p,s and their jets, checked exactly; the proof does not divide by f. Therefore L=D-q D^-1 r satisfies
L_t=[-(L²)_+,L]
to all orders by the rank-one PDO identity. sigma is generally quasiperiodic, but f,g,C and all L coefficients are periodic; no periodic gauge is asserted. This is a forward differential/gauge map, with no inverse or surjectivity theorem asserted.

All fixed-order I_n=(1/n) integral res L^n are therefore genuine finite differential-polynomial functionals of smooth periodic p,s and are conserved for every smooth solution on its existence interval. Full-series analytic convergence is unnecessary for each individual coefficient. The first two Lax coefficient identities are also directly certified in the script.

## General M hierarchy and prior proofs checked

For finite M let G=hMc/4 !=0 and B=gamma/(2c). The ordered monodromy has leading coefficients
M=I-G D^-1+(G²/2-GB)D^-2+... .
Define L=-G(M-I)^-1+(B-G/2)I =D+sum_{r>=1} ell_r D^-r.
The periodic full-intertwiner construction yields L_t=[-D²-V0,L]. Its order-zero identity yields (V0)_x=2(ell1)_x, hence the same negative KP t2 Lax equation (the spatial constant commutes).

The existing all-order bracket proof uses opposite free-field factor brackets, multiplication/inversion of the Adler map, and gauge invariance to transfer trace involution to this exact Jred. The underlying primary theorem is Mas--Ramos, The Constrained KP Hierarchy and the Generalised Miura Transformation, Theorems I/II, https://arxiv.org/html/q-alg/9501009v2 . It proves the factorization rule; identifying it with DLW is our calculation.

The previous independence argument on s_j=0, p0=2b,p1=-2b,other p=0 gives for J_k=Tr L^(2k+1)/(2k+1):
J_k quadratic top derivative term = (2/M)(-1)^(k+1) integral (D^k b)².
Distinct Fourier frequencies give a Vandermonde determinant for any finite block, hence generic arbitrarily large independent blocks on the fixed uniform-component-mean leaf. This is not a spectral-completeness theorem. It does not count different powers of one invariant as independent.

Prior low-order Q5 formulas require a mean-square correction; bare Q5 fails. Rechecked old numerical AD probes on M=3,4,5,7: corrected pair brackets were approximately 1e-12 or smaller, whereas uncorrected Q5 brackets were O(1)-O(10). Exact symbolic Q5 BCH certificate rerun separately. These probes supplement algebraic arguments.

## NEW analytic obstruction: unbounded high-frequency growth

At uniform equilibrium p=s=0, U=V=gamma/c, w=c, consider Fourier mode exp(i k x+i theta j), theta=2pi m/M !=0. The R symbol is -i h cot(theta/2)/2. The linearized generator is
A(k,theta)=[ [k²-iVk, -2i beta c k +k² R(theta)],[-ick,-k²-iVk] ].
Exactly,
lambda_±=-iVk ± sqrt(k⁴-(hc/2)cot(theta/2)k³-(h²c²/16)k²).
For every fixed nonzero lattice mode, the positive real part grows like k² as |k| grows. linearized_all_periods.py verifies the characteristic polynomial symbolically.

Consequences: for any t>0 the linearized solution operator is unbounded H^s->H^s, for every finite s. Consequently an ordinary local H^s flow differentiable at this equilibrium, whose derivative is this linearized solution operator, cannot exist on a full open neighborhood. This conclusion concerns real physical time and the stated real phase space. It is stronger than merely saying global existence is unproved; it supplies a specific obstruction. It is not, by itself, a full nonlinear norm-inflation theorem or a proof excluding all weaker notions of solution.

For M=2 the discriminant is k⁴-4eta² k². For c=-4,h=1/8 it is k⁴-k²/64. The split heat/backward-heat character is also explicit in the q,r equations above.

Thus the algebraic commuting hierarchy can be established for general periodic fields and evaluated on all smooth solutions, while a global analytic Liouville/action-angle theory on an unrestricted ordinary Sobolev neighborhood needs a fundamentally different analytic setting. Local conservation laws and Poisson identities do not ensure well-posed dynamics.
