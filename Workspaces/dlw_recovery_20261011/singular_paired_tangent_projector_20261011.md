# κ 非零层的 exact paired tangent 投影

2026-10-11。此为独立新推导，不运行旧证书。接续 [singular_branch_independent_audit.md](singular_branch_independent_audit.md) §§8–9，补足“主符号确来自真实约束切向”的算子依赖。

## 1. 全圆坐标与精确一阶约束

记 canonical 背景为 (Y,s)=(T,S)，ΠT=ΠS=Π(TS)=0，χ=κ≠0。前审已独核 T、S 逐点非零；令 σ=ΠS²>0、τ=ΠT²>0。Π 为格点平均，本稿内积均采用 Π。

\[
A_\phi(y,z)=\Pi(Sy+Tz),\qquad
A_\chi=(-S D-2c+S_x,\ T D-2e-T_x),
\]

c=VY、e=Vs。每个 exact primary tangent 唯一写成

\[
y=u+fS/\sigma,\qquad z=v-fT/\tau,
\qquad \Pi(Su)=\Pi(Tv)=0.
\tag{1}
\]

故 E={(u,v):ΠSu=ΠTv=0} 是主阶自由变量，f 是一个实标量函数。对 E 中的变量，微分约束 ΠSu=ΠTv=0 给

\[
h_E:=A_\chi(u,v)=-2\Pi[(c-S_x)u+(e+T_x)v].
\]

没有 u_x、v_x。对法方向 Z=(S/σ,−T/τ)，精确计算得到

\[
A_\chi(Zf)=Lf,\quad L=-2D+\vartheta,
\]

\[
\boxed{\vartheta=(\log(\sigma\tau))_x-
2\Pi(cS)/\sigma+2\Pi(eT)/\tau.}
\tag{2}
\]

例如 y 块的零阶系数为 σ_x/σ−2Π(cS)/σ，z 块为 τ_x/τ+2Π(eT)/τ，给出 (2) 的全部符号。

配对 stage 的次约束为 Pxχ=0，允许 δκ 为初态能量水平的变化。因此 exact tangent 条件是

\[
h_E+Lf=\delta\kappa,\qquad\delta\kappa\text{为空间常数}.
\tag{3}
\]

固定能量 κ 的切向另加 δκ=0；不能默认它是当前 phase 的 Casimir。

## 2. 不需非共振假设的统一增广逆

对任意实光滑周期 ϑ，算子

\[
\mathcal A:\ H^{r+1}_0\times\mathbb R\longrightarrow H^r,
\qquad(f_0,k)\longmapsto Lf_0-k,
\tag{4}
\]

是有界同构。下标 0 表示空间平均零。证明给出全部 holonomy 情形，而不是假设 D−ϑ/2 自动可逆。

令 γ=ϑ/2，E(x)=exp(∫0^xγ)，H=E(L)>0。若 H=1，Lf=0 的周期核由正函数 E 生成；adjoint L*=2D+ϑ 的核由正函数 E−1 生成。若 Lf0=k 常数，配正 adjoint 核给 k=0；再以 avg f0=0 消去正核，故 f0=0。

若 H≠1，L 已可逆。Lf=k 的周期解由 first-order integrating factor 得

\[
f(x)=\frac k2 E(x)\left[
\frac{H}{H-1}\int_0^LE^{-1}(s)ds-
\int_0^xE^{-1}(s)ds\right].
\]

当 k≠0，这个括号在全圆严格同号：H>1 时严格正，H<1 时严格负。因此 f 严格同号，avg f≠0，不能属于 H^{r+1}₀。故 (4) 仍单射。

L 是 circle 上的一阶 elliptic Fredholm 算子，index 0；限制 domain 均值零减去一个 index，加入 k 补回一个 index。因而 (4) index 0，单射即满射。ODE 正则性及闭图定理给所需一阶增益；局部 operator-inverse 公式还给背景 ϑ 的光滑依赖。ϑ 平均零或 holonomy 穿过 1 不造成这个增广逆退化。

## 3. exact tangent 参数化与阶零 projector

保留 ν=avg f 为一个真实全局自由参数，令 f=ν+f0。在 (4) 中解

\[
\mathcal A(f_0,\delta\kappa)=-h_E-\vartheta\nu.
\tag{5}
\]

再按 (1) 重建，得到全部 exact paired tangents。ν=0 是方便的高频图切片，但不是可以擅自删除的物理零模，也不一定是平移规范；平移方向的 ν=−avg Π(STx) 未必非零。

任意变分先唯一写 y=u+aS/σ、z=v+bT/τ，其中 a=ΠSy、b=ΠTz。将 primary 法向 a+b 去掉，并取 ν=avg[(a−b)/2]；用 (5) 更新 f，输出 (u+fS/σ,v−fT/τ)。这定义一个实线性、阶零、有界的 exact paired tangent projector。若输入已满足 Aφ=0、PxAχ=0，则 (5) 的唯一性恢复原 f，故 projector 幂等。

ν 的处理和 δκ 是有限 rank 全局项。高频部分中 hE 只有零阶，(4) 的 f0 逆增益一阶，所以 E→paired tangent 的 lift 为 I+order−1，投影的 principal symbol 正是

\[
\operatorname{diag}(I-S\otimes S/\sigma,
I-T\otimes T/\tau)
\]

（格点平均零空间内）。因此前审的 E 主符号并非 fake tangent 或仅忽略 lower-order 约束后的矩阵；它是 exact paired constraint chart 的 principal symbol。

若同时规定全部组件空间 Casimir 均值，还要在此 chart 中加入有限个全局线性条件。在其正则 stratum 可用有限 rank 修正；固定均值常背景的动量临界性并没有被本 projector 自动消除。有限 rank 条件不改变已经核实的微局部主符号。

## 4. 振荡块的一阶周期条件

恒定分离的二阶 principal eigenvalues ±i/√3 本身不足以证明 Schrödinger 中心块实际流。若进一步微局部消去不同二阶特征值的 off-diagonal 一阶项，某一复中心块为

\[
\lambda D^2+b(x)D+O(1),\qquad\lambda=\pm i/\sqrt3,
\]

周期 scalar 共轭取 ζx=(b−avg b)/(2λ)，只能去掉 b 的非恒定部分。剩余常数漂移 (avg b)D 的 Fourier 实增长率是 −k Im(avg b)。因此两侧频率的 Sobolev 双向流需要

\[
\boxed{\operatorname{Im}(\operatorname{avg}b)=0.}
\]

这个条件是 circle 上的必要 Mizohata 型平均条件。不能把只有 principal 振荡谱的证明扩大成完整中心流存在性；本稿没有独算原物理图中的全部 subprincipal b。

新的 exact constrained-KP 表示若已真实回拉成功，则其中心 Ψ 方程是纯 Schrödinger 加实平移、半线性项及 heat 源项导数，可以直接处理中心存在性，不必从裸 physical principal 矩阵猜测这个平均条件。该路线仍需源项、端点 mixed 估计和原物理回拉逐项证明。
