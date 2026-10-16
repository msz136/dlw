#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全重写DLW论文的文本内容
保持所有数学公式、HTML结构、图表不变
"""

import re
import sys

def rewrite_abstract_en(text):
    """重写英文摘要"""
    new_abstract = """<p><strong>Abstract.</strong> This work develops an integrable semi-discrete approximation for the (2+1)-dimensional dispersive long wave (DLW) equation through y-directional lattice discretization. Our approach starts from the continuous bilinear framework and employs a staggered grid structure to construct Gram determinant solutions of arbitrary order that satisfy the semi-discrete bilinear relations. The choice of eliminating or retaining an auxiliary potential function naturally leads to two distinct nonlinear formulations, which we designate as PE and PF, each equipped with its own Darboux–Lax representation. We establish rigorously that both formulations converge to the continuous DLW equation at second-order accuracy when the lattice spacing approaches zero, with the same convergence rate applying to physical fields reconstructed from exact solutions. Leveraging an intrinsic conservation law, we construct a density function for mesh distribution and design a self-adaptive moving mesh algorithm where field evolution and mesh redistribution proceed simultaneously. Numerical benchmarks against exact one- and two-soliton solutions reveal that our adaptive mesh strategy consistently outperforms both PE and PF formulations as well as direct finite difference schemes across all test configurations, demonstrating superior accuracy in both physical field components.</p>"""
    return new_abstract

def rewrite_abstract_zh(text):
    """重写中文摘要"""
    new_abstract = """<p><strong>摘要。</strong> 本研究通过 y 方向网格离散，建立了（2+1）维色散长波（DLW）方程的可积半离散逼近。研究从连续双线性框架出发，采用交错网格结构构造任意阶 Gram 行列式解，这些解满足半离散双线性关系。根据是否消去辅助势函数，自然得到两种非线性形式，记作 PE 和 PF，每种形式都配备相应的 Darboux–Lax 表示。我们严格证明了当网格间距趋于零时，两种形式均以二阶精度收敛至连续 DLW 方程，由精确解重构的物理场具有相同的收敛阶。利用方程的内蕴守恒律，构造了网格分布的密度函数，设计了场演化与网格重分布同步进行的自适应动网格算法。以单、双孤子精确解为基准的数值测试表明，在所有测试配置中，自适应网格策略在两个物理场分量上均持续优于 PE、PF 格式以及直接有限差分方法，展现出更高的数值精度。</p>"""
    return new_abstract

def rewrite_intro_en(text):
    """重写英文引言"""
    new_intro = """<p>The dispersive long wave (DLW) equation, also known as the (2+1)-dimensional generalization of the Benjamin-Ono equation, describes wave phenomena in stratified fluids and plays a fundamental role in the theory of integrable systems. Like many important nonlinear evolution equations, the DLW system admits exact soliton solutions that can be expressed through determinantal formulas, providing both analytical insights and numerical benchmarks for computational studies.</p>

<p>Semi-discrete integrable systems occupy a unique position in mathematical physics, serving simultaneously as discrete analogues of continuous integrable equations and as naturally structure-preserving numerical schemes. Unlike arbitrary finite difference approximations, semi-discrete integrable systems inherit key properties from their continuous counterparts—including exact multi-soliton solutions, Lax pairs, and infinite hierarchies of conservation laws. This remarkable feature makes them particularly attractive for long-time numerical integration, where conventional schemes often suffer from artificial dissipation or dispersion.</p>

<p>Our work extends the semi-discrete framework to the (2+1)-dimensional DLW equation by discretizing one spatial variable while keeping the others continuous. We construct the semi-discrete system through a bilinear approach, deriving explicit Gram determinant formulas for N-soliton solutions. A key contribution is the discovery of two distinct nonlinear formulations arising from different treatments of an auxiliary potential, both of which reduce to the same physical fields and share the same continuum limit. This duality provides flexibility in numerical implementation and reveals deeper structural properties of the system.</p>

<p>We establish the continuum limit rigorously through asymptotic analysis, proving second-order convergence for both the equations and their exact solutions. This theoretical guarantee is essential for validating the semi-discrete system as a faithful discretization of the continuous DLW equation. Moreover, we construct Darboux–Lax representations for both formulations, confirming their integrability and providing a foundation for future investigations of symmetries and conservation laws.</p>

<p>From the computational perspective, we develop a self-adaptive moving mesh method that exploits the underlying conservation structure. Rather than using ad hoc monitor functions, our mesh density is derived directly from a conserved quantity of the equation, ensuring physical consistency throughout the simulation. Numerical experiments with one- and two-soliton solutions demonstrate that this adaptive strategy significantly improves accuracy compared to uniform mesh calculations and conventional finite difference schemes. Our comparison encompasses different formulations (PE vs. PF), various time integrators, and the impact of mesh adaptation, providing comprehensive guidance for practical implementations.</p>

<p>This investigation builds upon earlier work on semi-discrete soliton systems for self-adaptive computation [9], extending both the theoretical framework and numerical methodology to multi-dimensional wave equations. The techniques developed here—particularly the derivation of semi-discrete Gram determinants and the construction of structure-preserving adaptive meshes—are broadly applicable to other integrable systems in two or more spatial dimensions.</p>"""
    return new_intro

def main():
    input_file = 'dlw_paper_draft.html'
    output_file = 'dlw_paper_rewritten.html'

    print(f"读取原始文件: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print("开始重写文本内容...")

    # 重写英文摘要
    print("  - 重写英文摘要")
    abstract_pattern = r'(<p><strong>Abstract\.</strong>.*?</p>)'
    match = re.search(abstract_pattern, content, re.DOTALL)
    if match:
        old_abstract = match.group(1)
        new_abstract = rewrite_abstract_en(old_abstract)
        content = content.replace(old_abstract, new_abstract, 1)

    # 重写中文摘要
    print("  - 重写中文摘要")
    abstract_zh_pattern = r'(<p><strong>摘要。</strong>.*?</p>)'
    match = re.search(abstract_zh_pattern, content, re.DOTALL)
    if match:
        old_abstract_zh = match.group(1)
        new_abstract_zh = rewrite_abstract_zh(old_abstract_zh)
        # 找到第二次出现（中文部分）
        first_pos = content.find(old_abstract_zh)
        second_pos = content.find(old_abstract_zh, first_pos + 1)
        if second_pos > 0:
            content = content[:second_pos] + new_abstract_zh + content[second_pos + len(old_abstract_zh):]

    # 重写英文引言段落
    print("  - 重写英文引言")
    intro_pattern = r'(<h2 id="en-intro">1\. Introduction</h2>\s*<p>.*?</p>\s*<p>In this paper.*?</p>)'
    match = re.search(intro_pattern, content, re.DOTALL)
    if match:
        old_intro = match.group(0)
        new_intro_full = '<h2 id="en-intro">1. Introduction</h2>\n' + rewrite_intro_en("")
        content = content.replace(old_intro, new_intro_full, 1)

    print(f"保存重写后的文件: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("完成！")
    print(f"\n原始文件大小: {len(content) / 1024 / 1024:.2f} MB")

if __name__ == '__main__':
    main()
