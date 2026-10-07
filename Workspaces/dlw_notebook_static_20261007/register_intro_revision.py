"""Register the narrative revision and stage only its shared-record additions."""
from pathlib import Path
import difflib
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROJECT = ROOT/'Workspaces/notebook_reports_20261006'
GSG = PROJECT/'gsg_second_order'
sha = lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p:json.loads(p.read_text('utf-8'))
record = read(HERE/'intro_revision.json')
build = read(HERE/'build_validation.json')
content = read(HERE/'content_validation.json')
browser = read(HERE/'browser_validation.json')
assert build['success'] and content['success'] and browser['success']
assert record['notebook_sha256'] == content['notebook_sha256'] == build['source_sha256']
record.update(html_sha256=content['html_sha256'],
    saved_png_sha256=content['png_sha256'],
    code_excerpts=build['visible_code_excerpts'], code_lines=build['visible_code_lines'],
    mathematical_expressions=build['math_expressions'],
    content_validation_sha256=sha(HERE/'content_validation.json'),
    browser_validation_sha256=sha(HERE/'browser_validation.json'))
(HERE/'intro_revision.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')

# Retain the original numerical-run hashes and link the present prose revision.
manifest_path = GSG/'revision_manifest.json'
manifest = read(manifest_path)
manifest['presentation_revision'] = dict(record='Workspaces/dlw_notebook_static_20261007/intro_revision.json',
    record_sha256=sha(HERE/'intro_revision.json'), notebook_sha256=record['notebook_sha256'],
    html_sha256=record['html_sha256'], code_and_saved_outputs_unchanged=True,
    exact_solution_excerpt_added=True)
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

readme = HERE/'README.md'
text = readme.read_text('utf-8').replace('115 个数学表达式','121 个数学表达式')
text = text.replace('6 段关键源码，共 54 行','7 段关键源码，共 83 行')
text = text.replace('SD 摘录 `SDModel.solve_one` 和 `advance`','精确解摘录 `Exact.tau` 至 `uv`；SD 摘录 `SDModel.solve_one` 和 `advance`')
text = text.replace('14d33d87d0c4d8eeca716162d70489f2aedc6472ea1efcdc9b9e60ab272ee5a7',record['notebook_sha256'])
text = text.replace('5125bebd928f2c9b9c9b01cedc243c5b306bbcbeba39c9e090106a68fce52f37',record['html_sha256'])
sentence = '开篇与第1.1节的叙述修订见 `intro_revision.json`；计算代码、执行计数和保存输出逐项保持，数值执行证据继续记录原始执行时的文件哈希。'
if sentence not in text:
    text = text.replace('\n## 生成与核验', '\n'+sentence+'\n\n## 生成与核验',1)
readme.write_text(text,encoding='utf-8')

note = ('**开篇与精确解说明（2026-10-07）：** 统一开头为两种可积半离散方法SD/SD2和直接差分FD的数值解及网格/时间误差比较；'
    '第1.1节改为孤子精确解，说明Exact.tau的归一化权重、mean/cov解析导数及uv组合，并在HTML展示29行真实源码。'
    '计算代码和全部保存输出保持；内容与离线桌面/390px/打印核验通过。证据见 '
    '[intro_revision.json](Workspaces/dlw_notebook_static_20261007/intro_revision.json)。 ')
marker = '**GSG三点二阶对齐（2026-10-07）：** '
progress = ROOT/'PROGRESS_LOG.md'
text = progress.read_text('utf-8')
assert marker in text
if note not in text:
    progress.write_text(text.replace(marker,note+marker,1),encoding='utf-8')
begin, end = '<!-- DLW_INTRO_REVISION_INDEX_BEGIN -->', '<!-- DLW_INTRO_REVISION_INDEX_END -->'
names = ['revise_intro.py','register_intro_revision.py','intro_revision.json']
block = begin+'\n**DLW 开篇与精确解计算说明（2026-10-07）：**\n\n'+'\n'.join(
    f'- [Workspaces/dlw_notebook_static_20261007/{n}](Workspaces/dlw_notebook_static_20261007/{n})' for n in names)+'\n'+end
index = ROOT/'FILE_INDEX.md'
text = index.read_text('utf-8')
if begin not in text:
    index.write_text(text.rstrip()+'\n\n'+block+'\n',encoding='utf-8')
patches=[]
for name in ('PROGRESS_LOG.md','FILE_INDEX.md'):
    before = subprocess.run(['git','show','HEAD:'+name],cwd=ROOT,check=True,capture_output=True).stdout.decode('utf-8')
    after = before.replace(marker,note+marker,1) if name=='PROGRESS_LOG.md' else before.rstrip()+'\n\n'+block+'\n'
    patches.append(''.join(difflib.unified_diff(before.splitlines(keepends=True),after.splitlines(keepends=True),
        fromfile='a/'+name,tofile='b/'+name)))
patch = HERE/'intro_records_staging.patch'
patch.write_text(''.join(patches),encoding='utf-8',newline='\n')
subprocess.run(['git','apply','--cached','--check',str(patch)],cwd=ROOT,check=True)
subprocess.run(['git','apply','--cached',str(patch)],cwd=ROOT,check=True)
print('Narrative revision registered; only its shared-record additions staged.')
