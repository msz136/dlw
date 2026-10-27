from pathlib import Path
import re,json,shutil
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'samm_three_20261027/appendices';OUT.mkdir(exist_ok=True)
paper=ROOT.parents[1]/'pdf/2hs/main.tex'
if not (OUT/'before_main.tex').exists():
 shutil.copy2(paper,OUT/'before_main.tex');shutil.copy2(paper.with_suffix('.pdf'),OUT/'before_main.pdf')
t=(OUT/'before_main.tex').read_text(encoding='utf-8')
app=(ROOT/'appendices_20261027.tex').read_text(encoding='utf-8')
rows=json.loads((ROOT/'samm_three_20261027/results.json').read_text())
raw=json.loads((ROOT/'data/natural_density_search/results.json').read_text())+json.loads((ROOT/'data/natural_density_search/hierarchy2.json').read_text())
diagnostics=json.loads((ROOT/'data/density_insights/analysis.json').read_text())['initial_diagnostics']
names={'fixed':'Fixed FD','rho':r'$R_\rho$','rm':r'$R_m$','hierarchy2':r'$R_2$'}
def sci(v):
 a,b=f'{v:.3e}'.split('e');return rf'${a}\times10^{{{int(b)}}}$'
def table(number,caption,cols,header,body):
 return rf'''\begin{{table}}[!htbp]
\centering
\caption*{{Table C.{number}. {caption}}}
\footnotesize\setlength{{\tabcolsep}}{{3pt}}\renewcommand{{\arraystretch}}{{1.18}}
\begin{{tabular}}{{{cols}}}
\toprule
{header} \\
\midrule
{body}
\bottomrule
\end{{tabular}}
\end{{table}}
\FloatBarrier
'''
b1=b2=b3='';orders=[]
for ci,p in enumerate([[5.],[1.1,1.25]]):
 title=['One soliton','Two solitons'][ci]
 b1+=r'\multicolumn{7}{l}{\textit{'+title+r'}} \\'+'\n'
 b2+=r'\multicolumn{5}{l}{\textit{'+title+r'}} \\'+'\n'
 b3+=r'\multicolumn{4}{l}{\textit{'+title+r'}} \\'+'\n'
 for kind,name in names.items():
  z=next(z for z in rows if z['p']==p and z['kind']==kind)
  coarse=next(z for z in raw if z['p']==p and z['kind']==kind and z['nodes']==1000)
  order={q:float(np.log(coarse[q]/z[q])/np.log(1999/999)) for q in ['u','rho']};orders.append(dict(p=p,kind=kind,**order))
  vals=[name,sci(coarse['u']),sci(z['u']),f"{order['u']:.3f}",sci(coarse['rho']),sci(z['rho']),f"{order['rho']:.3f}"]
  b1+=' & '.join(vals)+r' \\'+'\n'
  b2+=' & '.join([name,sci(z['halving_change']),sci(z['min_h']),f"{z['min_rho']:.6f}",f"{z['min_R']:.6f}"])+r' \\'+'\n'
  d=next(d for d in diagnostics if d['p']==p and d['kind']==kind)
  b3+=' & '.join([name,sci(d['D2_defect']),sci(d['isolated_poisson_error']),f"{d['mesh_ratio']:.3f}"])+r' \\'+'\n'
 if ci==0:b1+='\\midrule\n';b2+='\\midrule\n';b3+='\\midrule\n'
app=app.replace('% APPENDIX_REFINEMENT',table(1,'Nodal refinement at $T=0.25$ for fixed FD and the three SAMM formulations.','lrrrrrr',r'Mesh & $E_u^{(1000)}$ & $E_u^{(2000)}$ & $p_u$ & $E_\rho^{(1000)}$ & $E_\rho^{(2000)}$ & $p_\rho$',b1))
app=app.replace('% APPENDIX_CHECKS',table(2,'Step-halving changes and sampled minima for the 2000-node experiments.','lrrrr',r'Mesh & $\delta_{\Delta T}$ & $\min h$ & $\min\rho$ & $\min R$',b2))
app=app.replace('% APPENDIX_RECOVERY',table(3,'Initial-grid differentiation and isolated velocity recovery at 1000 nodes.','lrrr',r'Mesh & $\max|\mathcal D_2u_*-u_*^{\prime\prime}|$ & $\max|u_{\rm rec}-u_*|$ & $h_{\max}/h_{\min}$',b3))
# Body links point to named appendix anchors.
refs=[('The continuous-reference experiments examine the resulting field errors, including their accumulation through the reconstruction.',r'The continuous-reference experiments examine the resulting field errors, including their accumulation through the reconstruction. The algebra leading to (10) and the corresponding phase expansion are detailed in \hyperref[app:correction]{Appendix A}.'),
('The additional derivative',r'The nonuniform operators, their consistency expansions and the tridiagonal recovery are given in \hyperref[app:stencils]{Appendix B}. The additional derivative'),
('The change in ordering directs attention to the accumulated field and mesh evolution as well as the initial spatial representation.',r'The change in ordering directs attention to the accumulated field and mesh evolution as well as the initial spatial representation. \hyperref[app:checks]{Appendix C.3} gives this diagnostic for all four grids and both wave profiles.'),
('These checks accompany the terminal comparisons for all four mesh choices.',r'These checks accompany the terminal comparisons for all four mesh choices; the full values are reported in \hyperref[app:checks]{Appendix C.2}.'),
('Their relative errors remain close across these resolutions.',r'The errors and observed orders are listed in \hyperref[app:checks]{Appendix C.1}. Their relative errors remain close across these resolutions.')]
for a,b in refs:
 assert a in t,a;t=t.replace(a,b,1)
t=t.replace('Section 6 discusses the numerical implications of these results.','Section 6 discusses the numerical implications of these results. Appendices A--C provide the correction calculation, nonuniform difference formulas and supplementary numerical checks.')
t=t.replace(r'\FloatBarrier'+'\n'+r'\renewcommand{\refname}{References}',app+'\n'+r'\FloatBarrier'+'\n'+r'\renewcommand{\refname}{References}')
paper.write_text(t,encoding='utf-8')
(OUT/'tables_source.json').write_text(json.dumps(dict(fine_source='../results.json',coarse_sources=['../../data/natural_density_search/results.json','../../data/natural_density_search/hierarchy2.json'],orders=orders),indent=2))

# Exact checks of the algebra and consistency coefficients printed above.
a,c,r=s.symbols('a c r',nonzero=True)
assert s.simplify(((a/r-(a-c)*r)**2-c*c*r*r)/2-a*c*(1-r*r)-a*a*(1/r-r)**2/2)==0
hm,hp=s.symbols('hm hp',positive=True)
d1=[-hp/(hm*(hm+hp)),(hp-hm)/(hm*hp),hm/(hp*(hm+hp))]
d2=[2/(hm*(hm+hp)),-2/(hm*hp),2/(hp*(hm+hp))]
nodes=[-hm,0,hp]
for coeff,expected in [(d1,{0:0,1:1,2:0,3:hm*hp/6,4:hm*hp*(hp-hm)/24}),(d2,{0:0,1:0,2:1,3:(hp-hm)/3,4:(hp*hp-hp*hm+hm*hm)/12})]:
 for n,v in expected.items():assert s.simplify(sum(z*x**n for z,x in zip(coeff,nodes))/s.factorial(n)-v)==0
print('Appended A-C, inserted five targeted body links, verified correction and stencil coefficients.')
