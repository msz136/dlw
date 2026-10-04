"""Build the theory-first DLW idea report from the current registry."""
from pathlib import Path
import hashlib
import html
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
data = json.loads((HERE / 'ideas.json').read_text(encoding='utf-8'))
esc = html.escape
sections = []
for n, i in enumerate(data['ideas'], 1):
    cites = ' '.join(f'<a href="#ref-{s}">[{s[1:]}]</a>' for s in i['sources'])
    equations = ''.join(f'<p>{esc(e)}</p>' for e in i.get('equations', []))
    result = i.get('result_summary')
    if result:
        steps = ''.join(f'<h3>{esc(step["title"])}</h3><p>{esc(step["text"])}</p>' for step in result['steps'])
        details = ''.join(f'<p><strong>{esc(r["name"])}。</strong>{esc(r["text"])}</p>' for r in result['technical_results'])
        sections.append(f'''<section id="{i['id']}" data-status="{i['status']}">
<h2>{n}　{esc(i['title'])}</h2>
<p class="result"><strong>已得结论。</strong>{esc(result['plain_conclusion'])} {cites}</p>
<p class="conditions">{esc(result['scope'])}</p>
{steps}
<p><strong>对研究的含义。</strong>{esc(result['takeaway'])}</p>
<details><summary>定理要点与精确适用条件</summary>
<div class="equations">{equations}</div>{details}
<p><strong>理论预测。</strong>{esc(i['expectation'])}</p>
<p><strong>比较与自由度。</strong>{esc(i['comparison'])} {esc(i['minimal_variables'])}</p>
<p class="conditions"><strong>证明边界。</strong>{esc(i['falsifier'])}</p>
</details></section>''')
        continue
    sections.append(f'''<section id="{i['id']}">
<h2>{n}　{esc(i['title'])}</h2>
<p><strong>理论起点。</strong>{esc(i['known'])} {cites}</p>
<p><strong>研究目的。</strong>{esc(i['purpose'])} {esc(i['new_question'])}</p>
<div class="equations">{equations}</div>
<p><strong>理论预测。</strong>{esc(i['expectation'])}</p>
<p><strong>比较与自由度。</strong>{esc(i['comparison'])} {esc(i['minimal_variables'])}</p>
<p><strong>新增认识。</strong>{esc(i['new_increment'])}</p>
<p class="conditions"><strong>证明边界。</strong>{esc(i['falsifier'])}</p>
</section>''')

refs = []
for s in data['sources']:
    assert (ROOT / s['path']).is_file(), s['path']
    refs.append(f'<li id="ref-{s["id"]}"><a href="../{esc(s["path"], quote=True)}">{esc(s["title"])}</a>，{esc(s["sections"])}。</li>')
