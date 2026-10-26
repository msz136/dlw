"""Rewrite Section 5 from the supplied narrative, keeping the existing blocks.

The narrative follows the wording supplied by the user (a Gemini draft of Section 5).
Tables 1-5 and Figures 1-28 are taken verbatim from the current manuscript and placed
at the positions the narrative marks; every other section is left unchanged.
"""
from pathlib import Path
import hashlib, json, re, subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAPER = ROOT / 'dlw-paper.html'
BASELINE = HERE / 'before/dlw-paper.html'

maths = []


def m(tex, display=False):
    token = 'S5MATHS' + str(len(maths)) + 'END'
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
        text = text.replace('S5MATHS' + str(i) + 'END', result)
    return text


source = BASELINE.read_text(encoding='utf-8')

# ---------------------------------------------------------------- existing blocks
figures = {}
for match in re.finditer(r'<figure\b.*?</figure>', source, re.S):
    block = match.group()
    number = re.search(r'<strong>Figure (\d+)\.</strong>', block)
    assert number, block[:120]
    figures[int(number.group(1))] = block
assert sorted(figures) == list(range(1, 29)), sorted(figures)

tables = {}
for match in re.finditer(r'<div class="table-wrap">.*?</table></div>', source, re.S):
    block = match.group()
    number = re.search(r'<caption>Table (\d+)\.', block)
    assert number, block[:120]
    tables[int(number.group(1))] = block
assert sorted(tables) == [1, 2, 3, 4, 5], sorted(tables)

F = {n: figures[n] for n in figures}
T = {n: tables[n] for n in tables}


def fig(*numbers):
    return '\n'.join(F[n] for n in numbers)


# --------------------------------------------------------------------- Section 5
intro = f'''<section id="section-5"><h2>5. Numerical experiments</h2>
<p>In this section, we use four representative initial-value problems &mdash; a one-soliton wave, a two-soliton interaction, a localized Gaussian pulse, and a periodic sinusoidal wave &mdash; to examine how the spatial and temporal formulations developed in Sections 2&ndash;4 perform in practice. Section 5.1 introduces the test problems, their continuous reference solutions, and the native-grid error measures used throughout the comparisons. In Section 5.2, we compare the physical fields computed by Endpoint-SD, Centered-SD, and the finite-difference baseline (FD) at {m('T=0.01')} under common RK4 time integration, using the initial time-derivative defects at {m('t=0')} as a short diagnostic of the spatial approximation. Retaining Centered-SD on the fixed grid, Section 5.3 compares forward Euler, classical RK4, and Crank&ndash;Nicolson by following the error histories across the entire time interval. Finally, Section 5.4 examines how redistributing the shared {m('x')} nodes according to the semi-discrete conservation density affects the computed soliton fields.</p>'''

