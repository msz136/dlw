# 全有限 M 的 actual 谱微分核：周期规范方程引理

2026-10-11，mixed 子任务独立推导。此引理用实际有限维 periodic fundamental ODE，不用 formal resolvent、ordinary physical Cauchy 可解或尚未建立的全 M inverse spectral 图。它把全 M nonlinear closure 的下一步压缩为明确的周期规范方程及其 Hamilton span 完备性问题；单独不证明后者。

## 1. 固定实际谱点的结论

设 \(L(x,\lambda)\in\mathfrak{sl}_M(\mathbb C)\) 光滑周期，长度 \(\ell>0\)，
\[
Y_x=LY,\quad Y(0)=I,\quad N(\lambda)=Y(\ell,\lambda).
\]
取固定 \(\lambda\)，假设 \(N(\lambda)\) 的 \(M\) 个 eigenvalues \(t_i\) 全部不同。
令 \(\dot L(x)\) 是任意 smooth periodic trace-free variation，\(\dot N\) 是 actual ODE 变分。则下列条件等价：

1. 全部 actual characteristic coefficients 的一阶变分为零。
2. 全部 \(\operatorname{tr}N^r\)，\(1\le r\le M-1\)，的一阶变分为零。
3. 存在 smooth periodic \(g(x)\in\mathfrak{sl}_M\)，使
\[
\boxed{\dot L=g_x-[L,g].}
\tag{1}
\]

由于 \(\operatorname{tr}L=0\)，\(\det N=1\) 精确成立，其 variation 自动为零。若要用于原未归一 connection，还必须同时加入已记录 scalar holonomy 的 variation；不能漏去 source-dependent normalization。

## 2. 证明：simple monodromy 的 finite-dimensional conjugacy

实际 variation equation 给
\[
Z=\dot Y\,Y^{-1},\qquad Z_x=\dot L+[L,Z],\qquad
Z(0)=0,\quad Z(\ell)=\dot N\,N^{-1}.
\tag{2}
\]
在 diagonal basis \(N=\operatorname{diag}(t_i)\) 中，
\[
d\,\operatorname{tr}N^r=r\sum_i t_i^{r-1}\dot N_{ii}.
\]
另由 fixed determinant，
\[
\sum_i t_i^{-1}\dot N_{ii}=0.
\]
将后式视为 moment degree \(-1\)，与 \(r=1,\ldots,M-1\) 的 degree \(0,\ldots,M-2\) 合并；乘各 column \(t_i\ne0\) 后是 degrees \(0,\ldots,M-1\) 的 Vandermonde，simple \(t_i\) 使矩阵可逆。因此全部这些 trace derivatives 零等价于 \(\dot N_{ii}=0\)。
它又等价于
\[
\dot N=[g_0,N],
\qquad (g_0)_{ij}=\frac{\dot N_{ij}}{t_j-t_i}\quad(i\ne j),
\tag{3}
\]
对角项可任取 trace zero。Newton identities 在 \(\det N=1\) 下给 characteristic derivatives 与上述 trace derivatives 的等价。

定义
\[
g(x)=Z(x)+Y(x)g_0Y(x)^{-1}.
\tag{4}
\]
式 (2) 给 \(g_x=\dot L+[L,g]\)，即 (1)。由 (3)，
\[
g(\ell)=\dot N N^{-1}+Ng_0N^{-1}=g_0=g(0).
\]
所有 coefficients 周期，endpoint values 相等与 ODE 给全部 endpoint derivatives 相等；故 \(g\) 是 smooth periodic。其 trace 恒定；取 \(g_0\) trace zero，\(Z\) 因 \(\operatorname{tr}\dot L=0\) trace zero，所以 \(g\in\mathfrak{sl}_M\)。

反之，若 (1) 有 periodic solution，则实际 variation (2) 与
\(g-Yg(0)Y^{-1}\) 同初值同方程，故
\(\dot N=[g(0),N]\)。所有 characteristic derivatives 因而零。
这完成全部等价。

