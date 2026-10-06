# Periodic phase space and mean-mode reduction

Independent mathematical check, 2026-10-04. Notation:
\(D=\partial_x\), \(d=(1-E^{-1})/h\), \(M=(1+E^{-1})/2\),
\(\beta=h^2/32\). The exact equations are

\[
d\{U_t+D(\tfrac12U^2+\beta w^2)\}+D^2(dU+Mw)=0,
\qquad w_t=-D(Uw)+D^2w.
\]

Here \(U=u+2a\), \(w=v-\delta_0u-4\).

## 1. Periodic lattice compatibility

Take an \(N\)-site cyclic lattice and write
\(\langle f\rangle=N^{-1}\sum_jf_j\), \(P=I-\langle\cdot\rangle\).
For an \(x\)-circle, averaging the first equation gives
\(D^2\langle w\rangle=0\), hence \(\langle w\rangle=c(t)\).
Averaging the second equation and then integrating in \(x\) gives

\[
c_t=0,\qquad D\langle Uw\rangle=0.
\]

Thus \(q(t)=\langle Uw\rangle\) is a spatially constant free mode.
Writing \(U=m+p\), \(w=c+r\), \(Pp=p\), \(Pr=r\), and assuming
\(c\ne0\), the required lattice mean is

\[
m=\frac{q-\langle pr\rangle}{c}.
\]

Fixing \(m\) independently generally violates the second compatibility
condition. The \(c=0\) sector instead imposes
\(D\langle pr\rangle=0\), which cannot determine \(m\) by this formula.
The present regular reduction does not cover that sector.

Strictly periodic nonzero tau functions have
\(\langle W\rangle=(4/h)D\sum_j\log(G_{j+1}/G_j)=0\), so their natural
sector is \(c=-4\), covered by the regular reduction.

## 2. Inverse and adjoints

Define

\[
R=(d|_{\operatorname{im}P})^{-1}MP.
\]

It is a real finite matrix with Fourier symbol
\(-\mathrm i(h/2)\cot(\pi k/N)\) for \(1\le k<N\), and zero symbol for
\(k=0\). Thus \(R^*=-R\), \(RP=PR=R\), and \(RD=DR\).
For even \(N\), the Nyquist symbol is zero; this does not obstruct
invertibility of \(d\) on the zero-mean lattice sector.

The projected first equation is exactly

\[
p_t=-PD(\tfrac12U^2+\beta w^2+DU+RDw).
\]

For periodic \(x\), \(D^*=-D\), hence \((RD)^*=RD\).

## 3. Reduced Hamiltonian check

With the pairing \(h\sum_j\int dx\), define

\[
H_{\rm full}=h\sum_j\int
\left(\tfrac12U^2w+\tfrac\beta3w^3+wDU+\tfrac12wRDw\right)dx.
\]

Its gradients are

\[
H_U=Uw-Dw,\qquad
H_w=\tfrac12U^2+\beta w^2+DU+RDw.
\]

Define the reduced functional by substituting the mean constraint in
\(H_{\rm full}-hN\int qm\,dx\). Since
\(\langle H_U\rangle=q\) on the constraint, its mean-\(U\) derivative
vanishes after this subtraction. Consequently the chain rule gives

\[
(H_{\rm red})_p=P(Uw-Dw),\qquad
(H_{\rm red})_r=P(\tfrac12U^2+\beta w^2+DU+RDw).
\]

The constant operator

\[
J_{\rm red}=-\begin{pmatrix}0&PD\\PD&0\end{pmatrix}
\]

