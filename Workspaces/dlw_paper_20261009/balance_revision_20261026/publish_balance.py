"""Balanced revision: Abstract, Introduction, the 5.2 summary paragraphs, Conclusions."""
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
    token = 'BAMATH' + str(len(maths)) + 'END'
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
        text = text.replace('BAMATH' + str(i) + 'END', result)
    return text


def para(text):
    parts = text.split('$')
    assert len(parts) % 2 == 1, 'unbalanced dollars'
    out = []
    for i, part in enumerate(parts):
        out.append(m(part) if i % 2 else part.replace('&', '&amp;').replace('—', '&mdash;'))
    return '<p>' + ''.join(out) + '</p>'


# ---------------------------------------------------------------------- abstract
ABSTRACT = (
    "We study the integrable semi-discretization and numerical approximation of the $(2+1)$-dimensional "
    "dispersive long-wave (DLW) system, aiming to understand how different lattice arrangements at the bilinear "
    "$\\tau$-function level influence the reconstructed physical wave fields. Starting from the Hirota–Miwa "
    "equation and a two-time Miwa expansion, we discretize the transverse coordinate $y$ while keeping $x$ and $t$ "
    "continuous, obtaining two complementary semi-discrete formulations within a common bilinear framework: an "
    "endpoint-based formulation (Endpoint-SD) that follows directly from the unshifted Miwa reduction, and a "
    "centered staggered formulation (Centered-SD) obtained through a half-step parameter shift. For both "
    "formulations, we construct explicit Gram determinant solutions, establish positivity conditions for smooth "
    "physical fields, and derive compatible Darboux–Lax pairs alongside closed nonlinear field equations. While "
    "Endpoint-SD yields a direct two-field system with a compact structure, Centered-SD introduces an auxiliary "
    "logarithmic difference that restores full second-order consistency to both physical equations and provides an "
    "intrinsic semi-discrete conservation law. Numerical experiments on one-soliton, two-soliton, Gaussian, and "
    "sinusoidal initial data illustrate the respective strengths of the two schemes. Endpoint-SD gives the "
    "smallest initial $u_t$ errors and achieves the highest accuracy for the first field $u$ in the smooth "
    "Gaussian and sinusoidal regimes, whereas Centered-SD consistently improves the second field $v$ across all "
    "tests and achieves smaller errors in both components during nonlinear soliton propagation and interaction. We "
    "further examine Centered-SD under forward Euler, RK4, and Crank–Nicolson time integration by tracking "
    "full-time error histories, and demonstrate that redistributing the spatial nodes according to its native "
    "semi-discrete conservation density systematically reduces wave-band errors in both physical fields."
)

