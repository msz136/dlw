"""Read-only inventory of existing files; write purpose-based audit artifacts."""
from pathlib import Path
import os, json, csv, collections, zipfile, ast, struct, hashlib, html, re

ROOT = Path(r'C:\Users\msz\aca')
OUT = Path(__file__).resolve().parent
REPORT = ROOT / 'report/workspace_file_purposes_20261016.html'
CATS = {
 'source': ('研究源码、证明与配置', '保留', '算法、证明、生成器及配置，是复现工作的基础。'),
 'writing': ('论文、笔记与说明', '保留', '正文、推导、操作说明与研究记录。'),
 'literature': ('文献原件与阅读资料', '保留', '论文与外部参考资料。'),
 'evidence': ('实验摘要与核验证据', '保留', '误差表、参数、校验、运行清单等；通常体积小。'),
 'array': ('数值轨迹、场与终态', '研究证据，保留', '完整数值数组；重画图、改评价指标和独立核查需要。'),
 'checkpoint': ('断点续算状态', '完成状态待核对', '用于中断后继续计算，不等同于最终研究结果。'),
 'cache': ('可重算的中间数组', '可重建，按需保留', '为了避免重复计算而保存，移走会增加后续重算成本。'),
 'figure': ('图、动画与展示资源', '按引用保留', '论文插图、误差图、动画、网页资源及预览。'),
 'build': ('编译产物与证明运行环境', '可重建，按需保留', 'Lean 编译结果和隔离运行副本；不是新证明。'),
 'dependency': ('第三方依赖与工具', '运行需要，保留可用环境', 'Mathlib 源码、Python 包、前端库等。'),
 'bytecode': ('解释器及工具缓存', '低价值可重建', 'Python 字节码、工具临时缓存。'),
 'backup': ('历史版本、恢复备份与留档', '归档保留', '提供回滚和历史证据；不能仅据旧日期判定无用。'),
 'git': ('当前版本库内部数据', '保留', '当前 Git 对象与索引，支持版本历史。'),
 'log': ('运行日志', '辅助排障，按需保留', '计算与执行过程记录。'),
 'other': ('用途待核对', '待核对', '仅凭格式及路径无法可靠确定用途。'),
}

def content_kind(p):
 s=p.suffix.lower(); n=p.name.lower()
 if s in {'.py','.lean','.js','.mjs','.cjs','.ts','.tsx','.jsx','.sh','.ps1','.bat','.cmd','.toml','.yaml','.yml','.ini','.cfg','.css','.bib','.sty','.cls'} or n in {'makefile','dockerfile','.gitignore','.gitattributes','lean-toolchain'}: return 'source'
 if s in {'.md','.tex','.html','.htm','.ipynb','.docx','.rst'}: return 'writing'
 if s in {'.npz','.npy','.h5','.hdf5','.mat','.parquet','.pkl','.pickle','.bin'}: return 'array'
 if s in {'.json','.csv','.tsv'}: return 'evidence'
 if s in {'.png','.jpg','.jpeg','.gif','.webp','.svg','.mp4','.woff','.woff2','.ttf','.otf'}: return 'figure'
 if s=='.pdf': return 'literature' if str(p).replace('\\','/').startswith('Paper/') else 'figure'
 if s in {'.log','.out','.err'}: return 'log'
 if s in {'.txt'}: return 'writing'
 return 'other'

