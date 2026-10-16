# M2 实际迹核、周期规范方程与临界等谱纤维：独立审计

2026-10-11。独立读取并使用 [实际 Floquet 审稿 §13–14](../../刘维尔可积性/research/spectral_independent_review_20261011.md) 的连接、原物理括号及 actual trace 对合。下面的线性代数、周期 ODE、临界反例和半线稳定图估计重新逐项推导；没有运行旧检查。

## 1. 设定与结论

空间为 \(\mathbb T_L\)，\(S\in\mathbb R\setminus\{0\}\)，\(\delta=S/2\)。固定光滑实物理场 \(z=(u,v)\)，组件空间均值固定。准确的 traceless connection 为

\[
L_\lambda=L^0_\lambda+\frac u2H+vK_\lambda,\qquad
H=\begin{pmatrix}1&0\\0&-1\end{pmatrix},
\]
\[
L^0_\lambda=\frac S2(E-F)+\frac\lambda2(E+F),\qquad
K_\lambda=\frac\lambda S H+(1+\lambda/S)E+(1-\lambda/S)F,
\tag{1}
\]

其中 \(E_{12}=F_{21}=1\)，其余元素为零。令

\[
Y_x=L_\lambda Y,\quad Y(0)=I,\qquad
N_\lambda=Y(L),\quad F_\lambda=\operatorname{tr}N_\lambda .
\tag{2}
\]

\(\det N_\lambda=1\)。对实际物理变分 \(h=(\dot u,\dot v)\)，
\(A_\lambda=\delta L_\lambda=\dot uH/2+\dot vK_\lambda\) 光滑、周期且 traceless。

**固定参数命题成立：** 若 \(F_\lambda^2-4\ne0\)，则

\[
\delta F_\lambda=0
\quad\Longleftrightarrow\quad
A_\lambda=G_{\lambda,x}-[L_\lambda,G_\lambda]
\quad\text{有光滑周期 }G_\lambda\in\mathfrak{sl}_2(\mathbb C).
\tag{3}
\]

对实 \(\lambda\)，所有量实，\(G_\lambda\) 可取在 \(\mathfrak{sl}_2(\mathbb R)\)。该等价关系实际上对所有 **非中心** \(N_\lambda\ne\pm I\) 成立，包括非中心 Jordan 谱点。中心点的正确条件则为 \(\delta N_\lambda=0\)，仅有 \(\delta F_\lambda=0\) 不够。

固定参数规范方程不证明物理 Hamilton 场充满实际迹核；§6 给出其逻辑差别，§5、§7 给出均匀临界背景上的实际线性及非线性见证。

## 2. 实际变分公式与周期 ODE 的准确符号

本节暂时省略 \(\lambda\)。微分初值积分方程，或直接令 \(Z=Y^{-1}\delta Y\)，得

\[
Z_x=Y^{-1}AY,\qquad Z(0)=0,\qquad
I_A=\int_0^L Y^{-1}AY\,dx,\qquad
\delta N=NI_A .
\tag{4}
\]

每个被积矩阵 traceless，故 \(I_A\in\mathfrak{sl}_2\)。因此

\[
\delta F=\operatorname{tr}(NI_A),\qquad
\operatorname{tr}(N^{-1}\delta N)=0 .
\tag{5}
\]

第二式也是实际 determinant 变分。它不能在论证中被遗漏。

令 \(g=Y^{-1}GY\)，则

\[
g_x=Y^{-1}(G_x-[L,G])Y=Y^{-1}AY.
\]

所有解恰为

\[
G(x)=Y(x)\left(g_0+\int_0^xY^{-1}AY\,d\xi\right)Y(x)^{-1}.
\tag{6}
\]

周期端点条件 \(G(L)=G(0)=g_0\) 等价于

\[
N(g_0+I_A)N^{-1}=g_0
\quad\Longleftrightarrow\quad
( \operatorname{Ad}_{N^{-1}}-I)g_0=I_A
\quad\Longleftrightarrow\quad
\delta N=[g_0,N].
\tag{7}
\]

这里的交换子符号与 (3) 一致。光滑周期系数及 \(G(L)=G(0)\) 使 ODE 的逐次微分在两端一致，故 (6) 给圆周上的光滑周期解，而不只是端点相等的区间函数。

