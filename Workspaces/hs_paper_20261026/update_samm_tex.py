from pathlib import Path
import json,re,shutil
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'samm_three_20261027'
paper=ROOT.parents[1]/'pdf/2hs/main.tex'
backup=OUT/'before_main.tex'
if not backup.exists():
 shutil.copy2(paper,backup);shutil.copy2(paper.with_suffix('.pdf'),OUT/'before_main.pdf')
t=backup.read_text(encoding='utf-8')
start=t.index('\\FloatBarrier\n\\subsection*{3.4.')
end=t.index('\\FloatBarrier\n\\section*{4.',start)
t=t[:start]+t[end:]
start=t.index('\\FloatBarrier\n\\subsection*{4.4.')
end=t.index('\\FloatBarrier\n\\subsection*{4.5.',start)
t=t[:start]+t[end:]
t=t.replace('4.5. Propagation','4.4. Propagation')
t=t.replace('Section 4.4 compares uniform fixed meshes with conserved-density moving meshes. Section 4.5 follows','Section 4.4 follows')
t=t.replace('examined separately in Section 4.4.','examined separately in Section 5.')
# Renumber existing equations and figure/table references after relocating mesh material.
t=re.sub(r'\\tag\{(16|17|18)\}',lambda m:r'\tag{'+str(int(m[1])-1)+'}',t)
t=re.sub(r'(?<!\\tag\{)\((16|17|18)\)',lambda m:'('+str(int(m[1])-1)+')',t)
t=t.replace('Figures 9 and 10','Figures 7 and 8')
t=re.sub(r'Figure (9|10)(?=[. ])',lambda m:'Figure '+str(int(m[1])-2),t)
t=re.sub(r'Table (7|8)(?=[. ])',lambda m:'Table '+str(int(m[1])-2),t)
section=(ROOT/'samm_section.tex').read_text(encoding='utf-8')
rows=json.loads((OUT/'results.json').read_text())
names={'fixed':'Fixed FD','rho':r'SAMM $R_\rho$','rm':r'SAMM $R_m$','hierarchy2':r'SAMM $R_2$'}
def sci(v):
 a,b=f'{v:.3e}'.split('e');return rf'{a}\times10^{{{int(b)}}}'
for ci,word in enumerate(['ONE','TWO']):
 data=rows[4*ci:4*ci+4]; base=data[0]
 tab=rf'''\begin{{table}}[!htbp]
\centering
\caption*{{Table {7+ci}. {'One-soliton' if ci==0 else 'Two-soliton'} nodal errors at $T=0.25$ with 2000 nodes. Ratios are relative to fixed FD. Bold entries mark the smallest error in each field.}}
\small\setlength{{\tabcolsep}}{{5pt}}\renewcommand{{\arraystretch}}{{1.2}}
\begin{{tabular}}{{lrrrr}}
\toprule
Mesh & $E_u$ & $E_\rho$ & $E_u/E_u^{{\rm fixed}}$ & $E_\rho/E_\rho^{{\rm fixed}}$ \\
\midrule
'''
 for z in data:
  vals=[]
  for q in ['u','rho']:
   v=sci(z[q]);vals.append('$'+(r'\mathbf{'+v+'}' if z[q]==min(d[q] for d in data) else v)+'$')
  tab+=names[z['kind']]+' & '+' & '.join(vals)+f" & {z['u']/base['u']:.3f} & {z['rho']/base['rho']:.3f}"+r' \\'+'\n'
 tab+='\\bottomrule\n\\end{tabular}\n\\end{table}\n'
 section=section.replace('% SAMM_TABLE_'+word,tab)
 image=f'samm-three-{ci+1}.pdf';shutil.copy2(OUT/f'samm_case_{ci}.pdf',paper.parent/'images'/image)
 fig=rf'''\begin{{figure}}[!htbp]
\centering
\includegraphics[width=.88\linewidth,height=.68\textheight,keepaspectratio]{{images/{image}}}
\caption*{{Figure {9+ci}. {'One-soliton' if ci==0 else 'Two-soliton'} SAMM comparison at $T=0.25$. Top: interior cell widths. Middle and bottom: absolute nodal field errors on logarithmic scales. Curves connect actual samples; the plotted window is $[-2.5,2.5]$.}}
\end{{figure}}
'''
 section=section.replace('% SAMM_FIGURE_'+word,fig)
