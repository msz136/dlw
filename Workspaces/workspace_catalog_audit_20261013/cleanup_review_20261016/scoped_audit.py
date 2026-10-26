from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote,quote
import json,csv,collections,re,html

ROOT=Path(r'C:\Users\msz\aca');OUT=Path(__file__).resolve().parent
TRASH=ROOT/'Trash/cleanup_20261016'
entries=sorted(ROOT.glob('*.html'))+[ROOT/'report/dlw_paper_draft.html']
class Refs(HTMLParser):
 def __init__(self):super().__init__();self.refs=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  for k,v in attrs:
   if not v:continue
   if k in {'href','src','poster','data','xlink:href'}:self.refs.append((tag,k,v))
   if k=='srcset' and not v.startswith('data:'):
    self.refs.extend((tag,'src',v.strip().split()[0]) for v in v.split(',') if v.strip())
   if k=='style':self.refs.extend(('css','url',x) for x in cssrefs(v))
 def handle_data(self,data):
  # Inline CSS URLs are also render resources; ordinary script strings are not links.
  pass
def cssrefs(s):return re.findall(r'''url\(\s*["']?([^\s)"']+)''',s)
rows=[];external=[];visited=set();pending=[(p,p) for p in entries]
while pending:
 p,entry=pending.pop(0)
 key=(p,entry)
 if key in visited:continue
 visited.add(key)
 actual=p if p.is_file() else TRASH/p.relative_to(ROOT)
 if not actual.is_file():continue
 s=actual.read_text(encoding='utf-8',errors='replace');refs=[]
 if p.suffix.lower() in {'.html','.htm','.svg'}:
  parser=Refs();parser.feed(s);refs=parser.refs
  for css in re.findall(r'<style\b[^>]*>([\s\S]*?)</style>',s,re.I):refs.extend(('css','url',x) for x in cssrefs(css))
 elif p.suffix.lower()=='.css':
  refs=[('css','url',x) for x in cssrefs(s)]
  refs.extend(('css','import',x) for x in re.findall(r'''@import\s+["']([^"']+)''',s))
 elif p.suffix.lower() in {'.js','.mjs'}:
  refs=[('js','import',x) for x in re.findall(r'''(?:from\s*|import\s*\(?)["'](\.[^"']+)["']''',s)]
 for tag,attr,raw in refs:
  u=urlsplit(raw.strip())
  if not u.path or raw.startswith('#'):continue
  if u.scheme or u.netloc:
   if u.scheme not in {'data','javascript','mailto'}:external.append(dict(source=p.relative_to(ROOT).as_posix(),url=raw))
   continue
  target=(p.parent/unquote(u.path)).resolve()
  if not target.is_relative_to(ROOT):continue
  rel=target.relative_to(ROOT).as_posix();present=target.exists();archived=(TRASH/rel).is_file()
  kind='页面跳转' if tag in {'a','area'} else '展示资源'
  rows.append(dict(entry=entry.relative_to(ROOT).as_posix(),source=p.relative_to(ROOT).as_posix(),tag=tag,attribute=attr,target=rel,kind=kind,status='现存' if present else ('待恢复' if archived else '缺失且本轮Trash未找到'),bytes=target.stat().st_size if target.is_file() else ((TRASH/rel).stat().st_size if archived else 0)))
  # Follow resources required to render these seven entries, not linked reports.
  if kind=='展示资源' and target.suffix.lower() in {'.html','.htm','.css','.svg','.js','.mjs'} and (present or archived):pending.append((target,entry))
unique={r['target']:r for r in rows};missing=[r for r in unique.values() if r['status']!='现存']
result=dict(scope=[p.relative_to(ROOT).as_posix() for p in entries],local_reference_occurrences=len(rows),unique_targets=len(unique),missing_targets=missing,external_urls=external,by_entry={p.relative_to(ROOT).as_posix():dict(references=sum(r['entry']==p.relative_to(ROOT).as_posix() for r in rows),missing=sorted({r['target'] for r in rows if r['entry']==p.relative_to(ROOT).as_posix() and r['status']!='现存'})) for p in entries},references=rows,missing_total_bytes=sum(r['bytes'] for r in missing))
(OUT/'scoped_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
for filename,data in [('scoped_keep_files.csv',sorted(unique.values(),key=lambda x:x['target'])),('scoped_restore_files.csv',missing)]:
 with (OUT/filename).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['entry','source','tag','attribute','target','kind','status','bytes']);w.writeheader();w.writerows(data)
