# A constructive reduction using time padding and conditional uniqueness

2026-10-26. New analytic proof draft. This is a reduction of the fixed-data
existence/certification problem, not an attained reference certificate. No
uniform sequence satisfying the hypotheses below has been verified for the
actual independent perturbations.

## 1. Purpose and the new missing gate

The current matching approach seeks an exact terminal trace G whose mixed
solution has A(0)=A0. An infinite-dimensional inverse estimate would suffice,
but is not the only possible constructive route.

Instead choose a longer interval S=.02 and retain the requested final time
T=.01. Construct a sequence of exact mixed-time solutions on [0,S] with
exact B(0)=H, initial A mismatch delta_n tending to zero, and ONE uniform
analytic-x / bounded-z norm bound. A conditional uniqueness estimate makes
this sequence Cauchy on every shorter [0,T]. This can construct the fixed
initial-value solution up to T without an inverse on the entire terminal
tail. The hard gate becomes **uniform bounded approximate matching**, not
the mere solution of each finite matching problem.

This route has not been checked for the actual data. In particular, a
bounded sequence of finite-grid ODE trajectories is not the required
sequence of continuous mixed solutions.

## 2. Full nonlinear difference and norms

Use the shifted exact equations

    A_t=-A_XX-(u A)_X,
    B_t= B_XX-(u B)_X,
    u=(1/2) integral_0^z(A-B), z in [0,Z], Z=4.

Let Z1=(A1,B1), Z2=(A2,B2) be two exact mixed solutions. Write W=Z1-Z2,
w=(1/2)J(a-b), and let

    H=L2(T_L x [0,Z];R2), normalized by 1/(L Z),
    D=diag(-partial_XX,+partial_XX).

Their exact difference equation is

    W_t=D W+C(t)W,
    C(t)W=-partial_X[u1 W+w Z2].                         (P1)

The difference is exact, with the nonlinearity included in the coefficient
u1. Suppose each complete trajectory has Fourier Wiener norm at most R
with analytic radius rho, where that norm sums |A| and |B| and takes the
supremum in (z,t) coefficientwise. Then

    ||C(t)W||_H <= c1 ||W_X||_H+c0 ||W||_H,

    c1=R[Z/2+sqrt(2) Z/pi],
    c0=c1/(e rho).                                      (P2)

The exact Volterra L2 norm is ||J||=2Z/pi; hence ||(1/2)J(a-b)||<=sqrt(2)Z/pi
times the pair norm. The direct bound ||u1||infinity<=ZR/2 and the analytic
multiplier sup_r r exp(-rho r)=1/(e rho) prove P2. No x differentiation is
applied to unknown W in the zero-order part beyond the displayed W_X.

The pair difference obeys ||W(t)||_H<=M:=2R. Its time derivative satisfies

    ||W_t||_H<=Lw:=2[a2 R+Z a1 R^2],
    a1=1/(e rho), a2=4/(e^2 rho^2).                     (P3)

This follows by estimating the right-hand side of each full exact equation
using its analytic Wiener norm, then adding the two trajectory bounds.

## 3. Explicit Carleman estimate including nonzero initial mismatch

Assume the stable initial data agree exactly: b(0)=0. Let

    delta=||W(0)||_H=||a(0)||_H,
    c=4c1^2+1, phi(t)=exp(-ct), K=8c1^4+4c0^2.

Choose T<s<S and a C1 cutoff chi equal to one on [0,s], zero at S, with
|chi'|<=Hchi. The cubic smoothstep on [s,S] gives Hchi=3/[2(S-s)].
For lambda>0 put Y=exp(lambda phi)chi W and Dlambda=D+lambda phi' I.
Integration by parts for the selfadjoint D gives the exact identity

    integral ||Y_t-Dlambda Y||^2
      = integral [||Y_t||^2+||Dlambda Y||^2
                  +lambda phi'' ||Y||^2]
        + <Y(0),Dlambda(0)Y(0)>.                        (P4)

Because b(0)=0, <W(0),D W(0)>=||a_X(0)||^2>=0. Therefore the boundary
term is bounded below by -lambda c exp(2lambda)delta^2. This favorable
sign is why an exact B(0) is useful; no initial derivative mismatch norm
is required.

