# Complex growth of the actual periodic Gaussian: a distribution-valued obstruction

2026-10-26. Analytic proof. This supplies the complex-variable estimate needed by `DISTRIBUTIONAL_LINF_RESPONSE_AUDIT.md`. It concerns the actual Gaussian and carrier, rather than an added high-frequency input. It does not establish isolated-nonzero-amplitude nonexistence.

## 1. Definitions

Let L=192, d=pi/96, C=sqrt(pi)/32 and

    F(w)=C sum_(n in Z) exp(-9(nd)^2) exp(i nd w),
    J(w)=C w+C sum_(n!=0) exp(-9(nd)^2) exp(i nd w)/(i nd).

The latter series is symmetrically summed; it converges normally on compact complex sets, has J(0)=0 and J'=F. It is the actual initial periodic Gaussian primitive. Set kappa=pi/2 and K(w)=cos(kappa w).

For Y>0 choose

    w_Y=9pi/Y+iY,  eta_n=nd+Y/18,
    S_j(Y)=sum_n |eta_n|^j exp(-9 eta_n^2).

For each fixed integer j>=0, S_j is bounded uniformly in Y, by grouping lattice points according to their distance from the origin. Call an upper bound M_j. A nearest lattice point has |eta_n|<=d/2, so

    S_0(Y)>=m_0:=exp(-9d^2/4)>0.

The same uniform-moment fact holds with Gaussian exponent 9/2. These constants are independent of the carrier phase and Y.

## 2. Gaussian and derivative estimates

Completing the square and using nd*(9pi/Y)=-pi/2+9pi eta_n/Y gives exactly

    F(w_Y)=-i C exp(Y^2/36)
                  sum_n exp(-9eta_n^2) exp(i9pi eta_n/Y).

Because |exp(i theta)-1|<=|theta| for real theta,

    |F(w_Y)/[-i C exp(Y^2/36)]-S_0(Y)|<=9pi M_1/Y.

Consequently, for sufficiently large Y,

    (C m_0/2) exp(Y^2/36)<=|F(w_Y)|
                                <=C M_0 exp(Y^2/36).

Termwise differentiation and |nd|<=Y/18+|eta_n| give

    |F'(w_Y)|<=C exp(Y^2/36)[(Y/18)M_0+M_1].

In particular F'/F=O(Y). This proof uses a uniform lattice Gaussian bound; no unproved single-image asymptotic is used.

## 3. The primitive has an exponentially large positive real part

Multiply J(w_Y) by Y/[C exp(Y^2/36)]. In the sum, split into

    D_Y={n: |eta_n|<=Y/36} and its complement.

On D_Y, nd=-Y/18+eta_n is negative and |nd|>=Y/36. Thus

    |Y/(i nd)-18i|<=648 |eta_n|/Y.

Combining this with the exact carrier phase in Section 2, the contribution on D_Y differs from 18 sum_(D_Y) exp(-9eta_n^2) by at most

    (648+162pi)M_1/Y.

For n!=0 outside D_Y, |Y/(i nd)|<=Y/d. If M'_0 bounds sum_n exp(-(9/2)eta_n^2), then

    sum_(|eta_n|>Y/36) exp(-9eta_n^2)
                   <=M'_0 exp(-Y^2/288).

The omitted n=0 term in 18S_0 is 18exp(-Y^2/36). The mean term contributes Y w_Y exp(-Y^2/36), of magnitude O(Y^2exp(-Y^2/36)). It follows that

    |Y J(w_Y)/[C exp(Y^2/36)]-18S_0(Y)|
      <=(648+162pi)M_1/Y
        +(Y/d+18)M'_0 exp(-Y^2/288)
        +18exp(-Y^2/36)+|Y w_Y|exp(-Y^2/36).

The right side tends to zero. Hence there are constants c_J,C_J>0 and Y_0<infinity such that, for Y>=Y_0,

    Re J(w_Y)>=c_J exp(Y^2/36)/Y,
    |J(w_Y)|<=C_J exp(Y^2/36)/Y.

The sign is important: +9pi/Y yields F approximately -i times a positive real number, and J approximately a positive real number. The negative real shift would give the wrong sign for this proof.

## 4. The second term in the cleared initial identity cannot cancel the first

The carrier obeys

    |K(w_Y)|>=sinh(kappa Y),
    |K'(w_Y)/K(w_Y)|<=kappa coth(kappa Y).

Put D=F K'-F'K. By the preceding estimates,

    |D/(F^2 K)|
       <=[|K'/K|+|F'/F|]/|F|
       =O(Y exp(-Y^2/36)) ->0.

Choose a compact transverse interval I around z=1 contained in (0,2), and a nonnegative test function g supported in its interior with integral one. On this interval define

    s(z)=.05 sin(pi z/4)/2,
    a_u(z)=3[sin^2(pi z/4)]'/4,
    a_v(z)=sin^2(pi z/4)/4,

and b_u,b_v as in the linearized proof. Both choices have s>=s_*>0, a>=a_*>0, and |b|/a<=B<infinity after shrinking I if necessary. The initial cleared expression is

    H(w,z)=exp(s(z)J(w))[a(z)F(w)^2K(w)-b(z)D(w)].

Use the Y-dependent complex test

    g_Y(z)=g(z)exp(-i s(z)Im J(w_Y)).

Then, by ordinary integration of the smooth initial H,

    <H(w_Y),g_Y>=F(w_Y)^2K(w_Y) A_Y-D(w_Y) B_Y,
    A_Y=int g a exp(s Re J), B_Y=int g b exp(s Re J).

Here A_Y>=a_*exp(s_*Re J)>0 and |B_Y|<=B A_Y. Since D/(F^2K)->0,

    |<H(w_Y),g_Y>|
       >=(a_*/2)|F(w_Y)^2K(w_Y)|exp(s_*Re J(w_Y))

for all sufficiently large Y.

For every fixed finite m, differentiation of the phase gives

    ||g_Y||_(C^m)<=C_m(1+|J(w_Y)|)^m.

Thus log ||g_Y||_(C^m)=O_m(Y^2), whereas the logarithm of the preceding lower bound is at least

    s_* c_J exp(Y^2/36)/Y +O(Y^2),

which grows faster than every fixed multiple of Y^2.

## 5. Distribution-valued finite-order growth is impossible

Suppose H(w,.) were an entire function with values in transverse distributions and with a finite-order-two bound on the compact interval I. Concretely suppose, for some fixed m,C_1,C_2,N,

    |<H(w),phi>|<=C_1(1+|w|)^N exp(C_2|w|^2)||phi||_(C^m).

Testing at w=w_Y against g_Y makes the logarithm of the right side O_m(Y^2), contradicting Section 4. Therefore H cannot satisfy such a distribution-valued order-two bound.

The distributional backward-heat lift in the companion audit would force exactly this bound for F h_0'-F'h_0: the initial lift has Gaussian Fourier tails in a fixed finite-order transverse distribution seminorm, and F,F' have order at most two. Consequently no distribution-valued physical first variation can be obtained as a uniformly bounded physical-L-infinity normalized response.

This is a growth argument at the actual Gaussian background and the actual pure carrier. It neither asserts that a single epsilon=1e-6 solution is absent nor excludes an amplitude response with weaker non-Lipschitz behavior.
