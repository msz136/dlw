# A data-specific obstruction to finite heat/Laplace reconstruction

2026-10-26. This is a new exact result about the prescribed independent physical-field perturbations. It excludes finite termination of the particular Laplace chain used to construct the certified unperturbed Gaussian/sine reference. It does not prove nonexistence of the perturbed DLW solution, and it does not exclude an unrelated exact representation or an infinite inverse-scattering construction.

## 1. Fixed initial data and the known linearizable seed

Write X=x-4t, z=y+2, kappa=pi/4 and k=pi/2. The current benchmarks have

    u_b=A sin(kappa z) F(X),
    v_b=4-3 A kappa cos(kappa z) F(X),

at t=0, with F the specified sine or periodic Gaussian. The independent perturbations under consideration are

    u_0=u_b+epsilon_u phi(z) C(X),
    v_0=v_b+epsilon_v phi(z) C(X),
    phi=sin^2(kappa z),  C=cos(kX),                          (L1)

where (epsilon_u,epsilon_v) is real and nonzero. The two separate experiments set one epsilon to zero. No initial data are altered in the argument.

The BLP variables for the physical fields are

    Q=-u/2,  P=(v-4-u_z)/4,

and satisfy

    Q_zt=(Q^2-Q_X)_Xz+2P_XX,
    P_t=P_XX+2(QP)_X.                                    (L2)

The Laplace transformation used in the existing benchmark construction is

    Q*=Q+(log P)_X,  P*=P+Q*_z.                           (L3)

Only logarithmic derivatives occur; they mean P_X/P and are independent of a branch of the complex logarithm wherever P is nonzero. The seed used previously has P=Q_z. Its scalar equation can be reduced by Cole-Hopf to a linear heat equation with a potential independent of z.

## 2. Exact inverse recurrence

Number inverse transformations by j. Let Q_0=-u/2, P_0=(v-4-u_z)/4. Inverting (L3) gives

    P_(j+1)=P_j-(Q_j)_z,
    Q_(j+1)=Q_j-(log P_(j+1))_X.                          (L4)

Consequently

    P_1=(v-4+u_z)/4,
    P_(j+2)=2P_(j+1)-P_j+(log P_(j+1))_Xz.                (L5)

These relations also determine the chain in the opposite direction whenever the relevant invariant is nonzero. A finite chain reaches the old seed P_j=(Q_j)_z exactly when P_(j+1)=0. A seed with P_j=0 already has a zero invariant. Thus a zero P_j at some finite integer index is necessary for representation by a finite sequence of these Laplace transformations from either terminating seed.

For the unperturbed separated data, P_0=-u_b,z and P_1=-u_b,z/2. The mixed logarithmic derivative of u_b,z=A kappa cos(kappa z)F(X) vanishes, hence P_2=0 identically. This is the finite termination behind the previous heat representation.

## 3. The independent perturbations make the chain nonterminating

**Theorem.** For (L1), with real (epsilon_u,epsilon_v) not both zero, every finite integer-index invariant P_j in (L5) is nonzero as a function. Therefore the data cannot be generated from the terminating P=0 or P=Q_z seeds by a finite sequence of the transformations (L3) and (L4).

**Proof.** Put w=exp(i kappa z). All the initial expressions are Laurent polynomials in w with X-dependent coefficients:

    sin(kappa z)=(w-w^-1)/(2i),
    cos(kappa z)=(w+w^-1)/2,
    phi=(2-w^2-w^-2)/4,
    phi_z=(i kappa/2)(w^-2-w^2).                           (L6)

The unperturbed terms have only powers w^(-1), w and hence are of lower order at w=0 than the perturbations. In a neighborhood of any real X where C(X) is nonzero,

    P_0=c_0(X) w^-2+O(w^-1),
    P_1=c_1(X) w^-2+O(w^-1),
    c_0=C[-epsilon_v/16-i kappa epsilon_u/8],
    c_1=C[-epsilon_v/16+i kappa epsilon_u/8].               (L7)

If P_j=c_j(X)w^-2(1+O(w)) with c_j nonzero, then

    (log P_j)_z=-2i kappa+O(w),
    (log P_j)_Xz=O(w).                                    (L8)

This follows directly from partial_z=i kappa w partial_w. The remainder and the required X derivatives are uniform on a small X neighborhood avoiding zeros of c_j. The operations in (L5) preserve rational dependence on w, so the expansions remain meromorphic Laurent expansions.

The logarithmic term cannot change the w^-2 coefficient. By induction in both integer directions,

    c_j=2c_(j-1)-c_(j-2)
       =C[-epsilon_v/16+(2j-1)i kappa epsilon_u/8].         (L9)

For real epsilons and integer j, this coefficient is nonzero: its real and imaginary parts could both vanish only if epsilon_v=0 and (2j-1)epsilon_u=0, and 2j-1 never vanishes at an integer. Quantitatively,

    |c_j| >= |C| sqrt(epsilon_v^2/256+kappa^2 epsilon_u^2/64)>0.

