# No robust initial-value neighborhood for the same independent envelope

2026-10-26. Independently derived finite-jet proof and exact symbolic checks.
This result concerns open neighborhoods of the initial data. It does not
settle existence for the exact pure-carrier datum itself.

## 1. Equation, traces and solution class

Work on the periodic X torus of length 192, `z in [0,4]`, `0<=t<=T`, with
`T>0`, `u(X,0,t)=0`. Set

    A=u_z+v-4, B=v-u_z-4, u=(1/2) integral_0^z(A-B),
    A_t=-A_XX-(uA)_X, B_t=B_XX-(uB)_X.

For j<=m write `a_j=partial_z^j A(X,0,t)/j!` and similarly b_j. Require
these finite jets to be C1 in time with values in continuous periodic
functions, C0 in time with values in C2 periodic functions, with mixed
derivatives commuting so that the differentiated PDE is valid at z=0.
For u-only perturbations m=1 suffices; for v-only perturbations m=2 suffices.
In physical fields this involves u up to z order 2 or 3, and v up to order
1 or 2, together with the stated x/time regularity. These are finite
classical regularity requirements, not analyticity or all-order Gevrey
assumptions.

The exact triangular boundary equations are

    a_j,t=-a_j,XX-partial_X sum_(ell=1)^j
                    ((a_(ell-1)-b_(ell-1))/(2 ell)) a_(j-ell),
    b_j,t= b_j,XX-partial_X sum_(ell=1)^j
                    ((a_(ell-1)-b_(ell-1))/(2 ell)) b_(j-ell).

For j=0 the sums are empty. The lower u trace is essential: it removes
an additional zeroth-order transport coefficient from this hierarchy.

## 2. Perturbation with exactly the current transverse envelope

Let `alpha=pi/4`, `phi(z)=sin²(alpha z)`. Fix any positive periodic
frequency d (an integer multiple of pi/96) and any rho>0, and put

    H_rho(X)=sum_(n>=1) exp(-rho n) cos(ndX).

This is a real periodic analytic function, analytic for
`|Im X|<rho/d`. With r=exp(-rho), an exact closed expression is

    H_rho=(r cos(dX)-r²)/(1-2r cos(dX)+r²).

For eta!=0 alter a target initial datum in either independent direction:

    u-only:  delta u0=-eta phi H_rho, delta v0=0;
    v-only:  delta u0=0, delta v0=-eta phi H_rho.

This preserves the same phi envelope, independence of the physical fields,
the physical initial endpoint values, and the initial lower A/B traces.
It also preserves u_z at both initial transverse endpoints in the u-only
case because phi'=0 there. Both solutions, if they exist, have the same
prescribed lower u trace for every time.

These are perturbations of the FULL prescribed datum. That target may be
the current Gaussian or sinusoidal background plus its selected pure
carrier perturbation. No special Gaussian frequency property is required.

## 3. First changed boundary jet evolves by backward heat exactly

Assume a target solution and a solution for the neighboring datum both
belong to the finite-jet class above. Denote their jet differences by delta.

### u-only

The initial changes are exactly

    delta a0=delta b0=0,
    delta a1=-2 eta alpha² H_rho,
    delta b1=+2 eta alpha² H_rho.

Since a0,t=-a0,XX and b0,t=b0,XX, equal initial a0,b0 imply equality for
all times: Fourier coefficients solve scalar ordinary differential
equations, including the backward heat equation; uniqueness for a putative
classical solution needs no forward boundedness theorem.

The nonlinear forcing in the a1 equation is

    -partial_X[(a0-b0)a0/2],

and therefore cancels exactly between the two solutions. Hence

    delta a1,t=-delta a1,XX,
    [delta a1(t)]_(nd)=-eta alpha² exp(td²n²-rho n).       (R1)

For every t>0 these Fourier coefficients grow faster than any polynomial.
They cannot be Fourier coefficients even of a periodic distribution,
contradicting the assumed continuous boundary jet.

### v-only

Now the initial changes are

    delta a0=delta b0=delta a1=delta b1=0,
    delta a2=delta b2=-eta alpha² H_rho.

First a0,b0 agree; then the a1,b1 forcing agrees and the scalar Fourier
uniqueness argument makes a1,b1 agree. The nonlinear a2 forcing is

    -partial_X[(a0-b0)a1/2+(a1-b1)a0/4].

It also cancels exactly. Consequently

    delta a2,t=-delta a2,XX,
    [delta a2(t)]_(nd)=-(eta alpha²/2)
                            exp(td²n²-rho n).            (R2)

This again is not a distribution at any positive time. Thus both the target
and neighboring datum cannot admit solutions in the specified finite-jet
class, for either independent physical-field direction.

## 4. Arbitrarily small in standard initial-data norms

For every fixed finite C^r norm on the complete (X,z) initial fields,
phi H_rho has finite norm, so its eta multiple tends to zero with eta.

