from pathlib import Path
from bs4 import BeautifulSoup
import re,json,subprocess,shutil
R=Path('C:/Users/msz/aca'); H=Path(__file__).parent; H.mkdir(exist_ok=True)
p=R/'dlw-paper.html'; original=p.read_bytes(); s=original.decode('utf-8')
backup=H/'before.html'
assert not backup.exists(), 'Already applied'
backup.write_bytes(original)
changes=[]
def replace(a,b):
 global s
 n=s.count(a); assert n, a[:100]
 s=s.replace(a,b); changes.append([a[:90],n])
def math(t):
 js="const k=require('./Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js');process.stdout.write(k.renderToString(JSON.parse(process.argv[1]),{throwOnError:true}));"
 return subprocess.check_output(['node','-e',js,json.dumps(t)],cwd=R).decode()
def para(needle,new):
 global s
 hits=[m for m in re.finditer(r'<p\b[^>]*>.*?</p>',s,re.S) if needle in m.group()]
 assert len(hits)==1,(needle,len(hits))
 m=hits[0];s=s[:m.start()]+'<p>'+new+'</p>'+s[m.end():];changes.append([needle,1])
replace('we further establish convergence orders for the corresponding exact wave fields and derive explicit leading error coefficients, describing how the lattice modifies the continuous wave profiles.', 'we further establish second-order approximation of the exact Centered-SD wave fields. Together with the leading correction to the Endpoint-SD equation residual, this relates the lattice construction to its continuum approximation.')
replace('with convergence orders and leading error coefficients helping to explain the behavior at finite lattice spacing.', 'with the consistency analysis helping to interpret the behavior at finite lattice spacing.')
replace('We then establish the convergence orders of the corresponding exact wave fields and derive their leading error coefficients under the stated assumptions.', 'We derive the leading correction to the Endpoint-SD equation residual and establish second-order approximation of the exact Centered-SD wave fields under the stated assumptions.')
replace('We use spatial refinement tests to assess the predicted orders and follow the physical-field errors through time on soliton, Gaussian, and sinusoidal backgrounds.', 'We compare initial time-derivative errors and follow the physical-field errors through time on soliton, Gaussian, and sinusoidal backgrounds.')
replace('identify the shared initial U-derivative coefficient that will guide the spatial comparisons.', 'compare the initial u-derivative errors of the two formulations to interpret the spatial comparisons.')
replace('We have also compared the corresponding exact Gram wave families with their continuous counterparts under suitable regularity and positivity assumptions, establishing their convergence orders and deriving explicit leading error coefficients for the physical fields. In particular, the Centered-SD fields converge at second order.', 'We derive the leading correction to the Endpoint-SD equation residual and compare the exact Centered-SD Gram wave family with its continuous counterpart. Under suitable regularity and positivity assumptions, both Centered-SD fields converge at second order.')
replace('Together, they show how different approximation orders and error coefficients can arise within a common integrable construction,', 'Together, they show how different approximation properties can arise within a common integrable construction,')
criterion=math(r'\max\{\|r_u\|_\infty,(4/h)\|r_\omega\|_\infty\}<2\times10^{-14}')
control='A control calculation with a stopping level of '+math(r'2\times10^{-15}')+' changes the terminal error norms of Section 5.3 by at most '+math(r'8\times10^{-10}')+'.'
rule='The implementation advances '+math(r'(u,w)')+', where '+math(r'w=4\omega/h')+'. In the notation of the field equations, the trapezoidal residual satisfies '+criterion+' at termination.'
para('The implicit step uses an Euler prediction','The implicit step uses an Euler prediction followed by fixed-point iteration. The iteration and its stopping rule are restated in Appendix D, together with the closure rules and the control runs. '+rule+' '+control)
para('<strong>Implicit step.', '<strong>Implicit step.</strong> Crank–Nicolson is solved by an Euler predictor followed by fixed-point iteration on the trapezoidal residual. '+rule+' '+control)
# Replace the remaining table occurrence, including its rendered mathematics.
for m in list(re.finditer(r'<td\b[^>]*>.*?</td>',s,re.S)):
 if 'terminal errors change by at most' in m.group():
  replace(m.group(),'<td>terminal error norms change by at most '+math(r'8\times10^{-10}')+'</td>')
