"""Focus the manuscript on Sections 6.1/6.2; retain certification research separately."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re
import subprocess
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAPER = ROOT / 'dlw-paper.html'
before = PAPER.read_bytes()
src = before.decode('utf-8')
start = src.index('<section id="section-6"')
end = src.index('<section id="section-7">', start)
old = src[start:end]
assert '<section id="section-6.3">' in old
stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup = HERE / ('before_response_focus_' + stamp)
backup.mkdir()
(backup / 'dlw-paper.html').write_bytes(before)
(backup / 'section6.html').write_text(old, encoding='utf-8')
old63 = re.search(r'<section id="section-6\.3">.*?</section>', old, re.S)[0]
(backup / 'section63.html').write_text(old63, encoding='utf-8')
new = old.replace(old63, '')
new = new.replace('6. Perturbation dynamics and reference accuracy', '6. Response to initial perturbations')
new, count = re.subn(r'<p>We now examine.*?</p>',
    '<p>We examine how small, independent changes in the initial physical fields affect the computed evolution. '
    'The response depends on the coupling between the two fields and on the spatial operators used to advance them. '
    'Section 6.1 derives the constant-background response of Centered-SD, including the transverse integration fixed by the lower boundary. '
    'In Section 6.2, we perturb each field separately on the four wave backgrounds and use this analysis to interpret the resulting responses.</p>',
    new, count=1, flags=re.S)
assert count == 1
new = new.replace(' Section 6.3 considers the continuous reference problem for the same independent initial data.', '')

maths = []
def paragraph(text):
    pieces = text.split('$')
    assert len(pieces) % 2 == 1
    for i in range(1, len(pieces), 2):
        maths.append(pieces[i])
        pieces[i] = f'RESPONSEMATH{len(maths)-1}END'
    return '<p>' + ''.join(pieces) + '</p>'

analysis = paragraph(
    r'The initially perturbed field remains close to its initial magnitude over $0\le t\le0.01$, while coupling produces a response in the other field. '
    r'The largest transfer occurs when $v_0$ is perturbed in the two-soliton case, where $\|\delta u_h(T)\|_\infty/\varepsilon=0.97382$. '
    r'The transverse primitive in Section 6.1 helps explain this response. On the actual grids and observation regions, the constant-background formula gives $0.22248$ and $0.97158$ for the one- and two-soliton cases, compared with the measured values $0.22453$ and $0.97382$. '
    r'The close agreement shows that the longer transverse interval accounts for most of the difference between these two responses.')
analysis += '\n' + paragraph(
    r'The reverse transfer is more sensitive to the background. An initial $u$ perturbation generates normalized $v$ responses of $0.09186$ and $0.10278$ in the soliton cases, compared with constant-background values of $0.00389$ and $0.00097$. '
    r'The Gaussian and sinusoidal backgrounds give nearly identical responses, with pair gains of approximately $1.00055$ for $u_0$ input and $1.00147$ for $v_0$ input. '
    r'Their native-node maxima also reflect the translation of the wave peaks across the grid. Evaluating the saved Fourier interpolants on eight times as many $x$ points gives same-field peak ratios of $1.00036$&ndash;$1.00038$ relative to their initial peaks, explaining the slightly subunit values at the original nodes. '
    r'Together, the maximum responses and pair gains describe both the transfer between the fields and the change in the overall perturbation size.')
new, count = re.subn(r'<p>The initially perturbed component.*?</p>\s*<p>For the Gaussian and sinusoidal backgrounds.*?</p>',
                     lambda _: analysis, new, count=1, flags=re.S)
assert count == 1
js = "const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(t=>k.renderToString(t,{displayMode:false,throwOnError:true,strict:'error'}))));"
out = subprocess.run(['node', '-e', js, str(ROOT / 'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],
                     input=json.dumps(maths), text=True, encoding='utf-8', capture_output=True, check=True)
rendered = json.loads(out.stdout)
new = re.sub(r'RESPONSEMATH(\d+)END', lambda m: rendered[int(m[1])], new)
prefix = src[:start]
old_nav = '<a href="#section-6">6. Perturbation dynamics and reference accuracy</a>'
new_nav = '<a href="#section-6">6. Response to initial perturbations</a>'
nav63 = '<a class="subsection" href="#section-6.3">6.3 Continuous reference solutions and error certification</a>'
assert prefix.count(old_nav) == prefix.count(nav63) == 1
prefix = prefix.replace(old_nav, new_nav).replace(nav63, '')
updated = prefix + new + src[end:]
assert prefix.replace(new_nav, old_nav).replace('<a href="#section-7">', nav63 + '<a href="#section-7">') == src[:start]
assert updated[updated.index('<section id="section-7">'):] == src[end:]
assert re.search(r'<section id="section-6\.1">.*?</section>', old, re.S)[0] == re.search(r'<section id="section-6\.1">.*?</section>', new, re.S)[0]
for tag in ['figure', 'table']:
    assert re.findall(fr'<{tag}\b.*?</{tag}>', old, re.S) == re.findall(fr'<{tag}\b.*?</{tag}>', new, re.S)
soup = BeautifulSoup(updated, 'html.parser')
assert not soup.select('.katex-error')
assert soup.find(id='section-6.3') is None
assert len(soup.select('figure')) == 29 and len(soup.select('table')) == 7
assert 'Section 6.3' not in new
assert PAPER.read_bytes() == before, 'Main paper changed concurrently; review before retrying.'
PAPER.write_bytes(updated.encode('utf-8'))
(HERE / 'section6.html').write_text(new, encoding='utf-8')

report = ROOT / 'report/dlw_reference_certification_20261026.html'
report_before = report.read_bytes()
(backup / report.name).write_bytes(report_before)
report_text = report_before.decode('utf-8')
report_text = report_text.replace('../dlw-paper.html#section-6.3', '../dlw-paper.html#section-6')
report_text = report_text.replace('主论文 §6.3', '主论文：扰动响应')
report.write_bytes(report_text.encode('utf-8'))

status = dict(date='2026-10-26', user_scope='Focus on perturbation response in Sections 6.1/6.2; continuous certification deferred',
              title='6. Response to initial perturbations', retained_subsections=['6.1', '6.2'],
              unchanged=['Sections 1–5', 'Section 6.1 mathematical content', 'Section 7 conclusion body', 'all figures and tables'],
              figures=29, tables=7, katex_errors=0, certified=False, eta_u=None, eta_v=None,
              before_sha256=hashlib.sha256(before).hexdigest(), after_sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest(),
              backup=str(backup), certification_report=str(report))
(HERE / 'response_focus_validation.json').write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(status, ensure_ascii=False, indent=2))
