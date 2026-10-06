# Periodic DLW monodromy: formal conservation hierarchy and commuting traces

Date: 2026-10-04. This is a formal algebra theorem, not an IST or a statement
about the infinite lattice line-soliton scattering space.

## 1. Algebra and hypothesis

Write D=d/dx and use normal-form scalar pseudodifferential operators
sum a_k(x) D^k. Their multiplication is

    (a D^r)(b D^s)=sum_{m>=0} binom(r,m) a D^m(b) D^(r+s-m).

Trace means Tr X=int res_D X dx; work modulo D of coefficients, or use a
periodic x coordinate. Tr XY=Tr YX follows from this multiplication rule.

The lattice has N periodic sites. Let g_j=h w_j/4,
A_j=(U_j+g_j)/2, B_j=(U_j-g_j)/2 and

    S_j=(D-B_j)^(-1)(D-A_j),
    P=S_(N-1)...S_0.

The inverses of D-B_j exist formally because their leading coefficients are
one. No individual g_j or w_j needs to be nonzero. The two verified Darboux
intertwining identities, rather than just an arbitrary-wave ratio, give

    S_j,t=M_(j+1) S_j-S_j M_j,  M_j=-D^2-V_j.

Assume V_N=V_0, so P_t=[M_0,P]. Periodic potentials require sum g_j,x=0.
Use the fixed-average gauge

    G=sum g_j !=0,  T=sum U_j g_j,

where G,T are x,t constants. The original periodic SD admits the previously
specified fixed-mean leaf; a general time-dependent mean gauge has to be
handled separately. The first two monodromy coefficients are

    P=1+a D^(-1)+b D^(-2)+..., a=-G, b=(G^2-T)/2.

Therefore F=P-1 is formally invertible of order -1. Define

    L=a F^(-1)+b/a = D+ell_1 D^(-1)+ell_2 D^(-2)+... .

This normalization needs G!=0. Its coefficients are functions of all N
sites, with finite x differential order at each expansion level.

The periodic heat potential is available directly on the reduced SD leaf;
it need not be assumed as an unrelated extra condition. Let beta=h^2/32,

    e_j=U_j^2 w_j/2+beta w_j^3/3+w_j U_j,x+w_j(Rw_x)_j/2,
    ebar=mean_j e_j, lambda=2D ebar/c.

The reduced physical equation is

    U_t=-D(U^2/2+beta w^2+U_x+Rw_x)+lambda,
    w_t=D^2w-D(Uw).

Then choose the same periodic potential at every link from

    V_j=(Rw_x)_j/2-h w_j,x/4-ebar/c+v0(t).

It satisfies V_(j+1)-V_j=h w_j,x/2=2g_j,x. In the sum of the two
Darboux Riccati residuals, substitution leaves
-RD^2w+lambda+h D^2w/2+2D V=0; their difference is the displayed w
equation. Thus both full intertwiners hold for this reduced SD, and the
potential is periodic in both x and the lattice.

## 2. Conservation, cyclic gauge and recursion

Because a,b are constants, L_t=[M_0,L]. For C=L^n with
C=sum c_k D^k, direct multiplication gives

    res[-D^2-V,C] = -D(D c_(-1)+2 c_(-2)).

Thus rho_n=res L^n satisfies the exact local x conservation law

    rho_n,t+D(rho_n,x+2 coeff_(D^-2) L^n)=0.

The D^0 coefficient of L_t also says V_x=2 ell_1,x. Hence the evolution of
L is the negative second KP flow modulo the scalar time gauge in V. This
is a consequence of the full intertwiners, not a replacement proof that a
bare monodromy zero curvature characterizes all SD branches.

Changing the lattice starting point conjugates P and L by S_j. Therefore
Tr L^n is independent of the starting site; residue densities differ by a
total x derivative. All positive or negative integer powers of P itself
have res P^m=m a and give only the already fixed mass. They must be discarded.

An explicit generation algorithm is:

    s_(j,1)=-g_j,
    s_(j,n+1)=B_j s_(j,n)-D s_(j,n).

If a partial product has coefficients p_n, adding S_j on its left gives

    p_n,new=p_n+s_(j,n)
             +sum_(r>=0,k,l>=1,k+l+r=n)
                binom(-k,r) s_(j,k) D^r p_l.

