# AGENTS.md — 工作区索引与进度

> **2026-09-22（最新完整验收，优先于下方历史记录）：32 / 32 个冻结 Lean 目标全部完成。** `Main.lean` → **PASSED: 39 local module(s)**，退出码 0，run `20260922_221626_2fd722e0`。最后补齐 C22（实际 Gram 物理场的紧盒一致二阶极限）和 C23（任意 N 连续 Gram 双线性对）。全部终点仅依赖 `propext / Classical.choice / Quot.sound`；两个 Contracts 哈希不变，完整导入链源码哈希逐一核对。
> 独立页面 [lean_verification.html](lean_verification.html)、[衔接验收](Paper/dlw_semidiscrete/lean_contracts/INTEGRATION_STATUS.md)、[机器状态](Paper/dlw_semidiscrete/lean_contracts/status.json)、[C22/C23 关键证明](Paper/dlw_semidiscrete/lean_contracts/C22_C23_PROOF_NOTES.md) 已同步。数值部分保持此前 40 项回归 + 17 项产物检查和 E2/E3 六组自收敛的验收。**完成范围为 C01–C25、N01–N07；并不包含一般反向重构、IST、浮点求解器认证、求解器散射或非线性长期稳定。** 冻结 `ContDiff ℝ ⊤` 表示解析阶 ω，不能解释为仅 C∞。下方旧的未完成计数保留作历史记录。

