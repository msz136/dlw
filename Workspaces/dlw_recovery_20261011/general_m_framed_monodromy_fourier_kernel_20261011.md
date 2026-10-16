# 全 M 校准 framed monodromy 的 Fourier 核与实际 L² 状态逆

2026-10-11。独立核验 Volterra Fourier 核、解析收敛和两种 inverse-function 结论。只写本文件，未运行或重跑脚本。此处状态数据称 **calibrated framed spectral STATE DATA**：所有 monodromy 元素都在已给定的 wave frame 中取值；不以 trace 或 conjugacy class 替代这些元素。

设 \(m=M-1\)，\(a\in L^2_{\rm per}(0,L;\mathbb C^{1\times m})\)，
\(b\in L^2_{\rm per}(0,L;\mathbb C^{m\times1})\)，
\(H\in\mathbb C^{m\times m}\) 为常矩阵。研究实际 ODE
\[
Y_x=A_\lambda Y,\qquad Y(0)=I,\qquad
A_\lambda=\begin{pmatrix}\lambda&a(x)\\b(x)&H\end{pmatrix},
\qquad M_A(\lambda)=Y(L).
\tag{1}
\]
取 \(\lambda_n=2\pi in/L,\ n\in\mathbb Z\)。

结论：

1. 奇数阶 \(2r+1\) 的任意 alternating 多线性项都有一个 \(L^2(0,L)\) Fourier 核。其界含 \(1/r!\)，故非对角数据在任意有界 \(L^2\) 势球上整解析到 \(\ell^2\)；收敛本身无需小幅度。
2. 若 \(H\) 已知，全部整数 \(n\) 的两组非对角数据在 \(a=b=0\) 附近给实际局部解析 \(L^2\leftrightarrow\ell^2\) 状态逆。
3. 若 \(H\) 未知，加入 \(M_A(0)\) 的 slow 底块给有限维实际数据，在真空附近补成 \((a,b,H)\) 的解析状态逆。
4. 若原物理桥另已给出解析 finite graph，且 uniform 处的均值与 \(H\) 图函数的一阶导数为零，则小背景下只取 \(n\ne0\) 的校准非对角子集也可用 IFT 恢复该物理 graph。
5. 全部结论只在 \(L^2/\ell^2\) 层。不主张 raw sequences 保持全部 weighted \(h^N\)，不主张 action-angle、Poisson canonical 性或最大性。

## 1. 真空 benchmark 与首次项

实际 ODE 对 \(L^1\) 系数有唯一 absolutely continuous fundamental matrix。这里 \(L^2\subset L^1\)，可用 convergent Volterra series；以下额外控制采样谱数据的 \(\ell^2\) 范数。

在 \(a=b=0\)，
\[
Y_*(x)=\operatorname{diag}(e^{\lambda x},e^{Hx}).
\]
对固定 \(H\)，非对角数据的一阶 variation 为
\[
D_a(M_A(\lambda))_{0s}\cdot\dot a
=\int_0^Le^{\lambda(L-t)}\dot a(t)e^{Ht}\,dt,
\]
\[
D_b(M_A(\lambda))_{s0}\cdot\dot b
=\int_0^Le^{H(L-t)}\dot b(t)e^{\lambda t}\,dt.
\tag{2}
\]
因此在 \(\lambda_n\)，首次 Fourier 核为
\[
K_0^+(t)=a(t)e^{Ht},\qquad
K_0^-(t)=e^{H(L-t)}b(t).
\tag{3}
\]
在真空 \(H=0\)，准确为
\[
\dot M_{0s}(\lambda_n)=\int_0^L\dot a(t)e^{-2\pi int/L}\,dt,\qquad
\dot M_{s0}(\lambda_n)=\int_0^L\dot b(t)e^{2\pi int/L}\,dt.
\tag{4}
\]
没有遗漏 \(L\) 或 Fourier 的正负号。用 \(L^{-1/2}\) 归一化这些积分，Plancherel 给从两组 \(L^2\) 到两组 \(\ell^2\) 的 isometry。对任意已知常矩阵 \(H\)，(3) 的乘法也有 bounded inverse，范数至多 \(e^{L\|H\|}\)。