section51 = f'''<section class="numerical-section" id="section-5.1"><h3>5.1 Test problems and error measures</h3>
<p>All numerical tests use the parameters {m('a=2')} and {m(r'\lambda=-2')}. The one- and two-soliton reference solutions are generated directly from the continuous Gram determinant formulas (6)&ndash;(7) in Section 2.1, with {m(r'\rho_i=1')} and zero phase shifts. Table 1 lists their spectral parameters, evaluation windows, and computational intervals.</p>
{T[1]}
<p>Writing the periodic {m('x')} interval as {m('[-L,L)')}, we use the same interval in {m('y')} and place the computational boundaries well outside the region {m('[-R,R]^2')} containing the principal wave profiles.</p>
<p>As shown in Figures 1 and 2, the one-soliton case consists of a single oblique wave band with smooth negative troughs in both {m('u')} and {m('v')}.</p>
{fig(1, 2)}
<p>The two-soliton case (Figures 3 and 4) combines the spectral pair of the one-soliton wave with a second pair {m('(4,-3)')}. Its first field {m('u')} features a dominant negative trough alongside a shallower positive ridge, whereas both intersecting wave bands remain negative in the second field {m('v')}, allowing us to test the schemes on interacting waves of different amplitudes and polarities.</p>
{fig(3, 4)}
<p>For the Gaussian and sinusoidal tests, let {m('z=y+2')} and {m(r'\kappa=\pi/4')}, and take the separable initial fields</p>
{eq(r'u_0(x,y)=A\sin(\kappa z)F(x),\qquad v_0(x,y)=4-3A\kappa\cos(\kappa z)F(x).')}
<p>The Gaussian test uses {m('A=0.05')} with the periodic localized profile {m(r'F(x)=\sum_{j\in\mathbb Z}\exp[-((x+192j)/6)^2]')}, while the sinusoidal test uses {m('A=0.03')} with {m(r'F(x)=\cos(\pi x/12)')}. Both problems are computed on the periodic interval {m(r'x\in[-96,96)')} over the transverse strip {m(r'y\in[-2,2]')} with homogeneous lower boundary data {m('u=0')}.</p>
<p>Because the initial fields satisfy the relation {m(r'v_0=4-3u_{0y}')}, the subsequent evolution under the full DLW system can be represented through two linear heat equations and a Laplace transformation over {m(r'0\le t\le0.01')}. Interval evaluation of these analytical representations provides continuous reference values and initial time derivatives with an absolute error bound of {m(r'10^{-13}')}.</p>
<p>As illustrated in Figures 5 and 6, the Gaussian test starts from a localized positive hump in {m('u')}, while {m('v')} varies symmetrically about the background value {m('v=4')} with opposite signs in the upper and lower halves of the strip and remains equal to four along the central section {m('y=0')}.</p>
{fig(5, 6)}
<p>The sinusoidal test (Figures 7 and 8) replaces the localized pulse in {m('x')} by a periodic cosine wave, so that {m('u')} alternates in sign along {m('x')} while the departure of {m('v')} from its background {m('v=4')} reverses sign across {m('y=0')}.</p>
{fig(7, 8)}
<p>Each numerical method is initialized by sampling the continuous reference fields at its native grid locations. Recall that both semi-discrete formulations place {m('u')} at transverse nodes and {m('v')} at edge midpoints, whereas FD places both fields at the nodes. Errors are evaluated directly at these native sites inside the specified interior region ({m(r'|x|\le R')} and {m(r'|y|<R')} for the soliton tests, and all {m('x')} nodes with {m(r'|y|\le1.8')} for the Gaussian and sinusoidal tests). At the final time {m('T=0.01')}, we record the maximum absolute errors</p>
{eq(r'E_u(T)=\max_{\mathcal G_u}\left|u_h(T)-u^*(T)\right|,\qquad E_v(T)=\max_{\mathcal G_v}\left|v_h(T)-v^*(T)\right|,')}
<p>where {m(r'\mathcal G_u')} and {m(r'\mathcal G_v')} denote the native lattice sites of the two physical fields within the evaluation region. As an initial diagnostic of the spatial discretization, we also record {m(r'E_{u_t}')} and {m(r'E_{v_t}')}, defined analogously as the maximum absolute differences between the spatially computed and exact continuous time derivatives at {m('t=0')}. In all tables below, bold entries indicate the smallest error among the compared methods for each case and field.</p></section>'''

