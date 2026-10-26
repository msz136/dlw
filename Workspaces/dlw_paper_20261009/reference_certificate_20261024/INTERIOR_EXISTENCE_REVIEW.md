# Interior existence review for the approved reference problem

2026-10-24. Mathematical proof draft. This note does **not** establish existence or nonexistence for the prescribed sinusoidal or periodized-Gaussian interior data. It identifies exact reductions and a concrete failure of two tempting certification routes. The exact nonlinear example in Section 4 has different v data and is labelled accordingly.

## 1. The target and exact diagonal equations

Set z=y+2 in [0,4], e(z)=sin(pi z/4), a=2, and use periodic x of period 192. The requested data are

    sinusoid: u0=.03 e cos(omega x), v0=.02 e sin(omega x), omega=pi/12;
    Gaussian: u0=.05 e G, v0=.03 e G,
    G(x)=sum_m exp(-((x+192m)/6)^2).

The lower u trace is zero, and T=.01. The continuous equations are

    u_yt=-v_xx-[(u+4)u_y]_x,
    v_t=-u_xxy-[(u+4)v-4u]_x.

For a sufficiently regular solution, put p=u_y, R=p+v, S=v-p. Adding and subtracting the equations gives exactly

    R_t=-R_xx-[(u+4)R-4u]_x,
    S_t= S_xx-[(u+4)S-4u]_x,
    u(x,z,t)=1/2 integral_0^z (R-S)(x,s,t) ds.

Thus the interior contains both backward and forward parabolic components even before spatial discretization. This is an exact nonlinear identity, not an inference from Endpoint-SD.

The lower trace of u makes the nonlinear products disappear at z=0, explaining why the boundary formulas in BOUNDARY_THEOREM.md close. They do not close at a positive z.

## 2. A useful exact nonlinear transformation

Write w=S, and I for integration from z=0. The existing integral formulation is

    u_t=-u_xx-(u^2/2+4u)_x-I w_xx,
    w_t= w_xx-[(u+4)w-4u]_x.

On a local x chart, introduce a nonzero q with u=2 q_x/q. An x-independent time gauge can be chosen so that

    q_t=-q_xx-4q_x+Vq,
    V=-(1/2) I w_x.

Set r=(w-4)/q. Direct differentiation then gives

    r_t=r_xx-4r_x-Vr,
    V_y=-(qr)_x/2.

Indeed w-4=qr obeys (qr)_t=(q r_x-q_x r)_x-4(qr)_x, which equals w_xx-[(u+4)(w-4)]_x. The spatial mean of u is conserved. When this mean is nonzero, q is quasiperiodic; factoring out exp(mean(u)x/2) gives a periodic unknown with the corresponding constant-coefficient terms. In the sinusoidal case the mean is zero and q can be periodic without this step.

This transformation does not turn the requested problem into a known heat equation: V is unknown and coupled to q and r. Dropping V would change the nonlinear problem. It does, however, identify a natural place to investigate an integrable-data compatibility condition, or a validated forward/backward parabolic boundary-value formulation.

## 3. Why initial Fourier smoothness does not complete a certificate

### 3.1 Gaussian Fourier weights are not an algebra

Consider the Wiener norm sum_n |f_n| exp(sigma xi_n^2), sigma>0. It controls backward heat evolution for times less than sigma, but it is not a Banach algebra under multiplication: the ratio of the weight at n+m to the product of the weights is exp(2 sigma xi_n xi_m), unbounded for n=m tending to infinity. In particular, multiplying two coefficients with Gaussian exponent sigma yields a convolution whose exponent is only sigma/2.

For the approved G, Ghat_n=C exp(-9 xi_n^2). For even n, the m=n/2 contribution to the coefficient of G^2 already gives

    (G^2)hat_n >= C^2 exp(-(9/2)xi_n^2).

At an interior z with e(z) nonzero, the exact u_t at t=0 contains

    -(.05^2/2)e(z)^2 partial_x(G^2),

while the remaining terms are linear in G and have Gaussian exponent 9. Consequently u_t(0) is not in a Gaussian Fourier space with exponent greater than 9/2. A proof that merely propagates the initial exponent as 9-t and treats the nonlinear term as bounded in that same space is invalid.

This observation rules out that specific proof, not the existence of a solution in a different class. Nonlinear solution coordinates can have very different Fourier tails from physical fields.

### 3.2 Analytic Fourier weights control products but not backward heat

