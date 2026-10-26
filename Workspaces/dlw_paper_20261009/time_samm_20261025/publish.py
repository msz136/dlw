"""Publish Sections 4.2-4.3, 5.3-5.4: Centered-SD time integration and moving mesh.

Bounded replacements only: the current manuscript is read, the named sections and
two introduction paragraphs are replaced, the navigation gains two entries, and
every other byte is preserved. Mathematics is rendered with the local KaTeX build.
"""
from pathlib import Path
import hashlib, json, math, re, subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAPER = ROOT / 'dlw-paper.html'
BASELINE = HERE / 'before/dlw-paper.html'
FIGDIR = 'Workspaces/dlw_paper_20261009/time_samm_20261025/figures'
TIME = HERE / 'time'
SAMM = HERE / 'samm_periodic'
CASES = ['A', 'D', 'Gaussian', 'Sinusoidal']

maths = []


def m(tex):
    token = 'TSTIMEMATH' + str(len(maths)) + 'END'
    maths.append(dict(tex=tex, display=False))
    return token


def eq(tex):
    token = 'TSTIMEMATH' + str(len(maths)) + 'END'
    maths.append(dict(tex=tex, display=True))
    return '<div class="equation">' + token + '</div>'


def render(text):
    js = ("const fs=require('fs'),k=require(process.argv[1]);"
          "process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8'))"
          ".map(f=>k.renderToString(f.tex,{displayMode:f.display,throwOnError:true,strict:'error'}))));")
    katex = ROOT / 'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js'
    r = subprocess.run(['node', '-e', js, str(katex)], input=json.dumps(maths), text=True,
                       encoding='utf-8', capture_output=True, check=True)
    for i, result in enumerate(json.loads(r.stdout)):
        text = text.replace('TSTIMEMATH' + str(i) + 'END', result)
    return text


def section_span(text, identity):
    match = re.search(r'<section\b[^>]*\bid="' + re.escape(identity) + r'"[^>]*>', text)
    assert match, identity
    depth = 1
    for token in re.finditer(r'</?section\b[^>]*>', text[match.end():]):
        depth += -1 if token.group().startswith('</') else 1
        if depth == 0:
            return match.start(), match.end() + token.end()
    raise ValueError(identity)


def replace_section(text, identity, replacement):
    a, b = section_span(text, identity)
    return text[:a] + replacement + text[b:]


# ---------------------------------------------------------------- tabulated data
def sci(x):
    e = int(math.floor(math.log10(abs(x))))
    mant = x / 10 ** e
    if round(mant, 3) >= 10:
        mant /= 10
        e += 1
    return f'{mant:.3f} × 10<sup>{e}</sup>', round(mant, 3), e


def cell(x, bold=False):
    text, _, _ = sci(x)
    inner = f'<strong>{text}</strong>' if bold else text
    return f'<td data-value="{x!r}">{inner}</td>'


def load_time(case):
    rec = json.loads((TIME / f'{case}_time.json').read_text(encoding='utf-8'))
    return {k: rec['integrators'][k]['error'] for k in ('Euler', 'RK4', 'CN')}


TIME_TABLE_FIELDS = ('Euler', 'RK4', 'CN')
time_rows = []
TIME_TABLE_FIELDS = TIME_TABLE_FIELDS
for case in CASES:
    vals = load_time(case)
    row = [f'<th>{ "One-soliton" if case=="A" else "Two-soliton" if case=="D" else case }</th>']
    figures = {k: {idx: sci(vals[k][idx]) for idx in (0, 1)} for k in TIME_TABLE_FIELDS}
    smallest = {idx: min(TIME_TABLE_FIELDS, key=lambda k: vals[k][idx]) for idx in (0, 1)}
    tie = {idx: sum(1 for k in TIME_TABLE_FIELDS if figures[k][idx][1:] == figures[smallest[idx]][idx][1:]) > 1
           for idx in (0, 1)}
    for k in TIME_TABLE_FIELDS:
        for idx in (0, 1):
            row.append(cell(vals[k][idx], bold=(k == smallest[idx] and not tie[idx])))
    time_rows.append('<tr>' + ''.join(row) + '</tr>')

