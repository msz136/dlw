# DLW 数值实验

**2026-09-23 参数区域误差控制：** [新专题](PARAMETER_REGION_ERROR_REPORT.md)对实际固定网格 RK4 误差建立精确的参数敏感度递推、条件性小盒覆盖判据，并用 C053 周围的 25 条短时轨道核对局部变化量级；原始探针在 [`design/parameter_region_probe.json`](design/parameter_region_probe.json)。§8 进一步证明初始速度方向 `∂ν r(0)=S(∂x−D1)Z̄(0)`，将该方向的注入敏感度归为 x 差分及周期绕接误差；[`design/parameter_region_bound_diagnostic.json`](design/parameter_region_bound_diagnostic.json) 量化全域粗界在 T=.01 连中心点都无法认证的尺度，复现 `python experiments/parameter_region_bound_diagnostic.py`。其中的中心残差数据是连续时间 ODE 粗界诊断，角点与差分也仅为诊断。§9 对精确实数 RK4 的一次极短步 `7e−9` 给出**整片参数域**的双场归一化误差 `<9.40e−4` 解析证书；普通浮点舍入未外包。**目标 T=.01 尚无非零体积参数盒的严格误差认证**。原生产求解器、Gram、Lean 未改。

**2026-09-23 重分布间隔扫描：** [间隔专题](MESH_REFRESH_INTERVAL_REPORT.md)把仅在初始布点视为间隔无穷大，在 16 组参数及三档代表性分辨率上扫描每 1 至 1/16 个波宽刷新；184 条受控输运与 40 条短时 DLW 轨道完成。输运中适中刷新通常降低最终两场误差，但最短间隔并非普适最优；原 DLW 尚无通过长距离精度门槛的结论。逐次插值缺陷、精确误差递推、图 21、复现与哈希见专题及 `out/moving_mesh/interval_validation.json`。主数值报告与根目录网页从生成源同步。

**2026-09-23 固定网格 SD 注入—放大与配置选择：** [专题报告](INJECTION_AMPLIFICATION_REPORT.md)以有限 h Gram 精确场为参照，逐步分解实际 RK4 的注入、线性传播与非线性余项，并比较 P1/P5/P6/P10 的 x 分辨率、时间步和两种边界闭合。P5 加密到 nx=512 后，高频传播使短时误差反增；已做步长减半与切向差分复核。配置建议先锁定，再对 T=.01/.02 两批六组新参数共 36 个候选推进：六个建议均满足双场 0.1% 门槛，但 T=.01 有三处保守误判，T=.02 的 H6 则出现预测量低估；计入六候选诊断后，一次短时运行没有净成本节约。N2 独立局部窗口与匹配 N1 控制已检查，完整散射仍未验收。数据、两个锁定文件和 163 项验收见 [`out/injection_amplification/validation.json`](out/injection_amplification/validation.json)。复现顺序在专题 §5；原生产求解器、Gram、Lean 未改，本专题未开展移动网格实验。

**2026-09-23 路线一长距离复核：** [路线一专题](MOVING_MESH_ROUTE1_REPORT.md) §5 补充了真正演化数值场的受控输运实验：P1/P2/P7 移动网格相对冻结网格在 2 个波宽后，对 u/v 的自身节点和共同物理点误差均有跨三档分辨率的明显收益；P10 不一致。它验证网格跟踪机制，不是原 DLW 的长距离计算结果。原 DLW 按双场 1% 误差门槛的 16 条轨道都在位移 ≤0.055 个波宽时首次失败。图 20、数据和复现命令见专题；这一区分已同步 [数值总报告](REPORT.md) 与根目录 `numerical_analysis.html`。