therefore generates the projected first equation and the full second
equation; reconstructing \(m\) enforces both averaged equations.
It is skew-adjoint, and its field-independent coefficients make its
Jacobi identity exact on the usual admissible smooth functional algebra.
Fixed \(q\) gives an autonomous Hamiltonian. A prescribed \(q(t)\) gives
an explicitly time-dependent Hamiltonian for the reduced variables
\((p,r)\) with the same Poisson bracket. The physical reconstruction is
then time-dependent: its \((u,v)\) vector field contains the extra drift
\((q'/c,0)\). Thus a pure physical equation
\(z_t=J_z\,\delta H/\delta z\) is asserted here only for fixed \(q\),
or after the moving-frame gauge fixes \(q\).

For fixed \(q\), the physical coordinate map is
\(T(p,r)=(u,v)=(p+m-2a,c+r+4+\delta_0p)\). Its differential is

\[
T'=\begin{pmatrix}A&B\\\delta_0&I\end{pmatrix},\quad
A\xi=\xi-\frac{\mathbf1}{c}\langle r\xi\rangle,\quad
B\eta=-\frac{\mathbf1}{c}\langle p\eta\rangle.
\]

The operator \(J_z=T'J_{\rm red}(T')^*\) is the Poisson pushforward on
the constrained physical phase space. This map has inverse
\(p=Pu\), \(r=P(v-\delta_0u-4)\), so the Jacobi identity transfers
without an additional assumption. The lattice projection and the mean
constraint make this physical operator collective rather than
finite-range uniformly in \(N\).

For clarity, put \(s=\langle pr\rangle\). Dropping constants and total
\(x\)-derivatives, an equivalent expression is

\[
H_{\rm red}=hN\int\left[
\tfrac12\langle(c+r)p^2\rangle+\frac qc s-\frac{s^2}{2c}
+\beta c\langle r^2\rangle+\frac\beta3\langle r^3\rangle
+\langle rDp\rangle+\tfrac12\langle rRDr\rangle\right]dx.
\]

The collective \(s^2\) term is quartic; the density has one continuous
derivative, while \(R\) is generally dense in the periodic lattice.

## 4. Mean gauge and extra boundary data

The exact equations are invariant under

\[
U'(x,t)=U(x-A(t),t)+A'(t),\qquad
w'(x,t)=w(x-A(t),t)
\]

for arbitrary smooth \(A\). This sends \(q\) to \(q+cA'\); when
\(c\ne0\), one can choose a moving frame with \(q=0\).
In \(H_{\rm red}\), the \(q/c\) term multiplies the translation momentum
\(\mathcal P=hN\int s\,dx\), which generates \((-Dp,-Dr)\).
Translation invariance therefore preserves \(\mathcal P\).

The continuous means of every \(p_j,r_j\) are Casimirs of this bracket.
If periodic positive tau functions are also periodic in \(x\), then
\(\operatorname{avg}_xU_j=2a\) and
\(\operatorname{avg}_xw_j=-4\). Their mean compatibility fixes
\(q=-8a+\operatorname{avg}_x s\), which is constant by momentum
conservation.

## 5. Domains and limitations

Smooth real periodic fields provide a convenient formal phase space.
The Hamiltonian is already finite on \(H^1\) fields in one continuous
dimension; the vector field contains two \(x\)-derivatives. Hamiltonian
structure alone does not establish Sobolev well-posedness: its leading
continuous operators include both signs of \(D^2\), hence a backward
heat direction.

On the real line the same calculation applies to Schwartz perturbations
\(p,r\) of the constant background \((U,w)=(q/c,c)\), with the vacuum
density subtracted. Bounded backgrounds exclude affine lattice means.
Integration by parts then has no boundary terms.

For open chains there is no automatic skew inverse. Already for two
nodes, \(d=[-1,1]/h\), \(M=[1/2,1/2]\), and the zero-mean right inverse
gives

\[
R=\frac h4\begin{pmatrix}-1&-1\\1&1\end{pmatrix},\qquad
R+R^*=\frac h2\operatorname{diag}(-1,1)\ne0.
\]

Boundary terms or a different extension are required before transferring
the periodic construction. On an infinite lattice the multiplier
\(\cot(k/2)\) is unbounded near \(k=0\); a separate domain/range analysis
is required, rather than silently treating \(R\) as a bounded
\(\ell^2(\mathbb Z)\) operator.

## 6. A useful invariant two-periodic sector

For even \(N\), the subspace \(p_j=(-1)^jP(x)\),
\(r_j=(-1)^jS(x)\) is invariant. Here \(R=0\),
\(m=(q-PS)/c\), and

\[
P_t=-D(mP+2\beta cS)-D^2P,\qquad
S_t=-D(cP+mS)+D^2S.
\]

Its Hamiltonian density is
\(cP^2/2+(q/c)PS-(PS)^2/(2c)+\beta cS^2+SDP\), with the same off-diagonal
\(-D\) bracket after using the pairing inherited from the \(N\) sites.
For \(N=2\), this covers every zero-mean lattice field.
