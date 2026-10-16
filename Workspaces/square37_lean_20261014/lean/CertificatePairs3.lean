import CertificateData
import Mathlib.Tactic.FinCases
import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Fintype.Basic

set_option maxRecDepth 10000
set_option maxHeartbeats 0

namespace Packing37
open PackingGeometry

theorem sep_18_19 : QStrictSeparated sq_18 sq_19 normal_22.1 normal_22.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_19, normal_22]

theorem sep_18_20 : QStrictSeparated sq_18 sq_20 normal_23.1 normal_23.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_20, normal_23]

theorem sep_18_21 : QStrictSeparated sq_18 sq_21 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_21, normal_19]

theorem sep_18_22 : QStrictSeparated sq_18 sq_22 normal_22.1 normal_22.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_22, normal_22]

theorem sep_18_23 : QStrictSeparated sq_18 sq_23 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_23, normal_19]

theorem sep_18_24 : QStrictSeparated sq_18 sq_24 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_24, normal_0]

theorem sep_18_25 : QStrictSeparated sq_18 sq_25 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_25, normal_0]

theorem sep_18_26 : QStrictSeparated sq_18 sq_26 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_26, normal_3]

theorem sep_18_27 : QStrictSeparated sq_18 sq_27 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_27, normal_3]

theorem sep_18_28 : QStrictSeparated sq_18 sq_28 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_28, normal_0]

theorem sep_18_29 : QStrictSeparated sq_18 sq_29 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_29, normal_0]

theorem sep_18_30 : QStrictSeparated sq_18 sq_30 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_30, normal_0]

theorem sep_18_31 : QStrictSeparated sq_18 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_31, normal_0]

theorem sep_18_32 : QStrictSeparated sq_18 sq_32 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_32, normal_0]

theorem sep_18_33 : QStrictSeparated sq_18 sq_33 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_33, normal_19]

theorem sep_18_34 : QStrictSeparated sq_18 sq_34 normal_20.1 normal_20.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_34, normal_20]

theorem sep_18_35 : QStrictSeparated sq_18 sq_35 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_35, normal_19]

theorem sep_18_36 : QStrictSeparated sq_18 sq_36 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_18, sq_36, normal_19]

theorem row_18 : ∀ j : Fin 37, (18 : Fin 37) < j →
    QStrictSeparated (squares 18) (squares j) (normal 18 j).1 (normal 18 j).2 := by
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
  · exact sep_18_19
  · exact sep_18_20
  · exact sep_18_21
  · exact sep_18_22
  · exact sep_18_23
  · exact sep_18_24
  · exact sep_18_25
  · exact sep_18_26
  · exact sep_18_27
  · exact sep_18_28
  · exact sep_18_29
  · exact sep_18_30
  · exact sep_18_31
  · exact sep_18_32
  · exact sep_18_33
  · exact sep_18_34
  · exact sep_18_35
  · exact sep_18_36

theorem sep_19_20 : QStrictSeparated sq_19 sq_20 normal_22.1 normal_22.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_20, normal_22]

theorem sep_19_21 : QStrictSeparated sq_19 sq_21 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_21, normal_19]

theorem sep_19_22 : QStrictSeparated sq_19 sq_22 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_22, normal_19]

theorem sep_19_23 : QStrictSeparated sq_19 sq_23 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_23, normal_3]

theorem sep_19_24 : QStrictSeparated sq_19 sq_24 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_24, normal_0]

theorem sep_19_25 : QStrictSeparated sq_19 sq_25 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_25, normal_3]

theorem sep_19_26 : QStrictSeparated sq_19 sq_26 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_26, normal_3]

theorem sep_19_27 : QStrictSeparated sq_19 sq_27 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_27, normal_3]

theorem sep_19_28 : QStrictSeparated sq_19 sq_28 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_28, normal_0]

theorem sep_19_29 : QStrictSeparated sq_19 sq_29 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_29, normal_0]

theorem sep_19_30 : QStrictSeparated sq_19 sq_30 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_30, normal_0]

theorem sep_19_31 : QStrictSeparated sq_19 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_31, normal_0]

theorem sep_19_32 : QStrictSeparated sq_19 sq_32 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_32, normal_0]

theorem sep_19_33 : QStrictSeparated sq_19 sq_33 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_33, normal_0]

theorem sep_19_34 : QStrictSeparated sq_19 sq_34 normal_20.1 normal_20.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_34, normal_20]

theorem sep_19_35 : QStrictSeparated sq_19 sq_35 normal_20.1 normal_20.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_35, normal_20]

theorem sep_19_36 : QStrictSeparated sq_19 sq_36 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_19, sq_36, normal_19]

