# DLW 数值实验

当前结果、证据范围与复现命令见 [REPORT.md](REPORT.md)。2026-09-22 四项复审修复已落地：开链线性化和本征模检查、当前源码行为回归、E1 有限区间求积、E5 指定格点与初态周期积分。

```powershell
python -u run_all.py e1 e6 e2e3 e2e3time e5 e7
python -u experiments/check_regressions.py
python -u make_figures.py
```

完整实验可用 `python -u run_all.py`。原始结果在 `out/`；最终修复日志为 `final_four_fixes_log.txt`、`final_e6_log.txt`、`final_regressions_log.txt`。代码和产物哈希见 `out/final_validation_manifest.json`。

E6 的零背景开链线性谱是数值估计，模态时间不是非线性稳定硬界。E4 仍主要检查解析族；E2/E3 已新增六组同网格时间自收敛，分别支持 Euler/RK4/梯形的 1/4/2 阶行为（详见报告中的实际数值）；数据与源码哈希在 `out/e2_e3_self_convergence.json`。数值证据不等于 Lean 证明。