反向蕴含立即成立：若周期 \(G\) 存在，则 (7) 给
\(\delta F=\operatorname{tr}[g_0,N]=0\)。

## 3. 正则 monodromy 共轭轨道与显式解

写

\[
B=N-\frac F2I,\qquad
\Delta=F^2-4,\qquad d=\frac{\Delta}{4}.
\]

Cayley–Hamilton 给

\[
B^2=dI,\qquad N^{-1}=\frac F2I-B.
\tag{8}
\]

若 \(\delta F=0\)，(5) 同时给

\[
\operatorname{tr}\delta N=0,\qquad
\operatorname{tr}(B\delta N)=0.
\tag{9}
\]

对 traceless \(X\) 有 \(BX+XB=\operatorname{tr}(BX)I\)；故在
\(\operatorname{tr}(BX)=0\) 的二维空间上，

\[
[B,[B,X]]=4dX=\Delta X .
\tag{10}
\]

在 \(\Delta\ne0\) 时，取

\[
\boxed{\quad
g_0=-\frac{[B,\delta N]}{\Delta},\qquad
G(x)=Y(x)\left(g_0+\int_0^xY^{-1}AY\,d\xi\right)Y(x)^{-1}.
\quad}
\tag{11}
\]

由 (10)，
\([g_0,N]=-[ [B,\delta N],B]/\Delta=\delta N\)；
因此 (7) 成立。这是无特征值选支、无本征向量归一化的显式证明。

同一结构也解释了正则共轭轨道：\(SL_2\) 的切空间有维数 3，固定 determinant 与 trace 的切向量满足 (9)，有维数 2；\(\Delta\ne0\) 时 \(N\) 的特征值不同，其共轭轨道切空间
\(\{[g,N]:g\in\mathfrak{sl}_2\}\) 也有维数 2，且 (11) 明确实现了全部这种切向量。这里是实际 monodromy 的共轭切线，没有使用形式 resolvent。

所有周期解的差为

\[
G_{\rm hom}(x)=c\,Y(x)B Y(x)^{-1},\qquad c\in\mathbb C.
\tag{12}
\]

因为非中心 \(2\times2\) 矩阵在 \(\mathfrak{sl}_2\) 中的 centralizer 是一维的 \(\mathbb C B\)。在 \(\Delta\ne0\) 时，(11) 的条件 \(\operatorname{tr}(Bg_0)=0\) 固定这一自由度。

### 3.1 非中心 Jordan 点也成立

用 trace 配对 \(\langle X,Y\rangle=\operatorname{tr}(XY)\)：

\[
\operatorname{ran}(\operatorname{Ad}_{N^{-1}}-I)
=\bigl(\ker(\operatorname{Ad}_{N}-I)\bigr)^\perp
=(\mathbb C B)^\perp
\quad(N\ne\pm I).
\tag{13}
\]

\(\delta F=\operatorname{tr}(NI_A)=\operatorname{tr}(BI_A)\)，因此 (13) 给 (7) 可解的充分必要条件，完全不需要 \(d\ne0\)。所以 \(F^2-4=0\) 但 \(B\ne0\) 的非中心 Jordan 点仍满足 (3)。

在 \(N=\pm I\) 时，(7) 左侧的线性算子为零，周期解存在当且仅当 \(I_A=0\)，即 \(\delta N=0\)。此时 \(\delta F=0\) 对每个 traceless 变分自动成立，不能作为共轭切线判据。

## 4. 随谱参数的解析选择及临界障碍

对固定光滑源及变分，(1) 的系数对 \(\lambda\) 为多项式。Volterra 级数在每个紧参数集一致收敛，故 \(Y,N,\delta N,F\) 为整函数；\(Y^{-1}\) 也整，且其 \(x\) 导数在每个固定 \(C^r\) 范数中具有同样的局部一致解析性。

若已知 \(\delta F_\lambda=0\) 对全部参数成立，则 (11) 在

\[
\Omega_{\rm reg}=\{\lambda:\Delta(\lambda)\ne0\}
\]

给 **单值全纯** 的 \(C^\infty_x\) 周期 \(G_\lambda\)。不需要对 Floquet 特征值的平方根作全局选支。只在一个固定参数知道 \(\delta F=0\)，不提供一个全参数规范族。

