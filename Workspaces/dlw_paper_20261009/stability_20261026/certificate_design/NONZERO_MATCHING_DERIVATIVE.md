# Initial matching at a nonzero benchmark

2026-10-26. Proof development, with outward-rounded constants. This note advances the initial matching problem for independently perturbed physical fields. It gives the exact nonzero-base derivative, an analytic smoothing theorem with explicit hypotheses, and a data-specific first-order sideband calculation. It does not yet certify the perturbed continuous IVP.

## 1. Exact derivative of the matching map

Use the shifted variables and mixed problem of `INDEPENDENT_PERTURBATIONS.md`. Fix H=B(0), let (Abar,Bbar) be a mixed solution with terminal datum Gbar, and put ubar=(1/2) integral_0^z(Abar-Bbar). For a terminal variation g, the exact linearized mixed problem is

    a_t = -a_XX - partial_X(ubar*a + w*Abar),
    b_t =  b_XX - partial_X(ubar*b + w*Bbar),
    w   = (1/2) integral_0^z(a-b),
    a(T)=g,  b(0)=0.                                           (D1)

The matching derivative is DF_H(Gbar)g=a(0). Thus it includes both the transport by the evolving nonzero wave and the variation of the velocity itself. The latter produces w*Abar and w*Bbar. Omitting either would change the matching problem.

Writing S(t)=exp(t partial_XX), the equivalent Duhamel equations are

    a(t)=S(T-t)g + integral_t^T S(s-t) partial_X(ubar*a+w*Abar)(s) ds,
    b(t)=          -integral_0^t S(t-s) partial_X(ubar*b+w*Bbar)(s) ds. (D2)

## 2. Nonzero coefficients still give exponential compression of x tails

Let X_rho have norm sum_n exp(rho |xi_n|) sup_z |f_n(z)|. For trajectories the supremum is also over t. Suppose the *nonzero* base satisfies

    ||(Abar,Bbar)||_(rho+sigma) <= R,  sigma>0.                 (D3)

Set

    rho(t)=rho+sigma(1-t/T),
    h_sigma=sqrt(T) exp(sigma^2/(2T)),
    L_sigma=4 R h_sigma.

If L_sigma<1, then (D2) has a unique solution in this time-dependent analytic norm and

    ||DF_H(Gbar)g||_(rho+sigma)
       <= C_sigma ||g||_rho,
    C_sigma=exp(sigma^2/(4T))/(1-L_sigma).                     (D4)

**Proof.** For a backward heat segment of length r=s-t, increasing the analytic radius contributes exp(sigma r |xi|/T). Young's inequality gives

    exp(-r xi^2 + sigma r |xi|/T)
       <= exp(sigma^2/(2T)) exp(-r xi^2/2).

The time-integrated differentiated heat multiplier therefore has norm at most h_sigma. Forward b segments see a decreasing radius and obey the smaller ordinary heat bound. The terminal term is bounded by exp(sigma^2/(4T))||g||_rho. At each time multiplication is a Banach algebra, ||ubar||<=2R, and ||w||<=2||(a,b)||. Hence the sum of the two nonlinearized products is bounded by 4R||(a,b)||. Contraction proves (D4).

For T=.01, rho=sigma=.1 and R=.4, 256-bit Arb verifies

    h_sigma < .164873,
    L_sigma < .263796,
    C_sigma < 1.744115.                                       (D5)

Consequently, for an x-frequency cutoff K,

    ||P_(|xi|>K) DF_H(Gbar)g||_rho
       <= 1.744115 exp(-.1 K) ||g||_rho.                      (D6)

This is stronger than a finite-order smoothing estimate. It also shows that the map cannot have a bounded inverse onto the entire same-radius X_rho space: its range lies in the strictly smaller analytic class X_(rho+sigma). It does **not** prove that the exact smoothing rate is Gaussian, or determine every singular value.

