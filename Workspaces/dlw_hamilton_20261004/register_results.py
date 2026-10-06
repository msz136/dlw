"""Merge this topic into the shared progress and file index; preserve originals."""
from pathlib import Path
import hashlib
import json
import re
import shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
BEFORE=HERE/'before'
BEFORE.mkdir(exist_ok=True)
for name in ['PROGRESS_LOG.md','FILE_INDEX.md']:
    target=BEFORE/name
    if not target.exists():
        shutil.copy2(ROOT/name,target)

def merge_top(path,begin,end,entry):
    body=path.read_bytes().decode('utf-8')
    block=begin+'\r\n'+entry.replace('\n','\r\n')+'\r\n'+end+'\r\n\r\n'
    pattern=re.escape(begin)+r'[\s\S]*?'+re.escape(end)+r'\r?\n\r?\n?'
    if begin in body:
        body=re.sub(pattern,lambda _:block,body,count=1)
    else:
        body=block+body
    path.write_bytes(body.encode('utf-8'))

progress=('> **2026-10-04（半离散 DLW Hamilton 结构）：** [论文式报告](dlw_hamilton.html)。'
'**本轮非周期 A/B/C 审计与定理：** 原文1a=(a,p,q)=(2,1,2)、1b=(2,4,−3)、二孤子C=(6,−5)/(4,−3)，'
'采用精确有限h交错场、共同0<h<2。裸Hamilton密度每格点x远处非零；减真空后A/B每格点仍负常数，C趋于两臂负能量和。'
'h=1/8的E0分别−6.010278/−49.446039/尾极限−69.675029；旧γ=−8a修正亦发散。全h有理原函数证书及独立求积通过。'
'对称非周期R定义于ℓ1，端点±hΣf/2；零和一阶矩保证Rℓ1。但两条格点矩条件仍不在一般演化下保持，'
'三个背景附近有任意小两格点扰动反例。改用移动仿射B(t)+X、X=ℓ²L²，以K=RD的实自伴谱乘子及图域Y、动态域D'
'构造有限Bregman相对泛函。变分、反自伴J0、稠密测试柱形代数Jacobi及混合Jacobi、原SD双向等价由统一条件证明（定理B）；'
'物理剪切保J，完整z_t有背景漂移。Y瞬时态保持两坐标点态真空，不保证ℓ1/指数衰减，未证明Y/D不变或局部流。'
'相对K一般显时不守恒；初筛P=hΣ∫pr得到A的K+P、B的K−7P随动守恒量（各自背景、C1Y路径），'
'不是同一相空间的两独立对易量。C两臂速度11/7排除非零常系数aK+bP候选，不排除其他守恒量。'
'新增40项精确代数、两路定义域/守恒审阅通过；当前报告33公式块及宽窄屏/链接核验；材料在nonperiodic/，无新PDE演化。'
' **此前周期构造：** '
'固定周期格点与周期 x，先由原 SD 得到 Πw=c≠0、Π(Uw)=γ 的平均相容条件，并固定 γ 完成自治闭合；'
'不能任意固定 Πu。构造 R=(δ₋|零平均)⁻¹M₋P，精确周期核及 R*=−R 已证。'
'ℋ₀=hΣ∫(U²w/2+h²w³/96+wUₓ+wRwₓ/2)，扣除 γhΣ∫U 后限制于平均约束，'
'约化常括号 Jred=−offdiag(P∂x) 精确恢复原方程；物理 z=(u,v) 上 Jz=A Jred A*，'
'反对称与 Jacobi 由常括号和坐标推前证明，约束余法向被消去。'
'J 至一阶、泛函至一阶 x 导数，R 与平均项全格点耦合；物理泛函三次，自由坐标中出现整体四次项。'
'常同格点 J=−B∂x 的可逆对称数值矩阵窄类只允许交叉矩阵至比例；常零阶辛矩阵失败。'
'局部 J/局部泛函的复合半径 r 在 N≥2r+3 被 Laurent 零点计数排除（候选 J半径1、密度支撑[-1,1]：复合半径3，N≥9）；'
'不排除非局部、小N、奇异背景或特殊约化，不把搜索失败当不存在。'
'主121项精确代数检查及两路独立复核全部通过，含N=3–7、两个非零平均扇区、物理坐标推前与原两残差；'
'Jacobi 是一般证明而非采样断言；原周期18公式块核验保留。'
'c=0、开链与无限格点域仍需另证；γ(t) 重构另带(γ̇/c,0)漂移；无适定性、Liouville或全离散保持性结论。'
'源、精确核验、独立审阅、页面与原登记备份在Workspaces/dlw_hamilton_20261004/，未运行新PDE。')
merge_top(ROOT/'PROGRESS_LOG.md','<!-- DLW_HAMILTON_BEGIN -->','<!-- DLW_HAMILTON_END -->',progress)