## 2. 奇数阶项的实际相位

以 \(\operatorname{diag}(\lambda,H)\) 为自由传播子，对 off-diagonal 插入展开。只有奇数阶 \(k=2r+1\) 能贡献 \(0s\) 或 \(s0\) block。记 ordered simplex
\[
\Sigma_k=\{0<t_1<\cdots<t_k<L\},\qquad
\tau(t)=t_1-t_2+t_3-\cdots+t_{2r+1}.
\tag{5}
\]
总有 \(0<\tau<L\)。

上方 row block 的实际项为
\[
U_r(\lambda)=\int_{\Sigma_{2r+1}}
e^{\lambda(L-\tau(t))}W_r^+(t;H)\,dt,
\tag{6}
\]
其中 chronological path 从 slow sector 开始，在 odd 时刻由 \(a\) 跳到 fast sector，在 even 时刻由 \(b\) 跳回 slow sector。fast 传播子的所有 scalar exponential 已提出；\(W_r^+\) 保留每段 slow 传播的 \(e^{H\cdot}\) 和按原顺序的 \(a,b\)。例如
\[
W_0^+=a(t_1)e^{Ht_1},
\]
\[
W_1^+=a(t_3)e^{H(t_3-t_2)}b(t_2)a(t_1)e^{Ht_1}.
\tag{7}
\]
其 slow 传播时间的总和恰为 \(\tau(t)\)。

下方 column block 为
\[
V_r(\lambda)=\int_{\Sigma_{2r+1}}
e^{\lambda\tau(t)}W_r^-(t;H)\,dt.
\tag{8}
\]
chronological path 在 odd 时刻由 \(b\) 跳到 slow sector，在 even 时刻由 \(a\) 跳回 fast sector；slow 总时间为 \(L-\tau\)。例如
\[
W_0^-=e^{H(L-t_1)}b(t_1),
\]
\[
W_1^-=e^{H(L-t_3)}b(t_3)a(t_2)e^{H(t_2-t_1)}b(t_1).
\tag{9}
\]
特别在整数采样处，(6) 的额外 \(e^{\lambda_nL}\) 准确为 1。因此两个 block 分别是 \(\tau\) 核的负号与正号 Fourier coefficients。

## 3. fiber 参数化与准确体积

设 gaps
\[
s_0=t_1,\quad s_j=t_{j+1}-t_j\ (1\le j\le2r),\quad
s_{2r+1}=L-t_{2r+1}.
\]
则 \(s_j\ge0,\ \sum_js_j=L\)，并且
\[
\tau=s_0+s_2+\cdots+s_{2r}.
\tag{10}
\]
固定 \(\tau\) 时，把最后一个 even gap 和最后一个 odd gap 分别消去。其余 \(r\) 个 even 与 \(r\) 个 odd gaps 独立落在 simplex
\[
\sum_{\ell=0}^{r-1}s_{2\ell}\le\tau,\qquad
\sum_{\ell=0}^{r-1}s_{2\ell+1}\le L-\tau.
\]
从 \(t_1,\ldots,t_{2r+1}\) 到这些 \(2r\) 个变量与 \(\tau\) 的 Jacobian 绝对值为 1。因此所用 fiber Lebesgue 体积恰为
\[
\boxed{\quad v_r(\tau)=
\frac{\tau^r(L-\tau)^r}{(r!)^2}
\le\frac{(L/2)^{2r}}{(r!)^2}.\quad}
\tag{11}
\]
该公式是 kernel 积分的 Lebesgue 参数化，不把 Euclidean coarea 面积误认为同一测度。

定义
\[
K_r^\pm(\tau)=\int_{\text{fiber }\tau}W_r^\pm(t;H)\,dt_{\rm fiber}.
\tag{12}
\]
于是
\[
U_r(\lambda_n)=\int_0^LK_r^+(\tau)e^{-2\pi in\tau/L}\,d\tau,\quad
V_r(\lambda_n)=\int_0^LK_r^-(\tau)e^{2\pi in\tau/L}\,d\tau.
\tag{13}
\]
L² 输入按等价类给出时，这些公式均以 almost-everywhere kernel 与 Lebesgue 积分解释；上述非奇异变量变换与下节估计保证定义不依赖代表元。

