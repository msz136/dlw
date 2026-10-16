# Two conditional support bounds for the Cantrell 37 layout

This is a derivation for a specified orientation/contact class. It is **not** a
lower bound for arbitrary 37-square packings. In particular, none of the directed
separations below follows from non-overlap alone without choosing a branch.
Square numbers here are **one-based source numbers** from `n-37.cert`.

Let `p_i=(x_i,y_i)`, let `c=cos(theta)`, `s=sin(theta)`, and assume
`0 <= s <= c`, `c^2+s^2=1`. The relevant axial squares have directions `(1,0)`.
Squares 10--15 have basis `u_-=(c,-s), v_-=(s,c)`; squares 19--24 have
`u_+=(c,s), v_+=(-s,c)`. The middle square 36 has direction 45 degrees.
Only the specific squares appearing in an inequality need the corresponding
orientation assumption. Put `h=(1+c+s)/2` and `n=(s,-c)`.

## First chain: 13 inequalities

The exact algebraic assumptions are:

1. `x_1 >= 1/2`.
2. `x_4-x_1 >= 1`.
3. `x_6-x_4 >= 1`.
4. `y_6 <= L-1/2`.
5. `n dot (p_23-p_6) >= h`.
6. `n dot (p_22-p_23) >= 1`.
7. `n dot (p_24-p_22) >= 1`.
8. `n dot (p_31-p_24) >= h`.
9. `x_26 <= L-1/2`.
10. `x_26-x_31 >= 1`.
11. `y_29 >= 1/2`.
12. `y_30-y_29 >= 1`.
13. `y_31-y_30 >= 1`.

The chain telescopes to

`s(x_31-x_6)-c(y_31-y_6) >= 2h+2 = 3+c+s`.

The axial chains and walls give `x_6>=5/2`, `x_31<=L-3/2`,
`y_31>=5/2`, and `y_6<=L-1/2`. Since `s,c>=0`,

`s(x_31-x_6)-c(y_31-y_6) <= s(L-4)+c(L-3)`.

Thus

`(c+s)L >= 3+4c+5s`,

and, because `c+s>0`,

`F1(theta) := (3+4c+5s)/(c+s) <= L`.

The exact rational fixed-angle LP independently selected these same 13 rows.
Its positive dual weights sum to a valid coordinate cancellation. This LP
check is recorded in `n37_fixed_branch_dual.json`; the above derivation does
not depend on a numerical LP result.

## Second condition: the central diagonal brace

For the left half it suffices to have

* `x_8>=1/2`, `y_8>=3/2`;
* `x_3>=1/2`, `y_3<=L-5/2`;
* `v_- dot (p_11-p_8)>=h`, `v_- dot (p_13-p_11)>=1`;
* `u_- dot (p_14-p_3)>=h`, `u_- dot (p_13-p_14)>=1`.

The first two coordinate bounds are derived from the axial wall and chains:
`y_7>=1/2`, `y_8-y_7>=1`; and
`y_1<=L-1/2`, `y_1-y_2>=1`, `y_2-y_3>=1`.

Let `U=u_- dot p_13`, `V=v_- dot p_13`. Then

`U >= c+3s+3/2-sL`, `V >= s+2c+3/2`.

Since `x_13+y_13=(c-s)U+(c+s)V` and both weights are nonnegative,

`x_13+y_13 >= A := 3+3c+s(c-s)(5-L)`.

For the right half, apply the same argument to reflected coordinates
`R(x,y)=(L-y,L-x)` with the replacements
`8 -> R(p_17)`, `11 -> R(p_20)`, `13 -> R(p_22)`,
`3 -> R(p_6)`, `14 -> R(p_23)`.
Equivalently, the right support assumptions are

* `x_17<=L-3/2`, `y_17<=L-1/2`;
* `x_6>=5/2`, `y_6<=L-1/2`;
* `(-u_+) dot (p_20-p_17)>=h`, `(-u_+) dot (p_22-p_20)>=1`;
* `n dot (p_23-p_6)>=h`, `n dot (p_22-p_23)>=1`.

The first bound on `x_17` follows from `x_16<=L-1/2` and
`x_16-x_17>=1`. The bound on `x_6` follows from the first axial chain.
This reflected argument yields `x_22+y_22 <= 2L-A`.

Finally, assume the two directed central separations, for `w=(1,1)/sqrt(2)`,

`w dot (p_36-p_13) >= 1/2+c/sqrt(2)`,
`w dot (p_22-p_36) >= 1/2+c/sqrt(2)`.

The support half-width of either tilted square along `w` is **c/sqrt(2)**,
because `c>=s` and the sum of absolute projections is
`((c-s)+(c+s))/sqrt(2)`. This is essential; replacing `2c` by `c+s`
would give an incorrectly weakened expression.

Hence `(x_22+y_22)-(x_13+y_13) >= sqrt(2)+2c`.
Combining the upper and lower bounds gives

`2(1+s(c-s))L >= 6+8c+10s(c-s)+sqrt(2)`

or

`F2(theta) := (6+8c+10s(c-s)+sqrt(2))/(2+2s(c-s)) <= L`.

## Shape of the conditional minimax bound

