"""Plain-description revision: Abstract, Introduction paragraphs 3-5, 5.2 tail, Conclusions."""
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
    token = 'PLMATH' + str(len(maths)) + 'END'
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
        text = text.replace('PLMATH' + str(i) + 'END', result)
    return text


def para(text):
    parts = text.split('$')
    assert len(parts) % 2 == 1, 'unbalanced dollars'
    out = []
    for i, part in enumerate(parts):
        out.append(m(part) if i % 2 else part.replace('&', '&amp;').replace('—', '&mdash;'))
    return '<p>' + ''.join(out) + '</p>'


ABSTRACT = (
    "The $(2+1)$-dimensional dispersive long-wave (DLW) system is a fundamental integrable model for nonlinear "
    "shallow-water waves in two horizontal dimensions, for which preserving the underlying integrable structure "
    "under discretization is of both theoretical and computational interest. In this paper, we study the integrable "
    "semi-discretization and numerical approximation of the DLW system, with the goal of understanding how lattice "
    "arrangements at the bilinear $\\tau$-function level shape the reconstructed physical wave fields and their "
    "numerical evolution. Starting from the Hirota–Miwa equation and a two-time Miwa expansion, we discretize the "
    "transverse coordinate $y$ while keeping $x$ and $t$ continuous, deriving an endpoint-based semi-discretization "
    "(Endpoint-SD) and, through a half-step shift of the bilinear parameter and a staggered $\\tau$-function "
    "placement, a centered semi-discretization (Centered-SD). Both formulations admit explicit positive Gram "
    "determinant solutions, compatible Darboux–Lax representations, and closed nonlinear physical-field equations, "
    "with first- and second-order bilinear consistency, respectively. Numerical experiments across one-soliton, "
    "two-soliton, Gaussian, and sinusoidal initial data examine the resulting physical fields. At the spatial "
    "level, Endpoint-SD gives the smallest initial $u_t$ defects and the smallest $u$ errors in the Gaussian and "
    "sinusoidal tests, whereas Centered-SD gives the smallest $v$ errors across all four tests and achieves "
    "smaller errors in both $u$ and $v$ in the one- and two-soliton regimes. Following the full time histories "
    "under forward Euler, RK4, and Crank–Nicolson integration separates the spatially governed rate of error "
    "growth from the level shifts introduced by the time integrator. Finally, using the semi-discrete conservation "
    "law of the Centered-SD system to equidistribute a shared set of moving $x$ nodes lowers the wave-band errors "
    "in both physical components. Together, these results show how bilinear lattice symmetry and semi-discrete "
    "conservation laws translate directly into improved physical-field accuracy in the numerical computation of "
    "higher-dimensional integrable waves."
)

