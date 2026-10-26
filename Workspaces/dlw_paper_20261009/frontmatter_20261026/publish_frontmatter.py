"""Build Abstract, Introduction and Conclusions from the earlier draft.

The narrative follows report/dlw_paper_draft.html; the naming, the statement of
the two formulations, the numerical findings and the reference list are aligned
with the present manuscript.  Sections 4.4 and 5.5 are left untouched.
"""
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
    token = 'FMMATH' + str(len(maths)) + 'END'
    maths.append(dict(tex=tex, display=display))
    return token


def render(text):
    js = ("const fs=require('fs'),k=require(process.argv[1]);"
          "process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8'))"
          ".map(f=>k.renderToString(f.tex,{displayMode:f.display,throwOnError:true,strict:'error'}))));")
    katex = ROOT / 'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js'
    r = subprocess.run(['node', '-e', js, str(katex)], input=json.dumps(maths), text=True,
                       encoding='utf-8', capture_output=True, check=True)
    for i, result in enumerate(json.loads(r.stdout)):
        text = text.replace('FMMATH' + str(i) + 'END', result)
    return text


source = BASELINE.read_text(encoding='utf-8')

# ---------------------------------------------------------------------- abstract
abstract = f"""<section id="abstract"><h2>Abstract</h2>
<p>This paper constructs two integrable semi-discretizations of the {m('(2+1)')}-dimensional dispersive long-wave system and compares how accurately they compute its waves. Retaining two lattice directions of the Hirota&ndash;Miwa equation and introducing {m('x')} and {m('t')} through a Miwa expansion yields a bilinear lattice whose endpoint pairings define the endpoint-based semi-discretization (Endpoint-SD). Placing the same pairings symmetrically, with the bilinear parameter shifted by half a lattice spacing and the {m(r'\tau')} functions staggered, gives the centered semi-discretization (Centered-SD). Both retain Gram determinant solutions of arbitrary finite order, nonlinear equations for the physical fields and Darboux&ndash;Lax representations, and their exact fields approach the continuous ones at second order. The two differ in the second equation: Centered-SD is second-order consistent there as well, whereas Endpoint-SD leaves a first-order residual. The formulations are compared with each other and with a collocated finite-difference scheme on four initial-value problems&mdash;one- and two-soliton waves, a periodic Gaussian pulse and a sinusoidal wave&mdash;using Fourier differentiation in {m('x')}, a lattice in {m('y')}, three time integrators and a conservation-based moving mesh. Centered-SD attains the smallest second-field error in every test, while the ordering of the first field follows the initial derivative defects. Crank&ndash;Nicolson matches RK4, the apparent first-field accuracy of forward Euler proves to be an error cancellation, and equidistributing the semi-discrete conservation density lowers both errors without adding nodes.</p>
</section>"""

# ------------------------------------------------------------------ introduction
P1 = ("<p>The propagation and interaction of waves in shallow water have long attracted interest in the study of "
      "nonlinear wave phenomena. As waves evolve, nonlinear effects and dispersion can influence their profiles in "
      "different ways, and their balance can support coherent waves that persist during propagation. Nonlinear "
      "long-wave equations describe these effects in a reduced form, allowing wave motion to be studied without "
      "retaining the full complexity of the underlying fluid equations. Within this class, integrable models have "
      "received sustained attention for the analytical insight they offer. Their exact solutions make it possible to "
      "follow the evolution of individual waves and examine their interactions, while bilinear formulations and Lax "
      "representations reveal mathematical structures underlying these solutions. These analytical results also "
      "provide useful reference points for numerical studies, in which wave profiles and their evolution are "
      "represented on a discrete mesh. Passing from a continuous model to such a representation introduces choices "
      "that affect both the approximation of the waves and the mathematical structure of the resulting equations. "
      "Integrable discretization seeks to retain this connection, bringing the construction of discrete equations "
      "together with the study of their exact solutions and continuum limits.</p>")

