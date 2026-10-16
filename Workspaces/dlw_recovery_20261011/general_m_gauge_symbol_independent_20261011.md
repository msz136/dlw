# 全 M 原物理 trace 场的有理周期规范、约束图主符号及精确剩余缺口

2026-10-11。独立数学推导；未运行任何旧或新检查脚本，未修改共享记录。本稿实际读取了本轮 framed L² inverse、raw monodromy extraction、endpoint recovery、cyclic kernel、原 physical spectral audit，以及 periodic physical state inverse。这里使用完整状态图来书写物理约束，不把 framed inverse 解释成 action inverse。

范围：固定有限 \(M\ge2\)、\(m=M-1\)、\(S=M\delta\ne0\)，原 free component means 叶，已有近均匀背景的 mean-normalized physical state chart；内部常矩阵 \(H\) 满足非零 Fourier 无 alias。任意 spatialconstant \(B\) 可按当前截面保留；以下 centered 谱参数 \(\lambda=\lambda_{\rm orig}-B\) 的计算不推导 \(B_t=0\)。

新结果：

1. 全部原 physical trace-power Hamilton 场具有显式、单极点的 \(\lambda\)-有理周期规范。
2. 同一个 constant-\(H\) 物理图内，规范变分可化成两组 first-order periodic 方程和准确有限 graph 条件；相应增广算子 Fredholm index 为零。
3. 原 physical Poisson 张量在 \(y=(P_0a,P_0b)\) 图中的 order-two 主符号是常系数；下右 order-two 项由一个准确对称性消失。
4. 有有限有理规范证书的物理共同谱核方向属于实际 trace Hamilton 场的 \(C^\infty\) 闭包。该充分定理不产生任意共同谱核所需的证书。

## 1. 原 physical Hamilton 场的实际有理规范公式

沿用 [all-M actual audit](all_m_actual_spectral_independent_audit.md) §§1–3 的原 affine trace-free connection
\[
L_{ii}(\lambda)=\lambda(d_i/S-1/M)+\Delta_i-\overline\Delta,\qquad
L_{ij}(\lambda)=d_i(\lambda/S+s_{ij}),\quad i\ne j,
\]
\[
d_m=S-\sum_{j<m}d_j,\quad \Delta_m=0,\quad
H_i=E_{ii}-I/M,\quad K_i(a)=\sum_j(a+s_{ij})E_{ij}.
\]
这里 \(s_{ij}=\operatorname{sgn}(j-i)\)，本节的 \(H_i\) 是 Cartan 矩阵，与后文 constant slow matrix \(H\) 不同。

固定 \(\mu\) 与 \(1\le r\le M-1\)，取
\[
F_{\mu,r}=\frac1r\operatorname{tr}N_\mu^r,\qquad
W_{\mu,r}=Y_\mu N_\mu^rY_\mu^{-1},\qquad W_{\mu,r}'=[L_\mu,W_{\mu,r}].
\tag{1}
\]
实际 ODE 变分给
\[
(F_{\mu,r})_{\Delta_j}=\operatorname{tr}(W H_j),\qquad
(F_{\mu,r})_{d_j}=\operatorname{tr}\{W[K_j(\mu/S)-K_m(\mu/S)]\}.
\tag{2}
\]
原 ordinary-integral Poisson tensor 是
\[
J=-\frac1{16}\begin{pmatrix}0&I_mD\\I_mD&0\end{pmatrix}.
\tag{3}
\]
这里也可在 \((q,d_{\rm first})\) 使用同一 tensor；\(\Delta=q+S+\) skew-linear \(d\) 的变换保留 (3)。

