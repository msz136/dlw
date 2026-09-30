# 工作区逐文件索引

**DLW 固定网格二阶系数与三路线误差（2026-09-30／29）：**

- [固定网格空间二阶系数及上下界](Workspaces/dlw_h2_bounds_20260930/REPORT.md)（原文A/B/C；纯y残差、有限h余项、共同初值场误差首项初始增长率和传播条件界）
- `Workspaces/dlw_h2_bounds_20260930/single_bounds.py`、`bernstein.py`、`two_coefficients.py`、`two_strip_bounds.py`（精确有理极值包围及二孤子物理见证）
- `Workspaces/dlw_h2_bounds_20260930/velocity_bounds.py`、`remainder_bounds.py`（初始误差系数速度及有限h四阶余项）
- `Workspaces/dlw_h2_bounds_20260930/single_bounds.json`、`two_bounds.json`、`two_strip_bounds.json`、`velocity_bounds.json`、`remainder_bounds.json`（系数、包围及精确有理见证）
- `Workspaces/dlw_h2_bounds_20260930/validate_new_bounds.py`、`validate_two_coefficients.py`、`validation.json`、`make_report.py`（新界检查与报告生成）

- [单孤子配对补算交接](Workspaces/dlw_single_aligned_20260929/HANDOFF.md)（共同u/v及相容边界；三空间×两时间×两网格；156条，140新算/16复用；未改报告）
- `Workspaces/dlw_single_aligned_20260929/experiment.py`、`verify.py`、`audit.py`、`implementation_checks.json`（运行、单孤子适配核验与独立场读回）
- `Workspaces/dlw_single_aligned_20260929/out/index_t001.csv`、`comparison.csv`、`error_time_all.csv`、`euler_vs_rk4.csv`（可配对主表与全部误差）
- `Workspaces/dlw_single_aligned_20260929/out/control_comparisons.csv`、`fine_time_checks.csv`、`Euler_time_order.csv`、`initial_uv_matching.csv`、`evaluation_density.csv`、`qr_reconstruction.csv`（控制、时间阶、初边值和场恢复核对）
- `Workspaces/dlw_single_aligned_20260929/out/results.json`、`validation.json`、`status.csv`、`RK4/*.npz`、`Euler/*.npz`（完整计划、验收、状态、原始场和哈希）
- [index.html](index.html)（《DLW孤子数值解的误差比较》；单孤子A/B与二孤子C的三方案、两时间法、两网格配对结果；A的SD2固定格空间限制用†标记）
- `Workspaces/gsg_project/dlw_report/_src/index.md`、`_src/index.src.html`、`generate_index_report.py`（当前正文与生成入口）
- `Workspaces/index_recurrences_20260930/check_page.cjs`、`validation.json`、`recurrences_desktop.png`、`sd2_desktop.png`、`recurrences_mobile.png`（首页SD/SD2/FD递推式、连续编号与宽窄屏检查）；`before/`（修改前正文、模板、页面及同文副本）
- [CONTROLLED_RESULTS.md](Workspaces/dlw_error_inventory_20260929/CONTROLLED_RESULTS.md)（同文副本）；`check_paper.cjs`、`paper_preview/`（页面核对）；`before_paper_rewrite/`（上版存档）
- `Workspaces/dlw_error_inventory_20260929/publish_conclusions.py`、`controlled_results.fragment.html`（从交接主表生成精简报告并同步index源）；`check_index.cjs`、`index_preview/`（页面核对）；`before_uv_aligned_index/`（修改前报告/模板/页面）
- [REVIEW.md](Workspaces/dlw_error_inventory_20260929/REVIEW.md)（式7与21/22、原文参数、Euler实测、缺口与误差分析路线）
- `Workspaces/dlw_error_inventory_20260929/audit.py`、`audit.json`（56条既有轨道、1744误差及源码/场哈希读回核对）
- `Workspaces/dlw_error_inventory_20260929/euler_existing.csv`、`time_half_field_differences.csv`（原文单孤子Euler主/半步误差与完整场差）

**DLW SD2统一uv初始化复算（2026-09-29）：**

- [HANDOFF.md](Workspaces/dlw_sd2_uv_init_20260929/HANDOFF.md)（离散反求、相容物理边界、68条复算与新六方案表）
- `Workspaces/dlw_sd2_uv_init_20260929/consistent_sd2.py`、`probe_lift.py`（正式初始化/边界实现、保留的初步反求检查）
- `Workspaces/dlw_sd2_uv_init_20260929/verify.py`、`implementation_checks.json`（24初值、6边界方向导数、18有限h RHS核对）
- `Workspaces/dlw_sd2_uv_init_20260929/run_corrected.py`、`make_report.py`（只重跑SD2、读回/比较/作图）
- `Workspaces/dlw_sd2_uv_init_20260929/rk4_error_vs_time.png`、`.svg`、`euler_error_vs_time.png`、`.svg`（共同uv初值下六方案时间曲线）
- `Workspaces/dlw_sd2_uv_init_20260929/out/comparison.csv`、`SD2_before_after.csv`、`initial_uv_matching.csv`、`SD2_error_time.csv`（更新主表、前后比、初值逐点对齐及全曲线）
- `Workspaces/dlw_sd2_uv_init_20260929/out/control_comparisons.csv`、`Euler_time_order.csv`、`status.csv`、`validation.json`（控制/时间阶/状态/读回检查）
- `Workspaces/dlw_sd2_uv_init_20260929/out/results.json`、`out/RK4/*.npz`、`out/Euler/*.npz`（68轨道、参数/源码哈希、保存场及节点）
**DLW 二孤子Euler六方案（2026-09-29）：**

- [HANDOFF.md](Workspaces/dlw_two_soliton_euler_20260929/HANDOFF.md)（原参数六方案Euler主表、时间阶、RK4配对及可靠性限制）
- `Workspaces/dlw_two_soliton_euler_20260929/run_euler.py`、`make_report.py`（111轨道、读回/对照/作图）
- `Workspaces/dlw_two_soliton_euler_20260929/euler_error_vs_time.png`、`.svg`、`time_comparison_error_vs_time.png`、`.svg`（Euler六方案及moving Euler/RK4曲线）
- `Workspaces/dlw_two_soliton_euler_20260929/out/comparison.csv`、`euler_vs_rk4.csv`、`time_order.csv`（双场并列表、配对误差、场差时间观测阶）
- `Workspaces/dlw_two_soliton_euler_20260929/out/error_time_all.csv`、`control_comparisons.csv`、`fine_time_checks.csv`、`status.csv`（完整误差与控制/状态）
- `Workspaces/dlw_two_soliton_euler_20260929/out/results.json`、`validation.json`、`*.npz`（计划、哈希、原始场与节点）
**DLW 原文二孤子六方案（2026-09-29）：**

- [review/REVIEW.md](Workspaces/dlw_two_soliton_20260929/review/REVIEW.md)（独立复核、图4加密反增、SD2初始误差与下一步）；`review/audit.py`、`review/audit.json`（93轨道2226误差读回）
- [HANDOFF.md](Workspaces/dlw_two_soliton_20260929/HANDOFF.md)（图3/4/5原参数、六方案、初误差、控制门槛与短时结论）
- `Workspaces/dlw_two_soliton_20260929/reference.py`、`models.py`（完整二孤子tau参照及SD/SD2/FD适配）
- `Workspaces/dlw_two_soliton_20260929/verify.py`、`reference_checks.json`、`paper_fig345.png`（独立行列式/PDE/有限h RHS核对、原文页7参数核查图）
- `Workspaces/dlw_two_soliton_20260929/run_experiments.py`、`refine_time.py`（90主/控制轨道、3细网格减步）
- `Workspaces/dlw_two_soliton_20260929/make_report.py`、`error_vs_time.png`、`error_vs_time.svg`（读回、报告和三组双场时间曲线）
- `Workspaces/dlw_two_soliton_20260929/out/comparison.csv`、`error_time_all.csv`、`control_comparisons.csv`、`rankings.csv`、`status.csv`、`fine_time_checks.csv`（主并列表、完整误差、控制/排序/停止状态）
- `Workspaces/dlw_two_soliton_20260929/out/results.json`、`fine_time.json`、`validation.json`、`*.npz`（93轨道、源码/剖面哈希、原始场与网格）
**DLW SD2第21式数值对照（2026-09-29）：**

- [HANDOFF.md](Workspaces/dlw_sd2_20260929/HANDOFF.md)（Q/R方程、势边界、初始重构误差、SD/SD2/FD对照及空间控制限制）
- `Workspaces/dlw_sd2_20260929/sd2.py`、`run_sd2.py`、`run_controls.py`（独立SD2实现、28轨道）
- `Workspaces/dlw_sd2_20260929/check_equations.py`、`equation_checks.json`（制造场及实际RHS对有限h精确tau的18项一致性核对）
- `Workspaces/dlw_sd2_20260929/make_report.py`、`comparison_vs_time.png`、`.pdf`、`.svg`（六方案曲线及验证/报告生成）
- `Workspaces/dlw_sd2_20260929/out/comparison.csv`、`error_time_all.csv`、`control_comparisons.csv`、`time_checks.csv`（并列表、完整曲线、控制核对）
- `Workspaces/dlw_sd2_20260929/out/results.json`、`controls.json`、`validation.json`、`*.npz`（轨道、哈希、原始Q/R/u/v/节点）
**DLW 原文参数时间误差曲线（2026-09-28）：**

- [HANDOFF.md](Workspaces/dlw_time_curves_20260928/HANDOFF.md)（共同短时终点、指标、四方案与验证限制）
- `Workspaces/dlw_time_curves_20260928/error_vs_time.png`、`.pdf`、`.svg`（两原文算例的u/v误差时间曲线）
- `Workspaces/dlw_time_curves_20260928/out/error_time.csv`、`t001_t002.csv`（完整曲线及指定时刻表）
- `Workspaces/dlw_time_curves_20260928/out/results.json`、`validation.json`、`*.npz`（16轨道、核对与原始场）
- `Workspaces/dlw_time_curves_20260928/run_curves.py`、`make_report.py`（演化、读回及作图）
**2HS 原文二孤子单参数点（2026-09-28）：**

- [REPORT.md](Workspaces/hs_two_soliton_point_20260928/REPORT.md)（图 4 原始相位换算、单点时间线、连续/离散初值的不同结果及限制）
- `Workspaces/hs_two_soliton_point_20260928/run.py`、`make_comparison_figure.py`（同状态原半离散与普通移动差分、RK4 主/半步、双场剖面图）
- `Workspaces/hs_two_soliton_point_20260928/results.json`、`*_profiles.npz`、`comparison_before_failure.png`（逐时误差、失败时刻、原始场和图）；`continuous_initial/`、`exact_initial_first_run/`（保留的先前尝试）
- `Workspaces/hs_two_soliton_point_20260928/run_four_schemes.py`、`four_schemes_results.json`、`four_S*_profiles.npz`、`make_four_figure.py`、`four_schemes_line.png`（当前S1–S4在同一原文点的双场时间线）；`invalid_one_soliton_reference/`（首轮错误边界数据，禁止引用）
- `Workspaces/hs_two_soliton_point_20260928/run_four_half_dt.py`、`four_half_dt/`（S3/S4同点RK4半步核对）

**提交版报告（2026-09-27）：**

- [当前版审查](Workspaces/report_review_20260928/REVIEW.md)；`check.py`、`checks.json`、`page.json`（公式、原文式100、连续PDE点检、表格与显示核对）

- [Report.html](Report.html)（DLW两场与保留势Q/R/M非线性化、逐步变量重构；2HS原文单/二孤子Integrable与FD两方案比较）
- `Workspaces/gsg_project/dlw_report/_src/Report.md`、`_src/Report.src.html`（权威正文／生成模板）
- `Workspaces/gsg_project/dlw_report/submission_report/two_update_formulas_validation.json`、`two_update_formulas_page.png`（二孤子递推式14a/14b及初边值的页面核对）；`before_two_update_formulas_20260928/`（增补前正文及页面）
- `Workspaces/gsg_project/dlw_report/submission_report/update_formulas_validation.json`、`update_formulas_page.png`（Integrable/FD更新与恢复公式、共用RK4递推的页面核对）；`before_update_formulas_20260928/`（增补前正文及页面）
- `Workspaces/gsg_project/dlw_report/generate_submission_report.py`、`submission_report/`（单孤子及二孤子原文参数读回、rho误差图PNG/PDF、页面检查）
- `Workspaces/gsg_project/dlw_report/generate_two_soliton_section.py`（原文图4二孤子Integrable与FD两方案，从t=0初值推进至.5，x∈[-1,1]终点误差表及图；旧[-3,3]报告保存在submission_report/before_short_time_20260928/）
- [二孤子短时比较](Workspaces/hs_two_soliton_short_20260928/REPORT.md)：`run.py`、`validate.py`、`main/`、`half_dt/`、`validation.json`、`errors.csv`（3方案主/半步共6轨道、36指标独立核对、原文时间设置依据）；`paper_figure4.png`（原文第18页）
- `Workspaces/gsg_project/dlw_report/submission_report/short_time_page_validation.json`、`short_time_part2.png`（更新后页面核对）
- `Workspaces/gsg_project/dlw_report/submission_report/two_methods_validation.json`、`two_methods_page.png`（仅保留Integrable与FD后的页面/数值核对）；`before_two_methods_20260928/`（修改前报告、源文件与图表）
- `Workspaces/gsg_project/dlw_report/generate_waveform_comparison.py`、`submission_report/one_soliton_waveforms.png`、`.svg`、`two_soliton_waveforms.png`、`.svg`（单/二孤子各2×2：列Integrable/FD、行u/rho；红色解析线＋每面板121个蓝色数值点）；`waveform_validation.json`、`separate_waveform_page_validation.json`、`separate_waveform_page.png`（数据与页面核对）；`before_separate_panels_20260928/`（改图前报告与图源）
- `Workspaces/gsg_project/dlw_report/submission_report/editorial_validation.json`、`editorial_part2.png`（措辞精简后的数值、公式与页面检查）；`editorial_backup_20260928/`（修改前正文、模板、脚本及页面）

**DLW 原文图1参数点（2026-09-27）：**

- [HANDOFF.md](Workspaces/dlw_paper_cases_20260927/HANDOFF.md)（图1(a)/(b)固定参数、UV误差与未到t1的限制）
- `Workspaces/dlw_paper_cases_20260927/run.py`（双正则分支参照、40轨道和误差读回）
- `Workspaces/dlw_paper_cases_20260927/out/results.json`、`errors.csv`、`status.csv`、`summary.json`（逐时误差、停止记录、参数和源码哈希）
- `Workspaces/dlw_paper_cases_20260927/out/independent_pde_checks.json`、`*.npz`（连续PDE核对与原始场）


**2HS 四方案完整结果（2026-09-27；替代旧六组合，未改HTML）：**

- `Workspaces/hs_four_schemes_20260927/run_paper_point.py`、`paper_point/REPORT.md`（原文p5/c1/零相位/a=.005的32轨道四方案实验）
- `Workspaces/hs_four_schemes_20260927/paper_point/errors.csv`、`results.json`、`validation.json`、`*.npz`（误差、哈希、验证及数值/精确离散剖面）
- `Workspaces/hs_four_schemes_20260927/paper_point/waveforms.png`、`waveforms.pdf`（双场波形与绝对误差）


- [HANDOFF.md](Workspaces/hs_four_schemes_20260927/HANDOFF.md)（新S1–S4定义、数据接口、结论与比较限制）
- `Workspaces/hs_four_schemes_20260927/run_study.py`（四方案补算与新S3完整论文网格ALE演化）
- `Workspaces/hs_four_schemes_20260927/audit_and_handoff.py`（公式/连续一致性检查、同初始区间控制、读回与交接生成）
- `Workspaces/hs_four_schemes_20260927/out/main_wide.csv`、`main_cells.csv`（四列完整主表，1280双场值）
- `Workspaces/hs_four_schemes_20260927/out/time_half_wide.csv`、`time_half_cells.csv`、`comparisons.csv`、`all_cells.csv`（减步、配对比与全量逐格数据）
- `Workspaces/hs_four_schemes_20260927/out/plan.json`、`results.json`、`summary.json`、`validation.json`（计划、736轨道、哈希与核验）
- `Workspaces/hs_four_schemes_20260927/out/profiles/`、`domain_controls/`、`domain_control_cells.csv`（新主轨道及32条同初始区间控制；复用轨道在results中引用旧绝对路径）


**2HS 六组合表数据交接（2026-09-27；已审查并接入 HTML）：**

- [HANDOFF.md](Workspaces/hs_table_data_20260927/HANDOFF.md)（Agent交接、配置、已完成与未构造边界）
- [MODEL_GAP.md](Workspaces/hs_table_data_20260927/MODEL_GAP.md)（S1–S4的运动几何/质量通量障碍；不作一般不可积性断言）
- `Workspaces/hs_table_data_20260927/run_tables.py`、`make_handoff.py`（368配置的复用/补算、计量、逐格导出）
- `Workspaces/hs_table_data_20260927/out/html_cells.csv`、`html_cells_wide.csv`（现有8表逐格与宽表）
- `Workspaces/hs_table_data_20260927/out/expanded_cells.csv`、`expanded_cells_wide.csv`（20参数×四方法×两时刻×两配置；仅S5/S6有数值）
- `Workspaces/hs_table_data_20260927/out/time_half_cells.csv`、`all_errors.csv`（代表参数减步与所有评价网格误差）
- `Workspaces/hs_table_data_20260927/out/plan.json`、`results.json`、`summary.json`、`html_rounding_checks.csv`、`profiles/`（计划/哈希/结果/核对与新轨道，旧轨道用绝对路径引用）


**主目录数值分析重写（2026-09-27）：**

- [numerical_analysis.html](numerical_analysis.html)（GSG五方案指标 → 2HS四方案 → DLW空间方法×动/固定四方案；16张内嵌图）
- `Workspaces/gsg_project/dlw_report/_src/numerical_analysis.md`（权威正文），`_src/numerical_analysis.src.html`（生成的构建源）
- `Workspaces/gsg_project/dlw_report/sync_numerical_results.py`、`generate_numerical_report.py`（同步正文和已有实验表；再用原 `build_html.ps1` 输出根页面）
- `Workspaces/gsg_project/dlw_report/validate_numerical_report.cjs`、`_preview_numerical/validation.json`（公式、28表、三章、展开项、链接与宽窄屏核验），`numerical_report_build.json`（构建摘要）
- `Workspaces/gsg_project/dlw_report/sync_waveform_atlas.py`、`atlas_update/`（新图集S5/S6数据核对、误差图/参数比图、数据表与来源摘要；不跑演化）
- `Workspaces/gsg_project/dlw_report/gsg_figures/`（GSG原文365–368页及五Scheme结果图；页面近似峰值依据）
- `Trash/numerical_before_2hs_rewrite_20260927/`（重写前页面、源文件与同步脚本）

**Miura 与 DLW 推导报告（2026-09-26）：**

- [miura_dlw.html](miura_dlw.html)（米白色离线报告：原论文 → 方法 → 连续与半离散 DLW → 参数选择、误差阶与只含 u/v 的显式方程 → 二阶模型误差与 FD 对照）
- `Workspaces/gsg_project/dlw_report/_src/miura_dlw.src.html`（报告源文件，经 `build_html.ps1` 生成根目录 HTML）
- `Workspaces/gsg_project/dlw_report/validate_miura_report.cjs`（公式呈现、编号、链接与桌面/窄屏排版验证）
- `Workspaces/gsg_project/dlw_report/_preview_miura/`（页面预览与验证结果）
- `Workspaces/dlw_semidiscrete/verify_miura_choices.py`、`miura_choices_checks.json`（14 项符号恒等式：显式非线性方程、参数族、物理变量误差与变系数单孤子残差）
- `Workspaces/dlw_modified_equation_20260926/REPORT.md`（SD/FD 二阶残差、同谱精确解完整首项、受迫线性化误差方程与优化方向）
- `Workspaces/dlw_modified_equation_20260926/derive.py`、`symbolic.json`（24 项任意光滑函数 Taylor 与线性化恒等式）
- `Workspaces/dlw_modified_equation_20260926/measure.py`、`results.json`（四组单孤子、五档 h、纯模型误差、65 位独立微分及评价加密）
- `Workspaces/dlw_modified_equation_20260926/make_report.py`、`model_error.png`、`model_error.svg`（数据生成推导报告、科学图与 HTML 第五部分）
- `Workspaces/dlw_modified_equation_20260926/PARAMETER_OPTIMIZATION.md`（固定常数 c/κ 的空间残差二次优化、投影下限、共用系数与迁移限制）
- `Workspaces/dlw_modified_equation_20260926/optimize_residuals.py`、`optimization.json`（四剖面拟合、四剖面无重拟合对照、有限 h 残差与独立函数积分；无时间演化）
- `Workspaces/dlw_modified_equation_20260926/make_optimization_report.py`（数据生成参数优化推导与 HTML 第六部分）
- [DLW Euler 系数族比较报告](Workspaces/dlw_coefficient_euler_20260926/REPORT.md)（8波形×11方案、主/系数/加密表；Miura残差候选的实际演化检验，P5边界污染与扩域复核）
- `Workspaces/dlw_coefficient_euler_20260926/model.py`、`validate_model.py`、`model_validation.json`（统一P/v状态、固定物理h的c/κ族、18项独立/代数核验）
- `Workspaces/dlw_coefficient_euler_20260926/run.py`、`refine.py`、`boundary_control.py`（冻结418＋48＋15条Euler轨道；源码/初态哈希）
- `Workspaces/dlw_coefficient_euler_20260926/summarize.py`、`make_report.py`、`finish_docs.py`（误差回读、CSV/全表、报告与索引同步）
- `Workspaces/dlw_coefficient_euler_20260926/out/`（三份冻结JSON、481条物理场NPZ、errors.csv、summary.json、tables.md），`pilot_v1/`（4条先导与当时源码）
- [DLW 优势邻域与误差传播](Workspaces/dlw_advantage_regions_20260926/REPORT.md)（P2/P6参数盒、精确误差递推、三源传播、条件邻域半径与线性振荡频带定理）
- `Workspaces/dlw_advantage_regions_20260926/derive.py`、`symbolic.json`（12个色散/系数符号恒等式）；`error_model.py`、`validate.py`、`validation.json`（精确Jacobian、二次余项、解析x导数，8项检查）
- `Workspaces/dlw_advantage_regions_20260926/scan.py`、`propagate.py`、`initial_defect.py`（324邻域轨道、24无拟合误差预测与初始误差速度判据）
- `Workspaces/dlw_advantage_regions_20260926/out/`（冻结计划、348个场NPZ、neighborhood_ratios.csv、预测分量、全部失败点/分类与哈希审计）
- `Workspaces/dlw_advantage_regions_20260926/summarize.py`、`plot.py`、`make_report.py`、`finish_docs.py`（数据审计/科学图/报告/索引生成）；`dispersion_advantage.png/pdf`、`p6_error_sources.png/pdf`（频率判据和误差抵消图）

- [DLW 动网格密度构造](Workspaces/dlw_mesh_densities_20260926/REPORT.md)（连续/有限 h 两支守恒律、精确对称修正、正性、共同网格速度及曲率/缺陷候选；无新演化实验）
- `Workspaces/dlw_mesh_densities_20260926/verify.py`、`identity_checks.json`（14 项符号恒等式）；`snapshot.py`、`snapshots.json`（8 个参数族实例的正性/tau 检查与初始网格几何）
- `Workspaces/dlw_mesh_densities_20260926/p6_profiles.npz`、`plot.py`、`density_geometry.png/pdf`（P6 双场、两支密度位置与初始等质量节点的科学图）

- [DLW 两支自然密度持续动网格 Euler 比较](Workspaces/dlw_branch_mesh_euler_20260926/REPORT.md)（8参数、FD/SD×固定/r−/r+，主/加密表、增长反例及共同连续物理场总误差）
- `Workspaces/dlw_branch_mesh_euler_20260926/model.py`、`validate.py`、`validation.json`（共同ALE框架、两支监测通量及23项实现核验）
- `Workspaces/dlw_branch_mesh_euler_20260926/run.py`、`supplement.py`（168条主/敏感性及40条减步/微扰补测，保留失败前状态；另12先导）
- `Workspaces/dlw_branch_mesh_euler_20260926/summarize.py`、`plot.py`、`make_report.py`（哈希/场/误差回读、独立七次样条评价、科学图与数据生成报告）
- `Workspaces/dlw_branch_mesh_euler_20260926/out/`（冻结计划与JSON，正式/控制204个完整或部分NPZ、errors.csv、summary.json、main_table.md；先导另存）
- `Workspaces/dlw_branch_mesh_euler_20260926/main_error_ratios.png/pdf`、`motion_and_growth.png/pdf`（主表收益、实际节点运动及细网格增长图）

- [DLW 对称守恒密度 Euler 比较](Workspaces/dlw_symmetric_mesh_euler_20260926/REPORT.md)（新增72条，FD/SD与固定/两支匹配，主/加密表、v收益退化与失败轨道）
- `Workspaces/dlw_symmetric_mesh_euler_20260926/sym_model.py`、`verify.py`、`validation.json`（旧框架上的精确对称组合及23项核验）；`experiment.py`（冻结72条、部分失败状态保留）
- `Workspaces/dlw_symmetric_mesh_euler_20260926/analyze.py`、`refine_peaks.py`（72新＋204旧数据哈希及场/指标回读，P6细网格32/64倍共同物理点评价）
- `Workspaces/dlw_symmetric_mesh_euler_20260926/plot.py`、`make_report.py`、`symmetric_benefits.png/pdf`、`p6_tradeoff.png/pdf`（报告与双场取舍科学图）
- `Workspaces/dlw_symmetric_mesh_euler_20260926/out/`（results.json、72个NPZ、summary.json、errors.csv、main_tables.md、p6_dense_peak_check.json）

- [DLW p 参数优势带扫描](Workspaces/dlw_p_regions_20260926/REPORT.md)（a=4/q=3固定切片、条件密度排名、SD/FD候选带、时刻反转与大p增长）
- `Workspaces/dlw_p_regions_20260926/scan.py`、`refine.py`（216主扫描＋60局部确认记录，224新演化＋52匹配旧轨道，Euler）
- `Workspaces/dlw_p_regions_20260926/analyze.py`、`make_report.py`、`finish_docs.py`（276哈希/初态/误差审计、稠密评价、双场表/科学图与文档同步）
- `Workspaces/dlw_p_regions_20260926/out/`（scan/refinement冻结JSON、224新NPZ、summary.json、errors.csv、ratios.csv、full_tables.md；复用文件路径与哈希明确记录）
- `Workspaces/dlw_p_regions_20260926/sd_fd_regions.png/pdf`、`symmetric_regions.png/pdf`（同网格SD/FD比与对称/固定误差比随p变化）

**2HS 守恒密度动网格参数总体检验（2026-09-26）：**