After the final site, p_1=a,p_2=b. The equation

    F L = a+(b/a) F

recursively determines ell_m. Explicitly,

    ell_m=b p_(m+1)/a^2-p_(m+2)/a
          -(1/a)sum_(k=1,...,m-1)
            sum_(r>=0,j>=1,j+k+r=m+1)
               binom(-j,r) p_j D^r ell_k.

Finally multiply L recursively to obtain rho_n. This gives a generating
relation without solving a wave function or fitting any Gram solution.

## 3. Factor Poisson calculation without relying on a theorem name

Start with the unreduced constant bracket J0=-[[0,D],[D,0]] for U,w,
using h sum_j int dx as its pairing, as in the existing Hamilton result.
Equivalently, with ordinary unweighted functional derivatives its kernel
is -(1/h)[[0,D],[D,0]]. In A,B coordinates the latter kernel is

    J_AA=-(1/8)D, J_BB=+(1/8)D, J_AB=0,

with different sites independent. Define the Adler expression

    A_K(X)=(K X)_+ K-K(X K)_+.

For a first order factor K=D+q, put X=D^(-1)phi. Then
A_K(X)=-phi_x, so its coefficient bracket is exactly -D.

Two elementary identities establish the required product and inverse rule:

    A_(K H)(X)=A_K(HX) H+K A_H(XK),
    pushforward under K -> K^(-1) sends A_K to -A_(K^-1).

The first identity follows by expanding the two plus projections; the middle
terms cancel. For the inverse, d(K^-1)=-K^-1(dK)K^-1 and the gradient of a
functional of K^-1 is -K^-1 X K^-1. Substitution gives the stated minus sign.

Consequently D-A has +(1/8) Adler bracket, D-B has -(1/8) Adler bracket,
and (D-B)^-1 again has +(1/8) Adler bracket. The independent factor product
P therefore has the pushed-forward bracket (1/8) A_P. This calculation
only uses the constant J0, which already satisfies Jacobi.

## 4. Trace involution and tangency of the fixed-average constraints

Extend each trace functional to nearby unreduced fields by holding the
numerical parameters a,b fixed:

    H_n(P;a,b)=Tr[a(P-1)^(-1)+b/a]^n.

Its trace gradient is

    X_n=-n a (P-1)^(-2) L^(n-1)
       =-(n/a)(L-d)^2 L^(n-1), d=b/a.

Thus X_n commutes with P. Its Adler Hamiltonian vector is

    P_dot=(1/8)[(P X_n)_+,P],
    P X_n=-(n/a)[(L-d)^2+a(L-d)]L^(n-1),

where the right side is a polynomial in L. For any m,n,

    {H_m,H_n}_0=(1/8)Tr X_m[(P X_n)_+,P]=0

by cyclicity and [P,X_m]=0. This is an explicit trace calculation.

There is also a direct proof of the average tangency. Put Q=P X_n. Since
[Q,P]=0, P_dot=-(1/8)[Q_-,P-1]. Both factors have order at most -1;
their scalar leading coefficients commute, so this commutator has order
at most -3. Therefore p1,p2, and hence G,T, are preserved pointwise.

## 5. Passing to the existing J_red without inverting the periodic D zero mode

A naive Dirac inverse has a D kernel on a periodic x circle. The following
direct chain-rule argument avoids that issue on the trace functional algebra.

Let c=4G/(hN), gamma=4T/(hN), p=projection U, s=w-c. On the leaf

    U=p+B, w=c+s, B=(gamma-mean(p s))/c.

For an unreduced functional F write f=deltaF/deltaU,
k=deltaF/deltaw using ordinary unweighted derivatives, and alpha=mean f.
The restricted gradients, modulo lattice
constant representatives, are

    f_red=f-(alpha/c)s, k_red=k-(alpha/c)p.

If F preserves mean w under J0, then D alpha=0. The H_n above preserve G,
so they have this property. If F,G are additionally invariant under common
x translation, direct expansion of J_red=-[[0,projection D],[projection D,0]]
gives (both sides have the same overall 1/h in unweighted derivatives)

    {F|leaf,G|leaf}_red={F,G}_0|leaf.

