from pathlib import Path
import json,re,shutil
import numpy as np
import sympy as s
import pymupdf
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'samm_energy_20261028';paper=ROOT.parents[1]/'pdf/2hs/main.tex'
if not (OUT/'before_main.tex').exists():
 shutil.copy2(paper,OUT/'before_main.tex');shutil.copy2(paper.with_suffix('.pdf'),OUT/'before_main.pdf')
t=(OUT/'before_main.tex').read_text(encoding='utf-8')
old=t
start=t.index(r'\section*{5. Self-adaptive');end=t.index(r'\subsection*{5.2.',start)
t=t[:start]+(OUT/'selection.tex').read_text(encoding='utf-8')+t[end:]
def rep(a,b):
 global t
 assert a in t,a[:100];t=t.replace(a,b,1)
def para(start,new):
 global t
 i=t.index(start);j=t.index('\n\n',i);t=t[:i]+new+t[j:]
rep('We derive two further conserved densities by balancing curvature and density-gradient transport against mass stretching.','We construct two further conserved coordinates by balancing curvature against mass stretching and by cancelling slope--density exchange in a quadratic balance.')
rep('the gradient-sensitive density further reduces the single-wave density error while increasing the velocity error.','the energy-type density further reduces the single-wave density error while increasing the velocity error.')
rep('A density involving curvature or density gradients can assign resolution to different parts of the same wave.','A density involving curvature or the quadratic balance of slope and physical density can assign resolution to different parts of the same wave.')
rep('We then derive two further conserved densities from the coupled transport equations and use their fluxes, together with physical mass, to construct three moving meshes.','We then make the choice of conserved coordinate part of the numerical investigation. Starting from the field equations, we determine a curvature--mass ratio by balancing stretching rates and an energy-type density by cancelling the exchange in a quadratic slope--density balance. Their local fluxes, together with physical mass, define three moving meshes.')
rep('the gradient-sensitive choice improves the single-wave density error further at a cost in velocity accuracy.','the energy-type choice improves the single-wave density error further at a cost in velocity accuracy.')
rep('Appendices A--C provide the correction calculation, nonuniform difference formulas and supplementary numerical checks.','Appendices A--C provide the correction calculation, nonuniform difference formulas and supplementary numerical checks. Appendix D extends the density search to a curvature--gradient combination.')
rep(r'The additional derivative \(\rho_x\) in \(R_2\) uses the same three-point first-derivative operator.',r'The velocity gradient in \(R_E\) is evaluated by the same three-point first-derivative operator. The monitor and its flux are reconstructed at every stage from these numerical fields.')
rep(r'whereas \(R_m\) and \(R_2\) increase there.',r'whereas \(R_m\) and \(R_E\) increase there.')
para('The mass-based mesh has larger errors',r'''The mass-based mesh has larger errors in both fields than fixed FD. Its velocity error is about 9.86 times the fixed-grid value and its density error is about 2.10 times that value. Both alternative coordinates improve the density field: the error ratios are approximately 0.587 for \(R_m\) and 0.508 for \(R_E\). The energy-type coordinate therefore gives the smallest density error in this case. Its velocity error is about 1.64 times the fixed-grid value, compared with 1.47 for \(R_m\). The density depression and slope contribution in (23) supply a useful allocation for \(\rho\), while the velocity recovery and coupled evolution respond differently to that allocation.''')
para('The different field responses can be examined',r'''To examine the role of the initial mesh, we also apply the velocity recovery separately from time evolution. At 1000 nodes, supplying exact sampled curvature to the Poisson solver gives single-wave velocity errors of approximately \(1.39\times10^{-6}\), \(9.46\times10^{-7}\) and \(2.00\times10^{-6}\) on the fixed, \(R_m\) and \(R_E\) grids, respectively. The curvature--mass grid improves this isolated recovery even though its terminal velocity error is larger than the fixed-grid error. The energy-type grid has a larger error in both measurements. These results separate two contributions worth examining: the spatial recovery on a given grid and the curvature error accumulated during evolution. The diagnostic supplies analytic curvature, while the evolution uses the consistent discrete initialization in Section 5.2. \hyperref[app:recovery]{Appendix C.3} gives the differentiation and recovery errors for all four grids and both profiles.''')
para('Here \(R_m\) improves both fields',r'''For the two-wave profile, \(R_m\) improves both fields, with velocity and density errors approximately 0.732 and 0.522 times the fixed-grid values. The energy-type coordinate reduces the density error to about 0.753 of the baseline, while its velocity error is about 2.82 times larger. Physical mass gives the largest errors in both fields. Thus both alternatives direct resolution toward wave structure in a way that benefits the density, but the curvature--mass ratio also improves the recovered velocity for this profile. The relative error curves show where these differences occur across the two wave regions.''')
para('Across the two profiles,',r'''Across the two profiles, \(R_m\) gives the smallest velocity errors among the three moving meshes and improves density accuracy relative to fixed FD. The energy-type coordinate gives the smallest density error for the single wave, while \(R_m\) gives the smaller density error for the two-wave profile. Their different rankings connect the choice of local field information to a measurable change in accuracy. The quadratic balance emphasizes slope magnitude and density deficit; the ratio \(m/(2\rho)\) combines curvature with the density that stretches the grid. The results identify the latter as the more balanced allocation in these tests, and show how the energy-type allocation can favor one component of a smooth wave.''')
para('The conservation laws provide a second route',r'''The conservation laws provide a second route from structure to computation. We obtain three mesh densities from the field equations through physical mass conservation, a balance of curvature and mass stretching, and cancellation of slope--density exchange in a quadratic expression. Giving the construction explicitly makes the allocation rule traceable to the quantities represented by each density. In the tests, physical mass expands the mesh near the velocity peaks, whereas the curvature--mass and energy-type densities concentrate resolution there. The curvature--mass ratio improves density accuracy in both cases and velocity accuracy in the two-soliton case. The energy-type choice gives the smallest single-wave density error, accompanied by a larger velocity error. The common second-order refinement trend persists while the fieldwise error coefficients vary with the chosen coordinate. The initial recovery diagnostic further shows why grid selection needs to be assessed together with the accumulated field evolution. Among the three moving meshes, the curvature--mass ratio gives the most balanced results for the present profiles.''')
rep(r'The derivatives in the field equations, and the interior \(\rho_x\) entering \(R_2\), are evaluated on the current node positions at each time stage.',r'The derivatives in the field equations, including the velocity gradient entering \(R_E\), are evaluated on the current node positions at each time stage.')

