import CertificateData
import Mathlib.Tactic.FinCases
import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Fintype.Basic

set_option maxRecDepth 10000
set_option maxHeartbeats 0

namespace Packing37
open PackingGeometry

theorem sep_6_7 : QStrictSeparated sq_6 sq_7 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_7, normal_6]

theorem sep_6_8 : QStrictSeparated sq_6 sq_8 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_8, normal_1]

theorem sep_6_9 : QStrictSeparated sq_6 sq_9 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_9, normal_9]

theorem sep_6_10 : QStrictSeparated sq_6 sq_10 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_10, normal_9]

theorem sep_6_11 : QStrictSeparated sq_6 sq_11 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_11, normal_6]

theorem sep_6_12 : QStrictSeparated sq_6 sq_12 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_12, normal_9]

theorem sep_6_13 : QStrictSeparated sq_6 sq_13 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_13, normal_6]

theorem sep_6_14 : QStrictSeparated sq_6 sq_14 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_14, normal_9]

theorem sep_6_15 : QStrictSeparated sq_6 sq_15 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_15, normal_1]

theorem sep_6_16 : QStrictSeparated sq_6 sq_16 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_16, normal_6]

theorem sep_6_17 : QStrictSeparated sq_6 sq_17 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_17, normal_1]

theorem sep_6_18 : QStrictSeparated sq_6 sq_18 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_18, normal_10]

theorem sep_6_19 : QStrictSeparated sq_6 sq_19 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_19, normal_10]

theorem sep_6_20 : QStrictSeparated sq_6 sq_20 normal_7.1 normal_7.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_20, normal_7]

theorem sep_6_21 : QStrictSeparated sq_6 sq_21 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_21, normal_10]

theorem sep_6_22 : QStrictSeparated sq_6 sq_22 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_22, normal_10]

theorem sep_6_23 : QStrictSeparated sq_6 sq_23 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_23, normal_10]

theorem sep_6_24 : QStrictSeparated sq_6 sq_24 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_24, normal_1]

theorem sep_6_25 : QStrictSeparated sq_6 sq_25 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_25, normal_1]

theorem sep_6_26 : QStrictSeparated sq_6 sq_26 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_26, normal_1]

theorem sep_6_27 : QStrictSeparated sq_6 sq_27 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_27, normal_1]

theorem sep_6_28 : QStrictSeparated sq_6 sq_28 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_28, normal_1]

theorem sep_6_29 : QStrictSeparated sq_6 sq_29 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_29, normal_1]

theorem sep_6_30 : QStrictSeparated sq_6 sq_30 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_30, normal_1]

theorem sep_6_31 : QStrictSeparated sq_6 sq_31 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_31, normal_1]

theorem sep_6_32 : QStrictSeparated sq_6 sq_32 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_32, normal_1]

theorem sep_6_33 : QStrictSeparated sq_6 sq_33 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_33, normal_1]

theorem sep_6_34 : QStrictSeparated sq_6 sq_34 normal_11.1 normal_11.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_34, normal_11]

theorem sep_6_35 : QStrictSeparated sq_6 sq_35 normal_11.1 normal_11.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_35, normal_11]

theorem sep_6_36 : QStrictSeparated sq_6 sq_36 normal_12.1 normal_12.2 := by
  norm_num [QStrictSeparated, qsupport, sq_6, sq_36, normal_12]

theorem row_6 : ∀ j : Fin 37, (6 : Fin 37) < j →
    QStrictSeparated (squares 6) (squares j) (normal 6 j).1 (normal 6 j).2 := by
  intro j h
  fin_cases j
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · exact sep_6_7
  · exact sep_6_8
  · exact sep_6_9
  · exact sep_6_10
  · exact sep_6_11
  · exact sep_6_12
  · exact sep_6_13
  · exact sep_6_14
  · exact sep_6_15
  · exact sep_6_16
  · exact sep_6_17
  · exact sep_6_18
  · exact sep_6_19
  · exact sep_6_20
  · exact sep_6_21
  · exact sep_6_22
  · exact sep_6_23
  · exact sep_6_24
  · exact sep_6_25
  · exact sep_6_26
  · exact sep_6_27
  · exact sep_6_28
  · exact sep_6_29
  · exact sep_6_30
  · exact sep_6_31
  · exact sep_6_32
  · exact sep_6_33
  · exact sep_6_34
  · exact sep_6_35
  · exact sep_6_36

