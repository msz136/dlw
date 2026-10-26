from pathlib import Path
import json,collections,csv,html
from urllib.parse import quote
ROOT=Path(r'C:\Users\msz\aca');OUT=Path(__file__).resolve().parent
d=json.loads((OUT/'audit.json').read_text(encoding='utf-8'))
links=[x for x in d['broken_links'] if x['caused_by_cleanup']]
targets=sorted({x['target'] for x in links})
confirmed=[
 ('Workspaces/dlw_paper_20261009/tables.json','Workspaces/dlw_paper_20261009/assemble.py','装配脚本第48行直接读取表格输入；主论文当前HTML仍完整。'),
 ('Workspaces/dlw_error_mechanism_20261013/sources/validation.json','Workspaces/dlw_error_mechanism_20261013/validate_delivery.py','核验入口第24行开始读取既有核验记录。'),
 ('Workspaces/dlw_error_mechanism_20261013/intervention/summary.csv','Workspaces/dlw_error_mechanism_20261013/validate_delivery.py','核验入口第41行直接读取；绘图入口同样使用。'),
 ('复现/mch_ldg/results/all_runs.csv','复现/mch_ldg/README.md','README明确将其作为完整运行记录入口；分析所需summary和trajectory也被移走。'),
 ('复现/mch_ldg/search/figure3_dissipative_digitized.csv','复现/mch_ldg/analyze.py','分析脚本直接读取图3对照曲线。'),
 ('复现/mch_ldg/search/arxiv_source_response.bin','复现/mch_ldg/search/extract_figure3.py','提取图3曲线所需原文源包；这是文献来源材料，不能仅因bin扩展名当作数值摘要。'),
]
checks=[]
for target,source,why in confirmed:
 p=ROOT/target;t=ROOT/'Trash/cleanup_20261016'/target
 try:p.open('rb').close();read='可读'
 except FileNotFoundError:read='FileNotFoundError'
 checks.append(dict(target=target,source=source,evidence=why,read_check=read,trash_exists=t.is_file(),trash_bytes=t.stat().st_size if t.is_file() else None))
