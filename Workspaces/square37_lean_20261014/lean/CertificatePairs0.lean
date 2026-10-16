import CertificateData
import Mathlib.Tactic.FinCases
import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Fintype.Basic

set_option maxRecDepth 10000
set_option maxHeartbeats 0

namespace Packing37
open PackingGeometry

theorem sep_0_1 : QStrictSeparated sq_0 sq_1 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_1, normal_0]

theorem sep_0_2 : QStrictSeparated sq_0 sq_2 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_2, normal_0]

theorem sep_0_3 : QStrictSeparated sq_0 sq_3 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_3, normal_1]

theorem sep_0_4 : QStrictSeparated sq_0 sq_4 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_4, normal_0]

theorem sep_0_5 : QStrictSeparated sq_0 sq_5 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_5, normal_1]

theorem sep_0_6 : QStrictSeparated sq_0 sq_6 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_6, normal_0]

theorem sep_0_7 : QStrictSeparated sq_0 sq_7 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_7, normal_0]

theorem sep_0_8 : QStrictSeparated sq_0 sq_8 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_8, normal_0]

theorem sep_0_9 : QStrictSeparated sq_0 sq_9 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_9, normal_0]

theorem sep_0_10 : QStrictSeparated sq_0 sq_10 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_10, normal_0]

theorem sep_0_11 : QStrictSeparated sq_0 sq_11 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_11, normal_0]

theorem sep_0_12 : QStrictSeparated sq_0 sq_12 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_12, normal_2]

theorem sep_0_13 : QStrictSeparated sq_0 sq_13 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_13, normal_0]

theorem sep_0_14 : QStrictSeparated sq_0 sq_14 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_14, normal_2]

theorem sep_0_15 : QStrictSeparated sq_0 sq_15 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_15, normal_1]

theorem sep_0_16 : QStrictSeparated sq_0 sq_16 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_16, normal_1]

theorem sep_0_17 : QStrictSeparated sq_0 sq_17 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_17, normal_1]

theorem sep_0_18 : QStrictSeparated sq_0 sq_18 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_18, normal_1]

theorem sep_0_19 : QStrictSeparated sq_0 sq_19 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_19, normal_1]

theorem sep_0_20 : QStrictSeparated sq_0 sq_20 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_20, normal_1]

theorem sep_0_21 : QStrictSeparated sq_0 sq_21 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_21, normal_3]

theorem sep_0_22 : QStrictSeparated sq_0 sq_22 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_22, normal_1]

theorem sep_0_23 : QStrictSeparated sq_0 sq_23 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_23, normal_3]

theorem sep_0_24 : QStrictSeparated sq_0 sq_24 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_24, normal_1]

theorem sep_0_25 : QStrictSeparated sq_0 sq_25 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_25, normal_1]

theorem sep_0_26 : QStrictSeparated sq_0 sq_26 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_26, normal_1]

theorem sep_0_27 : QStrictSeparated sq_0 sq_27 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_27, normal_1]

theorem sep_0_28 : QStrictSeparated sq_0 sq_28 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_28, normal_0]

theorem sep_0_29 : QStrictSeparated sq_0 sq_29 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_29, normal_1]

theorem sep_0_30 : QStrictSeparated sq_0 sq_30 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_30, normal_1]

theorem sep_0_31 : QStrictSeparated sq_0 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_31, normal_0]

theorem sep_0_32 : QStrictSeparated sq_0 sq_32 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_32, normal_0]

theorem sep_0_33 : QStrictSeparated sq_0 sq_33 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_33, normal_0]

theorem sep_0_34 : QStrictSeparated sq_0 sq_34 normal_4.1 normal_4.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_34, normal_4]

theorem sep_0_35 : QStrictSeparated sq_0 sq_35 normal_4.1 normal_4.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_35, normal_4]

theorem sep_0_36 : QStrictSeparated sq_0 sq_36 normal_5.1 normal_5.2 := by
  norm_num [QStrictSeparated, qsupport, sq_0, sq_36, normal_5]

