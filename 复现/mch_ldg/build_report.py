"""Build a concise report from saved experiment records; never rerun the PDE."""
import json,html
from pathlib import Path
import numpy as np
from analyze import analyze,load_index

ROOT=Path(__file__).resolve().parents[2]
report=ROOT/'report/mch_ldg_reproduction_20261015.html'
data=analyze()
fmt=lambda x:f'{x:.6g}'
def table(head,rows):
    return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
base=load_index('suite_peakon_*.json')+load_index('suite_other_*.json')
rows=[]
for r in base:
    c=r['config'];f=r['final']
    rows.append([c['case'],c['flux'],c['n'],c['k'],fmt(f['l2_u']),fmt(f['energy_error']),fmt(f['energy_loss'])])
bench=table(['算例','通量','单元数','次数','‖U−u‖₂','联合能量范数误差','E(0)−E(5)'],rows)
smooth=[]
for r in load_index('control_domain_*.json'):
    if r['config']['flux']=='conservative':
        c=r['config'];smooth.append([c['k'],c['n'],fmt(80/c['n']),fmt(r['final']['energy_error'])])
conv=table(['次数','单元数','格距 h','联合误差'],smooth)
controls=table(['控制试验','通量','末态差的能量范数','控制后的平方能量损失'],[[r['control'],r['flux'],fmt(r['state_energy_distance']),fmt(r['energy_loss1'])] for r in data['controls']])
failed=table(['算例','次数','单元数','停止时刻','最后诊断时刻'],[[r['case'],r['k'],r['n'],fmt(r['reached']),fmt(r['diagnostic_time'])] for r in data['failed_runs']])
metric=data['figure3_metric_hypothesis']
body=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>mCH LDG：首轮复现</title>
<style>body{{max-width:1060px;margin:44px auto;padding:0 24px;color:#20252b;font:17px/1.8 "Microsoft YaHei",sans-serif;background:#fff}}h1{{font-size:30px;font-weight:600}}h2{{font-size:23px;margin-top:36px}}p{{margin:14px 0}}small,.caption{{font-size:14px;color:#555}}img{{width:100%;height:auto}}figure{{margin:24px 0}}table{{border-collapse:collapse;width:100%;font-size:14px}}th,td{{padding:8px 12px;text-align:right;border-bottom:1px solid #ddd;white-space:nowrap}}th:first-child,td:first-child{{text-align:left}}thead{{border-top:2px solid #333;border-bottom:1px solid #333}}.scroll{{overflow:auto}}.eq{{text-align:center;padding:16px;font-family:Georgia,serif;font-size:20px}}a{{color:#2166ac}}@media(max-width:600px){{body{{padding:0 14px;margin:24px auto;font-size:16px}}h1{{font-size:25px}}}}@media print{{body{{margin:0;font-size:11pt}}figure,table{{break-inside:avoid}}}}</style>
<main><h1>mCH 方程 LDG 方法的首轮复现</h1><p class="caption">Chang–Liu–Tao, arXiv:2608.28077v2 · 2026年10月15日</p>
<p>已实现两套 LDG 通量、RK4 时间推进和五个算例的解析参照，共保存 {data['total_runs']} 次运行，{data['completed_runs']} 次到达终点。周期基线通过离散能量恒等式与时间四阶检查。单尖峰实验重现了守恒格式更好保持峰形的现象；原文全部收敛表及边界设置尚未完成对齐。</p>
<h2>1　离散系统与核验</h2><p>将 R=U<sub>x</sub>、P=(U²R)<sub>x</sub>、S=(R³/3)<sub>x</sub> 引入一阶系统，在每个单元内用 Legendre 多项式展开。采用原文的交替通量和非线性耦合通量，分别选择守恒、耗散通量。体积分采用足以精确积分相关多项式的 Gauss 规则。</p>
<div class="eq">r=D⁻u，m=(I−D⁺D⁻)u，(I−D⁺D⁻)u<sub>t</sub>=m<sub>t</sub>。</div>
<p>固定边界下以上推进与演化 m 等价。周期算子的离散分部积分、质量守恒、能量导数恒等式、Helmholtz 求解及投影关系等 48 项检查全部通过。光滑单、双孤子的解析导数及方程残差另作独立差分核验。固定空间的 RK4 自收敛阶为 {', '.join(f'{p:.4f}' for p in data['rk4']['observed_orders'])}。</p>
<h2>2　单尖峰传播</h2><p>例5.4采用 U=√(3/2)exp(−|x−t|)，区间 (−20,20)，P³、640单元、T=5，首轮步长 0.0005。基线采用周期截断；原文称 compact-support 边界。更换为本次设计的零值边界闭合后，末态差的能量范数低于 5×10⁻⁷。本次选择的闭合不代表原作者实现。</p>
<figure><img src="../复现/mch_ldg/figures/peakon_first.png" alt="单尖峰的剖面、能量及原图纵轴比较"><figcaption class="caption">上：精确解与两套数值解。下：全区间平方能量差、时间步控制、范数差与原始EPS曲线的比较。右下比较仅检验指标解释的假设。</figcaption></figure>
<p>守恒版峰形明显更接近精确解，但仍有位置偏差和局部振荡。步长减半后平方能量漂移由 9.84×10⁻⁸ 降至 5.13×10⁻¹⁰；耗散版平方能量损失约 0.551718，基本不随步长减半改变。能量保持与波形误差分别评价。</p>
<h2>3　原图3的纵轴疑点</h2><p>原文定义 E=∫(u²+r²)dx。本次耗散结果的 E(0)−E(5)={fmt(metric['our_energy_loss'])}，而 √E(0)−√E(5)={fmt(metric['our_norm_loss'])}。直接读取原始 EPS 的矢量路径，最后一个点为 t={fmt(metric['paper_last_time'])}、纵坐标 {fmt(metric['paper_last_ordinate'])}。采样时刻上的范数差与原曲线最大绝对差约 {fmt(metric['norm_curve_max_difference'])}。</p>
<p>这提示原图可能绘制 H¹ 范数差，但尚未得到作者确认。两种指标均保留，未据此更改步长或通量以拟合原图。EPS 文件名中的 H1norm 只能作为线索，不能代替指标定义。</p>
<h2>4　光滑解与其他算例</h2><p>例5.1在原区间上的周期截断产生边界敏感性：P³误差随加密反而增加。保持相同格距、将区间扩为 (−40,40) 后误差持续下降。下表给出扩域守恒版结果；这些是边界控制实验，并非原文表1的复现值，局部观测阶也不能直接升级为一般误差定理。</p>{conv}
<figure><img src="../复现/mch_ldg/figures/smooth_convergence.png" alt="原区间与扩域的光滑解误差加密比较"><figcaption class="caption">相同格距下的原区间和扩域比较，均使用周期截断。原区间不能据此宣称得到空间收敛。</figcaption></figure>
<p>五个算例均有运行入口。以下为单尖峰及其他算例的首个网格结果；所有行 T=5。例5.2取 α=0.5，例5.3取 α₁=0.7、α₂=0.5。例5.5暂取 c=1，原文未另给数值 c。除例5.5外，基线均采用周期截断近似。</p>{bench}
<figure><img src="../复现/mch_ldg/figures/other_cases.png" alt="其余三个算例的终态剖面"><figcaption class="caption">例5.2、5.3、5.5的首版终态，尚未完成全部参数和加密矩阵。</figcaption></figure>
<p>例5.5守恒版的平方能量损失在 dt=0.0005 时约 6.83×10⁻⁴，缩至 0.000125 后约 6.50×10⁻⁷，说明初始时间分辨率不足以重现原图的小漂移。原图约10⁻¹⁰的漂移尚未对齐。时间步控制、零边界和 L² 初值对照如下。</p>{controls}
<h2>5　边界试验的失败结果</h2><p>本次另构造了固定 Dirichlet 值与内部辅助变量迹配合的闭合。零背景单尖峰结果与周期截断接近；非零背景例5.1的部分加密运行明显恶化，其中以下3次未到达终点。该闭合目前不作为可靠的非零背景算法。表中最后诊断时刻与停止时刻分列，未以早期误差冒充终态误差。</p>{failed}
<h2>6　参数检索与后续对齐</h2><p>完成首版后下载了 <a href="https://arxiv.org/src/2608.28077v2">arXiv v2 源包</a>：包含正文和14张EPS图，没有求解器代码或原始数组。检查正文及注释，并检索作者公开页面和GitHub索引，尚未找到具体 CFL 常数、体积分设置、尖峰初始化或截断边界通量。未发现公开仓库不等于作者没有代码。</p>
<p>下一步优先厘清图3纵轴口径，建立适合非零背景的边界闭合，再逐项对齐表1—5。当前已经具备独立运行、保存轨迹和诊断误差的基础设施，尚不能称为全文数值结果复现完成。</p>
<p class="caption"><a href="../复现/mch_ldg/README.md">复现入口与运行说明</a> · <a href="../复现/mch_ldg/results/all_runs.csv">全部运行数据表</a> · <a href="../复现/mch_ldg/search/FINDINGS.md">检索记录</a> · <a href="../Paper/refs/2608_28077/2608.28077v2.pdf">原论文</a></p></main></html>'''
report.write_text(body,encoding='utf-8')
print(str(report))
