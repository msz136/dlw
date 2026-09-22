"""Build a standalone Lean review document. Never compiles or proves Lean targets."""
from pathlib import Path
import hashlib, html, json, re, subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
REPORT=ROOT/'Paper/gsg_project/dlw_report'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def esc(s): return html.escape(str(s))
old_run=ROOT/'lean-toda/.lean-runs/20260919_121058_ca947c8e'
run=json.loads((old_run/'result.json').read_text(encoding='utf-8'))
old_log=(old_run/'build.log').read_text(encoding='utf-8')
old=[]
for f in run['files']:
    p=ROOT/'lean-toda/TodaFormalization'/Path(f['file']).name
    old.append(dict(file=str(p.relative_to(ROOT)).replace('\\','/'),name=p.name,
      recorded_sha256=f['sha256'],current_sha256=sha(p),matches=sha(p)==f['sha256'],
      historical_passed=f.get('passed',False),run=run['run_id']))
code=(HERE/'Contracts.lean').read_text(encoding='utf-8')
pattern=r'^def ([CN]\d{2}) : Prop :=[\s\S]*?(?=\n(?:def |/-)|\nend DLWContract)'
snips={m.group(1):m.group(0).rstrip() for m in re.finditer(pattern,code,re.M)}
items=[
('C01','连续第二式的真实导数桥','A','无','由 Bₐ(f,g)=0，把 DᵧBₐ−4Dₓ=0 化为 Bₐ(f,gᵧ)+2Dₓ=0。','不能仅假设两个无解释标量满足所需关系；必须证明乘积法则和混合导数交换。','DLW.six_iff_M1 / dy_reduction 只覆盖标量代数。'),
('C02','连续双线性 → 连续物理 DLW','A','C01','在联合光滑、正 τ 下，物理 u,v 满足 λ=−2 的连续两式。','cu/cv 与 c1/c2 必须保持实际导数定义；不覆盖任意 λ。','已证明（PkgC02.lean）。乘子只有 ±1：<code>c1 = 2·∂ₓ∂ᵧR</code>、<code>c2 = 2·∂ₓ∂ᵧR − 2·∂ₓS</code>；桥接式为 <code>cbil a f g = (f·g)·R</code>、<code>chx f g = (f·g)·Bₓ</code>、<code>2·cbil a f (sy g) = (f·g)·(E2 − 4Bₓ)</code>；<code>ContinuousPair</code> 经 <code>c02_hyp_from_ContinuousPair</code> 给出 <code>cbil a f g = 0 ∧ cbil a f (sy g) + 2·chx f g = 0</code>，于是 R=0、E2=0、S=0。<b>更正</b>：早期记录里把第二条标量假设写成 <code>E2 = β_y(S_xx+(D_x)²+D_t+2aD_x)+2B_x</code> 是错的（<code>β_y</code> 混用了 (x,t) 与 (x,y,t) 对象），文件 docstring 已逐字写出正确的 (I)(II) 并把旧式标为 WRONG；<code>cdybil − 4·chx = sy(cbil a f g) − 2(cbil a f (sy g) + 2·chx)</code> 是精确恒等式（λ=−2 为常数，余项是导数而非 R 的函数倍），所以 E+2Bₓ=0 是**推出**的，不是假设。'),
('C03','限定模板中的半格距参数','A','无','在指定二壁模板的全系数匹配和中心条件下，偏移只能是 ±h/2。','不能把“模板内唯一”扩展为所有可能离散化的唯一性。','wall_parameters / offset_gap_forced 等已有旧证明。'),
('C04','参数移位 = 格点移位：实际矩阵元','B','无','任意整数 n,j 的完整 Gram 矩阵元，在两种参数—格点组合下相等。','矩阵包含 δᵢₖ；整数负幂要求基底非零；不引入混合 y 相位。','staggered_entry_identity 已有 n=1 有理因子证明。'),
('C05','参数—格点恒等式提升到任意 N','B','C04','τₙ(j;a−h/2)=τₙ(j+n;a+h/2)，τ 是固定的 det(I+K)。','不能只证明任意两个已假定相等矩阵的行列式相等。','tau1_det_staggered 的矩阵未含完整 I+K，需接入新定义。'),
('C06','Gram 的导数和层更新','B','无','实际矩阵元的 x/t 导数、n→n+1 更新均等于固定显式表达式。','不是把 dx,dxx,dt 当自由变量的代数检查；求导要接到 exp。','本冻结端点已由所列证明包完成。'),
('C07','固定参数的任意 N 双线性链','B','C06','对实际 τ：Bₛ τₙ₊₁·τₙ=0，任意 N,n,j。','最终定理不能假设 Reservoir；若用逆矩阵，必须消除中途可逆性限制或明确缩小结论。','旧 T2 的 reservoir 是假设，本项是核心缺口。2026-09-22 用 fractions.Fraction（无浮点）在 N=1..4、j=0..2、n=0..2、三组参数上按实际指数向量合并检验，全部合并系数精确为 Fraction(0)：这些有限参数样例通过精确检查，<b>不构成任意 N 命题的证明</b>；任意 N 的完整行列式证明现已由 PkgC07Complete 验收。'),
('C08','离散双线性对的精确性','B','C05,C07','由已定义 F=τ₁(a−h/2)、G=τ₀ 得到两条真正的有限 h 方程。','是同一个 F 同时满足两壁；不是两份不相干 τ。','旧 T2 没有把 Res 与实际 bil/tau 接起来。'),
('C09','正参数区间的无零点与光滑性','B','Gram 定义','PositiveData 推出合法分母、F/G>0 和真实函数的联合光滑性。','任意 N；严格排序与振幅正性要留在假设中，不把正性当输入重复输出。','PkgC09Complete.lean 已完成完整 Lean 端点；原 PkgC09.lean 草稿保留但不导入。'),
('C10','两孤子归一化相互作用系数','B','Gram 定义','实际 N=2 行列式等于 1+e₀+e₁+A₁₂e₀e₁，A₁₂ 不含 h。','这还不是实际峰位的散射相移定理；后者需渐近分离和定位。','旧两指数代数材料不能直接替代本端点。'),
('C11','连续双线性 → 格点算子的二阶一致性','C','C01','二壁半和趋于 Bₐ，除 h 的差趋于 Bₐ(f,gᵧ)+2Dₓ；误差各 O(h²)。','取固定物理 y；对光滑函数的真实余项证明，不是截断多项式的 ring。','已证明（PkgC11.lean）。固定 y 令 Φ(s)=bil (a+s)(slice f y)(slice g (y+s))，两式共用同一次二阶 Taylor 展开：半和式误差 =(h²/8)Φ″(0)+(R(h/2)+R(−h/2))/2、半差式误差 =(R(h/2)−R(−h/2))/h，其中 R 是 PowBound 3 的 Taylor 余项（来自 PkgNumeric 的 powBound_taylor_poly）。bil 的 σ（斜对称）项在对称化中精确相消，因此无需单独的 bil 有界性。'),
('C12','格点对数速率的二阶误差','C','无','log λₕ(P)/h−1/P=O(h²)，P≠0。','旧 Tendsto 只给极限；还要补阶数与邻域分母控制。','lattice_rate_tendsto、centred_exact 已有证明。'),
('C13','归一化 Hirota 商恒等式','D','导数语义','B/(fg) 等于对数和的二阶导数、对数差的一阶项和平方项。','正 f,g、联合光滑不可删；平方项系数为 +1。','符号计算只作辅助；实际函数的冻结目标已由 Lean 证明。'),
('C14','双线性残差 → 非线性残差','D','C13','在不假设方程成立时，给出 N1/N2 与归一化 A,C 残差的精确恒等式。','此处最适合拦截符号/系数/位点错误；不能把 A=C=0 提前塞入本目标。','已证明（PkgNonlinear.lean，两个合取项都闭合，且不假设方程成立，故强于蕴含式）。路线：由 C13 的局部版本得 normA+normC=Φ+lxx Z、normA−normC=−lxx V+lx U·lx V+lt V+(2a)•lx V−h•lx U，再证 lt u+lx(H)=lx Φ、lxx(mm v−(h²/4)•lap(dm u))=dm h(lx(lxx Z))、lxx(d0 u+(h²/4)•lap W)=d0 h(lx(lxx Z))−(4/h)•lx(lxx V)、lt v=(4/h)•lx(lt V)+d0 h(lt u)，最后用 lxx/lx 交换与移位引理把两侧归约到同一批三阶 x-导数原子后 <code>ring</code>。此前 Agent 的手推在识别式 (2) 的最后两项符号上出过错（正确为 <code>+ (2a)•lx V − h•lx U</code>），已按 <code>Contracts.lean</code> 更正。'),
('C15','离散双线性 → 离散非线性','D','C14','同一正光滑 F,G 满足 SemiPair，推出 physU/physV 满足 NonlinearPair。','是正实全局版本的单向推论；不偷偷宣称周期全局等价。','已证明（PkgNonlinear.lean）。<code>SemiPair</code> 逐点给出 normA=normC=0（<code>zero_div</code>），于是 <code>lx 0=0</code>、<code>dm h 0=0</code>、<code>d0 h 0=0</code>，<code>c14_proved</code> 直接把两个分量压成 0。注意 C15 无法绕过 C14，故两者同时闭合。'),
('C16','Gram 解确实解非线性系统','D','C08,C09,C15','PositiveData 下，实际任意 N Gram 解经物理变换满足 N1/N2。','集成 theorem 的 type 不应再带“假设 N1/N2 成立”。','核心最终验收之一，现已完整证明。'),
('C17','交错观测位置与物理变换二阶极限','C','C13','离散物理场等于插值表达式在 F 位点的采样，并以二阶趋于连续 u/v。','先证精确位置对应，再证明渐近误差；不能把 G 与 F 当同点。','已证明（PkgC17.lean）：采样恒等式对所有 h 精确成立；两个 O(h²) 估计由一元 Taylor 余项的对称差给出，A′/B′ 项精确相消。'),
('C18','非线性格点方程的二阶一致性','C','差分算子与微积分','真实光滑场代入 N1/N2，分别对连续 c1(y−h/2)、c2(y) 的残差 O(h²)。','这是方程一致性，不是数值解收敛，也不是非线性稳定。','数学报告已有符号/Taylor 证据；Lean 待证。'),
('C19','局部守恒律','D','C15 可用于 Gram 实例','N1/N2 推出 W 与 v 的局部散度方程，通量 JW/JV 固定。','不能把逐点密度不变当作守恒律；积分版还需边界与微积分桥。','已由 PkgLattice.lean 的 c19_proved 完成。'),
('C20','周期求和只能给相容约束','D','差分求和','在周期格点上，N1/N2 推出 ∂ₓ²Σv=0。','这里没有 ūₜ；不能据此制造平均模态演化。','新验收目标。'),
('C21','平均模态自由度的明确见证','D','N1/N2 定义','任意光滑时间函数 c(t)，uⱼ=c(t),vⱼ=0 都满足系统。','用于拒绝没有基值条件却宣称唯一演化的数值实现。','新验收目标。'),
('C22','精确 Gram 物理场的紧盒一致二阶收敛','C','C09,C12,C17,C24','固定正则数据，在任意有界 x,y,t 盒上，有限 h 物理场与连续解误差 ≤C h²。','C 与 h 无关；须控制求导后的误差及 τ 的下界；单点相位极限不够。','已由解析延拓、奇偶性和紧集统一 Taylor 界完成；不是一般初值收敛定理。'),
('C23','连续 Gram 解接到连续起点','A','Gram 定义','固定连续 τ₁/τ₀ 真正满足 ContinuousPair。','禁止将原文事实当 Lean 公理；一般 N 的导数/行列式证明要补齐。','旧 N=1 代数残差只作辅助。'),
('C24','Gram 连续插值与整数格点完全一致','C','C09','带 offset=1/2 的 F 插值和 offset=0 的 G 插值采样后严格回到 F/G。','整数幂转 log/exp 需要 χ>0；不能忘记 F 的半格偏移。','新验收目标。'),
('C25','真实非线性系统的零背景线性化','D','N1/N2 与微积分','对扰动幅度 ε 求导，得到固定 linearN1/linearN2。','这是 Fourier 色散桥的前置；尚未证明模态增长式 (S)。','新验收目标。'),
('N01','Euler / RK4 / 梯形的一步缺陷阶','E','实际有限维光滑 ODE','Euler 缺陷 O(Δt²)、RK4 O(Δt⁵)、梯形方程残差 O(Δt³)。','不是直接得到全局 1/4/2 阶；边界驱动须纳入时变 RHS。','新目标；还需与实际 DLW x 离散的 RHS 连接。'),
('N02','有限步误差递推界','E','无','从 eₙ₊₁≤q eₙ+η 推出 qⁿe₀+ηΣqⁱ 上界。','算法实现者还必须证明实际一步稳定因子 q 与缺陷 η 的界；不能直接假定最终误差。','条件工具，不是 DLW 稳定性证明。'),
('N03','模型误差与求解误差分离','E','有限维范数','对连续参照的总误差 ≤ 数值对有限 h 的误差 + 有限 h 对连续解的误差。','两个参照必须在同一物理网格，两个分项各有证据。','基础工具目标。'),
('N04','有限样本数值误差证书','E','经证明的参考值区间','计算值、区间端点、阈值为有理数；真值有证明的包含关系，推出每个样本的误差界。','仅有 CSV 或小数打印不够；区间包住真值的证明不能缺失；仅有限样本。','证书规则目标；本轮没有实际数据证书。'),
('N05','开放链基值重构','E','无','从 p=δ₋u 和左端基值 b 重构，严格恢复差分与基值。','实际 b(x,t)、幽灵点与时间阶段的来源需在实现里另验。','基础重构目标。'),
('N06','正增长模态不会被准确积分消除','E','标量测试方程','g>0,Δt>0 时 Euler 放大因子与精确 exp 放大因子都大于 1。','不允许以“放大因子大于 1”单独判数值格式失败。','标量诊断，不是完整 Fourier 模态证明。'),
('N07','线性误差预算条件','E','正实 seed/tolerance','gT≤log(tolerance/seed) 推出 seed exp(gT)≤tolerance。','实际系统的 g、初始/每步误差 seed 需另证；不是非线性有效时间保证。','条件估计目标。'),
]
assert set(snips)=={r[0] for r in items}, (set(snips),len(items))