存在一个正则参数时，整函数 \(\Delta\) 不恒为零，其零点离散。在紧正则参数集上 \(|\Delta|\) 有正下界，(11) 与 ODE 给通常的有限阶连续依赖；靠近临界点则不能保持这一分母界。

- **非中心 Jordan 点：** \(\operatorname{Ad}_{N^{-1}}-I\) 的 rank 在附近恒为 2。选一个固定二维补空间与非零 \(2\times2\) minor，可由 (13) 的相容条件求出局部解析 \(g_0\)。所以 (11) 在这里出现的 pole 可以是其特定 normalization 的 pole，不能据此宣称实际规范方程无解。局部选择的差仍为 centralizer 方向。
- **中心点：** rank 降为 0。必须先满足 \(\delta N=0\)；否则任何解析或连续的周期规范族都不能跨过该点。即便逐点满足 \(\delta N=0\)，全纯选择还可能有更高消失阶的可除性条件。

后一项有一个独立的解析矩阵例子。取空间周期 1、
\(L(t)=t^2H,\ A(t)=tE\)，均为常系数。则

\[
N(t)=e^{t^2H},\qquad
\delta N(t)=t\,\frac{\sinh(t^2)}{t^2}E,\qquad
\delta F(t)=0 .
\]

在 \(t=0\)，\(N=I,\delta N=0\)，所以该单点有周期规范解。然而在 \(t\ne0\)，
\([g_0,N]=\delta N\) 强制 \(g_{0,E}=-1/(2t)\)，无法解析跨过 0。这是一般解析 connection 的例子，不声称它属于 (1) 的物理仿射参数族。它说明仅检查中心点的值还不足以证明全参数解析延拓。

## 5. 原 M2 物理叶上的中心谱点反例

取真实均匀物理场 \(u=v=0\)，仍为任意 \(S\ne0\)。选整数 \(n\ge1\)，使
\(k=2\pi n/L>|S|\)，并令

\[
\lambda_* = i\sqrt{k^2-S^2}.
\]

此时

\[
(L^0_{\lambda_*})^2=-\frac{k^2}{4}I,\qquad
N_{\lambda_*}=e^{L L^0_{\lambda_*}}=(-1)^n I.
\tag{14}
\]

取 **真实、光滑、组件均值为零** 的实际物理变分

\[
\dot u(x)=\cos(kx),\qquad \dot v(x)=0,\qquad
A_\lambda(x)=\tfrac12\cos(kx)H.
\tag{15}
\]

对全部 \(\lambda\)，背景 \(Y=e^{xL^0_\lambda}\) 与 \(N=e^{LL^0_\lambda}\) 交换，cyclic trace 给

\[
\delta F_\lambda
=\operatorname{tr}(N_\lambda H/2)\int_0^L\cos(kx)\,dx=0.
\tag{16}
\]

在 \(\lambda_*\)，\(H\) 与 \(L^0_{\lambda_*}\) 反交换，故

\[
e^{-xL^0_{\lambda_*}}H e^{xL^0_{\lambda_*}}
=\cos(kx)H-\frac{\sin(kx)}k[L^0_{\lambda_*},H].
\]

代入 (4) 得

\[
I_A=\frac L4H,\qquad
\boxed{\quad \delta N_{\lambda_*}=(-1)^n\frac L4H\ne0.\quad}
\tag{17}
\]

因此这个物理变分在 **全部实际 trace 的共同核** 内；但在 \(\lambda_*\) 不存在周期 \(G_{\lambda_*}\)。即使允许规范生成元依赖 \(\lambda\)，也不可能得到跨过所有谱点的全纯周期族。正则集上的 (11) 不受这一反例影响。

## 6. 与物理 Hamilton 张成的关系

本问题的真实 Poisson 算子是

\[
J_{uv}=-\frac1{16}\begin{pmatrix}0&D\\D&0\end{pmatrix},
\qquad X_{F_\lambda}=J_{uv}\,dF_\lambda .
\tag{18}
\]

