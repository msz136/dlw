import PkgC02
noncomputable section
open scoped BigOperators
namespace DLWContract

example (A : XYT) (hA : Smooth3 A) : Smooth3 (sx A) := by
  simp only [c02_smooth_sx, hA]

example (A : XYT) (hA : Smooth3 A) : Smooth3 (sx (sx (sy A))) := by
  simp only [c02_smooth_sx, c02_smooth_sy, hA]

example (A : XYT) (hA : Smooth3 A) : Smooth3 (sx (sy (c02R 1 A A))) := by
  simp only [c02R, c02_smooth_add, c02_smooth_mul, c02_smooth_smul, c02_smooth_sx,
    c02_smooth_sy, c02_smooth_st, hA]

example (A B : XYT) (hA : Smooth3 A) (hB : Smooth3 B) :
    sx ((2:ℝ) • sx B * (2:ℝ) • sy (sx B))
      = sx ((2:ℝ) • sx B * (2:ℝ) • sx (sy B)) := by
  simp only [c02_smooth_add, c02_smooth_mul, c02_smooth_smul, c02_smooth_sx, c02_smooth_sy,
    c02_sx_add, c02_sx_smul, c02_sx_mul, c02_sy_sx, hA, hB]

end DLWContract
