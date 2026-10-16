# 一般 M hybrid moving-norming 状态逆：谱分支独立审计

2026-10-11。完整实际读取并独立核验 [正式稿](general_m_augmented_actual_high_norming_state_inverse_recovery_20261011.md) §§1–7，包括本轮新增的 (14)–(15) 与完整矩阵指数微分段；最终版本变化后已实际重读 §6。受审版本 SHA256 为 DAA51914B2E4AB62EBA1619E0DE9750977C7BE533D903292970193AEBD0EFD15。只写本审稿；未修改正式稿，未运行机器检查。

结论：PASS。定理 (12) 是一般 M、任意固定满足 NR 的均匀背景、同一个 balanced real X₀ 邻域上的实际 augmented state 逆。必须保留 finite low coefficient metadata 与 full-frame calibration；它不是 class/action 逆或 Liouville 完备性。

## 1. 真实坐标数与 uniform derivative

原 Π=(P₀a,P₀b) 状态图的 DΠ₀ 是 real X₀→real (L²₀)^{2m} 的 bounded isomorphism。在 real Fourier representation 中，每个正 n 的 a-row、b-column 含 2m 个独立 complex 数，即 4m 个实数；负模由实 conjugation 决定。正式稿低频 target 的 complex dimension 2m(N−1)、每个高频的 complex dimension 2m 均与此匹配。

实际 Γ± 由 generator eigenvectors 定义，不含 Lρ 的 monodromy Born 因子。正 n 的 map (a_n,b_n)↦(Γ+ℓn,overline(Γ−ℓn)) 是 complex linear：负 Fourier mode 的 conjugation 被第二个整体 conjugation 消去。它的 high-n limit 是 (a_nsℓ,t_{M−ℓ}b_n)，slow eigenbasis、dual 及 channel permutation 均可逆。实际 T_n→T_∞、inverse bounds uniform 已在本支 high-gap 主稿和 child 独审证明。

正式 (10) 的 conjugated norming 是 real analytic map，不能将其当作删掉 independent negative modes 后的 complex-holomorphic IFT。正式稿准确采用 underlying real Hilbert spaces。exact Born selector 使 high-output 的 low-input derivative为零，因而 (11) 的 block-diagonal formula 没有遗漏 low/high 交叉项。

## 2. Gap center evaluation、basis derivative 和 scalar factor

准确背景 collision block 是 scalar ρI₂。actual Riesz intertwiner、source slow eigenbasis和其他 source frame 的一阶变化在压缩内只给与该 scalar 的 commutator，故为零。背景 spectral-parameter derivative 在 actual generator eigenbasis为 ρLdiag(y_f′,yℓ′)，所以 moving center 的 derivative 对 offdiag 不贡献。

固定 mean-normalized 物理叶另给 DH₀=D⟨a⟩₀=D⟨b⟩₀=0，全部 diagonal Born terms为零。精确背景 discriminant 的 simple difference F 在 root 处满足 F′=Lγ≠0，linear variation 2F(dot B11−dot B22) 除 F² 后在该点无 pole。因此 absolute center derivative为零，再由 Dhℓ(H)₀=0 得 Dcℓn₀=0。这里没有从 leading K_n+pℓ 猜测真实 root center。

未除 background χℓn=ρ_actual/e^{Lpℓ} 时，norming derivative是 χℓn LΓ±。正式 (5) 除准确 χ 后，(9) 为 LΓ±，factor正确。χ=1+O(1/n)、basis C=I+O(1/n)及其 inverse均有共同 bounds；这些操作保留 strong ℓ² real analyticity。

故 derivative (11) 的 infinite high block inverse为 uniformly bounded direct sum L⁻¹T_n⁻¹。与 finite low identity、Fourier representation 和 DΠ₀ 组成 bounded real Banach isomorphism。real analytic IFT给正式 (12) 的 actual local double inverse，所有 n≥N 使用同一 low source neighborhood。

## 3. Initial-value frame：常数 frame derivative不制造新 functional kernel

Q=G(0)、a^f=aQ⁻¹、b^f=Qb、H^f=QHQ⁻¹，真实 monodromy对应 diag(1,Q) 的相似变换。在背景 Q=I，其 source derivative的压缩 commutator仍因 scalar collision block消失。

DH^f₀=[dot Q,H₀]通常不为零；正式稿没有把它漏写成零。eigenvalue derivative却为零，且 P₀ 精确杀掉 a,b 变化中的常数 q₀dot Q、dot Qr₀。connection variation差 [dot D_Q,A₀] 是 spatialconstant，全部非零 Fourier coefficients为零；其 eigenbasis diagonal亦为零。因此 Γ±、Dc₀、P₀ coefficient derivative和整个 IFT保持不变。这支持正式 §6 的第二个实际 frame 版本。

## 4. 原 normalized full monodromy 恢复完整 H^f

原 χ endpoint T_d(0) 已由 actual positive-parameter projector limit恢复；G^f(0)=I，所以该 endpoint 的相似变换直接给 block frame。正式式 (14) 准确来自 actual normalization和新 FULL even+odd ℓ² kernel：

\[
e^{K_nL/M}\widehat N^f(K_n)
=\alpha\operatorname{diag}(1,e^{LH^f})+\mathcal E_n,
\quad\alpha=e^{-L\operatorname{tr}H^f/M},\quad \mathcal E\in\ell^2.
\]

因此 actual imaginary-sample limit的 top entry给 nonzero α，slow block/α给完整 matrix e^{LH^f}，不是只有其 eigenvalues。NR 排除 adH₀ spectrum中的非零 2πi/L 整数，使 Dexp_{LH₀} invertible；local finite-dimensional analytic IFT恢复唯一附近的完整 H^f。此为 arbitrary fixed NR 背景的 local exponential chart，不需要旧真空小势 ambient state IFT。

最终 §6 新增的完整微分也逐式通过：D(e^{LH})_{H₀}[K]=e^{LH₀}∫₀ᴸe^{-tH₀}Ke^{tH₀}dt。在 eigenmatrix Eᵢⱼ 上，积分因子为 (1−e^{-L(pᵢ−pⱼ)})/(pᵢ−pⱼ)，零差处为 L。NR 使所有非零差因子非零；左乘 e^{LH₀} 亦可逆。因此它恢复完整矩阵，包括全部 diagonal 与 offdiagonal directions，没有把 eigenvalue inverse 误当矩阵 inverse。

正式 (15) 再以准确 scalar factor恢复 actual untraced matrix，供 Riesz norming extraction。保留原 current B 参数与 centered labels是必要前提；正式最后一段明确没有添加 B_t=0 或 Γ_t=0。

## 5. Scope

low modes是实际向量势 Fourier coefficient supplements，不是 invariant谱数据。full H/eigenframe等若以metadata提供，必须是 recovered source 的函数；不能另作为自由 target坐标。general M 的 physical finite graph因 inverse重建原源而得到执行。

该定理不证明高 norming alone inverse、class/gap/actions inverse、canonical Poisson relations、weighted h^s inverse、all-hierarchy strong-domain membership或 nonlinear maximal isotropy。有限补充并未被隐去；受审稿的上述界限全部正确。
