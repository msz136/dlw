# KLTZ 谱图中实际 DLW 实结构：独立来源与中央消元核对

2026-10-11。只讨论已有条件性 M=2 近零谱图。读取本地 [AKNS 状态桥](akns_physical_state_inverse_bridge_20261011.md) §§4、4.3–4.5，以及 [reference metadata](../../Paper/refs/akns_transfer_20261011/reference_access_20261011.md)。metadata 明确本地没有成功保存的 KLTZ PDF；本次直接读 published PDF 与补充 primary source。未运行 checks，未改主证明、共享日志或索引。

**结论：选用 KLTZ 的标准 Abel/Dirichlet 归一化谱图，并取一次对称的共同近零域，可证明实际实结构在 full 及 reduced Cartesian 序列上具有同一精确线性公式。** 它是指标反射共轭，仍不同于标准 focusing/defocusing 实型。中央 action 的消元与背景零中央角的 gauge 截面保持这个公式。

## 1. 实际来源与归一化

* [Kappeler–Lohrmann–Topalov–Zung, published PDF](https://scispace.com/pdf/birkhoff-coordinates-for-the-focusing-nls-equation-3fe747h6fb.pdf)：§2.4 的 (2.18)–(2.19) 固定 Abel 角及归一化微分；§2.5 的 Theorem 2.1、Proposition 2.9、(2.21) 固定 Cartesian 图和 Fourier 微分；Theorem 1.1 给 focusing 实型；§4 的 Proposition 4.1 给 even 势的 y=0 截面。
* [Grébert–Kappeler, Symmetries of the nonlinear Schrödinger equation, BSMF 130 (2002), 603–618](https://www.numdam.org/item/10.24033/bsmf.2432.pdf)：Theorem 1.2、Proposition 3.3(ii) 给势共轭的实际 action/angle 对称性；§3.2 的 (3.4) 使用同一归一化 Abel–Dirichlet 构造。该文是 KLTZ bibliography [4]。

后一来源在 defocusing 势 ψ 上证明

\[
I_n(\bar\psi)=I_{-n}(\psi),\qquad
\theta_n(\bar\psi)=-\theta_{-n}(\psi)\pmod{2\pi}.
\tag{R1}
\]

这里只借这个确切对称性，不把实际 DLW 势当作 defocusing 势。下面通过全纯延拓使用它。

为核对两份来源的 Dirichlet 标定，可直接取常数 unitary

\[
C=\frac1{\sqrt2}\begin{pmatrix}1&i\\1&-i\end{pmatrix},
\quad \psi=-q+ip.
\]

它把 2002 文的 real AKNS 算子变为 KLTZ 的 ZS 算子：

\[
C^{-1}\!\left[i\begin{pmatrix}1&0\\0&-1\end{pmatrix}D
+\begin{pmatrix}0&\psi\\\bar\psi&0\end{pmatrix}\right]C
=\begin{pmatrix}0&-1\\1&0\end{pmatrix}D
+\begin{pmatrix}-q&p\\p&q\end{pmatrix}.
\tag{R2}
\]

AKNS 的第二分量零边界变为 F₁=F₂ 边界，直接矩阵乘法还给 M₁₂+M₂₁=Y₁−Z₂=−δ_GK。不能据此说两份文献的图逐项相同。实际 Abel 公式的匹配分三步：(i) T 保持 Δ、周期根与同一 Dirichlet 根；(ii) 两源的 canonical sheet 都由 iR>0 在 (λ₀⁺,λ₁⁻) 标定，归一化周期均为 2πδⱼₙ，故归一化唯一性给同一 Abel 微分 β；(iii) divisor 改到另一 sheet，而 sheet involution 固定 branch-point 基点 λⱼ⁻，把 β 反号，因此 θᴷ=−θᴳ mod 2π，路径调整只加整数周期。若 Cartesian 平方根记法另含统一 π 符号，KLTZ (2.21) 固定它；θ↦−θ+b、b∈{0,π} 都保持 (R1)，因为 2b=0 mod 2π。没有引入任何 action-dependent 角平移。这证明实际 KLTZ 谱归一化图的对称性，而不是援引另一份任意存在的 Birkhoff 图。故 (R1) 对这里采用的谱归一化 Cartesian 图给出

\[
\mathcal B P\varphi=R\mathcal B\varphi,
\quad P(\varphi_1,\varphi_2)=(\varphi_2,\varphi_1),
\quad R(x,y)_n=(x_{-n},-y_{-n}).
\tag{R3}
\]

先在 defocusing real-type 平面成立；闭隙处由 Cartesian 连续性补齐。该平面是 full complex L² pair 的 maximal totally real form，故全纯 identity theorem 把 (R3) 延拓到一份共同复近零域。不是仅由 Fourier 微分猜测 (R3)。

## 2. 实际 anti-involution 的线性公式

令

\[
C_d\varphi=(\bar\varphi_2,\bar\varphi_1),\qquad
C_f\varphi=(-\bar\varphi_2,-\bar\varphi_1).
\]

KLTZ 的 defocusing 和 focusing 实型定理及 analytic identity theorem 分别给

\[
\mathcal B C_d=\overline{\mathcal B},\qquad
\mathcal B C_f=-\overline{\mathcal B}
\tag{R4}
\]

（右边共轭作用于 x,y）。可以一次把源域缩到 P、C_d、C_f 不变的近零域；所有这些有限对称都是 Sobolev 等距变换，缩域不依赖高阶 N。这里仍要求实际非零常背景位于剩余近零域；没有新增数值半径结论。

实际 DLW 的 real a,b 经 φ₁=−iLa/2、φ₂=2iLb 后满足的固定点条件是

\[
\sigma\varphi=(-\bar\varphi_1,-\bar\varphi_2),
\qquad \sigma=P C_f.
\tag{R5}
\]

组合 (R3)–(R4)，

\[
\mathcal B\sigma\varphi
=(-\bar x_{-n},\bar y_{-n})_n.
\tag{R6}
\]

用本地桥稿的 wₙ=(xₙ+iyₙ)/√2、zₙ=(xₙ−iyₙ)/√2，得到

\[
\boxed{\quad
\Sigma(w,z)_n=(-\overline{w_{-n}},-\overline{z_{-n}}),
\qquad \mathcal B\sigma=\Sigma\mathcal B.
\quad}
\tag{R7}
\]

这是局部实际谱图上的精确线性 anti-involution，而非整幅全局势空间上的定理。它的固定点给 w₋ₙ=−bar wₙ、z₋ₙ=−bar zₙ，故 I₋ₙ=bar Iₙ；中央 w₀,z₀ 为纯虚，但 n≠0 的两个序列仍彼此独立。标准 focusing Cartesian 实型是 x,y 各自纯虚；标准 defocusing 实型是 x,y 各自实。它们均不能替代 (R7)。

KLTZ 的 (2.21) 还提供符号核对：D𝓑(0) 给 wₙ=−φ̂₂(n)、zₙ=−φ̂₁(−n)，与 (R7) 相容。这个线性化仅作符号核对；精确等变性依赖 (R1)–(R4)。

## 3. 中央 action 消元保持实结构

记全 action involution

\[
\mathfrak c(I)_n=\overline{I_{-n}}.
\]

对于 full potentials，实际 connection 共轭给

\[
\Delta_{\sigma\varphi}(z)
=\overline{\Delta_\varphi(-\bar z)}.
\tag{R8}
\]

背景根 z₊*=iLδ、z₋*=−iLδ 附近的小标定 disc 分别被 z↦−bar z 固定。因此简单根唯一性给

\[
z_\pm(\sigma\varphi)=-\overline{z_\pm(\varphi)},
\quad \chi(\sigma\varphi)=\overline{\chi(\varphi)}.
\tag{R9}
\]

结合本地 χ=χ̂(I)、∂I₀χ̂(I*)=4≠0，scalar IFT 的唯一分支满足

\[
\rho(\mathfrak c J)=\overline{\rho(J)},
\quad J=(I_n)_{n\ne0},
\quad \rho(0)=-L^2\delta^2.
\tag{R10}
\]

故 real reduced data 的 I₀ 保持实，且缩域后仍在负的非零背景值附近。谱中心恢复的 η 也满足 η(σφ)=bar η(φ)。

## 4. 中央角、root 分支与实际 gauge

实际常背景 φ*=(iLδ,iLδ) 是 KLTZ 的 even focusing 势。其非中央 Cartesian pair 已由本地桥稿的闭隙延拓证明为零；KLTZ even 截面给 y₀*=0，而 focusing 实型给 x₀* 纯虚。因此

\[
w_0^*=z_0^*\ne0,\qquad w_0^*/z_0^*=1.
\]

把 log(w₀/z₀) 取为 1 附近、log 1=0 的分支，定义 θ₀=(2i)⁻¹log(w₀/z₀)。从 (R7) 得

\[
\theta_0\circ\Sigma=-\overline{\theta_0}.
\tag{R11}
\]

因此背景中央角零截面 θ₀=0 不变。令 s(I₀) 为 s²=I₀ 且 s(I₀*)=w₀* 的唯一局部 root。因为 w₀* 纯虚，root 分支唯一性给

\[
s(\bar I_0)=-\overline{s(I_0)}.
\tag{R12}
\]

用 (R10) 补回 I₀，再设 w₀=z₀=s(I₀)，这个中央补全严格保持 Σ。其他 log 分支需先减去其背景常数，不能无条件沿用 (R11)；取上述零分支最直接。

本地 gauge 恒等式是

\[
g_\tau(a,b)=(e^\tau a,e^{-\tau}b),\qquad
G_\tau(w,z)=(e^{-\tau}w,e^\tau z),
\quad \theta_0\mapsto\theta_0+i\tau.
\tag{R13}
\]

它满足 ΣGτ=GbarτΣ。真实势给 θ₀ 纯虚；调到零中央角所需 τ=iθ₀ 为实。因此真实物理势到中央角截面的 gauge 保持 a,b 实。

反向也有实际唯一性证明。由 Σ-fixed reduced data 及 (R10)–(R12) 补全得到 Σ-fixed full data；KLTZ inverse 的 (R7) 给 σ-fixed φ，故其 a,b 实。χ=0 后，本地 full chart Ψ(u,v,τ,σ) 的表达式全部为 real coefficients，而且低 IFT inverse 唯一。因此对实的 (a,b)，Ψ inverse 给 u,v,τ 实及 σ=0。去除这个唯一实 gauge 后正是原 real physical 势；原 mean-zero physical inverse也保持共轭。

于是本地 reduced 状态图可以选到满足

\[
\boxed{\quad
\mathcal R(\bar u,\bar v)
=\Sigma_{\rm red}\mathcal R(u,v),
\quad \Sigma_{\rm red}(w,z)_n
=(-\bar w_{-n},-\bar z_{-n}),\ n\ne0.
\quad}
\tag{R14}
\]

一次取对称共同低域即可使全部 Hᴺ/hᴺ restrictions 保持这一身份。对称 finite-coordinate 截断 |n|≤N 与 Σred 交换；因此该实型的 rapid tangent sequences 有真实 finite-coordinate 逼近。这条结论仍不把原物理 Poisson tensor 替换为 NLS tensor。

## 5. 精确使用条件及未证部分

(R14) 的必要输入是：标准谱 Abel 角的反射归一化 (R1)–(R3)；已证明的 KLTZ 复解析状态逆；对称共同近零域与实际小背景；χ 的 action factorization 和简单中央 IFT 分支；背景零中央 log/root 分支；本地 Ψ 的唯一且保持共轭的物理 gauge inverse。当前来源及本地桥稿分别供应这些输入。

任意重新相位化 wₙ↦eᶠⁿ⁽ᴵ⁾wₙ、zₙ↦e⁻ᶠⁿ⁽ᴵ⁾zₙ 都保持 actions；仅有 canonicity 与 D𝓑(0) 不能排除这样的高阶相位。它保持 (R7) 的确切条件是

\[
f_n(\mathfrak c I)=\overline{f_{-n}(I)}
\]

（对选定的零附近 log 分支；指数形式只要求相差 2πi 整数）。因此若改用未经反射标定的 Birkhoff 图，应保留 transported nonlinear anti-involution，不能直接宣布 (R7)。本地此前仅声明 transported anti-involution 是正确的较弱陈述；本稿补上标准谱归一化下的线性识别。

这只是条件性 M=2 谱状态图的实结构澄清，不证明一般 M 的 norming 图、全部高阶实际流、regular fiber manifold 或 DLW Liouville 完备性。
