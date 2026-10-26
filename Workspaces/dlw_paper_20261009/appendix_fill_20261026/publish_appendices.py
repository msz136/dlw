"""Write Appendices A-D and remove the editorial guide (Appendix G)."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAPER = ROOT / 'dlw-paper.html'
BASELINE = HERE / 'before/dlw-paper.html'

maths = []


def m(tex, display=False):
    token = 'APMATH' + str(len(maths)) + 'END'
    maths.append(dict(tex=tex, display=display))
    return token


def eq(tex):
    return '<div class="equation">' + m(tex, True) + '</div>'


def render(text):
    js = ("const fs=require('fs'),k=require(process.argv[1]);"
          "process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8'))"
          ".map(f=>k.renderToString(f.tex,{displayMode:f.display,throwOnError:true,strict:'error'}))));")
    katex = ROOT / 'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js'
    r = subprocess.run(['node', '-e', js, str(katex)], input=json.dumps(maths), text=True,
                       encoding='utf-8', capture_output=True, check=True)
    for i, result in enumerate(json.loads(r.stdout)):
        text = text.replace('APMATH' + str(i) + 'END', result)
    return text


source = BASELINE.read_text(encoding='utf-8')

# ------------------------------------------------------------------ Appendix A
A = f"""<section id="appendix-A"><h2>Appendix A. Determinant identities and alternative solution representations</h2>
<p>Every field used in the main text is a logarithmic derivative of a {m(r'\tau')} function, so its evaluation reduces to an identity for a determinant and for the derivatives of that determinant. This appendix records the three identities on which the reconstruction rests, together with the relation between the two determinant families and the explicit low-order members.</p>
<p><strong>Rank-one identity.</strong> Let {m(r'M(\theta)=M_0+\theta\,r\,c^{\mathsf T}')} with {m(r'M_0')} invertible and {m(r'r,c')} column vectors. Factoring {m(r'M_0')} out of the rows of {m(r'M(\theta)')} gives</p>
{eq(r'\det M(\theta)=\det M_0\left(1+\theta\,c^{\mathsf T}M_0^{-1}r\right),\qquad \partial_\theta\log\det M(\theta)=c^{\mathsf T}M^{-1}r .\tag{A1}')}
<p>The second form follows from the first together with the Sherman&ndash;Morrison formula for {m(r'M^{-1}')}, and it is the only identity needed to differentiate a determinant in a parameter that enters linearly.</p>
<p><strong>Shift identity.</strong> The two families (20) and (22) differ only in their phases. Writing {m(r'\xi_i+\eta_j=(z_i+w_j)[x-2at+(w_j-z_i)t]')} for the Endpoint family, the additional factor {m(r'e^{-h(z_i+w_j)t}')} in (22) replaces {m(r'a')} by {m(r'a+h/2')} in the same exponent. Hence</p>
{eq(r'\tau_n^{\mathrm C}(k;h)=\tau_n^{\mathrm E}(k;h)\big|_{a\to a+h/2},\tag{A2}')}
<p>so the two determinant families share their minors and their positivity, and only the reference value of the bilinear parameter changes. This is the determinant counterpart of the shift introduced in Section 2.3, and it is why the centered pairings carry {m(r'a\pm h/2')}.</p>
<p><strong>Logarithmic fields.</strong> With {m(r'f_k=\tau_0(k)')} and {m(r'g_k=\tau_1(k)')} the definitions (26) and (33) become ratios of neighbouring determinants,</p>
{eq(r'U_k=2\partial_x\log\frac{\tau_0(k)}{\tau_1(k)},\qquad V_k=\frac2h\partial_x\log\frac{\tau_0(k)\tau_1(k)}{\tau_0(k-1)\tau_1(k-1)},\tag{A3}')}
<p>and analogously for {m(r'u_k')}, {m(r'v_k')} through (33). Smoothness of the fields is therefore equivalent to positivity of the {m(r'\tau')} functions, which Proposition 2.3 guarantees on the class (24). The same argument applies to the derivatives: since the phase factors are positive on that class, every principal minor of {m(r'M-C')} keeps the sign of the corresponding Cauchy minor (25), and the cofactor identity {m(r'\det M\,(M^{-1})_{ij}=\mathrm{cof}_{ij}M')} shows that the first minors inherit this sign. The reconstructed fields and their {m(r'x')} derivatives are consequently bounded on the region away from the lattice boundary.</p>
<p><strong>Low-order members.</strong> For {m(r'N=1')} with {m(r'c_{11}=1')}, writing {m(r'A=\alpha\beta/(z+w)')} gives {m(r'\tau_n(k)=1+A(-w/z)^nL(h)^k e^{\xi+\eta}')}. Substitution into (A3) reproduces the standard one-soliton field at the node and edge locations, and the two-soliton case used in Section 5 is the same formula with a {m(r'2\times2')} Cauchy matrix. The family with {m(r'c_{ij}=\delta_{ij}')} is the Gram reduction of the usual Casoratian determinants of the hierarchy [15]; we use the Gram form throughout because the Miwa expansion acts on it directly.</p>
</section>"""

# ------------------------------------------------------------------ Appendix B
B = f"""<section id="appendix-B"><h2>Appendix B. Field transformations and reconstruction conditions</h2>
<p>The numerical state of Centered-SD is the pair {m(r'(u_k,\omega_k)')}, whereas the physical comparison is made in the fields {m(r'(u,v)')}. This appendix records the two transformations between them, the conditions under which they are equivalent, and the lower trace required by the computation.</p>
<p><strong>Field relation and recurrence.</strong> The definitions (33) imply, for every edge,</p>
{eq(r'v_k-\Delta_hu_k=\frac2h\left(\omega_k+\omega_{k-1}\right),\qquad \omega_k=\partial_x\log\frac{g_k}{g_{k-1}},\tag{B1}')}
<p>where the second expression shows that {m(r'\omega_k')} is the lattice difference of the logarithmic potential and therefore carries a factor {m(r'h')} relative to {m(r'v-u_y')}. Rearranging (B1) gives the reconstruction (34),</p>
{eq(r'\omega_0=b,\qquad \omega_k=\frac h2\left(v_k-\Delta_hu_k\right)-\omega_{k-1},\qquad k=1,\dots,N .\tag{B2}')}
<p>The recurrence is linear and lower triangular, so it determines {m(r'(\omega_1,\dots,\omega_N)')} uniquely from the physical fields and the single lower value {m(r'b')}. Its solution is</p>
{eq(r'\omega_k=(-1)^k b+\frac h2\sum_{j=1}^{k}(-1)^{k-j}\left(v_j-\Delta_hu_j\right),\tag{B3}')}
<p>in which the coefficients have modulus one. No amplification of the lower data or of the edge differences is possible in this step, and no branch selection is involved: the map is an exact affine relation, not a nonlinear inversion.</p>
<p><strong>Conditions on the lower trace.</strong> For the {m(r'\tau')} functions of Theorem 2.1 the compatible trace is fixed by the lattice, namely {m(r'b=\partial_x\log(g_0/g_{-1})')}. In a computation the data are prescribed in the physical fields, so the trace is taken instead from the continuous reference, {m(r'\omega_0=h(v^*-u_y^*)/4')} evaluated at the lower node. The two agree to {m(r'O(h^2)')} on the smooth class of Section 3.4, and the resulting discrepancy enters (B3) with alternating sign only, that is without growth along the layer index. During the evolution the lower value is advanced by the same equation as the interior, so the trace is not frozen.</p>
<p><strong>Consistency of the initial data.</strong> Because (B2) reproduces {m(r'v_k')} on every edge by construction, the pair {m(r'(u,\omega)')} carries the same information as {m(r'(u,v)')} as soon as the lower trace is supplied. The only requirement on initial data is that {m(r'\omega')} be obtained from the same physical field that defines the state; mixing a trace computed from a different field produces an {m(r'O(1)')} mismatch in the lowest edge, which (B3) propagates upward undamped. All computations in Section 5 use the single construction above.</p>
</section>"""

# ------------------------------------------------------------------ Appendix C
C = f"""<section id="appendix-C"><h2>Appendix C. Operator compatibility and continuum expansions</h2>
<p>Two computations are compressed in the main text: the reduction of the compatibility condition (42) to scalar coefficient relations, and the expansions that yield the residuals (51)&ndash;(53). We record both.</p>
<p><strong>Coefficient form of the compatibility condition.</strong> Expanding {m(r'L_t+LM-\widetilde ML')} with the rules {m(r'Dq=qD+q_x')} and {m(r'Yq_k=q_{k-1}Y')} produces terms proportional to {m(r'DY')}, {m(r'Y')}, {m(r'D')} and {m(r'D^0')}. The coefficients of {m(r'DY')}, {m(r'Y')} and {m(r'D^0')} vanish by (47), (48) and (49), respectively, and the coefficient of {m(r'D')} vanishes identically. Since {m(r'L')} and {m(r'M')} are at most second order in {m(r'D')}, the compatibility condition (42) is therefore equivalent to those three scalar relations.</p>
<p><strong>Midpoint expansions.</strong> For smooth {m(r'q')} sampled at the nodes and edges of the lattice,</p>
{eq(r'\Delta_hq_k=q_y+\frac{h^2}{24}q_{yyy}+O(h^4),\qquad \mathcal M_-q_k=q+\frac{h^2}{8}q_{yy}+O(h^4),\tag{C1}')}
<p>evaluated at the edge midpoint. Substituting (C1) into the first Endpoint-SD equation gives {m(r'\mathcal R_u+O(h^2)')}, since both the difference and the average are second-order accurate there. The second equation carries an additional term from the flux. Expanding its bracket at the midpoint gives</p>
{eq(r'(u+2a)v-4u+u_{xy}+\frac h4\left(v^2-u_y^2-8v\right)+O(h^2),\tag{C2}')}
<p>and applying {m(r'\partial_x')} produces the coefficient {m(r'\tfrac h4\partial_x(v^2-u_y^2-8v)')} recorded in (51).</p>
<p><strong>Centered reconstruction.</strong> The relation {m(r'v_k=\Delta_hu_k+\mathcal M_-W_k')} with {m(r'W_k=4\omega_k/h')} expands as</p>
{eq(r'v=u_y+W+h^2\left(\frac{u_{yyy}}{24}+\frac{W_{yy}}8\right)+O(h^4),\tag{C3}')}
<p>so on the smooth family with {m(r'W=v-u_y+O(h^2)')} the reconstructed second field is second-order accurate. The extra flux of the first equation is {m(r'\omega^2/2-h\omega=h^2(W^2/32-W/4)')}, whose lattice difference and subsequent {m(r'x')} derivative are {m(r'O(h^2)')}, so the first residual is again {m(r'\mathcal R_u+O(h^2)')}. Differentiating (C3) in time and using {m(r'W_t=W_{xx}-\partial_x[(u+2a)W-4u]')} from (37) shows that the second residual is {m(r'\mathcal R_v+O(h^2)')}, which is the content of (52).</p>
</section>"""

# ------------------------------------------------------------------ Appendix D
D = f"""<section class="numerical-section" id="appendix-D"><h2>Appendix D. Numerical implementation and supplementary experiments</h2>
<p>This appendix collects the conventions of the computations, the closures at the transverse ends, and the control runs quoted in Sections 5.3 and 5.4.</p>
<p><strong>{m(r'x')} derivatives.</strong> All formulations use the same periodic Fourier operators, with multipliers {m(r'\mathrm i\xi')} for {m(r'\mathcal D_x')} and {m(r'-\xi^2')} for {m(r'\mathcal D_{xx}')}. The first-derivative multiplier is set to zero at the Nyquist frequency, the second retains its value there, and products are evaluated pointwise. No filtering, dealiasing or artificial viscosity is applied in any run.</p>
<p><strong>Closures.</strong> Endpoint-SD advances {m(r'(u_k,v_k)')} with the prescribed lower value of {m(r'u_t')} and a backward chain, so no upper datum is required. FD uses the same lower data and, at the upper end, the rule {m(r'u_{N+1}=u^*_{N+1}+3e_N-3e_{N-1}+e_{N-2}')} with {m(r'e_k=u_k-u^*_k')}, together with its differentiated form when {m(r'\dot u')} is needed. Centered-SD advances {m(r'(u_k,\omega_k)')}, needs no upper ghost, and advances the lower {m(r'\omega')} trace by the same equation as the interior.</p>
<p><strong>Implicit step.</strong> Crank&ndash;Nicolson is solved by an Euler predictor followed by fixed-point iteration on the trapezoidal residual. The iteration stops when the maximum residual falls below {m(r'2\times10^{-14}')}; since {m(r'\omega=hw/4')}, this corresponds to a residual smaller by the factor {m(r'h/4')} in the {m(r'\omega')} equation. A control with stopping level {m(r'2\times10^{-15}')} changes the terminal errors of Section 5.3 by at most {m(r'4\times10^{-13}')}.</p>
<p><strong>Moving mesh.</strong> On a nonuniform mesh the derivatives are mapped to the fixed computational coordinate, with {m(r'D_xf=\partial_\xi f/J')} and {m(r'D_{xx}f=\partial_{\xi\xi}f/J^2-(\partial_\xi J)(\partial_\xi f)/J^3')}, where {m(r'J=1+\partial_\xi s')} and {m(r'x_i=\xi_i+s_i')}. The three-point formulas of Section 4.3 evaluate {m(r'\partial_\xi')} and {m(r'\partial_{\xi\xi}')} on the uniform computational grid, and the node motion is coupled to the field equations through {m(r'\dot z=F_z+\mathcal V D_xz')}. The uniform-mesh results of Table 5 use the same operators with {m(r's=0')} and {m(r'\mathcal V=0')}.</p>
<p>The control runs underlying Sections 5.3 and 5.4 are summarized below. They use the same Centered-SD state, grid and reference as the corresponding main runs, and a single quantity is changed in each row.</p>
<div class="table-wrap"><table id="table-controls"><caption>Table 6. Control runs for Section 5. The change column states the only difference from the corresponding main run.</caption><thead><tr><th>Run</th><th>Change</th><th>{m(r'E_u')}</th><th>{m(r'E_v')}</th></tr></thead><tbody>
<tr><th rowspan="2" scope="rowgroup">One soliton<br><small>Euler</small></th><td>main, {m(r'\Delta t=10^{-4}')}</td><td>{m(r'1.664\times10^{-4}')}</td><td>{m(r'8.026\times10^{-5}')}</td></tr>
<tr><td>half step, {m(r'\Delta t=5\times10^{-5}')}</td><td>{m(r'1.671\times10^{-4}')}</td><td>{m(r'7.880\times10^{-5}')}</td></tr>
<tr><th rowspan="2" scope="rowgroup">Two solitons<br><small>Euler</small></th><td>main, {m(r'\Delta t=10^{-4}')}</td><td>{m(r'1.420\times10^{-4}')}</td><td>{m(r'1.090\times10^{-4}')}</td></tr>
<tr><td>half step, {m(r'\Delta t=5\times10^{-5}')}</td><td>{m(r'1.560\times10^{-4}')}</td><td>{m(r'1.048\times10^{-4}')}</td></tr>
<tr><th>All, CN</th><td>tight solve, {m(r'2\times10^{-15}')}</td><td colspan="2">terminal errors change by at most {m(r'4\times10^{-13}')}</td></tr>
<tr><th rowspan="2" scope="rowgroup">Mesh<br><small>one soliton</small></th><td>adaptive, nodes moving</td><td>{m(r'5.954\times10^{-4}')}</td><td>{m(r'1.157\times10^{-3}')}</td></tr>
<tr><td>equidistributed, frozen</td><td colspan="2">reductions of {m(r'12.8\%')} and {m(r'16.3\%')} relative to the uniform mesh</td></tr>
</tbody></table></div>
<p>The half-step rows show that the first-order temporal defect of forward Euler accounts for the whole displacement of its error level, as discussed in Section 5.3. The tight-solve row bounds the iteration error of the implicit scheme well below the reported discrepancies between integrators. The frozen row separates the two parts of the mesh construction: with the node count fixed, most of the reduction in Table 5 is already obtained by the initial equidistribution, as stated in Section 5.4.</p>
</section>"""

# ------------------------------------------------------- forward references
REFS_IN_TEXT = [
    ('the determinants and their required derivatives therefore differ from the continuous counterparts by',
     None),
]


def replace_block(text, pattern, new):
    hits = list(re.finditer(pattern, text, re.S))
    assert len(hits) == 1, (pattern, len(hits))
    return text[:hits[0].start()] + new + text[hits[0].end():]


out = source
out = replace_block(out, r'<section id="appendix-A">.*?</section>', A)
out = replace_block(out, r'<section id="appendix-B">.*?</section>', B)
out = replace_block(out, r'<section id="appendix-C">.*?</section>', C)
out = replace_block(out, r'<section id="appendix-D">.*?</section>', D)
# remove the editorial guide
out = replace_block(out, r'<section class="guide" id="appendix-G"[^>]*>.*?</section>\s*', '')

# forward references so the appendices are not orphaned
anchors = [
    ('Both admit explicit Gram determinant solutions, for which the positivity conditions established above ensure smooth logarithms for physical-field reconstruction.',
     ' Both admit explicit Gram determinant solutions, for which the positivity conditions established above ensure smooth logarithms for physical-field reconstruction. The determinant identities behind the field evaluations are collected in Appendix A.'),
    ('On a finite lattice, this recurrence uniquely determines the reconstruction from the fields and the lower trace.',
     ' On a finite lattice, this recurrence uniquely determines the reconstruction from the fields and the lower trace; Appendix B records the closed form and the conditions on that trace.'),
    ('This identity connects the nonlinear flux to the initial spatial comparisons in Section 5.2.',
     'This identity connects the nonlinear flux to the initial spatial comparisons in Section 5.2. The midpoint expansions behind (51) and (52) are given in Appendix C.'),
    ('Fourier differentiation acts on a periodic',
     None),
]
for old, new in anchors:
    if new is None:
        continue
    assert out.count(old) == 1, old[:60]
    out = out.replace(old, new)

# implementation reference in Section 4.2
old = 'The implicit step uses an Euler prediction followed by fixed-point iteration.'
assert out.count(old) == 1
out = out.replace(old, old + ' The iteration and its stopping rule are restated in Appendix D, together with the closure rules and the control runs.')

out = render(out)
assert 'APMATH' not in out
PAPER.write_text(out, encoding='utf-8')

manifest = dict(
    before=dict(path=str(BASELINE.relative_to(ROOT)),
                sha256=hashlib.sha256(BASELINE.read_bytes()).hexdigest()),
    after=dict(path='dlw-paper.html', sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest()),
    written=['appendix-A', 'appendix-B', 'appendix-C', 'appendix-D'],
    removed=['appendix-G (archived in appendix_G_archive.txt)'],
    new_table='Table 6 (control runs, Appendix D)',
    formulas=len(maths),
)
(HERE / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2))
