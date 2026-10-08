"""Register the font correction and compact code view without replacing history."""
from pathlib import Path
import hashlib
import json
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    evidence=HERE/'registration_compact.json'
    if evidence.exists():
        data=json.loads(evidence.read_text('utf-8'))
        for item in data['files']:
            path=ROOT/item['path']
            assert path.exists() and sha(path)==item['sha256'],item['path']
        print(json.dumps({'success':True,'mode':'verify','files':len(data['files'])}))
        return
    content=json.loads((HERE/'content_validation.json').read_text('utf-8'))
    browser=json.loads((HERE/'browser_validation.json').read_text('utf-8'))
    assert content['success'] and browser['success']
    notebook=ROOT/'notebook'/'DLW数值分析report.ipynb'
    assert sha(notebook)=='10bd4b256d7ea80246d5cdd0dcf202a8f6bcec6e6cc41328f4b892bdc23a2cfe'
    progress=ROOT/'PROGRESS_LOG.md'
    original=progress.read_bytes().decode('utf-8')
    pattern=r'\*\*单文件静态报告（2026-10-07）：\*\*.*?\*\*此前记录：\*\*'
    summary='**单文件静态报告与字体精简（2026-10-07）：** 按当前33单元DLW notebook重建主目录 [index.html](index.html)，恢复旧版Times New Roman／宋体正文，修复字体内嵌规则跨越CSS右花括号导致的KaTeX字体回退；20条字体注册及数学基础样式完整，真实字形检查确认正文Times／SimSun与内嵌KaTeX_Math。页面只展开SD／SD2／FD右端、时间更新和公共点误差五段真实摘录，共27行；全部17块源码统一在文末默认收起，6张表、3张原图、117处公式与11项保存输出保留。当前notebook字节未改、未运行，仍可只发送一个离线HTML。内容逐项核对，断网且禁用JavaScript的Edge桌面／390px／打印、实际字体和附录展开检查通过。原index留档 [原HTML](report/DLW数值分析_原HTML_20261007.html)，精简前展开版及记录在新项目before_compact/，最新登记为registration_compact.json；源与证据见 [静态导出项目](Workspaces/dlw_notebook_static_20261007/README.md)。 **此前记录：**'
    assert len(re.findall(pattern,original))==1
    progress.write_bytes(re.sub(pattern,lambda _:summary,original,count=1).encode('utf-8'))
    index=ROOT/'FILE_INDEX.md'
    original=index.read_bytes().decode('utf-8')
    replacements=[
      ('当前 DLW notebook 的单文件静态报告：正文、静态源码与保存的表图；','当前 DLW notebook 的单文件静态报告：宋体论文正文、正确数学字体、5段关键代码及保存表图，完整源码在文末收起；'),
      ('保留推导、17 块源码、6 张保存表和 3 张曲线图','保留推导、5 段关键代码、6 张保存表和 3 张曲线图；完整源码默认收起'),
      ('DLW notebook 的静态单文件报告；无代码执行机制','DLW notebook 的静态单文件报告；恢复旧版正文与公式字体，关键代码5段／27行，完整实现收起'),
    ]
    for old,new in replacements:
        assert old in original,old
        original=original.replace(old,new,1)
    prefix='Workspaces/dlw_notebook_static_20261007/'
    addition='\r\n'.join('- ['+prefix+name+']('+prefix+name+')'+label for name,label in [
      ('register_compact.py','（当前精简版登记与只读核对入口）'),
      ('registration_compact.json','（当前交付、原件及修改前后记录的哈希）'),
      ('before_compact/','（精简前完整展开版、生成器、核验、截图和根记录字节备份）')])
    marker='<!-- DLW_NOTEBOOK_STATIC_INDEX_END -->'
    assert original.count(marker)==1
    index.write_bytes(original.replace(marker,addition+'\r\n'+marker,1).encode('utf-8'))
    paths=[ROOT/'index.html',notebook,progress,index]
    paths+=sorted(p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=evidence)
    result={'success':True,'files':[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p)} for p in paths],
      'notebook_unchanged':True,'visible_code_excerpts':5,'visible_code_lines':27,
      'records_before_sha256':{name:sha(HERE/'before_compact'/name) for name in ['PROGRESS_LOG.md','FILE_INDEX.md']},
      'records_after_sha256':{p.name:sha(p) for p in [progress,index]},'actual_fonts':browser['usedFonts']}
    evidence.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'success':True,'mode':'register','files':len(paths),'notebook_unchanged':True}))


if __name__=='__main__':
    main()
