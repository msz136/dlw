from pathlib import Path
import shutil,json,hashlib,re
import nbformat
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
record=json.loads((HERE/'execution_validation.json').read_text(encoding='utf-8'))
assert record['success'] and not record['errors']
source=HERE/'DLW理论.executed.ipynb'
n=nbformat.read(source,as_version=4)
planned=nbformat.read(HERE/'DLW理论.input.ipynb',as_version=4)
assert len(n.cells)==len(planned.cells)
assert all(a.source==b.source for a,b in zip(n.cells,planned.cells))
assert all(c.execution_count is not None for c in n.cells if c.cell_type=='code')
outputs='\n'.join(o.get('text','') for c in n.cells if c.cell_type=='code' for o in c.outputs if o.output_type=='stream')
assert 'sorryAx' not in outputs and 'error(' not in outputs
footprints=re.findall(r'depends on axioms: \[([^]]*)\]',outputs)
assert len(footprints)>=18,len(footprints)
assert all(set(x.strip() for x in f.split(',')) <= {'propext','Classical.choice','Quot.sound'} for f in footprints)
alltext='\n'.join(c.source for c in n.cells)
assert 'dlw_residual' not in alltext and 'matplotlib' not in alltext and '空间残差与一致性' not in alltext
dest=ROOT/'notebook/DLW理论.ipynb'
if dest.exists():
    assert sha(dest)==sha(source),'An unexpected delivery already exists'
else:shutil.copy2(source,dest)
original=ROOT/'notebook/非线性化report.ipynb'
if original.exists():
    assert sha(original)==sha(HERE/'before/非线性化report.ipynb'),'Original changed during this task'
    trash=(ROOT/'Trash/dlw_theory_notebook_20261008').resolve()
    assert trash.is_relative_to((ROOT/'Trash').resolve())
    trash.mkdir(parents=True,exist_ok=True)
    assert not (trash/original.name).exists()
    shutil.move(str(original),str(trash/original.name))

edits={
 'report/notebook_usage.html': [('非线性化report.ipynb','DLW理论.ipynb'),('非线性化 report','DLW 理论'),('DLW 两套非线性化的推导与 Lean 证明，附空间残差估计。','连续 DLW、半离散双线性构造、τ 解与连续极限的推导和 Lean 证明。')],
 'Workspaces/report_colab_20261006/README.md': [('非线性化](../../notebook/非线性化report.ipynb)','DLW理论](../../notebook/DLW理论.ipynb)')],
}
for relative,replacements in edits.items():
    p=ROOT/relative
    before=HERE/'before'/relative
    before.parent.mkdir(parents=True,exist_ok=True)
    if not before.exists():shutil.copy2(p,before)
    t=p.read_text(encoding='utf-8')
    for a,b in replacements:t=t.replace(a,b)
    p.write_text(t,encoding='utf-8')

progress=ROOT/'PROGRESS_LOG.md'
t=progress.read_text(encoding='utf-8')
begin=t.index('> **2026-10-08：半离散 DLW 的 τ 解与完整双线性证明（合并 Gram 专题）**')
end=t.index('\n\n',begin)
old=t[begin:end]
update='> **2026-10-08：DLW 理论 Notebook（合并 τ 解与双线性证明专题）**：将原非线性化 report 重组为 [DLW理论.ipynb](notebook/DLW理论.ipynb)，正文按连续 DLW→连续双线性表示→交错半离散构造→单／双／任意 N Gram τ→精确性与正则性→非线性化→方程与精确解的连续极限展开，Q/R/M 留作补充。按用户要求移出全部误差分析、SD/FD 数值比较与绘图单元。'+str(record['code_cells'])+'个代码单元全部实际执行通过；定理公理依赖仅标准逻辑公理。离线 [阅读页](report/dlw_theory.html) 同步生成。原 notebook 留存 before 与 Trash；证明源从现有库逐字收集，未改原库。证据与构建入口在 `Workspaces/dlw_theory_notebook_20261008/`。\n'+old
t=t[:begin]+t[end+2:]
progress.write_text(update+'\n\n'+t,encoding='utf-8')

index=ROOT/'FILE_INDEX.md'
t=index.read_text(encoding='utf-8')
t=t.replace('[非线性化](notebook/非线性化report.ipynb)','[DLW理论](notebook/DLW理论.ipynb)')
t=t.replace('[notebook/非线性化report.ipynb](notebook/非线性化report.ipynb)','[notebook/DLW理论.ipynb](notebook/DLW理论.ipynb)')
t=t.replace('前者保留 DLW 两路 Lean 和空间残差估计','前者整合连续起点、半离散 τ 解、非线性化与连续极限的 Lean 证明')
t=t.replace('（当前主交付；DLW 两路非线性化、Lean 起点至终点与空间残差估计）','（当前理论交付；连续 DLW、半离散 τ 解、非线性化与连续极限，附 Lean 证明）')
files=['build.py','prepare.py','theory_runtime.py','execute.py','export.py','render_math.cjs','check_layout.cjs','deliver.py','README.md','proof_sources.json','build_validation.json','execution_validation.json','layout_validation.json','delivery_validation.json','DLW理论.input.ipynb','DLW理论.executed.ipynb']
block='<!-- DLW_THEORY_NOTEBOOK_INDEX -->\n**DLW 理论 Notebook（2026-10-08）：**\n\n- [notebook/DLW理论.ipynb](notebook/DLW理论.ipynb)\n- [report/dlw_theory.html](report/dlw_theory.html)\n'+''.join('- `Workspaces/dlw_theory_notebook_20261008/'+name+'`\n' for name in files)+''.join('- `'+p.relative_to(ROOT).as_posix()+'`\n' for p in sorted((HERE/'proofs').glob('*.lean')))+'\n'
index.write_text(block+t,encoding='utf-8')
record.update(delivery=str(dest),delivery_sha256=sha(dest),axiom_footprints=len(footprints),all_axioms_standard=True,numerical_content_removed=True,original_preserved=True)
(HERE/'delivery_validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(record,ensure_ascii=False))
