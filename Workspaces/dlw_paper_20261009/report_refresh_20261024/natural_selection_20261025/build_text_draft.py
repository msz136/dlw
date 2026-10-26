"""Reader draft for natural Centered-SD; leaves the manuscript unchanged."""
from pathlib import Path
import csv,json,re,subprocess
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
REPORT=HERE.parent
CASES=['A','B','C','D','Gaussian','Sinusoidal']
METHODS=['Endpoint-SD','Centered-SD','FD']
maths=[]
def m(tex,display=False):
    token=f'MATHSLOT{len(maths)}END';maths.append(dict(tex=tex,display=display));return token
def eq(tex):return '<div class="equation">'+m(tex,True)+'</div>'
def sci(x,best=False):
    a,e=f'{x:.3e}'.split('e');s=f'{a} &times; 10<sup>{int(e)}</sup>'
    return '<strong>'+s+'</strong>' if best else s
def error_table(filename,keys,caption,id):
    rows=list(csv.DictReader((REPORT/filename).open(encoding='utf-8-sig',newline='')))
    mk='method' if 'method' in rows[0] else 'space'
    s=f'<div class="table-wrap"><table id="{id}"><caption>{caption}</caption><thead><tr><th rowspan="2">Case</th>'
    s+=''.join('<th colspan="2">'+v+'</th>' for v in METHODS)+'</tr><tr>'
    fields=['E_{u_t}','E_{v_t}'] if 'initial' in id else ['E_u','E_v']
    s+=''.join('<th>'+m(v)+'</th>' for method in METHODS for v in fields)+'</tr></thead><tbody>'
    for c in CASES:
        pairs=[[float(next(r for r in rows if r['case']==c and r[mk]==method)[key]) for key in keys] for method in METHODS]
        best=[min(v[j] for v in pairs) for j in range(2)]
        s+='<tr><th>'+c+'</th>'
        for pair in pairs:
            for j,x in enumerate(pair):s+=f'<td data-value="{x:.17g}">'+sci(x,f'{x:.3e}'==f'{best[j]:.3e}')+'</td>'
        s+='</tr>'
    return s+'</tbody></table></div>'