For any prescribed finite x-analytic strip width s>0, choose rho>ds.
In the analytic Wiener norm the exact x factor is

    ||H_rho||_s=sum_(n>=1) exp(-(rho-ds)n)
                 =1/(exp(rho-ds)-1).

Every fixed number of transverse derivatives only multiplies this by the
finite corresponding phi derivative norm. Thus the changes also tend to
zero in any fixed x-analytic-strip norm with finite transverse regularity.
By embedding, the same conclusion applies to fixed finite Sobolev norms.

The scalar eta need never be numerically representable: the theorem concerns
arbitrarily small exact analytic perturbations of specified initial data.
The initial functions themselves have an explicit rational-trigonometric
expression, rather than an unspecified formal tail.

## 5. Precise theorem and implications

**Theorem.** Fix T>0 and a datum that admits a solution in the stated
finite-jet class with lower u trace zero. In every neighborhood of that
datum, measured by any fixed finite C^r or x-analytic-strip norm as above,
there is an explicitly described neighboring datum, with exactly the same
transverse phi envelope and independent u-only (respectively v-only)
change, that admits no solution in that class on [0,T].

If the target itself admits no solution in the class, it already has no
reference in that class. Otherwise the theorem excludes an open-neighborhood
existence theorem or a reference-error certificate that promises a solution
and a finite error guarantee for every exact input inside a positive-radius
uncertainty ball in those norms.

This conclusion applies conditionally to BOTH present Gaussian and sine
targets, including their independent pure-carrier perturbations, because
the forcing cancels by comparison. It does not require positivity or
frequency isolation of the background, and it does not use linearization:
the low boundary-jet equations are exact consequences of the full nonlinear
PDE.

There are also fully explicit examples with no conditional existence premise:
start from either of the known UNPERTURBED Gaussian/sine continuous solutions
constructed in `../../reference_certificate_20261024/nondegenerate_benchmarks/PROOF.md`.
Those solutions have the required finite jets. Therefore their initial data
plus either of the independent phi H_rho changes above admit no solution in
the stated finite-jet class for any eta!=0. This is a concrete nonexistence
result for arbitrarily small analytic perturbations of the current baselines.
Its x carrier is the specified analytic harmonic tail; it is not a
nonexistence proof for the currently simulated single cosine carrier.

The result does not claim that the particular exact pure-carrier target has
no solution. It does not exclude certification based on an exact special
formula or a priori admissible infinite-tail restrictions. A Gaussian
Fourier weight strong enough to suppress exp(td²n²), or a restricted
finite-frequency data manifold, lies outside the neighborhoods considered
here. It also does not address weaker solutions without the required finite
transverse boundary jets.

## 6. Optional strengthening: identical initial values on any finite x grid

Fix a finite collection of initial x sample positions X_1,...,X_m, including
the union of all grids whose initial field values are supplied to a verifier.
Replace H_rho by P H_rho, where

    P(X)=product_(j=1)^m sin²(d(X-X_j)/2).

Then the entire physical initial perturbation is exactly zero at every
specified x position, for every z. It still uses the same transverse phi
envelope and remains arbitrarily small in the norms of Section 4.

This replacement does not remove the backward-heat contradiction. Let
`P(X)=sum_(ell=-m)^m p_ell exp(i ell dX)` and let r=exp(-rho). For n>m,
all n-ell are positive, so

    [P H_rho]_(nd)=(r^n/2) sum_(ell=-m)^m p_ell r^(-ell)
                  =(r^n/2) P_L(r^-1),

where P_L(w)=sum p_ell w^ell is the Laurent polynomial of P. Each sine-squared
factor equals a nonzero constant times

    w^-1 (w-exp(i dX_j))².

All roots of P_L lie on the unit circle. Since r^-1>1, P_L(r^-1)!=0.
The large positive-frequency tail is therefore a fixed nonzero complex
constant times exp(-rho n). Equations (R1)/(R2) still produce
exp(td²n²-rho n), which is not a distribution at positive time.

If finitely many initial x derivatives are sampled as well, replace each
sine-squared factor by a sufficiently high even power. Its zeros then
annihilate those derivatives, while the same Laurent-root argument keeps
the high-frequency geometric coefficient nonzero.

Thus finite exact initial samples, even together with arbitrarily tight
finite-norm uncertainty, cannot distinguish the target from a neighboring
analytic datum without a reference in the finite-jet class. This is a
statement about finite information and an unrestricted analytic tail; exact
knowledge of a complete special initial formula is additional information.

## 7. Verification and scope

`robust_same_envelope_check.py/json` verifies the normalized sine-squared
coefficients and the exact cancellation of all nonlinear fluxes needed at
orders one and two. The Fourier contradiction and smallness argument are
analytic proofs; no spatial discretization enters them. This is an
independently reasoned proof draft, not a formal proof-assistant result.