INTRO_345 = [
    "In this paper, we address this question by developing two integrable transverse semi-discretizations of the "
    "$(2+1)$-dimensional DLW system, discretizing $y$ with lattice spacing $h$ while keeping $x$ and $t$ "
    "continuous. Retaining two lattice directions in the Hirota–Miwa equation and applying a Miwa expansion leads "
    "directly to the endpoint-based semi-discretization (Endpoint-SD). Examining its local approximation to the "
    "continuous bilinear system draws attention to the first-order term associated with the one-sided placement of "
    "the pairings, which motivates a symmetric placement through a half-step shift of the parameter reference and a "
    "staggered interpretation of the $\\tau$ functions, giving the centered semi-discretization (Centered-SD). Both "
    "formulations arise within the same bilinear construction, admit explicit Gram determinant solutions with a "
    "common positivity regime, and share a common Darboux–Lax operator form.",

    "Reconstructing the nonlinear physical fields $(u, v)$ shows how each lattice arrangement enters the field "
    "equations. Endpoint-SD expresses the dynamics directly in terms of the two physical fields, yielding a "
    "second-order approximation in the first equation and a first-order term in the second. Centered-SD pairs the "
    "nodal field $u_k$ with an auxiliary logarithmic difference $\\omega_k$ and recovers the midpoint field $v_k$ "
    "through a two-point recurrence, achieving second-order consistency in both equations as well as $O(h^2)$ "
    "convergence of the exact Gram wave fields. In addition, the $\\omega_k$ equation in Centered-SD forms a "
    "semi-discrete conservation law, which we use to construct a shared-node moving mesh in $x$ that "
    "redistributes longitudinal resolution while keeping the transverse lattice intact.",

    "We then use one-soliton, two-soliton, Gaussian, and sinusoidal initial data to examine the computed physical "
    "fields. Under common RK4 time integration, Endpoint-SD gives the smallest initial $u_t$ defects at $t = 0$ "
    "and the smallest terminal $u$ errors in the Gaussian and sinusoidal cases, whereas Centered-SD gives the "
    "smallest $v$ errors in all four cases and produces smaller errors in both $u$ and $v$ in the one- and "
    "two-soliton tests. Retaining Centered-SD on the fixed grid, we compare forward Euler, RK4, and "
    "Crank–Nicolson by recording the maximum error at every time step, showing how the error growth rate and the "
    "integrator-dependent level shift develop over time. Finally, we compare uniform and conservation-adapted "
    "meshes on the soliton tests and examine how node redistribution modifies the error profiles along the wave "
    "bands.",
]

S52 = [
    "Taken together, Table 2 and Table 3 show how the initial derivative defects and the evolved field errors "
    "relate across the four test problems. At $t = 0$, Endpoint-SD gives the smallest $u_t$ error in every case "
    "because its first equation does not include the $O(h^2)$ auxiliary flux term, whereas Centered-SD gives the "
    "smallest $v_t$ error due to its symmetric pairing. At $T = 0.01$, this initial ordering of $u$ is preserved in "
    "the small-amplitude Gaussian and sinusoidal tests, where the field gradients remain mild. In the one- and "
    "two-soliton tests, however, Centered-SD produces smaller terminal errors than Endpoint-SD in both $u$ and "
    "$v$, as the approximation of the second field enters the evolution of the first through the dispersive term "
    "$v_{xx}$.",

    "Across all four test regimes, Centered-SD consistently gives the smallest error in the second field $v$ among "
    "the three spatial formulations, improving upon both Endpoint-SD and the collocated FD baseline while "
    "maintaining second-order accuracy in $u$. These comparisons connect the placement of the bilinear pairings "
    "directly to the observed accuracy of the reconstructed waves. In Sections 5.3 and 5.4, we retain Centered-SD "
    "to examine how time integration and mesh redistribution affect the computed fields.",
]

CONCL = [
    "In this work, we have studied the integrable semi-discretization and numerical approximation of the "
    "$(2+1)$-dimensional dispersive long-wave system, tracing how the bilinear lattice construction enters the "
    "nonlinear field equations and their numerical evolution. Deriving Endpoint-SD and Centered-SD from the "
    "Hirota–Miwa equation allowed us to place both formulations within a common bilinear framework, with shared "
    "Gram determinant structures and compatible Darboux–Lax representations, and to examine how their different "
    "lattice pairings affect the reconstructed physical fields.",

    "The analytical and numerical results clarify three main aspects of the semi-discrete system. First, the "
    "spatial comparisons show how the arrangement of the $\\tau$ functions governs the behavior of the two "
    "physical components. Endpoint-SD yields a direct two-component system that gives the smallest initial $u_t$ "
    "defects and the smallest terminal $u$ errors in the smooth Gaussian and sinusoidal tests. Centered-SD, "
    "through its symmetric staggered arrangement, achieves second-order consistency in both equations, produces "
    "the smallest $v$ errors across all four test problems, and yields smaller errors in both $u$ and $v$ during "
    "one- and two-soliton evolution. Second, following the full time histories under forward Euler, RK4, and "
    "Crank–Nicolson separates the steady, spatially determined rate of error growth from the vertical level shift "
    "set by the time integrator, showing how a first-order temporal defect enters the two reconstructed fields "
    "with opposite signs. Third, using the intrinsic semi-discrete conservation law of Centered-SD to "
    "equidistribute the shared $x$ nodes concentrates grid resolution along the soliton wave bands and consistently "
    "reduces the errors in both physical fields without increasing the node count.",

    "Viewed in a broader context, this study illustrates that the value of an integrable discretization extends "
    "well beyond the formal preservation of exact determinant solutions or Lax pairs at the $\\tau$-function level. "
    "In higher-dimensional, multi-component wave systems, the internal geometry of the bilinear lattice and the way "
    "it is mapped to physical coordinates play a central role in determining cross-component accuracy during "
    "coupled nonlinear evolution. At the same time, structural features that emerge naturally from the integrable "
    "formulation—such as exact semi-discrete conservation laws—can be harnessed directly to guide numerical mesh "
    "adaptation. Bridging bilinear integrable structure with componentwise numerical diagnostics thus provides a "
    "coherent pathway for analyzing and improving structure-preserving solvers in higher-dimensional wave "
    "mechanics.",
]