- `Workspaces/hs_conserved_mesh_20260925/STATISTICAL_VALIDATION_PLAN.md`、`STATISTICAL_VALIDATION_REPORT.md`（冻结的 60 参数配对检验、主/次要统计结论及数值敏感性）
- `Workspaces/hs_conserved_mesh_20260925/run_statistical_validation.py`（48 条开发、120 条确认与 240 条敏感性轨道；固定随机种子与源码哈希）
- `Workspaces/hs_conserved_mesh_20260925/plot_statistical_validation.py`、`validate_statistical_results.py`（参数误差图与独立读回核验）
- `Workspaces/hs_conserved_mesh_20260925/out/statistical_validation/`（冻结参数清单、逐案例 JSON、汇总与精确检验、敏感性和图）

**2HS 新守恒密度动网格实测（2026-09-25）：**

- [2HS Euler 波形与误差图集](Workspaces/hs_waveform_atlas_20260927/index.html)、`REPORT.md`（2026-09-27；39个p、两个固定时刻；波形叠加、x/y误差、p扫描及x–p分布五类图）
- `Workspaces/hs_waveform_atlas_20260927/run_experiments.py`、`out/`（405记录：275新增、130复用；冻结清单、保存场、CSV、时间/空间敏感性和作图NPZ）
- `Workspaces/hs_waveform_atlas_20260927/make_atlas.py`、`figures/`（12张PNG与PDF科学图）；`build_report.py`、`build_html.ps1`、`_src/index.src.html`（米白图集构建），`validate_static.cjs`（公式/图片/链接静态检查；浏览器本地文件导航被安全策略拒绝）
- [2HS 持续动网格大表](Workspaces/hs_error_theory_20260926/DYNAMIC_MESH_REPORT.html)、`DYNAMIC_MESH_REPORT.md`（13参数×六方案，Euler/RK4，u/rho同格；含峰区表和实际网格运动图）
- `Workspaces/hs_error_theory_20260926/run_dynamic_mesh_table.py`、`summarize_dynamic_mesh.py`、`out_dynamic_mesh/`（414记录：392复用＋22补算，另12逐步网格核查；哈希/来源/公共点重评价/敏感性/CSV）
- `Workspaces/hs_error_theory_20260926/make_dynamic_mesh_report.py`、`build_dynamic_mesh.ps1`、`_src/dynamic_mesh.src.html`（大表与米白HTML生成），`validate_dynamic_mesh.cjs`、`preview_dynamic_mesh/`（公式、表格结构、桌面与窄屏验收），`dynamic_mesh_positions.pdf`（网格运动图）
- [2HS：从误差系数到主动选参](Workspaces/hs_error_theory_20260926/index.html)（米白色离线HTML：原可积式、校准式、胞元残差系数、主动选参及135条双场误差对照）
- `Workspaces/hs_error_theory_20260926/_src/report.template.html`、`make_report.py`、`build_html.ps1`（权威正文模板、数据表/图生成及自包含HTML构建；`_src/index.src.html`为中间生成源）
- `Workspaces/hs_error_theory_20260926/verify_theory.py`、`theory_checks.json`（14条符号恒等式、单孤子方程与峰值系数、独立胞元积分）
- `Workspaces/hs_error_theory_20260926/run_designed_cases.py`、`summarize_results.py`、`out_v2/`（冻结的五参数清单、135条正式轨道、初始/四时刻NPZ、全量CSV与敏感性；`out/`保留首轮反演故障记录）
- `Workspaces/hs_error_theory_20260926/coefficient_and_error_ratios.pdf`、`validate_report.cjs`、`preview/`（理论/实测比值图、公式/链接/桌面/窄屏检查）
- `Workspaces/hs_conserved_mesh_20260925/EULER_COMPARISON_REPORT.md`（九参数改用一阶Euler；双场并列、四档时间步、与RK4排名对照）
- `Workspaces/hs_conserved_mesh_20260925/run_euler_comparison.py`、`report_euler_comparison.py`、`out/euler_comparison/`（216条Euler轨道＋18条RK4参照减步核验；CSV、时间观测阶、评价点敏感性）
- `Workspaces/hs_conserved_mesh_20260925/ACCURACY_ORDER_COMPARISON.md`（2HS实测阶与GSG形式空间/时间阶区分；GSG固定格式(4.13)混合导数配点限制）
- `Workspaces/hs_conserved_mesh_20260925/CALIBRATION_PARAMETER_SCAN_REPORT.md`（九个p逐行、u/rho并列的未校准/校准/普通差分表；T=.25/.5及加密核验）
- `Workspaces/hs_conserved_mesh_20260925/scan_calibration_parameters.py`、`report_calibration_parameter_scan.py`、`out/calibration_parameter_scan/`（138条新轨道＋36条匹配复用记录；九参数表格CSV、原始数据及核验）
- `Workspaces/hs_conserved_mesh_20260925/PARAMETER_CALIBRATION_REPORT.md`（2026-09-26 校准后五主路线＋同变量差分对照×四时间算法；近二阶收敛及 p12/t.25 的 u 局部优势）
- `Workspaces/hs_conserved_mesh_20260925/run_parameter_calibration.py`、`validate_parameter_calibration.py`、`make_calibration_report.py`（204条矩阵/控制轨道、独立右端积分与有限格距精确解核验、数据生成报告）
- `Workspaces/hs_conserved_mesh_20260925/out/parameter_calibration/`（先导与正式 JSON、末态 NPZ、全量 CSV、核验、收敛图 PNG/PDF；旧冻结源码未改）
- `Workspaces/hs_conserved_mesh_20260925/TIME_METHOD_COMPARISON_REPORT.md`（2026-09-26 四条有定义路线×四时间算法；192条步长轨道、16条时间参照、60新参数×16方法的960条统计轨道）
- `Workspaces/hs_conserved_mesh_20260925/run_time_methods.py`、`run_time_cohort.py`（时间阶、总误差和跨时间算法的独立参数验证）
- `Workspaces/hs_conserved_mesh_20260925/out/time_methods/`（冻结清单、原始数据、统计汇总和回读核验）
- `Workspaces/hs_conserved_mesh_20260925/STATISTICAL_VALIDATION_PLAN.md`（两完整方案配对、双场多时刻收益成功率、精确二项检验；已执行，见上方统计验证报告）
- `Workspaces/hs_conserved_mesh_20260925/REPORT.md`（\(R_m\) 真正耦合推进、同框架三网格比较、交叉控制与长时限制）
- `Workspaces/hs_conserved_mesh_20260925/run_mesh_comparison.py`（统一 ALE 场求解器、RK4、初始等密度布点；本轮含交叉控制共 29 条实际轨道）
- `Workspaces/hs_conserved_mesh_20260925/validate_and_plot.py`（正性、网格有序、时间减半和近二阶空间收敛核查及图）
- `Workspaces/hs_conserved_mesh_20260925/out/`（短时/长时 JSON、末态 NPZ、验证 JSON、比较图）

**2-HS 三空间方法 × 四时间方法实测（2026-09-25）：**

- `Workspaces/hs_factorial_20260925/NEW_DENSITIES_AND_LOCAL_P.md`（新局部守恒密度、单孤子正性、11参数局部误差探索及限制）
- `Workspaces/hs_factorial_20260925/research_conserved_density.py`、`out/new_density/`（守恒/正性符号核对与密度图；新密度演化见上方新工作区）
- `Workspaces/hs_factorial_20260925/scan_local_advantage.py`、`check_local_search.py`、`out/local_p_search/`（33条局部扫描、21条控制与反演故障记录）

- `Workspaces/hs_factorial_20260925/PARAMETER_SCAN_REVIEW.md`（独立实现/指标审查、尾部误差和边界限制、同框架布点对照）
- `Workspaces/hs_factorial_20260925/review_parameter_scan.py`、`review_placement_controls.py`、`out/independent_review/`（原式符号核对、独立反演/推进及布点诊断）

- `Workspaces/hs_factorial_20260925/WAVE_PARAMETER_SELECTION.md`（解析选参：p=3/5/12 主算例、p=20 压力例、环形分支边界）
- `Workspaces/hs_factorial_20260925/select_wave_parameters.py`、`out/wave_selection/`（241 点解析扫描、参数数据与两张波形图；没有新演化）
- `Workspaces/hs_factorial_20260925/PARAMETER_SCAN_REPORT.md`（p=3/5/12/20 的 48 组合实际演化、时间/空间/边界控制、有限 a 精确解核查与三图）
- `Workspaces/hs_factorial_20260925/run_parameter_scan.py`、`audit_parameter_scan.py`（192 条主轨道、12 条细时间参照、39 条空间加密、12 条扩域、4 条有限 a 核查）
- `Workspaces/hs_factorial_20260925/validate_parameter_scan.py`、`make_parameter_report.py`（结果完整性与源码哈希验收、从 JSON 再生报告和图）
- `Workspaces/hs_factorial_20260925/out/parameter_scan/`（上述演化与控制原始 JSON、波形 NPZ、三张结果图）

- `Workspaces/hs_factorial_20260925/INTERPRETATION_AND_NEXT.md`（负收益分解、参数校准消一阶项的推导与后续实验）
- `Workspaces/hs_factorial_20260925/verify_parameter_calibration.py`、`out/parameter_calibration_identity.json`（原/校准 RHS 差的符号核对；没有新演化）

- `Workspaces/hs_factorial_20260925/REPORT.md`（12 组合报表、控制变量依据、双场误差、时间/空间/边界审计、三图）
- `Workspaces/hs_factorial_20260925/run_factorial.py`（48 条时间步扫描及 3 条细时间参照）
- `Workspaces/hs_factorial_20260925/spatial_audit.py`、`domain_audit.py`（9 条空间加密与 6 条扩域轨道）
- `Workspaces/hs_factorial_20260925/make_report.py`、`validate_results.py`（从保存数据生成图文报告及结果验收）
- `Workspaces/hs_factorial_20260925/out/`（实测 JSON 与 3 张图）

**2HS / DLW 自适应网格守恒密度调研（2026-09-25）：**

- `Workspaces/adaptive_mesh_research/RECOMMENDATIONS.md`（多种守恒密度/监测量、推导、选型理由与时间算法比较计划）
- `Workspaces/adaptive_mesh_research/EXPERIMENT_PROTOCOL.md`（v1 实验协议：密度/控制器分离、六阶段对照、确认集与胜负规则）
- `Workspaces/adaptive_mesh_research/build_experiment_matrix.py`（仅生成计划矩阵，不运行求解器）
- `Workspaces/adaptive_mesh_research/planned_matrix.json`（456 条计划记录，实际新演化为零，待 E0 与调参）
- `Workspaces/adaptive_mesh_research/verify_identities.py`（九条局部守恒恒等式的符号核对）
- `Workspaces/adaptive_mesh_research/identity_checks.json`（九条残差为零；不含演化实验）
- `Workspaces/adaptive_mesh_research/update_research_index.py`（将本轮成果合并到进度与索引）

**2-HS 数值方案（2026-09-24）：**

- `Workspaces/hs_numerics_plan/NUMERICAL_PLAN.md`（GSG 式移动网格数值设计与可编程公式）
- `Workspaces/hs_numerics_plan/REPORT.md`（已运行实验的结论、图表、局限与复现）
- `Workspaces/hs_numerics_plan/GSG_STYLE_REPORT.md`（GSG 式逐项完整报告源：解析/数值双场、误差分解、六种时间方法、网格与差分）
- `Workspaces/hs_numerics_plan/GSG_STYLE_REPORT.html`（自包含图文成品，13 张图、273 处公式）
- `Workspaces/hs_numerics_plan/LOCAL_ADVANTAGE_REPORT.md`（实际自适应动网格的局部优势、时间方法、模型误差因素及 Richardson 后处理）
- `Workspaces/hs_numerics_plan/CONSERVATIVE_HODOGRAPH.md`（2-HS 原有质量坐标及守恒加权监视器坐标的推导、适用范围）
- `Workspaces/hs_numerics_plan/hs_exact.py`（单/双孤子与物理坐标精确参照）
- `Workspaces/hs_numerics_plan/hs_solver.py`（半离散/普通动网格与时间推进）
- `Workspaces/hs_numerics_plan/hs_fixed.py`（固定网格 C–N 对照）
- `Workspaces/hs_numerics_plan/run_study.py`（完整 E1–E6 实验及 JSON/NPZ）
- `Workspaces/hs_numerics_plan/run_extended_methods.py`（一/二/四/八阶时间法、直接差分空间扫描和双孤子八阶审计）
- `Workspaces/hs_numerics_plan/adaptive_mesh_study.py`（等节点数自然/均匀/曲率网格的双场表示误差）
- `Workspaces/hs_numerics_plan/local_advantage_study.py`（非均匀质量动网格真实推进与局部参数扫描）
- `Workspaces/hs_numerics_plan/local_neighborhood_probe.py`（中心附近 27 组优势配对）
- `Workspaces/hs_numerics_plan/local_time_comparison.py`、`coarse_time_advantage.py`（时间阶与连续总误差分离）
- `Workspaces/hs_numerics_plan/model_factor_study.py`、`richardson_model.py`（格距/波形/时间因素与两格距后处理）
- `Workspaces/hs_numerics_plan/make_local_advantage_figures.py`（扩展图 11–13）
- `Workspaces/hs_numerics_plan/validate_local_advantage.py`（局部优势、时间阶和外推的逐组断言）
- `Workspaces/hs_numerics_plan/verify_conservative_hodograph.py`（加权守恒恒等式、初态等监视器质量与离散质量关系核验）
- `Workspaces/hs_numerics_plan/make_figures.py`（从实测结果生成四张图）
- `Workspaces/hs_numerics_plan/make_extended_figures.py`（扩展图 5–10）
- `Workspaces/hs_numerics_plan/build_extended_report.py`（从 Markdown 和实测图生成自包含网页）
- `Workspaces/hs_numerics_plan/validate_extended_report.js`（核对网页公式、图片和占位符）
- `Workspaces/hs_numerics_plan/validate.py`（解析 RHS、时间阶、Poisson 初态核验）
- `Workspaces/hs_numerics_plan/audit_conclusions.py`（步长、格距与区域审计）
- `Workspaces/hs_numerics_plan/perturbation_probe.py`（初态扰动对照）
- `Workspaces/hs_numerics_plan/long_window_probe.py`（保留长窗失败的复现）
- `Workspaces/hs_numerics_plan/error_budget.py`（移动坐标的逐点可加误差分解）
- `Workspaces/hs_numerics_plan/requirements.txt`（运行依赖）
- `Workspaces/hs_numerics_plan/verify_formulas.py`（方程化简及单/双孤子精确核对）
- `Workspaces/hs_numerics_plan/formula_checks.json`（核对结果；未运行时间积分）
- `Workspaces/hs_numerics_plan/out/`（实测 JSON、NPZ、十三张图与网页校验记录）
- `Workspaces/hs_numerics_plan/references/`（原文关键页的只读渲染图）

**近期研究文件：**

- `Workspaces/dlw_semidiscrete/BILINEAR_TO_NONLINEAR_REVIEW.md`（双线性到非线性的现行推导、短式与替代变换）
- `Workspaces/dlw_semidiscrete/ALTERNATIVE_DISCRETIZATIONS.md`（孤子与 τ 保持的非唯一性、条件唯一性）
- `Workspaces/dlw_semidiscrete/verify_alternative_discretizations.py`（有理数逐系数核对）
- `Workspaces/dlw_semidiscrete/numerics/PARAMETER_REGION_ERROR_REPORT.md`
- `Workspaces/dlw_semidiscrete/numerics/experiments/parameter_region_bound_diagnostic.py`
- `Workspaces/dlw_semidiscrete/numerics/design/parameter_region_bound_diagnostic.json`
- `Workspaces/dlw_semidiscrete/numerics/References/chatgpt_6ab32716/conversation.md`
- `Workspaces/dlw_semidiscrete/numerics/References/chatgpt_6ab32716/messages.json`
- `Workspaces/dlw_semidiscrete/numerics/References/chatgpt_6ab32716/README.md`

生成日期：2026-09-23。相对路径以 `C:\Users\msz\aca` 为根；共 3931 个文件（2026-09-23 新增 PROGRESS_LOG.md）。

收录根目录成品、Paper 与 Workspaces 的自有文件和实验数据；不展开 Trash、_lean_shared、lean-toda、第三方 KaTeX 包、.research_deps 与缓存。Lean 文件仅只读列名，不移动或修改。


## (根目录)

- `.gitignore`
- `AGENTS.md`
- `FILE_INDEX.md`
- `index.html`
- `lean_verification.html`
- `numerical_analysis.html`
- `PROGRESS_LOG.md`
- `PROGRESS_LOG.md`

## Paper/dlw_semidiscrete/lean_contracts

