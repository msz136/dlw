/-
DLW endpoint contracts, 2026-09-22.
This module DEFINES propositions. It contains NO proofs of these propositions.
Successful elaboration would check types, not establish any contract.
Use namespace DLWContract in separate proof modules; do not change these targets.
Real, globally smooth/positive fields are the initial scope. Local/complex versions
are separate extensions, not silently interchangeable with this interface.
-/
import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Topology.Algebra.Order.Field

noncomputable section
open scoped BigOperators
namespace DLWContract

abbrev XT := ℝ → ℝ → ℝ
abbrev XYT := ℝ → ℝ → ℝ → ℝ
abbrev Lattice := ℤ → XT
def dx (f : XT) : XT := fun x t => deriv (fun z => f z t) x
def dt (f : XT) : XT := fun x t => deriv (f x) t
def xx (f : XT) : XT := dx (dx f)
def sx (f : XYT) : XYT := fun x y t => deriv (fun z => f z y t) x
def sy (f : XYT) : XYT := fun x y t => deriv (fun z => f x z t) y
def st (f : XYT) : XYT := fun x y t => deriv (f x y) t
def slice (f : XYT) (y : ℝ) : XT := fun x t => f x y t
def SmoothXT (f : XT) : Prop := ContDiff ℝ ⊤ (fun z : ℝ × ℝ => f z.1 z.2)
def Smooth3 (f : XYT) : Prop :=
  ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => f z.1 z.2.1 z.2.2)
def SmoothL (f : Lattice) : Prop := ∀ j, SmoothXT (f j)
def PositiveL (f : Lattice) : Prop := ∀ j x t, 0 < f j x t
def Positive3 (f : XYT) : Prop := ∀ x y t, 0 < f x y t

def hx (f g : XT) : XT := dx f * g - f * dx g
def bil (a : ℝ) (f g : XT) : XT :=
  xx f * g - 2 * dx f * dx g + f * xx g + dt f * g - f * dt g + (2*a) • hx f g
def cbil (a : ℝ) (f g : XYT) : XYT := fun x y t => bil a (slice f y) (slice g y) x t
def chx (f g : XYT) : XYT := fun x y t => hx (slice f y) (slice g y) x t
def cdybil (a : ℝ) (f g : XYT) : XYT := cbil a (sy f) g - cbil a f (sy g)
def ContinuousPair (a : ℝ) (f g : XYT) : Prop :=
  cbil a f g = 0 ∧ cdybil a f g - 4 * chx f g = 0
def SemiPair (a h : ℝ) (F G : Lattice) : Prop :=
  ∀ j, bil (a-h/2) (F j) (G j) = 0 ∧ bil (a+h/2) (F j) (G (j+1)) = 0

def dm (h : ℝ) (z : Lattice) : Lattice := fun j => (1/h) • (z j-z (j-1))
def d0 (h : ℝ) (z : Lattice) : Lattice := fun j => (1/(2*h)) • (z (j+1)-z (j-1))
def mm (z : Lattice) : Lattice := fun j => (z j+z (j-1))/2
def lap (h : ℝ) (z : Lattice) : Lattice := fun j => (1/h^2) • (z (j+1)-2*z j+z (j-1))
def lx (z : Lattice) : Lattice := fun j => dx (z j)
def lt (z : Lattice) : Lattice := fun j => dt (z j)
def lxx (z : Lattice) : Lattice := lx (lx z)
def logL (z : Lattice) : Lattice := fun j x t => Real.log (z j x t)
def physU (F G : Lattice) : Lattice :=
  lx (2*logL F-logL G-(fun j => logL G (j+1)))
def physV (h : ℝ) (F G : Lattice) : Lattice :=
  (4/h) • lx ((fun j => logL G (j+1))-logL G)+d0 h (physU F G)
def W (h : ℝ) (u v : Lattice) : Lattice := v-d0 h u
def H (a h : ℝ) (u v : Lattice) : Lattice :=
  u^2/2+(2*a) • u+h^2 • ((W h u v)^2/32-W h u v/4)