index='''**半离散 DLW Hamilton 结构（2026-10-04）：**

- [dlw_hamilton.html](dlw_hamilton.html)（用户论文式报告；周期结构与非周期A/B/C总能量发散、相对弱Hamilton定理、算子定义域/远处行为、首批守恒候选与Liouville缺口）
- `Workspaces/dlw_hamilton_20261004/report.src.html`、`build_report.cjs`、`build_manifest.json`（当前正文源、离线 MathML 构建与33公式块登记）
- `Workspaces/dlw_hamilton_20261004/verify_hamilton.py`、`validation.json`（121项精确有理矩阵／多项式jet核验：N=3–7、两平均扇区、原物理残差、坐标推前与局部障碍）
- `Workspaces/dlw_hamilton_20261004/phase_space/periodic_reduction.md`（周期平均、边界域、时间依赖规范、零平均退化与两周期特殊约化）
- `Workspaces/dlw_hamilton_20261004/simple_candidate/NOTES.md`、`verify_exact.py`、`verification_result.json`、`REPORT_REVIEW.md`（独立变分／Helmholtz／约化及物理算子推前检查与报告审阅）
- `Workspaces/dlw_hamilton_20261004/local_obstructions/NOTES.md`、`check_algebra.py`、`algebra_checks.json`、`REPORT_REVIEW.md`（有限作用范围障碍、R精确核、相空间审计与报告符号修正证据）
- `Workspaces/dlw_hamilton_20261004/nonperiodic/energy/ENERGY_NOTES.md`、`check_energy.py`、`energy_checks.json`、`check_general_h.py`、`general_h_energy_checks.json`（原文1a/1b/二孤子C的能量、全0<h<2有理原函数证书、双臂渐近与独立求积）
- `Workspaces/dlw_hamilton_20261004/nonperiodic/operator/DOMAIN_AND_TANGENCY.md`、`SPECTRAL_WEAK_AUDIT.md`、`REPORT_AND_MOMENTUM_AUDIT.md`（对称非周期R定义域、矩条件反例、谱域与统一报告审计）
- `Workspaces/dlw_hamilton_20261004/nonperiodic/theorem/WEAK_HILBERT_HAMILTON_THEOREM.md`、`THEOREM_AUDIT.md`、`INITIAL_CHARGES.md`（定理B完整证明、Schwartz邻域否定、A/B守恒量与C窄类排除）
- `Workspaces/dlw_hamilton_20261004/nonperiodic/verify_relative.py`、`relative_validation.json`（40项精确原函数/变分/谱恒等式/切向反例及动量时间修正核验）
- `Workspaces/dlw_hamilton_20261004/nonperiodic/before/`（本轮修改前主HTML、正文源与共享记录保留）
- `Workspaces/dlw_hamilton_20261004/check_report.cjs`、`html_validation.json`、`report_top_1440.png`、`report_top_390.png`、`report_physical_1440.png`、`report_physical_390.png`（宽窄屏、数学、引用与可读性检查）
- `Workspaces/dlw_hamilton_20261004/report_nonperiodic_1440.png`、`report_nonperiodic_390.png`（当前非周期定理宽窄屏预览）
- `Workspaces/dlw_hamilton_20261004/register_results.py`、`registration.json`、`before/`（同专题合并登记、交付哈希与共享记录修改前备份）'''
merge_top(ROOT/'FILE_INDEX.md','<!-- DLW_HAMILTON_INDEX_BEGIN -->','<!-- DLW_HAMILTON_INDEX_END -->',index)
path=ROOT/'FILE_INDEX.md'
body=path.read_bytes().decode('utf-8')
body=body.replace('已按当前正文核对根目录 10 个 HTML。','已按当前正文核对根目录 11 个 HTML（含新增 Hamilton 报告）。')
row='| [dlw_hamilton.html](dlw_hamilton.html) | 周期结构与原文A/B/C非周期线波：总能量发散、相对Hamilton定理、算子定义域及首批守恒候选。 |\r\n'
body=re.sub(r'\| \[dlw_hamilton\.html\]\(dlw_hamilton\.html\) \|[^\r\n]*\|\r?\n',lambda _:row,body)
if row.strip() not in body:
    old='| [dlw_integrability_status.html](dlw_integrability_status.html) | DLW Gram、Darboux／Lax、非线性化与连续极限的当前完成情况及谱表示缺口。 |\r\n'
    if old not in body:
        raise AssertionError('Reading-map insertion anchor absent')
    body=body.replace(old,old+row,1)
path.write_bytes(body.encode('utf-8'))

paths=[ROOT/'dlw_hamilton.html',ROOT/'PROGRESS_LOG.md',ROOT/'FILE_INDEX.md']
paths += [p for p in HERE.rglob('*') if p.is_file() and p.suffix in ['.py','.cjs','.html','.md','.json']
          and 'before' not in p.parts and p.name!='registration.json']
data={'topic':'DLW Hamilton structure','date':'2026-10-04',
      'root_exact_checks':json.loads((HERE/'validation.json').read_text(encoding='utf-8'))['count'],
      'nonperiodic_exact_checks':json.loads((HERE/'nonperiodic/relative_validation.json').read_text(encoding='utf-8'))['count'],
      'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
(HERE/'registration.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'registered':True,'files':len(paths),'checks':data['root_exact_checks']}))
