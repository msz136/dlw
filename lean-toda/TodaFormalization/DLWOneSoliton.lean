import TodaFormalization.DLWSemidiscrete

/-!
Full pointwise algebraic verification of a one-exponential tau pair.

This module works over ANY characteristic-zero field supported by Lean.Grind,
not just Rat. Jet stores the value, x derivative, xx derivative and t derivative.
`waveJet` encodes E_x=k*E, E_xx=k^2*E, E_t=w*E.

Theorems verify the complete Hirota residuals, including constant, linear,
and quadratic exponential terms. They do not define analytic differentiation
or Real.exp: the analytic bridge from E=R^j exp(k*x+w*t+theta) to these jets
remains an explicit, ordinary calculus step outside this formalization.
-/

namespace DLWOneSoliton
open Lean.Grind

variable {K : Type} [Field K]

structure Jet (K : Type) where
  value : K
  dx : K
  dxx : K
  dt : K

def waveJet (A k w E : K) : Jet K :=
  ⟨1+A*E, A*k*E, A*k^2*E, A*w*E⟩

def hirotaX (F G : Jet K) : K := F.dx*G.value-F.value*G.dx

def hirotaB (a : K) (F G : Jet K) : K :=
  F.dxx*G.value-2*F.dx*G.dx+F.value*G.dxx
    + F.dt*G.value-F.value*G.dt+2*a*hirotaX F G

def edgeResidual (h lam a : K) (F G Fnext Gnext : Jet K) : K :=
  (hirotaB a Fnext G-hirotaB a F Gnext)/h
    +lam*(hirotaX Fnext G+hirotaX F Gnext)

theorem base_expansion (A C k w a E : K) :
    hirotaB a (waveJet A k w E) (waveJet C k w E)
    = (A*(k^2+w+2*a*k)+C*(k^2-w-2*a*k))*E := by
  simp [hirotaB, hirotaX, waveJet]
  grind

theorem edge_expansion (A C k w a E h lam R : K) :
    edgeResidual h lam a
      (waveJet A k w E) (waveJet C k w E)
      (waveJet A k w (R*E)) (waveJet C k w (R*E))
    = ((R-1)*(A*(k^2+w+2*a*k)-C*(k^2-w-2*a*k))/h
        +lam*k*(A-C)*(R+1))*E := by
  simp [edgeResidual, hirotaB, hirotaX, waveJet, Field.div_eq_mul_inv]
  grind

theorem full_one_soliton_residuals
    (A C k w a E h lam R : K)
    (hbase : A*(k^2+w+2*a*k)+C*(k^2-w-2*a*k)=0)
    (hedge : (R-1)*(A*(k^2+w+2*a*k)-C*(k^2-w-2*a*k))/h
        +lam*k*(A-C)*(R+1)=0) :
    hirotaB a (waveJet A k w E) (waveJet C k w E)=0 ∧
    edgeResidual h lam a
      (waveJet A k w E) (waveJet C k w E)
      (waveJet A k w (R*E)) (waveJet C k w (R*E))=0 := by
  rw [base_expansion, edge_expansion, hbase, hedge]
  grind

-- A concrete family from the discussion, valid for every h avoiding the pole.
variable [IsCharP K 0]

-- a=2, lambda=-2, k=3, w=3, A=1/12, C=1/3, ell=-3/4.
-- R=(8-3*h)/(8+3*h). The residual theorem itself also makes algebraic
-- sense if R=0; use R!=0 to construct a lattice indexed by all integers.
theorem concrete_one_soliton_all_steps
    (E h : K) (hh : h ≠ 0) (hpole : 8+3*h ≠ 0) :
    let R := (8-3*h)/(8+3*h)
    hirotaB 2 (waveJet (1/12) 3 3 E) (waveJet (1/3) 3 3 E)=0 ∧
    edgeResidual h (-2) 2
      (waveJet (1/12) 3 3 E) (waveJet (1/3) 3 3 E)
      (waveJet (1/12) 3 3 (R*E)) (waveJet (1/3) 3 3 (R*E))=0 := by
  apply full_one_soliton_residuals
  · simp [Field.div_eq_mul_inv]
    grind
  · simp [Field.div_eq_mul_inv]
    grind

theorem concrete_one_soliton_step_tenth (E : K) :
    hirotaB 2 (waveJet (1/12) 3 3 E) (waveJet (1/3) 3 3 E)=0 ∧
    edgeResidual (1/10) (-2) 2
      (waveJet (1/12) 3 3 E) (waveJet (1/3) 3 3 E)
      (waveJet (1/12) 3 3 ((77/83)*E))
      (waveJet (1/3) 3 3 ((77/83)*E))=0 := by
  apply full_one_soliton_residuals
  · simp [Field.div_eq_mul_inv]
    grind
  · simp [Field.div_eq_mul_inv]
    grind

end DLWOneSoliton