def classify(rel):
 p=Path(rel); parts=[v.lower() for v in p.parts]; low=rel.lower(); name=p.name.lower(); content=content_kind(p)
 if parts[0]=='trash' or any(v in {'archive','before','backups','backup'} or v.startswith(('before_','backup_')) or v.endswith('_before') for v in parts[:-1]) or p.stem.lower().endswith('_before'): return 'backup',content,'路径表明历史留档'
 if '.git' in parts: return 'git',content,'Git 内部路径'
 if '__pycache__' in parts or p.suffix.lower()=='.pyc' or any(v in {'.pytest_cache','.mypy_cache','.ruff_cache'} for v in parts): return 'bytecode',content,'工具缓存格式/路径'
 if any(v in {'.lean-runs','local_lean_runs','proof_cache'} for v in parts) or ('.lake' in parts and any(v in {'build','ir','lib','bin'} for v in parts[parts.index('.lake')+1:])) or p.suffix.lower() in {'.olean','.ilean','.o','.a','.trace','.barrel'}: return 'build',content,'编译格式/隔离证明运行路径'
 if parts[0]=='_lean_shared' or ('.lake' in parts and 'packages' in parts) or ('_assets' in parts and 'package' in parts) or any(v in {'.research_deps','node_modules','site-packages','vendor','.venv','venv'} or 'katex' in v for v in parts[:-1]): return 'dependency',content,'共享库/第三方依赖路径'
 if 'references' in parts: return 'literature',content,'外部参考材料（保留实际内容类型）'
 if 'checkpoint' in name: return 'checkpoint',content,'断点状态命名及续算代码'
 if 'independent_source_cache' in parts: return 'cache',content,'source_cache.py 的插值源项缓存'
 if content=='array':
  if 'dlw_paper_20261009' in parts and any(v in {'boundary_run','physd_domains_run','unified_run'} for v in parts): return 'backup',content,'finish_buffered.py 明确旧域结果不再作为当前论文结论；仍保留历史用途'
  return 'array',content,'数值二进制；需结合生成器判断使用范围'
 return content,content,'文件格式推断，非逐份内容审定'

rows=[]; errors=[]; skipped=[]; stack=[ROOT]
while stack:
 folder=stack.pop()
 try:
  with os.scandir(folder) as entries:
   for e in entries:
    try:
     p=Path(e.path)
     if p==OUT or p==REPORT: continue
     st=e.stat(follow_symlinks=False)
     if e.is_symlink() or (getattr(st,'st_file_attributes',0)&0x400): skipped.append(str(p.relative_to(ROOT))); continue
     if e.is_dir(follow_symlinks=False): stack.append(p)
     elif e.is_file(follow_symlinks=False):
      rel=str(p.relative_to(ROOT)).replace('\\','/'); cat,kind,why=classify(rel)
      rows.append(dict(path=rel,bytes=st.st_size,category=cat,content=kind,judgment=CATS[cat][1],basis=why,references=[]))
    except OSError as exc: errors.append(dict(path=str(p),error=str(exc)))
 except OSError as exc: errors.append(dict(path=str(folder),error=str(exc)))

# Match large research artifacts to local text consumers/producers. Mentions are leads, not proof of runtime access.
targets=[r for r in rows if r['bytes']>=10_000_000 and r['category'] in {'array','checkpoint','cache','backup'} and not r['path'].startswith('Trash/')]
byname=collections.defaultdict(list)
for r in targets: byname[Path(r['path']).name.lower()].append(r)
for r in rows:
 if r['category'] in {'build','dependency','bytecode','git','backup'} or r['bytes']>3_000_000 or Path(r['path']).suffix.lower() not in {'.py','.md','.html','.json','.ipynb','.js'}: continue
 try: body=(ROOT/r['path']).read_text(encoding='utf-8',errors='replace').lower().replace('\\\\','/').replace('\\','/')
 except OSError: continue
 for name in set(re.findall(r'[a-z0-9_.-]+\.(?:npz|npy|png|pdf|pack)',body)):
  for item in byname.get(name,[]):
   if len(item['references'])<6: item['references'].append(r['path'])

def inspect_npz(r):
 result=[]
 try:
  with zipfile.ZipFile(ROOT/r['path']) as z:
   for info in z.infolist():
    if not info.filename.endswith('.npy'): continue
    with z.open(info) as f:
     magic=f.read(8)
     if magic[:6]!=b'\x93NUMPY': continue
     nbytes=2 if magic[6]==1 else 4
     length=int.from_bytes(f.read(nbytes),'little')
     if length>100000: continue
     header=ast.literal_eval(f.read(length).decode('latin1').strip())
    result.append(dict(array=info.filename,shape=header['shape'],dtype=header['descr'],raw_bytes=info.file_size,compressed_bytes=info.compress_size))
 except Exception as exc: return dict(error=str(exc))
 return result

