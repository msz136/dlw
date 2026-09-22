from pathlib import Path
root=Path(__file__).resolve().parent/'proofs'
s=(root/'PkgC09.lean').read_text(encoding='utf-8')
a=s.index('  simp only [Matrix.add_apply',s.index('private lemma tau_eq_det_one_add'))
b=s.index('\nprivate lemma det_one_add_comm_diag',a)
s=s[:a]+'''  simp only [Matrix.add_apply, Matrix.one_apply, Matrix.mul_diagonal,
    Matrix.diagonal_mul, Matrix.of_apply]
  ring
'''+s[b:]
s=s.replace('(M.submatrix Subtype.val Subtype.val).det',
            '(M.submatrix (Subtype.val : s → Fin N) (Subtype.val : s → Fin N)).det')
s=s.replace('    intro k\n  rw [hgdef, hP]\n  simpa only using',
            '    intro k\n    rw [hgdef, hP]\n    simpa only using')
s=s.replace('    simp only [zpow_one]\n    refine mul_pos', '    refine mul_pos')
s=s.replace('    rw [hz]\n    simp only [mul_one]\n    exact mul_pos (zpow_pos',
            '    rw [hz]\n    exact mul_pos (zpow_pos')
s=s.replace('(OrderIso.toEquiv e)','(e.toEquiv)')
s=s.replace('((Matrix.of (fun i k : Fin N => (D.p i + D.q k)⁻¹) *\n        Matrix.diagonal c).submatrix Subtype.val Subtype.val).det',
            '((Matrix.of (fun i k : Fin N => (D.p i + D.q k)⁻¹) *\n        Matrix.diagonal c).submatrix (Subtype.val : s → Fin N) (Subtype.val : s → Fin N)).det')
s+='\n#print axioms DLWContract.c09_proved\n'
(root/'PkgC09Complete.lean').write_text(s,encoding='utf-8')
