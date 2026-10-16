# 一般 M 周期 block gauge 与低阶状态逆：根复核

2026-10-11。独立读取 [一般 M 低阶逆审计](general_m_periodic_gauge_state_inverse_independent_20261011.md)、[闭式微分证据](general_m_inverse_linearization_independent.md) 与 [holonomy 审稿](all_m_holonomy_image_independent_audit_20261011.md)。下面重新核对分析链；不运行旧脚本或把 coefficient state 图称为谱 norming 图。

## 1. 周期规范的真实 Banach IFT

固定有限 M≥2、m=M−1、S=Mδ≠0，原均匀组件均值叶。原 split 的 q 是 1×m row，r 是 m×1 column，V 是 m×m matrix。取 mean-normalized G_x=VG−GH、〈G〉=I。

G=I+g、〈g〉=0 时 H=〈V(I+g)〉，方程为 Dg−P₀[V(I+g)]+g〈V(I+g)〉=0。其值的平均为零；定义在 g∈H¹₀、V∈L²，因为只出现 H¹×L² 和 H¹×constant 的连续乘法。背景微分是 D−ad V₀，V₀=V*−BI。

在每个非零 Fourier k，(ik−ad V₀)⁻¹ 对大 |k| 具有 O(|k|⁻¹) 界；若所有低频无 alias，有限个低频界亦有限。因此它准确是 H¹₀→L²₀ 的有界同构，复解析 IFT 给同一低域 G∈H¹、H 常矩阵。缩域 G 点点可逆。没有采用不周期的 fundamental gauge 后丢弃 holonomy。

由 G_x=VG−GH 得 (DI−V)∘G=G∘(DI−H)，所以 ℒ=D−a(DI−H)⁻¹b、a=qG、b=G⁻¹r。Y_V=G e^{xH}G(0)⁻¹ 给真实内部单值矩阵 Y_V(L)=G(0)e^{LH}G(0)⁻¹。原 frame 须保留 G(0) 和原 split T(0)，不能将 (a,b,H) 的 class 数据冒称完整 framed 数据。

## 2. 原物理低阶预算与完整微分的单射

原 d_m=S−Σd_first，1ᵀd_x=0，故 Kd_x=d_first,x，准确 r=−d_first,x/S+F(q,d)。V 与 F 为 d 的有限多项式、对 q 至多一次。因此 q∈L²、d∈H¹ 时，V,r∈L²；规范 G、G⁻¹∈H¹ 是乘子，a,b∈L²。所有映射复解析，不含非法 L²×L² 非线性。

固定原 free 组件空间均值，在背景 δq=u、δd_first=v 零均值。δV=W(u,v)、δF=Z(u,v) 都零阶常系数，δH=〈δV〉=0。δa=u+q*g，δb=Z(u,v)−Dv/S−g r*，也零均值。

若某个非零 Fourier block 的 projected δa、δb 为零，则完整 δa、δb 与 δH 都为零。实际算子恒等式给 δℒ=0。直接从原有序 transfer 推得

\[
\delta\mathscr L=e^{zx}
\frac{-4S\,P_z(p)}{\mathcal R_M(p+z)\mathcal R_M(p)},
\qquad
P_z=\delta H_1(w)+pK_1(w),\quad w=p^2+zp-\delta^2.
\]

z≠0、δ≠0 时原 Bernstein 基 (w+zδ)^{m−j}(w−zδ)^j 独立；源的格点零和约束使 H₁,K₁ 的次数≤m−1。反射 p↦−z−p 保持 w，相减给 (2p+z)K₁(w)=0，继而 H₁=0，全部物理 Fourier 系数零。背景 free q,d 与原 b,d 的线性换元可逆。因此 projected potential 微分的每个 2m×2m block 单射、从而满射。

以上使用全部 x-dependent state 算子，**没有用 actual class traces 的微分**；那些在均匀态非零 Fourier 切向上都一阶为零。

## 3. 统一低/高频界与同一低域的全阶逆

源用 (u,Dv) 的 L² 等价 norm，非零 Fourier primitive在周期均值零空间有界。大 |k| 时 g=O(k⁻¹)u+O(k⁻²)Dv，projected map 微分趋于

\[
\begin{pmatrix}I&0\\Z_u&-I/S\end{pmatrix}
\quad\text{对 }(u,Dv).
\]

必须保留 Z_u 的零阶交叉项；矩阵依然可逆。由高频渐近和有限个低频已证单射，得到 L²₀^m×H¹₀^m→L²₀^{2m} 的全频有界同构；同样论证在各 Hᴺ×Hᴺ⁺¹ 层成立。解析 Banach IFT 因而给真正的一般函数状态开域，不止微分单射。

给高阶 a,b，先用同一低阶逆补回它们的平均及 H，再用 q=aG⁻¹、G_x=VG−GH、d_first,x=SF(q,d)−SGb。这组一阶方程从 qL²、d/G H¹ 逐阶 bootstrap，恢复 qHᴺ、d/G Hᴺ⁺¹。线性化同样 bootstrap，低阶逆唯一性及闭图定理给每个高阶导数逆有界；各高阶 Banach IFT 与低阶唯一逆识别。因此所有阶共用一份低域，未为每阶缩到零或人为选择新半径。

## 4. 参数、图约束及既有 strong 背景兼容

内部 H、〈a〉、〈b〉都是 projected potentials的有限解析函数，固定 B 时完整 (a,b,H) 像为复 codim 2m+m² graph。任意给定 B 增加 BI 到 V/H，q/r/G/a/b 不变。必须保留 B 参数；不能从 projected a,b 单独恢复它，亦不推导 B_t=0。原变量 c=S·8/(hM) 可在叶之间改变。

原均匀 V₀ 的 eigenvalues p_j=−iδcot(πj/M)、j=1,…,m；无 alias 条件为 ik₀n≠p_j−p_k，n≠0，k₀=2π/L。只排除可数 δ 值。此处可核对它与既有 strong 独立性背景相容：M>2 时

\[
\max_{j,k}|p_j-p_k|=2|\delta|\cot(\pi/M).
\]

若用 mixed §14–17 的 |δ|<(k₀/2)tan(π/(2M))，则

\[
2|\delta|\cot(\pi/M)
<k_0\tan(\pi/(2M))\cot(\pi/M)
=\tfrac{k_0}{2}\bigl[1-\tan^2(\pi/(2M))\bigr]
<k_0.
\]

所以已有全部 finite-charge 独立 strong 小背景自动无 alias，**这项状态图不要求为那些背景另加更小 c 条件**。M=2 的 ad V₀=0，非零频自动合法。mean-normalized gauge 的 Euclidean 粗 bound只是另一充分条件，不替代这个准确谱判据。

这证明新状态图可在既有 strong 均匀背景附近考虑。没有因此把 state map 的所有开放源点归入 S∞，也未证明全 M norming 逆或谱 actions 最大性。

## 5. 审结

PASS：一般 M 的低阶 periodic block gauge、保留 holonomy 的 coefficient 状态逆、同低域全阶正则、有限约束及 B 参数。需源文把 scalar-C_n 的既存 finite-factor inverse 与本轮新的低阶 Banach 图分清，不能重计旧 Jordan 旗标为新结果。

后续真正的缺口是从完整 framed spectral/norming 数据重建 a,b,H，以及 actual class Hamilton 场对周期规范共同微分核的稠密生成。已有 [cyclic 单值矩阵谱核引理](all_m_cyclic_monodromy_gauge_kernel_20261011.md)允许 Jordan 碰撞，可作为这一全 M route 的精确接口。没有给 ordinary regular fiber 或 Liouville 完结。