置 \(a=\lambda/S,\ b=\mu/S\)，定义已审 \(C_\pm=R\pm B_{ab}/2\)，即
\[
C_+=\rho\Pi_0+T+\sum_iH_i\otimes K_i(b),\qquad
C_-=\rho\Pi_0+T-\sum_iK_i(a)\otimes H_i,
\]
\[
\rho=\frac{1-ab}{a-b}=\frac{S^2-\lambda\mu}{S(\lambda-\mu)},\quad
\Pi_0=\sum_{ij}E_{ij}\otimes E_{ji}-I\otimes I/M,\quad
T=\sum_{i\ne j}s_{ij}E_{ij}\otimes E_{ji}.
\]
他们满足真正逐点矩阵恒等式
\[
[C_+,L_\lambda\otimes I]+[C_-,I\otimes L_\mu]=0.
\tag{4}
\]
对任一上述 \(W=W_{\mu,r}\) 定义
\[
Q_\pm(\lambda,\mu)=\operatorname{tr}_2\{C_\pm(I\otimes W)\}.
\tag{5}
\]
使用 \(\sum_iH_i=0\)，(2)–(3) 精确给
\[
\delta_{X_{F_{\mu,r}}}L_\lambda
=-\frac1{16}D(Q_+-Q_-).
\tag{6}
\]
没有把 \(d_m,\Delta_m\) 当作独立 source：例如
\(\sum_iH_i\operatorname{tr}(WK_i(b))
=\sum_{j<m}H_j\operatorname{tr}\{W(K_j(b)-K_m(b))\}\)。

用 (4) 作 partial trace 时第二 commutator 有准确符号
\[
\operatorname{tr}_2\{[C_-,I\otimes L_\mu](I\otimes W)\}
=\operatorname{tr}_2\{C_-(I\otimes[L_\mu,W])\}
=DQ_-.
\]
所以
\[
DQ_-=[L_\lambda,Q_+].
\tag{7}
\]
(6)–(7) 给原 physical Lax variation
\[
\boxed{\quad
\delta_{X_{F_{\mu,r}}}L_\lambda
=(g_{\lambda,\mu,r})_x-[L_\lambda,g_{\lambda,\mu,r}],
\qquad g_{\lambda,\mu,r}=-Q_+/16.
\quad}
\tag{8}
\]
这是实际 periodic gauge，不是 formal residue 或标准 AKNS bracket 的替换。

把 \(\Pi_0\) 的 contraction 写开，有
\[
Q_+=\rho W^0+
\sum_{i\ne j}s_{ij}E_{ij}W_{ij}
+\sum_iH_i\operatorname{tr}(K_i(\mu/S)W),\qquad
W^0=W-\operatorname{tr}(W)I/M.
\tag{9}
\]
因 \(\operatorname{tr}(E_{ji}W)=W_{ij}\)，这里没有把 \(W_{ij}\) 误换成 \(W_{ji}\)。\(Q_+\) trace-free、smooth periodic，且是 \(\lambda\) 的 bounded-at-infinity 单极点有理函数：
\[
g_{\lambda,\mu,r}=g_{\infty,\mu,r}
-\frac{S^2-\mu^2}{16S}\frac{W_{\mu,r}^0}{\lambda-\mu}.
\tag{10}
\]
在 \(\lambda=\mu\) 的 pole 是规范表示的 pole；(8) 的左端实际解析。
最高 Laurent coefficient 满足
\((D-\operatorname{ad}L_\mu)W_{\mu,r}^0=0\)，恰消去规范方程中的奇性。

式 (8) 是 all-M 的 exact physical Hamilton-to-gauge bridge。它提供 Hamilton span 内方向的规范表示，尚未给共同谱核全部方向的这种有理表示。

## 2. 同一个 constant-H 物理图的规范微分

已有 near-uniform mean-normalized chart 满足
\[
G_x=VG-GH,\quad\langle G\rangle=I,\qquad
a=qG,\quad b=G^{-1}r,\quad
r=F(q,d)-d_{{\rm first},x}/S.
\tag{11}
\]
独立状态坐标是 \(y=(P_0a,P_0b)\)，其完整物理像
\[
\langle a\rangle=\mathcal A(y),\quad
\langle b\rangle=\mathcal B(y),\quad H=\mathcal H(y)
\tag{12}
\]
是已证的有限 graph。固定 \(B\) 已包括在 \(\mathcal H\) 的 chart 标签；若加入 \(B\)，须保留相应一维参数，不能从 \(y\) 猜测它。