theorem sep_7_8 : QStrictSeparated sq_7 sq_8 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_8, normal_1]

theorem sep_7_9 : QStrictSeparated sq_7 sq_9 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_9, normal_1]

theorem sep_7_10 : QStrictSeparated sq_7 sq_10 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_10, normal_9]

theorem sep_7_11 : QStrictSeparated sq_7 sq_11 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_11, normal_6]

theorem sep_7_12 : QStrictSeparated sq_7 sq_12 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_12, normal_9]

theorem sep_7_13 : QStrictSeparated sq_7 sq_13 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_13, normal_9]

theorem sep_7_14 : QStrictSeparated sq_7 sq_14 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_14, normal_1]

theorem sep_7_15 : QStrictSeparated sq_7 sq_15 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_15, normal_1]

theorem sep_7_16 : QStrictSeparated sq_7 sq_16 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_16, normal_1]

theorem sep_7_17 : QStrictSeparated sq_7 sq_17 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_17, normal_1]

theorem sep_7_18 : QStrictSeparated sq_7 sq_18 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_18, normal_10]

theorem sep_7_19 : QStrictSeparated sq_7 sq_19 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_19, normal_10]

theorem sep_7_20 : QStrictSeparated sq_7 sq_20 normal_7.1 normal_7.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_20, normal_7]

theorem sep_7_21 : QStrictSeparated sq_7 sq_21 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_21, normal_10]

theorem sep_7_22 : QStrictSeparated sq_7 sq_22 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_22, normal_10]

theorem sep_7_23 : QStrictSeparated sq_7 sq_23 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_23, normal_10]

theorem sep_7_24 : QStrictSeparated sq_7 sq_24 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_24, normal_1]

theorem sep_7_25 : QStrictSeparated sq_7 sq_25 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_25, normal_1]

theorem sep_7_26 : QStrictSeparated sq_7 sq_26 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_26, normal_1]

theorem sep_7_27 : QStrictSeparated sq_7 sq_27 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_27, normal_1]

theorem sep_7_28 : QStrictSeparated sq_7 sq_28 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_28, normal_1]

theorem sep_7_29 : QStrictSeparated sq_7 sq_29 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_29, normal_1]

theorem sep_7_30 : QStrictSeparated sq_7 sq_30 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_30, normal_1]

theorem sep_7_31 : QStrictSeparated sq_7 sq_31 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_31, normal_1]

theorem sep_7_32 : QStrictSeparated sq_7 sq_32 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_32, normal_1]

theorem sep_7_33 : QStrictSeparated sq_7 sq_33 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_33, normal_1]

theorem sep_7_34 : QStrictSeparated sq_7 sq_34 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_34, normal_1]

theorem sep_7_35 : QStrictSeparated sq_7 sq_35 normal_11.1 normal_11.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_35, normal_11]

theorem sep_7_36 : QStrictSeparated sq_7 sq_36 normal_12.1 normal_12.2 := by
  norm_num [QStrictSeparated, qsupport, sq_7, sq_36, normal_12]