section52 = f'''<section class="numerical-section" id="section-5.2"><h3>5.2 Comparison of spatial formulations</h3>
<p>We first compare the physical fields produced by Endpoint-SD, Centered-SD, and FD at {m('T=0.01')}. All three spatial formulations use the grid spacings {m(r'h=\Delta x=0.1')} and advance from the exact initial data using classical RK4 with {m(r'\Delta t=10^{-4}')}. Before examining the evolved fields, Table 2 summarizes the initial time-derivative errors at {m('t=0')}, which reflect the local consistency properties analyzed in Section 3.4.</p>
{T[2]}
<p>At {m('t=0')}, the two semi-discrete formulations show a clear division between the two components: Endpoint-SD gives the smallest initial {m('u_t')} defect {m(r'E_{u_t}')} in all four cases, whereas Centered-SD gives the smallest {m('v_t')} defect {m(r'E_{v_t}')}. This pattern is consistent with Proposition 3.4. In the first equation, both formulations are second-order consistent, and the difference in {m(r'E_{u_t}')} comes from the {m(r'O(h^2)')} auxiliary flux term retained by Centered-SD. In the second equation, however, the one-sided pairing of Endpoint-SD leaves a first-order {m(r'O(h)')} truncation term, which makes its initial {m('v_t')} error significantly larger than those of Centered-SD and FD.</p>
<p>Table 3 follows these initial states to {m('T=0.01')} and reports the resulting errors in the physical fields {m('u')} and {m('v')}. In the accompanying figures, the cross-section panels compare the continuous reference profiles at {m('y=0')} with the numerical values (using a verified 12-point local polynomial interpolation in {m('y')} whenever {m('y=0')} lies between native lattice lines), while the planar heatmaps and three-dimensional surfaces display the spatial distribution of the absolute errors across the evaluation region.</p>
{T[3]}
<p>Looking across Table 3, we see that Centered-SD maintains the smallest {m('v')} error in all four tests, while the ordering of the {m('u')} error depends on the test problem.</p>
<h4>One-soliton and two-soliton cases</h4>
<p>In the one-soliton test (Figures 9&ndash;12), all three formulations capture the shape and position of the central pulse. Comparing the two semi-discrete schemes, we notice that Centered-SD not only reduces the terminal {m('v')} error relative to Endpoint-SD by a factor of {m('72')} (from {m(r'5.547\times10^{-3}')} to {m(r'7.734\times10^{-5}')}), but also achieves a smaller terminal {m('u')} error by a factor of {m('2.8')} (reducing {m('E_u')} from {m(r'4.702\times10^{-4}')} to {m(r'1.677\times10^{-4}')}), reversing their initial ordering in Table 2. A simple explanation for this reversal lies in the coupled evolution of the two fields: because the first DLW equation contains the dispersive term {m('v_{xx}')}, the much larger {m(r'O(h)')} error incurred by Endpoint-SD in {m('v')} feeds back into the time derivative of {m('u')} as the wave evolves, whereas the symmetric staggered arrangement of Centered-SD keeps both components at second order.</p>
{fig(9, 10, 11, 12)}
<p>The two-soliton test (Figures 13&ndash;16) shows the exact same behavior across the two intersecting wave bands. Relative to Endpoint-SD, Centered-SD reduces the terminal {m('u')} error from {m(r'4.942\times10^{-4}')} to {m(r'1.792\times10^{-4}')} and the {m('v')} error from {m(r'7.076\times10^{-3}')} to {m(r'1.009\times10^{-4}')}. The improvement factors &mdash; about {m('2.8')} in {m('u')} and {m('70')} in {m('v')} &mdash; are nearly identical to those observed in the single-soliton case, and Centered-SD also improves upon the FD baseline in the second field by a factor of about {m('1.7')}.</p>
{fig(13, 14, 15, 16)}
<h4>Gaussian and sinusoidal cases</h4>
<p>In the smooth, small-amplitude Gaussian (Figures 17&ndash;20) and sinusoidal (Figures 21&ndash;24) tests, the field gradients are much milder and the terminal error ordering at {m('T=0.01')} follows the initial derivative defects of Table 2. Endpoint-SD gives the smallest {m('u')} error, while Centered-SD lies between Endpoint-SD and FD in {m('u')} and produces the smallest {m('v')} error in both tests. Specifically, Centered-SD reduces {m('E_v')} to {m(r'6.967\times10^{-9}')} in the Gaussian case (about {m('3.2')} times smaller than FD and {m('87')} times smaller than Endpoint-SD) and to {m(r'4.706\times10^{-9}')} in the sinusoidal case ({m('3.5')} times smaller than FD and {m('60')} times smaller than Endpoint-SD). Because the exact second field remains constant at {m('v=4')} along the symmetry line {m('y=0')}, the cross-sectional {m('v')} error along {m('y=0')} is near machine precision, while the heatmaps and surface plots show how the errors distribute symmetrically across the upper and lower halves of the strip.</p>
{fig(17, 18, 19, 20, 21, 22, 23, 24)}
<p>Overall, the spatial comparisons show that moving from the one-sided Endpoint-SD lattice to the symmetric staggered Centered-SD formulation substantially improves the approximation of the second field across all four regimes, and in the nonlinear soliton tests this improvement carries over to the first field as well. We therefore retain Centered-SD in the next two subsections to examine the effects of time integration and mesh redistribution.</p></section>'''

