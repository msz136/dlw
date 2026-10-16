# 直接差分与 LDG 对照

用户入口：[对照结果](../../../report/mch_ldg_fd_comparison_20261015.html)。

本支线实现原始mCH的FD2/FD4及局部Rusanov耗散差分，复用现有LDG算法。协议见 `PROTOCOL.md`；所有配置在运行前保存，所有输出按时间戳保留，失败与不同终点分列。

```powershell
python verify_fd.py
python run_suite.py --mode peak
python run_suite.py --mode smooth
python run_suite.py --mode controls
python run_suite.py --mode ldg
python run_suite.py --mode rusanov
python run_suite.py --mode offset
python run_extra_controls.py
python analyze_comparison.py
python plot_comparison.py
python build_report.py
python audit.py
```

`analysis/physical_errors.csv` 保存每条轨迹的初态、共同t=.5及已完成终态的物理u误差。共同L²使用10240子区间×4点Gauss积分，采样L∞用80000等距点并补精确峰位；LDG另补单元边界双侧点。高自由度终态再次加密评价规则。FD用周期三次样条重构；原生节点误差另保留在各运行history.json中。评价和初始表示的选择不等于演化格式。

首轮52条比较轨迹含2条既有LDG复用，42条到目标终点；另有2条FD冒烟测试。10条未完成为尖顶对齐节点的中心差分及其半步长控制。半格FD、Rusanov与本轮LDG均完成。首轮共125组物理场评价。具体结论见HTML，光滑和尖峰的排名不同。

新增绘图沿用科研绘图库 `oa-tech-pone-0116670-f16` 的对齐多曲线面板结构，保持既有LDG颜色；源码和PNG/PDF均在本目录，不收进图库。

## 三阶直接差分

[三阶对照报告](../../../report/mch_ldg_fd3_comparison_20261015.html)。新增 `fd3.py`：三阶迎风LF通量分裂、四阶辅助导数，整体空间三阶；具体模板见 `PROTOCOL_THIRD.md`。16条新增轨迹全部到终点，联合比较清单现有68条、167组共同物理场评价。原FD2/FD4结果和运行源码保留。

```powershell
python verify_third.py
python run_third.py --mode smooth
python run_third.py --mode peak
python run_third.py --mode controls
python analyze_comparison.py
python report_third.py
python audit.py
```

`analysis/third_summary.json` 保存三阶光滑观测阶、同自由度表和时间步控制。两个报告对应不同阶段；总CSV包含已完成的所有比较。