def n1 (a h : ℝ) (u v : Lattice) : Lattice :=
  dm h (lt u+lx (H a h u v))+lxx (mm v-(h^2/4) • lap h (dm h u))
def n2 (a h : ℝ) (u v : Lattice) : Lattice :=
  lt v+lx (d0 h (H a h u v)+(u+(fun _ _ _ => 2*a))*W h u v-4*u)
    +lxx (d0 h u+(h^2/4) • lap h (W h u v))
def NonlinearPair (a h : ℝ) (u v : Lattice) : Prop := n1 a h u v=0 ∧ n2 a h u v=0
def cu (f g : XYT) : XYT :=
  2*sx (fun x y t => Real.log (f x y t)-Real.log (g x y t))
def cv (f g : XYT) : XYT :=
  2*sx (sy (fun x y t => Real.log (f x y t)+Real.log (g x y t)))
def c1 (a : ℝ) (u v : XYT) : XYT := sy (st u)+sx (sx v)+sx (u*sy u)+(2*a) • sx (sy u)
def c2 (a : ℝ) (u v : XYT) : XYT := st v+sx (u*v)+sx (sx (sy u))+(2*a) • sx v-4*sx u

/- C01: product-rule bridge to the actual continuous Hirota equation. -/
def C01 : Prop := ∀ (a : ℝ) (f g : XYT), Smooth3 f → Smooth3 g →
  cbil a f g=0 →
  (cdybil a f g-4*chx f g=0 ↔ cbil a f (sy g)+2*chx f g=0)
/- C02: continuous bilinear -> physical DLW, lambda = -2. -/
def C02 : Prop := ∀ (a : ℝ) (f g : XYT), Smooth3 f → Smooth3 g →
  Positive3 f → Positive3 g → ContinuousPair a f g →
  c1 a (cu f g) (cv f g)=0 ∧ c2 a (cu f g) (cv f g)=0

/- C03: uniqueness only within the specified centered two-wall template. -/
def C03 : Prop := ∀ (a h left right : ℝ), h≠0 →
  (∀ b : ℝ, (left+right)*b=0) →
  (∀ b : ℝ, 2*(right-left)*b=2*h*b) →
  a+left=a-h/2 ∧ a+right=a+h/2

structure Data (N : ℕ) where
  a : ℝ
  p : Fin N → ℝ
  q : Fin N → ℝ
  rho : Fin N → ℝ
def lam (h z : ℝ) : ℝ := (z+h/2)/(z-h/2)
def chi {N : ℕ} (D : Data N) (h : ℝ) (i k : Fin N) : ℝ :=
  lam h (D.p i-D.a)*lam h (D.q k+D.a)
def gamma {N : ℕ} (D : Data N) (s : ℝ) (i k : Fin N) : ℝ := -(D.p i-s)/(D.q k+s)
def Admissible {N : ℕ} (D : Data N) (h : ℝ) : Prop :=
  h≠0 ∧ (∀ i k, D.p i+D.q k≠0) ∧
  (∀ i, D.p i-D.a-h/2≠0 ∧ D.p i-D.a+h/2≠0) ∧
  (∀ k, D.q k+D.a-h/2≠0 ∧ D.q k+D.a+h/2≠0)
def LayerOK {N : ℕ} (D : Data N) (s : ℝ) : Prop :=
  (∀ i, D.p i-s≠0) ∧ (∀ k, D.q k+s≠0)
def PositiveData {N : ℕ} (D : Data N) (h : ℝ) : Prop :=
  0<h ∧ StrictMono D.p ∧ StrictMono D.q ∧
  (∀ i, 0<D.p i ∧ D.p i<D.a-h/2 ∧ 0<D.q i ∧ 0<D.rho i)
def entry {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (i k : Fin N) : XT :=
  fun x t => (if i=k then 1 else 0)+D.rho i/(D.p i+D.q k)*
    (gamma D s i k)^n*(chi D h i k)^j*
    Real.exp ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t)
def tau {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) : XT :=
  fun x t => Matrix.det (fun i k => entry D h s n j i k x t)