P2 = ("<p>The (2+1)-dimensional dispersive long wave (DLW) system extends the dispersive long wave equation to two "
      "spatial dimensions [1] and has been studied in connection with wave motion in wide channels and open seas of "
      "finite depth [3,4]. Since its introduction by Boiti, Leon and Pempinelli, its wave solutions have been studied "
      "through several closely related analytical approaches. The inverse spectral transform, B&auml;cklund "
      "transformation and superposition formula established in the original work [1] were followed by nonlinear "
      "transformations [2] and bilinear methods [3], which offered further ways to generate solutions and understand "
      "their relations. Determinant representations give these relations a concrete form. Hu, Xu and Yu developed "
      "Grammian and Wronskian solutions [4], and Sheng and Yu used a KP-hierarchy reduction to obtain Gram "
      "determinant solutions describing solitons, line breathers and rational waves on constant and periodic "
      "backgrounds [5].</p>")

P3 = ("<p>The bilinear relations underlying these solutions also offer a starting point for introducing a lattice "
      "[15]. In this approach, B&auml;cklund transformations relate neighbouring lattice values, allowing discrete "
      "equations to be constructed together with their solution structures. This idea has been developed for "
      "semi-discrete soliton equations [7] and extended to systems with two spatial dimensions [8]. For the DLW "
      "system, a further connection comes from its bilinear relation to the (2+1)-dimensional sinh-Gordon equation "
      "[5], whose integrable discretizations admit determinant solutions and B&auml;cklund&ndash;Lax structures [6]. "
      "Together with earlier studies of discrete DLW systems [11], these developments motivate a closer examination "
      "of how the continuous DLW solution family can be carried onto a spatial lattice, and how the resulting wave "
      "fields compare with their continuous counterparts.</p>")

P4 = ("<p>With these advancements, there is potential to study the preservation of integrable structure and the "
      "approximation of continuous waves within the same construction. With this in mind, we ask how to introduce a "
      "spatial lattice that preserves the bilinear and determinant structure, supports a consistent reconstruction "
      "of the physical fields, and admits a quantitative comparison between its exact solutions and those of the "
      "continuous system.</p>")

P5 = f"""<p>To address this question, we seek a semi-discrete description of the DLW system. First, the construction should retain the connection between explicit wave solutions and the integrable structure governing their evolution. Gram determinant solutions make the discrete wave fields accessible to analytical study, while a corresponding Lax representation should recover the same nonlinear equations through its compatibility conditions. Second, we wish to understand how the lattice changes the continuous wave fields. This requires a quantitative comparison of the corresponding exact solutions, complementing the recovery of the continuous equations in the limit. The comparison of exact wave fields also provides a basis for studying numerical approximations. Once the semi-discrete system is used in computation, the choice of nonlinear formulation, time integrator and mesh can affect how accurately these waves are resolved. We therefore seek to understand these effects through comparisons with the exact solutions, using classical one-step integrators [10] and a mesh obtained by equidistributing a semi-discrete conservation density, in the spirit of the self-adaptive moving mesh methods developed for integrable systems [9,12,13] and of adaptive mesh theory [14].</p>"""

P6 = f"""<p>In Section 2, we construct the semi-discrete DLW systems from the continuous bilinear formulation and the Gram determinant solutions of Sheng and Yu [5]. Retaining two lattice directions of the Hirota&ndash;Miwa equation and introducing {m('x')} and {m('t')} through a Miwa expansion gives an endpoint pairing of the {m(r'\tau')} functions, which we call Endpoint-SD. Placing the same pairings symmetrically, with the bilinear parameter shifted by half a lattice spacing and the {m(r'\tau')} functions staggered, gives Centered-SD. Both constructions retain Gram determinant solutions of arbitrary finite order. Section 3 derives the corresponding nonlinear equations for the physical fields and their Darboux&ndash;Lax representations, and then examines how the lattice fields approach the continuous ones: the exact fields of both formulations converge at second order, and both first equations are second-order consistent, but the second Endpoint-SD equation leaves a first-order residual whose coefficient is identified explicitly. Section 4 sets out the numerical formulation used in the computations, namely Fourier differentiation in {m('x')}, the two semi-discrete formulations together with a collocated finite-difference baseline, the initial and boundary data, the time integrators, and the moving mesh. Section 5 compares the formulations on four initial-value problems&mdash;a one-soliton wave, a two-soliton interaction, a periodic Gaussian pulse and a sinusoidal wave&mdash;first through the initial time derivatives and then in the evolved fields, before isolating the effects of time integration and of node redistribution. Section 6 collects the conclusions.</p>"""

introduction = ('<section id="section-1"><h2>1. Introduction</h2>\n' +
                '\n'.join([P1, P2, P3, P4, P5, P6]) + '\n</section>')

