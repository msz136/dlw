# M=2 实际 Floquet 对合：物理括号与归一化独立审计

2026-10-11。实际读取 `刘维尔可积性/research/spectral_independent_review_20261011.md` §12–13、`Workspaces/dlw_general_field_20261006/GENERAL_PERIOD_MATRIX_LAX.md`、`刘维尔可积性/research/scalar_poisson_quotient.md`、原物理 `periodic_reduction.md`，以及本次独有 tensor 脚本和 JSON。没有重跑旧检查或修改 spectral 主稿。

结论：§13 在 \(M=2,S=2\delta\ne0\) 的实际周期物理叶上成立。其核心是实际 normalized monodromy 的周期梯度及常数 tensor 恒等式，足以证明全有限谱参数迹、判别式及已定义移动 center/gap 对称组合对合。非零 \(\Gamma\) 的精确中心是原 scalar 谱参数减 \(B=\Gamma/(2c)\)，不是减 \(2B\)；错误系数曾只出现在代理消息中，已向作者和根说明，作者确认更正。以下保留所有规范因子。

## 1. 原物理张量的 \(1/16\) 常数

令 \(p_0=-p_1=u\)、\(s_0=-s_1=8v/h\)。\(M=2\) 的 \(R\) 为零，原约化张量在配对 \(h\sum_j\int\) 下是 \(-\operatorname{offdiag}D\)。一个泛函普通积分变分为

\[
\delta F=\int(F_u\delta p_0+F_vh\delta s_0/8)dx.
\]

原零和梯度分别为 \(F_u/(2h)\) 和 \(F_v/16\)，故

\[
u_t=-D F_v/16,
\qquad v_t=-D F_u/16.
\]

这独立给出

\[
J_{uv}=-\frac1{16}\begin{pmatrix}0&D\\D&0\end{pmatrix}.
\tag{A1}
\]

亦可从精确 free 变量 \(q_0=b_0-b_1-S=u-S,d_0=\delta+v\) 的原 \(J_0\) 得到。固定分量空间均值时，梯度应按常数法向取商；投影 \(P_x\) 与 \(D\) 交换且 \(DP_x=D\)，故 (A1) 的括号和真实速度没有遗漏均值修正。

## 2. 闭合、实际 original trace 和 \(\Gamma\) 中心

在 \(B=0\) 的自主截面，\(d_0=\delta+v,d_1=\delta-v,b_1=-d_0u/S,b_0=b_1+u\)，原 rank-one 系统是

\[
A^0_\lambda=\frac\lambda S
\begin{pmatrix}d_0&d_0\\d_1&d_1\end{pmatrix}
+\begin{pmatrix}b_0&d_0\\-d_1&b_1\end{pmatrix},
\qquad \operatorname{tr}A^0_\lambda=\lambda-2uv/S.
\]

去掉实际 scalar trace 后

\[
L_\lambda=A^0_\lambda-\tfrac12\operatorname{tr}A^0_\lambda I
=L^0_\lambda+uH/2+vK_\lambda,
\]

\[
L^0_\lambda=\tfrac S2(E-F)+\tfrac\lambda2(E+F),
\quad K_\lambda=\tfrac\lambda S H+(1+\lambda/S)E+(1-\lambda/S)F.
\tag{A2}
\]

这个梯度包含闭合 \(b_1(u,v)\) 及 trace 的全部变分，不是先在四个独立 \(b,d\) 分量中取梯度再忽略约束。令

\[
A(z)=-\frac2S\int_0^Luv\,dx.
\]