def F {N : ℕ} (D : Data N) (h : ℝ) : Lattice := tau D h (D.a-h/2) 1
def G {N : ℕ} (D : Data N) (h : ℝ) : Lattice := tau D h D.a 0

/- C04: the actual matrix includes the identity delta_ik. -/
def C04 : Prop := ∀ (N : ℕ) (D : Data N) (h : ℝ), Admissible D h →
  ∀ (n j : ℤ) (i k : Fin N),
  entry D h (D.a-h/2) n j i k=entry D h (D.a+h/2) n (j+n) i k
def C05 : Prop := ∀ (N : ℕ) (D : Data N) (h : ℝ), Admissible D h →
  ∀ n j, tau D h (D.a-h/2) n j=tau D h (D.a+h/2) n (j+n)

/- C06: actual derivative/update identities, not arbitrary independent jets. -/
def C06 : Prop := ∀ (N : ℕ) (D : Data N) (h s : ℝ),
  Admissible D h → LayerOK D s → ∀ n j i k,
  let e := entry D h s n j i k
  let c : XT := fun _ _ => if i=k then 1 else 0
  dx e=(D.p i+D.q k) • (e-c) ∧
  dt e=((D.q k)^2-(D.p i)^2) • (e-c) ∧
  entry D h s (n+1) j i k=e-((D.p i+D.q k)/(D.q k+s)) • (e-c)
/- C07: the formerly assumed reservoir must now be PROVED for this determinant. -/
def C07 : Prop := ∀ (N : ℕ) (D : Data N) (h s : ℝ),
  Admissible D h → LayerOK D s → ∀ n j,
  bil s (tau D h s (n+1) j) (tau D h s n j)=0
def C08 : Prop := ∀ (N : ℕ) (D : Data N) (h : ℝ),
  Admissible D h → SemiPair D.a h (F D h) (G D h)
def C09 : Prop := ∀ (N : ℕ) (D : Data N) (h : ℝ), PositiveData D h →
  Admissible D h ∧ PositiveL (F D h) ∧ PositiveL (G D h) ∧
  SmoothL (F D h) ∧ SmoothL (G D h)

def interaction (p₁ p₂ q₁ q₂ : ℝ) : ℝ :=
  ((p₁-p₂)*(q₁-q₂))/((p₁+q₂)*(p₂+q₁))
/- C10: actual N=2 tau expansion fixes normalized interaction, all integer layers. -/
def C10 : Prop := ∀ (D : Data 2) (h s : ℝ), Admissible D h → LayerOK D s →
  ∀ n j x t,
  let e₀ := entry D h s n j 0 0 x t-1
  let e₁ := entry D h s n j 1 1 x t-1
  tau D h s n j x t=1+e₀+e₁+interaction (D.p 0) (D.p 1) (D.q 0) (D.q 1)*e₀*e₁

def PowBound (p : ℕ) (e : ℝ → ℝ) : Prop :=
  ∃ C : ℝ, 0≤C ∧ ∃ ε : ℝ, 0<ε ∧ ∀ h : ℝ, 0 < |h| → |h| < ε → |e h|≤C*|h|^p
def wallMinus (a h y : ℝ) (f g : XYT) : XT := bil (a-h/2) (slice f y) (slice g (y-h/2))
def wallPlus (a h y : ℝ) (f g : XYT) : XT := bil (a+h/2) (slice f y) (slice g (y+h/2))
/- C11: fixed physical y, not fixed j; both residual combinations retained. -/
def C11 : Prop := ∀ (a : ℝ) (f g : XYT), Smooth3 f → Smooth3 g → ∀ x y t,
  PowBound 2 (fun h => (wallPlus a h y f g x t+wallMinus a h y f g x t)/2-cbil a f g x y t) ∧
  PowBound 2 (fun h => (wallPlus a h y f g x t-wallMinus a h y f g x t)/h-
    (cbil a f (sy g) x y t+2*chx f g x y t))
def C12 : Prop := ∀ P : ℝ, P≠0 → PowBound 2 (fun h => Real.log (lam h P)/h-1/P)