mesh = {(c, mode): json.loads((SAMM / f'{c}_{mode}_0.0001.json').read_text(encoding='utf-8'))
        for c in ('A', 'D') for mode in ('uniform', 'frozen', 'moving')}
mesh_rows = []
for case in ('A', 'D'):
    uni, ada = mesh[(case, 'uniform')]['error'], mesh[(case, 'moving')]['error']
    name = 'One-soliton' if case == 'A' else 'Two-soliton'
    ru, rv = 100 * (1 - ada[0] / uni[0]), 100 * (1 - ada[1] / uni[1])
    mesh_rows.append(
        f'<tr><th>{name}</th>'
        + cell(uni[0]) + cell(uni[1])
        + cell(ada[0], bold=True) + cell(ada[1], bold=True)
        + f'<td>{ru:.1f}%</td><td>{rv:.1f}%</td></tr>')

E_FIELDS = ''.join(f'<th>{m(r"E_u")}</th><th>{m(r"E_v")}</th>' for _ in range(3))
E_PAIR = ''.join(f'<th>{m(r"E_u")}</th><th>{m(r"E_v")}</th>' for _ in range(2))

table4 = f'''<div class="table-wrap"><table id="table-time"><caption>Table 4. Physical-field errors at T = 0.01 for Centered-SD with forward Euler, RK4 and Crank–Nicolson at h = Δx = 0.1 and Δt = 10⁻⁴.</caption><thead><tr><th rowspan="2">Case</th><th colspan="2">Forward Euler</th><th colspan="2">RK4</th><th colspan="2">Crank–Nicolson</th></tr><tr>{E_FIELDS}</tr></thead><tbody>{''.join(time_rows)}</tbody></table></div>'''

table5 = f'''<div class="table-wrap"><table id="table-mesh"><caption>Table 5. Physical-field errors at T = 0.01 on the uniform and adaptive meshes, with the relative change defined in the text. Both calculations use Centered-SD with mapped centred x differences, RK4, Δt = 10⁻⁴ and the same number of nodes.</caption><thead><tr><th rowspan="2">Case</th><th colspan="2">Uniform mesh</th><th colspan="2">Adaptive mesh</th><th colspan="2">Change</th></tr><tr>{E_PAIR}<th>{m(r"\mathcal R_u")}</th><th>{m(r"\mathcal R_v")}</th></tr></thead><tbody>{''.join(mesh_rows)}</tbody></table></div>'''


def figure(number, stem, alt, caption):
    return (f'<figure id="figure-{number}"><img loading="lazy" src="{FIGDIR}/{stem}.png" alt="{alt}">'
            f'<figcaption><strong>Figure {number}.</strong> {caption} '
            f'<a class="export" href="{FIGDIR}/{stem}.pdf">PDF</a></figcaption></figure>')


fig25 = figure(25, 'time_error_u', 'Error histories of the first field for three time integrators',
               'Development of the maximum absolute error in ' + m('u') + ' for Centered-SD with forward Euler (orange, triangles), RK4 (blue) and Crank–Nicolson (green dashed): (a) one-soliton, (b) two-soliton, (c) Gaussian and (d) sinusoidal cases. Each value is the maximum over the native field locations in the region of Section 5.1 and is evaluated at every time step; the vertical axis is logarithmic. All calculations use ' + m(r'h=\Delta x=0.1') + ' and ' + m(r'\Delta t=10^{-4}') + '. The initial error vanishes.')
fig26 = figure(26, 'time_error_v', 'Error histories of the second field for three time integrators',
               'Development of the maximum absolute error in ' + m('v') + ', with the same symbols as Figure 25. Each value is the maximum over the native midpoints ' + m(r'y_{k-1/2}') + ' of the second field in the region of Section 5.1.')
fig27 = figure(27, 'mesh_spacing', 'Normalized local spacing of the adaptive mesh',
               'Local ' + m('x') + ' spacing normalized by the uniform spacing ' + m(r'\Delta x=0.1') + ', plotted at the interval midpoints of (a) the one-soliton and (b) the two-soliton case. Grey dashed: initial adaptive mesh; blue: ' + m('T=0.01') + '; orange dotted: uniform spacing.')
