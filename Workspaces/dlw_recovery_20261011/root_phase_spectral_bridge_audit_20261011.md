# 根复核：同一强相域的实际谱 Hamilton 时间

2026-10-11。实读 mixed 主稿 §§16–17、谱稿 §§12–15、`spectral_m2_strong_domain_flow_bridge.md` 全文以及两份实际谱独立审稿。以下是根任务的复核判断，未重跑旧机器证书。

## 窗口和拓扑

强域规定旧坐标的正复内窗口在任意后续前缀中保留；这是桥的必要假设。固定旧 plot 的紧参数盒后，第 j 轴可以选一次正小窗，使新增共同轨道在全部旧紧复 box 上的 H¹ 改变量小于 ρ2⁻ʲ。紧性只用于一个有限前缀，不要求可数乘积紧。冻结各旧轴，求和给所有有限前缀的同一低阶球，因此固定谱场的低阶 Banach 流提供统一正谱时间。

谱场与每个局部 Cₙ 的实际对合来自真实 C¹ 渐近；constant J 的 Hamilton 恒等式给 smooth 场上的 commutator 为零。谱流 order zero，在足够高的有限 Sobolev 层中，推前差满足零初值的谱场变分 ODE，故它输送已存在的 Cₙ 共同轨道。这里没有需要原 Cₙ 的 Cauchy 开流。

桥 §5 不是直接将 ambient 值称为 strong plot：对固定谱参数紧盒逐轴重取 mixed 角点。每个有限前缀给 Fréchet 紧的光滑角点族；选一次正 mixed 窗和源 margin，以 mixed 收缩唯一性识别原输送轨道。旧复轴域已经存在，新增层可以更短；不把谱参数盒逐层缩至零。这个过程给真正同类相容 presentation。根复核支持该推导在所规定 strong 域中的结论，不扩大到任意实 coherent 族。

内部 ω 使用明确的 ambient cross pairing。内部切向注入与同基点密度给弱非退化；谱参数曲线现在是实际 admitted plot，故其物理速度确实是内部 Hamilton 速度，而非仅一个 ambient 形式身份。

## 同点谱块独立

谱稿式 (97) 可由 det N=1 直接复核：double point 的 first Born 矩阵为 off diagonal (b,c)，二阶 trace 为 bc，所以判别式二次系数 4bc；背景判别式的 ζ² 系数为 L²γ²。由此 g₂=−4bc/(L²γ²)，配合原 canonical 权重 K=Lk²γ/(16S)，准确为 −k²QP/(4SLγ)。这是二次齐次项，Hessian 要乘 2。

复合到 mixed §17 同一个 H 参数图时，Dg(0)=0，因而 D²F 的额外链式项消失。DF(0) 包含全部有限 Fourier 方向，足够构造每个有限 gap Jacobian 的非零见证；在同一参数球中作可数 Baire 交，给同一状态全有限块独立与每个 gₙ≠0。没有用不同 N 的不同状态替代同点结论。

## 保留的界线

固定 normalized trace 及未扣 holonomy 的固定 center/gap 是 order zero。重整 center 另含真实空间平移，不在任意 Hˢ 点声称低阶可微。谱场界不被宣称全频统一，也不定义无限多个非零时间同时流。

共同水平集的内部切映射目前只给像包含于共同微分核，未证注入或等号；全相域排 ghost 的延拓不保证留在水平集。强域的 D 拓扑也未证等于 ambient 子空间拓扑。上述流接合、同点独立和开 gap，仍不能替代 norming/inverse、非线性最大各向同性或正规 Liouville 积分叶。