def normA (a h : ℝ) (F G : Lattice) : Lattice :=
  fun j => bil (a-h/2) (F j) (G j)/(F j*G j)
def normC (a h : ℝ) (F G : Lattice) : Lattice :=
  fun j => bil (a+h/2) (F j) (G (j+1))/(F j*G (j+1))
/- C13: normalized Hirota quotient identity with REAL derivatives. -/
def C13 : Prop := ∀ (a : ℝ) (f g : XT), SmoothXT f → SmoothXT g →
  (∀ x t, 0<f x t ∧ 0<g x t) →
  let α : XT := fun x t => Real.log (f x t)
  let β : XT := fun x t => Real.log (g x t)
  bil a f g/(f*g)=xx (α+β)+(dx (α-β))^2+dt (α-β)+(2*a) • dx (α-β)
/- C14: identities before imposing equations: stronger than mere implication. -/
def C14 : Prop := ∀ (a h : ℝ) (F G : Lattice), h≠0 →
  SmoothL F → SmoothL G → PositiveL F → PositiveL G →
  let u := physU F G
  let v := physV h F G
  let A := normA a h F G
  let C := normC a h F G
  n1 a h u v=dm h (lx (A+C)) ∧
  n2 a h u v=d0 h (lx (A+C))+(4/h) • lx (A-C)
def C15 : Prop := ∀ (a h : ℝ) (F G : Lattice), h≠0 →
  SmoothL F → SmoothL G → PositiveL F → PositiveL G → SemiPair a h F G →
  NonlinearPair a h (physU F G) (physV h F G)
def C16 : Prop := ∀ (N : ℕ) (D : Data N) (h : ℝ), PositiveData D h →
  NonlinearPair D.a h (physU (F D h) (G D h)) (physV h (F D h) (G D h))

def sampleF (h : ℝ) (f : XYT) : Lattice := fun j => slice f (((j : ℝ)+1/2)*h)
def sampleG (h : ℝ) (g : XYT) : Lattice := fun j => slice g ((j : ℝ)*h)
def interpU (h : ℝ) (f g : XYT) : XYT := sx (fun x y t =>
  2*Real.log (f x y t)-Real.log (g x (y-h/2) t)-Real.log (g x (y+h/2) t))
def interpV (h : ℝ) (f g : XYT) : XYT :=
  (4/h) • sx (fun x y t => Real.log (g x (y+h/2) t)-Real.log (g x (y-h/2) t))+
  (fun x y t => (interpU h f g x (y+h) t-interpU h f g x (y-h) t)/(2*h))
def C17 : Prop := ∀ (f g : XYT), Smooth3 f → Smooth3 g → Positive3 f → Positive3 g →
  (∀ h, physU (sampleF h f) (sampleG h g)=sampleF h (interpU h f g) ∧
    physV h (sampleF h f) (sampleG h g)=sampleF h (interpV h f g)) ∧
  ∀ x y t, PowBound 2 (fun h => interpU h f g x y t-cu f g x y t) ∧
    PowBound 2 (fun h => interpV h f g x y t-cv f g x y t)
def localSamples (y h : ℝ) (u : XYT) : Lattice := fun j => slice u (y+(j : ℝ)*h)
/- N1 evaluated at j=0 lives at y-h/2; N2 lives at y. -/
def C18 : Prop := ∀ (a : ℝ) (u v : XYT), Smooth3 u → Smooth3 v → ∀ x y t,
  PowBound 2 (fun h => n1 a h (localSamples y h u) (localSamples y h v) 0 x t-c1 a u v x (y-h/2) t) ∧
  PowBound 2 (fun h => n2 a h (localSamples y h u) (localSamples y h v) 0 x t-c2 a u v x y t)

def JW (a h : ℝ) (u v : Lattice) : Lattice := (u+(fun _ _ _ => 2*a))*W h u v-4*u-lx (W h u v)
def JV (a h : ℝ) (u v : Lattice) : Lattice :=
  d0 h (H a h u v)+(u+(fun _ _ _ => 2*a))*W h u v-4*u+lx (d0 h u+(h^2/4) • lap h (W h u v))