# --- Second pass, 2026-09-22: proofs actually implemented and verified through the
# --- standard entry.  Root: Workspaces/lean_contracts/proofs, module Main.lean.
PROOF_ROOT='Workspaces/lean_contracts/proofs'
PROVEN={
 'C22':('PkgC22Complete.lean','c22_proved','将实际 Gram 插值改写为正的偶解析延拓；u 的一阶误差导数为零，h·v 的误差前三阶 jet 为零。紧性给出统一步长和导数界，分别得到一致二阶/三阶余项，再除 h，严格完成任意固定物理盒上的 u/v 二阶界。'),
 'C23':('PkgC23Complete.lean','c23_proved','连续 y 流通过行列式换序接入 C07；在合法辅助参数曲线上对实际 γ 因子和行列式求导，得到 Bₐ(τ₁ᵧ,τ₀)=2Dₓ，再与第一式的 y 导数组合，完成两条 ContinuousPair 方程。'),
 'C07':('PkgC07Complete.lean','c07_proved','任意 N、整数层/格点的实际 Gram 双线性链。行列式一阶/二阶微分与秩一更新给出 Plücker 恒等式；用特征多项式有限根和连续性消除可逆性限制，再接实际矩阵元的 x/t 导数与分离因子。没有 Reservoir 前提。'),
 'C08':('PkgGramComplete.lean','c08_proved','将已证明的 C07 接入两壁移位桥，完成冻结的有限 h 双线性对。'),
 'C16':('PkgGramComplete.lean','c16_proved','使用真实 C08、C09 正性与 C15 物理变换，完成任意 N Gram 物理场解 N1/N2 的完整终点。'),
 'N01':('PkgRK4Complete.lean','n01_proved','Euler、一般非线性含时间依赖 RK4、梯形的一步缺陷阶全部完成。RK4 使用时间增广、真实四级导数与四阶 Taylor 多项式匹配，余项给出 PowBound 5；不等于实际求解器全局收敛或浮点程序认证。'),
 'C18':('PkgC18Complete.lean','c18_proved','真实非线性残差乘 h 后作光滑延拓，前 0/1/2 阶误差 jet 为零，三阶余项除 h 给出二阶一致性。第一式在 y−h/2 比较，第二式在 y 比较。'),
 'C09':('PkgC09Complete.lean','c09_proved','任意 N 的 Cauchy 主子式正性与 det(I+K) 展开；从 PositiveData 推出合法分母、F/G 严格正性及联合光滑性。'),
 'C01':('PkgContinuous.lean','c01_proved','含一条 Mathlib 原本没有的混合偏导交换引理（由 ContDiffAt.isSymmSndFDerivAt 与 fderiv/deriv 桥接搭出）。'),
 'C02':('PkgC02.lean','c02_proved','乘子只有 ±1：c1=2·∂ₓ∂ᵧR、c2=2·∂ₓ∂ᵧR−2·∂ₓS，R、S 由 ContinuousPair 逼零。旧记录里那条 E2=β_y(S_xx+(D_x)²+D_t+2aD_x)+2B_x 形式是错的（把 (x,t) 与 (x,y,t) 的对象混在一起），文件里已标明并给出正确的 (I)(II)。'),
 'C03':('PkgTrivial.lean','c03_proved',''),
 'C04':('PkgGramEntry.lean','c04_proved',''),
 'C05':('PkgGramEntry.lean','c05_proved',''),
 'C06':('PkgGramEntry.lean','c06_proved',''),
 'C10':('PkgGramEntry.lean','c10_proved',''),
 'C11':('PkgC11.lean','c11_proved','两式由同一次二阶 Taylor 展开给出：固定 y，令 Φ(s)=bil (a+s)(slice f y)(slice g (y+s))，则半和式误差 =(h²/8)Φ″(0)+(R(h/2)+R(−h/2))/2、半差式误差 =(R(h/2)−R(−h/2))/h，R 为 PowBound 3 的 Taylor 余项。复用了 PkgNumeric 的 powBound_taylor_poly。'),
 'C14':('PkgNonlinear.lean','c14_proved','两个合取项各自闭合：normA+normC 与 normA−normC 先降到格点 jet，再用 lxx/ lx 交换律与移位引理把两边归约到同一批原子，最后 ring（字段 h≠0）。不含方程假设，故比蕴含式更强。'),
 'C15':('PkgNonlinear.lean','c15_proved','SemiPair 逐点给出 normA=normC=0（zero_div），于是 lx 0=0、dm h 0=0、d0 h 0=0，c14_proved 直接把两个分量压成 0。'),
 'C12':('PkgQuotientRate.lean','c12_proved','显式常数 C=1/(2|P|³)、ε=|P|/2；走中值定理而不是浮点判零。'),
 'C17':('PkgC17.lean','c17_proved','第一个合取项是对所有 h（含 h=0）成立的<b>精确恒等式</b>：physU∘sample = sample∘interpU、physV∘sample = sample∘interpV，纯格点脚标算术、不需要任何分析。第二个合取项把两个误差都归约成一元 Taylor 余项的对称差：(interpU−cu) = −2·((R_B(h/2)+R_B(−h/2))/2) − (h²/4)·B″(y)；(interpV−cv) = (7/2)·(R_B(h/2)−R_B(−h/2))/h − (3/2)·(R_B(3h/2)−R_B(−3h/2))/(3h) + 2·(R_A(h)−R_A(−h))/(2h)，其中 B′ 项因 4−1/2−3/2−2=0、A′ 项因 2−2=0 精确相消。陷阱：interpV−cv 的恒等式在 h=0 处为<b>假</b>（Lean 的 /0=0），故只能走 c11_powBound_congr_ne 而非 powBound_congr。'),
 'C13':('PkgQuotientRate.lean','c13_proved',''),
 'C21':('PkgTrivial.lean','c21_proved',''),
 'C24':('PkgQuotientRate.lean','c24_proved','整数幂由 exp(j·log χ) 与 χ^j 在 χ>0 下互转。'),
 'C19':('PkgLattice.lean','c19_proved','守恒律由纯格点算子恒等式闭合；第二式是定义展开即得。'),
 'C20':('PkgLattice.lean','c20_proved','只用第一式；周期求和让差分项望远镜消去，剩下 ∂ₓ²Σv=0。'),
 'C25':('PkgLattice.lean','c25_proved','先把残差写成 ε·linear + ε²·quad，再对 ε 在 0 处求导。'),
 'N02':('PkgTrivial.lean','n02_proved',''),
 'N03':('PkgTrivial.lean','n03_proved',''),
 'N04':('PkgTrivial.lean','n04_proved',''),
 'N05':('PkgTrivial.lean','n05_proved',''),
 'N06':('PkgTrivial.lean','n06_proved',''),
 'N07':('PkgTrivial.lean','n07_proved',''),
}
UNPROVED=[r[0] for r in items if r[0] not in PROVEN]
PARTIAL={}