## 4. 任意多线性项的 L² factorial bound

每段 slow exponential 的 operator norm 至多 \(e^{\|H\|\times\text{段长}}\)。因此对任意 distinct alternating row/column 输入 \(f_1,\ldots,f_{2r+1}\)，
\[
\|W_r^\pm(t;H)\|
\le e^{L\|H\|}\prod_{j=1}^{2r+1}|f_j(t_j)|.
\tag{14}
\]
先在 fiber 上 Cauchy–Schwarz，再用 (11)，得到
\[
\begin{aligned}
\|K_r^\pm\|_{L^2}^2
&\le e^{2L\|H\|}
\frac{(L/2)^{2r}}{(r!)^2}
\int_{\Sigma_{2r+1}}\prod_j|f_j(t_j)|^2\,dt\\
&\le e^{2L\|H\|}
\frac{(L/2)^{2r}}{(r!)^2}\prod_j\|f_j\|_{L^2}^2.
\end{aligned}
\]
故
\[
\boxed{\quad
\|K_r^\pm(f_1,\ldots,f_{2r+1};H)\|_2
\le e^{L\|H\|}\frac{(L/2)^r}{r!}
\prod_j\|f_j\|_2.
\quad}
\tag{15}
\]
这是独立于输入重复性的真正 multilinear estimate，足以控制 Frechet derivatives 与解析收敛。

若同一 \(a,b\) 重复出现，令 \(A=\|a\|_2,\ B=\|b\|_2\)，还可利用同类时刻的排序。上方有 \(r+1\) 个 \(a\) 时刻和 \(r\) 个 \(b\) 时刻；完整 ordered simplex 包含于两组各自排序的区域。其平方积分至多
\(A^{2r+2}B^{2r}/((r+1)!r!)\)。下方交换 \(A,B\)。因此更强的界为
\[
\boxed{\quad
\|K_r^+\|_2\le
e^{L\|H\|}
\frac{(L/2)^r A^{r+1}B^r}{r!\sqrt{(r+1)!r!}},\qquad
\|K_r^-\|_2\le
e^{L\|H\|}
\frac{(L/2)^r B^{r+1}A^r}{r!\sqrt{(r+1)!r!}}.
\quad}
\tag{16}
\]
并非依靠把 oscillatory integral 逐项取绝对值后的 \(\ell^2\) 求和；先有同一个真实 \(L^2_\tau\) kernel，再用 Parseval。

## 5. 解析 ℓ² 映射与 fixed-H IFT

由较弱的 (15) 已有
\[
\sum_{r\ge0}\|K_r^+\|_2\le e^{L\|H\|}A e^{LAB/2},\qquad
\sum_{r\ge0}\|K_r^-\|_2\le e^{L\|H\|}B e^{LAB/2}.
\tag{17}
\]
故两 kernel series 在任意 bounded \(L^2_a\times L^2_b\times\mathbb C^{m\times m}_H\) 球中一致绝对收敛于 \(L^2\)。每项是 \(a,b\) 的连续 multilinear polynomial，也是 \(H\) 的 entire function；uniform convergence 给 joint Banach-holomorphic map。

它与实际 monodromy 的一致性也可逐点确认：原 off-diagonal Volterra 项在每个 \(\lambda_n\) 的绝对值之和受
\(e^{L\|H\|}\sum_k(\sqrt L(A+B))^k/k!\) 控制，所以它们是实际 ODE 的 convergent Dyson series。另一方面 \(L^2_\tau\) 收敛蕴含 \(L^1_\tau\) 收敛，允许固定 \(n\) 时逐项 Fourier 积分。因此下式的 kernel Fourier 值准确等于实际 \(M_A(\lambda_n)\) 的元素。