theorem row_0 : ∀ j : Fin 37, (0 : Fin 37) < j →
    QStrictSeparated (squares 0) (squares j) (normal 0 j).1 (normal 0 j).2 := by
  intro j h
  fin_cases j
  · norm_num at h
  · exact sep_0_1
  · exact sep_0_2
  · exact sep_0_3
  · exact sep_0_4
  · exact sep_0_5
  · exact sep_0_6
  · exact sep_0_7
  · exact sep_0_8
  · exact sep_0_9
  · exact sep_0_10
  · exact sep_0_11
  · exact sep_0_12
  · exact sep_0_13
  · exact sep_0_14
  · exact sep_0_15
  · exact sep_0_16
  · exact sep_0_17
  · exact sep_0_18
  · exact sep_0_19
  · exact sep_0_20
  · exact sep_0_21
  · exact sep_0_22
  · exact sep_0_23
  · exact sep_0_24
  · exact sep_0_25
  · exact sep_0_26
  · exact sep_0_27
  · exact sep_0_28
  · exact sep_0_29
  · exact sep_0_30
  · exact sep_0_31
  · exact sep_0_32
  · exact sep_0_33
  · exact sep_0_34
  · exact sep_0_35
  · exact sep_0_36

theorem sep_1_2 : QStrictSeparated sq_1 sq_2 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_2, normal_0]

theorem sep_1_3 : QStrictSeparated sq_1 sq_3 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_3, normal_1]

theorem sep_1_4 : QStrictSeparated sq_1 sq_4 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_4, normal_1]

theorem sep_1_5 : QStrictSeparated sq_1 sq_5 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_5, normal_1]

theorem sep_1_6 : QStrictSeparated sq_1 sq_6 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_6, normal_0]

theorem sep_1_7 : QStrictSeparated sq_1 sq_7 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_7, normal_0]

theorem sep_1_8 : QStrictSeparated sq_1 sq_8 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_8, normal_0]

theorem sep_1_9 : QStrictSeparated sq_1 sq_9 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_9, normal_2]

theorem sep_1_10 : QStrictSeparated sq_1 sq_10 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_10, normal_0]

theorem sep_1_11 : QStrictSeparated sq_1 sq_11 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_11, normal_0]

theorem sep_1_12 : QStrictSeparated sq_1 sq_12 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_12, normal_2]

theorem sep_1_13 : QStrictSeparated sq_1 sq_13 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_13, normal_2]

theorem sep_1_14 : QStrictSeparated sq_1 sq_14 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_14, normal_2]

theorem sep_1_15 : QStrictSeparated sq_1 sq_15 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_15, normal_1]

theorem sep_1_16 : QStrictSeparated sq_1 sq_16 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_16, normal_1]

theorem sep_1_17 : QStrictSeparated sq_1 sq_17 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_17, normal_1]

theorem sep_1_18 : QStrictSeparated sq_1 sq_18 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_18, normal_1]

theorem sep_1_19 : QStrictSeparated sq_1 sq_19 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_19, normal_1]

theorem sep_1_20 : QStrictSeparated sq_1 sq_20 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_20, normal_1]

theorem sep_1_21 : QStrictSeparated sq_1 sq_21 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_21, normal_1]

theorem sep_1_22 : QStrictSeparated sq_1 sq_22 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_22, normal_1]

theorem sep_1_23 : QStrictSeparated sq_1 sq_23 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_23, normal_1]

theorem sep_1_24 : QStrictSeparated sq_1 sq_24 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_24, normal_1]

theorem sep_1_25 : QStrictSeparated sq_1 sq_25 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_25, normal_1]

theorem sep_1_26 : QStrictSeparated sq_1 sq_26 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_26, normal_1]

theorem sep_1_27 : QStrictSeparated sq_1 sq_27 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_27, normal_1]

theorem sep_1_28 : QStrictSeparated sq_1 sq_28 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_28, normal_1]

theorem sep_1_29 : QStrictSeparated sq_1 sq_29 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_29, normal_1]

