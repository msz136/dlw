# 工作区项目与探索支线索引

登记单位是项目或独立探索支线，不是文件。索引用于定位；近期交接见 [PROGRESS_LOG.md](PROGRESS_LOG.md) 对应小节，项目长期结论以其正文为准；工作历史继续保存，默认不读。

覆盖当前 Workspaces 下 96 个工作目录；相同探索的多次运行合并登记。一个目录内的独立问题在“共享目录内的支线”单列。

## 快速入口

- 理论总览：[理论成果](theory_results.html)；DLW 数值：[数值报告](dlw_numerical.html)；当前误差比较：[初始导数与短时物理场误差](Report.html)。
- Hamilton／可积性：[结构入口](dlw_hamilton.html)、[静态理论报告](dlw_integrability.html)；一般场最新探索：[action–angle](report/dlw_general_action_angle_20261013.html)。
- 论文：[原稿](report/dlw_paper_draft.html)、[优化稿](report/dlw_paper_optimized.html)、[重写稿](report/dlw_paper_rewritten.html)；版本关系见下方论文项目。
- 文献：[本地文献目录](Paper/LITERATURE.md)；Notebook：[交付目录](notebook)、[使用说明](report/notebook_usage.html)。

## 登记与读取约定

- 新探索登记名称、问题范围、主要入口和所属目录；同题续推更新原项目，独立问题增加支线。
- 每条项目只保留一个主要入口和所属目录；证明、代码、数据、图、日志、校验和备份均归入该项目，不在总索引逐一追加。
- 同一目录有多条研究线时，在支线表区分；审查、绘图、交付及维护材料登记为对应支撑项目。
- 查阅时按关键词定位项目，只读相关条目及项目入口的必要章节；不要默认完整读取本索引、进度档、历史或遍历产物。
- 项目范围不代表该问题已解决；科学结论、成立条件与未完成项以进度和项目正文为准。

## 基础构造与形式证明

| 项目 | 探索范围 | 入口与工作目录 |
| --- | --- | --- |
| 37单位方块的构造与条件下界 | Cantrell有理构造认证、代数端点、接触支条件最小值与17块证明接口迁移；全局最优未证 | [报告](report/square37_cantrell_lean_20261014.html)；[目录](Workspaces/square37_lean_20261014) |
| 早期双线性构造 | 双线性表达与离散恒等式的初步推导 | [目录](Workspaces/analysis_A_bilinear) |
| 早期 Bäcklund 路线 | Bäcklund 变换与相容性探索 | [目录](Workspaces/analysis_codex_backlund) |
| DLW 半离散构造 | Gram 解、双线性到非线性闭合及早期数值验证 | [入口](Workspaces/dlw_semidiscrete/REPORT.md)；[目录](Workspaces/dlw_semidiscrete) |
| 对数差商离散 | 替换离散算子的推导与孤子检验 | [入口](Workspaces/dlw_log_discretization/DERIVATION.md)；[目录](Workspaces/dlw_log_discretization) |
| Lean 证明主链 | 离散恒等式、非线性化端点及证明契约 | [入口](Workspaces/lean_contracts/NEXT_TARGETS.md)；[目录](Workspaces/lean_contracts) |
| 报告端点形式化 | 综合报告中的两路非线性化证明 | [入口](Workspaces/dlw_report_formal_20261002/report.source.html)；[目录](Workspaces/dlw_report_formal_20261002) |
| τ 函数证明 | 半离散 τ 构造、Gram 恒等式与解的证明 | [入口](Workspaces/dlw_tau_proof_20261008/report.src.html)；[目录](Workspaces/dlw_tau_proof_20261008) |
| Lax 推导 | 局部相容性、势函数与半离散 Lax 表示 | [入口](Workspaces/dlw_lax_derivation_20261009/manuscript.md)；[目录](Workspaces/dlw_lax_derivation_20261009) |
| Lax 专题汇报 | Lax 推导的统一叙述与适用范围 | [入口](Workspaces/dlw_lax_briefing_20261010/manuscript.md)；[目录](Workspaces/dlw_lax_briefing_20261010) |
| DLW Miura 连接 | 连续三 τ／modified GDLW、半离散 AKNS 型势约束与 NLS／Kaup 条件约化 | [报告](report/dlw_miura_connections_20261022.html)；[目录](Workspaces/dlw_miura_connections_20261022) |
| 可积结构早期复核 | Gram、Darboux、Lax 与非线性闭合的范围审查 | [入口](Workspaces/dlw_integrability_audit_20261002/SCOPE_AUDIT.md)；[目录](Workspaces/dlw_integrability_audit_20261002) |
| 早期多路线探索 | 有限差分、谱法、FEM/DG、SBP、Hamilton/Poisson、变分、多辛、Hirota/Bäcklund、Toda；各次运行作为同一项目的版本 | [运行1](Workspaces/expression_deepseek-v4-flash_20260917_220258)、[运行2](Workspaces/expression_deepseek-v4.1-flash_20260917_222927)、[运行3](Workspaces/expression_glm-5.3-flash_20260917_225005)、[运行4](Workspaces/expression_union-alpha_20260917_221034) |
| 既有 Lean Toda 工程 | 既有 Toda／DLW 构造与 Lean 工程 | [目录](lean-toda) |

