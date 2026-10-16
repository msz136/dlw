# 一般 M finite high-gap 独立性与 calibrated norming state IFT：第二独审

2026-10-11。完整读 [实际高频 Riesz/gap 引理](general_m_actual_high_frequency_riesz_gap_lemma_20261011.md)，重点独核 §8；§1–7 的主结论作为此前独审通过的输入。本次不重跑 checks、不修改主稿或共享 logs。另读实际 [physical coefficient/state 图](all_m_physical_holonomy_state_inverse_20261011.md) 的 Fourier derivative、mean/Floquet frame 与 [原 χ endpoint calibration](all_m_actual_framed_endpoint_recovery_20261011.md)。

当前审结：**§8 PASS**。下文给可选 real Banach norming state IFT 的严格证明，并区分该状态结论与 action/divisor 或 class-only 逆。

## 1. Real reflection 与准确 complex-linear coupling 方阵

Background H_0 为实矩阵，p_ℓ=−iδcot(πℓ/M)，故
\[
\overline{p_\ell}=p_{M-\ell}.
\]
Dispersion 的 rational coefficients 为实。Fast/slow 实际分支和 collision 标签由唯一解析延续给
\[
\overline{\lambda_{\ell n}}=\lambda_{M-\ell,-n},\qquad
\overline{\gamma_{\ell n}}=\gamma_{M-\ell,-n}.
\tag{S1}
\]
Right/left eigenbasis可以配成相同 conjugation。对于实物理源 dot A，\widehat{dot A}_{−n}=overline{\widehat{dot A}_n}，所以
\[
\Gamma^\pm_{M-\ell,-n}
=\overline{\Gamma^\pm_{\ell n}},\qquad
g_{M-\ell,-n}=\overline{g_{\ell n}}.
\tag{S2}
\]
这没有强制全部正 n 的 g 为实数。

固定正 n，记
\[
\widehat{\dot A}_n=\begin{pmatrix}0&A_n\\B_n&0\end{pmatrix}.
\]
在实 Fourier pairing 上，\Gamma^-_{ℓn} 使用 −n 模，故整体 conjugate 后
\[
\overline{\Gamma^-_{\ell n}}
=\overline{\ell_\ell}\,widehat{\dot A}_n\,overline{e_f}.
\]
它和 \Gamma^+ 均为 (A_n,B_n) 的 complex-linear functions。准确方阵
\[
T_n(A_n,B_n)
=(\Gamma^+_{\ell n},\overline{\Gamma^-_{\ell n}})_{\ell=1}^m
\tag{S3}
\]
由真实 generator 的 fast/slow asymptotics给
\[
T_n(A_n,B_n)
=(A_ns_\ell,t_{M-\ell}B_n)_\ell
+O(n^{-1})(|A_n|+|B_n|).
\tag{S4}
\]
有限 slow eigenbasis和其 inverse 加 permutation构成可逆极限。故存在 N，使全部 n≥N 的 T_n 与 T_n^{-1} 同时有界。背景 split T_0 是固定的，使用 χ orthonormal basis再作固定相似变换不会引入 n-dependent condition-number 损失。

## 2. 真正 real finite Fourier witness 与 nonlinear minor

实际 state 图的 D\Pi_0 是在实 X_0 与实 mean-zero L² row/column 数据间的 Fourier multiplier 同构。它的逐模 inverse 既保持有限 Fourier support，也保持 real conjugation。

对任意 finite F⊂{n≥N}，先在 coupling space选一个实源 witness f，使每个选中 (ℓ,n) 的
\[
\alpha_{\ell n}=\Gamma^+_{\ell n}=1,\qquad
\beta_{\ell n}=\overline{\Gamma^-_{\ell n}}=1.
\]
经每个 T_n^{-1} 得正频率 (A_n,B_n)，补上负 Fourier conjugates，再经 D\Pi_0^{-1} 得真正 real finite Fourier f。对每个选中通道，按同样步骤取两个 real test directions，使 δα=0，δβ 分别为 1 与 i，其余 coupling coordinates为零。这给恰好 d=2m|F| 个 tests。

输入已审准确 quadratic gap
\[
g^{[2]}_{\ell n}(f)
=-4\gamma_{\ell n}^{-2}
\alpha_{\ell n}\overline{\beta_{\ell n}},
\]
在上述 witness 上
\[
Dg^{[2]}_{\ell n}(f)h
=-4\gamma_{\ell n}^{-2}\overline{\delta\beta_{\ell n}}.
\tag{S5}
\]
乘非零 complex scalar后取 conjugation是 complex 一维上的 real-linear 同构。Fourier support和 (S3) 的全-channel inverse保证所选 tests无其他通道的 leading cross-block。Strong analytic cubic remainder可在有限 tests上求导，所以
\[
Dg(\varepsilon f)h
=\varepsilon Dg^{[2]}(f)h+O(\varepsilon^2).
\]
因此 (Re g,Im g) 的 d×d 实 Jacobian minor 为
\[
\varepsilon^d C_F+O(\varepsilon^{d+1}),\qquad C_F\ne0.
\tag{S6}
\]
指数正是 2m|F|。每个 finite block有任意靠近 uniform 的实际 nonlinear independence witnesses；uniform本身的零梯度未被误报成独立。