定义已归一化的实际数据
\[
\mathcal F(a,b,H)=
L^{-1/2}\big((M_A(\lambda_n))_{0s},
(M_A(\lambda_n))_{s0}\big)_{n\in\mathbb Z}.
\tag{18}
\]
Plancherel 与 (13) 证明 \(\mathcal F\) 是实际 \(\ell^2\)-valued 整解析映射，而非 formal series。对已知 \(H\)，(2)–(3) 给可逆的 bounded derivative。因此 Banach analytic IFT 在 \(a=b=0\) 的某个 \(L^2\) 开邻域给实际局部解析 state inverse，目标是 (18) 附近的 \(\ell^2\) 开集。

为小背景提供显式 sufficient bound，采用 pair norm \(E=A+B\)，令 \(x=LE^2/2\)。由 (15) 的多线性微分，
\[
\|D_{a,b}(\mathcal F-\mathcal F_{\rm linear,H})\|
\le e^{L\|H\|}\big((2x+1)e^x-1\big).
\tag{19}
\]
而 \(H\)-linear derivative 相对 \(H=0\) Fourier isometry 的差至多
\(e^{L\|H\|}-1\)。所以
\[
\|D_{a,b}\mathcal F-\mathcal U\|
\le e^{L\|H\|}-1+
e^{L\|H\|}\big((2x+1)e^x-1\big),
\tag{20}
\]
其中 \(\mathcal U\) 是 (4) 的两组 Fourier isometry。右侧小于 1 就足以由 Neumann series 得可逆 derivative。对 \(\|H_*\|=O(|\delta|)\)、\(A_*+B_*=O(|\delta|\sqrt L)\)，其阶为
\(O(|\delta|L+\delta^2L^2)\)，固定 \(M,L\) 时小背景满足条件。

## 6. H 未知：补 finite framed 数据后的 ambient IFT

若只使用 (18)，则 \(a=b=0\) 时对于所有 \(H\)，数据均为零。因此仅有 offdiag 数据不能恢复未知 \(H\)，尤其不能宣称 \((a,b,H)\) 的真空导数可逆。

在 \((a,b,H)=(0,0,0)\) 的邻域，取 slow 底块
\(M_A(0)_{ss}\)，它接近 \(I_m\)，principal matrix log 由 convergent power series 给出。定义有限维实际数据
\[
\mathcal H(a,b,H)=L^{-1}\log M_A(0)_{ss}.
\tag{21}
\]
它对全部输入解析，在真空
\[
D\mathcal H(\dot a,\dot b,\dot H)=\dot H.
\]
因为第一阶 \(a,b\) 插入只在非对角块，底块的第一阶变化准确为 \(L\dot H\)。

因此 augmented actual framed data
\[
\widehat{\mathcal F}=(\mathcal F,\mathcal H):
L^2_a\times L^2_b\times\mathbb C^{m\times m}
\longrightarrow\ell^2_{2m}\times\mathbb C^{m\times m}
\tag{22}
\]
在真空的 derivative 是 \(\mathcal U\oplus I\)。analytic IFT 给一个实际局部解析双逆。可以等价地输入 \(M_A(0)_{ss}\) 而不取 log；其有限维 derivative 则为 \(L\dot H\)。

此处加入的是 full framed monodromy 的实际底块，不是 eigenvalues、trace 或其他 class invariants。

## 7. 已验证 finite physical graph 的 conditional subset IFT

下述应用要求原物理桥已另外给出：

- 解析 \(L^2\) 状态坐标 \((a_0,b_0)\in(L^2_0)^{2m}\)，以及恢复原物理场的状态逆；
- 其 full calibrated 系数是 finite graph
\[
a=a_0+\alpha(a_0,b_0),\quad
b=b_0+\beta(a_0,b_0),\quad
H=\mathfrak h(a_0,b_0),
\]
其中 \(\alpha,\beta,H\) 是有限维常量图函数；
- uniform 背景对应 \((a_0,b_0)=0\)，
\(D\alpha(0)=D\beta(0)=D\mathfrak h(0)=0\)，以及
\(\|\alpha(0)\|+\|\beta(0)\|+\|H_*\|=O(|\delta|)\)。