replace('On the periodic interval that constant is the spatial mean of', 'We choose that constant as the negative of the nodal mean of')
replace('This choice leaves the mean displacement zero and keeps the mapping periodic.', 'This choice gives zero density-weighted mean nodal velocity and keeps the mapping periodic.')
replace('the adaptive mesh lowers the error across the entire wave zone', 'the adaptive mesh lowers the maximum errors and the main error peaks')
# Re-render the cofactor identity, including its transposed indices.
doc=BeautifulSoup(s,'html.parser')
for k in doc.select('.katex'):
 a=k.find('annotation')
 if a and r'\mathrm{cof}_{ij}M' in a.get_text():
  oldtex=a.get_text();newtex=oldtex.replace(r'\mathrm{cof}_{ij}M',r'\mathrm{cof}_{ji}M')
  # Locate original raw span via containing paragraph and replace that paragraph's math node.
  raw=next(m.group() for m in re.finditer(r'<p\b[^>]*>.*?</p>',s,re.S) if oldtex in m.group())
  frag=BeautifulSoup(raw,'html.parser')
  for n in frag.select('.katex'):
   if n.find('annotation') and n.find('annotation').get_text()==oldtex:n.replace_with(BeautifulSoup(math(newtex),'html.parser'))
  replace(raw,str(frag));break
para('No amplification of the lower data', 'in which the coefficients have modulus one. An error in the lower trace alone propagates with alternating sign and unchanged magnitude, while errors in the edge differences can accumulate through the sum. The reconstruction is an exact affine relation and requires no branch selection.')
para('Consistency of the initial data.', '<strong>Consistency of the initial data.</strong> Equation (B2) reproduces '+math(r'v_k')+' on every edge by construction. Once the lower trace is supplied, '+math(r'(u,\omega)')+' represents the prescribed physical fields '+math(r'(u,v)')+'. Changing the lower trace by '+math(r'\delta b')+' and repeating the recurrence adds '+math(r'\delta\omega_k=(-1)^k\delta b')+'. Its adjacent values sum to zero, so the reconstructed initial '+math(r'v_k')+' remains unchanged. This alternating auxiliary component can affect the subsequent evolution; the lower trace is therefore specified together with the physical initial data. All computations in Section 5 use the construction above.')
replace('The tight-solve row bounds the iteration error of the implicit scheme well below the reported discrepancies between integrators.', 'The tight-solve row shows that the terminal error norms change by less than the reported discrepancies between integrators when the stopping tolerance is reduced.')
p.write_bytes(s.encode('utf-8'))
doc=BeautifulSoup(s,'html.parser');old=BeautifulSoup(original.decode('utf-8'),'html.parser')
assert len(doc.find_all('figure'))==14 and len(doc.find_all('table'))==7
assert [str(x) for x in doc.find_all('figure')]==[str(x) for x in old.find_all('figure')]
assert not doc.select('.katex-error')
data={}
for case in ['A','D','Gaussian','Sinusoidal']:
 base=R/'Workspaces/dlw_paper_20261009/time_samm_20261025/time'
 a=json.loads((base/(case+'_time.json')).read_text())['integrators']['CN']['error']
 b=next(x for x in json.loads((base/(case+'_controls.json')).read_text())['controls'] if x['control']=='tight_solve')['error']
 data[case]=[abs(x-y) for x,y in zip(a,b)]
assert max(max(x) for x in data.values())<8e-10
(H/'validation.json').write_text(json.dumps(dict(changes=changes,cn_error_norm_changes=data,figures_unchanged=True,figures=14,tables=7),indent=2),encoding='utf-8')
print(json.dumps(data))
