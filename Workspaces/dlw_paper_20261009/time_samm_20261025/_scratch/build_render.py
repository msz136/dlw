"""Build standalone render pages for a visual check of the new sections."""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
t = (HERE.parents[3] / 'dlw-paper.html').read_text(encoding='utf-8')
styles = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', t, re.S))


def span(ident):
    m = re.search(r'<section\b[^>]*\bid="' + re.escape(ident) + r'"[^>]*>', t)
    depth = 1
    for tok in re.finditer(r'</?section\b[^>]*>', t[m.end():]):
        depth += -1 if tok.group().startswith('</') else 1
        if depth == 0:
            return t[m.start():m.end() + tok.end()]
    raise KeyError(ident)


parts = [span('section-4.3'), span('section-5.3'), span('section-5.4')]
head = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<base href="file:///C:/Users/msz/aca/">'
        '<link rel="stylesheet" href="file:///C:/Users/msz/aca/Workspaces/gsg_project/'
        'dlw_report/_assets/package/dist/katex.min.css">'
        f'<style>{styles}</style>'
        '<style>body{max-width:820px;margin:28px auto;padding:0 24px;'
        'font-family:Georgia,serif;font-size:17px;line-height:1.65}</style></head><body>')
for name, chunk in (('render_43', [parts[0]]), ('render_53', [parts[1]]), ('render_54', [parts[2]])):
    (HERE / f'{name}.html').write_text(head + ''.join(chunk) + '</body></html>', encoding='utf-8')
print('written')
