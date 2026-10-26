# Actual-data compatibility review

2026-10-24. New mathematical proof draft for the **actual sinusoidal initial data**. This note does not certify the reference trajectory. It proves a loss of every finite Gevrey order in the transverse boundary jets, conditional on existence of a sufficiently smooth solution. It does not prove nonexistence in a merely smooth or finite-regularity class. No corresponding result is obtained here for the approved periodic Gaussian.

## 1. Prescribed problem and conclusion

Write z=y+2 in [0,4], kappa=pi/4, omega=pi/12, and A=.03. The prescribed sinusoidal data are

    u(x,z,0)=A sin(kappa z) cos(omega x),
    v(x,z,0)=.02 sin(kappa z) sin(omega x),
    u(x,0,t)=0.

The x period is 192; these data have the smaller period 24. Suppose a periodic classical solution exists on [0,T], with all transverse derivatives and enough x,t regularity to differentiate the equations and take their lower-boundary traces. Then, for every fixed t>0, the derivatives of u in z at z=0 cannot satisfy

    sup_x |partial_z^n u(x,0,t)| <= C B^n (n!)^s

for any finite constants C,B and any finite Gevrey order s. In particular the solution cannot have analytic or finite-order Gevrey regularity in z uniformly in x on a neighborhood of the lower boundary at a positive time.

This is a statement about this initial datum, rather than the different-v Burgers counterexample in INTERIOR_EXISTENCE_REVIEW.md. Its scope must nevertheless be kept precise: C-infinity functions can have jets larger than every Gevrey bound, so this is not a proof of classical nonexistence. It rules out an analytic/Gevrey-y solution class as the route to certifying this prescribed problem.

## 2. Closed hierarchy of exact boundary jets

Use the exact variables

    R=u_z+v, S=v-u_z, u=1/2 integral_0^z (R-S) ds.

In the advected coordinate X=x-4t the exact nonlinear equations are

    R_t=-R_XX-(u R)_X+4u_X,
    S_t= S_XX-(u S)_X+4u_X.

Define normalized boundary jets

    R_m(X,t)=partial_z^m R(X,0,t)/m!,
    S_m(X,t)=partial_z^m S(X,0,t)/m!,
    U_j(X,t)=partial_z^j u(X,0,t)/j!
            =(R_(j-1)-S_(j-1))/(2j),  j>=1,
    U_0=0.

Their exact equations are triangular in m:

    (R_m)_t=-(R_m)_XX-partial_X sum_(j=1)^m U_j R_(m-j)+4 partial_X U_m,
    (S_m)_t= (S_m)_XX-partial_X sum_(j=1)^m U_j S_(m-j)+4 partial_X U_m.

At m=0, the sums and U_0 term vanish. Initially every jet contains only the fundamental harmonics +/-omega. By induction R_m,S_m contain no harmonics larger than (m+1)omega, and U_j contains none larger than j omega. This follows from the triangular equations and the scalar Fourier ODE for each harmonic; it does not assume that the full fields have a convergent Taylor series in z.

Let r_m,s_m be the positive highest-harmonic coefficients, at frequency (m+1)omega. The 4 partial_X U_m term has frequencies at most m omega and does not contribute. To reach the highest harmonic in a product U_j R_(m-j), both factors must use their positive highest harmonics. Consequently

    r'_m=(m+1)^2 omega^2 r_m
           -i(m+1)omega sum_(j=1)^m [(r_(j-1)-s_(j-1))/(2j)] r_(m-j),
    s'_m=-(m+1)^2 omega^2 s_m
           -i(m+1)omega sum_(j=1)^m [(r_(j-1)-s_(j-1))/(2j)] s_(m-j).

Put c=A kappa/2>0. The actual data give

    r_0(0)=c, s_0(0)=-c,
    r_m(0)=s_m(0)=0 for m>=1.

The second statement concerns their highest harmonic m+1, not the whole initial jet. The prescribed v data do contribute fundamental-frequency terms to higher jets, but cannot enter this highest-harmonic hierarchy. Thus the argument uses the actual prescribed v; it does not replace v by u_z+4 or by another special datum.

## 3. Positivity and quantitative growth

Set

    r_m=(-i)^m a_m, s_m=-(-i)^m b_m.

The hierarchy becomes a real triangular system

    a'_m=(m+1)^2 omega^2 a_m
         +(m+1)omega sum_(j=1)^m [(a_(j-1)+b_(j-1))/(2j)] a_(m-j),
    b'_m=-(m+1)^2 omega^2 b_m
         +(m+1)omega sum_(j=1)^m [(a_(j-1)+b_(j-1))/(2j)] b_(m-j).

