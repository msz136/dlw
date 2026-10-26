"""Standalone render pages for checking the rewritten Section 5."""
from pathlib import Path
import re, sys

HERE = Path(__file__).resolve().parent
t = (HERE.parents[2] / 'dlw-paper.html').read_text(encoding='utf-8')
styles = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', t, re.S))


def span(ident):
    m = re.search(r'<section\b[^>]*\bid="' + re.escape(ident) + r'"[^>]*>', t)
    depth = 1
    for tok in re.finditer(r'</?section\b[^>]*>', t[m.end():]):
        depth += -1 if tok.group().startswith('</') else 1
        if depth == 0:
            return t[m.start():m.end() + tok.end()]
    raise KeyError(ident)


head = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<base href="file:///C:/Users/msz/aca/">'
        '<link rel="stylesheet" href="file:///C:/Users/msz/aca/Workspaces/gsg_project/'
        'dlw_report/_assets/package/dist/katex.min.css">'
        f'<style>{styles}</style>'
        '<style>body{max-width:820px;margin:28px auto;padding:0 24px;'
        'font-family:Georgia,serif;font-size:17px;line-height:1.65}</style></head><body>')
name = sys.argv[1] if len(sys.argv) > 1 else 'render_51'
parts = sys.argv[2:]
(HERE / f'{name}.html').write_text(head + ''.join(span(p) for p in parts) + '</body></html>', encoding='utf-8')
print('ok', name)