周期 \(\mathfrak{sl}_2\) 规范函数 \(G_\lambda\) 是 connection 的辅助变量；它不是物理梯度，也没有自动给出一个物理 Hamilton 泛函。实际物理变分还要求同一个 \((\dot u,\dot v)\) 在所有参数满足
\(A_\lambda=\dot uH/2+\dot vK_\lambda\)，而逐参数 ODE 允许各参数独立选择 \(G_\lambda\)。

已证物理对合只给

\[
\operatorname{span}_{\mathbb R}\{X_{\operatorname{Re}F_\lambda},
X_{\operatorname{Im}F_\lambda}\}
\subseteq \bigcap_\lambda\ker dF_\lambda.
\tag{19}
\]

反向包含需要原物理弱辛形式中的非线性最大各向同性，以及适当的无限维拓扑闭包；(3) 不提供这些结论。

均匀 \(z=0\) 给一个直接检查：\(W_\lambda=Y N_\lambda Y^{-1}=N_\lambda\) 空间恒定，(76) 的两个实际梯度为常数，因此 \(D\) 杀掉它们，

\[
X_{\operatorname{Re}F_\lambda}(0)=
X_{\operatorname{Im}F_\lambda}(0)=0
\quad\text{对全部 }\lambda.
\tag{20}
\]

同一背景上所有组件均值零的切向量都满足 \(\delta F_\lambda=0\)。故在此临界背景，Hamilton 张成空间为零，而共同迹核不为零。这个临界背景见证不反驳未来在正则非线性谱层上的完备性命题。

## 7. 进一步独审：实际半线稳定图位于均匀背景的全迹纤维

本节审查以下新增 nonlinear lemma。取
\(k_0=2\pi/L,\ 0<|S|<k_0\)，固定均值零的真实 \(u,v\)，在零通量规范内考虑

\[
\begin{aligned}
u_t&=-u_{xx}-2S v_x+\frac2S D(u^2v),\\
v_t&= v_{xx}-\frac S2u_x+\frac2S D(uv^2).
\end{aligned}
\tag{21}
\]

### 7.1 原方程与线性谱的符号

对 M2，格点零均值模上的 \(R=0\)。重构

\[
p=(u,-u),\quad s=\frac8h(v,-v),\quad
c=\frac{4S}{h},\quad
b=-\frac{\Pi(ps)}c=-\frac{2uv}{S}.
\tag{22}
\]

原约化方程
\(p_t=-p_{xx}-D(bp)-P_0D(p^2/2+\beta w^2)\)、
\(s_t=s_{xx}-cp_x-D(bs)-P_0D(ps)\)
恰给 (21)：\(p^2,ps\) 的格点零均值部分为零，
\(P_0(\beta w^2)_0=2Sv\)。故没有改变原非线性方程。

写 \(z_t=\mathcal A z+D\mathcal N(z)\)，
\[
\mathcal N(z)=\frac2S(u^2v,uv^2),\qquad
\mathcal A(k)=
\begin{pmatrix}k^2&-2iSk\\-iSk/2&-k^2\end{pmatrix}.
\]

对 \(k\in k_0\mathbb Z\setminus\{0\}\)，

\[
\mathcal A(k)^2=\Lambda_k^2 I,\qquad
\Lambda_k=\sqrt{k^4-S^2k^2}>0,\qquad
\Pi_\pm(k)=\frac12\left(I\pm\frac{\mathcal A(k)}{\Lambda_k}\right).
\tag{23}
\]

\(\Pi_\pm\) 为一致有界的零阶 Fourier 乘子，
\(\Pi_\pm(-k)=\overline{\Pi_\pm(k)}\)，保持真实场和均值零。无需声称它们在普通 \(L^2\) 内正交。
\(\Lambda_*=\min_{k\ne0}\Lambda_k>0\)，且 \(\Lambda_k\ge c_S k^2\)。

### 7.2 全半线收缩与未来积分

取 \(s>1/2,\ 0<\gamma<\Lambda_*\)，定义

\[
X_\gamma^s=\left\{z\in C([0,\infty);H^s_0(\mathbb T_L;\mathbb R^2)):
\|z\|_{X_\gamma^s}=\sup_{t\ge0}e^{\gamma t}\|z(t)\|_{H^s}<\infty\right\}.
\]

这里 \(H^s_0\) 表示两个组件空间均值为零。给定
\(a\in\operatorname{ran}\Pi_-\cap H^s_0\)，正确的 Lyapunov–Perron 方程为