fig28 = figure(28, 'mesh_profile_A', 'Error profiles on the uniform and adaptive meshes',
               'One-soliton case at ' + m('T=0.01') + '. Maximum over the transverse layers of the absolute error at each native ' + m('x') + ' node for the uniform mesh (orange dashed, open circles) and the adaptive mesh (blue): (a) ' + m('u') + ' and (b) ' + m('v') + '. Both calculations use the mapped centred operators of Section 4.3, the same number of nodes and RK4 with ' + m(r'\Delta t=10^{-4}') + '.')

# ------------------------------------------------------------------- prose
intro4 = (' Section 4.3 uses a conservation law of the Centered-SD system to construct a shared moving mesh '
          'and couples its node motion to the field evolution.')

intro5 = (' Section 5.3 retains Centered-SD and compares the physical-field errors produced by three time '
          'integrators throughout the evolution. Section 5.4 examines how redistributing the shared ' + m('x') +
          ' nodes affects the same errors.')

old_cn = '<p>The implicit step uses an Euler prediction followed by fixed-point iteration'
assert old_cn in BASELINE.read_text(encoding='utf-8'), 'Crank-Nicolson paragraph not found'

new_cn = ('<p>The implicit step uses an Euler prediction followed by fixed-point iteration. The iteration is stopped when '
          'the maximum absolute residual of the trapezoidal update in the advanced variables falls below ' + m(r'2\times10^{-14}') +
          '; since Centered-SD stores ' + m(r'\omega=hw/4') + ', this bound corresponds to a residual that is smaller by the factor ' +
          m('h/4') + ' in the ' + m(r'\omega') + ' equation. A control calculation with a stopping level of ' +
          m(r'2\times10^{-15}') + ' changes the terminal errors of Section 5.3 by at most ' + m(r'4\times10^{-13}') +
          '. The spatial comparisons in Section 5.2 and the time comparisons in Section 5.3 use ' + m(r'\Delta t=10^{-4}') +
          ' with final time ' + m('T=0.01') + ', and the mesh comparison in Section 5.4 uses RK4 with the same step and final time. '
          'In every comparison, errors are measured in the physical fields ' + m('u,v') + '.</p>')

