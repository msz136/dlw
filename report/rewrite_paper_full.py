#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全重写DLW论文 - 完整版本
"""

import re
import sys

# ========== 英文部分重写 ==========

ABSTRACT_EN = """<p><strong>Abstract.</strong> This work develops an integrable semi-discrete approximation for the (2+1)-dimensional dispersive long wave (DLW) equation through y-directional lattice discretization. Our approach starts from the continuous bilinear framework and employs a staggered grid structure to construct Gram determinant solutions of arbitrary order that satisfy the semi-discrete bilinear relations. The choice of eliminating or retaining an auxiliary potential function naturally leads to two distinct nonlinear formulations, which we designate as PE and PF, each equipped with its own Darboux–Lax representation. We establish rigorously that both formulations converge to the continuous DLW equation at second-order accuracy when the lattice spacing approaches zero, with the same convergence rate applying to physical fields reconstructed from exact solutions. Leveraging an intrinsic conservation law, we construct a density function for mesh distribution and design a self-adaptive moving mesh algorithm where field evolution and mesh redistribution proceed simultaneously. Numerical benchmarks against exact one- and two-soliton solutions reveal that our adaptive mesh strategy consistently outperforms both PE and PF formulations as well as direct finite difference schemes across all test configurations, demonstrating superior accuracy in both physical field components.</p>"""

INTRO_EN_PARA1 = """<p>The dispersive long wave (DLW) equation, also known as the (2+1)-dimensional generalization of the Benjamin-Ono equation, describes wave phenomena in stratified fluids and plays a fundamental role in the theory of integrable systems. Like many important nonlinear evolution equations, the DLW system admits exact soliton solutions that can be expressed through determinantal formulas, providing both analytical insights and numerical benchmarks for computational studies.</p>"""

INTRO_EN_PARA2 = """<p>Semi-discrete integrable systems occupy a unique position in mathematical physics, serving simultaneously as discrete analogues of continuous integrable equations and as naturally structure-preserving numerical schemes. Unlike arbitrary finite difference approximations, semi-discrete integrable systems inherit key properties from their continuous counterparts—including exact multi-soliton solutions, Lax pairs, and infinite hierarchies of conservation laws. This remarkable feature makes them particularly attractive for long-time numerical integration, where conventional schemes often suffer from artificial dissipation or dispersion.</p>"""

INTRO_EN_MAIN = """<p>Our work extends the semi-discrete framework to the (2+1)-dimensional DLW equation by discretizing one spatial variable while keeping the others continuous. We construct the semi-discrete system through a bilinear approach, deriving explicit Gram determinant formulas for N-soliton solutions. A key contribution is the discovery of two distinct nonlinear formulations arising from different treatments of an auxiliary potential, both of which reduce to the same physical fields and share the same continuum limit. This duality provides flexibility in numerical implementation and reveals deeper structural properties of the system. We establish the continuum limit rigorously through asymptotic analysis, proving second-order convergence for both the equations and their exact solutions. Moreover, we construct Darboux–Lax representations for both formulations, confirming their integrability. From the computational perspective, we develop a self-adaptive moving mesh method that exploits the underlying conservation structure, with numerical experiments demonstrating significant accuracy improvements compared to uniform mesh calculations.</p>"""

# ========== 中文部分重写 ==========

ABSTRACT_ZH = """<p><strong>摘要。</strong> 本研究通过 y 方向网格离散，建立了（2+1）维色散长波（DLW）方程的可积半离散逼近。研究从连续双线性框架出发，采用交错网格结构构造任意阶 Gram 行列式解，这些解满足半离散双线性关系。根据是否消去辅助势函数，自然得到两种非线性形式，记作 PE 和 PF，每种形式都配备相应的 Darboux–Lax 表示。我们严格证明了当网格间距趋于零时，两种形式均以二阶精度收敛至连续 DLW 方程，由精确解重构的物理场具有相同的收敛阶。利用方程的内蕴守恒律，构造了网格分布的密度函数，设计了场演化与网格重分布同步进行的自适应动网格算法。以单、双孤子精确解为基准的数值测试表明，在所有测试配置中，自适应网格策略在两个物理场分量上均持续优于 PE、PF 格式以及直接有限差分方法，展现出更高的数值精度。</p>"""

INTRO_ZH_PARA1 = """<p>色散长波（DLW）方程，亦称（2+1）维 Benjamin-Ono 方程的推广形式，描述分层流体中的波动现象，在可积系统理论中占据重要地位。与许多重要的非线性演化方程类似，DLW 系统具有可用行列式公式表达的精确孤子解，为计算研究提供了解析洞察和数值基准。</p>"""

INTRO_ZH_PARA2 = """<p>半离散可积系统在数学物理中具有独特地位，既是连续可积方程的离散类比，又是天然保结构的数值格式。与任意有限差分逼近不同，半离散可积系统继承了连续对应物的关键性质——包括精确多孤子解、Lax 对和无穷守恒律层级。这一显著特性使其特别适合长时间数值积分，而传统格式往往受到人工耗散或色散的困扰。</p>"""

INTRO_ZH_MAIN = """<p>本研究将半离散框架拓展至（2+1）维 DLW 方程，对一个空间变量离散化而保持其他变量连续。通过双线性方法构造半离散系统，导出 N-孤子解的显式 Gram 行列式公式。一个关键贡献是发现了源于辅助势不同处理方式的两种截然不同的非线性表述，两者都归约到相同的物理场并共享相同的连续极限。这种对偶性为数值实现提供了灵活性，并揭示了系统更深层的结构性质。通过渐近分析严格建立了连续极限，证明了方程及其精确解的二阶收敛性。此外，为两种表述构造了 Darboux–Lax 表示，确认了其可积性。从计算角度，发展了利用底层守恒结构的自适应动网格方法，数值实验展示了相较于均匀网格计算的显著精度提升。</p>"""

def main():
    input_file = 'dlw_paper_draft.html'
    output_file = 'dlw_paper_rewritten.html'

    print(f"读取原始文件: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print("开始完全重写文本内容...")

    # 1. 重写英文摘要
    print("  - 重写英文摘要")
    pattern = r'<p><strong>Abstract\.</strong>.*?</p>'
    content = re.sub(pattern, ABSTRACT_EN, content, count=1, flags=re.DOTALL)

    # 2. 重写中文摘要
    print("  - 重写中文摘要")
    # 找到中文部分的摘要（在英文部分之后）
    zh_section_start = content.find('<h2 id="zh-intro">')
    if zh_section_start > 0:
        before_zh = content[:zh_section_start]
        zh_and_after = content[zh_section_start:]

        pattern = r'<p><strong>摘要。</strong>.*?</p>'
        zh_and_after = re.sub(pattern, ABSTRACT_ZH, zh_and_after, count=1, flags=re.DOTALL)

        content = before_zh + zh_and_after

    # 3. 重写英文引言
    print("  - 重写英文引言段落")
    # 找到英文引言部分
    intro_start = content.find('<h2 id="en-intro">1. Introduction</h2>')
    intro_end = content.find('<h2 id="en-continuous">')

    if intro_start > 0 and intro_end > intro_start:
        before_intro = content[:intro_start]
        after_intro = content[intro_end:]

        new_intro = f'''<h2 id="en-intro">1. Introduction</h2>
{INTRO_EN_PARA1}
{INTRO_EN_PARA2}
{INTRO_EN_MAIN}
'''

        content = before_intro + new_intro + after_intro

    # 4. 重写中文引言
    print("  - 重写中文引言段落")
    intro_zh_start = content.find('<h2 id="zh-intro">1. 引言</h2>')
    intro_zh_end = content.find('<h2 id="zh-continuous">')

    if intro_zh_start > 0 and intro_zh_end > intro_zh_start:
        before_intro_zh = content[:intro_zh_start]
        after_intro_zh = content[intro_zh_end:]

        new_intro_zh = f'''<h2 id="zh-intro">1. 引言</h2>
{INTRO_ZH_PARA1}
{INTRO_ZH_PARA2}
{INTRO_ZH_MAIN}
'''

        content = before_intro_zh + new_intro_zh + after_intro_zh

    print(f"保存重写后的文件: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    file_size_mb = len(content) / 1024 / 1024
    print(f"完成！文件大小: {file_size_mb:.2f} MB")
    print(f"\n已重写的部分:")
    print("  ✓ 英文摘要")
    print("  ✓ 中文摘要")
    print("  ✓ 英文引言")
    print("  ✓ 中文引言")

if __name__ == '__main__':
    main()
