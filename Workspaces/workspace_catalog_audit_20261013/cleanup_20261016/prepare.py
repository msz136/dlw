"""Prepare an auditable move-only cleanup; never delete originals."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import csv, json, re, os, collections, hashlib

ROOT=Path(r'C:\Users\msz\aca')
OUT=Path(__file__).resolve().parent
TRASH=ROOT/'Trash/cleanup_20261016'
OLD=OUT.parent/'file_purpose_20261016'
DRAFT=ROOT/'report/dlw_paper_draft.html'
keep={DRAFT.resolve()}; pending=[DRAFT]; broken=[]
class Refs(HTMLParser):
 def __init__(self):super().__init__();self.refs=[]
 def handle_starttag(self,tag,attrs):
  for key,value in attrs:
   if key in {'src','href','poster','data'} and value:self.refs.append(value)
   if key=='srcset':self.refs.extend(v.strip().split()[0] for v in value.split(',') if v.strip())
while pending:
 file=pending.pop();text=file.read_text(encoding='utf-8',errors='replace');refs=[]
 if file.suffix.lower() in {'.html','.htm'}:
  parser=Refs();parser.feed(text);refs+=parser.refs
 refs+=re.findall(r'url\(\s*[\"\']?([^\)\"\']+)',text)
 for ref in refs:
  u=urlsplit(ref.strip())
  if u.scheme or u.netloc or not u.path:continue
  target=(file.parent/unquote(u.path)).resolve()
  if not target.is_relative_to(ROOT):continue
  if not target.exists():broken.append(str(target));continue
  if target.is_file() and target not in keep:
   keep.add(target)
   if target.suffix.lower() in {'.html','.htm','.css','.svg'}:pending.append(target)
if broken:raise RuntimeError('Draft has missing local references: '+repr(broken))

with (OLD/'files_by_purpose.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
candidates={};runtime=[];protected=[];retained_sources={}
source_ext={'.py','.lean','.js','.mjs','.cjs','.ts','.tsx','.jsx','.ps1','.bat','.cmd','.sh','.css','.toml','.yaml','.yml','.ini','.cfg','.bib','.tex','.sty','.cls','.ipynb'}
for row in rows:
 rel=row['路径'];p=ROOT/rel;cat=row['用途'];suffix=p.suffix.lower();parts=[v.lower() for v in Path(rel).parts]
 if parts[0] in {'trash','.git'} or not p.is_file():continue
 if rel.startswith('Workspaces/workspace_catalog_audit_20261013/file_purpose_20261016/'):continue
 if p.resolve() in keep:protected.append(rel);continue
 reason=None
 if cat in {'数值轨迹、场与终态','断点续算状态','可重算的中间数组','解释器及工具缓存','运行日志'}:reason=cat
 elif cat=='历史版本、恢复备份与留档':reason=cat
 elif cat=='图、动画与展示资源':reason='未被当前论文草稿引用的图形产物'
 elif cat=='实验摘要与核验证据':
  # Keep inputs, frozen code and dependency descriptors. Move result tables/receipts.
  name=p.name.lower()
  is_input=any(v in name for v in ('config','manifest','parameter','protocol','solver','cells','package','lock','input','settings','inventory','projects'))
  if not is_input:reason='可重新生成的数值摘要、核验回执或表格'
 elif cat=='编译产物与证明运行环境':
  env=rel.startswith('_lean_shared/') or '/.lake/packages/' in rel
  in_library='/build/lib/lean/' in rel
  tool=env and '/build/bin/' in rel and p.name.lower() not in {'runlinter','runlinter.exe','runlinter.rsp'}
  # Imported .olean/private/server, IR, editor metadata and cache tools remain usable.
  lake_config='/.lake/config/' in rel or '/.lake/lakefile.' in rel or rel.endswith(('/proofwidgets/widget/js/lake.trace','/proofwidgets/widget/package-lock.json.trace'))
  if lake_config or (env and (in_library or tool)):runtime.append(rel)
  else:reason='编译中间输出、下载归档或隔离证明运行副本'
 if reason:candidates[rel]=dict(path=rel,bytes=p.stat().st_size,reason=reason)
 elif suffix in source_ext and not any(v in parts for v in {'.lake','.research_deps','vendor','node_modules'}) and not rel.startswith('_lean_shared/'):
  retained_sources[rel]=hashlib.sha256(p.read_bytes()).hexdigest()

# Coalesce fully selected subtrees only after a fresh, non-link-traversing scan.
all_files=set();blocked=[];stack=[ROOT]
excluded={ROOT/'Trash',ROOT/'.git',OUT,ROOT/'Workspaces/git_maintenance_20261010/cleanup_20261016_remote'}
while stack:
 folder=stack.pop()
 try:
  with os.scandir(folder) as entries:
   for e in entries:
    path=Path(e.path)
    if path in excluded:continue
    try:
     st=e.stat(follow_symlinks=False)
     if e.is_symlink() or getattr(st,'st_file_attributes',0)&0x400:blocked.append(path);continue
     if e.is_dir(follow_symlinks=False):stack.append(path)
     elif e.is_file(follow_symlinks=False):all_files.add(path.relative_to(ROOT).as_posix())
    except OSError:blocked.append(path)
 except OSError:blocked.append(folder)
total=collections.Counter();selected=collections.Counter()
for rel in all_files:
 for parent in Path(rel).parents:
  if str(parent)=='.':continue
  key=parent.as_posix();total[key]+=1
  if rel in candidates:selected[key]+=1
bad_dirs=set()
for path in blocked:
 for folder in [path,*path.parents]:
  if folder.is_relative_to(ROOT):bad_dirs.add(folder.relative_to(ROOT).as_posix())
eligible={d for d,n in selected.items() if n==total[d] and n>=2 and d not in bad_dirs}
units=[];covered=set()
for d in sorted(eligible,key=lambda v:(v.count('/'),v)):
 if any(p.as_posix() in covered for p in Path(d).parents):continue
 covered.add(d);units.append(dict(path=d,kind='directory'))
for rel in sorted(candidates):
 if not any(p.as_posix() in covered for p in Path(rel).parents):units.append(dict(path=rel,kind='file'))
stats=collections.Counter()
for row in candidates.values():stats[row['reason']]+=row['bytes']
hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in keep}
plan=dict(root=str(ROOT),trash=str(TRASH),files=len(candidates),bytes=sum(v['bytes'] for v in candidates.values()),by_reason=dict(stats),move_units=units,files_detail=list(candidates.values()),protected_paper_hashes=hashes,retained_source_hashes=retained_sources,retained_environment_files=len(runtime),unreadable_or_links=[str(p) for p in blocked])
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'move_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in plan.items() if k in {'files','bytes','by_reason','protected_paper_hashes','retained_environment_files'}},ensure_ascii=True,indent=2))
print('Move units:',len(units),'Retained source files:',len(retained_sources))