rows=json.loads((OUT/'results.json').read_text());raw=json.loads((ROOT/'data/natural_density_search/results.json').read_text())
diag=json.loads((ROOT/'data/density_insights/analysis.json').read_text())['initial_diagnostics']
names={'fixed':'Fixed FD','rho':r'$R_\rho$','rm':r'$R_m$','energy':r'$R_E$'}
def sci(v):
 a,b=f'{v:.3e}'.split('e');return rf'{a}\times10^{{{int(b)}}}'
def replace_table(label,body,cols,header,caption):
 global t
 i=t.index(r'\caption*{Table '+label+'.');start=t.rfind(r'\begin{table}',0,i);end=t.index(r'\end{table}',i)+len(r'\end{table}')
 size=r'\small' if label in ['7','8'] else r'\footnotesize'
 new=rf'''\begin{{table}}[!htbp]
\centering
\caption*{{Table {label}. {caption}}}
{size}\setlength{{\tabcolsep}}{{3pt}}\renewcommand{{\arraystretch}}{{1.18}}
\begin{{tabular}}{{{cols}}}
\toprule
{header} \\
\midrule
{body}
\bottomrule
\end{{tabular}}
\end{{table}}'''
 t=t[:start]+new+t[end:]
b1=b2=b3='';orders=[]
for ci,p in enumerate([[5.],[1.1,1.25]]):
 case=['One soliton','Two solitons'][ci];b='';data=rows[ci*4:ci*4+4];fixed=data[0]
 b1+=rf'\multicolumn{{7}}{{l}}{{\textit{{{case}}}}} \\'+'\n';b2+=rf'\multicolumn{{5}}{{l}}{{\textit{{{case}}}}} \\'+'\n';b3+=rf'\multicolumn{{4}}{{l}}{{\textit{{{case}}}}} \\'+'\n'
 for z in data:
  kind=z['kind'];name=names[kind];vals=[]
  for q in ['u','rho']:
   val=sci(z[q]);vals.append('$'+(r'\mathbf{'+val+'}' if z[q]==min(d[q] for d in data) else val)+'$')
  b+=' & '.join([name]+vals+[f"{z['u']/fixed['u']:.3f}",f"{z['rho']/fixed['rho']:.3f}"])+r' \\'+'\n'
  coarse=next(r for r in raw if r['p']==p and r['kind']==kind and r['nodes']==1000)
  order={q:float(np.log(coarse[q]/z[q])/np.log(1999/999)) for q in ['u','rho']};orders.append(dict(p=p,kind=kind,**order))
  b1+=' & '.join([name,'$'+sci(coarse['u'])+'$','$'+sci(z['u'])+'$',f"{order['u']:.3f}",'$'+sci(coarse['rho'])+'$','$'+sci(z['rho'])+'$',f"{order['rho']:.3f}"])+r' \\'+'\n'
  b2+=' & '.join([name,'$'+sci(z['halving_change'])+'$','$'+sci(z['min_h'])+'$',f"{z['min_rho']:.6f}",f"{z['min_R']:.6f}"])+r' \\'+'\n'
  d=next(d for d in diag if d['p']==p and d['kind']==kind)
  b3+=' & '.join([name,'$'+sci(d['D2_defect'])+'$','$'+sci(d['isolated_poisson_error'])+'$',f"{d['mesh_ratio']:.3f}"])+r' \\'+'\n'
 replace_table(str(7+ci),b,'lrrrr',r'Mesh & $E_u$ & $E_\rho$ & $E_u/E_u^{\rm fixed}$ & $E_\rho/E_\rho^{\rm fixed}$',f'{case}: nodal errors at $T=0.25$ with 2000 nodes. Ratios are relative to fixed FD. Bold entries mark the smallest error in each field.')
 if ci==0:b1+='\\midrule\n';b2+='\\midrule\n';b3+='\\midrule\n'
