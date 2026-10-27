from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
import numpy as np,re,shutil,json
R=Path('C:/Users/msz/aca');H=Path(__file__).parent;P=R/'dlw-paper.html'
raw=P.read_bytes();s=raw.decode('utf-8');assert 'id="print-row-pagination"' not in s
(H/'before_rows.html').write_bytes(raw);shutil.copy2(H/'optimized.pdf',H/'before_rows.pdf')
out=H/'row_figures';out.mkdir(exist_ok=True);records=[]
figs=BeautifulSoup(s,'html.parser').find_all('figure')
for n in list(range(1,11))+[13,14]:
 fid=figs[n-1]['id'];pat=r'<figure\b[^>]*id="'+fid+r'"[^>]*>.*?</figure>'
 m=re.search(pat,s,re.S);frag=BeautifulSoup(m[0],'html.parser');fig=frag.figure
 for old in fig.select('.print-figure-part'):old.decompose()
 img=fig.img;caption=fig.figcaption
 img['class']=['screen-composite'];caption['class']=['screen-composite'];fig['class']=fig.get('class',[])+['row-paginated-figure']
 im=Image.open(R/img['src']).convert('RGB');w,h=im.size;a=np.asarray(im);white=np.all(a>245,axis=(1,2))
 targets=[.295,.53,.767] if 5<=n<=8 else [.53]
 cuts=[0]
 for target in targets:
  ys=[i for i in range(int((target-.03)*h),int((target+.03)*h)) if white[i]]
  assert ys,(n,target)
  cuts.append(min(ys,key=lambda y:abs(y-target*h)))
 cuts.append(h)
 maxheight=95 if n<=4 else 85 if n>=13 else 100
 width=min(190,maxheight*w/h) if not 5<=n<=8 else 190
 for j,(lo,hi) in enumerate(zip(cuts,cuts[1:])):
  # Remove only blank outer rows; retain a small white breathing margin.
  used=np.flatnonzero(~white[lo:hi]);assert len(used)
  y0=max(lo,lo+int(used[0])-10);y1=min(hi,lo+int(used[-1])+11)
  path=out/f'figure_{n}_row_{j+1}.png';im.crop((0,y0,w,y1)).save(path)
  block=frag.new_tag('div',attrs={'class':'print-figure-part print-row'})
  pic=frag.new_tag('img',src=path.relative_to(R).as_posix(),alt=f'Figure {n}, panel row {j+1}')
  pic['style']=f'width:{width:.4f}mm!important;max-height:none!important;height:auto!important;max-width:100%;margin:auto'
  block.append(pic)
  if j==len(cuts)-2:
   cap=BeautifulSoup(str(caption),'html.parser').figcaption;del cap['class'];block.append(cap)
  fig.append(block)
 records.append(dict(figure=n,cuts=cuts,width_mm=width))
 s=s[:m.start()]+str(fig)+s[m.end():]
css='''<style id="print-row-pagination">
@media print{
 .numerical-section figure.row-paginated-figure{break-inside:auto!important;margin:8pt 0!important}
 .print-row{break-inside:avoid;margin:0 0 7pt}
}
</style>'''
s=s.replace('</head>',css+'</head>',1);P.write_bytes(s.encode('utf-8'))
(H/'row_splits.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