theorem row_7 : ∀ j : Fin 37, (7 : Fin 37) < j →
    QStrictSeparated (squares 7) (squares j) (normal 7 j).1 (normal 7 j).2 := by
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
  · exact sep_7_8
  · exact sep_7_9
  · exact sep_7_10
  · exact sep_7_11
  · exact sep_7_12
  · exact sep_7_13
  · exact sep_7_14
  · exact sep_7_15
  · exact sep_7_16
  · exact sep_7_17
  · exact sep_7_18
  · exact sep_7_19
  · exact sep_7_20
  · exact sep_7_21
  · exact sep_7_22
  · exact sep_7_23
  · exact sep_7_24
  · exact sep_7_25
  · exact sep_7_26
  · exact sep_7_27
  · exact sep_7_28
  · exact sep_7_29
  · exact sep_7_30
  · exact sep_7_31
  · exact sep_7_32
  · exact sep_7_33
  · exact sep_7_34
  · exact sep_7_35
  · exact sep_7_36

theorem sep_8_9 : QStrictSeparated sq_8 sq_9 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_9, normal_9]

theorem sep_8_10 : QStrictSeparated sq_8 sq_10 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_10, normal_6]

theorem sep_8_11 : QStrictSeparated sq_8 sq_11 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_11, normal_6]

theorem sep_8_12 : QStrictSeparated sq_8 sq_12 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_12, normal_6]

theorem sep_8_13 : QStrictSeparated sq_8 sq_13 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_13, normal_6]

theorem sep_8_14 : QStrictSeparated sq_8 sq_14 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_14, normal_9]

theorem sep_8_15 : QStrictSeparated sq_8 sq_15 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_15, normal_6]

theorem sep_8_16 : QStrictSeparated sq_8 sq_16 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_16, normal_6]

theorem sep_8_17 : QStrictSeparated sq_8 sq_17 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_17, normal_1]

theorem sep_8_18 : QStrictSeparated sq_8 sq_18 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_18, normal_10]

theorem sep_8_19 : QStrictSeparated sq_8 sq_19 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_19, normal_10]

theorem sep_8_20 : QStrictSeparated sq_8 sq_20 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_20, normal_6]

theorem sep_8_21 : QStrictSeparated sq_8 sq_21 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_21, normal_10]

theorem sep_8_22 : QStrictSeparated sq_8 sq_22 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_22, normal_6]

theorem sep_8_23 : QStrictSeparated sq_8 sq_23 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_23, normal_10]

theorem sep_8_24 : QStrictSeparated sq_8 sq_24 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_24, normal_1]

theorem sep_8_25 : QStrictSeparated sq_8 sq_25 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_25, normal_1]

theorem sep_8_26 : QStrictSeparated sq_8 sq_26 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_26, normal_1]

theorem sep_8_27 : QStrictSeparated sq_8 sq_27 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_27, normal_1]

theorem sep_8_28 : QStrictSeparated sq_8 sq_28 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_28, normal_1]

theorem sep_8_29 : QStrictSeparated sq_8 sq_29 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_29, normal_1]

theorem sep_8_30 : QStrictSeparated sq_8 sq_30 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_30, normal_1]

theorem sep_8_31 : QStrictSeparated sq_8 sq_31 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_31, normal_1]

theorem sep_8_32 : QStrictSeparated sq_8 sq_32 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_32, normal_1]

theorem sep_8_33 : QStrictSeparated sq_8 sq_33 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_33, normal_1]

theorem sep_8_34 : QStrictSeparated sq_8 sq_34 normal_11.1 normal_11.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_34, normal_11]

theorem sep_8_35 : QStrictSeparated sq_8 sq_35 normal_11.1 normal_11.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_35, normal_11]

theorem sep_8_36 : QStrictSeparated sq_8 sq_36 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_8, sq_36, normal_6]