- `Paper/dlw_semidiscrete/lean_contracts/build_dashboard.py`
- `Paper/dlw_semidiscrete/lean_contracts/C22_C23_PROOF_NOTES.md`
- `Paper/dlw_semidiscrete/lean_contracts/Contracts.lean`
- `Paper/dlw_semidiscrete/lean_contracts/INTEGRATION_STATUS.md`
- `Paper/dlw_semidiscrete/lean_contracts/page_validation_current.json`
- `Paper/dlw_semidiscrete/lean_contracts/page_validation.json`
- `Paper/dlw_semidiscrete/lean_contracts/README.md`
- `Paper/dlw_semidiscrete/lean_contracts/status.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_181354_2a22d465

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_181354_2a22d465/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_181354_2a22d465/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_181557_1b820437

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_181557_1b820437/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_181557_1b820437/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_181757_2c457654

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_181757_2c457654/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_181757_2c457654/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_181821_4272acef

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_181821_4272acef/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_181821_4272acef/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_181851_582359eb

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_181851_582359eb/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_181851_582359eb/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_181916_5d95ceb9

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_181916_5d95ceb9/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_181916_5d95ceb9/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_181944_7c6a7061

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_181944_7c6a7061/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_181944_7c6a7061/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182006_ea855b8a

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182006_ea855b8a/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182006_ea855b8a/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182123_257b8f7e

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182123_257b8f7e/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182123_257b8f7e/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182146_d5657b08

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182146_d5657b08/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182146_d5657b08/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182210_50b0ef65

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182210_50b0ef65/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182210_50b0ef65/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182232_801b291a

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182232_801b291a/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182232_801b291a/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182251_99789bab

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182251_99789bab/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182251_99789bab/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182315_775b3b28

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182315_775b3b28/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182315_775b3b28/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182322_90262916

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182322_90262916/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182322_90262916/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182344_b745b219

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182344_b745b219/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182344_b745b219/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182415_183fef73

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182415_183fef73/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182415_183fef73/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182436_77445033

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182436_77445033/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182436_77445033/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182457_1e7af0c4

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182457_1e7af0c4/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182457_1e7af0c4/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182520_571f609e

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182520_571f609e/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182520_571f609e/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182600_9aaac342

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182600_9aaac342/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182600_9aaac342/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182621_bc6a9dde

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182621_bc6a9dde/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182621_bc6a9dde/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182656_7ef67c47

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182656_7ef67c47/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182656_7ef67c47/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182731_7051c843

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182731_7051c843/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182731_7051c843/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182755_7ecac447

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182755_7ecac447/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182755_7ecac447/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182824_14cf8262

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182824_14cf8262/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182824_14cf8262/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182840_c4eed0c4

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182840_c4eed0c4/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182840_c4eed0c4/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182910_f8616238

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182910_f8616238/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182910_f8616238/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_182938_4253b291

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182938_4253b291/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_182938_4253b291/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_183122_a68450bc

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183122_a68450bc/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183122_a68450bc/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_183145_4e48f444

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183145_4e48f444/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183145_4e48f444/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_183204_2a75de00

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183204_2a75de00/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183204_2a75de00/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_183220_30ab388c

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183220_30ab388c/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183220_30ab388c/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_183256_da01f3e8

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183256_da01f3e8/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183256_da01f3e8/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_183315_fac6af9e

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183315_fac6af9e/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183315_fac6af9e/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_183353_90e67304

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183353_90e67304/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183353_90e67304/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_183438_1fef615f

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183438_1fef615f/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183438_1fef615f/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_183500_5e280d2d

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183500_5e280d2d/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183500_5e280d2d/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_183520_03676da0

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183520_03676da0/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183520_03676da0/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_183658_fce6d306

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183658_fce6d306/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183658_fce6d306/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_183752_f0577609

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183752_f0577609/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183752_f0577609/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_183822_53b4576c

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183822_53b4576c/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183822_53b4576c/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_183909_6d1f24a0

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183909_6d1f24a0/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183909_6d1f24a0/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_183943_a9812cc2

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183943_a9812cc2/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_183943_a9812cc2/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184027_108df16f

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184027_108df16f/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184027_108df16f/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184103_3507a95a

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184103_3507a95a/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184103_3507a95a/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184128_54128932

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184128_54128932/build.log`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184128_54128932/lib/lean

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184128_54128932/lib/lean/Probe.olean`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184128_54128932

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184128_54128932/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184205_dda8173a

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184205_dda8173a/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184205_dda8173a/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184236_c99ce2a5

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184236_c99ce2a5/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184236_c99ce2a5/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184322_5b7e3c7f

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184322_5b7e3c7f/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184322_5b7e3c7f/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184354_97fdc279

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184354_97fdc279/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184354_97fdc279/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184424_69e20ed1

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184424_69e20ed1/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184424_69e20ed1/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184500_44cfcb6b

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184500_44cfcb6b/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184500_44cfcb6b/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184529_ba2c65b1

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184529_ba2c65b1/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184529_ba2c65b1/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184613_d189bc09

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184613_d189bc09/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184613_d189bc09/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184650_ab307ad7

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184650_ab307ad7/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184650_ab307ad7/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184721_73ef1c06

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184721_73ef1c06/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184721_73ef1c06/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184756_a61dd363

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184756_a61dd363/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184756_a61dd363/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184823_a339098c

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184823_a339098c/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184823_a339098c/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184856_8327cdc5

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184856_8327cdc5/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184856_8327cdc5/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_184947_f0ff7099

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184947_f0ff7099/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_184947_f0ff7099/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185037_7cb9e60d

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185037_7cb9e60d/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185037_7cb9e60d/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185101_b9f0f665

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185101_b9f0f665/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185101_b9f0f665/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185133_07f858cd

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185133_07f858cd/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185133_07f858cd/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185155_4171ab85

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185155_4171ab85/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185155_4171ab85/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185217_48255442

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185217_48255442/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185217_48255442/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185241_1b1c657b

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185241_1b1c657b/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185241_1b1c657b/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185310_5cbeafe4

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185310_5cbeafe4/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185310_5cbeafe4/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185344_cb7f26ac

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185344_cb7f26ac/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185344_cb7f26ac/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185410_43430561

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185410_43430561/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185410_43430561/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185425_bcefd39f

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185425_bcefd39f/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185425_bcefd39f/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185515_8953edf6

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185515_8953edf6/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185515_8953edf6/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185543_ec7b0260

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185543_ec7b0260/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185543_ec7b0260/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185623_33176651

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185623_33176651/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185623_33176651/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185705_c5240409

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185705_c5240409/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185705_c5240409/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185730_ab83370b

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185730_ab83370b/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185730_ab83370b/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185812_26be2a5e

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185812_26be2a5e/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185812_26be2a5e/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185845_468eb6b0

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185845_468eb6b0/build.log`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185845_468eb6b0/lib/lean

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185845_468eb6b0/lib/lean/Probe.olean`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185845_468eb6b0

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185845_468eb6b0/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_185926_77baa499

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185926_77baa499/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_185926_77baa499/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_190006_5367c0ec

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190006_5367c0ec/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190006_5367c0ec/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_190059_2d136550

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190059_2d136550/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190059_2d136550/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_190125_667b55ed

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190125_667b55ed/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190125_667b55ed/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_190201_a4aee827

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190201_a4aee827/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190201_a4aee827/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_190226_6d86a81b

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190226_6d86a81b/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190226_6d86a81b/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_190258_f26c81bf

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190258_f26c81bf/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190258_f26c81bf/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_190325_b85aebc1

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190325_b85aebc1/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190325_b85aebc1/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_190355_f6b3c608

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190355_f6b3c608/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190355_f6b3c608/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_190426_db16d80e

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190426_db16d80e/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190426_db16d80e/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_190520_e3149b15

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190520_e3149b15/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190520_e3149b15/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_190556_87e246af

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190556_87e246af/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190556_87e246af/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_190634_c35bd547

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190634_c35bd547/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190634_c35bd547/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_190719_9313fa06

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190719_9313fa06/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190719_9313fa06/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_190913_d209ce40

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190913_d209ce40/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_190913_d209ce40/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_191020_9d9d53aa

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191020_9d9d53aa/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191020_9d9d53aa/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_191203_772d1d44

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191203_772d1d44/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191203_772d1d44/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_191237_9a9277f0

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191237_9a9277f0/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191237_9a9277f0/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_191319_5ddbccf0

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191319_5ddbccf0/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191319_5ddbccf0/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_191430_b46c52f5

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191430_b46c52f5/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191430_b46c52f5/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_191502_5fc025b8

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191502_5fc025b8/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191502_5fc025b8/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_191530_a246a450

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191530_a246a450/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191530_a246a450/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_191602_5aa40c11

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191602_5aa40c11/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191602_5aa40c11/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_191637_bc9b0575

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191637_bc9b0575/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191637_bc9b0575/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_191703_b8c0a7b0

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191703_b8c0a7b0/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191703_b8c0a7b0/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_191802_cfadded5

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191802_cfadded5/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191802_cfadded5/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_191914_10943ab7

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191914_10943ab7/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_191914_10943ab7/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_192101_fdef5cd0

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192101_fdef5cd0/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192101_fdef5cd0/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_192202_b69039d5

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192202_b69039d5/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192202_b69039d5/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_192228_5c32c3ce

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192228_5c32c3ce/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192228_5c32c3ce/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_192255_bce3a194

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192255_bce3a194/build.log`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_192255_bce3a194/lib/lean

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192255_bce3a194/lib/lean/Probe.olean`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_192255_bce3a194

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192255_bce3a194/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_192403_c0143572

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192403_c0143572/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192403_c0143572/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_192443_2e5c5604

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192443_2e5c5604/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192443_2e5c5604/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_192705_638aea77

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192705_638aea77/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192705_638aea77/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_192839_5d806ae5

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192839_5d806ae5/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192839_5d806ae5/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_192905_1cfbe5b2

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192905_1cfbe5b2/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192905_1cfbe5b2/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_192938_91da67ee

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192938_91da67ee/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_192938_91da67ee/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193005_e698c26e

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193005_e698c26e/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193005_e698c26e/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193035_895b7dfc

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193035_895b7dfc/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193035_895b7dfc/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193109_8246c5fa

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193109_8246c5fa/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193109_8246c5fa/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193138_8fed47b7

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193138_8fed47b7/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193138_8fed47b7/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193206_bab6e067

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193206_bab6e067/build.log`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193206_bab6e067/lib/lean

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193206_bab6e067/lib/lean/Probe.olean`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193206_bab6e067

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193206_bab6e067/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193245_ad49b2b1

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193245_ad49b2b1/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193245_ad49b2b1/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193313_4306f317

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193313_4306f317/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193313_4306f317/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193342_a776ec52

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193342_a776ec52/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193342_a776ec52/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193406_14ebbcaf

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193406_14ebbcaf/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193406_14ebbcaf/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193430_0bb5fe7d

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193430_0bb5fe7d/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193430_0bb5fe7d/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193457_619c5c61

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193457_619c5c61/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193457_619c5c61/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193545_238f0ad9

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193545_238f0ad9/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193545_238f0ad9/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193610_b4a69ad0

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193610_b4a69ad0/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193610_b4a69ad0/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193640_75e45d07

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193640_75e45d07/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193640_75e45d07/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193703_f672c3a5

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193703_f672c3a5/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193703_f672c3a5/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193731_f403da4d

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193731_f403da4d/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193731_f403da4d/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193753_9ab5c781

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193753_9ab5c781/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193753_9ab5c781/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193816_b689109d

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193816_b689109d/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193816_b689109d/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193854_11afac2b

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193854_11afac2b/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193854_11afac2b/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193920_f5db18f7

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193920_f5db18f7/build.log`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193920_f5db18f7/lib/lean

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193920_f5db18f7/lib/lean/Probe.olean`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193920_f5db18f7

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193920_f5db18f7/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_193946_ee88f072

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193946_ee88f072/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_193946_ee88f072/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194010_ded3be4c

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194010_ded3be4c/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194010_ded3be4c/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194035_6c4a0433

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194035_6c4a0433/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194035_6c4a0433/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194058_ecd389ec

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194058_ecd389ec/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194058_ecd389ec/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194121_5130597e

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194121_5130597e/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194121_5130597e/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194150_24e56a8e

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194150_24e56a8e/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194150_24e56a8e/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194219_0da40216

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194219_0da40216/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194219_0da40216/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194243_49480f64

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194243_49480f64/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194243_49480f64/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194313_9b15ccda

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194313_9b15ccda/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194313_9b15ccda/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194336_b3585d19

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194336_b3585d19/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194336_b3585d19/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194423_b0529d81

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194423_b0529d81/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194423_b0529d81/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194451_55a6feb6

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194451_55a6feb6/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194451_55a6feb6/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194516_d24837e8

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194516_d24837e8/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194516_d24837e8/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194542_f8ceafd8

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194542_f8ceafd8/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194542_f8ceafd8/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194608_f4e367d0

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194608_f4e367d0/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194608_f4e367d0/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194637_e94d0c3c

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194637_e94d0c3c/build.log`
- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194637_e94d0c3c/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194707_88c4a647

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194707_88c4a647/build.log`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194707_88c4a647/lib/lean

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194707_88c4a647/lib/lean/DLWLaxDegenerate.olean`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194707_88c4a647

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194707_88c4a647/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194750_b461f0c6

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194750_b461f0c6/build.log`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194750_b461f0c6/lib/lean

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194750_b461f0c6/lib/lean/DLWLaxDegenerate.olean`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194750_b461f0c6

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194750_b461f0c6/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194825_be94aea7

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194825_be94aea7/build.log`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194825_be94aea7/lib/lean

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194825_be94aea7/lib/lean/DLWLaxDegenerate.olean`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194825_be94aea7

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194825_be94aea7/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194841_722f3a2f

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194841_722f3a2f/build.log`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194841_722f3a2f/lib/lean

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194841_722f3a2f/lib/lean/Probe.olean`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_194841_722f3a2f

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_194841_722f3a2f/result.json`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_195017_372289de

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_195017_372289de/build.log`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_195017_372289de/lib/lean

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_195017_372289de/lib/lean/DLWLaxDegenerate.olean`

## Paper/gsg_project/lax/lean/.lean-runs/20260919_195017_372289de

- `Paper/gsg_project/lax/lean/.lean-runs/20260919_195017_372289de/result.json`

## Paper/gsg_project/lax/lean

- `Paper/gsg_project/lax/lean/DLWLaxDegenerate.lean`
- `Paper/gsg_project/lax/lean/Probe.lean`

## Paper/refs

- `Paper/refs/ap818.pdf`
- `Paper/refs/ap818.txt`
- `Paper/refs/arxiv_dlw.xml`
- `Paper/refs/arxiv_dlw2.xml`
- `Paper/refs/arxiv_hu.xml`
- `Paper/refs/arxiv_sg.xml`
- `Paper/refs/arxiv_yu.xml`
- `Paper/refs/arxiv1406.1330.pdf`
- `Paper/refs/arxiv1406.1330.txt`
- `Paper/refs/boiti1987.pdf`
- `Paper/refs/cpb_c.pdf`
- `Paper/refs/ctp8805.pdf`
- `Paper/refs/ctp8805.txt`
- `Paper/refs/ctp9298.pdf`
- `Paper/refs/ctp9298.txt`
- `Paper/refs/fu1802.pdf`
- `Paper/refs/fu1802.txt`
- `Paper/refs/gauge0802.2334.pdf`
- `Paper/refs/gauge0802.2334.txt`
- `Paper/refs/gauge0907.3205.pdf`
- `Paper/refs/gauge0907.3205.txt`
- `Paper/refs/gordoa_full_raw.txt`
- `Paper/refs/gordoa_raw.txt`
- `Paper/refs/gordoa.pdf`
- `Paper/refs/gordoa.txt`
- `Paper/refs/hainan.pdf`
- `Paper/refs/hainan.txt`
- `Paper/refs/hannover.pdf`
- `Paper/refs/hannover.txt`
- `Paper/refs/huyu2007.json`
- `Paper/refs/jnmp_sg.pdf`
- `Paper/refs/jnmp_sg.txt`
- `Paper/refs/lump2410.20059.pdf`
- `Paper/refs/lump2410.20059.txt`
- `Paper/refs/math9804162.pdf`
- `Paper/refs/math9804162.txt`
- `Paper/refs/miura9803007.pdf`
- `Paper/refs/miura9803007.txt`
- `Paper/refs/moyal9410048.pdf`
- `Paper/refs/moyal9410048.txt`
- `Paper/refs/nivala.pdf`
- `Paper/refs/nlin0011039.pdf`
- `Paper/refs/nlin0011039.txt`
- `Paper/refs/romjphys113.pdf`
- `Paper/refs/romjphys113.txt`
- `Paper/refs/shodh_ch2.pdf`
- `Paper/refs/takasaki_aa95.pdf`
- `Paper/refs/takasaki_aa95.txt`
- `Paper/refs/toda1908.08725.pdf`
- `Paper/refs/toda1908.08725.txt`
- `Paper/refs/toda2104.06123.pdf`
- `Paper/refs/toda2104.06123.txt`

## Paper/reports

- `Paper/reports/dlw_laxpair_report.md`

## Paper/sources

- `Paper/sources/2 Huner Saxton.pdf`
- `Paper/sources/gsg.txt`
- `Paper/sources/hirota-book-new.pdf`
- `Paper/sources/Numerical_Algorithms_gsg (1).pdf`
- `Paper/sources/PhysD-published.pdf`
- `Paper/sources/physd.txt`

## Workspaces/analysis_A_bilinear

- `Workspaces/analysis_A_bilinear/derive_A_bilinear.py`
- `Workspaces/analysis_A_bilinear/more_forms_rigidity.py`
- `Workspaces/analysis_A_bilinear/n2_output.txt`
- `Workspaces/analysis_A_bilinear/n2_soliton_test.py`
- `Workspaces/analysis_A_bilinear/output.txt`
- `Workspaces/analysis_A_bilinear/rigidity_output.txt`

## Workspaces/analysis_codex_backlund

- `Workspaces/analysis_codex_backlund/backlund_raw.txt`
- `Workspaces/analysis_codex_backlund/conversation.txt`
- `Workspaces/analysis_codex_backlund/dump_conversation.py`
- `Workspaces/analysis_codex_backlund/dump_transcript.py`
- `Workspaces/analysis_codex_backlund/extract_backlund.py`
- `Workspaces/analysis_codex_backlund/probe.py`
- `Workspaces/analysis_codex_backlund/transcript.txt`

## Workspaces/dlw_semidiscrete

- `Workspaces/dlw_semidiscrete/audit_cont.py`
- `Workspaces/dlw_semidiscrete/audit_gauge.py`
- `Workspaces/dlw_semidiscrete/audit_h.py`
- `Workspaces/dlw_semidiscrete/audit_points.py`
- `Workspaces/dlw_semidiscrete/audit_tau.py`
- `Workspaces/dlw_semidiscrete/AUDIT.md`
- `Workspaces/dlw_semidiscrete/cert_result.txt`
- `Workspaces/dlw_semidiscrete/certify.py`
- `Workspaces/dlw_semidiscrete/check_1264.py`
- `Workspaces/dlw_semidiscrete/check_core.py`
- `Workspaces/dlw_semidiscrete/chk1264.txt`
- `Workspaces/dlw_semidiscrete/cmp.py`
- `Workspaces/dlw_semidiscrete/cont_nl.py`
- `Workspaces/dlw_semidiscrete/dbg_bilin.py`
- `Workspaces/dlw_semidiscrete/dbg_tau.py`
- `Workspaces/dlw_semidiscrete/dbg10.py`
- `Workspaces/dlw_semidiscrete/dbg11.py`
- `Workspaces/dlw_semidiscrete/dbg2.py`
- `Workspaces/dlw_semidiscrete/dbg3.py`
- `Workspaces/dlw_semidiscrete/dbg4.py`
- `Workspaces/dlw_semidiscrete/dbg5.py`
- `Workspaces/dlw_semidiscrete/dbg6.py`
- `Workspaces/dlw_semidiscrete/dbg7.py`
- `Workspaces/dlw_semidiscrete/dbg8.py`
- `Workspaces/dlw_semidiscrete/dbg9.py`
- `Workspaces/dlw_semidiscrete/debug.py`
- `Workspaces/dlw_semidiscrete/debug2.py`
- `Workspaces/dlw_semidiscrete/debug3.py`
- `Workspaces/dlw_semidiscrete/debug4.py`
- `Workspaces/dlw_semidiscrete/derive1.py`
- `Workspaces/dlw_semidiscrete/diag.py`
- `Workspaces/dlw_semidiscrete/dlwcommon.py`
- `Workspaces/dlw_semidiscrete/dlwcommon2.py`
- `Workspaces/dlw_semidiscrete/engine2.py`
- `Workspaces/dlw_semidiscrete/exact7.py`
- `Workspaces/dlw_semidiscrete/exact7b.py`
- `Workspaces/dlw_semidiscrete/exactexp.py`
- `Workspaces/dlw_semidiscrete/final_verdict.py`
- `Workspaces/dlw_semidiscrete/final7.py`
- `Workspaces/dlw_semidiscrete/GRAM_INTEGRABILITY_REASSESSMENT.md`
- `Workspaces/dlw_semidiscrete/gram_reassessment_results.json`
- `Workspaces/dlw_semidiscrete/h_scaling.py`
- `Workspaces/dlw_semidiscrete/hscale.txt`
- `Workspaces/dlw_semidiscrete/idcheck.py`
- `Workspaces/dlw_semidiscrete/idcheck3.py`
- `Workspaces/dlw_semidiscrete/jet.py`
- `Workspaces/dlw_semidiscrete/jet2.py`
- `Workspaces/dlw_semidiscrete/jet3.py`
- `Workspaces/dlw_semidiscrete/jet4.py`
- `Workspaces/dlw_semidiscrete/NL_RESULT.md`
- `Workspaces/dlw_semidiscrete/nlaudit.py`
- `Workspaces/dlw_semidiscrete/nlbuild.py`
- `Workspaces/dlw_semidiscrete/nlcont.py`
- `Workspaces/dlw_semidiscrete/nlexact.py`
- `Workspaces/dlw_semidiscrete/nlfinal.py`
- `Workspaces/dlw_semidiscrete/nlfinal2.py`
- `Workspaces/dlw_semidiscrete/nlfinal3.py`
- `Workspaces/dlw_semidiscrete/NLFINAL4.py`
- `Workspaces/dlw_semidiscrete/nlparams.py`
- `Workspaces/dlw_semidiscrete/nlscalar.py`
- `Workspaces/dlw_semidiscrete/nlscan.py`
- `Workspaces/dlw_semidiscrete/nlstep1.py`
- `Workspaces/dlw_semidiscrete/nlstep2.py`
- `Workspaces/dlw_semidiscrete/nlstep3.py`
- `Workspaces/dlw_semidiscrete/nlverify.py`
- `Workspaces/dlw_semidiscrete/no_result.txt`
- `Workspaces/dlw_semidiscrete/NONLINEAR_CLOSURE.md`
- `Workspaces/dlw_semidiscrete/nosearch_uniform.py`
- `Workspaces/dlw_semidiscrete/nosearch.py`

## Workspaces/dlw_semidiscrete/numerics

- `Workspaces/dlw_semidiscrete/numerics/BASELINE_REPORT_20260922.md`

## Workspaces/dlw_semidiscrete/numerics/design

- `Workspaces/dlw_semidiscrete/numerics/design/manifest.json`

## Workspaces/dlw_semidiscrete/numerics

- `Workspaces/dlw_semidiscrete/numerics/DYNAMICS_REPORT.md`
- `Workspaces/dlw_semidiscrete/numerics/ERROR_BUDGET_REPORT.md`

## Workspaces/dlw_semidiscrete/numerics/experiments

- `Workspaces/dlw_semidiscrete/numerics/experiments/amplification_controls.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/check_regressions.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/config_rule_cost.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/config_rule_lock.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/config_rule_time_holdout.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/config_rule_validate.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/dynamics_controls.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/dynamics_cost.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/dynamics_report.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/dynamics_study.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/dynamics_validate.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/e0_benchmark.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/e1_continuum.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/e2_e3_self_convergence.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/e2_e3_solver.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/e4_twosoliton.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/e5_conservation.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/e6_growth.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/e7_fd_baseline.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/initial_state_design_validate.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/initial_state_design.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/injection_amplification.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/injection_multisoliton.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/injection_validate.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/manifold_scattering_figure.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/manifold_scattering_validate.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/manifold_scattering.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_common_grid.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_continuum.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_controls.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_interval_analyze.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_interval_extended.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_interval_parameter_model.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_interval_study.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_report.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_route1_cost.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_route1_coupled.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_route1_dlw_gate.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_route1_figure.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_route1_geometry.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_route1_perturb.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_route1_replay.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_route1_transport_dt.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_route1_transport_figure.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_route1_transport.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_route1_validate.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_study.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/moving_mesh_validate.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/multisoliton_figure.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/multisoliton_study.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/parametric_assess.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/parametric_bounds.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/parametric_controls.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/parametric_cost.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/parametric_open_bounds.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/parametric_open_control.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/parametric_open_parameter_sweep.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/parametric_open_study.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/parametric_perturb.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/parametric_reference.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/parametric_report.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/parametric_study.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/parametric_validate.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/route2_adjoint.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/route2_budget.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/route2_crossparam.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/route2_figures.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/route2_validate.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/smoke_exact.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/space_error.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/two_error_budget_figure.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/two_error_budget.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/validate_derivs.py`
- `Workspaces/dlw_semidiscrete/numerics/experiments/verify_n1n2.py`

## Workspaces/dlw_semidiscrete/numerics/figures

- `Workspaces/dlw_semidiscrete/numerics/figures/fig1_e0_e1_convergence.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig10_dynamics_error_maps.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig11_parameter_errors.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig12_forced_prediction.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig13_boundary_perturbations.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig14_parameter_perturbation_matrix.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig15_multisoliton_defect.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig16_moving_mesh_comparison.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig16_two_error_budget.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig17_manifold_scattering.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig18_route2_budget.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig19_route1_mesh.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig19_route2_adjoint.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig2_e6_growth_budget.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig20_route1_transport.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig21_mesh_refresh_interval.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig3_e4_phase_shift.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig4_e2_e3_time_order.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig5_dynamics_profiles.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig6_dynamics_errors.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig7_dynamics_refinement.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig8_dynamics_comparison.png`
- `Workspaces/dlw_semidiscrete/numerics/figures/fig9_dynamics_sensitivity.png`

## Workspaces/dlw_semidiscrete/numerics

- `Workspaces/dlw_semidiscrete/numerics/INITIAL_STATE_DESIGN.md`
- `Workspaces/dlw_semidiscrete/numerics/INJECTION_AMPLIFICATION_REPORT.md`

## Workspaces/dlw_semidiscrete/numerics/lib

- `Workspaces/dlw_semidiscrete/numerics/lib/dynamics.py`
- `Workspaces/dlw_semidiscrete/numerics/lib/exact.py`
- `Workspaces/dlw_semidiscrete/numerics/lib/gramtau.py`
- `Workspaces/dlw_semidiscrete/numerics/lib/linearized.py`
- `Workspaces/dlw_semidiscrete/numerics/lib/moving_mesh.py`
- `Workspaces/dlw_semidiscrete/numerics/lib/multigram.py`
- `Workspaces/dlw_semidiscrete/numerics/lib/parametric_open.py`
- `Workspaces/dlw_semidiscrete/numerics/lib/parametric.py`
- `Workspaces/dlw_semidiscrete/numerics/lib/soliton_expansion.py`
- `Workspaces/dlw_semidiscrete/numerics/lib/solver.py`

## Workspaces/dlw_semidiscrete/numerics

- `Workspaces/dlw_semidiscrete/numerics/make_figures.py`
- `Workspaces/dlw_semidiscrete/numerics/MANIFOLD_SCATTERING_REPORT.md`
- `Workspaces/dlw_semidiscrete/numerics/MESH_REFRESH_INTERVAL_REPORT.md`
- `Workspaces/dlw_semidiscrete/numerics/MOVING_MESH_REPORT.md`
- `Workspaces/dlw_semidiscrete/numerics/MOVING_MESH_ROUTE1_REPORT.md`
- `Workspaces/dlw_semidiscrete/numerics/MULTISOLITON_REPORT.md`
- `Workspaces/dlw_semidiscrete/numerics/NEXT_STAGE_PLAN_20260923.md`

## Workspaces/dlw_semidiscrete/numerics/out

- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_checks.json`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_comparison_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_comparison.json`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_controls_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_cost_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_cost.json`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_0083145289cd.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_0411b4b83030.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_04d1541baa04.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_1395373c7fce.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_14a95b43f6ad.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_1a3cca8bfd0e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_21e5f3bd71d7.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_23eeb9a99068.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_260458343a99.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_297c4cf53a4f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_29b4dc9870b3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_361982756ad2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_488caa5126bb.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_4af43f773595.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_565474d0b579.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_576ffe8c027b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_5e839510bb84.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_647946150e42.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_675c805fc04d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_69bc2c7b63f9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_69f02e9f3961.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_6b93b5c9bc03.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_7ca62c5e2988.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_7e1fb09b943f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_8778d8cd93fc.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_8b2ea0ec2306.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_8c6c8c74d1b3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_8d59bffe2732.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_9b2508ad4780.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_9b7f66275e99.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_9b866590922d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_a4124f4b2ca1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_a9cfee8cbebd.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_aadac14df8cf.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_aae0408728d3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_ab0f9f862beb.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_b1054f88f704.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_bafd2d110cad.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_c3afd822add5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_c41ea3190305.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_d14611228c26.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_d6bd8c5d90e0.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_db3aed26a6d6.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_ddd19a640dd5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_e27dbea4b71f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_e4ba2730df0b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_e551e5f3f68f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_e910c8545ad6.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_e9bdd4dcab8d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_ed7a8c8977a0.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_eea9ccf52f59.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_eea9ff884192.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_f86bbf357e12.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_field_f9aa2cde9b61.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_model_limit.json`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_propagation_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_propagation.json`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_regressions_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_run_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_sensitivity_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_sensitivity.json`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_short_controls.json`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_validation_manifest.json`
- `Workspaces/dlw_semidiscrete/numerics/out/dynamics_verification.json`
- `Workspaces/dlw_semidiscrete/numerics/out/e0_benchmark.json`
- `Workspaces/dlw_semidiscrete/numerics/out/e1_continuum.json`
- `Workspaces/dlw_semidiscrete/numerics/out/e2_e3_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/e2_e3_self_convergence_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/e2_e3_self_convergence.json`
- `Workspaces/dlw_semidiscrete/numerics/out/e2_e3_solver.json`
- `Workspaces/dlw_semidiscrete/numerics/out/e4_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/e4_twosoliton.json`
- `Workspaces/dlw_semidiscrete/numerics/out/e5_conservation.json`
- `Workspaces/dlw_semidiscrete/numerics/out/e5_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/e6_growth.json`
- `Workspaces/dlw_semidiscrete/numerics/out/e7_fd_baseline.json`
- `Workspaces/dlw_semidiscrete/numerics/out/e7_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/final_e6_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/final_four_fixes_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/final_regressions_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/final_validation_manifest.json`
- `Workspaces/dlw_semidiscrete/numerics/out/fontlist-v3.11.0.json`

## Workspaces/dlw_semidiscrete/numerics/out/injection_amplification

- `Workspaces/dlw_semidiscrete/numerics/out/injection_amplification/holdout.json`
- `Workspaces/dlw_semidiscrete/numerics/out/injection_amplification/locked_rule.json`
- `Workspaces/dlw_semidiscrete/numerics/out/injection_amplification/locked_time_rule.json`
- `Workspaces/dlw_semidiscrete/numerics/out/injection_amplification/mechanism.json`
- `Workspaces/dlw_semidiscrete/numerics/out/injection_amplification/multisoliton.json`
- `Workspaces/dlw_semidiscrete/numerics/out/injection_amplification/p5_controls.json`
- `Workspaces/dlw_semidiscrete/numerics/out/injection_amplification/rule_cost.json`
- `Workspaces/dlw_semidiscrete/numerics/out/injection_amplification/time_holdout.json`
- `Workspaces/dlw_semidiscrete/numerics/out/injection_amplification/validation.json`

## Workspaces/dlw_semidiscrete/numerics/out

- `Workspaces/dlw_semidiscrete/numerics/out/manifold_scattering_validation.json`
- `Workspaces/dlw_semidiscrete/numerics/out/manifold_scattering.json`

## Workspaces/dlw_semidiscrete/numerics/out/moving_mesh

- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/common_grid.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P1_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P1_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P1_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P1_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P1_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P1_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P10_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P10_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P10_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P10_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P10_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P10_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P11_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P11_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P11_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P11_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P11_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P11_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P12_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P12_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P12_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P12_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P12_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P12_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P13_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P13_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P13_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P13_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P13_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P13_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P14_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P14_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P14_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P14_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P14_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P14_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P15_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P15_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P15_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P15_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P15_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P15_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P16_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P16_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P16_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P16_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P16_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P16_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P2_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P2_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P2_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P2_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P2_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P2_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P3_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P3_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P3_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P3_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P3_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P3_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P4_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P4_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P4_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P4_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P4_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P4_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P5_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P5_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P5_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P5_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P5_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P5_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P6_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P6_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P6_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P6_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P6_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P6_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P7_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P7_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P7_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P7_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P7_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P7_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P8_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P8_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P8_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P8_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P8_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P8_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P9_fd_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P9_fd_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P9_fd_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P9_structure_moving.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P9_structure_static_adaptive.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuous_P9_structure_uniform.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/continuum.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/controls.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_fd_moving_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_fd_moving_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_fd_static_adaptive_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_fd_static_adaptive_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_fd_uniform_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_fd_uniform_high_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_fd_uniform_low_256_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_fd_uniform_low_384_3p125e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_fd_uniform_low_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_fd_uniform_low_512_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_fd_uniform_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_fd_uniform_vonly_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_structure_moving_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_structure_moving_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_structure_static_adaptive_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_structure_static_adaptive_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_structure_uniform_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_structure_uniform_high_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_structure_uniform_low_256_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_structure_uniform_low_384_3p125e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_structure_uniform_low_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_structure_uniform_low_512_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_structure_uniform_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P1_structure_uniform_vonly_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_fd_moving_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_fd_moving_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_fd_static_adaptive_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_fd_static_adaptive_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_fd_uniform_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_fd_uniform_high_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_fd_uniform_low_256_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_fd_uniform_low_384_3p125e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_fd_uniform_low_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_fd_uniform_low_512_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_fd_uniform_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_fd_uniform_vonly_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_structure_moving_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_structure_moving_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_structure_static_adaptive_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_structure_static_adaptive_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_structure_uniform_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_structure_uniform_high_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_structure_uniform_low_256_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_structure_uniform_low_384_3p125e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_structure_uniform_low_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_structure_uniform_low_512_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_structure_uniform_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P10_structure_uniform_vonly_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P16_fd_uniform_low_256_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P16_fd_uniform_low_384_3p125e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P16_fd_uniform_low_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P16_fd_uniform_low_512_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P16_structure_uniform_low_256_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P16_structure_uniform_low_384_3p125e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P16_structure_uniform_low_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P16_structure_uniform_low_512_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_fd_moving_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_fd_moving_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_fd_static_adaptive_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_fd_static_adaptive_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_fd_uniform_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_fd_uniform_high_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_fd_uniform_low_256_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_fd_uniform_low_384_3p125e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_fd_uniform_low_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_fd_uniform_low_512_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_fd_uniform_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_fd_uniform_vonly_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_structure_moving_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_structure_moving_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_structure_static_adaptive_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_structure_static_adaptive_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_structure_uniform_high_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_structure_uniform_high_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_structure_uniform_low_256_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_structure_uniform_low_384_3p125e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_structure_uniform_low_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_structure_uniform_low_512_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_structure_uniform_vonly_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/ctrl_P2_structure_uniform_vonly_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/interval_extended.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/interval_quick.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/interval_study.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/interval_validation.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P1_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P1_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P1_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P1_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P1_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P1_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P1_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P1_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P1_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P1_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P1_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P1_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P1_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P1_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P10_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P10_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P10_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P10_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P10_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P10_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P10_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P10_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P10_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P10_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P10_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P10_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P10_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P10_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P11_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P11_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P11_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P11_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P11_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P11_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P11_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P11_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P11_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P11_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P11_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P11_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P11_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P11_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P12_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P12_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P12_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P12_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P12_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P12_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P12_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P12_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P12_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P12_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P12_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P12_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P12_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P12_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P13_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P13_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P13_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P13_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P13_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P13_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P13_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P13_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P13_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P13_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P13_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P13_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P13_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P13_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P14_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P14_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P14_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P14_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P14_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P14_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P14_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P14_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P14_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P14_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P14_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P14_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P14_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P14_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P15_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P15_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P15_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P15_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P15_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P15_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P15_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P15_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P15_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P15_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P15_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P15_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P15_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P15_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P16_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P16_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P16_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P16_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P16_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P16_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P16_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P16_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P16_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P16_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P16_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P16_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P16_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P16_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P2_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P2_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P2_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P2_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P2_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P2_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P2_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P2_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P2_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P2_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P2_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P2_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P2_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P2_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P3_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P3_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P3_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P3_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P3_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P3_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P3_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P3_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P3_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P3_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P3_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P3_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P3_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P3_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P4_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P4_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P4_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P4_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P4_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P4_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P4_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P4_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P4_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P4_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P4_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P4_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P4_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P4_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P5_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P5_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P5_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P5_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P5_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P5_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P5_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P5_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P5_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P5_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P5_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P5_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P5_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P5_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P6_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P6_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P6_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P6_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P6_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P6_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P6_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P6_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P6_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P6_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P6_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P6_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P6_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P6_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P7_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P7_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P7_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P7_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P7_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P7_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P7_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P7_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P7_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P7_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P7_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P7_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P7_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P7_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P8_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P8_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P8_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P8_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P8_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P8_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P8_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P8_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P8_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P8_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P8_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P8_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P8_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P8_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P9_fd_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P9_fd_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P9_fd_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P9_fd_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P9_fd_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P9_fd_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P9_fd_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P9_structure_moving_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P9_structure_moving_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P9_structure_static_adaptive_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P9_structure_static_adaptive_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P9_structure_uniform_gram_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P9_structure_uniform_pert_128_0p000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/P9_structure_uniform_pert_384_6p25e-05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/route1_cost.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/route1_coupled.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/route1_dlw_gate.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/route1_geometry.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/route1_gradient.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/route1_perturb.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/route1_replay.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/route1_transport_dt.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/route1_transport_quick.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/route1_transport.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/route1_validation.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/study.json`
- `Workspaces/dlw_semidiscrete/numerics/out/moving_mesh/validation.json`

