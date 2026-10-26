from pathlib import Path

p = Path(r'C:\Users\msz\aca\Workspaces\dlw_paper_20261009\frontmatter_v2_20261026\publish_frontmatter_v2.py')
s = p.read_text(encoding='utf-8')

old_tail = (
    "\"distribution\\u2014is the central motivation of the present work. The same questions arise for other integrable \"\n"
    "    \"semi-discrete systems [6\\u20139] and for discrete DLW-type reductions [11], while the moving meshes used here \"\n"
    "    \"follow the self-adaptive constructions built on semi-discrete conservation laws [9,12,13] and the general \"\n"
    "    \"theory of equidistribution [14]; the classical one-step integrators of Section 4 are taken from [10].\","
)
# the source uses literal em dashes, not escapes; normalise before searching
s_norm = s
old_tail = old_tail.replace('\\u2014', '\u2014').replace('\\u2013', '\u2013')
if old_tail not in s_norm:
    # try without the trailing comma / with actual line breaks
    print('tail not found verbatim; searching fragments')
    i = s.find('is the central motivation of the present work.')
    print('motivation index', i)
    j = s.find('taken from [10].', i)
    print('citation tail index', j)
    if i > 0 and j > i:
        block = s[i:j + len('taken from [10].')]
        print('BLOCK>>>')
        print(block)
        print('<<<')
    raise SystemExit(1)