theorem row_8 : ∀ j : Fin 37, (8 : Fin 37) < j →
    QStrictSeparated (squares 8) (squares j) (normal 8 j).1 (normal 8 j).2 := by
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
  · exact sep_8_9
  · exact sep_8_10
  · exact sep_8_11
  · exact sep_8_12
  · exact sep_8_13
  · exact sep_8_14
  · exact sep_8_15
  · exact sep_8_16
  · exact sep_8_17
  · exact sep_8_18
  · exact sep_8_19
  · exact sep_8_20
  · exact sep_8_21
  · exact sep_8_22
  · exact sep_8_23
  · exact sep_8_24
  · exact sep_8_25
  · exact sep_8_26
  · exact sep_8_27
  · exact sep_8_28
  · exact sep_8_29
  · exact sep_8_30
  · exact sep_8_31
  · exact sep_8_32
  · exact sep_8_33
  · exact sep_8_34
  · exact sep_8_35
  · exact sep_8_36

theorem sep_9_10 : QStrictSeparated sq_9 sq_10 normal_13.1 normal_13.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_10, normal_13]

theorem sep_9_11 : QStrictSeparated sq_9 sq_11 normal_14.1 normal_14.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_11, normal_14]

theorem sep_9_12 : QStrictSeparated sq_9 sq_12 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_12, normal_9]

theorem sep_9_13 : QStrictSeparated sq_9 sq_13 normal_13.1 normal_13.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_13, normal_13]

theorem sep_9_14 : QStrictSeparated sq_9 sq_14 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_14, normal_9]

theorem sep_9_15 : QStrictSeparated sq_9 sq_15 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_15, normal_9]

theorem sep_9_16 : QStrictSeparated sq_9 sq_16 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_16, normal_9]

theorem sep_9_17 : QStrictSeparated sq_9 sq_17 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_17, normal_9]

theorem sep_9_18 : QStrictSeparated sq_9 sq_18 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_18, normal_9]

theorem sep_9_19 : QStrictSeparated sq_9 sq_19 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_19, normal_9]

theorem sep_9_20 : QStrictSeparated sq_9 sq_20 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_20, normal_9]

theorem sep_9_21 : QStrictSeparated sq_9 sq_21 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_21, normal_9]

theorem sep_9_22 : QStrictSeparated sq_9 sq_22 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_22, normal_9]

theorem sep_9_23 : QStrictSeparated sq_9 sq_23 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_23, normal_10]

theorem sep_9_24 : QStrictSeparated sq_9 sq_24 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_24, normal_1]

theorem sep_9_25 : QStrictSeparated sq_9 sq_25 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_25, normal_1]

theorem sep_9_26 : QStrictSeparated sq_9 sq_26 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_26, normal_1]

theorem sep_9_27 : QStrictSeparated sq_9 sq_27 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_27, normal_9]

theorem sep_9_28 : QStrictSeparated sq_9 sq_28 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_28, normal_1]

theorem sep_9_29 : QStrictSeparated sq_9 sq_29 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_29, normal_1]

theorem sep_9_30 : QStrictSeparated sq_9 sq_30 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_30, normal_1]

theorem sep_9_31 : QStrictSeparated sq_9 sq_31 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_31, normal_2]

theorem sep_9_32 : QStrictSeparated sq_9 sq_32 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_32, normal_1]

theorem sep_9_33 : QStrictSeparated sq_9 sq_33 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_33, normal_2]

theorem sep_9_34 : QStrictSeparated sq_9 sq_34 normal_11.1 normal_11.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_34, normal_11]

theorem sep_9_35 : QStrictSeparated sq_9 sq_35 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_35, normal_9]

theorem sep_9_36 : QStrictSeparated sq_9 sq_36 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_9, sq_36, normal_9]

theorem row_9 : ∀ j : Fin 37, (9 : Fin 37) < j →
    QStrictSeparated (squares 9) (squares j) (normal 9 j).1 (normal 9 j).2 := by
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
  · exact sep_9_10
  · exact sep_9_11
  · exact sep_9_12
  · exact sep_9_13
  · exact sep_9_14
  · exact sep_9_15
  · exact sep_9_16
  · exact sep_9_17
  · exact sep_9_18
  · exact sep_9_19
  · exact sep_9_20
  · exact sep_9_21
  · exact sep_9_22
  · exact sep_9_23
  · exact sep_9_24
  · exact sep_9_25
  · exact sep_9_26
  · exact sep_9_27
  · exact sep_9_28
  · exact sep_9_29
  · exact sep_9_30
  · exact sep_9_31
  · exact sep_9_32
  · exact sep_9_33
  · exact sep_9_34
  · exact sep_9_35
  · exact sep_9_36

