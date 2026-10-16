# Strong coherent 相域的拓扑、内部切向与水平集范围

2026-10-11。独立复核 `mixed_independent_review_20261011.md` §16–17 的数学结构。该补充不修改已同步主稿，不改变其弱辛证明；明确不能从该证明自动推出的其他拓扑与积分叶结论。辅助代理亦独立核对以下表述。

设 \(E\) 为固定均值叶上的周期光滑场空间，配备 Sobolev 半范数生成的 Fréchet 拓扑。真实 strong coherent 域 \(\mathfrak S_\infty\subset E\) 配备主稿规定的 strong plots；所有这些 plots 都光滑地映入 \(E\)。它的 D-topology 为全部 plots 定义的终拓扑，因此

\[
\tau_E|_{\mathfrak S_\infty}\subseteq\tau_D.
\]

尚未证明两种拓扑相等。主稿的域及切向稠密性均指 ambient Fréchet 拓扑；§17 的 Baire 使用 Hilbert 参数 norm topology，不自动给整个相域的 D-topological residual 性。

内部切空间 \(T_z^{\rm int}\mathfrak S_\infty\) 是 pointed plot germs 的切空间形成的**代数向量空间 colimit**，没有预设完备拓扑、局部平凡切丛或普通 manifold 坐标。共同坐标轴延拓使任意有限组切向能够在一个 plot 中同时实现；主稿抛物线延拓排除物理速度为零的 ghost，故 inclusion 导出的

\[
j_*:T_z^{\rm int}\mathfrak S_\infty\longrightarrow E
\]

单射，且其像在 ambient 切空间中稠密。这个像尚未证明等于 \(E\)。

主稿闭二形式是 ambient 弱辛形式沿每个 plot 的拉回，内部配对应明确为

\[
\omega_z(v,w)=\Omega_{E,z}(j_*v,j_*w).
\]

这个公式与切向代表无关。共同坐标轴延拓使任意两切向的配对也可在同一 plot 中实现；不能把一般 diffeological 二形式当作自动提供不同 plots 内部切向间交叉配对的对象。由 \(j_*\) 注入、像稠密、ambient 形式连续弱非退化，这个明确内部配对弱非退化。闭性成立于每个 plot 上。该结论不包含强辛同构或普通切丛局部平凡性。

共同 charge 水平集

\[
Y_c=\{z\in\mathfrak S_\infty:I_\nu(z)=c_\nu\}
\]

取 inherited subset diffeology。真实有限支持交换流保持这些水平集，但目前没有证明它们是正规积分叶、子流形、coisotropic leaf 或局部纤维丛。内部切向只具有

\[
\operatorname{im}\bigl(T_z^{\rm int}Y_c\longrightarrow T_z^{\rm int}\mathfrak S_\infty\bigr)
\subseteq\bigcap_\nu\ker dI_\nu(z).
\]

此映射的单射性与包含的等号都需另证：主稿在整个相域中排 ghost 的二维延拓可能离开水平集，不能移植到 \(Y_c\)。水平集自身 D-topology 也可能比从相域 D-topology 继承的子空间拓扑更细；限制二形式不自动弱非退化。一些有限参数 plots 上的 charge Jacobian 满秩不等于相域为 manifold 或 charge map 为 submersion。
