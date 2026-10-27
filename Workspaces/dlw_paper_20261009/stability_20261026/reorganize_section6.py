"""Keep all perturbation/stability material in Section 6, per user direction."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re
import subprocess
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PAPER=ROOT/'dlw-paper.html'
pub=json.loads((HERE/'publication_validation.json').read_text())
original=(Path(pub['backup'])/'dlw-paper.html').read_text(encoding='utf-8')
before=PAPER.read_bytes()
src=before.decode('utf-8')
assert hashlib.sha256(before).hexdigest()==pub['after_sha256'], 'Main paper changed; review before editing.'

def outer(text,ident):
    start=re.search(r'<section\b[^>]*\bid="'+re.escape(ident)+r'"[^>]*>',text).start()
    depth=0
    for tag in re.finditer(r'<section\b[^>]*>|</section>',text[start:]):
        depth += -1 if tag[0].startswith('</') else 1
        if depth==0:
            return text[start:start+tag.end()]
    raise ValueError(ident)

maths=[]
def m(t,display=False):
    token=f'S6MATH{len(maths)}END'; maths.append(dict(tex=t,display=display)); return token
def p(t):
    a=t.split('$');assert len(a)%2==1
    return '<p>'+''.join(m(x) if i%2 else x for i,x in enumerate(a))+'</p>\n'
def eq(t):return '<div class="equation">'+m(t,True)+'</div>\n'

intro=p(r'We now examine how independent changes in the initial physical fields propagate through the coupled evolution. The analysis connects the spatial growth branches, the transverse integration imposed by the boundary closure, and the accuracy required of a continuous reference solution. Section 6.1 derives the constant-background response of the current Centered-SD formulation. Section 6.2 follows independent $u$ and $v$ perturbations on the four wave backgrounds, and Section 6.3 examines the continuous reference problem for these perturbed data.')

s63='<section id="section-6.3"><h3>6.3 Continuous reference solutions and error certification</h3>\n'
s63+=p(r'To compare a perturbed numerical trajectory with the continuous equation, the reference solution must satisfy the same perturbed initial fields. For the Gaussian and sinusoidal strip, the lower trace is $u=0$. With $X=x-4t$, $z=y+2\in[0,4]$, and $A=u_y+v-4$, $B=v-u_y-4$, the full nonlinear equations take the form')
s63+=eq(r'A_t=-A_{XX}-(uA)_X,\qquad B_t=B_{XX}-(uB)_X,\qquad u(X,z,t)=\frac12\int_0^z(A-B)(X,s,t)\,ds.')
s63+=p(r'Independent physical-field perturbations change the two initial components by $\delta A_0=\delta u_{0,y}+\delta v_0$ and $\delta B_0=\delta v_0-\delta u_{0,y}$. The equation for $A$ has a backward heat principal part. A useful construction therefore prescribes $G=A(T)$ and $H=B(0)$ and solves the resulting mixed initial–terminal problem. Both heat operators then act in their smoothing direction in the integral equations.')
s63+=p(r'This mixed problem admits a quantitative small-data estimate. Use the analytic Fourier norm $\|f\|_\rho=\sum_n e^{\rho|\xi_n|}\sup_{z,t}|f_n(z,t)|$, with the time supremum omitted for the data. The differentiated heat integral is bounded by $\gamma_T=\sqrt{T/2}$, multiplication is bounded in the same norm, and $\|u\|_\rho\le2\|(A,B)\|_\rho$. For data satisfying $\|G\|_\rho+\|H\|_\rho\le0.3$, the mixed integral map $\mathcal T$ on the ball of radius $R=0.4$ consequently satisfies, at $T=0.01$,')
s63+=eq(r'\|\mathcal T(A,B)\|_\rho\le0.3+2\gamma_T R^2<0.322628,\qquad\operatorname{Lip}(\mathcal T)\le4\gamma_T R<0.113138.')
s63+=p(r'The contraction gives a unique mixed solution in this ball. For the independently specified initial fields, the terminal function $G$ must additionally solve')
s63+=eq(r'F_H(G)=A_G(0)=A_0^{\varepsilon},\qquad H=B_0^{\varepsilon}.')
s63+=p(r'The distinction is significant for accuracy. At the constant background, the matching derivative has Fourier multiplier $e^{-T\xi^2}$, so an initial coefficient error is amplified by $e^{T\xi^2}$ when propagated to the terminal unstable component. At a nonzero background, the derivative also contains the coupled terms $\delta u\,\bar A$ and $\delta u\,\bar B$. These terms transfer information between Fourier modes and must be retained when bounding the inverse matching problem.')
s63+=p(r'For the present Gaussian and sinusoidal data, the first coefficient of the matching correction in the background and perturbation amplitudes can be computed explicitly. Its Gaussian Fourier tail has a finite analytic bound. Completing the reference estimate requires controlling all higher corrections and the inverse on the unresolved modes, together with spatial-domain errors for the soliton problems. Those estimates have not yet been established for the independently perturbed data. The response measurements in Section 6.2 therefore remain finite-grid perturbation diagnostics, while the mixed-problem estimate identifies the initial matching that a continuous error certificate must resolve.')
s63+='</section>'

js=("const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(x=>k.renderToString(x.tex,{displayMode:x.display,throwOnError:true,strict:'error'}))));")
r=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(maths),text=True,encoding='utf-8',capture_output=True,check=True)
rendered=json.loads(r.stdout)
def render(t):return re.sub(r'S6MATH(\d+)END',lambda x:rendered[int(x[1])],t)
intro,s63=render(intro),render(s63)

s61=(HERE/'section44.html').read_text(encoding='utf-8').replace('section-4.4','section-6.1').replace('4.4 Linearized','6.1 Linearized')
s62=(HERE/'section55.html').read_text(encoding='utf-8').replace('section-5.5','section-6.2').replace('5.5 Independent','6.2 Independent').replace('Section 4.4','Section 6.1')
s62=s62.replace('An error relative to the independently perturbed continuous solution additionally requires a reference bound for that initial-value problem; such a bound remains open here.','Section 6.3 considers the continuous reference problem for the same independent initial data.')
s6='<section id="section-6" class="numerical-section"><h2>6. Perturbation dynamics and reference accuracy</h2>\n'+intro+s61+'\n'+s62+'\n'+s63+'\n</section>'

# Restore the original introduction and numerical-section overviews.
for ident in ('section-1','section-4','section-5'):
    restored=outer(original,ident)
    if ident=='section-4':
        restored=restored.replace(outer(restored,'section-4.4'),'')
        restored=restored.replace('4. Numerical formulation and linear stability','4. Numerical formulation')
    if ident=='section-5':
        restored=restored.replace(outer(restored,'section-5.5'),'')
    src=src.replace(outer(src,ident),restored,1)

conclusion=outer(original,'section-6')
conclusion7=conclusion.replace('id="section-6"','id="section-7"',1).replace('<h2>6. Conclusions</h2>','<h2>7. Conclusions</h2>',1)
src=src.replace(outer(src,'section-6'),s6+'\n'+conclusion7,1)
src=src.replace('4. Numerical formulation and linear stability</a>','4. Numerical formulation</a>',1)
src=src.replace('<a href="#section-6">6. Conclusions</a>',
    '<a href="#section-6">6. Perturbation dynamics and reference accuracy</a>'
    '<a class="subsection" href="#section-6.1">6.1 Linearized evolution under the numerical closure</a>'
    '<a class="subsection" href="#section-6.2">6.2 Independent physical-field perturbations</a>'
    '<a class="subsection" href="#section-6.3">6.3 Continuous reference solutions and error certification</a>'
    '<a href="#section-7">7. Conclusions</a>',1)
assert 'id="section-4.4"' not in src and 'id="section-5.5"' not in src
backup=HERE/('before_section6_'+datetime.now().strftime('%Y%m%d_%H%M%S'));backup.mkdir()
(backup/'dlw-paper.html').write_bytes(before)
assert PAPER.read_bytes()==before, 'Concurrent paper edit detected.'
PAPER.write_text(src,encoding='utf-8')
(HERE/'section6.html').write_text(s6,encoding='utf-8')

report=ROOT/'report/dlw_independent_stability_20261026.html'
rt=report.read_text(encoding='utf-8').replace('../dlw-paper.html#section-4.4','../dlw-paper.html#section-6.1').replace('主论文 §4.4','主论文 §6.1').replace('../dlw-paper.html#section-5.5','../dlw-paper.html#section-6.2').replace('主论文 §5.5','主论文 §6.2')
report.write_text(rt,encoding='utf-8')

new,old=BeautifulSoup(src,'html.parser'),BeautifulSoup(original,'html.parser')
assert str(new.find('section',id='abstract'))==str(old.find('section',id='abstract'))
assert outer(src,'section-1')==outer(original,'section-1')
assert outer(src,'section-7')==conclusion7
assert len(new.find_all('figure'))==29 and len(new.find_all('table'))==7
assert not new.select('.katex-error')
for ident in ('section-4.1','section-4.2','section-4.3','section-5.1','section-5.2','section-5.3','section-5.4'):
    assert outer(src,ident)==outer(original,ident),ident
ids=[x['id'] for x in new.select('[id]')]; assert len(ids)==len(set(ids))
badlinks=[a['href'] for a in new.find_all('a',href=True) if a['href'].startswith('#') and a['href'][1:] not in ids]
assert not badlinks,badlinks
manifest=dict(date='2026-10-26',section6_title='Perturbation dynamics and reference accuracy',
    subsections=['6.1 Linearized evolution under the numerical closure','6.2 Independent physical-field perturbations','6.3 Continuous reference solutions and error certification'],
    figures=29,tables=7,existing_numerical_subsections_unchanged=True,
    abstract_unchanged=True,introduction_unchanged=True,conclusion_body_unchanged=True,
    conclusion_number=7,roadmap_content_deliberately_not_aligned=True,
    before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest(),
    backup=str(backup),continuous_perturbed_reference_certified=False,eta_u=None,eta_v=None,
    report=str(report),katex_errors=0,missing_internal_links=badlinks)
(HERE/'section6_validation.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
