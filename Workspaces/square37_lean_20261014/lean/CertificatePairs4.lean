import CertificateData
import Mathlib.Tactic.FinCases
import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Fintype.Basic

set_option maxRecDepth 10000
set_option maxHeartbeats 0

namespace Packing37
open PackingGeometry

theorem sep_24_25 : QStrictSeparated sq_24 sq_25 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_24, sq_25, normal_6]

theorem sep_24_26 : QStrictSeparated sq_24 sq_26 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_24, sq_26, normal_6]

theorem sep_24_27 : QStrictSeparated sq_24 sq_27 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_24, sq_27, normal_6]

theorem sep_24_28 : QStrictSeparated sq_24 sq_28 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_24, sq_28, normal_18]

theorem sep_24_29 : QStrictSeparated sq_24 sq_29 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_24, sq_29, normal_18]

theorem sep_24_30 : QStrictSeparated sq_24 sq_30 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_24, sq_30, normal_6]

theorem sep_24_31 : QStrictSeparated sq_24 sq_31 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_24, sq_31, normal_18]

theorem sep_24_32 : QStrictSeparated sq_24 sq_32 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_24, sq_32, normal_18]

theorem sep_24_33 : QStrictSeparated sq_24 sq_33 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_24, sq_33, normal_18]

theorem sep_24_34 : QStrictSeparated sq_24 sq_34 normal_26.1 normal_26.2 := by
  norm_num [QStrictSeparated, qsupport, sq_24, sq_34, normal_26]

theorem sep_24_35 : QStrictSeparated sq_24 sq_35 normal_26.1 normal_26.2 := by
  norm_num [QStrictSeparated, qsupport, sq_24, sq_35, normal_26]

theorem sep_24_36 : QStrictSeparated sq_24 sq_36 normal_17.1 normal_17.2 := by
  norm_num [QStrictSeparated, qsupport, sq_24, sq_36, normal_17]

theorem row_24 : ∀ j : Fin 37, (24 : Fin 37) < j →
    QStrictSeparated (squares 24) (squares j) (normal 24 j).1 (normal 24 j).2 := by
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
  · exact sep_24_25
  · exact sep_24_26
  · exact sep_24_27
  · exact sep_24_28
  · exact sep_24_29
  · exact sep_24_30
  · exact sep_24_31
  · exact sep_24_32
  · exact sep_24_33
  · exact sep_24_34
  · exact sep_24_35
  · exact sep_24_36

theorem sep_25_26 : QStrictSeparated sq_25 sq_26 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_25, sq_26, normal_6]

theorem sep_25_27 : QStrictSeparated sq_25 sq_27 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_25, sq_27, normal_6]

theorem sep_25_28 : QStrictSeparated sq_25 sq_28 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_25, sq_28, normal_18]

theorem sep_25_29 : QStrictSeparated sq_25 sq_29 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_25, sq_29, normal_18]

theorem sep_25_30 : QStrictSeparated sq_25 sq_30 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_25, sq_30, normal_18]

theorem sep_25_31 : QStrictSeparated sq_25 sq_31 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_25, sq_31, normal_18]

theorem sep_25_32 : QStrictSeparated sq_25 sq_32 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_25, sq_32, normal_18]

theorem sep_25_33 : QStrictSeparated sq_25 sq_33 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_25, sq_33, normal_18]

theorem sep_25_34 : QStrictSeparated sq_25 sq_34 normal_26.1 normal_26.2 := by
  norm_num [QStrictSeparated, qsupport, sq_25, sq_34, normal_26]

theorem sep_25_35 : QStrictSeparated sq_25 sq_35 normal_26.1 normal_26.2 := by
  norm_num [QStrictSeparated, qsupport, sq_25, sq_35, normal_26]

theorem sep_25_36 : QStrictSeparated sq_25 sq_36 normal_17.1 normal_17.2 := by
  norm_num [QStrictSeparated, qsupport, sq_25, sq_36, normal_17]

theorem row_25 : ∀ j : Fin 37, (25 : Fin 37) < j →
    QStrictSeparated (squares 25) (squares j) (normal 25 j).1 (normal 25 j).2 := by
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
  · exact sep_25_26
  · exact sep_25_27
  · exact sep_25_28
  · exact sep_25_29
  · exact sep_25_30
  · exact sep_25_31
  · exact sep_25_32
  · exact sep_25_33
  · exact sep_25_34
  · exact sep_25_35
  · exact sep_25_36

theorem sep_26_27 : QStrictSeparated sq_26 sq_27 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_26, sq_27, normal_6]

theorem sep_26_28 : QStrictSeparated sq_26 sq_28 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_26, sq_28, normal_0]

theorem sep_26_29 : QStrictSeparated sq_26 sq_29 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_26, sq_29, normal_18]

theorem sep_26_30 : QStrictSeparated sq_26 sq_30 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_26, sq_30, normal_18]

theorem sep_26_31 : QStrictSeparated sq_26 sq_31 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_26, sq_31, normal_18]

theorem sep_26_32 : QStrictSeparated sq_26 sq_32 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_26, sq_32, normal_18]

theorem sep_26_33 : QStrictSeparated sq_26 sq_33 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_26, sq_33, normal_18]

theorem sep_26_34 : QStrictSeparated sq_26 sq_34 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_26, sq_34, normal_18]