theorem row_19 : ∀ j : Fin 37, (19 : Fin 37) < j →
    QStrictSeparated (squares 19) (squares j) (normal 19 j).1 (normal 19 j).2 := by
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
  · exact sep_19_20
  · exact sep_19_21
  · exact sep_19_22
  · exact sep_19_23
  · exact sep_19_24
  · exact sep_19_25
  · exact sep_19_26
  · exact sep_19_27
  · exact sep_19_28
  · exact sep_19_29
  · exact sep_19_30
  · exact sep_19_31
  · exact sep_19_32
  · exact sep_19_33
  · exact sep_19_34
  · exact sep_19_35
  · exact sep_19_36

theorem sep_20_21 : QStrictSeparated sq_20 sq_21 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_21, normal_3]

theorem sep_20_22 : QStrictSeparated sq_20 sq_22 normal_24.1 normal_24.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_22, normal_24]

theorem sep_20_23 : QStrictSeparated sq_20 sq_23 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_23, normal_3]

theorem sep_20_24 : QStrictSeparated sq_20 sq_24 normal_25.1 normal_25.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_24, normal_25]

theorem sep_20_25 : QStrictSeparated sq_20 sq_25 normal_25.1 normal_25.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_25, normal_25]

theorem sep_20_26 : QStrictSeparated sq_20 sq_26 normal_25.1 normal_25.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_26, normal_25]

theorem sep_20_27 : QStrictSeparated sq_20 sq_27 normal_25.1 normal_25.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_27, normal_25]

theorem sep_20_28 : QStrictSeparated sq_20 sq_28 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_28, normal_0]

theorem sep_20_29 : QStrictSeparated sq_20 sq_29 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_29, normal_0]

theorem sep_20_30 : QStrictSeparated sq_20 sq_30 normal_25.1 normal_25.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_30, normal_25]

theorem sep_20_31 : QStrictSeparated sq_20 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_31, normal_0]

theorem sep_20_32 : QStrictSeparated sq_20 sq_32 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_32, normal_0]

theorem sep_20_33 : QStrictSeparated sq_20 sq_33 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_33, normal_0]

theorem sep_20_34 : QStrictSeparated sq_20 sq_34 normal_25.1 normal_25.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_34, normal_25]

theorem sep_20_35 : QStrictSeparated sq_20 sq_35 normal_20.1 normal_20.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_35, normal_20]

theorem sep_20_36 : QStrictSeparated sq_20 sq_36 normal_21.1 normal_21.2 := by
  norm_num [QStrictSeparated, qsupport, sq_20, sq_36, normal_21]

theorem row_20 : ∀ j : Fin 37, (20 : Fin 37) < j →
    QStrictSeparated (squares 20) (squares j) (normal 20 j).1 (normal 20 j).2 := by
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
  · exact sep_20_21
  · exact sep_20_22
  · exact sep_20_23
  · exact sep_20_24
  · exact sep_20_25
  · exact sep_20_26
  · exact sep_20_27
  · exact sep_20_28
  · exact sep_20_29
  · exact sep_20_30
  · exact sep_20_31
  · exact sep_20_32
  · exact sep_20_33
  · exact sep_20_34
  · exact sep_20_35
  · exact sep_20_36

theorem sep_21_22 : QStrictSeparated sq_21 sq_22 normal_22.1 normal_22.2 := by
  norm_num [QStrictSeparated, qsupport, sq_21, sq_22, normal_22]

theorem sep_21_23 : QStrictSeparated sq_21 sq_23 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_21, sq_23, normal_3]

theorem sep_21_24 : QStrictSeparated sq_21 sq_24 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_21, sq_24, normal_3]

theorem sep_21_25 : QStrictSeparated sq_21 sq_25 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_21, sq_25, normal_3]

theorem sep_21_26 : QStrictSeparated sq_21 sq_26 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_21, sq_26, normal_3]

theorem sep_21_27 : QStrictSeparated sq_21 sq_27 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_21, sq_27, normal_1]

theorem sep_21_28 : QStrictSeparated sq_21 sq_28 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_21, sq_28, normal_0]

theorem sep_21_29 : QStrictSeparated sq_21 sq_29 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_21, sq_29, normal_3]

theorem sep_21_30 : QStrictSeparated sq_21 sq_30 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_21, sq_30, normal_3]

theorem sep_21_31 : QStrictSeparated sq_21 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_21, sq_31, normal_0]

theorem sep_21_32 : QStrictSeparated sq_21 sq_32 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_21, sq_32, normal_0]

theorem sep_21_33 : QStrictSeparated sq_21 sq_33 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_21, sq_33, normal_0]

theorem sep_21_34 : QStrictSeparated sq_21 sq_34 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_21, sq_34, normal_3]

theorem sep_21_35 : QStrictSeparated sq_21 sq_35 normal_20.1 normal_20.2 := by
  norm_num [QStrictSeparated, qsupport, sq_21, sq_35, normal_20]

theorem sep_21_36 : QStrictSeparated sq_21 sq_36 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_21, sq_36, normal_19]