在任意 smooth 状态处令
\[
k=G^{-1}\dot G,\qquad f=G^{-1}\dot V G.
\]
对 (11) 的准确线性化是
\[
(D-\operatorname{ad}H)k+\dot H=f,\qquad \langle Gk\rangle=0.
\tag{13}
\]
设内部无 alias：
\[
ik_0n\notin\operatorname{spec}(\operatorname{ad}H),\quad n\ne0,\qquad k_0=2\pi/L.
\]
则 \(R_H=(D-\operatorname{ad}H)^{-1}P_0\) 对每层 \(H^s\to H^{s+1}\) 有界。由非零 Fourier 模和平均分别得到
\[
\boxed{\quad
k_0=R_Hf,\quad
\bar k=-\langle Gk_0\rangle,\quad
k=k_0+\bar k,\quad
\dot H=\langle f\rangle+[H,\bar k].
\quad}
\tag{14}
\]
下标 \(k_0\) 在 (14) 指 zero-mean matrix function，不是 Fourier 频率常数。
\(\langle G\rangle=I\) 是使平均式精确成立的必要 normalization。

因此 \(\dot G\) 的非局部部分严格为 order \(-1\)；\(\dot H\) 是有限秩 source functional。该公式比只在均匀背景写 \(R_{V_0}\dot V\) 更强，并适用于同一个 nonlinear state 图内的任意 smooth 状态。Cauchy frame 的 endpoint 校准会增加有限秩项，不能抹掉这些项或将 graph 的 finite derivatives 假定为零。

## 3. periodic block gauge 的必要方程与有限条件

在 constant-H frame 用 trace-free connection
\[
A^0_\lambda=
\begin{pmatrix}\lambda&a\\b&H\end{pmatrix}
-\frac{\lambda+\operatorname{tr}H}{M}I_M.
\tag{15}
\]
对全谱共同 class kernel，实际 scalar holonomy 变分还可独立确定。全 M actual spectral audit §§5–6 已证大正实 \(\lambda\) 的 simple fast root及
\[
\log\widehat\mu_f=(1-1/M)\lambda L+\mathcal K_\lambda-\tau,\qquad
\mathcal K_\lambda=O_{C^1}(\lambda^{-1}),\qquad
\tau=L\operatorname{tr}H/M.
\]
若全部 normalized characteristic differentials 沿 v 为零，则这个 simple root 的微分为零，故
\(d\mathcal K_\lambda(v)-d\tau(v)=0\)。取正实 \(\lambda\to+\infty\) 得
\[
d\tau(v)=0,\qquad \operatorname{tr}\dot H=0.
\tag{15a}
\]
这里使用已证实际 \(C^1\) 余项，不能只从 formal series 取常数项。fixed-single-\(\lambda\) kernel不一定满足 (15a)，所以下面 (17) 的通用方程仍保留 \(\operatorname{tr}K\) 的 normalization 项。

physical tangent \(h\in C^\infty_0{}^{\,2m}\) 给
\[
\alpha=h_a+D\mathcal A(y)h,\quad
\beta=h_b+D\mathcal B(y)h,\quad
K=D\mathcal H(y)h.
\tag{16}
\]
矩阵 \(K\) 为 constant，并不必为零。

写 trace-free gauge
\[
g=\begin{pmatrix}\sigma&p\\t&Z\end{pmatrix},\quad
C=Z-\sigma I_m,\quad \sigma=-\operatorname{tr}C/M.
\]
直接计算 \(\dot A^0=g_x-[A^0,g]\) 四个块，等价于
\[
\boxed{\begin{aligned}
\alpha&=p_x-\lambda p+pH-aC,\\
\beta&=t_x+\lambda t-Ht+Cb,\\
K&=(D-\operatorname{ad}H)C-bp+ta+(at-pb)I_m.
\end{aligned}}
\tag{17}
\]
第一 scalar block 被第三式的 trace 恰好包含：
\[
\sigma_x=at-pb-\operatorname{tr}K/M.
\]
没有额外删除 scalar holonomy；\(\operatorname{tr}K\) 正是 normalization 中的实际变分。

