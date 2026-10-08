from pathlib import Path
import json,re,shutil,hashlib
import nbformat
from focus_theory import focus,EXACT_LIMIT
from notebook_prose import S2_PROOF
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
backup=HERE/'before_focus'
backup.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
paths=[ROOT/'notebook/DLW理论.ipynb',HERE/'DLW理论.executed.ipynb',HERE/'DLW理论.input.ipynb']
records=[]
for p in paths:
    target=backup/p.name
    assert not target.exists()
    shutil.copy2(p,target)
    n=nbformat.read(p,as_version=4)
    oldcodes={c.id:dict(c) for c in n.cells if c.cell_type=='code'}
    n.cells=focus(n.cells)
    assert oldcodes=={c.id:dict(c) for c in n.cells if c.cell_type=='code'}
    nbformat.write(n,p)
    text='\n'.join(c.source for c in n.cells if c.cell_type=='markdown')
    tags=re.findall(r'\\tag\{([^}]+)\}',text)
    assert len(tags)==len(set(tags))
    assert set(re.findall(r'（([A-Z]\d+)）',text))<=set(tags)
    records.append({'path':str(p.relative_to(ROOT)),'before':sha(target),'after':sha(p),'code_and_outputs_unchanged':True})
assert paths[0].read_bytes()==paths[1].read_bytes()

paper=HERE/'paper.src.md'
shutil.copy2(paper,backup/paper.name)
shutil.copy2(ROOT/'report/dlw_theory.html',backup/'dlw_theory.html')
s=paper.read_text(encoding='utf-8')
mapping=json.loads((HERE/'paper_revision.json').read_text(encoding='utf-8'))['equation_map']
reverse={v:k for k,v in mapping.items()}
s=re.sub(r'\\tag\{(\d+)\}',lambda m:r'\tag{'+reverse[m[1]]+'}',s)
s=re.sub(r'（(\d+)）',lambda m:'（'+reverse[m[1]]+'）',s)
a=s.index('**定理 1');b=s.index('## 2　',a)
s=s[:a]+r'将（C2）代入并求导，由（C3）得到连续 DLW 方程（C1）。'+'\n\n'+s[b:]
a=s.index('证明。取 $\\Phi');b=s.index('## 3　',a)
s=s[:a]+S2_PROOF+'\n\n'+s[b:]
s=s.replace('**定理 2（二阶双线性一致性）。**','二阶展开为：')
a=s.index('## 3　');b=s.index('## 4　',a)
old=s[a:b]
def formula(tag):
    return next(m[0] for m in re.finditer(r'\$\$[\s\S]*?\$\$',old) if r'\tag{'+tag+'}' in m[0])
section='## 3　孤子解与 Gram 行列式\n\n记 $d=h/2$，定义\n\n'+formula('T3')+'\n\n'+formula('T4')+'\n\n一般 $N$ 孤子的 τ 函数为\n\n'+formula('T7')+r'''

空乘积取 $1$，$G_{j+1}$ 由 $E_i\mapsto\chi_iE_i$ 得到。以下用等价的 Gram 行列式证明这对函数满足半离散方程。

'''+formula('T10')+'\n\n'+formula('T11')+r'''

这里 $N$ 是行列式阶数，$n$ 是辅助层编号；$\tau_0$ 与 $s$ 无关。所有分母和格点乘子均取非零值；当使用负整数层 $n$ 时，还要求 $p_i-s\ne0$。

由主子式展开和 Cauchy 行列式公式

'''+formula('T12')+r'''

提出每个主子式的行、列指数因子，即得到（T7）。其中 $A_{ik}$ 是归一化相互作用系数，与格距 $h$ 无关。

'''
s=s[:a]+section+s[b:]
s=s.replace('**定理 4（Gram 解）。**','**主定理（Gram 解）。**').replace('**定理 5（正则物理解）。**','').replace('**定理 6（二阶非线性一致性）。**','二阶非线性一致性如下。')
a=s.index('## 7　');b=s.index('## 附录',a)
s=s[:a]+EXACT_LIMIT+'\n\n'+s[b:]
tags=re.findall(r'\\tag\{([^}]+)\}',s)
mapping={tag:str(i+1) for i,tag in enumerate(tags)}
assert len(tags)==len(set(tags))
s=re.sub(r'\\tag\{([^}]+)\}',lambda m:r'\tag{'+mapping[m[1]]+'}',s)
s=re.sub(r'（([A-Z]\d+)）',lambda m:'（'+mapping[m[1]]+'）',s)
assert '单孤子可直接验证' not in s and '**推论 3' not in s and '这里的 $O(h^2)$ 指' not in s
paper.write_text(s,encoding='utf-8')
record={'notebooks':records,'code_cells_unchanged':14,'lean_reexecuted':False,'paper_equation_map':mapping,'paper_numbered_equations':len(tags),'paper_source_sha256':sha(paper)}
(HERE/'focus_validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ('execution_validation.json','delivery_validation.json'):
    p=HERE/name;shutil.copy2(p,backup/name)
    r=json.loads(p.read_text(encoding='utf-8'));r['before_focus_sha256']=r['sha256'];r['sha256']=sha(paths[1])
    if 'delivery_sha256' in r:r['delivery_sha256']=sha(paths[0])
    r['focus_revision']='Markdown-only simplification; all 14 code cells and saved execution outputs unchanged; no new Lean run'
    p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(record,ensure_ascii=False))