\[
\begin{aligned}
z(t)={}&e^{-\Lambda t}a
+\int_0^t e^{-\Lambda(t-\tau)}\Pi_-D\mathcal N(z(\tau))\,d\tau\\
&-\int_t^\infty e^{-\Lambda(\tau-t)}\Pi_+D\mathcal N(z(\tau))\,d\tau .
\end{aligned}
\tag{24}
\]

最后一个负号必需；它给正谱空间的方程
\((\Pi_+z)_t=+\Lambda\Pi_+z+\Pi_+D\mathcal N(z)\)。

任取 \(\gamma<\nu<\Lambda_*\)。高频热估计及低频指数余量给

\[
\|e^{-\Lambda\sigma}\Pi_\pm\|_{H^{s-1}\to H^s}
\le C_{\nu,S}\sigma^{-1/2}e^{-\nu\sigma},\qquad \sigma>0.
\tag{25}
\]

**不能把 (25) 的 \(\nu\) 直接取为 \(\Lambda_*\)：**
最低频在 \(\sigma\to\infty\) 没有额外的 \(\sigma^{-1/2}\) 衰减。

\(H^s\) 是代数，所以在 \(X_\gamma^s\) 的半径 \(R\) 球上，

\[
\|D\mathcal N(z(t))\|_{H^{s-1}}\le C_SR^3e^{-3\gamma t},
\]
\[
\|D(\mathcal N(z)-\mathcal N(\widetilde z))(t)\|_{H^{s-1}}
\le C_SR^2e^{-3\gamma t}\|z-\widetilde z\|_{X_\gamma^s}.
\tag{26}
\]

对过去积分加权可用
\(\int_0^\infty\sigma^{-1/2}e^{-(\nu-\gamma)\sigma}d\sigma<\infty\)；
对未来积分则用
\(\int_0^\infty\sigma^{-1/2}e^{-(\nu+3\gamma)\sigma}d\sigma<\infty\)。
因此两项合起来给 \(C_{\gamma,S}R^3\) 的球内界和
\(C_{\gamma,S}R^2\) 的 Lipschitz 常数。取
\(R=2C\|a\|_{H^s}\) 足够小，(24) 是收缩。

未来积分是 \(H^s\) 中的实际 Bochner 积分：\(\tau=t\) 的奇性可积，远端指数可积；没有使用不受控的正时间逆热半群。所得 \(z=S(a)\) 真实，解析依赖小参数 \(a\)，并保持组件均值零。

### 7.3 方程正则性、光滑参数与同一半线

低阶解属于 \(C_tH^s\)，(24) 在 \(H^{s-2}\) 中可微，并满足 (21)。对未来项微分时，\(A\) 作用于热核在此目标空间仍只有可积的 \(\sigma^{-1/2}\) 奇性；不能直接在 \(H^s\) 中以一个不可积的二阶核作微分。

空间平移与 \(\Pi_\pm,\Lambda,D\) 交换，且 \(\mathcal N\) 无显含 \(x\)。收缩唯一性给

\[
S(T_\eta a)=T_\eta S(a).
\tag{27}
\]

如果 \(a\) 光滑，\(\eta\mapsto T_\eta a\) 在低阶 \(H^s\) 参数空间为 \(C^\infty\)，而 \(S\) 解析。故 (27) 左侧在 **同一** \(X_\gamma^s\) 内为 \(C^\infty\)；差商的分布极限识别其导数为 \(D_x^jz\)。于是所有空间阶导数也属于 \(X_\gamma^s\)。再由 (21) 归纳得到全部时间和混合导数，直到 \(t=0\) 的右端点；各阶保持 \(e^{-\gamma t}\) 衰减。

这里不会随高阶 Sobolev 指标缩短半线或重新要求高阶范数小；高阶常数可以依赖高阶参数范数。

### 7.4 稳定图是真实解析图

在 \(t=0\)，(24) 给

\[
\Pi_-z(0)=a,\qquad
\Pi_+z(0)=\Phi(a)
=-\int_0^\infty e^{-\Lambda\tau}\Pi_+D\mathcal N(S(a)(\tau))\,d\tau ,
\tag{28}
\]