theorem sep_10_11 : QStrictSeparated sq_10 sq_11 normal_13.1 normal_13.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_11, normal_13]

theorem sep_10_12 : QStrictSeparated sq_10 sq_12 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_12, normal_9]

theorem sep_10_13 : QStrictSeparated sq_10 sq_13 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_13, normal_9]

theorem sep_10_14 : QStrictSeparated sq_10 sq_14 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_14, normal_2]

theorem sep_10_15 : QStrictSeparated sq_10 sq_15 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_15, normal_9]

theorem sep_10_16 : QStrictSeparated sq_10 sq_16 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_16, normal_9]

theorem sep_10_17 : QStrictSeparated sq_10 sq_17 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_17, normal_9]

theorem sep_10_18 : QStrictSeparated sq_10 sq_18 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_18, normal_10]

theorem sep_10_19 : QStrictSeparated sq_10 sq_19 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_19, normal_9]

theorem sep_10_20 : QStrictSeparated sq_10 sq_20 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_20, normal_9]

theorem sep_10_21 : QStrictSeparated sq_10 sq_21 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_21, normal_10]

theorem sep_10_22 : QStrictSeparated sq_10 sq_22 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_22, normal_9]

theorem sep_10_23 : QStrictSeparated sq_10 sq_23 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_23, normal_10]

theorem sep_10_24 : QStrictSeparated sq_10 sq_24 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_24, normal_1]

theorem sep_10_25 : QStrictSeparated sq_10 sq_25 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_25, normal_1]

theorem sep_10_26 : QStrictSeparated sq_10 sq_26 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_26, normal_1]

theorem sep_10_27 : QStrictSeparated sq_10 sq_27 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_27, normal_1]

theorem sep_10_28 : QStrictSeparated sq_10 sq_28 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_28, normal_2]

theorem sep_10_29 : QStrictSeparated sq_10 sq_29 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_29, normal_1]

theorem sep_10_30 : QStrictSeparated sq_10 sq_30 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_30, normal_1]

theorem sep_10_31 : QStrictSeparated sq_10 sq_31 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_31, normal_2]

theorem sep_10_32 : QStrictSeparated sq_10 sq_32 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_32, normal_1]

theorem sep_10_33 : QStrictSeparated sq_10 sq_33 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_33, normal_2]

theorem sep_10_34 : QStrictSeparated sq_10 sq_34 normal_11.1 normal_11.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_34, normal_11]

theorem sep_10_35 : QStrictSeparated sq_10 sq_35 normal_11.1 normal_11.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_35, normal_11]

theorem sep_10_36 : QStrictSeparated sq_10 sq_36 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_10, sq_36, normal_9]

theorem row_10 : ∀ j : Fin 37, (10 : Fin 37) < j →
    QStrictSeparated (squares 10) (squares j) (normal 10 j).1 (normal 10 j).2 := by
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
  · exact sep_10_11
  · exact sep_10_12
  · exact sep_10_13
  · exact sep_10_14
  · exact sep_10_15
  · exact sep_10_16
  · exact sep_10_17
  · exact sep_10_18
  · exact sep_10_19
  · exact sep_10_20
  · exact sep_10_21
  · exact sep_10_22
  · exact sep_10_23
  · exact sep_10_24
  · exact sep_10_25
  · exact sep_10_26
  · exact sep_10_27
  · exact sep_10_28
  · exact sep_10_29
  · exact sep_10_30
  · exact sep_10_31
  · exact sep_10_32
  · exact sep_10_33
  · exact sep_10_34
  · exact sep_10_35
  · exact sep_10_36

