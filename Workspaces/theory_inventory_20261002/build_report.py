from pathlib import Path
import base64
import hashlib
import html
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ASSETS = ROOT / 'Workspaces/gsg_project/dlw_report/_assets/package/dist'
data = json.loads((HERE / 'inventory.json').read_text(encoding='utf-8'))

def esc(value):
    return html.escape(value, quote=False)

def source_link(source):
    name = source['label']
    if source.get('theorem'):
        name += ' · ' + source['theorem']
    if source.get('line'):
        name += '（第' + str(source['line']) + '行起）'
    return '<a href="' + html.escape(source['path'], quote=True) + '">' + esc(name) + '</a>'

blocks = []
for group in data['groups']:
    rows = []
    for result in group['results']:
        links = '；'.join(source_link(s) for s in result['sources'])
        rows.append(
            '<article id="' + result['id'] + '"><h3>' + result['id'] + '　' + esc(result['title']) + '</h3>'
            '<dl><dt>起点</dt><dd>' + esc(result['start']) + '</dd>'
            '<dt>结论</dt><dd>' + esc(result['conclusion']) + '</dd></dl>'
            '<p class="status"><strong>证据：</strong>' + esc(result['status']) + '。'
            + ('<span> ' + esc(result['scope']) + '</span>' if result.get('scope') else '') + '</p>'
            '<details class="proof"><summary>证明依据</summary><p>' + links + '</p></details></article>'
        )
    blocks.append('<section id="' + group['id'] + '"><h2>' + esc(group['title']) + '</h2><p class="intro">'
                  + esc(group['intro']) + '</p>' + ''.join(rows) + '</section>')

summary_rows = ''.join('<tr><td><a href="#' + row['target'] + '">' + esc(row['label']) + '</a></td>'
                       '<td>' + esc(row['start']) + '</td><td>' + esc(row['conclusion']) + '</td>'
                       '<td>' + esc(row['status']) + '</td></tr>' for row in data['summary'])