其中 \(\Phi\) 解析且 \(\|\Phi(a)\|_{H^s}\le C\|a\|_{H^s}^3\)。
因此 \(a\mapsto a+\Phi(a)\) 为嵌入，逆参数就是有界投影 \(\Pi_-\)，其在 0 的切空间是整个 \(\operatorname{ran}\Pi_-\cap H^s_0\)。这是真实无限维图，并非有限 Fourier 或两幅值构造。

### 7.5 原 Hamiltonian 与 actual trace 守恒逐项核对

用 split 坐标

\[
q=-S+u,\qquad
r=\frac{(S^2/4-v^2)(1+u/S)-v_x}{S},\qquad C_1=-\int_0^L qr\,dx .
\]

直接展开

\[
qr=\frac{u^2}{4}-\frac{S^2}{4}
-\frac{u^2v^2}{S^2}+v^2-\frac{u v_x}{S}+v_x.
\]

分部积分给准确身份

\[
\boxed{\quad
K=\int_0^L\left(16vu_x+4Su^2+16Sv^2-\frac{16}{S}u^2v^2\right)dx
=-16S C_1+4LS^3.\quad}
\tag{29}
\]

真实变分为

\[
K_u=-16v_x+8Su-\frac{32}{S}uv^2,\qquad
K_v=16u_x+32Sv-\frac{32}{S}u^2v.
\]

代入 (18) 精确产生 (21)。此外直接代入 (21) 并周期分部积分给
\(\frac d{dt}\int uv=0\)，所以 \(A=-2S^{-1}\int uv\) 也守恒。

[实际 Floquet 审稿 §14](../../刘维尔可积性/research/spectral_independent_review_20261011.md) 已证
\(\{F_\lambda,C_1\}_{\rm physical}=0\)，其证明使用 actual Riccati 解和真实 \(C^1\) 余项。因此沿光滑 (21) 轨道，

\[
\frac d{dt}F_\lambda(z(t))
=\{F_\lambda,K\}_{\rm physical}
=-16S\{F_\lambda,C_1\}_{\rm physical}=0.
\tag{30}
\]

这个守恒不是仅由形式留数猜测。原 §14 的小源图限制也不必强加为所有光滑参数的高范数小条件：对任意光滑 \(z\)，
\(\{F_\lambda,C_1\}(tz)\) 是复数 \(t\) 的整函数。确切地，actual connection 仿射，monodromy/梯度在 \(H^3\) 源上整解析；\(C_1\) 为有限局部多项式，\(X_{C_1}:H^3\to H^1\)，其与 actual 梯度的积分配对合法。该整函数在小 \(t\) 上由已证身份为零，故在所有 \(t\) 上为零。这为这里的光滑原轨道补齐了守恒的适用范围。

### 7.6 实际全迹纤维与范围

光滑小 \(a\) 的 \(z(t)\to0\) 在任意固定空间光滑阶成立。Actual monodromy 对源连续，结合 (30)，对每个 \(\lambda\in\mathbb C\) 有

\[
\boxed{\quad F_\lambda(a+\Phi(a))=F_\lambda(0).\quad}
\tag{31}
\]

因此 (28) 的光滑参数部分是均匀背景 actual 全谱 trace 纤维中的真实无限维子流形。它在 0 的非零切空间与 (20) 的零 Hamilton 张成构成 nonlinear 见证，不再只是一次微分的假想纤维方向。

这说明临界等谱纤维可以包含实际非平凡一般函数场；不证明规范生成元跨过中心谱点，也不反驳在正则 generic 谱层上的 Liouville 完备性。这里构造的是半线稳定边界条件选出的实际轨道，未建立全部初值的 Sobolev Cauchy 流、完整 norming/divisor 逆或全部 Hamilton 场的非线性最大性。

## 8. 新的正面全参数桥：无中心单值矩阵时可取整规范族

对固定光滑源及固定物理变分，再明确增加

\[
\Delta\not\equiv0,\qquad N_\lambda\ne\pm I
\quad\text{对全部 }\lambda\in\mathbb C.
\tag{32}
\]

第一项由至少存在一个正则参数保证。在这些条件下，

\[
\delta F_\lambda=0\ \text{对全部 }\lambda
\quad\Longleftrightarrow\quad
\text{存在 }\lambda\text{-整、}C^\infty_x\text{ 周期的 }
G_\lambda\in\mathfrak{sl}_2
\text{ 满足 (3)}.
\tag{33}
\]

