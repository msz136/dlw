from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
import re, json

root = Path('C:/Users/msz/aca')
target = root / 'dlw-paper.html'
folder = Path(__file__).parent
old = target.read_bytes()
source = old.decode('utf-8')
match = re.search(r'<section id="abstract">.*?</section>', source, re.S)
assert match
section = match.group()
soup = BeautifulSoup(section, 'html.parser')
math = {s.find('annotation').get_text(): str(s) for s in soup.select('span.katex')}
text = '''Exact solutions of the [[DIM]]-dimensional dispersive long-wave (DLW) system provide a detailed description of nonlinear wave propagation and interaction. Extending these solutions to a spatial lattice brings their integrable structure into a discrete setting and raises the question of how the lattice changes the physical waves. In this work, we develop two related integrable semi-discretizations to study this connection between lattice construction and wave approximation. Starting from the Hirota–Miwa equation, a Miwa expansion gives an endpoint formulation (Endpoint-SD). A half-step parameter shift and a staggered placement of the [[TAU]] functions then yield a centered formulation (Centered-SD). Both admit explicit Gram determinant solutions and nonlinear physical-field equations with compatible Darboux–Lax representations, allowing the effects of lattice placement to be studied within a common integrable framework. To quantify these effects, we first examine how the equations and their exact wave fields approach their continuous counterparts. Endpoint-SD is second-order consistent in the first field equation and first-order consistent in the second, while Centered-SD achieves second-order consistency in both. Under suitable regularity and positivity assumptions, we further establish convergence orders for the corresponding exact wave fields and derive explicit leading error coefficients, describing how the lattice modifies the continuous wave profiles. These analytical comparisons provide a basis for numerical experiments with soliton, Gaussian and sinusoidal profiles. Through these experiments, we show how lattice placement, wave profile and field reconstruction jointly influence computational accuracy, with convergence orders and leading error coefficients helping to explain the behavior at finite lattice spacing. Building on this spatial comparison, we then examine how the errors develop during numerical evolution under different time integrators. The semi-discrete structure also offers a way to improve the resolution of the waves. Specifically, we establish a conservation law and use it to construct a self-adaptive moving mesh, improving the accuracy of both fields in the soliton tests at a fixed node count. Overall, this work connects the passage from continuous waves to integrable lattices with a quantitative understanding of the resulting approximation, and shows how the retained mathematical structure can guide numerical computation.'''
body = text.replace('[[DIM]]', math['(2+1)']).replace('[[TAU]]', math[r'\tau'])
replacement, count = re.subn(r'<p>.*?</p>', lambda m: '<p>' + body + '</p>', section, count=1, flags=re.S)
assert count == 1
updated = source[:match.start()] + replacement + source[match.end():]
assert updated[:match.start()] == source[:match.start()]
assert updated[match.start()+len(replacement):] == source[match.end():]
stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
(folder / ('before_abstract_' + stamp + '.html')).write_bytes(old)
target.write_bytes(updated.encode('utf-8'))
check = BeautifulSoup(updated, 'html.parser')
assert not check.select('.katex-error')
assert len(check.select('#abstract p')) == 1
result = {'only_abstract_changed': True, 'reused_validated_inline_math': ['(2+1)', r'\tau'], 'figures': len(check.find_all('figure')), 'tables': len(check.find_all('table'))}
(folder / 'abstract_validation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result))
