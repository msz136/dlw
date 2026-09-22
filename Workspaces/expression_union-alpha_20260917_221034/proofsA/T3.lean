structure Jet (R : Type*) where
  value : R

theorem t (F : Jet Nat) : F.value = F.value := rfl