theorem sep_26_35 : QStrictSeparated sq_26 sq_35 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_26, sq_35, normal_18]

theorem sep_26_36 : QStrictSeparated sq_26 sq_36 normal_17.1 normal_17.2 := by
  norm_num [QStrictSeparated, qsupport, sq_26, sq_36, normal_17]

theorem row_26 : ∀ j : Fin 37, (26 : Fin 37) < j →
    QStrictSeparated (squares 26) (squares j) (normal 26 j).1 (normal 26 j).2 := by
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
  · exact sep_26_27
  · exact sep_26_28
  · exact sep_26_29
  · exact sep_26_30
  · exact sep_26_31
  · exact sep_26_32
  · exact sep_26_33
  · exact sep_26_34
  · exact sep_26_35
  · exact sep_26_36

theorem sep_27_28 : QStrictSeparated sq_27 sq_28 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_27, sq_28, normal_0]

theorem sep_27_29 : QStrictSeparated sq_27 sq_29 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_27, sq_29, normal_0]

theorem sep_27_30 : QStrictSeparated sq_27 sq_30 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_27, sq_30, normal_18]

theorem sep_27_31 : QStrictSeparated sq_27 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_27, sq_31, normal_0]

theorem sep_27_32 : QStrictSeparated sq_27 sq_32 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_27, sq_32, normal_18]

theorem sep_27_33 : QStrictSeparated sq_27 sq_33 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_27, sq_33, normal_18]

theorem sep_27_34 : QStrictSeparated sq_27 sq_34 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_27, sq_34, normal_18]

theorem sep_27_35 : QStrictSeparated sq_27 sq_35 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_27, sq_35, normal_18]

theorem sep_27_36 : QStrictSeparated sq_27 sq_36 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_27, sq_36, normal_18]

theorem row_27 : ∀ j : Fin 37, (27 : Fin 37) < j →
    QStrictSeparated (squares 27) (squares j) (normal 27 j).1 (normal 27 j).2 := by
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
  · exact sep_27_28
  · exact sep_27_29
  · exact sep_27_30
  · exact sep_27_31
  · exact sep_27_32
  · exact sep_27_33
  · exact sep_27_34
  · exact sep_27_35
  · exact sep_27_36

theorem sep_28_29 : QStrictSeparated sq_28 sq_29 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_28, sq_29, normal_6]

theorem sep_28_30 : QStrictSeparated sq_28 sq_30 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_28, sq_30, normal_6]

theorem sep_28_31 : QStrictSeparated sq_28 sq_31 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_28, sq_31, normal_18]

theorem sep_28_32 : QStrictSeparated sq_28 sq_32 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_28, sq_32, normal_18]

theorem sep_28_33 : QStrictSeparated sq_28 sq_33 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_28, sq_33, normal_18]

theorem sep_28_34 : QStrictSeparated sq_28 sq_34 normal_26.1 normal_26.2 := by
  norm_num [QStrictSeparated, qsupport, sq_28, sq_34, normal_26]

theorem sep_28_35 : QStrictSeparated sq_28 sq_35 normal_26.1 normal_26.2 := by
  norm_num [QStrictSeparated, qsupport, sq_28, sq_35, normal_26]

theorem sep_28_36 : QStrictSeparated sq_28 sq_36 normal_17.1 normal_17.2 := by
  norm_num [QStrictSeparated, qsupport, sq_28, sq_36, normal_17]

theorem row_28 : ∀ j : Fin 37, (28 : Fin 37) < j →
    QStrictSeparated (squares 28) (squares j) (normal 28 j).1 (normal 28 j).2 := by
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
  · exact sep_28_29
  · exact sep_28_30
  · exact sep_28_31
  · exact sep_28_32
  · exact sep_28_33
  · exact sep_28_34
  · exact sep_28_35
  · exact sep_28_36

theorem sep_29_30 : QStrictSeparated sq_29 sq_30 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_29, sq_30, normal_6]

theorem sep_29_31 : QStrictSeparated sq_29 sq_31 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_29, sq_31, normal_18]

theorem sep_29_32 : QStrictSeparated sq_29 sq_32 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_29, sq_32, normal_18]

theorem sep_29_33 : QStrictSeparated sq_29 sq_33 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_29, sq_33, normal_18]

theorem sep_29_34 : QStrictSeparated sq_29 sq_34 normal_26.1 normal_26.2 := by
  norm_num [QStrictSeparated, qsupport, sq_29, sq_34, normal_26]

theorem sep_29_35 : QStrictSeparated sq_29 sq_35 normal_26.1 normal_26.2 := by
  norm_num [QStrictSeparated, qsupport, sq_29, sq_35, normal_26]

theorem sep_29_36 : QStrictSeparated sq_29 sq_36 normal_17.1 normal_17.2 := by
  norm_num [QStrictSeparated, qsupport, sq_29, sq_36, normal_17]

theorem row_29 : ∀ j : Fin 37, (29 : Fin 37) < j →
    QStrictSeparated (squares 29) (squares j) (normal 29 j).1 (normal 29 j).2 := by
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
  · exact sep_29_30
  · exact sep_29_31
  · exact sep_29_32
  · exact sep_29_33
  · exact sep_29_34
  · exact sep_29_35
  · exact sep_29_36

end Packing37
