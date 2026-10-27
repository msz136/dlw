# Finite regular Darboux constructions from heat seeds also force Laplace termination

2026-10-26. New algebraic extension for the actual prescribed independent initial data. This is a proof draft with exact symbolic checks. It does not exclude infinite dressing, a general integral binary transform not shown to factor into the transformations below, or a reference in an unrestricted weaker solution class.

## 1. Source and operator conventions

The primary source Maltseva–Popovych, arXiv:2103.08734v4 (2024), Section 8.2, presents two standard Darboux transformations and their finite Wronskian compositions for the spatial Lax operator

    L = D_X D_z + Q D_z + P.

Its potential q satisfies q_z=P. A nonzero auxiliary function phi solves L phi=0 and the corresponding time equation. Writing s=phi_X/phi and a=phi/phi_z, the spatial transformations are

    T1 psi = psi-a psi_z,
    Q1=Q-a_X/a,  P1=P-(aP)_z,

    T2 psi = psi_X-s psi,
    Q2=Q-(Q+s)_X/(Q+s),  P2=P+s_z.

Regularity means all denominators required by each intermediate transformation are nonzero on an open neighborhood containing t=0. The source gives sufficient transformation formulas, not an arbitrary Cauchy-data completeness theorem. Only this brief description uses the source; the termination argument below is derived here.

The two factorizable heat seed classes are P=0 and P=Q_z. The physical variables are Q=-u/2, P=(v-4-u_z)/4.

## 2. An arbitrary-function family forces a finite Laplace chain

All statements are local on an open regular patch. An arbitrary function means an arbitrary smooth function of the indicated one spatial variable; it is only used to compare differential coefficients in the spatial Lax equation. No well-posedness of a backward heat problem is assumed.

### Pure-X operators

Suppose a nonzero finite-order operator

    D = sum_(j=0)^N a_j(X,z) D_X^j

satisfies L(D f)=0 for every smooth f=f(X). Comparison of the coefficients of f^(N+1) and f^N gives

    (a_N)_z=0,
    (a_(N-1))_z=-P a_N                  (N>=1).

If P is nonzero, the regular forward Laplace transformation psi -> psi_z/P maps Df to another pure-X operator applied to f, of order N-1 and leading coefficient -a_N. For N=0, the coefficient equations give P a_0=0, so P=0 on any patch where a_0 is nonzero.

Thus a pure-X arbitrary-function family of order N forces forward Laplace termination after at most N regular steps. If an earlier invariant vanishes, termination already occurs there.

### Pure-z operators

Similarly, suppose

    E = sum_(j=0)^N b_j(X,z) D_z^j

satisfies L(E f)=0 for every f=f(z). The highest two coefficient equations are

    (D_X+Q)b_N=0,
    (D_X+Q)b_(N-1)=-(P-Q_z)b_N          (N>=1).

Writing K=P-Q_z, the regular inverse Laplace transformation psi -> (D_X+Q)psi reduces the pure-z order by one whenever K is nonzero. At order zero, K b_0=0. Consequently the inverse chain reaches K=0 after at most N steps, equivalent to the next inverse invariant P_next=0.

These statements require no bound on the coefficients of the arbitrary-function operators.

## 3. Finite regular Darboux transformations preserve such families

For the seed P=0, L=(D_X+Q)D_z and psi=f(X) is an arbitrary-function family, represented by the order-zero pure-X operator D=1.

Assume a current pure-X operator has order N with nonzero leading coefficient a_N. Since it represents solutions, (a_N)_z=0. Applying T1 yields D-a D_z, still of order N and with the same leading coefficient. Applying T2 yields (D_X-s)D, of order N+1 with that same nonzero leading coefficient. Therefore every finite regular composition of T1,T2 preserves a nonzero finite-order pure-X arbitrary-function family. Section 2 forces finite forward Laplace termination.

For the seed P=Q_z, L=D_z(D_X+Q). Choose a local nonzero R satisfying R_X=-Q R. Then psi=R(X,z) f(z) is an arbitrary-function family. Its pure-z operator is order zero.

For a current pure-z family of order N, (D_X+Q)b_N=0. T1 raises the order to N+1 with leading coefficient -a b_N, nonzero under regularity. T2 keeps order N with leading coefficient

    (b_N)_X-s b_N = -(Q+s)b_N,

which is nonzero because Q+s is precisely the required denominator of the regular T2 field transformation. Hence finite regular compositions preserve a nonzero pure-z family, forcing inverse Laplace termination.

The same argument also accommodates regular forward/inverse Laplace steps interspersed with the Darboux steps: in the corresponding arbitrary-function family, one Laplace direction lowers the order and the other increases it. A zero invariant ends the chain immediately.

## 4. Consequence for the prescribed independent data

The previous data-specific proof in ../../certificate_continuation/constructive_laplace_chain.md establishes that every finite integer-index Laplace invariant of the current independently perturbed A, D, Gaussian and sine initial data is a nonzero function. The initial fields are analytic, and each finite invariant is meromorphic on regular patches. Therefore a nonzero invariant cannot vanish identically on any open regular patch.

If any of these initial pairs were generated from a P=0 or P=Q_z heat seed by a finite composition of the regular standard Darboux transformations above, Section 3 would supply a finite-order arbitrary-function family. Section 2 would force a zero finite Laplace invariant, contradicting the data-specific result.

**Theorem.** For each of the current independently perturbed A/D/Gaussian/sine initial pairs, with nonzero real u-only or v-only perturbation, no finite regular composition of the two standard Darboux types, optionally interspersed with regular Laplace steps, generates the pair from either factorizable heat seed class. This includes finite Wronskian formulas whenever their factorization into elementary transformations is regular on such an initial open patch.

This strengthens the earlier finite-Laplace-only obstruction. In particular, replacing the failed heat/Laplace construction by an arbitrary finite Wronskian composition of these two Darboux types cannot solve the initial matching problem.

## 5. Scope that remains open

- A generic already nonterminating seed is outside this theorem. Constructing that seed with a certified evolution would itself require new initial-value information.
- An infinite determinant/dressing construction is not a finite differential operator and is not excluded.
- No claim is made for an integral binary transformation unless it is first shown to factor into the finite regular transformations above.
- Singular intermediate transformations, confluent limits, or removable denominators at t=0 require a separate extension argument. They are not covered automatically.
- The result is a construction-class obstruction. It does not prove nonexistence of the exact single-carrier perturbed IVP or yield a physical-field eta.

The finite-Darboux theorem uses only initial spatial Lax algebra, so it does not assume that the desired perturbed positive-time solution exists.

## 6. Reproducible checks

`finite_darboux_termination_check.py/json` verifies the exact spatial transformation identities (including nonzero auxiliary residuals), pure-X and pure-z leading coefficient formulas through orders 0–4, and family order preservation. The proof for every finite order is the coefficient argument above.

Primary source: https://arxiv.org/html/2103.08734v4, equations (69)–(73), Section 8.2. The source distinguishes these general Darboux transformations from Laplace transformations. The extension connecting their finite compositions to Laplace termination is derived in this note.
