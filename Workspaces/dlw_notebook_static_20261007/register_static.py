"""Merge the static export into existing DLW records, keeping originals."""
from pathlib import Path
import hashlib
import json
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    evidence=HERE/'registration.json'
    if evidence.exists():
        record=json.loads(evidence.read_text('utf-8'))
        for item in record['files']:
            path=ROOT/item['path']
            assert path.exists() and sha(path)==item['sha256'], item['path']
        print(json.dumps({'success':True,'mode':'verify','files':len(record['files'])}))
        return
    assert json.loads((HERE/'content_validation.json').read_text('utf-8'))['success']
    assert json.loads((HERE/'browser_validation.json').read_text('utf-8'))['success']
    before=HERE/'before'
    record_before={}
    for name in ['PROGRESS_LOG.md','FILE_INDEX.md']:
        path=ROOT/name
        original=path.read_bytes()
        backup=before/name
        assert not backup.exists()
        backup.write_bytes(original)
        record_before[name]=hashlib.sha256(original).hexdigest()
    progress=ROOT/'PROGRESS_LOG.md'
    text=progress.read_bytes().decode('utf-8')
    marker='> **2026-10-06（DLW数值分析笔记本）：**'
    assert text.count(marker)==1
    summary=' **单文件静态报告（2026-10-07）：** 按当前33单元DLW notebook原顺序重建主目录 [index.html](index.html)，正文、17块静态源码、117处数学表达及全部11项保存输出逐一对应，6张表与3张原图保留。公式预渲染为HTML/MathML，字体与PNG均内嵌，单个HTML可离线双击和直接发送；无运行按钮或JavaScript依赖。当前notebook字节未改、未重新执行。原index精确备份在新项目before/index.html，可阅读留档 [原HTML](report/DLW数值分析_原HTML_20261007.html)。内容比对、断网且禁用JavaScript的Edge桌面／390px／打印检查通过；源、验证与截图见 [静态导出项目](Workspaces/dlw_notebook_static_20261007/README.md)。 **此前记录：**'
    progress.write_bytes(text.replace(marker,marker+summary,1).encode('utf-8'))
    index=ROOT/'FILE_INDEX.md'
    text=index.read_bytes().decode('utf-8')
    old='| [index.html](index.html) | DLW 数值比较主报告；可运行版为 [DLW数值分析report.ipynb](notebook/DLW数值分析report.ipynb)：三组孤子、三种空间方案与时间推进、实际误差和曲线。 |'
    new='| [index.html](index.html) | 当前 DLW notebook 的单文件静态报告：正文、静态源码与保存的表图；双击离线打开或直接发送此文件。可运行原件为 [DLW数值分析report.ipynb](notebook/DLW数值分析report.ipynb)。 |'
    assert old in text
    text=text.replace(old,new,1)
    old='- [index.html](index.html)（《DLW孤子数值解的误差比较》；三组孤子的实际双场误差、42组最小值加粗、递推伪代码与12张Euler误差曲线；A的SD2固定格分辨率敏感性用†标记）'
    new='- [index.html](index.html)（当前 DLW notebook 的静态单文件导出：33 单元，保留推导、17 块源码、6 张保存表和 3 张曲线图；旧版保留在 report/DLW数值分析_原HTML_20261007.html）'
    assert old in text
    text=text.replace(old,new,1)
    prefix='Workspaces/dlw_notebook_static_20261007/'
    entries=[
        ('index.html','DLW notebook 的静态单文件报告；无代码执行机制'),
        ('report/DLW数值分析_原HTML_20261007.html','替换前 index 的可阅读留档；保留原相对链接'),
    ]
    files=['README.md','build_static.py','render_math.cjs','verify_static.py','check_static.cjs',
      'build_validation.json','content_validation.json','browser_validation.json',
      'report_1440.png','report_sd_1440.png','report_table_1440.png','report_figure_1440.png','report_390.png',
      'register_static.py','registration.json','before/index.html','before/PROGRESS_LOG.md','before/FILE_INDEX.md']
    entries.extend((prefix+name,'') for name in files)
    block='<!-- DLW_NOTEBOOK_STATIC_INDEX_BEGIN -->\r\n**DLW notebook 单文件静态报告（2026-10-07）：**\r\n\r\n'
    block+='\r\n'.join('- ['+path+']('+path+')'+('（'+description+'）' if description else '') for path,description in entries)
    block+='\r\n<!-- DLW_NOTEBOOK_STATIC_INDEX_END -->\r\n\r\n'
    marker='<!-- NOTEBOOK_REPORTS_INDEX_BEGIN -->'
    assert text.count(marker)==1 and 'DLW_NOTEBOOK_STATIC_INDEX_BEGIN' not in text
    index.write_bytes(text.replace(marker,block+marker,1).encode('utf-8'))
    tracked=[ROOT/'index.html',ROOT/'notebook'/'DLW数值分析report.ipynb',ROOT/'report'/'DLW数值分析_原HTML_20261007.html',progress,index]
    tracked+=sorted(p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='registration.json')
    record={'success':True,'files':[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p)} for p in tracked],
       'records_before_sha256':record_before,'records_after_sha256':{p.name:sha(p) for p in [progress,index]},
       'notebook_preserved':sha(ROOT/'notebook'/'DLW数值分析report.ipynb')==json.loads((HERE/'build_validation.json').read_text('utf-8'))['source_sha256']}
    assert record['notebook_preserved']
    evidence.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'success':True,'mode':'register','files':len(tracked),'notebook_preserved':True}))


if __name__=='__main__':
    main()
