#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

# 读取文件
with open('dlw_paper_rewritten.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("开始重写第2节、第3节、结论和章节过渡...")

# ==================== 第2节引导语重写 ====================
print("  - 重写第2节引导语（英文）")

section2_intro_en = """<h2 id="en-continuous">2. Semi-discrete DLW system and exact solutions</h2>
<p>In this section, we develop the semi-discrete framework for the DLW equation by introducing a lattice structure in the y-direction while maintaining continuity in x and t. Our construction proceeds through the bilinear formalism, which provides a natural pathway to exact solutions. We begin by reviewing the continuous DLW system and its bilinear representation, then systematically discretize the y-variable using a staggered grid. The resulting semi-discrete bilinear equations admit Gram determinant solutions of arbitrary order, generalizing the continuous case. By eliminating or preserving an auxiliary potential, we derive two equivalent nonlinear formulations—each yielding the same physical fields but offering different computational advantages. We rigorously establish that both formulations converge to the continuous limit at second-order accuracy, and we construct their Darboux–Lax representations to confirm the integrable structure.</p>"""

# 找到第2节标题位置
pos = content.find('<h2 id="en-continuous">2. Semi-discrete DLW system and exact solutions</h2>')
if pos > 0:
    # 找到下一个h3标题
    next_h3 = content.find('<h3', pos)
    if next_h3 > 0:
        # 替换这之间的内容
        before = content[:pos]
        after = content[next_h3:]
        content = before + section2_intro_en + '\n' + after

print("  - 重写第2节引导语（中文）")

section2_intro_zh = """<h2 id="zh-continuous">2. 半离散 DLW 系统与精确解</h2>
<p>本节通过在 y 方向引入格点结构同时保持 x 和 t 的连续性，构建 DLW 方程的半离散框架。我们的构造基于双线性形式，这为精确解提供了自然的途径。首先回顾连续 DLW 系统及其双线性表示，然后使用交错网格系统地离散 y 变量。所得的半离散双线性方程具有任意阶 Gram 行列式解，推广了连续情形。通过消去或保留辅助势，导出两种等价的非线性表述——它们给出相同的物理场但提供不同的计算优势。我们严格证明了两种表述均以二阶精度收敛至连续极限，并构造了它们的 Darboux–Lax 表示以确认可积结构。</p>"""

pos_zh = content.find('<h2 id="zh-continuous">2. 半离散 DLW 系统与精确解</h2>')
if pos_zh > 0:
    next_h3_zh = content.find('<h3', pos_zh)
    if next_h3_zh > 0:
        before_zh = content[:pos_zh]
        after_zh = content[next_h3_zh:]
        content = before_zh + section2_intro_zh + '\n' + after_zh

# ==================== 第3节完全重写 ====================
print("  - 重写第3节开头（英文）")

section3_intro_en = """<h2 id="en-numerics">3. Numerical methods and experiments</h2>
<p>Having established the theoretical foundations of the semi-discrete DLW system, we now turn to practical implementation and numerical validation. This section presents a comprehensive computational framework built upon the integrable structure developed in Section 2. We first describe how the semi-discrete formulations PE and PF translate into concrete numerical schemes through spatial discretization. A key innovation is the self-adaptive moving mesh algorithm, which dynamically redistributes grid points according to a density function derived from the equation's conservation law. This approach ensures that mesh refinement aligns with the physical features of the solution, particularly in regions of high gradient or wave interaction.</p>
<p>Our numerical experiments serve dual purposes: to validate the theoretical convergence results and to assess the practical performance of different formulations and algorithmic choices. We employ exact one- and two-soliton solutions as benchmark problems, enabling precise quantification of numerical errors. The test suite systematically compares PE versus PF formulations, examines various time integration methods, and evaluates the impact of adaptive mesh refinement. Through these controlled experiments, we demonstrate that structure-preserving discretizations combined with adaptive meshing significantly outperform conventional finite difference schemes, particularly for long-time simulations where preservation of invariants becomes critical.</p>"""

pos_s3 = content.find('<h2 id="en-numerics">3. Numerical methods and experiments</h2>')
if pos_s3 > 0:
    next_h3_s3 = content.find('<h3', pos_s3)
    if next_h3_s3 > 0:
        before_s3 = content[:pos_s3]
        after_s3 = content[next_h3_s3:]
        content = before_s3 + section3_intro_en + '\n' + after_s3

print("  - 重写第3节开头（中文）")

section3_intro_zh = """<h2 id="zh-numerics">3. 数值方法与实验</h2>
<p>在建立了半离散 DLW 系统的理论基础后，我们转向实际实现和数值验证。本节呈现基于第2节所发展的可积结构构建的综合计算框架。首先描述如何通过空间离散将半离散表述 PE 和 PF 转化为具体的数值格式。一个关键创新是自适应动网格算法，它根据从方程守恒律导出的密度函数动态重分布网格点。这一方法确保网格加密与解的物理特征对齐，特别是在高梯度或波相互作用的区域。</p>
<p>我们的数值实验具有双重目的：验证理论收敛结果并评估不同表述和算法选择的实际性能。采用精确的单、双孤子解作为基准问题，能够精确量化数值误差。测试套件系统地比较 PE 与 PF 表述，考察各种时间积分方法，并评估自适应网格加密的影响。通过这些对照实验，我们展示了保结构离散与自适应网格的结合显著优于传统有限差分格式，特别是在不变量保持成为关键的长时间模拟中。</p>"""

pos_s3_zh = content.find('<h2 id="zh-numerics">3. 数值方法与实验</h2>')
if pos_s3_zh > 0:
    next_h3_s3_zh = content.find('<h3', pos_s3_zh)
    if next_h3_s3_zh > 0:
        before_s3_zh = content[:pos_s3_zh]
        after_s3_zh = content[next_h3_s3_zh:]
        content = before_s3_zh + section3_intro_zh + '\n' + after_s3_zh

# ==================== 结论部分重写 ====================
print("  - 重写结论部分（英文）")

conclusion_en = """<h2 id="en-conclusion">4. Conclusion</h2>
<p>This work establishes a comprehensive framework for the semi-discrete approximation of the (2+1)-dimensional dispersive long wave equation, bridging the gap between continuous integrable systems and practical numerical computation. Our principal contributions span theoretical analysis, structural characterization, and algorithmic development.</p>
<p>On the theoretical front, we have constructed a semi-discrete bilinear system through y-directional lattice discretization that preserves the integrable structure of the continuous DLW equation. The derivation of arbitrary-order Gram determinant solutions provides explicit formulas for multi-soliton dynamics in the discrete setting. Perhaps most significantly, we have identified two distinct nonlinear formulations—PE and PF—arising from different treatments of an auxiliary potential, both converging to the same continuous limit. This duality reveals a rich structure in the semi-discrete approximation space and offers flexibility in numerical implementation. The rigorous proof of second-order convergence, applying to both the governing equations and their exact solutions, establishes a firm mathematical foundation for the semi-discrete approach.</p>
<p>The construction of Darboux–Lax representations for both formulations confirms their integrable nature and opens avenues for future investigation of symmetries, conservation laws, and transformations. These representations not only validate the mathematical consistency of our approach but also suggest potential extensions to other integrable systems in multiple spatial dimensions.</p>
<p>From the computational perspective, our self-adaptive moving mesh algorithm represents a natural synthesis of integrable structure and numerical adaptivity. By deriving the mesh density function directly from an intrinsic conservation law rather than relying on ad hoc indicators, we ensure physical consistency throughout the evolution. Numerical experiments with one- and two-soliton benchmarks demonstrate that this adaptive strategy consistently delivers superior accuracy compared to both uniform mesh calculations and conventional finite difference schemes. The performance gains are particularly pronounced in capturing localized wave structures and maintaining long-time accuracy—precisely the scenarios where structure preservation matters most.</p>
<p>Our comparative analysis reveals interesting distinctions between the PE and PF formulations in practical computation. While both converge to the same continuum limit theoretically, their numerical behaviors exhibit subtle differences depending on the choice of time integrator and mesh adaptation parameters. These observations underscore the importance of matching discretization strategy to problem characteristics.</p>
<p>Several directions merit further exploration. The extension to higher-dimensional integrable systems, the development of fully discrete schemes that retain integrability, and the investigation of more sophisticated adaptive strategies based on multiple conservation laws all represent promising research avenues. Additionally, the application of our semi-discrete framework to other (2+1)-dimensional integrable equations—such as the Kadomtsev-Petviashvili, Davey-Stewartson, and Nizhnik-Novikov-Veselov systems—could yield valuable insights into the universality of structure-preserving discretization principles.</p>
<p>In conclusion, this work demonstrates that semi-discrete integrable systems offer a principled pathway from continuous soliton equations to effective numerical algorithms. By respecting the underlying mathematical structure rather than imposing arbitrary approximations, we achieve both theoretical elegance and computational efficiency—a combination that continues to drive progress in the numerical analysis of integrable systems.</p>"""

# 找到英文结论部分
pos_concl = content.find('<h2 id="en-conclusion">4. Conclusion</h2>')
if pos_concl > 0:
    # 找到下一个h2标题
    next_h2_concl = content.find('<h2 id="en-data">')
    if next_h2_concl > 0:
        before_concl = content[:pos_concl]
        after_concl = content[next_h2_concl:]
        content = before_concl + conclusion_en + '\n' + after_concl

print("  - 重写结论部分（中文）")

conclusion_zh = """<h2 id="zh-conclusion">4. 结论</h2>
<p>本研究为（2+1）维色散长波方程的半离散逼近建立了综合框架，在连续可积系统与实际数值计算之间架起桥梁。我们的主要贡献涵盖理论分析、结构刻画和算法开发。</p>
<p>在理论层面，通过 y 方向格点离散构造了保持连续 DLW 方程可积结构的半离散双线性系统。任意阶 Gram 行列式解的导出为离散环境中的多孤子动力学提供了显式公式。最重要的是，我们识别出源于辅助势不同处理的两种截然不同的非线性表述——PE 和 PF，两者收敛至相同的连续极限。这种对偶性揭示了半离散逼近空间的丰富结构，并为数值实现提供了灵活性。对控制方程及其精确解的二阶收敛性的严格证明，为半离散方法奠定了坚实的数学基础。</p>
<p>为两种表述构造的 Darboux–Lax 表示确认了其可积性质，并为未来研究对称性、守恒律和变换开辟了途径。这些表示不仅验证了我们方法的数学一致性，还提示了向多空间维可积系统推广的潜力。</p>
<p>从计算角度看，我们的自适应动网格算法代表了可积结构与数值自适应性的自然融合。通过直接从内蕴守恒律导出网格密度函数而非依赖临时指标，确保了演化过程中的物理一致性。以单、双孤子为基准的数值实验表明，这一自适应策略相较于均匀网格计算和传统有限差分格式持续提供更优的精度。性能提升在捕捉局域波结构和维持长时间精度方面尤为显著——恰恰是结构保持最为重要的场景。</p>
<p>我们的对比分析揭示了 PE 和 PF 表述在实际计算中的有趣区别。虽然两者在理论上收敛至相同的连续极限，但其数值行为根据时间积分器和网格自适应参数的选择表现出微妙差异。这些观察强调了将离散化策略与问题特性相匹配的重要性。</p>
<p>若干方向值得进一步探索。向高维可积系统的推广、保持可积性的完全离散格式的发展、基于多个守恒律的更复杂自适应策略的研究，都代表了有前景的研究方向。此外，将我们的半离散框架应用于其他（2+1）维可积方程——如 Kadomtsev-Petviashvili、Davey-Stewartson 和 Nizhnik-Novikov-Veselov 系统——可能会对保结构离散化原理的普适性产生有价值的洞察。</p>
<p>总之，本研究证明了半离散可积系统为从连续孤子方程到有效数值算法提供了原则性路径。通过尊重底层数学结构而非施加任意逼近，我们实现了理论优雅性与计算效率的结合——这一结合持续推动可积系统数值分析的进步。</p>"""

pos_concl_zh = content.find('<h2 id="zh-conclusion">4. 结论</h2>')
if pos_concl_zh > 0:
    next_h2_concl_zh = content.find('<h2 id="zh-data">')
    if next_h2_concl_zh > 0:
        before_concl_zh = content[:pos_concl_zh]
        after_concl_zh = content[next_h2_concl_zh:]
        content = before_concl_zh + conclusion_zh + '\n' + after_concl_zh

# 保存文件
with open('dlw_paper_rewritten.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n完成！已重写:")
print("  - 第2节引导语（中英文）")
print("  - 第3节开头段落（中英文）")
print("  - 第4节结论（中英文完全重写）")
print(f"\n文件大小: {len(content)/1024/1024:.2f} MB")