replace_table('C.1',b1,'lrrrrrr',r'Mesh & $E_u^{(1000)}$ & $E_u^{(2000)}$ & $p_u$ & $E_\rho^{(1000)}$ & $E_\rho^{(2000)}$ & $p_\rho$','Nodal refinement at $T=0.25$ for fixed FD and the three SAMM formulations.')
replace_table('C.2',b2,'lrrrr',r'Mesh & $\delta_{\Delta T}$ & $\min h$ & $\min\rho$ & $\min R$','Step-halving changes and sampled minima for the 2000-node experiments.')
replace_table('C.3',b3,'lrrr',r'Mesh & $\max|\mathcal D_2u_*-u_*^{\prime\prime}|$ & $\max|u_{\rm rec}-u_*|$ & $h_{\max}/h_{\min}$','Initial-grid differentiation and isolated velocity recovery at 1000 nodes.')
para('All three densities,',rf'All three densities, the physical density and the mesh widths remain positive at the sampled full-step states; the smallest recorded cell width is {min(z["min_h"] for z in rows):.4f}. Halving the time step changes the terminal node positions and field values by at most \({sci(max(z["halving_change"] for z in rows))}\). These checks accompany the terminal comparisons for all four mesh choices; the full values are reported in \hyperref[app:timesteps]{{Appendix C.2}}.')
values=[z[q] for z in orders for q in ['u','rho']]
t=re.sub(r'observed orders for the four mesh choices and both fields lie between [0-9.]+ and [0-9.]+\.',f'observed orders for the four mesh choices and both fields lie between {min(values):.3f} and {max(values):.3f}.',t)
rep('the smaller density error of the curvature-based meshes persists under refinement','the smaller density error of the curvature--mass and energy-type meshes persists under refinement')
para('For the single wave, both curvature-based grids',r'''For the single wave, both alternative coordinates reduce the local differentiation defect compared with the uniform grid, but only \(R_m\) also reduces the isolated recovery error. Its larger terminal velocity error in Table C.1 therefore occurs despite the favorable initial recovery result. For the two-wave profile, both alternatives give larger isolated recovery errors than fixed FD, although \(R_m\) later produces the smallest terminal velocity error. The diagnostic and the evolved field error measure different parts of the computation. The latter includes the curvature error accumulated through transport and stretching, together with the changing mesh on which velocity is recovered.''')

