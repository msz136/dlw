# 连续 Gram 起点与一致二阶极限：证明结构

本文解释 C22、C23 的关键中间结论。是否已经验收，以 [机器状态](status.json)、[完整入口证据](INTEGRATION_STATUS.md) 和根目录 [独立 Lean 页面](../../../lean_verification.html) 为准。冻结的起点、终点和假设均保持原样。

## C23：连续 Gram 确实满足连续双线性对

1. 保留连续的 y 指数流，在整数层因子 γ 中引入辅助参数 s。借助 det(I+UV)=det(I+VU)，把列上的 y 权重转到行振幅；随后直接调用已证明的任意 N 双线性链 C07。由此得到所有合法 s 下的 Bₛ(Fₛ,G)=0。
2. 取 s(e)=a+h₀e/(1+e²)。其值始终落在合法参数区间，s(0)=a，s′(0)=h₀。因此不会为了求导而额外假设原始数据有更大的无奇点区域。
3. 对实际 γ 因子求导，再对实际行列式求导，得到 ∂ₑFₛ|₀=−h₀∂ᵧτ₁；G 与 e 无关。这里的偏导均为 Mathlib 的真实导数。
4. 在 Bₐ(Fₛ,G)=−2(s−a)Dₓ(Fₛ,G) 中对 e 求导，约去 h₀>0，得到 Bₐ(∂ᵧτ₁,τ₀)=2Dₓ(τ₁,τ₀)。另一方面，对 Bₐ(τ₁,τ₀)=0 求 y 导数，得到两项之和为零。两式相减即冻结的第二条 ContinuousPair 方程。

对应模块：`PkgContinuousGram` → `PkgContinuousGramCurve` → `PkgC23Complete`。该证明适用于冻结 PositiveData 中任意 N，不使用原论文结论作为公理。

## C22：在固定物理盒中统一控制误差

记 Pᵢ=pᵢ−a、Qᵢ=qᵢ+a。PositiveData 保证 Pᵢ<0、Qᵢ>0，并提供有限步长合法区间。

1. 将 log λₕ(P)/h 在 h=0 的可去奇点填为 1/P。用解析差商证明该延拓在零点解析，并且关于 h 为偶函数；不是只证明一个数值极限。
2. 通过 det(I+UV)=det(I+VU) 将插值 τ 改写为行权重形式。G 的权重为 ρᵢexp(y rᵢ(h))；F 的权重为 ρᵢexp(y rᵢ(h)+aᵢ(h))，其中

   rᵢ(h)=extendedRate(Pᵢ,h)+extendedRate(Qᵢ,h)，

   aᵢ(h)=[log(−Pᵢ−h/2)+log(−Pᵢ+h/2)−log(Qᵢ−h/2)−log(Qᵢ+h/2)]/2。

   这两组权重都关于 h 偶对称。严格证明它们在 0<h≤h₀ 时等于冻结的 tauI，并在 h=0 时等于冻结的 tau0。F 的半格位移是该偶对称性的必要组成部分。
3. 行权重始终为正，Cauchy 主子式定理给出延拓 τ 的严格正性。有限行列式、指数、对数及实际偏导因而在每个 (0,x,y,t) 附近联合解析。
4. 令 Aₕ=∂ₓlog Fₕ、Bₕ=∂ₓlog Gₕ。实际 u 插值严格等于

   Uₕ(y)=2Aₕ(y)−Bₕ(y−h/2)−Bₕ(y+h/2)。

   U 为 h 的偶函数，其零点值恰为连续 cu；因此一阶误差导数为零。
5. 为避免直接对 1/h 求导，将实际 v 乘以 h，分子恰为

   Jₕ(y)=Aₕ(y+h)−Aₕ(y−h)+(7/2)[Bₕ(y+h/2)−Bₕ(y−h/2)]−(1/2)[Bₕ(y+3h/2)−Bₕ(y−3h/2)]。

   J 是 h 的奇函数，J₀=J″₀=0；实际链式法则给出 J′₀=2∂ᵧ(A₀+B₀)。混合偏导交换将其识别为冻结的 cv。因此 Jₕ−h·cv 的零、一、二阶导数都为零。
6. 对每个固定盒 K=[−R,R]³，用紧性从逐点解析邻域取得共同步长区间；最高阶导数在紧集 [0,ε]×K 上有统一上界。重复中值定理得到 Uₕ−cu 的一致 O(h²) 界，以及 Jₕ−h·cv 的一致 O(h³) 界。最后在 h>0 下除以 h，得到 v 的一致 O(h²) 界。

通用工具是 `PkgUniformTaylor`、`PkgUniformAnalytic`、`PkgAnalyticJets`、`PkgCenteredFamily`、`PkgCenteredUniform`；Gram 的实际公式由 `PkgGramRateExtension`、`PkgGramInterpolation`、`PkgGramInterpolationBridge`、`PkgGramExtensionBridge`、`PkgGramExtensionAnalytic` 接入，最终导出名为 `c22_proved : C22`。

## 可以据此担保的范围

C22 针对固定正则 Gram 数据、任意固定有界物理区域，常数允许依赖数据和区域，但不依赖趋零的 h。这是精确解族的收敛结论，不是任意初值的数值求解器收敛定理。C23 与 C02 接通连续 Gram 到连续非线性 DLW 的前向链。浮点程序、舍入误差、求解器散射和非线性长期稳定仍须分别立项验收。
