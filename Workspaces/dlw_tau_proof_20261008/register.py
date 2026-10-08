from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'PROGRESS_LOG.md'
text=p.read_text(encoding='utf-8')
start=text.index('> **最新研究更新：Gram 与可积性复核（2026-09-19，优先于下方所有旧结论）**')
end=text.index('\n\n',start)
old=text[start:end]
new='> **2026-10-08：半离散 DLW 的 τ 解与完整双线性证明（合并 Gram 专题）**：新增 [阅读页](report/dlw_tau_solution_proof.html)，27 个公式，展示单／双／任意 N 孤子、Gram 行列式与子集展开、单孤子逐项代入、一般 N 秩一更新证明、格点移位及正则实参数域。补全标量消去与振幅多项式延拓，覆盖 τ 零点处的双线性恒等式。符号消去精确为零；N=1..5、两格距、三格点共30组两条双线性式逐指数系数精确为零，N≤3 主子式与行列式展开一致。源、构建、核验与结果在 `Workspaces/dlw_tau_proof_20261008/`。\n> **此前 Gram 复核（2026-09-19 历史记录；其中谱结构进度见后续专题）：**\n'+old.split('\n',1)[1]
text=text[:start]+text[end+2:]
p.write_text(new+'\n\n'+text,encoding='utf-8')
p=root/'FILE_INDEX.md'
text=p.read_text(encoding='utf-8')
block='<!-- DLW_TAU_PROOF_INDEX -->\n**半离散 DLW τ 解与证明（2026-10-08）：**\n\n- [阅读报告](report/dlw_tau_solution_proof.html)\n- `Workspaces/dlw_tau_proof_20261008/report.src.html`：完整证明正文源。\n- `Workspaces/dlw_tau_proof_20261008/build.cjs`：离线 MathML 构建。\n- `Workspaces/dlw_tau_proof_20261008/verify.py`：符号及精确系数核验。\n- `Workspaces/dlw_tau_proof_20261008/validation.json`：本次核验结果。\n- `Workspaces/dlw_tau_proof_20261008/register.py`：合并进度与登记索引。\n\n'
if '<!-- DLW_TAU_PROOF_INDEX -->' not in text:
    p.write_text(block+text,encoding='utf-8')
