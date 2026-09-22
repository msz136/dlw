# RUN_CONTEXT — DLW 沿 y 方向八类离散化方法并行研究

- 运行目录：`expression_glm-5.3-flash_20260917_225005`
- 主 Agent 模型：glm-5.3-flash（系统提示声明；slug 原样，无非法字符）
- 开始时间：2026-09-17 22:50；Lean 验证入口确认：2026-09-17 23:2x
- 平台：Windows / PowerShell 5.1；Python 3.13.3 + SymPy 1.13.3

## 环境与验证入口（按用户指令，统一使用共享环境，不另搭建）

- Lean 4.34.0 + Mathlib v4.34.0（commit 5ed2965256430c3649e86755f9576b54eca72435），`_lean_shared\HEALTHCHECK.json` 状态 PASSED
- 唯一验证入口：`C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1 -Root <proofRoot> -File <proofFile>`
- 各方向使用独立 proofRoot（各方向目录下 `proofs\`），`import Common.Operators` 对应 `<proofRoot>\Common\Operators.lean`
- 禁止：lake/elan 安装类命令、修改 `_lean_shared` / `lean-toda` / 其他模型目录、新增 axiom、sorry
- 结果写入 `<proofRoot>\.lean-runs\<编号>\result.json`；返回码 0 且 PASSED 才算通过
- 关键定理附 `#print axioms`，记录公理依赖

## 参考材料（只读）

- `PhysD-published.pdf`：Sheng & Yu, Physica D 432 (2022) 133140, DOI 10.1016/j.physd.2021.133140
- `hirota-book-new.pdf`、`2 Huner Saxton.pdf`
- `lean-toda\`（已有推导与旧 Lean 模块，只读参考）
- `tmp\PhysD.txt`（论文提取文本，行号引用见下）
- 他人运行目录（不修改）：`expression_deepseek-v4-flash_20260917_220258`、`expression_deepseek-v4.1-flash_20260917_222927`、`expression_union-alpha_20260917_221034`

## 主 Agent 已核对的论文公式（`tmp/PhysD.txt` 行号）

- (1)：`u_yt + v_xx + u u_xy + u_x u_y + 2a u_xy = 0`（行 81）
- (2)：`v_t + (uv)_x + u_xxy + 2a v_x + 2λ u_x = 0`（行 82）
- (5)：`u = 2(ln(f/g))_x`，`v = 2(ln fg)_{xy}`（行 116）
- (6)：`[D_y(D_x²+D_t+2aD_x) + 2λD_x] f·g = 0`（行 121）；(7)：`B f·g = 0`，`B = D_x²+D_t+2aD_x`（行 122）
- λ = −2（行 134；与 (9) 中 −4D_x1 一致）
- modified KP (9)-(10)、Gram 行列式解 τ_n = det(m_ij)（行 136-164；Lemma 2.1 引用 [41]）
- 行列式元素 (13)-(15) 及 p̃/q̃ 形式 (22)-(26)（行 241-261）；(25)(26)：ξ_i = p̃_i x − (p̃_i+a)² t + y/p̃_i + ξ_i0 等

## 研究假设（首轮约定）

1. 只离散 y；x、t 保持连续。进一步离散 x/t 必须单独标注层次。
2. 首轮 λ = −2，保留任意 a；其他参数约化须在报告说明。
3. 非线性改写 `w = u_y`：
   - `w_t + ∂_x[v_x + (u+2a)w] = 0` ⇔ (1)
   - `v_t + ∂_x[(u+2a)v + w_x + 2λu] = 0` ⇔ (2)
   （主 Agent SymPy 核对，见 `experiments\verify_wform_lin.py`）
4. 常数背景线性化（扰动 `e^{st+i(kx+ℓy)}`，ℓ≠0）：
   `[s+i(u0+2a)k]² = k⁴ − (v0+2λ)k³/ℓ`；高频 |s|~k² 增长。
   该障碍不因隐式/守恒/有限元/辛方法消失，所有方向必须正视。
5. 既有交错 tau 系统（独立审查，不当已完成证明，不做新颖性断言）：
   `(B−hD_x)F_j·G_j = 0`，`(B+hD_x)F_j·G_{j+1} = 0`，G_j 在 y=jh，F_j 在 y=(j+½)h；
   参考 `common\REFERENCE_staggered_construction.md`（lean-toda 原文副本）。

## 主 Agent 独立验证记录（2026-09-17 23:2x–23:5x，SymPy 精确/符号计算）

| 编号 | 结论 | 等级 | 脚本 |
|---|---|---|---|
| M1 | (1)(2) ⇔ w=u_y 改写（两式） | 符号恒等（假设混合偏导相等，光滑 u） | `experiments\verify_wform_lin.py` |
| M2 | 线性化：eq1 `iℓsU−k²V−(u0+2a)kℓU=0`，eq2 `(s+i(u0+2a)k)V+ik(v0+2λ−kℓ)U=0` | 符号恒等 | `experiments\verify_linearization.py` |
| M3 | 色散 `[s+i(u0+2a)k]² = k⁴−(v0+2λ)k³/ℓ`（ℓ≠0） | 符号恒等 + 数值 1e-15 | 同上 |
| M4 | 高频 `s/k² → ±1`（ℓ 固定）：连续问题沿 y 强不适定 | 符号极限 | 同上 |
| M5 | 交错系统 N=1 色散：`r1=−(P+d)/(Q−d)`，`ρ1=(P+d)(Q+d)/((P−d)(Q−d))`，d=h/2，P=p−a，Q=q+a | 符号恒等（一般参数） | `experiments\verify_staggered.py` |
| M6 | 交错系统二孤子（一般参数）：两方程所有指数系数为零 | 实验验证（6 组精确随机有理点；一般参数的 Lean 证明归 G 方向） | 同上 |
| M7 | 连续二孤子（论文 (11)(13)-(15)，c=1，λ=−2）满足 (6)(7) | 实验验证（6 组精确随机有理点） | `experiments\verify_continuous_2soliton.py` |

注：M6/M7 的随机点检验是 Schwartz–Zippel 式实验证书，不是一般参数证明；一般参数代数证明由 G 方向在 Lean 中完成（先清分母成多项式恒等式）。

## Lean 共享模块规划

- 规范源：`lean\Common\Operators.lean`（主 Agent 维护并测试）
- 各方向 proofRoot：`<方向目录>\proofs\`，内含 `Common\Operators.lean` 副本
- 入口命令示例（方向 A）：
  `& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' -Root 'C:\Users\msz\学术内容\Workspaces\expression_glm-5.3-flash_20260917_225005\A_finite_difference\proofs' -File '...\A_finite_difference\proofs\Main.lean'`

## 目录职责与隔离

- `common\`：共享数学规格 `SHARED_MATH_SPEC.md`、交错构造参考副本（主 Agent 维护）
- `A_...\`…`H_...\`：八个方向独立目录；每方向一个独立 proofRoot `proofs\`
- `lean\`：主 Agent 规范与共享 `Common\Operators.lean` 源
- `experiments\`、`reports\`：主 Agent 实验与最终报告
- Sub Agent 只写自己的目录；需要共享的变更交主 Agent 整合