置
\[
\mathscr F(p,t)=bp-ta-(at-pb)I_m.
\]
周期性与 no-alias 使第三式准确化为
\[
C=C_*+R_H\mathscr F(p,t),\qquad
K=-[H,C_*]-\langle\mathscr F(p,t)\rangle,
\tag{18}
\]
其中 \(C_*\in\operatorname{Mat}_m\) 是一个常矩阵。把 (18) 代入前两式后，所得完整 \(\alpha,\beta,K\) 还必须满足
\[
\langle\alpha\rangle=D\mathcal A(y)h,\quad
\langle\beta\rangle=D\mathcal B(y)h,\quad
K=D\mathcal H(y)h,\quad h=(P_0\alpha,P_0\beta).
\tag{19}
\]
这是 \(2m+m^2\) 个 finite graph 条件，不是 \(m^2\) 个自由 slow fields。
特别不能只保留 (17) 的 offdiagonal 方程，或仅令 \(K=0\) 来获得较小的假问题。

### 3.1 一个准确的 Fredholm 增广算子

将 (17)–(18) 的输出记为 \((\alpha_{p,t,C_*},\beta_{p,t,C_*},K_{p,t,C_*})\)，并置 \(h=(P_0\alpha,P_0\beta)\)。定义
\[
\mathcal T_\lambda(p,t,C_*)=
\left(
h,\
\langle\alpha\rangle-D\mathcal A\,h,\
\langle\beta\rangle-D\mathcal B\,h,\
K-D\mathcal H\,h
\right).
\tag{20}
\]
对每个 \(s\ge0\)，这是
\[
(H^{s+1}_{\rm per})^{2m}\oplus\operatorname{Mat}_m
\longrightarrow
(H^s_0)^{2m}\oplus\mathbb C^{2m}\oplus\operatorname{Mat}_m
\]
的有界算子。主部是 \((Dp,Dt,0)\)；其 kernel 与 cokernel 的维数均为 \(2m+m^2\)。其他非有限秩项是 order zero 或更低，因此由 \(H^{s+1}\hookrightarrow H^s\) 的 compact inclusion 给 compact perturbation。故
\[
\operatorname{index}\mathcal T_\lambda=0.
\tag{21}
\]
若实际 normalized monodromy \(N_\lambda\) cyclic，\(\ker\mathcal T_\lambda\) 正是 periodic homogeneous trace-free adjoints，经 \(p,t,C\) 的块分解一一识别，维数恰 \(M-1=m\)。regularity bootstrap 给该 kernel 全部 smooth。

该 index 结论没有说 \(\mathcal T_\lambda\) 可逆，也没有说物理 source 上的 \(m\) 个 trace covectors 独立：在均匀背景它们对所有 zero-mean 物理 tangents 可一阶为零。增广 cokernel 可以在 finite graph normal 方向非零，而在物理 source 切片上消失。

### 3.2 边界障碍恰是实际 trace covectors

cyclic 引理把 \(\mathcal T_\lambda(p,t,C_*)=(h,0,0,0)\) 的可解性刻画为所有实际 normalized class derivatives 为零。其显式 source covectors由 (16) 给
\[
dF_{\lambda,r}(h)=
\int_0^L
\left[
\alpha_h W_{sf,r}
+W_{fs,r}\beta_h
+\operatorname{tr}(W_{ss,r}K_h)
\right]dx,
\tag{22}
\]
其中可将 \(W_r\) 换成 trace-free \(W_r^0\)。\(K_h\) 的配对是
\(\operatorname{tr}\{(\int W_{ss,r})K_h\}\)，属于有限 graph 项；
\(\alpha_h,\beta_h\) 的 means 也给 finite terms。periodic state-frame 的变分在 (22) 中积分成零，因为 \(W_r\) 是 homogeneous adjoint。这里没有额外 assumed canonical Poisson matching。

这给 full trace differential kernel 的明确 first-order/Fredholm 表示。它仍是逐个固定谱点的表示，不能据 (21) 推出全谱共同核已经由 trace Hamilton 场生成。