In particular a_0=c exp(omega^2 t), b_0=c exp(-omega^2 t), and all a_m,b_m are nonnegative. The j=1 term yields

    a'_m >= (m+1)^2 omega^2 a_m+(m+1)omega c a_(m-1),

because (a_0+b_0)/2=c cosh(omega^2 t)>=c. Induction, dropping the positive linear growth only during the first part of the interval, gives for every delta>0

    a_m(delta)>=(m+1)c^(m+1)(omega delta)^m.

Then retain the linear growth from delta to t and choose delta=t/2:

    a_m(t)>=(m+1)c^(m+1)(omega t/2)^m
                   exp((m+1)^2 omega^2 t/2).                (A1)

This bound is deliberately elementary; it is not an estimate of the moderate-resolution numerical coefficients.

## 4. Consequence for transverse regularity

The positive n-th harmonic of U_n is

    (r_(n-1)-s_(n-1))/(2n)
       =(-i)^(n-1)(a_(n-1)+b_(n-1))/(2n).

A Fourier coefficient has magnitude no greater than the sup norm. Hence (A1) gives the explicit derivative lower bound

    sup_x |partial_z^n u(x,0,t)|
       >= (n!/2)c^n (omega t/2)^(n-1)
                    exp(n^2 omega^2 t/2).                  (A2)

For every finite s, the logarithm of the right side grows as omega^2 t n^2/2+O(n log n), whereas log(C B^n (n!)^s)=O(n log n). Thus (A2) contradicts every finite-order Gevrey-y bound at t>0.

The transport X=x-4t changes only Fourier phases, so the sup-norm bound applies in the original x coordinate. The reasoning holds at T=.01 as well as at any other positive time.

## 5. What this adds to the reference-certificate problem

1. The actual sinusoidal datum has a compatibility issue stronger than the generic observation that backward diffusion is present: its exact boundary-jet hierarchy is incompatible with every finite-order Gevrey dependence on y at positive time.
2. A continuum verifier cannot assume a geometric Chebyshev tail in y, or a stretched-exponential tail implying finite Gevrey regularity, for this initial-boundary problem. A small finite tail in the computed polynomial does not validate such an assumption for the exact solution.
3. The calculation still does not rule out a C-infinity, non-Gevrey solution, a finite-regularity solution, or a certificate established in an appropriately weaker class. Borel-type smooth functions can have arbitrarily fast-growing endpoint jets. Therefore it must not be presented as a proof that the requested continuous solution does not exist.
4. No finite numeric upper bound eta_u or eta_v follows from this result. It supplies a rigorous exclusion of a candidate proof class, not the requested error certificate.
5. For the approved periodic Gaussian, the highest-harmonic induction above is unavailable because its initial Fourier support is infinite. Its all-frequency compatibility remains unresolved here.

There is no justified fixed-positive-y positivity argument in this note. Only the highest Fourier harmonic of each transverse boundary jet has the sign structure used above. Lower harmonics contain the 4u_X coupling, the prescribed v quadrature phase, negative-frequency interactions, and alternating transverse derivatives of sin(kappa z). Summing the divergent transverse Taylor series is invalid. A possible smooth solution could contain contributions flat at z=0 that the entire jet hierarchy does not determine. These points prevent promotion of (A2) to nonexistence of a classical solution or a lower bound on the actual finite-resolution reference error.

## 6. Algebraic checks and status

The normalized-jet equations follow by the ordinary Leibniz rule after division by m!. For m=1 the formula predicts a_1'(0)=b_1'(0)=2 omega c^2, so the coefficient of sin(2 omega x) in (U_2)_t at t=0 is 2 omega c^2=A^2 kappa^2 omega/2. This agrees with the z^2 coefficient of the exact nonlinear term -u u_x at t=0. The recurrence and lower bound use no floating-point trajectory or fitted constant.

An independent agent algebraically reviewed the PDE signs, transport, factorial normalization, highest-harmonic closure, initial v-phase exclusion, phase factors, positivity and the n!/2 bound, and found no discrepancy. This is an internal mathematical review, not an external theorem verification.

Status: internally reviewed proof draft of the conditional actual-sinusoid non-Gevrey result above; no actual-data existence theorem and no certified reference-error upper bound. Independent mathematical review is appropriate before including this result in a paper.
