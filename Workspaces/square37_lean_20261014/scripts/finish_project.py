"""Record a successful unified build and register this research project."""
import argparse
import hashlib
import json
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('receipt')
args=ap.parse_args()
ROOT=Path(__file__).resolve().parents[1]
ACA=ROOT.parents[1]
receipt=Path(args.receipt).resolve()
run=json.loads(receipt.read_text(encoding='utf-8'))
assert run['status']=='PASSED' and Path(run['target'])==ROOT/'lean/All.lean'
assert all(f['passed'] and f['exit_code']==0 and hashlib.sha256(Path(f['file']).read_bytes()).hexdigest()==f['sha256'] for f in run['files'])
status={
 'project':'Cantrell 37-square packing: construction and conditional lower bound',
 'date':'2026-10-14','global_optimality':'OPEN_NOT_PROVED',
 'exact_endpoint_packing':'NOT_PROVED',
 'conditional_minimax_lean_passed':True,
 'conditional_geometric_lower_bound_lean_passed':True,
 'upper':'659861960924437/100000000000000',
 'candidate_side':'Unique real root of Cantrell37.poly on [6.59861960924436,6.59861960924437]',
 'final_receipt':receipt.relative_to(ROOT).as_posix(),
 'local_modules':len(run['files']),
 'toolchain':run['toolchain'],'mathlib_commit':run['mathlib_commit'],
 'allowed_axioms':['propext','Classical.choice','Quot.sound'],
 'entry':'lean/All.lean',
 'main_theorems':[
  'Packing37.exists_packing_37','Packing37.closed_disjoint',
  'Cantrell37.candidateSide_strict_interval',
  'Cantrell37.support_model_minimum','Cantrell37.support_model_attains_minimum',
  'Cantrell37.conditional_branch_lower_bound'],
 'conditional_assumptions':'Common direction parameters 0<=s<=c, c^2+s^2=1; FirstChain, LeftBrace, RightBrace, and two explicit central support inequalities. No claim arbitrary packings satisfy these.',
 'remaining':['37-specific complete geometric cover and occupancy classification','Verified exhaustive exclusions and endpoint capture','Exact 37-square packing at the algebraic endpoint'],
 'next_global_route':'analysis/global_route_next.json',
 'source37_commit':'b8c930338ee3577a43faccb52472c6975ab7eccd',
 'source17_commit':'0a7167efa8dcae7fa73855890630fb7e2de550ed',
 'source17_review':'Partial interface/manifest audit; full released generated proof not rebuilt.',
 'replay_command':f'python -X utf8 "{ACA / "_lean_shared/check_lean.py"}" --root "{ROOT / "lean"}" --file "{ROOT / "lean/All.lean"}" --timeout 300'
}
(ROOT/'STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'analysis/lean_source_manifest.json').write_text(json.dumps({
 'receipt':status['final_receipt'],
 'files':[{k:f[k] for k in ('file','sha256','passed')} for f in run['files']]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

registry=[]
def write_preserving(path,new,old):
    assert path.read_bytes()==old, 'Concurrent edit detected; rerun registration against latest content.'
    path.write_bytes(new)
    registry.append({'path':str(path),'before_sha256':hashlib.sha256(old).hexdigest(),
                     'after_sha256':hashlib.sha256(new).hexdigest()})

index=ACA/'FILE_INDEX.md'
old=index.read_bytes()
text=old.decode('utf-8-sig')
row='| 37单位方块的构造与条件下界 | Cantrell有理构造认证、代数端点、接触支条件最小值与17块证明接口迁移；全局最优未证 | [报告](report/square37_cantrell_lean_20261014.html)；[目录](Workspaces/square37_lean_20261014) |'
if 'Workspaces/square37_lean_20261014' not in text:
    anchor='| 早期双线性构造 |'
    pos=text.index(anchor)
    text=text[:pos]+row+'\n'+text[pos:]
    write_preserving(index,text.encode('utf-8'),old)

progress=ACA/'PROGRESS_LOG.md'
old=progress.read_bytes()
marker='<!-- SQUARE37_LEAN_20261014 -->'
endmarker='<!-- /SQUARE37_LEAN_20261014 -->'
entry=f'''{marker}
> **2026-10-14（37方块：Cantrell构造与条件下界形式化）：** 按用户转向要求，停止17块上界搜索，复用DLW共享Lean环境建立 `Workspaces/square37_lean_20261014/`，主阅读入口为[研究报告](report/square37_cantrell_lean_20261014.html)。原目录37块仍为open，报告界6.44至6.59861960924437，不能称为已证最优。本轮{len(run['files'])}个Lean模块统一编译通过：37项单位性、148墙约束、666对严格SAT构成实数单位方形可行见证，并证明闭方块两两不交；独立有理多边形裁剪全部通过。对理想共同倾角与显式有向接触支，形式证明两条支撑下界、半角参数全八分区覆盖、交点隔离、共轭根排除和目录八次多项式识别；整数Bernstein恒等式给两支撑函数的完整区间minimax，最终 `conditional_branch_lower_bound` 给任意满足该接触支的坐标数组 L≥L*。L*严格位于6.59861960924436与6.59861960924437之间。所有关键定理仅依赖propext/Classical.choice/Quot.sound，无新axiom、占位证明或native_decide。已审核17块T-154可得源码的覆盖/重编号/装配接口并复用六个通用有限覆盖引理，未重建其全部生成证书；区别T-153条件候选。统一运行 `{run['run_id']}`，源码哈希与核验收据在项目内。**未完成：任意37块布局的全局完备排除/端点归约，以及代数端点处的完整37块可行构造。** 朴素8×8中心网格有846636978475316672占用集，后续须开发可核验的自适应剪枝，保留每块独立正负角度。原17项目与其他研究保持原样。
{endmarker}

'''
oldtext=old.decode('utf-8-sig')
if marker in oldtext:
    start=oldtext.index(marker); end=oldtext.index(endmarker,start)+len(endmarker)
    newtext=oldtext[:start]+entry.rstrip()+oldtext[end:]
else:
    newtext=entry+oldtext
write_preserving(progress,newtext.encode('utf-8'),old)
(ROOT/'analysis/registry_update.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'recorded','modules':len(run['files']),'receipt':status['final_receipt']},ensure_ascii=False))