## 4. 原 physical Poisson tensor 在状态图的准确主符号

对原 centered \(C_{ij}=b_i\delta_{ij}+d_i s_{ij}\)，
\[
F_i=(ECd)_i/S
=\frac{d_i}{S}\left(
\Delta_i-\frac1S\sum_{j<m}d_j\Delta_j+\sum_{j=0}^{m}s_{ij}d_j
\right),\quad i<m.
\]
因 \(\partial\Delta_i/\partial q_j=\delta_{ij}\)，得到全场恒等式
\[
\boxed{\quad
A:=F_q=\frac{\operatorname{diag}(d_{\rm first})}{S}
-\frac{d_{\rm first}d_{\rm first}^{T}}{S^2},\qquad A^T=A.
\quad}
\tag{23}
\]
不是仅 uniform 处的对称性。

用 \(f=Dd_{\rm first}\) 作为 smooth zero-mean 源坐标。原 (3) 化为
\[
J_{q,f}=\frac1{16}
\begin{pmatrix}0&I_mD^2\\-I_mD^2&0\end{pmatrix};
\tag{24}
\]
正号来自 \(D^*=-D\)，不能继续抄成 \(-\operatorname{offdiag}D^2/16\)。

将 row \(a,q\) 以 column of components 记录，(11)、(14) 的 derivative
\(\Lambda=D(q,f)\mapsto D(P_0a,P_0b)\) 的 order-zero 主部为
\[
\Lambda_0=
\begin{pmatrix}
G^T&0\\
G^{-1}A&-G^{-1}/S
\end{pmatrix},
\qquad \Lambda-\Lambda_0\text{ 为 order }-1
\text{ 加 finite rank}.
\tag{25}
\]
例如 \(\dot a=\dot q\,G+ak\)，
\(\dot b=G^{-1}(A\dot q-D\dot d/S+\text{zero-order }\dot d)-kb\)；
在 \(f\) 坐标里 \(\dot d=D^{-1}\dot f\)，故被省略项至少低一阶。
target \(P_0\) 投影只改变有限秩部分。

原张量的 pushforward \(\Lambda J_{q,f}\Lambda^*\) 因 (23) 精确得到
\[
\boxed{\quad
J_y=
\frac1{16S}
\begin{pmatrix}0&-I_mD^2\\I_mD^2&0\end{pmatrix}
+R_1,\qquad
R_1:H^{s+1}\to H^s\text{ 有界}
\quad(s\ge0).
\quad}
\tag{26}
\]
下右 order-two coefficient 为
\(G^{-1}(A^T-A)G^{-T}/(16S)=0\)；
交叉 principal coefficients 中 \(G^TG^{-T}=I\) 与 \(G^{-1}G=I\) 恰消去所有状态系数。
variable multiplication 与 \(D^2\) 的 commutators，以及 order-\(-1\) 的 gauge derivative，均只贡献 order \(\le1\)；finite graph 部分仍为有限秩。

(26) 是原 physical tensor 的 elliptic、constant principal symbol，保留准确 \(1/(16S)\)。它不等于标准 vector NLS 的 order-zero canonical tensor。状态逆自身不能提供 action/norming 坐标，因而 (26) 目前不能直接重用 M2 的 action-angle Fredholm 闭包定理。

## 5. λ-independent periodic gauge 在物理图内没有非零方向

下面的刚性是本稿 §6 的必要最后一步。

假设 physical tangent 满足
\(\dot A^0_\lambda=g_x-[A^0_\lambda,g]\)，且 \(g(x)\) 不依赖 \(\lambda\)。
由于 \(\dot A^0_\lambda\) 的 \(\lambda\) coefficient 为零，
\[
[E_{ff}-I/M,g]=0.
\]
故 \(p=t=0\)，\(g=\operatorname{diag}(\sigma,Z)\)。第一 scalar block给
\(\sigma_x=-\operatorname{tr}K/M\)。periodicity 强制 \(\operatorname{tr}K=0\)，再给 \(\sigma\) constant。slow block
\[
Z_x-[H,Z]=K
\]
与 no-alias 条件使全部非零 Fourier modes \(Z_n\) 为零；Z constant。写 \(C=Z-\sigma I\)，则
\[
\dot a=-aC,\quad \dot b=Cb,\quad \dot H=[C,H].
\tag{27}
\]
这恰是内部 constant \(GL_m\) frame 方向。

