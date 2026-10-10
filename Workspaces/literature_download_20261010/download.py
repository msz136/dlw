from pathlib import Path
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
import json, hashlib, html

ROOT = Path(r'C:\Users\msz\aca')
DEST = ROOT / 'Paper' / 'sources'
PAPERS = [
    dict(stem='2022_Dougalis_Duran_KdV_high_order', title='A high-order fully discrete scheme for the Korteweg–de Vries equation with a time-stepping procedure of Runge–Kutta-composition type', authors='Vassilios A. Dougalis; Ángel Durán', journal='IMA Journal of Numerical Analysis', year=2022, doi='10.1093/imanum/drab060', candidates=[('publisher', 'https://academic.oup.com/imajna/article-pdf/42/4/3022/46464798/drab060.pdf'), ('author manuscript', 'https://uvadoc.uva.es/bitstream/handle/10324/62420/2022IMA.pdf?sequence=1')]),
    dict(stem='2022_Ning_Wu_Zhao_mKdV_low_regularity', title='An Embedded Exponential-Type Low-Regularity Integrator for mKdV Equation', authors='Cui Ning; Yifei Wu; Xiaofei Zhao', journal='SIAM Journal on Numerical Analysis', year=2022, doi='10.1137/21M1408166', candidates=[('publisher', 'https://epubs.siam.org/doi/pdf/10.1137/21M1408166'), ('author manuscript', 'https://cam.tju.edu.cn/en/research/downAchiev.php?id=619')]),
    dict(stem='2024_Feng_Schratz_sine_Gordon_long_time', title='Improved uniform error bounds on a Lawson-type exponential integrator for the long-time dynamics of sine-Gordon equation', authors='Yue Feng; Katharina Schratz', journal='Numerische Mathematik', year=2024, doi='10.1007/s00211-024-01423-w', candidates=[('publisher', 'https://link.springer.com/content/pdf/10.1007/s00211-024-01423-w.pdf'), ('arXiv preprint', 'https://arxiv.org/pdf/2211.09402')]),
    dict(stem='2022_Yang_gKdV_high_order_conservative', title='Arbitrarily High-Order Conservative Schemes for the Generalized Korteweg–de Vries Equation', authors='Kai Yang', journal='SIAM Journal on Scientific Computing', year=2022, doi='10.1137/21M140777X', candidates=[('publisher', 'https://epubs.siam.org/doi/pdf/10.1137/21M140777X'), ('arXiv preprint', 'https://arxiv.org/pdf/2103.13608')]),
    dict(stem='2020_Cai_Shen_local_energy_preserving', title='Two classes of linearly implicit local energy-preserving approach for general multi-symplectic Hamiltonian PDEs', authors='Jiaxiang Cai; Jie Shen', journal='Journal of Computational Physics', year=2020, doi='10.1016/j.jcp.2019.108975', candidates=[('author-hosted published PDF', 'https://www.math.purdue.edu/~shen7/pub/CaiS20.pdf')]),
    dict(stem='2021_Sh eng_Yu_Feng_integrable_mCH'.replace('Sh eng','Sheng'), title='An integrable semi-discretization of the modified Camassa-Holm equation with linear dispersion term', authors='Han-Han Sheng; Guo-Fu Yu; Bao-Feng Feng', journal='arXiv preprint (journal publication not verified)', year=2021, doi=None, page='https://arxiv.org/abs/2110.15876', candidates=[('arXiv preprint', 'https://arxiv.org/pdf/2110.15876')]),
]

def fetch(p):
    p = dict(p)
    p['page'] = p.get('page') or 'https://doi.org/' + p['doi']
    p['attempts'] = []
    (DEST / (p['stem'] + '.url')).write_text('[InternetShortcut]\nURL=' + p['page'] + '\n', encoding='utf-8')
    target = DEST / (p['stem'] + '.pdf')
    if target.exists():
        p['status'] = 'existing file retained'
        return p
    for version, url in p['candidates']:
        try:
            req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
            with urlopen(req, timeout=22) as res:
                data = res.read(30000000)
                final_url = res.url
                ctype = res.headers.get('Content-Type', '')
            if not data.lstrip().startswith(b'%PDF-') or b'%%EOF' not in data[-8192:]:
                raise ValueError('response is not a complete PDF; content type: ' + ctype)
            target.write_bytes(data)
            p.update(status='PDF downloaded', version=version, download_url=url, resolved_url=final_url, filename=target.name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
            break
        except Exception as e:
            p['attempts'].append({'url':url, 'error':str(e)[:220]})
    else:
        p['status'] = 'link saved; PDF unavailable'
    print(p['stem'], p['status'], p.get('version',''), flush=True)
    return p

DEST.mkdir(parents=True, exist_ok=True)
with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(fetch, PAPERS))
(DEST / 'literature_download_20261010.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
rows = []
for p in results:
    esc = html.escape
    pdf = '<a href="' + esc(p['filename']) + '">PDF</a>' if p.get('filename') else 'PDF 未能下载'
    rows.append('<tr><td>' + str(p['year']) + '</td><td><a href="' + esc(p['page']) + '">' + esc(p['title']) + '</a><br><small>' + esc(p['authors']) + '</small></td><td>' + esc(p['journal']) + '</td><td>' + pdf + '<br><small>' + esc(p.get('version','仅链接')) + '</small></td></tr>')
page = '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>可积方程与数值分析文献</title><style>body{font:16px/1.6 system-ui;max-width:1200px;margin:40px auto;padding:0 20px}table{border-collapse:collapse;width:100%}td,th{padding:12px;text-align:left;border-bottom:1px solid #ddd}small{color:#555}a{color:#1453a0}</style><h1>可积方程与数值分析文献</h1><p>2026-10-10 收集。包含此前列出的 5 篇期刊论文与 1 篇补充预印本。公开版本与出版社版本分别标注；未验证 SJTU 订阅权限。保守恒格式不自动等于可积离散化；连续极限不等于严格数值误差估计。</p><table><tr><th>年份</th><th>论文与原文链接</th><th>期刊</th><th>本地全文及版本</th></tr>' + ''.join(rows) + '</table></html>'
(DEST / 'literature_links_20261010.html').write_text(page, encoding='utf-8')
print('TOTAL', sum(p['status']=='PDF downloaded' for p in results), 'PDFs;', len(results), 'links', flush=True)
