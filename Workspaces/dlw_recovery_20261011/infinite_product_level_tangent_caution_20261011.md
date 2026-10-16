# 无限 Cartesian action 水平集：微分核与真实曲线切向

2026-10-11，根复核。此小例用于明确 nonlinear 谱闭包证明的几何范围。它是复序列空间上的准确障碍，不把未校准的标准 NLS 实型当作原 DLW 实型。

令 s=∩_{N≥0}h^N 是快速下降序列的 Fréchet 空间，action map 为 I_n=w_n z_n。在状态 w_n=z_n=e^{-n²}，所有 actions 均非零；方向 v_n=(e^{-n},−e^{-n}) 属 s²，并满足每个 dI_n(v)=0。因此 v 属全部 action 微分的共同核。

若存在 s² 中 C² 曲线 (w(t),z(t))，保持所有 I_n 且在 t=0 的速度为 v，逐坐标二阶微分强制

\[
e^{-n²}(w_n''(0)+z_n''(0))=2e^{-2n},\qquad
w_n''(0)+z_n''(0)=2e^{n²-2n}.
\]

右侧甚至不属于 ℓ²，与 C² 曲线矛盾。所以全部 actions 非零，也不足以使真实 fiber 曲线切向等于 action 微分核，或使这个 fiber 自动成为 ambient Fréchet regular submanifold。有限坐标投影的相位方向则是真实 fiber 速度，且投影在每个 h^N 中趋于 v。

因此正确可证的目标可以是：在指定 topology 中，实际有限 Hamilton 轨道速度的闭包等于共同微分核；这不自动给未取闭包的 fiber 内部切向等号。对于 DLW 的 strong diffeology，还要保留其同一相域、内部切向定义及 fiber ghost 的独立问题。此例不否定该闭包最大性路线，反而说明为何应准确区分这两种结论。
