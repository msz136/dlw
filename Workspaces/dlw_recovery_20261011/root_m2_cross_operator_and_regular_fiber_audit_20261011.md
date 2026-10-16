# M=2：actual action–angle cross operator 与真实水平集的根复核

2026-10-11。逐式读取 [新的 cross-operator 证明](m2_action_angle_cross_operator_and_profile_obstructions_20261011.md) §§1–8，独立核验其分析预算、same-action 测试及 period 障碍。没有运行机器检查。本稿不把新算子逆升级为尚未证明的 regular fiber 或 strong infinite Hamilton 流。

## 1. 精确 pure-action torque 与归一化

沿用已审 reduced Cartesian W=(wn,zn)、Jn=wnzn、I0=ρ(J)、η=η̃(J) 及 central-angle section。θn=(2i)⁻¹log(wn/zn)，standard XI 的 θ 速度为 −1；因此由 DR XFλ=ωλΠY 和 Y=(L/i)Xstd，physical trace 的 reduced θ 速度是
\[
iL\omega_\lambda\,(\partial_{I_n}d-\partial_{I_0}d),
\qquad \omega_\lambda=(S^2-\lambda^2)/(16S).
\]
Δ=d(z,I) 和 η̃ 都只依赖 actions，所以该速度只依赖 J。full-action contour 的 holonomy 项已由实际 winding 消去，因而
\[
B_{nm}(J)=-\frac{iL}{\pi}\oint_{\Gamma_m}
\frac{\omega_{\eta-2iz/L}(\partial_{I_n}d-\partial_{I_0}d)}R\,dz.
\]
它使用 projected full derivative，不偷换为 dρ 参与的 reduced functional derivative。

闭隙背景的 simple R 零点 residue 恢复 dIm。λm*=−2izm*/L、(zm*)²=π²m²−L²δ²、S=2δ 给
\[
B_{nm}(0)=\frac{iLk_n^2}{16S}\delta_{nm}=:D_n\delta_{nm}.
\]
角符号 iL 已独核；Cartesian torque 为 ẇn=iwn(Bc)n、żn=−izn(Bc)n。每固定 nm 的 pure-action coefficient 可跨零对全纯延续。实际 Hc=ΣcmIm 对 bounded c 在 low h⁰ chart 中确有意义。

## 2. 真正 physical h²→h⁰ 预算

小 h² 状态给 u∈H²、v∈H³。辅助 canonical identity只用于 KLTZ 图转置的 H² 有界性；physical potential transpose 再给 gradients H²×H¹，其唯一 differential entry为 D/S。原 Juv=−offdiag(D)/16 给 physical velocity L²×H¹，low 状态图 derivative 给 h⁰。所有系数/finite central terms 在该 Banach 球解析且 uniform，所以
\[
\|\mathbb J(W)-\mathbb J(0)\|_{h^2\to h^0}
\le C\|W\|_{h^2}.
\]
这是原 physical tensor 的预算，并未把 NLS bracket 移植回来。作用于 dHc=(cz,cw)，得到 uniform error ≤C‖c‖∞‖W‖²h²。

## 3. 全频 same-action 测试与确切生成

对 ‖J‖ℓ¹₄≤r²，在第 n 对取 wn=r⟨n⟩⁻²、zn=Jn⟨n⟩²/r，其他 pairs取 balanced square roots。测试的 h² 范数 ≤Cr，与 n 无关；它们全在同一个 low branch。不需要 square-root 选择对 J 全纯，也不声称这些复测试态是物理实态。

pure-action torque 允许用这份同 J 的测试代替任意原 wn。用 uniform field error除以刻意选取的 r⟨n⟩⁻²，而非实际可能极小的 wn，准确得到
\[
\sup_n\frac{|(B(J)c)_n-D_nc_n|}{\langle n\rangle^2}
\le Cr\|c\|_\infty.
\]
令 V₂={v:sup|vn|/⟨n⟩²<∞}；D:ℓ∞→V₂ 是 iso，故足够小单一 r 上
\[
\boxed{B(J):\ell^\infty\longleftrightarrow V_2\text{ bounded iso}.}
\]
bounded c 的 bare finite truncations不在ℓ∞范数中收敛，但乘 rapid W 后在所有所需 hᴺ 中收敛；实际转置/J 连续性给其 Hamilton 场。这证明在 smooth 状态，每个 V₂ angular velocity 是某个 genuine Hc 的确切速度，超过只取闭包的结论。

尚未证明这个 Hc 在同一 S∞ 的内部切向存在、或有实际 joint Banach flow。也没有将 V₂ 宣称为整个 ambient smooth 共同核的角速度空间。

## 4. 不能省去的真实水平集问题

若 Eg=sup|θn|/gn、gn→∞，则 4πi en→0 而指数 wn*exp(θn/2)、zn*exp(−θn/2) 完全回到同态。故任何 complex Eg 球都不是局部单射 state 图；点对点截 imaginary strip 在此拓扑没有 interior。商的 period kernel 也不离散。加 variable actions 仍保留这一缺陷。

即使只用 real hyperbolic logs，适当 decay margin 下 θn=rgn en 的 Cartesian 像趋于基点，但其 profile 范数固定，故 inverse 对 inherited rapid/C∞ topology不连续。另指定 stronger topology可以研究 immersed 相域，但必须明确，不能称 ambient regular submanifold。

当前核心接续是选择 period 离散的真实函数相域，证明完整 variable-action/angle 图及原 reality，证明 continuous 原 Ω 在该域弱非退化，并容纳实际原 DLW 时间和足够 Hamilton 轨道。bounded compact angles 加独立原时间/平移方向是候选；尚未成为 theorem。上述 cross-operator iso 为这一工作提供 actual 物理输入，闭包最大性仍不代替 regular fiber 与完整 Liouville 可积区域。