The analytic weight exp(sigma |xi_n|) is submultiplicative. However, no finite decrease in sigma absorbs exp(t xi_n^2) for t>0. The same problem holds for any fixed-order Sobolev weight. Thus replacing Gaussian weights with ordinary analytic weights does not repair a forward initial-value fixed-point argument.

For the actual sinusoidal data, the initially finite Fourier support is immediately lost. With A=.03 and B=.02,

    (R_t)_second-harmonic
       = A^2 omega e e' sin(2 omega x)
         - A B omega e^2 cos(2 omega x).

The two coefficients follow from -(u0 R0)_x and are nonzero in the interior. Finite support at t=0 therefore cannot be used as an exact Fourier truncation for the nonlinear reference.

These two facts explain why the previously proposed conditional Gronwall formula does not yet provide finite, validated continuum constants. Neither is a proof that the two requested solutions do not exist.

## 4. A rigorous nonlinear example showing that ordinary analytic data are insufficient

This subsection uses **different initial v data**. It is a counterexample to a proposed general analytic-data existence theorem, not a nonexistence result for the user's two cases.

Choose

    u0=A e(z) cos(omega x), v0=partial_y u0+4,

so w0=v0-u0_y=4. Assume a classical periodic solution on [0,T] with bounded coefficients sufficient for uniqueness of the forward parabolic equation for w-4. That equation is

    (w-4)_t=(w-4)_xx-[(u+4)(w-4)]_x.

An energy estimate, or forward parabolic uniqueness, gives w=4. The u equation therefore reduces at every fixed interior z to backward viscous Burgers with advection,

    u_t=-u_xx-u u_x-4u_x.

The mean of u is zero. The periodic positive Cole-Hopf variable, after scalar time gauge, satisfies

    q_t=-q_xx-4q_x,
    q(x,0)=exp(c sin(omega x)), c=A e(z)/(2 omega).

At any z with c nonzero, the magnitude of its Fourier coefficient at harmonic n is I_n(|c|). The defining positive series for the modified Bessel function gives

    I_n(|c|) >= (|c|/2)^n/n!.

Hence the magnitude at positive time would be

    exp(n^2 omega^2 t) I_n(|c|)
       >= exp(n^2 omega^2 t) (|c|/2)^n/n!.

This grows faster than every polynomial as n tends to infinity for each t>0. Fourier coefficients of a periodic distribution have at most polynomial growth. It contradicts the existence of the smooth, periodic Cole-Hopf variable obtained from a classical u solution. Thus these analytic physical initial data admit no such positive-time classical solution.

The example establishes that 'the profiles are analytic, so a standard local existence theorem applies' is false for the present PDE and boundary specification. It does **not** apply directly to the requested v0=.02 e sin or v0=.03 e G: neither makes w0=4, and their potential V in Section 2 is nonzero.

## 5. What a valid constructive route would have to add

A rigorous continuum certificate for the specified data must control the backward component by more than ordinary-norm truncation error. Two mathematically concrete routes remain:

1. Prove a data-specific nonlinear compatibility theorem in transformed variables (or via a spectral/integrable construction). It must show that the actual initial q,r lie on a class admitting the coupled positive-time evolution, bound that solution to T=.01, and enclose its unresolved modes. The Gaussian boundary width 9 and the sinusoidal boundary solution verify only the z=0 part of this requirement.

2. Solve a forward/backward parabolic problem with a terminal condition on the unstable component, validating the infinite-dimensional solution and its initial trace. To certify the specified initial-value problem, the initial trace must match the prescribed data exactly in the required class, or its mismatch must have a rigorously controlled Gaussian-type unstable tail. An ordinary small max-norm mismatch is insufficient. Arbitrarily choosing a terminal condition or filtering high modes produces a different problem.

Either route could support an a posteriori residual bound after its hypotheses are established. At present neither supplies a numeric eta for the original interior trajectory. Generating a fine mesh trajectory and assigning the finite-cutoff ODE estimate to the continuum would omit precisely the uncontrolled component above.

## 6. Review conclusion

The exact reductions and coefficient calculations are established algebraically. The nonlinear counterexample has a complete argument under the explicitly stated classical regularity/forward uniqueness assumptions. For the user's actual sinusoidal and approved periodized-Gaussian data, no data-specific positive-time existence theorem, infinite-tail enclosure, or numeric reference-error upper bound is obtained in this review. A claimed guaranteed reference at T=.01 cannot be justified from these results alone.