rows = ''.join(f'<tr><td><a href="#{i["id"]}">{n}</a></td><td>{esc(i["title"])}</td><td>{esc(i["priority"])}</td></tr>' for n, i in enumerate(data['ideas'], 1))
document = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="从谱曲率、离散重构、孤子流形与高频传播出发的四个DLW理论研究命题。">
<title>DLW：理论驱动的研究命题</title>
<style>
*{box-sizing:border-box}body{margin:0;color:#171717;background:#f2f1ef;font:17px/1.9 "Times New Roman","SimSun",serif}
main{max-width:1040px;margin:32px auto;padding:52px 70px 60px;background:white}
h1{font-size:29px;line-height:1.55;text-align:center;margin:0 0 8px;font-weight:600}
.date{text-align:center;font-size:14px;color:#666;margin-bottom:26px}
.abstract{border-top:1px solid #777;border-bottom:1px solid #777;padding:16px 0}
h2{font-size:22px;line-height:1.65;margin:34px 0 14px;break-after:avoid}
h3{font-size:18px;line-height:1.65;margin:22px 0 8px}.result{border-block:1px solid #999;padding:14px 0}details{margin:20px 0;padding:12px 0;border-top:1px solid #bbb}summary{cursor:pointer;font-weight:600}summary:focus-visible{outline:2px solid #284f69;outline-offset:4px}
p{margin:12px 0;text-align:justify;overflow-wrap:break-word}strong{font-weight:600}
a{color:#284f69;text-underline-offset:3px}a:focus-visible{outline:2px solid #284f69;outline-offset:4px}
table{border-collapse:collapse;width:100%;font-size:15px;border-top:1.5px solid #333;border-bottom:1.5px solid #333;margin:22px 0}
th,td{padding:8px 9px;text-align:left;vertical-align:top;border-bottom:1px solid #ddd}
th{border-bottom:1px solid #666}tr:last-child td{border-bottom:0}th:first-child,td:first-child{width:54px}th:last-child,td:last-child{width:92px}
.equations{margin:18px 0;padding:10px 16px;border-left:2px solid #aaa;background:#fafafa;font-size:16px;line-height:1.8}
.equations p{margin:8px 0;text-align:left;overflow-wrap:anywhere}
.conditions{font-size:15px;color:#444}.references{font-size:14px;line-height:1.85;padding-left:26px}
.scope{font-size:14px;color:#555;border-top:1px solid #bbb;padding-top:14px;margin-top:28px}
@media(max-width:700px){main{margin:0;padding:28px 20px 40px}body{font-size:16px}h1{font-size:24px}h2{font-size:20px}table{font-size:13px}th,td{padding:8px 5px}.equations{font-size:14px;padding:8px 11px}.conditions{font-size:14px}th:last-child,td:last-child{width:62px}}
@media print{body{background:white;font-size:11pt}main{max-width:none;margin:0;padding:0}h1{font-size:19pt}h2{font-size:14pt}.equations,.conditions,.references{font-size:10pt}a{color:inherit}table{font-size:10pt}}
</style></head><body><main>
<h1>DLW：理论驱动的研究命题</h1>
<p class="date">2026年10月1日</p>
<p class="abstract"><strong>摘要</strong>　研究起点应是方程与离散结构提出的数学问题。这里保留四个方向：结构参数的谱范围障碍、离散变量表示的等价性、孤子流形的不可去形变，以及统一精度所需的数据空间。先给出可证明或可否定的预测，再进入数值验证。后验排名与小幅误差差异不作为立题依据。</p>
<p>优化类主张以同一物理初边值和冻结指标下至少十倍的改善为目标；若声称双场改善，两场分别满足。定量下界、结构性反例和适用域定理本身也可构成成果。局部相位改善、参照拟合和总演化误差分别讨论，不互相替代。</p>
<table><thead><tr><th scope="col">编号</th><th scope="col">核心问题</th><th scope="col">定位</th></tr></thead><tbody>''' + rows + '''</tbody></table>
<p>已有三条结果：<a href="#T01">调准相位不保证真实场同比改善</a>；<a href="#T03">保留精确孤子不消除二阶波形形变</a>；<a href="#T04">高阶精度需要输入数据具有足够的高频衰减余量</a>。三者分别约束参数校准、结构保持和误差传播。T02的离散表示等价性仍为待研究命题。</p>
''' + '\n'.join(sections) + '''
<h2>先证明什么，再验证什么</h2>
<p>每条命题先固定比较对象、允许自由度、适用类及主要量，给出可复核的证明或带明确余项的预测；只有无法由现有理论排除、且可能达到数量级收益的优化主张，才进入数值验证。数值工作检验预测的系数、结构或失效条件，不据结果重新选择原命题。</p>
<h2>理论来源</h2><ol class="references">''' + '\n'.join(refs) + '''</ol>
<p class="scope">T01限于声明的谱族及指标；T03为静态局部族距离；T04限于声明的线性模型。三者尚不能合成一般非线性、共同初值下的有限时间双场误差定理。T02保留待研究命题。本页尚未判定文献原创性。<a href="../Workspaces/dlw_research_pipeline_20261001/ideas.json">命题与结果登记</a>；<a href="../Workspaces/dlw_theory_precision_domain_20261001/report.html">T04完整证明</a>。</p>
</main></body></html>'''
(HERE / '_src').mkdir(exist_ok=True)
(HERE / '_src' / 'dlw_research_ideas.html').write_text(document, encoding='utf-8')
output = ROOT / 'report/dlw_research_ideas.html'
output.parent.mkdir(exist_ok=True)
output.write_text(document, encoding='utf-8')
manifest = {
    'date': data['date'], 'revision': data['revision'],
    'ideas': [i['id'] for i in data['ideas']],
    'registry_sha256': hashlib.sha256((HERE / 'ideas.json').read_bytes()).hexdigest(),
    'html_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
    'source_links_checked': len(refs), 'new_pde_runs': 0,
    'basis': 'theory_first; historical numerical rankings excluded from motivation',
}
(HERE / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(manifest, ensure_ascii=False))
