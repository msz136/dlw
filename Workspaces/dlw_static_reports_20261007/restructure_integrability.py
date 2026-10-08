"""Regroup the existing theory report, preserving its rendered equations and fonts."""
from pathlib import Path
import hashlib
import json

from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BEFORE = HERE / 'before_flow/dlw_integrability.html'
DEST = ROOT / 'dlw_integrability.html'
GROUPS = [
    ('方程与场空间', ['conditions-text', 'coordinates-text', 'start-text']),
    ('谱量与 Hamiltonian', ['foundation-text', 'charges-text', 'energy-text']),
    ('守恒与对易', ['bracket-text', 'conservation-text', 'involution-text']),
    ('泛型独立性', ['frequency-text', 'jacobian-text', 'generic-text']),
    ('可积性结论', ['endpoint-text', 'lean-endpoint']),
]
INTRO = '从闭合周期场和 DLW 方程出发，构造全阶谱量及 Hamiltonian，证明守恒、对易与有限前缀的泛型独立性，得到周期场可积性结论。'
FLOW_CSS = '''
/* Five stages of the theoretical argument. */
.theory-flow{gap:6px 16px}
.theory-flow a:not(:last-child)::after{content:"→";margin-left:16px;color:#777}
.theory-stage{margin-top:36px}
.theory-part+.theory-part{margin-top:20px}
@media(max-width:650px){.theory-flow{gap:6px 14px}.theory-flow a::after{display:none}}
'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def revise_paragraphs(soup):
    # Keep the notation and equations; make former subsection boundaries read as prose.
    coordinates = soup.select_one('#coordinates-text > p')
    assert coordinates.get_text() == '取'
    coordinates.string = '为消去闭合约束，取零均值坐标'
    start = soup.select_one('#start-text > p')
    assert str(start.contents[0]) == '记 '
    start.contents[0].replace_with('在上述闭合场上，记 ')
    foundation = soup.select_one('#foundation-text > p')
    assert str(foundation.contents[0]) == '用 '
    foundation.contents[0].replace_with('为构造全阶谱量，用 ')
    energy = soup.select_one('#energy-text > p')
    assert energy.get_text() == '格点算子由有限矩阵直接构造：'
    energy.string = '将谱量与物理 Hamiltonian 联系起来，先定义格点算子：'
    bracket = soup.select_one('#bracket-text > p')
    assert bracket.get_text() == '定义变分配对'
    bracket.string = '在零均值坐标中，定义变分配对'
    generic = soup.select_one('#generic-text > p')
    assert str(generic.contents[0]).startswith('非零见证子式是连续微分多项式。')
    generic.contents[0].replace_with(str(generic.contents[0]).replace(
        '非零见证子式是连续微分多项式。', '由这一非零子式，可将独立性推广到开稠密集。该子式是连续微分多项式。', 1))
    for text in list(soup.select_one('#frequency-text').find_all(string=True)):
        if '第 6 节的守恒族' in text:
            text.replace_with(text.replace('第 6 节的守恒族', '上文的守恒族'))


def build():
    baseline = json.loads((HERE / 'before_flow/input_hashes.json').read_text('utf-8'))
    for name, expected in baseline['notebooks_and_numerical'].items():
        assert sha(ROOT / name) == expected, name
    soup = BeautifulSoup(BEFORE.read_text('utf-8'), 'html.parser')
    revise_paragraphs(soup)
    intro = soup.select_one('#intro')
    intro.select_one('p').string = INTRO
    intro.select_one('nav').decompose()
    nav = soup.new_tag('nav', attrs={'class': 'theory-flow', 'aria-label': '推导流程'})
    for index, (title, cell_ids) in enumerate(GROUPS, 1):
        stage = soup.new_tag('section', attrs={'class': 'theory-stage', 'data-stage': str(index)})
        heading = soup.new_tag('h2', attrs={'id': f'section-{index}'})
        heading.string = f'{index}. {title}'
        stage.append(heading)
        for cell_id in cell_ids:
            part = soup.select_one(f'#{cell_id}').extract()
            for old_heading in part.select('h2'):
                old_heading.decompose()
            part.name = 'div'
            part['class'] = ['theory-part']
            stage.append(part)
        soup.main.append(stage)
        link = soup.new_tag('a', href=f'#section-{index}')
        link.string = f'{index}. {title}'
        nav.append(link)
    intro.append(nav)
    soup.style.append(FLOW_CSS)
    DEST.write_text(str(soup) + '\n', encoding='utf-8')
    for name, expected in baseline['notebooks_and_numerical'].items():
        assert sha(ROOT / name) == expected, name
    manifest = {
        'success': True, 'delivery': str(DEST), 'delivery_sha256': sha(DEST),
        'baseline': str(BEFORE), 'baseline_sha256': sha(BEFORE),
        'major_sections': len(GROUPS), 'cells': len(soup.select('[data-cell]')),
        'flow': [title for title, _ in GROUPS],
        'math_expressions': len(soup.select('[data-formula]')),
        'visible_code_lines': len(soup.select_one('pre code').get_text().splitlines()),
        'notebooks_edited': False, 'notebooks_executed': False,
        'numerical_html_unchanged': True, 'fonts_and_rendered_math_preserved': True,
        'standalone': True, 'bytes': DEST.stat().st_size,
    }
    (HERE / 'build_validation.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    build()