Only x tails have been controlled. With continuous z, finite x truncation still leaves an infinite-dimensional transverse space, so (D6) alone is not a claim of compactness in all variables. With a fixed finite-dimensional transverse discretization it gives compactness and exponentially small approximation numbers in x.

There is also a same-space high-input conclusion requiring only the original radius-.1 base ball. Apply (D4) with input radius 0, output radius .1 and sigma=.1. If ||(Abar,Bbar)||_.1<=.4 and g_N is supported at the single x frequency xi_N, normalized by ||g_N||_.1=1, then

    ||g_N||_0=exp(-.1|xi_N|),
    ||DF_H(Gbar)g_N||_.1 <=1.744115 exp(-.1|xi_N|).           (D6a)

Uniqueness of (D2) identifies this solution with the derivative in the original radius-.1 space. Thus DF is not bounded below there even with the full nonzero coefficients. This conclusion requires no transverse compactness and no radius-.2 base enclosure. It is valid for every nonzero mixed solution in the original .4 ball. The stronger-radius condition (D3) is needed only for the earlier same-input-radius gain statement (D4) with rho=.1 and sigma=.1.

Condition (D3) is an explicit verification task. It follows for every mixed solution whose *stronger-radius* data satisfy ||Gbar||_(rho+sigma)+||H||_(rho+sigma)<=.3, by the earlier .4-ball theorem. The actual explicit Gaussian/sine benchmark has not yet been enclosed in that stronger ball in this work. The constants in (D5) therefore remain conditional for that particular benchmark. The formula for its exact derivative (D1) is unconditional.

## 3. A calculated sideband for the actual benchmark family

This calculation checks the effect of the nonzero wave instead of replacing it by a constant background. Scale the current benchmark amplitude by lambda:

    u0=lambda f(z) F0(X),  v0=4-3lambda f'(z)F0(X),
    f(z)=sin(pi z/4).

For one Fourier coefficient c_q of F0, the exact first derivatives of the base at lambda=0 are

    Abar_1,q(t)=-2 f' c_q exp(q^2 t),
    Bbar_1,q(t)=-4 f' c_q exp(-q^2 t),
    ubar_1,q(t)=f c_q[-exp(q^2 t)+2exp(-q^2 t)].              (D7)

For terminal variation g=phi(z) exp(ikX), the zero-base mixed variation is

    a_0(t)=phi exp(-(T-t)k^2) exp(ikX),  b_0=0,
    w_0(t)=(1/2) Iphi exp(-(T-t)k^2) exp(ikX),
    Iphi(z)=integral_0^z phi(s) ds.