largest=sorted(rows,key=lambda r:r['bytes'],reverse=True)
npz=[r for r in largest if r['path'].endswith('.npz') and r['category'] not in {'dependency','build','backup'}][:12]
array_details={r['path']:inspect_npz(r) for r in npz}
checkpoints=[]
for r in rows:
 if r['category']=='checkpoint' and r['path'].endswith('.npz'):
  folder=(ROOT/r['path']).parent; receipt=folder/'validation.json'
  complete=receipt.exists()
  step=None
  try: step=json.loads((folder/'checkpoint.json').read_text(encoding='utf-8')).get('n')
  except (OSError,ValueError): pass
  match=re.search(r'_T([0-9.]+)_dt([0-9.]+)',folder.name)
  target_steps=round(float(match[1])/float(match[2])) if match else None
  end_time=None
  if complete:
   try:
    receipt_data=json.loads(receipt.read_text(encoding='utf-8'))
    end_time=max(v['t'] for v in receipt_data.get('final_metrics',[]) if 't' in v)
   except (OSError,ValueError,KeyError): pass
  finished=complete and target_steps==step and match and end_time is not None and abs(end_time-float(match[1]))<1e-10
  checkpoints.append(dict(path=r['path'],bytes=r['bytes'],checkpoint_step=step,target_steps=target_steps,completion_receipt_exists=complete,receipt_final_time=end_time,judgment='已到目标步数且终态回执到T；续算用途已完成，可归档' if finished else '未核实完成，保留续算能力'))
  r['judgment']=checkpoints[-1]['judgment']

# Hash only equal-size large research files; never infer duplication from names.
sizes=collections.defaultdict(list)
for r in rows:
 if r['bytes']>=10_000_000 and r['category'] not in {'dependency','build','git','bytecode'} and not r['path'].startswith('Trash/'): sizes[r['bytes']].append(r)
duplicates=[]
for size,group in sizes.items():
 if len(group)<2: continue
 digests=collections.defaultdict(list)
 for r in group:
  h=hashlib.sha256()
  try:
   with (ROOT/r['path']).open('rb') as f:
    for block in iter(lambda:f.read(4*1024*1024),b''): h.update(block)
   digests[h.hexdigest()].append(r['path'])
  except OSError: continue
 for digest,paths in digests.items():
  if len(paths)>1: duplicates.append(dict(bytes_each=size,sha256=digest,paths=paths,redundant_bytes=size*(len(paths)-1)))

stats={}
for cat,(title,judgment,description) in CATS.items():
 subset=[r for r in rows if r['category']==cat]
 stats[cat]=dict(title=title,files=len(subset),bytes=sum(r['bytes'] for r in subset),judgment=judgment,description=description)
summary=dict(date='2026-10-16',files=len(rows),bytes=sum(r['bytes'] for r in rows),categories=stats,largest_files=largest[:60],array_details=array_details,checkpoints=checkpoints,large_exact_duplicates=duplicates,unreadable=errors,skipped_links=skipped,method='Logical bytes, no symlink traversal; pathname/format classification with targeted source inspection. Absence of a textual mention is not evidence of disuse. Audit outputs excluded. Duplicate check: equal-size non-environment research files >=10 MB, excluding Trash.')
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'files_by_purpose.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['用途','内容类型','大小字节','保留判断','判断依据','路径','同名文本引用线索'])
 for r in sorted(rows,key=lambda r:(r['category'],-r['bytes'])): w.writerow([CATS[r['category']][0],CATS[r['content']][0],r['bytes'],r['judgment'],r['basis'],r['path'],' | '.join(r['references'])])