反向由 §2 立即成立。正向证明可以完全具体化如下。

1. (11) 的初值 \(g^{\rm can}_0=-[B,\delta N]/\Delta\) 在整个参数平面为 meromorphic；全部 pole 位于 \(\Delta\) 的离散零集。
2. 在每个零点 \(\lambda_j\)，(32) 使 \(B(\lambda_j)\ne0\)，§3.1 的 rank 恒为 2，有限非零 minor 给局部全纯初值 \(g^{(j)}_0\) 且
   \([g^{(j)}_0,N]=\delta N\)。在删去零点的小邻域，
   \(g^{\rm can}_0-g^{(j)}_0=h_j B\)。
   选 \(B(\lambda_j)\) 的非零 entry，除以该 entry 表明 \(h_j\) 是局部 meromorphic scalar，其 principal part 有限。不同局部解相差一个全纯 scalar 乘 \(B\)，故该 principal part 与局部解选择无关。
3. 可以选一个全平面 meromorphic scalar \(h\)，在每个 \(\lambda_j\) 具有 \(h_j\) 的 principal part，且无额外 pole。下面给出所需 Mittag–Leffler 构造，不要求增长估计：若 pole 集无限，按 \(|\lambda_j|\to\infty\) 枚举；将有限的初始 pole 分开。对其余 principal parts \(p_j\)，选 \(R_j\to\infty\) 且 \(R_j<|\lambda_j|\)，然后取 \(p_j\) 在 0 的 Taylor 多项式 \(q_j\)，使
   \(\sup_{|\lambda|\le R_j}|p_j-q_j|\le2^{-j}\)。
   则 \(\sum_j(p_j-q_j)\) 在所有避开 pole 的紧集上正常收敛，具有恰好指定的 principal parts；补回有限初始项即得 \(h\)。有限 pole 时直接求和即可。
4. 因此
   \[
   g^{\rm ent}_0=g^{\rm can}_0-hB
   \]
   在每个零点可去，成为整函数。减去 \(hB\) 不改变交换子，所以
   \([g^{\rm ent}_0,N]=\delta N\) 在正则集成立，随后由解析恒等式在全平面成立。
5. 将 \(g^{\rm ent}_0\) 代入 (6)，实际 variation-of-constants 给整参数族。§2 的端点等式给其周期性；所有空间阶导数在紧参数集上一致全纯。

真实源与变分时，最后用
\[
G^{\rm real}_\lambda
=\tfrac12\left(G_\lambda+\overline{G_{\bar\lambda}}\right)
\]
保持整性、周期性和 (3)，并取得实型
\(G^{\rm real}_{\bar\lambda}=\overline{G^{\rm real}_\lambda}\)。

一个容易核对的充分条件是 **\(\Delta\) 的全部零点简单**：若某点 \(N=\varepsilon I\)，determinant 微分给
\(\operatorname{tr}N'=0\)，即 \(F'=0\)，所以
\(\Delta'=2FF'=0\)，该零点不可能简单。

(33) 确实增强了逐参数规范结论；它没有给 \(\lambda\to\infty\) 的统一增长界。上述 Taylor 校正的次数和大小可以很大，任意 weighted squared-eigenfunction 闭包估计不能从整性中直接读出。因此即使满足 (32)，仍不能从 (33) 宣称 (19) 的反向包含。

## 9. 独核有限正则谱块的实际纤维与弱辛商

已实际读取 [新增正文 §4](../../刘维尔可积性/research/m2_nonlinear_spectral_kernel_20261011.md)。以下结论在其明确假设下成立，并可以不要求弱辛映射 onto 整个 Banach 对偶。

取固定均值叶 \(E=H^s_{\rm per,0}(\mathbb T_L;\mathbb R)^2\)，\(s\ge1\)，有限个真实 actual 谱泛函 \(I_1,\ldots,I_N\)。假设它们在同一个邻域内实解析、真实对合，且已有真实 order-zero 解析 Hamilton 场
\(X_i:E\to E\)。这是有限个 actual trace 的实部/虚部及合法紧轮廓谱组合所具有的性质。再设一个光滑点 \(z_*\) 上
\(dI_1,\ldots,dI_N\) 线性无关。

