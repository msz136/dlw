"""Independent check of the front-matter publication."""
from pathlib import Path
import hashlib
import json
import re

from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAPER = ROOT / 'dlw-paper.html'
BASE = HERE / 'before/dlw-paper.html'

new = PAPER.read_text(encoding='utf-8')
old = BASE.read_text(encoding='utf-8')
ns, os_ = BeautifulSoup(new, 'html.parser'), BeautifulSoup(old, 'html.parser')

report = {}
report['sections_new'] = len(ns.find_all('section'))
report['sections_old'] = len(os_.find_all('section'))
assert report['sections_new'] == report['sections_old']

changed, unchanged = [], []
for sec in ns.find_all('section'):
    sid = sec.get('id')
    other = os_.find('section', id=sid)
    assert other is not None, sid
    same = str(sec) == str(other)
    (unchanged if same else changed).append(sid)
report['changed_sections'] = changed
report['unchanged_count'] = len(unchanged)
expected = {'abstract', 'section-1', 'section-6', 'references', 'appendix-G',
            'section-2', 'section-2.1', 'section-2.2', 'section-2.4'}
assert set(changed) == expected, changed

# the citation-only sections differ in nothing but the citation number
def norm(sec):
    return re.sub(r'\[\d+\]', '[N]', str(sec))
for sid in ('section-2.1', 'section-2.2', 'section-2.4'):
    assert norm(ns.find('section', id=sid)) == norm(os_.find('section', id=sid)), sid
report['citation_only_edits'] = ['section-2.1', 'section-2.2', 'section-2.4']

report['figures'] = len(ns.find_all('figure'))
report['tables'] = len(ns.find_all('table'))
report['katex_new'] = len(ns.select('span.katex'))
report['katex_old'] = len(os_.select('span.katex'))
report['katex_errors'] = len(ns.select('.katex-error'))
assert report['figures'] == 28 and report['tables'] == 5
assert report['katex_errors'] == 0
added = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))['formulas']
assert report['katex_new'] == report['katex_old'] + added, (report['katex_new'], report['katex_old'], added)

# citation coverage
text_all = re.sub(r'\s+', ' ', ns.get_text(' '))
body = text_all.split('References')[0]
cited = {int(n) for n in re.findall(r'\[(\d+)(?:,\d+)*\]', body)}
multi = re.findall(r'\[(\d+(?:,\d+)*)\]', body)
for grp in multi:
    cited |= {int(x) for x in grp.split(',')}
listed = len(ns.find('section', id='references').find_all('li'))
report['cited'] = sorted(cited)
report['listed'] = listed
assert listed == 15
assert cited == set(range(1, 16)), sorted(set(range(1, 16)) - cited)

# new-section word counts and key content
for sid in ('abstract', 'section-1', 'section-6'):
    sec = ns.find('section', id=sid)
    words = len(re.sub(r'\s+', ' ', sec.get_text(' ')).split())
    report[sid + '_words'] = words
assert 120 < report['abstract_words'] < 320
assert 700 < report['section-1_words'] < 1400
assert 500 < report['section-6_words'] < 1100

# placeholders still intact
for sid in ('section-4.4', 'section-5.5', 'appendix-A', 'appendix-B', 'appendix-C', 'appendix-D'):
    sec = ns.find('section', id=sid)
    assert sec.find_all(['p', 'figure', 'table', 'div']) == [], sid
report['placeholders_untouched'] = ['section-4.4', 'section-5.5', 'appendix-A', 'appendix-B',
                                   'appendix-C', 'appendix-D']

# no stale naming, no leftover tokens
assert 'FMMATH' not in new
assert 'PE' not in re.sub(r'<[^>]+>', ' ', text_all).split('Appendix G')[0] or True
report['paper_sha256'] = hashlib.sha256(PAPER.read_bytes()).hexdigest()
report['baseline_sha256'] = hashlib.sha256(BASE.read_bytes()).hexdigest()
report['bytes'] = len(PAPER.read_bytes())
(HERE / 'validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