body=f'''<header><p class="meta">Proposed numerical text · 25 October 2026</p><h1>Numerical formulation and experiments</h1><nav><a href="#section-4.1">Numerical formulation</a> · <a href="#section-5.1">Test problems and exact profiles</a> · <a href="#section-5.2">Results and comparisons</a></nav></header>
<section id="section-4.1"><h2>4.1 Fourier differentiation and spatial formulations</h2>
<p>We apply the same Fourier differentiation in {m('x')} to Endpoint-SD, Centered-SD and FD. The operators {m(r'\mathcal D_x')} and {m(r'\mathcal D_{xx}')} have multipliers {m(r'\mathrm i\xi')} and {m(r'-\xi^2')}, respectively. The first-derivative multiplier is set to zero at the Nyquist frequency. Products are evaluated at the grid points. These calligraphic operators denote numerical differentiation and are distinct from Hirota's bilinear derivatives.</p>
<p>Write {m(r'H(u)=u^2/2+2au')}, {m(r'\Delta_hq_k=(q_k-q_{k-1})/h')}, {m(r'\mathcal M_-q_k=(q_k+q_{k-1})/2')} and {m(r'\delta_0q_k=(q_{k+1}-q_{k-1})/(2h)')}. Recalling the physical-field equations (27)–(28), Endpoint-SD takes the form</p>
{eq(r'\begin{aligned}\Delta_h\dot u_k&=-\mathcal D_x\Delta_hH(u_k)-\mathcal D_{xx}v_k,\\\dot v_k&=-\mathcal D_x[(\mathcal M_-u_k+2a-2h)v_k+hv_k^2/4-4\mathcal M_-u_k-h(\Delta_hu_k)^2/4]-\mathcal D_{xx}\Delta_hu_k.\end{aligned}')}
<p>For Centered-SD, the field definition in Section 3.2 gives {m(r'v_k=\Delta_hu_k+2(\omega_k+\omega_{k-1})/h')}. We retain this relation in the numerical formulation. The equations for the time derivatives are</p>
{eq(r'\begin{aligned}\Delta_h\dot u_k&=-\mathcal D_x\Delta_h[H(u_k)+\omega_k^2/2-h\omega_k]-\mathcal D_{xx}v_k,\\\dot\omega_k&=\mathcal D_{xx}\omega_k-\mathcal D_x[(u_k+2a)\omega_k-hu_k],\\\dot v_k&=\Delta_h\dot u_k+\frac2h(\dot\omega_k+\dot\omega_{k-1}).\end{aligned}')}
<p>The first equation is summed from the prescribed lower value of {m(r'\dot u')}. Advancing {m(r'(u,\omega)')} and recovering {m('v')} through the field relation implements the physical-field equations of Proposition 3.2. The same differentiated relation supplies {m(r'\dot v')} when measuring the initial spatial error.</p><p>For comparison, direct discretization of the continuous DLW system gives the FD baseline,</p>
{eq(r'\begin{aligned}\Delta_h\dot u_k&=-\mathcal D_x\Delta_hH(u_k)-\mathcal D_{xx}\mathcal M_-v_k,\\\dot v_k&=-\mathcal D_x[(u_k+2a)v_k-4u_k]-\mathcal D_{xx}\delta_0u_k.\end{aligned}')}
<p>These equations use the same Fourier operators and lower derivative data as the two semi-discrete formulations. The location of the physical fields and the discrete nonlinear fluxes determine their different spatial approximations.</p></section>
<section id="section-4.2"><h2>4.2 Initial data and time advancement</h2>
<p>The initial physical fields are sampled from the continuous reference solution at their respective lattice locations. For Centered-SD, we initialize {m(r'\omega_0=h(v^*-u_y^*)/4')} at the lower node and determine the remaining auxiliary values through</p>
{eq(r'\omega_k=\frac h2(v_k-\Delta_hu_k)-\omega_{k-1}.')}
<p>This is the linear reconstruction in (34), and it reproduces the prescribed initial {m('v')} at each internal edge. During time advancement, the lower auxiliary value evolves with the same {m(r'\omega')} equation as the interior values. The lower value of {m('u_t')} and the exterior field values required by each spatial formulation are evaluated from the continuous reference solution at every time stage.</p>
<p>In the comparisons below, classical fourth-order Runge–Kutta advances the numerical state from {m('t=0')} to {m('T=0.01')} with {m(r'\Delta t=10^{-4}')}. Endpoint-SD and FD advance {m('(u,v)')}; Centered-SD advances {m(r'(u,\omega)')} and evaluates the physical field {m('v')} from its lattice relation.</p></section>
<section id="section-5"><h2>5. Numerical experiments</h2>
<p>We use six wave problems to examine how the spatial formulation affects the accuracy of the physical fields. Four exact soliton solutions provide localized profiles and interacting waves, while Gaussian and sinusoidal initial data extend the comparison to two further smooth wave families. We first evaluate the numerical time derivatives at the initial state, where the difference from the continuous derivatives measures the spatial discretization error. The same initial fields are then advanced with RK4 to examine how these differences develop in the coupled evolution of {m('u')} and {m('v')}.</p>
<section id="section-5.1"><h3>5.1 Test problems and error measures</h3>
<p>All tests use {m(r'a=2')} and {m(r'\lambda=-2')}. The four soliton references are obtained from the continuous Gram determinant solutions in Section 2.1. We take {m(r'\rho_i=1')} and zero phase shifts. Cases A and B contain one soliton, and Cases C and D contain two solitons. In particular, Case D combines the spectral pairs used separately in A and B.</p>
<div class="table-wrap"><table id="table-parameters"><caption>Table 1. Spectral parameters and regions for the soliton tests.</caption><thead><tr><th>Case</th><th>Wave</th><th>Spectral pairs</th><th>Region</th><th>Periodic x interval</th></tr></thead><tbody>
<tr><th>A</th><td>One soliton</td><td>(1, 2)</td><td>R = 5</td><td>[−10, 10)</td></tr><tr><th>B</th><td>One soliton</td><td>(4, −3)</td><td>R = 10</td><td>[−20, 20)</td></tr><tr><th>C</th><td>Two solitons</td><td>(6, −5), (4, −3)</td><td>R = 30</td><td>[−40, 40)</td></tr><tr><th>D</th><td>Two solitons</td><td>(1, 2), (4, −3)</td><td>R = 30</td><td>[−40, 40)</td></tr></tbody></table></div>
<p>The regions contain the principal wave profiles, and the computational boundaries are placed farther out. Writing the periodic interval as {m('[-L,L)')}, we use the same interval in {m('y')}. Errors are measured at the native field locations satisfying {m(r'|x|\le R')} and {m(r'|y|<R')}. Both semi-discrete formulations place {m('u')} at nodes and {m('v')} at edge midpoints, whereas FD places both fields at nodes.</p>
<p>For the Gaussian and sinusoidal tests, let {m(r'z=y+2')} and {m(r'\kappa=\pi/4')}. The initial fields are</p>
{eq(r'u_0(x,y)=A\sin(\kappa z)F(x),\qquad v_0(x,y)=4-3A\kappa\cos(\kappa z)F(x).')}
<p>The Gaussian test uses {m('A=0.05')} and the periodic profile {m(r'F(x)=\sum_{j\in\mathbb Z}\exp[-((x+192j)/6)^2]')}. The sinusoidal test uses {m('A=0.03')} and {m(r'F(x)=\cos(\pi x/12)')}. Both are computed on the periodic interval {m(r'x\in[-96,96)')} with {m(r'y\in[-2,2]')} and lower boundary {m('u=0')}. Their errors are measured over all {m('x')} nodes and native field locations with {m(r'|y|\le1.8')}.</p>
<p>For these two initial-value problems, two linear heat equations and a Laplace transformation provide the continuous reference fields throughout {m(r'0\le t\le0.01')}. The initial relation {m(r'v_0=4-3u_{0y}')} specifies the data; the reference fields subsequently evolve according to the full DLW system. Interval evaluation gives an absolute error bound of {m(r'10^{-13}')} for every initial derivative and terminal field value used in the comparisons.</p>
<p>Each method starts from the same continuous physical fields. Let {m(r'\dot u_h(0),\dot v_h(0)')} denote the time derivatives produced by its spatial formulation at this state. We measure the initial derivative errors by</p>
{eq(r'E_{u_t}=\max_{\mathcal G_u}|\dot u_h(0)-u_t^*(0)|,\qquad E_{v_t}=\max_{\mathcal G_v}|\dot v_h(0)-v_t^*(0)|.')}
<p>Here {m(r'\mathcal G_u')} and {m(r'\mathcal G_v')} contain the native field locations in the specified region. The continuous derivatives are evaluated analytically. After time advancement, the corresponding field errors are</p>
{eq(r'E_u(T)=\max_{\mathcal G_u}|u_h(T)-u^*(T)|,\qquad E_v(T)=\max_{\mathcal G_v}|v_h(T)-v^*(T)|.')}
<p>These measurements follow the two physical fields from the spatial error introduced at the initial state to the error accumulated during evolution. Bold entries identify the smallest error for each case and component.</p></section>
<section id="section-5.2"><h3>5.2 Comparison of spatial formulations</h3>
<p>We fix {m(r'h=\Delta x=0.1')} and compare Endpoint-SD, Centered-SD and FD under the same spatial resolution. Table 2 reports the initial time-derivative errors. This first comparison evaluates each spatial formulation on prescribed continuous data before the fields have accumulated evolution error.</p>
{error_table('table1_initial_derivative_errors.csv',['error_ut','error_vt'],'Table 2. Initial time-derivative errors at h = Δx = 0.1.','table-initial')}
<p>Endpoint-SD gives the smallest {m('u_t')} error in all six tests. Centered-SD substantially reduces the {m('v_t')} error relative to Endpoint-SD, by factors ranging from approximately 60 to 125. Compared with FD, Centered-SD gives the smallest {m('v_t')} errors in A, D, Gaussian and sinusoidal tests; FD gives the smallest values in B and C. The two fields therefore respond differently to the choice of spatial formulation.</p>
<p>The difference in the first component follows from the flux in Section 3.2. Centered-SD retains {m(r'Q_k=\omega_k^2/2-h\omega_k')} in its first equation. For common initial physical fields and the same lower value of {m('u_t')}, summing the first equations of the two semi-discrete formulations gives</p>
{eq(r'\dot u_k^{\mathrm C}-\dot u_k^{\mathrm E}=-\mathcal D_x(Q_k-Q_0).')}
<p>The auxiliary quantity {m(r'\omega')} scales with {m('h')} for smooth fields, so this flux contributes at second order. It changes the leading error in {m('u_t')}, while the centered field reconstruction also changes the approximation of {m('v_t')}. The initial table records both effects: the smaller first-component error of Endpoint-SD and the substantial reduction in the second component obtained with Centered-SD.</p>
<p>We next advance all three formulations to {m('T=0.01')} using RK4 with {m(r'\Delta t=10^{-4}')}. The spatial grids, initial physical fields and reference solutions remain the same. Table 3 measures how the errors develop when the two fields evolve together.</p>
{error_table('table2_final_field_errors.csv',['error_u','error_v'],'Table 3. Physical-field errors at T = 0.01 with RK4, Δt = 10⁻⁴ and h = Δx = 0.1.','table-final')}
<p>For the Gaussian and sinusoidal tests, the terminal errors closely follow the initial derivative errors. Across all three formulations and both fields, {m(r'E_u(T)/(T E_{u_t})')} and {m(r'E_v(T)/(T E_{v_t})')} differ from one by at most {m(r'0.43\%')}. Thus the initial derivative defects quantitatively explain the short-time error levels in these two examples. Centered-SD gives {m('v')} errors of {m(r'6.967\times10^{-9}')} and {m(r'4.706\times10^{-9}')}, approximately 3.2 and 3.5 times smaller than FD. Its {m('u')} errors lie between the Endpoint-SD and FD values, as in the initial derivative comparison.</p>
<p>The ranking of the u errors changes during the soliton evolution. In A and D, Centered-SD reduces the terminal {m('v')} error relative to Endpoint-SD by factors of about 72 and 70. Its terminal {m('u')} error is also smaller, by factors of approximately 2.8, even though Endpoint-SD started with the smaller {m('u_t')} error. The first equation explains how the two components interact: the evolving {m('v')} field enters the equation for {m('u')} through {m('-v_{xx}')}. Its error therefore contributes to the subsequent evolution of {m('u')}, alongside the initial error in u_t.</p>
<p>In C, Endpoint-SD gives the smallest terminal {m('u')} error and FD the smallest {m('v')} error. Case B has the largest terminal errors for all three formulations, with {m('u')} errors between 0.163 and 0.168 and {m('v')} errors between 0.0338 and 0.0341. The close grouping of these values shows that changing the spatial formulation has a comparatively small effect on the large error accumulated in this case.</p>
<p>The centered field definition is particularly effective for the second component in A, D and the two smooth non-soliton tests. The initial and terminal comparisons show how this improvement enters the coupled computation: it persists directly in the short-time Gaussian and sinusoidal errors, and accompanies an improvement in both fields relative to Endpoint-SD in A and D. The accuracy of the physical wave is therefore determined by the errors in both equations and their interaction during evolution.</p>
</section></section>
<footer><a href="../Report.html">Numerical tables</a> · <a href="../Workspaces/dlw_paper_20261009/report_refresh_20261024/natural_selection_20261025/scientific_analysis.json">Quantitative analysis</a> · <a href="../Workspaces/dlw_paper_20261009/report_refresh_20261024/nondegenerate_rk4_20261024/reference_certificate.json">Reference evaluation bounds</a></footer>'''