# ------------------------------------------------------------------- conclusions
C1 = f"""<p>In this work, we have connected the construction of integrable semi-discrete DLW systems with an analysis of their numerical approximation. Starting from the continuous bilinear equations, we retained two lattice directions of the Hirota&ndash;Miwa equation and introduced {m('x')} and {m('t')} through a Miwa expansion, which places the {m(r'\tau')} functions at the endpoints of each lattice interval. Shifting the bilinear parameter by half a spacing and staggering the {m(r'\tau')} functions instead places the same pairings symmetrically and gives the centered formulation. Both constructions retain Gram determinant solutions of arbitrary finite order and remain positive on the stated parameter domain. Eliminating the logarithmic variables gives the nonlinear equations of Endpoint-SD and Centered-SD, for which we established Darboux&ndash;Lax representations and verified their compatibility with the nonlinear equations.</p>"""

C2 = f"""<p>The explicit solutions also allow us to follow how the discrete wave fields approach their continuous counterparts. The exact physical fields of both formulations converge at second order on the stated smooth branches, and both first equations are second-order consistent. The second equations distinguish them. Endpoint-SD leaves a first-order residual {m(r'\frac h4\partial_x(v^2-u_y^2-8v)')}, derived in Proposition&nbsp;3.4, whereas Centered-SD is second-order consistent in both equations. This difference is not merely formal: with common continuous samples at {m('t=0')}, it produces the first-order defect in the initial time derivative of {m('v')} recorded in the experiments, and that defect is what separates the two formulations once the waves are evolved.</p>"""

C3 = f"""<p>When the remaining variables are discretized, the choice of formulation becomes consequential even though both describe the same exact semi-discrete fields. Centered-SD gives the smaller maximum error in the second field in all four tests, by factors of {m('60')} to {m('87')} relative to Endpoint-SD and {m('1.7')} to {m('3.5')} relative to the collocated finite-difference baseline. Its first field is not uniformly better: in the one- and two-soliton tests it reduces the first-field error relative to Endpoint-SD by factors near {m('2.8')}, whereas in the Gaussian and sinusoidal tests Endpoint-SD retains the smallest first-field error. Reading the two components together, and comparing the initial defects of Table&nbsp;2 with the evolved errors of Table&nbsp;3, explains the reversal. The first-order defect of Endpoint-SD sits in {m('v')}, and the dispersive term {m('v_{xx}')} feeds it back into {m('u')} as the wave evolves, so the initial advantage in {m('u_t')} survives only where the data are smooth and the amplitude small.</p>"""

C4 = f"""<p>With Centered-SD as the spatial formulation, we then examined how time integration and node placement affect the computation. At the tested resolution, Crank&ndash;Nicolson and RK4 give nearly coincident error histories, whereas forward Euler moves the two fields in opposite directions: its first-field error is the smallest of the three in every test, while the same first-order defect raises its second-field error, and halving the step brings both values back toward the RK4 level. The agreement at consecutive steps therefore reflects a cancellation between temporal and spatial errors rather than a more accurate resolution of the wave. For the mesh, the conservation law of the semi-discrete system supplies a density whose equidistribution concentrates nodes along the wave band. With the node count and the time step unchanged, the adaptive mesh lowers the maximum error in both fields, by {m('11.7\\%')} and {m('17.4\\%')} in the one-soliton test and by {m('6.0\\%')} and {m('5.6\\%')} in the two-soliton test; holding the initially equidistributed nodes fixed reproduces these reductions to within {m('1.1')} percentage points, so over the present horizon the gain comes from the initial redistribution rather than from the node motion.</p>"""

C5 = ("<p>Our work illustrates how the analytical structure of a semi-discrete system can inform both the "
      "interpretation and the design of its numerical approximation. The exact solutions let us follow the changes "
      "introduced by the lattice, the error coefficients explain why formulations with the same formal order can "
      "perform differently on the same wave, and the conservation law obtained from the semi-discrete system turns "
      "that structure into a rule for allocating the available nodes. At the same time, the present comparisons are "
      "finite-time and confined to a fixed resolution: over the interval examined the wave translates by a small "
      "fraction of a grid cell, so the dynamic part of the mesh construction is only partly exercised, and longer "
      "runs, in which the soliton crosses many cells, would be required to test its tracking capability. Extending "
      "the same construction to longer horizons, and separating the effect of the lattice from that of the time "
      "integrator more sharply, remain natural next steps.</p>")