## Workspaces/dlw_semidiscrete/numerics/out/mpl_cache

- `Workspaces/dlw_semidiscrete/numerics/out/mpl_cache/fontlist-v3.11.0.json`
- `Workspaces/dlw_semidiscrete/numerics/out/mpl_cache/fontlist-v390.json`

## Workspaces/dlw_semidiscrete/numerics/out

- `Workspaces/dlw_semidiscrete/numerics/out/multisoliton_study.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_013524f42cdc.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_04496dec0c23.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_04cd5b85d75c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_051686dfa812.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_057f4c6c50a8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_05bc7029d314.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_05d8f4e19c7a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_06a97a4e26dd.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_092acd0ff6a3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_09dc3a162c24.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_0ad45e342098.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_0b8968399e4f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_0c9ce7245adf.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_0db76899c29b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_10f1858464d6.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_1125bd2632d7.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_11e6adc176a2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_12915533fcd3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_155a24aeede8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_15c7c6016a41.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_15e9c7ae2ef5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_1a53261acf29.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_1abc856da8b5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_1cd57442170c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_1e2f662ec4a3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_1e94994655d4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_204dd0f6e2d8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_20732e4d37f4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_214457784cca.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_227a4e969b4d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_22e68098b48c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_238af2b38a04.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_24337cb49897.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_2446d4073cdb.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_2514cc78f79e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_28016ab913fd.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_2a07950c75ad.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_2ab332e8eb73.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_2bda1ca4c403.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_2c10999d4059.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_2d10c3f65b95.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_2ea1d9b4896f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_3418a241d589.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_35c9e32e153a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_38848b6f6c87.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_3937a024230e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_3a084cb06ff0.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_3b52baf3b5d3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_3c8bacc8571a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_3e4dc4644213.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_4020772dc280.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_4688351a782b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_49fe252e8f4c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_4a2570614932.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_4e9ced802ff9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_51f647402444.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_532261cafce1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_549c1e7e9dda.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_55885a01cc49.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_55e92bc1bb71.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_5607e951843f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_56db50c139c7.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_592a3bd9d6c1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_5964ac3cd20e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_5c133c3925c4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_5ce5251c8310.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_5e55fe9044f1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_603bcca0c8eb.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_648b88153d69.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_652b224246d1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_65ef638b3a8b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_65f34c212c43.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_67d8d051879c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_6954b611146e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_69d54fe828af.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_6a6a05cc575e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_6bcfa8081dba.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_6d0e7b5f65f7.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_7028149fad0c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_707abbd791fe.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_7111c51dcd9e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_71b1ad001567.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_72493f9c1792.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_73f2f4fa27e5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_74d05b8d7673.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_785e02a7356e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_7948487e9051.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_7990a5b70bc8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_7a3020fbe026.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_7dd17bebd38e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_7f39e8595ecd.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_7fba8815ab0d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_8182d32097dd.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_836f476d4a06.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_85627dcb78b7.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_864241d33cde.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_8adb3847e5a7.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_8c14de055b6a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_8cc10de56aeb.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_8f93c1a618a9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_90557eeeb54b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_960050ffa96a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_972f383f4d06.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_97788a84ea34.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_97dd890a22d0.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_9a1c91b0ba54.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_9b7d772ac160.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_9bf73665273f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_9cf826c0fea6.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_9d002b67be23.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_9f72c1b74cd2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_a010e4677dac.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_a12781338c3d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_a162fadc069c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_a201857bec0b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_a3b173349e4f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_a5b647181795.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_a926388179b8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_a9450d1a4f11.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_aadacc43cd82.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_accfc1317004.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_ad238932d727.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_ad278a8b66f8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_ad5a99686da6.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_ad7bd569708d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_assessment_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_assessment.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_b10387a1a08c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_b10a849d7ef2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_b13535fc4713.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_b733cfb2f781.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_b94dc893b691.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_bbd5173eea62.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_bc28c72da5b8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_bdccaeda8a00.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_bf19ff92a54b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_bf598bfc572f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_bounds_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_bounds.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_c0843fef4912.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_c3bce5527286.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_c5c7f3b6debe.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_c72356d4d7ec.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_c8b04dbc8bbf.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_ca53f825bc31.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_cb5c4bc977c8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_cd70326d9240.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_controls_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_cost_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_cost_run_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_cost.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_d1d7f09597dc.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_d4efa0533ce2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_da2209339b16.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_dba1ffddf734.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_dbeb0e1da970.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_dc4bc29e5694.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_defects.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_df1c21099d39.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_df34fe87f686.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_df93bb9c26f6.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_e1bacd78e2a7.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_e29d2edadf6c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_e2d2a55d2407.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_e4cad5b61d6c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_e543d9fd4cc1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_e59a56323e7e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_e640917291b3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_e79863ae4ac1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_e8d3bf5973ba.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_e9be7892fc1c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_ea1c45a8dc74.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_eab5fda21447.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_ebea20c3a117.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_ec9ea3f04179.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_ed61bf6c8a9c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_edd4208b54ec.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_f0db087da209.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_f4d2d83e132f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_f50d86c958cc.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_f6073bc87c72.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_f6f6ad17960f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_f74bffa83dc9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_f860d847b8d4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_fb5c5a0c6159.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_fc93988323a8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_fcf768186fa2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_fe8a79af57e7.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_feb7d622de5d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_finite_h.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_open_bounds_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_open_bounds.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_open_controls_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_open_controls.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_open_gates.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_open_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_open_parameter_sweep_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_open_parameter_sweep.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_open_run_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_open_verification.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_open.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_parameter_gates.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_perturb_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_perturbations.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_reference_controls.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_reference_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_regressions_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_scan_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_scan.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_time_domain_controls.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_validation_manifest.json`
- `Workspaces/dlw_semidiscrete/numerics/out/parametric_verification.json`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_0017959fe71f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_00c3a6997354.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_031968b300e8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_037bd9aa95e9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_03858c4d685d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_0566daae15a4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_0597155d3cc2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_05fa7ca9c46c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_0699627b9dac.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_07f6a257dce5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_080a9420563a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_089e0d23a2e7.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_09b82b4979a2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_0af9df47acf5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_0b2e62204988.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_0c6a5815415f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_0d9617c85ef6.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_0e1b1fc08228.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_0e2df9c83ead.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_0e4c954266ef.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_0fbbaf8eb8fe.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_0fe6363795c0.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_110bfb5c2423.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1116ad6b5e6b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_11615946ec16.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_11dac94e8eb0.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_12de95629550.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_133cd4198575.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1359713b158e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_13ec8d542854.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_13f14089196e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_140158151a9a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_140f8f52f7ad.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_141125f1888f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_14c5dd6e7e2b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_15cf31884714.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_17100ed034a0.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_17862c44e0f5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1786bc8ec7ac.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_17a4c0e4e332.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_18718bc55341.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1880d2f71ce3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_19536b8f7851.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_19d715bdabca.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_19fd9b8c53f3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1b1cd259caf9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1c3237605986.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1c4d6b29c475.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1c611510365b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1c956f31f48b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1ce799db34e2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1cf77a7d8165.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1d08d0d1daaf.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1d83cf6f4659.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1dce8f5c121f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1ddcfe850075.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1e1e09e8e447.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1f4b00f137ba.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_1fca7a3c3ae8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_206e788b0e22.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_210bf531972a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_21650d690c27.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_21961a0622f8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_219d17fd67c2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_23b4e78242d9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_23efbb4dd6e7.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_2434e159c4d1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_24629fad340f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_24aa065f6318.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_2588a87cd89d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_25d51449adff.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_289f4d01a00c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_294827a385b6.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_29ccee70e687.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_2a5310b3ecde.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_2b096e297c34.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_2b21dca6d541.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_2b72979a11a4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_2b7e808ed6d6.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_2bb4babc3f00.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_2c808079fda4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_2cc3bbf9fafe.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_2d1afdf54282.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_2d3e8eda3206.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_2d3ed6300ab7.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_2d4b65285238.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_301d8cb72b51.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_30326b38cdc5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_3054b2bec14c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_306c04fc3fcb.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_306c21cf1045.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_30b78f853d55.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_30f3c19e762e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_316cd5c83106.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_32349e25b7a2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_32a2a4fe1b65.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_33d5f449ff4c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_33e32664d46d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_340eb2810ae5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_34ee459bbc2c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_3576c4792a95.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_368c6f051290.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_370c5f6b1380.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_37199f0bdbba.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_384fa3612bfe.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_3ac06c091dfd.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_3b13c5e88946.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_3bf888ef7321.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_3c40e0886543.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_3c49c10fe8c8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_3c5929a1e958.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_3d1e6c26b35e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_3d9311b9bb5e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_3e3620ce6847.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_3e928222faf4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_401b83f37893.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_408aa2ef3ab8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_40f3f9bcc8fa.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_41d67dc3e5d8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_41edd90a8c30.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_4232ef11dc4b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_4292a5d72937.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_430031be3e59.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_433a44b0c8fd.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_43fa56d6cbeb.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_4402a7e6786a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_4604b1419715.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_463ea674f862.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_47c962c3ba6d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_484f065fa8bb.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_4859a9fbc115.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_4887a4febacc.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_48b45921dd74.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_48f6e5583fef.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_49afcbead3b4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_4a36058aa1f1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_4cfa95498b70.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_4d15fd4929d5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_4d1b0aa81f21.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_4d1f5e8de263.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_4d858f3ddaab.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_4e4c3062fc3c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_4f787c45f8a7.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_4ffb65b80dac.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_503a6faebe2e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5292743a9cb0.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_52a24bead510.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_52c8eb0213f3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_53165eed0745.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_53346ebc3ab1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5348f1563ff2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_53e39aaf90cc.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_53e831f9dc7b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5467d39b1442.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_54db64fe472c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_557c45eb1f18.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_55b07fe511cf.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5636b9b7f6ad.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_56a59848133b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_56ef350a0c90.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_56f04ce2f6f5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5775521febe0.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_57a0fc553d39.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_57a528ad5c97.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5889f44bbe12.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5912ea26e5e1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_59f9b8730714.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5a95b8ddbea8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5ae787f090ef.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5b175e14350c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5c27b35bb87c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5ccce44c8c71.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5ce49d7a3a19.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5e0a99add928.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5e1698b20e35.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5f88acec5ae5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5f97e06fb01d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_5fa052010797.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_6037124a834a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_603aa09ef49e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_6209fbae61e1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_63654f164f25.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_6365e829dba2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_63cde6e8f386.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_63db4b5fa4ec.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_6420550056e4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_6438eb287768.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_643c85ff9b44.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_644ae7685fee.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_64c377b2ecdc.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_65ec8edd2401.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_65f25cf3d0b2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_65f5e62e3256.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_6612504133a3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_668352c03127.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_67178fdd55d4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_671b22a6f1bd.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_675ae03a2d9f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_6761c33e1f71.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_67a1c301fb0a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_682f2bf0f766.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_6850586a2863.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_69b7f8b9b1c5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_6c030d185a20.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_6d47460c1cd0.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_6e2335b1b50d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_6ea5f66c653f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_6ebd7a4a9e10.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_6ed0f849722e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_6ed164c9d14c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_7055514a6c8c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_71fdc7b07484.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_7303cc9e5d16.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_73db19ed4146.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_7419ea2eb993.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_7535d8b65fbb.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_753623006d2e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_754112355004.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_75936c8e7be9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_760d2391efd5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_769039114d05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_76df660ecb37.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_76e319278d75.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_77ad9906e165.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_77d5e520126a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_77e3d19f5978.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_784f4c23c7d3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_78812ac3928e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_7a0a1079ef6c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_7a4175d916b2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_7c73a3447c1b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_7ca8e6f32220.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_7d361fee70a5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_7f0b6e471270.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_802f3a09829d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_80f53ef3d8b9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_80f7a19a5721.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_815653a3e68e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_81daa6f342c9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_825528c05fc3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_83ac5a0c411f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_83f64e417f56.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_84388a880898.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_84952c0a676c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_858fb6f06cfe.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_859e52c0778d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_868f83ce1e0d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_86e12f62ec9f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_87e32922c7d0.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_88f88d01e333.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_8a17895b0c05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_8ac02e281b25.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_8c363feffb1f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_8c7eaaf771e2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_8ca294808d96.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_8ce79bd31bf9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_8d1e7c4d6014.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_8daacce95f87.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_8e02ec144d0c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_8f5f3a2cb495.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_90e565f604c9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_928f9c1534f3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_9374fe4687a5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_93fcf8d7dd99.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_94a14fab2571.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_954a5ec0fbc9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_955d5a238132.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_95d4ebb4a7c3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_9642f6b98682.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_96edbd9bedb5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_975324ec5629.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_97c9ffa0cbaf.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_97f5e9663639.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_97f9b87a1f2f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_990fe868a544.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_99f9fa0882bb.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_9b1571ce49b0.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_9b1b655c82ec.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_9b70cbedfff3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_9c9e0e932730.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_9cb5bd8375d9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_9d38a8fc33cd.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_9e1217f08149.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_9f2c2f8be7c3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_9f75a32aeca2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_9ffb39c6e202.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a0214f61dc16.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a045daff1f83.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a134b7fd22b1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a18bbd49b28b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a24e8ead5781.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a25b064033de.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a265cccfa794.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a26e779b0e14.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a2a0cdb14422.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a2b129a17741.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a31a75dfe4cb.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a3562713bc76.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a512a30573db.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a535a977dc89.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a70790f1811f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a768f04bda07.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a84393f42e73.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a868f85fd37b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a88830eac4d4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a949bd33212b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a98fd76cc5a5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a9ca75995bae.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_a9e099dd078f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_aa250a09de8c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_aa39c3f30a6d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_aa5138c17349.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_aa8163860034.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_ad6c4b635930.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_adcd654ca535.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_ae315aa55f41.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_aea329cefab5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_af08ca7d0f47.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_afbfe7101268.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_b005252fcbdb.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_b0a904b1f19f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_b1cba0458c6f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_b1d3c845381e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_b2b94a3ca112.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_b2ce258387e1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_b364818a82b1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_b48de75770e8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_b4beff0c0d77.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_b50b93f4dff2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_b67972563520.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_b7eede8cdca2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_b839b105eb0a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_b8ad66838967.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_b93d3c4714f9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_ba199f7541a8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_ba681ca4fa64.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_bbf1ee44fbde.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_bc91e9cdecc2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_be2830c7b08e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_bf26163e6bf7.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c096732a3e5c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c09d6e70cb98.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c10d9ee96400.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c1bfa30b99aa.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c1f1838c48b4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c25a2fc8255a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c2f1d23b8ad1.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c3ca44a2095d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c3e9cfa89dc5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c4f1b32407e4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c562457c7c81.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c5c83f31c207.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c5fff61b0239.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c765b4c3e013.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c793b90dd322.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c8004cb8cb7f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c80232df897e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c891b248f662.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c8a21c5f541f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c95f90abb20a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_c9664c12531f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_cb883ec07c52.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_cd281c2c9920.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_cd3c0743e9d4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_cdb4891fb961.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_ceb175407b7c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_cf7b12d353ba.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_cf89fd82acd9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d0f3dc7bfedd.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d13679673d41.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d1549fec4730.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d18f4d6112db.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d28d7b4868a5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d2f574439f06.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d34f19b6ea39.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d4afa037b8e3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d4e46d579d1c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d501c0ab845c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d61964981611.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d621ea285c01.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d6303edb146a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d67d098e4433.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d6926d4adebc.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d6eea271888e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d7461fb71471.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_d979c67f288e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_db6d8148d00d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_dbcb4b89e82b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_dd6b0d3e1a38.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_de27d2f8a8ac.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_de87831f90e4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_dfbde3f372b4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_dfcb700d5b38.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e055b6657592.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e0bec766aa72.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e0c4292c907a.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e1358d0dd8e5.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e146cda7b935.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e1688aa7069c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e34195a42054.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e38f9fc32312.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e46d45b0acbc.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e5af18572c4e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e6aa41068507.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e6b442f15dab.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e7102641fd18.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e7514163dfd7.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e7e92b8c164b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e96457636c2d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e9b1bd3be377.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_e9e7c8d4a0b0.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_ea08dcb2df29.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_eb23e1945d65.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_ec4746efeb32.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_ed001ffa76cd.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_edd8c56b0c05.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_ee39cef427d9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_ef9928156204.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f01c00290688.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f082e9e27d14.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f0d183a8f496.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f12eb36a1ca2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f1a2d078abeb.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f1bf446a83a8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f2d016dda2ed.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f3a53a7709aa.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f3db9e396c9d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f42ccb5772c7.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f449e1446a57.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f4713204d1f8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f5691b1117e8.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f6189da6193c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f6c8a9f20a09.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f716ffdf6649.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f8661111082d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f91c6ff5eebb.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_f9a27d5a9cf6.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_fabea54fb2e2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_fbb0eaa925c0.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_fcc262c4b9a2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_fd748357daa9.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_fd8e46a18260.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_fdb28b8c6201.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_fe2ac38817fa.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_fe52e807d6e4.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_fe615543690f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_fed194c779be.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_ff041c157db2.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_ffc8e6346397.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/perturb_fff67b230789.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_A_16_1e-05_0.000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_A_16_1e-05_0.00025.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_A_16_5e-06_0.000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_A_16_5e-06_0.00025.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_A_2_1e-05_0.000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_A_2_1e-05_0.00025.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_A_2_5e-06_0.000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_A_2_5e-06_0.00025.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_B_16_1e-05_0.000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_B_16_1e-05_0.00025.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_B_16_5e-06_0.000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_B_16_5e-06_0.00025.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_B_2_1e-05_0.000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_B_2_1e-05_0.00025.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_B_2_5e-06_0.000125.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/response_B_2_5e-06_0.00025.npz`

## Workspaces/dlw_semidiscrete/numerics/out/route2

- `Workspaces/dlw_semidiscrete/numerics/out/route2/adjoint.json`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/budget.json`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/crossparam.json`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_01ee8d15d85e.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_0bd3e7543ffb.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_15e185898c84.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_1a82c6065994.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_2681fd796baa.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_27f34ea3d896.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_28425bf497a3.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_3184c9ed7fde.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_3c281a6a0437.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_41534526f01d.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_501faec89e12.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_51c8e673a06c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_676de9eec045.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_6f7d6ac39b6b.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_71145ccc075c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_756775dfc14f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_97c8e83e361c.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_b28d00b0c8cf.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_c9586c1c4551.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_d0af273d2776.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_dbfca3b57f85.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_e8e5183a963f.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_ef4d3ba05099.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_ef9ea36d6261.npz`
- `Workspaces/dlw_semidiscrete/numerics/out/route2/fields_f9b7e1770d7e.npz`

## Workspaces/dlw_semidiscrete/numerics/out/route2/mplconfig

- `Workspaces/dlw_semidiscrete/numerics/out/route2/mplconfig/fontlist-v3.11.0.json`

## Workspaces/dlw_semidiscrete/numerics/out

- `Workspaces/dlw_semidiscrete/numerics/out/run_all_log.txt`
- `Workspaces/dlw_semidiscrete/numerics/out/two_error_budget.json`

## Workspaces/dlw_semidiscrete/numerics

- `Workspaces/dlw_semidiscrete/numerics/PARAMETRIC_REPORT.md`
- `Workspaces/dlw_semidiscrete/numerics/PARAMETRIC_RUN.md`
- `Workspaces/dlw_semidiscrete/numerics/PARAMETRIC_THEORY.md`
- `Workspaces/dlw_semidiscrete/numerics/PRE_PARAMETRIC_REPORT_20260923.md`
- `Workspaces/dlw_semidiscrete/numerics/README.md`

## Workspaces/dlw_semidiscrete/numerics/References/chatgpt_6ab32716

- `Workspaces/dlw_semidiscrete/numerics/References/chatgpt_6ab32716/conversation.md`

## Workspaces/dlw_semidiscrete/numerics

- `Workspaces/dlw_semidiscrete/numerics/REPORT.md`
- `Workspaces/dlw_semidiscrete/numerics/run_all.py`
- `Workspaces/dlw_semidiscrete/numerics/summary.py`

## Workspaces/dlw_semidiscrete

- `Workspaces/dlw_semidiscrete/pin.py`
- `Workspaces/dlw_semidiscrete/REPORT.md`
- `Workspaces/dlw_semidiscrete/S_INTEGRABILITY_STATUS.md`
- `Workspaces/dlw_semidiscrete/settle.py`
- `Workspaces/dlw_semidiscrete/sol_result.txt`
- `Workspaces/dlw_semidiscrete/soliton_lattice.png`
- `Workspaces/dlw_semidiscrete/soliton_lattice.py`
- `Workspaces/dlw_semidiscrete/solo.py`
- `Workspaces/dlw_semidiscrete/solo2.py`
- `Workspaces/dlw_semidiscrete/stag_h.py`
- `Workspaces/dlw_semidiscrete/stag_h.txt`
- `Workspaces/dlw_semidiscrete/taujet.py`
- `Workspaces/dlw_semidiscrete/taujet2.py`
- `Workspaces/dlw_semidiscrete/test_v2.py`
- `Workspaces/dlw_semidiscrete/test_v4_N7.py`
- `Workspaces/dlw_semidiscrete/tiny.py`
- `Workspaces/dlw_semidiscrete/uni_id.txt`
- `Workspaces/dlw_semidiscrete/uni_identity.py`
- `Workspaces/dlw_semidiscrete/uni_result.txt`
- `Workspaces/dlw_semidiscrete/v2_final.txt`
- `Workspaces/dlw_semidiscrete/v2_result.txt`
- `Workspaces/dlw_semidiscrete/v3.py`
- `Workspaces/dlw_semidiscrete/v4_result.txt`
- `Workspaces/dlw_semidiscrete/v4.py`
- `Workspaces/dlw_semidiscrete/v5.py`
- `Workspaces/dlw_semidiscrete/verdict7.py`
- `Workspaces/dlw_semidiscrete/verify_gram_reassessment.py`
- `Workspaces/dlw_semidiscrete/verify_integrability_structure.py`
- `Workspaces/dlw_semidiscrete/verify_nl.py`
- `Workspaces/dlw_semidiscrete/verify_nl2.py`
- `Workspaces/dlw_semidiscrete/verify_nonlinear_closure.py`
- `Workspaces/dlw_semidiscrete/verify_s_spectral.py`
- `Workspaces/dlw_semidiscrete/verifynl.py`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/A_finite_difference

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/A_finite_difference/DirA.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/A_finite_difference/DirA

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/A_finite_difference/DirA/Core.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/A_finite_difference

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/A_finite_difference/lake-manifest.json`
- `Workspaces/expression_deepseek-v4-flash_20260917_220258/A_finite_difference/lakefile.lean`
- `Workspaces/expression_deepseek-v4-flash_20260917_220258/A_finite_difference/lean-toolchain`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/B_spectral

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/B_spectral/DirB.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/B_spectral/DirB

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/B_spectral/DirB/Core.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/B_spectral

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/B_spectral/lakefile.lean`
- `Workspaces/expression_deepseek-v4-flash_20260917_220258/B_spectral/lean-toolchain`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/C_mixed_fem_dg

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/C_mixed_fem_dg/DirC.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/C_mixed_fem_dg/DirC

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/C_mixed_fem_dg/DirC/Core.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/C_mixed_fem_dg

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/C_mixed_fem_dg/lakefile.lean`
- `Workspaces/expression_deepseek-v4-flash_20260917_220258/C_mixed_fem_dg/lean-toolchain`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/common

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/common/SHARED_MATH_SPEC.md`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/D_conservative_sbp

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/D_conservative_sbp/DirD.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/D_conservative_sbp/DirD

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/D_conservative_sbp/DirD/Core.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/D_conservative_sbp

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/D_conservative_sbp/lakefile.lean`
- `Workspaces/expression_deepseek-v4-flash_20260917_220258/D_conservative_sbp/lean-toolchain`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/E_hamiltonian_poisson

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/E_hamiltonian_poisson/DirE.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/E_hamiltonian_poisson/DirE

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/E_hamiltonian_poisson/DirE/Core.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/E_hamiltonian_poisson

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/E_hamiltonian_poisson/lakefile.lean`
- `Workspaces/expression_deepseek-v4-flash_20260917_220258/E_hamiltonian_poisson/lean-toolchain`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/F_variational_multisymplectic

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/F_variational_multisymplectic/DirF.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/F_variational_multisymplectic/DirF

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/F_variational_multisymplectic/DirF/Core.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/F_variational_multisymplectic

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/F_variational_multisymplectic/lakefile.lean`
- `Workspaces/expression_deepseek-v4-flash_20260917_220258/F_variational_multisymplectic/lean-toolchain`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/G_hirota_backlund

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/G_hirota_backlund/DirG.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/G_hirota_backlund/DirG

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/G_hirota_backlund/DirG/Core.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/G_hirota_backlund

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/G_hirota_backlund/lakefile.lean`
- `Workspaces/expression_deepseek-v4-flash_20260917_220258/G_hirota_backlund/lean-toolchain`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/H_toda_hierarchy

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/H_toda_hierarchy/DirH.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/H_toda_hierarchy/DirH

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/H_toda_hierarchy/DirH/Core.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/H_toda_hierarchy

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/H_toda_hierarchy/lakefile.lean`
- `Workspaces/expression_deepseek-v4-flash_20260917_220258/H_toda_hierarchy/lean-toolchain`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/lean

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/lean/DLWLean.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/lean/DLWLean

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/lean/DLWLean/Core.lean`

