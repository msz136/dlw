import CertificateData
import Mathlib.Tactic.FinCases
import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Fintype.Basic

set_option maxRecDepth 10000
set_option maxHeartbeats 0

namespace Packing37
open PackingGeometry

theorem sep_30_31 : QStrictSeparated sq_30 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_30, sq_31, normal_0]

theorem sep_30_32 : QStrictSeparated sq_30 sq_32 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_30, sq_32, normal_18]

theorem sep_30_33 : QStrictSeparated sq_30 sq_33 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_30, sq_33, normal_18]

theorem sep_30_34 : QStrictSeparated sq_30 sq_34 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_30, sq_34, normal_18]

theorem sep_30_35 : QStrictSeparated sq_30 sq_35 normal_26.1 normal_26.2 := by
  norm_num [QStrictSeparated, qsupport, sq_30, sq_35, normal_26]

theorem sep_30_36 : QStrictSeparated sq_30 sq_36 normal_17.1 normal_17.2 := by
  norm_num [QStrictSeparated, qsupport, sq_30, sq_36, normal_17]

theorem row_30 : ∀ j : Fin 37, (30 : Fin 37) < j →
    QStrictSeparated (squares 30) (squares j) (normal 30 j).1 (normal 30 j).2 := by
  intro j h
  fin_cases j
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · exact sep_30_31
  · exact sep_30_32
  · exact sep_30_33
  · exact sep_30_34
  · exact sep_30_35
  · exact sep_30_36

theorem sep_31_32 : QStrictSeparated sq_31 sq_32 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_31, sq_32, normal_6]

theorem sep_31_33 : QStrictSeparated sq_31 sq_33 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_31, sq_33, normal_18]

theorem sep_31_34 : QStrictSeparated sq_31 sq_34 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_31, sq_34, normal_6]

theorem sep_31_35 : QStrictSeparated sq_31 sq_35 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_31, sq_35, normal_6]

theorem sep_31_36 : QStrictSeparated sq_31 sq_36 normal_17.1 normal_17.2 := by
  norm_num [QStrictSeparated, qsupport, sq_31, sq_36, normal_17]

theorem row_31 : ∀ j : Fin 37, (31 : Fin 37) < j →
    QStrictSeparated (squares 31) (squares j) (normal 31 j).1 (normal 31 j).2 := by
  intro j h
  fin_cases j
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · exact sep_31_32
  · exact sep_31_33
  · exact sep_31_34
  · exact sep_31_35
  · exact sep_31_36

theorem sep_32_33 : QStrictSeparated sq_32 sq_33 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_32, sq_33, normal_18]

theorem sep_32_34 : QStrictSeparated sq_32 sq_34 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_32, sq_34, normal_6]

theorem sep_32_35 : QStrictSeparated sq_32 sq_35 normal_26.1 normal_26.2 := by
  norm_num [QStrictSeparated, qsupport, sq_32, sq_35, normal_26]

theorem sep_32_36 : QStrictSeparated sq_32 sq_36 normal_17.1 normal_17.2 := by
  norm_num [QStrictSeparated, qsupport, sq_32, sq_36, normal_17]

theorem row_32 : ∀ j : Fin 37, (32 : Fin 37) < j →
    QStrictSeparated (squares 32) (squares j) (normal 32 j).1 (normal 32 j).2 := by
  intro j h
  fin_cases j
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · exact sep_32_33
  · exact sep_32_34
  · exact sep_32_35
  · exact sep_32_36

theorem sep_33_34 : QStrictSeparated sq_33 sq_34 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_33, sq_34, normal_6]

theorem sep_33_35 : QStrictSeparated sq_33 sq_35 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_33, sq_35, normal_6]

theorem sep_33_36 : QStrictSeparated sq_33 sq_36 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_33, sq_36, normal_6]

theorem row_33 : ∀ j : Fin 37, (33 : Fin 37) < j →
    QStrictSeparated (squares 33) (squares j) (normal 33 j).1 (normal 33 j).2 := by
  intro j h
  fin_cases j
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · exact sep_33_34
  · exact sep_33_35
  · exact sep_33_36

theorem sep_34_35 : QStrictSeparated sq_34 sq_35 normal_26.1 normal_26.2 := by
  norm_num [QStrictSeparated, qsupport, sq_34, sq_35, normal_26]

theorem sep_34_36 : QStrictSeparated sq_34 sq_36 normal_26.1 normal_26.2 := by
  norm_num [QStrictSeparated, qsupport, sq_34, sq_36, normal_26]

theorem row_34 : ∀ j : Fin 37, (34 : Fin 37) < j →
    QStrictSeparated (squares 34) (squares j) (normal 34 j).1 (normal 34 j).2 := by
  intro j h
  fin_cases j
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · exact sep_34_35
  · exact sep_34_36

theorem sep_35_36 : QStrictSeparated sq_35 sq_36 normal_26.1 normal_26.2 := by
  norm_num [QStrictSeparated, qsupport, sq_35, sq_36, normal_26]

theorem row_35 : ∀ j : Fin 37, (35 : Fin 37) < j →
    QStrictSeparated (squares 35) (squares j) (normal 35 j).1 (normal 35 j).2 := by
  intro j h
  fin_cases j
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · exact sep_35_36

end Packing37
