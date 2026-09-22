# -*- coding: utf-8 -*-
"""给 HTML 报告源码插入作废横幅（一次性使用）。"""
import io

P = r'C:\Users\msz\学术内容\Paper\gsg_project\dlw_report\_src\index.src.html'
s = io.open(P, encoding='utf-8').read()

if 'AUDIT-BANNER' in s:
    print('already inserted')
    raise SystemExit

BANNER = '''
<div id="AUDIT-BANNER" style="margin:1.2em 0;padding:1em 1.2em;border:2px solid #b91c1c;background:#fef2f2;border-radius:6px">
<h2 style="margin-top:0;color:#b91c1c">⚠ 作废声明：本报告 §3 起的离散（格点）结果无效</h2>
<p><b>审计结论见 <code>dlw_semidiscrete/AUDIT.md</code>。</b>复核发现两个缺陷：</p>
<ol>
<li><b>浮点噪声被当成零。</b>计算引擎 <code>jet3.py</code> 的系数是 <code>mpmath.mpf</code>（60–90 位浮点），
所以残差 <code>1e-89</code> 是舍入噪声，不是数学意义上的 0。</li>
<li><b>单点判零（致命）。</b>所有判零都只在<b>单个基点</b>
<code>(x,t,y)=(1/5,&nbsp;2/7,&nbsp;0)</code> 上求值，而该点恰好落在使残差为零的曲面上：
<code>(7)_h</code> 的残差精确正比于 <code>exp(433y/385)&nbsp;−&nbsp;1</code>。
于是<b>非恒等式被误判为恒等式</b>。</li>
</ol>
<p><b>核心双线性方程 <code>(7)_h</code>、<code>(6)_h</code> 并不恒成立</b>：残差在一般点上的量级为
<code>O(0.02–2833)</code>，且随 <code>h→0</code> 按 <b><code>O(h)</code></b> 衰减
（比值 0.483&nbsp;→&nbsp;0.498），它们是离散化误差而非有限 <code>h</code> 下的恒等式。
由它们导出的 <code>(★)</code>、<code>(★')</code>、<code>(†)</code>、以及<b>整个"非线性层"</b>
<code>(A)_h</code>/<code>(B)_h</code>/<code>(A')</code> 与连续极限那张表，<b>全部作废</b>。</p>
<p><b>仍然成立</b>：</p>
<ul>
<li><code>(H1)</code> 商恒等式
<code>D_x²F·G/(FG)&nbsp;=&nbsp;(lnF)_xx+(lnG)_xx+[(lnF)_x−(lnG)_x]²</code>（交叉项系数 <b>+1</b>）——
这是<b>真正的精确代数恒等式</b>，由 <code>idcheck3.py</code> 在任意符号 <code>F,G</code> 上
用 sympy 严格证明，并用 <code>Fraction</code> 得到字面 0。</li>
<li>连续层 <code>(7)&nbsp;B_a f·g = 0</code>：精确为零（N=1、N=2 均确认）。</li>
<li>论文形态的 <code>(6)</code> 与所实现 τ 函数<b>不相容</b>（残差与相位常数无关，对相位常数无解）——
此问题尚未解决。</li>
</ul>
<p style="margin-bottom:0">下文正文保留以便对照，但 <b>§3 起的一切"精确验证"字样请勿采信</b>。</p>
</div>
'''

i = s.find('<body')
j = s.find('>', i) + 1
s = s[:j] + BANNER + s[j:]
io.open(P, 'w', encoding='utf-8').write(s)
print('banner inserted at offset', j)
