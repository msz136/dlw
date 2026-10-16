# 冻结协议：共同物理态上的空间误差源分解

2026-10-13。使用 `dlw_three_tracks_20261013/shared/solver_cells.json` 冻结的论文 SD/FD 求解器。固定网格 `d1` 是二阶中心一阶差分，`d2` 是独立的三点二阶差分；不是四阶模板，也不是 `d1 @ d1`。

## 比较对象

在同一连续 Gram 参考的物理状态 `p=delta_-u,v` 及相同 t 上，分别评估：

1. 精确 x 导数的半离散物理 RHS；
2. x 两端使用真实连续参考外延值的同一中心差分 RHS；
3. 原求解器的周期 x stencil RHS。

三者同用原 y 闭合。精确时间导数由 tau 指数率的 cumulant 公式获得。物理 SD 导数包括 `v_t=w_t+delta0(u_t)`；下边界导数来自参考，上 ghost 导数包含误差外推导数。

定义 `y_model=F_analytic-zdot_ref`、`x_stencil=F_extended-F_analytic`、`x_wrap=F_periodic-F_extended`。三项之和严格等于实际 RHS 残差。y_model 包括原 prescribed y 闭合，不能称为无边界 PDE 的纯 y 局部截断误差。

## 冻结实验矩阵

- A、C 原参数，t=0,0.005,0.01，h=dx=0.1。
- 在 t=0 独立扫描 h=0.2,0.1,0.05,0.025（dx=0.1），以及 dx=0.2,0.1,0.05,0.025（h=0.1）；C 的 0.025 层仅在内存允许时运行。
- 固定 h=dx=0.1，将 x/y buffer 扩为原值 +5/+10，分开改变，检验 y 闭合及 x wrap 对内观察窗的贡献。
- 观察窗保持论文原 eval_half/eval_yhalf；同时记录全域与观察窗 L-infinity、RMS。
- SD−FD 的 p 差拆成显式 h² 非线性通量项 N 和 y 重构项 G；v 差拆成 FD 兼容性项 C 与上述 p 差经物理恢复产生的项。报告项范数与抵消，不由瞬时残差单独推断终态误差。

## 验证

精确 jets 与原 uv 输出对照；x/t 导数用中心差商多步长独立核验；共同物理 RHS 与原 native RHS+精确输出映射导数对照；三源和及 SD−FD 代数恒等式逐例核验。所有输出保留原始 CSV/JSON，接口可供其他实验沿时间传播。