本文件不以核估计替代这些物理桥的证明。若上述条件成立，取
\[
\mathcal F_{\rm phys}(a_0,b_0)
=P_{n\ne0}\mathcal F(a,b,H).
\tag{23}
\]
背景处 finite graph 的导数准确消失，所以其 derivative 就是 (20) 的 fixed-\(H_*\) derivative 限制到零均值输入，再投影掉 \(n=0\)。vacuum Fourier isometry 限制后仍是
\[
(L^2_0)^{2m}\ \xrightarrow{\ \mathcal U\ }\ 
(\ell^2_{\mathbb Z\setminus\{0\}})^{2m}
\]
的同构。投影的 norm 不超过 1，故充分小但非零 \(\delta\) 时仍有可逆 derivative。analytic IFT 给实际 calibrated offdiag 子集的 \(L^2/\ell^2\) 局部状态逆。未取的 \(n=0\)、slow 底块和其他 framed 数据随后是该子集的解析图函数。

若均值/\(H\) 图函数的一阶导数未被证明为零，须另计
\(D_H\mathcal F\,D\mathfrak h\) 及 \(D\alpha,D\beta\)；仅凭 \(H_*=O(\delta)\) 不能省略这些项。

## 8. 原 Nχ 的 endpoint calibration 是独立输入

物理桥的矩阵 \(M_A\) 是原 \(N_\chi\) 经 endpoint frame
\[
E_0=T(d(0))\operatorname{diag}(1,G(0))
\]
校准后的 source-dependent similarity。按桥稿给定的规范，
\[
M_A(\lambda)=E_0^{-1}N_\chi(\lambda)E_0.
\tag{24}
\]
若采用另一个 scalar normalization 或 centered spectral parameter，其已知因子和参数变换也须按原规范保留。

本稿的 IFT 对象是 (18)、(22)、(23) 的 **calibrated framed spectral STATE DATA**。从 original full \(N_\chi\) 加有限 \(E_0\) 可以计算这些实际采样；从 raw \(N_\chi\) 单独，本稿未证明所选数据可计算，更未证明 intrinsic spectral image 的 onto 性。物理状态逆建立后，endpoint 与未取数据可按原 finite graph 附加约束恢复；这不能反过来省略 input calibration 的论证。

## 9. weighted h^N 失败的明确 benchmark

raw sampled data 一般不把 smooth periodic 系数送到全部 weighted \(h^N\)。

第一种精确反例：\(m=1,\ b=0,\ a\) 是非零常数，\(H=h\ne0\) 是常数且 \(e^{hL}\ne1\)。upper triangular ODE 给
\[
M_{01}(\lambda_n)
=a\frac{e^{hL}-1}{h-\lambda_n}.
\tag{25}
\]
它有非零 \(1/n\) 尾，属于 \(\ell^2\)，但不属于 \(h^1\)。(3) 的 kernel \(a e^{ht}\) 在周期端点不匹配，准确解释这个尾部。

第二种 benchmark：\(m=1,\ H=0,\ a,b\) 为非零常数。odd third-order kernel 为
\[
K_1^+(\tau)=a^2b\,\tau(L-\tau).
\]
对 \(n\ne0\)，
\[
\int_0^L\tau(L-\tau)e^{-2\pi in\tau/L}\,d\tau
=\frac{2L}{\lambda_n^2}.
\tag{26}
\]
准确常矩阵 exponential 同样给
\[
M_{01}(\lambda_n)=\frac{2La^2b}{\lambda_n^2}
+O(|\lambda_n|^{-4}).
\tag{27}
\]
所以即使 \(H=0\) 且源完全 smooth，raw 数据仍一般不属于 \(h^2\)。若要高阶 weighted spectral coordinates，必须减去端点/渐近项并另作 uniform regularity 证明；本稿不作此宣称。

已独立通过：actual odd Volterra 相位与 fiber Jacobian，任意 alternating multilinear L² factorial bound，whole-series actual \(\ell^2\) analyticity，fixed-\(H\) 与 augmented ambient IFT，以及在明确 finite-graph 条件下的 physical subset IFT。