checks=rf'All three densities, the physical density and the mesh widths remain positive at the sampled full-step states; the smallest recorded cell width is {min(z["min_h"] for z in rows):.4f}. Halving the time step changes the terminal node positions and field values by at most \({sci(max(z["halving_change"] for z in rows))}\). These checks accompany the terminal comparisons for all four mesh choices.'
section=section.replace('% SAMM_CHECKS',checks)
audit=json.loads((ROOT/'data/density_insights/analysis.json').read_text())
orders=[z[q] for z in audit['observed_orders'] if z['kind'] in names for q in ['u','rho']]
section=section.replace('% SAMM_ORDER\n',f'{min(orders):.3f} and {max(orders):.3f}')
t=t.replace('\\FloatBarrier\n\\section*{5. Conclusions}',section+'\\FloatBarrier\n\\section*{6. Conclusions}')
t=t.replace('Section 4 examines spatial errors, time integration, mesh allocation and perturbation responses. Section 5 discusses the numerical implications of these results.','Section 4 examines spatial errors, time integration and perturbation responses. Section 5 develops three conservation-law-based self-adaptive meshes and examines their fieldwise accuracy. Section 6 discusses the numerical implications of these results.')
t=t.replace('A second conserved density, derived from the velocity curvature and physical density, generates a mesh that concentrates nodes in the wave region and improves density accuracy in both soliton tests, with the velocity response depending on the wave profile.','We derive two further conserved densities by balancing curvature and density-gradient transport against mass stretching. Comparisons of the three resulting self-adaptive meshes show that the curvature--mass ratio improves density accuracy in both soliton tests and velocity accuracy for the two-wave profile, while the gradient-sensitive density redistributes accuracy between the fields.')
t=t.replace('We then derive a conserved density involving the velocity curvature and use its flux to construct a moving mesh. A matched comparison with uniform fixed FD examines how this allocation affects the two nodal fields.','We then derive two further conserved densities from the coupled transport equations and use their fluxes, together with physical mass, to construct three moving meshes. A matched comparison with uniform fixed FD examines how these allocations affect the two nodal fields.')
old='The conservation laws provide a second route from structure to computation.'
st=t.index(old,t.index('\\section*{6. Conclusions}'));en=t.index('\n\n',st)
t=t[:st]+r'''The conservation laws provide a second route from structure to computation. Physical mass, the curvature--mass ratio and a quadratic curvature--gradient density generate three self-adaptive meshes through their local fluxes. Their derivation follows the stretching and coupling terms of the same transport equations. In the numerical tests, physical mass expands the mesh near the velocity peaks, whereas the other two densities concentrate resolution there. The curvature--mass ratio improves density accuracy in both cases and velocity accuracy in the two-soliton case. The quadratic density gives a slightly smaller density error for the single wave, accompanied by a larger velocity error. Across refinement, the common second-order trend persists while the error coefficients depend on the chosen conserved coordinate. These results show how the local form of a conservation law affects the distribution of numerical accuracy between coupled fields.'''+t[en:]
paper.write_text(t,encoding='utf-8')
assert [int(x) for x in re.findall(r'\\tag\{(\d+)\}',t)]==list(range(1,26))
assert [int(x) for x in re.findall(r'\\caption\*\{Figure (\d+)\.',t)]==list(range(1,11))
assert [int(x) for x in re.findall(r'\\caption\*\{Table (\d+)\.',t)]==list(range(1,9))
assert '% SAMM_' not in t
print('Updated section structure, 25 equations, 10 figures, 8 tables.')