## Hamilton、守恒与谱可积性

| 项目 | 探索范围 | 入口与工作目录 |
| --- | --- | --- |
| 原 Hamilton 结构 | 周期约化、非周期背景与相对 Hamilton 构造 | [入口](Workspaces/dlw_hamilton_20261004/report.src.html)；[目录](Workspaces/dlw_hamilton_20261004) |
| 守恒生成与层级 | 谱矩、形式对易族、连续层级及开链障碍 | [入口](Workspaces/dlw_conservation_hierarchy_20261004/OPEN_CHAIN_AND_BENCHMARKS.md)；[目录](Workspaces/dlw_conservation_hierarchy_20261004) |
| 原子 Poisson 与跨格点拼接 | 原子结构、跨 N 拼接及早期 Liouville 路线 | [入口](Workspaces/dlw_liouville_20261005/README.md)；[目录](Workspaces/dlw_liouville_20261005) |
| 周期一般场层级 | 积分独立性、Hamilton 真流与解析障碍 | [入口](Workspaces/dlw_field_liouville_20261006/THEORY.md)；[目录](Workspaces/dlw_field_liouville_20261006) |
| 一般场与平均模态 | 矩阵 Lax、Poisson、两格点逆与 mixed 时间 | [入口](Workspaces/dlw_general_field_20261006/README.md)；[目录](Workspaces/dlw_general_field_20261006) |
| 一般周期可积性形式化 | balanced 系数与可积性证明链 | [入口](Workspaces/dlw_integrability_lean_20261006/LEAN_PROOF_REPORT.md)；[目录](Workspaces/dlw_integrability_lean_20261006) |
| 平均模态核验 | DLW 平均相容条件的独立验证 | [入口](Workspaces/dlw_mean_modes_20261008)；[目录](Workspaces/dlw_mean_modes_20261008) |
| 一般场谱完备性恢复 | M=2、一般 M、奇异分支与原物理结构的证明及审查 | [目录](Workspaces/dlw_recovery_20261011) |
| 一般场 action–angle | 小非零背景全模态原弱辛坐标、相对角变量与原时间重构；局部定理证明稿 | [入口](Workspaces/dlw_action_angle_20261013/LOCAL_ACTION_ANGLE_THEOREM.md)；[目录](Workspaces/dlw_action_angle_20261013) |
| 守恒量、频谱与 Poisson | 周期守恒试验、孤子频谱诊断与括号结构 | [入口](Workspaces/dlw_three_tracks_20261013/README.md)；[目录](Workspaces/dlw_three_tracks_20261013) |
| 合法约化、保辛与误差 Lax | M=2 行波约化、时间映射辛缺陷与误差结构桥；六项成果摘要及相位误差机制 | [入口](Workspaces/dlw_stage2_20261013/README.md)；[目录](Workspaces/dlw_stage2_20261013) |
| 一般场可积性研究记录 | 跨会话研究状态、检查点、奇异与 mixed 分支；与恢复项目共同使用 | [入口](刘维尔可积性/README.md)；[目录](刘维尔可积性) |

## 误差理论与研究命题

