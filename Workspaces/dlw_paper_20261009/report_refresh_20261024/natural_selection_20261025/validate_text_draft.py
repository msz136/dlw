from pathlib import Path
import csv,json,hashlib
from bs4 import BeautifulSoup
from PIL import Image
import fitz
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PATH=ROOT/'report/dlw_numerical_text_20261025.html'
text=PATH.read_text(encoding='utf8')
doc=BeautifulSoup(text,'html.parser')
ids=[e['id'] for e in doc.select('[id]')]
assert len(ids)==len(set(ids))
assert 'MATHSLOT' not in text and 'katex-error' not in text
assert not any(t in doc.get_text() for t in ['CSD0','full-potential'])
assert len(doc.find_all('table'))==3 and len(doc.find_all('figure'))==30
for e in doc.select('img[src],a[href],link[href]'):
    target=e.get('src') or e['href']
    if target.startswith('#'):assert target[1:] in ids
    else:assert (PATH.parent/target).exists(),target
methods=['Endpoint-SD','Centered-SD','FD'];cases=list('ABCD')+['Gaussian','Sinusoidal']
numbers=0;minima=0
for tid,fn,keys,mk in [('table-initial','table1_initial_derivative_errors.csv',['error_ut','error_vt'],'method'),
                      ('table-final','table2_final_field_errors.csv',['error_u','error_v'],'space')]:
    rows=list(csv.DictReader((HERE.parent/fn).open(encoding='utf-8-sig',newline='')))
    trs=doc.find(id=tid).select('tbody tr');assert len(trs)==6
    for tr,case in zip(trs,cases):
        pairs=[[float(next(r for r in rows if r['case']==case and r[mk]==method)[key]) for key in keys] for method in methods]
        best=[min(v[j] for v in pairs) for j in range(2)]
        for i,td in enumerate(tr.find_all('td')):
            x=pairs[i//2][i%2];assert float(td['data-value'])==x
            winner=f'{x:.3e}'==f'{best[i%2]:.3e}';assert bool(td.strong)==winner
            numbers+=1;minima+=winner
figures=[]
for f in doc.find_all('figure'):
    png=(PATH.parent/f.img['src']).resolve()
    pdf=(PATH.parent/f.a['href']).resolve()
    with Image.open(png) as im:
        assert min(im.size)>1500
        assert all(abs(v-300)<1 for v in im.info['dpi'])
    with fitz.open(pdf) as d:
        assert len(d)==1
        page=d[0];rect=page.rect
        for b in page.get_text('dict')['blocks']:
            if b['type']!=0:continue
            for line in b['lines']:
                for span in line['spans']:
                    x0,y0,x1,y1=span['bbox']
                    assert x0>=-1 and y0>=-1 and x1<=rect.width+1 and y1<=rect.height+1,(pdf.name,span['text'])
    figures.append(dict(id=f['id'],png=png.name,pdf=pdf.name,
        png_sha256=hashlib.sha256(png.read_bytes()).hexdigest(),
        pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest()))
pres=json.loads((HERE/'report_preservation.json').read_text(encoding='utf8'))
assert hashlib.sha256((ROOT/'dlw-paper.html').read_bytes()).hexdigest()==pres['paper_sha256']
data=json.loads((HERE/'figures/data/validation.json').read_text(encoding='utf8'))
assert data['max_table_rate_difference']==data['max_table_final_difference']==0
result=dict(status='passed',tables=3,table_values_checked=numbers,bold_minima_checked=minima,
    figures=30,initial_exact_figures=6,initial_derivative_figures=12,final_field_figures=12,
    png_dpi=300,pdfs_single_page=True,pdf_text_inside_page=True,
    formulas=len(doc.select('annotation[encoding="application/x-tex"]')),
    assets_and_links_valid=True,main_paper_unchanged=True,
    native_maxima_match_tables=True,section_rule='Native y=0 or 12-point local barycentric interpolation; degree15 and exact-sample checks recorded.',
    visual_review='All30figures contact sheet plus individual representative exact/section/error plots; comparison agent reviewed24.',
    artifacts=figures)
(HERE/'text_draft_validation.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k!='artifacts'},indent=2))