已有物理 graph 的 finite-minor transversality排除 (27) 中的非零 physical tangent。可将其微分形式单独说明：以 (12) 的 finite graph normals配对
\((-aC,Cb,[C,H])\)，得到从 \(\operatorname{Mat}_m\) 到 finite normal space 的矩阵。
在均匀背景，\(D\mathcal A=D\mathcal B=D\mathcal H=0\)，这个矩阵由
\((-q_*C,Cr_* ,[C,H_*])\) 给出。H_* simple 且 \(q_*P_\ell r_*\ne0\)，所以矩阵单射。
选择一个非零 \(m^2\) minor，它在一个共同 smooth/low state 邻域内仍非零。故该邻域任何物理 tangent 的 constant-frame orbit 方向只能为零。

原 χ frame 到 (15) 需使用一个实际 periodic、与 \(\lambda\) 无关的 SL-normalized frame
\[
\mathfrak F=
T_z\,\operatorname{diag}(1,G)\,(\det G)^{-1/M}.
\tag{28}
\]
near-I 的 determinant root 是唯一 local periodic branch；\(\det T_z\) 为非零常数。
\(D\log\det G=\operatorname{tr}V-\operatorname{tr}H\) 精确把 source trace subtraction改成 (15) 的 constant trace subtraction。
任一 original gauge \(g^\chi\) 因而变成
\[
g^A=\mathfrak F^{-1}g^\chi\mathfrak F
-\mathfrak F^{-1}\dot{\mathfrak F}.
\tag{29}
\]
如果 original \(g^\chi\) 不依赖 \(\lambda\)，(29) 也不依赖 \(\lambda\)，因此以上刚性适用于原 physical affine connection。省掉 \(\dot{\mathfrak F}\) 会给错误的规范代表。

## 6. 有有限有理规范证书的共同核方向属于 Hamilton 闭包

### 精确充分定理

设当前 physical state 在 §§2、5 的近背景域中。取一个 smooth physical tangent \(v\)。假设存在 periodic trace-free gauge \(g(x,\lambda)\)，具有以下额外性质：

* \(\dot L_\lambda(v)=g_x-[L_\lambda,g]\) 作为 \(\lambda\) 的 meromorphic identity 成立；
* \(g\) 是 \(\lambda\) 的有理函数，在 infinity 有界，极点集合为一个与 x 无关的固定有限集合，有限 Laurent coefficients 均 smooth periodic；
* 全部有限 poles \(\mu_j\) 的 actual \(N_{\mu_j}\) cyclic，且先取 \(\mu_j\ne\pm S\)。

那么
\[
v\in
\operatorname{span}\left\{
X_{\partial_\mu^k F_{\mu,r}}\big|_{\mu=\mu_j}:
1\le r\le M-1,\ 0\le k< p_j
\right\},
\tag{30}
\]
其中 \(p_j\) 是对应 pole 阶。尤其所有 poles simple 时，v 是有限个实际 \(X_{F_{\mu_j,r}}\) 的线性组合。
一般有限阶 pole 时，
\[
v\in\overline{\operatorname{span}\{X_{F_{\mu,r}}\}}^{\,C^\infty}.
\tag{31}
\]

### 证明

在一个 p 阶 pole \(\mu\) 写
\[
g=\frac{R_p(x)}{(\lambda-\mu)^p}+\cdots.
\]
因 \(\dot L_\lambda\) 没有 pole，最高 coefficient满足
\[
(D-\operatorname{ad}L_\mu)R_p=0.
\tag{32}
\]
cyclic lemma 给所有 periodic homogeneous trace-free adjoints 恰由
\(\{W_{\mu,r}^0:1\le r\le M-1\}\) 张成。因此 \(R_p=\sum_r c_rW_{\mu,r}^0\)。