> **2026-09-22（主目录数值报告已同步）：** [numerical_analysis.html](numerical_analysis.html#results) 前部现展示最新 `numerics/REPORT.md` 全文结果、6 张实测表和 4 张图，含 E2/E3 六组时间自收敛；保留后部 GSG 方法与设计说明。`index.html` §11 已更新入口及执行状态。仅更新文档，没有重跑实验或修改 Lean。权威结果仍为 `Paper/dlw_semidiscrete/numerics/REPORT.md`；以后先运行 `python Paper/gsg_project/dlw_report/sync_numerical_results.py`，再按既有构建命令生成根目录 HTML。静态链接/图片/锚点检查通过，数值页 204 段、主报告 1233 段公式编译通过；记录见 `Paper/gsg_project/dlw_report/numerical_results_validation.json`。下方“HTML 未更新”的描述是历史记录。

> **2026-09-22（数值继续实施）：E2/E3 自身时间自收敛已补齐。** 两个 h（1/4、1/8）× Euler/RK4/梯形，固定 nx=256、T=0.05、相同初态与时变边界，n=4/8/16/32/64 共 30 次推进完成。比较相邻时间网格的 P/W/u/v，六组末级观测阶通过与 1/4/2 相差小于 0.35 的验收；原先“E2/E3 自身时间阶未测出”的记录已成为历史。真实末级阶见 [数值报告](Paper/dlw_semidiscrete/numerics/REPORT.md)，不能把有限观测当作阶数定理。日志与源码哈希 `out/e2_e3_self_convergence*.{txt,json}`；复现 `python -u run_all.py e2e3time`。最终 **40 项回归 + 17 项产物检查**。求解器散射、非线性长期稳定与程序级 Lean 认证仍未完成。

> **2026-09-22（Lean 继续实施，优先于下方旧完成数）：30 / 32 个冻结目标已证明。** `Main.lean` → **PASSED: 25 local module(s)**，退出码 0，run `20260922_212234_3a4b6e8e`。本轮闭合 N01（非线性含时间依赖 RK4）、C18（二阶非线性一致性），以及 C07/C08/C16（任意 N Gram 双线性链、有限 h 双线性对、非线性精确解）。C07 通过行列式微分、Plücker 恒等式与特征多项式有限根的连续延拓，**没有额外可逆性或 Reservoir 前提**。全部已验收目标仅依赖标准三个逻辑公理，冻结 Contracts 哈希不变。
> **仍未证明 2 项**：C22 紧盒一致二阶极限、C23 连续 Gram 双线性对；正在继续。独立页面 [lean_verification.html](lean_verification.html)、[衔接验收](Paper/dlw_semidiscrete/lean_contracts/INTEGRATION_STATUS.md)、[机器状态](Paper/dlw_semidiscrete/lean_contracts/status.json) 随真实检查同步。**正则性更正**：冻结 `ContDiff ℝ ⊤` 在当前 Mathlib 表示解析阶 ω，强于通常 C∞；不得把适用范围扩大到仅 C∞。

> **2026-09-22（四项数值复审修复已完成，优先于下方旧状态）：** 见 [Workspaces/numerics_review_20260922/RESOLUTION.md](Workspaces/numerics_review_20260922/RESOLUTION.md)。E6 采用实际开链零背景线性化，核对四阶符号、RHS 导数、本征模增长与形状，并区分谱估计/线性范数界/非线性稳定；回归直接运行当前源码；E1 修复 x 端点权重；E5 修复格点、初态与周期积分。E1/E6/E2E3/E5/E7 重跑成功，**40 项回归 + 13 项产物验收通过**。主报告 `Paper/dlw_semidiscrete/numerics/REPORT.md` 与 README、3 张图已同步；日志和哈希 `out/final_validation_manifest.json`。原始报告归档于复审工作区。**本条不等于所有研究任务完成**：E2/E3 自身时间自收敛、数值两孤子散射、非线性长期稳定仍未验收；用户现已授权继续补齐 Lean 证明并整合系统转换与数值证据，Lean 工作另行记录。

> **2026-09-22（修复后独立复审，优先于下方“全部验收”）：主要实现修复有效，整体仍有验收缺口。** 见 [Workspaces/numerics_review_20260922/RECHECK.md](Workspaces/numerics_review_20260922/RECHECK.md)。重跑现有回归全部 PASS，独立执行当前 E7 得时间阶 3.861→3.910→3.953；连续相位、逐级重构、梯形失败拒绝、二阶模板已修。剩余：E6 仍是固定格点相位的色散估计，未包含实际开链谱，扰动预测还误用二阶模板；E7 回归只检查 JSON 可读，不能防止旧 bug 回归；E1 x 端点求积权重不匹配；E5 新检测实际取 MID−1 却标 MID，且未从 t=0 计算漂移。**本轮仅复审，未改生产代码/实验输出；下方“六项全部修复并验收”应按此限定理解。** Lean 未复审。

> **2026-09-22（数值审查 → 已修复验收，优先于下方同日执行结论）：E0–E7 六项审查发现已全部修复并重跑验收。**
> 审查及独立复核见 [Workspaces/numerics_review_20260922/REVIEW.md](Workspaces/numerics_review_20260922/REVIEW.md)，同目录有 `review_probes.py` 与 `probe_results.json`。
> 已确认并已修：① `ContRef` 时间相位（现 `qv**2-pv**2`，`gramtau.py`），原"连续参照不是 DLW 解"归因**已撤回**——修正后解析残差 `≤6.3e-61`，连续参照就是解，O(1) 探针值是相位 bug；② E7 每级重构 `u`（`deriv()`），时间自收敛 `3.861→3.910→3.958` 近四阶，原"重构路线一阶瓶颈"归因**已撤回**；③ E1 固定窗口 L2（`y∈[-1.5,1.5]`），`E_∞`/`E₂` **都二阶**（旧 `E₂ 2.50` 是区域随 h 缩小的假象，**已撤回**）；④ E6 预算改按**离散谱** `g_max_discrete`（奈奎斯特模被 D1 精确消灭，连续 `k=π/dx` 估计约保守 5 倍），旧"溢出必然不是 bug"断言**已撤回**（无日志不可归因）；另修：梯形法不收敛拒绝时间步、order=2 差分系数补 `[(-1,-0.5),(1,0.5)]`。
> **验收**：`python -u experiments/check_regressions.py` → **24 项全部 PASS**；`python -u run_all.py` 9 阶段全 ok（日志 `numerics\out\run_all_log.txt`）；`REPORT.md`（§4/§6.1/§8.4/§9 两处【已撤回】/§11）、`README.md` 已按实测重写；`make_figures.py` 重出 3 图（fig1 `E₂` 参考线改 `O(h²)`，fig2 加连续估计对照曲线）。E7 曾在重跑中因初值 `U,V` 未定义失败一次，已补回并重跑通过。
> **边界仍在**：E4/E5 主要核验解析 Gram 场，不能替代求解器的散射/守恒验收（E5 已补求解器守恒 `1e-16`，§8.4）；E2/E3 对精确参照仍测不出时间阶（自收敛待补）。Lean 状态未重新审查或更改。下方执行记录保留作历史证据（其中 ②③④ 及两条边界的旧表述已被本横幅更正，行内已加【已更正】/【已撤回】标记）。

> **2026-09-22（最新）：DLW 半离散数值分析 E0–E7 已真实跑完，结果落在 `Paper\dlw_semidiscrete\numerics\`。**
> 专题报告 `numerical_analysis.html` 原先声明"尚未运行新的数值时间推进实验"；**本轮是第一次真实执行**，全部脚本新建在
> `Paper\dlw_semidiscrete\numerics\`，未安装任何新依赖，未改动工作区其它部分。主文档 **`numerics\REPORT.md`**；一屏汇总 `python -u summary.py`；全量复现 `python -u run_all.py`（约 20 分钟）。
> **四条实测结论**：
> ① **迁移成立**——纯格点 Gram τ 是闭合非线性系统 (N1)(N2) 的精确解，N=1,2 × h=1/4,1/8 残差 `~1e-6`（差商截断地板），逐项分解 `d_ut + d_Hx + d2 = 5.3e-8`；E0 精确双线性残差 `~1e-14`（float64）/ `~1e-60`（60 位 mpmath），而朴素差商残差 `O(1)` 且每减半 h 精确降 4 倍。
> ② **收敛阶与采样点**——【已更正 2026-09-22】E1 实测 `E_∞` 斜率 `1.9958→1.9994`、`E₂` 斜率 `2.0011→2.0000`（**两者都是二阶**；旧记的 `E₂ 斜率 2.50` 是 L2 积分区域随 h 缩小造成的假象，固定窗口 `y∈[-1.5,1.5]` 后消失，见 `numerics\REPORT.md` §4【已撤回】）；采样点必须是 F 位点 `y=(j+1/2)h`，改用 `jh` 或 `(j+1)h` 退化为**一阶**；非零时刻 `t=0.2/−0.35` 同为二阶。§4.3 两个展开式独立验证通过。
> ③ **相移与守恒**——E4 两个孤子**分别**测得相移 `0.900` 与 `0.350`，对预测 `log6/2=0.895880`、`log6/5=0.358352`；`A_12=1/6` 精确。E5 积分漂移 `~1e-15`、精确质量公式吻合 `2.4e-15`/`5.1e-14`、局部散度残差 `1.8e-3`/`7.4e-4`（**截断级，不是机器零**，符合 §6.3 的"不要预设机器零"）。
> ④ **硬限制已被量化**——E6 复现报告 §7 的 `Re σ ~ k²`（比值 → `1.000979`），因此**网格越细可用时间越短**。【已更正 2026-09-22】预算**必须按实际离散谱**（`g_max_discrete`）算：离散 `nx=128` 预算 `1.251`、`nx=1024` 剩 `2.42e-2`、`nx=2048` 剩 `6.17e-3`；旧引用的 `0.271 / 4.72e-3 / 1.19e-3` 是**连续 `k=π/dx` 估计**（约保守 5 倍，奈奎斯特模被 D1 精确消灭：`D1_action=0.0`）。【已撤回】旧文"第一次 E2/E3 在 `nx=1024, T=0.4` 上必然溢出，**是报告预言的性质，不是 bug**"——无运行日志可归因，不能断言溢出必然不是 bug（`REPORT.md` §6.1【已撤回】框）。
> **两条必须如实说明的边界（2026-09-22 复核后已改写）**：① **E2/E3 的时间阶数没对精确参照测出来**——空间误差主导，Euler/RK4/梯形都收敛到同一空间地板（`E_∞(u)≈1.945e-02`，对 dt 完全不敏感）；分离方法是**同网格时间自收敛**（E7 已示范得 `3.86→3.96` 近四阶，不需要高精度算术——旧说"要分离需更高精度算术"不准确），E2/E3 自身尚未做。② 【已撤回】旧记"`ContRef` 的 `(u⁰,v⁰)` 不是连续 DLW 的解（左端 O(1)：2.02/4.36，缺 O(h²) 首项）"——真因是时间相位 bug（`Q²−P²` 误作 `q²−p²`），修正后解析残差 `≤6.3e-61`，**连续参照就是 DLW 的解**；当前 `nx=256` 探针残差 `1.82e-2/1.26e-2` 是 **dx⁴ 差分截断地板**（nx 加密比值 →16，`probe_e7_offset.py`）。旧记"E7 时间收敛一阶（1.018→1.217），瓶颈在 `u_y` 推进+重构路线"——真因是 **RK 级漏更新 `u`**，修复后 `3.861→3.910→3.958` 近四阶（`REPORT.md` §9 两处【已撤回】框）。
> 排查用过的 13 个临时脚本已移入 `Trash\dlw_numerics_diagnostics_20260922\`（见 `Trash\README.md`）；**其中 `diag_lsq.py` 的输出因设计矩阵条件数 5838 而不可引用**。
> 产物：`out/*.json`（7 个实验）、`out/run_all_log.txt`、`figures/*.png`（3 张，由 `make_figures.py` 从 JSON 直接生成，图与数字不会脱节）。

> **2026-09-22：32 个新命题开始落地，24 项已由标准入口 PASSED（另 N01 部分完成）。** 证明根目录 `Workspaces\lean_contracts\proofs\`，
> 整合模块 `Main.lean`（导入 `Contracts` + 10 个证明包 + `Main` 自身 = 12 个本地模块，逐目标 `#print axioms`）。
> 命令：`& 'C:\Users\msz\aca\_lean_shared\Check-Lean.ps1' -Root 'C:\Users\msz\aca\Workspaces\lean_contracts\proofs' -File '...\Main.lean' -TimeoutSeconds 1500`
> → 退出码 0、`PASSED: 12 local module(s).`（run `20260922_125635_4e9e9d5e`）。全部 24 个目标 + 3 条 N01 部分引理都只依赖 `propext / Classical.choice / Quot.sound`，无 `sorryAx`、无新增公理。
> **已证明 24 项**：C01、C02、C03、C04、C05、C06、C10、C11、C12、C13、C14、C15、C17、C19、C20、C21、C24、C25、N02、N03、N04、N05、N06、N07。
> 证明包：`PkgTrivial.lean`（C03/C21/N02–N07）、`PkgGramEntry.lean`（C04/C05/C06/C10）、`PkgQuotientRate.lean`（C12/C13/C24）、`PkgContinuous.lean`（C01）、`PkgLattice.lean`（C19/C20/C25）、`PkgNumeric.lean`（N01 的两个合取项）、`PkgC11.lean`（C11）、`PkgNonlinear.lean`（C14/C15）、`PkgC02.lean`（C02）、`PkgC17.lean`（C17）。
> **N01 部分完成**：`n01_euler_part`（PowBound 2）与 `n01_trapezoid_part`（PowBound 3）假设与 N01 完全一致，已过；剩下 RK4（PowBound 5）已归约成单条已检查的命题 `n01_rk4_of_taylor_poly`（经典 RK4 阶条件），**未证明**，故**没有 `n01_proved` 声明**。
> **未证明 7 项**：C07、C08、C09、C16、C18、C22、C23（另有 N01 只完成 Euler 与梯形两个合取项）。按缺口分两类（读了 `Contracts.lean` 原文后分类，不是猜的）：
> **(a) 只差同一族机器**：C18 与已过的 C11/C17 同族（采样/一致性，都是 `PowBound 2`），是「格点算子 vs 连续算子」的 Taylor 展开，可直接复用 `PkgNumeric.lean` 的 `powBound_taylor_poly` 与 `PkgC11.lean`/`PkgC17.lean` 的 PowBound 组合器。**注意 C18 的 `n1` 那一支的第一阶修正必须靠 `y-h/2` 移位吸收**（`dm` 是后向差商、`mm` 是后向平均，两者各带 `−(h/2)∂_y`，正好与目标在 `y-h/2` 处取值抵消）；`n2` 那一支全是中心差分，不需要移位。这一条已用符号代数核对过。
> **(b) 需要研究级机器 —— 不能只靠"接线"**：C16、C22、C23 与 C07/C08/C09 属于同一类，都卡在**任意 N 的实际 Gram 双线性恒等式**上。具体地：C16 需要 `PositiveData D h → SemiPair D.a h (F D h) (G D h)`（`PkgNonlinear.lean` 的 C15 只提供了这条**最后一步**：`SemiPair ⇒ NonlinearPair`），C23 需要 `ContinuousPair D.a (tau0 D 1) (tau0 D 0)`（连续 N-孤子 τ 的双线性对），C22 还要在此之上叠 C17 的一致盒估计。而这条 Gram 双线性恒等式正是 README 里明说**不能挪用旧 `T2_discrete_pair_exact`** 的那一条（后者假设任意 `Reservoir Res`），需要 Cauchy–Binet 主子式展开 + Jacobi/Plücker + 指数线性无关。**上一版横幅曾把 C16 写成"只差把 C15 与 Gram 数据接起来"，此说不准确，已按契约原文更正。**
> **C02/C11/C14/C15 的实质更正与收获（可复用）**：① **C02**：乘子只有 ±1 —— `c1 = 2·∂ₓ∂ᵧR`、`c2 = 2·∂ₓ∂ᵧR − 2·∂ₓS`；早期记录里把第二条标量假设写成 `E2 = β_y(S_xx+(D_x)²+D_t+2aD_x)+2B_x` **是错的**（`β_y` 混用了 (x,t) 与 (x,y,t) 的对象），`PkgC02.lean` 的 docstring 已逐字写出正确的 (I)(II) 并把旧式标为 WRONG。精确恒等式是 `cdybil − 4·chx = sy(cbil a f g) − 2·(cbil a f (sy g) + 2·chx)`，所以 `E+2Bₓ=0` 是**推出来的**，不是假设。② **C11**：两个合取项其实共用同一次二阶 Taylor 展开（`Φ(s) = bil (a+s)(slice f y)(slice g (y+s))`），`bil` 的斜对称项在对称化中精确相消，因此**不需要**单独的 `bil` 有界性引理。③ **C14**：手推时容易在识别式 `normA − normC` 的最后两项符号上出错（正确为 `+ (2a)•lx V − h•lx U`）；`ring` 把 defeq 但写法不同的原子当不同对象，必须先用 `lxx/lx` 交换与移位引理把两侧规范化到同一批原子。
> **两处环境/接口障碍已排除并如实记录**：① `_lean_shared\runtime.json` 的 `workspace` 与 10 条 `lean_paths` 原指向迁移前 `C:\Users\msz\学术内容`，入口在编译前退出；
> 已只改路径重指向 `C:\Users\msz\aca`，备份 `runtime.json.bak_pre_aca_migration`，未动工具链/Mathlib 提交/任何数学。② `Contracts.lean` 里 `PowBound` 的 `0<|h|` 被词法器读成 `<|` 管道算子导致文件无法类型检查，
> 已提交**最小词法差异** `0 < |h|`（仅加空格），原字节备份 `Trash\lean_contracts_pre_syntax_fix_20260922\Contracts.lean.orig`（SHA-256 `40a624c2…`）；
> 冻结后的 `Contracts.lean` SHA-256 为 `e70876c538d52939b030e7813a6b1c60917a79e56e28b29146d22df8da98d656`，且证明目录里的同名文件与之逐字节相同。**起始/最终命题一字未改，无目标被削弱或重述。**
> **C07 已单独查清**：用 `fractions.Fraction`（无浮点）在 N=1..4、j=0..2、n=0..2、三组参数上按实际指数向量合并检验，全部合并系数精确为 `Fraction(0)`
> → **仅这些有限样例精确通过，不能推出任意 N 命题为真**；仍缺形式化机器（Cauchy–Binet 主子式展开 + Jacobi/Plücker 关系 + 指数线性无关），不是数学反例。脚本 `Workspaces\lean_contracts\audit_c07.py`。
> **三条 Lean 工程陷阱（本轮实际踩到）**：未标注类型的 `4 • x` 按 **ℕ** 标量乘法解析，须写 `(4 : ℝ) • x`；tactic 关闭目标后再接 tactic 会硬报错 `No goals to be solved`；
> `HasDerivAt.comp` 在内层函数点由元变量给出时高阶合一失败，改用 `HasDerivAt.comp_const_add` 最稳。
> 状态与证据：`Paper\dlw_semidiscrete\lean_contracts\status.json`；页面：根目录 `lean_verification.html`（由 `build_dashboard.py` 重新生成，已如实标出 23/32 与 N01 的部分状态）。

> **2026-09-22：新增独立 Lean 核验页。** 根目录 `lean_verification.html` 展示已有 Lean 证明的实际范围、7 个旧模块与 2026-09-19 PASSED 日志的源码哈希核对、32 个新命题（C01–C25 / N01–N07）、依赖关系、Agent 分工与数值验收边界。用户明确要求独立页面，**本轮未修改原 `index.html`、`numerical_analysis.html` 或它们的源文件**。
> 命题与共享定义：`Paper/dlw_semidiscrete/lean_contracts/Contracts.lean`；交接：同目录 `README.md`；状态与哈希：`status.json`；页面同步构建：`build_dashboard.py`。**新文件只定义 Prop，没有证明实现；32 项均待证明，不能把定义通过或旧辅助引理当作新端点通过。**
> 验证障碍：实际调用唯一标准 Lean 入口返回 1（尚未进入 Lean 编译），因 `_lean_shared/runtime.json` 的 workspace / 库路径仍指向迁移前 `C:\Users\msz\学术内容`。公共环境未改；新接口标记为“已审阅、待类型检查草案”。页面另已通过浏览器检查：32 个命题卡、筛选与折叠正常，11 段公式渲染无错误，链接/锚点有效，桌面与窄屏无页面溢出；记录见 `lean_contracts/page_validation.json`。旧日志与现有 7 个模块 SHA-256 全部吻合，只支持原 theorem type。尤其旧 `T2_discrete_pair_exact` 假设任意 `Reservoir Res`，不能替代 C07/C08 对实际 Gram 行列式的证明。

> **2026-09-22：GSG 数值方法迁移专题。** 当前项目已迁移到 `C:\Users\msz\aca`（旧 `学术内容` 路径为历史记录）。新增根目录 `numerical_analysis.html`：核对 GSG §4 五种方案、解析初值与图 1–8；给出 DLW 双线性残差、有限 h / 连续参照分离、非线性与双线性独立推进、开链基值、实验矩阵与高频预算。**本次是方案，未运行新的数值时间积分。** 同步纠正主报告 §11 的平均模态、制造解命名、误差测阶、ETD 与守恒预期表述；现有系统与证明不变。
> 源：`Paper/gsg_project/dlw_report/_src/numerical_analysis.src.html`；构建：`pwsh -File Paper/gsg_project/dlw_report/build_html.ps1 -SourceFile _src/numerical_analysis.src.html -OutputFile numerical_analysis.html`。构建脚本默认参数仍生成原主报告 `index.html`。主报告 §11 已增加专题入口。不要手改两个生成 HTML。
> 验证：两份 HTML 已重新构建，各内嵌 60 个字体；浏览器检查专题 204 段、主报告 1233 段公式，0 渲染错误、0 可见美元定界符残留，文件链接均存在；专题桌面与窄屏显示已检查。


> **2026-09-20：HTML 语言整理。** 按用户要求，以现有论文版为准重述正文，改写 114 个段落及 30 个列表说明，简化章节标题与衔接语；未开展新的数学审查或研究。源仍为 `Paper/gsg_project/dlw_report/_src/index.src.html`，已重新生成主目录 `index.html`。原有 122 段独立公式及 16 个章节锚点保持不变；1233 段数学表达式经 KaTeX 编译无错误。语言整理前的完整 HTML 与源文件备份在 `Trash/html_before_language_edit_20260920/`，还原说明见 `Trash/README.md`。本条为最新编辑记录，下文尺寸与渲染计数是历史版本记录。


> 这是本工作区（`C:\Users\msz\aca`）的**唯一入口文档**。
> 任何 agent / 人接手前先读这一页：它告诉你**什么东西在哪里**、**当前结论是什么**、
> **哪些结论已经被推翻**。
>
> 最后整理时间：2026-09-19 20:16（目录整理，只做 `mv`，没有删除任何文件，详见 `Trash/README.md`）；
> 2026-09-19 晚追加：主目录 `index.html` 改写成论文（见文首横幅与 §5）。

> **2026-09-19 晚（最新）：主目录 `index.html` 已改写成论文式文档（12 章 + 附录 A/B/C）**
> 源：`Paper\gsg_project\dlw_report\_src\index.src.html`（151,507 字节，唯一权威源）；
> 构建：`pwsh -File Paper\gsg_project\dlw_report\build_html.ps1` → 主目录 `index.html`（1,887,510 字节，自包含）。
> 新结构：§0 速览 → §1 底层工具 → §2 系统 0 连续 DLW → §3 为什么直接差商不行（no-go/唯一性）→ §4 系统 1 半离散双线性（任意 N 证明）
> → §5 系统 1 性质 → §6 系统 2 非线性闭合（消元推导 + 二阶一致）→ §7 系统 2 性质与线性谱 → §8 可积性定位（S 可积？强可积？）
> → §9 验证方法与证据分级 → §10 理论上还能做什么 → §11 数值上怎么做 → §12 结论 → 附录 A 符号表 / B 文件与复现命令 / C 更正与作废清单。
> **旧版 `index.html` 的两条横幅已删除**：其内容被写进正文（§4.6 表 4.3 的"谁被推翻、谁被恢复"、§8.4 五条、附录 C 十二条），
> 因为新版本身已是最新文档，不再需要"先去看别的文件"的提示。旧版完整备份在 `Trash\html_before_paper_rewrite_20260919\`。
> 写法：全程只用底层概念（从 $D$ 算子、差分算子、行列式引擎搭起），每条结论带证据徽章
> （精确 / LEAN / 数值 / 条件 / 未完成 / 已作废）。
> **渲染已程序化验证**：用 KaTeX 自身渲染器逐段编译（1260 段数学、0 错误），
> 再用无头浏览器 dump DOM 复查（10,415 个 katex 节点、0 个 katex-error、可见文本残留 `$` = 0）。
> 途中修掉一个真实缺陷：数学段内的**裸 `<`**（如 `\prod_{i<k}`）会被 HTML 解析器当成标签起始、
> 切断 `$$…$$` 配对，已对 17 个数学段做 `&lt;`/`&gt;` 实体转义（**以后写公式请用 `&lt;` 或 `\lt`**）。
> 写作脚手架（`head.html` / `body_01..12.html` / `tail.html` / `old_body.html`）已移入 `Trash\html_paper_parts_20260919\`；
> **改报告请直接改 `_src\index.src.html`**，不要再用分块文件（它们已不同步）。

> **S 可积性专项更新（2026-09-19）**：`Paper/dlw_semidiscrete/S_INTEGRABILITY_STATUS.md`。
> 新增任意 N Gram 解上的精确谱波函数
> `exp(zx-z²t) λ_h(z-a)^j τ_1(j;z)/τ_0(j)`，秩一格点更新证明其满足物理场的格点线性关系；
> 固定归一化的谱渐近比为 `∏(z-p_i)/(z+q_i)`。180 组精确系数检查通过。
> **严格 IST 意义的 S 可积仍未确证，也未被否定**；旧“双线性已 S 可积”标签缺乏完整证明。
> 局部变量重构可传递已有谱/Darboux 结构；一般 IST 的传递还需边界/函数空间上的可逆性。

> **最新研究更新：Gram 与可积性复核（2026-09-19，优先于下方所有旧结论）**
> 见 `Paper/dlw_semidiscrete/GRAM_INTEGRABILITY_REASSESSMENT.md`。
> **纯 x,t,j Gram 构造已恢复并给出任意 N 证明**：双线性对和参数—格点恒等式精确成立，
> 因而是 `NONLINEAR_CLOSURE.md` 新 u/v 系统的精确行列式解。
> 旧审计失败的是额外连续 y 相位随 s 改变的混合构造，不能否定纯格点构造。
> 新验证：N=1..5 双线性 200 组系数恒零；N=1..3 非线性 54 组 Fraction(0)；
> 辅助 Toda 45 组。已证明正实无奇点区间、相互作用系数保持、局部守恒律、Darboux 交织关系。
> **旧 `lax/VERDICT.md` 的全系统“不是强可积/S-可积”定论撤回**：其矩阵、周期条件、
> 守恒密度解释存在错误；Lean 指定矩阵恒等式不能排除其他谱表示。
> 完整不可消去谱参数、无穷独立守恒量仍未建立；x 高频线性增长仍在。

> **2026-09-19 后续研究更新（优先于下方旧进度）**：已完成指定双线性对
> `B_(a-h/2) F_j·G_j=0`、`B_(a+h/2) F_j·G_(j+1)=0` 的条件性非线性化。
> 见 `Paper/dlw_semidiscrete/NONLINEAR_CLOSURE.md`：对称交错物理变量、仅含 u/v 的闭合系统、
> 二阶一致性及 λ=-2 的 DLW 极限；`verify_nonlinear_closure.py` 已通过任意符号函数验证。
> **没有恢复旧有限 h Gram τ/孤子声称。** 另外，旧 `audit_gauge.py` 将 Hirota `D_y B`
> 错写为 `B(f,g_y)`，故下方及旧审计中“连续 (6) 与 τ 不相容”的判断应撤回；
> 正确连续 N=1 双线性对已作一般参数的符号验证。细节见新报告 §7。

---

## 0. 主目录一眼地图

```
C:\Users\msz\aca\
├── lean_verification.html ← 独立 Lean 核验页：旧证据、新命题与证明状态
├── numerical_analysis.html ← 数值总报告与图表 + GSG 方法说明（已同步最新实测结果）
├── AGENTS.md              ← 本文件：索引 + 进度（给 agent 看）
├── index.html             ← ★ 给人直接看的自包含 HTML 报告（双击即可；KaTeX 已内联）
├── Paper\                 ← 论文主线（代码 + 报告 + 文献 + 原文）
│   ├── dlw_semidiscrete\  ★ 当前最新结论所在（先读 GRAM_INTEGRABILITY_REASSESSMENT.md、NONLINEAR_CLOSURE.md）
│   │   └── numerics\      ★ E0–E7 数值实验的实现与实测结果（先读 REPORT.md；run_all.py 复现）
│   ├── gsg_project\         GSG→DLW 移植；Lax 对/守恒量；HTML 报告的模板与构建脚本
│   ├── refs\                文献库：52 个 PDF + pdftotext 文本
│   ├── reports\             文献调研报告（dlw_laxpair_report.md）
│   └── sources\             原文/参考书 PDF（PhysD 论文、GSG 论文、Hirota 书、Hunter–Saxton）
├── Workspaces\            ← 各次尝试的独立工作区（4 个模型 run + 2 个临时分析）
├── Trash\                 ← 暂不需要但保留（只 mv 进来，未删除；含还原说明）
├── lean-toda\             ⚠ Lean 形式化工程（原地不动，勿移动/改名）
└── _lean_shared\          ⚠ 共享 Lean 4.34.0 + Mathlib 环境（原地不动，勿移动/改名）
```

**硬规则**

1. `_lean_shared\` 与 `lean-toda\` **原地不动**。Lean 入口是绝对路径写死的
   （`_lean_shared\Check-Lean.ps1`），`lean-toda\.lake` 里有构建产物；移动它们会断依赖。
2. 不用的东西**挪到 `Trash\`，不要 `rm`**。`Trash/README.md` 记录每件的来源与还原命令。
3. 本目录的 `dlw_semidiscrete`、`gsg_project` 两个**报告（.md）**的正文里含有**已作废结论**，
   读的时候必须看文首的作废横幅，别只看结论表。
   （主目录 `index.html` 不适用本条：它已于 2026-09-19 晚重写成论文，作废范围写在正文 §4.6 / §8.4 / 附录 C 里。）
4. 主目录 `index.html` 是**生成物，不要手改**：改 `Paper\gsg_project\dlw_report\_src\index.src.html`，
   再跑 `pwsh -File Paper\gsg_project\dlw_report\build_html.ps1`（输出已经指向主目录 `index.html`）。

---

## 1. 关键文件索引（"我要找 X，去哪个文件"）

| 我想知道 / 我要找 | 文件 |
|---|---|
| Lean 已证明什么、缺什么、如何派工和验收 | `lean_verification.html`（已标出 23/32，另 N01 部分完成）；命题与交接 `Paper/dlw_semidiscrete/lean_contracts/Contracts.lean`、`README.md`；证据 `status.json`；证明源码 `Workspaces/lean_contracts/proofs/`（入口 `Main.lean`）；C07 真伪审计 `Workspaces/lean_contracts/audit_c07.py` |
| GSG 数值实验如何迁移到本项目 | 实测总报告与方法专题 `numerical_analysis.html`（根目录）；源 `Paper/gsg_project/dlw_report/_src/numerical_analysis.src.html`。**实际执行与实测结果在 `Paper\dlw_semidiscrete\numerics\`（先读 `REPORT.md`）** |
| **当前（最新）到底成不成立** | `Paper\dlw_semidiscrete\GRAM_INTEGRABILITY_REASSESSMENT.md`（Gram/τ/可积性复核）、`NONLINEAR_CLOSURE.md`（闭合非线性系统）；旧 `AUDIT.md`、`NL_RESULT.md` 有范围性纠正 |
| 半离散双线性方程那套推导的**原文**（含 ⚠ 作废声明） | `Paper\dlw_semidiscrete\REPORT.md` |
| 审计与被推翻的装置（脚本） | `Paper\dlw_semidiscrete\audit_tau.py`、`audit_points.py`、`audit_h.py`、`audit_cont.py`、`audit_gauge.py`、`nlaudit.py`、`exact7.py`、`diag.py`、`idcheck3.py` |
| **DLW 有没有 Lax 对 / 算不算完全可积**（文献层面） | `Paper\reports\dlw_laxpair_report.md` |
| **半离散 DLW 的线性结构与守恒律** | `Paper\dlw_semidiscrete\GRAM_INTEGRABILITY_REASSESSMENT.md` §6–9；旧 `Paper\gsg_project\lax\VERDICT.md` 全系统定论已撤回，见文首 |
| 8 条离散化路线的横向比较与推荐 | `Workspaces\expression_deepseek-v4.1-flash_20260917_222927\reports\FINAL_REPORT.md` |
| 8 路线中每条声称结论的证据分级 | `Workspaces\expression_deepseek-v4.1-flash_20260917_222927\reports\CLAIMS_AND_PROOFS.md` |
| 整个项目的共享数学约定（符号、双线性算子、V1–V10 已验证结果） | `Workspaces\expression_deepseek-v4.1-flash_20260917_222927\common\SHARED_MATH_SPEC.md`、同目录 `reports\MAIN_VERIFICATION.md` |
| GSG→DLW 移植的**早期版本**（已被 dlw_semidiscrete 修订） | `Paper\gsg_project\OUT_GSG_DLW_report.md`、`Paper\gsg_project\OUT_GSG_DLW_short_report.md` |
| 可读的论文式 HTML 报告（带公式渲染，给人看） | **`index.html`（工作区主目录，1.89 MB，自包含、可直接双击）**——12 章 + 附录 A/B/C 的完整论文；源 `Paper\gsg_project\dlw_report\_src\index.src.html` + 构建 `build_html.ps1`（输出已指向主目录） |
| 论文原文 | `Paper\sources\PhysD-published.pdf`（Sheng–Yu, Physica D 432 (2022) 133140）；文本抽取 `Paper\gsg_project\physd.txt`、`Paper\refs\...` |
| GSG 半离散化方法的原文 | `Paper\sources\Numerical_Algorithms_gsg (1).pdf`（Feng–Sheng–Yu, Numer. Algorithms 94 (2023) 351–370）；文本 `Paper\gsg_project\gsg.txt` |
| Hirota 双线性方法参考书 | `Paper\sources\hirota-book-new.pdf` |
| Hunter–Saxton 半离散化（同类先例，方向 G/H 的 prior art） | `Paper\sources\2 Huner Saxton.pdf` |
| 某个具体文献的 PDF / 抽取文本 | `Paper\refs\`（命名 = 一作或 arXiv 号，`.pdf` + 同名 `.txt`） |
| Lean 证明：离散 Lax 对谱退化 | `lean-toda\TodaFormalization\DLWLaxDegenerate.lean`、`Paper\gsg_project\lax\lean\DLWLaxDegenerate.lean` |
| Lean 证明：交错格式 / 单孤子 / 连续极限 | `lean-toda\TodaFormalization\DLWStaggered.lean`、`DLWOneSoliton.lean`、`DLWSemidiscrete.lean`、`DLWContinuum.lean`、`DLWDiscretePair.lean` |
| Lean 验证入口（唯一合规方式） | `_lean_shared\Check-Lean.ps1`（用法见 `_lean_shared\README.md`） |
| 被挪走的东西还能不能找回来 | `Trash\README.md` |

---

## 2. 当前进度（研究主线）

**总问题**：把 Feng–Sheng–Yu 对广义 sine-Gordon (GSG) 的**半离散化方法**移植到
Sheng–Yu 的 (2+1) 维色散长波 (DLW) 系统（*Physica D* **432** (2022) 133140），
给出离散双线性方程与孤立子结构，并判断这个离散系统本身有没有可积结构。

### 2.1 时间线（结论变更史，很重要）

| 时间 | 阶段 | 结论 | 证据文件 |
|---|---|---|---|
| 09-17 | **8 条路线并行探索**（4 个模型 run：deepseek-v4-flash / v4.1-flash / glm-5.3-flash / union-alpha） | **结构性障碍**：DLW 主部含不定的 `J∂_x²`（`J=[[0,1],[1,0]]`，特征值 ±1），`w−v` 支是**后向热方程**，`x` 方向本身不适定；`y` 离散在原理上触及不到它（`k⁴` 系数恒为 1）。正面成果：**交错双 tau 半离散系统**精确验证（N=1..5）、`w=u_y` 改写把离散化影响压成一对算子 | `Workspaces\expression_deepseek-v4.1-flash_...\reports\FINAL_REPORT.md` |
| 09-18 | **移植 GSG 三件套**（`dlw_semidiscrete` 主线） | 声称得到"最终答案"：交错对 `(7)_h: B_{a−d}F_j·G_j=0`、`(6)_h: B_{a+d}F_j·G_{j+1}=0`，靠结构恒等式 `(†) τ₁(j;a−d)=τ₁(j+1;a+d)`；并给出非线性层 `(A)_h`、物理形式 `(A')` | `Paper\dlw_semidiscrete\REPORT.md`（★ 已被推翻） |
| 09-19 上午 | **半离散系统的 Lax 对 / 守恒量** | 定论：离散方向**谱退化**——单值矩阵 `T_N` 的四个矩阵元与 `tr T_N` 都**不含谱参数**（Lean 已证 `zf_all`/`trace_z_free`/`det_z_free`），谱曲线平凡；`I_0..I_3` 都不是流动不变量。系统只是**弱 Lax 对 / S-可积**，**不通过 Painlevé 检验**。 | `Paper\gsg_project\lax\VERDICT.md` |
| 09-19 下午 | **文献调研** | DLW 是 Boiti 的 **weak Lax pair**（含 `∂_x^{-1}`）可积；WTC/ARS 两种 Painlevé 检验**均不通过**；守恒密度 `ρ_k,σ_k` 任何可及文献都没印；**离散/半离散 DLW 文献里完全没有**。 | `Paper\reports\dlw_laxpair_report.md` |
| 09-19 19:58–20:16 | **审计（推翻 09-18）** | 09-18 的"精确验证"有**两个叠加缺陷**：① `jet3.py` 用 `mpmath.mpf` 浮点存系数（`1e-89` 是噪声地板）；② **所有判零只在单个基点 `(x,t,y)=(1/5,2/7,0)` 上做**，而该点恰落在残差的零点曲面上。真相：`(7)_h`、`(6)_h` **不是恒等式**，残差 `O(0.02–2833)`、随 `h` 按 `O(h)` 衰减；结构恒等式 `(†)` **不成立**（`y` 相位系数 `T₁≠T₂`，除非 `d=0`/`p+q=0`/`p−q=2a`）；非线性层全部作废。 | `Paper\dlw_semidiscrete\AUDIT.md`、`NL_RESULT.md` |

### 2.2 现在还活着的结论（可靠）

- **[精确代数恒等式]** Hirota 商恒等式
  `D_x²F·G/(FG) = (ln F)_xx + (ln G)_xx + [(ln F)_x − (ln G)_x]²`（交叉项系数 **+1**），
  由 `idcheck3.py` 在任意符号 `F,G` 上用 sympy 唯一确定 `(c₁,c₂,c₃)=(1,1,1)`，且用 `Fraction` 得字面 0。
  同类：`D_tF·G/(FG)=(ln F)_t−(ln G)_t`、`D_xF·G/(FG)=(ln F)_x−(ln G)_x`。
- **[精确验证]** 连续层 `(7)`：`B_a f·g = 0` 对 Gram τ 恒成立（N=1、N=2 多点确认）。
- **[Lean 定理]** 离散 Lax 对的谱退化：`zf_all`、`trace_z_free`、`det_formula`、`det_z_free`、
  `trace_charpoly_z_free`、`mobius_telescopes`、`no_constant_trace`
  —— 只依赖 `[propext, Classical.choice, Quot.sound]`，无 `sorryAx`。
- **[精确验证]** 交错格式的双线性结构与 N-孤子解保持、两孤子**相互作用系数 κ 与 `h` 无关**
  （这一点由 `Paper\dlw_semidiscrete\` 与 `Paper\gsg_project\` 两条独立代码路径复核过）。
- **[结构结论]** DLW 主部的 `J∂_x²` 不定 ⇒ 半离散化救不了适定性（Lean 代数验证 + 6 种符号验证）。
- **[文献结论]** DLW = 弱 Lax 对可积 + 无穷维 Kac–Moody–Virasoro / `W_∞` 对称，但 Painlevé 失败。

### 2.3 已作废（**不要引用**）

> ⚠ 本节作废范围以**文首「最新研究更新」**为准：被否定的是**额外连续 y 相位随 s 改变的混合构造**；
> 纯 `x,t,j` 的 Gram 构造已由 `GRAM_INTEGRABILITY_REASSESSMENT.md` **恢复并给出任意 N 证明**。
> 另外本列表中"连续 (6) 与 τ 不相容"一条**已撤回**（旧 `audit_gauge.py` 写错了 `D_y B`）。

- `(7)_h`、`(6)_h` 作为"有限 `h` 的精确格点恒等式"的**全部**声明 → 实为 `O(h)` 离散化；
- 结构恒等式 `(†)`；由它导出的 `(★)`、`(★')`、格点位移结构；
- 整个"非线性层" `(A)_h`、`(B)_h`、`(A')` 与那张连续极限表；
- 旧报告 `Paper\gsg_project\OUT_GSG_DLW_report.md` §3.3(c) 的"对称二点恒等式"（仅 N=1 假象）；
- `mshift.py` 的"剖面 = 连续剖面在 `a→a−h/2`"（正确说法是**速率重正化** `1/P ↦ Λ_h(P)`）；
- `REPORT_LAX.md` 里"$\operatorname{tr}T(z)$ 给出守恒量族"的那一轮结论（被 `VERDICT.md` 推翻）。

### 2.4 下一步（还没做的）

1. **换离散化路线**：`NL_RESULT.md` §5 给了两条——(a) 不用参数移位，改成"格点移位 + 谱参数不变"，
   让 `y` 相位系数严格匹配；(b) 直接做 Hirota 型 `y` 差分，反解合法的 `λ(z)`。两条都要重新推导。
2. **论文形态 `(6)` 与实现的 τ 不相容**（`audit_gauge.py`：残差与相位常数无关、对相位常数无解）——**尚未解决**。
3. **格点 Lax 对 / 守恒量**未写出。**非线性层的数值实验已做**（`Paper\dlw_semidiscrete\numerics\`，E0–E7）：精确 τ 满足 (N1)(N2)、二阶收敛、相移与守恒均验证；但**保结构长时间行为仍未做**（受 §7 高频预算限制，见 `numerics\REPORT.md` §11）。
4. 2DTL 探针（`certify.py` §H）只在 N=2 复核过，未做 N=3,4。
5. GSG 的第三件工具（离散 hodograph / SAMM）在 DLW **没有对应物**（无 hodograph 对称性）——已论证。
6. 更大搜索模板：纳入 `τ_2`、`τ_{−1}`、位点 `(±2,0)`、多层 `s=a±kd (k≥2)`，未探讨。

### 2.5 方法学铁律（血泪教训，务必遵守）

1. **判零不许用浮点**：用 `fractions.Fraction`，让零是字面 `Fraction(0)`（见 `jet4.py`）。
2. **判零不许单点**：单点会碰巧落在残差零点集上；必须多点，或把 `(x,t,y)` 留作符号。
   本项目最严重的一次错误就是这么来的。
3. **有 `h` 就必须扫 `h` 看标度**，区分"恒为 0"与"`O(h)`"。
4. **指数和判零按实际指数向量合并**：有限和 `Σ C_k e^{k·z} ≡ 0` 当且仅当每个不同实际向量 k
   的合并系数为零。不同向量即使存在有理线性关系，也不能直接视为同一个指数；乘积关系要先换算为指数向量相加。
   新例见 `verify_gram_reassessment.py`，旧 `exactexp.py` 的分类方法不能直接当作判零定理引用。
5. **结构恒等式要单独验证**，不能因为"看起来对"就接受（`(†)` 就死在 `y` 相位系数上）。
6. **Lean 只是代数桥**：τ 函数输入、文献事实、以及"线性化模增长 ⇒ 非线性不适定"这些桥接步骤
   **没有**被形式化，报告里要如实标注。

---

## 3. 各组详细说明

### 3.1 `Paper\dlw_semidiscrete\` — 当前最新结论（★ 优先读）

- **先读**：`GRAM_INTEGRABILITY_REASSESSMENT.md`（Gram/τ/可积性复核，最新）、`NONLINEAR_CLOSURE.md`（闭合非线性系统）、
  `S_INTEGRABILITY_STATUS.md`（谱波函数 / S 可积现状）。
- **再读（历史层）**：`AUDIT.md`（审计报告 + 存活/作废清单）、`NL_RESULT.md`（非线性层结论 + 换路线建议）、
  `REPORT.md`（09-18 那套推导的完整正文，文首有 ⚠ 作废横幅，保留作对照）。
- 复现（在该目录下）：
  ```powershell
  cd C:\Users\msz\aca\Paper\dlw_semidiscrete
  python -u audit_tau.py      # sympy 独立复核 (7)_h：给出残差的精确解析式
  python -u audit_points.py   # 多点体检：打印反例点
  python -u audit_h.py        # 残差随 h 的标度（O(h)）
  python -u audit_cont.py     # 连续层：(7) 恒零、(6) 不成立
  python -u audit_gauge.py    # 相位常数救不活 (6)
  python -u nlaudit.py        # 所有声明的多点判定表
  python -u idcheck3.py       # (H1) 的符号证明，唯一解 (1,1,1)
  python -u exact7.py         # B_a(F,G) 的精确闭式
  python -u diag.py           # (H1)(H2)(H3) 残差；(A)_h = (7)_h/FG 逐位一致
  python -u nlfinal.py / nlcont.py / soliton_lattice.py   # 旧路线的验证电池（结论已作废，仅供追溯）
  ```

#### 3.1.1 `Paper\dlw_semidiscrete\numerics\` — E0–E7 数值实验（2026-09-22 新建）

实现根目录 `numerical_analysis.html` 所规划的全部实验，**全部脚本新建于此，未安装新依赖**。

- **入口**：`REPORT.md`（实测结果主文档）；`README.md`（结构说明）
- **运行**：`python -u experiments/check_regressions.py`（24 项回归，先跑）→ `python -u run_all.py`（约 20 分钟，9 个阶段）→ `python -u summary.py`（一屏汇总）→ `python -u make_figures.py`（出图）
- **不做**的事：不修改工作区其它任何文件；不手改生成的 HTML
- **两条边界**（引用时务必带上，**2026-09-22 复核后已更正**）：① E2/E3 时间阶数未对精确参照测出（空间误差主导；同网格自收敛可分离，E7 已示范近四阶）；② 【已撤回】旧说"`ContRef` 的 `(u⁰,v⁰)` 只是首项、不是连续 DLW 的解"——相位 bug 修复后解析残差 `≤6.3e-61`，它**就是**解；探针的 `1e-2` 残差是 dx⁴ 差分截断地板

### 3.2 `Paper\gsg_project\` — GSG→DLW 移植 + Lax/守恒量

- `OUT_GSG_DLW_report.md` / `OUT_GSG_DLW_short_report.md`：移植报告（被 `dlw_semidiscrete` 修订）。
- `lax\VERDICT.md`：谱退化 / "不是强可积"的定论（**全系统部分已撤回**，见文首"最新研究更新"；其矩阵、周期条件、
  守恒密度解释有误，Lean 只证了指定矩阵的恒等式）。可复现命令仍有效。
- `lax\REPORT_LAX.md`：过程版（含被推翻的守恒量说法，文首有说明）。
- `lax\lean\DLWLaxDegenerate.lean`：谱退化的 Lean 证明。
- `dlw_report\`：**HTML 报告已移到主目录**（`..\..\..\index.html`，双击即可）。这里留下的是生成链：
  `_src\index.src.html`（**唯一权威源，2026-09-19 晚已重写为论文式正文**）+ `build_html.ps1`（把 KaTeX 与字体内联，输出到主目录 `index.html`）
  + `_assets\package`（KaTeX 依赖）+ `verify_claims.py` / `verify_output.txt`（旧版报告结论的独立复核）。
- `fundamentals\loop_soliton_demo.py`（+ 本次归位的 `loop_demo.csv` / `loop_demo.png`）：loop soliton 演示。
- `out\verification_log.txt`：早期验证日志。
- 复现：见 `lax\VERDICT.md` §7（数值 + Lean 两条命令，路径已更新为新位置）。

### 3.3 `Paper\refs\` — 文献库（52 个文件）

- 命名规则：一作姓 + 年，或 arXiv 号；每个 PDF 常配一个同名 `.txt`（`pdftotext` 抽取）。
- 关键文献：`math9804162`（DLW 方程形式）、`solv-int/9803007` → `miura9803007`（弱 Lax 对）、
  `nlin0107027`、`ctp9298`、`ctp8805`（Painlevé / 对称性）、`gordoa`（广义 DWW 递归算子与 Lax 对）、
  `gauge0802.2334` / `gauge0907.3205`（Leble 的规范不变算子 Lax 对）、
  `toda1908.08725` / `toda2104.06123` / `fu1802`（2D Toda Lax 对）、`takasaki_aa95`（dKP）、
  `ap818`（dispersionless Lax）、`jnmp_sg` / `huyu2007.json`（离散 sinh-Gordon）。
- 索引与每篇的作用见 `Paper\reports\dlw_laxpair_report.md`。

### 3.4 `Paper\reports\` — 文献调研

- `dlw_laxpair_report.md`：DLW 的 Lax 对 / 守恒密度 / 2DTL 与 dKP / 离散 DLW 的系统检索报告，
  逐条标注来源 URL 与"未找到/未核实"的诚实边界。是 §2.1 中"文献层面"结论的依据。

### 3.5 `Paper\sources\` — 原文与参考书（PDF）

`PhysD-published.pdf`（主源论文）、`Numerical_Algorithms_gsg (1).pdf`（GSG 方法）、
`hirota-book-new.pdf`（双线性方法）、`2 Huner Saxton.pdf`（Hunter–Saxton 半离散化先例，arXiv:2606.18701v2）。

### 3.6 `Workspaces\` — 各次尝试的工作区（隔离保留）

| 目录 | 内容 | 一句话 |
|---|---|---|
| `expression_deepseek-v4.1-flash_20260917_222927\` | 8 个方向目录 A–H + `proofs\` + `reports\` + `pdftext\` | **内容最全的一次**；`reports\FINAL_REPORT.md` 是横向比较的权威文件（41 KB） |
| `expression_deepseek-v4-flash_20260917_220258\` | 同上骨架，较薄 | 第一轮跑，被 v4.1 那次覆盖 |
| `expression_glm-5.3-flash_20260917_225005\` | 同上骨架 | 另一模型的同题独立跑 |
| `expression_union-alpha_20260917_221034\` | 含 `proofsA..proofsH` 八个 Lean 根 | union-alpha 的跑，Lean 目录按方向隔离 |
| `analysis_A_bilinear\` | 6 个小脚本 + 输出 | A 方向（双线性形式）的临时分析 |
| `analysis_codex_backlund\` | 会话转储 + Bäcklund 抽取脚本 | 从 codex 会话里抽 Bäcklund 相关的临时分析 |

> 每个 `expression_*` 里的 `RUN_CONTEXT.md` 记录：跑的模型、时间、环境（Lean 4.34.0 / Mathlib 提交）、
> 假设 V1–V10、目录约束、复现命令。**读它们就能知道那次跑到底做了什么。**
> 这些目录里的 `lean\`、`proofs\` 是**工作区内的 Lean scratch**，不是共享环境，随便动；
> 但共享入口仍必须用 `_lean_shared\Check-Lean.ps1`。

### 3.7 `Trash\` — 暂不需要（未删除）

`tmp\`（会话转储 / PDF 页 PNG / 与别处重复的 `PhysD.txt`）、`_hirota_pages\`（从 Hirota 书 PDF 抽的 91 张页图）、
`refs_dupes\`（3 个 0 字节的失败下载 + 1 个与 `cpb_c.pdf` 内容相同的副本）、
`pycache_from_syntax_check\`（语法普查产生的 237 个 `.pyc`）、
`html_before_paper_rewrite_20260919\`（**改写前的旧 HTML 报告全文**，含 `index.html` 与 `index.src.html`）、
`html_paper_parts_20260919\`（本次改写的分块脚手架 `head/body_01..12/tail/old_body.html`）。
来源与还原命令见 `Trash\README.md`。

### 3.8 `lean-toda\` 与 `_lean_shared\`（⚠ 原地不动）

- `_lean_shared\`：**共享 Lean 环境**，Lean 4.34.0 + Mathlib（提交 `5ed29652...`），7 GB / 14 万文件。
  唯一合规入口 `Check-Lean.ps1`（返回码 0 **且** 输出 `PASSED` 才算过；`sorry`/`admit`/新 `axiom` 一律拒绝）。
  用法见 `_lean_shared\README.md`。**禁止** `lake init/update/build Mathlib`、禁止 clone Mathlib、禁止改公共目录。
- `lean-toda\`：Lean 形式化工程（`TodaFormalization\DLW*.lean`，见 §1 索引）。
  另有 `check_dlw_candidate.py`、`check_dlw_staggered.py` 及配套 JSON 做精确有理数系数检查；
  `dlw_staggered_construction.md` 是交错构造的文档。
  验证：`lake build TodaFormalization`（在这个目录下）或走 `_lean_shared` 入口。
- 这两块被**故意保留在原位**：入口路径写死、`.lake` 里有构建产物，挪动会断依赖。
  索引里已标明它们的位置，所以不需要为了"摆整齐"去动它们。

---

## 4. 本次整理做了什么（可回滚）

- 新建 `Paper\`、`Workspaces\`、`Trash\`，把散在根目录的研究目录/文献/原文/报告**移动**（`Move-Item`，等价 `mv`）进对应位置；
  根目录由 20 项（7 个文件 + 13 个目录）降到 6 项（本文件 + `Paper`、`Workspaces`、`Trash`、`lean-toda`、`_lean_shared`）。
  文件数已逐目录核对：`dlw_semidiscrete` 109、`gsg_project` 659(+2 回位)、`refs` 52(+4 入 Trash)、
  `expression_*` 76/734/93/178、`lean-toda` 10324、`_lean_shared` 144576 —— 与整理前一致，无丢失。
- 移动后**同步更新了 73 个文本文件里的 120 处旧绝对路径**（`学术内容\X` → `学术内容\Paper\X` / `Workspaces\X`），
  保证报告里的 `cd ...` 与脚本里的 `sys.path` 仍然有效。
- **没有删除任何文件**；`_lean_shared\`、`lean-toda\` 内容一字未动。
- 追加一步：把 HTML 报告 `Paper\gsg_project\dlw_report\index.html` **移到主目录 `index.html`**（它 100% 自包含：
  KaTeX CSS/JS 与 20 个 woff2 字体全部内联，0 个外部资源引用，挪到任何地方都能单独打开）。
  同时在 `_src\index.src.html` 里加了一条**「后续进展」横幅**（指向 `NONLINEAR_CLOSURE.md`、
  `GRAM_INTEGRABILITY_REASSESSMENT.md`、`S_INTEGRABILITY_STATUS.md`，并注明两处撤回），
  再把 `build_html.ps1` 的输出改到主目录并**重新构建**（1,831,584 字节，60 个字体全部嵌入、0 个残留占位符），
  所以 `index.html` 里最新横幅在最上面、旧的红色作废横幅在下面，生成链仍然一致。
- 已知副作用（如实记录）：
  - 上述 73 个被改写路径的文件，其**修改时间**变成了整理时间（内容未变）；
    其中 `Paper\dlw_semidiscrete\AUDIT.md`、`NL_RESULT.md` 的原始时间（09-19 19:58、20:09）已手工还原。
  - `Workspaces\analysis_codex_backlund\transcript.txt` 里保留了会话日志中的旧路径
    （`C:/Users/msz/学术内容/tmp/pdfs/...`）。那是**历史记录**，故意不改。
  - `Paper\refs\` 建目录时曾短暂嵌套成 `Paper\refs\dlw_refs`，已修正，`Paper\refs\` 现有 52 个文件。

---

## 5. 2026-09-19 晚：主目录 HTML 报告改写成论文（可回滚）

**做了什么**：把 `index.html`（原来是"结论清单 + 两条作废横幅"）整体重写为论文式文档，并**补齐了此前正文缺失的推导**。

| 章 | 内容 | 关键点 |
|---|---|---|
| §0 | 速览 + 三系统对照表 + 阅读指南 | 一页看懂有什么/什么是证过的 |
| §1 | 底层工具 | $D$ 算子、$\lambda_h$、差分算子、柯西行列式、矩阵行列式引理、离散指数定理、主子式展开（从积木搭起） |
| §2 | 系统 0 连续 DLW | 原文 (1)(2)、双线性对、$\lambda=-2$ 的化简 (2.6)、Gram τ、**$D_yB_a$ 写法的更正** |
| §3 | 为什么直接差商不行 | 一阶残差闭式、逐点 (7) 的平坦性、24 组合穷举 + **no-go/唯一性**、伪恒等式 $h^{-2}$ 陷阱 |
| §4 | 系统 1 半离散双线性 | **六步完整推导**（格点 τ → 逐矩阵元恒等式 → 任意 $N$ 的定理 4.3 → 定理 4.4）；表 4.3“谁被推翻、谁被恢复” |
| §5 | 系统 1 性质 | 离散指数定理、$A_{ik}$ 与 $h$ 无关、单孤子显式、无奇点区间、守恒律、Darboux 交织 |
| §6 | 系统 2 非线性格点系统 | 对称交错变量的**动机**、六步消元推导 (6.4)–(6.11) → (N1)(N2)、$O(h^2)$ 一致性与 $\lambda=-2$ 极限、反向重构 |
| §7 | 系统 2 性质与线性谱 | 精确谱波函数（含秩一更新证明思路）、谱渐近比 $\mathcal T(z)$、线性色散 (S) 与 $x$ 高频增长 |
| §8 | 可积性定位 | S 可积/C 可积的底层定义、四件缺的东西、旧“不是强可积”定论的**5 条撤回理由**、能说/不能说对照表 |
| §9 | 验证方法 | 五条铁律、两次翻车、证据分级、Lean 的边界 |
| §10 | 理论上还能做什么 | 谱与逆散射四缺口、守恒量递归、正则性/退化、边界整体相容、$x$ 高频四条出路、推广、可发表性、Lean 路线 |
| §11 | 数值上怎么做 | 四类任务、奇异质量矩阵（$\delta_-$ 的核 = 平均模态）、IF/ETD 方案、**高频预算公式 $k_{\max}^2T\lesssim\ln(1/\varepsilon)$**、制造解收敛、两孤子相移、守恒监测、谱提取、九陷阱 |
| §12 + 附录 A/B/C | 结论、符号表、脚本↔陈述对照、**12 条更正与作废清单** | 附录 C 逐条写明“作废的是哪个对象” |

**验证方式（以后改 HTML 请照做）**：
1. `pwsh -File Paper\gsg_project\dlw_report\build_html.ps1` → 主目录 `index.html`；
2. **KaTeX 逐段编译**：用 Node 载入 `_assets\package\dist\katex.min.js`，抽取全部 `$…$`/`$$…$$` 段，
   先解码 HTML 实体再 `renderToString(..., {throwOnError:true})` —— 本次 1260 段、0 错误；
3. **无头浏览器 dump DOM**：`msedge --headless --dump-dom`，统计 `class="katex"` 节点数、
   `katex-error` 数，并**去掉 `<script>/<style>/<math>` 后检查可见文本里是否还有残留 `$` 或 LaTeX 命令**（本次均为 0）。
   > 只看截图会漏判：截图工具对“程序化滚动后重绘”不可靠，**必须以 DOM 统计为准**。

**踩过的坑**：数学段里的**裸 `<`/`>`**（如 `\prod_{i<k}`、`0<p_1<…`）会被 HTML 解析器当作标签起始，
把 `$$…$$` 的配对切断，导致那几段公式**完全不渲染**。已对 17 个数学段做 `&lt;`/`&gt;` 实体转义，
并修掉一处跨行的 inline 公式（跨行会让基于 `[^$\n]` 的抽取器漏掉它）。
**结论：以后在 HTML 里写公式，小于号请写 `&lt;` 或 `\lt`。**

**移入 Trash**：`head.html` / `body_01..12.html` / `tail.html` / `old_body.html` → `Trash\html_paper_parts_20260919\`（见 `Trash\README.md` §5）。
**没删任何文件**；旧版报告全文在 `Trash\html_before_paper_rewrite_20260919\`。

**数值实验（2026-09-22 已执行）**：§11 的三大实验（制造解收敛、两孤子相移、高频预算）**均已跑完**，见 `Paper\dlw_semidiscrete\numerics\REPORT.md`；
`_src\index.src.html` 里所有脚本引用均已核对存在（见附录 B）。
**注意**：`numerical_analysis.html` 本身未改，文首仍写着"尚未运行新的数值时间推进实验"——
那句话对该 HTML 是准确的（它描述的是写作时状态），**最新数值结论请看 `numerics\REPORT.md`**。
