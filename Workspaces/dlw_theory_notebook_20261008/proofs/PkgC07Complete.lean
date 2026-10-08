import PkgGramActual
import PkgGramHirota

noncomputable section
open scoped BigOperators Matrix
namespace DLWContract
open GramActual

theorem c07_proved : C07 := by
  intro N D h s hD hs n j
  funext x t
  change bil s (fun x t => (M D h s (n+1) j x t).det)
    (fun x t => (M D h s n j x t).det) x t=0
  apply GramDeterminant.bil_det_of_jets s
    (M D h s n j) (M D h s (n+1) j)
    (V D h s n j) (V D h s (n+1) j)
    (GramActual.W D h s n j) (GramActual.W D h s (n+1) j)
    (T D h s n j) (T D h s (n+1) j)
    (matrix_x D h s n j) (matrix_x D h s (n+1) j)
    (matrix_xx D h s n j) (matrix_xx D h s (n+1) j)
    (matrix_t D h s n j) (matrix_t D h s (n+1) j)
    x t (r D h s n j x t) (b D h s n j x t)
    (u D h s n j x t) (c D h s n j x t)
    (matrix_shift D h s n j hD hs x t)
    (rank_one D h s n j hD x t) (next_rank_one D h s n j hD hs x t)
  · ext i k
    have hv := congrFun (congrFun (rank_one D h s n j hD x t) i) k
    change (D.p i+D.q k)*K D h s n j x t i k=
      r D h s n j x t i*c D h s n j x t k at hv
    change (D.p i+D.q k)^2*K D h s n j x t i k-
      ((D.q k)^2-(D.p i)^2)*K D h s n j x t i k-
      (2*s)*((D.p i+D.q k)*K D h s n j x t i k)=
      (-2)*((s-D.p i)*r D h s n j x t i*c D h s n j x t k)
    linear_combination 2*(D.p i-s)*hv
  · ext i k
    have hv := congrFun (congrFun (next_rank_one D h s n j hD hs x t) i) k
    change (D.p i+D.q k)*K D h s (n+1) j x t i k=
      (s-D.p i)*r D h s n j x t i*(c D h s n j x t k/(D.q k+s)) at hv
    change (D.p i+D.q k)^2*K D h s (n+1) j x t i k+
      ((D.q k)^2-(D.p i)^2)*K D h s (n+1) j x t i k+
      (2*s)*((D.p i+D.q k)*K D h s (n+1) j x t i k)=
      2*((s-D.p i)*r D h s n j x t i*c D h s n j x t k)
    have he : (D.p i+D.q k)^2*K D h s (n+1) j x t i k+
      ((D.q k)^2-(D.p i)^2)*K D h s (n+1) j x t i k+
      (2*s)*((D.p i+D.q k)*K D h s (n+1) j x t i k)=
      2*(D.q k+s)*((D.p i+D.q k)*K D h s (n+1) j x t i k) := by ring
    rw [he,hv]
    field_simp [hs.2 k]

#print axioms c07_proved
end DLWContract
