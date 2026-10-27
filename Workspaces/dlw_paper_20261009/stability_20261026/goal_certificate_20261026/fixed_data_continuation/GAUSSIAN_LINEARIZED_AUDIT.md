# Independent audit of the actual Gaussian single-carrier obstruction

2026-10-26. Independent mathematical audit of
`GAUSSIAN_PURE_CARRIER_LINEARIZED_OBSTRUCTION.md`. This is a proof audit,
not proof-assistant verification and not an independent rerun of the full
2026-10-24 Arb reference certificate.

## Verdict and scope

The stated no-classical-first-variation theorem is supported by the
argument. I found no sign, time-direction, Gaussian-width, Bloch-kernel,
or entire-order error. The stated finite-classical-norm obstruction is
also justified; its compactness passage can be made more direct using
the exact transformed defects, as detailed below.

These results concern the actual amplitude-zero Gaussian benchmark and
the two exact directions

    (du0,dv0)=(sin²(pi z/4) cos(pi X/2),0),
    (du0,dv0)=(0,sin²(pi z/4) cos(pi X/2)).

They do not establish nonexistence at the isolated amplitude 1e-6, do not
exclude a nondifferentiable solution family, and do not exclude a bound
using only the undifferentiated physical maximum norm. In particular,
they do not certify a perturbed continuous reference or a numerical
reference error eta.

## Exact algebra and coverage

I reran `gaussian_linearized_gauge_check.py`: every reported identity
passed. Its scope is the arbitrary-BLP-pair defect identity, the gauge,
the time-dependent Darboux identity, and both initial variations and
their cleared entire identities. It does not itself check that the
inverse Laplace transformation preserves solutions, the Gaussian
positivity, the Bloch inversion, compactness, or entire-function theory.

I separately checked with SymPy the full forward Laplace residual
identities and inverse reconstruction. For

    A(q,p)=q_zt-(q²-q_X)_Xz-2p_XX,
    B(q,p)=p_t-p_XX-2(qp)_X,
    q*=q+(log|p|)_X, p*=p+q*_z,

the two exact identities are

    A*=A+(B/p)_Xz,
    B*=B+A+(B/p)_Xz.

Hence a solution (q*,p*) with inverse p=p*-q*_z nonzero has B=B*-A*=0
and then A=0. This closes the inverse-solution step used in the note.
The physical moving-frame residuals were also checked independently:
with q=-u/2 and p=(v-4-u_z)/4, their BLP residuals are respectively
-E_u/2 and (E_v-E_u)/4, where

    E_u=u_zt+v_XX+(u u_z)_X,
    E_v=v_t+u_XXz+(uv-4u)_X.

Thus the physical and BLP signs agree after X=x-4t. For p1=(v-4+u_z)/4,
q1=q-(log|p1|)_X, the inverse defect is indeed

    R=p1-q1_z=(v-4+3u_z)/4+(log|p1|)_Xz.

At the certified base, p1=s_z F D/psi², q1=Phi_X/Phi,
and R=0. The base construction and its nonzero psi,D bounds are used as
inputs here. Writing log|p1|, rather than log p1, makes the real formula
literal because p1 is negative on the selected slice; every derivative
and identity in the proof is unchanged.

## Gaussian, gauge, and Bloch checks

For L=192, d=pi/96 and C=sqrt(pi)/32, the exact Fourier coefficients are

    F_n(t)=C exp(-(9-t)(nd)²).

An explicit positive real-space representation is

    F(X,t)=3/sqrt(9-t) sum_j
        exp(-(X+192j)²/[4(9-t)]).

It is positive for real X and t<9. In particular, division by F on the
closed physical cylinder is legitimate. At z=1, s=.05 sin(pi/4)/2>0
and s_z=.05(pi/4)cos(pi/4)/2>0. The nonzero base p1 has a positive
absolute minimum on this compact slice, even though it is extremely
small in the far Gaussian tail. It is consequently also nonzero for
sufficiently small perturbations in the response classes under study.
This fact supplies no quantitative license to invert p1 for the
isolated perturbation 1e-6, where its zeros can be a real issue.

