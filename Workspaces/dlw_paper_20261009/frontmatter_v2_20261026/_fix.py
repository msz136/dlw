from pathlib import Path
import hashlib

b = Path(r'C:\Users\msz\aca\Workspaces\dlw_paper_20261009\frontmatter_v2_20261026\before\dlw-paper.html')
print('baseline sha256:', hashlib.sha256(b.read_bytes()).hexdigest())

p = Path(r'C:\Users\msz\aca\Workspaces\dlw_paper_20261009\frontmatter_v2_20261026\publish_frontmatter_v2.py')
s = p.read_text(encoding='utf-8')
old = "out.append(part.replace('—', '&mdash;').replace('&', '&amp;'))"
new = "out.append(part.replace('&', '&amp;').replace('—', '&mdash;'))"
assert s.count(old) == 1, s.count(old)
p.write_text(s.replace(old, new), encoding='utf-8')
print('escape order fixed')