## 3. Residual locus 与 strong 域的条件传递

固定 F 和上述 fixed tests后，minor是 connected X_0 源球上的 real analytic scalar function。由 (S6) 它不恒为零，故其非零 locus为 open dense。有限 positive frequency subsets是可数族；open Banach 源球是 Baire space，所以交集是 residual，并在每个 finite block上同时独立。

主稿 §8.3 的附加假设也充分且必要地被保留：real analytic F:O_H→X_0、F(0)=0、common parameter ball，且 DF(0) 的 range含所有所用 real finite Fourier directions。因 Dg(0)=0，
\[
D^2(g\circ F)(0)[u,v]
=D^2g(0)[DF(0)u,DF(0)v].
\]
取 finite witness/tests 的参数原像即得同一非零 leading minor和参数球中的 residual结论。不可以只凭 X_0 residual 或 ambient smooth density将其移到薄 strong 图。当前结论没有宣称 common Hamiltonian closure、与所有 C_n 合并独立或 Liouville 最大性。

## 4. 可选 actual calibrated norming state IFT 的线性预算

在主稿 §7 的实际 rank-two compression上作 source-independent、uniformly bounded的背景 basis calibration，使每个准确 collision λ_{ℓn} 的 basis等于 §6 的 generator basis。背景 block此时为 scalar ρ_{ℓn}I_2，故 norming offdiagonal在 source 0 为零。

保持原 compression的 template scalar normalization时，norming derivative是
\chi_{ℓn}L\Gamma^\pm，而非直接 L\Gamma^\pm，
\[
\chi_{\ell n}=\rho_{\ell n}/\rho_\ell(H_0)=1+O(n^{-1}).
\]
再逐通道除以这个已知背景常数即可得校准后的 \nu^\pm_{ℓn}，其 exact derivative为 L\Gamma^\pm。High χ及χ^{-1} uniformly bounded，因此不损失 ℓ² analyticity。

在 mean-normalized G frame，D⟨a⟩=D⟨b⟩=DH=0，故 background Born diagonal entries均为零。Actual cluster center的 linear variation因而为零；moving grid的 Dh_ℓ也为零，所以
\[
Dc_{\ell n}(0)=0,\qquad Dh_\ell(0)=0.
\tag{S7}
\]
在 B(c(z),z)求导时，源的 center shift不贡献。Compression/intertwiner及 moving frame的 source derivative在 scalar collision block中只给 commutator，因此也不贡献 offdiagonal导数。

定义 real analytic state map：低频 1≤n<N取 (P_0a,P_0b) 的正 Fourier coefficients；高频 n≥N取
\[
(\nu^+_{\ell n},\overline{\nu^-_{\ell n}})_{\ell=1}^m.
\tag{S8}
\]
Target是正频率 ℓ²(C^{2m}) 的 underlying real Banach space。它的 derivative准确为
\[
\operatorname{diag}\big(I_{1\le n<N},L T_n{}_{n\ge N}\big)
\circ D\Pi_0,
\tag{S9}
\]
其中 Fourier identification的固定 Parseval norm factor仅改变等价 norm。由 (S3)–(S4)，(S9) 是 real Banach 同构。前向 map的 high ℓ² analyticity已由实际 function-valued Riesz compression及 center evaluation证明；低频只有有限个 continuous Fourier functionals。因此 real analytic Banach IFT给真正的局部 state inverse。

该逆作用于 fixed component-mean physical state domain；finite physical image compatibility由该前向 map的 source定义和 IFT保证。它仍是 framed norming state chart，没有提供 canonical Poisson relations、divisor或 action-angle coordinates，也不能用于 class-only数据逆。

## 5. Source-dependent frame 与原 χ 数据的校准细节

Mean-normalized coefficient frame中的 E_0=T(d(0))diag(1,G(0)) 是 source-dependent。原 χ full normalized monodromy能由 actual endpoint ratio恢复 d(0)，并在 G^f(0)=I frame中恢复完整 H^f；它并不直接提供 mean-normalized G(0)。因此，如果 (S8) 在 mean-G frame定义，必须标明该 frame已经 calibrated或 supplied/recovered；不能省略 G(0) 后称其自动由 class 或未经校准的 χ矩阵计算。

