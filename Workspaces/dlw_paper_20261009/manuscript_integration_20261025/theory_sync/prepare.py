"""Local synchronization of §§3.3–3.4 with the adopted natural §3.2.

Writes replacement sections only; it never writes the main manuscript.
"""
from pathlib import Path
import json, re, subprocess
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
source = (HERE.parent / 'before_dlw-paper.html').read_text(encoding='utf8')
paper = BeautifulSoup(source, 'html.parser')

def plain_section(section_id):
    sec = BeautifulSoup(str(paper.find(id=section_id)), 'html.parser').section
    for k in list(sec.select('.katex')):
        tex = k.find('annotation', encoding='application/x-tex').get_text().strip()
        display = k.parent.get('class') == ['katex-display']
        (k.parent if display else k).replace_with(('\\[' if display else '\\(') + tex + ('\\]' if display else '\\)'))
    return str(sec)

def once(s, a, b):
    assert s.count(a) == 1, (s.count(a), a)
    return s.replace(a, b)

s33 = plain_section('section-3.3')
s33 = once(s33, 'For Centered-SD, with U and w defined in (33),',
           'For Centered-SD, with the physical field \\(u\\) and logarithmic difference \\(\\omega\\) defined in Section 3.2,')
s33 = once(s33, r'A_k=\frac{U_{k-1}}2-\frac h8(w_{k-1}),\qquad' + '\n' + r'C_k=\frac{U_k}2+\frac h8(w_k)-h.',
           r'A_k=\frac{u_{k-1}-\omega_{k-1}}2,\qquad' + '\n' + r'C_k=\frac{u_k+\omega_k}2-h.')
s33 = once(s33, r'(r_{k-1})_x=\frac{U_{k-1}}2-\frac h8(w_{k-1}),\qquad' + '\n' + r'(R_k)_x=\frac{U_k}2+\frac h8(w_k),',
           r'(r_{k-1})_x=\frac{u_{k-1}-\omega_{k-1}}2,\qquad' + '\n' + r'(R_k)_x=\frac{u_k+\omega_k}2,')
start = s33.index('For Centered-SD, the corresponding combination is')
end = s33.index('</p>', start)
s33 = s33[:start] + r'''For Centered-SD, the corresponding combination is
\[
C_k-A_{k+1}=\omega_k-h.
\]
Subtracting the forward-shifted equation (48) from (49) therefore gives
\[
(\omega_k)_t+\partial_x[(u_k+2a)\omega_k-hu_k]-(\omega_k)_{xx}=0,
\]
which is (37). The potential relation (47), together with (39), becomes
\[
\Delta_hS_k=\partial_x\left[\Delta_hu_k+\frac{\omega_k+\omega_{k-1}}h\right]
=\frac12\partial_x(v_k+\Delta_hu_k).
\]
To recover the first physical-field equation, use \(u_k=2A_{k+1}+\omega_k\) and add the preceding \(\omega\) equation to twice the forward-shifted equation (48). This gives
\[
u_{k,t}=u_{k,xx}-\partial_x[H(u_k)+\omega_k^2/2-h\omega_k]-2(S_k)_x.
\]
Taking its lattice difference and substituting the relation for \(\Delta_hS_k\) yields the first equation in (35). Differentiating (39) in time and using (37) then yields the second. The recurrence (34) expresses every \(\omega_k\) through the physical fields and the specified lower trace.''' + s33[end:]