The gauge follows exactly from Phi_t=Phi_XX+2W_X Phi,
W=F_X/F:

    R=Phi r  =>  r_t=-r_XX-2W_X r.

Since W_t=-W_XX-2W W_X, T=partial_X-W has the stated intertwining sign.
The multiplier of r is exp(mu L), mu=sC>0. The kernel of T consists
of cF, which has multiplier one. Consequently T has a unique inverse
in this nontrivial Bloch sector. Its time dependence preserves this
sector, so T(h_t+h_XX)=0 implies h_t=-h_XX without a leftover kernel
term. No decay or temperedness of h on the entire real line is needed.

Writing h=exp(mu X)p gives exactly

    p_n(t)=exp(((nd)²-2i mu nd-mu²)t) p_n(0).

A periodic distribution at any positive time therefore forces Gaussian
decay of p_n(0). The Fourier series then gives an entire h0 with
log maximum modulus bounded by a constant times 1+|X|².

## Initial entire-function contradiction

Direct differentiation gives the stated a,b in both directions. At
z=1, a_u=3pi/16 and a_v=1/8. For the actual initial gauge,

    F0 h0'-F0' h0=exp(sJ0) E,
    E=a F0² Ck-b(F0 Ck'-Ck F0').

F0 is even, Ck is even and Ck(0)=1, so E(0)=aF0(0)²>0.
This establishes nonvanishing of the entire function E without any
tail asymptotics. Both E and the left side would have finite entire
order at most two if a positive-time distribution solution existed.

The quotient step uses the standard closure of finite-order meromorphic
functions under division: the quotient of the two finite-order entire
functions has finite Nevanlinna order. Here the quotient equals the
zero-free entire function exp(sJ0); it therefore has finite entire
order as well. Hadamard factorization forces it to equal exp(P) for a
polynomial P. Differentiation then gives sF0=P', impossible because
F0 is nonconstant periodic. This formulation makes explicit why zeros
of E or cancellations in an integral expression for h0 do not defeat
the argument.

## A direct justification of the finite-norm conclusion

The finite tensor norm in Section 7 is sufficient. A shorter rigorous
passage avoids extracting a full physical first variation. Suppose
exact classical solutions exist for epsilon_n ->0 and their normalized
physical differences are uniformly bounded in that norm. On the fixed
z=1 slice, p1^n stays away from zero for all sufficiently large n.
Define the exact nonlinear transformed defect R^n and rho^n=R^n/epsilon_n.
Taylor expansion of the rational derivative expression for R gives:

1. rho^n is uniformly bounded, since R uses at most u_Xzz and v_Xz;
2. q1^n converges uniformly to the base q1;
3. rho^n(0) converges to the explicitly computed initial defect.

The exact equation holds before taking the limit:

    rho^n_t=-rho^n_XX+2(q1^n rho^n)_X.

Weak-star compactness on the finite cylinder yields a bounded limiting
rho. Passing to its weak formulation, including the initial boundary
term, gives the linear defect equation and its specified initial
trace. The fixed gauge and Bloch inverse T^-1 then give a
distributional backward-heat h with that initial value. The spatial
inverse maps bounded inputs to bounded h on a period; at a common
positive time for the countably many Fourier coefficients, their ODEs
give the Gaussian initial tail estimate. The entire-order
contradiction follows unchanged.

This also avoids needing to spell out time-derivative estimates from
the lower u trace. It proves the stated conclusion in the displayed
finite norm, but still does not prove an obstruction in the bare
physical L-infinity norm: that norm does not bound rho^n.

## Recommended presentation changes

- Use log|p1| in real inverse-Laplace expressions.
- State explicitly that the entire quotient step uses finite-order
  meromorphic division before applying the zero-free entire Hadamard
  theorem.
- Replace or supplement Section 7's general compactness paragraph by
  the exact-normalized-defect argument above.
- Keep the isolated-amplitude and physical-maximum-norm limitations
  prominent. There is no certified perturbed reference error here.

These are clarifications of a supported result, not repairs of a
detected mathematical counterexample. The full reference certificate's
interval calculations and uniqueness theorem remain outside this audit.
