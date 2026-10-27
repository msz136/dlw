from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
import re, shutil,json
R=Path('C:/Users/msz/aca');H=Path(__file__).parent;P=R/'dlw-paper.html'
raw=P.read_bytes();s=raw.decode('utf-8');assert 'id="compact-print-layout"' not in s
(H/'before.html').write_bytes(raw)
shutil.copy2('C:/Users/msz/Desktop/paper/dlw/dlw-paper-1027.pdf',H/'before.pdf')
out=H/'figures';out.mkdir(exist_ok=True)
for n in range(5,9):
 pat=r'<figure\b[^>]*id="figure-'+str(n)+r'"[^>]*>.*?</figure>'
 m=re.search(pat,s,re.S);assert m
 fragment=BeautifulSoup(m[0],'html.parser');fig=fragment.figure;img=fig.img
 im=Image.open(R/img['src']).convert('RGB');w,h=im.size
 # Split only through the whitespace between section plots and heatmaps.
 import numpy as np
 arr=np.asarray(im);ink=np.any(arr<235,axis=2).sum(axis=1)
 lo,hi=int(h*.49),int(h*.54);candidates=[y for y in range(lo,hi) if ink[y]==0]
 assert candidates
 cut=min(candidates,key=lambda y:abs(y-h*.515))
 paths=[]
 for label,box in [('sections',(0,0,w,cut)),('heatmaps',(0,cut,w,h))]:
  path=out/f'figure_{n}_{label}.png';im.crop(box).save(path);paths.append(path.relative_to(R).as_posix())
 img['class']=img.get('class',[])+['screen-composite']
 first=fragment.new_tag('div',attrs={'class':'print-figure-part'})
 first.append(fragment.new_tag('img',src=paths[0],alt=f'Figure {n}, cross-sections and section errors'))
 second=fragment.new_tag('div',attrs={'class':'print-figure-part'})
 second.append(fragment.new_tag('img',src=paths[1],alt=f'Figure {n}, two-dimensional error maps'))
 caption=fig.figcaption
 # Keep one visible caption in each medium, attached to the lower print panel.
 printcap=BeautifulSoup(str(caption),'html.parser').figcaption
 second.append(printcap);caption['class']=caption.get('class',[])+['screen-composite']
 fig.insert(1,first);fig.insert(2,second)
 s=s[:m.start()]+str(fig)+s[m.end():]
css='''<style id="compact-print-layout">
.print-figure-part{display:none}
@media print{
 @page{size:A4;margin:10mm}
 .numerical-section figure{margin:10pt 0 12pt}
 .numerical-section figcaption{font-size:9pt;line-height:1.35;margin-top:6pt}
 #section-5\\.1 figure img{max-height:95mm;width:auto;max-width:100%;margin:auto}
 #figure-5,#figure-6,#figure-7,#figure-8{break-inside:auto}
 .screen-composite{display:none!important}
 .print-figure-part{display:block;break-inside:avoid;margin:0 0 8pt}
 .numerical-section .print-figure-part img{width:100%;height:auto}
 .numerical-section .table-wrap{margin:16pt 0}
 p{orphans:3;widows:3}
}
</style>'''
s=s.replace('</head>',css+'</head>',1);P.write_bytes(s.encode('utf-8'))
(H/'layout_notes.json').write_text(json.dumps({'split_figures':[5,6,7,8],'initial_figures_max_height_mm':95,'body_font_unchanged':True,'split_in_white_gutter':True},indent=2),encoding='utf-8')