若 \(T^0_\chi\) 是原 rank-one monodromy，\(Y'=L_\lambda Y,Y(0)=I,N_\lambda=Y(L)\)，则没有 square-root 分支选择的精确公式是

\[
N_\lambda=e^{-(\lambda L+A)/2}T^0_\chi(\lambda,z),
\quad \det N_\lambda=1,
\quad \mathcal F_\lambda=\operatorname{tr}N_\lambda.
\tag{A3}
\]

原 full-\(M\) 公式取 \(\nu=B-S\)、\(P=d\mathbf1^T/S\)、

\[
C=\operatorname{diag}(b-d)-2\operatorname{diag}(d)H-(\nu/S)d\mathbf1^T.
\]

因此 \(M=2\) 时原 \(C\) 比上述 raw \(b,d\) 矩阵多 \(-BP\)。物理闭合为 \(b_j=B+b_j^0\)，故对原 scalar 谱参数 \(\lambda_{\rm orig}\)，

\[
A^B_\chi(\lambda_{\rm orig})
=B I+A^0_\chi(\lambda_{\rm orig}-B).
\tag{A4}
\]

设 \(\Lambda=\lambda_{\rm orig}-B\)，则

\[
T^B_\chi(\lambda_{\rm orig})=e^{BL}T^0_\chi(\Lambda),
\quad \operatorname{tr}A^B_\chi=\lambda_{\rm orig}+B-2uv/S,
\]

\[
e^{-[(\lambda_{\rm orig}+B)L+A]/2}\operatorname{tr}T^B_\chi
=\mathcal F_\Lambda.
\tag{A5}
\]

背景 scalar symbol \(B+y+\delta^2/y\) 也独立核对 \(\Lambda=\lambda_{\rm orig}-B\)。本静态审计将 \(c\) 视为 Casimir 叶标签、\(B\) 视为任意既定规范截面；它没有给原方程添加 \(\Gamma_t=0\)。任意 \(\Gamma(t)\) 必须使用根任务已证的移动平移与中心化公式。若人为把 \(B\) 当作 \(z\) 的函数，(A5) 另有 \(\partial_\Lambda\mathcal F\,\delta B\) 链式项，不能套本固定规范梯度。

## 3. 实际周期 adjoint 梯度

原 \(L_\lambda\) 周期。由 \(Y(x+L)=Y(x)N\)，

\[
W_\lambda(x)=Y_\lambda(x)N_\lambda Y_\lambda(x)^{-1}
\]

满足 \(W(x+L)=W(x)\)、\(W'=[L,W]\)。实际 ODE 的 Duhamel 变分及 cyclic trace 给

\[
\delta\mathcal F_\lambda
=\int\operatorname{tr}(W_\lambda\delta L_\lambda)dx,
\quad (\mathcal F_{\lambda,u},\mathcal F_{\lambda,v})
=(\operatorname{tr}W_\lambda H/2,\operatorname{tr}W_\lambda K_\lambda).
\tag{A6}
\]

周期性不依赖零均值、均匀背景、倍子互异或无端点别名。实际 \(H^1\) 场使 \(L\in H^1\)，ODE 给 \(W\in H^1\)，再由代数估计 \(W'=[L,W]\in H^1\) 得 \(W\in H^2\)。故 (A6) 的梯度可容许，\(J\nabla\mathcal F\in H^1\)，周期分部积分完全合法。更高 \(H^s,s\ge1\) 类似。所有这些都是实际有限 \(\lambda\) 的梯度，不从形式渐近 series 推断。

## 4. Tensor 恒等式与准确 total derivative

取 \(\lambda\ne\mu\)，令

\[
B_{\lambda\mu}=H/2\otimes K_\mu+K_\lambda\otimes H/2.
\]

§13 的 \(R_{\lambda\mu}\) 在 \(H,E,F\otimes H,E,F\) 基中各系数为

\[
\begin{pmatrix}
\frac{2S^2-\lambda^2-\mu^2}{4S(\lambda-\mu)}&\frac{S+\mu}{4S}&\frac{S-\mu}{4S}\\
-\frac{S+\lambda}{4S}&0&\frac{(S+\lambda)(S-\mu)}{S(\lambda-\mu)}\\
\frac{\lambda-S}{4S}&\frac{(S-\lambda)(S+\mu)}{S(\lambda-\mu)}&0
\end{pmatrix}.
\]

用 \([H,E]=2E,[H,F]=-2F,[E,F]=H\) 比较 \(1,u,v\) 三组系数，得

\[
[R,L_\lambda\otimes I+I\otimes L_\mu]
=\tfrac12[B,I\otimes L_\mu-L_\lambda\otimes I].
\tag{A7}
\]

例如 \(u\) 系数直接确定 \(r_{HE}=(S+\mu)/(4S),r_{HF}=(S-\mu)/(4S),r_{EH}=-(S+\lambda)/(4S),r_{FH}=(\lambda-S)/(4S)\)；常数项的 \(H\otimes E\) 系数是

\[
e_\mu(2r_{HH}-b_{HH})-e_\lambda r_{FE}=0,
\quad e_\lambda=(S+\lambda)/2,\ b_{HH}=(\lambda+\mu)/(2S),
\]

代入即给所列 \(r_{FE}\)。其余系数由相同三条 Lie 关系核对；这也与原 48 scalar 方程证书相符。

设 \(W_{12}=W_\lambda\otimes W_\mu\)，并记

\[
I_1=\operatorname{tr}_{12}(W_{12}[B,I\otimes L_\mu]),
\quad I_2=\operatorname{tr}_{12}(W_{12}[B,L_\lambda\otimes I]).
\]

则原括号 integrand \(\mathcal F_{\lambda,u}D\mathcal F_{\mu,v}+\mathcal F_{\lambda,v}D\mathcal F_{\mu,u}=I_1\)，而

\[
D\operatorname{tr}_{12}(RW_{12})=\tfrac12(I_1-I_2),
\qquad D\operatorname{tr}_{12}(BW_{12})=I_1+I_2.
\]

因此甚至有准确逐点式

\[
I_1=D\operatorname{tr}_{12}[(R+B/2)W_{12}],
\]

也可只用周期分部积分 \(\int I_2=-\int I_1\) 得 §13 的积分式。二者都给

\[
\{\mathcal F_\lambda,\mathcal F_\mu\}
=-\frac1{16}\int I_1dx=0.
\tag{A8}
\]

不把 \(I_1=D\operatorname{tr}(RW_{12})\) 误当逐点式。实际泛函与梯度 entire 于谱参数，故 \(\lambda=\mu\) 由连续性取极限，证明 tensor 的 pole 不产生实际泛函 pole。实场的 \(\mathcal F_{\bar\lambda}=\overline{\mathcal F_\lambda}\) 给各实部、虚部相互对合。

## 5. 判别式、轮廓 center/gap 与 holonomy 的链式法则

实际 \(\mathscr D=\mathcal F^2-4\)，故两谱参数判别式对合。在 §12 的共同实际源球上，各固定轮廓的分母非零并有正下界，统一 log 分支可微分。源变分与紧轮廓积分交换；所得梯度是 (A6) 梯度的轮廓积分乘以 scalar 权重，仍属于 \(H^{s+1}\)。先取两个轮廓的双积分，再用 (A8)，得到全部 \(a_n,g_n\) 及其实、虚部对合。这里使用对称轮廓坐标，不对可能不光滑的有序根求导。

又 \(P_{\rm mom}=16\int uv\)，所以 \(A=-P_{\rm mom}/(8S)\)，直接由 (A1) 得

\[
X_A=(u_x,v_x)/(8S).
\]

原 monodromy 在基点平移下共轭，trace 不变，因此 \(\{\mathcal F_\lambda,A\}=0\)。这说明归一化中的 \(A\) 虽依赖场，却不破坏括号：原 \(\operatorname{tr}T^0_\chi=e^{(\lambda L+A)/2}\mathcal F_\lambda\)、\(\det T^0_\chi=e^{\lambda L+A}\) 彼此对合。移动 holonomy 重整化 \(a_n-A/L\) 与 \(g_n\) 全部对合；(A5) 同样处理任意静态 \(B\) 截面。没有把 \(A\) 误记为 Casimir。

## 6. 证据状态及保留缺口

本次读取脚本 `spectral_m2_actual_poisson_tensor_checks_20261011.py` 的 SHA256 为 `966318BF7023887FF857EFAB6DB1B9498DCD1EBF1F28B4AA9F9CB6DD5962B7F8`，与 JSON 一致。证书记录 48 方程、9 tensor 未知量及 exact identity、actual connection、trace、spectral flip 四项 true。本独审没有重跑该脚本，也没有改脚本或 JSON。

已证范围不限均匀平均叶；只要为上述实际 \(M=2,c\ne0\) 周期物理状态，固定谱参数迹的对合计算都成立。移动双根坐标仍保留 §12 的小源球和无轮廓零点条件。它尚未证明一般 \(M>2\)、norming/divisor 完整逆、非线性谱梯度闭包最大各向同性或正规 Liouville 积分叶。实际 \(\{\mathcal F_\lambda,C_n\}=0\) 与 strong 无限域输送另需实际 Lax 或梯度证明，不能仅从形式 local-charge 互相对合跳出。

## 7. 后续 §14–15 的独立复核

§14 已由真实 periodic Riccati 与 Sobolev \(C^1\) 余项补上上一段当时所列的 local-charge 对合缺口；详核及 strong 相域实际输送见独有 `spectral_m2_strong_domain_flow_bridge.md` §1–5。本节另外逐式核对 §15 的实际二阶 gap、center 与同点可数独立性，结论成立，以下说明常数与范围。

令 \(k=k_n,\omega=\omega_n,\gamma=\omega/k,\lambda_n=i\omega\)，背景 normalized monodromy 为 \(N_0=\sigma_n I,\sigma_n=(-1)^n\)。其真实一阶 off-diagonal 元素为 \(c_+,\overline{c_-}\)，无一阶 diagonal 项。由 \(\det N=1\)，二阶 trace 修正为 \(c_+\overline{c_-}\)，实际判别式二阶系数于是为

\[
D_2(\lambda_n)=4c_+\overline{c_-}.
\]

canonical 归一化 (26) 中 \(Q=k^{-1/2}c_+/\sqrt{|K|}\)、\(P=\operatorname{sgn}(S)k^{1/2}\overline{c_-}/\sqrt{|K|}\)，故两半阶因子恰消去，并有

\[
c_+\overline{c_-}=KQP,
\quad K=\frac{Lk\omega}{16S}.
\]

背景判别式在 \(\lambda_n+\zeta\) 的首项为 \(L^2\gamma^2\zeta^2\)。轮廓式 (67) 因而给半 gap 平方的实际二阶项

\[
g_n^{[2]}=-\frac{D_2(\lambda_n)}{L^2\gamma^2}
=-\frac{k^2}{4SL\gamma}Q_nP_n.
\tag{A9}
\]

这核对 (97) 的 \(4\)、\(S\) 符号及半 gap 规范；它不是完整 gap 平方。实型的 \(\overline{c_-}\) 已在 \(P\) 中，不能再额外共轭 \(QP\)。

令 \(\Upsilon(\lambda)=\sqrt{\lambda^2-4\delta^2}\) 为局部支（用 \(\Upsilon\) 避免与物理通量 \(\Gamma\) 混淆）。则

\[
\Upsilon'(\lambda_n)=\gamma,
\qquad \Upsilon''(\lambda_n)=-4i\delta^2/k^3.
\]

背景判别式的 cubic 系数为 \(L^2\gamma\Upsilon''\)。取 \(D_2/D_0\) 的 \(\zeta^{-1}\) coefficient，准确得到 (99)

\[
a_n^{[2]}=-\frac12\left[
\frac{D_2'(\lambda_n)}{L^2\gamma^2}
-\frac{D_2(\lambda_n)\Upsilon''(\lambda_n)}{L^2\gamma^3}\right].
\tag{A10}
\]

原 normalized connection 仿射于源，故 double Born 项就是实际二阶项，不遗漏闭合的二阶 coefficient。这里需保留 \(D_2'\) 的所有 off-resonant 耦合；只用共振 coupling product 推 center shift 会不完整。§12 的 \(c_0\) 解析映射使每个源 Taylor coefficient 落在 \(c_0\)，严格给 (100) 的 \(a_n^{[2]}-A^{[2]}/L\in c_0\)，没有隐含加权 \(\ell^2\) 衰减。

对任意有限 positive frequency 集合，用真实 Fourier 逆选择同一个 \(\eta\) 使各 \(Q_n=P_n=1\)，再以 \(\delta P_n=1,i\) 作两个真实方向测试。(A9) 的 Hessian-gradient minor 正是 \(\operatorname{diag}(b_n,b_n)\)，\(b_n=-k_n^2/(4SL\gamma_n)\ne0\)。因而 (101) 的 \(\varepsilon^{2|E|}\prod b_n^2\) 和 selected gaps 非零成立。这里 \(\eta\) 是一个共同 witness，而不只是各 quadratic forms 分别独立。

§15.4 使用 mixed §17 的一份固定 holomorphic \(F:B_R(H_{\mathbb C})\to\mathfrak S_\infty\)，在原点连续性下缩到同一更小 H 球，使整个像留在 §12 的统一实际源球。\(DF(0)\) 覆盖全部有限 Fourier，\(Dg_n(0)=0\) 排除复合 Hessian 的 \(D^2F\) 项，因此 (102) 是真正内部 strong plots 上的 nonzero real-analytic minor。所有 gap functions 在同一个 H 球解析，Baire 得同一个实际 strong 状态上全部 finite prefixes 独立且所有 \(g_n\ne0\)。还可与 local-charge minors 的 residual 集相交，使两族**各自**全部有限块独立，未宣称合并族独立。

这项独立性保持 §12–15 的 \(M=2,0<|\delta|<k_0/2\)、指定均匀平均叶与实际小源球范围；泛型只在固定 H 参数球。它不证明整个 strong 相域或所有平均叶泛型、regular integral fibers、norming/divisor 或 nonlinear maximality。
