"""Replace Abstract, Introduction and Conclusions with the new supplied text."""
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
    token = 'FMTEXT' + str(len(maths)) + 'END'
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
        text = text.replace('FMTEXT' + str(i) + 'END', result)
    return text


def para(text):
    """Convert $..$ segments to KaTeX and wrap the result in a paragraph."""
    parts = text.split('$')
    assert len(parts) % 2 == 1, 'unbalanced dollar signs'
    out = []
    for i, part in enumerate(parts):
        if i % 2:
            out.append(m(part))
        else:
            out.append(part.replace('&', '&amp;').replace('—', '&mdash;'))
    return '<p>' + ''.join(out) + '</p>'


# ---------------------------------------------------------------------- abstract
ABSTRACT = (
    "We study the integrable semi-discretization and numerical approximation of the $(2+1)$-dimensional "
    "dispersive long-wave (DLW) system, with the aim of understanding how structural choices at the bilinear "
    "$\\tau$-function level govern the accuracy and dynamics of the reconstructed physical wave fields. Starting "
    "from the Hirota–Miwa equation and a two-time Miwa expansion, we retain a discrete transverse lattice in $y$ "
    "while keeping $x$ and $t$ continuous. Within this common bilinear construction, we examine two semi-discrete "
    "formulations: an endpoint-based lattice (Endpoint-SD) that arises directly from the unshifted Miwa reduction, "
    "and a symmetric staggered lattice (Centered-SD) obtained by a half-step shift of the bilinear parameter "
    "reference and a staggered placement of the $\\tau$ functions. For both formulations, we construct explicit "
    "$N$-soliton Gram determinant solutions, establish sufficient conditions for $\\tau$-function positivity and "
    "smooth field regularity, and derive compatible Darboux–Lax representations together with closed nonlinear "
    "evolution equations for the physical fields. Continuum consistency analysis shows that while both schemes "
    "approximate the first DLW equation to second order, the one-sided pairing of Endpoint-SD introduces a leading "
    "$O(h)$ truncation defect in the second equation, whereas Centered-SD restores full second-order consistency in "
    "both fields and admits an intrinsic semi-discrete conservation law through its auxiliary logarithmic "
    "derivative. Numerical experiments across one-soliton, two-soliton, Gaussian, and sinusoidal regimes connect "
    "these analytical properties to computation. We show that the $O(h)$ defect in Endpoint-SD not only degrades "
    "the second field $v$, but also feeds back into the first field $u$ through dispersive coupling during "
    "nonlinear soliton evolution, allowing Centered-SD to outperform Endpoint-SD in both components. Furthermore, "
    "full-time error histories under forward Euler, RK4, and Crank–Nicolson integration separate the spatially "
    "governed rate of error accumulation from temporal level shifts, demonstrating how opposite-sign truncation "
    "defects in the staggered reconstruction can produce fortuitous error cancellation at a fixed terminal time. "
    "Finally, coupling Centered-SD to a shared-node moving mesh driven by its native conservation density "
    "systematically reduces wave-band errors in both physical components."
)

