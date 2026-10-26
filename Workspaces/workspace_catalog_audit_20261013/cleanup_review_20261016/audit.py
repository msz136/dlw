from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import os, json, csv, collections, subprocess, hashlib, re

ROOT=Path(r'C:\Users\msz\aca')
OUT=Path(__file__).resolve().parent
PLAN=json.loads((OUT.parent/'cleanup_20261016/move_plan.json').read_text(encoding='utf-8'))
TRASH=Path(PLAN['trash'])
moved={x['path']:x for x in PLAN['files_detail']}
issues=[]; errors=[]; texts=[]; coverage=[]
skip={'.git','Trash','_lean_shared','.lake','.research_deps','node_modules','vendor','__pycache__'}
for folder, dirs, files in os.walk(ROOT, onerror=lambda e:errors.append(str(e))):
 dirs[:]=[d for d in dirs if d not in skip and not (Path(folder)/d).is_symlink()]
 for name in files:
  p=Path(folder)/name
  if p.suffix.lower() in {'.html','.htm','.md','.py','.js','.ps1','.ipynb','.json','.css'} and p.stat().st_size<12_000_000:
   if p.is_relative_to(OUT.parent):continue
   texts.append(p)
for rel,row in moved.items():
 a=ROOT/rel;b=TRASH/rel
 coverage.append(dict(path=rel,original_exists=a.is_file(),trash_exists=b.is_file(),size_ok=b.is_file() and b.stat().st_size==row['bytes'],reason=row['reason']))
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.refs=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if v and k in {'src','href','poster','data'}:self.refs.append((k,v))
   if v and k=='srcset':self.refs.extend(('src',r.strip().split()[0]) for r in v.split(',') if r.strip())
links=[]; code_refs=[]
names=collections.defaultdict(list)
for rel in moved:names[Path(rel).name].append(rel)
for p in texts:
 s=p.read_text(encoding='utf-8',errors='replace');rel=p.relative_to(ROOT).as_posix()
 refs=[]
 if p.suffix.lower() in {'.html','.htm'}:
  parser=Parser()
  try:parser.feed(s);refs=parser.refs
  except Exception as e:errors.append(f'{rel}: {e}')
 elif p.suffix.lower()=='.md':refs=[('link',m) for m in re.findall(r'\]\(<?([^\s)>]+)>?\)',s)]
 for kind,raw in refs:
  try:u=urlsplit(raw)
  except ValueError:continue
  if u.scheme or u.netloc or not u.path:continue
  target=(p.parent/unquote(u.path)).resolve()
  if not target.is_relative_to(ROOT):continue
  t=target.relative_to(ROOT).as_posix()
  if not target.exists():links.append(dict(source=rel,target=t,kind=kind,caused_by_cleanup=t in moved,trash_exists=(TRASH/t).is_file()))
 if p.suffix.lower() in {'.py','.js','.ps1'}:
  for literal in set(re.findall(r'''["']([^"'\r\n]{3,240})["']''',s)):
   base=literal.replace('\\','/').split('/')[-1]
   if base in names and Path(base).suffix.lower() in {'.npz','.npy','.csv','.json','.png','.pdf','.h5','.html','.md'}:
    for t in names[base]:
     if Path(t).parts[:2]==Path(rel).parts[:2]:code_refs.append(dict(source=rel,literal=literal,target=t))
deleted=subprocess.check_output(['git','-c','core.quotepath=false','ls-files','--deleted','-z'],cwd=ROOT).decode('utf-8').split('\0')
unaccounted=[r for r in deleted if r and r not in moved]
prior=[]
with (OUT.parent/'file_purpose_20261016/files_by_purpose.csv').open(encoding='utf-8-sig',newline='') as f:
 for r in csv.DictReader(f):
  if r['路径'] in moved and ('保留' in r['保留判断'] and '不' not in r['保留判断']):prior.append(r)
hash_errors=[]
for rel,h in {**PLAN['protected_paper_hashes'],**PLAN['retained_source_hashes']}.items():
 p=ROOT/rel
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:hash_errors.append(rel)
result=dict(scanned_text_files=len(texts),moved_files=len(moved),coverage_failures=[x for x in coverage if not x['trash_exists'] or not x['size_ok']],originals_present=sum(x['original_exists'] for x in coverage),preserved_hash_failures=hash_errors,git_deleted_count=sum(bool(x) for x in deleted),git_deleted_not_in_plan=unaccounted,broken_links=links,code_literal_candidates=code_refs,prior_keep_moved_count=len(prior),prior_keep_by_category=dict(collections.Counter(r['用途'] for r in prior)),errors=errors)
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
for name,rows in [('move_coverage',coverage),('broken_links',links),('code_literal_candidates',code_refs),('prior_keep_moved',prior)]:
 if rows:
  with (OUT/(name+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={k:v for k,v in result.items() if k not in {'broken_links','code_literal_candidates','errors'}}
summary['cleanup_broken_links']=sum(x['caused_by_cleanup'] for x in links)
summary['cleanup_broken_images']=sum(x['caused_by_cleanup'] and x['kind'] in {'src','poster'} for x in links)
summary['broken_by_source']=dict(collections.Counter(x['source'] for x in links if x['caused_by_cleanup']))
summary['code_literal_candidates_count']=len(code_refs)
print(json.dumps(summary,ensure_ascii=False,indent=2))
