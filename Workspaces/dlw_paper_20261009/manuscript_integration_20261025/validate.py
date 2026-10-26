"""Check the integrated draft against the selected data and preserved sections."""
from pathlib import Path
from bs4 import BeautifulSoup
import csv, hashlib, json, re, subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PAPER=ROOT/'dlw-paper.html'
text=PAPER.read_text(encoding='utf-8')
before=(HERE/'before_dlw-paper.html').read_text(encoding='utf-8')
doc=BeautifulSoup(text,'html.parser')
draft=BeautifulSoup((ROOT/'report/dlw_numerical_text_20261025.html').read_text(encoding='utf-8'),'html.parser')
selected=ROOT/'Workspaces/dlw_paper_20261009/report_refresh_20261024/natural_selection_20261025'

def raw_section(s, identity):
    first=re.search(r'<section\b[^>]*\bid="'+re.escape(identity)+r'"[^>]*>',s)
    assert first,identity
    depth=1
    for token in re.finditer(r'</?section\b[^>]*>',s[first.end():]):
        depth+=-1 if token.group().startswith('</') else 1
        if depth==0:return s[first.start():first.end()+token.end()]
    raise ValueError(identity)

protected=['section-1','section-2','section-3.1','section-3.2','section-4.3','section-4.4','section-5.4','section-5.5','section-6','appendix-A','appendix-B','appendix-C','appendix-D','references']
for identity in protected:
    assert raw_section(text,identity)==raw_section(before,identity),identity

ids=[e['id'] for e in doc.select('[id]')]
assert len(ids)==len(set(ids)), 'duplicate id'
for a in doc.select('[href^="#"]'):
    assert a['href'][1:] in ids,a['href']
for e in doc.select('img[src],a[href],link[href]'):
    target=e.get('src') or e.get('href')
    if target.startswith(('#','http:','https:','mailto:','data:')):continue
    assert (ROOT/target.split('#')[0]).exists(),target

assert len(doc.find_all('figure'))==30
assert len(doc.find_all('table'))==3
for figure in draft.find_all('figure'):
    current=doc.find(id=figure['id'])
    assert current
    assert current.figcaption.get_text(' ',strip=True)==figure.figcaption.get_text(' ',strip=True)
    old=(ROOT/'report'/figure.img['src']).resolve()
    new=(ROOT/current.img['src']).resolve()
    assert old==new

for identity in ['table-parameters','table-initial','table-final']:
    assert str(doc.find(id=identity))==str(draft.find(id=identity)),identity
methods=['Endpoint-SD','Centered-SD','FD']
cases=list('ABCD')+['Gaussian','Sinusoidal']
numbers=minima=0
for tid,fn,keys,mk in [('table-initial','table1_initial_derivative_errors.csv',['error_ut','error_vt'],'method'),('table-final','table2_final_field_errors.csv',['error_u','error_v'],'space')]:
    rows=list(csv.DictReader((selected.parent/fn).open(encoding='utf-8-sig',newline='')))
    trs=doc.find(id=tid).select('tbody tr')
    assert len(trs)==6
    for tr,case in zip(trs,cases):
        pairs=[[float(next(r for r in rows if r['case']==case and r[mk]==method)[key]) for key in keys] for method in methods]
        best=[min(v[j] for v in pairs) for j in range(2)]
        for i,td in enumerate(tr.find_all('td')):
            x=pairs[i//2][i%2]
            assert float(td['data-value'])==x
            winner=f'{x:.3e}'==f'{best[i%2]:.3e}'
            assert bool(td.strong)==winner
            numbers+=1;minima+=winner

active=' '.join(doc.find(id=s).get_text(' ',strip=True) for s in ['section-3.3','section-3.4','section-4.1','section-4.2','section-5.1','section-5.2','section-5.3'])
for obsolete in ['full-potential','CSD0','damped fixed-point','identical to the Endpoint-SD first equation','shared first equation','selected inverse branch']:
    assert obsolete not in active,obsolete
time=doc.find(id='section-4.2')
for method in ['forward Euler','RK4','Crank–Nicolson']:
    assert method in time.get_text(),method
assert not doc.find(id='section-5.3').find('table')
assert not re.search(r'(?:MATHSLOT|INTEGRATIONMATH)\d+END|katex-error',text)
tex=[e.get_text() for e in doc.select('annotation[encoding="application/x-tex"]')]
js="const fs=require('fs'),k=require(process.argv[1]);const a=JSON.parse(fs.readFileSync(0,'utf8'));a.forEach(t=>k.renderToString(t,{displayMode:true,throwOnError:true,strict:'error'}));process.stdout.write(String(a.length));"
r=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(tex),text=True,encoding='utf-8',capture_output=True,check=True)
result=dict(status='passed',paper_sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest(),protected_sections_unchanged=protected,table_values_checked=numbers,bold_minima_checked=minima,figures=30,figure_captions_and_assets_match_draft=True,formulas_rendered=int(r.stdout),links_valid=True,unique_ids=True,old_time_comparison_archived=True,current_time_comparison='RK4 only; Euler/CN results pending',moving_mesh_unchanged=True)
(HERE/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