theorem sep_1_30 : QStrictSeparated sq_1 sq_30 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_30, normal_1]

theorem sep_1_31 : QStrictSeparated sq_1 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_31, normal_0]

theorem sep_1_32 : QStrictSeparated sq_1 sq_32 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_32, normal_1]

theorem sep_1_33 : QStrictSeparated sq_1 sq_33 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_33, normal_0]

theorem sep_1_34 : QStrictSeparated sq_1 sq_34 normal_4.1 normal_4.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_34, normal_4]

theorem sep_1_35 : QStrictSeparated sq_1 sq_35 normal_4.1 normal_4.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_35, normal_4]

theorem sep_1_36 : QStrictSeparated sq_1 sq_36 normal_5.1 normal_5.2 := by
  norm_num [QStrictSeparated, qsupport, sq_1, sq_36, normal_5]

theorem row_1 : ∀ j : Fin 37, (1 : Fin 37) < j →
    QStrictSeparated (squares 1) (squares j) (normal 1 j).1 (normal 1 j).2 := by
  intro j h
  fin_cases j
  · norm_num at h
  · norm_num at h
  · exact sep_1_2
  · exact sep_1_3
  · exact sep_1_4
  · exact sep_1_5
  · exact sep_1_6
  · exact sep_1_7
  · exact sep_1_8
  · exact sep_1_9
  · exact sep_1_10
  · exact sep_1_11
  · exact sep_1_12
  · exact sep_1_13
  · exact sep_1_14
  · exact sep_1_15
  · exact sep_1_16
  · exact sep_1_17
  · exact sep_1_18
  · exact sep_1_19
  · exact sep_1_20
  · exact sep_1_21
  · exact sep_1_22
  · exact sep_1_23
  · exact sep_1_24
  · exact sep_1_25
  · exact sep_1_26
  · exact sep_1_27
  · exact sep_1_28
  · exact sep_1_29
  · exact sep_1_30
  · exact sep_1_31
  · exact sep_1_32
  · exact sep_1_33
  · exact sep_1_34
  · exact sep_1_35
  · exact sep_1_36

theorem sep_2_3 : QStrictSeparated sq_2 sq_3 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_3, normal_6]

theorem sep_2_4 : QStrictSeparated sq_2 sq_4 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_4, normal_1]

theorem sep_2_5 : QStrictSeparated sq_2 sq_5 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_5, normal_1]

theorem sep_2_6 : QStrictSeparated sq_2 sq_6 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_6, normal_0]

theorem sep_2_7 : QStrictSeparated sq_2 sq_7 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_7, normal_0]

theorem sep_2_8 : QStrictSeparated sq_2 sq_8 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_8, normal_0]

theorem sep_2_9 : QStrictSeparated sq_2 sq_9 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_9, normal_2]

theorem sep_2_10 : QStrictSeparated sq_2 sq_10 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_10, normal_2]

theorem sep_2_11 : QStrictSeparated sq_2 sq_11 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_11, normal_0]

theorem sep_2_12 : QStrictSeparated sq_2 sq_12 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_12, normal_2]

theorem sep_2_13 : QStrictSeparated sq_2 sq_13 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_13, normal_2]

theorem sep_2_14 : QStrictSeparated sq_2 sq_14 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_14, normal_2]

theorem sep_2_15 : QStrictSeparated sq_2 sq_15 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_15, normal_1]

theorem sep_2_16 : QStrictSeparated sq_2 sq_16 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_16, normal_1]

theorem sep_2_17 : QStrictSeparated sq_2 sq_17 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_17, normal_1]

theorem sep_2_18 : QStrictSeparated sq_2 sq_18 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_18, normal_1]

theorem sep_2_19 : QStrictSeparated sq_2 sq_19 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_19, normal_1]

theorem sep_2_20 : QStrictSeparated sq_2 sq_20 normal_7.1 normal_7.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_20, normal_7]