section53 = f'''<section class="numerical-section" id="section-5.3"><h3>5.3 Comparison of time integrators</h3>
<p>We next hold the Centered-SD spatial discretization fixed on the uniform grid ({m(r'h=\Delta x=0.1')}) and vary only the time integrator. Starting from the same initial data and using the same boundary conditions and Fourier {m('x')} operators, we advance each test problem from {m('t=0')} to {m('T=0.01')} with step size {m(r'\Delta t=10^{-4}')} using forward Euler, classical RK4, and Crank&ndash;Nicolson.</p>
{T[4]}
<p>Table 4 collects the terminal errors at {m('T=0.01')}. The RK4 columns reproduce the Centered-SD benchmarks from Table 3, and the implicit second-order Crank&ndash;Nicolson scheme matches these values to within a relative difference of at most {m(r'7.3\times10^{-3}')} (attained in {m('u')} for the two-soliton case). By contrast, first-order forward Euler shifts the error levels in opposite directions for the two physical components: it produces a larger {m('v')} error than RK4 in every test &mdash; by {m(r'3.8\%')} and {m(r'8.0\%')} in the two soliton cases, and by factors of {m('8.2')} and {m('9.0')} in the Gaussian and sinusoidal cases &mdash; yet it gives the smallest terminal {m('u')} error in all four tests, lying below the RK4 value by {m(r'0.8\%')}, {m(r'21\%')}, {m(r'82\%')}, and {m(r'38\%')}. Looking only at the final time {m('T=0.01')} therefore ranks the integrators differently depending on which component is inspected, without showing how these differences develop.</p>
<p>To see how the errors accumulate during the computation, we record the maximum absolute error over the native grid sites at every time step {m(r't_n=n\Delta t')},</p>
{eq(r'E_u^{(m)}(t_n)=\max_{\mathcal G_u}\left|u_h^{(m)}(t_n)-u^*(t_n)\right|,\qquad E_v^{(m)}(t_n)=\max_{\mathcal G_v}\left|v_h^{(m)}(t_n)-v^*(t_n)\right|,')}
<p>where {m('m')} labels the time integrator. Because the grid point attaining the maximum can shift as the wave moves, these curves track the evolution of the worst-case error in each field across the domain.</p>
{fig(25, 26)}
<p>Figures 25 and 26 plot the resulting error histories for {m('u')} and {m('v')}. In all four problems, the errors start at zero and grow monotonically without numerical oscillations, reaching their maxima at {m('T=0.01')}. For the one-soliton, Gaussian, and sinusoidal tests, the growth is nearly linear in {m('t')}, with the ratio {m('E_u(t)/t')} varying by less than {m(r'10\%')} over the interval; on the logarithmic vertical scale, this steady accumulation appears as a smooth concave curve. The two-soliton case follows the same near-linear trend up to about {m('t=0.009')} and then steepens, with {m('E_u(t)/t')} increasing by {m(r'36\%')} over the final tenth of the run. This late-stage steepening corresponds to the time window in which the two soliton branches meet and form sharper gradients on the scale of the grid.</p>
<p>Comparing the three curves within each panel, we see that RK4 and Crank&ndash;Nicolson lie on top of each other throughout the entire evolution, whereas the forward Euler curve is shifted vertically by a factor that remains nearly constant in time. For {m('u')} (Figure 25), the Euler curve lies below RK4 by factors near {m('0.99')}, {m('0.18')}, and {m('0.62')} in the one-soliton, Gaussian, and sinusoidal tests, and drifts from {m('0.97')} to {m('0.79')} during the two-soliton interaction. For {m('v')} (Figure 26), the Euler curve follows the same shape but is displaced above RK4 &mdash; by factors of {m('1.04')} and {m('1.08')} in the two soliton tests and {m('8.2')} and {m('9.0')} in the Gaussian and sinusoidal tests.</p>
<p>This opposite displacement is a straightforward consequence of adding a first-order temporal defect to a slowly varying spatial residual. In Centered-SD, the state variables {m(r'(u_k,\omega_k)')} are advanced in time and {m('v_k')} is recovered from the differentiated staggered relation {m(r'\dot v_k=\Delta_h\dot u_k+\frac2h(\dot\omega_k+\dot\omega_{k-1})')}. Through this relation, the leading {m(r'O(\Delta t)')} truncation error of forward Euler enters the two physical fields with opposite signs, partially canceling the spatial discretization error in {m('u')} while adding to it in {m('v')}. Confirming this interpretation, if we halve the time step to {m(r'\Delta t=5\times10^{-5}')}, the first-order defect diminishes and the Euler errors move back toward the RK4 benchmark in both components &mdash; changing from {m(r'(1.664\times10^{-4},\,8.026\times10^{-5})')} to {m(r'(1.671\times10^{-4},\,7.880\times10^{-5})')} in the one-soliton test, and from {m(r'(1.420\times10^{-4},\,1.090\times10^{-4})')} to {m(r'(1.560\times10^{-4},\,1.048\times10^{-4})')} in the two-soliton test. The smaller {m('u')} error of forward Euler in Table 4 is therefore a cancellation between temporal and spatial errors rather than a more accurate resolution of the wave.</p>
<p>Taken together, the terminal table and the time histories clarify three points. First, the rate at which the numerical solution departs from the continuous reference is governed by the spatial discretization: all three integrators share the same growth profile, which remains steady until sharper wave interactions develop. Second, at {m(r'\Delta t=10^{-4}')}, a second-order time integrator already matches the fourth-order benchmark, whereas a first-order scheme introduces a noticeable vertical shift, particularly in the more sensitive second field {m('v')}. Third, because temporal and spatial errors can combine with opposite signs in different components, tracking both fields over time is necessary to distinguish genuine accuracy from error cancellation. In Section 5.4, we therefore retain RK4 at {m(r'\Delta t=10^{-4}')} so that temporal errors remain negligible when comparing fixed and adaptive meshes.</p></section>'''