可以选择完全实际的 initial-value coefficient frame G^f(0)=I解决这一点。令 Q(z)=G_z(0)，那么
\[
a^f=aQ^{-1},\quad b^f=Qb,\quad H^f=QHQ^{-1},\qquad
M_{A^f}=D_QM_A D_Q^{-1},\quad D_Q=\operatorname{diag}(1,Q).
\tag{S10}
\]
Background Q(0)=I；一阶额外变化为 constant frame commutator。每个准确 collision block为 scalar，所以该 commutator的 rank-two压缩为零。Hence exact first norming derivative继续是 L\Gamma^\pm。

在此 frame中，D⟨a^f⟩、D⟨b^f⟩和完整 DH^f一般不为零；不能照搬 mean-G 的零 matrix derivative。准确关系是
\[
D(P_0a^f,P_0b^f)_0=D\Pi_0,\qquad
DH^f_0=[DQ_0,H_0],\qquad Dh^f_\ell(0)=0.
\tag{S11}
\]
Scalar collision仍给 source Born压缩对角变化为零，因此 Dc(0)=0。于是 (S9) 的 state IFT和原 χ端点校准可以真实接合，且无需一个未知 mean-G frame。

当前 B仅作原外部参数截面，μ/λ仍用 original label减去B；所有这些 derivatives保持B不变。外给B(t)的变化属于section变化，没有在此被冻结为原PDE的新守恒量。

最终审结：**finite high-gap independence、X_0 residual与所列strong传递前提均 PASS；calibrated framed norming real state IFT 的严格路线 PASS**。是否可将独立 statelemma直接称为原 χ full-data inverse，取决于其是否明确保留上述 actual frame calibration；不能据此称为 invariant divisor/action-angle inverse。

## 6. Saved formal state lemma 的最终逐式 readback

已完整读 [正式 augmented high-norming state lemma](general_m_augmented_actual_high_norming_state_inverse_recovery_20261011.md) §§1–7、(1)–(15)。本次读取版本 SHA256：

`DAA51914B2E4AB62EBA1619E0DE9750977C7BE533D903292970193AEBD0EFD15`。

其 (5) 保留 χ_{ℓn}^{−1} 的实际背景 scalar校准；(7)–(9) 逐一处理背景 spectral derivative、source center与 source-dependent frame；(10)–(12) 用 real positive-mode目标和uniform T_n inverse给真正 infinite-dimensional Banach state inverse。它没有丢掉复杂源的独立负频率后误用 complex IFT。

正式 §6 的 initial-value-frame版本完全解决本审查 §5 的 frame条件：原 χ full固定矩阵经 actual endpoint limit恢复 T_d(0)，其 conjugation直接给 normalized initial-value block。其 (13) 的 source-Q derivative在 scalarcollision压缩中为零；P_0 derivative相同，完整 H^f derivative虽为 [δQ,H_0]，eigenvalue derivative仍为零。因此同一 LΓ norming derivative与realIFT成立。两种frame的低 coefficient supplements始终按各自frame定义。

新增 imaginary-sample (14) 也成立。Actual FULL ℓ² remainder在 arbitrary bounded L² vector coefficients球上成立，故
\[
e^{K_nL/M}\widehat N^f(K_n)
=\alpha\operatorname{diag}(1,e^{LH^f})+\mathcal E_n,
\quad \mathcal E\in\ell^2,\quad
\alpha=e^{-L\operatorname{tr}H^f/M}\ne0.
\]
ℓ² sequence逐项趋零，limit的top-left先恢复 α，slow block再恢复完整 e^{LH^f}。H↦e^{LH} 的 derivative为
\[
K\longmapsto e^{LH_0}\int_0^L e^{-tH_0}Ke^{tH_0}dt.
\]
H_0 simple eigenbasis中，integral的eigenmatrix factors为 (1−e^{−L(p_i−p_j)})/(p_i−p_j)，difference为0时取L；(NR)使它们全部非零。因此 local finite-dimensional analytic IFT恢复唯一nearby完整 H^f，不只恢复eigenvalues。其 (15) 的 denormalization准确，不要求oldnear-zero ambient vector-potential inverse。

这些是实际数据的static恢复；正式稿未对整张 entire-function monodromy数据空间声明一个未证Banach topology。Finite low Fourier coefficients仍明确是 nonspectral supplements；H/frame metadata不是独立free targetcoordinates。Current B、component means及S标签均保留，也未添加Γ冻结条件。

**Saved formal readback：PASS，无剩余修正。** 范围是实际 augmented framed L²/ℓ² state inverse，不是high coordinates alone、class/divisor/action inverse、nonlinear canonical norming或all-H^N/strong-hierarchy theorem。
