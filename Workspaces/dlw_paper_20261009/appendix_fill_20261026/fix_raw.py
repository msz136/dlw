from pathlib import Path

p = Path(r'C:\Users\msz\aca\Workspaces\dlw_paper_20261009\appendix_fill_20261026\publish_appendices.py')
s = p.read_text(encoding='utf-8')
n = s.count("{m('")
s = s.replace("{m('", "{m(r'")
p.write_text(s, encoding='utf-8')
print('converted to raw strings:', n)
print('remaining non-raw m(:', s.count("{m('"))