Indeed the lattice mean terms integrate to zero since alpha_F,alpha_G are
x constants. The shear correction terms are constant multiples of the
x-translation derivatives of F and G; the remaining bilinear correction
is int D(sum p_j s_j)=0. Every Tr L^n is x translation invariant, so all
these trace functionals commute under the previously verified J_red.

This proves pairwise involution on the stated periodic formal leaf. It does
not prove infinite functional independence, IST, or applicability to the
nonperiodic moving-background Hamilton bracket.

For the present trace algebra there is an even stronger check. Under an
arbitrary common shift U_j -> U_j+2 phi_x, both D-A_j and D-B_j, hence P
and L, are conjugated by the same scalar e^phi. Scalar conjugation keeps
res_D K pointwise unchanged: a differential part stays differential, and
only the original D^-1 term of the negative part can contribute D^-1, with
the same coefficient. A periodic phi_x is enough; phi itself may be
quasiperiodic. Hence each H_n is invariant under every common periodic U
variation and sum_j deltaH_n/deltaU_j=0. Thus alpha=0 for these traces:
the restriction shear vanishes, their restricted J_red flows coincide
with the projected ambient flows, and the bracket identity above is exact
without even an overall translation correction. This does not assert a
Dirac restriction formula for arbitrary nontangent functionals.

## 6. Low densities and removal of duplicates

Modulo D, the first five residues are

    rho1=ell1,
    rho2=2ell2,
    rho3=3(ell3+ell1^2),
    rho4=4(ell4+3ell1 ell2),
    rho5=5(ell5+4ell1 ell3+2ell2^2+2ell1^3
           +2ell1 D ell2-(D ell1)^2).

In monodromy coefficients:

    rho1=b^2/a^2-p3/a,
    rho2 equiv -2p4/a+4b p3/a^2-2b^3/a^3,
    rho3 equiv -3p5/a+6b p4/a^2+6p3^2/a^2
                -15b^2 p3/a^3+6b^4/a^4.

Write H0(x)=h sum[U^2w/2+h^2w^3/96+w U_x+w Rw_x/2] and
K=H0-gamma h sum U. Then a general triangular-sum calculation gives

    p3 equiv -H0/8+GT/2-G^3/6,
    rho1 equiv -H0/(8G)+G^2/12+T^2/(4G^2).

On reduced coordinates with old translation momentum Pmom=h sum p s,

    rho1 equiv -K/(8G)+T Pmom/(8G^2)+G^2/12-T^2/(4G^2).

Consequently the old autonomous Hamilton functional is a linear combination
of Tr L and the x-translation momentum, up to a constant. Every trace is
x translation invariant, so the trace involution also gives conservation
under that old Hamilton flow. This agrees with the independent full
intertwining/residue-flux argument.

So rho1 is a duplicate. The general-N coefficient calculation below proves

    rho2 equiv -3 Q4_h/(16G)+T H0/(4G^2)+GT/12-T^3/(4G^3),

where Q4_h is h times the independently derived quartic density. Therefore
rho2 and Q4 are the same new charge modulo the old Hamilton and momentum;
they must not be counted as two extra charges.

Here is the general coefficient proof. Put C=log P and C_j=log S_j.
Since each C_j has order -1, [C_i,C_j] has order at most -3, and all
nested commutators have order at most -5. Thus up through D^-4 the BCH
formula is just sum C_j+(1/2)sum_(i>j)[C_i,C_j]. At one site let
C_j=a_j D^-1+b_j D^-2+... . Direct multiplication gives

    a_j=-g_j, b_j=g_j,x-U_j g_j/2,
    coeff_(D^-3) C_j equiv -U_j^2 g_j/4-g_j^3/12+U_j g_j,x/2,
    coeff_(D^-4) C_j equiv -(U_j^3 g_j+U_j g_j^3)/8
                              -3U_j g_j U_j,x/4+U_j,x g_j,x/2.

