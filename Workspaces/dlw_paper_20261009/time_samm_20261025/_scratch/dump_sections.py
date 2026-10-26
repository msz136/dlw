"""Dump readable text of manuscript sections for editing (scratch tool)."""
import re, sys
from pathlib import Path
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[3] / 'dlw-paper.html'
soup = BeautifulSoup(PAPER.read_text(encoding='utf-8'), 'html.parser')

def tex_of(node):
    ann = node.find('annotation', attrs={'encoding': 'application/x-tex'})
    return ann.get_text() if ann else None

def flatten(node, out):
    for child in node.children:
        name = getattr(child, 'name', None)
        if name is None:
            out.append(str(child))
            continue
        cls = child.get('class') or []
        if name == 'span' and 'katex' in cls:
            tex = tex_of(child)
            display = 'katex-display' in ' '.join(cls)
            if tex is not None:
                out.append(('\n$$' + tex + '$$\n') if display else ('$' + tex + '$'))
            else:
                flatten(child, out)
        elif name == 'annotation':
            continue
        elif name == 'img':
            out.append('[IMG src=' + child.get('src', '') + ']')
        elif name == 'table':
            out.append('\n[TABLE]\n')
            for tr in child.find_all('tr'):
                cells = [c.get_text(' ', strip=True) for c in tr.find_all(['th', 'td'])]
                out.append(' | '.join(cells) + '\n')
            out.append('[/TABLE]\n')
        elif name == 'section':
            out.append('\n[SECTION ' + str(child.get('id')) + ']\n')
            flatten(child, out)
            out.append('\n[/SECTION ' + str(child.get('id')) + ']\n')
        else:
            if name in ('p', 'h2', 'h3', 'h4', 'h5', 'li', 'figcaption', 'caption', 'div', 'figure', 'details', 'summary'):
                out.append('\n')
                flatten(child, out)
                out.append('\n')
            else:
                flatten(child, out)

wanted = sys.argv[1:]
for ident in wanted:
    sec = soup.find(id=ident)
    print('=' * 30, ident, '=' * 30)
    if sec is None:
        print('MISSING')
        continue
    out = []
    flatten(sec, out)
    text = ''.join(out)
    text = re.sub(r'\n{3,}', '\n\n', text)
    print(text.strip())