theorem sep_11_12 : QStrictSeparated sq_11 sq_12 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_12, normal_2]

theorem sep_11_13 : QStrictSeparated sq_11 sq_13 normal_15.1 normal_15.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_13, normal_15]

theorem sep_11_14 : QStrictSeparated sq_11 sq_14 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_14, normal_2]

theorem sep_11_15 : QStrictSeparated sq_11 sq_15 normal_15.1 normal_15.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_15, normal_15]

theorem sep_11_16 : QStrictSeparated sq_11 sq_16 normal_15.1 normal_15.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_16, normal_15]

theorem sep_11_17 : QStrictSeparated sq_11 sq_17 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_17, normal_1]

theorem sep_11_18 : QStrictSeparated sq_11 sq_18 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_18, normal_10]

theorem sep_11_19 : QStrictSeparated sq_11 sq_19 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_19, normal_10]

theorem sep_11_20 : QStrictSeparated sq_11 sq_20 normal_15.1 normal_15.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_20, normal_15]

theorem sep_11_21 : QStrictSeparated sq_11 sq_21 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_21, normal_10]

theorem sep_11_22 : QStrictSeparated sq_11 sq_22 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_22, normal_10]

theorem sep_11_23 : QStrictSeparated sq_11 sq_23 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_23, normal_10]

theorem sep_11_24 : QStrictSeparated sq_11 sq_24 normal_16.1 normal_16.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_24, normal_16]

theorem sep_11_25 : QStrictSeparated sq_11 sq_25 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_25, normal_1]

theorem sep_11_26 : QStrictSeparated sq_11 sq_26 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_26, normal_1]

theorem sep_11_27 : QStrictSeparated sq_11 sq_27 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_27, normal_1]

theorem sep_11_28 : QStrictSeparated sq_11 sq_28 normal_16.1 normal_16.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_28, normal_16]

theorem sep_11_29 : QStrictSeparated sq_11 sq_29 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_29, normal_1]

theorem sep_11_30 : QStrictSeparated sq_11 sq_30 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_30, normal_1]

theorem sep_11_31 : QStrictSeparated sq_11 sq_31 normal_16.1 normal_16.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_31, normal_16]

theorem sep_11_32 : QStrictSeparated sq_11 sq_32 normal_16.1 normal_16.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_32, normal_16]

theorem sep_11_33 : QStrictSeparated sq_11 sq_33 normal_16.1 normal_16.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_33, normal_16]

theorem sep_11_34 : QStrictSeparated sq_11 sq_34 normal_16.1 normal_16.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_34, normal_16]

theorem sep_11_35 : QStrictSeparated sq_11 sq_35 normal_11.1 normal_11.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_35, normal_11]

theorem sep_11_36 : QStrictSeparated sq_11 sq_36 normal_12.1 normal_12.2 := by
  norm_num [QStrictSeparated, qsupport, sq_11, sq_36, normal_12]

theorem row_11 : ∀ j : Fin 37, (11 : Fin 37) < j →
    QStrictSeparated (squares 11) (squares j) (normal 11 j).1 (normal 11 j).2 := by
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
  · exact sep_11_12
  · exact sep_11_13
  · exact sep_11_14
  · exact sep_11_15
  · exact sep_11_16
  · exact sep_11_17
  · exact sep_11_18
  · exact sep_11_19
  · exact sep_11_20
  · exact sep_11_21
  · exact sep_11_22
  · exact sep_11_23
  · exact sep_11_24
  · exact sep_11_25
  · exact sep_11_26
  · exact sep_11_27
  · exact sep_11_28
  · exact sep_11_29
  · exact sep_11_30
  · exact sep_11_31
  · exact sep_11_32
  · exact sep_11_33
  · exact sep_11_34
  · exact sep_11_35
  · exact sep_11_36

end Packing37
