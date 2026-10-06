# GSG、2HS、DLW原文：文献类型与方法主线

2026-10-02，只读原文调研，不运行新实验，不改原论文。

## GSG

Feng/Sheng/Yu，Numerical Algorithms 94 (2023), 351–370，DOI 10.1007/s11075-023-01504-1。首页ORIGINAL PAPER；不是书。

核心：r²=1+ux²的守恒律 → 以守恒质量定义计算坐标 → sG的Bäcklund/2DTL双线性结构 → 保持结构的空间半离散 → 离散倒数变换 → 场与网格耦合的SAMM算法。光滑正分支xy=1/r，坡度高时物理间距小；参数曲线表示还用于折返/多值孤子。

构造两套可积、一套非可积半离散方程；数值部分四个SAMM方案和一个C–N比较方案，单孤子三种形态。可积标签主要针对空间半离散；文中时间Euler步进不等于已经证明完全离散可积性。非可积3/4在部分kink算例更好，loop中scheme1更好；无一般误差界/网格一致稳定证明。出处：gsg.txt行1–13、110–161、355–435、496–712、718–899。

## 2HS

工作区PDF为Hori/Tanaka/Maruno/Ohta，arXiv:2606.18701v2，2026-09-02。题名An integrable semi-discretization of the two-component Hunter–Saxton equation。本文件为预印本，不能凭PDF版式宣称正式期刊发表。

核心：为保留u、rho两场，换用新的两tau双线性表达（相对于已有三tau表达） → 在这一结构上空间离散 → pseudo 2-reduction → 离散倒数变换 → 物理两场半离散系统。连续Wronskian、离散Casoratian孤子解和Lax对支持可积结构。

rho_t=(rho u)_x，dX=rho dx+rho u dt；计算步长a与物理间距δk=a/rhok联系。网格xk,T=−uk、δk,T=uk−1−uk；rho既是物理分量又决定网格。自然密度并非任意选择的误差最优监测函数。主要是结构构造，不是类似GSG的多算法误差比较。依据PDF第1、4、12–16、18–21页；完整相关页及公式已读取并渲染核对。

## DLW原文

Sheng/Yu，Physica D 432 (2022), 133140，DOI 10.1016/j.physd.2021.133140。

核心：DLW → u=2(log(f/g))x、v=2(log(fg))xy → Hirota双线性方程 → 修改KP层级的Gram行列式tau函数与约化 → 指数元素得到孤子、谱参数微分得到有理/代数类型 → 分析传播碰撞与渐近行为。

实际主体为Gram构造；Wronskian只在回顾前人文献时提到。图中展示解析解，不构成自适应时间推进/误差阶证明。原文没有给目前项目的SD/SDR、自适应数值方案或FD对比。依据physd.txt行14–27、81–122、139–260、1103–1108。

## 共同点与区别

三篇共同利用tau函数将非线性方程改写成可控的双线性代数结构。DLW侧重造解；2HS侧重保持两场结构的可积空间离散；GSG继续把半离散与坐标变换做成数值移动网格算法。当前DLW精度研究需另建离散残差、边界和传播放大分析，不能从可积性或精确孤子公式直接推出数值误差收益。

源PDF未改。hs_extract.txt与tmp/pdfs/只用于阅读核对。并行原文核验采用gsg_paper_reading、dlw_paper_reading两代理；2HS由主代理PDF阅读。
