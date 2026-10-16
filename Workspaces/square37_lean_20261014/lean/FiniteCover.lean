import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Data.List.Nodup

/-!
Finite coverage and owner reindexing, for any packing size n and cell count m.

These are abstract bridges, not a certificate for 37 squares. A geometric proof
must still supply a pointwise cell cover, capacity one for each cell, and a valid
complete census with a proved conclusion for every represented cell subset.

The architecture follows the explicit coverage and reindexing interfaces of
ofitzharding/sq17-lean (MIT), commit 0a7167efa8dcae7fa73855890630fb7e2de550ed,
FiniteOrbitCoverCheck.lean and HalfPlaneDispatch.lean; no 17-specific certificate
data or numerical bound is used here.
-/
namespace SquarePacking37.FiniteCover

/-- Full cardinality only proves coverage after row validity and distinctness. -/
theorem exhaustive_of_nodup_card (n m : ℕ) (rows : List (Finset (Fin m)))
    (unique : rows.Nodup)
    (valid : ∀ s ∈ rows, s.card = n)
    (count : rows.length = Nat.choose m n) :
    ∀ s : Finset (Fin m), s.card = n → s ∈ rows := by
  classical
  let allSubsets := (Finset.univ : Finset (Fin m)).powersetCard n
  have hsub : rows.toFinset ⊆ allSubsets := by
    intro s hs
    exact Finset.mem_powersetCard.mpr
      ⟨Finset.subset_univ _, valid s (List.mem_toFinset.mp hs)⟩
  have hrows : rows.toFinset.card = Nat.choose m n := by
    rw [List.toFinset_card_of_nodup unique, count]
  have htotal : allSubsets.card = Nat.choose m n := by
    simp [allSubsets, Finset.card_powersetCard]
  have heq : rows.toFinset = allSubsets :=
    Finset.eq_of_subset_of_card_le hsub (by rw [hrows, htotal])
  intro s hs
  apply List.mem_toFinset.mp
  rw [heq]
  exact Finset.mem_powersetCard.mpr ⟨Finset.subset_univ _, hs⟩

/-- A certified property of every valid census row holds for every n-subset. -/
theorem property_of_complete_census (n m : ℕ)
    (rows : List (Finset (Fin m))) (P : Finset (Fin m) → Prop)
    (unique : rows.Nodup)
    (valid : ∀ s ∈ rows, s.card = n)
    (count : rows.length = Nat.choose m n)
    (checked : ∀ s ∈ rows, P s) :
    ∀ s : Finset (Fin m), s.card = n → P s := by
  intro s hs
  exact checked s (exhaustive_of_nodup_card n m rows unique valid count s hs)

/-- A pointwise cover plus pairwise capacity one yields a distinct cell for
every owner. The relation can include angles or other geometric restrictions. -/
theorem injective_assignment_of_capacity (n m : ℕ)
    (belongs : Fin n → Fin m → Prop)
    (cover : ∀ i, ∃ c, belongs i c)
    (capacity : ∀ i j, i ≠ j → ∀ c, ¬ (belongs i c ∧ belongs j c)) :
    ∃ assigned : Fin n → Fin m, Function.Injective assigned ∧
      ∀ i, belongs i (assigned i) := by
  classical
  choose assigned ha using cover
  refine ⟨assigned, ?_, ha⟩
  intro i j hij
  by_contra hne
  apply capacity i j hne (assigned i)
  exact ⟨ha i, hij ▸ ha j⟩

/-- An injective assignment of n owners into an n-cell occupied set fills it. -/
theorem image_eq_of_exact_occupancy (n m : ℕ)
    (assigned : Fin n → Fin m) (occupied : Finset (Fin m))
    (hinj : Function.Injective assigned)
    (hmem : ∀ i, assigned i ∈ occupied)
    (hcard : occupied.card = n) :
    Finset.univ.image assigned = occupied := by
  classical
  apply Finset.eq_of_subset_of_card_le
  · intro c hc
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hc
    exact hmem i
  · rw [Finset.card_image_of_injective _ hinj, hcard]
    simp

/-- Two injective cell rosters with the same occupied set differ by a genuine
permutation of all n owners. No default owner or out-of-range lookup is used. -/
theorem equiv_reindex_of_image_eq (n m : ℕ)
    (assigned roster : Fin n → Fin m)
    (_hassigned : Function.Injective assigned)
    (hroster : Function.Injective roster)
    (himage : Finset.univ.image assigned = Finset.univ.image roster) :
    ∃ π : Fin n ≃ Fin n, ∀ i, assigned (π i) = roster i := by
  classical
  have hex : ∀ i, ∃ j, assigned j = roster i := by
    intro i
    have hmem : roster i ∈ Finset.univ.image assigned := by
      rw [himage]
      exact Finset.mem_image.mpr ⟨i, Finset.mem_univ i, rfl⟩
    obtain ⟨j, _, hj⟩ := Finset.mem_image.mp hmem
    exact ⟨j, hj⟩
  choose π hπ using hex
  have hinj : Function.Injective π := by
    intro i j heq
    apply hroster
    rw [← hπ i, ← hπ j, heq]
  have hbij : Function.Bijective π :=
    (Fintype.bijective_iff_injective_and_card π).mpr ⟨hinj, rfl⟩
  exact ⟨Equiv.ofBijective π hbij, hπ⟩

/-- The exact-occupancy form needed to connect geometric assignment to a
certificate's local owner ordering. -/
theorem equiv_reindex_of_exact_occupancy (n m : ℕ)
    (assigned roster : Fin n → Fin m) (occupied : Finset (Fin m))
    (hassigned : Function.Injective assigned)
    (hroster : Function.Injective roster)
    (hmem : ∀ i, assigned i ∈ occupied)
    (hcard : occupied.card = n)
    (himage : Finset.univ.image roster = occupied) :
    ∃ π : Fin n ≃ Fin n, ∀ i, assigned (π i) = roster i := by
  apply equiv_reindex_of_image_eq n m assigned roster hassigned hroster
  rw [image_eq_of_exact_occupancy n m assigned occupied hassigned hmem hcard, himage]

end SquarePacking37.FiniteCover

#print axioms SquarePacking37.FiniteCover.exhaustive_of_nodup_card
#print axioms SquarePacking37.FiniteCover.property_of_complete_census
#print axioms SquarePacking37.FiniteCover.injective_assignment_of_capacity
#print axioms SquarePacking37.FiniteCover.image_eq_of_exact_occupancy
#print axioms SquarePacking37.FiniteCover.equiv_reindex_of_image_eq
#print axioms SquarePacking37.FiniteCover.equiv_reindex_of_exact_occupancy