On `0 <= theta <= pi/4`,

`F1'(theta) = (1-3(c-s))/(c+s)^2`.

Thus `F1` is increasing after the point `c-s=1/3`, approximately
31.36698 degrees. Also write

`F2 = 5 + (4c-2+1/sqrt(2))/(1+s(c-s))`.

With `k=2-1/sqrt(2)`, the negative of its derivative has positive denominator
and numerator

`H = (c-s)[4c^2-k(c+s)] + 2kcs`.

Here `4c^2-k(c+s) >= 2-k sqrt(2) = 3-2sqrt(2) > 0`.
Therefore `F2` strictly decreases throughout this interval. A crossing in the
region `c-s<1/3` is the unique global minimizer of `max(F1,F2)` on the interval.
The crossing at about `theta=42.086607474205903...` has
`L=6.59861960924436011617837046268...`.

The monotonicity algebra above is exact. The displayed decimals are for
readability; exact existence and isolation evidence is recorded below. Turning
that argument into a Lean theorem is a separate step from the Python audit.

## Exact crossing isolation with a half-angle parameter

Set `q=tan(theta/2)` and `r=sqrt(2)`, so
`c=(1-q^2)/(1+q^2)`, `s=2q/(1+q^2)`. Exact simplification gives

`F1-F2 = N(q,r) / [2(q-1)(q+1)(q^2-2q-1)]`,

`N(q,r)=(4-r)q^4+(12-2r)q^2-r`.

Both nonconstant coefficients are positive. Thus `N` is strictly increasing
on positive `q`. The rational interval script proves, using an 80-digit
integer-square-root enclosure of `sqrt(2)`, that

`q_lo = 0.38473144692145990860539210349560684265858197326689`,

`q_hi = 0.38473144692145990860539210349560684265858197326690`

satisfy `N(q_lo,r)<0<N(q_hi,r)`. The intermediate value theorem and the
strict increase give exactly one positive root, lying strictly between these
endpoints. The script also proves `0<q_lo<q_hi<sqrt(2)-1`, positivity of the
displayed denominator on that interval, and `0<c-s<1/3` throughout its image.
Consequently this root is in the correct orientation regime and is the unique
conditional minimax crossing discussed above. One can also write its exact
radical expression as

`q = sqrt((-6+r+2sqrt(9-2r))/(4-r))`.

The side at the crossing is the rational function

`L(q)=(7+10q-q^2)/(1+2q-q^2)`.

Rational interval evaluation of the entire `q` enclosure lies strictly inside

`6.5986196092443601161783704626783488043909 < L < 6.5986196092443601161783704626783488043910`.

The degree-eight polynomial has opposite exact signs at these two endpoints,
and its derivative is negative throughout their interval. Thus the crossing
side and that uniquely isolated polynomial root are connected by an exact
interval image, rather than by comparing floating-point decimals.

For Lean, a calculus-free decrease certificate is also available in
`n37_bernstein_support.json`. Write `F2(q)=N2(q)/D2(q)`, with

`N2(q)=r q^4-2q^4-20q^3+2r q^2-28q^2+20q+r+14`,

`D2(q)=2(q-1)(q+1)(q^2-2q-1)`.

Then `N2(q)D2(a)-N2(a)D2(q)=(a-q)K(q,a,r)`. The supplied degree-(3,3)
Bernstein expansion proves `K>=12` on the entire rectangle
`0<=q,a<=2/5`, `7/5<=r<=3/2`. All sixteen coefficients of `K/4` exceed
3; the smallest coefficient over the two `r` endpoints is exactly
`39931/11250`. This proves `F2(q)>=F2(a)` for `q<=a` because both
denominators are positive. The certificate includes an integer-scaled identity
with no divisions in its polynomial expansion, verified by exact expansion.

## Elimination and the catalogue polynomial

At a crossing set `t=c+s`, `d=c-s`, `r=sqrt(2)`. Then
`t^2+d^2=2`. The equality `F1=L` gives `d=6-(2L-9)t`.
The two equations become

`f = ((2L-9)^2+1)t^2-12(2L-9)t+34 = 0`,

`g = 2(L-5)^2t^2-14(L-5)t+20+r = 0`.

Exact polynomial calculation, reducing with `r^2=2`, gives

`resultant_t(f,g) = (24-16r) Q(L,r)`,

where

`Q(L,r) = 6L^4-(208+64r)L^3+(2058+850r)L^2-(7936+3658r)L+11163+5502r`.

Taking the field norm gives exactly

`Q(L,r)Q(L,-r) = 36L^8-2496L^7+59768L^6-733760L^5+5289248L^4-23462672L^3+63458276L^2-96673872L+64068561`.

These identities are independently recomputed by
`scripts/n37_symbolic_support.py`. Resultants provide necessary relations;
they do not by themselves prove the correct real root, feasibility, or global
packing optimality.

## Remaining global step

To prove unrestricted optimality, one still needs either an exhaustive reduction
of every smaller 37-square packing to a class satisfying a sufficient family of
such inequalities, or a completely different unrestricted lower bound matching
the construction. No such reduction is established here. Free squares and other
contact branches can invalidate these particular assumptions.