The interpolation identity ||Y_X||^2=<|D|Y,Y> and Young's inequality give

    2||C Y||^2 <= (1/2)||Dlambda Y||^2
             +[8c1^4+4c0^2+4c1^2 lambda |phi'|]||Y||^2.

Use Y_t-Dlambda Y=C Y+exp(lambda phi)chi'W. For

    lambda >= lambda_min:=2 K exp(cS)/c,

one obtains, after absorbing the coefficient terms,

    Q_T:=integral_0^T ||W(t)||_H^2 dt
      <= [4 exp(cS)Hchi^2(S-s)/(lambda c)] M^2
             exp(-2lambda[phi(T)-phi(s)])
        +2 exp(cS)delta^2 exp(2lambda[1-phi(T)]).        (P5)

Every term in P5 is explicit. The maximum norm of the time cutoff is one.
The cutoff error is supported in [s,S], giving the strict positive gap
phi(T)-phi(s).

For delta<M choose

    lambda=log(M/delta)/(1-phi(s)),
    theta=[phi(T)-phi(s)]/[1-phi(s)] > 0.

Provided lambda>=lambda_min, P5 becomes

    Q_T <= exp(cS)[4Hchi^2(S-s)/(lambda c)+2]
                  M^[2(1-theta)] delta^[2theta].        (P6)

For larger delta, simply use Q_T<=TM^2. As delta tends to zero, P6 tends
to zero, regardless of the lack of a bounded terminal matching inverse.

The Lipschitz bound P3 gives a pointwise endpoint bound

    ||W(T)||_H <= max(2 sqrt(Q_T/T),(8Lw Q_T)^(1/3)).    (P7)

Indeed, if h=||W(T)|| and h/(2Lw)<=T, its norm is at least h/2 on a final
interval of length h/(2Lw), yielding Q_T>=h^3/(8Lw). Otherwise it is at
least h/2 on the entire interval and Q_T>=Th^2/4. Both cases give P7.
This is intentionally elementary; stronger pointwise logarithmic convexity
could improve the exponent, but is not assumed here.

## 4. Concrete conditional scales

Take R=.4, rho=.1, Z=4, S=.02, s=.015 and T=.01. These are compatible
with the existing mixed contraction theorem when its data norm condition
||G||rho+||H||rho<=.3 holds. The accompanying Arb script outward-encloses
c1,c0,c,K,lambda_min,theta,Lw and evaluates P5-P7 for representative delta.

The printed table is a conditional comparison of TWO exact mixed solutions
in this ball. It is not an error certificate for the current numerical
reference. In particular, it supplies no terminal G matching A0.

## 5. Existence by a bounded approximate-matching sequence

Suppose there are exact continuous mixed solutions Zn on [0,S] with

    Bn(0)=H exactly,
    ||An(0)-A0||_H -> 0,
    sup_n ||Zn||rho <= R.

Apply P6-P7 to pairs n,m. Their initial difference is at most the sum of
the two matching errors, and all constants are uniform. This gives Cauchy
convergence in C([0,T];H) for every T<S. Explicitly, any maximum of
||W(t)|| on [0,T] has at least one side interval of length T/2. The same
Lipschitz argument as P7 gives the uniform bound

    sup_(0<=t<=T)||W(t)||_H
        <=max(sqrt(8 Q_T/T),(8Lw Q_T)^(1/3)).

This tends to zero with Q_T. The uniform analytic-x bound also gives
Cauchy convergence of every finite x derivative in smaller analytic strips
by finite-mode interpolation plus a uniform tail estimate. The Volterra
map gives convergence of u uniformly in z after x interpolation. One can
pass P1's original full nonlinear equations to the limit in H, obtaining
a strong-in-x, L2-in-z solution with the prescribed full initial data.

The limit is bounded in L-infinity(z,x,t) by weak-star compactness. It
need not have continuous v in z merely from these hypotheses. A uniform
finite transverse derivative bound on the matching sequence would promote
the convergence to a physical-field maximum-norm statement. That bound is
additional information, and the existing no-Gevrey theorem does not supply
it or rule out a fixed finite derivative bound.

To avoid overclaiming: this argument is a sufficient reduction, not a
verified existence proof for the actual data. Passing to a weaker z class
does not by itself satisfy the user's requested maximum-field reference.
The physically relevant gap is now explicit: construct the uniformly
bounded approximate-matching sequence, and, for a sharp max-norm v
reference, prove enough uniform transverse regularity or a direct uniform
convergence estimate. Existing finite retained-mode Newton solutions and
tiny first-correction tails do not yet establish either condition.

## 6. Why this is progress and what it does not repair

This replaces the need for a globally bounded inverse of the smoothing
matching map by an overspecified-time compactness/conditional-stability
criterion. Time padding is essential: at T=S the exponent theta vanishes,
and the residual no-go mechanism is recovered. At the requested final time
strictly inside a uniformly controlled longer interval, initial matching
can control the difference.

The new gate is not automatically easier to prove: an exact datum outside
the range will force any approximate-matching sequence out of the uniform
ball. Monitoring finite approximants can expose that behavior, but proving
a bound for all approximants still needs analysis. No value of eta_u or
eta_v is assigned here.
