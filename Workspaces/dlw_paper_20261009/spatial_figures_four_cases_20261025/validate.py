from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image,ImageOps,ImageDraw
import numpy as np
import fitz,csv,json,re,hashlib,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
PAPER=ROOT/'dlw-paper.html';text=PAPER.read_text(encoding='utf-8')
before=(HERE/'before_dlw-paper.html').read_text(encoding='utf-8')
doc=BeautifulSoup(text,'html.parser')
names=['One-soliton','Two-soliton','Gaussian','Sinusoidal'];cases=['A','C','Gaussian','Sinusoidal']
def span(s,identity):
    f=re.search(r'<section\b[^>]*\bid="'+re.escape(identity)+r'"[^>]*>',s);assert f
    depth=1
    for t in re.finditer(r'</?section\b[^>]*>',s[f.end():]):
        depth+=-1 if t.group().startswith('</') else 1
        if depth==0:return s[f.start():f.end()+t.end()]
protected=['section-1','section-2','section-3','section-4','section-5.3','section-5.4','section-5.5','section-6','appendix-A','appendix-B','appendix-C','appendix-D','references']
for s in protected:assert span(text,s)==span(before,s),s
ids=[e['id'] for e in doc.select('[id]')];assert len(ids)==len(set(ids))
for e in doc.select('img[src],a[href],link[href]'):
    path=e.get('src') or e.get('href')
    if path.startswith('#'):assert path[1:] in ids,path
    elif not path.startswith(('http:','https:','mailto:','data:')):assert (ROOT/path.split('#')[0]).exists(),path
assert len(doc.select('figure'))==12
assert not doc.select('details')
assert [tr.th.get_text() for tr in doc.find(id='table-parameters').select('tbody tr')]==names[:2]
report=ROOT/'Workspaces/dlw_paper_20261009/report_refresh_20261024'
count=bestcount=0
for tid,fn,keys,mk in [('table-initial','table1_initial_derivative_errors.csv',['error_ut','error_vt'],'method'),('table-final','table2_final_field_errors.csv',['error_u','error_v'],'space')]:
    source=list(csv.DictReader((report/fn).open(encoding='utf-8-sig',newline='')))
    assert len(source)==12
    trs=doc.find(id=tid).select('tbody tr');assert [tr.th.get_text() for tr in trs]==names
    for tr,case in zip(trs,cases):
        pairs=[[float(next(r for r in source if r['case']==case and r[mk]==method)[key]) for key in keys] for method in ['Endpoint-SD','Centered-SD','FD']]
        mins=[min(x[j] for x in pairs) for j in range(2)]
        for i,td in enumerate(tr.find_all('td')):
            v=pairs[i//2][i%2];assert float(td['data-value'])==v
            win=f'{v:.3e}'==f'{mins[i%2]:.3e}';assert bool(td.strong)==win
            count+=1;bestcount+=win
visible=' '.join(doc.find(id=s).get_text(' ',strip=True) for s in ['section-5.1','section-5.2'])
for t in ['Case A','Case B','Case C','Case D','six cases','six tests','four soliton','two periods','full-potential']:
    assert t not in visible,t
assert 'FOURCASEMATH' not in text and 'katex-error' not in text
formulas=[e.get_text() for e in doc.select('annotation[encoding="application/x-tex"]')]
js="const fs=require('fs'),k=require(process.argv[1]);const a=JSON.parse(fs.readFileSync(0,'utf8'));a.forEach(t=>k.renderToString(t,{displayMode:true,throwOnError:true,strict:'error'}));process.stdout.write(String(a.length));"
r=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(formulas),text=True,encoding='utf-8',capture_output=True,check=True)
manifest=json.loads((HERE/'figures/manifest.json').read_text(encoding='utf-8'));assert len(manifest)==12
for item in manifest:
    png=HERE/'figures'/item['png'];pdf=HERE/'figures'/item['pdf']
    assert hashlib.sha256(png.read_bytes()).hexdigest()==item['png_sha256']
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==item['pdf_sha256']
    with Image.open(png) as im:assert all(abs(x-300)<1 for x in im.info['dpi'])
    with fitz.open(pdf) as d:
        assert len(d)==1
        page=d[0]
        for b in page.get_text('dict')['blocks']:
            if b['type']!=0:continue
            for line in b['lines']:
                for s in line['spans']:
                    x0,y0,x1,y1=s['bbox'];assert min(x0,y0)>=-1 and x1<=page.rect.width+1 and y1<=page.rect.height+1,(item['pdf'],s['text'])
    if item['stage']!='exact':
        d=np.load(item['source']);assert hashlib.sha256(Path(item['source']).read_bytes()).hexdigest()==item['source_sha256']
        for curve in item['curves']:
            assert not curve['marker'];assert curve['all_x_points']==len(d['x'])
            assert curve['maximum']==float(abs(d[curve['source_key']]).max())
        for q in ['u','v']:
            maps=[m for m in item['maps'] if m['field']==q]
            assert len(set((m['vmin'],m['vmax']) for m in maps))==1

# A contact sheet records the complete layout review; individual plots are also inspected.
canvas=Image.new('RGB',(1500,4*560),'white');draw=ImageDraw.Draw(canvas)
for i,c in enumerate(cases):
    for j,stage in enumerate(['exact','rate','final']):
        item=next(e for e in manifest if e['case']==c and e['stage']==stage)
        with Image.open(HERE/'figures'/item['png']) as im:
            thumb=ImageOps.contain(im.convert('RGB'),(480,515))
            canvas.paste(thumb,(j*500+(500-thumb.width)//2,i*560+30))
        draw.text((j*500+12,i*560+10),names[i]+' / '+stage,fill='black')
canvas.save(HERE/'figures/contact_sheet.png')
out=dict(status='passed',cases=cases,display_names=names,figures=12,all_heatmaps_in_body=True,protected_sections_unchanged=protected,table_values=count,bold_minima=bestcount,formulas_rendered=int(r.stdout),links_and_ids_valid=True,pdfs_single_page_and_text_inside=True,png_dpi=300,all_sampled_errors_connected=True,common_log_colors_per_field=True,source_arrays_unchanged=True,paper_sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest())
(HERE/'validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
