"""Independent check of the appendix publication."""
from pathlib import Path
import hashlib
import json
import re

from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAPER = ROOT / 'dlw-paper.html'
BASE = HERE / 'before/dlw-paper.html'

new, old = PAPER.read_text(encoding='utf-8'), BASE.read_text(encoding='utf-8')
ns, os_ = BeautifulSoup(new, 'html.parser'), BeautifulSoup(old, 'html.parser')

report = {}
changed = []
for sec in ns.find_all('section'):
    sid = sec.get('id')
    other = os_.find('section', id=sid)
    changed.append((sid, other is None or str(sec) != str(other)))
report['sections'] = len(ns.find_all('section'))
report['changed'] = [s for s, c in changed if c]
report['gone'] = [s.get('id') for s in os_.find_all('section') if ns.find('section', id=s.get('id')) is None]
assert report['gone'] == ['appendix-G']
assert set(report['changed']) == {'appendix-A', 'appendix-B', 'appendix-C', 'appendix-D',
                                  'section-2', 'section-2.4', 'section-3', 'section-3.2',
                                  'section-3.4', 'section-4', 'section-4.2'}, report['changed']

report['figures'] = len(ns.find_all('figure'))
report['tables'] = len(ns.find_all('table'))
report['table_numbers'] = re.findall(r'<caption>Table (\d+)\.', new)
report['katex'] = len(ns.select('span.katex'))
report['katex_errors'] = len(ns.select('.katex-error'))
assert report['figures'] == 28 and report['tables'] == 6
assert report['table_numbers'] == ['1', '2', '3', '4', '5', '6']
added = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))['formulas']
assert report['katex'] == len(os_.select('span.katex')) + added
assert report['katex_errors'] == 0

# appendix content
for sid, mins in (('appendix-A', 300), ('appendix-B', 300), ('appendix-C', 250), ('appendix-D', 350)):
    sec = ns.find('section', id=sid)
    words = len(re.sub(r'\s+', ' ', sec.get_text(' ')).split())
    report[sid + '_words'] = words
    assert words > mins, (sid, words)
report['appendix_A_equations'] = len(ns.find('section', id='appendix-A').select('div.equation'))
report['appendix_B_equations'] = len(ns.find('section', id='appendix-B').select('div.equation'))
report['appendix_C_equations'] = len(ns.find('section', id='appendix-C').select('div.equation'))
report['appendix_D_equations'] = len(ns.find('section', id='appendix-D').select('div.equation'))
assert report['appendix_A_equations'] == 3
assert report['appendix_B_equations'] == 3
assert report['appendix_C_equations'] == 3
assert report['appendix_D_equations'] == 0

# no dangling editorial guide, no leftover tokens
body = re.sub(r'\s+', ' ', ns.get_text(' '))
assert 'Editorial guide' not in body
assert '暂存，投稿前移除' not in body
assert 'APMATH' not in new
assert 'appendix-G' not in new

# forward references
report['appendix_mentions'] = sorted(set(re.findall(r'Appendix [A-D]\b', body)))

report['paper_sha256'] = hashlib.sha256(PAPER.read_bytes()).hexdigest()
report['bytes'] = len(PAPER.read_bytes())
(HERE / 'validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