theorem sep_2_21 : QStrictSeparated sq_2 sq_21 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_21, normal_1]

theorem sep_2_22 : QStrictSeparated sq_2 sq_22 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_22, normal_1]

theorem sep_2_23 : QStrictSeparated sq_2 sq_23 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_23, normal_1]

theorem sep_2_24 : QStrictSeparated sq_2 sq_24 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_24, normal_1]

theorem sep_2_25 : QStrictSeparated sq_2 sq_25 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_25, normal_1]

theorem sep_2_26 : QStrictSeparated sq_2 sq_26 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_26, normal_1]

theorem sep_2_27 : QStrictSeparated sq_2 sq_27 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_27, normal_1]

theorem sep_2_28 : QStrictSeparated sq_2 sq_28 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_28, normal_1]

theorem sep_2_29 : QStrictSeparated sq_2 sq_29 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_29, normal_1]

theorem sep_2_30 : QStrictSeparated sq_2 sq_30 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_30, normal_1]

theorem sep_2_31 : QStrictSeparated sq_2 sq_31 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_31, normal_1]

theorem sep_2_32 : QStrictSeparated sq_2 sq_32 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_32, normal_1]

theorem sep_2_33 : QStrictSeparated sq_2 sq_33 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_33, normal_0]

theorem sep_2_34 : QStrictSeparated sq_2 sq_34 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_34, normal_1]

theorem sep_2_35 : QStrictSeparated sq_2 sq_35 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_35, normal_1]

theorem sep_2_36 : QStrictSeparated sq_2 sq_36 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_2, sq_36, normal_1]

theorem row_2 : ∀ j : Fin 37, (2 : Fin 37) < j →
    QStrictSeparated (squares 2) (squares j) (normal 2 j).1 (normal 2 j).2 := by
  intro j h
  fin_cases j
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · exact sep_2_3
  · exact sep_2_4
  · exact sep_2_5
  · exact sep_2_6
  · exact sep_2_7
  · exact sep_2_8
  · exact sep_2_9
  · exact sep_2_10
  · exact sep_2_11
  · exact sep_2_12
  · exact sep_2_13
  · exact sep_2_14
  · exact sep_2_15
  · exact sep_2_16
  · exact sep_2_17
  · exact sep_2_18
  · exact sep_2_19
  · exact sep_2_20
  · exact sep_2_21
  · exact sep_2_22
  · exact sep_2_23
  · exact sep_2_24
  · exact sep_2_25
  · exact sep_2_26
  · exact sep_2_27
  · exact sep_2_28
  · exact sep_2_29
  · exact sep_2_30
  · exact sep_2_31
  · exact sep_2_32
  · exact sep_2_33
  · exact sep_2_34
  · exact sep_2_35
  · exact sep_2_36

theorem sep_3_4 : QStrictSeparated sq_3 sq_4 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_4, normal_0]

theorem sep_3_5 : QStrictSeparated sq_3 sq_5 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_5, normal_1]

theorem sep_3_6 : QStrictSeparated sq_3 sq_6 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_6, normal_0]

theorem sep_3_7 : QStrictSeparated sq_3 sq_7 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_7, normal_0]

theorem sep_3_8 : QStrictSeparated sq_3 sq_8 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_8, normal_0]

theorem sep_3_9 : QStrictSeparated sq_3 sq_9 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_9, normal_0]

theorem sep_3_10 : QStrictSeparated sq_3 sq_10 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_10, normal_0]

theorem sep_3_11 : QStrictSeparated sq_3 sq_11 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_11, normal_0]

theorem sep_3_12 : QStrictSeparated sq_3 sq_12 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_12, normal_0]

theorem sep_3_13 : QStrictSeparated sq_3 sq_13 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_13, normal_0]

theorem sep_3_14 : QStrictSeparated sq_3 sq_14 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_14, normal_0]

theorem sep_3_15 : QStrictSeparated sq_3 sq_15 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_15, normal_1]

theorem sep_3_16 : QStrictSeparated sq_3 sq_16 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_16, normal_1]