section43 = f'''<section class="numerical-section" id="section-4.3"><h3>4.3 A conservation-based moving mesh</h3>
<p>A uniform grid assigns the same spacing to weakly varying regions and to the narrow parts of a wave profile. We therefore let the {m('x')} nodes move with the solution, keep the {m('y')} lattice uniform, and use the same moving {m('x')} nodes in every transverse layer. This shared mesh preserves the lattice pairing of the Centered-SD equations while allowing the resolution in {m('x')} to follow the computed fields.</p>
<p>The auxiliary equation of the natural formulation supplies the conservation law used to determine the mesh. Setting {m(r'\rho_k=1-\omega_k/h')} and choosing the flux so that it vanishes on the zero-field background gives</p>
{eq(r'\rho_k=1-\frac{\omega_k}{h},\qquad q_k=(u_k+2a)\rho_k-\partial_x\rho_k-2a.')}
<p>Substituting {m(r'\omega_k=h(1-\rho_k)')} into the {m(r'\omega')} equation yields {m(r'\partial_t\rho_k+\partial_xq_k=0')}: the density evolves through a flux that is already present in the semi-discrete system.</p>
<p>Since all layers share the same {m('x')} nodes, we average the density and the flux over the stored layers,</p>
{eq(r'\bar\rho=\frac1{N_y}\sum_k\rho_k,\qquad \bar q=\frac1{N_y}\sum_k q_k,')}
<p>and the averaged quantities satisfy the same conservation relation. The initial nodes equidistribute the cumulative density; with an arbitrary reference node fixed we require</p>
{eq(r'\int_{x_0}^{x_i(0)}\bar\rho\,dx=\frac{i}{N_x}\int_{x_0}^{x_0+L}\bar\rho\,dx,\qquad i=0,\dots,N_x,')}
<p>so intervals in regions of larger {m(r'\bar\rho')} receive more nodes. During the evolution each node keeps its cumulative-density label, which is equivalent to preserving the mass of every cell {m(r'[x_i,x_{i+1}]')}. This requires {m(r'\bar\rho_i\mathcal V_i-\bar q_i')} to take the same value at every node. On the periodic interval that constant is the spatial mean of {m(r'\bar q')}, and the velocity is</p>
{eq(r'\dot x_i=\mathcal V_i=\frac{\bar q_i-\langle\bar q\rangle}{\bar\rho_i},\qquad \langle\bar q\rangle=\frac1{N_x}\sum_i\bar q_i.')}
<p>This choice leaves the mean displacement zero and keeps the mapping periodic. The construction requires {m(r'\bar\rho>0')}, and the ordering of the nodes is preserved while the discrete Jacobian remains positive.</p><p>On a nonuniform mesh the derivatives in {m('x')} are evaluated through the fixed uniform coordinate {m(r'\xi')}, with {m(r'x_i=\xi_i+s_i')} and {m(r'J=1+\partial_\xi s')}. The chain rule gives</p>
{eq(r'D_xf=\frac{\partial_\xi f}{J},\qquad D_{xx}f=\frac{\partial_{\xi\xi}f}{J^2}-\frac{(\partial_\xi J)(\partial_\xi f)}{J^3},')}
<p>where {m(r'\partial_\xi')} and {m(r'\partial_{\xi\xi}')} are centred three-point differences on the uniform computational grid. We write {m('D_x')} and {m('D_{xx}')} for these mapped centred operators, to distinguish them from the Fourier operators {m(r'\mathcal D_x')} and {m(r'\mathcal D_{xx}')} of Section 4.1. The uniform calculation of Section 5.4 has {m('s=0')} and {m('J=1')}.</p>
<p>At a moving node the time derivative also contains the change of its position, so we advance</p>
{eq(r'\dot u_k=F_{u,k}+\mathcal V_kD_xu_k,\qquad \dot\omega_k=F_{\omega,k}+\mathcal V_kD_x\omega_k,\qquad \dot x_k=\mathcal V_k.')}
<p>Here {m('F_u')} and {m(r'F_\omega')} denote the Centered-SD right-hand sides evaluated with the mapped operators at the current mesh. Every layer shares the node velocity, so the reconstruction of {m('v')} is retained during the coupled evolution, and at the lower node the prescribed rate is transported along the node trajectory, {m(r'u_t=u^*_t+\mathcal V_0u^*_x')}. Setting {m(r'\mathcal V=0')} recovers the fixed-grid equations.</p></section>'''

