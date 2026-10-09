from pathlib import Path
import re, json, hashlib
from bs4 import BeautifulSoup

here=Path(__file__).resolve().parent
old=(here/'before_narrative_revision/manuscript.md').read_text(encoding='utf-8')
new=(here/'manuscript.md').read_text(encoding='utf-8')
assert re.findall(r'\$\$[\s\S]*?\$\$',old)==re.findall(r'\$\$[\s\S]*?\$\$',new)
assert re.findall(r'\\tag\{(\d+)\}',new)==[str(i) for i in range(1,75)]
assert not any(ord(c)<32 and c not in '\n\r\t' for c in new)
ot=BeautifulSoup(old,'html.parser').select('table.comparison')
nt=BeautifulSoup(new,'html.parser').select('table.comparison')
count=0
for i,j in [(0,0),(1,2),(2,3)]:
 a=[td.get_text(strip=True) for td in ot[i].select('tbody td')]
 b=[td.get_text(strip=True) for td in nt[j].select('tbody td')]
 assert a==b
 count+=len(a)
assert count==108
oldsrc=re.findall(r'<img src="([^"]+)"',old)
newsrc=re.findall(r'<img src="([^"]+)"',new)
assert sorted(oldsrc)==sorted(newsrc) and len(newsrc)==6
ratio=json.loads((here/'results_reorganization.json').read_text(encoding='utf-8'))
assert all(0<v<1 for v in ratio['ratios_from_saved_mesh_table'].values())
result={'numbered_equations':74,'all_displayed_equations_unchanged':True,
 'original_numeric_cells_preserved':count,'original_images_retained':6,
 'ratios_computed_from_saved_table':18,'experiments_rerun':False,
 'source_sha256':hashlib.sha256(new.encode()).hexdigest()}
(here/'narrative_content_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