s34 = r'''<section id="section-3.4"><h3>3.4 Continuous limit and approximation of the physical fields</h3>
<p>We examine the nonlinear equations at the physical locations of their fields. Write the continuous residuals as
\[
\mathcal R_u=u_{yt}+v_{xx}+\partial_x[(u+2a)u_y],\qquad
\mathcal R_v=v_t+u_{xxy}+\partial_x[(u+2a)v-4u].\tag{50}
\]
Both representations place the first field at nodes and the second at edge midpoints. For Centered-SD, the nodes occupy the staggered locations specified in Section 3.2. To state its smooth-limit assumption, write \(W_k=4\omega_k/h\), so that (39) becomes \(v_k=\Delta_hu_k+\mathcal M_-W_k\), where \(\mathcal M_-W_k=(W_k+W_{k-1})/2\).</p>
<p><strong>Proposition 3.4 (Consistency on smooth branches).</strong> Let \(u\) and \(v\) be sufficiently smooth on a fixed compact region. Substituting their samples into Endpoint-SD gives
\[
\mathcal R_{\mathrm E,1}=\mathcal R_u+O(h^2),\qquad
\mathcal R_{\mathrm E,2}=\mathcal R_v+\frac h4\partial_x(v^2-u_y^2-8v)+O(h^2).\tag{51}
\]
For Centered-SD, assume the recurrence (34) selects a smooth reconstructed family with \(W=v-u_y+O(h^2)\), including the derivative bounds required in the equations. Then
\[
\mathcal R_{\mathrm C,1}=\mathcal R_u+O(h^2),\qquad
\mathcal R_{\mathrm C,2}=\mathcal R_v+O(h^2).\tag{52}
\]
The residuals are evaluated at the corresponding edge midpoint.</p>
<p><em>Proof.</em> Midpoint expansion gives \(\Delta_hU=u_y+h^2u_{yyy}/24+O(h^4)\) and \(\mathcal M_-U=u+h^2u_{yy}/8+O(h^4)\). The first Endpoint-SD equation therefore gives \(\mathcal R_u+O(h^2)\). In its second equation, the flux becomes
\[
(u+2a)v-4u+u_{xy}+\frac h4(v^2-u_y^2-8v)+O(h^2),
\]
which yields (51). For Centered-SD, the reconstruction has the expansion
\[
v=u_y+W+h^2\left(\frac{u_{yyy}}{24}+\frac{W_{yy}}8\right)+O(h^4).\tag{53}
\]
The extra flux in its first equation is \(\omega^2/2-h\omega=h^2(W^2/32-W/4)\). On the stated smooth family, its lattice difference and subsequent \(x\) derivative are \(O(h^2)\), so the first residual is \(\mathcal R_u+O(h^2)\). Scaling (37) gives \(W_t=W_{xx}-\partial_x[(u+2a)W-4u]\). Differentiating the reconstruction in time and using this equation, the right-hand side for \(v_t\) is
\[
-\partial_y\partial_xH(u)-v_{xx}
+(v-u_y)_{xx}-\partial_x[(u+2a)(v-u_y)-4u]+O(h^2)
=-u_{xxy}-\partial_x[(u+2a)v-4u]+O(h^2).
\]
This proves (52). ∎</p>
<p>The smooth-family assumption includes the lower trace in the reconstruction (34), together with the resulting spatial derivatives. For matched exact waves, this expansion follows from the Gram formulas.</p>
<p>Set \(P_i=p_i-a\), \(Q_j=q_j+a\). In the Centered-SD Gram family, choose \(z_i=P_i-h/2\), \(w_j^{\rm spec}=Q_j+h/2\), \(c_{ij}=\delta_{ij}\) and \(\alpha_i\beta_j=-\rho_i z_i/w_j^{\rm spec}\). The superscript identifies the spectral parameter. The \(x,t\) phase then agrees exactly with the continuous one, and the \(y\) phase rate is
\[
\frac1h\log\frac{(P_i+h/2)(Q_j+h/2)}{(P_i-h/2)(Q_j-h/2)}
=\frac1{P_i}+\frac1{Q_j}+O(h^2).
\]
At their respective staggered positions, the \(g\) amplitude agrees with the continuous amplitude, while the \(f\) amplitude differs by the factor \(\sqrt{(1-h^2/(4P_i^2))/(1-h^2/(4Q_j^2))}=1+O(h^2)\). For nonzero spectral denominators, sufficiently small \(h\), and positive tau functions bounded away from zero on the fixed region, the determinants and their required derivatives therefore differ from the continuous counterparts by \(O(h^2)\). Symmetric averaging in (33) gives \(u_h=u+O(h^2)\); applying the midpoint difference to the logarithmic potential gives \(v_h=\Delta_hZ_h=v+O(h^2)\). Thus both exact physical fields approximate their continuous counterparts at second order.</p>
<p>The extra flux also distinguishes the initial derivative errors of the two semi-discrete formulations. With common continuous physical samples and the same lower value of \(u_t\), subtracting their first equations and summing along the lattice gives
\[
(u_{k,t})_{\mathrm C}-(u_{k,t})_{\mathrm E}
=-\partial_x\left[\left(\frac{\omega_k^2}{2}-h\omega_k\right)-\left(\frac{\omega_0^2}{2}-h\omega_0\right)\right].
\]
On the smooth reconstructed family, this difference is \(O(h^2)\). The two formulations therefore share the second-order approximation of the first equation while retaining different leading derivative errors. This identity connects the nonlinear flux to the initial spatial comparisons in Section 5.2.</p>
</section>'''

sections = {'section-3.3': s33, 'section-3.4': s34}
forms=[]
def slot(match):
    display=match.group(1) is not None
    tex=match.group(1) if display else match.group(2)
    i=len(forms); forms.append({'tex':tex,'display':display})
    return 'THEORYMATH'+str(i)+'END'
templ={name:re.sub(r'\\\[(.*?)\\\]|\\\((.*?)\\\)',slot,text,flags=re.S) for name,text in sections.items()}
js="const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(f=>k.renderToString(f.tex,{displayMode:f.display,throwOnError:true,strict:'error'}))));"
r=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(forms),text=True,encoding='utf8',capture_output=True,check=True)
rendered=json.loads(r.stdout)
for name,html in templ.items():
    for i,value in enumerate(rendered):html=html.replace('THEORYMATH'+str(i)+'END',value)
    assert 'THEORYMATH' not in html
    (HERE/(name+'.html')).write_text(html,encoding='utf8')
    (HERE/(name+'.source.html')).write_text(sections[name],encoding='utf8')
alltex='\n'.join(f['tex'] for f in forms)
tags=re.findall(r'\\tag\{(\d+)\}',alltex)
assert tags==[str(i) for i in range(40,54)],tags
assert 'full-potential' not in ''.join(sections.values())
assert 'J\\partial_y' not in alltex
out={'status':'passed','formulas':len(forms),'numbered_equations':tags,'main_written':False,'mapping':'omega=h*w/4','changes':['Lax coefficients and recovery expressed in natural omega','bounded-primitive condition and primitive reconstruction removed','natural field consistency and exact Gram convergence retained with smoothness/positivity assumptions','shared first error coefficient replaced by exact extra-flux difference']}
(HERE/'validation.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out))