# ------------------------------------------------------------------ introduction
INTRO = [
    "The $(2+1)$-dimensional dispersive long-wave (DLW) system describes the evolution of shallow-water waves in "
    "two horizontal spatial dimensions under weak dispersion and nonlinearity. In addition to its physical "
    "relevance in fluid mechanics, the continuous DLW system is a prototypical higher-dimensional integrable "
    "model: it admits a Hirota bilinear representation, multi-soliton and breather solutions expressible in terms "
    "of Gram determinants, and compatible linear Lax problems [1–4]. In particular, Sheng and Yu [5] established "
    "a systematic bilinear framework and continuous Gram determinant family for the DLW equations, providing a "
    "transparent link between pairs of positive $\\tau$ functions and smooth physical wave fields.",

    "When transitioning from continuous integrable theory to numerical computation, structure-preserving or "
    "integrable discretizations offer a compelling bridge [7,8]. By deriving discrete lattice equations from "
    "fundamental bilinear identities—most notably the Hirota–Miwa equation via Miwa's continuous-time expansion "
    "[15]—one can preserve exact solvability, determinant solution structures, and Darboux–Lax compatibility on a "
    "discrete grid. The same programme has been carried out for other integrable semi-discrete systems [6–9] and "
    "for discrete DLW-type reductions [11]; the moving meshes used in such computations follow the self-adaptive "
    "constructions built on semi-discrete conservation laws [9,12,13] and the general theory of equidistribution "
    "[14], while the one-step integrators of Section 4 are classical [10]. Yet an important and often "
    "underappreciated question lies between the bilinear lattice and "
    "practical scientific computing: how do structural arrangements at the $\\tau$-function level translate into "
    "approximation accuracy for the actual physical fields? In a bilinear semi-discretization, two lattices may be "
    "algebraically equivalent up to a parameter shift at fixed grid spacing and may share the exact same "
    "determinant machinery, while inducing markedly different truncation errors once logarithmic derivatives and "
    "lattice differences are taken to reconstruct the physical variables. Understanding this interplay—between "
    "bilinear lattice geometry, nonlinear field reconstruction, temporal integration, and spatial mesh "
    "distribution—is the central motivation of the present work.",

    "In this paper, we address this question by developing and comparing two integrable transverse "
    "semi-discretizations of the $(2+1)$-dimensional DLW system, keeping the longitudinal coordinate $x$ and time "
    "$t$ continuous while discretizing the transverse coordinate $y$ with spacing $h$. Starting from an unreduced "
    "two-direction retention of the Hirota–Miwa equation, the Miwa expansion leads directly to what we term the "
    "endpoint-based semi-discretization (Endpoint-SD). Examining its local approximation to the continuous "
    "bilinear system reveals a first-order $O(h)$ correction tied to the one-sided placement of the "
    "$\\tau$-function pairings relative to the continuous reference parameter. To eliminate this one-sided bias "
    "without leaving the Hirota–Miwa family, we introduce a half-step shift in the bilinear operator parameter "
    "together with a staggered interpretation of the $\\tau$ functions, arriving at the centered semi-discretization "
    "(Centered-SD). Both formulations are shown to admit explicit Gram determinant solutions, for which we identify "
    "a concrete real parameter regime guaranteeing strict positivity of the determinants and smoothness of the "
    "reconstructed physical fields.",

    "Passing from the bilinear equations to the physical variables $(u, v)$ exposes the analytical and "
    "computational consequences of these two lattice arrangements. For Endpoint-SD, the logarithmic field "
    "transformation yields a closed two-component nonlinear system directly, but the one-sided bilinear pairing "
    "leaves an explicit $O(h)$ drift-flux defect in the evolution equation for $v$. For Centered-SD, the symmetric "
    "staggered pairings lead naturally to a nonlinear formulation coupling the nodal field $u_k$ with an auxiliary "
    "logarithmic-difference variable $\\omega_k$, from which the edge-midpoint field $v_k$ is recovered via a "
    "two-point recurrence. We prove that both nonlinear systems possess compatible Darboux–Lax representations "
    "sharing a common operator form, and that Centered-SD achieves full $O(h^2)$ consistency in both physical "
    "equations as well as in its matched exact Gram wave fields. Moreover, the auxiliary $\\omega_k$ equation in "
    "Centered-SD takes the form of an exact semi-discrete conservation law. We exploit this structural feature to "
    "design a shared-node conservation-based moving mesh in $x$, which dynamically concentrates longitudinal "
    "resolution across active wave bands while preserving the transverse lattice pairings.",

    "We then conduct a sequence of controlled numerical experiments across four test problems—one-soliton "
    "propagation, two-soliton interaction, localized Gaussian data, and periodic sinusoidal data—to see how these "
    "theoretical properties manifest in practice. Comparing Endpoint-SD, Centered-SD, and a standard collocated "
    "finite-difference (FD) baseline under fourth-order Runge–Kutta (RK4) integration confirms that while "
    "Endpoint-SD has a slightly smaller initial $u_t$ residual at $t=0$, its $O(h)$ defect in $v$ feeds back into "
    "$u$ through dispersive coupling during soliton evolution, allowing Centered-SD to achieve substantially "
    "smaller errors in both fields. Extending the investigation to time integration and mesh adaptation yields "
    "further insight into the numerical behavior of the coupled system. By tracking full-time error histories for "
    "forward Euler, RK4, and Crank–Nicolson, we show how a single terminal-time comparison can be misled by "
    "opposite-sign error cancellation between temporal and spatial truncation defects. Finally, we evaluate the "
    "conservation-based adaptive mesh on the soliton tests, demonstrating how equidistributing the native "
    "auxiliary density suppresses errors along the entire wave band and clarifying the respective roles of initial "
    "static equidistribution and dynamic node motion over short integration horizons.",

    "The remainder of the paper is organized as follows. Section 2 recalls the continuous DLW bilinear system, "
    "derives the Endpoint-SD and Centered-SD bilinear lattices from the Hirota–Miwa equation, and establishes their "
    "Gram determinant solutions and positivity conditions. In Section 3, we reconstruct the nonlinear "
    "physical-field equations for both formulations, prove their Darboux–Lax compatibility, and analyze their "
    "continuum consistency and exact-solution convergence. Section 4 describes the numerical implementation, "
    "including Fourier spectral and mapped finite-difference spatial operators, boundary closures, time "
    "integrators, and the conservation-based moving-mesh formulation. Section 5 presents the numerical experiments "
    "comparing the spatial formulations, time integrators, and fixed versus adaptive meshes. Section 6 summarizes "
    "our main conclusions and the insights gained into the semi-discrete DLW system.",
]