## 3. 非唯一性和 exact periodic adjoints

两份 \(g\) 相差
\[
h(x)=Y(x)h_0Y(x)^{-1},\qquad [h_0,N]=0,\quad \operatorname{tr}h_0=0.
\tag{5}
\]
simple \(N\) 的 centralizer 是 \(I,N,\ldots,N^{M-1}\) 的 span；其 trace-free 部分维数 \(M-1\)。因此所有 trace-free periodic solutions \(h_x=[L,h]\) 恰由 actual monodromy trace powers 的 adjoints 生成。这证明固定 regular \(\lambda\) 下，使用全部 \(r=1,\ldots,M-1\) 的 actual trace powers 不漏任何 periodic adjoint branch；只使用 fundamental trace 对 \(M>2\) 一般不足。

当 \(L,\dot L\) 对 \(\lambda\) 在周期 smooth 空间 holomorphic，且在 simple-monodromy 谱点的一个邻域中**每个** \(\lambda\) 的全部 normalized characteristic derivatives 恒等为零时，可在该邻域解析选 eigenprojections 和 (3) 的 off-diagonal right inverse；所以 \(g(x,\lambda)\) 局部 holomorphic。只在单个 \(\lambda_0\) 满足 kernel 条件不足以给邻域的 periodic 解，必须保留上述 image 条件；共同全谱微分核的应用自动满足它。这里只是避开 collisions 的局部陈述；没有跨全部 \(\lambda\) 的 uniform norm、whole-plane extension 或全频 gap bound。

## 4. 对已建立全 M 物理谱结构的具体应用

全 M 独审已有 actual normalized affine connection
\[
L_{ii}=\lambda(d_i/S-1/M)+\Delta_i-\overline\Delta,\qquad
L_{ij}=d_i(\lambda/S+\operatorname{sgn}(j-i)),
\]
其中 \(d_{M-1}=S-\sum_{j<M-1}d_j\)、\(\Delta_{M-1}=0\)。
物理 variation 是其实际 free-state derivative，仍 smooth periodic trace-free。
因此，若一个 smooth physical tangent 灭去全部 normalized characteristic coefficients，那么在每个 simple-monodromy \(\lambda\) 上其 \(\dot L\) 满足 (1)。

目前可严格使用的原物理场为
\[
X_{\Delta_j}=-\frac1{16}\operatorname{tr}W[
K_j(\lambda/S)-K_{M-1}(\lambda/S),L],
\quad
X_{d_j}=-\frac1{16}\operatorname{tr}W[H_j,L],
\]
\[
H_j=E_{jj}-I/M,\qquad
K_j(a)=\sum_k(a+\operatorname{sgn}(k-j))E_{jk}.
\]
其中 \(W=YN^rY^{-1}\) 的 scalar part 任意删去，且上述 expressions 由实际 gradient 的 \(-D/16\) 消去 spatial derivative 得出；它们是 fixed finite \((r,\lambda)\) 的 order-zero actual Hamilton fields。这里 \(\operatorname{tr}W[\cdot,L]\) 为 matrix contraction，不是 trace of scalar zero。

下一待证引理可准确写为：在一个明确 nonempty 全 M regular strong state 域上，若 physical tangent 的 \(\dot L\) 对全部 actual regular \(\lambda\) 有 (1)，则该 tangent 属于全部上述 fixed-finite-\((r,\lambda)\) Hamilton directions 的 ambient \(C^\infty\) 闭包。或者先建立该周期 cohomology 的具体 vector-spectral Cartesian state inverse，再以 finite velocity truncation 证明闭包。引理 (1)–(5) 本身不能代替这个完备性步骤。

若该闭包完成，已证 actual Poisson involution、原 \(\Omega\) 连续和 same-strong-domain finite flow 接合将按 M2 的论证给 nonlinear common differential kernel 最大性。实际 common fiber regularity 和 unclosed fiber tangent equality 仍需另证。