theorem sep_3_17 : QStrictSeparated sq_3 sq_17 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_17, normal_1]

theorem sep_3_18 : QStrictSeparated sq_3 sq_18 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_18, normal_3]

theorem sep_3_19 : QStrictSeparated sq_3 sq_19 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_19, normal_1]

theorem sep_3_20 : QStrictSeparated sq_3 sq_20 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_20, normal_1]

theorem sep_3_21 : QStrictSeparated sq_3 sq_21 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_21, normal_3]

theorem sep_3_22 : QStrictSeparated sq_3 sq_22 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_22, normal_3]

theorem sep_3_23 : QStrictSeparated sq_3 sq_23 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_23, normal_3]

theorem sep_3_24 : QStrictSeparated sq_3 sq_24 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_24, normal_0]

theorem sep_3_25 : QStrictSeparated sq_3 sq_25 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_25, normal_1]

theorem sep_3_26 : QStrictSeparated sq_3 sq_26 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_26, normal_1]

theorem sep_3_27 : QStrictSeparated sq_3 sq_27 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_27, normal_1]

theorem sep_3_28 : QStrictSeparated sq_3 sq_28 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_28, normal_0]

theorem sep_3_29 : QStrictSeparated sq_3 sq_29 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_29, normal_0]

theorem sep_3_30 : QStrictSeparated sq_3 sq_30 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_30, normal_1]

theorem sep_3_31 : QStrictSeparated sq_3 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_31, normal_0]

theorem sep_3_32 : QStrictSeparated sq_3 sq_32 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_32, normal_0]

theorem sep_3_33 : QStrictSeparated sq_3 sq_33 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_33, normal_0]

theorem sep_3_34 : QStrictSeparated sq_3 sq_34 normal_4.1 normal_4.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_34, normal_4]

theorem sep_3_35 : QStrictSeparated sq_3 sq_35 normal_4.1 normal_4.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_35, normal_4]

theorem sep_3_36 : QStrictSeparated sq_3 sq_36 normal_5.1 normal_5.2 := by
  norm_num [QStrictSeparated, qsupport, sq_3, sq_36, normal_5]

theorem row_3 : ∀ j : Fin 37, (3 : Fin 37) < j →
    QStrictSeparated (squares 3) (squares j) (normal 3 j).1 (normal 3 j).2 := by
  intro j h
  fin_cases j
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · exact sep_3_4
  · exact sep_3_5
  · exact sep_3_6
  · exact sep_3_7
  · exact sep_3_8
  · exact sep_3_9
  · exact sep_3_10
  · exact sep_3_11
  · exact sep_3_12
  · exact sep_3_13
  · exact sep_3_14
  · exact sep_3_15
  · exact sep_3_16
  · exact sep_3_17
  · exact sep_3_18
  · exact sep_3_19
  · exact sep_3_20
  · exact sep_3_21
  · exact sep_3_22
  · exact sep_3_23
  · exact sep_3_24
  · exact sep_3_25
  · exact sep_3_26
  · exact sep_3_27
  · exact sep_3_28
  · exact sep_3_29
  · exact sep_3_30
  · exact sep_3_31
  · exact sep_3_32
  · exact sep_3_33
  · exact sep_3_34
  · exact sep_3_35
  · exact sep_3_36

theorem sep_4_5 : QStrictSeparated sq_4 sq_5 normal_6.1 normal_6.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_5, normal_6]

theorem sep_4_6 : QStrictSeparated sq_4 sq_6 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_6, normal_0]

theorem sep_4_7 : QStrictSeparated sq_4 sq_7 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_7, normal_0]

theorem sep_4_8 : QStrictSeparated sq_4 sq_8 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_8, normal_0]

theorem sep_4_9 : QStrictSeparated sq_4 sq_9 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_9, normal_0]

theorem sep_4_10 : QStrictSeparated sq_4 sq_10 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_10, normal_0]

theorem sep_4_11 : QStrictSeparated sq_4 sq_11 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_11, normal_0]