**2026-09-23 路线二：预测性误差预算与离散伴随。** [独立报告](ERROR_BUDGET_REPORT.md) 将 SD 的 u/v 总误差逐点拆为有限 h 模型误差与求解误差，以试跑系数预测留出 h 的主导区域，并用 7 组训练参数预测 P1/P6/P10 三组真正留出参数；还对 SD/FD 的短时位置目标建立实际 RK4 一步映射的离散伴随分解。25 组预算推进、7 组额外校准轨道和 4 组伴随诊断已完成，76 项数据一致性检查通过。预测、逐格代数界和实际剖面拟合分开报告；没有普遍 SD/FD 场误差胜者，也没有连续时间严格误差上界。数据在 `out/route2/`，图 18–19 在 `figures/`。复现顺序：`experiments/route2_budget.py`、`route2_crossparam.py`、`route2_adjoint.py`、`route2_validate.py`、`route2_figures.py`；原生产 solver 与 Lean 未改。

**2026-09-23 路线一深化：** [共同网格专题](MOVING_MESH_ROUTE1_REPORT.md) 分别检验初始重分布、持续移动和间歇重分布。精确场在移动约一个波宽后显示持续移动的采样收益；实际 SD/FD 耦合推进目前只走到远小于一个波宽，移动相对冻结加密尚无稳定额外场误差收益。摘要已纳入 [数值总报告](REPORT.md) 和根目录 `numerical_analysis.html`；重建先运行 `experiments/parametric_report.py`，再运行 `Workspaces/gsg_project/dlw_report/sync_numerical_results.py` 与 `build_html.ps1`。报告包含高频非零扰动、梯度监控、网格轨迹交叉重放、真实成本、时间步检查和失败样本；数据及源码哈希在 `out/moving_mesh/route1_*.json`，图 19 可由 `experiments/moving_mesh_route1_figure.py` 再生。原生产求解器、Gram、Lean 未改。

**2026-09-23 路线 3：** [孤子流形与散射专题](MANIFOLD_SCATTERING_REPORT.md) 已完成有限 h Gram N2 五阶段相位切向／法向缺陷、独立短时真实推进、匹配单孤子控制、连续轨道 1% 门槛，以及 N3 两两因子化与两种相遇几何。SD 在所测流形参照下的短时缺陷较低；法向误差占主导。连续轨道在进入碰撞区前失败，完整求解器散射相移和数值三体因子化仍未验收。原始数据、源码哈希见 [manifold_scattering.json](out/manifold_scattering.json)，图 17 可由 `experiments/manifold_scattering_figure.py` 重生；原生产 solver、Gram、Lean 未改。

**2026-09-23 共同 x 移动网格实验：** [专题报告](MOVING_MESH_REPORT.md) 以守恒密度和有限 h Gram 坐标势构造所有 y 层共用的 x 网格，完成 16 组正则单孤子参数的固定均匀、初始加密冻结、持续移动三方案对照。分别记录有限 h Gram 与共同连续精确场的 u/v 绝对误差，并补做共同物理 x 点复核、非零扰动、同模型细 x 参照、高频/仅 v、时间步和长时网格几何检查。所测短时收益主要来自初始加密，两模型均受益；持续移动相对冻结加密未显示稳定额外收益。原生产 solver、Gram 与 Lean 未改。复现依次运行 `experiments/moving_mesh_study.py`、`moving_mesh_controls.py`、`moving_mesh_continuum.py`、`moving_mesh_common_grid.py`、`moving_mesh_validate.py`、`moving_mesh_report.py`；原始数组与哈希在 `out/moving_mesh/`。

**2026-09-23 两孤子连续误差预算：** 在相同交错物理点比较有限格距 Gram 解和连续两孤子解，并把实际 u/v 总误差逐点拆为半离散模型误差与求解误差；结构模型的 v 求解误差再拆为 W 误差与 u 重构误差。图 16 与原始数据分别在 [两孤子专题报告](MULTISOLITON_REPORT.md) 和 [two_error_budget.json](out/two_error_budget.json)。另有两模型相同连续初边值对照。复现命令：`python -u experiments/two_error_budget.py`、`python experiments/two_error_budget_figure.py`。

