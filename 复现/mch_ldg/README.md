# mCH LDG 复现

目标论文：Chang–Liu–Tao, arXiv:2608.28077v2。
本目录按用户要求建于工作区主目录 `复现/` 下。

源文献沿用 `../../Paper/refs/2608_28077/2608.28077v2.pdf`。
所有首轮参数、原始输出与核验均留在本目录；未明确的作者参数不作猜测性归属。

## 架构

- `mch/ldg.py`：Legendre 模态 LDG、精确多项式积分、两套通量、离散 Helmholtz 求解。
- `mch/exact.py`：例5.1–5.5的解析场、导数及参数坐标反解。
- `mch/boundary.py`：实验性的固定 Dirichlet 闭合；非零背景存在失败结果，尚不作为可靠方案。
- `mch/experiment.py`：RK4、初始化、逐时刻能量/质量/误差及原始轨迹。
- `verify.py`：独立代数恒等式、投影、椭圆求解和解析解核验。
- `run.py`：JSON 配置运行入口；`suite.py`：首轮实验矩阵。
- `controls.py`、`alignment.py`：扩域、时间步、初值与边界控制；`paper_cases.json`：原文完整实验参数清单。
- `analyze.py`、`figures/plot_results.py`、`build_report.py`：仅读取保存数据，生成汇总、图和报告。
- `configs/`：可重跑参数；`results/`：带时间戳且不覆盖的结果。
- `figures/`：保存数据生成的图；`search/`：首轮完成后的参数检索证据。

实现采用 u 为时间状态，实际求解 `(I-Dplus Dminus) u_t = m_t`，与固定边界下推进 m 代数等价。每个RK阶段计算 r,p,s。

运行：在本目录执行 `python verify.py`、`python suite.py`。
依赖：Python、NumPy、SciPy；绘图另需已有 Matplotlib。

初版以周期闭合建立严格的半离散能量验证。例5.5原生周期；例5.1–5.4首轮周期截断明确标注为边界近似，不能称完全对齐原文 compact-support/background 边界。

首轮结果见 [HTML报告](../../report/mch_ldg_reproduction_20261015.html)。已保存67次运行，64次到达终点；3次失败均为非零背景Dirichlet试验。全部原始记录见 `results/all_runs.csv`，失败运行的停止时刻与最后诊断时刻分别记录，不混入共同终点比较。

```powershell
python verify.py
python check_reference.py
python suite.py --mode smoke
python suite.py --mode smooth
python suite.py --mode peakon
python suite.py --mode other
python suite.py --mode timecheck
python controls.py --mode domain
python controls.py --mode rk4
python analyze.py
python figures/plot_results.py
python build_report.py
python audit.py
```

单项配置重跑：`python run.py configs/peakon_00.json`。每次新建时间戳目录；分析脚本默认读取对应实验清单中的最新一批，因此重跑后应保留完整批次再生成报告。

`versions/v1_periodic/` 保存首轮原始代码；后续结果目录另存运行开始时的求解器源码。历史记录与新闭合分开，不覆盖。图3范数差与平方能量差的疑点和作者参数检索见 `search/FINDINGS.md`。

## 直接差分对照

已新增 [FD2／FD4／Rusanov 与 LDG 对照](../../report/mch_ldg_fd_comparison_20261015.html)，代码、协议与数据见 [fd_comparison/README.md](fd_comparison/README.md)。光滑与尖峰分别比较，按演化自由度及格距区分；失败结果和半格偏移控制全部保留。
