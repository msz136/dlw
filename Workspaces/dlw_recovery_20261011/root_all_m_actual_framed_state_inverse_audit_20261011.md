# 一般 M：真实 full framed 单值矩阵状态逆的根复核

2026-10-11。完整读取两份独立 Fourier-kernel 证明、原框架恢复稿及其独立审计后，以下关键连接通过。没有运行符号检查，也没有从 framed 状态资料推出共轭不变量完备性。

依赖：

- [独立 vector AKNS L² 证明](vector_akns_framed_l2_state_inverse_recovery_proof_20261011.md) §§1–7；
- [实际 Fourier 核与 normalized IFT](general_m_framed_monodromy_fourier_kernel_20261011.md) §§1–6、10；
- [原 full 单值矩阵恢复独审](general_m_raw_monodromy_state_extraction_independent_20261011.md) §§1–8；
- [实际 endpoint 与 slow holonomy](all_m_actual_framed_endpoint_recovery_20261011.md)、[独审](all_m_full_framed_endpoint_holonomy_independent_audit_20261011.md)；
- [原物理 periodic coefficient 状态图](all_m_physical_holonomy_state_inverse_20261011.md) §§1–9，及[根复核](root_general_m_periodic_state_inverse_audit_20261011.md)。

## 1. 校准框架中的真正 Banach 双逆

固定有限 m=M−1≥1、L>0，令
\[
A_\lambda=\begin{pmatrix}\lambda&a(x)\\b(x)&H\end{pmatrix},
\quad a\in L^2(\mathbb C^{1\times m}),\quad b\in L^2(\mathbb C^{m\times1}),
\quad H\in\operatorname{Mat}_m(\mathbb C),
\]
其中 H 为常矩阵。Y′=AλY、Y(0)=I 的实际 Volterra 解定义 Tλ=Y(L)，并取
\[
N_\lambda=e^{-\lambda L/M-L\operatorname{tr}H/M}T_\lambda.
\]
全部对象在 L¹ 系数下有意义，不要求 a、b 的端点值。以 λn=2πin/L 定义实际资料
\[
\mathcal D(a,b,H)=\left(
\left[L^{-1/2}e^{2\pi in/M}(N_{\lambda_n})_{0s}\right]_n,
\left[L^{-1/2}e^{2\pi in/M}(N_{\lambda_n})_{s0}\right]_n,
(N_0)_{ss}-I_m\right).
\tag{1}
\]
则 D 是从 L²×L²×Matₘ 到 ℓ²×ℓ²×Matₘ 的整解析映射，在零势附近有真实局部双解析逆。

### 独核 L² 预算

每个 offdiagonal Dyson 项有 2r+1 次 alternating 插入。将其 ordered 时刻换成 fast/slow 区间长度，固定总 fast duration τ 的 Lebesgue 条件体积为
\[
v_r(\tau)=\frac{\tau^r(L-\tau)^r}{(r!)^2}.
\]
这已经包含 coarea 中的 1/√(2r+1)，不能再乘 Euclidean 面积因子。对任意各自独立的 alternating L² 输入 fj，保留 slow 矩阵指数的原乘法顺序，fiber Cauchy–Schwarz 再积分给
\[
\|K_r\|_2\le e^{L\|H\|}\frac{(L/2)^r}{r!}\prod_j\|f_j\|_2.
\tag{2}
\]
证明只用 ∫ordered∏|fj(tj)|²≤∏‖fj‖²，不用同一位置的 L²×L² 乘法。该多线性界给所有 bounded source 球上一致的 L² kernel 收敛及联合解析性。每个 λ 上的真实 Dyson 收敛与 L² kernel 的积分可逐项交换，因而其 Fourier 系数确实是实际 Tλn 的矩阵元。Parseval 给未缩放样点范数 √L‖K‖₂；式 (1) 的 L⁻¹ᐟ² 恰好恢复 Fourier isometry。

归一化乘子带有 H 的 scalar e⁻ᴸᵗʳᴴ⁄ᴹ，但在零势两组 offdiagonal 值为零，故其 H 微分没有额外首项。有限矩阵首项为
\[
D\mathcal D(0)(\alpha,\beta,K)
=\left(\mathcal U_+\alpha,\mathcal U_-\beta,
L\left[K-\frac{\operatorname{tr}K}{M}I_m\right]\right).
\tag{3}
\]
因为 m=M−1，K↦K−trK I/M 的逆是 C↦C+trC I。因此有限逆为 (C+trC I)/L；并未遗失 scalar holonomy。两组 U 是相反 Fourier convention 的 isometry。式 (3) 是真正 bounded Banach 同构，analytic IFT 适用，无额外 τ 或 determinant metadata。

## 2. 从原 full 框架恢复校准