def C19 : Prop := ∀ (a h : ℝ) (u v : Lattice), h≠0 → SmoothL u → SmoothL v →
  NonlinearPair a h u v → lt (W h u v)+lx (JW a h u v)=0 ∧ lt v+lx (JV a h u v)=0
def PeriodicL (m : ℕ) (z : Lattice) : Prop := ∀ j, z (j+(m : ℤ))=z j
def C20 : Prop := ∀ (m : ℕ) (a h : ℝ) (u v : Lattice), 0<m → h≠0 →
  SmoothL u → SmoothL v → PeriodicL m u → PeriodicL m v → NonlinearPair a h u v →
  xx (∑ j ∈ Finset.range m, v (j : ℤ))=0
/- C21 demonstrates the undetermined mean: any smooth time-only u, v=0 solves. -/
def C21 : Prop := ∀ (a h : ℝ) (c : ℝ → ℝ), ContDiff ℝ ⊤ c → h≠0 →
  NonlinearPair a h (fun _ _ t => c t) 0

/- Explicit interpolation for finite-h Gram families and their continuous limit. -/
def tauI {N : ℕ} (D : Data N) (h s : ℝ) (n : ℤ) (offset : ℝ) : XYT :=
  fun x y t => Matrix.det (fun i k => (if i=k then 1 else 0)+
    D.rho i/(D.p i+D.q k)*(gamma D s i k)^n*
    Real.exp ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t+
      (y/h-offset)*Real.log (chi D h i k)))
def tau0 {N : ℕ} (D : Data N) (n : ℤ) : XYT :=
  fun x y t => Matrix.det (fun i k => (if i=k then 1 else 0)+
    D.rho i/(D.p i+D.q k)*(gamma D D.a i k)^n*
    Real.exp ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t+
      y*(1/(D.p i-D.a)+1/(D.q k+D.a))))
def UniformBoxO2 (e : ℝ → XYT) : Prop := ∀ R : ℝ, 0<R →
  ∃ C : ℝ, 0≤C ∧ ∃ ε : ℝ, 0<ε ∧ ∀ h x y t : ℝ,
    0<h → h<ε → |x|≤R → |y|≤R → |t|≤R → |e h x y t|≤C*h^2
def C22 : Prop := ∀ (N : ℕ) (D : Data N) (h₀ : ℝ), PositiveData D h₀ →
  UniformBoxO2 (fun h => interpU h (tauI D h (D.a-h/2) 1 (1/2)) (tauI D h D.a 0 0)-cu (tau0 D 1) (tau0 D 0)) ∧
  UniformBoxO2 (fun h => interpV h (tauI D h (D.a-h/2) 1 (1/2)) (tauI D h D.a 0 0)-cv (tau0 D 1) (tau0 D 0))
def C23 : Prop := ∀ (N : ℕ) (D : Data N) (h₀ : ℝ), PositiveData D h₀ →
  ContinuousPair D.a (tau0 D 1) (tau0 D 0)
def C24 : Prop := ∀ (N : ℕ) (D : Data N) (h : ℝ), PositiveData D h →
  sampleF h (tauI D h (D.a-h/2) 1 (1/2))=F D h ∧ sampleG h (tauI D h D.a 0 0)=G D h

def linearH (a h : ℝ) (u v : Lattice) : Lattice := (2*a) • u-(h^2/4) • W h u v
def linearN1 (a h : ℝ) (u v : Lattice) : Lattice :=
  dm h (lt u+lx (linearH a h u v))+lxx (mm v-(h^2/4) • lap h (dm h u))
def linearN2 (a h : ℝ) (u v : Lattice) : Lattice :=
  lt v+lx (d0 h (linearH a h u v)+(2*a) • W h u v-4*u)+
    lxx (d0 h u+(h^2/4) • lap h (W h u v))
/- C25 is the actual amplitude derivative, not a guessed dispersion polynomial. -/
def C25 : Prop := ∀ (a h : ℝ) (u v : Lattice), h≠0 → SmoothL u → SmoothL v → ∀ j x t,
  deriv (fun ε : ℝ => n1 a h (ε • u) (ε • v) j x t) 0=linearN1 a h u v j x t ∧
  deriv (fun ε : ℝ => n2 a h (ε • u) (ε • v) j x t) 0=linearN2 a h u v j x t