page = r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DLW与2HS：理论结果与命题结构</title>
<meta name="description" content="将现有Lean证明、解析推导、严格区间认证与待证问题整理为逐条的假设到结论。">
<style>@@KATEX_CSS@@</style><style>
:root{color-scheme:light;--ink:#191919;--muted:#555;--line:#ccc}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--ink);font-family:"Times New Roman","SimSun",serif;line-height:1.8;font-size:17px}
main{max-width:1060px;margin:46px auto 72px;padding:0 36px}header{text-align:center;border-bottom:1px solid #444;padding-bottom:20px}h1{font-size:29px;line-height:1.5;font-weight:600;margin:0 0 10px}.date{font-size:14px;color:var(--muted);margin:0}
h2{font-size:22px;line-height:1.55;margin:36px 0 12px}h3{font-size:18px;line-height:1.6;margin:0 0 10px}p{margin:12px 0}a{color:#1e4055;text-underline-offset:3px}nav{display:flex;flex-wrap:wrap;gap:8px 20px;margin:20px 0;font-size:14px}
.abstract{margin:24px 0}.tablewrap{overflow:auto;margin:18px 0}table{width:100%;border-collapse:collapse;font-size:15px;border-top:1.5px solid #222;border-bottom:1.5px solid #222}th{border-bottom:1px solid #555}td,th{text-align:left;vertical-align:top;padding:10px 12px}thead th{font-weight:600}td:first-child{width:18%}td:last-child{width:16%;font-size:14px}tbody tr+tr td{border-top:1px solid #e1e1e1}
.chain{padding:13px 0;border-top:1px solid #aaa;border-bottom:1px solid #aaa;line-height:2;font-size:17px}.intro{font-size:15px;color:var(--muted)}article{padding:20px 0;border-bottom:1px solid var(--line);scroll-margin-top:20px}dl{display:grid;grid-template-columns:42px minmax(0,1fr);column-gap:15px;row-gap:7px;margin:8px 0}dt{font-weight:600}dd{margin:0;min-width:0;overflow-wrap:anywhere}.status{font-size:14px;color:var(--muted);margin:11px 0 6px}.status strong{color:var(--ink)}details{font-size:14px}summary{cursor:pointer;text-decoration:underline;text-decoration-color:#999;text-underline-offset:3px}details p{margin:6px 0;overflow-wrap:anywhere}.katex{font-size:1.03em}.katex-display{overflow-x:auto;overflow-y:hidden;padding:4px 0}.proof .katex{font-size:1em}.eq{overflow-x:auto;overflow-y:hidden;margin:14px 0;padding:4px 0}.foot{font-size:14px;color:var(--muted)}.template{border-top:1px solid #999;border-bottom:1px solid #999;padding:12px 0}.template p{margin:6px 0}ol{padding-left:24px}li{margin:8px 0}footer{border-top:1px solid #555;padding-top:14px;margin-top:30px;font-size:14px}
@media(max-width:650px){body{font-size:16px}main{padding:0 18px;margin:25px auto 48px}h1{font-size:24px}h2{font-size:20px}h3{font-size:17px}table{min-width:780px}dl{grid-template-columns:36px minmax(0,1fr);gap:7px 10px}.katex{font-size:.98em}nav{gap:6px 14px}}
@media print{main{max-width:none;margin:0;padding:0}a{color:inherit}details.proof{display:none}table{font-size:12px}article{break-inside:avoid}nav{display:none}}
</style></head><body><main>
<header><h1>DLW与2HS：理论结果与命题结构</h1><p class="date">现有成果整理　2026年10月2日</p></header>
<p class="abstract"><strong>摘要。</strong>现有成果可分为精确结构、二阶一致性与残差、参数校准限制、孤子族几何、线性传播的适用空间以及守恒坐标。下文把每项写成明确的起点与结论，并保留证明所需的条件。形式化证明、解析推导、严格区间认证和数值观察分别标明；数值排名只作为验证材料。</p>
<nav aria-label="目录"><a href="#overview">结果总览</a><a href="#lean">Lean已证部分</a><a href="#dlw">DLW解析结果</a><a href="#hs">2HS理论结果</a><a href="#writing">命题的组织方式</a><a href="#gaps">待完成的结论</a></nav>
<section id="overview"><h2>1　结果总览</h2>
<p>此前所说的“连续双线性到离散双线性”，准确含义是：<strong>指定任意 (N) Gram 解族的有限 (h) 精确双线性构造、连续双线性极限与二阶一致性已经由 Lean 证明。</strong>这一构造不意味着任意连续双线性解直接采样后，都精确满足有限 (h) 离散方程。</p>
<div class="tablewrap"><table><thead><tr><th>结果组</th><th>起点／假设</th><th>结论</th><th>现有证据</th></tr></thead><tbody>@@SUMMARY@@</tbody></table></div>
<p class="foot">下列编号按数学内容归并。32个Lean冻结目标是技术契约，合并后并非32个独立研究定理。文中“当前工作新增”仅指本工作区的增量，文献原创性尚需查重。</p></section>
@@BLOCKS@@
<section id="writing"><h2>5　怎样整理为逐条命题</h2>
<p>先固定结论讨论的对象：方程残差、两个精确解族的静态距离、共同初值的演化误差、模态频率误差或网格几何。随后写出允许变化的参数、边界与范数，使每条箭头有完整的起点。</p>
<div class="template"><p><strong>命题标题。</strong>直接写要得到的数学性质。</p><p><strong>假设。</strong>方程与参数域；正则性和非零条件；边界、初值、评价域和范数；哪些量固定、哪些量趋零。</p><p><strong>结论。</strong>给出恒等式、不等式、存在唯一性、渐近阶或反例；明确常数依赖与量词。</p><p><strong>证明。</strong>引用已有引理，再给本命题的关键一步。数值核验另列为验证，不充当一般证明。</p></div>
<p>建议先形成六个主命题：精确非线性化（L03）；一般解的二阶残差（D01）；完整孤子族不可去形变（D09）；两参数校准的谱范围与初速限制（D06、D08）；共同初值纠正公式（D03、D07）；高阶精度的数据空间（D11、D12）。守恒坐标、显式谱结构和离散表示反例分别作为支线。</p>
<p class="chain">DLW：精确双线性构造 → 物理闭合 → 二阶残差 → 静态形变与参数限制<br>演化支线：共同物理初值 → 受迫线性化 → 传播与余项控制 → 指定时刻场误差<br>2HS：守恒坐标 → 同状态右端差 → 校准 → 胞元残差系数 → 局部选参条件</p>
<p>这些链条在论文中宜分成“引理—命题—推论”：换元、主子式和Taylor恒等式作引理；不可去形变、校准下界和Gaussian适用域作主命题；严格残差包围、十倍门槛和特定孤子正性作推论。两个系统可以采用同一叙述方式，各自保留方程与证明。</p></section>
<section id="gaps"><h2>6　尚未获得的结论</h2><ol>
<li><strong>当前初边值问题在指定终点的非线性双场误差上下界。</strong>已有残差、初始增长率和条件误差公式，尚需包围真实传播、边界响应和高阶余项。</li>
<li><strong>当前开链SD/SDR在允许状态上的完整坐标等价。</strong>周期非单射反例已成立；真实边界下的单射性、动力可投影性及受限状态类的演化闭合仍待证明。</li>
<li><strong>线性Gaussian结论到孤子背景、非线性问题及实际全离散求解器的推广。</strong>周期零背景的精确频率论证还不能代替这些传播分析。</li>
<li><strong>一般初值的完整逆散射理论。</strong>显式Gram解族、Darboux关系和非平凡谱渐近比已有，直接／逆变换及完备性未建立。</li>
</ol><p>“某方案在已有算例中更准”“动网格更好”“加密后误差反增”属于数值发现。若要成为定理，须先指定适用类和指标，再补上统一估计或严格反例。</p></section>
<footer>完整证明入口：<a href="report/dlw_error_theory.html">DLW误差推导</a>；<a href="report/dlw_research_ideas.html">T01—T04研究结果</a>。逐条证明材料由各条“证明依据”链接给出。</footer>
</main><script>@@KATEX_JS@@</script><script>
document.addEventListener('DOMContentLoaded',()=>{renderMathInElement(document.querySelector('main'),{delimiters:[{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false}],throwOnError:true});document.documentElement.dataset.mathReady='true';});
</script></body></html>'''
page = page.replace('@@SUMMARY@@', summary_rows).replace('@@BLOCKS@@', ''.join(blocks))
css = (ASSETS / 'katex.min.css').read_text(encoding='utf-8')
fonts = []
def embed(match):
    file = ASSETS / 'fonts' / match[1]
    mime = {'.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf'}[file.suffix]
    fonts.append(file.name)
    return 'url(data:' + mime + ';base64,' + base64.b64encode(file.read_bytes()).decode() + ')'
css = re.sub(r'url\((?:"|\x27)?fonts/([^\)"\x27]+)(?:"|\x27)?\)', embed, css)
js = (ASSETS / 'katex.min.js').read_text(encoding='utf-8') + '\n' + (ASSETS / 'contrib/auto-render.min.js').read_text(encoding='utf-8')
page = page.replace('@@KATEX_CSS@@', css).replace('@@KATEX_JS@@', js)
assert '@@' not in page
output = ROOT / 'theory_results.html'
output.write_text(page, encoding='utf-8')
source_hashes = {}
for group in data['groups']:
    for result in group['results']:
        for source in result['sources']:
            file = ROOT / source['path']
            assert file.exists(), source['path']
            source_hashes[source['path']] = hashlib.sha256(file.read_bytes()).hexdigest()
manifest = {'date': data['date'], 'output': str(output), 'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
            'result_count': sum(len(g['results']) for g in data['groups']), 'fonts_embedded': len(fonts),
            'source_hashes': source_hashes, 'new_mathematical_proofs': False, 'new_pde_runs': 0,
            'lean_audit': data['lean_audit']}
(HERE / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in manifest.items() if k not in ['source_hashes', 'lean_audit']}, ensure_ascii=False))
