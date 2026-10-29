# 当前工作与最近交接

## 本次工作｜DLW Miwa 与统一 Gram 叙述重组（2026-10-29，完成）

已同步主HTML与TeX。第2.2节按τ三项→F/G平移→共同中点与Hirota指数→逐阶抵消展开Miwa推导，再给出自由参数b下的统一半离散格点与Gram解。恢复旧稿相邻层lemma及完整秩一更新、行列式比值微分消元proof，替换最新的全离散Gram系数提取证明；辅助层方向及一般常数矩阵C的奇异延拓已对齐。第2.3节分别代入Endpoint-SD与Centered-SD参数，纳入显式解、一致性及正性；原2.4合并。全文式号(1)–(133)、正文附录引用和HTML目录同步。两稿共同公式一致，符号核验通过；2.2–2.3本地替代字体双遍编译6页并目视检查，整篇PDF未重编译。下一步可按新结构审阅并在原字体环境重编译PDF。入口：`dlw-paper.html`；`pdf/dlw/main.tex`；`Workspaces/dlw_paper_20261009/miwa_stepwise_20261029/README.md`。

## 上一次工作｜2HS 能量型密度与选取叙述（2026-10-28，完成）

LaTeX Section5改用rho、Rm、RE，重述原PDE，解释幂次平衡与二次候选系数抵消；区别守恒律推导和网格背景归一化。按用户最新要求移除R2及拟议附录D，旧推导数据保留。补算两例RE与步长减半共4组；图9/10、表7/8及附录C三表、摘要引言结论同步，原误差诊断叙述也纠正为仅Rm改善单波初始恢复。RE单波rho比值.508，双波.753；Rm较均衡，最大步长减半差3.137e-13。PDF24页、10图、8+3表已同步桌面；矢量拆面板避免留白。主HTML与DLW未动。下一步审阅密度选取（PDF14–16页）。入口：`pdf/2hs/main.tex`；`Workspaces/hs_paper_20261026/samm_energy_20261028/README.md`；同目录`validation.json`。

本轮文字收尾（2026-10-28）：按用户逐项确认，仅替换 DLW 与 2HS 摘要末句，并删除 2HS Section 4.4 两个算例各自重复的共同设置。保留小目录、章节总结、图表导读及所有公式、数据、图注。TeX 内容核对通过；拉取后已重编译两篇 PDF，DLW 39 页、2HS 24 页，第二遍无未定义引用警告；HTML 保持原样。入口：`pdf/dlw/main.tex`、`pdf/2hs/main.tex`。

局部措辞续修（2026-10-29）：DLW的HTML与TeX同步Section2标题为Integrable semi-discrete formulations and exact solutions；Sheng–Yu引用句改为“In the work of Sheng and Yu [5], we have…”引出上下文。HTML目录同步，公式数据未动。随后XeLaTeX双遍编译完成，39页，无未定义引用/缺字/越界警告，第3页目视通过，已更新pdf/dlw/main.pdf。备份：`Workspaces/dlw_paper_20261009/wording_revision_20261029/`。
