from pathlib import Path
import re
p=Path('review/revised.md'); s=p.read_text(encoding='utf8')
s=s.replace('Proposition 2.10','Proposition 2.9').replace('命题 2.10','命题 2.9').replace('Theorem 2.9','Theorem 2.10').replace('定理 2.9','定理 2.10')
for a,b in [
(' Substituting these fields into the PE equations gives $\\dot P=F_P$ and $\\dot W=F_W$, with',''),
('将重构的物理场代入 PE 方程，得到 $\\dot P=F_P$、$\\dot W=F_W$，其中',''),
(' With m determined, the evolution equations are $\\dot Q_j=F_{Q,j}$ and $\\dot R_j=F_{R,j}$, where',''),
('确定 m 后，演化方程为 $\\dot Q_j=F_{Q,j}$、$\\dot R_j=F_{R,j}$，其中',''),
]: s=s.replace(a,b)
# Relocate the PF initialization algebra while keeping the actual boundary choice in the body.
for l,start,end,short in [
('en','For PF, Q is determined','**Computational settings', 'PF uses the same continuous physical data, with Q normalized at the left x node; its reconstruction and lower-boundary initialization are specified in Appendix D.\n\n'),
('zh','对于 PF，由','**计算设置', 'PF 采用同一连续物理初边值，并在最左 x 节点归一化 Q；重构及下边界初始化见附录 D。\n\n')]:
 a=s.index(start);b=s.index(end,a);block=s[a:b].strip();s=s[:a]+short+s[b:]
 i=s.index('{#'+l+'-app-d}')+len('{#'+l+'-app-d}');s=s[:i]+'\n\n'+block+s[i:]
# Explicitly retain physical boundary rules and distinguish compute and observation domains.
for marker,text in [
('The experiments use fixed grids', 'The corresponding computational domains are $[-10,10]^2$, $[-20,20]^2$, $[-40,40]^2$ and $[-40,40]^2$. PE and FD use periodic x continuation; PF uses the prescribed additive jumps of Q and R. Lower y data and u ghost values are supplied by the continuous exact solution. All methods use the same computational and evaluation regions.\n\n'),
('实验中分别设置固定网格', '相应计算域依次为 $[-10,10]^2$、$[-20,20]^2$、$[-40,40]^2$ 和 $[-40,40]^2$。PE 与 FD 在 x 方向周期延拓，PF 对 Q、R 采用给定的加性跳跃；y 下边界数据和 u 的幽灵层值由连续精确解给定。各方法使用相同的计算域和评价区域。\n\n')]:
 i=s.index(marker);s=s[:i]+text+s[i:]
# Appendix labels keep main-text tables/figures in reading order without changing results.
s=s.replace('Table 2','Table F1').replace('Figure 5','Figure F1').replace('表 2','表 F1').replace('图 5','图 F1')
s=s.replace('Table 3','Table 2').replace('Figure 6','Figure 5').replace('表 3','表 2').replace('图 6','图 5')
p.write_text(s,encoding='utf8')
print('polished',len(s))
