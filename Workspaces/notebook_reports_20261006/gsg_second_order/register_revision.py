"""Record the GSG-aligned spatial revision after execution and report validation."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ROOT = PROJECT.parents[1]
STATIC = ROOT/'Workspaces/dlw_notebook_static_20261007'
BACKUP = PROJECT/'before_gsg_second_order'

def read(path):
    return json.loads(path.read_text('utf-8'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

data = read(PROJECT/'dlw_numeric_results.json')
old = read(BACKUP/'Workspaces/notebook_reports_20261006/dlw_numeric_results.json')
key = lambda r: (r['case'], r['model'], r['method'], r['mesh'])
old_rows = {key(r): r for r in old['rows']}
comparison = [dict(case=r['case'], model=r['model'], method=r['method'], mesh=r['mesh'],
    old_errors=old_rows[key(r)]['errors'], new_errors=r['errors'],
    new_over_old={f:r['errors'][f]/old_rows[key(r)]['errors'][f] for f in ('u','v')})
    for r in data['rows']]
(HERE/'result_comparison.json').write_text(json.dumps(comparison, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
delivery = read(HERE/'dlw_delivery_validation.json')
spatial = read(HERE/'verify_second_order_spatial.json')
execution = read(PROJECT/'dlw_execution_validation.json')
content = read(STATIC/'content_validation.json')
browser = read(STATIC/'browser_validation.json')
assert delivery['success'] and spatial['success'] and execution['success']
assert execution['image_outputs'] == 3
assert content['success'] and browser['success']
notebook = ROOT/'notebook/DLW数值分析report.ipynb'
html = ROOT/'dlw_numerical.html'
assert delivery['notebook_sha256'] == sha(notebook)

sources = ['dlw_numeric_cells.py', 'sd_tau_cell.py', 'tau_report_cells.py',
           'revise_dlw_structure.py', 'build_dlw_numerics_notebook.py',
           'execute_dlw_notebook.py', 'verify_dlw_tau.py',
           'verify_second_order_spatial.py', 'verify_direct_tau_delivery.py']
artifacts = [notebook, html, *(PROJECT/name for name in sources),
    PROJECT/'dlw_numeric_results.json', PROJECT/'dlw_numeric_curves.npz',
    PROJECT/'dlw_execution_validation.json', HERE/'verify_second_order_spatial.json',
    HERE/'verify_dlw_tau.json', HERE/'dlw_delivery_validation.json',
    HERE/'result_comparison.json', STATIC/'build_validation.json',
    STATIC/'content_validation.json', STATIC/'browser_validation.json']
manifest = dict(date='2026-10-07', source_reference={
    'title':'Integrable semi-discretizations and self-adaptive moving mesh method for a generalized sine-Gordon equation',
    'authors':'Bao-Feng Feng, Han-Han Sheng, Guo-Fu Yu',
    'doi':'10.1007/s11075-023-01504-1', 'paper_page':364, 'pdf_page':14,
    'scheme':5, 'equations':['4.13','4.14'],
    'local_pdf':'Paper/sources/Numerical_Algorithms_gsg (1).pdf',
    'interpretation':'GSG directly uses the three-point second derivative. DLW D1 uses the standard three-point centered first derivative; moving D2 follows the hodograph chain rule.'},
    old_spatial_order=4, new_spatial_order=2,
    operators={'Dxi':'(f[i+1]-f[i-1])/(2*dx)',
        'Dxxi':'(f[i+1]-2*f[i]+f[i-1])/dx**2',
        'D1':'Dxi(f)/J', 'D2':'Dxxi(f)/J**2-Dxi(J)*Dxi(f)/J**3'},
    configuration=read(PROJECT/'dlw_build_validation.json')['configuration'],
    time_methods={'SD':'Midpoint','SD2':['Euler','RK4'],'FD':['Euler','RK4']},
    primary_runs=24, additional_time_refinement_runs=12,
    code_cells=17, executed_cells=execution['executed_cells'],
    image_outputs=execution['image_outputs'], execution_seconds=execution['seconds'],
    sd_midpoint_order_range=delivery['sd_midpoint_order_range'],
    sd2_euler_order_range=delivery['sd2_euler_order_range'],
    initial_node_field_maximum_difference=delivery['initial_maximum_evaluation_node_error'],
    independent_raw_bilinear_relative_residual=delivery['independent_raw_bilinear_max_relative_residual'],
    spatial_audit=spatial,
    presentation={'sections':7, 'table_of_contents':False, 'code_appendix':False,
                  'tables':'five three-line tables', 'local_error_figures':3},
    backup='Workspaces/notebook_reports_20261006/before_gsg_second_order/',
    file_hashes={p.relative_to(ROOT).as_posix():sha(p) for p in artifacts},
    images_sha256={p.name:sha(p) for p in HERE.glob('dlw_notebook_figure_*.png')},
    browser_screenshots_sha256={p.name:sha(p) for p in STATIC.glob('report_*.png')})
(HERE/'revision_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

progress = ROOT/'PROGRESS_LOG.md'
text = progress.read_text('utf-8')
marker = '> **2026-10-06（DLW数值分析笔记本）：** '
note = ('**GSG三点二阶对齐（2026-10-07）：** 核对 GSG 原文第364页式(4.13)–(4.14)，'
    '将当前Notebook的x向五点四阶替换为三点二阶D1与直接三点D2；动格同步Jacobian链式公式、'
    'SD线性矩阵与SD2跃量延拓。保持256节点、dt=0.000125、T=0.01和时间算法，'
    f'17代码单元全量重跑（{execution["seconds"]:.3f}秒），24组主试验与12组时间细化完成，更新6表3图及主HTML。'
    '独立固定／动格制造解空间阶约2；SD双线性相对残差≤1.10e-10，初始物理场节点差≤1.67e-12；'
    'SD中点时间阶1.995–2.000、SD2 Euler阶0.995–1.000。主HTML保留七节、无目录和完整代码附录、五张三线表；'
    '离线桌面／390px／打印与字体检查通过。源、旧新误差逐值比较与交付证据见 '
    '[GSG对齐记录](Workspaces/notebook_reports_20261006/gsg_second_order/README.md)，四阶原件保存在before_gsg_second_order。 ')
if note not in text:
    assert marker in text
    progress.write_text(text.replace(marker,marker+note,1), encoding='utf-8')

index = ROOT/'FILE_INDEX.md'
text = index.read_text('utf-8')
begin = '<!-- DLW_GSG_SECOND_ORDER_INDEX_BEGIN -->'
end = '<!-- DLW_GSG_SECOND_ORDER_INDEX_END -->'
paths = [HERE/'README.md', PROJECT/'requirements_dlw.txt', HERE/'register_revision.py',
         HERE/'revision_manifest.json', *artifacts]
paths = list(dict.fromkeys(paths))
block = begin+'\n**DLW 三点二阶空间差分（2026-10-07）：**\n\n'+ '\n'.join(
    f'- [{p.relative_to(ROOT).as_posix()}]({p.relative_to(ROOT).as_posix()})' for p in paths)+'\n'+end
if begin in text:
    text = re.sub(re.escape(begin)+r'.*?'+re.escape(end), lambda _:block, text, flags=re.S)
else:
    text += '\n\n'+block+'\n'
index.write_text(text, encoding='utf-8')
(HERE/'record_snippets.json').write_text(json.dumps(dict(progress_note=note,index_block=block), ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(success=True, primary_runs=24, images=3, notebook_sha256=sha(notebook), html_sha256=sha(html)), indent=2))
