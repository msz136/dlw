from pathlib import Path
import json,hashlib,subprocess,os,collections
ROOT=Path(r'C:\Users\msz\aca');OUT=Path(__file__).resolve().parent
plan=json.loads((OUT/'move_plan.json').read_text(encoding='utf-8'));trash=Path(plan['trash'])
failures=[];moved_bytes=0
for row in plan['files_detail']:
 src=ROOT/row['path'];dst=trash/row['path']
 if src.exists():failures.append('Still at source: '+row['path'])
 if not dst.is_file():failures.append('Missing destination: '+row['path'])
 elif dst.stat().st_size!=row['bytes']:failures.append('Size mismatch: '+row['path'])
 else:moved_bytes+=row['bytes']
for rel,digest in {**plan['protected_paper_hashes'],**plan['retained_source_hashes']}.items():
 p=ROOT/rel
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:failures.append('Preserved file mismatch: '+rel)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
git_state=dict(head=git('rev-parse','HEAD'),branches=git('for-each-ref','--format=%(refname)','refs/heads'),stash=git('stash','list'),commit_count=int(git('rev-list','--count','HEAD')),shallow=git('rev-parse','--is-shallow-repository'),git_bytes=sum(p.stat().st_size for p in (ROOT/'.git').rglob('*') if p.is_file()))
if git_state['branches']!='refs/heads/main' or git_state['stash'] or git_state['commit_count']!=1:failures.append('Unexpected active Git history')
old_git=trash/'git_history/.git';old_git_bytes=sum(p.stat().st_size for p in old_git.rglob('*') if p.is_file())
if not old_git.is_dir():failures.append('Missing original Git archive')
# Independent residual binary scan. Dependencies and inaccessible entries are explicitly excluded.
residual=[];errors=[];stack=[ROOT]
while stack:
 directory=stack.pop()
 try:
  with os.scandir(directory) as entries:
   for e in entries:
    p=Path(e.path);rel=p.relative_to(ROOT).as_posix()
    if rel in {'Trash','.git'} or rel.startswith('Workspaces/workspace_catalog_audit_20261013/'):continue
    try:
     st=e.stat(follow_symlinks=False)
     if e.is_symlink() or getattr(st,'st_file_attributes',0)&0x400:continue
     if e.is_dir(follow_symlinks=False):stack.append(p)
     elif p.suffix.lower() in {'.npz','.npy','.h5','.hdf5'} and not any(v in rel for v in ('/.research_deps/','/vendor/','/node_modules/','/.lake/packages/','_lean_shared/')):residual.append(rel)
    except OSError as exc:errors.append(str(exc))
 except OSError as exc:errors.append(str(exc))
result=dict(ok=not failures,failures=failures,moved_files=plan['files'],moved_product_bytes=moved_bytes,old_git_bytes=old_git_bytes,total_moved_bytes=moved_bytes+old_git_bytes,protected_paper_files=len(plan['protected_paper_hashes']),preserved_source_files=len(plan['retained_source_hashes']),active_git=git_state,residual_research_arrays=residual,unreadable=errors,by_reason=plan['by_reason'])
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in {'unreadable'}},ensure_ascii=True,indent=2))
print('Unreadable entries:',len(errors))
if failures or residual:raise SystemExit(1)
