import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

example (x N : ℕ) (hN : N % 2 = 0) : (x % N) % 2 = x % 2 := by
  omega

example (x N : ℕ) (hN : N % 2 = 0) : (x + N) % 2 = x % 2 := by
  omega

example (x N : ℕ) (hN : N % 2 = 0) : (x + 2) % N % 2 = x % 2 := by
  omega
