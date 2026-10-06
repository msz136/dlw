from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
file = HERE / 'inventory.json'
data = json.loads(file.read_text(encoding='utf-8'))
items = {r['id']: r for g in data['groups'] for r in g['results']}
items['L02']['start'] = 'h≠0，采用实际Gram行列式，全部相关分母合法；辅助参数s要求pᵢ−s、qₖ+s均非零。正性再要求h>0、p/q严格递增、0<pᵢ<a−h/2、qᵢ及幅值ρᵢ>0。'
items['L06']['start'] = 'h≠0；指定中心两壁模板并要求零阶／一阶匹配；或取N=2的实际Gram行列式。'
if '格点速率另取P≠0' not in items['L04']['start']:
    items['L04']['start'] += ' 格点速率另取P≠0。'
if r'\log\lambda_h(P)/h-1/P' not in items['L04']['conclusion']:
    items['L04']['conclusion'] += r' 另有\(\log\lambda_h(P)/h-1/P=O(h^2)\)。'
if not any(s.get('theorem') == 'c12_proved' for s in items['L04']['sources']):
    items['L04']['sources'].append({'path':'Workspaces/lean_contracts/proofs/PkgQuotientRate.lean','line':240,'label':'格点速率','theorem':'c12_proved'})
for source in items['L07']['sources']:
    if source.get('theorem') == 'c21_proved':
        source.update(path='Workspaces/lean_contracts/proofs/PkgTrivial.lean',line=33)
    if source.get('theorem') == 'c25_proved':
        source.update(path='Workspaces/lean_contracts/proofs/PkgLattice.lean',line=432)
if '总误差满足' not in items['L09']['conclusion']:
    items['L09']['conclusion'] += ' 总误差满足“数值误差＋模型误差”的三角上界。'
items['L09']['sources'][1]['line'] = 271
if '更新后分母非零' not in items['D04']['start']:
    items['D04']['start'] += ' 相关高阶导数及非零Q分支受控；精确一步关系取固定网格内点，更新后分母非零。'
items['D05']['start'] = '连续DLW或相应有限h闭合；有限h密度按μ=1+κh²归一化，μ≠0；采用精确通量、固定非负层权重。正性另取连续指定孤子支，或有限h支hμ>0、p<s₋、q+s₋>0。'
items['D07']['sources'][0]['line'] = 124
items['D08']['sources'][0]['line'] = 166
items['D14']['start'] = '采用L02所述正实无零τ充分域的任意N Gram解；相移另要求不同速度与分离渐近；独立谱参数z避开极点和格点乘子的零点，采用规定背景归一化。'
file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

entry = '> **2026-10-02（DLW／2HS理论结果与命题目录）：** 新增根目录[理论结果与命题结构](theory_results.html)，将现有成果归并为31个“起点／假设→结论”条目（9组Lean技术结果、14组DLW解析结果、8组2HS结果），给总览、六个主命题的组织方式与尚缺箭头。核读真实Lean定义／定理；32冻结目标C01–C25/N01–N07通过记录完整，当前39份源码哈希与run 20260922_221626_2fd722e0一致，端点只依赖标准三公理，本轮未重编译。明确已证为指定任意N Gram构造、有限h精确双线性对与紧盒O(h²)连续极限，非任意连续解采样即满足离散方程；T01相位／初速限制、T03局部静态不可去形变、T04限定线性Gaussian／带宽定理、周期重构非单射与2HS校准／密度／胞元残差分别列条件与证据。两次分域审查修正LayerOK、密度归一化、更新分母与谱渐近正数据条件。无新数学证明或PDE演化，未改旧报告。源与逐来源哈希在 Workspaces/theory_inventory_20261002/；31双项结构、数学资源、本地引用和宽窄屏核验记录随页保存。\n'
progress = ROOT / 'PROGRESS_LOG.md'
text = progress.read_text(encoding='utf-8')
prefix = '> **2026-10-02（DLW／2HS理论结果与命题目录）：**'
if prefix in text:
    lines = text.splitlines(keepends=True)
    text = ''.join(entry if line.startswith(prefix) else line for line in lines)
else:
    text = entry + '\n' + text
progress.write_text(text, encoding='utf-8')

index = ROOT / 'FILE_INDEX.md'
text = index.read_text(encoding='utf-8')
section = '''**DLW／2HS理论结果与命题目录（2026-10-02）：**

- [理论结果与命题结构](theory_results.html)（根目录论文式总览；31个起点／结论条目、已证层级、命题组织与关键待证环节）
- Workspaces/theory_inventory_20261002/inventory.json（现有Lean／DLW／2HS逐条目录、真实证明来源及假设）
- Workspaces/theory_inventory_20261002/build_report.py、finalize_inventory.py、manifest.json（自包含页面生成、审查修订、来源SHA-256及Lean核对范围）
- Workspaces/theory_inventory_20261002/check_report.cjs、validation.json、report_1440.png、report_390.png、report_theorem.png（31双项结构、公式／本地链接／宽窄屏核验与直接视觉检查）

'''
if section.splitlines()[0] not in text:
    title, rest = text.split('\n', 1)
    index.write_text(title + '\n\n' + section + rest.lstrip('\n'), encoding='utf-8')
print(json.dumps({'updated_entries':11,'progress_record':'merged_or_created','index_record':'present'},ensure_ascii=False))
