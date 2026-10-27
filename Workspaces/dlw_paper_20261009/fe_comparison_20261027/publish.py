from pathlib import Path
import re,json,subprocess,copy,hashlib
import numpy as np
from bs4 import BeautifulSoup
from PIL import Image
R=Path('C:/Users/msz/aca');H=Path(__file__).parent;path=R/'dlw-paper.html'
s=BeautifulSoup(path.read_text(encoding='utf8'),'html.parser')
assert s.find(id='fe-formulation') is None
def frag(text):return BeautifulSoup(text,'html.parser')
def paragraph(text):return frag('<p>'+text+'</p>').p
def replace_start(start,text):
 p=next(p for p in s.find_all('p') if p.get_text().startswith(start));p.replace_with(paragraph(text))
def replace_text(old,new):
 for node in list(s.find_all(string=True)):
  if node.parent.name in ['script','style','annotation']:continue
  if old in node:node.replace_with(node.replace(old,new))
replace_text('together with a direct finite-difference discretization of the continuous DLW system as a baseline.','together with finite-difference (FD) and finite-element (FE) approximations of the continuous DLW system as baselines.')
replace_text('Endpoint-SD, Centered-SD, and the direct finite-difference baseline use','Endpoint-SD, Centered-SD, FD, and FE use')
replace_text('FD places both fields at nodes.','FD and FE place both fields at nodes.')
replace_text('whereas FD places both fields at the nodes.','whereas FD and FE place both fields at the nodes.')
replace_text('Endpoint-SD and FD advance','Endpoint-SD, FD, and FE advance')
fe=r'''<div id="fe-formulation">
<p>We also construct a piecewise-linear finite-element approximation in \(y\), denoted by FE. On the same nodes as FD, let \(\phi_j\) be the continuous hat functions and write \(u_h=\sum_j u_j\phi_j\), \(v_h=\sum_j v_j\phi_j\). We integrate the first DLW equation over each transverse cell and test the second equation against the hat functions. With \(I_y=[y_0,y_N]\), define</p>
<p>\[M_{ij}=\int_{I_y}\phi_i\phi_j\,dy,\qquad C_{ij}=\int_{I_y}\phi_i\partial_y\phi_j\,dy,\qquad B_i(u,v)=\int_{I_y}\phi_i\bigl[(u_h+2a)v_h-4u_h\bigr]\,dy.\]</p>
<p>The resulting system is</p>
<p>\[\begin{aligned}\Delta_h\dot u_k&amp;=-\mathcal D_x\Delta_hH(u_k)-\mathcal D_{xx}\mathcal M_-v_k,\\ M\dot v&amp;=-\mathcal D_x B(u,v)-\mathcal D_{xx}Cu.\end{aligned}\]</p>
<p>The cell average of \(v_h\) is exactly \(\mathcal M_-v_k\), so the first equation agrees with FD. In the second equation, we retain the consistent mass matrix and evaluate the element integrals exactly. For a uniform mesh, \(M_{ii}=2h/3\) at interior nodes, \(M_{00}=M_{NN}=h/3\), and \(M_{i,i+1}=M_{i+1,i}=h/6\). The nonlinear load integrates the product of the two piecewise-linear fields. At each time stage, a tridiagonal solve supplies \(\dot v\), and the first equation is summed from the same prescribed lower value of \(\dot u\). Endpoint hat functions are retained in the mass, derivative, and nonlinear-load integrals, closing the FE system on \(I_y\) without transverse ghost nodes.</p>
</div>'''
p=next(p for p in s.find_all('p') if p.get_text().startswith('The three spatial formulations use'))
p.insert_before(frag(fe).div)
p.replace_with(paragraph(r'The four spatial formulations share the Fourier approximation in \(x\), the continuous initial fields, and the lower-boundary value used to recover \(u_t\). FD and FE place both fields at the same nodes and have the same first equation; their different transverse approximations enter through the second equation. Alongside the two integrable lattices, these baselines allow us to examine how field placement, nonlinear fluxes, and weak projection affect the computed waves.'))
replace_start('In this subsection, we examine how the spatial formulation',r'In this subsection, we examine how the spatial formulation affects the accuracy of the two physical fields, following the initial spatial approximation through to the computed wave profiles. The analysis in Section 3.4 identifies different truncation errors for Endpoint-SD and Centered-SD, and we use the four test problems to investigate how these differences appear during evolution. FD and FE provide two approximations of the continuous equations on a common nodal grid. All four formulations use \(h=\Delta x=0.1\) and advance from the exact initial data to \(T=0.01\) using classical RK4 with \(\Delta t=10^{-4}\). The computational domains, reference fields, and error-evaluation regions are unchanged across the comparison. We first examine the initial time-derivative errors in Table 2, then consider the evolved physical fields and their spatial error distributions.')
replace_start('At ',r'PLACEHOLDER') if False else None
p=next(p for p in s.find_all('p') if 'the two semi-discrete formulations show a clear division' in p.get_text())
p.replace_with(paragraph(r'Table 2 separates the initial approximation of the two components. Endpoint-SD gives the smallest \(u_t\) defect in all four cases, and Centered-SD reduces the \(v_t\) defect relative to Endpoint-SD. This difference follows the consistency analysis of Section 3.4: the first equations are second-order consistent, whereas the endpoint pairing in the second equation retains an \(O(h)\) term. FE gives the smallest initial \(v_t\) defect in these tests. Its \(u_t\) defect agrees with FD because their first equations and initial nodal fields coincide, while the consistent-mass projection changes the approximation of \(v_t\).'))
replace_start('Looking across Table 3',r'Table 3 shows that FE has the smallest terminal \(v\) error in all four tests. The smallest \(u\) error is attained by FE for the one-soliton case, FD for the two-soliton case, and Endpoint-SD for the Gaussian and sinusoidal cases. FD and FE begin with identical \(u_t\), but their different \(v\) evolutions enter the first equation through \(v_{xx}\), producing different terminal \(u\) errors. The comparison thus follows the effect of the transverse approximation through the coupled physical fields.')
replace_text('all three formulations follow','all four formulations follow')
replace_text('all three sets of numerical symbols','all four sets of numerical symbols')
replace_text('other two methods in','other three methods in')
replace_text('Figure 5(e–j)','Figure 5(e–l)');replace_text('Figure 6(e–j)','Figure 6(e–l)')
replace_text('errors of Centered-SD and FD visible','errors of Centered-SD, FD, and FE visible')
replace_text('the Centered-SD and FD maps retain','the Centered-SD, FD, and FE maps retain')
replace_text('with columns for Endpoint-SD, Centered-SD and FD.','with columns for Endpoint-SD, Centered-SD, FD, and FE.')
replace_text('and produces the smallest ', 'and produces a smaller ') if False else None
p=next(p for p in s.find_all('p') if p.get_text().startswith('In the smooth, small-amplitude Gaussian'))
p.replace_with(paragraph(r'In the smooth, small-amplitude Gaussian (Figure 7) and sinusoidal (Figure 8) tests, the terminal error ordering follows the initial derivative defects closely. Endpoint-SD gives the smallest \(u\) error, followed by Centered-SD, with FD and FE at almost the same level. For \(v\), FE gives errors of \(6.120\times10^{-9}\) and \(2.856\times10^{-9}\), compared with \(6.967\times10^{-9}\) and \(4.706\times10^{-9}\) for Centered-SD. Relative to FD, the FE error in this component is smaller by factors of about \(3.6\) and \(5.7\). The exact second field remains constant at \(v=4\) along \(y=0\); the central section therefore shows errors near machine precision, while the heatmaps reveal the variation away from this symmetry line.'))
# Add a short FE/FD observation to the soliton discussion without changing SD comparisons.
p=next(p for p in s.find_all('p') if p.get_text().startswith('Relative to Endpoint-SD, Centered-SD reduces'))
p.insert_after(paragraph(r'FE reduces the terminal \(v\) error relative to FD by factors of about \(7.9\) and \(6.6\) in the one- and two-soliton tests. Its effect on \(u\) is smaller: the error decreases from \(5.568\times10^{-5}\) to \(4.574\times10^{-5}\) for the one-soliton case, and increases slightly from \(1.149\times10^{-4}\) to \(1.158\times10^{-4}\) for the two-soliton case. The common first equation makes this pair useful for tracing how a change in the second-field approximation affects the coupled evolution.'))
cases=['A','D','Gaussian','Sinusoidal'];records={c:json.loads((H/f'{c}.json').read_text()) for c in cases}
for name,key in [('table-initial','initial'),('table-final','error')]:
 tb=s.find(id=name);head=tb.thead.find_all('tr');th=s.new_tag('th',colspan='2');th.string='FE';head[0].append(th)
 for th in list(head[1].find_all('th'))[-2:]:head[1].append(copy.deepcopy(th))
 for case,tr in zip(cases,tb.tbody.find_all('tr')):
  for v in records[case][key]:
   td=s.new_tag('td');td['data-value']=format(v,'.17g');tr.append(td)
  cells=tr.find_all('td');values=[float(td['data-value']) for td in cells]
  for i,td in enumerate(cells):
   val=values[i];a,b=f'{val:.3e}'.split('e');txt=f'{a} × 10<sup>{int(b)}</sup>'
   if i==min(range(i%2,len(values),2),key=lambda j:values[j]):txt='<strong>'+txt+'</strong>'
   td.clear();td.append(frag(txt))
