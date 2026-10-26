"""Independent read-only validation of the four main-paper heatmap repairs.

Only validation.json is written. No plot renderer, solver, reference evaluator,
publisher, or preceding project validation script is imported/run.
"""
from pathlib import Path
import ast, hashlib, json, re
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.colors import LogNorm
from bs4 import BeautifulSoup
from PIL import Image
from pypdf import PdfReader

HERE=Path(__file__).resolve().parent
ACTIVE=HERE.parent
ROOT=HERE.parents[3]
CASES=['A','D','Gaussian','Sinusoidal']
IDS=['figure-9','figure-13','figure-17','figure-21']
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def text(p):return p.read_bytes().decode('utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def raw_figure(s,ident):
 matches=list(re.finditer(r'<figure\b[^>]*\bid="'+re.escape(ident)+r'"[^>]*>.*?</figure>',s,re.S))
 assert len(matches)==1,('figure missing/duplicated',ident)
 return matches[0].group()
def exclude_figures(s):
 for ident in IDS:s=s.replace(raw_figure(s,ident),'HEATMAP_SLOT_'+ident)
 return s
def exclude_caption_and_image(s):
 s=re.sub(r'<figcaption\b[^>]*>.*?</figcaption>','CAPTION_SLOT',s,flags=re.S)
 return re.sub(r'(<img\b[^>]*\bsrc=")[^"]+("[^>]*>)',r'\1IMAGE_SLOT\2',s)
def raw_section(s,ident):
 start=re.search(r'<section\b[^>]*\bid="'+ident+r'"[^>]*>',s);assert start
 depth=1
 for token in re.finditer(r'</?section\b[^>]*>',s[start.end():]):
  depth+=-1 if token.group().startswith('</') else 1
  if depth==0:return s[start.start():start.end()+token.end()]
 raise AssertionError(('unclosed section',ident))

baseline=read(HERE/'before.json')
paper=ROOT/'dlw-paper.html'
before=text(HERE/'before_dlw-paper.html');after=text(paper)
old_source=text(HERE/'before_section-5.2.html')
new_source=text(ACTIVE/'section-5.2.html')
assert sha(HERE/'before_dlw-paper.html')==baseline['paper_sha256']
assert exclude_figures(before)==exclude_figures(after),'Main paper changed outside the four authorized figure blocks'
assert exclude_figures(old_source)==exclude_figures(new_source),'Section source changed outside the four authorized figure blocks'
if raw_section(before,'section-5.2').strip()==old_source.strip():
 assert raw_section(after,'section-5.2').strip()==new_source.strip(),'Section source does not match main paper'

protected=[]
for group in ['image_hashes','protected_hashes']:
 for path,wanted in baseline[group].items():
  p=Path(path);assert p.exists() and sha(p)==wanted,('protected file modified',path)
  protected.append(dict(group=group,path=path,sha256=wanted))

oldmanifest=read(ACTIVE/'figures/manifest.json')
newmanifest=read(HERE/'figures/manifest.json')
assert len(newmanifest)==4 and {e['case'] for e in newmanifest}==set(CASES)
old_entries={e['case']:e for e in oldmanifest if e['stage']=='final'}
new_entries={e['case']:e for e in newmanifest}
allowed_top={'color_scale','png','pdf','png_sha256','pdf_sha256','maps'}
allowed_map_additions={'zero_values','low_end_policy','lower_color_rgba','colorbar_threshold_label'}
methods={'Endpoint-SD':'endpoint','Centered-SD':'centered','FD':'fd'}
manifestchecks=[];figurechecks=[]
for case,ident in zip(CASES,IDS):
 old=old_entries[case];new=new_entries[case]
 assert set(new)==set(old),('unexpected top-level manifest keys',case,set(new)^set(old))
 for key in set(old)-allowed_top:assert old[key]==new[key],('manifest content changed',case,key)
 assert 'including zero' in new['color_scale'] and '<=' in new['color_scale']
 source=Path(new['source']);assert sha(source)==new['source_sha256']==old['source_sha256']
 data=np.load(source);x=data['x'];crop=(x>=old['heatmap_xlim'][0])&(x<=old['heatmap_xlim'][1])
 assert len(old['maps'])==len(new['maps'])==6
 for om,nm in zip(old['maps'],new['maps']):
  assert set(nm)-set(om)==allowed_map_additions
  for key in om:assert om[key]==nm[key],('map original key changed',case,key)
  z=abs(data[nm['source_key']])[:,crop]
  assert np.all(np.isfinite(z)) and np.all(z>=0)
  assert nm['zero_values']==int(np.sum(z==0))
  assert nm['below_color_minimum']==int(np.sum(z<nm['vmin']))
  assert nm['low_end_policy']=='clip to lowest viridis color, including zero'
  assert nm['colorbar_threshold_label']=='<= '+format(nm['vmin'],'.2e')
  low=list(matplotlib.colormaps['viridis'](0.0));assert nm['lower_color_rgba']==low
  norm=LogNorm(vmin=nm['vmin'],vmax=nm['vmax'],clip=True)
  mapped=norm(z);assert not np.any(np.ma.getmaskarray(mapped))
  assert np.all(np.asarray(mapped)[z<=nm['vmin']]==0)
  assert np.all(np.asarray(norm(np.array([0.,nm['vmin']/2,nm['vmin']])))==0)
  manifestchecks.append(dict(case=case,field=nm['field'],method=nm['method'],vmin=nm['vmin'],vmax=nm['vmax'],original_map_metadata_unchanged=True,zeros=nm['zero_values'],below_limit=nm['below_color_minimum'],zero_and_subthreshold_map_to_lowest_color=True,lower_label=nm['colorbar_threshold_label']))
 for kind in ['png','pdf']:
  p=HERE/'figures'/new[kind]
  assert p.name==f'spatial_{case}.{kind}' and p.exists() and sha(p)==new[kind+'_sha256']
  oldp=ACTIVE/'figures'/old[kind];assert oldp.exists() and sha(oldp)==old[kind+'_sha256']
  if kind=='png':
   with Image.open(p) as im:im.verify()
  else:assert len(PdfReader(p).pages)==1
 for olddoc,newdoc,name in [(before,after,'main paper'),(old_source,new_source,'section source')]:
  oldfig=raw_figure(olddoc,ident);newfig=raw_figure(newdoc,ident)
  assert exclude_caption_and_image(oldfig)==exclude_caption_and_image(newfig),('unauthorized figure attributes/layout changed',name,ident)
  od=BeautifulSoup(oldfig,'html.parser');nd=BeautifulSoup(newfig,'html.parser')
  assert len(nd.select('img'))==1 and len(nd.select('a[href$=".pdf"]'))==1
  assert nd.figure.attrs==od.figure.attrs
  expected=(HERE/'figures'/f'spatial_{case}.png').resolve()
  assert (ROOT/nd.img['src']).resolve()==expected
  pdf=nd.select_one('a[href$=".pdf"]')
  assert (ROOT/pdf['href']).resolve()==expected.with_suffix('.pdf')
  oldimg=dict(od.img.attrs);newimg=dict(nd.img.attrs);oldimg.pop('src');newimg.pop('src');assert oldimg==newimg
  cap=nd.figcaption.get_text(' ',strip=True)
  assert 'including zero' in cap and '≤' in cap and 'darkest color' in cap
  assert 'light gray' not in cap
  figurechecks.append(dict(document=name,figure=ident,case=case,new_image=str(expected),new_pdf=str(expected.with_suffix('.pdf')),only_resource_path_and_caption_changed=True))

# Preserve all error-table markup and independently check the requested counts.
bd=BeautifulSoup(before,'html.parser');ad=BeautifulSoup(after,'html.parser')
table_values=bold=0
for tid in ['table-initial','table-final']:
 assert str(bd.find(id=tid))==str(ad.find(id=tid)),('table markup changed',tid)
 for row in ad.find(id=tid).select('tbody tr'):
  cells=row.find_all('td');assert len(cells)==6
  values=[float(c['data-value']) for c in cells]
  for j,cell in enumerate(cells):
   assert bool(cell.strong)==(values[j]==min(values[j%2::2]))
   table_values+=1;bold+=int(bool(cell.strong))
assert table_values==48 and bold==16
assert len(ad.find_all('figure'))==len(bd.find_all('figure'))==24

# Renderer inspection checks the actual repair instruction without executing it.
renderer=HERE/'plot_figures.py';tree=ast.parse(text(renderer));calls=[]
for node in ast.walk(tree):
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='LogNorm':
  calls.append(node)
assert calls and all(any(k.arg=='clip' and isinstance(k.value,ast.Constant) and k.value.value is True for k in n.keywords) for n in calls)
assert 'set_under(cmap(0.0))' in text(renderer) and "r'$\\leq '" in text(renderer)
result=dict(status='passed',paper_before_sha256=baseline['paper_sha256'],paper_after_sha256=sha(paper),scope='Figures 9,13,17,21 and matching Section 5.2 figure blocks only',all_bytes_outside_authorized_figure_blocks_unchanged=True,table_values_unchanged=table_values,bold_minima_unchanged=bold,protected_file_hashes=protected,figure_block_checks=figurechecks,map_checks=manifestchecks,curves_source_arrays_native_coordinates_scales_and_original_metadata_unchanged=True,new_png_and_single_page_pdf_count=8,old_assets_unchanged=True,renderer_lognorm_clip_true=True)
(HERE/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(status=result['status'],table_values=table_values,bold_minima=bold,protected_hashes=len(protected),figure_blocks=len(figurechecks),map_checks=len(manifestchecks),new_assets=8),ensure_ascii=False,indent=2))