section53 = f'''<section class="numerical-section" id="section-5.3"><h3>5.3 Comparison of time integrators</h3>
<p>We next retain Centered-SD on the fixed grid and vary only the time integrator. Forward Euler, classical RK4 and Crank–Nicolson use the same initial fields, the same boundary data and the same Fourier {m('x')} operators, with {m(r'h=\Delta x=0.1')} and {m(r'\Delta t=10^{-4}')}, and each calculation is followed from {m('t=0')} to {m('T=0.01')}.</p>
<p>Table 4 collects the values at {m('T=0.01')}. The RK4 entries reproduce the Centered-SD values of Table 3 and fix the reference level; Crank–Nicolson stays within {m(r'7.3\times10^{-3}')} relative of that level, its largest deviation being the first field of the two-soliton case. Forward Euler moves the level in a direction that depends on the field: it gives the smallest {m('u')} error of the three methods in all four tests, by {m(r'0.8\%')}, {m(r'21\%')}, {m(r'82\%')} and {m(r'38\%')}, while its {m('v')} error exceeds the RK4 value by {m(r'3.8\%')}, {m(r'8.0\%')}, and factors of {m('8.2')} and {m('9.0')}. The terminal comparison therefore orders the schemes only within one field at a time, and it leaves open how the differences are produced.</p>
{table4}
<p>To see that, we record the largest discrepancy at every time step,</p>
{eq(r'E_u^{(m)}(t_n)=\max_{\mathcal G_u}\left|u_h^{(m)}(t_n)-u^*(t_n)\right|,\qquad E_v^{(m)}(t_n)=\max_{\mathcal G_v}\left|v_h^{(m)}(t_n)-v^*(t_n)\right|,')}
<p>with {m('m')} labelling the time integrator. The location of the maximum may move during the evolution, so the two histories describe how the worst error in each field develops rather than the history of one material point.</p>
{fig25}
<p>All four panels of Figure 25 rise monotonically from zero and attain their largest value at the final time. In the one-soliton, Gaussian and sinusoidal cases the growth is almost linear in {m('t')}, the ratio {m('E_u(t)/t')} varying by less than {m(r'10\%')} over the interval; on the logarithmic axis this is the concave shape of the curves, and it indicates an error produced at a nearly constant rate rather than an emerging instability. The two-soliton panel is the exception: its curves follow the same near-linear growth until about {m('t=0.009')} and then steepen, so that over the last tenth of the interval {m('E_u(t)/t')} rises by {m(r'36\%')}. This is the stage at which the two wave branches meet and the fields develop structure on the scale of the grid.</p>
<p>Within each panel, RK4 and Crank–Nicolson are indistinguishable, whereas the Euler curve is displaced by a factor that stays near {m('0.99')}, {m('0.18')} and {m('0.62')} in the one-soliton, Gaussian and sinusoidal panels and drifts from {m('0.97')} to {m('0.79')} in the two-soliton panel, over the same interval in which the higher-order curves steepen.</p>
<p>The second field develops in the same way. Figure 26 repeats the measurement at the midpoints {m(r'y_{k-1/2}')} of {m('v')}, and its panels reproduce the features of Figure 25: monotone growth that is almost linear in {m('t')}, maxima at the final time, and RK4 and Crank–Nicolson lying on top of each other. The one-soliton panel behaves as it did for {m('u')}, with a displacement of only {m('1.04')}, and the two-soliton panel again shows a mild steepening in the interaction window.</p>
{fig26}
<p>The difference lies in the direction and the size of the Euler displacement, which here lies above the RK4 level, by factors of {m('1.04')} and {m('1.08')} in the two soliton cases and of {m('8.2')} and {m('9.0')} in the Gaussian and sinusoidal cases. The same first-order defect that lowers the {m('u')} error therefore raises the {m('v')} error by almost an order of magnitude in the smooth tests.</p>
<p>A first-order defect in a slowly varying right-hand side produces exactly such a level shift, and it disappears as the step is reduced. Halving the step moves the Euler values back towards RK4 in all four tests, for the one-soliton case from {m(r'1.664\times10^{-4}')} and {m(r'8.026\times10^{-5}')} to {m(r'1.671\times10^{-4}')} and {m(r'7.880\times10^{-5}')}, and for the two-soliton case from {m(r'1.420\times10^{-4}')} and {m(r'1.090\times10^{-4}')} to {m(r'1.560\times10^{-4}')} and {m(r'1.048\times10^{-4}')}. The smaller {m('u')} error of Euler is therefore a cancellation between the temporal defect and the spatial error, not a better resolution of that field. That the two fields respond in opposite directions in every test is consistent with the differentiated lattice relation that defines {m('v')} from {m('u')} and {m(r'\omega')}: the same temporal defect reaches the two fields with opposite sign.</p>
<p>Taken together, the table and the histories separate three effects that a single error number merges. First, the rate at which the computed solution departs from the exact one is fixed by the spatial discretization: it is nearly the same for all three integrators, constant in {m('t')} except where new structure appears, and it changes as soon as the interaction region forms. Second, the time integrator sets the level of that departure, and at {m(r'\Delta t=10^{-4}')} only the first-order scheme shifts it appreciably, so a second-order scheme already matches the fourth-order one. Third, the level is not a monotone measure of accuracy, because the temporal and spatial errors can combine with either sign in a given field: a lower-order scheme may show the smaller error in one component while being less accurate in the other. The histories add what the terminal table cannot. They place the growth in time, showing that the discretization is stressed when structure forms, and they separate the field that carries the larger absolute error, {m('u')} in all four tests, from the field that is most sensitive to the time integrator, {m('v')}, where the first-order defect raises the error by up to a factor of nine. They also justify the choice made below: RK4 is retained for the mesh comparison, where a common integrator isolates the effect of the node distribution, and a temporal refinement becomes the relevant question only when {m(r'\Delta t')} or {m('h')} is changed far enough for the two error sources to become comparable.</p></section>'''

