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

rep = {}
changed = [s.get('id') for s in ns.find_all('section')
           if str(s) != str(os_.find('section', id=s.get('id')))]
rep['changed'] = changed
assert set(changed) == {'abstract', 'section-1', 'section-6'}, changed

rep['figures'] = len(ns.find_all('figure'))
rep['tables'] = len(ns.find_all('table'))
rep['katex'] = len(ns.select('span.katex'))
rep['katex_errors'] = len(ns.select('.katex-error'))
added = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))['formulas']
assert rep['figures'] == 28 and rep['tables'] == 6
blocks = ('abstract', 'section-1', 'section-6')
new_in = sum(len(ns.find('section', id=s).select('span.katex')) for s in blocks)
old_in = sum(len(os_.find('section', id=s).select('span.katex')) for s in blocks)
rep['katex_in_blocks'] = [old_in, new_in]
assert new_in == added, (new_in, added)
assert rep['katex'] == len(os_.select('span.katex')) - old_in + added
assert rep['katex_errors'] == 0

text = re.sub(r'\s+', ' ', ns.get_text(' '))
body = text.split('References')[0]
cited = set()
for grp in re.findall(r'\[([\d,\u2013\-\s]+)\]', body):
    for part in grp.split(','):
        part = part.strip()
        m = re.fullmatch(r'(\d+)\s*[\u2013-]\s*(\d+)', part)
        if m:
            cited |= set(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.isdigit():
            cited.add(int(part))
rep['cited_raw'] = sorted(cited)
# brackets such as [-30,30] in figure captions also match; keep the reference range only
cited = {n for n in cited if 1 <= n <= 15}
rep['cited'] = sorted(cited)
assert cited == set(range(1, 16)), sorted(set(range(1, 16)) - cited)
assert len(ns.find('section', id='references').find_all('li')) == 15

for sid in ('abstract', 'section-1', 'section-6'):
    sec = ns.find('section', id=sid)
    rep[sid + '_words'] = len(re.sub(r'\s+', ' ', sec.get_text(' ')).split())
    rep[sid + '_paragraphs'] = len(sec.find_all('p'))
assert rep['section-1_paragraphs'] == 6 and rep['section-6_paragraphs'] == 5
assert rep['abstract_paragraphs'] == 1

# spot checks on the supplied wording
for phrase in ('structural choices at the bilinear', 'endpoint-based lattice (Endpoint-SD)',
               'prototypical higher-dimensional integrable model',
               'central motivation of the present work',
               'decisive for balanced multi-component accuracy',
               'fortuitous error cancellation', 'frozen-mesh control experiments'):
    assert phrase in text, phrase
rep['spot_checks'] = 7

# placeholders untouched
for sid in ('section-4.4', 'section-5.5'):
    assert ns.find('section', id=sid).find_all(['p', 'figure', 'table', 'div']) == []

rep['paper_sha256'] = hashlib.sha256(PAPER.read_bytes()).hexdigest()
rep['bytes'] = len(PAPER.read_bytes())
(HERE / 'validation.json').write_text(json.dumps(rep, indent=2), encoding='utf-8')
print(json.dumps(rep, indent=2))
