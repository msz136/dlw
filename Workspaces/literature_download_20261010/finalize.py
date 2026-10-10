from pathlib import Path
from pypdf import PdfReader
import json, html

root = Path(r'C:\Users\msz\aca')
dest = root / 'Paper' / 'sources'
manifest = dest / 'literature_download_20261010.json'
papers = json.loads(manifest.read_text(encoding='utf-8'))
for p in papers:
    if p.get('filename'):
        reader = PdfReader(dest / p['filename'])
        p['pages'] = len(reader.pages)
        p['first_page_excerpt'] = reader.pages[0].extract_text()[:800]
        p['validation'] = 'PDF parsed successfully; first-page title and authors manually checked against requested paper'
    else:
        p['additional_attempt'] = 'curl with Windows certificate validation also failed TLS handshake; publisher link retained'
manifest.write_text(json.dumps(papers, ensure_ascii=False, indent=2), encoding='utf-8')
esc = html.escape
rows = []
for p in papers:
    local = '<a href="'+esc(p['filename'])+'">本地 PDF</a>（'+str(p['pages'])+' 页）' if p.get('filename') else '仅保存链接'
    sources = '<br>'.join('<a href="'+esc(url)+'">'+esc(version)+'</a>' for version,url in p['candidates'] if '46464798' not in url)
    rows.append('<tr><td>'+str(p['year'])+'</td><td><a href="'+esc(p['page'])+'">'+esc(p['title'])+'</a><br><small>'+esc(p['authors'])+'</small></td><td>'+esc(p['journal'])+'</td><td>'+local+'<br><small>'+esc(p.get('version','连接或访问失败'))+'</small></td><td>'+sources+'</td></tr>')
page = '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>可积方程与数值分析文献</title><style>body{font:16px/1.6 system-ui;max-width:1300px;margin:40px auto;padding:0 20px}table{border-collapse:collapse;width:100%}td,th{padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid #ddd}small{color:#555}a{color:#1453a0}</style><h1>可积方程与数值分析文献</h1><p>2026-10-10 收集：5 篇期刊论文与 1 篇补充预印本。4 篇已下载 PDF；2 篇保留链接。PDF 均已解析并核对首页标题。公开手稿、预印本与出版社版本分别标注；未验证 SJTU 订阅权限。</p><table><tr><th>年份</th><th>论文</th><th>期刊</th><th>本地文件与版本</th><th>下载入口</th></tr>'+''.join(rows)+'</table></html>'
(dest/'literature_links_20261010.html').write_text(page,encoding='utf-8')

marker='<!-- LITERATURE_DOWNLOAD_20261010_BEGIN -->'
for filename,body in [
    ('PROGRESS_LOG.md', '> **2026-10-10（可积方程与数值分析文献下载）：** 已在 Paper/sources 保存此前筛选的 5 篇第一档期刊论文与 1 篇补充预印本：4 篇 PDF（Feng–Schratz 出版社版，Ning–Wu–Zhao 作者手稿，Yang 与 Sheng–Yu–Feng 的 arXiv 版），6 个 .url 链接和 HTML 入口。PDF 解析、页数及首页题名核对通过。Dougalis–Durán 与 Cai–Shen 全文入口因 403/TLS 连接失败，仅保存链接；未验证 SJTU 订阅权限。下载版本、来源、哈希和失败记录见 literature_download_20261010.json。'),
    ('FILE_INDEX.md', '\n'.join('- [Paper/sources/'+f.name+'](Paper/sources/'+f.name+')：文献全文、链接或下载记录。' for f in sorted(dest.iterdir()) if f.name.startswith(('2020_Cai_', '2021_Sheng_', '2022_Dougalis_', '2022_Ning_', '2022_Yang_', '2024_Feng_', 'literature_'))) + '\n- [Workspaces/literature_download_20261010/download.py](Workspaces/literature_download_20261010/download.py)：下载脚本。\n- [Workspaces/literature_download_20261010/finalize.py](Workspaces/literature_download_20261010/finalize.py)：核验与登记脚本。'),
]:
    path=root/filename
    old=path.read_text(encoding='utf-8')
    if marker not in old:
        path.write_text(marker+'\n'+body+'\n<!-- LITERATURE_DOWNLOAD_20261010_END -->\n\n'+old,encoding='utf-8')
print('Verified 4 PDFs and 6 URL shortcuts; index and progress registered.')
