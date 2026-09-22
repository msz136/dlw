from pathlib import Path
p=Path(__file__).resolve().parent/'proofs/PkgC09Complete.lean'
s=p.read_text(encoding='utf-8').replace('import Mathlib.Tactic','import Mathlib.Algebra.BigOperators.Group.Finset.Powerset\nimport Mathlib.Tactic')
s=s.replace('M.map (algebraMap ℝ ℝ[X])','M.map Polynomial.C')
a=s.index('  have heval :');b=s.index('  have h1 :',a)
s=s[:a]+'''  have heval : P.eval (1:ℝ) = Matrix.det (1 + M) := by
    change (Polynomial.evalRingHom (1:ℝ)) P = _
    rw [hP, RingHom.map_det]
    congr 1
    ext i j
    simp [Matrix.add_apply, Matrix.one_apply, Matrix.map_apply, Matrix.smul_apply,
      Algebra.smul_def]
'''+s[b:]
s=s.replace('    simp only [mul_one]\n    exact Finset.sum_congr rfl (fun k _ => hcoeff k).symm',
            '    simp only [one_pow, mul_one]\n    exact Finset.sum_congr rfl (fun k _ => hcoeff k)')
a=s.index('  have hempty :');b=s.index('  have hg_big :',a)
s=s[:a]+'''  have hempty : ∀ k : ℕ, N < k →
      (Finset.univ : Finset (Fin N)).powersetCard k = ∅ := by
    intro k hk
    apply Finset.powersetCard_eq_empty.mpr
    simpa using hk
'''+s[b:]
s=s.replace('    rw [hgdef, hempty k hk]\n    simp','    simp [hgdef, hempty k hk]')
a=s.index('    rw [← Finset.sum_sigma]');b=s.index('  rw [← heval, h1, h2, h3]',a)
s=s[:a]+'''    simpa only [Finset.card_univ, Fintype.card_fin, hgdef] using
      (Finset.sum_powerset (Finset.univ : Finset (Fin N))
        (fun s => (M.submatrix (Subtype.val : s → Fin N)
          (Subtype.val : s → Fin N)).det)).symm
'''+s[b:]
p.write_text(s,encoding='utf-8')