# A green card must be backed by a successful integrated run for these exact bytes.
proof_root=ROOT/PROOF_ROOT
candidates=[]
for rp in sorted((proof_root/'.lean-runs').glob('*/result.json'), reverse=True):
    rr=json.loads(rp.read_text(encoding='utf-8-sig'))
    if rr.get('status')=='PASSED' and Path(rr.get('target','')).name=='Main.lean':
        candidates.append((rp,rr))
assert candidates, 'No successful Main.lean run exists'
verified_path, verified_run=candidates[0]
verified_log=(verified_path.parent/'build.log').read_text(encoding='utf-8-sig')
verified_files={Path(f['file']).name:f for f in verified_run['files']}
for f in verified_run['files']:
    assert f['passed'] and f['exit_code']==0 and sha(Path(f['file']))==f['sha256'], \
        f"Integrated proof source changed since verification: {f['file']}"
assert sha(HERE/'Contracts.lean')==sha(proof_root/'Contracts.lean')==\
 'e70876c538d52939b030e7813a6b1c60917a79e56e28b29146d22df8da98d656'
allowed_axioms={'propext','Classical.choice','Quot.sound'}
for target,(file,theorem,_) in PROVEN.items():
    assert file in verified_files, f'{file} not in integrated check'
    source=(proof_root/file).read_text(encoding='utf-8')
    assert re.search(r'\btheorem\s+'+theorem+r'\s*:\s*'+target+r'\s*:=',source), target
    footprint=re.search(r"'DLWContract\."+theorem+r"' depends on axioms: \[([^\]]*)\]",verified_log)
    assert footprint, f'Missing axiom audit for {target}'
    assert set(x.strip() for x in footprint[1].split(',') if x.strip())<=allowed_axioms
