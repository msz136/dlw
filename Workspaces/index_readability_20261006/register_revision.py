"""Merge the new index presentation into its existing workspace record."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
validation = json.loads((HERE / 'verification/validation.json').read_text(encoding='utf-8'))
assert validation['passed'] and not validation['failures'], validation['failures']
assert validation['source']['sha256'] == hashlib.sha256((ROOT / 'index.html').read_bytes()).hexdigest()

log = ROOT / 'PROGRESS_LOG.md'
text = log.read_text(encoding='utf-8')
marker = '**2026-10-06（Index阅读与算法展示）'
if marker not in text:
    match = re.search(r'> \*\*2026-09-30（Index方法递推）[\s\S]*?(?= \*\*2026-09-30（Git 工作区同步）)', text)
    assert match, 'Existing index topic missing'
    old = match.group(0)[2:]
    text = text[:match.start()] + '> ' + text[match.end():].lstrip()
    entry = (
        '> **2026-10-06（Index阅读与算法展示）：** [index.html](index.html) 开头压为两句，全文删去推论限制式与工程叙述。表3–5改为90个实际误差值的分场并列比较，42组逐行最小值加粗；算例与方案用合并单元格区分，表后各用短段解释结果。'
        'Euler局部图由36张二维热图改为12张全宽曲线，每图SD/SD2/FD蓝/橙/绿三条线，纵轴为24个y层上的最大绝对误差；同算例同场两网格共用线性纵轴。'
        '第2节新增SD、SD2、FD及共用Euler/RK4/ALE递推伪代码，按实际实现核对每级边界、离散lift及节点更新；16条原公式逐式保留。'
        '正文源、生成器与同文副本同步。90值与原CSV、42高亮、36条401点曲线及零峰值差核对通过；1280/390px公式、图像、链接、字重及无页面横溢出通过。'
        '脚本、数据核对、宽窄屏截图和修改前备份在 [Workspaces/index_readability_20261006/](Workspaces/index_readability_20261006/)。'
        '原独立36热图图集保留；本轮未新增PDE推进。 **此前递推公式整理（2026-09-30）：** '
        + old.split('：** ', 1)[1] + '\n\n'
    )
    text = entry + text
    log.write_text(text, encoding='utf-8')

index = ROOT / 'FILE_INDEX.md'
text = index.read_text(encoding='utf-8')
replacements = {
    '| [index.html](index.html) | DLW 数值比较主报告：三组孤子、SD／SD2／FD、Euler／RK4、固定／移动网格与误差图。 |':
    '| [index.html](index.html) | DLW 数值比较主报告：三组孤子、实际误差与最优值、递推伪代码、12张彩色误差曲线。 |',
    '| [dlw_waveform_fields.html](report/dlw_waveform_fields.html) | index 第 6 节的独立 Euler 局部误差图集；36 张图片源逐一相同，另有单图 PDF 下载。 |':
    '| [dlw_waveform_fields.html](report/dlw_waveform_fields.html) | Euler 局部误差热图集：36 张二维分布图，附单图 PDF 下载；index 第 6 节另以曲线比较。 |',
    '- [index.html](index.html)（《DLW孤子数值解的误差比较》；单孤子A/B与二孤子C的三方案、两时间法、两网格配对结果；A的SD2固定格空间限制用†标记）':
    '- [index.html](index.html)（《DLW孤子数值解的误差比较》；三组孤子的实际双场误差、42组最小值加粗、递推伪代码与12张Euler误差曲线；A的SD2固定格分辨率敏感性用†标记）',
    '- [DLW：Euler 局部误差分布](report/dlw_waveform_fields.html)（T=.01、x∈[-1,1]；18Euler组合，u/v、三方案、两网格分别绘成36张单图；index第6节同步）':
    '- [DLW：Euler 局部误差分布](report/dlw_waveform_fields.html)（T=.01、x∈[-1,1]；18Euler组合的36张原二维热图；index第6节采用相同保存误差的max_y曲线）',
    '（当前单面板绘图与两根HTML生成，build_reports.py入口转发）':
    '（原36张二维热图绘图与双页生成入口；当前index曲线修订由index_readability_20261006/revise_index.py生成）',
}
for old, new in replacements.items():
    if old in text:
        text = text.replace(old, new, 1)

anchor = '- `Workspaces/gsg_project/dlw_report/_src/index.md`、`_src/index.src.html`、`generate_index_report.py`（当前正文与生成入口）'
assert anchor in text
record = '''
- `Workspaces/index_readability_20261006/revise_index.py`、`algorithm_pseudocode.md`、`table_results.json`、`register_revision.py`（论文式阅读修订、实现核对伪代码、42组配对数据与合并登记）
- `Workspaces/index_readability_20261006/plot_error_curves.py`、`error_curves.fragment.html`、`error_curves.npz`、`curve_validation.json`（12图、36条401点max_y曲线与原峰值核对）
- `Workspaces/index_readability_20261006/figures/*.png/.pdf`（12张全宽曲线，三空间方案蓝/橙/绿，同算例同场统一纵轴）
- `Workspaces/index_readability_20261006/verification/check_index.cjs`、`verification/validation.json`、`verification/*.png`、`before/`（90原值、42最小值、公式/图像/链接及1280/390排版核验与修改前备份）'''
if '- `Workspaces/index_readability_20261006/revise_index.py`' not in text:
    text = text.replace(anchor, anchor + record, 1)
index.write_text(text, encoding='utf-8')

paths = [ROOT / 'index.html', ROOT / 'Workspaces/gsg_project/dlw_report/_src/index.md',
         ROOT / 'Workspaces/gsg_project/dlw_report/generate_index_report.py', HERE / 'algorithm_pseudocode.md',
         HERE / 'table_results.json', HERE / 'curve_validation.json', HERE / 'verification/validation.json']
manifest = [dict(path=path.relative_to(ROOT).as_posix(), bytes=path.stat().st_size,
                 sha256=hashlib.sha256(path.read_bytes()).hexdigest()) for path in paths]
(HERE / 'delivery_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Existing index topic, file index and delivery manifest updated.')
