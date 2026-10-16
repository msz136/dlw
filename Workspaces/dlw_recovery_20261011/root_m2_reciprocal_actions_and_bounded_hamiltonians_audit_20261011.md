# 根复核：原物理 reciprocal actions 与全部有界角 Hamilton 流

2026-10-11。本稿独立推导 reciprocal contour 的变分与无穷求和。依赖已审 [真实物理 trace push](m2_physical_trace_poisson_closure_proof_20261011.md)、[mixed-low 实际谱场](m2_actual_mixed_low_fields_bounded_torques_real_form_20261011.md) 及 [条件性 reduced 状态图](akns_physical_state_inverse_bridge_20261011.md)。本稿没有运行 checks，不替代一般 M 完备性证明。

## 1. 精确变分，保留随源变化的谱中心

令
\[
\lambda(z)=\eta-2iz/L,\quad
\omega_\lambda=(S^2-\lambda^2)/(16S),\quad
R(z)=\sqrt{\Delta(z)^2-4}.
\]
在每个非中央固定 contour 附近取解析 primitive
\[
P_n(z,\eta)=4iL\log_n\frac{S+\lambda(z)}{S-\lambda(z)}.
\]
需同低域内所有这些 contour 都避开 \(\lambda=\pm S\)；中央标定 disc 与非中央 \(n\pi\) disc 的分离供应这一条件。primitive 的源依赖加常数无影响，因为已有零 winding
\(\oint_{\Gamma_n}\Delta_z/R\,dz=0\)。实际非中央 charge 定义为
\[
A_n=\pi^{-1}\oint_{\Gamma_n}P_n\Delta_z/R\,dz.
\tag{1}
\]
直接求导给
\[
P_z=\omega_\lambda^{-1},\quad P_\eta=iL/(2\omega_\lambda),\quad
F'_\lambda=(iL/2)\Delta_z.
\]
因 \(\delta(\Delta_z/R)=\partial_z(\delta\Delta/R)\)，分部积分并保留 \(\delta\eta\) 后，
\[
\delta A_n=-\pi^{-1}\oint\frac{\delta\Delta}{\omega_\lambda R}\,dz
+\pi^{-1}\oint\frac{iL\Delta_z}{2\omega_\lambda R}\,dz\,\delta\eta.
\]
而 \(\delta\Delta=\delta F_\lambda+F'_\lambda\delta\eta\)，其中 \(\delta F_\lambda\) 是固定原 centered 参数的场变分。两个中心项严格抵消。因此
\[
\boxed{\ dA_n=-\pi^{-1}\oint\frac{dF_\lambda}{\omega_\lambda R}\,dz\ }.
\tag{2}
\]
此计算没有固定 \(\eta\)，也没有把随源变化的参数误当常数。

精确实际 trace 场关系 \(D\mathcal R X_{F_\lambda}=\omega_\lambda\Pi Y\Delta\) 代入 (2) 后给
\[
\boxed{\ D\mathcal R X_{A_n}=\Pi YI_n
=L(-w_ne_n,z_ne_n).\ }
\tag{3}
\]
数值系数来自已审 \(Y=(L/i)X_{\mathrm{std}}\) 和 \(X_{I_n}^{\mathrm{std}}\theta_n=-1\)。故 (3) 是原物理 Hamilton 场，不是另设 NLS Poisson 张量。

各 \(A_n\) 只依赖真实共同 actions；在背景非中央闭隙处 (1) 为零。因此 \(A_n(0)=0\)。它们彼此对合，并与全部实际 trace、原 \(C_j\) 和平移对合。实结构和对称 log 标定给 \(A_{-n}=\overline{A_n}\) 于真实物理片上。

## 2. mixed-low 原辛形式给一致求和

源空间 \(X_0=L^2_0\times H^1_0\) 上原 \(\Omega\) 是连续闭二形式：\(D^{-1}\) 在零平均空间连续，其积分配对连续。实际 reduced 低图 \(\mathcal R\) 双解析，故
\(\widetilde\Omega=(\mathcal R^{-1})^*\Omega\) 在一个星形 \(E_0=(\ell^2)^2\) 球上解析且局部有界。

对有限支持 \(d\)，令 \(H_d=\sum d_n A_n\) 及
\[
Z_d(W)=L(-d_nw_n,d_nz_n)_n.
\]
由 (3)，\(dH_d=\widetilde\Omega(Z_d,\cdot)\)。径向积分给
\[
H_d(W)=\int_0^1\widetilde\Omega_{tW}(Z_d(tW),W)\,dt,
\quad |H_d(W)|\le C\|d\|_\infty\|W\|_{E_0}^2.
\tag{4}
\]
有限支持 \(d_n\) 可独立取与 \(A_n(W)\) 相反的相位，故
\[
\sum_{n\ne0}|A_n(W)|\le C\|W\|_{E_0}^2.
\tag{5}
\]

对于任意 \(d\in\ell^\infty\)，\(Z_d\) 是有界线性低场。其有限截断在每个固定 \(W\) 及固定切向上强收敛。于是解析一形式
\(\alpha_d=\widetilde\Omega(Z_d,\cdot)\) 的外微分可逐个固定切向取有限截断极限；每个有限截断闭，故 \(d\alpha_d=0\)。径向积分 (4) 仍是解析函数，且由闭一形式的径向 primitive 身份给 \(dH_d=\alpha_d\)。逐点主导收敛把它识别为绝对收敛的 \(\sum d_nA_n(W)\)。

这一步没有宣称 bare multiplier 截断在算子范数中收敛。强收敛只用于固定 \(W,U,V\) 的二形式和外微分；连续性供应极限。因全部 \(\ell^\infty=(\ell^1)^*\) 配对函数解析而 (5) 局部有界，\(A:E_0\to\ell^1\) 为 Banach 值解析映射。

因此每个 bounded coefficient charge 是真实低 Hamiltonian，并有低 Banach 唯一流
\[
\boxed{\quad w_n(t)=e^{-Ld_nt}w_n(0),\quad
z_n(t)=e^{Ld_nt}z_n(0).\quad}
\tag{6}
\]
在低图的存在窗内，(6) 保持全部 \(J_n=w_nz_n\)。对实系数形式 \(d_{-n}=\overline{d_n}\)，它保持精确原物理 reality。对任意光滑初态，bounded multiplier 也保持每个 \(h^N\)，故对应真实光滑原物理轨道。

## 3. 精确范围

(1)–(6) 供应整个相邻 action 域上的全部有界 logarithmic 角 Hamilton 场，解决仅在一点选择 \(B(J_0)^{-1}\) 的邻域流缺口。它没有宣称全部二次增长频率都是有界频率，也没有把旧 \(S_\infty\) 的 inherited 水平集改成普通流形。原时间的二次频率仍需单独 heat 方向；平移仍需单独有限方向。以这两方向加 bounded profiles 构造的新变量 action 相空间，须另审单射、普通 fiber、原 \(\Omega\) 非退化及实际共同轨道。

完整一般场、一般 M 目标保持 OPEN。
