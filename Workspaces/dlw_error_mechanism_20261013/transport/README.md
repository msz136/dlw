# 共同物理态中的误差源与传播

结论入口：`FINDINGS.md`。冻结设计：`PROTOCOL.md`。C 的缓存及时间步控制：`CACHE_PROTOCOL.md`，独立接口审阅：`CACHE_REVIEW.md`。

## 可复查汇总

- `analysis_validation.json`：逐场闭合、方法差闭合、时间步控制和四格归因总表。
- `independent_closure.csv`：独立预测与真实误差场、三源之和与真实误差场、SD−FD 方法差的相对残差。
- `cross_source_attribution.csv`：行=传播器，列=源的四格 RMS；对称交换顺序归因同时报告标量范数差和场差投影两种指标。二者的百分数不能混称。
- `transported_source_budget.csv`：y 源、x 模板源与 x 包装源分别传播后的逐场 RMS；y/x 余弦；误差能量中的自身项及交叉项。
- `time_refinement_validation.csv`：A .04 的 dt 对半；C .002 的粗/细步实际场、四格场及分项；C .01 粗步与原归档末态。

这些文件由 `summarize_transport.py` 从保存的误差场直接重算。未完成运行不纳入完整终态结论。

## 完整试验目录

- `A_T0.010_dt0.000100_parts`：原时间步、三源精确逐阶段评估、四格输运及 λ=.5/1 源幅值干预。
- `A_T0.040_dt0.000100`：四格输运延长时间，不计算三源细拆。
- `A_T0.040_dt0.000050`：上一试验半时间步。
- `C_T0.010_dt0.000500_parts_cache5`：三源缓存插值、四格输运；与原时间步末态归档校验。

每个完整目录包含 `validation.json`、逐时间 `timeseries.csv`/`comparison.csv`/`sources.csv`，必要时另有 `source_budget.csv`/`intervention.csv`。`frame_*.npz` 为物理观察窗的双精度误差场，`final_common.npz` 为完整计算域共同态。

## 保留的部分运行

- `C_T0.010_dt0.000100_parts`：最初全精确源运行因会话中断停止，只有前段帧，不能用作终态结论。
- `C_T0.010_dt0.000100_parts_cache5`：20步、t=.002 完整 checkpoint；为粗步早期独立控制及必要恢复保留。不是已完成 T=.01 结果。

缓存的五个源节点及四个中点留出值保存在 `independent_source_cache`。初次过严统一阈值诊断保留于 `C_cache5.stderr.log`；修订接受条件和理由明确列于补充协议。

## 共同口径

物理误差场的 axis 0 为 u,v。joint RMS 定义为 sqrt(mean(u²)+mean(v²))，不再除以2。所有场在原论文 native 观察点上比较。源残差、实际误差与反事实预测均使用相同 y 边界重构。SD 是论文 PE 路线的代码名称；这里的实验不能单独隔离抽象可积性。
