# DLW：实际半离散求解路线的误差机制

论文章节：[从解析式看误差为什么抵消](../../dlw_error_composition.html)。2026-10-14按用户要求以 Humanizer 改写，成稿位于工作区主目录。权威正文为 `composition.paper.source.html`，由 `build_composition.py` 生成。正文包含连续积分式、离散累加、AFD/APE 的系数推导、共同 x 主项、四行原数值表及有限时间误差的衔接；23个编号公式。此前讲解版仍保留，修改前快照在 `before_paper_style_20261014/`。

完整实验报告：[可积半离散如何影响实际误差？](../../report/dlw_error_mechanism_20261013.html)

聚焦推导：[从解析式看误差为什么抵消](../../report/dlw_error_composition_20261013.html)。按用户后续要求，以同一 u 场推导精确梯形重构源及领先式 r=h²A+dx²B+wrap+O(h⁴+h²dx²+dx⁴)，明确 PE 的两项 y 系数修正与共同 x 系数。A/C 原参数代入使用最高五阶 log-tau 累积量，无末态拟合；领先源与完整源场相对差分别为 A 1.84%–2.12%、C 0.119%–0.131%，四种叠加/抵消方向一致。解析式、独立审查及数据均在 `sources/LEADING_U_FORMULAS.md` 和 `leading_u_*`。该新增结果是初始瞬时源的领先阶验证，不是新长期误差定理，也未新做余项阶数加密扫描。

本项目研究原论文 PE（代码中记为 SD）与 FD 在 A/C 孤子算例中的实际误差。连续 Gram 解、初值、原缓冲域、原观察窗、物理边界与二阶 x 模板保持原口径。主问题是误差如何注入、组成、传播和演化，而不是仅比较末态误差范数。

## 证据链

1. `sources/`：在精确参考上独立计算右端残差，分为 y 模型及边界闭合、x 差分、x 周期卷绕三源；解析导数、独立源核验、分方向加密、有符号能量预算。
2. `transport/`：实际 RK4 一步缺陷与解析切映射，四格交换源与传播器，完整物理场预测，三源分别传播，半幅缺陷扣除的非线性干预，A 延长至 T=.04 与时间步复核。
3. `morphology/`：A 一个、C 两个共同 Gram 相位，双场联合拟合与线性正交分解；原窗和中央子窗、全时间序列、半时间步检查。
4. `boundary/`：A 的 y 缓冲半宽由10扩为20、观察窗不变，检测误差场的 y 常数条带分量。
5. `intervention/`：在共同 (p,v) 状态上混合完整 PE/FD 一步更新，五个预定比例，A 中点时间步复核；C 两端复用已经核验的原轨道，其余为新演化。
6. `refinement/`：源诊断之后、演化之前固定方向预测；C 保持 h=.1，减小 dx=.1→.025，在同一 T=.001 比较并复核细网格 PE 半时间步。两方法绝对误差都减小，但 PE/FD 的 u 比值 .8212→2.6956，v 比值 .99966→1.5474。

各目录 `FINDINGS.md`、协议、CSV/JSON 与原生数组保存定义、结论和适用范围。根 `PROTOCOL.md` 是初始研究协议；`refinement_prediction.md` 是诊断后的预测实验。协议修订及缓存验证保存在 `transport/`，不能把后续修订称为原始预注册条件。

## 指标与解释

所有比较使用同一连续参考和实际原生物理格点。主联合范数为 sqrt(RMS(u_error)^2 + RMS(v_error)^2)，两场等权；同时保存各场 RMS 与 Linf。相位百分比指平方误差的解释率，不是 RMS 的下降率。误差源是带符号的场，各项范数不能直接相加。

短窗的 PE/FD 差距主要来自注入源及其有符号抵消。四格交换条件于经过完整场核验的线性误差模型；这不是单独切换抽象可积性的实验。y_model 包含实际 y 边界闭合。原 x 差分是二阶中心 D1 和独立三点 D2，不是 D1 的平方，也不是旧报告使用过的四阶模板。

扩 y 缓冲同时移动上下边界；初始源恒等式定位下边界积分重构，完整演化不被解释为单独下边界干预。相位外残差没有被认定为新增孤子。长窗 T=.04 只是当前实验的延长时间，不能视为一般长期稳定性结论。

## 复现入口

冻结求解器：`../dlw_three_tracks_20261013/shared/solver_cells.json`，由 `../dlw_three_tracks_20261013/generate_shared.py:load_solver()` 只读导入。原始共享轨迹和末态仍在该项目 `shared/`。本项目未改动原论文或求解器。

主要脚本：

- `sources/run_sources.py`、`sources/verify_sources.py`、`sources/summarize_sources.py`：源预算。
- `transport/run_transport.py --help`：传播与干预，命令参数和具体运行版本见该目录协议。
- `morphology/phase_decomposition.py`：相位预算。
- `boundary/`：固定窗口边界对照，具体入口见 `boundary/FINDINGS.md`。
- `homotopy.py --help`：更新混合。
- `refinement_test.py --help`、`check_refinement.py`：预报后的网格对照。
- `make_figures.py`：仅从已完成数据生成五张总览图；场图由 `figures/` 内脚本生成。
- `build_report.py`：从真实 CSV/JSON 填表，严格离线 KaTeX 渲染并检查链接。

运行环境使用现有 Python 的 NumPy、SciPy、pandas、Matplotlib、BeautifulSoup 与现有 Node/KaTeX；本阶段没有新增依赖。实验需要较多内存，C 的完整传播优先阅读已经保存的结果。未完成或中断运行保留；只有带完整验证记录的目录进入报告。

## 绘图与核验

版式参照绘图库的 `oa-tech-pone-0116670-f16`（对齐比较曲线）与 `oa-geo-bg-21-811-2024-f02`（显式色标比较面板）。保持项目 PE 蓝、FD 绿的语义；所有图来自保存的实验数据，输出 PNG 300 dpi 与 PDF。

`validation.json` 记录报告数学、表格、图片和本地链接检查。各研究分支保存数值核验及独立交叉审阅；最终交付检查见 `FINAL_REVIEW.md`。