run_id_log=verified_run['run_id']
module_count=len(verified_run['files'])
manifest={'date':'2026-09-22','contracts_sha256':sha(HERE/'Contracts.lean'),
 'typecheck':{'status':'PASSED','exit_code':0,
  'entry':"_lean_shared/Check-Lean.ps1 -Root Workspaces/lean_contracts/proofs -File .../Main.lean",
  'output':f'PASSED: {module_count} local module(s).',
  'run_id':run_id_log,'source_hashes_verified':True,
  'fixed':'runtime.json 的 workspace 与 lean_paths 已由旧 C:/Users/msz/学术内容 重指向 C:/Users/msz/aca（原文备份为 runtime.json.bak_pre_aca_migration）。此次修改只改路径，未改工具链、Mathlib 提交或任何证明语义。',
  'interface_revision':'2026-09-22 原始 Contracts.lean 在 PowBound 处写作 0<|h|，被 Lean 词法器读成 <| 管道算子，文件无法通过类型检查。已按 README 第 4 条提交最小词法差异 0 < |h|；数学内容不变。原字节备份在 Trash/lean_contracts_pre_syntax_fix_20260922/Contracts.lean.orig（SHA-256 40a624c2…）。',
  'note':'编译器返回 0 只表示证明项类型检查通过，不自动审计假设是否非空、是否就是目标。'},
 'historical_run':run['run_id'],'historical_modules':old,
 'proof_root':PROOF_ROOT,
 'verification_run':str(verified_path.relative_to(ROOT)).replace('\\','/'),
 'partial':PARTIAL,
 'conditional_bridges':{'C08':'c08_of_c07 : C07 → C08',
  'C16':'c16_of_c07 : C07 → C16 (uses proved C09)'},
 'proved_count':len(PROVEN),'unproved_count':len(UNPROVED),
 'proved':{k:{'file':v[0],'theorem':v[1],'note':v[2]} for k,v in PROVEN.items()},
 'contracts':[dict(id=r[0],title=r[1],owner=r[2],dependencies=r[3],
   status=('PROVED' if r[0] in PROVEN else 'PARTIAL' if r[0] in PARTIAL else 'UNPROVED'),
   evidence=(f'{PROVEN[r[0]][0]} :: {PROVEN[r[0]][1]}' if r[0] in PROVEN else None),
   claim=r[4],review=r[5],prior=r[6]) for r in items]}
