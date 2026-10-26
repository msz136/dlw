from pathlib import Path
import csv,json,hashlib,shutil
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote

ROOT=Path(r'C:\Users\msz\aca').resolve();OUT=Path(__file__).resolve().parent
TRASH=(ROOT/'Trash/cleanup_20261016').resolve()
with (OUT/'scoped_restore_files.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
assert len(rows)==8 and len({r['target'] for r in rows})==8
prepared=[]
for row in rows:
 target=(ROOT/row['target']).resolve();source=(TRASH/row['target']).resolve()
 assert target.is_relative_to(ROOT/'Workspaces') and source.is_relative_to(TRASH)
 assert target.suffix=='.json' and source.is_file() and not target.exists(),row['target']
 data=source.read_bytes();assert len(data)==int(row['bytes']);json.loads(data)
 prepared.append((source,target,hashlib.sha256(data).hexdigest()))
records=[]
for source,target,digest in prepared:
 target.parent.mkdir(parents=True,exist_ok=True)
 shutil.move(str(source),str(target))
 assert target.is_file() and not source.exists()
 assert hashlib.sha256(target.read_bytes()).hexdigest()==digest
 records.append(dict(path=target.relative_to(ROOT).as_posix(),bytes=target.stat().st_size,sha256=digest,verified=True))
audit=json.loads((OUT/'scoped_audit.json').read_text(encoding='utf-8'))
missing=[]
for row in audit['references']:
 p=ROOT/row['target']
 row['status']='现存' if p.exists() else '缺失'
 if not p.exists():missing.append(row)
assert not missing
for v in audit['by_entry'].values():v['missing']=[]
audit['missing_targets']=[];audit['missing_total_bytes']=0
(OUT/'scoped_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
unique={r['target']:r for r in audit['references']}
with (OUT/'scoped_keep_files.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['entry','source','tag','attribute','target','kind','status','bytes']);w.writeheader();w.writerows(sorted(unique.values(),key=lambda x:x['target']))
receipt=dict(restored=records,total_bytes=sum(r['bytes'] for r in records),scope=audit['scope'],local_reference_occurrences=len(audit['references']),unique_targets=len(unique),missing_targets=[])
(OUT/'restoration_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
p=ROOT/'report/workspace_cleanup_review_20261016.html';s=p.read_text(encoding='utf-8')
s=s.replace('按当前保留范围，只需补回8个JSON文件，合计85,254字节（约83.3 KiB）。没有发现缺失的图片或其他展示资源。','8个JSON文件已恢复到原路径，合计85,254字节（约83.3 KiB），逐文件SHA256与归档原件一致。7份入口HTML涉及的129个本地引用目标现已全部存在。')
s=s.replace('需要恢复并保留的8个文件','已恢复的8个文件')
s=s.replace('以上文件全部保存在 <code>Trash/cleanup_20261016/</code> 下的同相对路径。本轮只核对，尚未恢复。','以上8个文件已从Trash移回原路径。恢复前后逐项核对大小、JSON可读性与SHA256，全部一致。其余Trash内容未处理。')
s=s.replace('其中121个现存、8个待恢复','其中129个现存、0个缺失').replace('8个待恢复文件清单','本次8个恢复文件清单')
for page in ('dlw_hamilton.html','theory_results.html'):
 count=audit['by_entry'][page]['references']
 s=s.replace('<td>'+page+'</td><td>'+str(count)+'</td><td>4</td>','<td>'+page+'</td><td>'+str(count)+'</td><td>0</td>')
p.write_text(s,encoding='utf-8')
log=ROOT/'PROGRESS_LOG.md';s=log.read_text(encoding='utf-8')
note='> **2026-10-16八项引用恢复完成：** 按用户授权，将scoped_restore_files.csv中8个JSON从Trash移回原路径，共85254字节；恢复前后SHA256、大小及JSON可读性核验通过。根目录6份HTML及report/dlw_paper_draft.html的175处本地引用、129个去重目标现全部存在，无缺失。恢复回执归既有cleanup_review_20261016/restoration_receipt.json，清理复核报告与保留清单已同步；其余Trash未处理。 '
log.write_text(note+s[2:] if s.startswith('> ') else note+'\n\n'+s,encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=True,indent=2))