/- Numerical contracts: finite dimensional, conditional, no global DLW stability. -/
def euler {m : ℕ} (f : ℝ → (Fin m → ℝ) → (Fin m → ℝ)) (t h : ℝ) (z : Fin m → ℝ) :=
  z+h • f t z
def rk4 {m : ℕ} (f : ℝ → (Fin m → ℝ) → (Fin m → ℝ)) (t h : ℝ) (z : Fin m → ℝ) :=
  let k₁ := f t z
  let k₂ := f (t+h/2) (z+(h/2) • k₁)
  let k₃ := f (t+h/2) (z+(h/2) • k₂)
  let k₄ := f (t+h) (z+h • k₃)
  z+(h/6) • (k₁+2 • k₂+2 • k₃+k₄)
def trapResidual {m : ℕ} (f : ℝ → (Fin m → ℝ) → (Fin m → ℝ))
    (t h : ℝ) (z z' : Fin m → ℝ) := z'-z-(h/2) • (f t z+f (t+h) z')
def N01 : Prop := ∀ (m : ℕ) (f : ℝ → (Fin m → ℝ) → (Fin m → ℝ))
  (z : ℝ → (Fin m → ℝ)),
  ContDiff ℝ ⊤ (fun q : ℝ × (Fin m → ℝ) => f q.1 q.2) → ContDiff ℝ ⊤ z →
  (∀ t, HasDerivAt z (f t (z t)) t) → ∀ t,
  PowBound 2 (fun h => ‖z (t+h)-euler f t h (z t)‖) ∧
  PowBound 5 (fun h => ‖z (t+h)-rk4 f t h (z t)‖) ∧
  PowBound 3 (fun h => ‖trapResidual f t h (z t) (z (t+h))‖)
/- Recurrence includes all per-step defects; instantiation is a separate obligation. -/
def N02 : Prop := ∀ (e : ℕ → ℝ) (q η : ℝ), 0≤q → 0≤η →
  (∀ n, e (n+1)≤q*e n+η) → ∀ n,
  e n≤q^n*e 0+η*∑ i ∈ Finset.range n, q^i
def N03 : Prop := ∀ (m : ℕ) (computed exactH exact0 : Fin m → ℝ),
  ‖computed-exact0‖≤‖computed-exactH‖+‖exactH-exact0‖
/- This verifies a finite sample ONLY AFTER real reference enclosures are proved. -/
def N04 : Prop := ∀ (m : ℕ) (computed lo hi : Fin m → ℚ) (reference : Fin m → ℝ) (tol : ℚ),
  0≤tol → (∀ i, (lo i : ℝ)≤reference i ∧ reference i≤(hi i : ℝ)) →
  (∀ i, |computed i-lo i|≤tol ∧ |computed i-hi i|≤tol) →
  ∀ i, |(computed i : ℝ)-reference i|≤(tol : ℝ)
/- Open-chain reconstruction; the time-dependent left value must be supplied. -/
def reconstruct (h b : ℝ) (p : ℕ → ℝ) (j : ℕ) : ℝ :=
  b+h*∑ k ∈ Finset.range j, p (k+1)
def N05 : Prop := ∀ (h b : ℝ) (p : ℕ → ℝ), h≠0 → reconstruct h b p 0=b ∧
  ∀ j, (reconstruct h b p (j+1)-reconstruct h b p j)/h=p (j+1)
/- Scalar diagnostic; must not be promoted to stability of the full nonlinear PDE. -/
def N06 : Prop := ∀ (g Δt : ℝ), 0<g → 0<Δt → 1<1+Δt*g ∧ 1<Real.exp (Δt*g)
def N07 : Prop := ∀ (seed tolerance g T : ℝ), 0<seed → seed≤tolerance →
  0≤g → 0≤T → g*T≤Real.log (tolerance/seed) → seed*Real.exp (g*T)≤tolerance

end DLWContract
