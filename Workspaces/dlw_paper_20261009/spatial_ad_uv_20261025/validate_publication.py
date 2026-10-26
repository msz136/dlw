"""Validate the A/D physical-field publication without modifying its inputs.

Run after publish.py. Only publication_validation.json is written.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit
from collections import Counter
import csv
import hashlib
import json
import re
import subprocess
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REPORT = HERE.parent / 'report_refresh_20261024'
CASES = ['A', 'D', 'Gaussian', 'Sinusoidal']
NAMES = ['One-soliton', 'Two-soliton', 'Gaussian', 'Sinusoidal']
METHODS = ['Endpoint-SD', 'Centered-SD', 'FD']
PAPER = ROOT / 'dlw-paper.html'
DRAFT = ROOT / 'report/dlw_numerical_text_20261025.html'
GALLERY = ROOT / 'report/dlw_uv_figure_choices_20261025.html'


def raw_section(text, identity):
    first = re.search(r'<section\b[^>]*\bid="' + re.escape(identity) + r'"[^>]*>', text)
    assert first, ('missing section', identity)
    depth = 1
    for token in re.finditer(r'</?section\b[^>]*>', text[first.end():]):
        depth += -1 if token.group().startswith('</') else 1
        if depth == 0:
            return text[first.start():first.end() + token.end()]
    raise AssertionError(('unclosed section', identity))


def local_target(base, target):
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None, parsed.fragment
    path = unquote(parsed.path)
    return (base.parent / path).resolve() if path else base.resolve(), parsed.fragment


def inspect_document(path):
    text = path.read_text(encoding='utf-8')
    doc = BeautifulSoup(text, 'html.parser')
    ids = [e['id'] for e in doc.select('[id]')]
    assert len(ids) == len(set(ids)), ('duplicate id', path)
    assert not re.search(r'(?:ADUVMATH|FOURCASEMATH|MATHSLOT)\d+END|katex-error', text), path
    for element in doc.select('img[src],a[href],link[href]'):
        target = element.get('src') or element.get('href')
        actual, fragment = local_target(path, target)
        if actual is None:
            continue
        assert actual.exists(), ('broken local link', path, target)
        if actual == path.resolve() and fragment:
            assert fragment in ids, ('broken internal anchor', path, target)
    return text, doc


def expected_figures(include_exact=True):
    stems = []
    for case in CASES:
        if include_exact:
            stems.append('exact_' + case)
        stems.extend(['exact_3d_' + case, 'spatial_' + case, 'errors_3d_separate_' + case, 'errors_3d_overlay_' + case, 'plain_' + case])
    return Counter(stems)


def check_figures(doc, path, include_exact):
    figures = doc.find_all('figure')
    assert len(figures) == (24 if include_exact else 20), (path, len(figures))
    stems = []
    for figure in figures:
        images = figure.find_all('img')
        assert len(images) == 1, (path, figure.get('id'))
        image = images[0]
        stem = Path(urlsplit(image['src']).path).stem
        stems.append(stem)
        assert not stem.startswith(('initial_', 'rate_')), ('derivative figure', path, stem)
        assert figure.figcaption is not None, ('caption missing', path, stem)
        pdfs = [a for a in figure.select('a[href]') if urlsplit(a['href']).path.endswith('.pdf')]
        if figure.get('data-view') == 'surface':
            assert not pdfs, ('surface preview is PNG', path, stem)
        else:
            assert len(pdfs) == 1 and Path(urlsplit(pdfs[0]['href']).path).stem == stem, (path, stem)
    assert Counter(stems) == expected_figures(include_exact), (path, stems)
    assert not doc.find(id='initial-rate-figures'), ('old derivative plot block', path)
    return len(figures)


def normalize_fragment(element, origin, strip_id=False):
    fragment = BeautifulSoup(str(element), 'html.parser')
    if strip_id:
        first = fragment.find()
        if first is not None:
            first.attrs.pop('id', None)
    for node in fragment.select('[src],[href]'):
        for attr in ['src', 'href']:
            if attr not in node.attrs:
                continue
            actual, anchor = local_target(origin, node[attr])
            if actual is not None:
                node[attr] = actual.as_posix() + ('#' + anchor if anchor else '')
    return str(fragment)


def check_tables(doc, path):
    assert len(doc.find_all('table')) == 3, path
    parameters = doc.find(id='table-parameters')
    assert parameters is not None
    rows = parameters.select('tbody tr')
    assert [r.th.get_text(strip=True) for r in rows] == NAMES[:2]
    compact = lambda s: re.sub(r'\s+', '', s).replace('−', '-').replace('–', '-')
    expected = [
        ['(1,2)', 'R=5', '[-10,10)'],
        ['(1,2),(4,-3)', 'R=30', '[-40,40)'],
    ]
    for row, cells in zip(rows, expected):
        assert [compact(td.get_text(' ', strip=True)) for td in row.find_all('td')] == cells, (path, row.get_text())
    values_checked = bold_checked = 0
    for tid, filename, keys, method_key in [
        ('table-initial', 'table1_initial_derivative_errors.csv', ['error_ut', 'error_vt'], 'method'),
        ('table-final', 'table2_final_field_errors.csv', ['error_u', 'error_v'], 'space'),
    ]:
        source = list(csv.DictReader((REPORT / filename).open(encoding='utf-8-sig', newline='')))
        assert len(source) == 12
        assert [(r['case'], r[method_key]) for r in source] == [(c, m) for c in CASES for m in METHODS]
        table = doc.find(id=tid)
        assert table is not None, (path, tid)
        assert [h.get_text(strip=True) for h in table.select('thead tr:first-child th[colspan]')] == METHODS
        table_rows = table.select('tbody tr')
        assert [r.th.get_text(strip=True) for r in table_rows] == NAMES, (path, tid)
        for row, case in zip(table_rows, CASES):
            pairs = [[float(next(r for r in source if r['case'] == case and r[method_key] == method)[key]) for key in keys] for method in METHODS]
            minima = [min(v[j] for v in pairs) for j in [0, 1]]
            cells = row.find_all('td')
            assert len(cells) == 6
            for index, cell in enumerate(cells):
                value = pairs[index // 2][index % 2]
                assert float(cell['data-value']) == value, (path, tid, case, index)
                winner = f'{value:.3e}' == f'{minima[index % 2]:.3e}'
                assert bool(cell.strong) == winner, (path, tid, case, index, 'minimum')
                mantissa, exponent = f'{value:.3e}'.split('e')
                assert mantissa in cell.get_text() and cell.sup.get_text() == str(int(exponent))
                values_checked += 1
                bold_checked += winner
    assert values_checked == 48 and bold_checked == 16
    return dict(error_values=values_checked, bold_minima=bold_checked, parameter_cases=['A', 'D'])


def check_formula_rendering(documents):
    formulas = [e.get_text() for doc in documents for e in doc.select('annotation[encoding="application/x-tex"]')]
    unique = list(dict.fromkeys(formulas))
    js = "const fs=require('fs'),k=require(process.argv[1]);const a=JSON.parse(fs.readFileSync(0,'utf8'));a.forEach(t=>k.renderToString(t,{displayMode:true,throwOnError:true,strict:'error'}));process.stdout.write(String(a.length));"
    result = subprocess.run(['node', '-e', js, str(ROOT / 'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')], input=json.dumps(unique), text=True, encoding='utf-8', capture_output=True, check=True)
    return dict(total_occurrences=len(formulas), unique_rendered=int(result.stdout))


def main():
    paper_text, paper = inspect_document(PAPER)
    draft_text, draft = inspect_document(DRAFT)
    gallery_text, gallery = inspect_document(GALLERY)
    before = (HERE / 'before_dlw-paper.html').read_text(encoding='utf-8')
    protected = ['abstract', 'section-1', 'section-2', 'section-3', 'section-4', 'section-5.3', 'section-5.4', 'section-5.5', 'section-6', 'appendix-A', 'appendix-B', 'appendix-C', 'appendix-D', 'references']
    for identity in protected:
        assert raw_section(paper_text, identity) == raw_section(before, identity), ('protected section changed', identity)
    paper_tables = check_tables(paper, PAPER)
    draft_tables = check_tables(draft, DRAFT)
    figure_counts = dict(paper=check_figures(paper, PAPER, True), draft=check_figures(draft, DRAFT, True), gallery=check_figures(gallery, GALLERY, False))
    for identity in ['section-5.1', 'section-5.2']:
        assert normalize_fragment(paper.find(id=identity), PAPER) == normalize_fragment(draft.find(id=identity), DRAFT), ('draft differs', identity)
    assert [s['id'] for s in gallery.select('section[id]')] == ['case-' + c for c in CASES]
    assert not gallery.find_all('table')
    for case in CASES:
        for view in ['exact-3d', 'heatmap', 'separate', 'overlay', 'surface']:
            primary = paper.find('figure', attrs={'data-case': case, 'data-view': view})
            candidate = gallery.find(id='choice-' + view + '-' + case)
            assert primary is not None and candidate is not None
            assert normalize_fragment(primary, PAPER, True) == normalize_fragment(candidate, GALLERY, True), ('gallery differs', case, view)
    for doc, path in [(paper, PAPER), (draft, DRAFT)]:
        introduction = doc.find(id='section-5.1')
        comparisons = doc.find(id='section-5.2')
        assert len(introduction.find_all('figure')) == 8, ('initial-field figure count', path)
        assert len(comparisons.find_all('figure')) == 16, ('terminal-error figure count', path)
        assert [f['id'] for f in doc.find_all('figure')] == ['figure-' + str(i) for i in range(1,25)], ('figure numbering', path)
        for case in CASES:
            overlay=comparisons.find('figure',attrs={'data-case':case,'data-view':'overlay'})
            surface=overlay.find_next_sibling('figure')
            assert surface['data-view']=='surface' and surface['data-case']==case, ('surface adjacency', path, case)
        assert [f['data-case'] for f in introduction.find_all('figure', attrs={'data-view': 'exact-3d'})] == CASES, ('initial-field 3D case order', path)
        assert not comparisons.find_all('figure', attrs={'data-view': 'exact-3d'}), ('initial-field 3D placement', path)
    visible = ' '.join(paper.find(id=s).get_text(' ', strip=True) for s in ['section-5.1', 'section-5.2'])
    for stale in ['Case C', 'Case B', '(6, −5)', 'six cases', 'six tests', 'full-potential']:
        assert stale not in visible, ('stale visible content', stale)
    assert not paper.find(id='section-5.2').find_all('details'), 'Candidate figures should remain visible in the body'
    rendering = check_formula_rendering([paper, draft, gallery])
    result = dict(status='passed', cases=CASES, display_names=NAMES, protected_sections_unchanged=protected,
        main_tables=paper_tables, draft_tables=draft_tables, figures=figure_counts,
        initial_derivative_table_retained=True, derivative_figures=0, exact_initial_field_3d_figures=4,
        terminal_error_figures=16, surface_only_3d_figures=4, main_draft_numerical_sections_identical=True,
        gallery_matches_published_figures=True, links_and_ids_valid=True, katex=rendering,
        input_hashes={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in [PAPER, DRAFT, GALLERY]})
    (HERE / 'publication_validation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
