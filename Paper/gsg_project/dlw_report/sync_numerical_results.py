"""Refresh the root numerical report's source from the authoritative Markdown report.

Run before build_html.ps1 -SourceFile _src/numerical_analysis.src.html
                         -OutputFile numerical_analysis.html.
Does not run experiments or change their outputs.
"""
from pathlib import Path
import json
from urllib.parse import urlsplit
import markdown
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = HERE / '_src/numerical_analysis.src.html'
NUMERICS = ROOT / 'Paper/dlw_semidiscrete/numerics'
START = '<!-- NUMERICAL_RESULTS_START -->'
END = '<!-- NUMERICAL_RESULTS_END -->'


def main():
    report = BeautifulSoup(markdown.markdown(
        (NUMERICS / 'REPORT.md').read_text(encoding='utf-8'),
        extensions=['tables', 'fenced_code']), 'html.parser')
    report.h1.decompose()
    headings = []
    for index, heading in enumerate(report.find_all(['h2', 'h3']), 1):
        heading['id'] = f'result-{index}'
        if heading.name == 'h2':
            headings.append((heading['id'], heading.get_text()))
        heading.name = 'h' + str(int(heading.name[1]) + 1)
    for tag in report.find_all(['a', 'img']):
        attr = 'src' if tag.name == 'img' else 'href'
        value = tag.get(attr, '')
        if value and not urlsplit(value).scheme and not value.startswith('#'):
            tag[attr] = (NUMERICS / value).resolve().relative_to(ROOT).as_posix()
        if tag.name == 'img':
            tag['loading'] = 'lazy'
    for table in report.find_all('table'):
        table.wrap(report.new_tag('div', attrs={'class': 'tablewrap'}))
    nav = report.new_tag('nav', attrs={'aria-label': '实测结果目录'})
    ol = report.new_tag('ol')
    for ident, title in headings:
        li = report.new_tag('li')
        link = report.new_tag('a', href='#' + ident)
        link.string = title
        li.append(link)
        ol.append(li)
    nav.append(ol)
    manifest = json.loads((NUMERICS / 'out/final_validation_manifest.json').read_text(encoding='utf-8'))
    content = f'''{START}
<section aria-labelledby="results">
<h2 id="results">最新数值分析总报告 · 2026-09-22</h2>
<div class="lead"><strong>已完成的验收：</strong>{manifest['regression_pass_count']} 项回归检查、{len(manifest['checks'])} 项产物检查；E2/E3 六组同网格时间自收敛共 30 次推进完成。固定区域连续极限接近二阶，Euler / RK4 / 梯形法的时间自收敛支持 1 / 4 / 2 阶行为。以下直接同步当前总报告，保留实测值与适用范围。</div>
<p><a href="Paper/dlw_semidiscrete/numerics/REPORT.md">总报告原文</a> · <a href="Paper/dlw_semidiscrete/numerics/README.md">复现说明</a> · <a href="Paper/dlw_semidiscrete/numerics/out/final_validation_manifest.json">验收与文件哈希</a> · <a href="lean_verification.html">Lean 独立核验页</a></p>
{nav}
{report}
</section>
{END}'''
    source = SOURCE.read_text(encoding='utf-8')
    if START in source:
        a, rest = source.split(START, 1)
        _, b = rest.split(END, 1)
        source = a + content + b
    else:
        source = source.replace('<h2 id="gsg">', content + '\n\n<h2 id="gsg">', 1)
    SOURCE.write_text(source, encoding='utf-8')
    print(f'Synchronized REPORT.md: {len(headings)} sections, {len(report.find_all("img"))} figures')


if __name__ == '__main__':
    main()
