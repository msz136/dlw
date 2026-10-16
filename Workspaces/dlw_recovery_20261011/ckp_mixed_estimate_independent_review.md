# 三阶 constrained-KP 混合存在估计：独立复核

2026-10-11。实际读取 `刘维尔可积性/research/singular_ckp_actual_mixed_flow_20261011.md` §1、§3–4。这里只核验其解析混合固定点，不替代有理坐标逆、Floquet 因子图或原物理 Hamiltonian 证明。

## 1. 范围与方程

设 \(M\ge3\)、\(n=M-3\)、固定实 \(\mu_i\)。周期变量满足

\[
\Psi_t=-\frac i{\sqrt3}\Psi_{xx}
+\frac23uu_x-2D\sum_i f_i g_i,
\qquad u=m_0+2\sqrt3D^{-1}\Im\Psi,
\]

\[
f_{i,t}=-(D+\mu_i)^2f_i-\frac23u f_i,
\qquad g_{i,t}=(D-\mu_i)^2g_i+\frac23u g_i.
\]

要求 \(\overline{\Im\Psi(0)}=0\)；输入为 \(\Psi(0),f_i(T),g_i(0)\)。\(f_i,g_i\) 是独立实变量。恢复 \(\phi_i=e^{\mu_i x}f_i\)、\(\psi_i=e^{-\mu_i x}g_i\) 时 twist 在 \(\phi_i\psi_i=f_i g_i\) 中消去。不能设 \(\psi=\overline\phi\)：两热方向相反，该条件一般不保持。

原稿式 (10) 的 Schrödinger 项与 \(2uu_x/3\) 项之间曾缺一个排版加号；已通知作者。正确方程如上。

## 2. 统一热能量及正确的时间方向

令 \(s>1/2\)、\(0<T\le1\)。周期前向算子 \((D\pm\mu)^2\) 的 Fourier 符号是

\[
-k^2\pm2i\mu k+\mu^2.
\]

对 \(h_t=(D\pm\mu)^2h+F\)，\(H^s\) 能量与 \(H^{s-1}\)—\(H^{s+1}\) 对偶、Young 不等式给

\[
\frac d{dt}\|h\|_{H^s}^2+\|h\|_{H^{s+1}}^2
\le C_\mu\|h\|_{H^s}^2+C\|F\|_{H^{s-1}}^2.
\]

积分并 Gronwall，得一致于 \(0<T\le1\) 的

\[
\|h\|_{C_tH^s}+\|h\|_{L_t^2H^{s+1}}
\le C_\mu(\|h(0)\|_{H^s}+\|F\|_{L_t^2H^{s-1}}).
\]

\(g\) 使用此始端估计；\(f\) 以 \(\tau=T-t\) 反转后使用相同前向估计及指定末端 \(f(T)\)。没有把反向热当成 Cauchy 初值问题。固定复 \(\mu\) 时也有 sectorial 估计，但实物理约束需要另行成对处理；本核验采用原稿明确的实 twists。

## 3. Schrödinger forcing 恰由热的一阶积分增益控制

令 \(B_T^s=C_tH^s\cap L_t^2H^{s+1}\)。一维 \(H^s\) 代数性质给

\[
\|D(fg)\|_{H^s}
\le C_s(\|f\|_{H^{s+1}}\|g\|_{H^s}
          +\|f\|_{H^s}\|g\|_{H^{s+1}}).
\]

时间 Cauchy–Schwarz 因而给

\[
\|D(fg)\|_{L_t^1H^s}
\le C_s\sqrt T\,\|f\|_{B_T^s}\|g\|_{B_T^s}.
\]

Schrödinger 群 \(e^{-itD^2/\sqrt3}\) 在 \(H^s\) 酉，故其 mild forcing 只需此 \(L_t^1H^s\)。不能只用 \(C_tH^s\) 声称 \(D(fg)\in L_t^1H^s\)；\(L_t^2H^{s+1}\) 正是补齐该一阶导数的项。

又 \(u\in C_tH^{s+1}\)，并有

\[
\|uu_x\|_{L_t^1H^s}
\le C_sT(|m_0|+\|\Psi\|_{C_tH^s})\|\Psi\|_{C_tH^s},
\]

\[
\|u f\|_{L_t^2H^{s-1}}
\le C_s\sqrt T(|m_0|+\|\Psi\|_{C_tH^s})\|f\|_{C_tH^s}.
\]

热 forcing 只需 \(L_t^2H^{s-1}\)，无需强行要求它带一个额外导数。

## 4. 固定点、实约束与同窗光滑持久性

在

\[
C_tH^s(\Psi)\times(B_T^s)^{2n}
\]

的固定数据球上，上述双线性估计及其差分给 mixed Duhamel 映射的 Lipschitz 常数 \(C_R(T+\sqrt T)\)。小 \(T>0\) 使其严格收缩并保持球，得唯一实际 mild 解及低 Banach 层的实解析数据依赖。\(n=0\) 时直接删去热对。

\(f,g\) 始终实，非线性 Schrödinger forcing 因而实值；空间积分及周期导数给 \(\overline{\Im\Psi}=0\)、\(\overline{\Re\Psi}\) 保持。于是周期 \(D^{-1}\) 合法，\(u,z=\Re\Psi\) 是实变量。含 \(\Re,\Im\) 的方程为 real-analytic；若需要 holomorphic 复化，应复化独立实状态，不能把复共轭误当成 holomorphic 运算。

全部周期方程、\(D^{-1}\)、固定 \(\mu_i\) 与空间平移交换。唯一低阶图 \(\mathcal S\) 故满足 \(\mathcal S(T_hb)=T_h\mathcal S(b)\)。对 smooth 数据的平移轨道反复微分，得

\[
D_x^q\mathcal S(b)
=\sum_{\sum i_\nu=q}c_{\mathbf i}
D^k\mathcal S(b)[D_x^{i_1}b,\ldots,D_x^{i_k}b].
\]

这些量属于原来的同一 Banach 轨道空间，平移生成元判据给任意空间阶持久性；方程再给全部时间导数。此过程保留首次选定的同一正 \(T\)，无需随高阶不断缩窗。

结论：所列混合存在估计及同窗光滑持久性成立。物理最小有理因子图的可逆性和图保持是另一步；不能由本解析估计自动声称任意物理初态的 Cauchy 流或 Liouville 完备性。