**2026-09-23 Gram 两孤子新增实验：** [专题报告](MULTISOLITON_REPORT.md) 把已有解析相移 E4 扩展到有限 $h$ 两孤子背景的实际短时演化。结构/FD 两模型共同使用相同的精确初态和开链背景；记录两场瞬时缺陷、固定 $h$ 的 $x$ 加密、时间步控制，以及两种频率的背景平衡扰动。结构模型在分辨 $x$ 后更贴合有限 $h$ Gram 流形；完整求解器散射仍未验收。原始数据：[multisoliton_study.json](out/multisoliton_study.json)。复现：先运行 `python -u experiments/multisoliton_study.py`，再运行 `python experiments/multisoliton_figure.py`。

**2026-09-23 最新：** [研究主体](DYNAMICS_REPORT.md) 已落实引用会话的四个核心问题，含 20 组传播/扩域、6 组共同早期误差分解、28 组同连续初边值模型对照、16 组成对扰动（32 条轨道）、16 组成本配置各重复 3 次。早期准确性有支持，但足够传播距离的单孤子和完整两孤子散射尚未验收。图 5–10 为实测结果；先前记录保存在 [BASELINE_REPORT_20260922.md](BASELINE_REPORT_20260922.md)，总报告把它作为附录。

```powershell
python -u experiments/dynamics_study.py all
python -u experiments/dynamics_controls.py
python -u experiments/dynamics_cost.py
python -u experiments/dynamics_report.py
python -u experiments/check_regressions.py
```

成本实验应在其他计算结束后顺序运行。首次失败日志仍保留，正式分项日志与数据为 `out/dynamics_*`；新增检查和完整文件哈希为 `out/dynamics_validation_manifest.json`。科学实验未通过精度门槛与程序回归失败是不同概念。

当前结果、证据范围与复现命令见 [REPORT.md](REPORT.md)。2026-09-22 四项复审修复已落地：开链线性化和本征模检查、当前源码行为回归、E1 有限区间求积、E5 指定格点与初态周期积分。

```powershell
python -u run_all.py e1 e6 e2e3 e2e3time e5 e7
python -u experiments/check_regressions.py
python -u make_figures.py
```

完整实验可用 `python -u run_all.py`。原始结果在 `out/`；最终修复日志为 `final_four_fixes_log.txt`、`final_e6_log.txt`、`final_regressions_log.txt`。代码和产物哈希见 `out/final_validation_manifest.json`。

E6 的零背景开链线性谱是数值估计，模态时间不是非线性稳定硬界。E4 仍主要检查解析族；E2/E3 已新增六组同网格时间自收敛，分别支持 Euler/RK4/梯形的 1/4/2 阶行为（详见报告中的实际数值）；数据与源码哈希在 `out/e2_e3_self_convergence.json`。数值证据不等于 Lean 证明。
# 2026-09-23 参数误差研究更新

低频非零扰动的对照已扩展到 P1–P10 全部十组正则参数背景；P1/P2/P10 另有高频、仅 v 扰动与幅度对照。最新 `PARAMETRIC_REPORT.md` §5 包含 u/v 两场四方案误差表、参照分项检查及图 14；原 A 示例已成为具体说明而非全体结果。扩展数据与逐时刻门槛记录分别在 `out/parametric_open_parameter_sweep.json`、`out/parametric_parameter_gates.json`。

最新研究见 [PARAMETRIC_REPORT.md](PARAMETRIC_REPORT.md)，理论见 [PARAMETRIC_THEORY.md](PARAMETRIC_THEORY.md)，复现见 [PARAMETRIC_RUN.md](PARAMETRIC_RUN.md)。总报告由 `experiments/parametric_report.py` 生成。旧 `dynamics_report.py` 会覆盖总报告；若重生成旧阶段，随后必须再运行新生成器。原求解器与 Lean 未改；新边界方案改变了右端闭合，适用范围与失败结果均见最新报告。下方保留原有复现记录。