| 项目 | 探索范围 | 入口与工作目录 |
| --- | --- | --- |
| 修正方程与参数响应 | 截断误差系数及参数优化 | [入口](Workspaces/dlw_modified_equation_20260926/REPORT.md)；[目录](Workspaces/dlw_modified_equation_20260926) |
| Euler 误差系数 | 系数预测与一阶时间推进的数值比较 | [入口](Workspaces/dlw_coefficient_euler_20260926/REPORT.md)；[目录](Workspaces/dlw_coefficient_euler_20260926) |
| 误差因子模型 | 参数、初始表示与误差放大的分解 | [入口](Workspaces/dlw_factor_model_20260930/REPORT.md)；[目录](Workspaces/dlw_factor_model_20260930) |
| 二阶误差界 | h² 误差估计与核验 | [入口](Workspaces/dlw_h2_bounds_20260930/REPORT.md)；[目录](Workspaces/dlw_h2_bounds_20260930) |
| 实际半离散误差机制 | PE／FD 二阶截断残差的推导与抵消、分源传播、相位及边界条带、预测后的网格排名反转 | [入口](dlw_error_composition.html)；[目录](Workspaces/dlw_error_mechanism_20261013) |
| 理论命题总线 T01–T04 | 结构参数、坐标表示、孤子形变与精度数据空间 | [入口](Workspaces/dlw_research_pipeline_20261001/RESEARCH_NOTES.md)；[目录](Workspaces/dlw_research_pipeline_20261001) |
| T01：结构参数优化上限 | 谱范围校准与共同初值物理响应下界 | [入口](Workspaces/dlw_theory_parameter_limits_20261001/REPORT.md)；[目录](Workspaces/dlw_theory_parameter_limits_20261001) |
| T03：孤子二阶形变 | 谱与相位重标记不可去的物理形变 | [入口](Workspaces/dlw_theory_soliton_geometry_20261001/THEORY.md)；[目录](Workspaces/dlw_theory_soliton_geometry_20261001) |
| T04：高阶精度适用域 | Gaussian 数据空间、联合极限与可信时间 | [入口](Workspaces/dlw_theory_precision_domain_20261001/THEORY_AUDIT.md)；[目录](Workspaces/dlw_theory_precision_domain_20261001) |
| 理论成果盘点 | 证明来源、成果范围与理论总览生成 | [入口](Workspaces/theory_inventory_20261002/inventory.json)；[目录](Workspaces/theory_inventory_20261002) |

## DLW 数值与网格实验

| 项目 | 探索范围 | 入口与工作目录 |
| --- | --- | --- |
| GSG／DLW 基础数值项目 | 原文方法、求解器、报告源码与 Lax 基础 | [入口](Workspaces/gsg_project/OUT_GSG_DLW_report.md)；[目录](Workspaces/gsg_project) |
| 2HS／DLW 守恒密度联合选型 | 守恒密度候选、共同物理指标与预定实验协议 | [入口](Workspaces/adaptive_mesh_research/RECOMMENDATIONS.md)；[目录](Workspaces/adaptive_mesh_research) |
| 网格密度选型 | 守恒密度候选及共同网格比较 | [入口](Workspaces/dlw_mesh_densities_20260926/REPORT.md)；[目录](Workspaces/dlw_mesh_densities_20260926) |
| 分支密度与 Euler | 不同密度分支的一阶时间实验 | [入口](Workspaces/dlw_branch_mesh_euler_20260926/REPORT.md)；[目录](Workspaces/dlw_branch_mesh_euler_20260926) |
| 对称密度与 Euler | 对称监测密度的持续动网格比较 | [入口](Workspaces/dlw_symmetric_mesh_euler_20260926/REPORT.md)；[目录](Workspaces/dlw_symmetric_mesh_euler_20260926) |
| 优势区域探索 | 参数与时刻相关的误差优势区域 | [入口](Workspaces/dlw_advantage_regions_20260926/REPORT.md)；[目录](Workspaces/dlw_advantage_regions_20260926) |
| p 参数优势带 | p 参数扫描、场间取舍与排名变化 | [入口](Workspaces/dlw_p_regions_20260926/REPORT.md)；[目录](Workspaces/dlw_p_regions_20260926) |
| 原文算例控制 | 单／双孤子、空间加密、长时与可靠性控制 | [入口](Workspaces/dlw_paper_cases_20260927/HANDOFF.md)；[目录](Workspaces/dlw_paper_cases_20260927) |
| 时间误差曲线 | 保存轨道的时间曲线与误差呈现 | [入口](Workspaces/dlw_time_curves_20260928/HANDOFF.md)；[目录](Workspaces/dlw_time_curves_20260928) |
| 第二非线性表示 SD2 | 辅助变量演化、重构与离散实现 | [入口](Workspaces/dlw_sd2_20260929/HANDOFF.md)；[目录](Workspaces/dlw_sd2_20260929) |
| SD2 物理初值对齐 | 初始逆变换、物理边界与新版比较 | [入口](Workspaces/dlw_sd2_uv_init_20260929/HANDOFF.md)；[目录](Workspaces/dlw_sd2_uv_init_20260929) |
| 单孤子共同口径 | 单孤子三离散化、时间法与网格对照 | [入口](Workspaces/dlw_single_aligned_20260929/HANDOFF.md)；[目录](Workspaces/dlw_single_aligned_20260929) |
| 二孤子配对实验 | 二孤子共同参照与空间／网格比较 | [入口](Workspaces/dlw_two_soliton_20260929/HANDOFF.md)；[目录](Workspaces/dlw_two_soliton_20260929) |
| 二孤子 Euler 补测 | 补齐二孤子一阶时间法比较 | [入口](Workspaces/dlw_two_soliton_euler_20260929/HANDOFF.md)；[目录](Workspaces/dlw_two_soliton_euler_20260929) |
| 误差证据整合 | 空间、时间与网格的同口径配对结论 | [入口](Workspaces/dlw_error_inventory_20260929/CONTROLLED_RESULTS.md)；[目录](Workspaces/dlw_error_inventory_20260929) |
| Euler 局部误差图集 | 单／双孤子双场误差热图与峰值定位 | [入口](Workspaces/dlw_waveform_fields_20261001/README.md)；[目录](Workspaces/dlw_waveform_fields_20261001) |
| 守恒密度持续动网格 | 短窗与 T=.01 密度、冻结格和高频增长控制 | [入口](Workspaces/dlw_conserved_mesh_20261002/RESEARCH_NOTES.md)；[目录](Workspaces/dlw_conserved_mesh_20261002) |
| 直接双线性 τ 推进 | τ 离散推进与物理场误差比较 | [入口](Workspaces/dlw_direct_tau_20261007/report_source.html)；[目录](Workspaces/dlw_direct_tau_20261007) |
| 早期数值修复 | 早期求解器修复材料 | [目录](Workspaces/numerics_fix_20260922) |
| 早期数值复核 | 实现、误差与修复结果审查 | [入口](Workspaces/numerics_review_20260922/RESOLUTION.md)；[目录](Workspaces/numerics_review_20260922) |

