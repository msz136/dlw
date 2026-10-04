const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'../..');
const reportDir=path.join(root,'report');
const katex=require(path.join(root,'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js'));
const math=s=>'<div class="eq">'+katex.renderToString(s,{output:'mathml',displayMode:true,throwOnError:true})+'</div>';
const body=`<p class="meta">DLW · 可积结构复核 · 2026年10月2日</p>
<h1>我们已有怎样的 Lax 结构？</h1>
<p class="lead">已有精确格点孤子、两条 Darboux 算子相容关系，以及孤子族上的非平凡谱波函数。一般物理场的局部相容性已有推导；指定边界与规范后的完整谱表示还没有整理完成。</p>
<h2>一、先分清原论文与我们的工作</h2>
<p>DLW 原论文从连续双线性系统构造 Gram 行列式解，包括孤子、呼吸子与有理解。本项目在此基础上另作 y 方向半离散构造，得到 SD 与 SDR；x、t 仍连续。精确格点解属于我们的半离散工作，不能直接归为原论文的结论。</p>
<p>2HS 论文则走完了“双线性表达—空间离散—离散坐标变换—非线性系统—Lax 相容性—连续极限”的路线。按这条路线比较，DLW 的主要缺口已不是寻找几个精确解。</p>
<h2>二、按 2HS 的流程对照</h2>
<table><thead><tr><th>环节</th><th>DLW 当前结果</th><th>范围</th></tr></thead><tbody>
<tr><td>双线性半离散</td><td>已建立两条交错双线性方程</td><td>仅 y 离散</td></tr>
<tr><td>精确格点解</td><td>任意有限 N 的 Gram 构造与恒等式已证</td><td>正谱数据条件保证一类无奇异解</td></tr>
<tr><td>非线性化</td><td>从共同起点严格推出 SD、SDR 与物理 u、v</td><td>Lean 已核验正实解析分支的前向推导</td></tr>
<tr><td>Lax 相容性</td><td>完整双 Darboux 结构；局部开链可接回 SD，亦可转写 SDR</td><td>需相容势函数与积分自由度；全局边界版本待补</td></tr>
<tr><td>谱参数</td><td>任意 N Gram 族有精确谱波函数和非恒定谱渐近因子</td><td>不是一般初值的完整谱理论</td></tr>
<tr><td>连续极限</td><td>已有方程极限与 Gram 物理场紧盒一致二阶估计</td><td>不等于一般数值求解器二阶收敛定理</td></tr>
<tr><td>自适应网格</td><td>已有守恒密度、通量与数值实验</td><td>实际非均匀 x 差分及 RK4 尚未证明保持此结构</td></tr>
</tbody></table>
<h2>三、Lax 结构具体是什么？</h2>
<p>引入辅助波函数 ψ。它既随时间演化，又在相邻格点之间传递。两种操作相容，才约束物理场满足原来的非线性方程。这与直接写出一个孤子公式不同。</p>
${math(String.raw`W_j=v_j-\delta_0u_j,\qquad w_j^\pm=a+\frac{u_j}{2}\mp\frac h8(W_j-4),\qquad T_j^\pm=\partial_x-w_j^\pm.`)}
${math(String.raw`\mathcal H_j=\partial_t+\partial_x^2+V_j,\qquad \mathcal H_j\psi_j=0,\qquad T_j^+\psi_{j+1}=T_j^-\psi_j.`)}
<p>真正使用的是下面两条共同中间势的算子关系，连同势差约束；不能只保留形式上的格点递推：</p>
${math(String.raw`\mathcal H_j^F T_j^-=T_j^-\mathcal H_j,\qquad \mathcal H_j^F T_j^+=T_j^+\mathcal H_{j+1},\qquad V_{j+1}-V_j=\frac h2W_{j,x}.`)}
<p>这里 Vⱼ=2(log Gⱼ)ₓₓ。保留完整两条关系，可以在局部开链、规范相容的条件下恢复 SD 方程。只写 (T⁺)⁻¹T⁻ 可能在退化分支上丢掉约束，不能据此宣称与全系统无条件等价。DLW 仍有连续 x 方向，采用微分算子是自然的，不必强行要求与 2HS 相同尺寸的矩阵。</p>
<p>在任意 N 的 Gram 解族上，谱参数 z 已给出真正非恒定的归一化渐近因子：</p>
${math(String.raw`\mathcal T(z)=\prod_{i=1}^N\frac{z-p_i}{z+q_i}.`)}
<p>它在所考察正则分支上与 t、j、h 无关。这是谱结构的实质证据，但有限孤子族不能覆盖一般初值。</p>
<h2>四、下一步应补什么？</h2>
<p><strong>先补一条完整的物理场相容性定理：</strong>明确场的光滑性、非退化条件、边界条件及势函数规范，证明完整线性结构的相容条件与 SD 方程等价，并写出 SDR 的对应表达及谱归一化。局部结果已经存在，需要把适用条件与两个方向的推导合起来。</p>
<p>这一步完成后，再研究坐标变换如何作用在线性结构上，判断哪一种自适应离散确实保留它。一般逆散射是更远的目标，不是确认 Lax 对的前置要求。</p>
<h2>依据与核验</h2>
<p>本次重新运行四组精确代数检查，均通过；已有 Lean 主链 39 模块与新端点 9 模块的成功记录，当前源码哈希分别全数吻合，本次未重新编译。旧报告中笼统的“非 S 可积”判断已撤回，不能继续作为结论。</p>
<ul><li><a href="../Workspaces/dlw_integrability_audit_20261002/GRAM_CHAIN_AUDIT.md">Gram 与形式证明链复核</a></li><li><a href="../Workspaces/dlw_integrability_audit_20261002/LAX_AUDIT.md">Lax 算子、局部相容性及退化反例</a></li><li><a href="../Workspaces/dlw_integrability_audit_20261002/SCOPE_AUDIT.md">半离散结构与实际算法的范围</a></li><li><a href="../Workspaces/dlw_integrability_audit_20261002/LAX_CHECK_RUNS.md">实际检查输出</a></li><li><a href="../Workspaces/dlw_semidiscrete/NONLINEAR_CLOSURE.md">非线性闭合与局部反向重构</a></li></ul>`;
const html='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW 可积结构复核</title><style>body{margin:0;background:#faf9f6;color:#242424;font-family:Georgia,"Noto Serif SC","Microsoft YaHei",serif;line-height:1.85}main{max-width:900px;margin:auto;padding:48px 24px 80px}h1{font-size:32px;line-height:1.4}h2{font-size:22px;margin-top:36px}.meta{color:#777;font-size:14px}.lead{font-size:19px;border-left:3px solid #61746a;padding-left:18px}table{border-collapse:collapse;width:100%;font-size:15px}td,th{padding:12px 10px;text-align:left;border-bottom:1px solid #d8d5cf;vertical-align:top}th{background:#efede7}.eq{overflow-x:auto;padding:12px 0}a{color:#365b73}math{font-size:1.08em}@media(max-width:600px){main{padding:24px 16px}h1{font-size:27px}td,th{padding:8px 5px;font-size:13px}.lead{font-size:17px}}</style><main>'+body+'</main></html>';
fs.mkdirSync(reportDir,{recursive:true});
fs.writeFileSync(path.join(reportDir,'dlw_integrability_status.html'),html);
