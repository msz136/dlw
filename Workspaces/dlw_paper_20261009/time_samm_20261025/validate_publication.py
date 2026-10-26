"""Independent checks of the published Sections 4.2-4.3 and 5.3-5.4."""
from pathlib import Path
import hashlib, json, re
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAPER = ROOT / 'dlw-paper.html'
BEFORE = HERE / 'before/dlw-paper.html'
TIME = HERE / 'time'
SAMM = HERE / 'samm_periodic'
FIG = HERE / 'figures'

report = {}


def text_of(soup, ident):
    node = soup.find(id=ident)
    assert node is not None, ident
    return re.sub(r'\s+', ' ', node.get_text(' ', strip=True))


before = BeautifulSoup(BEFORE.read_text(encoding='utf-8'), 'html.parser')
after = BeautifulSoup(PAPER.read_text(encoding='utf-8'), 'html.parser')

sections = [s['id'] for s in after.find_all('section') if s.get('id')]
changed = sorted(i for i in sections if text_of(before, i) != text_of(after, i))
report['changed_sections'] = changed
assert set(changed) <= {'section-4', 'section-4.2', 'section-4.3', 'section-5', 'section-5.3',
                        'section-5.4', 'appendix-G'}, changed
for protected in ('section-1', 'section-2', 'section-2.1', 'section-2.2', 'section-2.3', 'section-2.4',
                  'section-3', 'section-3.1', 'section-3.2', 'section-3.3', 'section-3.4', 'section-4.1',
                  'section-4.4', 'section-5.1', 'section-5.2', 'section-5.5', 'section-6'):
    assert text_of(before, protected) == text_of(after, protected), protected

report['figures'] = len(after.find_all('figure'))
report['tables'] = len(after.find_all('table'))
assert report['figures'] == 28 and report['tables'] == 5
for img in after.find_all('img'):
    src = img.get('src', '')
    if src.startswith('Workspaces/'):
        assert (ROOT / src).exists(), src

# Captions are numbered consecutively in document order.
numbers = [int(m.group(1)) for m in
           (re.match(r'Figure (\d+)\.', f.figcaption.get_text(' ', strip=True)) for f in after.find_all('figure'))
           if m]
assert numbers == list(range(1, 29)), numbers
table_numbers = [int(m.group(1)) for m in
                 (re.match(r'Table (\d+)\.', t.caption.get_text(' ', strip=True)) for t in after.find_all('table'))
                 if m]
assert table_numbers == list(range(1, 6)), table_numbers

# Terminal errors quoted in Table 4 agree with the recorded runs.
def sci(x):
    e = int(__import__('math').floor(__import__('math').log10(abs(x))))
    mant = x / 10 ** e
    if round(mant, 3) >= 10:
        mant /= 10
        e += 1
    return f'{mant:.3f} × 10{e}'


def text_cells(table):
    return [[c.get_text(' ', strip=True).replace(' ', '') for c in row.find_all(['th', 'td'])]
            for row in table.find('tbody').find_all('tr')]


t4 = after.find('table', id='table-time')
for row, case in zip(text_cells(t4), ('A', 'D', 'Gaussian', 'Sinusoidal')):
    rec = json.loads((TIME / f'{case}_time.json').read_text(encoding='utf-8'))
    want = [sci(rec['integrators'][k]['error'][i]).replace(' ', '').replace('<sup>', '').replace('</sup>', '')
            for k in ('Euler', 'RK4', 'CN') for i in (0, 1)]
    got = [c.replace('<sup>', '').replace('</sup>', '') for c in row[1:]]
    assert got == want, (case, got, want)
report['table4_entries_checked'] = 24

# Table 5 and the reductions quoted in the text.
t5 = after.find('table', id='table-mesh')
rows = text_cells(t5)
expected_text = {'A': ('11.7%', '17.4%'), 'D': ('6.0%', '5.6%')}
for row, case in zip(rows, ('A', 'D')):
    uni = json.loads((SAMM / f'{case}_uniform_0.0001.json').read_text(encoding='utf-8'))['error']
    ada = json.loads((SAMM / f'{case}_moving_0.0001.json').read_text(encoding='utf-8'))['error']
    got = [c.replace('<sup>', '').replace('</sup>', '') for c in row[1:5]]
    want = [sci(uni[0]).replace(' ', ''), sci(uni[1]).replace(' ', ''),
            sci(ada[0]).replace(' ', ''), sci(ada[1]).replace(' ', '')]
    assert got == want, (case, got, want)
    assert tuple(row[5:7]) == expected_text[case], (case, row[5:7])
    ru, rv = 100 * (1 - ada[0] / uni[0]), 100 * (1 - ada[1] / uni[1])
    assert abs(ru - float(expected_text[case][0][:-1])) < 0.05
    assert abs(rv - float(expected_text[case][1][:-1])) < 0.05
report['table5_entries_checked'] = 12

# The paper states that the RK4 row reproduces Table 3; check the Centered-SD column.
t3 = before.find('table', id='table-final')
c3 = text_cells(t3)
for row, case in zip(c3, ('A', 'D', 'Gaussian', 'Sinusoidal')):
    rec = json.loads((TIME / f'{case}_time.json').read_text(encoding='utf-8'))['integrators']['RK4']['error']
    paper = [row[3].replace('<sup>', '').replace('</sup>', ''), row[4].replace('<sup>', '').replace('</sup>', '')]
    assert paper == [sci(rec[0]).replace(' ', ''), sci(rec[1]).replace(' ', '')], (case, paper)
report['rk4_reproduced_table3'] = True

# Caption and prose claims that must not drift from the data.
full = re.sub(r'\s+', ' ', after.get_text(' ', strip=True))
for claim in ('11.7', '17.4', '6.0', '5.6', '12.8', '16.3', '5.3', '5.8', '7.3 × 10',
              '1.664 × 10', '1.671 × 10', '1.560 × 10', '1.048 × 10', '9.5 × 10', '5.2 × 10',
              '0.79', '0.18', '36%'):
    assert claim in full, claim
report['claims_checked'] = 18

report['after_sha256'] = hashlib.sha256(PAPER.read_bytes()).hexdigest()
report['before_sha256'] = hashlib.sha256(BEFORE.read_bytes()).hexdigest()
report['figure_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted(FIG.glob('*.png'))}
(HERE / 'validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps({k: v for k, v in report.items() if k not in ('figure_sha256',)}, indent=2))