仍需原物理桥独立提供：同一低阶 analytic state graph、endpoint calibration、其 uniform 导数条件及原物理恢复。action-angle、Hamiltonian closure、最大各向同性和 intrinsic raw spectral inverse 均不由本稿推出。


## 10. normalized FULL monodromy：无 τ metadata 的实际状态 IFT

本节是归一化 FULL monodromy 的独有补充，保留 §§1–9 已审的 unnormalized/calibrated 逻辑。记 \(T_\lambda=M_A(\lambda)\)，以 actual determinant normalization 定义
\[
\mathcal N_\lambda
=\exp\!\left(-\frac{\lambda L}{M}-\frac{L\operatorname{tr}H}{M}\right)
T_\lambda.
\tag{28}
\]
因为 \(\det T_\lambda=\exp(\lambda L+L\operatorname{tr}H)\)，(28) 的 determinant 准确为 1。这里 \(M=m+1\)，不是用 slow 维数 \(m\) 作归一化。

### 10.1 实际 offdiag 样点的相位与 L 尺度

对于 \(\lambda_n=ik_n,\ k_n=2\pi n/L\)，定义
\[
\mathcal F_{\rm norm}(a,b,H)
=L^{-1/2}
\left(e^{ik_nL/M}
(\mathcal N_{ik_n})_{0s},
e^{ik_nL/M}
(\mathcal N_{ik_n})_{s0}\right)_{n\in\mathbb Z}.
\tag{29}
\]
相位是已知的 \(M\)-次单位根，准确抵消 normalized matrix 中的 fast scalar factor。故
\[
\boxed{\quad
\mathcal F_{\rm norm}
=\exp(-L\operatorname{tr}H/M)\,\mathcal F(a,b,H).
\quad}
\tag{30}
\]
§§3–5 的 kernel 和 Parseval 估计因此直接给 (29) 的 whole-series \(\ell^2\) 整解析性。指数 scalar factor 是 \(H\) 的 entire、非零函数，不破坏在任意有界源球上的一致解析估计。

在 \(a=b=H=0\)，raw offdiag 本身为零。因此 (30) 的 \(H\) 微分项为零，而对 \(a,b\) 的 derivative 仍准确为 (4) 经 \(L^{-1/2}\) 归一化后的 Fourier isometry \(\mathcal U\)。未归一化 Fourier 积分的 \(\ell^2\) 范数是 \(\sqrt L\) 倍 \(L^2\) 范数；(29) 保留这个 \(L^{-1/2}\)，不额外乘或除 \(L\)。

### 10.2 slow 底块恢复 trace 与完整 H 的线性逆

取实际有限矩阵数据
\[
C(a,b,H)=(\mathcal N_0)_{ss}.
\tag{31}
\]
在 vector vacuum \(a=b=0\)，
\[
C=e^{LK},\qquad
K=\mathsf P H:=H-\frac{\operatorname{tr}H}{M}I_m.
\tag{32}
\]
归一化并未消掉 \(H\) 的 trace：因为 \(m=M-1\)，
\[
\operatorname{tr}K=\operatorname{tr}H/M,\qquad
\boxed{\quad\mathsf P^{-1}K=K+\operatorname{tr}K\,I_m.\quad}
\tag{33}
\]
所以 \(\mathsf P\) 是整个 \(\mathbb C^{m\times m}\) 上的线性同构。

在真空 \(a=b=H=0\)，
\[
D C(\dot a,\dot b,\dot H)=L\mathsf P\dot H.
\tag{34}
\]
第一阶 \(a,b\) 插入仍只贡献非对角块。于是使用 \(C\) 本身作 finite 数据时，线性逆准确为
\[
\dot H=\frac{\dot C+\operatorname{tr}(\dot C)\,I_m}{L}.
\tag{35}
\]
若改用 \(L^{-1}\log C\) 的 local finite 坐标，其 derivative 则是
\(\mathsf P\dot H\)，逆为 (33)，不再含额外 \(L^{-1}\)。

### 10.3 normalized FULL dataset 的 ambient IFT