(HERE/'status.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

rows=''.join(f'<tr><td><a href="{esc(f["file"])}">{esc(f["name"])}</a></td><td>{"哈希吻合；历史通过" if f["matches"] and f["historical_passed"] else "当前哈希不同；须复验"}</td><td><code>{esc(f["current_sha256"][:16])}…</code></td></tr>' for f in old)
cards=''
for id,title,owner,deps,claim,review,prior in items:
    if id in PROVEN:
        f,th,note=PROVEN[id]
        badge=f'<p class="badge verified">已证明 · <code>{esc(th)}</code> · {esc(f)}</p>'
        if note: badge+=f'<p class="muted">{esc(note)}</p>'
        state='proved'
    elif id in PARTIAL:
        badge=f'<p class="badge partial">部分证明 · 未完成</p><p class="muted">{PARTIAL[id]}</p>'
        state='partial'
    else:
        badge='<p class="badge pending">未证明</p>'
        state='pending'
    cards+=f'''<article class="contract" id="{id}" data-group="{owner}" data-state="{state}"><h3><span class="id">{id}</span> {esc(title)}</h3>{badge}<p><b>目标：</b>{esc(claim)}</p><p><b>验收重点：</b>{esc(review)}</p><p class="muted"><b>已有基础：</b>{esc(prior)}<br>负责包 {owner} · 前置：{esc(deps)}</p><details><summary>查看准确 Lean 命题</summary><pre><code>{esc(snips[id])}</code></pre></details></article>'''

proof_rows=''.join(
    f'<tr><td><code>{esc(i)}</code></td><td><a href="{esc(PROOF_ROOT)}/{esc(PROVEN[i][0])}">{esc(PROVEN[i][0])}</a></td>'
    f'<td><code>{esc(PROVEN[i][1])}</code></td><td>PASSED · 仅 propext / Classical.choice / Quot.sound</td></tr>'
    for i in sorted(PROVEN))
unproved_list='、'.join(UNPROVED) or '无'

page=r'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW Lean 证明状态与关键命题</title><style>@@KATEX_CSS@@</style><style>
:root{--ink:#172f43;--muted:#54616e;--rule:#d7dee4;--blue:#174e78}*{box-sizing:border-box}body{margin:0;background:#eef2f5;color:var(--ink);font:16px/1.8 "Microsoft YaHei",sans-serif}main{max-width:1120px;margin:30px auto;background:white;padding:48px 58px 72px}h1{font-size:32px;line-height:1.5}h2{font-size:24px;margin-top:44px;border-bottom:1px solid var(--rule);padding-bottom:10px}h3{font-size:19px}p{margin:10px 0}a{color:var(--blue);text-underline-offset:3px}header{border-bottom:3px solid var(--blue);padding-bottom:20px}.muted{color:var(--muted)}.callout{background:#edf3f8;border-left:4px solid var(--blue);padding:18px 22px;margin:24px 0}.warn{background:#fff6e9;border-color:#a26716}.stats{display:flex;gap:14px;flex-wrap:wrap;margin:24px 0}.stats div{flex:1;min-width:160px;border:1px solid var(--rule);padding:14px 18px}.stats strong{display:block;font-size:28px}.badge{display:inline-block;padding:3px 10px;border:1px solid;border-radius:4px;font-size:13px}.verified{color:#146045;background:#eef8f2}.pending{color:#835818;background:#fff7e9}.partial{color:#345c89;background:#edf3fc}nav ul{columns:2}.tablewrap{overflow:auto}table{width:100%;border-collapse:collapse;font-size:14px}td,th{border-bottom:1px solid var(--rule);padding:11px;text-align:left;vertical-align:top}th{background:#f1f4f7}.contract{border:1px solid var(--rule);padding:20px 24px;margin:20px 0;scroll-margin-top:16px}.contract h3{margin-top:0}.id{font-family:Consolas,monospace;color:var(--blue)}pre{overflow:auto;background:#132b3e;color:#edf3f8;padding:20px;font:14px/1.65 Consolas,monospace;tab-size:2}code{font-family:Consolas,monospace;overflow-wrap:anywhere}summary{cursor:pointer;color:var(--blue);padding:9px 0}.filters{display:flex;gap:14px;align-items:end;flex-wrap:wrap;padding:18px;background:#f1f5f8;margin-top:22px}.filters label{display:block}.filters input,.filters select{font:inherit;padding:8px;max-width:100%;border:1px solid #8b9ba7}.flow{padding:18px;border:1px solid var(--rule);line-height:2.2}.katex-display{overflow:auto;padding:5px 0}a:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid #b87b28;outline-offset:3px}footer{border-top:1px solid var(--rule);margin-top:36px;padding-top:20px;font-size:14px}[hidden]{display:none!important}@media(max-width:700px){main{margin:0;padding:24px 18px}h1{font-size:26px}nav ul{columns:1}.contract{padding:16px}table{min-width:640px}.filters{display:block}.filters label{margin:10px 0}.stats div{min-width:130px}}@media print{main{margin:0;padding:0;max-width:none}body{background:white}.filters{display:none}.contract{break-inside:avoid}h2,h3{break-after:avoid}}
</style></head><body><main>
<header><p class="muted">独立核验页 · 2026-09-22 · <a href="index.html">数学主报告</a> · <a href="numerical_analysis.html">数值分析方案</a> · <a href="AGENTS.md">项目索引</a></p><h1>DLW 的 Lean 证明状态<br>关键命题、依赖关系与 Agent 验收</h1><p>这一页把关键结论的起点、终点和证明状态说清楚。本轮已先修复环境迁移导致的验证障碍、让 32 个命题通过类型检查，然后逐包实现证明：<b>@@PROVEDCOUNT@@ 项已由标准入口 PASSED 并附 <code>#print axioms</code> 证据</b>。冻结的 32 个目标已全部完成；接口之外的研究任务另列，不计入完成率。</p></header>
<div class="stats"><div><strong>@@PROVEDCOUNT@@ / 32</strong>已证明并通过标准入口</div><div><strong>@@UNPROVEDCOUNT@@</strong>仍未证明</div><div><strong>@@MATCHES@@ / 7</strong>旧模块与通过日志哈希吻合</div><div><strong>0</strong>新增公理 · 0 sorry</div></div>
<div class="callout"><b>验收原则：</b>先固定实际数学对象及目标命题，再让 Agent 证明，最后由 Lean 检查完整证明、由负责人核对目标与假设。负责人可以不手推所有中间计算，但不能只看定理名称或“编译通过”。<code>def C15 : Prop := …</code> 只是把任务写成命题；只有构造出类型为 <code>C15</code> 的证明，并通过完整依赖检查，才算完成。</div>
<nav aria-label="目录"><ul><li><a href="#status">1. 哪些已被证明，哪些没有</a></li><li><a href="#route">2. 两条数学链与验收边界</a></li><li><a href="#definitions">3. 共享定义与真实语义</a></li><li><a href="#targets">4. 32 个可交接命题</a></li><li><a href="#numerics">5. 数值分析如何在 Lean 上验收</a></li><li><a href="#agents">6. Agent 分工与验收程序</a></li><li><a href="#extensions">7. 仍需设计接口的扩展</a></li><li><a href="#files">8. 文件、证据与环境状态</a></li></ul></nav>

<h2 id="status">1. 已有证明与未证明部分</h2>
<p><span class="badge verified">历史通过，哈希核对</span> 指旧模块存在标准入口 PASSED 日志，且当前源码哈希与记录相同。<span class="badge partial">只覆盖辅助/条件引理</span> 指证明成立，但范围小于新的最终结论。<span class="badge pending">未证明</span> 指目标尚无完整 Lean 证明。32 个接口均已类型检查；有目标定义不等于有目标证明。</p>
<p>已读取并核对 <a href="lean-toda/.lean-runs/20260919_121058_ca947c8e/result.json">2026-09-19 的 result.json</a> 与 <a href="lean-toda/.lean-runs/20260919_121058_ca947c8e/build.log">build.log</a>。日志中关键定理的逻辑依赖只有标准 <code>propext / Classical.choice / Quot.sound</code>。这是旧版本的通过记录，不是本轮复跑；源码吻合情况如下。</p>
<div class="tablewrap"><table><thead><tr><th>旧模块</th><th>证据状态</th><th>当前 SHA-256 前缀</th></tr></thead><tbody>@@OLD_ROWS@@</tbody></table></div>
<div class="tablewrap"><table><caption>已证明内容的真实范围</caption><thead><tr><th>已有定理</th><th>可以算作 Lean 已证明</th><th>还不能算作已证明</th></tr></thead><tbody>
<tr><td>discretePair_iff_centred；wall_parameters</td><td>两个标量方程与中心组合的等价；给定匹配条件下的偏移代数。</td><td>任意连续解经过采样就成为有限 h 精确离散解；所有离散化唯一。</td></tr>
<tr><td>staggered_entry_identity；tau1_det_staggered</td><td>有理因子的 n=1 格点移位与行列式提升。</td><td>最新完整 det(I+K) 的任意整数层、真实 x/t 导数和任意 N 双线性链。</td></tr>
<tr><td>T2_discrete_pair_exact</td><td>在 Reservoir Res 假设下，取出两点的 Res=0，并附加矩阵恒等式。</td><td>实际 Gram 函数的双线性残差恒零；Res 与 τ、Hirota 导数未在该 theorem type 中连接。</td></tr>
<tr><td>taylor_jet3/4_isBigO；symmetric/antisymmetric_remainder_isBigO</td><td>真实 C⁴/C⁵ 槽函数的 Taylor 余项和中心组合误差。</td><td>自动完成具体 DLW 的槽函数光滑性、求导桥、非线性观测或紧集一致误差。</td></tr>
<tr><td>lattice_rate_tendsto；lattice_rate_centred_exact</td><td>log λ/h→1/P；Cayley 中心比率的精确代数。</td><td>整个 Gram 物理场及求解器二阶收敛；C12 还要求明确二阶界。</td></tr>
<tr><td>OneSoliton / Semidiscrete 早期检查</td><td>对应旧模板的代数展开、具体参数和有限指数关系。</td><td>不经方程版本核对就复用于最新 N1/N2。</td></tr>
</tbody></table></div>
<div class="callout warn"><b>旧 T2 的核心缺口：</b>其参数中有 <code>Res : ℝ → ℤ → ℝ</code> 和 <code>hres : ∀ s j, Res s j = 0</code>。这不是 Lean 证明错误，而是结论的适用范围有限。新 C07/C08 不接收这个任意残差或“已满足双线性链”的假设，必须对固定的真实行列式证明。</div>

<h2 id="route">2. 从连续到离散，再到非线性</h2>
<p>连续起点明确为 $B_a f\cdot g=0$、$(D_y B_a-4D_x)f\cdot g=0$，$B_a=D_x^2+D_t+2aD_x$，对应 $\lambda=-2$。这里“从连续系统推导离散系统”是一项<b>结构保持构造</b>：选择交错模板、匹配连续极限、构造格点 Gram 解，再证明有限 h 精确性；不是从连续 PDE 单靠逻辑就能推出某个唯一差分方程。</p>
<div class="flow"><b>构造链：</b>C01/C23 连续双线性与连续 Gram → C03 模板匹配 → C04–C06 参数移位与真实矩阵 → C07 任意 N 链 → C08 有限 h 双线性对。<br><b>回归链：</b>C11/C12 算子与速率极限；C24 插值对应 → C17 物理位置与变换 → C22 紧集上的精确解族极限。<br><b>非线性链：</b>C13 商恒等式 → C14 两条残差身份式 → C15 解映射；C08+C09+C15 → C16 任意 N 非线性精确解。<br><b>数值链：</b>C18 一致性、C20/C21 平均模态约束、N05 开链重构 → 实际有限维求解器 → N01/N02 误差控制 → N03 分项组合 → N04 实验样本证书。</div>
<p>关键终点是 C08、C16、C22。Agent 可以自由选择中间引理和证明方法，但不能改变这些目标背后的定义。C14 特意保留非零残差：它能把任意正光滑输入的双线性残差转换成非线性残差，比只在 A=C=0 时验算更能检查系数和格点错位。</p>
$$N_1=\delta_-\partial_x(A+C),\qquad N_2=\delta_0\partial_x(A+C)+\frac4h\partial_x(A-C).$$
<p>这里 $A=B_{a-h/2}F_j\cdot G_j/(F_jG_j)$、$C=B_{a+h/2}F_j\cdot G_{j+1}/(F_jG_{j+1})$。A=C=0 之后才推出 N1=N2=0。</p>

<div class="callout"><b>本轮新闭合与仍有条件的连接：</b>
<code>c09_proved : C09</code> 已证明任意 N 的正性、合法性和光滑性。
<code>c08_of_c07 : C07 → C08</code> 与 <code>c16_of_c07 : C07 → C16</code>
为此前的条件桥；现在真实 <code>c07_proved</code> 已通过，<code>c08_proved : C08</code> 与 <code>c16_proved : C16</code> 也已完整验收。C22 的紧盒一致误差和 C23 的连续 Gram 方程也已完整验收。
完整验收路线与剩余目标见 <a href="Paper/dlw_semidiscrete/lean_contracts/INTEGRATION_STATUS.md">系统—数值—Lean 衔接记录</a>。</div>

<h2 id="definitions">3. 共享定义必须接到真正的数学对象</h2>
<p>首轮接口采用全局光滑正实 τ，以避免把局部对数分支、边界积分规范和复谱问题混入基本消元。它是一般非零局部版本的充分子范围，不宣称已经覆盖所有奇点、复参数或周期重构。冻结代码使用 <code>ContDiff ℝ ⊤</code>；当前 Mathlib 的阶数类型是 ℕ∞ω，⊤ 为解析阶 ω，强于通常的 C∞。此前将它解释为仅需 C∞ 不准确。保持冻结命题不变，降低到最小正则性须另立目标。</p>
<ul><li><code>XT</code> 的顺序是 x,t；<code>XYT</code> 是 x,y,t；<code>Lattice</code> 是整数 j 后接 x,t。</li><li><code>dx/dt/sx/sy/st</code> 使用 Mathlib 的真实 <code>deriv</code>；联合光滑假设使求导、乘积法则与交换导数具有意义。</li><li><code>entry/tau</code> 固定为完整的 $\delta_{ik}+K_{ik}$ 与 <code>Matrix.det</code>，不是自由残差或缺少单位矩阵的替代模型。</li><li><code>Admissible/LayerOK</code> 明确排除分母及整数负幂的零基底；<code>PositiveData</code> 则要求有序正参数区间并由 C09 推出合法性。</li><li><code>physU/physV</code> 和 <code>n1/n2</code> 直接写成最新报告的函数。F/G 的位置由 <code>sampleF/sampleG</code> 固定；C18 中 N1 在 y−h/2，N2 在 y。</li><li><code>PowBound</code> 是存在 C,ε 的真实不等式；C22 使用更强的 <code>UniformBoxO2</code>，不能以单点界代替。</li></ul>
<p>所有定义与命题完整展开在下方，不依赖不可见的“正确算子”黑箱。<a href="Paper/dlw_semidiscrete/lean_contracts/Contracts.lean">下载命题源</a>。当前 SHA-256：<code>@@HASH@@</code>。</p>
<details><summary>查看完整 Lean 定义和全部命题（没有中间证明）</summary><pre><code>@@ALL_CODE@@</code></pre></details>

<h2 id="targets">4. 关键结论的 Lean 命题与状态</h2>
<p>下列都是<b>新的最终接口</b>。带绿色徽章的项目已由 <code>@@PROOFROOT@@/Main.lean</code> 经标准入口整体 PASSED，并有 <code>#print axioms</code> 证据；橙色徽章的仍无完整 Lean 证明。证明人交付的必须是类型为该编号的 theorem，而不是只交付本文件编译通过。所有代码块为实际源文件的同步摘录。</p>
<div class="callout"><b>本轮已证明的 @@PROVEDCOUNT@@ 项（标准入口 PASSED，退出码 0，run <code>@@RUNID@@</code>）：</b>
<div class="tablewrap"><table><thead><tr><th>编号</th><th>证明文件</th><th>导出定理名</th><th>逻辑依赖</th></tr></thead><tbody>@@PROOF_ROWS@@</tbody></table></div>
<p class="muted">整链由 <code>Workspaces/lean_contracts/proofs/Main.lean</code> 一次性导入全部已验收证明包，并逐个 <code>#print axioms</code>；每个目标都只依赖 <code>propext / Classical.choice / Quot.sound</code>，无 <code>sorryAx</code>、无新增公理。冻结的 <code>Contracts.lean</code> 未被任何证明包修改。</p></div>
<p><b>冻结目标中仍未证明的 @@UNPROVEDCOUNT@@ 项：</b>@@UNPROVED_LIST@@。每张卡片列出实际验收状态。连续 Gram 和一致极限的关键推导详见 <a href="Paper/dlw_semidiscrete/lean_contracts/C22_C23_PROOF_NOTES.md">C22/C23 证明结构</a>。</p>
<p class="muted">另有两条工程性提醒留给后续接手者（由本轮实际踩到）：① 未标注类型的 <code>4 • x</code> 在 Lean 里按 <b>ℕ</b> 标量乘法解析，与 <code>(4:ℝ) • x</code> 不 definitional 相等，必须写成 <code>(4 : ℝ) • x</code>；② 某个 tactic 已关闭目标后再接一个 tactic 会硬报错 <code>No goals to be solved</code>，不是警告。</p>
<div class="filters"><label>查找命题或关键词<br><input id="search" type="search" placeholder="例如 C14、Gram、平均模态"></label><label>按任务包筛选<br><select id="group"><option value="all">所有任务包</option><option value="A">A 连续与语义</option><option value="B">B Gram 精确性</option><option value="C">C 分析与极限</option><option value="D">D 非线性桥</option><option value="E">E 数值方法</option></select></label><span id="count" aria-live="polite">32 项</span></div>
@@CARDS@@

<h2 id="numerics">5. 数值分析怎样在 Lean 上验收</h2>
<p>本节是原数值方案的 Lean 补充，<b>原两份 HTML 不作修改</b>。这里的证明验收分三层：方程/基准是否正确；实际算法对目标有限维方程是否有误差界；本次输出是否有可核验的误差证书。三层缺一时，状态只能写到已完成的那一层。</p>
<div class="tablewrap"><table><thead><tr><th>数值任务</th><th>对应 Lean 验收</th><th>不能省略的桥</th></tr></thead><tbody>
<tr><td>E0 双线性/物理残差</td><td>C07,C08,C14,C16；输出样本可接 N04。</td><td>证明器中的实际 τ 与数值求值公式对应；高精度浮点小量不是恒等式。</td></tr>
<tr><td>E1 h 连续极限</td><td>C22+C24，必要时 C17；紧盒一致 O(h²)。</td><td>固定物理区域、半格位置、统一参数；导数和正分母界。</td></tr>
<tr><td>E2/E3 数值推进与加密</td><td>N05 边界重构；N01 一步阶数；N02 在实际 q,η 上实例化；N03 分误差。</td><td>具体 x 算子、边界闭合、求解器实现与 RHS 的一致性；稳定常数不随步数变化，且明示其 h/Δx 依赖。</td></tr>
<tr><td>E4 两孤子相移</td><td>C10 只能证明相互作用系数；C16 给精确解。</td><td>渐近分離、峰/相位定位、有限时间偏差仍需新接口，不能把 log A 写出就宣布实测相移获证。</td></tr>
<tr><td>E5 守恒</td><td>C19 局部散度；积分与离散求积版单独证明。</td><td>端点通量、时间积分、求积误差、浮点漂移；普通 RK 不保证机器零。</td></tr>
<tr><td>E6 高频增长</td><td>C25 真实线性化；N06/N07 仅提供标量诊断与预算。</td><td>Fourier 模态代入→色散式(S)→增长率的桥还未写成完成接口；不能预设 (S) 就称已从 PDE 证明。</td></tr>
<tr><td>E7 常规差分对照</td><td>每种格式分别证明一致性、边界和误差界，再统一参照/成本。</td><td>不能拿本格式的证明直接给另一格式认证；尚需那套实际算子定义。</td></tr>
</tbody></table></div>
<p><b>N01 与 N02 的连接要求：</b>对给定有限维、已闭合初边值问题，令 $q=1+L\Delta t$，证明一步缺陷 $\eta\le C\Delta t^{p+1}+\eta_{\rm solve}+\eta_{\rm round}$，并对计算与参照实际轨道证明一步放大界。才可使用</p>
$$e_n\le q^n e_0+\eta\sum_{i=0}^{n-1}q^i.$$
<p>这个不等式可得固定有限维模型上的全局时间误差估计。随着 x 分辨率增大，L 可能因真实高频增长而增大；不能偷换成连续 DLW 的无条件稳定/收敛结论。隐式法还要证明根的选取、迭代误差，不能只证明理想梯形残差。</p>
<p><b>N04 的证书边界：</b>把输出的二进制浮点值按其准确有理数值读入，证明参考量处于有理区间，再检查每个样本误差阈值。若要扩展到整个 x,y 域，需要额外的插值/导数界。Gram/exp/log 区间求值也必须有包含真值的证明，不能把 Python 给出的区间直接当作假设后宣布整次计算已获证。</p>
<p>数值实现与实验已运行，四项复审修正已有 <b>40 项回归和 17 项产物检查</b>。见 <a href="Paper/dlw_semidiscrete/numerics/REPORT.md">数值结果报告</a>、<a href="Workspaces/numerics_review_20260922/RESOLUTION.md">修复验收</a>及 <a href="Paper/dlw_semidiscrete/numerics/out/final_validation_manifest.json">运行证据与哈希</a>。E6 已改用实际开链线性化，检验 RHS 导数、本征模增长和形状；E1 固定窗口与端点权重已修；E5 格点和初始时刻已修；E7 实时执行当前代码得接近四阶。<b>这些是数值验收，不是 N04 区间证书，也不是全部求解器已被 Lean 认证。</b>E2/E3 已补齐六组同网格时间自收敛，支持当前算例下 Euler/RK4/梯形的 1/4/2 阶；30 次推进均完成。求解器两孤子散射、非线性长期稳定仍未验收。</p>

<h2 id="agents">6. 派工与验收程序</h2>
<div class="tablewrap"><table><thead><tr><th>包</th><th>任务</th><th>前置与交付</th></tr></thead><tbody>
<tr><td>A</td><td>C01,C02,C03,C23</td><td>冻结共享定义后开始；连续真实函数语义、模板匹配及连续 Gram。</td></tr>
<tr><td>B</td><td>C04–C10</td><td>C06→C07，C04→C05，二者合成 C08；正性 C09 独立收口。</td></tr>
<tr><td>C</td><td>C11,C12,C17,C18,C22,C24</td><td>通用余项可复用旧证明；C22 依赖 C09/C24 并控制求导误差。</td></tr>
<tr><td>D</td><td>C13–C16,C19–C21,C25</td><td>先证明残差身份式；C16 必须导入 B 的真实结果，不重复假设。</td></tr>
<tr><td>E</td><td>N01–N07</td><td>先完成有限维数值基础；实际 DLW 求解器实例化另作验收里程碑。</td></tr>
<tr><td>F / 负责人</td><td>最终组合、证据与状态更新</td><td>统一 definitions 哈希，检查 theorem type、假设非空和逻辑依赖；复跑完整导入链。</td></tr>
</tbody></table></div>
<ol><li><b>接口检查：</b>先处理环境迁移，再检查 Contracts.lean 的类型。必要的接口修订由负责人逐项审查，不允许实现 Agent 私自削弱结论。</li><li><b>版本固定：</b>记录共享定义 SHA-256。每个 Agent 用一致快照；最终整合导入单一权威模块。</li><li><b>证明交付：</b>独立工作目录、完整 theorem、实际依赖、证明日志；保留模型和假设解释。</li><li><b>双重验收：</b>Lean 检查证明项；负责人核对命题是否就是目标、假设是否不包含待证结论、是否对应最新方程。不可只看名字。</li><li><b>证据入表：</b>只有返回 0 且 PASSED，所有本地依赖哈希吻合，且 <code>#print axioms</code> 合格后，才把该目标由“待证”改为“已验证”。</li></ol>
<p>不需要逐行手推 tactic 细节，但应抽查关键中间引理的<strong>陈述</strong>：是否丢失非零分母、把函数导数当自由变量、遗漏单位矩阵、交换 F/G、改变 h 极限位置，或把有限样例升级为任意 N。至少验证一个非退化合法参数实例，防止所有假设合在一起不可能成立。</p>
<p>例如 C16 的最终 type 必须是 <code>DLWContract.C16</code>，而不是“若 Gram 已经满足 N1/N2，则 Gram 满足 N1/N2”。对不成立的加强版，交反例和范围更正，不能通过修改定义制造成功。完整交接要求见 <a href="Paper/dlw_semidiscrete/lean_contracts/README.md">Agent 交接与验收说明</a>。</p>

<h2 id="extensions">7. 尚需单独设计接口的扩展</h2>
<p>为了不把未明确的假设藏在 Lean 名称里，下列工作标为<b>接口待定、未证明</b>，不放进上述 32 项完成率。首轮主链不以完成它们为前提：</p>
<ul><li><b>非线性 → τ 的局部反向重构：</b>要固定开链/局部矩形、积分常数和规范，并使用局部导数语义；不能用全局正解析接口冒充一般局部可逆定理。</li><li><b>谱/Darboux、复参数和 IST：</b>项目有精确构造与数学证据，但一般 IST 尚未建立。后续需固定复函数、谱参数、边界和规范，分别定义已知谱关系；不能从旧无谱矩阵定理推出全系统不可积。</li><li><b>色散关系和高频增长：</b>C25 只走到真实线性化。还需复 Fourier 模态与格点算子符号的桥、非零 Kₕ 条件及零模处理、实际特征根增长率。</li><li><b>相移与积分守恒：</b>C10/C19 分别给系数/局部身份式；渐近定位与积分边界是新的分析任务。</li><li><b>实际计算程序认证：</b>选定 x 算子、边界、平均模态条件、时间算法与浮点模型后，才能冻结求解器专属 Lean 目标。当前通用 N01–N07 不是全部程序正确性。</li></ul>

<h2 id="files">8. 文件与当前验证障碍</h2>
<div class="callout"><b>验证障碍已排除，新接口已类型检查通过。</b>2026-09-22 实际执行项目唯一允许的 <code>_lean_shared/Check-Lean.ps1</code>（<code>-Root Workspaces/lean_contracts/proofs -File .../Main.lean</code>），返回码 <b>0</b>，输出 <code>PASSED: @@MODULECOUNT@@ local module(s).</code>（run <code>@@RUNID@@</code>）。两处障碍及处置：<br>
① <code>runtime.json</code> 的 <code>workspace</code> 与 10 条 <code>lean_paths</code> 仍指向迁移前 <code>C:\Users\msz\学术内容</code>，入口在编译前即以 <code>Root must be a dedicated subdirectory of the academic workspace, not the workspace itself.</code> 退出。已只改路径重指向 <code>C:\Users\msz\aca</code>，原文备份 <code>runtime.json.bak_pre_aca_migration</code>；未改工具链、Mathlib 提交或任何证明语义。<br>
② <code>Contracts.lean</code> 中 <code>PowBound</code> 的 <code>0<|h|</code> 被 Lean 词法器读成 <code>&lt;|</code> 管道算子，报 <code>Function expected at 0</code> 与 <code>unexpected token '|'</code>，文件根本无法进入类型检查。已按交接约定提交<b>最小词法差异</b> <code>0 &lt; |h|</code>（仅加空格，数学内容不变），并记录为需负责人复核的接口差异。</div>
<p>因此本页的状态是<b>已验证</b>与<b>未证明</b>两类，而不是“草案待检查”。已证明项的证据是：标准入口 PASSED 日志 + 冻结定义 SHA-256 + 逐目标 <code>#print axioms</code>。32 个冻结目标均有完整证明；第 7 节列出的扩展仍未证明，不以完成率掩盖。</p>
<ul><li><a href="Paper/dlw_semidiscrete/lean_contracts/Contracts.lean">完整 Lean 命题与共享定义</a></li><li><a href="Paper/dlw_semidiscrete/lean_contracts/status.json">状态、依赖、旧日志哈希和验证障碍</a></li><li><a href="Paper/dlw_semidiscrete/lean_contracts/README.md">给后续 Agent 的交接说明</a></li><li><a href="Paper/dlw_semidiscrete/NONLINEAR_CLOSURE.md">非线性闭合权威报告</a> · <a href="Paper/dlw_semidiscrete/GRAM_INTEGRABILITY_REASSESSMENT.md">Gram 最新复核</a> · <a href="Paper/dlw_semidiscrete/S_INTEGRABILITY_STATUS.md">谱与 S 可积性状态</a></li></ul>
<footer>独立页面源：<code>Paper/gsg_project/dlw_report/_src/lean_verification.src.html</code>。内容由 <code>Paper/dlw_semidiscrete/lean_contracts/build_dashboard.py</code> 同步命题与状态，复用本地 KaTeX 构建链。页面、公式、字体均可离线显示；文件链接需项目相对位置保持。原 <code>index.html</code> 与 <code>numerical_analysis.html</code> 本轮不修改。</footer>
</main><script>@@KATEX_JS@@</script><script>
document.addEventListener('DOMContentLoaded',function(){renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false});const search=document.getElementById('search'),group=document.getElementById('group'),cards=[...document.querySelectorAll('.contract')];function filter(){const q=search.value.toLocaleLowerCase();let n=0;cards.forEach(c=>{const show=(group.value==='all'||c.dataset.group===group.value)&&c.textContent.toLocaleLowerCase().includes(q);c.hidden=!show;if(show)n++;});document.getElementById('count').textContent=n+' / '+cards.length+' 项';}search.addEventListener('input',filter);group.addEventListener('change',filter);});
</script></body></html>'''
for a,b in {'@@MODULECOUNT@@':str(module_count),'@@MATCHES@@':str(sum(f['matches'] and f['historical_passed'] for f in old)),
 '@@OLD_ROWS@@':rows,'@@HASH@@':manifest['contracts_sha256'],'@@ALL_CODE@@':esc(code),'@@CARDS@@':cards,
 '@@PROOFROOT@@':PROOF_ROOT,'@@PROOF_ROWS@@':proof_rows,'@@RUNID@@':run_id_log,
 '@@PROVEDCOUNT@@':str(len(PROVEN)),'@@UNPROVEDCOUNT@@':str(len(UNPROVED)),
 '@@UNPROVED_LIST@@':esc(unproved_list)}.items(): page=page.replace(a,b)
assert '@@PROOF' not in page and '@@UNPROVED' not in page and '@@RUNID@@' not in page, \
 'unsubstituted placeholder remains (KATEX_CSS/KATEX_JS are filled later by build_html.ps1)'
src=REPORT/'_src/lean_verification.src.html'
src.write_text(page,encoding='utf-8')
protected=[ROOT/'index.html',ROOT/'numerical_analysis.html',REPORT/'_src/index.src.html',REPORT/'_src/numerical_analysis.src.html']
before={str(p):sha(p) for p in protected}
subprocess.run(['pwsh','-File',str(REPORT/'build_html.ps1'),'-SourceFile','_src/lean_verification.src.html','-OutputFile','lean_verification.html'],check=True)
assert before=={str(p):sha(p) for p in protected}, 'Existing report changed unexpectedly'
print(json.dumps({'new_contracts':len(items),'old_hash_matches':sum(f['matches'] for f in old),'existing_reports_unchanged':True},ensure_ascii=False))