section54 = f'''<section class="numerical-section" id="section-5.4"><h3>5.4 Fixed and adaptive meshes</h3>
<p>In our final experiment, we examine how redistributing the shared {m('x')} nodes according to the conservation law of Section 4.3 affects the accuracy of Centered-SD. Both the uniform-mesh and adaptive-mesh calculations use the same number of nodes, the same uniform {m('y')} lattice ({m(r'h=\Delta x=0.1')}), and the same RK4 time step {m(r'\Delta t=10^{-4}')} up to {m('T=0.01')}. To ensure a direct comparison in which node placement is the only difference, both calculations evaluate {m('x')} derivatives using the mapped three-point centered difference operators {m('D_x')} and {m('D_{xx}')} of Section 4.3 (with zero node displacement and unit Jacobian on the uniform grid). Because these local difference operators are less accurate than the spectral Fourier multipliers used in Sections 5.2 and 5.3, the uniform-mesh errors reported below are larger than those in Table 3. We perform this comparison on the one- and two-soliton problems, where the fields decay to zero in the background. In the Gaussian and sinusoidal problems, the second field oscillates about {m('v=4')} so that the transverse-averaged conservation density vanishes identically, leaving the equidistribution mapping and mesh velocity of Section 4.3 undefined.</p>
<p>In the adaptive runs, the initial {m('x')} nodes are placed by equidistributing the transverse-averaged density {m(r'\bar\rho')} computed from the exact initial fields, and the nodes subsequently evolve according to the conservation-based velocity of Section 4.3. The averaged density ranges from {m('1.000')} in the background to {m('1.150')} across the wave core in the one-soliton case, and from {m('1.000')} to {m('1.050')} in the wider domain of the two-soliton case. Figure 27 plots the resulting local grid spacing, normalized by the uniform spacing {m(r'\Delta x=0.1')}, at {m('t=0')} and {m('T=0.01')}.</p>
{fig(27)}
<p>As seen in Figure 27, the equidistribution concentrates nodes in the region of larger density. In the one-soliton test, the local spacing contracts to {m(r'0.90\Delta x')} across the wave trough while stretching to {m(r'1.04\Delta x')} in the background; in the two-soliton test, it varies more mildly between {m(r'0.97\Delta x')} and {m(r'1.02\Delta x')}. Over the short evolution to {m('T=0.01')}, the initial and final node distributions are nearly indistinguishable: the maximum node displacement is {m(r'9.5\times10^{-4}')} in the one-soliton case and {m(r'5.2\times10^{-4}')} in the two-soliton case, and the total discrete mass of {m(r'\bar\rho')} is conserved to within {m(r'10^{-7}')} relative error. The spatial resolution pattern is thus established by the initial equidistribution and adjusted only slightly by the node motion during the run.</p>
<p>Table 5 compares the terminal errors at {m('T=0.01')} on the uniform and adaptive meshes, measuring the relative improvement via</p>
{eq(r'\mathcal R_f=100\left(1-\frac{E_f^{\mathrm{adaptive}}(T)}{E_f^{\mathrm{uniform}}(T)}\right)\%,\qquad f=u,v.')}
{T[5]}
<p>Positive values of {m(r'\mathcal R_f')} indicate an error reduction. The adaptive mesh lowers the errors in both physical fields for both test problems: by {m(r'11.7\%')} in {m('u')} and {m(r'17.4\%')} in {m('v')} for the one-soliton case, and by {m(r'6.0\%')} in {m('u')} and {m(r'5.6\%')} in {m('v')} for the two-soliton case. These improvements are modest and commensurate with the {m(r'3\%')}&ndash;{m(r'10\%')} local spacing reductions shown in Figure 27, but they occur consistently across both components without degrading either field. Moreover, a control calculation in which the initially equidistributed nodes are held fixed in time ({m(r'\mathcal V_i=0')}) yields reductions of {m(r'12.8\%')} and {m(r'16.3\%')} for the one-soliton case and {m(r'5.3\%')} and {m(r'5.8\%')} for the two-soliton case &mdash; within {m('1.1')} percentage points of the moving-mesh values in Table 5. Over this short time interval, the accuracy gain therefore comes primarily from the initial density-adapted node placement rather than from dynamic node motion.</p>
<p>To show where this reduction takes place in space, Figure 28 plots the transverse-maximum error profiles {m(r'\max_{|y|<5}|u_h-u^*|')} and {m(r'\max_{|y|<5}|v_h-v^*|')} as functions of {m('x')} for the one-soliton case. On the uniform mesh, the numerical error is not distributed evenly across the domain, but is localized along the central wave band {m(r'x\in[-3,3]')}. Because the conservation density {m(r'\bar\rho')} peaks in this same band, the equidistribution shifts nodes from the quiet background directly into the region where the truncation error is generated. As a result, the adaptive mesh lowers the error across the entire wave zone &mdash; reducing the main peak in {m('u')} from {m(r'6.74\times10^{-4}')} to {m(r'5.95\times10^{-4}')} and lowering the broad plateau in {m('v')} from {m(r'1.40\times10^{-3}')} to {m(r'1.16\times10^{-3}')}. We also notice that the relative gain in the one-soliton test is larger for {m('v')} ({m(r'17.4\%')}) than for {m('u')} ({m(r'11.7\%')}). This is natural in the Centered-SD formulation: the monitor density {m(r'\rho_k=1-\omega_k/h')} is a shifted rescaling of the auxiliary variable {m(r'\omega_k')}, which enters the staggered reconstruction {m(r'v_k=\Delta_hu_k+\frac2h(\omega_k+\omega_{k-1})')} and specifically weights the part of {m('v')} not captured by the backward difference of {m('u')}.</p>
{fig(28)}
<p>In summary, the mesh comparison illustrates both the utility and the natural scope of the conservation-based grid over the present test horizon. With a fixed node count and time integrator, equidistributing the semi-discrete conservation density places additional resolution along the soliton wave band and produces a consistent error reduction in both physical fields. At the same time, because the local difference operators remain second order and the transverse-averaged density varies moderately over the domain, the magnitude of the improvement is bounded by the local spacing compression. Finally, because the wave translates by only a small fraction of a grid cell over {m('T=0.01')}, the present experiments primarily test the static adaptation of the grid to the conservation density; longer-time simulations, in which the soliton core travels over many grid spacings, would be required to test the dynamic tracking capability of the moving mesh.</p></section>'''


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