# ------------------------------------------------------------------ introduction
INTRO = [
    "The $(2+1)$-dimensional dispersive long-wave (DLW) system models the evolution of shallow-water waves in two "
    "horizontal spatial dimensions under weak nonlinearity and dispersion. Beyond its hydrodynamic relevance, the "
    "continuous DLW system is a classic higher-dimensional integrable model that admits a Hirota bilinear "
    "representation, multi-soliton and breather solutions in Gram determinant form, and compatible linear Lax "
    "problems [1–4]. In particular, Sheng and Yu [5] established a systematic bilinear representation and "
    "continuous Gram construction that connect pairs of positive $\\tau$ functions directly to smooth physical "
    "wave fields.",

    "When transitioning from continuous integrable theory to numerical computation, structure-preserving or "
    "integrable discretizations offer a compelling bridge [7,8]. By deriving discrete lattice equations from "
    "fundamental bilinear identities—most notably the Hirota–Miwa equation via Miwa's continuous-time expansion "
    "[15]—one can preserve exact solvability, determinant solution structures, and Darboux–Lax compatibility on a "
    "discrete grid. Yet an important and often underappreciated question lies between the bilinear lattice and "
    "practical scientific computing: how do structural arrangements at the $\\tau$-function level translate into "
    "approximation accuracy for the actual physical fields? In a bilinear semi-discretization, two lattices may be "
    "algebraically equivalent up to a parameter shift at fixed grid spacing and may share the exact same "
    "determinant machinery, while inducing markedly different truncation errors once logarithmic derivatives and "
    "lattice differences are taken to reconstruct the physical variables. Understanding this interplay—between "
    "bilinear lattice geometry, nonlinear field reconstruction, temporal integration, and spatial mesh "
    "distribution—is the central motivation of the present work. The same questions arise for other integrable "
    "semi-discrete systems [6–9] and for discrete DLW-type reductions [11], while the moving meshes used here "
    "follow the self-adaptive constructions built on semi-discrete conservation laws [9,12,13] and the general "
    "theory of equidistribution [14]; the classical one-step integrators of Section 4 are taken from [10].",

    "In this paper, we explore these connections by developing and comparing two integrable transverse "
    "semi-discretizations of the $(2+1)$-dimensional DLW system, discretizing $y$ with lattice spacing $h$ while "
    "keeping $x$ and $t$ continuous. Retaining two lattice directions in the Hirota–Miwa equation and applying a "
    "Miwa expansion leads naturally to the endpoint-based semi-discretization (Endpoint-SD), which pairs $\\tau$ "
    "functions at the interval endpoints. Examining its continuum limit motivates a symmetric placement of the "
    "same bilinear pairings: shifting the operator reference parameter by $h/2$ and interpreting the $\\tau$ "
    "functions on a staggered grid yields the centered semi-discretization (Centered-SD). Both formulations arise "
    "along the same bilinear construction, share a common family of positive Gram determinant solutions, and admit "
    "compatible Darboux–Lax representations of identical operator form.",

    "Reconstructing the nonlinear physical fields $(u, v)$ reveals the distinct analytical features of the two "
    "arrangements. Endpoint-SD translates the bilinear equations directly into a closed system for the physical "
    "fields without auxiliary variables, providing a first-order bilinear approximation that is already "
    "second-order accurate in the first field equation. Centered-SD incorporates an auxiliary logarithmic "
    "difference $\\omega_k$ to achieve full second-order consistency in both physical equations, and we show that "
    "its exact Gram determinant solutions converge to the continuous wave fields at $O(h^2)$. Equally important, "
    "the evolution equation for $\\omega_k$ in Centered-SD provides an exact semi-discrete conservation law. We "
    "use this conserved density to construct a shared-node moving mesh in $x$ that concentrates resolution in the "
    "wave core while preserving the transverse lattice structure.",

    "We then test the formulations numerically across four representative regimes: a one-soliton wave, a "
    "two-soliton interaction, a localized Gaussian profile, and a periodic sinusoidal wave. Comparing "
    "Endpoint-SD, Centered-SD, and a collocated finite-difference (FD) baseline shows how each scheme performs "
    "across different wave structures: Endpoint-SD yields the smallest initial $u_t$ defects and the most accurate "
    "$u$ field in the smooth Gaussian and sinusoidal tests, whereas Centered-SD provides the most accurate $v$ "
    "field in all four cases and achieves lower errors in both physical components for the steeper soliton "
    "problems. Retaining Centered-SD, we next compare forward Euler, RK4, and Crank–Nicolson by following the "
    "maximum errors over time, which clarifies how spatial truncation and temporal integration combine in each "
    "component. Finally, we compare fixed and conservation-adapted meshes on the soliton tests, showing that "
    "equidistributing the integrable conservation density consistently improves the numerical approximation "
    "across both physical fields.",

    "The paper is organized as follows. Section 2 introduces the continuous DLW bilinear system, derives "
    "Endpoint-SD and Centered-SD from the Hirota–Miwa equation, and constructs their positive Gram determinant "
    "solutions. Section 3 develops the nonlinear physical-field equations, establishes their Darboux–Lax "
    "representations, and analyzes their continuum consistency. Section 4 describes the spatial discretization in "
    "$x$, the boundary data and time integrators, and the conservation-based moving mesh. Section 5 presents the "
    "numerical experiments, and Section 6 summarizes our conclusions.",
]

# -------------------------------------------------- Section 5.2 closing paragraphs
S52 = [
    "Taken together, the initial diagnostics in Table 2 and the terminal errors in Table 3 show how the two "
    "integrable semi-discretizations complement each other across different wave regimes. Because Endpoint-SD "
    "reconstructs the physical fields directly without the $O(h^2)$ auxiliary flux term, it achieves the smallest "
    "initial derivative defect in $u_t$ across all four tests, and in the small-amplitude Gaussian and sinusoidal "
    "problems this advantage carries over to the terminal $u$ field at $T = 0.01$. In the steeper one- and "
    "two-soliton regimes, however, the coupled evolution links the accuracy of $u$ more closely to that of $v$ "
    "through the dispersive term $v_{xx}$ in the first equation.",

    "By placing the $\\tau$ functions and bilinear parameters symmetrically, Centered-SD achieves second-order "
    "consistency in both equations. As a result, it yields the smallest error in the second field $v$ across all "
    "four test problems—improving upon both Endpoint-SD and the collocated FD baseline—and in the soliton tests "
    "this improved resolution of $v$ also leads to a more accurate approximation of $u$ than Endpoint-SD. Because "
    "Centered-SD provides balanced second-order accuracy across both components and supplies the conservation law "
    "needed for mesh adaptation, we retain it in Sections 5.3 and 5.4 to examine time integration and adaptive "
    "node redistribution.",
]