def fmt(n): return f'{n/1e9:.2f} GB' if n>=1e9 else f'{n/1e6:.1f} MB' if n>=1e6 else f'{n/1e3:.1f} KB'
def esc(s): return html.escape(str(s))
table=''.join(f'<tr><td>{esc(v["title"])}</td><td>{fmt(v["bytes"])}</td><td>{v["files"]:,}</td><td>{esc(v["judgment"])}</td><td>{esc(v["description"])}</td></tr>' for k,v in sorted(stats.items(),key=lambda kv:-kv[1]['bytes']))
bigrows=''.join(f'<tr data-cat="{r["category"]}"><td>{esc(CATS[r["category"]][0])}</td><td>{fmt(r["bytes"])}</td><td>{esc(r["judgment"])}</td><td><a href="../{esc(r["path"])}">{esc(r["path"])}</a><small>{esc(r["basis"])}</small></td></tr>' for r in largest if r['bytes']>=10_000_000)
options=''.join(f'<option value="{k}">{esc(v[0])}</option>' for k,v in CATS.items())
detail=''
for path,items in array_details.items():
 if isinstance(items,dict): continue
 main=sorted(items,key=lambda a:-a['raw_bytes'])[:6]
 detail+=f'<tr><td>{esc(path)}</td><td>'+ '<br>'.join(f'{esc(a["array"])}：{esc(a["shape"])}，{esc(a["dtype"])}' for a in main)+f'</td><td>{fmt(sum(a["raw_bytes"] for a in items))}</td></tr>'
