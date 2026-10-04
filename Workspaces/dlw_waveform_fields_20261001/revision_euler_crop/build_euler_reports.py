"""Revise both paper pages to separate Euler error maps in x=[-1,1]."""
from pathlib import Path
import base64
import hashlib
import html
import json
import re
import subprocess
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
REPORT=ROOT/'Workspaces/gsg_project/dlw_report'
SOURCE=REPORT/'_src/index.md'
OUTPUT=ROOT/'report/dlw_waveform_fields.html'
BEGIN='<!-- DLW_SAVED_FIELDS_BEGIN -->'
END='<!-- DLW_SAVED_FIELDS_END -->'
NAMES={'fig1a':'单孤子 A','fig1b':'单孤子 B','fig3':'二孤子 C'}
PARAMETERS={'fig1a':'$(p,q)=(1,2)$','fig1b':'$(p,q)=(4,-3)$',
    'fig3':'$(p_1,q_1)=(6,-5)$，$(p_2,q_2)=(4,-3)$'}


def label(item):
    return NAMES[item['case']]+' · Euler · '+('固定网格' if item['mesh']=='fixed' else '动网格')+' · '+item['model']+' · '+item['field']


def figure(item,number,downloads=False):
    title=label(item)
    limit=f'{item["cropped_max"]:.3e}'
    dagger='†' if item['case']=='fig1a' and item['mesh']=='fixed' and item['model']=='SD2' else ''
    value=f'图 {number}　{title}{dagger}。窗口内最大绝对误差 {limit}。'
    block='<figure class="field-figure"><img src="'+item['png']+'" alt="'+html.escape(title+'，x从−1到1的单张绝对误差分布')+'" loading="lazy">'
    block+='<figcaption>'+value+'</figcaption></figure>'
    if downloads:block+='<p class="downloads"><a href="'+item['pdf']+'">此图 PDF</a></p>'
    return block


def grouped_figures(data,downloads=False):
    blocks=[];number=0
    for case in NAMES:
        letter={'fig1a':'A','fig1b':'B','fig3':'C'}[case]
        blocks.append(f'<h3 id="error-case-{letter}">{NAMES[case]}：Euler 误差分布</h3>')
        for mesh in ('fixed','moving'):
            for field in ('u','v'):
                name=('固定网格' if mesh=='fixed' else '动网格')+' · '+field+' 场 · SD / SD2 / FD'
                opened=' open' if mesh=='fixed' and field=='u' else ''
                blocks.append('<details class="field-details"'+opened+'><summary>'+name+'</summary>')
                for item in data['figures']:
                    if (item['case'],item['mesh'],item['field'])==(case,mesh,field):
                        number+=1
                        blocks.append(figure(item,number,downloads))
                blocks.append('</details>')
    assert number==36
    return '\n\n'.join(blocks)


def update_index(data):
    current=SOURCE.read_text(encoding='utf-8')
    section=[BEGIN,'## 6　Euler 局部误差分布',
        '取 $T=0.01$，只展示 Euler 的绝对误差分布，统一限制在 $x\\in[-1,1]$。每个算例、空间方案、网格和物理场各用一张图；$u$、$v$ 及三个方案分别展示。',
        '同一算例、同一物理场共用色标。色标采用平方根映射，刻度仍表示实际绝对误差。青色十字标出当前窗口内的误差峰值；图中 window max 仅指 $[-1,1]$ 窗口，与前文表格的全域误差指标分开。',
        '<p><a href="report/dlw_waveform_fields.html">Euler 误差分布图集</a>可查看所有单张图并下载 PDF。</p>',
        '<p class="table-note">† 单孤子 A 的 SD2 固定网格保留原空间加密对照未通过的标记。误差包含初始表示误差。</p>',
        grouped_figures(data),END]
    assert BEGIN in current and END in current
    updated=re.sub(re.escape(BEGIN)+r'[\s\S]*?'+re.escape(END),lambda m:'\n\n'.join(section),current,count=1)
    SOURCE.write_text(updated,encoding='utf-8')