Thus the induction never encounters an identically zero invariant. Each P_j has a genuine pole of order two at w=0 and cannot be the zero function. This proves the result. In terms of z=iR the pole is the nonzero exp(2 kappa R) leading term. The proof uses the rational initial-data expressions, not an assumption that a future solution exists at complex z. End proof.

For the separate experiments the leading terms are particularly simple:

    v-only: P_j ~ -epsilon_v C exp(2 kappa R)/16,
    u-only: P_j ~ (2j-1)i kappa epsilon_u C exp(2 kappa R)/8.

The theorem holds for any sufficiently differentiable F(X) in the separated base; in particular it covers both current sine and periodic Gaussian profiles with their original amplitudes. It applies for every nonzero perturbation size, including 1e-6.

## 4. Extension to the actual A/D soliton initializations

The same obstruction also applies to the current A/D continuous Gram profiles, using a different initial-data argument. This does not invoke the small v=4 mixed-problem ball.

The continuous Gram phases have transverse exponents

    gamma_i=1/(p_i-2)+1/(q_i+2).

For A, (p,q)=(1,2), so gamma=-3/4. For D, (p_1,p_2)=(1,4), (q_1,q_2)=(2,-3), so the two exponents are -3/4 and -1/2. Every term in either tau determinant therefore has imaginary y period 8*pi. The tau functions, reconstructed physical fields and their derivatives return to the same values after y -> y+8*pi*i*n. On a small complex neighborhood of a real point the tau denominators stay uniformly away from zero, because the real profiles are regular and the translated germs are identical.

Let the actual transverse perturbation envelope be sin^2(kappa*(y-y_L)), with any kappa>0 (including the domain-dependent kappa used in the soliton experiment). Along this sequence of imaginary translates the unperturbed fields and all fixed-order derivatives stay bounded, while the perturbation has a nonzero exp(2*kappa*8*pi*n) leading term. On each translated neighborhood this leading term separates into a function of X and exp(-2i*kappa*(y-y_L)). Its mixed logarithmic derivative vanishes; the lower terms contribute a quantity tending to zero.

Inducting through (L5) therefore gives precisely the coefficients (L9), now along the translated neighborhoods rather than in a single Laurent variable. For each fixed integer j, P_j has the nonzero growing leading term and cannot vanish identically. Thus the current independently perturbed A and D data also cannot reach a zero invariant by any finite number of the specified Laplace transformations.

The conclusion uses the actual continuous Gram exponents. It does not assert that a discrete tau lattice or a time-stepping approximation has been certified.

## 5. What this decides for the reference construction

One inverse Laplace step no longer reaches the old scalar linearizable relation. More strongly, adding finitely many such steps cannot restore it. The obstruction is the leading transverse harmonic in the initial invariants, not a lack of numerical precision or a poor choice of the number of heat modes.

It remains possible that the independently perturbed problem has a continuous solution admitting a nonterminating representation, an infinite determinant, or a validated nonlinear initial-matching construction. None of those is supplied by this theorem. The full nonlinear reference certificate therefore still has `eta_u=null` and `eta_v=null`.

The assertion is deliberately specific to the Laplace chain (L3). A general Darboux transformation need not coincide with this chain; no impossibility is claimed for all transformations bearing that name. Section 4 covers the current A/D backgrounds separately through their exact imaginary period.

## 6. General dressing and the lower-regularity possibility

The [Garagash 1995 dissertation synopsis](https://fizmathim.com/pryamaya-i-obratnaya-zadachi-dlya-2-1-mernogo-nelineynogo-uravneniya-blp), chapters 3–4, treats whole-plane Schwartz potentials relative to an operator with constant term 1. It assumes unique solvability of the resolvent integral equations and excludes extra singularities. Its evolution analysis imposes additional spectral decay and compatibility conditions. These hypotheses do not supply a periodic-strip kernel bound or an initial-data matching theorem for (L1). Constructing a direct Lax resolvent at a fixed auxiliary spectral value would not establish the required time-evolved inverse reconstruction. No calculable general dressing kernel with a proved time interval and physical error enclosure for the present data has been obtained here.

The finite-chain obstruction also leaves open a reference in a weaker transverse class. The mixed-time contraction uses C_z and the Volterra operation u=(1/2) integral_0^z(A-B); it does not require analyticity or Gevrey bounds in z. A theorem that the actual evolved solution cannot be finite-Gevrey in z would therefore not by itself contradict that mixed theorem or exclude a C-infinity, non-Gevrey matched terminal G. Conversely, specifying all boundary jets or a Borel extension only fixes jets. A flat remainder can still change the interior matching function. No full-interval inverse estimate follows from the Volterra structure alone, and the smoothing x-frequency inverse remains to be bounded on the actual range.

`constructive_laplace_checks.py/json` verifies the inverse recurrence algebra, the transformed initial invariants, unperturbed termination, the leading-coefficient recurrence, and the A/D imaginary-period exponents. The proof of nontermination for every finite integer j is the induction above. The Gaussian/sine asymptotic argument was independently reviewed by the stability audit agent on 2026-10-26, with the scope restriction in this section. The extension in Section 4 is a self-reviewed proof at this stage.