conclusions = ('<section id="section-6"><h2>6. Conclusions</h2>\n' +
               '\n'.join([C1, C2, C3, C4, C5]) + '\n</section>')

# ------------------------------------------------------------------- references
REFS = [
    ('M. Boiti, J.J.-P. Leon, F. Pempinelli. Spectral transform for a two spatial dimension extension of the '
     'dispersive long wave equation. <em>Inverse Problems</em> <strong>3</strong> (1987), 371&ndash;387.',
     'https://doi.org/10.1088/0266-5611/3/3/007', 'DOI'),
    ('M. Wang, Y. Zhou, Z. Li. A nonlinear transformation of the dispersive long wave equations in (2+1) '
     'dimensions and its applications. <em>Journal of Nonlinear Mathematical Physics</em> <strong>5</strong> '
     '(1998), 120&ndash;125.', 'https://doi.org/10.2991/jnmp.1998.5.2.2', 'DOI'),
    ('K. Sun, B. Tian, W.-J. Liu, M. Li, Q.-X. Qu, Y. Jiang. Symbolic-computation study on the (2+1)-dimensional '
     'dispersive long wave system. <em>SIAM Journal on Applied Mathematics</em> <strong>70</strong> (2010), '
     '2259&ndash;2272.', 'https://doi.org/10.1137/090774847', 'DOI'),
    ('J. Hu, Z.-W. Xu, G.-F. Yu. Determinant structure for the (2+1)-dimensional dispersive long wave system. '
     '<em>Applied Mathematics Letters</em> <strong>62</strong> (2016), 76&ndash;83.',
     'https://doi.org/10.1016/j.aml.2016.07.003', 'DOI'),
    ('H.-H. Sheng, G.-F. Yu. Solitons, breathers and rational solutions for a (2+1)-dimensional dispersive long '
     'wave system. <em>Physica D</em> <strong>432</strong> (2022), 133140.',
     'https://doi.org/10.1016/j.physd.2021.133140', 'DOI'),
    ('X.-B. Hu, G.-F. Yu. Integrable discretizations of the (2+1)-dimensional sinh-Gordon equation. '
     '<em>Journal of Physics A: Mathematical and Theoretical</em> <strong>40</strong> (2007), 12645&ndash;12659.',
     'https://doi.org/10.1088/1751-8113/40/42/S10', 'DOI'),
    ('Y. Zhang, X. Chang, J. Hu, X. Hu, H.-W. Tam. Integrable discretization of soliton equations via bilinear '
     'method and B&auml;cklund transformation. <em>Science China Mathematics</em> <strong>58</strong> (2015), '
     '279&ndash;296.', 'https://doi.org/10.1007/s11425-014-4952-6', 'DOI'),
    ('G.-F. Yu, Z.-W. Xu. Dynamics of a differential-difference integrable (2+1)-dimensional system. '
     '<em>Physical Review E</em> <strong>91</strong> (2015), 062902.',
     'https://doi.org/10.1103/PhysRevE.91.062902', 'DOI'),
    ('B.-F. Feng, H.-H. Sheng, G.-F. Yu. Integrable semi-discretizations and self-adaptive moving mesh method for '
     'a generalized sine-Gordon equation. <em>Numerical Algorithms</em> <strong>94</strong> (2023), '
     '351&ndash;370.', 'https://doi.org/10.1007/s11075-023-01504-1', 'DOI'),
    ('E. Hairer, S. P. N&oslash;rsett, G. Wanner. <em>Solving Ordinary Differential Equations I: Nonstiff '
     'Problems</em>. 2nd revised ed., Springer, 1993.',
     'https://link.springer.com/book/10.1007/978-3-540-78862-1', 'Publisher'),
    ('S.-F. Tian, T.-T. Zhang, P.-L. Ma, X.-Y. Zhang. Lie symmetries and nonlocally related systems of the '
     'continuous and discrete dispersive long waves system by geometric approach. <em>Journal of Nonlinear '
     'Mathematical Physics</em> <strong>22</strong> (2015), 180&ndash;193.',
     'https://doi.org/10.1080/14029251.2015.1023562', 'DOI'),
    ('B.-F. Feng, K. Maruno, Y. Ohta. A self-adaptive moving mesh method for the Camassa&ndash;Holm equation. '
     '<em>Journal of Computational and Applied Mathematics</em> <strong>235</strong> (2010), 229&ndash;243.',
     'https://doi.org/10.1016/j.cam.2010.05.044', 'DOI'),
    ('B.-F. Feng, K. Maruno, Y. Ohta. Self-adaptive moving mesh schemes for short pulse type equations and their '
     'Lax pairs. <em>Pacific Journal of Mathematics for Industry</em> <strong>6</strong> (2014), 8.',
     'https://doi.org/10.1186/s40736-014-0008-7', 'DOI'),
    ('W. Huang, R. D. Russell. <em>Adaptive Moving Mesh Methods</em>. Applied Mathematical Sciences, vol. 174, '
     'Springer, 2011.', 'https://doi.org/10.1007/978-1-4419-7916-2', 'DOI'),
    ('R. Hirota. <em>The Direct Method in Soliton Theory</em>. Cambridge Tracts in Mathematics, vol. 155, '
     'Cambridge University Press, 2004.', 'https://doi.org/10.1017/CBO9780511543043', 'DOI'),
]
assert len(REFS) == 15
refs_html = '<ol>\n' + '\n'.join(
    f'<li>{text} <a href="{href}">{label}</a>.</li>' for text, href, label in REFS) + '\n</ol>'

