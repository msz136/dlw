from pathlib import Path

p = Path(r'C:\Users\msz\aca\Workspaces\dlw_paper_20261009\frontmatter_v2_20261026\publish_frontmatter_v2.py')
s = p.read_text(encoding='utf-8')
n1 = s.count('[1,3,4]')
s = s.replace('[1,3,4]', '[1\u20134]')
p.write_text(s, encoding='utf-8')
print('replaced', n1, 'occurrences; remaining', s.count('[1,3,4]'))
