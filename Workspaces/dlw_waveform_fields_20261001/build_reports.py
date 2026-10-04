"""Current entry point: separate Euler error maps, x in [-1,1]."""
from pathlib import Path
import base64
import hashlib
import html
import json
import re
import shutil
import subprocess
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REPORT = ROOT / 'Workspaces/gsg_project/dlw_report'
BACKUP = HERE / 'before'
SOURCE = REPORT / '_src/index.md'
BEGIN = '<!-- DLW_SAVED_FIELDS_BEGIN -->'
END = '<!-- DLW_SAVED_FIELDS_END -->'
CASE_NAMES = {'fig1a': '单孤子 A', 'fig1b': '单孤子 B', 'fig3': '二孤子 C'}
PARAMETERS = {'fig1a': '$(p,q)=(1,2)$', 'fig1b': '$(p,q)=(4,-3)$',
              'fig3': '$(p_1,q_1)=(6,-5)$，$(p_2,q_2)=(4,-3)$'}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def backup():
    BACKUP.mkdir(exist_ok=True)
    paths = [ROOT/'index.html', SOURCE, REPORT/'_src/index.src.html',
             REPORT/'generate_index_report.py', ROOT/'Workspaces/dlw_error_inventory_20260929/CONTROLLED_RESULTS.md']
    for p in paths:
        target = BACKUP / p.name
        if not target.exists():
            shutil.copy2(p, target)


def caption(item):
    mesh = '固定网格' if item['mesh']=='fixed' else '动网格'
    return f'{CASE_NAMES[item["case"]]} · {item["method"]} · {mesh}'


def img(path, alt):
    return f'<img src="{path}" alt="{html.escape(alt)}" loading="lazy">'


def profile_figure(item, number):
    label = caption(item)
    return ('<figure class="field-figure">'+img(item['profiles'][0], label+'：u/v解析波形、数值节点与逐点绝对误差')+
        f'<figcaption>图 {number}　{label}。上行为 $u,v$ 波形，下行为同一 $y=-1/16$ 层的绝对误差。</figcaption></figure>')


def update_index(data):
    current = SOURCE.read_text(encoding='utf-8')
    if BEGIN in current:
        current = re.sub(re.escape(BEGIN)+r'[\s\S]*?'+re.escape(END)+r'\s*', '', current)
        current = current.replace('## 7　结论', '## 6　结论')
    current = current.replace('| 二孤子 C | SD2 | 1.189 | 11.345 |', '| 二孤子 C | SD2 | 1.190 | 11.345 |')
    sections = [BEGIN, '## 6　波形与误差分布',
        '在表 3–5 的同一终点 $T=0.01$，将连续解析波形与保存的数值场直接比较。沿用 `Report.html` 的曲线与节点叠加方式：红线为解析解，蓝圆点、绿方点、紫三角分别为 SD、SD2、FD 的实际保存节点。剖面取真实中点层 $y=-1/16$；下方曲线表示该层上的逐点绝对误差，不能将其峰值等同于全部 $y$ 层的最大误差。',
        '<p><a href="report/dlw_waveform_fields.html">完整二维波形与误差分布图集</a>给出三个算例、两种时间算法和两种网格的全部分布。二维图使用与式（1）相同的 4001 个 $x$ 评价点和 24 个 $y$ 中点层；同一算例、同一物理场共用色标，青色十字标出全场误差峰值。</p>',
        '<p class="table-note">† 单孤子 A 的 SD2 固定网格仍保留原有空间加密对照未通过的标记。误差包含初始表示误差。</p>']
    items = data['figures']
    number = 0
    for item in items:
        if (item['method'], item['mesh']) == ('RK4', 'fixed'):
            number += 1
            sections.append(profile_figure(item, number))
    for method, mesh in (('RK4', 'moving'), ('Euler', 'fixed'), ('Euler', 'moving')):
        label = method+' · '+('固定网格' if mesh=='fixed' else '动网格')
        sections.append(f'<details class="field-details"><summary>{label}：三个算例的波形与误差剖面</summary>')
        for item in items:
            if (item['method'], item['mesh']) == (method, mesh):
                number += 1
                sections.append(profile_figure(item, number))
        sections.append('</details>')
    sections.append(END)
    assert '## 6　结论' in current
    current = current.replace('## 6　结论', '\n\n'.join(sections)+'\n\n## 7　结论', 1)
    SOURCE.write_text(current, encoding='utf-8')


