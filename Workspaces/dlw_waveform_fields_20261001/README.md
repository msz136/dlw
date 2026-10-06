# DLW Euler 局部误差分布

当前交付：根目录 index.html 第6节与 dlw_waveform_fields.html。按用户修订要求，撤下波形/剖面和RK4图，仅显示Euler在T=0.01、物理x∈[-1,1]的绝对误差。

3算例（A/B单孤子、C二孤子）×3空间方案（SD/SD2/FD）×2网格（fixed/moving）×2场（u/v），共36张单图。每张只有一个误差分布面板和一根色条。按算例、网格、物理场折叠，三个方案逐张纵向显示。

读取18份原Euler主轨道；按原CubicSpline重构口径在原4001点中选含±1的401点，保留24个y中点层。色条采用gamma=0.5平方根映射，刻度为绝对误差，同case/field跨三方案与两网格统一上限。十字与window max均是当前窗口内峰值；原表的[-10,10]误差指标不改。误差含初始表示误差，A/SD2/fixed保留†。

## 当前文件与复现

- revision_euler_crop/plot_euler_errors.py：36张单面板PNG/PDF、euler_plot_validation.json、euler_cropped_errors.csv、euler_cropped_errors.npz。
- revision_euler_crop/build_euler_reports.py：生成两根HTML，原5表与16公式保留；旧build_reports.py入口已转发此脚本。
- revision_euler_crop/euler_crop_audit.py、euler_crop_audit.json：独立有理tau参照、18源哈希及36局部误差/峰位/色标复核。
- check_euler_report.cjs、euler_html_validation.json、euler_preview/：两页36单图，桌面/390px图片、公式、折叠、链接与溢出核验。
- revision_euler_crop/before/：修订前两页、正文/模板/构建器与说明副本。

运行 python revision_euler_crop/plot_euler_errors.py，再运行 python build_reports.py。旧plot_fields.py仅供上一版重现与当前参照接口，正常交付不再调用它的main。旧图、旧图数据与核验文件保留在原目录；本次没有新PDE演化。
