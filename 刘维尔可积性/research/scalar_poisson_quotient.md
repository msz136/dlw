# 全周期标量系数像上的物理 Poisson 商与弱辛非退化

2026-10-11。以下命题接续 [全周期非线性局部像逆](completeness_routes.md)，不使用标准 AKNS 正则坐标来代替原物理括号。它完成的是静态完整物理叶的标量系数 Poisson 商；不是对任意混合边值中心像的辛性作推断。

## 源空间、归一化与准确常数

固定 M≥2、h>0、c≠0，x∈R/(LZ)。周期物理平均强制 c 恒定，任意 Γ(t) 的平移规范可先移去；以下使用固定的中心化谱参数。令 m=M−1。原物理叶固定各 pⱼ,sⱼ 的空间均值。

使用已有的精确自由场坐标 q₀,…,qₘ₋₁,d₀,…,dₘ₋₁：

$$
d_j=hw_j/8,
\quad q_j=b_j-b_m-d_j-2\sum_{k=j+1}^{m}d_k+d_m,
\quad b_j=U_j/2.
$$

它们与原 p,s 之间是可逆仿射变换，所以固定原分量均值等价于固定这些自由场的分量均值。在无权 integral 的变分配对下，准确物理张量为

$$
J_0=-\frac1{16}
\begin{pmatrix}0&I_mD\\I_mD&0\end{pmatrix}. \tag{1}
$$

源切空间是

$$
E_0=C^\infty_{{\rm per},0}(S^1;\mathbb R^{2m}),
$$

每个分量空间均值为零。D 在此空间可逆，故

$$
W_0=J_0^{-1}=-16
\begin{pmatrix}0&I_mD^{-1}\\I_mD^{-1}&0\end{pmatrix}. \tag{2}
$$

配对取普通 ∫、没有遗漏 h：若改用 h 加权配对，张量是 −(h/16)offdiag D，其逆与 h 配对相乘仍给 (2) 的相同二形式。

采用 $\omega_0(v,w)=\langle W_0v,w\rangle$ 的约定，使 $\omega_0(X_H,w)=dH(w)$。展开得

$$
\omega_0(v,w)=-16\int
[(D^{-1}v_q)\cdot w_d+(D^{-1}v_d)\cdot w_q]dx. \tag{3}
$$

等价地，分部积分可把 D⁻¹ 移到 w 一侧，得到正的 16 系数。D⁻¹ 是零均值周期逆，反对称；(3) 因而反对称、闭合且弱非退化。

## 有限系数像不应被误当作 ambient 开集

令

$$
F:z=(q,d)\longmapsto(\ell_1,\ldots,\ell_{2m})
$$

为已经证明有非线性局部像逆的标量 Lax 系数映射。记实际像为 $\mathcal Y$，局部逆为 G。F 由有限 jets 给出；G 由有限矩阵、ODE 旗标、Wronskian 和逆交换给出，允许有限导数损失。

这里不需要声明 $\mathcal Y$ 是无约束的 Banach 开集。对源叶上任一光滑曲线，F 给像上的曲线；用这些曲线定义切空间即可。令

$$
A_z=DF_z,
\qquad B_y=DG_y,
\qquad y=F(z).
$$

对源切向量和实际像切向量，链式法则给

$$
B_yA_z=I_{E_0},\qquad
A_zB_y=I_{T_y\mathcal Y},
\quad T_y\mathcal Y=A_zE_0. \tag{4}
$$

这些等式是 C∞ 分级意义下的等式；不能从它们推出同阶 Sobolev 上的有界 Banach 同构。事实上 A 通常含高阶 D，B 也有有限损失。

## 物理 cotangent 的真正商

先考虑 ambient 的光滑系数协向量 $\lambda\in C^\infty_{\rm per}(S^1;\mathbb R^{2m})$。源叶上其拉回是

$$
a_\lambda=\mathcal P_x A_z^*\lambda,
$$

其中 $\mathcal P_x$ 分量逐个移去空间均值。该投影不能删去：源叶的常数协向量正是原物理 Casimir 法向。

准确的标量系数推前是

$$
J_{\mathcal Y}\lambda=A_zJ_0a_\lambda
=A_zJ_0\mathcal P_xA_z^*\lambda. \tag{5}
$$

由 (4) 的 A 单射及 (1) 在 E₀ 上可逆，

$$
J_{\mathcal Y}\lambda=0
\quad\Longleftrightarrow\quad
\mathcal P_xA_z^*\lambda=0. \tag{6}
$$

另一方面

$$
\langle\lambda,A_zv\rangle
=\langle\mathcal P_xA_z^*\lambda,v\rangle,
\quad v\in E_0.
$$

所以 (6) 的核恰是实际像切空间的 conormal。这个结论明确排除了“推前张量可能在像上还有未发现的连续核”的疑虑：其 ambient 核全部来自冗余法向协向量，包含源常数 Casimir 的拉回。

**不能暗中增加的结论：** 上述论证没有证明所有像上的可容许协向量均能由光滑 ambient 系数数组 λ 表示。仅凭非线性像逆，不能自动断言 $A^*$ 在这个特定 ambient 光滑数组类中满射。需要更大弱 cotangent 类，或另证具体 Sobolev/分级代表的可解性。