appendix=r'''\FloatBarrier
\section*{Appendix D. Extending the density search to spatial gradients}
\label{app:additional-density}

The same transport calculation can be continued after introducing a spatial derivative of the physical density. We record this extension to distinguish the low-order energy-type construction used in Section 5 from a further curvature--gradient balance. Recall \(m=u_{xx}+2\) and \(D=\partial_t-u\partial_x\). The field equations and their differentiated mass equation give
\paperdisplay{Dm=2u_xm+c^2\rho\rho_x,\qquad D\rho=u_x\rho,\qquad D\rho_x=2u_x\rho_x+\rho(m-2).}{\tag{D.1}}
The first and third quantities carry the same stretching rate. To cancel their mixed source terms, consider \(K=m^2-c^2\rho_x^2\). Direct calculation yields
\paperdisplay{DK=2m(2u_xm+c^2\rho\rho_x)-2c^2\rho_x\bigl(2u_x\rho_x+\rho(m-2)\bigr)=4u_xK+4c^2\rho\rho_x.}{\tag{D.2}}
Dividing by \(\rho^3\) removes three of the four stretching factors, giving \(D(K/\rho^3)-u_xK/\rho^3=4c^2\rho_x/\rho^2\). The remaining spatial derivative produces
\paperdisplay{R_2=\frac{m^2-c^2\rho_x^2}{4\rho^3},\qquad Q_2=-uR_2+c^2\left(\frac1\rho-1\right),\qquad (R_2)_t+(Q_2)_x=0.}{\tag{D.3}}
The numerator is selected by cancellation of the coupling, the denominator by the stretching balance, and the factor four by the unit background normalization. This construction requires the additional local information \(\rho_x\). It yields a positive coordinate where \(\rho>0\) and \(m^2>c^2\rho_x^2\). In terms of the curvature--mass ratio, \(R_2=R_m^2/\rho-c^2(\partial_x\log\rho)^2/(4\rho)\), so the relative density gradient modifies the allocation. It provides a further analytical candidate beyond the three choices compared in the main experiments.

'''
t=t.replace(r'\FloatBarrier'+'\n'+r'\renewcommand{\refname}{References}',appendix+r'\FloatBarrier'+'\n'+r'\renewcommand{\refname}{References}')
# Preserve the previous large-label vector split for Figure 9.
for ci in [0,1]:shutil.copy2(OUT/f'samm_energy_{ci}.pdf',paper.parent/f'images/samm-energy-{ci+1}.pdf')
with pymupdf.open(OUT/'samm_energy_0.pdf') as src:
 for suffix,y0,y1 in [('upper',0,328),('lower',328,src[0].rect.height)]:
  clip=pymupdf.Rect(0,y0,src[0].rect.width,y1)
  with pymupdf.open() as dst:
   pg=dst.new_page(width=clip.width,height=clip.height);pg.show_pdf_page(pg.rect,src,0,clip=clip);dst.save(paper.parent/f'images/samm-energy-1-{suffix}.pdf')
t=t.replace('images/samm-three-1-','images/samm-energy-1-').replace('images/samm-three-2.pdf','images/samm-energy-2.pdf')
# User selected only rho, Rm and RE: retain the old R2 derivation in backups, not the paper.
start=t.index(r'\FloatBarrier'+'\n'+r'\section*{Appendix D.')
end=t.index(r'\FloatBarrier'+'\n'+r'\renewcommand{\refname}{References}',start)
t=t[:start]+t[end:]
t=t.replace(' Appendix D extends the density search to a curvature--gradient combination.','')
t=t.replace(r' The further curvature--gradient construction \(R_2\) is derived in \hyperref[app:additional-density]{Appendix D} as an extension of the same search procedure.','')
with pymupdf.open(OUT/'samm_energy_1.pdf') as src:
 for suffix,y0,y1 in [('upper',0,328),('lower',328,src[0].rect.height)]:
  clip=pymupdf.Rect(0,y0,src[0].rect.width,y1)
  with pymupdf.open() as dst:
   pg=dst.new_page(width=clip.width,height=clip.height);pg.show_pdf_page(pg.rect,src,0,clip=clip);dst.save(paper.parent/f'images/samm-energy-2-{suffix}.pdf')
i=t.index(r'\caption*{Figure 10.');start=t.rfind(r'\begin{figure}',0,i);end=t.index(r'\end{figure}',i)+len(r'\end{figure}')
caption=t[i:t.index(r'\end{figure}',i)].strip().replace(r'\caption*',r'\captionof*{figure}',1)
new='\\begin{center}\n\\includegraphics[width=.88\\linewidth]{images/samm-energy-2-upper.pdf}\n\\end{center}\n\\noindent\\begin{minipage}{\\linewidth}\n\\centering\n\\includegraphics[width=.88\\linewidth]{images/samm-energy-2-lower.pdf}\n'+caption+'\n\\end{minipage}\n'
t=t[:start]+new+t[end:]
# References follow the final appendix without a forced page break.
paper.write_text(t,encoding='utf-8')
# Check the proposed family and its energy flux at general c.
u,w,r,c,A=s.symbols('u w r c A');Dw=w*w/2+4*u+c*c*(r*r-1)/2;Dr=r*w
E=w*w+A*(r*r-1)
res=s.expand(s.diff(E,w)*Dw+s.diff(E,r)*Dr-w*E)
assert s.simplify(res-(8*u*w+(c*c+A)*r*r*w+(A-c*c)*w))==0
assert s.simplify(res.subs(A,-c*c)-(8*u-2*c*c)*w)==0
assert old[:old.index(r'\section*{5.')].count(r'\tag{')==t[:t.index(r'\section*{5.')].count(r'\tag{')
(OUT/'validation_algebra.json').write_text(json.dumps(dict(energy_balance_general_c=True,coefficient_cancellation=True,observed_orders=orders),indent=2))
print('Updated density derivations, body results, 5 tables, 2 figures and Appendix D.')
