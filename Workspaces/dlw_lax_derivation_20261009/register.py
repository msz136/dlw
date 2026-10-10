from pathlib import Path
import hashlib,json,re,shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
backup=HERE/'registration_before'
backup.mkdir(exist_ok=True)
for name in ['PROGRESS_LOG.md','FILE_INDEX.md']:
    if not (backup/name).exists():shutil.copy2(ROOT/name,backup/name)
def update(name,begin,end,text):
    path=ROOT/name
    source=path.read_text(encoding='utf-8-sig')
    block=begin+'\n'+text.strip()+'\n'+end+'\n\n'
    if begin in source:
        source=re.sub(re.escape(begin)+r'[\s\S]*?'+re.escape(end)+r'\s*',lambda _:block,source,count=1)
    else:source=block+source
    path.write_text(source,encoding='utf-8')
update('PROGRESS_LOG.md','<!-- DLW_LAX_DERIVATION_BEGIN -->','<!-- DLW_LAX_DERIVATION_END -->',
'> **2026-10-09（半离散 DLW 的 Lax 推导）：** [论文式 HTML](report/dlw_lax_derivation.html) 按用户要求保留四部分：原方程、辅助势与所需条件、Lax对、相容性与原方程的对应。最新措辞修订补明连续／离散变量、辅助势局部重构、残差含义和Darboux交织作用，展开相邻格点的时间导数比较，并解释非退化条件在反向推导中的使用。12个编号公式与修订前逐字一致，共60处严格渲染数学；桌面／390px／打印核验通过。前序已移出 c、γ、周期单值算子和守恒量延伸，7项局部符号核对证据保留。当前正文为 `compact_manuscript.md`，措辞核对见 `prose_revision_validation.json`；前版保存在 `before_prose_revision/`。源、构建与证据在 `Workspaces/dlw_lax_derivation_20261009/`。')
files=sorted(p for p in HERE.iterdir() if p.is_file())
index='**半离散 DLW 的 Lax 推导（2026-10-09）：**\n\n- [report/dlw_lax_derivation.html](report/dlw_lax_derivation.html)：四部分、12式；原方程、条件、Lax对及相容性证明。\n'
descriptions={
    'manuscript.md':'前版固定平均周期推导正文。','local_manuscript.md':'前版局部推导与周期条件正文。','compact_manuscript.md':'当前四部分精简正文源。','build.py':'离线HTML构建、公式编号与链接检查。',
    'render.cjs':'严格KaTeX公式渲染。','verify.py':'31项精确符号检查。',
    'local_verify.py':'当前局部推导的7项精确符号检查。','local_symbolic_validation.json':'当前局部推导核对证据。','check_layout.cjs':'桌面、390px和打印布局检查。','register.py':'合并登记进度和逐文件索引。',
    'formulas.json':'数学表达式清单。','rendered.json':'已渲染数学。',
    'symbolic_validation.json':'符号核对证据。','build_validation.json':'构建核验结果。',
    'layout_validation.json':'布局核验结果。','registration.json':'登记与交付哈希。'}
descriptions.update({'verify_prose_revision.py':'四节结构与12个编号公式逐字保持检查。','prose_revision_validation.json':'措辞修订范围与源码哈希核验。'})
for p in files:
    rel=p.relative_to(ROOT).as_posix()
    index+=f'- [{rel}]({rel})：'+descriptions.get(p.name,'页面核验截图。')+'\n'
if not (HERE/'registration.json').exists():
    index+='- `Workspaces/dlw_lax_derivation_20261009/registration.json`：登记与交付哈希。\n'
index+='- `Workspaces/dlw_lax_derivation_20261009/registration_before/`：登记前进度与索引原件。\n'
index+='- `Workspaces/dlw_lax_derivation_20261009/before_local_revision/`：前版HTML、构建／登记脚本与核验记录。\n'
index+='- `Workspaces/dlw_lax_derivation_20261009/before_compact_revision/`：四部分精简前的HTML、正文、构建及登记脚本。\n'
index+='- `Workspaces/dlw_lax_derivation_20261009/before_prose_revision/`：措辞修订前的HTML、正文及登记脚本。\n'
update('FILE_INDEX.md','<!-- DLW_LAX_DERIVATION_INDEX_BEGIN -->','<!-- DLW_LAX_DERIVATION_INDEX_END -->',index)
hashes={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'report/dlw_lax_derivation.html',HERE/'compact_manuscript.md',ROOT/'PROGRESS_LOG.md',ROOT/'FILE_INDEX.md']}
(HERE/'registration.json').write_text(json.dumps(hashes,indent=2,ensure_ascii=False),encoding='utf-8')
print('Progress and file index registered')