section54 = f'''<section class="numerical-section" id="section-5.4"><h3>5.4 Fixed and adaptive meshes</h3>
<p>We now examine how the distribution of the shared {m('x')} nodes affects the computed fields. The uniform and adaptive calculations have the same node count, the same {m('y')} lattice, the same RK4 step {m(r'\Delta t=10^{-4}')} and the same final time. Both use the mapped centred operators of Section 4.3, so the only difference is the node distribution; those operators are local in the computational coordinate rather than Fourier multipliers, so the fixed-mesh errors below are larger than those of Table 3. The comparison uses the two soliton tests, whose second field vanishes on the background. In the Gaussian and sinusoidal data the second field is centred on {m('v=4')}, the transverse-averaged density vanishes, and both the equidistribution and the velocity of Section 4.3 are undefined; those two families are therefore excluded here.</p>
<p>In the adaptive calculation the initial nodes equidistribute the transverse-averaged conservation density computed from the exact initial fields, and the nodes then move with the velocity of Section 4.3. The density ranges from {m('1.000')} to {m('1.150')} in the one-soliton case and from {m('1.000')} to {m('1.050')} in the two-soliton case. Figure 27 shows the resulting local spacing, normalized by the uniform spacing, at {m('t=0')} and {m('T=0.01')}.</p>
{fig27}
<p>Nodes are concentrated where the density is large. In the one-soliton case the spacing falls to {m(r'0.90\,\Delta x')} across the wave region, and the background is stretched to {m(r'1.04\,\Delta x')}; in the two-soliton case the spacing varies between {m(r'0.97\,\Delta x')} and {m(r'1.02\,\Delta x')}. The initial and final distributions nearly coincide: the largest node displacement during the calculation is {m(r'9.5\times10^{-4}')} in the one-soliton case and {m(r'5.2\times10^{-4}')} in the two-soliton case. The pattern is therefore set by the initial equidistribution and adjusted only slightly by the evolution, and the total discrete mass of the averaged density changes by less than {m(r'10^{-7}')} relative.</p>
<p>Table 5 compares the terminal errors on the fixed and adaptive meshes and reports the relative change</p>
{eq(r'\mathcal R_f=100\left(1-\frac{E_f^{\mathrm{adaptive}}(T)}{E_f^{\mathrm{uniform}}(T)}\right)\%,\qquad f=u,v.')}
{table5}
<p>Positive values correspond to a reduction. The adaptive mesh lowers both errors in both cases: by {m(r'11.7\%')} in {m('u')} and {m(r'17.4\%')} in {m('v')} for the one-soliton case, and by {m(r'6.0\%')} and {m(r'5.6\%')} for the two-soliton case. The changes are modest, of the same order as the spacing change that produces them, but they appear in both fields of both tests, and in neither case does a field become worse. The reduction is also already obtained from the initial distribution. Holding the equidistributed initial nodes fixed gives changes of {m(r'12.8\%')} and {m(r'16.3\%')} for the one-soliton case and {m(r'5.3\%')} and {m(r'5.8\%')} for the two-soliton case, within {m('1.1')} percentage points of the values in Table 5. The node motion over this short interval is therefore not the main mechanism; it slightly raises the first-field error of the one-soliton case and slightly lowers the second-field error.</p>
<p>Figure 28 shows the corresponding error profiles for the one-soliton case, that is, the maximum over the transverse layers at each native {m('x')} node. The adaptive mesh lowers the error over the central region of both fields: the dominant peak of {m('u')} falls from {m(r'6.74\times10^{-4}')} to {m(r'5.95\times10^{-4}')}, and the plateau of {m('v')} along the wave band falls from {m(r'1.40\times10^{-3}')} to {m(r'1.16\times10^{-3}')}. The reduction thus extends along the band rather than occurring at the single point that defines the maximum. In the two-soliton case it is smaller, as the last row of Table 5 shows.</p>
{fig28}
<p>Read together, the spacing, the table and the profiles describe a consistent mechanism. The error of the fixed calculation is not spread uniformly over the region: it follows the wave band, and the equidistribution puts the additional nodes in the same band. Moving them there lowers the error along the whole band, so the largest value falls too. The relative gain is larger in {m('v')} than in {m('u')} for the one-soliton case, which is natural in this formulation: the density is a shifted copy of the auxiliary field {m(r'\omega')}, and {m(r'\omega')} enters the reconstruction of {m('v')} through the staggered pair, so the monitor weights the part of {m('v')} that is not determined by the backward difference of {m('u')}.</p>
<p>Taken together, the comparison says what a mesh of this kind can and cannot provide at the resolution and horizon used here. It can move resolution to the part of the region where the error is produced, and it does so with a modest and systematic gain in both fields, with the same node count and the same time integrator. It does not change the origin of the error: the nodes are redistributed, the operator and its truncation are unchanged, and the improvement is limited by how much the local spacing can be reduced before the background is emptied. Nor does the present calculation test the motion of the mesh, since the initial and final distributions nearly coincide and the frozen control gives almost the same numbers. The measured gain is therefore the gain of a grid adapted to the conservation density; a longer computation, in which the density itself changes on the scale of the spacing, is what would test the adaptive part of the method.</p></section>'''