## 2HS 数值与误差研究

| 项目 | 探索范围 | 入口与工作目录 |
| --- | --- | --- |
| 2HS 综合数值研究 | GSG 方法、hodograph、空间／时间及网格比较 | [入口](Workspaces/hs_numerics_plan/GSG_STYLE_REPORT.md)；[目录](Workspaces/hs_numerics_plan) |
| 空间×时间析因与选参 | 三空间路线、多阶时间法、参数扫描与新密度 | [入口](Workspaces/hs_factorial_20260925/REPORT.md)；[目录](Workspaces/hs_factorial_20260925) |
| Rm 网格、统计与校准 | 持续动网格、独立统计验证及可积参数校准 | [入口](Workspaces/hs_conserved_mesh_20260925/REPORT.md)；[目录](Workspaces/hs_conserved_mesh_20260925) |
| 误差系数与主动选参 | 校准残差、主动选参与六路线持续动格大表 | [入口](Workspaces/hs_error_theory_20260926/index.html)；[目录](Workspaces/hs_error_theory_20260926) |
| 四格式共同点比较 | 不同格式在统一物理点的数值对照 | [入口](Workspaces/hs_four_schemes_20260927/HANDOFF.md)；[目录](Workspaces/hs_four_schemes_20260927) |
| 误差表与模型差 | 误差表数据整理及连续／离散模型差异 | [入口](Workspaces/hs_table_data_20260927/MODEL_GAP.md)；[目录](Workspaces/hs_table_data_20260927) |
| Euler 波形与参数图谱 | 双场波形、39 参数扫描与 x–p 误差分布 | [入口](Workspaces/hs_waveform_atlas_20260927/REPORT.md)；[目录](Workspaces/hs_waveform_atlas_20260927) |
| 二孤子短窗 | 双孤子短时间演化与参照控制 | [入口](Workspaces/hs_two_soliton_short_20260928/REPORT.md)；[目录](Workspaces/hs_two_soliton_short_20260928) |
| 二孤子共同点评价 | 统一物理点评价及无效单孤子参照留档 | [入口](Workspaces/hs_two_soliton_point_20260928/REPORT.md)；[目录](Workspaces/hs_two_soliton_point_20260928) |

## 论文、报告与 Notebook

