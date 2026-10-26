"""Expand the concluding paragraph of Section 5.2 into two summary paragraphs.

The replacement text is the version supplied by the user. Mathematics is rendered with the
local KaTeX build; every other byte of the manuscript is preserved.
"""
from pathlib import Path
import hashlib, json, re, subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAPER = ROOT / 'dlw-paper.html'
BASELINE = HERE / 'before' / 'summary_expansion' / 'dlw-paper.html'

maths = []


def m(tex):
    token = 'S52MATHS' + str(len(maths)) + 'END'
    maths.append(dict(tex=tex, display=False))
    return token


def render(text):
    js = ("const fs=require('fs'),k=require(process.argv[1]);"
          "process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8'))"
          ".map(f=>k.renderToString(f.tex,{displayMode:f.display,throwOnError:true,strict:'error'}))));")
    katex = ROOT / 'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js'
    r = subprocess.run(['node', '-e', js, str(katex)], input=json.dumps(maths), text=True,
                       encoding='utf-8', capture_output=True, check=True)
    for i, result in enumerate(json.loads(r.stdout)):
        text = text.replace('S52MATHS' + str(i) + 'END', result)
    return text


old = ('<p>Overall, the spatial comparisons show that moving from the one-sided Endpoint-SD lattice to the '
       'symmetric staggered Centered-SD formulation substantially improves the approximation of the second field '
       'across all four regimes, and in the nonlinear soliton tests this improvement carries over to the first '
       'field as well. We therefore retain Centered-SD in the next two subsections to examine the effects of time '
       'integration and mesh redistribution.</p>')

new = (
    f'<p>Taken together, the initial diagnostics in Table 2 and the evolved errors in Table 3 illustrate how the '
    f'lattice geometry shapes the numerical approximation of the coupled DLW fields. Although Endpoint-SD and '
    f'Centered-SD originate from the same Hirota&ndash;Miwa bilinear reduction and share the same Lax integrability, '
    f'their physical-field reconstructions behave quite differently in computation. At {m("t=0")}, Endpoint-SD shows '
    f'a smaller residual in the first equation because it avoids the {m(r"O(h^2)")} auxiliary flux term, whereas its '
    f'one-sided pairing leaves an {m(r"O(h)")} truncation defect in the second equation. Following the evolution to '
    f'{m("T=0.01")} shows that this initial advantage in {m("u_t")} is fragile: in the small-amplitude Gaussian and '
    f'sinusoidal regimes, the mild gradients allow the initial ordering of {m("u")} to persist over short times, but '
    f'in the steeper one- and two-soliton regimes, the first-order defect in {m("v")} feeds back into {m("u")} '
    f'through the dispersive coupling term {m("v_{xx}")}, causing Endpoint-SD to lose accuracy in both components.</p>'
    f'\n'
    f'<p>By placing the {m(r"\tau")} functions and bilinear parameters symmetrically, Centered-SD restores '
    f'second-order consistency to both equations and prevents this cross-component degradation. Across all four '
    f'test problems&mdash;spanning single and interacting solitons as well as localized and periodic dispersive '
    f'waves&mdash;Centered-SD consistently delivers the most accurate approximation of the second field {m("v")}, '
    f'improving upon Endpoint-SD by factors of {m("60")} to {m("87")} and upon the collocated FD baseline by factors '
    f'of {m("1.7")} to {m("3.5")}, while maintaining a competitive second-order approximation in {m("u")}. These '
    f'results confirm that preserving the symmetric staggered structure of the bilinear system translates directly '
    f'into a more balanced and reliable physical-field solver. With the spatial behavior of the three formulations '
    f'established, we retain Centered-SD in Sections 5.3 and 5.4 to examine how time integration and adaptive node '
    f'redistribution affect the computed waves.</p>'
)

current = PAPER.read_text(encoding='utf-8')
assert current.count(old) == 1, 'summary paragraph not found exactly once'
paper = current.replace(old, new, 1)
paper = render(paper)
assert 'S52MATHS' not in paper and 'katex-error' not in paper
assert paper.count('<p>') == current.count('<p>') + 1, 'paragraph count'

# The quoted factor ranges must match Table 3.
import itertools
from bs4 import BeautifulSoup
soup = BeautifulSoup(paper, 'html.parser')
rows = {r.find('th').get_text(strip=True): [float(c['data-value']) for c in r.find_all('td')]
        for r in soup.find('table', id='table-final').find('tbody').find_all('tr')}
assert set(rows) == {'One-soliton', 'Two-soliton', 'Gaussian', 'Sinusoidal'}
ep_to_ce = [rows[k][1] / rows[k][3] for k in rows]
fd_to_ce = [rows[k][5] / rows[k][3] for k in rows]
assert all(rows[k][3] == min(rows[k][1], rows[k][3], rows[k][5]) for k in rows), 'Centered-SD must give the smallest v'
# The text quotes the rounded range: 60 to 87 (Endpoint) and 1.7 to 3.5 (FD).
assert 59.5 <= min(ep_to_ce) and max(ep_to_ce) <= 87.5, ep_to_ce
assert 1.65 <= min(fd_to_ce) and max(fd_to_ce) <= 3.55, fd_to_ce
assert paper.count('<figure') == 28 and paper.count('<table id=') == 5

BASELINE.parent.mkdir(parents=True, exist_ok=True)
BASELINE.write_text(current, encoding='utf-8')
PAPER.write_text(paper, encoding='utf-8')

manifest = dict(before_sha256=hashlib.sha256(current.encode('utf-8')).hexdigest(),
                after_sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest(),
                replaced='section-5.2 concluding paragraph',
                formulas=len(maths),
                endpoint_to_centered_v=[round(x, 2) for x in ep_to_ce],
                fd_to_centered_v=[round(x, 2) for x in fd_to_ce])
(HERE / 'manifest_summary_expansion.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2))