为避免把这个问题藏在“cotangent”一词里，定义像上的物理可容许协向量为：作用在 $T_y\mathcal Y$ 上的线性泛函 α，且其源拉回 $A_z^*\alpha$ 在 E₀ 的 L² 配对下有一个光滑零均值代表。所有由源光滑 Hamilton 泛函 $H$ 经 $H\circ G$ 得到的协向量都属于此类。这一定义同时包括现有的有限 differential trace 泛函。

在该类中，以“在实际像切空间上作用相同”为等价关系。拉回给出的商

$$
T^*_{y,\rm adm}\mathcal Y\ \cong\ E_0
$$

是明确的同构：任意源代表 a∈E₀，可定义
$\alpha(v)=\langle a,B_yv\rangle$，其拉回就是 a。这里没有声称 α 必有光滑 ambient 数组代表。

对这整个物理 admissible cotangent，定义

$$
J_{\mathcal Y}\alpha=A_zJ_0(A_z^*\alpha).
$$

由 (4)，它是从该弱 cotangent 到实际像切空间的双射，且与 (5) 在光滑 ambient 代表上相同。

## 显式弱辛形式与非退化测试

像上的物理二形式无需借标准 AKNS 张量，可直接写成

$$
\boxed{\quad
\omega_{\mathcal Y}(v,w)
=\omega_0(B_yv,B_yw)
=\langle W_0B_yv,B_yw\rangle.
\quad} \tag{7}
$$

它是原物理二形式的真实换坐标。闭合由 $\omega_{\mathcal Y}=G^*\omega_0$ 及 dω₀=0 得到；反对称同样立即成立。

对任意非零 v∈Tᵧ𝒴，令 η=Bᵧv。由 (4)，η≠0。取

$$
w=A_zW_0\eta\in T_y\mathcal Y.
$$

则

$$
\omega_{\mathcal Y}(v,w)
=\langle W_0\eta,W_0\eta\rangle
=\int|W_0\eta|^2dx>0. \tag{8}
$$

因此 **ω𝒴 在整个实际标量系数像的光滑切空间上弱非退化**。这个明确的测试向量比只说“坐标变换应保持辛性”更强：它给出了任何疑似核向量的物理配对伙伴，并记录了原 D⁻¹ 的边界与常数因子。

若 H 是可容许 Hamilton 泛函，(7) 给

$$
\omega_{\mathcal Y}(J_{\mathcal Y}\delta H,w)=dH(w),
$$

所以 (5) 真正是 (7) 的 inverse Poisson tensor。Jacobi 由原 J₀ 的 Poisson 性在实际像上的坐标变换继承，不是从未核对的 scalar constrained-KP 名称继承。

## 谱极大性的下一条精确判据

设 $I_\alpha$ 为已证明对合且可容许的谱泛函，记

$$
\mathcal V_y=\operatorname{span}\{J_{\mathcal Y}\delta I_\alpha\}.
$$

由 Hamilton 恒等式，

$$
\mathcal V_y^{\omega}
=\{v\in T_y\mathcal Y:\ dI_\alpha(v)=0\ \forall\alpha\}. \tag{9}
$$

若选定 C∞ 分级拓扑，闭包的连续性应在该拓扑中逐项核验；最大等方性的目标就是

$$
\overline{\mathcal V_y}=\mathcal V_y^{\omega}. \tag{10}
$$

将 (9)–(10) 拉回源叶，可完全排除 ambient conormal 的干扰：需要证明

$$
\overline{\operatorname{span}\{J_0a_\alpha\}}
=\bigcap_\alpha\ker\langle a_\alpha,\cdot\rangle,
\qquad
a_\alpha=\mathcal P_xA_z^*\delta I_\alpha. \tag{11}
$$

这把“谱数据是否完备”变成具体的源 covector/span 恒等式。无限多个独立 aα 只给左边包含在右边；完整 Floquet/divisor 逆或 squared-eigenfunction 完备性必须给反向包含。式 (6)–(8) 已经证明 Poisson 商及弱辛核不是剩余障碍，不能再以未知 ambient bracket 代替这个具体谱问题。

## 范围与没有宣称的事项

已证明的是全 M、任意函数自由度的局部完整物理叶到其有限标量系数像的准确 Poisson 商、原物理弱辛形式与非退化性。它没有使用 finite-gap 近似，也没有为源向量假设实际实时间 Sobolev 流存在。

若另选实际混合边值中心像 $\mathcal Z\subset\mathcal Y$，它的切空间可能小于 A E₀。(8) 的配对伙伴 w 未必属于 T𝒵，所以不能把本命题直接移到那张中心像；须另证其切空间对这些伙伴或等价的辛投影封闭。

尚未证明 (10)–(11)、谱作用角的全局/无限维解析逆，或实际解流上的共同层级域。但现在这些问题可以在已明确且非退化的原物理 Ω 上审计，无需再选择一个与原括号不相干的 canonical AKNS 张量。
