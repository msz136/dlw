# Independent audit of finite regular Darboux termination

2026-10-26. Audit of `FINITE_DARBOUX_TERMINATION.md`. The theorem is valid
with its explicitly stated local regularity and elementary-transformation
scope. This is an independently checked proof draft, not formal
verification and not a general fixed-data nonexistence theorem.

## 1. Checks of the arbitrary-function argument

Let `L=D_X D_z+Q D_z+P`, `K=P-Q_z`.

For a pure-X operator `D=sum a_j D_X^j` satisfying `L(Df)=0` for every
smooth f(X), the top coefficient gives `(a_N)_z=0`. The next coefficient,
after using that identity, gives `(a_(N-1))_z=-P a_N`. Hence the forward
Laplace map `psi -> psi_z/P` reduces the order by exactly one with leading
coefficient `-a_N`, wherever P and a_N are nonzero. At order0, the two
coefficient equations give `P a_0=0`; on a nonzero leading-coefficient
patch this forces `P=0`.

For a pure-z operator `E=sum b_j D_z^j`, the top equation is
`(D_X+Q)b_N=0`. Differentiating that equation in z shows
`L b_N=(P-Q_z)b_N=K b_N`. Therefore the next coefficient is
`(D_X+Q)b_(N-1)=-K b_N`. The inverse map
`psi -> (D_X+Q)psi` reduces order by exactly one with leading coefficient
`-K b_N`. At order0, `K b_0=0` forces `K=0`; this is the next inverse
Laplace invariant being zero.

The argument holds for every finite order, not only the orders covered by
symbolic spot checks. If an invariant vanishes on the patch before order
zero, the required termination has already been reached. If an invariant
is not identically zero but has zeros, restrict the patch to its nonzero
set before the next regular step. For the final actual analytic data,
their nonzero meromorphic invariants cannot vanish on any open patch.

## 2. Independent verification of the Laplace maps

The exact forward transformed operator is

    Lplus=D_X D_z+(Q+(log P)_X)D_z+P+Q_z+(log P)_Xz,

and it obeys the off-shell identity

    Lplus(psi_z/P)=partial_z[(L psi)/P].

For the inverse transformation,

    Lminus=D_X D_z+(Q-(log K)_X)D_z+K,

one has

    Lminus[(D_X+Q)psi]
       =(D_X+Q-(log K)_X)(L psi).

Thus the stated arbitrary-function order reductions really map spatial
solutions to the transformed spatial Lax equation. No time equation for
every member f is required: the family is only used as an algebraic
invariant of each fixed-time spatial operator. The auxiliary function
used to construct the Darboux field transformation must still satisfy
the source's spatial and time equations.

## 3. Both Darboux types preserve the needed nonzero family

For the P=0 seed, `psi=f(X)` starts a pure-X order0 family. Under T1,
`D-a D_zD` retains its order and leading coefficient because
`(a_N)_z=0`. Under T2, `(D_X-s)D` increases order by one with the same
nonzero leading coefficient.

For the P=Q_z seed, choose local nonzero R with `R_X=-Q R`.
Then `psi=R f(z)` is a pure-z order0 family. Under T1, the leading
coefficient becomes `-a b_N` at order N+1. Under T2, it becomes
`-(Q+s)b_N` at order N. These are nonzero under exactly the assumed
regularity: `a=phi/phi_z` is defined and nonzero, and Q+s is the
denominator required by the T2 field transformation.

Regular forward/inverse Laplace steps can also be interspersed. In the
pure-X family the forward direction lowers order and the inverse
direction raises it; in the pure-z family the directions are reversed.
Their leading factors remain nonzero on a regular patch. The final
finite-order family forces termination in the corresponding direction.

## 4. Consequence and exact scope

The supplied data-specific nontermination result for A/D/Gaussian/sine
then contradicts any such finite regular construction from either seed
class. This is a genuine extension of the earlier finite-Laplace-only
result. In particular, a regular finite Wronskian representation that
factors into these elementary types is excluded for the exact prescribed
independent perturbation data.

The known unperturbed nondegenerate Gaussian/sine initialization has a
terminating chain and is compatible with this construction class. Its
existence does not contradict the obstruction after the independent
perturbation is introduced.

No strengthening to every finite expression labelled “Darboux” is
justified. In particular, integral binary transformations not proved to
factor into these regular elementary types, singular intermediate
transformations, confluent/removable limits, nonterminating seed data,
and infinite dressing remain outside the audited theorem. Nor does the
absence of this finite construction imply nonexistence of a continuous
solution or impossibility of all error certificates.

## 5. Reproducible outcome

The parent script `finite_darboux_termination_check.py` was rerun
independently: all26 recorded checks passed. An additional independent
script `finite_darboux_audit_check.py/json` verifies the two off-shell
Laplace identities and the pure-z coefficient simplification. The
transformation formulas and all-order leading-coefficient induction
are consistent. No correction to the theorem was required.