def inline_images(soup):
    from PIL import Image
    for image in soup.find_all('img'):
        path=ROOT/image['src']
        image['src']='data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
        with Image.open(path) as pic:image['width'],image['height']=pic.size


def main():
    data=json.loads((HERE/'euler_plot_validation.json').read_text(encoding='utf-8'))
    update_index(data)
    subprocess.run(['python',str(REPORT/'generate_index_report.py')],check=True,cwd=ROOT)
    subprocess.run(['powershell','-NoProfile','-File',str(REPORT/'build_html.ps1')],check=True,cwd=ROOT)
    paper=BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'),'html.parser')
    styles='\n'.join(str(t) for t in paper.find_all('style'))
    scripts='\n'.join(str(t) for t in paper.find_all('script'))
    css='''<style>main{max-width:1000px;padding:50px 50px}h2{font-size:14pt}h3{margin-top:32px}
      .field-figure{max-width:780px;margin:24px auto 36px}img{display:block;max-width:100%}
      .downloads,.atlas-nav{text-indent:0;font-size:10.5pt}.downloads{text-align:center}
      @media(max-width:650px){main{padding:28px 16px}.field-figure{margin:20px 0}}
      @media print{details:not([open]){display:none}.downloads,.atlas-nav{display:none}}</style>'''
    body=['<h1>DLW：Euler 局部误差分布</h1>',
        '<p class="abstract">单孤子 A、B 与二孤子 C，在 $T=0.01$ 的 Euler 绝对误差。所有图统一取 $x\\in[-1,1]$，每张图展示一个空间方案、一个网格和一个物理场。</p>',
        '<p>同一算例、同一物理场共用色标；颜色采用平方根映射，刻度仍为实际绝对误差。青色十字表示当前窗口内的误差峰，window max 为该窗口内的最大值。横向采用原评价点，纵向保留原 24 个中点层。</p>',
        '<p class="table-note">† 单孤子 A 的 SD2 固定网格保留原空间加密对照未通过的标记。误差包含初始表示误差。</p>',
        '<p class="atlas-nav"><a href="#error-case-A">单孤子 A</a> · <a href="#error-case-B">单孤子 B</a> · <a href="#error-case-C">二孤子 C</a> · <a href="../index.html#section-6">返回主报告</a></p>',
        '<h2 id="euler-errors">Euler 误差分布</h2>']
    for case in NAMES:
        body.append(f'<p>{NAMES[case]}：{PARAMETERS[case]}。</p>')
    body.append(grouped_figures(data,downloads=True))
    body=[part.replace('href="Workspaces/', 'href="../Workspaces/') for part in body]
    source='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW：Euler 局部误差分布</title>'+styles+css+'</head><body><main>'+'\n'.join(body)+'</main>'+scripts+'</body></html>'
    (HERE/'euler_errors.src.html').write_text(source,encoding='utf-8')
    soup=BeautifulSoup(source,'html.parser');inline_images(soup)
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(str(soup),encoding='utf-8')
    # Original analytical sections and tables are unchanged in this revision.
    before=BeautifulSoup((HERE/'before/index.html').read_text(encoding='utf-8'),'html.parser')
    assert [x.get_text(' ',strip=True) for x in before.find_all('table')]==[x.get_text(' ',strip=True) for x in paper.find_all('table')]
    assert len(paper.find_all('img'))==36
    before_text=(HERE/'before/index.md').read_text(encoding='utf-8')
    now=SOURCE.read_text(encoding='utf-8')
    assert re.findall(r'\\tag\{\d+\}',before_text)==re.findall(r'\\tag\{\d+\}',now)
    files=[ROOT/'index.html',OUTPUT,SOURCE,HERE/'euler_plot_validation.json']
    result=dict(scope='Euler only, x=[-1,1], one distribution per figure',index_figures=36,atlas_figures=36,
        original_tables_unchanged=5,original_equations_unchanged=16,
        files=[dict(path=str(f),size=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in files])
    (HERE/'euler_delivery_manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='files'},ensure_ascii=False))


if __name__=='__main__':
    main()