paper = source
# Replace only the Section 5 introduction, then the four subsections. 5.5 is untouched.
intro_start = re.search(r'<section\b[^>]*\bid="section-5"[^>]*>', paper).start()
first_child = re.search(r'<section\b[^>]*\bid="section-5\.1"', paper)
paper = paper[:intro_start] + intro + paper[first_child.start():]
for identity, content in (('section-5.1', section51), ('section-5.2', section52),
                          ('section-5.3', section53), ('section-5.4', section54)):
    paper = replace_section(paper, identity, content)

paper = render(paper)
assert 'S5MATHS' not in paper and 'katex-error' not in paper


# ---------------------------------------------------------- tie-aware bold in Table 4
def sci(x):
    import math
    e = int(math.floor(math.log10(abs(x))))
    mant = x / 10 ** e
    if round(mant, 3) >= 10:
        mant /= 10
        e += 1
    return f'{mant:.3f}e{e}'


def rebold_time_table(html):
    start = html.index('<table id="table-time">')
    end = html.index('</table>', start) + len('</table>')
    table = html[start:end]
    body_start = table.index('<tbody>')
    body_end = table.index('</tbody>') + len('</tbody>')
    body = table[body_start:body_end]
    rows = []
    for row in re.findall(r'<tr>.*?</tr>', body, re.S):
        cells = re.findall(r'<td[^>]*>.*?</td>', row, re.S)
        assert len(cells) == 6, cells
        values = [float(re.search(r'data-value="([^"]+)"', c).group(1)) for c in cells]
        keep = row[:row.index('<td')]
        rebuilt = [keep]
        for idx, (cell, value) in enumerate(zip(cells, values)):
            field_cells = values[idx % 2::2]
            best = sci(min(field_cells))
            head = re.match(r'<td[^>]*>', cell).group()
            inner = re.sub(r'^(-?[\d.]+)e(-?\d+)$', r'\1 × 10<sup>\2</sup>', sci(value))
            rebuilt.append(head + (f'<strong>{inner}</strong>' if sci(value) == best else inner) + '</td>')
        rebuilt.append('</tr>')
        rows.append(''.join(rebuilt))
    new_body = '<tbody>' + ''.join(rows) + '</tbody>'
    return html[:start] + table[:body_start] + new_body + table[body_end:] + html[end:]