对 bounded a、b、H 及大正实 λ，周期 Riccati 方程
\[
\eta=(D+\lambda)^{-1}\{b+H\eta-\eta(a\eta)\}
\]
在 L∞ 的 O(λ⁻¹ᐟ²) 球上收缩。周期 convolution 给 L²→L∞ 的 O(λ⁻¹ᐟ²)、L²→L² 的 λ⁻¹ 和 L∞→L∞ 的 λ⁻¹ 界，故
\[
\|\eta\|_\infty=O(\lambda^{-1/2}),\quad
\|\eta\|_2=O(\lambda^{-1}),\quad
\|a\eta\|_1=O(\lambda^{-1}),\quad \eta\in H^1.
\]
实际周期三角化给 slow monodromy E=eᴸᴴ+O(λ⁻¹)、fast multiplier μ=e^{λL+O(λ⁻¹)}。upper row divided by μ 是
\[
\int_0^L e^{-\lambda t-\int_0^t a\eta}a(t)Y_s(t)dt
=O(\lambda^{-1/2}),
\]
最后一步用 Cauchy–Schwarz，而非 a(0)。三角 gauge 的 endpoint 也趋 I，故准确得到
\[
\frac{N_A(\lambda)}{\operatorname{tr}N_A(\lambda)}\longrightarrow E_{00}.
\tag{4}
\]
原物理 periodic graph 改用 based Gf=G G(0)⁻¹，保证 Gf(0)=Gf(L)=I。原 χ-frame 于是只剩
\[
N_\chi=T_d(0)N_A T_d(0)^{-1},\qquad
T_d=[d/S,Z],\quad (T_d^{-1})_{0\cdot}=\mathbf1^T.
\]
在物理低域 d∈H¹，其端点已定义。由 (4)
\[
\boxed{\lim_{\lambda\to+\infty}
N_\chi/\operatorname{tr}N_\chi=d(0)\mathbf1^T/S.}
\tag{5}
\]
每列准确恢复 d(0)/S，从而恢复 Td(0)。其可逆性不依赖任何单个 dj 非零。一个常数 conjugation Td(0)⁻¹NχTd(0) 就给式 (1) 的 based monodromy，没有额外未知 G(0)。实际 determinant normalization 的 scalar 在 (4)–(5) 消去；其余 Fourier 采样仍按式 (1) 保留 phase。

另一个可选真实资料是 fast spectral projector 去项后的 slow block 极限：
\[
e^{\lambda L/M}[(I-P_A)N_A]_{ss}
\longrightarrow e^{L(H-\operatorname{tr}H I/M)}.
\]
这里 finite λ 的 slow block 精确为 (I−η(0)cλ)E，不可直接写 E。无 ad-Fourier-alias 的背景允许局部 matrix logarithm 恢复完整 H；式 (1) 的 near-zero IFT 本身不需要该极限或 logarithm。

## 3. 原一般函数场的局部唯一恢复

固定任意有限 M、非零充分小 δ=S/M、给定组件均值，使用已独审的物理低域
\[
(q-q_*,d_{\rm first}-\delta\mathbf1)
\in (L^2_0)^m\times(H^1_0)^m.
\]
其 based coefficients a、b、H 在均匀背景为 O(δ)，因而充分小非零 δ 落入第 1 节的 ambient inverse 球。该额外半径确实存在，但不能仅由旧 mixed 小背景数值阈值宣布满足。该图允许一般周期函数；没有 Fourier 截断或有限维 ansatz。

原 normalized full Nχ 函数先经式 (5) 定 frame，再算式 (1) 的全整数样点与有限 slow block。实际 ambient inverse 恢复 a、b、H；物理图的 projected (P₀a,P₀b) inverse 恢复 q、d。对于 based graph，有限均值/H 的背景微分并非全零，因此这里使用 augmented ambient IFT；没有偷用仅 n≠0 的 mean-normalized subset IFT。

B=Γ/(2c) 可随初态和原时间改变。取固定参考 B₀、谱参数 λorig=λ+B₀，扣除公共 scalar B₀ 后，slow matrix 是
\[
H_{\rm tot}=H_c+(B-B_0)I_m.
\]
q、r 和 based G 不变。由恢复的 q、d 算得 centered Hc，随后
\[
B-B_0=\frac{\operatorname{tr}(H_{\rm tot}-H_c)}m.
\]
因此真实 normalized full 资料不丢 B；无需给 τ metadata，也没有加入 B′=0。c 和组件均值在这里是可变邻近叶的参数标签，各叶图需自己的非零 S；没有统一延伸到 S=0。

结论：上述邻域中的原完整 framed monodromy 函数局部唯一决定原物理态，包括共同 B。校准后的式 (1) 在 ambient vector-potential 空间具有明确 L²/ℓ² 双解析逆。原 raw entire-function 空间尚未指定 natural Banach 范数及自由 onto 域，故不能把这两个不同层次合并为 raw 任意数据双逆。

## 4. 未作的升级

framed 数据含 eigendirection/norming 信息；迹与 characteristic coefficients 去掉框架，不能由本定理恢复所有物理态。一般 M 的 invariant action 坐标、原 Poisson 的 Hamilton 闭包和最大性仍待证明。

raw weighted hᴺ 也未建立。即使 m=1、b=0、a常数、H=h≠0，upper 样点准确为 a(e^{hL}−1)/(h−λn)，具有非零 1/n 尾，不能放进 h¹。smooth input 不自动提供 raw hᴺ；需 actual endpoint/asymptotic renormalization 后另证同阶逆。

本稿所认证的是一个新的全 M 真实非线性谱状态连接。共同 invariant fiber 的 regular 几何、同一 S∞ 中 trace Hamilton 稠密生成、零平均深层和最终一般物理场 Liouville 结论均保持开放。