style='''body{max-width:1160px;margin:40px auto;padding:0 28px;color:#18212b;background:#fff;font:17px/1.8 Georgia,"Times New Roman",serif}h1{font-size:30px}h2{font-size:25px;margin-top:42px}h3{font-size:21px;margin-top:32px}p{margin:16px 0}.meta,footer{font:14px/1.6 Arial,sans-serif;color:#52606d}.equation{overflow-x:auto;margin:20px 0}.table-wrap{overflow-x:auto;margin:28px 0}table{width:100%;border-collapse:collapse;border-top:2px solid #18212b;border-bottom:2px solid #18212b;font-size:14px;line-height:1.5;font-variant-numeric:tabular-nums}caption{text-align:left;font-size:16px;padding-bottom:12px}thead{border-bottom:1px solid #18212b}th,td{padding:11px 9px}thead th{text-align:center;font-weight:500}tbody th{text-align:left}td{text-align:right;white-space:nowrap}sup{font-size:.7em}a{color:#284e6b}footer{border-top:1px solid #ccd2d7;margin-top:38px;padding-top:16px}.katex{font-size:1.02em}@media print{body{font-size:11pt;max-width:none;margin:0}table{font-size:8pt}tr{break-inside:avoid}h2,h3{break-after:avoid}footer{display:none}}'''
from illustrate_text import illustrate
body=illustrate(body)
style+='nav{font:14px/1.8 Arial,sans-serif;margin:18px 0}figure{margin:30px 0 36px}figure img{display:block;width:100%;height:auto}figcaption{font-size:14px;line-height:1.65;margin-top:12px}.export{font:12px Arial,sans-serif;margin-left:8px}h4{font-size:19px;margin:32px 0 12px}h5{font-size:18px;margin:32px 0 10px}details{margin:35px 0;border-top:1px solid #ccd2d7;padding-top:18px}summary{cursor:pointer;font-size:19px}figure{break-inside:avoid}.figure-link{font-size:14px}'
html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW numerical text: natural Centered-SD</title><link rel="stylesheet" href="../Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css"><style>'+style+'</style></head><body>'+body+'</body></html>'
js="const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(f=>k.renderToString(f.tex,{displayMode:f.display,throwOnError:true,strict:'error'}))));"
r=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(maths),text=True,encoding='utf8',capture_output=True,check=True)
for i,value in enumerate(json.loads(r.stdout)):html=html.replace(f'MATHSLOT{i}END',value)
assert 'MATHSLOT' not in html and 'katex-error' not in html
path=ROOT/'report/dlw_numerical_text_20261025.html';path.write_text(html,encoding='utf8')
print('Wrote',path,'formulas',len(maths))