paper = rebold_time_table(paper)

# ------------------------------------------------------------------- validation
for identity in ('section-1', 'section-2', 'section-2.1', 'section-2.2', 'section-2.3', 'section-2.4',
                 'section-3', 'section-3.1', 'section-3.2', 'section-3.3', 'section-3.4', 'section-4',
                 'section-4.1', 'section-4.2', 'section-4.3', 'section-4.4', 'section-5.5', 'section-6',
                 'appendix-A', 'appendix-B', 'appendix-C', 'appendix-D', 'appendix-G'):
    assert paper[slice(*section_span(paper, identity))] == source[slice(*section_span(source, identity))], identity

assert paper.count('<figure') == 28 and paper.count('<table id=') == 5
for number in range(1, 29):
    assert paper.count(f'<strong>Figure {number}.</strong>') == 1, number
for number in range(1, 6):
    assert paper.count(f'<caption>Table {number}.') == 1, number
for ref in ('Proposition 3.4', 'Section 2.1', 'Section 3.4', 'Section 4.3'):
    assert ref in paper, ref

current = hashlib.sha256(PAPER.read_bytes()).hexdigest()
assert current == hashlib.sha256(BASELINE.read_bytes()).hexdigest(), 'manuscript changed concurrently'
PAPER.write_text(paper, encoding='utf-8')
for identity in ('section-5', 'section-5.1', 'section-5.2', 'section-5.3', 'section-5.4'):
    a, b = section_span(paper, identity)
    (HERE / f'{identity}.html').write_text(paper[a:b], encoding='utf-8')

manifest = dict(before_sha256=current, after_sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest(),
                replaced=['section-5', 'section-5.1', 'section-5.2', 'section-5.3', 'section-5.4'],
                blocks_kept=dict(figures=28, tables=5), formulas=len(maths))
(HERE / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2))