定义
\[
\mathscr D_{\rm norm}=(\mathcal F_{\rm norm},C):
L^2_a\times L^2_b\times\mathbb C^{m\times m}_H
\longrightarrow
\ell^2_{2m}\times\mathbb C^{m\times m}.
\tag{36}
\]
在真空，中心数据为 \((0,I_m)\)，derivative 为
\[
\boxed{\quad D\mathscr D_{\rm norm}(0)=
\mathcal U\oplus L\mathsf P.\quad}
\tag{37}
\]
由 (33)–(35) 这是 bounded Banach 同构。analytic IFT 因此给 (36) 在真空附近的实际局部解析 \(L^2/\ell^2\) 状态双逆。所有输入都来自 normalized FULL matrix：两组 offdiag 的全部整数样点以及零参数 slow 底块。此结论不另输入 \(\tau\)、\(\operatorname{tr}H\)、未归一化 determinant 或其他 scalar metadata。

在非零 vector-vacuum \(H=H_0,\ a=b=0\)，offdiag derivative 为
\(\exp(-L\operatorname{tr}H_0/M)\mathcal U_{H_0}\)，其中
\(\mathcal U_{H_0}\) 是 (2)–(3) 给出的 bounded Fourier-multiplication 同构。slow derivative 可写为
\[
D C_{H_0}\dot H
=e^{LK_0}\,
\varphi(L\operatorname{ad}H_0)\,
L\mathsf P\dot H,\qquad
\varphi(z)=\frac{1-e^{-z}}{z},\quad\varphi(0)=1.
\tag{38}
\]
因为 \(\operatorname{ad}K_0=\operatorname{ad}H_0\)，
\[
\sigma(\operatorname{ad}H_0)
\cap\frac{2\pi i}{L}(\mathbb Z\setminus\{0\})=\varnothing
\tag{39}
\]
就保证 (38) 可逆。该条件也覆盖非对角化的矩阵：entire functional calculus 的 \(\varphi\) 在整个 spectrum 上非零，故没有 Jordan-block 障碍。于是 (36) 在这些 \(H_0\) 附近也有局部解析逆；这是局部 exponential chart，不主张跨越 logarithm alias 的全局单射。

### 10.4 物理 finite graph 与 original frame 的范围

若 §7 的物理 analytic finite graph 已独立通过，且均值/\(H\) 的背景 derivative 为零，则 normalized \(n\ne0\) 子集的 derivative 只是
\(\exp(-L\operatorname{tr}H_*/M)\) 倍 §7 的 derivative。因此小背景的 Neumann/IFT 论证同样成立。若 \(D\mathfrak h\ne0\)，(30) 还产生
\[
-\frac L M\operatorname{tr}(D\mathfrak h)\,
\exp(-L\operatorname{tr}H_*/M)\,\mathcal F_*,
\]
必须与原 \(D_H\mathcal F\,D\mathfrak h\) 一并计算，不能省略。

(36) 的 ambient 结论消除了 \(\tau\) metadata，仍以已校准的 FULL matrix \(\mathcal N\) 为数据。§8 关于 \(E_0\) 的限制保留其当时给定 endpoint metadata 的方案。父任务另开的 original-frame endpoint 重构稿使用 **未经 endpoint 校准的 original FULL normalized matrix 的整 \(\lambda\) 数据** 提取 \(P(d(0))\)，并处理消去 \(G(0)\) metadata 的步骤；它需要 raw entire-\(\lambda\) 输入，不是仅有本节的离散样点或 traces。本节没有审核那一额外整参数步骤，后续无 endpoint metadata 的原框架结论须同时引用该证明。

新增通过：normalized phase、\(L^{-1/2}\) Fourier 尺度、\(C\) 的 \(L\mathsf P\) 有限维尺度、\(\mathsf P^{-1}\) 的 trace correction、非零 \(H_0\) 的 nonresonant dexp，以及无 \(\tau\) metadata 的 calibrated normalized FULL ambient 状态 IFT。仍不推出 weighted \(h^N\)、actions、Poisson canonical 性或最大性。


