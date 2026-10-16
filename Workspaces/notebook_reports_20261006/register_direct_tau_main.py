"""Merge the completed direct-tau main report into its existing topic."""
from pathlib import Path
import hashlib
import json
import re
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def read_json(path):
    return json.loads(path.read_text('utf-8'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    execution = read_json(HERE/'dlw_execution_validation.json')
    delivery = read_json(HERE/'dlw_delivery_validation.json')
    audit = read_json(HERE/'verify_dlw_tau.json')
    static = ROOT/'Workspaces/dlw_notebook_static_20261007'
    content = read_json(static/'content_validation.json')
    browser = read_json(static/'browser_validation.json')
    build = read_json(static/'build_validation.json')
    assert audit['passed'] and all(d['success'] for d in (execution,delivery,content,browser))
    notebook = ROOT/'notebook/DLW数值分析report.ipynb'
    report = ROOT/'dlw_numerical.html'
    assert sha(notebook)==delivery['notebook_sha256']
    for name in ('PROGRESS_LOG.md','FILE_INDEX.md'):
        target = HERE/'before_direct_tau'/name
        if not target.exists():
            shutil.copy2(ROOT/name,target)
    path = ROOT/'PROGRESS_LOG.md'
    # Patch only the existing DLW numerical topic; never print its long history.
    original = path.read_bytes().decode('utf-8')
    pattern = re.compile(r'(^> \*\*\d{4}-\d{2}-\d{2}（DLW数值分析笔记本）：\*\* )([^\r\n]*)',re.MULTILINE)
    matches = list(pattern.finditer(original))
    assert len(matches)==1
    match = matches[0]
    history = re.sub(r'^\*\*2026-10-07直接τ：\*\* .*? \*\*既有记录：\*\* ', '', match.group(2))
    history = re.sub(r'^\*\*2026-10-07主报告直接τ：\*\* .*? \*\*既有记录：\*\* ', '', history)
    note = ('**2026-10-07主报告直接τ：** [Notebook](notebook/DLW数值分析report.ipynb) 与 '
        '[主HTML](dlw_numerical.html) 已同步替换原SD P/W为原始双线性τ隐式中点，'
        '展示B方程到F新层、G下一层的两次线性递推；三方案共同连续u/v初值，SD含动格中点ALE。'
        '24组主试验及12组时间细化全部完成T=0.01，17代码单元实际执行并保存6表3图；'
        'SD时间阶1.979–2.000，初值评价区间差1.064e-12，SD2/FD的36个保留误差值不变。'
        '独立raw B残差≤1.27e-10，原P/W与解析内点重置均不参与SD。'
        '结论、局部曲线和时间方法标签按新结果更新，删除防御性段落；离线桌面/窄屏/打印检查通过。'
        '有限h Gram专项12组试验另见 [推导与结果](report/dlw_direct_tau.html)。'
        '源与证据在 `Workspaces/notebook_reports_20261006/` 和 `Workspaces/dlw_notebook_static_20261007/`。'
        ' **既有记录：** ')
    updated = match.group(1)+note+history
    original = original[:match.start()]+updated+original[match.end():]
    path.write_bytes(original.encode('utf-8'))

    path = ROOT/'FILE_INDEX.md'
    original = path.read_bytes().decode('utf-8')
    original = original.replace('当前用户报告共13个：主目录保留5个入口，8个专题页面位于',
        '当前用户报告共14个：主目录保留5个入口，9个专题页面位于',1)
    original = original.replace('5段关键代码及保存表图','直接双线性SD递推、关键代码及最新保存表图',1)
    original = original.replace('保留推导、5 段关键代码、6 张保存表和 3 张曲线图',
        '保留直接双线性SD推导、6 段关键代码、6 张保存表和 3 张曲线图',1)
    original = original.replace('关键代码5段／27行，完整实现收起',
        f"直接双线性SD递推，关键代码{build['visible_code_excerpts']}段／{build['visible_code_lines']}行，完整实现收起",1)
    original = original.replace('（当前主交付；DLW 三组孤子与空间、时间方案数值比较）',
        '（当前主交付；SD原始τ中点递推、SD2/FD比较；24组主试验及12组时间细化已执行）',1)
    begin,end = '<!-- DLW_TAU_MAIN_INDEX_BEGIN -->','<!-- DLW_TAU_MAIN_INDEX_END -->'
    names = ['sd_tau_cell.py','tau_report_cells.py','integrate_direct_tau.py',
        'finalize_direct_tau_text.py','verify_dlw_tau.py','verify_dlw_tau.json',
        'verify_direct_tau_delivery.py','sd_tau_validation.json','register_direct_tau_main.py',
        'direct_tau_main_manifest.json','before_direct_tau/']
    prefix = 'Workspaces/notebook_reports_20261006/'
    newline = '\r\n' if '\r\n' in original else '\n'
    block = newline.join([begin,'','**DLW 主报告直接双线性 τ 更新（2026-10-07）：**','',
        *['- ['+prefix+n+']('+prefix+n+')' for n in names],'',end])
    if begin in original:
        original = re.sub(re.escape(begin)+'.*?'+re.escape(end),lambda _:block,original,flags=re.DOTALL)
    else:
        anchor = '<!-- NOTEBOOK_REPORTS_INDEX_END -->'
        assert anchor in original
        original = original.replace(anchor,block+newline+newline+anchor,1)
    path.write_bytes(original.encode('utf-8'))
    paths = [notebook,report,HERE/'sd_tau_cell.py',HERE/'tau_report_cells.py',
        HERE/'dlw_numeric_cells.py',HERE/'build_dlw_numerics_notebook.py',HERE/'revise_dlw_structure.py',
        HERE/'dlw_numeric_results.json',HERE/'dlw_numeric_curves.npz',HERE/'verify_dlw_tau.json',
        HERE/'dlw_execution_validation.json',HERE/'dlw_delivery_validation.json',
        static/'build_static.py',static/'build_validation.json',static/'content_validation.json',
        static/'browser_validation.json',ROOT/'PROGRESS_LOG.md',ROOT/'FILE_INDEX.md']
    manifest = dict(success=True,date='2026-10-07',primary_runs=24,time_refinement_runs=12,
        notebook=str(notebook),report=str(report),sd_method='Original tau implicit midpoint',
        sd_time_order_range=delivery['sd_midpoint_order_range'],
        files={p.relative_to(ROOT).as_posix():sha(p) for p in paths})
    (HERE/'direct_tau_main_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(success=True,primary_runs=24,time_refinement_runs=12,indexed_new_files=len(names))))

if __name__=='__main__':
    main()