checkpoint_html=''.join(f'<li><code>{esc(c["path"])}</code>（{fmt(c["bytes"])}）：{esc(c["judgment"])}；已保存 {c["checkpoint_step"]}/{c["target_steps"]} 步，终态回执时间 {c["receipt_final_time"]}。</li>' for c in checkpoints)
duplicate_html=''.join(f'<li>{fmt(d["bytes_each"])} × {len(d["paths"])}：'+ '<br>'.join(esc(p) for p in d['paths'])+'</li>' for d in duplicates) or '<li>本轮限定范围内没有发现大文件逐字节重复。不同参数、不同时间和不同数组布局不属于重复。</li>'
page=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>工作区文件用途与保留判断</title>
<style>body{{max-width:1280px;margin:40px auto;padding:0 24px;color:#222;font:16px/1.7 system-ui,"Microsoft YaHei",sans-serif}}h1{{font-size:28px}}h2{{margin-top:36px;font-size:22px}}table{{border-collapse:collapse;width:100%;font-size:14px}}td,th{{padding:10px;text-align:left;border-bottom:1px solid #ddd;vertical-align:top}}th{{background:#f5f5f5}}td:last-child{{overflow-wrap:anywhere}}a{{color:#175c93}}small{{display:block;color:#666}}input,select{{padding:9px;margin:8px 12px 16px 0;font:inherit;max-width:100%}}code{{overflow-wrap:anywhere}}.scroll{{overflow:auto}}.note{{color:#555}}</style>
<h1>工作区文件用途与保留判断</h1><p>2026-10-16 · 已读取 {len(rows):,} 个文件，共 {fmt(summary['bytes'])}。按用途归类，子目录中的源码、数据、缓存与备份分别计数。</p>
<h2>空间主要花在哪里</h2><p>最大的三类开销来自数值实验的完整数组、Lean 编译与运行环境、以及历史留档。论文正文、研究源码和摘要表通常很小。文件是否有用取决于它支持的计算和证据链，不能由后缀或“cache”字样单独决定。</p>
<div class="scroll"><table><thead><tr><th>用途</th><th>大小</th><th>文件数</th><th>保留判断</th><th>实际作用</th></tr></thead><tbody>{table}</tbody></table></div>
<h2>已核对的大文件在做什么</h2><p><b>共享孤子轨迹：</b><code>dlw_three_tracks_20261013/shared/*.npz</code> 保存21个实际时刻的 u、v、精确 u、精确 v；数组轴为时间×y×x。Fourier、小波、误差演化动画和半步长对照使用这些数据。三个约216 MB的C算例文件代表不同算法或时间步，不能视为三份相同副本。依据：该项目 README、generate_shared.py 和 spectrum/analyze_error_fields.py。</p>
<p><b>误差传播与分源：</b><code>transport/frame_*.npz</code> 除实际误差外，还存交叉传播、未传播源项累加和三个误差来源分量。字段多、网格大、时刻多，体积自然增长；summarize_transport.py 与 figures/error_fields.py 会读取这些帧。<code>final_common.npz</code> 保存完整终态；<code>independent_source_cache/</code> 是可重算的五节点源项插值缓存。依据：run_transport.py、source_cache.py。</p>
<p><b>论文数值文件：</b><code>buffered_run/</code> 的原生状态与物理场缓存用于结果剖面、场图和比较。<code>boundary_run/</code>、<code>physd_domains_run/</code>、<code>unified_run/</code> 的数组属于较早计算域版本；finish_buffered.py 明确记录“旧域结果仅保留为历史，不再作为当前论文结论”。旧数据仍可支持对照与追溯，宜归档；该判断不扩展到同目录的源代码或说明。</p>
<p><b>Lean 与 Mathlib：</b><code>.lake/build/</code>、<code>.olean</code> 和各证明运行副本是编译／执行产物。Mathlib 源码与包属于依赖，自己的 <code>.lean</code> 属于研究源码；二者和编译结果分别分类。编译产物可重建，但重建需要时间，首次恢复依赖也可能需要网络。不能整包搬走仍在使用的共享环境。</p>
<p><b>旧 Git 快照：</b><code>Trash/git_snapshot_20261010_212349/.git</code> 是10月10日仓库瘦身前保存的恢复副本，原记录大小2.845 GB。<code>archive_result.json</code> 记录了归档分支与提交，当前根目录另有活动 <code>.git</code>。它承担恢复用途，不参与普通数值计算；内部 pack 应随完整备份一同保留或归档，不能拆散。</p>
<h2>续算文件是否还需要</h2><ul>{checkpoint_html}</ul><p class="note">结束回执存在仅说明生成流程留下完成标记；尚未逐项重验其科学结论。没有回执的任务不能按已完成处理。</p>
<h2>数值文件内部保存了哪些数组</h2><p>只读取压缩包目录和数组头，不执行文件内容。下表列每个文件最大的六个数组；最后一列是包内全部数组未压缩体积。</p><div class="scroll"><table><thead><tr><th>文件</th><th>数组与形状</th><th>未压缩大小</th></tr></thead><tbody>{detail}</tbody></table></div>
<h2>大文件的精确重复核对</h2><p>对研究与留档区中≥10 MB、大小相同的文件计算 SHA256；不含第三方环境、Git内部数据及Trash。本项只判断字节相同，不判断科学内容等价。</p><ul>{duplicate_html}</ul>
<h2>逐文件用途清单</h2><p>下表列出全部≥10 MB文件，可按用途和路径筛选。完整清单包含每个可读文件的用途、大小、判断及依据：<a href="../Workspaces/workspace_catalog_audit_20261013/file_purpose_20261016/files_by_purpose.csv">下载完整 CSV</a>。</p>
<select id="cat"><option value="">全部用途</option>{options}</select><input id="query" placeholder="搜索文件名或路径" aria-label="搜索文件名或路径"><span id="count"></span><div class="scroll"><table><thead><tr><th>用途</th><th>大小</th><th>判断</th><th>路径与依据</th></tr></thead><tbody id="files">{bigrows}</tbody></table></div>
<h2>统计范围</h2><p>按逻辑文件大小计数，GB为10亿字节；没有计算磁盘簇、压缩或硬链接去重。{len(errors)}项访问失败，{len(skipped)}个链接或重解析点跳过，因此总数为可读部分。没有移动或删除原文件。通用分类依据路径和格式，重点大文件另外核对生成与读取代码；“未找到文本引用”不等于没有用途。未知项单列，不直接判废。</p>
<script>const rs=[...document.querySelectorAll('#files tr')],cat=document.querySelector('#cat'),q=document.querySelector('#query');function filter(){{let n=0;for(const r of rs){{let ok=(!cat.value||r.dataset.cat===cat.value)&&r.textContent.toLowerCase().includes(q.value.toLowerCase());r.hidden=!ok;if(ok)n++;}}document.querySelector('#count').textContent=n+' 个文件';}}cat.addEventListener('change',filter);q.addEventListener('input',filter);filter();</script></html>'''
REPORT.write_text(page,encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k in {'files','bytes','categories','checkpoints','large_exact_duplicates'}},ensure_ascii=True,indent=2))
print('Unreadable:',len(errors),'Skipped:',len(skipped))
