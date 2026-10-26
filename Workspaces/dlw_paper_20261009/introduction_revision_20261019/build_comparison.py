from pathlib import Path
import html, re, json
import markdown

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
old = (HERE/'before_manuscript.md').read_text(encoding='utf-8')
current = (HERE.parent/'manuscript.md').read_text(encoding='utf-8')

def paragraphs(text, lang):
    start = text.index('## 1.', text.index('{#'+lang+'-title}'))
    stop = text.index('## 2.', start)
    return text[start:stop].strip().split('\n\n')[1:]

versions = {'old': {l: paragraphs(old,l) for l in ['en','zh']},
            'new': {l: paragraphs(current,l) for l in ['en','zh']}}
assert len(versions['old']['en']) == len(versions['old']['zh']) == 10
assert len(versions['new']['en']) == len(versions['new']['zh']) == 18

groups = [
 ('研究背景与研究对象', [1], [1,2], '新版第1段为新增背景，第2段改写研究对象的介绍。'),
 ('已有解析研究及 sinh-Gordon 联系', [2], [3,4,5,7], '原来的一段展开为多个段落；新版第5段新增近年对称性研究。'),
 ('可积离散化、误差参照与动网格', [3], [6,9,10,11], '将原段的多个论点拆开论述，补充方法背景、误差参照及二维网格条件。'),
 ('已有工作与本文问题的定位', [4], [8], '修正原稿对离散DLW研究空白的笼统判断。'),
 ('本文研究安排与贡献', [5,6,7,8,9], [12,13,14,15,16,17], '新增数值比较的总体安排，重新组织四项贡献并明确适用条件。'),
 ('文章结构', [10], [18], '保留原结构，补全各节研究内容。'),
]
seen={'old':[], 'new':[]}
def render(text):
    # The introduction only contains simple inline Latin variables and h^2.
    text=re.sub(r'\$([^$]+)\$', lambda m:'<i>'+html.escape(m[1])+'</i>',text)
    return markdown.markdown(text)
def column(version, indices):
    seen[version].extend(indices)
    heading='修改前' if version=='old' else '修改后'
    blocks=[]
    for n in indices:
        en=versions[version]['en'][n-1]
        zh=versions[version]['zh'][n-1]
        blocks.append(f'<div class="pair"><h4>{heading} · 第 {n} 段</h4><div class="english" lang="en"><span class="label">English 原文</span>{render(en)}</div><div class="chinese" lang="zh-CN"><span class="label">中文对应</span>{render(zh)}</div></div>')
    return f'<section class="version {version}"><h3>{heading}</h3>'+''.join(blocks)+'</section>'

sections=[]
nav=[]
for i,(title,oi,ni,note) in enumerate(groups,1):
    nav.append(f'<a href="#group-{i}">{i}. {title}</a>')
    sections.append(f'<section class="group" id="group-{i}"><h2>{i}. {title}</h2><p class="note">{note}</p><div class="columns">'+column('old',oi)+column('new',ni)+'</div></section>')
assert sorted(seen['old']) == list(range(1,11))
assert sorted(seen['new']) == list(range(1,19))

css='''*{box-sizing:border-box}body{margin:0;background:#fafaf8;color:#242424;font-family:Georgia,"Noto Serif SC","Microsoft YaHei",serif;line-height:1.8}main{max-width:1500px;margin:auto;padding:40px 28px}h1{font-size:30px;line-height:1.4}h2{font-size:23px;margin-top:0}h3{font-size:20px;margin:0 0 20px}h4{font-family:system-ui,sans-serif;font-size:14px;margin:0 0 14px;color:#565656}.intro,.note{color:#575757}nav{display:flex;gap:12px 24px;flex-wrap:wrap;margin:22px 0 40px}a{color:#245174;text-underline-offset:3px}.group{margin-bottom:48px;scroll-margin-top:20px}.columns{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start}.version{border:1px solid #d8d8d3;background:white;padding:24px;min-width:0}.old{border-top:4px solid #8c8277}.new{border-top:4px solid #477560}.pair+.pair{border-top:1px solid #ddd;margin-top:26px;padding-top:26px}.english p{font-size:17px;line-height:1.8;margin:8px 0 18px}.chinese{border-top:1px dashed #ddd;padding-top:12px}.chinese p{font-size:16px;line-height:1.9;margin:8px 0}.label{font:12px system-ui,sans-serif;letter-spacing:.03em;color:#606060}.footer{border-top:1px solid #ccc;padding-top:20px;color:#555}@media(max-width:900px){main{padding:24px 16px}.columns{grid-template-columns:1fr}.version{padding:20px}h1{font-size:25px}}@media print{body{background:white}main{padding:0}nav{display:none}.columns{display:block}.version{margin-bottom:20px}.pair{break-inside:avoid}a{color:inherit}}'''
page='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW Introduction｜逐段中英文修改对照</title><style>'+css+'</style></head><body><main><h1>DLW Introduction：逐段中英文修改对照</h1><p class="intro">左侧为修改前，右侧为修改后。每段先列英文原文，再列该版本对应的中文。按主题归组，段号保留各版本中的原始顺序；四项贡献及其引导语也分别计段。两版引言全文均完整收录，未以摘要代替。</p><p class="intro">修改前文字包含本轮已纠正的表述，仅供版本对照。中文均取自相应版本的论文译文。</p><nav>'+''.join(nav)+'</nav>'+''.join(sections)+'<p class="footer"><a href="dlw_paper_draft.html#en-intro">阅读当前英文 Introduction 及参考文献</a> · <a href="dlw_paper_draft.html#zh-intro">阅读当前中文译文</a></p></main></body></html>'
dest=ROOT/'report/dlw_introduction_comparison_20261019.html'
dest.write_text(page,encoding='utf-8')
result={'old_paragraphs_per_language':10,'new_paragraphs_per_language':18,'all_paragraphs_included_once':True,'text_source':'verbatim versioned manuscript paragraphs','output':str(dest)}
(HERE/'comparison_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
