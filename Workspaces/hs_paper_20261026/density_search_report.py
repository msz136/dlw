from pathlib import Path
import json
import sympy as sp
ROOT=Path(__file__).resolve().parent;D=ROOT/'data/density_search'
read=lambda f:json.loads((D/f).read_text())
scan=read('scan.json');candidate=read('candidate.json');checks=read('candidate_checks.json');held=read('heldout.json')
w,r,u,wx,rx,c=sp.symbols('w r u wx rx c')
E=w*w-c*c*(r*r-1)
DE=2*w*(w*w/2+4*u+c*c*(r*r-1)/2)-2*c*c*r*r*w
assert sp.expand(DE-(w*E+8*u*w-2*c*c*w))==0
summary=[]
for d in candidate:
 b=next(x for x in scan if x['nodes']==d['nodes'] and x['p']==d['p'] and x['alpha']==0)
 gains={q:100*(1-d[q]/b[q]) for q in ['u','rho']}
 assert min(gains.values())>0
 for z in checks:
  if z['nodes']==d['nodes'] and z['p']==d['p']:
   assert z['u']<b['u'] and z['rho']<b['rho'] and z['min_h']>0 and z['min_monitor']>0
 summary.append(dict(nodes=d['nodes'],p=d['p'],fixed=b,candidate=d,gains=gains))
(D/'summary.json').write_text(json.dumps({'current_cases_all_improve':True,'energy_conservation_symbolic_check':True,'results':summary,'heldout':held},indent=2))
def table(rows,headers):
 return '<table><thead><tr>'+''.join('<th>'+x+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table>'
rows=[]
for d in summary:
 for q in ['u','rho']:
  rows.append([d['nodes'],'单孤子' if len(d['p'])==1 else '双孤子',q,f'{d["fixed"][q]:.7e}',f'{d["candidate"][q]:.7e}',f'{d["gains"][q]:.3f}%'])
hr=[]
for i in range(0,len(held),2):
 a,b=held[i:i+2];hr.append([str(a['p']),*[f'{100*(1-b[q]/a[q]):+.3f}%' for q in ['u','rho']]])
html='''<!doctype html><html lang="zh"><meta charset="utf-8"><title>2HS 守恒密度探索</title><style>body{max-width:1050px;margin:48px auto;padding:0 24px;font:17px/1.85 Georgia,"Microsoft YaHei",serif;color:#222}h1{font-size:29px}h2{font-size:23px;margin-top:36px}table{border-collapse:collapse;width:100%;font-size:14px;margin:24px 0;border-top:2px solid #333;border-bottom:2px solid #333}th,td{text-align:right;padding:8px 10px}th{border-bottom:1px solid #666}th:first-child,td:first-child{text-align:left}.eq{padding:16px;background:#f5f6f8;text-align:center}a{color:#28648c}</style><h1>2HS：守恒密度的选择与双场节点误差</h1>
<p>在当前单孤子 p=5 和双孤子 (1.1,1.25) 上，找到一个统一的候选密度，在200、1000、2000个实际节点下均使两场最大节点误差下降。单孤子收益约0.2%–0.4%，双孤子约7%–18%。这是由当前算例扫描得到的参数；另外三个未参与选择的参数测试显示，其优势具有波形依赖性。主论文暂保留原方案，本报告记录探索结果。</p>
<h2>1. 协议与误差来源</h2><p>物理区间[-4,4]，终点T=0.25，RK4时间步0.0005。同一非均匀三点FD、Poisson恢复、精确边界；200/1000/2000均为实际节点数。误差直接取各自最终节点在[-2.5,2.5]内的最大值，与同位置连续精确解比较，无场插值或平滑。初始节点由监视量累计积分反求，初始场直接用精确公式求值。</p>
<p>均匀网格集中到波区后，局部格距变小，但非均匀性也改变差分的首项误差。令相邻格距为h₋、h₊，三点二阶导数满足</p>
<div class="eq">D₂u − uₓₓ = (h₊−h₋)uₓₓₓ/3 + (h₋²−h₋h₊+h₊²)uₓₓₓₓ/12 + …</div>
<p>因此，缩小格距和控制格距变化同时重要。速度u通过全区间Poisson问题恢复，局部误差会被整体传递；ρ则通过局部输运和速度梯度耦合演化。单纯在波峰附近加密并不保证两场最大误差同时减小。</p>
<p>把Rₘ初始网格固定后，200节点单孤子u误差约4.589×10⁻⁶；持续运动时约4.536×10⁻⁶，均匀固定网格约3.081×10⁻⁶。这表明当前单孤子u的劣势已存在于非均匀布点及其差分中，不能全部归因于节点运动。该诊断分离了两种网格运动设置，但不构成误差首项的完整归因证明。</p>
<h2>2. 守恒密度的组合</h2><p>第一轮扫描R=1+α(Rₘ−1)，α=0.1、0.25、0.5、0.75、1，在三个节点数下均未得到四项同时改善。进一步使用能量型密度E=uₓ²−c²(ρ²−1)。由D=∂t−u∂x及原方程可得DE=uₓE+8uuₓ−2c²uₓ，因此</p>
<div class="eq">Eₜ+(Q<sub>E</sub>)ₓ=0，　Q<sub>E</sub>=−uE−4u²+2c²u。</div>
<p>与Rₘ=(uₓₓ+2)/(2ρ)、Qₘ=−uRₘ−c²(ρ−1)/2组合，得到</p>
<div class="eq">R=1+α(Rₘ−1)+βE，　Q=αQₘ+βQ<sub>E</sub>，　Rₜ+Qₓ=0，　V=Q/R。</div>
<p>当前候选取α=0.1、β=−0.07，且所有实验c=1。E和Rₘ的空间分布不同，组合使网格从单一波峰集中转为较温和的再分配。两个系数由数值扫描选择，不是理论最优值。守恒关系由代数成立；监视量的正性在这些算例中得到检查，并非对任意初值的正性定理。内节点按V运动，边界节点固定。</p>
<h2>3. 当前两个算例</h2>'''+table(rows,['节点数','算例','场','固定FD误差','候选动网格误差','下降比例'])+'''
<p>同一参数用于全部三个节点数，未按分辨率重新选参。时间步减半和构网积分采样加倍后，全部四项改善在三个节点数下均保留。单孤子的收益虽然可重复，但幅度小；双孤子的收益更明显。</p>
<h2>4. 固定参数后的其他波形</h2><p>参数冻结后，另取200节点测试p=4、p=6及双孤子(1.12,1.28)。表中正值表示误差下降，负值表示增大。</p>'''+table(hr,['参数','u误差下降','ρ误差下降'])+'''
<p>因此，该组合满足当前两个算例的四项改善目标，但尚未获得跨波形统一优势。适合的论文表述是研究守恒密度组合如何改变两场误差，并明确参数选择及适用算例。若将其作为通用网格推荐，还需要用更广泛的独立波形评价。</p>
<h2>5. 可复核数据</h2><p>全部扫描含不成功的配置均保存在<a href="../Workspaces/hs_paper_20261026/data/density_search/summary.json">汇总</a>及同目录的scan、energy_scan、mixed_scan、balance_scan、mild_scan、candidate、candidate_checks、heldout JSON文件中。实现入口为<a href="../Workspaces/hs_paper_20261026/density_search.py">density_search.py</a>；符号守恒核对和本报告由density_search_report.py生成。</p></html>'''
(ROOT.parent.parent/'report/hs_density_search_20261027.html').write_text(html,encoding='utf-8')
print('Report and checks saved; candidate improves all 12 current-case metrics.')