abstract_html = '<section id="abstract"><h2>Abstract</h2>\n' + para(ABSTRACT) + '\n</section>'
concl_html = ('<section id="section-6"><h2>6. Conclusions</h2>\n' +
              '\n'.join(para(p) for p in CONCL) + '\n</section>')
s52_html = '\n'.join(para(p) for p in S52)

source = BASELINE.read_text(encoding='utf-8')
out = source

# abstract
hits = list(re.finditer(r'<section id="abstract">.*?</section>', out, re.S))
assert len(hits) == 1
out = out[:hits[0].start()] + abstract_html + out[hits[0].end():]

# introduction: replace paragraphs 3-5, keep 1, 2 and the roadmap
i = out.index('<section id="section-1">')
j = out.index('</section>', i)
seg = out[i:j]
paras, pos = [], 0
while True:
    k = seg.find('<p>', pos)
    if k < 0:
        break
    e = seg.find('</p>', k) + len('</p>')
    paras.append(seg[k:e])
    pos = e
assert len(paras) == 6, len(paras)
head = seg[:seg.find('<p>')]
new_seg = (head + paras[0] + '\n' + paras[1] + '\n' +
           '\n'.join(para(p) for p in INTRO_345) + '\n' + paras[5] + '\n')
out = out[:i] + new_seg + out[j:]

# 5.2 tail
start = out.index('<section class="numerical-section" id="section-5.2">')
end = out.index('</section>', start)
seg = out[start:end]
k = seg.index('<p>Taken together')
tail = seg.rindex('</p>') + len('</p>')
out = out[:start] + seg[:k] + s52_html + seg[tail:] + out[end:]

# conclusions
hits = list(re.finditer(r'<section id="section-6">.*?</section>', out, re.S))
assert len(hits) == 1
out = out[:hits[0].start()] + concl_html + out[hits[0].end():]

out = render(out)
assert 'PLMATH' not in out
PAPER.write_text(out, encoding='utf-8')

manifest = dict(
    before=dict(path=str(BASELINE.relative_to(ROOT)),
                sha256=hashlib.sha256(BASELINE.read_bytes()).hexdigest()),
    after=dict(path='dlw-paper.html', sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest()),
    replaced=['section#abstract', 'section#section-1 paragraphs 3-5',
              'section#section-5.2 last two paragraphs', 'section#section-6'],
    kept=['section-1 paragraph 1', 'section-1 paragraph 2 (refs 6-14)', 'section-1 paragraph 6 (roadmap)'],
    paragraphs=dict(abstract=1, introduction=6, section52=len(S52), conclusions=len(CONCL)),
    formulas=len(maths),
)
(HERE / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2))