# ------------------------------------------------------------------- conclusions
CONCL = [
    "In this paper, we have investigated the integrable semi-discretization and numerical approximation of the "
    "$(2+1)$-dimensional dispersive long-wave system, connecting the bilinear lattice construction to the "
    "practical computation of physical wave fields. By deriving Endpoint-SD and Centered-SD from a common "
    "Hirota–Miwa reduction, we obtained two integrable formulations that share explicit positive Gram determinant "
    "solutions and compatible Darboux–Lax pairs, while offering different trade-offs in physical-field "
    "reconstruction.",

    "Our analytical and numerical results deepen our understanding of the semi-discrete DLW system in three main "
    "respects: First, comparing the spatial formulations clarifies how the arrangement of the bilinear pairings "
    "shapes the accuracy of the physical variables. Endpoint-SD provides a direct and compact two-field "
    "formulation that gives the smallest initial $u_t$ residual and performs very well for the first field $u$ on "
    "smooth, small-amplitude Gaussian and sinusoidal waves. Centered-SD, by introducing a symmetric staggered "
    "placement, achieves full second-order consistency in both equations. This symmetry consistently delivers the "
    "highest accuracy in the second field $v$ across all test regimes, and in nonlinear soliton propagation and "
    "interaction it also improves the evolution of $u$ through the dispersive coupling between the two components.",

    "Second, our comparison of time integrators shows the value of following full error histories alongside "
    "terminal error tables. Tracking the errors at every time step demonstrates that the numerical solution "
    "departs from the continuous reference at a steady, nearly linear rate governed by the spatial discretization, "
    "steepening only when interacting waves form sharper gradients. At the chosen step size, second-order "
    "Crank–Nicolson and fourth-order RK4 produce virtually identical trajectories. Examining the full time "
    "evolution also explains why first-order forward Euler can show a smaller terminal error in $u$ while "
    "producing a larger error in $v$: its temporal truncation error enters the two reconstructed fields with "
    "opposite signs, partially canceling the spatial error in one component while adding to it in the other.",

    "Finally, the adaptive-mesh experiments illustrate a direct practical benefit of preserving the integrable "
    "structure in numerical computation. The nonlinear formulation of Centered-SD naturally supplies an exact "
    "semi-discrete conservation law through its auxiliary variable. Using this conserved density to equidistribute "
    "the shared $x$ nodes automatically concentrates resolution along the soliton wave bands where the numerical "
    "error is generated. Without increasing the node count or changing the time integrator, this "
    "conservation-guided redistribution systematically lowers the errors across the wave band in both $u$ and $v$. "
    "Over the short time horizon tested here, this improvement comes primarily from the initial density-adapted "
    "node placement, while the coupled moving-mesh framework provides a natural foundation for tracking propagating "
    "solitons over longer evolution times.",
]

abstract_html = '<section id="abstract"><h2>Abstract</h2>\n' + para(ABSTRACT) + '\n</section>'
intro_html = ('<section id="section-1"><h2>1. Introduction</h2>\n' +
              '\n'.join(para(p) for p in INTRO) + '\n</section>')
concl_html = ('<section id="section-6"><h2>6. Conclusions</h2>\n' +
              '\n'.join(para(p) for p in CONCL) + '\n</section>')
s52_html = '\n'.join(para(p) for p in S52) + '\n'


def replace_block(text, pattern, new):
    hits = list(re.finditer(pattern, text, re.S))
    assert len(hits) == 1, (pattern, len(hits))
    return text[:hits[0].start()] + new + text[hits[0].end():]


source = BASELINE.read_text(encoding='utf-8')
out = source
out = replace_block(out, r'<section id="abstract">.*?</section>', abstract_html)
out = replace_block(out, r'<section id="section-1">.*?</section>', intro_html)
out = replace_block(out, r'<section id="section-6">.*?</section>', concl_html)

# Section 5.2: replace the two closing paragraphs
start = out.index('<section class="numerical-section" id="section-5.2">')
end = out.index('</section>', start)
seg = out[start:end]
k = seg.index('<p>Taken together')
tail = seg.rindex('</p>') + len('</p>')
seg_new = seg[:k] + s52_html.rstrip('\n') + seg[tail:]
out = out[:start] + seg_new + out[end:]

out = render(out)
assert 'BAMATH' not in out
PAPER.write_text(out, encoding='utf-8')

manifest = dict(
    before=dict(path=str(BASELINE.relative_to(ROOT)),
                sha256=hashlib.sha256(BASELINE.read_bytes()).hexdigest()),
    after=dict(path='dlw-paper.html', sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest()),
    replaced=['section#abstract', 'section#section-1', 'section#section-5.2 (last two paragraphs)',
              'section#section-6'],
    paragraphs=dict(abstract=1, introduction=len(INTRO), section52=len(S52), conclusions=len(CONCL)),
    citations={'added': '[1–4] in Introduction paragraph 1', 'Sheng–Yu': '[5]',
               'Miwa expansion': '[15]'},
    formulas=len(maths),
)
(HERE / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2))