def atlas_source(data):
    blocks = ['<h1>DLW 孤子波形与误差分布</h1>',
        '<p class="abstract">在 $T=0.01$，比较单孤子 A、B 与二孤子 C 的 $u,v$ 数值波形和绝对误差。每个算例覆盖 SD、SD2、FD，Euler、RK4，以及固定、移动网格，共 36 组实验。</p>',
        '<p>二维波形图按列排列解析解与三个数值方案；误差图按列排列 SD、SD2、FD，上、下行分别为 $u,v$。同一算例、同一场的所有波形图共用幅值色标，所有误差图共用从零起的误差色标。误差色标采用平方根映射以显示较小误差，刻度仍为绝对误差值。青色十字为 4001×24 评价格点上的全场最大误差位置，图中 max 为该误差值。</p>',
        '<p>剖面图取实际保存层 $y=-1/16$：红线为解析解，彩色符号为原始数值节点；下行为同一层的逐点绝对误差。二维图只显示原 24 个 $y$ 层，沿 $x$ 使用与主报告相同的三次样条重构。色块在 $y$ 方向代表中点层所在的格带。</p>',
        '<p class="table-note">† 单孤子 A 的 SD2 固定网格在此时刻未通过空间加密对照。误差保留初始表示误差。</p>',
        '<p class="atlas-nav"><a href="#case-A">单孤子 A</a> · <a href="#case-B">单孤子 B</a> · <a href="#case-C">二孤子 C</a> · <a href="index.html#section-6">返回误差比较报告</a></p>']
    n = 0
    for case in CASE_NAMES:
        letter = case[-1] if case=='fig3' else {'fig1a': 'A', 'fig1b': 'B'}[case]
        if case=='fig3': letter='C'
        blocks.append(f'<h2 id="case-{letter}">{CASE_NAMES[case]}：波形与误差分布</h2>')
        blocks.append(rf'<p>{PARAMETERS[case]}，$a=2$、$c_i=1$，初相位为零；$N_x=256$、$h_y=1/8$、$\Delta t=1.25\times10^{{-4}}$。</p>')
        for item in data['figures']:
            if item['case'] != case: continue
            label = caption(item)
            is_default = item['method']=='RK4' and item['mesh']=='fixed'
            blocks.append('<details class="field-details"'+(' open' if is_default else '')+f'><summary>{label}</summary>')
            for kind, description in (('wavefields', '二维波形分布；两行为 $u,v$，四列为解析解、SD、SD2、FD'),
                                      ('errorfields', '二维绝对误差分布；全场误差峰用青色十字标出'),
                                      ('profiles', '$y=-1/16$ 层的波形及逐点绝对误差')):
                n += 1
                blocks.append('<figure>'+img(item[kind][0],label+'：'+description.replace('$',''))+
                    f'<figcaption>图 {n}　{label}。{description}。</figcaption></figure>')
            pdf = ' · '.join(f'<a href="{item[k][1]}">{name} PDF</a>' for k, name in (
                ('wavefields', '波形'), ('errorfields', '误差'), ('profiles', '剖面')))
            blocks.append(f'<p class="downloads">{pdf}</p></details>')
    blocks.append('<p class="table-note">数据：<a href="Workspaces/dlw_waveform_fields_20261001/field_errors.csv">72 项全场误差与峰值位置</a>。36 份保存场哈希核验通过；独立参照重算与原始表值的最大差小于 $10^{-12}$。</p>')
    return '\n'.join(blocks)


def inline_images(soup):
    for im in soup.find_all('img'):
        path = ROOT / im['src']
        im['src'] = 'data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
        from PIL import Image
        with Image.open(path) as pic:
            im['width'], im['height'] = pic.size


def main():
    data = json.loads((HERE/'plot_validation.json').read_text(encoding='utf-8'))
    backup()
    update_index(data)
    subprocess.run(['python', str(REPORT/'generate_index_report.py')], check=True, cwd=ROOT)
    subprocess.run(['powershell', '-NoProfile', '-File', str(REPORT/'build_html.ps1')], check=True, cwd=ROOT)
    page = BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'), 'html.parser')
    styles = '\n'.join(str(tag) for tag in page.find_all('style'))
    scripts = '\n'.join(str(tag) for tag in page.find_all('script'))
    additional = '''<style>
      main{max-width:1240px;padding:54px 48px}.atlas-nav,.downloads{text-indent:0}
      .field-details{margin:24px 0;border-top:1px solid #b7b7b7;padding-top:12px}
      summary{cursor:pointer;font-weight:bold;font-size:12pt}
      summary:focus-visible,a:focus-visible{outline:2px solid #1776bc;outline-offset:4px}
      figcaption{max-width:920px;margin:auto}figure{margin:20px 0 36px}
      .downloads{font-size:10.5pt}img{display:block;max-width:100%}
      @media(max-width:650px){main{padding:28px 16px}summary{font-size:11pt}}
      @media print{details:not([open]){display:none}.atlas-nav,.downloads{display:none}}
      </style>'''
    body = atlas_source(data).replace('href="Workspaces/', 'href="../Workspaces/').replace('href="index.html#', 'href="../index.html#')
    source = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW 孤子波形与误差分布</title>'+styles+additional+'</head><body><main>'+body+'</main>'+scripts+'</body></html>'
    (HERE/'waveform_fields.src.html').write_text(source, encoding='utf-8')
    soup = BeautifulSoup(source, 'html.parser')
    inline_images(soup)
    output = ROOT/'report/dlw_waveform_fields.html'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(str(soup), encoding='utf-8')
    files = [ROOT/'index.html', output, SOURCE,
             HERE/'plot_validation.json', HERE/'plotted_fields.npz', HERE/'field_errors.csv']
    result = dict(root_reports={p.name:dict(path=str(p), size=p.stat().st_size, sha256=sha(p)) for p in files[:2]},
                  sources=[dict(path=str(p), sha256=sha(p)) for p in files[2:]],
                  original_backups=str(BACKUP), index_profile_figures=12, atlas_figures=36,
                  index_rounding_correction='Table 4: C/SD2/u Euler-to-RK4 ratio 1.189 -> 1.190')
    (HERE/'delivery_manifest.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps(result['root_reports'], ensure_ascii=False))


if __name__ == '__main__':
    import runpy
    runpy.run_path(str(HERE/'revision_euler_crop/build_euler_reports.py'), run_name='__main__')
