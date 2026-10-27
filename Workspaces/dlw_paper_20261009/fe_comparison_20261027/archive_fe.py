from pathlib import Path
import re,json,subprocess,copy,hashlib
import numpy as np
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import unquote,urlparse
R=Path('C:/Users/msz/aca');H=Path(__file__).parent;path=R/'dlw-paper.html'
archive=R/'report/dlw-paper-add-fem.html'
assert not archive.exists()
original=path.read_text(encoding='utf8')
(H/'before_fe_withdrawal.html').write_text(original,encoding='utf8')
a=BeautifulSoup(original,'html.parser')
for tag in a.find_all(['img','a','link','script']):
 key='src' if tag.name in ['img','script'] else 'href';v=tag.get(key,'')
 if v and not v.startswith(('#','/','data:')) and not urlparse(v).scheme:tag[key]='../'+v
archive.write_text(str(a),encoding='utf8')
# Reapply only the already-authorized TeX synchronization to the pre-FE snapshot.
code=(H/'sync_tex.py').read_text(encoding='utf8')
code=code.replace("assert not backup.exists();shutil.copy2(path,backup)",'assert backup.exists()')
code=code.replace("shutil.copy2(R/'pdf/dlw/main.tex',H/'tex_sync_source.tex')",'')
code=code.replace("s=BeautifulSoup(path.read_text(encoding='utf8'),'html.parser')","s=BeautifulSoup(backup.read_text(encoding='utf8'),'html.parser')")
exec(compile(code,str(H/'sync_tex.py'),'exec'))
s=BeautifulSoup(path.read_text(encoding='utf8'),'html.parser')
def frag(text):return BeautifulSoup(text,'html.parser')
pub=(H/'publish.py').read_text(encoding='utf8')
exec(pub[pub.index('nodes=[];jobs=[]'):pub.index('# Regenerate print panel rows')])
for i,f in enumerate(s.find_all('figure'),1):
 for link in f.find_all('a'):
  if link.get('href','').endswith('.pdf'):link['href']=f'pdf/dlw/images/figure-{i:02}.pdf'
# Separate print assets so the archived four-method edition remains intact.
refresh=pub[pub.index("rows=H/'print_rows'"):pub.index("(H/'publication.json')")]
refresh=refresh.replace("rows=H/'print_rows'","rows=H/'three_method_print_rows'")
exec(refresh)
assert s.find(id='fe-formulation') is None
assert len(s.find_all('figure'))==14 and len(s.find_all('table'))==8
for id in ['table-initial','table-final']:
 assert all(len(tr.find_all('td'))==6 for tr in s.find(id=id).tbody.find_all('tr'))
 assert all(len(tr.find_all('td'))==8 for tr in a.find(id=id).tbody.find_all('tr'))
for doc,base in [(s,R),(a,R/'report')]:
 for img in doc.find_all('img'):assert (base/unquote(img['src'])).exists(),img['src']
assert a.find(id='fe-formulation') is not None
(H/'withdrawal_validation.json').write_text(json.dumps(dict(main_methods=3,archived_methods=4,figures=14,tables=8,tex_sync_preserved=True,archive=str(archive),archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),main_sha256=hashlib.sha256(path.read_bytes()).hexdigest()),indent=2),encoding='utf8')
print('Archived complete FE edition; restored three-method main paper with TeX synchronization.')
