from pathlib import Path
import sys,json,re,shutil
import pymupdf
from bs4 import BeautifulSoup
R=Path('C:/Users/msz/aca');H=Path(__file__).parent
sys.path.insert(0,str(R/'Workspaces/paper_latex_20261027'))
from convert import Converter
path=R/'dlw-paper.html';backup=H/'before.html'
assert not backup.exists();shutil.copy2(path,backup)
tex=(R/'pdf/dlw/main.tex').read_text(encoding='utf8')
shutil.copy2(R/'pdf/dlw/main.tex',H/'tex_sync_source.tex')
s=BeautifulSoup(path.read_text(encoding='utf8'),'html.parser');c=Converter('dlw-paper.html','dlw')
ed=json.loads((R/'Workspaces/paper_latex_20261027/figure_review/narrative_edits.json').read_text(encoding='utf8'))
for p in s.find_all('p'):
 if p.get_text().startswith('Figures 9 and 10 plot the resulting error histories'):
  p.clear();p.string=ed['revised_time_u'];s.find(id='figure-9').insert_before(p.extract())
 elif p.get_text().startswith('Comparing the three curves within each panel'):
  p.clear();p.string=ed['revised_time_v'];s.find(id='figure-10').insert_before(p.extract())
for f in s.find_all('figure'):
 for cap in f.find_all('figcaption'):
  for txt in list(cap.find_all(string=True)):
   old='Equal-length dashes are staggered to keep all three colors visible where curves overlap.'
   if old in txt:txt.replace_with(txt.replace(old,'Where curves overlap, their colors alternate; separated curves are solid. The Endpoint-SD response in panel (d) is slightly larger than the other two responses.'))
out=H/'tex_figures';out.mkdir(exist_ok=True)
moved=[]
for i,f in enumerate(s.find_all('figure'),1):
 pdf=R/f'pdf/dlw/images/figure-{i:02}.pdf';doc=pymupdf.open(pdf)
 dst=out/f'figure-{i:02}.png';doc[0].get_pixmap(matrix=pymupdf.Matrix(3,3)).save(dst)
 f.find('img')['src']=dst.relative_to(R).as_posix()
 anchor=f.find('a')
 if anchor:anchor['href']=pdf.relative_to(R).as_posix()
 pos=tex.find(f'images/figure-{i:02}.pdf')
 # Move after-image descriptions before their image, matching TeX narrative.
 for p in list(f.find_next_siblings()):
  if p.name in ('figure','h2','h3','h4','table'):break
  if p.name!='p':continue
  val=c.children(p).strip();at=tex.find(val)
  if val and at>=0 and at<pos:
   f.insert_before(p.extract());moved.append(i)
path.write_text(str(s),encoding='utf8')
(H/'tex_sync.json').write_text(json.dumps(dict(moved_paragraphs=moved,replaced_figures=14,revised_paragraphs=2),indent=2))
print('TeX text and figures synchronized')
