# 首轮之后的参数检索（2026-10-15）

## 实际检索

- arXiv正式条目：https://arxiv.org/abs/2608.28077
- arXiv v2源包：https://arxiv.org/src/2608.28077v2
- Chang研究所页面：https://icmsec.cc.ac.cn/en/article/5/34.html?language=cn&section=5&zy=34
- Tao学校页面：https://msm.bjut.edu.cn/info/1088/2582.htm
- Liu个人主页及论文列表：https://lsec.cc.ac.cn/~liuyong/ 、https://lsec.cc.ac.cn/~liuyong/Paper.html
- 检索全文题名/arXiv编号结合code、implementation、timestep及site:github.com。

## 找到的材料

已下载v2源包，含paper.tex、14个EPS图和arXiv说明文件；无求解器、原始数值数组、配置文件。原始响应保存为arxiv_source_response.bin，清单见source_inventory.json。EPS标注Creator: TECPLOT，只说明绘图工具，不能据此推断求解器语言。

检查paper.tex及注释，数值部分仍仅说明经典RK4、dt=O(h)；未找到具体CFL、求积节点数、尖峰专用初始化或compact-support边界通量。理论初始化为P_h^- U0，不据此断言所有实验使用该初始化。未检索到与该论文对应的公开求解器仓库；这不证明作者没有代码。

例5.5没有明确另给c，本版使用c=1并保留未确认标记。没有给作者发送邮件。

## 图3纵轴口径的新增疑点

首轮例5.4耗散版本得到 E(0)-E(5)=0.5517175，而 sqrt(E(0))-sqrt(E(5))=0.167352。
原图3耗散曲线的末值约0.168。正文定义E为H1范数平方，但EPS文件名含H1norm。
这些证据提示原图可能绘制H1范数差而非平方能量差；目前只能作为待确认假设。
为便于核对，保留两种指标，并直接读取原EPS路径坐标得到曲线；不修改算法参数来拟合此曲线，不把绘图坐标当原始数值数据。