| 项目 | 探索范围 | 入口与工作目录 |
| --- | --- | --- |
| DLW 论文主项目 | 正式成果整合、英文正文、Endpoint-SD／Centered-SD／FD 空间比较与时间积分、动网格与修订 | [正式整合稿](dlw-paper.html)；[既有正文](Workspaces/dlw_paper_20261009/manuscript.md)；[二维图试绘](report/dlw_heatmap_preview_20261022.html)；[目录](Workspaces/dlw_paper_20261009) |
| 论文推导与范围审查 | 草稿理论推导、适用条件与结论审查 | [入口](Workspaces/dlw_draft_audit_20261010/audit.md)；[目录](Workspaces/dlw_draft_audit_20261010) |
| 研究定位与文献对标 | 结构和数值论证的参照文献 | [入口](Workspaces/dlw_structure_benchmarks/guide.html)；[目录](Workspaces/dlw_structure_benchmarks) |
| 理论英文版本 | 理论正文英文整理 | [目录](Workspaces/dlw_theory_english_20261009) |
| DLW 理论 Notebook | 理论正文、形式证明及静态预览 | [入口](Workspaces/dlw_theory_notebook_20261008/README.md)；[目录](Workspaces/dlw_theory_notebook_20261008) |
| 可积性 Notebook | 数学审查、运行器与可积性讲稿 | [入口](Workspaces/integrability_notebook_20261007/README.md)；[目录](Workspaces/integrability_notebook_20261007) |
| 数值 Notebook 交付 | DLW／2HS 数值笔记本、保存表图与时间法扩展 | [入口](Workspaces/notebook_reports_20261006/README.md)；[目录](Workspaces/notebook_reports_20261006) |
| Notebook 独立审查 | 2HS、DLW、C–N 时间法与保存输出复核 | [目录](Workspaces/notebook_audit_20261008) |
| 静态理论报告 | 离线数学、可积性五阶段叙述及排版 | [入口](Workspaces/dlw_static_reports_20261007/README.md)；[目录](Workspaces/dlw_static_reports_20261007) |
| 静态数值报告 | 从 Notebook 保存输出生成无代码报告 | [入口](Workspaces/dlw_notebook_static_20261007/README.md)；[目录](Workspaces/dlw_notebook_static_20261007) |
| 三份 Notebook 讲稿 | 非线性化、2HS 数值与 DLW 数值的讲稿生成 | [入口](Workspaces/notebook_lectures_20261006/README.md)；[目录](Workspaces/notebook_lectures_20261006) |
| 综合报告运行器 | HTML／Notebook 集成、Lean 执行与本地启动 | [入口](Workspaces/report_notebook_20261002/README.md)；[目录](Workspaces/report_notebook_20261002) |
| Colab 交付 | 云端引导、Lean 运行与交付镜像 | [入口](Workspaces/report_colab_20261006/README.md)；[目录](Workspaces/report_colab_20261006) |
| 综合报告审查 | 旧综合报告的结果与叙述审查 | [入口](Workspaces/report_review_20260928/REVIEW.md)；[目录](Workspaces/report_review_20260928) |
| 数值报告叙述修订 | 配对误差、曲线及算法解释 | [入口](Workspaces/index_readability_20261006/algorithm_pseudocode.md)；[目录](Workspaces/index_readability_20261006) |
| 递推公式整理 | 主报告递推表达的整理材料 | [目录](Workspaces/index_recurrences_20260930) |
| 成果展示整理 | 报告目录迁移与入口组织 | [目录](Workspaces/report_organization_20261004) |
| Notebook 交付区 | 理论、2HS 数值、DLW 数值与可积性四份交付及静态资源包 | [目录](notebook) |
| 论文优化与重写版本 | 原稿、优化稿、重写稿及版本比较；并列保留，采用版本以用户选择与进度记录为准 | [入口](report/rewrite_comparison.md)；[目录](report) |

## 绘图与展示探索

| 项目 | 探索范围 | 入口与工作目录 |
| --- | --- | --- |
| DLW 场图初选 | 解析双场切片与绘图风格预览 | [目录](Workspaces/dlw_plot_preview_20261008) |
| 双场版式探索 | 盒式曲面、底面投影与热图的成组预览 | [目录](Workspaces/paired_field_preview_20261008) |
| 宽 y 双场预览 | 扩大 y 范围的二孤子数值图候选 | [目录](Workspaces/paired_field_preview_20261009) |
| 精度曲面与 KP 版式 | 数值／解析场、绝对误差及 KP 三列试画 | [目录](Workspaces/dlw_precision_surface_20261008) |
| 论文图形参考 | 原文图注、变量与版式核读 | [目录](Workspaces/paper_plot_reference_20261008) |

## 文献与原文阅读

| 项目 | 探索范围 | 入口与工作目录 |
| --- | --- | --- |
| GSG／2HS／DLW 方法核读 | 原文方法、公式与证明层级 | [入口](Workspaces/paper_reading_20261002/READING_NOTES.md)；[目录](Workspaces/paper_reading_20261002) |
| 孤子与 Darboux 阅读 | 教材与 Darboux 文献的阅读起点 | [入口](Workspaces/soliton_reading_20261002/READING_NOTES.md)；[目录](Workspaces/soliton_reading_20261002) |
| mCH LDG 论文导读 | LDG 方法、误差估计与数值实验核读 | [入口](Workspaces/paper_2608_28077_reading_20261009/notes_method.md)；[目录](Workspaces/paper_2608_28077_reading_20261009) |
| mCH LDG 数值复现 | 两套通量、五例解析参照、RK4、能量与边界控制；首版结果及未知参数检索 | [首轮报告](report/mch_ldg_reproduction_20261015.html)；[入口](复现/mch_ldg/README.md)；[目录](复现/mch_ldg) |
| 本地文献编目 | PDF 题名、来源与文献清单生成 | [目录](Workspaces/literature_catalog_20261010) |
| 文献检索与下载 | 可积方程和数值分析文献的原件与来源登记 | [目录](Workspaces/literature_download_20261010) |
| 原件与文献目录 | 论文、文献原件与来源；逐篇查阅本地文献目录 | [入口](Paper/LITERATURE.md)；[目录](Paper) |

