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
old_replaced = (len(os_.find('section', id='abstract').select('span.katex')) +
                len(os_.find('section', id='section-1').select('span.katex')) +
                len(os_.find('section', id='section-6').select('span.katex')) +
                sum(len(p.select('span.katex')) for p in old52[-2:]))
rep['katex_accounting'] = dict(old_total=len(os_.select('span.katex')),
                               old_replaced=old_replaced, new_replaced=added,
                               new_total=rep['katex'])
assert rep['katex'] == len(os_.select('span.katex')) - old_replaced + added, rep['katex_accounting']
assert rep['figures'] == 28 and rep['tables'] == 6
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
cited = {n for n in cited if 1 <= n <= 15}
rep['cited'] = sorted(cited)
assert cited == set(range(1, 16)), sorted(set(range(1, 16)) - cited)

# structure of 5.2: the closing paragraphs are the supplied ones
s52 = ns.find('section', id='section-5.2')
ps = s52.find_all('p', recursive=False)
rep['section52_paragraphs'] = len(ps)
rep['section52_last_two'] = [p.get_text(' ', strip=True)[:60] for p in ps[-2:]]
assert ps[-2].get_text(strip=True).startswith('Taken together, the initial diagnostics in Table 2')
assert ps[-1].get_text(strip=True).startswith('By placing the')
assert 'complement each other' in ps[-2].get_text()

# conclusions: four paragraphs, no mention of stability sections
concl = ns.find('section', id='section-6')
ctext = re.sub(r'\s+', ' ', concl.get_text(' '))
rep['section6_paragraphs'] = len(concl.find_all('p'))
assert rep['section6_paragraphs'] == 4
for bad in ('Section 4.4', 'Section 5.5', 'linearized evolution', 'stability properties',
            'perturbed initial data', 'future work'):
    assert bad not in ctext, bad
rep['section6_words'] = len(ctext.split())

# balanced wording present
for phrase in ('direct and compact two-field formulation',
               'different trade-offs in physical-field reconstruction',
               'yields the smallest error in the second field',
               'complement each other across different wave regimes',
               'naturally supplies an exact semi-discrete conservation law'):
    assert phrase in text, phrase
rep['balance_checks'] = 5
for bad in ('degrades', 'degraded', 'contaminated', 'defective', 'fragile'):
    assert bad not in text, bad
rep['no_negative_framing'] = True

rep['abstract_words'] = len(re.sub(r'\s+', ' ', ns.find('section', id='abstract').get_text(' ')).split())
rep['section1_paragraphs'] = len(ns.find('section', id='section-1').find_all('p'))
rep['paper_sha256'] = hashlib.sha256(PAPER.read_bytes()).hexdigest()
rep['bytes'] = len(PAPER.read_bytes())
(HERE / 'validation.json').write_text(json.dumps(rep, indent=2), encoding='utf-8')
print(json.dumps(rep, indent=2))