theorem row_21 : ∀ j : Fin 37, (21 : Fin 37) < j →
    QStrictSeparated (squares 21) (squares j) (normal 21 j).1 (normal 21 j).2 := by
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
  · exact sep_21_22
  · exact sep_21_23
  · exact sep_21_24
  · exact sep_21_25
  · exact sep_21_26
  · exact sep_21_27
  · exact sep_21_28
  · exact sep_21_29
  · exact sep_21_30
  · exact sep_21_31
  · exact sep_21_32
  · exact sep_21_33
  · exact sep_21_34
  · exact sep_21_35
  · exact sep_21_36

theorem sep_22_23 : QStrictSeparated sq_22 sq_23 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_22, sq_23, normal_3]

theorem sep_22_24 : QStrictSeparated sq_22 sq_24 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_22, sq_24, normal_3]

theorem sep_22_25 : QStrictSeparated sq_22 sq_25 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_22, sq_25, normal_3]

theorem sep_22_26 : QStrictSeparated sq_22 sq_26 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_22, sq_26, normal_3]

theorem sep_22_27 : QStrictSeparated sq_22 sq_27 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_22, sq_27, normal_3]

theorem sep_22_28 : QStrictSeparated sq_22 sq_28 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_22, sq_28, normal_3]

theorem sep_22_29 : QStrictSeparated sq_22 sq_29 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_22, sq_29, normal_3]

theorem sep_22_30 : QStrictSeparated sq_22 sq_30 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_22, sq_30, normal_3]

theorem sep_22_31 : QStrictSeparated sq_22 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_22, sq_31, normal_0]

theorem sep_22_32 : QStrictSeparated sq_22 sq_32 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_22, sq_32, normal_0]

theorem sep_22_33 : QStrictSeparated sq_22 sq_33 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_22, sq_33, normal_0]

theorem sep_22_34 : QStrictSeparated sq_22 sq_34 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_22, sq_34, normal_3]

theorem sep_22_35 : QStrictSeparated sq_22 sq_35 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_22, sq_35, normal_3]

theorem sep_22_36 : QStrictSeparated sq_22 sq_36 normal_21.1 normal_21.2 := by
  norm_num [QStrictSeparated, qsupport, sq_22, sq_36, normal_21]

theorem row_22 : ∀ j : Fin 37, (22 : Fin 37) < j →
    QStrictSeparated (squares 22) (squares j) (normal 22 j).1 (normal 22 j).2 := by
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
  · exact sep_22_23
  · exact sep_22_24
  · exact sep_22_25
  · exact sep_22_26
  · exact sep_22_27
  · exact sep_22_28
  · exact sep_22_29
  · exact sep_22_30
  · exact sep_22_31
  · exact sep_22_32
  · exact sep_22_33
  · exact sep_22_34
  · exact sep_22_35
  · exact sep_22_36

theorem sep_23_24 : QStrictSeparated sq_23 sq_24 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_23, sq_24, normal_3]

theorem sep_23_25 : QStrictSeparated sq_23 sq_25 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_23, sq_25, normal_3]

theorem sep_23_26 : QStrictSeparated sq_23 sq_26 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_23, sq_26, normal_3]

theorem sep_23_27 : QStrictSeparated sq_23 sq_27 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_23, sq_27, normal_1]

theorem sep_23_28 : QStrictSeparated sq_23 sq_28 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_23, sq_28, normal_0]

theorem sep_23_29 : QStrictSeparated sq_23 sq_29 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_23, sq_29, normal_0]

theorem sep_23_30 : QStrictSeparated sq_23 sq_30 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_23, sq_30, normal_3]

theorem sep_23_31 : QStrictSeparated sq_23 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_23, sq_31, normal_0]

theorem sep_23_32 : QStrictSeparated sq_23 sq_32 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_23, sq_32, normal_0]

theorem sep_23_33 : QStrictSeparated sq_23 sq_33 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_23, sq_33, normal_19]

theorem sep_23_34 : QStrictSeparated sq_23 sq_34 normal_20.1 normal_20.2 := by
  norm_num [QStrictSeparated, qsupport, sq_23, sq_34, normal_20]

theorem sep_23_35 : QStrictSeparated sq_23 sq_35 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_23, sq_35, normal_19]

theorem sep_23_36 : QStrictSeparated sq_23 sq_36 normal_17.1 normal_17.2 := by
  norm_num [QStrictSeparated, qsupport, sq_23, sq_36, normal_17]

theorem row_23 : ∀ j : Fin 37, (23 : Fin 37) < j →
    QStrictSeparated (squares 23) (squares j) (normal 23 j).1 (normal 23 j).2 := by
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
  · exact sep_23_24
  · exact sep_23_25
  · exact sep_23_26
  · exact sep_23_27
  · exact sep_23_28
  · exact sep_23_29
  · exact sep_23_30
  · exact sep_23_31
  · exact sep_23_32
  · exact sep_23_33
  · exact sep_23_34
  · exact sep_23_35
  · exact sep_23_36

end Packing37