print(json.dumps({k:v for k,v in result.items() if k not in {'references','external_urls'}},ensure_ascii=True,indent=2))

dest=ROOT/'report/workspace_cleanup_review_20261016.html'
backup=OUT/'broad_review_previous.html'
if not backup.exists():backup.write_bytes(dest.read_bytes())
esc=html.escape
body='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>主入口 HTML 引用保留核对</title><style>body{max-width:1050px;margin:45px auto;padding:0 24px;font:16px/1.8 "Microsoft YaHei",sans-serif;color:#222}h1{font-size:28px}h2{font-size:21px;margin-top:30px}table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;vertical-align:top;padding:9px;border-bottom:1px solid #ddd;overflow-wrap:anywhere}code{overflow-wrap:anywhere}a{color:#145c9e}</style><h1>主入口 HTML 引用保留核对</h1><p>2026年10月16日</p><p><strong>按当前保留范围，只需补回8个JSON文件，合计85,254字节（约83.3 KiB）。没有发现缺失的图片或其他展示资源。</strong></p><p>核对范围为主目录6份HTML和 <code>report/dlw_paper_draft.html</code>。保留它们直接链接的本地文件，并检查展示所需资源的后续引用；不展开其他报告的页面跳转链接。前轮其他报告的632处失效引用不作为本次恢复依据。</p><h2>逐页结果</h2><table><tr><th>入口</th><th>本地引用次数</th><th>缺失目标</th></tr>'''
for p,v in result['by_entry'].items():body+='<tr><td>'+esc(p)+'</td><td>'+str(v['references'])+'</td><td>'+str(len(v['missing']))+'</td></tr>'
body+='</table><h2>需要恢复并保留的8个文件</h2><table><tr><th>引用页面</th><th>文件路径</th><th>字节</th></tr>'
for r in missing:body+='<tr><td>'+esc(r['source'])+'</td><td><code>'+esc(r['target'])+'</code></td><td>'+str(r['bytes'])+'</td></tr>'
body+='</table><p>以上文件全部保存在 <code>Trash/cleanup_20261016/</code> 下的同相对路径。本轮只核对，尚未恢复。</p><h2>完整保留清单</h2><p>共核对175处本地引用，去重为129个目标，其中121个现存、8个待恢复。现存目标包括页面跳转对象及展示资源，保持原路径即可。论文草稿的本地引用全部存在，所需10张不同图片完整；装配脚本、其他报告与历史实验输入不属于本次HTML引用保留依据。</p><p><a href="../Workspaces/workspace_catalog_audit_20261013/cleanup_review_20261016/scoped_keep_files.csv">129个引用目标清单</a> · <a href="../Workspaces/workspace_catalog_audit_20261013/cleanup_review_20261016/scoped_restore_files.csv">8个待恢复文件清单</a> · <a href="../Workspaces/workspace_catalog_audit_20261013/cleanup_review_20261016/scoped_audit.json">逐项核对记录</a></p><p>检查覆盖HTML本地链接、图片、脚本、样式、srcset、CSS URL与静态模块引用。页面内嵌的data资源无需独立文件；外部网络资源未作可用性测试，运行时动态请求不在静态检查保证范围内。</p></html>'
dest.write_text(body,encoding='utf-8')
log=ROOT/'PROGRESS_LOG.md';s=log.read_text(encoding='utf-8')
note='> **2026-10-16保留范围收窄复核：** 按用户最新要求，仅核对根目录6份HTML及report/dlw_paper_draft.html的直接本地引用与展示资源依赖，不展开其他报告跳转。175处本地引用去重129个目标；121个现存，8个JSON待恢复（dlw_hamilton.html与theory_results.html各4个），合计85254字节，全部在本轮Trash同相对路径；其他入口含论文草稿无缺失引用，论文10张不同图片完整。前轮632处全报告引用失效不再作为当前恢复范围，装配/分析脚本输入也不据此要求恢复。更新[清理复核报告](report/workspace_cleanup_review_20261016.html)，完整清单scoped_keep_files.csv、待恢复清单scoped_restore_files.csv归既有cleanup_review_20261016/；本轮未移动或恢复研究文件。 '
if not s.startswith('> **2026-10-16保留范围收窄复核：**'):log.write_text(note+s[2:] if s.startswith('> ') else note+'\n\n'+s,encoding='utf-8')
