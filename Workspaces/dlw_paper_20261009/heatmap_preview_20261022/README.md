# DLW 二维图试绘（2026-10-22）
入口：../../../report/dlw_heatmap_preview_20261022.html。
沿用参考 PDF 第14–15页截面/热图布局，未修改论文正文和原图。
四组连续解析 t=0 场来自 ../plot_exact_solutions.py；A 的 PE/PF/FD 固定网格 RK4 重新调用现有 Notebook 求解器。源 Notebook 摘要、参数与误差记录见 validation.json；数组 A_PE/PF/FD.npz。
y=0 不在原始数值网格上：三次样条重构数值场，再减直接求值的连续解析基准，不能称作原生零截面。解析场重构控制误差 u=1.23e-7、v=5.10e-8。
plot_preview.py 重现 PNG/SVG（已有数组时复用）。本轮仅试绘；B/C/D 数值误差及多时刻截面尚未新增。下一步按用户选择将图补入稿件；旧 max-y 曲线保留其定义。