## Workspaces/expression_deepseek-v4-flash_20260917_220258/lean

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/lean/lake-manifest.json`
- `Workspaces/expression_deepseek-v4-flash_20260917_220258/lean/lakefile.lean`
- `Workspaces/expression_deepseek-v4-flash_20260917_220258/lean/lean-toolchain`

## Workspaces/expression_deepseek-v4-flash_20260917_220258

- `Workspaces/expression_deepseek-v4-flash_20260917_220258/RUN_CONTEXT.md`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/experiments

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/experiments/exp1_symbols.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/experiments/exp2_symbols.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/experiments/exp3_constraint.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/experiments/exp4_lattice.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/experiments/exp6_mechanical.py`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_234929_0abc2e5b

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_234929_0abc2e5b/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_234929_0abc2e5b/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235023_e4e63567

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235023_e4e63567/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235023_e4e63567/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235125_956e896d

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235125_956e896d/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235125_956e896d/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235134_970efce7

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235134_970efce7/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235134_970efce7/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235223_7bc8a381

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235223_7bc8a381/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235223_7bc8a381/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235409_16e938a4

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235409_16e938a4/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235409_16e938a4/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235504_6462c970

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235504_6462c970/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235504_6462c970/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235605_d9af12ef

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235605_d9af12ef/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235605_d9af12ef/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235646_37f754db

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235646_37f754db/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235646_37f754db/lib/lean/.probe

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235646_37f754db/lib/lean/.probe/P6.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235646_37f754db

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235646_37f754db/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235730_2b0a9fbe

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235730_2b0a9fbe/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235730_2b0a9fbe/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235809_30133f73

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235809_30133f73/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235809_30133f73/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235849_c8f199db

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235849_c8f199db/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235849_c8f199db/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235857_98c7118b

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235857_98c7118b/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235857_98c7118b/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235933_c3a594d5

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235933_c3a594d5/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260917_235933_c3a594d5/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000006_45c3e878

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000006_45c3e878/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000006_45c3e878/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000045_9addf2df

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000045_9addf2df/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000045_9addf2df/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000128_ef156df4

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000128_ef156df4/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000128_ef156df4/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000140_ead2e118

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000140_ead2e118/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000140_ead2e118/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000214_fd215a05

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000214_fd215a05/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000214_fd215a05/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000300_cb6bfb77

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000300_cb6bfb77/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000300_cb6bfb77/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000344_975f5d7a

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000344_975f5d7a/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000344_975f5d7a/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000439_36f4087d

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000439_36f4087d/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000439_36f4087d/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000708_93cf80ee

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000708_93cf80ee/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000708_93cf80ee/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000829_085050c6

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000829_085050c6/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000829_085050c6/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000912_42dd0a2c

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000912_42dd0a2c/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_000912_42dd0a2c/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001003_30b95439

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001003_30b95439/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001003_30b95439/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001052_67f3e3ca

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001052_67f3e3ca/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001052_67f3e3ca/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001412_3f5da5c9

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001412_3f5da5c9/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001412_3f5da5c9/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001500_51cadbcc

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001500_51cadbcc/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001500_51cadbcc/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001537_0731f681

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001537_0731f681/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001537_0731f681/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001616_fec1d862

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001616_fec1d862/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001616_fec1d862/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001804_98964a8c

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001804_98964a8c/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001804_98964a8c/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001804_98964a8c/lib/lean/DirA_Periodic.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001804_98964a8c

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001804_98964a8c/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001841_5ff1c648

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001841_5ff1c648/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001841_5ff1c648/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001841_5ff1c648/lib/lean/DirA_Periodic.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001841_5ff1c648

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_001841_5ff1c648/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_002031_ee9fea93

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_002031_ee9fea93/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_002031_ee9fea93/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_002031_ee9fea93/lib/lean/DirA_Periodic.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_002031_ee9fea93

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.lean-runs/20260918_002031_ee9fea93/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/P1.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/P2.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/P3.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/P4.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/P5.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/P6.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/P7.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/P8.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/P9.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/PA.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/PB.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/PC.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/PD.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/PE.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/PF.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/PG.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/PH.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/.probe/PI.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/Common/Operators.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/CONCLUSIONS.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/DirA_Periodic.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/proofs/maincheck.txt`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/report.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/A_finite_difference/VERIFY.md`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/experiments

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/experiments/run_log.txt`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/experiments/spectral_diagnostic_summary.json`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/experiments/spectral_diagnostic.py`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_232858_a2a964cf

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_232858_a2a964cf/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_232858_a2a964cf/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_233552_d5fc4b3d

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_233552_d5fc4b3d/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_233552_d5fc4b3d/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_233709_80dfcde7

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_233709_80dfcde7/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_233709_80dfcde7/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_233808_39d0eb3e

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_233808_39d0eb3e/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_233808_39d0eb3e/lib/lean/Spectral

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_233808_39d0eb3e/lib/lean/Spectral/Multiplier.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_233808_39d0eb3e

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_233808_39d0eb3e/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234031_ca829f1e

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234031_ca829f1e/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234031_ca829f1e/lib/lean/Spectral

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234031_ca829f1e/lib/lean/Spectral/Multiplier.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234031_ca829f1e

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234031_ca829f1e/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234207_42d27739

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234207_42d27739/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234207_42d27739/lib/lean/Spectral

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234207_42d27739/lib/lean/Spectral/Growth.olean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234207_42d27739/lib/lean/Spectral/Multiplier.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234207_42d27739

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234207_42d27739/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234402_5405af8b

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234402_5405af8b/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234402_5405af8b/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234402_5405af8b/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234402_5405af8b/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234402_5405af8b/lib/lean/DirB.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234402_5405af8b/lib/lean/Spectral

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234402_5405af8b/lib/lean/Spectral/Aliasing.olean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234402_5405af8b/lib/lean/Spectral/Growth.olean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234402_5405af8b/lib/lean/Spectral/Multiplier.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234402_5405af8b

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234402_5405af8b/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234813_89aea708

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234813_89aea708/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234813_89aea708/lib/lean/Spectral

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234813_89aea708/lib/lean/Spectral/Multiplier.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234813_89aea708

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_234813_89aea708/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235141_2aeca8ed

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235141_2aeca8ed/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235141_2aeca8ed/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235141_2aeca8ed/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235141_2aeca8ed/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235141_2aeca8ed/lib/lean/DirB.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235141_2aeca8ed/lib/lean/Spectral

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235141_2aeca8ed/lib/lean/Spectral/Aliasing.olean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235141_2aeca8ed/lib/lean/Spectral/Growth.olean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235141_2aeca8ed/lib/lean/Spectral/Multiplier.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235141_2aeca8ed

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235141_2aeca8ed/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235557_54694482

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235557_54694482/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235557_54694482/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235557_54694482/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235557_54694482/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235557_54694482/lib/lean/DirB.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235557_54694482/lib/lean/Spectral

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235557_54694482/lib/lean/Spectral/Aliasing.olean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235557_54694482/lib/lean/Spectral/Growth.olean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235557_54694482/lib/lean/Spectral/Multiplier.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235557_54694482

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260917_235557_54694482/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000017_481edb1e

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000017_481edb1e/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000017_481edb1e/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000017_481edb1e/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000017_481edb1e/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000017_481edb1e/lib/lean/DirB.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000017_481edb1e/lib/lean/Spectral

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000017_481edb1e/lib/lean/Spectral/Aliasing.olean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000017_481edb1e/lib/lean/Spectral/Growth.olean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000017_481edb1e/lib/lean/Spectral/Multiplier.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000017_481edb1e

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000017_481edb1e/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000219_a8e04503

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000219_a8e04503/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000219_a8e04503/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000219_a8e04503/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000219_a8e04503/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000219_a8e04503/lib/lean/DirB.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000219_a8e04503/lib/lean/Spectral

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000219_a8e04503/lib/lean/Spectral/Aliasing.olean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000219_a8e04503/lib/lean/Spectral/Growth.olean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000219_a8e04503/lib/lean/Spectral/Multiplier.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000219_a8e04503

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/.lean-runs/20260918_000219_a8e04503/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/Common/Operators.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/CONCLUSIONS.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/DirB.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/Spectral

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/Spectral/Aliasing.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/Spectral/Growth.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/proofs/Spectral/Multiplier.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/report.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/B_spectral/VERIFY.md`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/experiments

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/experiments/c_fem_dg_checks.py`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_233650_6118a13b

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_233650_6118a13b/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_233650_6118a13b/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_233650_6118a13b/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_233650_6118a13b

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_233650_6118a13b/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_233858_d971b25d

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_233858_d971b25d/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_233858_d971b25d/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_233858_d971b25d/lib/lean/C_FEM_DG.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_233858_d971b25d/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_233858_d971b25d/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_233858_d971b25d

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_233858_d971b25d/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234011_e76ddcd2

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234011_e76ddcd2/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234011_e76ddcd2/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234011_e76ddcd2/lib/lean/C_FEM_DG.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234011_e76ddcd2/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234011_e76ddcd2/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234011_e76ddcd2/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234011_e76ddcd2/lib/lean/Main.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234011_e76ddcd2

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234011_e76ddcd2/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234037_5d1b10ef

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234037_5d1b10ef/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234037_5d1b10ef/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234037_5d1b10ef/lib/lean/C_FEM_DG.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234037_5d1b10ef/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234037_5d1b10ef/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234037_5d1b10ef/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234037_5d1b10ef/lib/lean/Main.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234037_5d1b10ef

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/.lean-runs/20260917_234037_5d1b10ef/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/C_FEM_DG.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/Common/Operators.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/CONCLUSIONS.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/lastcheck.txt`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/proofs/Main.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/report.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/C_mixed_fem_dg/VERIFY.md`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/common/MAIN_verify_core.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/common/SHARED_MATH_SPEC.md`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/experiments

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/experiments/e1_exact_identities.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/experiments/e2_linear_symbol.py`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234319_dd226ef3

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234319_dd226ef3/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234319_dd226ef3/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234319_dd226ef3/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234319_dd226ef3

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234319_dd226ef3/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234442_f7ecfd12

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234442_f7ecfd12/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234442_f7ecfd12/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234442_f7ecfd12/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234442_f7ecfd12

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234442_f7ecfd12/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234555_3401314e

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234555_3401314e/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234555_3401314e/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234555_3401314e/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234555_3401314e

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234555_3401314e/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234815_f153ae14

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234815_f153ae14/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234815_f153ae14/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234815_f153ae14/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234815_f153ae14

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234815_f153ae14/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234922_3b88176c

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234922_3b88176c/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234922_3b88176c/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234922_3b88176c/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234922_3b88176c

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_234922_3b88176c/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235031_b01db5df

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235031_b01db5df/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235031_b01db5df/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235031_b01db5df/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235031_b01db5df

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235031_b01db5df/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235141_0235d0d0

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235141_0235d0d0/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235141_0235d0d0/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235141_0235d0d0/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235141_0235d0d0

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235141_0235d0d0/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235246_9742cb34

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235246_9742cb34/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235246_9742cb34/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235246_9742cb34/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235246_9742cb34

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235246_9742cb34/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235340_943d6089

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235340_943d6089/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235340_943d6089/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235340_943d6089/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235340_943d6089

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235340_943d6089/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235447_31bed668

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235447_31bed668/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235447_31bed668/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235447_31bed668/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235447_31bed668

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235447_31bed668/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235550_5e0e0c04

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235550_5e0e0c04/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235550_5e0e0c04/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235550_5e0e0c04/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235550_5e0e0c04

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235550_5e0e0c04/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235640_01afd724

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235640_01afd724/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235640_01afd724/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235640_01afd724/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235640_01afd724

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235640_01afd724/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235731_70852388

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235731_70852388/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235731_70852388/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235731_70852388/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235731_70852388

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235731_70852388/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235841_73fdc39b

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235841_73fdc39b/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235841_73fdc39b/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235841_73fdc39b/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235841_73fdc39b

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235841_73fdc39b/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235929_a3e02fd8

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235929_a3e02fd8/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235929_a3e02fd8/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235929_a3e02fd8/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235929_a3e02fd8

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260917_235929_a3e02fd8/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000017_6787ac28

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000017_6787ac28/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000017_6787ac28/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000017_6787ac28/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000017_6787ac28

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000017_6787ac28/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000138_6d6f362a

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000138_6d6f362a/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000138_6d6f362a/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000138_6d6f362a/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000138_6d6f362a

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000138_6d6f362a/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000250_5d31d33a

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000250_5d31d33a/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000250_5d31d33a/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000250_5d31d33a/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000250_5d31d33a

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000250_5d31d33a/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000350_3ac884e0

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000350_3ac884e0/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000350_3ac884e0/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000350_3ac884e0/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000350_3ac884e0

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000350_3ac884e0/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000443_ec6ce8b1

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000443_ec6ce8b1/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000443_ec6ce8b1/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000443_ec6ce8b1/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000443_ec6ce8b1

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000443_ec6ce8b1/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000507_ba11380e

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000507_ba11380e/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000507_ba11380e/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000507_ba11380e/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000507_ba11380e

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000507_ba11380e/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000526_025f2058

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000526_025f2058/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000526_025f2058/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000526_025f2058/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000526_025f2058

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000526_025f2058/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000643_b2c99d41

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000643_b2c99d41/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000643_b2c99d41/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000643_b2c99d41/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000643_b2c99d41

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000643_b2c99d41/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000751_afb09cec

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000751_afb09cec/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000751_afb09cec/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000751_afb09cec/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000751_afb09cec

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000751_afb09cec/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000837_463d71b0

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000837_463d71b0/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000837_463d71b0/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000837_463d71b0/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000837_463d71b0

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000837_463d71b0/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000913_c1dbfe02

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000913_c1dbfe02/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000913_c1dbfe02/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000913_c1dbfe02/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000913_c1dbfe02

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_000913_c1dbfe02/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001002_423ea6d1

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001002_423ea6d1/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001002_423ea6d1/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001002_423ea6d1/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001002_423ea6d1

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001002_423ea6d1/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001057_889649f0

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001057_889649f0/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001057_889649f0/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001057_889649f0/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001057_889649f0

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001057_889649f0/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001229_75530b7f

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001229_75530b7f/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001229_75530b7f/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001229_75530b7f/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001229_75530b7f

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001229_75530b7f/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001312_607b769b

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001312_607b769b/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001312_607b769b/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001312_607b769b/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001312_607b769b

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001312_607b769b/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001352_08a9ab8a

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001352_08a9ab8a/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001352_08a9ab8a/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001352_08a9ab8a/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001352_08a9ab8a/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001352_08a9ab8a/lib/lean/DirD.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001352_08a9ab8a

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001352_08a9ab8a/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001436_450b05fd

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001436_450b05fd/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001436_450b05fd/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001436_450b05fd/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001436_450b05fd

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001436_450b05fd/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001524_2409ba17

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001524_2409ba17/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001524_2409ba17/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001524_2409ba17/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001524_2409ba17

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001524_2409ba17/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001609_9a3b35cf

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001609_9a3b35cf/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001609_9a3b35cf/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001609_9a3b35cf/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001609_9a3b35cf/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001609_9a3b35cf/lib/lean/DirD.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001609_9a3b35cf

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001609_9a3b35cf/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001742_6face4d9

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001742_6face4d9/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001742_6face4d9/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001742_6face4d9/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001742_6face4d9/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001742_6face4d9/lib/lean/DirD.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001742_6face4d9

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_001742_6face4d9/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_002058_b528fa98

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_002058_b528fa98/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_002058_b528fa98/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_002058_b528fa98/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_002058_b528fa98/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_002058_b528fa98/lib/lean/DirD.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_002058_b528fa98

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/.lean-runs/20260918_002058_b528fa98/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/Common/Operators.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/CONCLUSIONS.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/DirD.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/proofs/maincheck.txt`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/report.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/D_conservative_sbp/VERIFY.md`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/experiments

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/experiments/e1_poisson_search.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/experiments/e2_poisson_antisym.py`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260917_234056_6adb52fc

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260917_234056_6adb52fc/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260917_234056_6adb52fc/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260917_234438_df1afb40

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260917_234438_df1afb40/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260917_234438_df1afb40/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260917_234438_df1afb40/lib/lean/E_Poisson.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260917_234438_df1afb40

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260917_234438_df1afb40/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260917_234613_56c85104

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260917_234613_56c85104/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260917_234613_56c85104/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260917_234613_56c85104/lib/lean/E_Poisson.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260917_234613_56c85104

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260917_234613_56c85104/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260918_001951_1df4c811

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260918_001951_1df4c811/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260918_001951_1df4c811/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260918_001951_1df4c811/lib/lean/E_Poisson.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260918_001951_1df4c811

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/.lean-runs/20260918_001951_1df4c811/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/Common/Operators.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/CONCLUSIONS.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/E_Poisson.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/proofs/maincheck.txt`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/report.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/E_hamiltonian_poisson/VERIFY.md`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/experiments

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/experiments/MAIN_discrete_dispersion.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/experiments/run_discrete_dispersion.txt`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/experiments

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/experiments/f_multisymplectic_checks.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/experiments/run_output.txt`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/proofs/.lean-runs/20260917_233950_f9a8fcf4

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/proofs/.lean-runs/20260917_233950_f9a8fcf4/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/proofs/.lean-runs/20260917_233950_f9a8fcf4/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/proofs/.lean-runs/20260917_234228_8a2980f5

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/proofs/.lean-runs/20260917_234228_8a2980f5/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/proofs/.lean-runs/20260917_234228_8a2980f5/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/proofs/.lean-runs/20260917_234228_8a2980f5/lib/lean/F_Multisymplectic.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/proofs/.lean-runs/20260917_234228_8a2980f5

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/proofs/.lean-runs/20260917_234228_8a2980f5/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/proofs/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/proofs/Common/Operators.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/proofs

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/proofs/F_Multisymplectic.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/proofs/lastcheck.txt`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/F_variational_multisymplectic/report.md`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/experiments

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/experiments/g1_sympy_core.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/experiments/g2_degeneracy_audit.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/experiments/g3_mode_audit.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/experiments/g4_eigen_16cases.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/experiments/g5_decisive.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/experiments/g6_pair_vanishing.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/experiments/g6a_closed_form.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/experiments/g6b_solve.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/experiments/hunter_saxton_layout.txt`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/experiments/hunter_saxton.txt`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_234432_f44a6864

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_234432_f44a6864/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_234432_f44a6864/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_234702_2e8651b4

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_234702_2e8651b4/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_234702_2e8651b4/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_234748_8bcad985

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_234748_8bcad985/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_234748_8bcad985/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_234839_1dc6a548

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_234839_1dc6a548/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_234839_1dc6a548/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_234922_708dba86

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_234922_708dba86/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_234922_708dba86/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235005_3be1f014

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235005_3be1f014/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235005_3be1f014/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235050_85784c4c

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235050_85784c4c/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235050_85784c4c/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235138_25425d29

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235138_25425d29/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235138_25425d29/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235217_d9a90a2a

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235217_d9a90a2a/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235217_d9a90a2a/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235256_ce88f38a

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235256_ce88f38a/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235256_ce88f38a/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235332_e91068b8

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235332_e91068b8/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235332_e91068b8/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235420_73a98733

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235420_73a98733/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235420_73a98733/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235458_784d41c3

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235458_784d41c3/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235458_784d41c3/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235535_1cbeb969

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235535_1cbeb969/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235535_1cbeb969/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235625_3bb1cda3

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235625_3bb1cda3/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235625_3bb1cda3/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235726_3a0ed9b2

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235726_3a0ed9b2/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235726_3a0ed9b2/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235803_dd30dcab

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235803_dd30dcab/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235803_dd30dcab/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235846_903e9fba

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235846_903e9fba/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235846_903e9fba/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235945_a2fc96ea

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235945_a2fc96ea/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260917_235945_a2fc96ea/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000031_988a9a46

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000031_988a9a46/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000031_988a9a46/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000122_66a27ad9

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000122_66a27ad9/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000122_66a27ad9/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000213_36964a3a

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000213_36964a3a/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000213_36964a3a/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000257_01ed6b14

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000257_01ed6b14/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000257_01ed6b14/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000338_de412ec1

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000338_de412ec1/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000338_de412ec1/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000539_715eef1f

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000539_715eef1f/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000539_715eef1f/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000645_d0d8e6b1

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000645_d0d8e6b1/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000645_d0d8e6b1/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000713_b4a0273a

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000713_b4a0273a/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000713_b4a0273a/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000809_a1ae110b

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000809_a1ae110b/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000809_a1ae110b/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000912_34666d3c

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000912_34666d3c/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000912_34666d3c/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000959_f1350cfa

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000959_f1350cfa/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_000959_f1350cfa/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001035_bc4c527e

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001035_bc4c527e/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001035_bc4c527e/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001150_3233bda3

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001150_3233bda3/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001150_3233bda3/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001234_e7e273a2

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001234_e7e273a2/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001234_e7e273a2/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001243_171a9b78

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001243_171a9b78/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001243_171a9b78/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001354_c5f2bacb

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001354_c5f2bacb/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001354_c5f2bacb/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001435_12f07c8f

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001435_12f07c8f/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001435_12f07c8f/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001544_56f4d18c

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001544_56f4d18c/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001544_56f4d18c/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001614_2a254f45

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001614_2a254f45/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001614_2a254f45/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001702_3f0376ad

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001702_3f0376ad/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001702_3f0376ad/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001758_fec5ce03

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001758_fec5ce03/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001758_fec5ce03/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001837_c31dabc2

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001837_c31dabc2/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001837_c31dabc2/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001938_259cfdce

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001938_259cfdce/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_001938_259cfdce/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002012_aff28934

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002012_aff28934/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002012_aff28934/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002037_637e96d7

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002037_637e96d7/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002037_637e96d7/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002112_89563820

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002112_89563820/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002112_89563820/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002130_6f853adc

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002130_6f853adc/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002130_6f853adc/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002212_c283c39e

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002212_c283c39e/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002212_c283c39e/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002243_01aac6d2

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002243_01aac6d2/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002243_01aac6d2/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002302_742af898

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002302_742af898/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002302_742af898/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002323_8102f2ca

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002323_8102f2ca/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002323_8102f2ca/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002342_1700261c

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002342_1700261c/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002342_1700261c/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002452_a89c06b2

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002452_a89c06b2/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002452_a89c06b2/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002515_41776e99

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002515_41776e99/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002515_41776e99/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002537_7bdfde27

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002537_7bdfde27/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002537_7bdfde27/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002559_e73ddb90

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002559_e73ddb90/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002559_e73ddb90/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002620_7f275ead

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002620_7f275ead/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002620_7f275ead/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002658_634fc39a

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002658_634fc39a/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002658_634fc39a/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002720_dde57685

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002720_dde57685/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002720_dde57685/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002742_723a913c

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002742_723a913c/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002742_723a913c/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002805_a7563af5

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002805_a7563af5/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002805_a7563af5/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002825_2af10ed1

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002825_2af10ed1/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002825_2af10ed1/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002845_dc3a81e7

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002845_dc3a81e7/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002845_dc3a81e7/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002909_f8ed5cde

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002909_f8ed5cde/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002909_f8ed5cde/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002927_2d87e51a

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002927_2d87e51a/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002927_2d87e51a/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002949_d6512a45

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002949_d6512a45/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_002949_d6512a45/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003015_73d3c9aa

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003015_73d3c9aa/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003015_73d3c9aa/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003034_0cfe7212

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003034_0cfe7212/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003034_0cfe7212/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003055_ddf36f51

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003055_ddf36f51/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003055_ddf36f51/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003227_e7e1cbf7

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003227_e7e1cbf7/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003227_e7e1cbf7/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003250_94e34c98

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003250_94e34c98/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003250_94e34c98/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003310_36a539d4

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003310_36a539d4/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003310_36a539d4/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003330_b4ef9355

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003330_b4ef9355/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003330_b4ef9355/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003351_b70fb95b

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003351_b70fb95b/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003351_b70fb95b/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003411_9ede7886

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003411_9ede7886/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003411_9ede7886/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003439_e3a53ecb

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003439_e3a53ecb/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003439_e3a53ecb/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003503_fb2ab56b

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003503_fb2ab56b/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003503_fb2ab56b/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003527_09e03b37

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003527_09e03b37/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003527_09e03b37/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003556_ca3203c3

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003556_ca3203c3/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003556_ca3203c3/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003624_f5d9f89f

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003624_f5d9f89f/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003624_f5d9f89f/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003653_7a89c87c

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003653_7a89c87c/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003653_7a89c87c/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003653_7a89c87c/lib/lean/Probe.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003653_7a89c87c

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003653_7a89c87c/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003733_38d2c10f

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003733_38d2c10f/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003733_38d2c10f/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003802_319dc4fa

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003802_319dc4fa/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003802_319dc4fa/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003830_cd6f1782

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003830_cd6f1782/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003830_cd6f1782/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003858_3751ade0

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003858_3751ade0/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003858_3751ade0/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003926_f5ab9ae5

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003926_f5ab9ae5/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_003926_f5ab9ae5/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004114_f9bda7f8

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004114_f9bda7f8/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004114_f9bda7f8/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004434_bf568871

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004434_bf568871/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004434_bf568871/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004508_40d2834d

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004508_40d2834d/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004508_40d2834d/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004541_398d6af4

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004541_398d6af4/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004541_398d6af4/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004614_6b22d956

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004614_6b22d956/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004614_6b22d956/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004647_59b89120

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004647_59b89120/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004647_59b89120/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004719_16017d38

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004719_16017d38/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004719_16017d38/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004813_e20cc143

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004813_e20cc143/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004813_e20cc143/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004818_d1a138cb

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004818_d1a138cb/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004818_d1a138cb/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004822_cf1cd2a5

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004822_cf1cd2a5/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004822_cf1cd2a5/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004852_997c16f0

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004852_997c16f0/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004852_997c16f0/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004924_24b8fe42

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004924_24b8fe42/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004924_24b8fe42/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004924_24b8fe42/lib/lean/DirG.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004924_24b8fe42

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_004924_24b8fe42/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_005324_81704190

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_005324_81704190/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_005324_81704190/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_005324_81704190/lib/lean/DirG.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_005324_81704190

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_005324_81704190/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_010225_ce134558

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_010225_ce134558/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_010225_ce134558/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_010225_ce134558/lib/lean/DirG.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_010225_ce134558

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/.lean-runs/20260918_010225_ce134558/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/Common/Operators.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/CONCLUSIONS.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/proofs/DirG.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/report.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/G_hirota_backlund/VERIFY.md`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/experiments

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/experiments/diagnose_mkp_tau.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/experiments/num_mkp_check.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/experiments/run_audit.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/experiments/run_diagnose.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/experiments/run_E1E4.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/experiments/run_lean.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/experiments/run_num_mkp.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/experiments/run_symbolic.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/experiments/verify_h_toda.py`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/experiments/verify_symbolic_spine.py`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001629_825d3005

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001629_825d3005/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001629_825d3005/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001629_825d3005/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001629_825d3005

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001629_825d3005/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001732_c3839348

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001732_c3839348/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001732_c3839348/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001732_c3839348/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001732_c3839348

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001732_c3839348/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001819_13ad47c1

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001819_13ad47c1/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001819_13ad47c1/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001819_13ad47c1/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001819_13ad47c1

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001819_13ad47c1/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001921_f5b4befe

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001921_f5b4befe/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001921_f5b4befe/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001921_f5b4befe/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001921_f5b4befe

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_001921_f5b4befe/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002016_1ad66683

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002016_1ad66683/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002016_1ad66683/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002016_1ad66683/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002016_1ad66683

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002016_1ad66683/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002143_cd8ad356

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002143_cd8ad356/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002143_cd8ad356/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002143_cd8ad356/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002143_cd8ad356

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002143_cd8ad356/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002205_b3d55cb9

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002205_b3d55cb9/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002205_b3d55cb9/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002205_b3d55cb9/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002205_b3d55cb9

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002205_b3d55cb9/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002300_79c6a623

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002300_79c6a623/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002300_79c6a623/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002300_79c6a623/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002300_79c6a623

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002300_79c6a623/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002344_fe9a959a

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002344_fe9a959a/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002344_fe9a959a/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002344_fe9a959a/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002344_fe9a959a

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002344_fe9a959a/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002444_cae4d938

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002444_cae4d938/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002444_cae4d938/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002444_cae4d938/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002444_cae4d938

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002444_cae4d938/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002533_11772286

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002533_11772286/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002533_11772286/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002533_11772286/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002533_11772286

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002533_11772286/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002720_228fff04

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002720_228fff04/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002720_228fff04/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002720_228fff04/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002720_228fff04

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002720_228fff04/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002804_f54dc6b2

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002804_f54dc6b2/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002804_f54dc6b2/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002804_f54dc6b2/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002804_f54dc6b2

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002804_f54dc6b2/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002844_ba4f1e32

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002844_ba4f1e32/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002844_ba4f1e32/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002844_ba4f1e32/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002844_ba4f1e32

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002844_ba4f1e32/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002929_c15ec62f

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002929_c15ec62f/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002929_c15ec62f/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002929_c15ec62f/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002929_c15ec62f

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_002929_c15ec62f/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003120_24eec714

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003120_24eec714/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003120_24eec714/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003120_24eec714/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003120_24eec714

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003120_24eec714/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003219_95a156d8

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003219_95a156d8/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003219_95a156d8/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003219_95a156d8/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003219_95a156d8

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003219_95a156d8/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003256_df17c532

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003256_df17c532/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003256_df17c532/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003256_df17c532/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003256_df17c532

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003256_df17c532/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003412_0e707b44

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003412_0e707b44/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003412_0e707b44/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003412_0e707b44/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003412_0e707b44

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003412_0e707b44/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003451_deb7f337

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003451_deb7f337/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003451_deb7f337/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003451_deb7f337/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003451_deb7f337

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003451_deb7f337/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003539_0ca3a947

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003539_0ca3a947/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003539_0ca3a947/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003539_0ca3a947/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003539_0ca3a947

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003539_0ca3a947/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003617_d6578572

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003617_d6578572/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003617_d6578572/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003617_d6578572/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003617_d6578572

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003617_d6578572/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003659_99fcd6b0

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003659_99fcd6b0/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003659_99fcd6b0/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003659_99fcd6b0/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003659_99fcd6b0/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003659_99fcd6b0/lib/lean/DirH.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003659_99fcd6b0

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003659_99fcd6b0/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003732_6a4278a3

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003732_6a4278a3/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003732_6a4278a3/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003732_6a4278a3/lib/lean/AuditH.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003732_6a4278a3/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003732_6a4278a3/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003732_6a4278a3/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003732_6a4278a3/lib/lean/DirH.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003732_6a4278a3

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_003732_6a4278a3/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005240_1d7ebce6

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005240_1d7ebce6/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005240_1d7ebce6/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005240_1d7ebce6/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005240_1d7ebce6

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005240_1d7ebce6/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005313_78709060

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005313_78709060/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005313_78709060/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005313_78709060/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005313_78709060

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005313_78709060/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005353_29a7fbe7

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005353_29a7fbe7/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005353_29a7fbe7/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005353_29a7fbe7/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005353_29a7fbe7

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005353_29a7fbe7/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005439_4130c260

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005439_4130c260/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005439_4130c260/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005439_4130c260/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005439_4130c260/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005439_4130c260/lib/lean/DirH.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005439_4130c260

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005439_4130c260/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005511_0a67f7d4

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005511_0a67f7d4/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005511_0a67f7d4/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005511_0a67f7d4/lib/lean/AuditH.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005511_0a67f7d4/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005511_0a67f7d4/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005511_0a67f7d4/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005511_0a67f7d4/lib/lean/DirH.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005511_0a67f7d4

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_005511_0a67f7d4/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010443_92cf2170

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010443_92cf2170/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010443_92cf2170/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010443_92cf2170/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010443_92cf2170/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010443_92cf2170/lib/lean/DirH.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010443_92cf2170

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010443_92cf2170/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010503_62654013

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010503_62654013/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010503_62654013/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010503_62654013/lib/lean/AuditH.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010503_62654013/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010503_62654013/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010503_62654013/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010503_62654013/lib/lean/DirH.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010503_62654013

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/.lean-runs/20260918_010503_62654013/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/AuditH.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/Common/Operators.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/CONCLUSIONS.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/DirH.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/proofs/maincheck.txt`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/report.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/H_toda_hierarchy/VERIFY.md`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/pdftext

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/pdftext/HunterSaxton.txt`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/pdftext/pages

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/pdftext/pages/p-02.png`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/pdftext

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/pdftext/PhysD.txt`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_231823_807977ea

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_231823_807977ea/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_231823_807977ea/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_231844_3ad54527

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_231844_3ad54527/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_231844_3ad54527/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_231912_5010e44d

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_231912_5010e44d/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_231912_5010e44d/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_231938_1948e15d

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_231938_1948e15d/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_231938_1948e15d/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232051_5c8cfb2d

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232051_5c8cfb2d/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232051_5c8cfb2d/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232116_34ce397f

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232116_34ce397f/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232116_34ce397f/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232215_b71e1926

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232215_b71e1926/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232215_b71e1926/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232241_6a28a1ee

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232241_6a28a1ee/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232241_6a28a1ee/lib/lean/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232241_6a28a1ee/lib/lean/Common/Operators.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232241_6a28a1ee/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232241_6a28a1ee/lib/lean/Smoke.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232241_6a28a1ee

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232241_6a28a1ee/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232743_1c7d7b02

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232743_1c7d7b02/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_232743_1c7d7b02/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233036_52be82d2

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233036_52be82d2/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233036_52be82d2/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233251_4346cd7c

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233251_4346cd7c/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233251_4346cd7c/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233416_7004722c

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233416_7004722c/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233416_7004722c/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233459_5214113f

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233459_5214113f/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233459_5214113f/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233532_3456033d

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233532_3456033d/build.log`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233532_3456033d/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233635_aa6cea69

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233635_aa6cea69/build.log`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233635_aa6cea69/lib/lean

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233635_aa6cea69/lib/lean/MainNoGo.olean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233635_aa6cea69/lib/lean/Smoke.olean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233635_aa6cea69

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/.lean-runs/20260917_233635_aa6cea69/result.json`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/Common

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/Common/ApiProbe.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/Common/Operators.lean`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/core_v_567_10_output.txt`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/core_v_output.txt`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/IProbe.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/lastcheck.txt`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/MainNoGo.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/Smoke.lean`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/v4_output.txt`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/v8_output.txt`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/proofs/v9_output.txt`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927/reports

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/reports/CLAIMS_AND_PROOFS.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/reports/FINAL_REPORT.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/reports/MAIN_VERIFICATION.md`
- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/reports/REPRODUCE.md`

## Workspaces/expression_deepseek-v4.1-flash_20260917_222927

- `Workspaces/expression_deepseek-v4.1-flash_20260917_222927/RUN_CONTEXT.md`

## Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/.lean-runs/20260918_004112_5d29956b

- `Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/.lean-runs/20260918_004112_5d29956b/build.log`

## Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/.lean-runs/20260918_004112_5d29956b/lib/lean/Common

- `Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/.lean-runs/20260918_004112_5d29956b/lib/lean/Common/Operators.olean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/.lean-runs/20260918_004112_5d29956b