for i,c in enumerate(cases,5):
 f=s.find(id=f'figure-{i}');f.img['src']=(H/'figures'/f'spatial_{c}.png').relative_to(R).as_posix()
 for a in f.find_all('a'):
  if a.get('href','').endswith('.pdf'):a['href']=(H/'figures'/f'spatial_{c}.pdf').relative_to(R).as_posix()
# Render new inline/display mathematics, including the two synchronized TeX paragraphs.
nodes=[];jobs=[]
for node in list(s.find_all(string=True)):
 if node.find_parent('annotation') or node.find_parent(class_='katex'):continue
 if node.parent.name in ['style','script']:continue
 matches=list(re.finditer(r'\\\((.*?)\\\)|\\\[(.*?)\\\]',str(node),re.S))
 if matches:
  nodes.append((node,matches))
  jobs.extend(dict(tex=m.group(1) or m.group(2),display=m.group(2) is not None) for m in matches)
js="const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(f=>k.renderToString(f.tex,{displayMode:f.display,throwOnError:true}))));"
proc=subprocess.run(['node','-e',js,str(R/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(jobs),capture_output=True,text=True,encoding='utf8',check=True)
rendered=iter(json.loads(proc.stdout))
for node,matches in nodes:
 raw=str(node);parts=[];last=0
 for m in matches:parts.extend([raw[last:m.start()],next(rendered)]);last=m.end()
 parts.append(raw[last:]);node.replace_with(frag(''.join(parts)))
# Regenerate print panel rows from the synchronized/new full images.
rows=H/'print_rows';rows.mkdir(exist_ok=True)
for n,f in enumerate(s.find_all('figure'),1):
 if n in [11,12]:continue
 for old in f.select('.print-figure-part'):old.decompose()
 im=Image.open(R/f.img['src']).convert('RGB');w,h=im.size;white=np.all(np.asarray(im)>245,axis=(1,2))
 targets=[.295,.53,.767] if 5<=n<=8 else [.53];cuts=[0]
 for v in targets:
  ys=np.flatnonzero(white[max(0,int((v-.07)*h)):min(h,int((v+.07)*h))])+max(0,int((v-.07)*h))
  assert len(ys),(n,v);cuts.append(int(ys[np.argmin(abs(ys-v*h))]))
 cuts.append(h)
 width=190 if 5<=n<=8 else min(190,(95 if n<=4 else 85 if n>=13 else 100)*w/h)
 for j,(lo,hi) in enumerate(zip(cuts,cuts[1:])):
  used=np.flatnonzero(~white[lo:hi]);y0=max(lo,lo+int(used[0])-10);y1=min(hi,lo+int(used[-1])+11)
  dst=rows/f'figure_{n}_row_{j+1}.png';im.crop((0,y0,w,y1)).save(dst)
  part=s.new_tag('div',attrs={'class':'print-figure-part print-row'})
  img=s.new_tag('img',src=dst.relative_to(R).as_posix(),alt=f'Figure {n}, panel row {j+1}')
  img['style']=f'width:{width:.4f}mm!important;max-height:none!important;height:auto!important;max-width:100%;margin:auto';part.append(img)
  if j==len(cuts)-2:
   cap=copy.deepcopy(f.figcaption);cap.attrs.pop('class',None);part.append(cap)
  f.append(part)
path.write_text(str(s),encoding='utf8')
(H/'publication.json').write_text(json.dumps(dict(cases=records,tex_unchanged=hashlib.sha256((R/'pdf/dlw/main.tex').read_bytes()).hexdigest()==hashlib.sha256((H/'tex_sync_source.tex').read_bytes()).hexdigest(),figure_count=len(s.find_all('figure')),table_count=len(s.find_all('table'))),indent=2))
print('Published four-method comparison')