## 工作区维护

| 项目 | 探索范围 | 入口与工作目录 |
| --- | --- | --- |
| 10/8 提交复核 | 提交范围与检查证据 | [目录](Workspaces/dlw_commit_review_20261008) |
| 10/9 提交复核 | 后续提交范围与检查证据 | [目录](Workspaces/dlw_commit_review_20261009) |
| Git 合并与恢复 | 同步、冲突与工作区恢复材料 | [目录](Workspaces/git_merge_20261009) |
| 轻量归档发布 | 论文、源码、文献与提交排除核验 | [入口](Workspaces/git_publish_20261010)；[目录](Workspaces/git_publish_20261010) |
| Git 体积整理 | 仓库快照保留与活动仓库维护 | [入口](Workspaces/git_maintenance_20261010)；[目录](Workspaces/git_maintenance_20261010) |
| 索引与项目登记整理 | 展示页盘点、项目登记、产物迁移恢复、当前交接与按月工作历史（默认不读历史） | [用途报告](report/workspace_file_purposes_20261016.html)；[清理复核](report/workspace_cleanup_review_20261016.html)；[入口](Workspaces/workspace_catalog_audit_20261013)；[目录](Workspaces/workspace_catalog_audit_20261013) |

## 共享目录内的支线

| 所属项目 | 支线 | 独立问题 | 定位 |
| --- | --- | --- | --- |
| mCH LDG 数值复现 | 直接差分对照 | 原方程FD2/FD3/FD4/Rusanov、共同物理场评价、相同自由度、网格相位与时间步控制 | [对照报告](report/mch_ldg_fd_comparison_20261015.html)；[目录](复现/mch_ldg/fd_comparison) |
| 早期多路线探索 | A：有限差分 | 有限差分格式、误差与离散恒等式 | [入口](Workspaces/expression_deepseek-v4-flash_20260917_220258/A_finite_difference) |
| 早期多路线探索 | B：谱法 | 谱离散与模态层面的精度／结构 | [入口](Workspaces/expression_deepseek-v4-flash_20260917_220258/B_spectral) |
| 早期多路线探索 | C：FEM／DG | 混合有限元与 DG 路线 | [入口](Workspaces/expression_deepseek-v4-flash_20260917_220258/C_mixed_fem_dg) |
| 早期多路线探索 | D：守恒 SBP | 守恒格式与离散分部积分 | [入口](Workspaces/expression_deepseek-v4-flash_20260917_220258/D_conservative_sbp) |
| 早期多路线探索 | E：Hamilton／Poisson | Hamilton 与 Poisson 离散构造 | [入口](Workspaces/expression_deepseek-v4-flash_20260917_220258/E_hamiltonian_poisson) |
| 早期多路线探索 | F：变分／多辛 | 变分离散与多辛结构 | [入口](Workspaces/expression_deepseek-v4-flash_20260917_220258/F_variational_multisymplectic) |
| 早期多路线探索 | G：Hirota／Bäcklund | 双线性与 Bäcklund 方法 | [入口](Workspaces/expression_deepseek-v4-flash_20260917_220258/G_hirota_backlund) |
| 早期多路线探索 | H：Toda 层级 | Toda 关联与层级构造 | [入口](Workspaces/expression_deepseek-v4-flash_20260917_220258/H_toda_hierarchy) |
| DLW 半离散构造 | 数值实现与放大诊断 | 数值设计、两路演化、注入放大与动网格诊断 | [入口](Workspaces/dlw_semidiscrete/numerics) |
| 原 Hamilton 结构 | 周期与局部结构 | 周期约化、局部结构障碍及简单候选 | [入口](Workspaces/dlw_hamilton_20261004) |
| 原 Hamilton 结构 | 非周期背景 | 原文线波、相对泛函、算子域与守恒候选 | [入口](Workspaces/dlw_hamilton_20261004/nonperiodic) |
| 守恒生成与层级 | 谱矩与开链 | 形式层级、直接密度证书、连续层级与开链范围 | [入口](Workspaces/dlw_conservation_hierarchy_20261004) |
| 一般场谱完备性恢复 | M=2 条件结构 | 非中央谱逆、原物理 trace/action 桥与条件性完备结构 | [入口](report/dlw_m2_conditional_theorem_20261011.html) |
| 一般场谱完备性恢复 | M=2 正则 Liouville | 解除冻结、regular fiber、原弱辛结构与真实 Hamilton 轨道 | [入口](report/dlw_m2_regular_liouville_20261011.html) |
| 一般场谱完备性恢复 | 一般 M 谱逆与真流 | framed/vector AKNS 状态逆、高频谱隙、norming 与有界组合场 | [入口](report/dlw_liouville_recovery_20261011.html) |
| 一般场谱完备性恢复 | 奇异／零平均／mixed 分支 | c=0、非零通量、旗标与实际 mixed 时间；独立于正则非零平均分支 | [入口](刘维尔可积性/research) |
| 一般场 action–angle | 周期与高环面 | reciprocal 周期、norming、统一 Cauchy／跳跃估计及无限状态图 | [入口](report/dlw_general_action_angle_20261013.html) |
| 一般场 action–angle | 作用量逆与原时间 | 带权作用量逆、保辛全模态坐标、小非零背景与Gaussian谱域上的原时间重构；证明审计状态查进度 | [入口](Workspaces/dlw_action_angle_20261013/RESEARCH.md) |
| 理论命题总线 T01–T04 | T02：表示可逆与动力可投影 | 离散 Q/R 重构、交替模态核及 SD／SDR 坐标等价条件 | [入口](report/dlw_research_ideas.html#T02) |
| 理论命题总线 T01–T04 | 下一步方向评议 | 谱结构约束误差、有限隙／定常约化与 Miwa 展开 | [入口](report/dlw_next_directions_20261013.html) |
| 守恒量、频谱与 Poisson | 1A：周期守恒 | 原约束流形上的积分、漂移与缺陷恒等式 | [入口](report/dlw_three_tracks_20261013.html) |
| 守恒量、频谱与 Poisson | 1B：孤子频谱 | Fourier／小波诊断及新增孤子证据判别 | [入口](report/dlw_three_tracks_20261013.html) |
| 守恒量、频谱与 Poisson | 1C：原物理 Poisson | 坐标推前、Casimir、Jacobi 与动量反例 | [入口](report/dlw_three_tracks_20261013.html) |
| 合法约化、保辛与误差 Lax | 2A：合法约化 | M=2 行波辛环域与一自由度 Liouville | [入口](report/dlw_stage2_20261013.html) |
| 合法约化、保辛与误差 Lax | 2B：时间推进保辛 | Euler／RK4／中点真实切映射与 Newton 精度 | [入口](report/dlw_stage2_20261013.html) |
| 合法约化、保辛与误差 Lax | 2C：误差 Lax 桥 | 误差 PDE、势残差与谱量缺陷 | [入口](report/dlw_stage2_20261013.html) |
| 原文算例控制 | 空间可靠性与长时动格 | 空间加密、增长诊断、长时动网格与共同参照控制 | [入口](Workspaces/dlw_paper_cases_20260927) |
| 守恒密度持续动网格 | 短窗／延长／冻结控制 | T=.001 与 T=.01、密度分支、冻结初始格和高频诊断 | [入口](Workspaces/dlw_conserved_mesh_20261002) |
| 2HS 综合数值研究 | hodograph 与局部优势 | 守恒坐标、原格式比较、长时失败与局部优势 | [入口](Workspaces/hs_numerics_plan) |
| 空间×时间析因与选参 | 参数扫描与新守恒密度 | 解析波形选参、四参数比较、Rm 密度推导与独立审查 | [入口](Workspaces/hs_factorial_20260925) |
| Rm 网格、统计与校准 | 新密度持续动网格 | 统一 ALE 下 Rm 的真实节点推进与交叉控制 | [入口](Workspaces/hs_conserved_mesh_20260925/REPORT.md) |
| Rm 网格、统计与校准 | 独立统计验证 | 随机参数配对实验、双场成功标准与敏感性复核 | [入口](Workspaces/hs_conserved_mesh_20260925/STATISTICAL_VALIDATION_REPORT.md) |
| Rm 网格、统计与校准 | 时间法与路线扩展 | 四路线×四时间方法、独立参数批次与收敛 | [入口](Workspaces/hs_conserved_mesh_20260925/TIME_METHOD_COMPARISON_REPORT.md) |
| Rm 网格、统计与校准 | 可积参数校准 | C(a) 校准、九参数比较、空间阶与 Euler 时间误差 | [入口](Workspaces/hs_conserved_mesh_20260925/PARAMETER_CALIBRATION_REPORT.md) |
| 误差系数与主动选参 | 主动选参与持续动格大表 | 残差系数选参；13 参数六路线完整持续动格比较 | [入口](Workspaces/hs_error_theory_20260926/DYNAMIC_MESH_REPORT.html) |
| DLW 论文主项目 | 理论与数值正文及双语论文排版 | 格点来源与转换、τ／Gram、PE／PF、Lax、连续极限及数值整合 | [正式整合稿](dlw-paper.html)；[既有稿](report/dlw_paper_draft.html)；[英文排版](report/dlw_paper_en_print.html)、[中文排版](report/dlw_paper_zh_print.html)；[目录](Workspaces/dlw_paper_20261009) |
| DLW 论文主项目 | 三格式数值比较与图文整合 | 四算例（A/D孤子、高斯、正弦）的RK4终态物理场；初始导数仅表，精确初始场3D、截面/热图及分格式与同轴3D误差 | [主论文图文](dlw-paper.html)；[当前误差表](Report.html)；[当前图文与核验](Workspaces/dlw_paper_20261009/spatial_ad_uv_20261025/README.md)；[图表独立审查](report/dlw_figtable_audit_20261025.html)；[英文图文草稿](report/dlw_numerical_text_20261025.html)；[报告数据入口](Workspaces/dlw_paper_20261009/report_refresh_20261024/README.md)；[图文与核验目录](Workspaces/dlw_paper_20261009/report_refresh_20261024/natural_selection_20261025)；[并行稿归档](Paper/sources/dlw_y_lattice_20261018/INDEX.md) |
| Notebook 独立审查 | 2HS／DLW／C–N 支线 | 各笔记本逐项复核及 C–N 容差、保存输出审查 | [入口](Workspaces/notebook_audit_20261008) |
| DLW 物理场重构支线 | 转移Endpoint的u首项优势至Centered解族 | 完整势与自然边场重构、匹配Gram二阶、空间扫描与五格式RK4比较 | [自然边场比较](report/dlw_natural_edge_comparison_20261024.html)；[完整势实验](report/dlw_full_potential_experiments_20261024.html)；[推导报告](report/dlw_centered_reconstruction_probe_20261023.html)；[当前入口](Workspaces/dlw_paper_20261009/spatial_audit_20261023/separated/reconstruction_probe/rerun_20261024/README.md) |
| DLW 非孤子参考解认证 | 高斯/正弦连续参考的可计算误差界 | 混合小解存在性、原初值唯一性、条件匹配/误差、解析桥梁与BLP谱理论对接；值域待解；保留残差/正则性障碍证明稿（待独立复核）；原问题未认证 | [最新匹配进展](report/dlw_reference_matching_20261024.html)；[否定路线报告](report/dlw_reference_no_go_20261024.html)；[高斯理论报告](report/dlw_reference_theory_20261024.html)；[尾部推导与高斯证明稿](Workspaces/dlw_paper_20261009/reference_certificate_20261024/TAIL_ESTIMATE_CONTINUATION.md)；[全场候选报告](report/dlw_continuum_reference_20261024.html)；[入口](Workspaces/dlw_paper_20261009/reference_certificate_20261024/README.md)；[目录](Workspaces/dlw_paper_20261009/reference_certificate_20261024) |
| DLW 兼容正弦／高斯基准 | 用户允许重选v₀=4−u₀_y的独立初始化支线 | 正向热方程参考、存在唯一性证明稿、连续全域截断界与Arb区间求值；不替代原初值认证 | [阅读报告](report/dlw_compatible_reference_20261024.html)；[证明与求值器目录](Workspaces/dlw_paper_20261009/reference_certificate_20261024/compatible_benchmarks) |
| DLW 非退化高斯／正弦基准 | 纯波形与非零Endpoint一阶v误差首项 | v₀=4−3u₀_y，仅初时配对；热方程/Laplace参考、全域误差界及四格式RK4比较；解析证明稿与独立数值核验 | [阅读报告](report/dlw_nondegenerate_reference_20261024.html)；[当前误差表](Report.html)；[证明与求值器目录](Workspaces/dlw_paper_20261009/reference_certificate_20261024/nondegenerate_benchmarks)；[比较与认证目录](Workspaces/dlw_paper_20261009/report_refresh_20261024/nondegenerate_rk4_20261024) |

## 历史索引与资源归属

- 工作历史归 `Workspaces/workspace_catalog_audit_20261013/progress_history/`，按月追加；主进度只保留本次和上次交接。仅明确追溯时检索历史，不默认读取；规则见 AGENTS.md。

- 原逐文件索引完整保存于 [历史台账](Trash/cleanup_20261016/Workspaces/workspace_catalog_audit_20261013/archive/20261013_152457_066375/FILE_INDEX.md)，只在追溯具体旧文件时按需检索。
- `report/` 与根目录 HTML 是各项目的展示输出；旧版、留档与试画保留原位置，本轮只调整登记。
- `Paper/` 的原件按文献目录查阅；旧证明／报告副本归原研究项目。`notebook/` 是交付区，静态资源归对应 Notebook 项目。
- `_lean_shared/` 是共享环境；Git、依赖、构建缓存及 `Trash/` 是环境或归档，不作为新探索项目。
- 本索引的维护数据与覆盖核验：[项目登记数据](Workspaces/workspace_catalog_audit_20261013/projects.json)、[核验结果](Workspaces/workspace_catalog_audit_20261013)。