Inserting (D7) into (D2) gives the exact first derivative with respect to lambda of DF at the sideband p=k+q:

    d_lambda[DF g]_p|_0
      = i p c_q exp(-T k^2)
        {-(f phi+f' Iphi) J(2kq) +2 f phi J(2q(k+q))},
    J(d)=(1-exp(-Td))/d, J(0)=T.                            (D8)

This includes the w*Abar contribution. It is an exact perturbation coefficient of the current nonzero benchmark family, not a finite-difference fit. For the sine case q=pi/12 and c_q=1/2. For the Gaussian case q=n*pi/96 and c_q=(sqrt(pi)/32)exp(-9q^2); each nonzero q contributes (D8).

Take phi=sin^2(pi z/4), the transverse envelope used in the experiments. At z=2, f=phi=1 and f'=0. After multiplying the output by the naive inverse heat factor exp(Tp^2), the coefficient is

    i p c_q exp(T(p^2-k^2))[-J(2kq)+2J(2q(k+q))].            (D9)

For fixed q>0 and k tending to infinity, its magnitude is asymptotic to

    |c_q| exp(T(2kq+q^2))/(2q).                             (D10)

Thus the first amplitude derivative of the inverse-heat-preconditioned matching operator is unbounded in the same exponential Wiener norm. The factor exp(rho q) for the change from k to k+q does not remove the growth. A uniform small-amplitude operator-norm perturbation argument around the diagonal inverse heat operator therefore cannot be justified by this first-order expansion. This does **not**, by itself, prove that the full operator at a fixed nonzero amplitude has the same asymptotic, nor prove nonexistence of the IVP.

For the actual sine amplitude lambda=.03, the first-order preconditioned sideband contributions at z=2 are

| terminal carrier k | first-order contribution |
|---|---:|
| pi/2 (the current perturbation carrier) | 2.758343e-4 |
| pi/.1 | 5.161461e-3 |
| pi/.05 | 1.119972e-2 |
| pi/.025 | 2.670886e-2 |

These are coefficients in the linear matching derivative, not physical errors in an experiment. They quantify a specific change needed in a tail preconditioner: variable-coefficient sidebands must be included. The retained-mode Jacobian is not diagonal even for initially single-carrier independent perturbations.

## 4. Precision scales for the constant-state linear mechanism

At u=0,v=4, the matching multiplier for A is exp(-T xi^2). For T=.01 and resolved cutoff K=pi/dx, the exact inverse amplification and required initial A-mode matching precision for a terminal A-mode tolerance 1e-10 are

| dx | exp(TK^2) | 1e-10 exp(-TK^2) |
|---|---:|---:|
| .1 | 1.933369e4 | 5.172319e-15 |
| .05 | 1.397202e17 | 7.157166e-28 |
| .025 | 3.810971e68 | 2.624003e-79 |

This table is a *linear constant-state scale*, not the singular spectrum of the nonzero Gaussian, sine or soliton matching map. It is also not a claim that the actual calculation contains Nyquist-size errors.

For comparison, replacing partial_XX by a centered second difference changes the largest growth exponent to 4T/dx^2. Its corresponding amplifications are 54.5982, 8.886111e6 and 6.235149e27. That finite-grid scale must not be presented as the continuum scale.

The 1e-10 tolerance in the table belongs to one transformed A-mode. For the transverse shape phi=sin^2(pi z/4), a pure matching error a with b(0)=0 at the constant state gives ||delta u||<=||a|| and ||delta v||<=||a||/2, so it also provides a simple sufficient field scale. Arbitrary transverse profiles require their own integration factor, and the full nonzero variational problem requires the coupled a,b estimate.

## 5. A checkable certificate target and its unclosed part

For a terminal approximation Ghat, an injective left preconditioner L defined on the residuals, and terminal Banach space X, a Newton map is

    N(G)=G-L(F_H(G)-A0).

A concrete sufficient a posteriori condition is

    ||L(F_H(Ghat)-A0)|| <= Y,
    ||I-L DF_H(Ghat)|| <= Z0,
    sup_(||d||<=r) ||L(DF_H(Ghat+d)-DF_H(Ghat))|| <= Z2*r,
    Y+(Z0+Z2*r)*r < r,  Z0+Z2*r < 1.                       (D11)

Then N contracts the r-ball and injectivity of L gives exact initial matching. All three estimates must include the infinite Fourier tail and the continuous z dependence. Enclosing a retained Jacobian supplies only the finite block of Z0.

The new findings locate the missing part more precisely. An x-analytic tail upper bound on DF is available under (D3), but it is an upper bound for a smoothing operator and supplies no inverse tail bound. The actual first sideband (D8) prevents treating the inverse tail as an unmodified diagonal inverse heat multiplier by a bounded small-perturbation argument. Consequently the infinite-tail pieces of Y and Z0 in (D11) have not yet been bounded for the selected independent data. No admissible r or full-field eta has been obtained.

The A/D solitons require their own nonzero-base bounds and transverse boundary problem. Neither the small v=4 ball nor the numerical table of constant-state heat multipliers is a certificate for those solitons.

`matching_conditioning.py/json` reproduces the outward-rounded constants and the finite sideband evaluations. The status remains `certified=false`, `eta_u=null`, `eta_v=null`.

Independent review: the moving-radius multiplier bound, contraction constant and high-input corollary were checked by the stability audit agent on 2026-10-26. The first sideband calculation is a self-checked proof calculation at this stage.