theorem sep_4_12 : QStrictSeparated sq_4 sq_12 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_12, normal_0]

theorem sep_4_13 : QStrictSeparated sq_4 sq_13 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_13, normal_0]

theorem sep_4_14 : QStrictSeparated sq_4 sq_14 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_14, normal_2]

theorem sep_4_15 : QStrictSeparated sq_4 sq_15 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_15, normal_1]

theorem sep_4_16 : QStrictSeparated sq_4 sq_16 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_16, normal_1]

theorem sep_4_17 : QStrictSeparated sq_4 sq_17 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_17, normal_1]

theorem sep_4_18 : QStrictSeparated sq_4 sq_18 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_18, normal_1]

theorem sep_4_19 : QStrictSeparated sq_4 sq_19 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_19, normal_1]

theorem sep_4_20 : QStrictSeparated sq_4 sq_20 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_20, normal_1]

theorem sep_4_21 : QStrictSeparated sq_4 sq_21 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_21, normal_1]

theorem sep_4_22 : QStrictSeparated sq_4 sq_22 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_22, normal_1]

theorem sep_4_23 : QStrictSeparated sq_4 sq_23 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_23, normal_3]

theorem sep_4_24 : QStrictSeparated sq_4 sq_24 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_24, normal_1]

theorem sep_4_25 : QStrictSeparated sq_4 sq_25 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_25, normal_1]

theorem sep_4_26 : QStrictSeparated sq_4 sq_26 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_26, normal_1]

theorem sep_4_27 : QStrictSeparated sq_4 sq_27 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_27, normal_1]

theorem sep_4_28 : QStrictSeparated sq_4 sq_28 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_28, normal_0]

theorem sep_4_29 : QStrictSeparated sq_4 sq_29 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_29, normal_1]

theorem sep_4_30 : QStrictSeparated sq_4 sq_30 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_30, normal_1]

theorem sep_4_31 : QStrictSeparated sq_4 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_31, normal_0]

theorem sep_4_32 : QStrictSeparated sq_4 sq_32 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_32, normal_0]

theorem sep_4_33 : QStrictSeparated sq_4 sq_33 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_33, normal_0]

theorem sep_4_34 : QStrictSeparated sq_4 sq_34 normal_4.1 normal_4.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_34, normal_4]

theorem sep_4_35 : QStrictSeparated sq_4 sq_35 normal_4.1 normal_4.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_35, normal_4]

theorem sep_4_36 : QStrictSeparated sq_4 sq_36 normal_5.1 normal_5.2 := by
  norm_num [QStrictSeparated, qsupport, sq_4, sq_36, normal_5]

theorem row_4 : ∀ j : Fin 37, (4 : Fin 37) < j →
    QStrictSeparated (squares 4) (squares j) (normal 4 j).1 (normal 4 j).2 := by
  intro j h
  fin_cases j
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · exact sep_4_5
  · exact sep_4_6
  · exact sep_4_7
  · exact sep_4_8
  · exact sep_4_9
  · exact sep_4_10
  · exact sep_4_11
  · exact sep_4_12
  · exact sep_4_13
  · exact sep_4_14
  · exact sep_4_15
  · exact sep_4_16
  · exact sep_4_17
  · exact sep_4_18
  · exact sep_4_19
  · exact sep_4_20
  · exact sep_4_21
  · exact sep_4_22
  · exact sep_4_23
  · exact sep_4_24
  · exact sep_4_25
  · exact sep_4_26
  · exact sep_4_27
  · exact sep_4_28
  · exact sep_4_29
  · exact sep_4_30
  · exact sep_4_31
  · exact sep_4_32
  · exact sep_4_33
  · exact sep_4_34
  · exact sep_4_35
  · exact sep_4_36

theorem sep_5_6 : QStrictSeparated sq_5 sq_6 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_6, normal_0]

theorem sep_5_7 : QStrictSeparated sq_5 sq_7 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_7, normal_0]

