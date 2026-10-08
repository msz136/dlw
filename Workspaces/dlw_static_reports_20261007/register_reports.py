"""Register the renamed numerical page and the new integrability page."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
STATIC=ROOT/'Workspaces'/'dlw_notebook_static_20261007'


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def update(path,text): path.write_bytes(text.encode('utf-8'))


def main():
    record_path=HERE/'registration.json'
    if record_path.exists():
        record=json.loads(record_path.read_text('utf-8'))
        for item in record['files']:
            path=ROOT/item['path']
            assert path.exists() and sha(path)==item['sha256'],item['path']
        print(json.dumps({'success':True,'mode':'verify','files':len(record['files'])}))
        return
    content=json.loads((HERE/'content_validation.json').read_text('utf-8'))
    browser=json.loads((HERE/'browser_validation.json').read_text('utf-8'))
    assert content['success'] and browser['success']
    assert not (ROOT/'index.html').exists()
    assert sha(ROOT/'dlw_numerical.html')==sha(HERE/'before'/'index.html')
    assert sha(ROOT/'notebook'/'DLW刘维尔可积性report.ipynb')==content['source_sha256']
    # Keep workspace conventions aligned with the user's explicit root names.
    agents=ROOT/'AGENTS.md'
    text=agents.read_bytes().decode('utf-8')
    old='theory_results.html / index.html / Report.html / dlw_hamilton.html'
    new='theory_results.html / dlw_numerical.html / Report.html / dlw_hamilton.html / dlw_integrability.html'
    assert old in text
    text=text.replace(old,new,1)
    old='主目录保留 theory_results.html、index.html、Report.html、dlw_hamilton.html'
    new='主目录保留 theory_results.html、dlw_numerical.html、Report.html、dlw_hamilton.html、dlw_integrability.html'
    assert old in text
    update(agents,text.replace(old,new,1))
    progress=ROOT/'PROGRESS_LOG.md'
    text=progress.read_bytes().decode('utf-8')
    marker='> **Notebook 展示（2026-10-07）：**'
    assert text.count(marker)==1
    summary=' **静态 HTML：** 新增主目录 [dlw_integrability.html](dlw_integrability.html)，从当前可积性 notebook 只读导出；31单元、100处数学与原式（1）—（19）对应，正文只展示7段关键Lean代码／31行，14项原始编译输出完整保留，参数／基础接口等长声明和完整代码集中收起。显式FactorSpectralFoundation条件及有限前缀范围原样保留。字体沿用Times New Roman／宋体与完整KaTeX；离线、禁用JavaScript的桌面／390px／打印及原生附录检查通过。原notebook未编辑、未运行、未重编Lean；导出、核对、截图与哈希见 [静态报告项目](Workspaces/dlw_static_reports_20261007/README.md)。 **此前记录：**'
    text=text.replace(marker,marker+summary,1)
    marker='> **2026-10-06（DLW数值分析笔记本）：**'
    assert text.count(marker)==1
    text=text.replace(marker,marker+' **入口改名（2026-10-07）：** 按用户要求将当前静态index.html直接改名为主目录 [dlw_numerical.html](dlw_numerical.html)，内容字节与改名前一致，生成器目标及当前索引同步更新。 **此前记录：**',1)
    text=text.replace('[index.html](index.html)','[dlw_numerical.html](dlw_numerical.html)')
    update(progress,text)
    index=ROOT/'FILE_INDEX.md'
    text=index.read_bytes().decode('utf-8')
    text=text.replace('[index.html](index.html)','[dlw_numerical.html](dlw_numerical.html)')
    text=text.replace('DLW 数值结果先看 `index.html`','DLW 数值结果先看 `dlw_numerical.html`')
    lines=text.splitlines(keepends=True)
    for i,line in enumerate(lines):
        if line.startswith('当前用户报告共12个：主目录保留4个入口'):
            lines[i]=line.replace('当前用户报告共12个：主目录保留4个入口','当前用户报告共13个：主目录保留5个入口')
    text=''.join(lines)
    table_row='| [dlw_numerical.html](dlw_numerical.html) |'
    assert text.count(table_row)==1
    lines=text.splitlines(keepends=True)
    for i,line in enumerate(lines):
        if line.startswith(table_row):
            lines.insert(i+1,'| [dlw_integrability.html](dlw_integrability.html) | 一般周期 DLW 刘维尔可积性 notebook 的静态报告；数学推导、关键 Lean 结论和原始编译输出，显式形式 PDO 基础条件保留。 |\r\n')
            break
    text=''.join(lines)
    prefix='Workspaces/dlw_static_reports_20261007/'
    entries=[('dlw_integrability.html','（新的单文件静态可积性报告）'),('dlw_numerical.html','（由index.html改名，内容字节未改）')]
    names=['README.md','build_integrability.py','verify_reports.py','check_reports.cjs','register_reports.py',
      'build_validation.json','content_validation.json','browser_validation.json','registration.json',
      'dlw_integrability_1440.png','dlw_integrability_390.png','integrability_conservation_1440.png','integrability_endpoint_1440.png',
      'dlw_numerical_1440.png','dlw_numerical_390.png','before/index.html','before/AGENTS.md','before/PROGRESS_LOG.md','before/FILE_INDEX.md',
      'before/build_static.py','before/check_static.cjs','before/README.md']
    entries.extend((prefix+name,'') for name in names)
    block='<!-- DLW_STATIC_REPORTS_INDEX_BEGIN -->\r\n**DLW 两份主目录静态报告（2026-10-07）：**\r\n\r\n'
    block+='\r\n'.join('- ['+p+']('+p+')'+label for p,label in entries)
    block+='\r\n<!-- DLW_STATIC_REPORTS_INDEX_END -->\r\n\r\n'
    marker='<!-- DLW_NOTEBOOK_STATIC_INDEX_BEGIN -->'
    assert text.count(marker)==1 and 'DLW_STATIC_REPORTS_INDEX_BEGIN' not in text
    update(index,text.replace(marker,block+marker,1))
    readme=STATIC/'README.md'
    text=readme.read_text('utf-8').replace('交付：根目录 `index.html`。','交付：根目录 `dlw_numerical.html`（按用户要求由 `index.html` 改名，内容字节保持）。',1)
    text+='\n## 当前文件名\n\n2026-10-07：主目录入口按用户要求改名为 `dlw_numerical.html`；此目录的生成器和浏览器检查已同步目标名。当前两页的核验与最新交付登记在 `Workspaces/dlw_static_reports_20261007/registration.json`；此前本目录的登记保持历史原样。\n'
    update(readme,text)
    paths=[ROOT/'dlw_numerical.html',ROOT/'dlw_integrability.html',agents,progress,index]
    paths+=sorted((ROOT/'notebook').glob('*.ipynb'))
    paths+=[STATIC/'build_static.py',STATIC/'check_static.cjs',STATIC/'README.md',STATIC/'render_math.cjs']
    paths+=sorted(p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=record_path)
    record={'success':True,'files':[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p)} for p in paths],
      'numerical_rename':{'from':'index.html','to':'dlw_numerical.html','content_unchanged':True,'sha256':sha(ROOT/'dlw_numerical.html')},
      'integrability_notebook_unchanged':True,'notebook_executed':False,
      'records_before_sha256':{name:sha(HERE/'before'/name) for name in ['AGENTS.md','PROGRESS_LOG.md','FILE_INDEX.md']},
      'records_after_sha256':{p.name:sha(p) for p in [agents,progress,index]}}
    record_path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'success':True,'mode':'register','files':len(paths),'notebook_unchanged':True}))


if __name__=='__main__': main()