(OUT/'confirmed_cases.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
recommended=sorted(set(targets)|{x['target'] for x in checks})
with (OUT/'priority_restore_candidates.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['原相对路径','归档相对路径','依据'])
 for t in recommended:w.writerow([t,'Trash/cleanup_20261016/'+t,'现存文档直接引用' if t in targets else '人工复核的读取依赖'])
counts=collections.Counter(x['source'] for x in links)
images=[x for x in links if x['kind'] in {'src','poster'}]
pages=sorted({x['source'] for x in links if x['source'].endswith('.html')})
esc=html.escape
def link(p):return '<a href="../'+quote(p,safe='/')+'">'+esc(p)+'</a>'
body='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>工作区清理复核</title><style>body{max-width:1080px;margin:48px auto;padding:0 24px;font:17px/1.75 "Microsoft YaHei",sans-serif;color:#202124}h1{font-size:30px}h2{font-size:22px;margin-top:36px}table{border-collapse:collapse;width:100%;font-size:14px}td,th{text-align:left;vertical-align:top;border-bottom:1px solid #ddd;padding:10px;overflow-wrap:anywhere}a{color:#145c9e}code{overflow-wrap:anywhere}small{color:#555}</style><h1>工作区清理复核</h1><p>2026年10月16日 · C:\\Users\\msz\\aca</p><p><strong>存在误移，应恢复仍被报告、分析与核验使用的材料。</strong>本轮清理文件均能在Trash中找到，未发现本轮清单内文件丢失。现存源码和论文草稿保持完整，并不能据此认定其他研究资料可以移走。</p>'''
body+=f'<h2>核查结果</h2><p>逐项核对本轮{d["moved_files"]:,}份迁移记录：归档文件全部存在且大小吻合。Git显示的{d["git_deleted_count"]:,}份已跟踪缺失文件均在迁移清单中。原先记录的7,289份保留源码及11份论文与直接资源，SHA256核对均通过。</p>'
body+=f'<p>浏览并静态检查{d["scanned_text_files"]:,}份文本文件，发现由本轮迁移造成的{len(links)}处本地文件引用失效，涉及{len(targets)}个不同目标、{len(counts)}份文档，其中{len(pages)}份HTML页面；39处为图片或poster引用。引用次数包含历史记录和用途盘点页，不等同于独立故障数。</p>'
body+='<h2>已确认的误移</h2><table><tr><th>文件</th><th>影响与证据</th></tr>'
for x in checks:body+='<tr><td><code>'+esc(x['target'])+'</code></td><td>'+esc(x['evidence'])+'<br>'+link(x['source'])+'<br><small>原路径读取：'+x['read_check']+'；Trash副本：'+('存在' if x['trash_exists'] else '不存在')+'</small></td></tr>'
body+='</table><h2>报告引用受损</h2><table><tr><th>文档</th><th>失效引用次数</th></tr>'
for p,n in counts.most_common():body+='<tr><td>'+link(p)+'</td><td>'+str(n)+'</td></tr>'
body+='</table><h2>保留判断</h2><p>清理程序只以当前论文草稿的引用闭包保护图片，导致其他报告、Notebook HTML及研究图集的资源被移走。它还将实验摘要、核验记录和表格按名称统一归档，未区分后续脚本输入、已发表结论的证据与临时回执。可重算不等于无须保留，尤其是带时间戳的运行、失败记录和冻结的数值证据。</p><p>建议优先恢复现存报告直接引用的资源及上述读取依赖，再按项目复核数值轨迹、实验汇总和续算状态。解释器缓存和普通编译中间文件可继续留在Trash；不建议将全部38,130份文件无差别恢复。</p><h2>范围与证据</h2><p>本次不移动研究文件、不重跑数值实验。文件可恢复性按存在和字节大小验证，未对13.81GB归档全部逐字节比对；“源码完整”仅指清理前记录的哈希集合。静态引用检查不覆盖运行时动态拼接、外部服务和第三方依赖内部。代码字符串匹配只作候选线索，未把42,828条同名匹配当作已确认依赖。</p>'
body+='<p>'+link('Workspaces/workspace_catalog_audit_20261013/cleanup_review_20261016/broken_links.csv')+'<br>'+link('Workspaces/workspace_catalog_audit_20261013/cleanup_review_20261016/priority_restore_candidates.csv')+'<br>'+link('Workspaces/workspace_catalog_audit_20261013/cleanup_review_20261016/audit.json')+'</p></html>'
dest=ROOT/'report/workspace_cleanup_review_20261016.html';dest.write_text(body,encoding='utf-8')
log=ROOT/'PROGRESS_LOG.md';s=log.read_text(encoding='utf-8')
prefix=f'> **2026-10-16清理复核：** 逐项核对38130份迁移文件，Trash副本均存在且大小一致；2455份Git已跟踪缺失文件均在迁移清单内，7289份源码及11份论文/直接资源哈希核对通过。但发现误移：静态扫描6131份文本，清理造成{len(links)}处本地引用失效（{len(targets)}个目标、{len(counts)}份文档，含39处图片/poster引用）；确认论文装配tables.json、误差机制核验JSON/CSV、mCH运行记录与图3对照曲线/原文源包仍有使用用途。仅保护当前论文引用资源及按文件类别批量清理不足以证明无用。审查报告见[清理复核](report/workspace_cleanup_review_20261016.html)，证据与优先恢复候选归既有维护项目cleanup_review_20261016/。本轮只审查，未恢复或移动研究文件；归档内容仅作存在/大小核验，未对全部归档作哈希认证。 '
if not s.startswith('> **2026-10-16清理复核：**'):log.write_text(prefix+s[2:] if s.startswith('> ') else prefix+'\n\n'+s,encoding='utf-8')
print(json.dumps(dict(unique_missing_targets=len(targets),affected_documents=len(counts),affected_html=len(pages),confirmed_cases=checks,report=str(dest)),ensure_ascii=True,indent=2))
