"""Publish the selected numerical text through bounded manuscript replacements."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib, json, re, subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAPER = ROOT / 'dlw-paper.html'
DRAFT = ROOT / 'report/dlw_numerical_text_20261025.html'
BASELINE = HERE / 'before_dlw-paper.html'
source = BASELINE.read_text(encoding='utf-8')
draft = BeautifulSoup(DRAFT.read_text(encoding='utf-8'), 'html.parser')

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

def import_section(identity):
    sec = BeautifulSoup(str(draft.find(id=identity)), 'html.parser').section
    sec['class'] = ['numerical-section']
    if identity.startswith('section-4.'):
        sec.find(re.compile('^h[23]$')).name = 'h3'
    for e in sec.select('[src], [href]'):
        for attr in ('src', 'href'):
            if e.get(attr, '').startswith('../'):
                e[attr] = e[attr][3:]
    return str(sec)

maths = []
def m(tex, display=False):
    token = 'INTEGRATIONMATH' + str(len(maths)) + 'END'
    maths.append(dict(tex=tex, display=display))
    return token

def eq(tex):
    return '<div class="equation">' + m(tex, True) + '</div>'

def render(text):
    js = "const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(f=>k.renderToString(f.tex,{displayMode:f.display,throwOnError:true,strict:'error'}))));"
    r = subprocess.run(['node', '-e', js, str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')], input=json.dumps(maths), text=True, encoding='utf-8', capture_output=True, check=True)
    for i, result in enumerate(json.loads(r.stdout)):
        text = text.replace('INTEGRATIONMATH' + str(i) + 'END', result)
    return text

replacements = {s: import_section(s) for s in ['section-4.1', 'section-5.1', 'section-5.2']}
replacements['section-4.1'] = replacements['section-4.1'].replace(
    '<p>Write ', '<p>Both semi-discrete formulations place '+m('u')+' at nodes and '+m('v')+' at edge midpoints; FD places both fields at nodes. Write ', 1)

replacements['section-4.2'] = f'''<section id="section-4.2" class="numerical-section"><h3>4.2 Initial and boundary data and time integration</h3>
<p>We specify the initial and boundary data, then describe how forward Euler, classical RK4 and Crank–Nicolson advance the physical fields in our numerical experiments. Each spatial formulation samples the same continuous reference fields at its native lattice locations. Endpoint-SD and FD advance the state {m(r'z=(u_k,v_k)_k')}; Centered-SD advances {m(r'z=(u_k,\omega_k)_k')} and recovers {m('v')} through the field relation in Section 4.1. At each time stage, the current state and the prescribed boundary data determine the derivatives required by the time integrator.</p>
<p>For Centered-SD, the initial lower auxiliary value is {m(r'\omega_0=h(v^*-u_y^*)/4')}, evaluated at the lower node. The remaining values follow from the linear reconstruction (34),</p>
{eq(r'\omega_k=\frac h2(v_k-\Delta_hu_k)-\omega_{k-1}.')}
<p>This recurrence reproduces the prescribed physical field {m('v')} on every internal edge. During evolution, the lower auxiliary value follows the same {m(r'\omega')} equation as the interior values. The lower value of {m('u_t')} is supplied by the continuous reference solution at every stage.</p>
<p>Endpoint-SD uses the prescribed lower derivative and the continuous lower ghost value of {m('u')} in its backward lattice relations. For FD, the lower data are supplied in the same way, while the upper ghost value extrapolates the departure from the continuous reference. Writing {m(r'e_k=u_k-u_k^*')}, this closure is {m(r'u_{N+1}=u_{N+1}^*+3e_N-3e_{N-1}+e_{N-2}')}. The reference values are evaluated at the current stage time. Fourier differentiation acts on a periodic {m('x')} interval extending beyond the principal wave profiles; the products are evaluated at the nodes without filtering, dealiasing or artificial viscosity.</p>
<p>Writing the resulting evolution equations as {m(r'\dot z=F(t,z)')}, forward Euler advances the state by {m(r'z^{n+1}=z^n+\Delta t F(t_n,z^n)')}. Classical RK4 uses four stage derivatives,</p>
{eq(r'\begin{aligned}K_1&=F(t_n,z^n),&K_2&=F(t_n+\Delta t/2,z^n+\Delta t K_1/2),\\K_3&=F(t_n+\Delta t/2,z^n+\Delta t K_2/2),&K_4&=F(t_n+\Delta t,z^n+\Delta t K_3),\\z^{n+1}&=z^n+\frac{\Delta t}{6}(K_1+2K_2+2K_3+K_4).\end{aligned}')}
<p>Crank–Nicolson determines the next state from</p>
{eq(r'z^{n+1}=z^n+\frac{\Delta t}{2}\bigl[F(t_n,z^n)+F(t_{n+1},z^{n+1})\bigr].')}
<p>The implicit step uses an Euler prediction followed by fixed-point iteration, with a stopping criterion of {m(r'10^{-12}')} for the maximum absolute equation residual. The spatial-formulation comparisons in Section 5.2 use RK4 with {m(r'\Delta t=10^{-4}')} and final time {m('T=0.01')}. In every comparison, errors are measured in the physical fields {m('u,v')}.</p></section>'''

# The former comparison belongs to a different field reconstruction. Archive it
# and retain the subsection's anchor for the next, separately requested study.
a, b = section_span(source, 'section-5.3')
archive = HERE / 'archived_full_potential_time_comparison.html'
if not archive.exists():
    archive.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Archived full-potential time comparison</title><link rel="stylesheet" href="../../gsg_project/dlw_report/_assets/package/dist/katex.min.css"><body>'+source[a:b]+'</body></html>', encoding='utf-8')
replacements['section-5.3'] = '<section id="section-5.3"><h3>5.3 Comparison of time integrators</h3><!-- Current natural Centered-SD: RK4 results appear in Section 5.2. Euler and Crank–Nicolson comparisons require current-form runs. The previous full-potential comparison is archived in manuscript_integration_20261025. --></section>'

intro = f'''<section id="section-5"><h2>5. Numerical experiments</h2><p>We use six wave problems to examine how the spatial formulation affects the accuracy of the physical fields. Four exact soliton solutions provide localized profiles and interacting waves, while Gaussian and sinusoidal initial data extend the comparison to two further smooth wave families. Section 5.1 introduces these test problems, their continuous references and the error measures. In Section 5.2, we first evaluate the numerical time derivatives at the initial state, where the difference from the continuous derivatives measures the spatial discretization error. We then advance the same initial fields with RK4 and examine how these differences develop in the coupled evolution of {m('u')} and {m('v')}.</p>\n'''
start, end = section_span(source, 'section-5')
first_child = re.search(r'<section\b[^>]*\bid="section-5\.1"', source[start:end])
assert first_child
intro_span = (start, start+first_child.start())

paper = source
paper = paper[:intro_span[0]] + intro + paper[intro_span[1]:]
for identity, content in replacements.items():
    paper = replace_section(paper, identity, content)

theory = HERE / 'theory_sync'
for identity in ['section-3.3', 'section-3.4']:
    path = theory / (identity + '.html')
    if not path.exists():
        raise RuntimeError('Awaiting audited theory synchronization: ' + str(path))
    paper = replace_section(paper, identity, path.read_text(encoding='utf-8'))

# Match the imported heading in the existing contents.
nav = BeautifulSoup(re.search(r'<nav\b.*?</nav>', paper, re.S).group(), 'html.parser')
for identity in ['section-4.1','section-5.1','section-5.2']:
    heading = BeautifulSoup(replacements[identity], 'html.parser').find(re.compile('^h[23]$')).get_text()
    nav.find('a', href='#'+identity).string = heading
paper = re.sub(r'<nav\b.*?</nav>', lambda _: str(nav), paper, count=1, flags=re.S)

# The editorial guide is agent-facing and records what actually remains open.
guide = '''<section class="guide" id="appendix-G" lang="zh-CN"><h2>Appendix G. Editorial guide（暂存，投稿前移除）</h2><p class="status">2026-10-25：六算例图文及三格式比较已并入主文。Centered-SD统一采用3.2的自然边场；3.3–3.4、4.1–4.2已同步变量和重构。5.1–5.2含三张表、30组图及图间分析，统一RK4比较当前三种空间格式。</p><p>4.2保留Euler、RK4、Crank–Nicolson的方法介绍。5.3的旧完整势时间比较已归档；当前自然Centered-SD的Euler与Crank–Nicolson数据尚待计算。5.3仅保留标题和源内备注。动网格4.3、5.4及稳定性4.4、5.5保持本轮之前的状态。</p><p>后续从当前正文继续。旧全节发布器会恢复过时的完整势表示，不能直接运行。当前整合源与核验位于Workspaces/dlw_paper_20261009/manuscript_integration_20261025/。</p></section>'''
paper = replace_section(paper, 'appendix-G', guide)

css = '''
/* Integrated numerical figures and three-line tables. */
.numerical-section .equation{overflow-x:auto;margin:20px 0}
.numerical-section .table-wrap{overflow-x:auto;margin:28px 0}
.numerical-section table{width:100%;border-collapse:collapse;border-top:2px solid #222;border-bottom:2px solid #222;font-size:14px;line-height:1.5;font-variant-numeric:tabular-nums}
.numerical-section caption{text-align:left;font-size:16px;padding-bottom:12px}
.numerical-section thead{border-bottom:1px solid #222}
.numerical-section th,.numerical-section td{padding:11px 9px}
.numerical-section thead th{text-align:center;font-weight:500}
.numerical-section tbody th{text-align:left}
.numerical-section td{text-align:right;white-space:nowrap}
.numerical-section sup{font-size:.7em}
.numerical-section figure{margin:30px 0 36px;break-inside:avoid}
.numerical-section figure img{display:block;width:100%;height:auto}
.numerical-section figcaption{font-size:14px;line-height:1.65;margin-top:12px}
.numerical-section .export{font:12px Arial,sans-serif;margin-left:8px}
.numerical-section h4{font-size:19px;margin:32px 0 12px}
.numerical-section h5{font-size:18px;margin:32px 0 10px}
.numerical-section details{margin:35px 0;border-top:1px solid #ccd2d7;padding-top:18px}
.numerical-section summary{cursor:pointer;font-size:19px}
.numerical-section .figure-link{font-size:14px}
@media print{.numerical-section table{font-size:8pt}.numerical-section tr{break-inside:avoid}.numerical-section h3,.numerical-section h4{break-after:avoid}.numerical-section .export{display:none}.numerical-section details::details-content{content-visibility:visible;height:auto}.numerical-section details>summary{list-style:none}}
'''
paper = paper.replace('</style>', css+'</style>', 1)
paper = render(paper)
assert 'INTEGRATIONMATH' not in paper and 'katex-error' not in paper

current_sha = hashlib.sha256(PAPER.read_bytes()).hexdigest()
before_sha = hashlib.sha256(BASELINE.read_bytes()).hexdigest()
previous = HERE/'integration_manifest.json'
allowed = {before_sha}
if previous.exists():
    allowed.add(json.loads(previous.read_text(encoding='utf-8'))['after_sha256'])
assert current_sha in allowed, 'The manuscript has changed concurrently; review before publishing.'
PAPER.write_text(paper, encoding='utf-8')
for identity in replacements:
    a,b=section_span(paper,identity)
    (HERE/(identity+'.html')).write_text(paper[a:b],encoding='utf-8')
manifest=dict(before_sha256=before_sha,after_sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest(),draft_sha256=hashlib.sha256(DRAFT.read_bytes()).hexdigest(),replaced_sections=list(replacements)+['section-3.3','section-3.4','appendix-G'],moving_mesh_changed=False,time_methods_preserved=['Euler','RK4','Crank–Nicolson'],current_time_comparison_data='RK4 only; old full-potential table archived',figures=30)
previous.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