GUIDE = ("<p class=\"status\">2026-10-26（Front matter）：Abstract、Introduction、Section 6 Conclusions 由既有稿 "
         "report/dlw_paper_draft.html 的同名部分改写而成，叙述与数据对齐当前稿（Endpoint-SD／Centered-SD／FD、表 2–5、"
         "图 25–28），PE/PF 旧名已替换；参考文献补全为 15 条（取自旧稿），正文原 [1]（Sheng–Yu）改为 [5]、原 [2]"
         "（Feng 等 mCH）改为 [15]（Hirota 专著），因原 [2] 与所引“Hirota–Miwa Gram 构造”不符。4.4 与 5.5 未动。</p>\n")

# ------------------------------------------------------------------------ apply
def replace_block(text, pattern, new):
    hits = list(re.finditer(pattern, text, re.S))
    assert len(hits) == 1, (pattern, len(hits))
    return text[:hits[0].start()] + new + text[hits[0].end():]


out = source
out = replace_block(out, r'<section id="abstract">.*?</section>', abstract)
out = replace_block(out, r'<section id="section-1">.*?</section>', introduction)
out = replace_block(out, r'<section id="section-6">.*?</section>', conclusions)
out = replace_block(out, r'<section id="references"><h2>References</h2>\s*<ol>.*?</ol>',
                    '<section id="references"><h2>References</h2>\n' + refs_html)

guide_head = '<h2>Appendix G. Editorial guide（暂存，投稿前移除）</h2>'
assert out.count(guide_head) == 1
out = out.replace(guide_head, guide_head + '\n' + GUIDE)

for old, new in [
    ('continuous Gram construction of Sheng and Yu [1].', 'continuous Gram construction of Sheng and Yu [5].'),
    ('We use the inverse-spacing convention and Gram construction in [2]. Set',
     'We use the inverse-spacing convention and Gram construction in [15]. Set'),
    ('In the Hirota&ndash;Miwa Gram construction [2], the',
     'In the Hirota&ndash;Miwa Gram construction [15], the'),
]:
    if old in out:
        out = out.replace(old, new)
    else:
        assert old.replace('&ndash;', '–') in out, old
        out = out.replace(old.replace('&ndash;', '–'), new.replace('&ndash;', '–'))

out = render(out)
assert 'FMMATH' not in out
PAPER.write_text(out, encoding='utf-8')

manifest = dict(
    before=dict(path=str(BASELINE.relative_to(ROOT)), sha256=hashlib.sha256(BASELINE.read_bytes()).hexdigest()),
    after=dict(path='dlw-paper.html', sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest()),
    replaced=['section#abstract', 'section#section-1', 'section#section-6', 'section#references ol'],
    citations_remapped={'[1] Sheng and Yu': '[5]', '[2] Gram construction': '[15]'},
    formulas=len(maths),
    references=len(REFS),
)
(HERE / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2))