- `Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/.lean-runs/20260918_004112_5d29956b/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/.lean-runs/20260918_004153_54d2f15e

- `Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/.lean-runs/20260918_004153_54d2f15e/build.log`

## Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/.lean-runs/20260918_004153_54d2f15e/lib/lean/Common

- `Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/.lean-runs/20260918_004153_54d2f15e/lib/lean/Common/Operators.olean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/.lean-runs/20260918_004153_54d2f15e/lib/lean

- `Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/.lean-runs/20260918_004153_54d2f15e/lib/lean/Smoke.olean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/.lean-runs/20260918_004153_54d2f15e

- `Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/.lean-runs/20260918_004153_54d2f15e/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/Common

- `Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/Common/Operators.lean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs

- `Workspaces/expression_glm-5.3-flash_20260917_225005/A_finite_difference/proofs/Smoke.lean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_001519_35707dc2

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_001519_35707dc2/build.log`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_001519_35707dc2/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_001527_e23f5291

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_001527_e23f5291/build.log`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_001527_e23f5291/lib/lean

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_001527_e23f5291/lib/lean/Smoke.olean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_001527_e23f5291

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_001527_e23f5291/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002229_c82ffdc8

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002229_c82ffdc8/build.log`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002229_c82ffdc8/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002425_65e3974d

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002425_65e3974d/build.log`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002425_65e3974d/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002444_db2abba3

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002444_db2abba3/build.log`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002444_db2abba3/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002548_31fc7c4d

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002548_31fc7c4d/build.log`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002548_31fc7c4d/lib/lean/B

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002548_31fc7c4d/lib/lean/B/Modal.olean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002548_31fc7c4d

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002548_31fc7c4d/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002855_005fa3e6

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002855_005fa3e6/build.log`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_002855_005fa3e6/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003250_f640741f

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003250_f640741f/build.log`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003250_f640741f/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003441_bd44bfc6

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003441_bd44bfc6/build.log`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003441_bd44bfc6/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003632_5201a531

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003632_5201a531/build.log`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003632_5201a531/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003717_d9bf70a1

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003717_d9bf70a1/build.log`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003717_d9bf70a1/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003751_06d8b8bf

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003751_06d8b8bf/build.log`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003751_06d8b8bf/lib/lean/B

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003751_06d8b8bf/lib/lean/B/Dispersion.olean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003751_06d8b8bf

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003751_06d8b8bf/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003831_d1c85f4f

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003831_d1c85f4f/build.log`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003831_d1c85f4f/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003903_21e1bd39

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003903_21e1bd39/build.log`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003903_21e1bd39/lib/lean/B

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003903_21e1bd39/lib/lean/B/Modal.olean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003903_21e1bd39

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_003903_21e1bd39/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004149_8ce72cd1

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004149_8ce72cd1/build.log`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004149_8ce72cd1/lib/lean/B

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004149_8ce72cd1/lib/lean/B/Modal.olean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004149_8ce72cd1

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004149_8ce72cd1/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004450_7aa3e757

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004450_7aa3e757/build.log`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004450_7aa3e757/lib/lean/B

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004450_7aa3e757/lib/lean/B/Modal.olean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004450_7aa3e757

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004450_7aa3e757/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004651_5de3ed59

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004651_5de3ed59/build.log`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004651_5de3ed59/lib/lean/B

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004651_5de3ed59/lib/lean/B/Modal.olean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004651_5de3ed59

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004651_5de3ed59/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004726_3cd1efaf

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004726_3cd1efaf/build.log`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004726_3cd1efaf/lib/lean/B

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004726_3cd1efaf/lib/lean/B/Modal.olean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004726_3cd1efaf

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004726_3cd1efaf/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004806_765ebfbc

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004806_765ebfbc/build.log`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004806_765ebfbc/lib/lean/B

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004806_765ebfbc/lib/lean/B/Aliasing.olean`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004806_765ebfbc/lib/lean/B/Modal.olean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004806_765ebfbc

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_004806_765ebfbc/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_005211_12f1a398

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_005211_12f1a398/build.log`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_005211_12f1a398/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_005337_3762a66d

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_005337_3762a66d/build.log`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/.lean-runs/20260918_005337_3762a66d/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/B

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/B/Aliasing.lean`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/B/Band.lean`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/B/Dispersion.lean`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/B/Modal.lean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/Common

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/Common/Operators.lean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs

- `Workspaces/expression_glm-5.3-flash_20260917_225005/B_spectral/proofs/Smoke.lean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/C_mixed_fem_dg/proofs/Common

- `Workspaces/expression_glm-5.3-flash_20260917_225005/C_mixed_fem_dg/proofs/Common/Operators.lean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/common

- `Workspaces/expression_glm-5.3-flash_20260917_225005/common/REFERENCE_staggered_construction.md`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/common/SHARED_MATH_SPEC.md`

## Workspaces/expression_glm-5.3-flash_20260917_225005/D_conservative_sbp/proofs/Common

- `Workspaces/expression_glm-5.3-flash_20260917_225005/D_conservative_sbp/proofs/Common/Operators.lean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/E_hamiltonian_poisson/proofs/Common

- `Workspaces/expression_glm-5.3-flash_20260917_225005/E_hamiltonian_poisson/proofs/Common/Operators.lean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/experiments

- `Workspaces/expression_glm-5.3-flash_20260917_225005/experiments/debug_cont2sol.py`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/experiments/verify_continuous_2soliton.py`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/experiments/verify_linearization.py`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/experiments/verify_staggered.py`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/experiments/verify_wform_lin.py`

## Workspaces/expression_glm-5.3-flash_20260917_225005/F_variational_multisymplectic/proofs/Common

- `Workspaces/expression_glm-5.3-flash_20260917_225005/F_variational_multisymplectic/proofs/Common/Operators.lean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/G_hirota_backlund/proofs/Common

- `Workspaces/expression_glm-5.3-flash_20260917_225005/G_hirota_backlund/proofs/Common/Operators.lean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/H_toda_hierarchy/proofs/Common

- `Workspaces/expression_glm-5.3-flash_20260917_225005/H_toda_hierarchy/proofs/Common/Operators.lean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_000709_b16c4a9b

- `Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_000709_b16c4a9b/build.log`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_000709_b16c4a9b/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_000933_305731a5

- `Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_000933_305731a5/build.log`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_000933_305731a5/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_001032_4525708b

- `Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_001032_4525708b/build.log`
- `Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_001032_4525708b/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_001119_86e03866

- `Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_001119_86e03866/build.log`

## Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_001119_86e03866/lib/lean/Common

- `Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_001119_86e03866/lib/lean/Common/Operators.olean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_001119_86e03866/lib/lean

- `Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_001119_86e03866/lib/lean/Smoke.olean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_001119_86e03866

- `Workspaces/expression_glm-5.3-flash_20260917_225005/lean/.lean-runs/20260918_001119_86e03866/result.json`

## Workspaces/expression_glm-5.3-flash_20260917_225005/lean/Common

- `Workspaces/expression_glm-5.3-flash_20260917_225005/lean/Common/Operators.lean`

## Workspaces/expression_glm-5.3-flash_20260917_225005/lean

- `Workspaces/expression_glm-5.3-flash_20260917_225005/lean/Smoke.lean`

## Workspaces/expression_glm-5.3-flash_20260917_225005

- `Workspaces/expression_glm-5.3-flash_20260917_225005/RUN_CONTEXT.md`

## Workspaces/expression_union-alpha_20260917_221034/common

- `Workspaces/expression_union-alpha_20260917_221034/common/SPEC.md`

## Workspaces/expression_union-alpha_20260917_221034/experiments

- `Workspaces/expression_union-alpha_20260917_221034/experiments/dlw_staggered_checks.json`

## Workspaces/expression_union-alpha_20260917_221034/lean

- `Workspaces/expression_union-alpha_20260917_221034/lean/DLWCommon.lean`

## Workspaces/expression_union-alpha_20260917_221034/lean/DLWCommon

- `Workspaces/expression_union-alpha_20260917_221034/lean/DLWCommon/DirA.lean`
- `Workspaces/expression_union-alpha_20260917_221034/lean/DLWCommon/DirB.lean`
- `Workspaces/expression_union-alpha_20260917_221034/lean/DLWCommon/DirC.lean`
- `Workspaces/expression_union-alpha_20260917_221034/lean/DLWCommon/DirD.lean`
- `Workspaces/expression_union-alpha_20260917_221034/lean/DLWCommon/DirE.lean`
- `Workspaces/expression_union-alpha_20260917_221034/lean/DLWCommon/DirF.lean`
- `Workspaces/expression_union-alpha_20260917_221034/lean/DLWCommon/DirG.lean`
- `Workspaces/expression_union-alpha_20260917_221034/lean/DLWCommon/DirH.lean`

## Workspaces/expression_union-alpha_20260917_221034/lean

- `Workspaces/expression_union-alpha_20260917_221034/lean/DLWLean.lean`
- `Workspaces/expression_union-alpha_20260917_221034/lean/lake-manifest.json`
- `Workspaces/expression_union-alpha_20260917_221034/lean/lakefile.lean`
- `Workspaces/expression_union-alpha_20260917_221034/lean/lean-toolchain`

## Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_231824_d852acef

- `Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_231824_d852acef/build.log`

## Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_231824_d852acef/lib/lean

- `Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_231824_d852acef/lib/lean/Main.olean`

## Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_231824_d852acef

- `Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_231824_d852acef/result.json`

## Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_231851_23af189c

- `Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_231851_23af189c/build.log`
- `Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_231851_23af189c/result.json`

## Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_231954_12098863

- `Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_231954_12098863/build.log`
- `Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_231954_12098863/result.json`

## Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_232002_a0d6e8dd

- `Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_232002_a0d6e8dd/build.log`

## Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_232002_a0d6e8dd/lib/lean

- `Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_232002_a0d6e8dd/lib/lean/Main.olean`

## Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_232002_a0d6e8dd

- `Workspaces/expression_union-alpha_20260917_221034/proofs/.lean-runs/20260917_232002_a0d6e8dd/result.json`

## Workspaces/expression_union-alpha_20260917_221034/proofs

- `Workspaces/expression_union-alpha_20260917_221034/proofs/Main.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_232252_61c03306

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_232252_61c03306/build.log`
- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_232252_61c03306/result.json`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_232921_1a667dd9

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_232921_1a667dd9/build.log`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_232921_1a667dd9/lib/lean

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_232921_1a667dd9/lib/lean/T1.olean`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_232921_1a667dd9

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_232921_1a667dd9/result.json`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_233552_2df830fd

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_233552_2df830fd/build.log`
- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_233552_2df830fd/result.json`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234036_cd0c3026

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234036_cd0c3026/build.log`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234036_cd0c3026/lib/lean

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234036_cd0c3026/lib/lean/T2.olean`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234036_cd0c3026

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234036_cd0c3026/result.json`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234217_0ba0a992

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234217_0ba0a992/build.log`
- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234217_0ba0a992/result.json`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234355_5b62ef2d

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234355_5b62ef2d/build.log`
- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234355_5b62ef2d/result.json`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234717_b21d23c8

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234717_b21d23c8/build.log`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234717_b21d23c8/lib/lean/Common

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234717_b21d23c8/lib/lean/Common/DirA.olean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234717_b21d23c8/lib/lean/Common/Operators.olean`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234717_b21d23c8

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234717_b21d23c8/result.json`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234913_ae5e667b

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234913_ae5e667b/build.log`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234913_ae5e667b/lib/lean/Common

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234913_ae5e667b/lib/lean/Common/DirA.olean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234913_ae5e667b/lib/lean/Common/Operators.olean`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234913_ae5e667b/lib/lean

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234913_ae5e667b/lib/lean/Main.olean`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234913_ae5e667b

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/.lean-runs/20260917_234913_ae5e667b/result.json`

## Workspaces/expression_union-alpha_20260917_221034/proofsA/Common

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/Common/DirA.lean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsA/Common/Operators.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsA

- `Workspaces/expression_union-alpha_20260917_221034/proofsA/LEAN_POLICY.md`
- `Workspaces/expression_union-alpha_20260917_221034/proofsA/Main.lean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsA/Mini.lean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsA/Smoke.lean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsA/T1.lean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsA/T2.lean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsA/T3.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsB/.lean-runs/20260917_235057_87542037

- `Workspaces/expression_union-alpha_20260917_221034/proofsB/.lean-runs/20260917_235057_87542037/build.log`

## Workspaces/expression_union-alpha_20260917_221034/proofsB/.lean-runs/20260917_235057_87542037/lib/lean/Common

- `Workspaces/expression_union-alpha_20260917_221034/proofsB/.lean-runs/20260917_235057_87542037/lib/lean/Common/DirB.olean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsB/.lean-runs/20260917_235057_87542037/lib/lean/Common/Operators.olean`

## Workspaces/expression_union-alpha_20260917_221034/proofsB/.lean-runs/20260917_235057_87542037/lib/lean

- `Workspaces/expression_union-alpha_20260917_221034/proofsB/.lean-runs/20260917_235057_87542037/lib/lean/Main.olean`

## Workspaces/expression_union-alpha_20260917_221034/proofsB/.lean-runs/20260917_235057_87542037

- `Workspaces/expression_union-alpha_20260917_221034/proofsB/.lean-runs/20260917_235057_87542037/result.json`

## Workspaces/expression_union-alpha_20260917_221034/proofsB/Common

- `Workspaces/expression_union-alpha_20260917_221034/proofsB/Common/DirB.lean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsB/Common/Operators.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsB

- `Workspaces/expression_union-alpha_20260917_221034/proofsB/LEAN_POLICY.md`
- `Workspaces/expression_union-alpha_20260917_221034/proofsB/Main.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsC/.lean-runs/20260917_235319_5851b38b

- `Workspaces/expression_union-alpha_20260917_221034/proofsC/.lean-runs/20260917_235319_5851b38b/build.log`

## Workspaces/expression_union-alpha_20260917_221034/proofsC/.lean-runs/20260917_235319_5851b38b/lib/lean/Common

- `Workspaces/expression_union-alpha_20260917_221034/proofsC/.lean-runs/20260917_235319_5851b38b/lib/lean/Common/DirC.olean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsC/.lean-runs/20260917_235319_5851b38b/lib/lean/Common/Operators.olean`

## Workspaces/expression_union-alpha_20260917_221034/proofsC/.lean-runs/20260917_235319_5851b38b/lib/lean

- `Workspaces/expression_union-alpha_20260917_221034/proofsC/.lean-runs/20260917_235319_5851b38b/lib/lean/Main.olean`

## Workspaces/expression_union-alpha_20260917_221034/proofsC/.lean-runs/20260917_235319_5851b38b

- `Workspaces/expression_union-alpha_20260917_221034/proofsC/.lean-runs/20260917_235319_5851b38b/result.json`

## Workspaces/expression_union-alpha_20260917_221034/proofsC/Common

- `Workspaces/expression_union-alpha_20260917_221034/proofsC/Common/DirC.lean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsC/Common/Operators.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsC

- `Workspaces/expression_union-alpha_20260917_221034/proofsC/LEAN_POLICY.md`
- `Workspaces/expression_union-alpha_20260917_221034/proofsC/Main.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsD/.lean-runs/20260917_235434_a30875fb

- `Workspaces/expression_union-alpha_20260917_221034/proofsD/.lean-runs/20260917_235434_a30875fb/build.log`

## Workspaces/expression_union-alpha_20260917_221034/proofsD/.lean-runs/20260917_235434_a30875fb/lib/lean/Common

- `Workspaces/expression_union-alpha_20260917_221034/proofsD/.lean-runs/20260917_235434_a30875fb/lib/lean/Common/DirD.olean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsD/.lean-runs/20260917_235434_a30875fb/lib/lean/Common/Operators.olean`

## Workspaces/expression_union-alpha_20260917_221034/proofsD/.lean-runs/20260917_235434_a30875fb/lib/lean

- `Workspaces/expression_union-alpha_20260917_221034/proofsD/.lean-runs/20260917_235434_a30875fb/lib/lean/Main.olean`

## Workspaces/expression_union-alpha_20260917_221034/proofsD/.lean-runs/20260917_235434_a30875fb

- `Workspaces/expression_union-alpha_20260917_221034/proofsD/.lean-runs/20260917_235434_a30875fb/result.json`

## Workspaces/expression_union-alpha_20260917_221034/proofsD/Common

- `Workspaces/expression_union-alpha_20260917_221034/proofsD/Common/DirD.lean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsD/Common/Operators.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsD

- `Workspaces/expression_union-alpha_20260917_221034/proofsD/LEAN_POLICY.md`
- `Workspaces/expression_union-alpha_20260917_221034/proofsD/Main.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsE/.lean-runs/20260917_235540_a7742423/lib/lean/Common

- `Workspaces/expression_union-alpha_20260917_221034/proofsE/.lean-runs/20260917_235540_a7742423/lib/lean/Common/Operators.olean`

## Workspaces/expression_union-alpha_20260917_221034/proofsE/Common

- `Workspaces/expression_union-alpha_20260917_221034/proofsE/Common/DirE.lean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsE/Common/Operators.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsE

- `Workspaces/expression_union-alpha_20260917_221034/proofsE/LEAN_POLICY.md`
- `Workspaces/expression_union-alpha_20260917_221034/proofsE/Main.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsF/Common

- `Workspaces/expression_union-alpha_20260917_221034/proofsF/Common/DirF.lean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsF/Common/Operators.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsF

- `Workspaces/expression_union-alpha_20260917_221034/proofsF/LEAN_POLICY.md`
- `Workspaces/expression_union-alpha_20260917_221034/proofsF/Main.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsG/Common

- `Workspaces/expression_union-alpha_20260917_221034/proofsG/Common/DirG.lean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsG/Common/Operators.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsG

- `Workspaces/expression_union-alpha_20260917_221034/proofsG/LEAN_POLICY.md`
- `Workspaces/expression_union-alpha_20260917_221034/proofsG/Main.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsH/Common

- `Workspaces/expression_union-alpha_20260917_221034/proofsH/Common/DirH.lean`
- `Workspaces/expression_union-alpha_20260917_221034/proofsH/Common/Operators.lean`

## Workspaces/expression_union-alpha_20260917_221034/proofsH

- `Workspaces/expression_union-alpha_20260917_221034/proofsH/LEAN_POLICY.md`
- `Workspaces/expression_union-alpha_20260917_221034/proofsH/Main.lean`

## Workspaces/expression_union-alpha_20260917_221034

- `Workspaces/expression_union-alpha_20260917_221034/RUN_CONTEXT.md`

## Workspaces/gsg_project/code/_scratch

- `Workspaces/gsg_project/code/_scratch/amp.py`
- `Workspaces/gsg_project/code/_scratch/amp2.py`
- `Workspaces/gsg_project/code/_scratch/check_core_identities.py`
- `Workspaces/gsg_project/code/_scratch/check_n1_candidates.py`
- `Workspaces/gsg_project/code/_scratch/check_n1_symbolic.py`
- `Workspaces/gsg_project/code/_scratch/dbg1.py`
- `Workspaces/gsg_project/code/_scratch/dbg2.py`
- `Workspaces/gsg_project/code/_scratch/dbg3.py`
- `Workspaces/gsg_project/code/_scratch/dlw_core.py`
- `Workspaces/gsg_project/code/_scratch/explore1.py`
- `Workspaces/gsg_project/code/_scratch/mshift2.py`
- `Workspaces/gsg_project/code/_scratch/solve_n1_symbolic.py`
- `Workspaces/gsg_project/code/_scratch/solve_n2_universal.py`
- `Workspaces/gsg_project/code/_scratch/solve_n2_wide.py`
- `Workspaces/gsg_project/code/_scratch/solve_twosite.py`
- `Workspaces/gsg_project/code/_scratch/solve_x2.py`
- `Workspaces/gsg_project/code/_scratch/solve_xlattice.py`
- `Workspaces/gsg_project/code/_scratch/solve_xlattice2.py`
- `Workspaces/gsg_project/code/_scratch/solve_y_full.py`
- `Workspaces/gsg_project/code/_scratch/t1.py`
- `Workspaces/gsg_project/code/_scratch/t10.py`
- `Workspaces/gsg_project/code/_scratch/t11.py`
- `Workspaces/gsg_project/code/_scratch/t12.py`
- `Workspaces/gsg_project/code/_scratch/t2.py`
- `Workspaces/gsg_project/code/_scratch/t3.py`
- `Workspaces/gsg_project/code/_scratch/t4.py`
- `Workspaces/gsg_project/code/_scratch/t5.py`
- `Workspaces/gsg_project/code/_scratch/t6.py`
- `Workspaces/gsg_project/code/_scratch/t7.py`
- `Workspaces/gsg_project/code/_scratch/t8.py`
- `Workspaces/gsg_project/code/_scratch/t9.py`
- `Workspaces/gsg_project/code/_scratch/test_exp_form.py`

## Workspaces/gsg_project/code

- `Workspaces/gsg_project/code/check_n1_chi.py`
- `Workspaces/gsg_project/code/engine.py`
- `Workspaces/gsg_project/code/independent_verify.py`
- `Workspaces/gsg_project/code/main_checks.py`
- `Workspaces/gsg_project/code/mshift.py`
- `Workspaces/gsg_project/code/obstruction.py`
- `Workspaces/gsg_project/code/onesoliton_check.py`
- `Workspaces/gsg_project/code/soliton_analysis.py`
- `Workspaces/gsg_project/code/solve_n1_numeric.py`
- `Workspaces/gsg_project/code/solve_n1_universal.py`
- `Workspaces/gsg_project/code/solve_n1_x2.py`
- `Workspaces/gsg_project/code/solve_x2_3site.py`
- `Workspaces/gsg_project/code/t13.py`
- `Workspaces/gsg_project/code/t14_staggered.py`
- `Workspaces/gsg_project/code/t15_search6.py`
- `Workspaces/gsg_project/code/verify_nullvec.py`

## Workspaces/gsg_project/dlw_report

- `Workspaces/gsg_project/dlw_report/_add_banner.py`

## Workspaces/gsg_project/dlw_report/_assets

- `Workspaces/gsg_project/dlw_report/_assets/katex-0.18.7.tgz`

## Workspaces/gsg_project/dlw_report/_src

- `Workspaces/gsg_project/dlw_report/_src/index.src.html`
- `Workspaces/gsg_project/dlw_report/_src/lean_verification.src.html`
- `Workspaces/gsg_project/dlw_report/_src/numerical_analysis.src.html`

## Workspaces/gsg_project/dlw_report

- `Workspaces/gsg_project/dlw_report/build_html.ps1`
- `Workspaces/gsg_project/dlw_report/check_template.py`
- `Workspaces/gsg_project/dlw_report/numerical_results_validation.json`
- `Workspaces/gsg_project/dlw_report/route1_sync_validation.json`
- `Workspaces/gsg_project/dlw_report/sync_numerical_results.py`
- `Workspaces/gsg_project/dlw_report/validate_route1_sync.py`
- `Workspaces/gsg_project/dlw_report/verify_claims.py`
- `Workspaces/gsg_project/dlw_report/verify_output.txt`

## Workspaces/gsg_project/fundamentals

- `Workspaces/gsg_project/fundamentals/loop_demo.csv`
- `Workspaces/gsg_project/fundamentals/loop_demo.png`
- `Workspaces/gsg_project/fundamentals/loop_soliton_demo.py`

## Workspaces/gsg_project/lax

- `Workspaces/gsg_project/lax/cons.py`
- `Workspaces/gsg_project/lax/cons2.py`
- `Workspaces/gsg_project/lax/conserved.py`
- `Workspaces/gsg_project/lax/conslaws.py`
- `Workspaces/gsg_project/lax/core.py`
- `Workspaces/gsg_project/lax/crosscheck.py`
- `Workspaces/gsg_project/lax/curve.py`
- `Workspaces/gsg_project/lax/diag1.py`
- `Workspaces/gsg_project/lax/dkp.py`
- `Workspaces/gsg_project/lax/final_check.py`
- `Workspaces/gsg_project/lax/final_test.py`
- `Workspaces/gsg_project/lax/final_verdict.py`
- `Workspaces/gsg_project/lax/FINAL.py`
- `Workspaces/gsg_project/lax/final2.py`
- `Workspaces/gsg_project/lax/gen_cons.py`
- `Workspaces/gsg_project/lax/gen.py`
- `Workspaces/gsg_project/lax/lax1.py`
- `Workspaces/gsg_project/lax/lax10.py`
- `Workspaces/gsg_project/lax/lax11.py`
- `Workspaces/gsg_project/lax/lax12.py`
- `Workspaces/gsg_project/lax/lax2.py`
- `Workspaces/gsg_project/lax/lax3.py`
- `Workspaces/gsg_project/lax/lax4.py`
- `Workspaces/gsg_project/lax/lax5.py`
- `Workspaces/gsg_project/lax/lax6.py`
- `Workspaces/gsg_project/lax/lax7.py`
- `Workspaces/gsg_project/lax/lax8.py`
- `Workspaces/gsg_project/lax/lax9.py`
- `Workspaces/gsg_project/lax/laxfinal.py`
- `Workspaces/gsg_project/lax/laxpair.py`
- `Workspaces/gsg_project/lax/laxverify.py`
- `Workspaces/gsg_project/lax/link.py`
- `Workspaces/gsg_project/lax/mono.py`
- `Workspaces/gsg_project/lax/mpt.py`
- `Workspaces/gsg_project/lax/numeric_check.py`
- `Workspaces/gsg_project/lax/numeric_check2.py`
- `Workspaces/gsg_project/lax/probe1.py`
- `Workspaces/gsg_project/lax/probe2.py`
- `Workspaces/gsg_project/lax/probe3.py`
- `Workspaces/gsg_project/lax/probe4.py`
- `Workspaces/gsg_project/lax/probe5.py`
- `Workspaces/gsg_project/lax/rank.py`
- `Workspaces/gsg_project/lax/REPORT_LAX.md`
- `Workspaces/gsg_project/lax/tau_ref.py`
- `Workspaces/gsg_project/lax/tau2.py`
- `Workspaces/gsg_project/lax/tau3.py`
- `Workspaces/gsg_project/lax/tau4.py`
- `Workspaces/gsg_project/lax/v3.py`
- `Workspaces/gsg_project/lax/v4.py`
- `Workspaces/gsg_project/lax/validate_ref.py`
- `Workspaces/gsg_project/lax/VERDICT.md`
- `Workspaces/gsg_project/lax/verify_final.py`
- `Workspaces/gsg_project/lax/verify_structure.py`
- `Workspaces/gsg_project/lax/verify2.py`
- `Workspaces/gsg_project/lax/veto.py`
- `Workspaces/gsg_project/lax/veto2.py`
- `Workspaces/gsg_project/lax/wave.py`

## Workspaces/gsg_project

- `Workspaces/gsg_project/OUT_GSG_DLW_report.md`
- `Workspaces/gsg_project/OUT_GSG_DLW_short_report.md`

## Workspaces/gsg_project/out

- `Workspaces/gsg_project/out/verification_log.txt`

## Workspaces/lean_contracts/_c02_scratch

- `Workspaces/lean_contracts/_c02_scratch/appendix.lean`
- `Workspaces/lean_contracts/_c02_scratch/build.ps1`
- `Workspaces/lean_contracts/_c02_scratch/build2.ps1`
- `Workspaces/lean_contracts/_c02_scratch/build3.ps1`
- `Workspaces/lean_contracts/_c02_scratch/check_old_form.py`
- `Workspaces/lean_contracts/_c02_scratch/merge.ps1`
- `Workspaces/lean_contracts/_c02_scratch/new_header.txt`

## Workspaces/lean_contracts/_c02_scratch/olean

- `Workspaces/lean_contracts/_c02_scratch/olean/Contracts.olean`
- `Workspaces/lean_contracts/_c02_scratch/olean/PkgC02_merged.olean`
- `Workspaces/lean_contracts/_c02_scratch/olean/PkgC02.olean`
- `Workspaces/lean_contracts/_c02_scratch/olean/PkgQuotientRate.olean`

## Workspaces/lean_contracts/_c02_scratch

- `Workspaces/lean_contracts/_c02_scratch/PkgC02.lean.orig_backup`
- `Workspaces/lean_contracts/_c02_scratch/Probe2.lean`
- `Workspaces/lean_contracts/_c02_scratch/verify_c02_cert.py`
- `Workspaces/lean_contracts/_c02_scratch/verify_c02_cert2.py`

## Workspaces/lean_contracts/_c11dev/lib/lean

- `Workspaces/lean_contracts/_c11dev/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/_c11dev/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/_c11dev/lib/lean/PkgNumeric.olean`

## Workspaces/lean_contracts/.dev

- `Workspaces/lean_contracts/.dev/devcheck.ps1`

## Workspaces/lean_contracts/.dev/lib/lean

- `Workspaces/lean_contracts/.dev/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/.dev/lib/lean/PkgNonlinear.olean`

## Workspaces/lean_contracts

- `Workspaces/lean_contracts/audit_c02_final.py`
- `Workspaces/lean_contracts/audit_c02_linalg.py`
- `Workspaces/lean_contracts/audit_c02_mult.py`
- `Workspaces/lean_contracts/audit_c02_mult2.py`
- `Workspaces/lean_contracts/audit_c02_mult3.py`
- `Workspaces/lean_contracts/audit_c02_reduce.py`
- `Workspaces/lean_contracts/audit_c02_rigorous.py`
- `Workspaces/lean_contracts/audit_c02_subsets.py`
- `Workspaces/lean_contracts/audit_c02_which.py`
- `Workspaces/lean_contracts/audit_c02_which2.py`
- `Workspaces/lean_contracts/audit_c02.py`
- `Workspaces/lean_contracts/audit_c07.py`
- `Workspaces/lean_contracts/audit_c14.py`
- `Workspaces/lean_contracts/audit_c14b.py`
- `Workspaces/lean_contracts/audit_c14c.py`
- `Workspaces/lean_contracts/audit_c18.py`
- `Workspaces/lean_contracts/continue_c09.py`
- `Workspaces/lean_contracts/finalize_all_targets.py`
- `Workspaces/lean_contracts/fix_c09_polynomial.py`
- `Workspaces/lean_contracts/NEXT_TARGETS.md`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_093620_6b743d56

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_093620_6b743d56/build.log`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_093620_6b743d56/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_093909_78b61667

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_093909_78b61667/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_093909_78b61667/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_093909_78b61667/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_093909_78b61667

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_093909_78b61667/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_094053_d70ad09a

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094053_d70ad09a/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_094053_d70ad09a/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094053_d70ad09a/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_094053_d70ad09a

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094053_d70ad09a/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_094214_5ce8aefb

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094214_5ce8aefb/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_094214_5ce8aefb/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094214_5ce8aefb/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_094214_5ce8aefb

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094214_5ce8aefb/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_094300_e20cbdfe

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094300_e20cbdfe/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_094300_e20cbdfe/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094300_e20cbdfe/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094300_e20cbdfe/lib/lean/PkgTrivial.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_094300_e20cbdfe

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094300_e20cbdfe/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_094816_b8b7dfe2

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094816_b8b7dfe2/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_094816_b8b7dfe2/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094816_b8b7dfe2/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_094816_b8b7dfe2

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094816_b8b7dfe2/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_094817_883250c5

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094817_883250c5/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_094817_883250c5/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094817_883250c5/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094817_883250c5/lib/lean/PkgTrivial.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_094817_883250c5

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_094817_883250c5/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_095509_debb9c39

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_095509_debb9c39/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_095509_debb9c39/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_095509_debb9c39/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_095509_debb9c39

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_095509_debb9c39/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_095543_0908fd08

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_095543_0908fd08/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_095543_0908fd08/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_095543_0908fd08/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_095543_0908fd08

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_095543_0908fd08/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_095819_91eda416

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_095819_91eda416/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_095819_91eda416/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_095819_91eda416/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_095819_91eda416

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_095819_91eda416/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_095826_490db071

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_095826_490db071/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_095826_490db071/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_095826_490db071/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_095826_490db071

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_095826_490db071/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100005_9f9495da

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100005_9f9495da/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100005_9f9495da/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100005_9f9495da/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100005_9f9495da

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100005_9f9495da/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100156_353f5556

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100156_353f5556/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100156_353f5556/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100156_353f5556/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100156_353f5556

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100156_353f5556/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100234_793cb8c0

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100234_793cb8c0/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100234_793cb8c0/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100234_793cb8c0/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100234_793cb8c0/lib/lean/ProbeGramEntry2.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100234_793cb8c0

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100234_793cb8c0/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100346_ee418007

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100346_ee418007/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100346_ee418007/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100346_ee418007/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100346_ee418007/lib/lean/PkgGramEntry.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100346_ee418007

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100346_ee418007/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100355_9539bf63

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100355_9539bf63/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100355_9539bf63/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100355_9539bf63/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100355_9539bf63

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100355_9539bf63/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100442_55008ab6

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100442_55008ab6/build.log`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100442_55008ab6/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100444_0b530ea3

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100444_0b530ea3/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100444_0b530ea3/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100444_0b530ea3/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100444_0b530ea3/lib/lean/PkgGramEntry.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100444_0b530ea3

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100444_0b530ea3/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100537_adabc663

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100537_adabc663/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100537_adabc663/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100537_adabc663/lib/lean/ProbeContinuous.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100537_adabc663

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100537_adabc663/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100721_a0fa1621

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100721_a0fa1621/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100721_a0fa1621/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100721_a0fa1621/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100721_a0fa1621/lib/lean/PkgQuotientRate.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100721_a0fa1621

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100721_a0fa1621/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100818_d379bcdc

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100818_d379bcdc/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100818_d379bcdc/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100818_d379bcdc/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100818_d379bcdc/lib/lean/PkgQuotientRate.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_100818_d379bcdc

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_100818_d379bcdc/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_101118_a9941fd0

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_101118_a9941fd0/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_101118_a9941fd0/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_101118_a9941fd0/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_101118_a9941fd0

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_101118_a9941fd0/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_101139_51e1d818

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_101139_51e1d818/build.log`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_101139_51e1d818/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_101357_06bf7bbb

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_101357_06bf7bbb/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_101357_06bf7bbb/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_101357_06bf7bbb/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_101357_06bf7bbb

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_101357_06bf7bbb/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_101551_3e1f9b7b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_101551_3e1f9b7b/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_101551_3e1f9b7b/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_101551_3e1f9b7b/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_101551_3e1f9b7b/lib/lean/PkgContinuous.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_101551_3e1f9b7b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_101551_3e1f9b7b/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_102641_3a4a67c1

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_102641_3a4a67c1/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_102641_3a4a67c1/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_102641_3a4a67c1/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_102641_3a4a67c1

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_102641_3a4a67c1/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_102732_05fa73b4

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_102732_05fa73b4/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_102732_05fa73b4/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_102732_05fa73b4/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_102732_05fa73b4/lib/lean/Main.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_102732_05fa73b4/lib/lean/PkgContinuous.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_102732_05fa73b4/lib/lean/PkgGramEntry.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_102732_05fa73b4/lib/lean/PkgQuotientRate.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_102732_05fa73b4/lib/lean/PkgTrivial.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_102732_05fa73b4

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_102732_05fa73b4/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_103419_5d932ba1

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_103419_5d932ba1/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_103419_5d932ba1/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_103419_5d932ba1/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_103419_5d932ba1

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_103419_5d932ba1/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_103528_0f7bbdf6

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_103528_0f7bbdf6/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_103528_0f7bbdf6/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_103528_0f7bbdf6/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_103528_0f7bbdf6/lib/lean/PkgLattice.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_103528_0f7bbdf6

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_103528_0f7bbdf6/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104130_578f5abd

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104130_578f5abd/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104130_578f5abd/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104130_578f5abd/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104130_578f5abd

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104130_578f5abd/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104428_fad9c9d1

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104428_fad9c9d1/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104428_fad9c9d1/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104428_fad9c9d1/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104428_fad9c9d1

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104428_fad9c9d1/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104606_7282603b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104606_7282603b/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104606_7282603b/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104606_7282603b/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104606_7282603b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104606_7282603b/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104724_07fa1c84

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104724_07fa1c84/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104724_07fa1c84/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104724_07fa1c84/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104724_07fa1c84

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104724_07fa1c84/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104802_cc90492e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104802_cc90492e/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104802_cc90492e/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104802_cc90492e/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104802_cc90492e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104802_cc90492e/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104836_6c962820

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104836_6c962820/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104836_6c962820/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104836_6c962820/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104836_6c962820/lib/lean/PkgNumeric.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104836_6c962820

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104836_6c962820/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104932_8d3c3f56

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104932_8d3c3f56/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104932_8d3c3f56/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104932_8d3c3f56/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104932_8d3c3f56/lib/lean/PkgLattice.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_104932_8d3c3f56

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_104932_8d3c3f56/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_105127_fee8076f

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_105127_fee8076f/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_105127_fee8076f/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_105127_fee8076f/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_105127_fee8076f/lib/lean/Main.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_105127_fee8076f/lib/lean/PkgContinuous.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_105127_fee8076f/lib/lean/PkgGramEntry.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_105127_fee8076f/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_105127_fee8076f/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_105127_fee8076f/lib/lean/PkgQuotientRate.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_105127_fee8076f/lib/lean/PkgTrivial.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_105127_fee8076f

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_105127_fee8076f/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_105215_a1faf55b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_105215_a1faf55b/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_105215_a1faf55b/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_105215_a1faf55b/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_105215_a1faf55b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_105215_a1faf55b/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_110322_27ba250c

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_110322_27ba250c/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_110322_27ba250c/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_110322_27ba250c/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_110322_27ba250c

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_110322_27ba250c/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_110642_ec4feac2

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_110642_ec4feac2/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_110642_ec4feac2/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_110642_ec4feac2/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_110642_ec4feac2

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_110642_ec4feac2/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_110852_5fdbde16

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_110852_5fdbde16/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_110852_5fdbde16/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_110852_5fdbde16/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_110852_5fdbde16

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_110852_5fdbde16/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_111124_ff032711

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_111124_ff032711/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_111124_ff032711/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_111124_ff032711/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_111124_ff032711

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_111124_ff032711/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_111438_194ec65e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_111438_194ec65e/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_111438_194ec65e/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_111438_194ec65e/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_111438_194ec65e/lib/lean/ProbeNonlinear.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_111438_194ec65e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_111438_194ec65e/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_112535_0814bff7

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_112535_0814bff7/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_112535_0814bff7/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_112535_0814bff7/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_112535_0814bff7/lib/lean/ProbeNonlinear.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_112535_0814bff7

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_112535_0814bff7/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_112943_9a2f0e5f

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_112943_9a2f0e5f/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_112943_9a2f0e5f/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_112943_9a2f0e5f/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_112943_9a2f0e5f

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_112943_9a2f0e5f/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_113032_5ff59a9c

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_113032_5ff59a9c/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_113032_5ff59a9c/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_113032_5ff59a9c/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_113032_5ff59a9c/lib/lean/PkgC02.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_113032_5ff59a9c

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_113032_5ff59a9c/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_114510_a1288240

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_114510_a1288240/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_114510_a1288240/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_114510_a1288240/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_114510_a1288240/lib/lean/PkgNonlinear.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_114510_a1288240

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_114510_a1288240/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_115549_8d4d46d9

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_115549_8d4d46d9/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_115549_8d4d46d9/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_115549_8d4d46d9/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_115549_8d4d46d9/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_115549_8d4d46d9/lib/lean/PkgNumeric.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_115549_8d4d46d9

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_115549_8d4d46d9/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_121033_36920a33

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_121033_36920a33/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_121033_36920a33/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_121033_36920a33/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_121033_36920a33/lib/lean/PkgNonlinear.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_121033_36920a33

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_121033_36920a33/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_121158_7eb4a5b8

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_121158_7eb4a5b8/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_121158_7eb4a5b8/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_121158_7eb4a5b8/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_121158_7eb4a5b8/lib/lean/PkgNonlinear.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_121158_7eb4a5b8

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_121158_7eb4a5b8/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_121556_924a57da

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_121556_924a57da/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_121556_924a57da/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_121556_924a57da/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_121556_924a57da/lib/lean/PkgC02.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_121556_924a57da

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_121556_924a57da/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6/lib/lean/Main.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6/lib/lean/PkgContinuous.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6/lib/lean/PkgGramEntry.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6/lib/lean/PkgNonlinear.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6/lib/lean/PkgQuotientRate.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6/lib/lean/PkgTrivial.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_122257_656f4ec6/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0/lib/lean/Main.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0/lib/lean/PkgContinuous.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0/lib/lean/PkgGramEntry.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0/lib/lean/PkgNonlinear.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0/lib/lean/PkgQuotientRate.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0/lib/lean/PkgTrivial.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_123007_8274bbe0/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_124536_054847e5

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_124536_054847e5/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_124536_054847e5/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_124536_054847e5/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_124536_054847e5

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_124536_054847e5/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_124758_9aa11b2c

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_124758_9aa11b2c/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_124758_9aa11b2c/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_124758_9aa11b2c/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_124758_9aa11b2c/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_124758_9aa11b2c/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_124758_9aa11b2c/lib/lean/PkgNumeric.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_124758_9aa11b2c

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_124758_9aa11b2c/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_124922_c245d228

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_124922_c245d228/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_124922_c245d228/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_124922_c245d228/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_124922_c245d228

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_124922_c245d228/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_125149_72448bd6

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125149_72448bd6/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_125149_72448bd6/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125149_72448bd6/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_125149_72448bd6

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125149_72448bd6/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_125225_56faa6b8

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125225_56faa6b8/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_125225_56faa6b8/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125225_56faa6b8/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125225_56faa6b8/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125225_56faa6b8/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125225_56faa6b8/lib/lean/PkgNumeric.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_125225_56faa6b8

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125225_56faa6b8/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_125418_7dc0f672

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125418_7dc0f672/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_125418_7dc0f672/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125418_7dc0f672/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125418_7dc0f672/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125418_7dc0f672/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125418_7dc0f672/lib/lean/PkgC17.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125418_7dc0f672/lib/lean/PkgNumeric.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_125418_7dc0f672

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125418_7dc0f672/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_125541_ede8547c

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125541_ede8547c/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_125541_ede8547c/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125541_ede8547c/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_125541_ede8547c

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125541_ede8547c/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e/lib/lean/Main.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e/lib/lean/PkgC17.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e/lib/lean/PkgContinuous.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e/lib/lean/PkgGramEntry.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e/lib/lean/PkgNonlinear.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e/lib/lean/PkgQuotientRate.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e/lib/lean/PkgTrivial.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_125635_4e9e9d5e/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_141127_54b5bc8e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141127_54b5bc8e/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_141127_54b5bc8e/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141127_54b5bc8e/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_141127_54b5bc8e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141127_54b5bc8e/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_141227_e0fae953

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141227_e0fae953/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_141227_e0fae953/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141227_e0fae953/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_141227_e0fae953

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141227_e0fae953/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_141343_83426d83

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141343_83426d83/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_141343_83426d83/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141343_83426d83/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_141343_83426d83

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141343_83426d83/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_141459_2118cfbb

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141459_2118cfbb/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_141459_2118cfbb/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141459_2118cfbb/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_141459_2118cfbb

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141459_2118cfbb/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_141556_e14709ce

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141556_e14709ce/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_141556_e14709ce/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141556_e14709ce/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141556_e14709ce/lib/lean/PkgC09.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_141556_e14709ce

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_141556_e14709ce/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_143532_75591ba0

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_143532_75591ba0/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_143532_75591ba0/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_143532_75591ba0/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_143532_75591ba0

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_143532_75591ba0/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_144023_e97d1f1b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_144023_e97d1f1b/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_144023_e97d1f1b/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_144023_e97d1f1b/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_144023_e97d1f1b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_144023_e97d1f1b/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_144435_002e2908

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_144435_002e2908/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_144435_002e2908/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_144435_002e2908/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_144435_002e2908

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_144435_002e2908/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_160338_1cc6cce6

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_160338_1cc6cce6/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_160338_1cc6cce6/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_160338_1cc6cce6/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_160338_1cc6cce6

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_160338_1cc6cce6/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec/lib/lean/Main.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec/lib/lean/PkgC17.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec/lib/lean/PkgContinuous.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec/lib/lean/PkgGramEntry.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec/lib/lean/PkgNonlinear.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec/lib/lean/PkgQuotientRate.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec/lib/lean/PkgTrivial.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163644_cb1451ec/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_163721_902b2f0e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163721_902b2f0e/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_163721_902b2f0e/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163721_902b2f0e/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_163721_902b2f0e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_163721_902b2f0e/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_164034_2bc06514

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164034_2bc06514/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_164034_2bc06514/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164034_2bc06514/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_164034_2bc06514

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164034_2bc06514/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_164237_61136837

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164237_61136837/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_164237_61136837/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164237_61136837/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_164237_61136837

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164237_61136837/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_164621_4333d332

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164621_4333d332/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_164621_4333d332/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164621_4333d332/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_164621_4333d332

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164621_4333d332/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_164729_5d1a1762

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164729_5d1a1762/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_164729_5d1a1762/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164729_5d1a1762/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164729_5d1a1762/lib/lean/PkgGramBridges.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164729_5d1a1762/lib/lean/PkgGramEntry.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164729_5d1a1762/lib/lean/PkgNonlinear.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_164729_5d1a1762

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164729_5d1a1762/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_164855_77d6933b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164855_77d6933b/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_164855_77d6933b/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164855_77d6933b/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164855_77d6933b/lib/lean/PkgC09Complete.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_164855_77d6933b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_164855_77d6933b/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_165142_50bf7522

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165142_50bf7522/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_165142_50bf7522/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165142_50bf7522/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165142_50bf7522/lib/lean/PkgNumeric.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_165142_50bf7522

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165142_50bf7522/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_165305_d75ea4ac

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165305_d75ea4ac/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_165305_d75ea4ac/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165305_d75ea4ac/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165305_d75ea4ac/lib/lean/PkgNumeric.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_165305_d75ea4ac

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165305_d75ea4ac/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_165506_5bb68fc8

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165506_5bb68fc8/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_165506_5bb68fc8/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165506_5bb68fc8/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165506_5bb68fc8/lib/lean/PkgNumeric.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_165506_5bb68fc8

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165506_5bb68fc8/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_165946_d71349ac

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165946_d71349ac/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_165946_d71349ac/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165946_d71349ac/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165946_d71349ac/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165946_d71349ac/lib/lean/PkgRK4.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_165946_d71349ac

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_165946_d71349ac/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean/Main.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean/PkgC17.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean/PkgContinuous.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean/PkgGramBridges.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean/PkgGramEntry.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean/PkgNonlinear.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean/PkgQuotientRate.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean/PkgRK4.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/lib/lean/PkgTrivial.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_170312_ccfb42ed/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_173531_7d023b9f

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_173531_7d023b9f/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_173531_7d023b9f/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_173531_7d023b9f/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_173531_7d023b9f/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_173531_7d023b9f/lib/lean/PkgRK4.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_173531_7d023b9f

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_173531_7d023b9f/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_180212_e8c4db1c

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180212_e8c4db1c/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_180212_e8c4db1c/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180212_e8c4db1c/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180212_e8c4db1c/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180212_e8c4db1c/lib/lean/PkgRK4.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_180212_e8c4db1c

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180212_e8c4db1c/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_180419_3460d784

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180419_3460d784/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_180419_3460d784/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180419_3460d784/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180419_3460d784/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180419_3460d784/lib/lean/PkgRK4.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_180419_3460d784

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180419_3460d784/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_180631_ef8276b9

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180631_ef8276b9/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_180631_ef8276b9/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180631_ef8276b9/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180631_ef8276b9/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180631_ef8276b9/lib/lean/PkgRK4.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_180631_ef8276b9

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180631_ef8276b9/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_180807_acd365eb

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180807_acd365eb/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_180807_acd365eb/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180807_acd365eb/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180807_acd365eb/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180807_acd365eb/lib/lean/PkgRK4.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180807_acd365eb/lib/lean/PkgRK4Complete.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_180807_acd365eb

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_180807_acd365eb/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_181153_3a607bac

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181153_3a607bac/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_181153_3a607bac/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181153_3a607bac/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181153_3a607bac/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181153_3a607bac/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181153_3a607bac/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181153_3a607bac/lib/lean/PkgNumeric.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_181153_3a607bac

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181153_3a607bac/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_181543_aac944d7

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181543_aac944d7/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_181543_aac944d7/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181543_aac944d7/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181543_aac944d7/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181543_aac944d7/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181543_aac944d7/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181543_aac944d7/lib/lean/PkgNumeric.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_181543_aac944d7

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181543_aac944d7/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_181914_db68496b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181914_db68496b/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_181914_db68496b/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181914_db68496b/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181914_db68496b/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181914_db68496b/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181914_db68496b/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181914_db68496b/lib/lean/PkgNumeric.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_181914_db68496b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_181914_db68496b/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_182705_bcc35126

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_182705_bcc35126/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_182705_bcc35126/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_182705_bcc35126/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_182705_bcc35126/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_182705_bcc35126/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_182705_bcc35126/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_182705_bcc35126/lib/lean/PkgNumeric.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_182705_bcc35126

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_182705_bcc35126/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_183158_49b3f258

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183158_49b3f258/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_183158_49b3f258/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183158_49b3f258/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183158_49b3f258/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183158_49b3f258/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183158_49b3f258/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183158_49b3f258/lib/lean/PkgNumeric.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_183158_49b3f258

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183158_49b3f258/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_183352_b3418288

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183352_b3418288/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_183352_b3418288/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183352_b3418288/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_183352_b3418288

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183352_b3418288/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_183655_b6a07394

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183655_b6a07394/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_183655_b6a07394/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183655_b6a07394/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183655_b6a07394/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183655_b6a07394/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183655_b6a07394/lib/lean/PkgC18Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183655_b6a07394/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183655_b6a07394/lib/lean/PkgNumeric.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_183655_b6a07394

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183655_b6a07394/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_183845_e4a86459

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183845_e4a86459/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_183845_e4a86459/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183845_e4a86459/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_183845_e4a86459

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_183845_e4a86459/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_205202_c6138cb3

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205202_c6138cb3/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_205202_c6138cb3/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205202_c6138cb3/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_205202_c6138cb3

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205202_c6138cb3/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/Main.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/PkgC17.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/PkgC18Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/PkgContinuous.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/PkgGramBridges.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/PkgGramEntry.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/PkgNonlinear.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/PkgQuotientRate.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/PkgRK4.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/PkgRK4Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/lib/lean/PkgTrivial.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205213_cf5e67c9/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_205623_b1d87593

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205623_b1d87593/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_205623_b1d87593/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205623_b1d87593/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205623_b1d87593/lib/lean/PkgGramDeterminant.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_205623_b1d87593

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205623_b1d87593/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_205828_5b80265b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205828_5b80265b/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_205828_5b80265b/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205828_5b80265b/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_205828_5b80265b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205828_5b80265b/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_205949_18338570

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205949_18338570/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_205949_18338570/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205949_18338570/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_205949_18338570

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_205949_18338570/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210114_eace6246

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210114_eace6246/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210114_eace6246/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210114_eace6246/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210114_eace6246

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210114_eace6246/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210254_b4ad60eb

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210254_b4ad60eb/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210254_b4ad60eb/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210254_b4ad60eb/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210254_b4ad60eb/lib/lean/PkgGramDeterminant.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210254_b4ad60eb

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210254_b4ad60eb/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210446_0bc77c9f

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210446_0bc77c9f/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210446_0bc77c9f/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210446_0bc77c9f/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210446_0bc77c9f/lib/lean/PkgGramDeterminant.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210446_0bc77c9f

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210446_0bc77c9f/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210457_5f3cfc78

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210457_5f3cfc78/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210457_5f3cfc78/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210457_5f3cfc78/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210457_5f3cfc78/lib/lean/PkgGramDeterminant.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210457_5f3cfc78

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210457_5f3cfc78/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210727_e37e4f56

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210727_e37e4f56/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210727_e37e4f56/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210727_e37e4f56/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210727_e37e4f56/lib/lean/PkgGramDeterminant.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210727_e37e4f56/lib/lean/PkgGramPlucker.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210727_e37e4f56

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210727_e37e4f56/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210738_474ab5ed

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210738_474ab5ed/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210738_474ab5ed/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210738_474ab5ed/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210738_474ab5ed/lib/lean/PkgGramCalculus.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210738_474ab5ed/lib/lean/PkgGramDeterminant.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210738_474ab5ed

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210738_474ab5ed/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210950_f15a99f5

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210950_f15a99f5/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210950_f15a99f5/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210950_f15a99f5/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210950_f15a99f5/lib/lean/PkgGramDeterminant.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210950_f15a99f5/lib/lean/PkgGramPlucker.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_210950_f15a99f5

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_210950_f15a99f5/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211135_dc5e70c3

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211135_dc5e70c3/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211135_dc5e70c3/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211135_dc5e70c3/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211135_dc5e70c3/lib/lean/PkgGramCalculus.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211135_dc5e70c3/lib/lean/PkgGramDeterminant.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211135_dc5e70c3/lib/lean/PkgGramIdentity.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211135_dc5e70c3/lib/lean/PkgGramPlucker.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211135_dc5e70c3

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211135_dc5e70c3/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211321_7e5d765a

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211321_7e5d765a/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211321_7e5d765a/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211321_7e5d765a/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211321_7e5d765a

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211321_7e5d765a/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211348_843ce1b4

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211348_843ce1b4/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211348_843ce1b4/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211348_843ce1b4/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211348_843ce1b4/lib/lean/PkgGramCalculus.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211348_843ce1b4/lib/lean/PkgGramDeterminant.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211348_843ce1b4/lib/lean/PkgGramHirota.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211348_843ce1b4/lib/lean/PkgGramIdentity.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211348_843ce1b4/lib/lean/PkgGramPlucker.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211348_843ce1b4

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211348_843ce1b4/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211502_24388216

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211502_24388216/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211502_24388216/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211502_24388216/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211502_24388216

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211502_24388216/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211632_95de476e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211632_95de476e/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211632_95de476e/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211632_95de476e/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211632_95de476e/lib/lean/PkgGramActual.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211632_95de476e/lib/lean/PkgGramCalculus.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211632_95de476e/lib/lean/PkgGramDeterminant.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211632_95de476e/lib/lean/PkgGramHirota.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211632_95de476e/lib/lean/PkgGramIdentity.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211632_95de476e/lib/lean/PkgGramPlucker.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211632_95de476e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211632_95de476e/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211901_117b2571

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211901_117b2571/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211901_117b2571/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211901_117b2571/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211901_117b2571/lib/lean/PkgC07Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211901_117b2571/lib/lean/PkgGramActual.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211901_117b2571/lib/lean/PkgGramCalculus.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211901_117b2571/lib/lean/PkgGramDeterminant.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211901_117b2571/lib/lean/PkgGramHirota.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211901_117b2571/lib/lean/PkgGramIdentity.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211901_117b2571/lib/lean/PkgGramPlucker.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_211901_117b2571

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_211901_117b2571/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_212151_f7e05e3c

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212151_f7e05e3c/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_212151_f7e05e3c/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212151_f7e05e3c/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212151_f7e05e3c/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212151_f7e05e3c/lib/lean/PkgC07Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212151_f7e05e3c/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212151_f7e05e3c/lib/lean/PkgGramActual.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212151_f7e05e3c/lib/lean/PkgGramCalculus.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212151_f7e05e3c/lib/lean/PkgGramDeterminant.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212151_f7e05e3c/lib/lean/PkgGramHirota.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212151_f7e05e3c/lib/lean/PkgGramIdentity.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212151_f7e05e3c/lib/lean/PkgGramPlucker.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_212151_f7e05e3c

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212151_f7e05e3c/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/Main.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgC07Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgC17.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgC18Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgContinuous.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgGramActual.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgGramBridges.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgGramCalculus.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgGramComplete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgGramDeterminant.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgGramEntry.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgGramHirota.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgGramIdentity.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgGramPlucker.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgNonlinear.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgQuotientRate.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgRK4.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgRK4Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/lib/lean/PkgTrivial.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212234_3a4b6e8e/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_212719_366d09ab

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212719_366d09ab/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_212719_366d09ab/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212719_366d09ab/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212719_366d09ab/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212719_366d09ab/lib/lean/PkgC07Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212719_366d09ab/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212719_366d09ab/lib/lean/PkgGramActual.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212719_366d09ab/lib/lean/PkgGramCalculus.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212719_366d09ab/lib/lean/PkgGramDeterminant.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212719_366d09ab/lib/lean/PkgGramHirota.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212719_366d09ab/lib/lean/PkgGramIdentity.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212719_366d09ab/lib/lean/PkgGramPlucker.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_212719_366d09ab

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_212719_366d09ab/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507/lib/lean/PkgC07Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507/lib/lean/PkgContinuousGram.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507/lib/lean/PkgGramActual.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507/lib/lean/PkgGramCalculus.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507/lib/lean/PkgGramDeterminant.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507/lib/lean/PkgGramHirota.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507/lib/lean/PkgGramIdentity.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507/lib/lean/PkgGramPlucker.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213212_56205507/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213550_95f11b63

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213550_95f11b63/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213550_95f11b63/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213550_95f11b63/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213550_95f11b63

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213550_95f11b63/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213644_a950d35c

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213644_a950d35c/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213644_a950d35c/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213644_a950d35c/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213644_a950d35c

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213644_a950d35c/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992/lib/lean/PkgC07Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992/lib/lean/PkgContinuousGram.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992/lib/lean/PkgGramActual.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992/lib/lean/PkgGramCalculus.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992/lib/lean/PkgGramDeterminant.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992/lib/lean/PkgGramHirota.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992/lib/lean/PkgGramIdentity.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992/lib/lean/PkgGramPlucker.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213855_8df21992/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213906_a9cec1ac

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213906_a9cec1ac/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213906_a9cec1ac/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213906_a9cec1ac/lib/lean/Contracts.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213906_a9cec1ac

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213906_a9cec1ac/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213917_ddc5a302

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213917_ddc5a302/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213917_ddc5a302/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213917_ddc5a302/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213917_ddc5a302/lib/lean/PkgUniformTaylor.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_213917_ddc5a302

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_213917_ddc5a302/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214127_0ac4cb2a

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214127_0ac4cb2a/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214127_0ac4cb2a/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214127_0ac4cb2a/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214127_0ac4cb2a/lib/lean/PkgGramRateExtension.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214127_0ac4cb2a

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214127_0ac4cb2a/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214238_b5add276

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214238_b5add276/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214238_b5add276/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214238_b5add276/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214238_b5add276/lib/lean/PkgUniformTaylor.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214238_b5add276

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214238_b5add276/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b/lib/lean/PkgC07Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b/lib/lean/PkgContinuousGram.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b/lib/lean/PkgContinuousGramCurve.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b/lib/lean/PkgGramActual.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b/lib/lean/PkgGramCalculus.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b/lib/lean/PkgGramDeterminant.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b/lib/lean/PkgGramHirota.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b/lib/lean/PkgGramIdentity.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b/lib/lean/PkgGramPlucker.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214428_07a2a97b/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214439_108d7d8d

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214439_108d7d8d/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214439_108d7d8d/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214439_108d7d8d/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214439_108d7d8d/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214439_108d7d8d/lib/lean/PkgGramRateExtension.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214439_108d7d8d

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214439_108d7d8d/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214735_5b619619

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214735_5b619619/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214735_5b619619/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214735_5b619619/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214735_5b619619/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214735_5b619619/lib/lean/PkgGramInterpolation.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214735_5b619619/lib/lean/PkgGramRateExtension.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214735_5b619619

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214735_5b619619/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214903_81be8e7d

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214903_81be8e7d/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214903_81be8e7d/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214903_81be8e7d/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214903_81be8e7d/lib/lean/PkgUniformTaylor.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_214903_81be8e7d

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_214903_81be8e7d/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/lib/lean/PkgC07Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/lib/lean/PkgC23Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/lib/lean/PkgContinuousGram.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/lib/lean/PkgContinuousGramCurve.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/lib/lean/PkgGramActual.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/lib/lean/PkgGramCalculus.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/lib/lean/PkgGramDeterminant.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/lib/lean/PkgGramHirota.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/lib/lean/PkgGramIdentity.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/lib/lean/PkgGramPlucker.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215358_2874410b/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215409_f79bead4

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215409_f79bead4/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215409_f79bead4/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215409_f79bead4/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215409_f79bead4/lib/lean/PkgUniformTaylor.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215409_f79bead4

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215409_f79bead4/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215419_a4555a05

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215419_a4555a05/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215419_a4555a05/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215419_a4555a05/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215419_a4555a05/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215419_a4555a05/lib/lean/PkgGramInterpolation.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215419_a4555a05/lib/lean/PkgGramRateExtension.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215419_a4555a05

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215419_a4555a05/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215547_c088d7fb

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215547_c088d7fb/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215547_c088d7fb/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215547_c088d7fb/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215547_c088d7fb/lib/lean/PkgUniformAnalytic.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215547_c088d7fb/lib/lean/PkgUniformTaylor.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215547_c088d7fb

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215547_c088d7fb/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215636_085e526a

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215636_085e526a/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215636_085e526a/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215636_085e526a/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215636_085e526a/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215636_085e526a/lib/lean/PkgGramInterpolation.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215636_085e526a/lib/lean/PkgGramInterpolationBridge.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215636_085e526a/lib/lean/PkgGramRateExtension.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215636_085e526a

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215636_085e526a/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215815_c873a9f4

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215815_c873a9f4/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215815_c873a9f4/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215815_c873a9f4/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215815_c873a9f4/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215815_c873a9f4/lib/lean/PkgGramExtensionBridge.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215815_c873a9f4/lib/lean/PkgGramInterpolation.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215815_c873a9f4/lib/lean/PkgGramInterpolationBridge.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215815_c873a9f4/lib/lean/PkgGramRateExtension.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215815_c873a9f4

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215815_c873a9f4/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/Main.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgC07Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgC17.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgC18Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgC23Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgContinuous.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgContinuousGram.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgContinuousGramCurve.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgGramActual.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgGramBridges.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgGramCalculus.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgGramComplete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgGramDeterminant.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgGramEntry.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgGramHirota.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgGramIdentity.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgGramPlucker.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgNonlinear.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgQuotientRate.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgRK4.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgRK4Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/lib/lean/PkgTrivial.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_215953_3da9b828/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220055_89231145

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220055_89231145/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220055_89231145/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220055_89231145/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220055_89231145/lib/lean/PkgUniformAnalytic.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220055_89231145/lib/lean/PkgUniformTaylor.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220055_89231145

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220055_89231145/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220238_e72e4383

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220238_e72e4383/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220238_e72e4383/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220238_e72e4383/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220238_e72e4383/lib/lean/PkgAnalyticJets.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220238_e72e4383/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220238_e72e4383/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220238_e72e4383/lib/lean/PkgGramExtensionBridge.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220238_e72e4383/lib/lean/PkgGramInterpolation.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220238_e72e4383/lib/lean/PkgGramInterpolationBridge.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220238_e72e4383/lib/lean/PkgGramRateExtension.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220238_e72e4383/lib/lean/PkgUniformAnalytic.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220238_e72e4383/lib/lean/PkgUniformTaylor.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220238_e72e4383

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220238_e72e4383/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220512_8dd63baa

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220512_8dd63baa/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220512_8dd63baa/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220512_8dd63baa/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220512_8dd63baa/lib/lean/PkgAnalyticJets.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220512_8dd63baa/lib/lean/PkgUniformAnalytic.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220512_8dd63baa/lib/lean/PkgUniformTaylor.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220512_8dd63baa

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220512_8dd63baa/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220639_37d9d497

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220639_37d9d497/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220639_37d9d497/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220639_37d9d497/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220639_37d9d497/lib/lean/PkgAnalyticJets.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220639_37d9d497/lib/lean/PkgUniformAnalytic.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220639_37d9d497/lib/lean/PkgUniformTaylor.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220639_37d9d497

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220639_37d9d497/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da/lib/lean/PkgAnalyticJets.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da/lib/lean/PkgGramExtensionAnalytic.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da/lib/lean/PkgGramExtensionBridge.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da/lib/lean/PkgGramInterpolation.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da/lib/lean/PkgGramInterpolationBridge.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da/lib/lean/PkgGramRateExtension.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da/lib/lean/PkgUniformAnalytic.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da/lib/lean/PkgUniformTaylor.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220812_d455b7da/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220859_0a093404

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220859_0a093404/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220859_0a093404/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220859_0a093404/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220859_0a093404/lib/lean/PkgAnalyticJets.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220859_0a093404/lib/lean/PkgCenteredFamily.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220859_0a093404/lib/lean/PkgUniformAnalytic.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220859_0a093404/lib/lean/PkgUniformTaylor.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_220859_0a093404

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_220859_0a093404/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/lib/lean/PkgAnalyticJets.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/lib/lean/PkgCenteredFamily.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/lib/lean/PkgCenteredUniform.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/lib/lean/PkgGramExtensionAnalytic.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/lib/lean/PkgGramExtensionBridge.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/lib/lean/PkgGramInterpolation.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/lib/lean/PkgGramInterpolationBridge.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/lib/lean/PkgGramRateExtension.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/lib/lean/PkgUniformAnalytic.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/lib/lean/PkgUniformTaylor.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221046_8ba9d4ef/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_221147_0c717d1e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221147_0c717d1e/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_221147_0c717d1e/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221147_0c717d1e/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221147_0c717d1e/lib/lean/PkgAnalyticJets.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221147_0c717d1e/lib/lean/PkgCenteredFamily.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221147_0c717d1e/lib/lean/PkgCenteredUniform.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221147_0c717d1e/lib/lean/PkgUniformAnalytic.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221147_0c717d1e/lib/lean/PkgUniformTaylor.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_221147_0c717d1e

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221147_0c717d1e/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/lib/lean/PkgAnalyticJets.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/lib/lean/PkgC22Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/lib/lean/PkgCenteredFamily.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/lib/lean/PkgCenteredUniform.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/lib/lean/PkgGramExtensionAnalytic.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/lib/lean/PkgGramExtensionBridge.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/lib/lean/PkgGramInterpolation.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/lib/lean/PkgGramInterpolationBridge.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/lib/lean/PkgGramRateExtension.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/lib/lean/PkgUniformAnalytic.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/lib/lean/PkgUniformTaylor.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221556_6742b525/result.json`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/build.log`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/Contracts.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/Main.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgAnalyticJets.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgC02.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgC07Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgC09Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgC11.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgC17.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgC18Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgC22Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgC23Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgCenteredFamily.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgCenteredUniform.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgContinuous.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgContinuousGram.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgContinuousGramCurve.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgGramActual.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgGramBridges.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgGramCalculus.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgGramComplete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgGramDeterminant.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgGramEntry.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgGramExtensionAnalytic.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgGramExtensionBridge.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgGramHirota.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgGramIdentity.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgGramInterpolation.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgGramInterpolationBridge.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgGramPlucker.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgGramRateExtension.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgLattice.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgNonlinear.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgNumeric.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgQuotientRate.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgRK4.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgRK4Complete.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgTrivial.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgUniformAnalytic.olean`
- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/lib/lean/PkgUniformTaylor.olean`

## Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/result.json`

## Workspaces/lean_contracts/proofs

- `Workspaces/lean_contracts/proofs/AGENT_BRIEF.md`
- `Workspaces/lean_contracts/proofs/Contracts.lean`
- `Workspaces/lean_contracts/proofs/Main.lean`
- `Workspaces/lean_contracts/proofs/PkgAnalyticJets.lean`
- `Workspaces/lean_contracts/proofs/PkgC02.lean`
- `Workspaces/lean_contracts/proofs/PkgC07Complete.lean`
- `Workspaces/lean_contracts/proofs/PkgC09.lean`
- `Workspaces/lean_contracts/proofs/PkgC09Complete.lean`
- `Workspaces/lean_contracts/proofs/PkgC11.lean`
- `Workspaces/lean_contracts/proofs/PkgC17.lean`
- `Workspaces/lean_contracts/proofs/PkgC18Complete.lean`
- `Workspaces/lean_contracts/proofs/PkgC22Complete.lean`
- `Workspaces/lean_contracts/proofs/PkgC23Complete.lean`
- `Workspaces/lean_contracts/proofs/PkgCenteredFamily.lean`
- `Workspaces/lean_contracts/proofs/PkgCenteredUniform.lean`
- `Workspaces/lean_contracts/proofs/PkgContinuous.lean`
- `Workspaces/lean_contracts/proofs/PkgContinuousGram.lean`
- `Workspaces/lean_contracts/proofs/PkgContinuousGramCurve.lean`
- `Workspaces/lean_contracts/proofs/PkgGramActual.lean`
- `Workspaces/lean_contracts/proofs/PkgGramBridges.lean`
- `Workspaces/lean_contracts/proofs/PkgGramCalculus.lean`
- `Workspaces/lean_contracts/proofs/PkgGramComplete.lean`
- `Workspaces/lean_contracts/proofs/PkgGramDeterminant.lean`
- `Workspaces/lean_contracts/proofs/PkgGramEntry.lean`
- `Workspaces/lean_contracts/proofs/PkgGramExtensionAnalytic.lean`
- `Workspaces/lean_contracts/proofs/PkgGramExtensionBridge.lean`
- `Workspaces/lean_contracts/proofs/PkgGramHirota.lean`
- `Workspaces/lean_contracts/proofs/PkgGramIdentity.lean`
- `Workspaces/lean_contracts/proofs/PkgGramInterpolation.lean`
- `Workspaces/lean_contracts/proofs/PkgGramInterpolationBridge.lean`
- `Workspaces/lean_contracts/proofs/PkgGramPlucker.lean`
- `Workspaces/lean_contracts/proofs/PkgGramRateExtension.lean`
- `Workspaces/lean_contracts/proofs/PkgLattice.lean`
- `Workspaces/lean_contracts/proofs/PkgNonlinear.lean`
- `Workspaces/lean_contracts/proofs/PkgNumeric.lean`
- `Workspaces/lean_contracts/proofs/PkgQuotientRate.lean`
- `Workspaces/lean_contracts/proofs/PkgRK4.lean`
- `Workspaces/lean_contracts/proofs/PkgRK4Complete.lean`
- `Workspaces/lean_contracts/proofs/PkgTrivial.lean`
- `Workspaces/lean_contracts/proofs/PkgUniformAnalytic.lean`
- `Workspaces/lean_contracts/proofs/PkgUniformTaylor.lean`
- `Workspaces/lean_contracts/proofs/ProbeC09.lean`

## Workspaces/lean_contracts

- `Workspaces/lean_contracts/sync_verified_index.py`
- `Workspaces/lean_contracts/update_progress_docs.py`
- `Workspaces/lean_contracts/validate_dashboard.py`

## Workspaces/numerics_fix_20260922

- `Workspaces/numerics_fix_20260922/check_leading_term.py`
- `Workspaces/numerics_fix_20260922/check_model_offset_scaling.py`
- `Workspaces/numerics_fix_20260922/check_phase_fix.py`
- `Workspaces/numerics_fix_20260922/decide_phase.py`
- `Workspaces/numerics_fix_20260922/probe_e7_offset.py`
- `Workspaces/numerics_fix_20260922/verify_review_claims.py`

## Workspaces/numerics_review_20260922

- `Workspaces/numerics_review_20260922/finalize_docs.py`
- `Workspaces/numerics_review_20260922/finalize_self_convergence.py`
- `Workspaces/numerics_review_20260922/implement_fixes.py`
- `Workspaces/numerics_review_20260922/probe_results.json`
- `Workspaces/numerics_review_20260922/recheck_results.json`
- `Workspaces/numerics_review_20260922/RECHECK.md`
- `Workspaces/numerics_review_20260922/recheck.py`
- `Workspaces/numerics_review_20260922/REPORT_before_final_fixes.md`
- `Workspaces/numerics_review_20260922/RESOLUTION.md`
- `Workspaces/numerics_review_20260922/review_probes.py`
- `Workspaces/numerics_review_20260922/REVIEW.md`
- `Workspaces/numerics_review_20260922/upgrade_regressions.py`
- `Workspaces/numerics_review_20260922/validate_final.py`
