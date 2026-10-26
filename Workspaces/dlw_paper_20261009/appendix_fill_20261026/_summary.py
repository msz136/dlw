from bs4 import BeautifulSoup
import re
from pathlib import Path

s = BeautifulSoup(Path(r'C:\Users\msz\aca\dlw-paper.html').read_text(encoding='utf-8'), 'html.parser')
print('section          words  fig  tab  eq')
for sec in s.find_all('section'):
    sid = sec.get('id') or '?'
    if sec.find(['h2', 'h3']) is None:
        continue
    w = len(re.sub(r'\s+', ' ', sec.get_text(' ')).split())
    print(f'{sid:16s} {w:6d} {len(sec.find_all("figure")):4d} {len(sec.find_all("table")):4d} {len(sec.select("div.equation")):3d}')