# ------------------------------------------------------------------- conclusions
CONCL = [
    "In this work, we have developed an integrable semi-discrete framework for the $(2+1)$-dimensional dispersive "
    "long-wave system and used it to investigate how bilinear lattice structure, physical-field reconstruction, "
    "time integration, and mesh adaptation interact in numerical computation. By deriving both Endpoint-SD and "
    "Centered-SD from the same Hirota–Miwa bilinear reduction, we obtained two integrable semi-discretizations "
    "that share explicit positive Gram determinant solutions and a common Darboux–Lax operator structure, yet "
    "differ fundamentally in how they approximate the continuous physical wave fields.",

    "Our analytical and numerical comparisons provide several insights into the behavior of the system. First, at "
    "the spatial level, the transition from the one-sided Endpoint-SD arrangement to the symmetric staggered "
    "Centered-SD formulation is decisive for balanced multi-component accuracy. While Endpoint-SD inherits exact "
    "integrability and exhibits a small initial derivative defect in $u_t$, its one-sided pairing leaves an $O(h)$ "
    "truncation error in the second equation. Our experiments demonstrate that in strongly nonlinear soliton "
    "regimes, this first-order defect does not remain confined to $v$: because the evolution of $u$ is driven by "
    "the dispersive curvature term $v_{xx}$, the large error in $v$ contaminates $u$ over time. By restoring "
    "second-order bilinear symmetry, Centered-SD eliminates this $O(h)$ source, improves the accuracy of $v$ by "
    "nearly two orders of magnitude over Endpoint-SD (and by factors of $1.7$ to $3.5$ over a collocated "
    "finite-difference baseline), and reverses the initial error ordering to outperform Endpoint-SD in $u$ as well.",

    "Second, our examination of temporal integration highlights the importance of inspecting full time histories "
    "rather than relying solely on terminal error norms in coupled multi-field systems. Tracking the maximum errors "
    "across every step reveals that the secular rate of error accumulation is fixed by the spatial "
    "discretization—remaining nearly constant during smooth propagation and steepening only when colliding soliton "
    "branches form grid-scale gradients—whereas the time integrator sets the vertical level of the error "
    "trajectory. Because Centered-SD recovers $v$ from $u$ and the auxiliary variable $\\omega$ through a "
    "differentiated staggered relation, a first-order temporal defect in forward Euler enters the two physical "
    "fields with opposite algebraic signs, partially canceling the spatial error in $u$ while amplifying it in "
    "$v$. Step-size refinement and full-time diagnostics cleanly separate this cancellation artifact from genuine "
    "numerical resolution.",

    "Third, the natural nonlinear formulation of Centered-SD reveals an intrinsic semi-discrete conservation law "
    "governed by the auxiliary variable $\\omega_k$, which provides a physically meaningful monitor density for mesh "
    "redistribution without introducing ad hoc gradient parameters. Because the truncation error on a uniform grid "
    "is localized along the soliton wave bands where $\\omega_k$ is active, equidistributing the transverse-averaged "
    "conservation density automatically concentrates shared $x$ nodes into the error-producing core and reduces "
    "the error across the entire wave band in both components, with a particularly strong relative gain in $v$. At "
    "the same time, our frozen-mesh control experiments clarify the operational scope of this strategy over short "
    "time horizons: when the wave translates by less than a grid spacing, the observed improvement comes primarily "
    "from the initial static adaptation of the grid to the conservation density.",

    "Several natural extensions follow from these findings. On the analytical side, the linearized evolution of the "
    "semi-discrete equations under the numerical boundary closures, together with robustness tests under non-exact "
    "or perturbed initial data, will further clarify the long-time stability properties of the staggered "
    "formulation. On the computational side, extending the conservation-based moving mesh to longer integration "
    "horizons—where propagating and interacting solitons travel across many grid cells—will provide a direct test "
    "of dynamic node tracking and long-time phase preservation.",
]

abstract_html = '<section id="abstract"><h2>Abstract</h2>\n' + para(ABSTRACT) + '\n</section>'
intro_html = ('<section id="section-1"><h2>1. Introduction</h2>\n' +
              '\n'.join(para(p) for p in INTRO) + '\n</section>')
concl_html = ('<section id="section-6"><h2>6. Conclusions</h2>\n' +
              '\n'.join(para(p) for p in CONCL) + '\n</section>')


def replace_block(text, pattern, new):
    hits = list(re.finditer(pattern, text, re.S))
    assert len(hits) == 1, (pattern, len(hits))
    return text[:hits[0].start()] + new + text[hits[0].end():]


source = BASELINE.read_text(encoding='utf-8')
out = source
out = replace_block(out, r'<section id="abstract">.*?</section>', abstract_html)
out = replace_block(out, r'<section id="section-1">.*?</section>', intro_html)
out = replace_block(out, r'<section id="section-6">.*?</section>', concl_html)

out = render(out)
assert 'FMTEXT' not in out
PAPER.write_text(out, encoding='utf-8')

manifest = dict(
    before=dict(path=str(BASELINE.relative_to(ROOT)),
                sha256=hashlib.sha256(BASELINE.read_bytes()).hexdigest()),
    after=dict(path='dlw-paper.html', sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest()),
    replaced=['section#abstract', 'section#section-1', 'section#section-6'],
    paragraphs=dict(abstract=1, introduction=len(INTRO), conclusions=len(CONCL)),
    citations_remapped={'[1] Sheng and Yu': '[5]', '[2] Miwa expansion': '[15]'},
    added_citations=['[1–4]', '[6–9]', '[11]', '[9,12,13]', '[14]', '[10]'],
    formulas=len(maths),
)
(HERE / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2))
