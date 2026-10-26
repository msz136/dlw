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
assert set(changed) == {'abstract', 'section-1', 'section-5.2', 'section-5', 'section-6'}, changed

rep['figures'] = len(ns.find_all('figure'))
rep['tables'] = len(ns.find_all('table'))
rep['katex'] = len(ns.select('span.katex'))
rep['katex_errors'] = len(ns.select('.katex-error'))
added = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))['formulas']

old52 = os_.find('section', id='section-5.2').find_all('p', recursive=False)
old1 = os_.find('section', id='section-1').find_all('p')
old_replaced = (len(os_.find('section', id='abstract').select('span.katex')) +
                sum(len(p.select('span.katex')) for p in old1[2:5]) +
                len(os_.find('section', id='section-6').select('span.katex')) +
                sum(len(p.select('span.katex')) for p in old52[-2:]))
rep['katex_accounting'] = dict(old_total=len(os_.select('span.katex')),
                               old_replaced=old_replaced, new_replaced=added,
                               new_total=rep['katex'])
assert rep['katex'] == len(os_.select('span.katex')) - old_replaced + added, rep['katex_accounting']
assert rep['figures'] == 28 and rep['tables'] == 6
assert rep['katex_errors'] == 0

# introduction: paragraphs 1, 2, 6 unchanged
newp = ns.find('section', id='section-1').find_all('p')
oldp = os_.find('section', id='section-1').find_all('p')
rep['intro_paragraphs'] = len(newp)
assert len(newp) == 6 and len(oldp) == 6
assert str(newp[0]) == str(oldp[0]) and str(newp[1]) == str(oldp[1]) and str(newp[5]) == str(oldp[5])
assert all(str(newp[i]) != str(oldp[i]) for i in (2, 3, 4))
rep['intro_kept'] = [1, 2, 6]

text = re.sub(r'\s+', ' ', ns.get_text(' '))
body = text.split('References')[0]
cited = set()
for grp in re.findall(r'\[([\d,\u2013\-\s]+)\]', body):
    for part in grp.split(','):
        part = part.strip()
        mm = re.fullmatch(r'(\d+)\s*[\u2013-]\s*(\d+)', part)
        if mm:
            cited |= set(range(int(mm.group(1)), int(mm.group(2)) + 1))
        elif part.isdigit():
            cited.add(int(part))
cited = {n for n in cited if 1 <= n <= 15}
rep['cited'] = sorted(cited)
assert cited == set(range(1, 16)), sorted(set(range(1, 16)) - cited)

# section 5.2 tail
s52ps = ns.find('section', id='section-5.2').find_all('p', recursive=False)
assert s52ps[-2].get_text(strip=True).startswith('Taken together, Table 2 and Table 3')
assert s52ps[-1].get_text(strip=True).startswith('Across all four test regimes')
rep['section52_paragraphs'] = len(s52ps)

# conclusions
concl = ns.find('section', id='section-6')
cps = concl.find_all('p')
rep['section6_paragraphs'] = len(cps)
assert len(cps) == 3
ctext = re.sub(r'\s+', ' ', concl.get_text(' '))
rep['section6_words'] = len(ctext.split())
assert ctext.strip().startswith('6. Conclusions In this work')
assert 'Viewed in a broader context' in ctext
for bad in ('Section 4.4', 'Section 5.5', 'linearized evolution', 'stability properties',
            'perturbed initial data', 'future work'):
    assert bad not in ctext, bad

# plain description: no evaluative framing
for bad in ('complementary', 'strengths', 'trade-off', 'trade-offs', 'degrades', 'degraded',
            'contaminated', 'defective', 'fragile', 'outperform'):
    assert bad not in text, bad
rep['plain_description'] = True

# abstract structure
ab = re.sub(r'\s+', ' ', ns.find('section', id='abstract').get_text(' '))
rep['abstract_words'] = len(ab.split())
assert ab.strip().startswith('Abstract')
assert 'dispersive long-wave (DLW) system is a fundamental integrable model' in ab
assert 'Together, these results show how bilinear lattice symmetry' in ab

rep['paper_sha256'] = hashlib.sha256(PAPER.read_bytes()).hexdigest()
rep['bytes'] = len(PAPER.read_bytes())
(HERE / 'validation.json').write_text(json.dumps(rep, indent=2), encoding='utf-8')
print(json.dumps(rep, indent=2))
