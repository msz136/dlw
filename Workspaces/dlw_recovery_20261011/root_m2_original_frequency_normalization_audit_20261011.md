# 根复核：原 DLW 时间的二次频率与有界余项

2026-10-11。使用真实 [trace/quasimomentum 桥](m2_physical_trace_poisson_closure_proof_20261011.md) 与 [同低域谱状态图](akns_physical_state_inverse_bridge_20261011.md)。本稿独立核对 Riccati 系数、time normalization 和频率来源。未运行 checks。

## 1. 固定辅助参数的实际 Riccati 系数

对 \(A_\zeta=\left(\begin{smallmatrix}\zeta&a\\b&0\end{smallmatrix}\right)\)，\(\beta_x=b-\zeta\beta-a\beta^2\)。前三项是 b、−b_x、b_xx−ab²。实际 fast multiplier 的审定 C¹ 余项遂给
\[
\ell_\zeta=L\zeta/2+c_1/\zeta+c_2/\zeta^2+c_3/\zeta^3+O_{C^1}(\zeta^{-4}),
\]
\[
c_1=\int ab,\quad c_2=-\int ab_x,\quad
c_3=\int(ab_{xx}-a^2b^2).
\tag{1}
\]
这不是从形式 Laurent 系数直接宣布实际场展开；固定有限 angular covector 按已审 high Sobolev transpose 预算应用 C¹ 余项，允许逐个 angular component 比较。

KLTZ 势 \(\varphi_1=-iLa/2,\varphi_2=2iLb\)、单位周期 \(y=x/L\) 下，NLS Hamiltonian 为
\[
E=\int_0^1(\varphi_{1,y}\varphi_{2,y}+\varphi_1^2\varphi_2^2)dy
=L^3\int_0^L(a_xb_x+a^2b^2)dx.
\]
周期分部积分给 \(c_3=-E/L^3\)。质量 \(c_1\) 的标准场只是 constant diagonal gauge，因此 \(\Pi Yc_1=0\)；\(c_2=-\int ab_x\) 的辅助 x-normalized 场恰为平移 \(Yc_2=(a_x,b_x)\)。其中 \(Y=(L/i)X_{\rm std}\)。

## 2. 原 centered 时间不重标定

原 centered \(\lambda\) 满足 \(\zeta=\lambda-\eta\)，\(\omega_\lambda=(S^2-\lambda^2)/(16S)\)。实际 quasimomentum 身份是
\[
D\mathcal R X_{\mathcal K_\lambda}
=\omega_\lambda\Pi Y\ell_\zeta+(L/2)D\mathcal R X_\eta,
\qquad \mathcal K_\lambda=-C_1/\lambda+O_{C^1}(\lambda^{-2}).
\tag{2}
\]
原 \(X_\eta=\partial_x/(8SL)\)。右侧常数项是
\(-\partial_x/(16S)+(L/2)\partial_x/(8SL)=0\)，这是中心项保留正确的独立核对。

右侧 \(\lambda^{-1}\) 系数为
\(-\Pi(Yc_3+2\eta Yc_2)/(16S)\)。比较 (2) 得
\[
D\mathcal R X_{C_1}=\Pi(Yc_3+2\eta Yc_2)/(16S).
\]
原物理 Hamiltonian 的已审时间归一化 \(H=-16SC_1\) 因而给
\[
D\mathcal R X_H=-\Pi Yc_3-2\eta\,\partial_x
=-i\Pi X_E^{\rm std}/L^2-2\eta\,\partial_x.
\tag{3}
\]
本地 \(w=(x+iy)/\sqrt2\)、\(\theta=(2i)^{-1}\log(w/z)\) 的 convention 下 \(X_E^{\rm std}\theta_n=-\omega_n^{\rm NLS}\)。中央角投影减去 n=0 频率；平移对 w 的指数为 \(ik_n\)、\(k_n=2\pi n/L\)。因此精确原时间 torque 是
\[
\boxed{\quad
\Omega_{H,n}(J)=-\frac{\omega_n^{\rm NLS}(I(J))-
\omega_0^{\rm NLS}(I(J))}{L^2}-2i\widetilde\eta(J)k_n.
\quad}
\tag{4}
\]

## 3. 唯一新增的频率分析输入

实际读取 [Berti–Kappeler–Montalto 全文 PDF](https://arxiv.org/pdf/1603.09252) Theorem 3.2（PDF 第23页，正文页22）。它在包含整个正 action cone、特别包含 0 的 complex \(\ell^{1,2}\) 邻域上给 \((\omega_n^{\rm NLS}-4\pi^2n^2)_n\) 的有界解析性。不是把其 defocusing 实型替代原 DLW 实型。

取该 complex zero-neighborhood 中半径 \(r_*>0\) 的小球。原中央背景 \(I_0^*=-L^2S^2/4\) 需满足 \(|I_0^*|<r_*/2\)，且
\[
\sum_{n\ne0}\langle n\rangle^2|J_n|+
|\rho(J)-I_0^*|<r_*/2.
\]
原负中央 action 在这种额外 small-background 条件下合法进入 complex extension。没有主张一个数值明确的半径，也不以旧 mixed 阈值自动代替它。

(4) 于是给
\[
\boxed{\ \Omega_{H,n}=-k_n^2-2i\widetilde\eta(J)k_n+r_n(J),
\quad r:\ell^{1,2}\supset\mathcal V\to\ell^\infty\text{ analytic}.\ }
\tag{5}
\]
实际原实结构给 \(\eta\in\mathbb R\)、\(r_{-n}=\overline{r_n}\)。该输入供应 Gaussian 原时间 phase 的频率条件；它没有供应一般 M 的 action 逆或旧 strong 域全部高阶流。