theorem sep_5_8 : QStrictSeparated sq_5 sq_8 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_8, normal_0]

theorem sep_5_9 : QStrictSeparated sq_5 sq_9 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_9, normal_0]

theorem sep_5_10 : QStrictSeparated sq_5 sq_10 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_10, normal_0]

theorem sep_5_11 : QStrictSeparated sq_5 sq_11 normal_8.1 normal_8.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_11, normal_8]

theorem sep_5_12 : QStrictSeparated sq_5 sq_12 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_12, normal_0]

theorem sep_5_13 : QStrictSeparated sq_5 sq_13 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_13, normal_0]

theorem sep_5_14 : QStrictSeparated sq_5 sq_14 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_14, normal_0]

theorem sep_5_15 : QStrictSeparated sq_5 sq_15 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_15, normal_1]

theorem sep_5_16 : QStrictSeparated sq_5 sq_16 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_16, normal_1]

theorem sep_5_17 : QStrictSeparated sq_5 sq_17 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_17, normal_1]

theorem sep_5_18 : QStrictSeparated sq_5 sq_18 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_18, normal_3]

theorem sep_5_19 : QStrictSeparated sq_5 sq_19 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_19, normal_3]

theorem sep_5_20 : QStrictSeparated sq_5 sq_20 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_20, normal_1]

theorem sep_5_21 : QStrictSeparated sq_5 sq_21 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_21, normal_3]

theorem sep_5_22 : QStrictSeparated sq_5 sq_22 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_22, normal_3]

theorem sep_5_23 : QStrictSeparated sq_5 sq_23 normal_3.1 normal_3.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_23, normal_3]

theorem sep_5_24 : QStrictSeparated sq_5 sq_24 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_24, normal_0]

theorem sep_5_25 : QStrictSeparated sq_5 sq_25 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_25, normal_0]

theorem sep_5_26 : QStrictSeparated sq_5 sq_26 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_26, normal_1]

theorem sep_5_27 : QStrictSeparated sq_5 sq_27 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_27, normal_1]

theorem sep_5_28 : QStrictSeparated sq_5 sq_28 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_28, normal_0]

theorem sep_5_29 : QStrictSeparated sq_5 sq_29 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_29, normal_0]

theorem sep_5_30 : QStrictSeparated sq_5 sq_30 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_30, normal_0]

theorem sep_5_31 : QStrictSeparated sq_5 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_31, normal_0]

theorem sep_5_32 : QStrictSeparated sq_5 sq_32 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_32, normal_0]

theorem sep_5_33 : QStrictSeparated sq_5 sq_33 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_33, normal_0]

theorem sep_5_34 : QStrictSeparated sq_5 sq_34 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_34, normal_0]

theorem sep_5_35 : QStrictSeparated sq_5 sq_35 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_35, normal_0]

theorem sep_5_36 : QStrictSeparated sq_5 sq_36 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_5, sq_36, normal_0]

theorem row_5 : ∀ j : Fin 37, (5 : Fin 37) < j →
    QStrictSeparated (squares 5) (squares j) (normal 5 j).1 (normal 5 j).2 := by
  intro j h
  fin_cases j
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · exact sep_5_6
  · exact sep_5_7
  · exact sep_5_8
  · exact sep_5_9
  · exact sep_5_10
  · exact sep_5_11
  · exact sep_5_12
  · exact sep_5_13
  · exact sep_5_14
  · exact sep_5_15
  · exact sep_5_16
  · exact sep_5_17
  · exact sep_5_18
  · exact sep_5_19
  · exact sep_5_20
  · exact sep_5_21
  · exact sep_5_22
  · exact sep_5_23
  · exact sep_5_24
  · exact sep_5_25
  · exact sep_5_26
  · exact sep_5_27
  · exact sep_5_28
  · exact sep_5_29
  · exact sep_5_30
  · exact sep_5_31
  · exact sep_5_32
  · exact sep_5_33
  · exact sep_5_34
  · exact sep_5_35
  · exact sep_5_36

end Packing37