guide = '''<section class="guide" id="appendix-G" lang="zh-CN"><h2>Appendix G. Editorial guide（暂存，投稿前移除）</h2><p class="status">2026-10-25：5.3补入当前自然Centered-SD的Euler/RK4/CN终值表（表4）与u/v误差随时间发展两图（图25–26）；5.4补入守恒密度动网格的构造（4.3）、间距图（图27）、固定/动网格误差表（表5）与单孤子误差剖面（图28）。两节均按“表—图—解读”穿插写，末尾给出认识性收尾。</p><p>5.4的讨论只用已有量：表5的固定/动网格误差与冻结对照、图27的间距分布、图28的剖面，以及正文已报的节点位移与质量守恒。试写过的额外诊断（均方根范数、节点计数与波带误差占比、(Δx)²截断估算、由精确场重算等分网格的位移、波形平移量）已按要求撤除，脚本与数值留在samm_periodic/not_used_in_paper_20261025/，不进入正文。</p><p>4.3与5.4的固定/动网格对照统一采用映射中心差分，故表5的固定网格值与表3的Fourier结果不同；正文已作说明。冻结初始等分网格作为对照，其数值只在5.4正文给出，不单列。误差剖面对两孤子情形在节点尺度上呈锯齿，故正文只展示单孤子剖面；Gaussian/Sinusoidal因横向平均密度恒为零（第二场以v=4为中心）不参与动网格对照，正文首段已说明。</p><p>稳定性部分4.4与5.5仍为占位，待后续讨论；Euler/CN的时间步敏感性仅保留一孤子与正弦两例的半步对照（其余待补）。动网格的周期速度取q的节点空间平均作为常数，避免节点整体漂移并保持映射周期性。旧全节发布器不得再运行。</p><p>当前数据与图源：Workspaces/dlw_paper_20261009/time_samm_20261025/（time、samm_periodic、figures、prose_notes.md、PROTOCOL.md）。</p></section>'''

# ------------------------------------------------------------------- publish
source = BASELINE.read_text(encoding='utf-8')
paper = source

anchor42 = '<a class="subsection" href="#section-4.2">4.2 Initial and boundary data and time integration</a>'
assert anchor42 in paper
paper = paper.replace(anchor42, anchor42 + '\n<a class="subsection" href="#section-4.3">4.3 A conservation-based moving mesh</a>', 1)
anchor53 = '<a class="subsection" href="#section-5.3">5.3 Comparison of time integrators</a>'
assert anchor53 in paper
paper = paper.replace(anchor53, anchor53 + '\n<a class="subsection" href="#section-5.4">5.4 Fixed and adaptive meshes</a>', 1)

intro4_old = ('<p>We use the physical-field equations to examine how spatial approximation and time integration affect the computed waves. '
              'Section 4.1 describes the common x operators and the three spatial formulations. In Section 4.2, we specify the initial '
              'and boundary data and introduce the time integrators used in the experiments.</p>')