环境形式为

\[
\Omega(V,W)=\int_0^L(J^{-1}V)\cdot W\,dx,\qquad
J^{-1}=-16\,\mathrm{swap}\,D^{-1}.
\tag{34}
\]

它连续、闭且弱非退化；\(D^{-1}\) 为两个组件均值零的周期逆导数。实际梯度的零均值投影不影响 \(J\)，所以
\(\Omega(X_i,\cdot)=dI_i\)。因而 \(X_i(z_*)\) 独立。可选连续有限 smooth 测试 \(\ell_j\)，使
\(\ell_j(X_i(z_*))=\delta_{ij}\)，并令

\[
\Sigma=z_*+\bigcap_j\ker\ell_j .
\]

有限个真实解析 ODE 流局部存在。对合及常数 \(J\) 给
\([X_i,X_j]=0\)，所以它们构成局部 commuting \(\mathbb R^N\) 作用。映射

\[
\Psi(t,y)=\operatorname{Fl}^{X_1}_{t_1}\cdots
\operatorname{Fl}^{X_N}_{t_N}(y),\qquad y\in\Sigma
\]

在 \((0,z_*)\) 的微分为
\((\dot t,\dot y)\mapsto\sum_i\dot t_iX_i(z_*)+\dot y\)，
是 Banach 直和同构。因此解析逆函数定理给实际局部坐标 \((t,y)\)，不是形式 flow-box。

所有 \(I_i\) 在这些流下恒定。\(dI|_{T\Sigma}\) 仍 onto
\(\mathbb R^N\)：任意 \(V\in E\) 可分为 \(V=\sum_i a_iX_i+\eta\)，\(\eta\in T\Sigma\)，而对合给 \(dI(X_i)=0\)。选有限 smooth 方向 \(\eta_j\in T\Sigma\)，使 \(dI_i(\eta_j)=\delta_{ij}\)，再用有限秩解析 submersion 图，得到真正的 \((t,I,w)\) 局部坐标。

所以固定有限值 \(I=I(z_*)\) 的实际水平集是 split Banach 子流形，其切空间准确为

\[
K_z^N=\bigcap_{i=1}^N\ker dI_i(z).
\tag{35}
\]

其 restricted 二形式的 characteristic 核准确为

\[
\boxed{\quad
\ker\left(\Omega|_{K_z^N}\right)
=\operatorname{span}\{X_1(z),\ldots,X_N(z)\}.
\quad}
\tag{36}
\]

证明需要的只是有限 codimension 的 annihilator 事实：若 \(V\in K_z^N\) 且
\(\Omega(V,\cdot)\) 在 \(K_z^N\) 上为零，则连续泛函
\(\Omega(V,\cdot)=\sum_i a_i dI_i\)。于是
\(\Omega(V-\sum_i a_iX_i,\cdot)=0\) 在全部 \(E\) 上成立，弱非退化给
\(V=\sum_i a_iX_i\)。反向由对合立即成立。没有把 \(\Omega^\sharp:E\to E^*\) 误作满射。

Hamilton 流保持 \(\Omega\)，(36) 又使水平集上二形式对 characteristic 方向为零。因此在上述实际 flow-box 中它与 \(t\) 无关并下降到水平集的局部 \(\mathbb R^N\) 商。下降的形式闭、连续且弱非退化：商切向若 annihilate 全部商方向，将其抬到 \(K_z^N\) 后落在 (36) 的 characteristic span，故商类为零。

光滑子域的相容性也可以具体说明：order-zero actual 谱场与空间平移交换，其解析低阶流及 translation-generator 判据保持同一短时间窗内的全部空间光滑阶；inverse chart 用同一有限时间逆流。有限横截修正和 submersion 修正只加有限 smooth 方向，因此不需要额外的 Fréchet 逆函数定理。

**这证明有限谱块的真实非线性正则商，未证明无限谱纤维的最大性。** 有限水平集仍有无限多个非 characteristic 方向，(36) 并不说有限谱流填满该水平集。取 \(N\to\infty\) 会新增 dual 闭包、谱权重和弱辛像的相容问题；所有有限块的正规性与商不能自动提供该极限。