(10) 的 \(\partial_\mu^{p-1}g_{\lambda,\mu,r}\) 最高 pole coefficient为
\[
-(p-1)!\frac{S^2-\mu^2}{16S}W_{\mu,r}^0
\quad\text{在 }(\lambda-\mu)^{-p}\text{ 前}.
\tag{33}
\]
该 coefficient 非零缩放，故可用一个有限线性组合精确消去 \(R_p\)。对 (8) 在固定 source、固定 \(\lambda\) 求 \(\mu\) 导数给
\[
\dot L_\lambda(X_{\partial_\mu^{p-1}F_{\mu,r}})
=(\partial_\mu^{p-1}g_{\lambda,\mu,r})_x
-[L_\lambda,\partial_\mu^{p-1}g_{\lambda,\mu,r}],
\tag{34}
\]
因为 physical \(J\) 不依赖谱参数。
相减既消去 gauge 的最高 pole，也相应减去真正 physical Hamilton tangent；
其他 poles 不受影响。逐阶、逐个 pole 进行有限次，剩余 gauge 无有限 poles、且仍 rational bounded at infinity，因而不依赖 \(\lambda\)。

§5 使剩余 physical tangent 为零，所以得到 (30)。实际 monodromy ODE、gradient 和其全部空间 jets在 bounded \(\mu\) 盘内解析；有限差分
\(X_{\partial_\mu^kF_{\mu,r}}\) 因而在全部 \(C^\infty\) seminorm同时是实际 \(X_{F_{\nu,r}}\) 的极限，得到 (31)。取实部/虚部可在原实物理场空间得到相应实闭包；没有假定标准 NLS 的 real structure。

pole 位于 \(\pm S\) 时 (33) 退化，不能直接除 \(S^2-\mu^2\)。这一附加限制用于保持当前定理的最简审计版；不代表原场在这些谱点失败。若另处理 critical poles，应使用更高的 \(\mu\)-jets并逐式核验其最高 Laurent coefficient，而不能沿用 (33) 的非零缩放。

### 证明真正没有提供的部分

局部 cyclic kernel 引理只在每个 cyclic neighborhood给某个 local holomorphic \(g(x,\lambda)\)。它没有给：

* 一个 global rational、bounded-at-infinity periodic gauge；
* 对不同谱邻域的解可作保留 physical affine variation 的有理逼近；
* 任意共同谱核 v 可由满足 (30) 假设的 physical tangents 在 \(C^\infty\) 中逼近。

上述任一点若被证明，可与本节的 pole 消元接合推进 all-M 闭包。没有这一步，(31) 只能应用于带上述有限有理证书的方向。这里没有借 entire growth，也没有把局部规范解的非唯一性当成 global approximation 定理。

## 7. 当前结果对完整目标的准确贡献

(8) 明确给所有实际 trace powers 的 Hamilton 场一个 rational periodic gauge；(17)–(22) 明确给任意 common trace-kernel tangent 的 fixed-parameter约束方程和有限 boundary obstruction；(26) 明确给原物理张量的 constant elliptic principal symbol；(30)–(31) 将可有限有理表示的物理核方向准确化为 Hamilton span/闭包。

仍缺 general-M class/action 或 squared-eigenfunction 完备性，或者本稿 §6 所列的 global gauge approximation。framed full monodromy 的 L²↔ℓ² 状态逆保留了 norming frame，但 scalar class 数据没有提供这些样点；它不能自动填补这个缺口。原共同行为叶的 regularity、实际 fiber internal tangent 等号也未由本稿推出。

## 8. 独立子审核对

子审 rational_gauge_audit 已分别手核：原 J 到 (6) 的系数；partial trace 的无 transpose约定；(7) 的符号；(10)、(33) 的留数和 factorial；消去极点的物理谱参数微分；(29) 中必须有的负 frame derivative；normalized scalar block强制 trace variation零；near-background finite-minor横截性。未发现推导缺项。子审明确保留 §6 的额外 global rational 条件，未将其提升成全部共同核的结论。