assert intro4_old in paper
paper = paper.replace(intro4_old, intro4_old[:-4] + intro4 + '</p>', 1)

intro5_old = ('<p>We use a one-soliton wave, a two-soliton interaction, Gaussian initial data and sinusoidal initial data to examine '
              'the physical fields computed by the three spatial formulations. Section 5.1 introduces these test problems, their '
              'continuous references and the error measures. Section 5.2 compares the fields at ')
assert intro5_old in paper
i = paper.index(intro5_old)
j = paper.index('</p>', i)
paper = paper[:j] + intro5 + paper[j:]

section42 = source[slice(*section_span(source, 'section-4.2'))]
i = section42.index(old_cn)
j = section42.index('</p>', i) + 4
section42 = section42[:i] + new_cn + section42[j:]
paper = replace_section(paper, 'section-4.2', section42)
paper = replace_section(paper, 'section-4.3', section43)
paper = replace_section(paper, 'section-5.3', section53)
paper = replace_section(paper, 'section-5.4', section54)
paper = replace_section(paper, 'appendix-G', guide)
paper = render(paper)
assert 'TSTIMEMATH' not in paper and 'katex-error' not in paper

# ---------------------------------------------------------------- validation
protected = ['section-1', 'section-2', 'section-2.1', 'section-2.2', 'section-2.3', 'section-2.4',
             'section-3', 'section-3.1', 'section-3.2', 'section-3.3', 'section-3.4',
             'section-4', 'section-4.1', 'section-4.4', 'section-5', 'section-5.1', 'section-5.2',
             'section-5.5', 'section-6']
for identity in protected:
    before = source[slice(*section_span(source, identity))]
    after = paper[slice(*section_span(paper, identity))]
    if identity in ('section-4', 'section-5'):
        continue
    assert before == after, 'protected section changed: ' + identity

assert paper.count('<figure') == 28, paper.count('<figure')
assert paper.count('<figure id=') == 24, paper.count('<figure id=')
assert paper.count('<table id=') == 5, paper.count('<table id=')
for number in range(25, 29):
    assert f'id="figure-{number}"' in paper
for stem in ('time_error_u', 'time_error_v', 'mesh_spacing', 'mesh_profile_A'):
    for ext in ('png', 'pdf'):
        assert (ROOT / FIGDIR / f'{stem}.{ext}').exists(), stem + ext
    assert f'{FIGDIR}/{stem}.png' in paper
for anchor in ('#section-4.3', '#section-5.4'):
    assert paper.count(anchor) == 1, (anchor, paper.count(anchor))
assert paper.count('id="table-time"') == 1 and paper.count('id="table-mesh"') == 1
assert paper != source

# Refuse to overwrite a concurrently modified manuscript.
current = hashlib.sha256(PAPER.read_bytes()).hexdigest()
allowed = {hashlib.sha256(BASELINE.read_bytes()).hexdigest()}
manifest_path = HERE / 'publication_manifest.json'
if manifest_path.exists():
    allowed.add(json.loads(manifest_path.read_text(encoding='utf-8'))['after_sha256'])
assert current in allowed, 'The manuscript changed concurrently; review before publishing.'

PAPER.write_text(paper, encoding='utf-8')
for identity in ('section-4.2', 'section-4.3', 'section-5.3', 'section-5.4'):
    a, b = section_span(paper, identity)
    (HERE / f'{identity}.html').write_text(paper[a:b], encoding='utf-8')

manifest = dict(before_sha256=hashlib.sha256(BASELINE.read_bytes()).hexdigest(),
                after_sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest(),
                replaced=['section-4.2', 'section-4.3', 'section-5.3', 'section-5.4', 'appendix-G',
                          'nav-4.3', 'nav-5.4', 'intro-4', 'intro-5'],
                figures=[25, 26, 27, 28], tables=['table-time', 'table-mesh'],
                formulas=len(maths), placeholder=['section-4.4', 'section-5.5'],
                data=['time', 'samm_periodic'], scripts=['figures/plot_time_history.py', 'figures/plot_mesh.py',
                                                         'samm_periodic/run_samm_periodic.py'])
manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2))