For two such operators the D^-3 commutator coefficient is
-a_i a_j,x+a_j a_i,x. Its D^-4 coefficient, modulo D, is
3(b_j a_i,x-b_i a_j,x). Therefore the pair terms in C give

    coeff_(D^-3) pair equiv -sum_(i>j) g_i g_j,x,
    coeff_(D^-4) pair equiv
       (3/4)sum_(i>j)(U_j g_j g_i,x-U_i g_i g_j,x).

For periodic R/h=(1-E^-1)^(-1)(1+E^-1)/2 on lattice-mean-zero fields,
the elementary triangular primitive says

    sum f_j (R/h) g_j,x equiv
        sum_(i>j) f_i g_j,x+(1/2)sum f_j g_j,x,

provided sum f_j and sum g_j are x constants. The unspecified constant
of that primitive multiplies sum f_j and contributes only D of a scalar.
Use f=g for the cubic term and f=Ug for the quartic term. Then

    coeff_(D^-3) C equiv -H0/8,
    coeff_(D^-4) C equiv -3 Q4_h/32.

Moreover the first two C coefficients are exactly -G and -T/2. Expanding
P=exp C through fourth order gives

    p4 equiv -3 Q4_h/32+G H0/8+T^2/8-G^2T/4+G^4/24,

which establishes the general comparison formula. Single-site log and
pair-commutator arithmetic is also checked symbolically by the script.

Exact general-field PDO arithmetic verifies five residue-flux identities,
five normalized coefficients, and the first five density forms. A fixed
Casimir-leaf Fourier witness on N=3 proves that rho2,rho3 supply two
independent functionals beyond old momentum and Hamilton at one regular
point. This does not prove independence of the full infinite family.

For clarity the witness uses G=6,T=12 and

    p=(-3,0,3)+(alpha,beta,-alpha-beta)cos x,
    g=(1,2,3)+(eta,zeta,-eta-zeta)cos x,
    U=p+(12-sum p g)/6.

At (alpha,beta,eta,zeta)=(1/5,-2/5,1/6,1/7), the four mean densities
[sum U,H0,rho2,rho3] have an exact gradient determinant
411796986221479423/4426355198361600000. Every x mean of p_j,g_j is fixed,
so this is a genuine fixed-Casimir-leaf independence witness, not merely
a comparison across different mean leaves. It is not a dynamical Fourier
truncation. The computation sets h=4 to make w=g; remapping w=4g/h gives
the same witness for any h>0.

There is also a symbolic general-x-field check at N=3,G=6,T=12 of the
relation to the independently constructed corrected quintic charge:

    rho3 equiv -Q5red/128+3Q4_h/32-H0/2+228/5,
    Q5red=Q5_h-(1/3)H0(x)^2.

Here H0(x)^2 is a squared density before integration. A general-N,
arbitrary-G,T version of this quintic comparison has not been proved;
the general involution theorem already applies to rho3 itself.

## 7. Continuous and nonperiodic scope

Let y=jh and let N h tend to a fixed y period Y. Then

    S_j=1-(h/4)(D-U/2)^(-1) w+O(h^2),
    psi_y=-(1/4)(D-U/2)^(-1)w psi,
    (D-U/2)psi_y=-(w/4)psi.

P tends to the y-ordered exponential of this continuous DLW transport
operator. G tends to (1/4)int w dy and T to (1/4)int Uw dy. The same
inverse-monodromy normalization has a finite formal limit when G!=0.
This is a continuous periodic-y monodromy hierarchy; locality in y is not
claimed. Keeping N fixed while h->0 collapses the y period and can make the
hierarchy trivial. That is not the two-dimensional continuum limit.

For the original 1(a),1(b),two-soliton infinite-lattice baselines no finite
periodic monodromy exists. Finite open products satisfy M_end P-P M_start,
not a commutator unless the endpoint potentials match. Infinite vacuum
products need relative/scattering normalization. Neither that construction
nor convergence/renormalization of Tr L^n has been proved here. These
periodic trace charges must not be assigned to those baselines as already
defined finite invariants.

Files: verify_monodromy_hierarchy.py and monodromy_hierarchy_checks.json;
verify_fixed_leaf_independence.py and fixed_leaf_independence_checks.json.
The quintic comparison uses verify_rho3_quintic_comparison.py and
rho3_quintic_comparison_checks.json.
