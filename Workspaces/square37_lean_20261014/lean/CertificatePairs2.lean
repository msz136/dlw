import CertificateData
import Mathlib.Tactic.FinCases
import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Fintype.Basic

set_option maxRecDepth 10000
set_option maxHeartbeats 0

namespace Packing37
open PackingGeometry

theorem sep_12_13 : QStrictSeparated sq_12 sq_13 normal_13.1 normal_13.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_13, normal_13]

theorem sep_12_14 : QStrictSeparated sq_12 sq_14 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_14, normal_2]

theorem sep_12_15 : QStrictSeparated sq_12 sq_15 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_15, normal_9]

theorem sep_12_16 : QStrictSeparated sq_12 sq_16 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_16, normal_9]

theorem sep_12_17 : QStrictSeparated sq_12 sq_17 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_17, normal_9]

theorem sep_12_18 : QStrictSeparated sq_12 sq_18 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_18, normal_10]

theorem sep_12_19 : QStrictSeparated sq_12 sq_19 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_19, normal_9]

theorem sep_12_20 : QStrictSeparated sq_12 sq_20 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_20, normal_9]

theorem sep_12_21 : QStrictSeparated sq_12 sq_21 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_21, normal_9]

theorem sep_12_22 : QStrictSeparated sq_12 sq_22 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_22, normal_9]

theorem sep_12_23 : QStrictSeparated sq_12 sq_23 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_23, normal_10]

theorem sep_12_24 : QStrictSeparated sq_12 sq_24 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_24, normal_2]

theorem sep_12_25 : QStrictSeparated sq_12 sq_25 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_25, normal_1]

theorem sep_12_26 : QStrictSeparated sq_12 sq_26 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_26, normal_1]

theorem sep_12_27 : QStrictSeparated sq_12 sq_27 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_27, normal_1]

theorem sep_12_28 : QStrictSeparated sq_12 sq_28 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_28, normal_2]

theorem sep_12_29 : QStrictSeparated sq_12 sq_29 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_29, normal_2]

theorem sep_12_30 : QStrictSeparated sq_12 sq_30 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_30, normal_1]

theorem sep_12_31 : QStrictSeparated sq_12 sq_31 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_31, normal_2]

theorem sep_12_32 : QStrictSeparated sq_12 sq_32 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_32, normal_2]

theorem sep_12_33 : QStrictSeparated sq_12 sq_33 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_33, normal_0]

theorem sep_12_34 : QStrictSeparated sq_12 sq_34 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_34, normal_2]

theorem sep_12_35 : QStrictSeparated sq_12 sq_35 normal_11.1 normal_11.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_35, normal_11]

theorem sep_12_36 : QStrictSeparated sq_12 sq_36 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_12, sq_36, normal_9]

theorem row_12 : ∀ j : Fin 37, (12 : Fin 37) < j →
    QStrictSeparated (squares 12) (squares j) (normal 12 j).1 (normal 12 j).2 := by
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
  · exact sep_12_13
  · exact sep_12_14
  · exact sep_12_15
  · exact sep_12_16
  · exact sep_12_17
  · exact sep_12_18
  · exact sep_12_19
  · exact sep_12_20
  · exact sep_12_21
  · exact sep_12_22
  · exact sep_12_23
  · exact sep_12_24
  · exact sep_12_25
  · exact sep_12_26
  · exact sep_12_27
  · exact sep_12_28
  · exact sep_12_29
  · exact sep_12_30
  · exact sep_12_31
  · exact sep_12_32
  · exact sep_12_33
  · exact sep_12_34
  · exact sep_12_35
  · exact sep_12_36

theorem sep_13_14 : QStrictSeparated sq_13 sq_14 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_14, normal_2]

theorem sep_13_15 : QStrictSeparated sq_13 sq_15 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_15, normal_9]

theorem sep_13_16 : QStrictSeparated sq_13 sq_16 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_16, normal_9]

theorem sep_13_17 : QStrictSeparated sq_13 sq_17 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_17, normal_1]

theorem sep_13_18 : QStrictSeparated sq_13 sq_18 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_18, normal_10]

theorem sep_13_19 : QStrictSeparated sq_13 sq_19 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_19, normal_10]

theorem sep_13_20 : QStrictSeparated sq_13 sq_20 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_20, normal_9]

theorem sep_13_21 : QStrictSeparated sq_13 sq_21 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_21, normal_10]

theorem sep_13_22 : QStrictSeparated sq_13 sq_22 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_22, normal_9]

theorem sep_13_23 : QStrictSeparated sq_13 sq_23 normal_10.1 normal_10.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_23, normal_10]

theorem sep_13_24 : QStrictSeparated sq_13 sq_24 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_24, normal_2]

theorem sep_13_25 : QStrictSeparated sq_13 sq_25 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_25, normal_2]

theorem sep_13_26 : QStrictSeparated sq_13 sq_26 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_26, normal_1]

theorem sep_13_27 : QStrictSeparated sq_13 sq_27 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_27, normal_1]

theorem sep_13_28 : QStrictSeparated sq_13 sq_28 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_28, normal_2]

theorem sep_13_29 : QStrictSeparated sq_13 sq_29 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_29, normal_2]

theorem sep_13_30 : QStrictSeparated sq_13 sq_30 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_30, normal_1]

theorem sep_13_31 : QStrictSeparated sq_13 sq_31 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_31, normal_2]

theorem sep_13_32 : QStrictSeparated sq_13 sq_32 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_32, normal_2]

theorem sep_13_33 : QStrictSeparated sq_13 sq_33 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_33, normal_2]

theorem sep_13_34 : QStrictSeparated sq_13 sq_34 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_34, normal_2]

theorem sep_13_35 : QStrictSeparated sq_13 sq_35 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_35, normal_2]

theorem sep_13_36 : QStrictSeparated sq_13 sq_36 normal_12.1 normal_12.2 := by
  norm_num [QStrictSeparated, qsupport, sq_13, sq_36, normal_12]

theorem row_13 : ∀ j : Fin 37, (13 : Fin 37) < j →
    QStrictSeparated (squares 13) (squares j) (normal 13 j).1 (normal 13 j).2 := by
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
  · exact sep_13_14
  · exact sep_13_15
  · exact sep_13_16
  · exact sep_13_17
  · exact sep_13_18
  · exact sep_13_19
  · exact sep_13_20
  · exact sep_13_21
  · exact sep_13_22
  · exact sep_13_23
  · exact sep_13_24
  · exact sep_13_25
  · exact sep_13_26
  · exact sep_13_27
  · exact sep_13_28
  · exact sep_13_29
  · exact sep_13_30
  · exact sep_13_31
  · exact sep_13_32
  · exact sep_13_33
  · exact sep_13_34
  · exact sep_13_35
  · exact sep_13_36

theorem sep_14_15 : QStrictSeparated sq_14 sq_15 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_15, normal_9]

theorem sep_14_16 : QStrictSeparated sq_14 sq_16 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_16, normal_9]

theorem sep_14_17 : QStrictSeparated sq_14 sq_17 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_17, normal_9]

theorem sep_14_18 : QStrictSeparated sq_14 sq_18 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_18, normal_9]

theorem sep_14_19 : QStrictSeparated sq_14 sq_19 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_19, normal_9]

theorem sep_14_20 : QStrictSeparated sq_14 sq_20 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_20, normal_9]

theorem sep_14_21 : QStrictSeparated sq_14 sq_21 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_21, normal_9]

theorem sep_14_22 : QStrictSeparated sq_14 sq_22 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_22, normal_9]

theorem sep_14_23 : QStrictSeparated sq_14 sq_23 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_23, normal_9]

theorem sep_14_24 : QStrictSeparated sq_14 sq_24 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_24, normal_2]

theorem sep_14_25 : QStrictSeparated sq_14 sq_25 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_25, normal_1]

theorem sep_14_26 : QStrictSeparated sq_14 sq_26 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_26, normal_1]

theorem sep_14_27 : QStrictSeparated sq_14 sq_27 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_27, normal_9]

theorem sep_14_28 : QStrictSeparated sq_14 sq_28 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_28, normal_2]

theorem sep_14_29 : QStrictSeparated sq_14 sq_29 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_29, normal_1]

theorem sep_14_30 : QStrictSeparated sq_14 sq_30 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_30, normal_1]

theorem sep_14_31 : QStrictSeparated sq_14 sq_31 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_31, normal_2]

theorem sep_14_32 : QStrictSeparated sq_14 sq_32 normal_2.1 normal_2.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_32, normal_2]

theorem sep_14_33 : QStrictSeparated sq_14 sq_33 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_33, normal_0]

theorem sep_14_34 : QStrictSeparated sq_14 sq_34 normal_11.1 normal_11.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_34, normal_11]

theorem sep_14_35 : QStrictSeparated sq_14 sq_35 normal_9.1 normal_9.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_35, normal_9]

theorem sep_14_36 : QStrictSeparated sq_14 sq_36 normal_17.1 normal_17.2 := by
  norm_num [QStrictSeparated, qsupport, sq_14, sq_36, normal_17]

theorem row_14 : ∀ j : Fin 37, (14 : Fin 37) < j →
    QStrictSeparated (squares 14) (squares j) (normal 14 j).1 (normal 14 j).2 := by
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
  · exact sep_14_15
  · exact sep_14_16
  · exact sep_14_17
  · exact sep_14_18
  · exact sep_14_19
  · exact sep_14_20
  · exact sep_14_21
  · exact sep_14_22
  · exact sep_14_23
  · exact sep_14_24
  · exact sep_14_25
  · exact sep_14_26
  · exact sep_14_27
  · exact sep_14_28
  · exact sep_14_29
  · exact sep_14_30
  · exact sep_14_31
  · exact sep_14_32
  · exact sep_14_33
  · exact sep_14_34
  · exact sep_14_35
  · exact sep_14_36

theorem sep_15_16 : QStrictSeparated sq_15 sq_16 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_16, normal_18]

theorem sep_15_17 : QStrictSeparated sq_15 sq_17 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_17, normal_0]

theorem sep_15_18 : QStrictSeparated sq_15 sq_18 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_18, normal_19]

theorem sep_15_19 : QStrictSeparated sq_15 sq_19 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_19, normal_19]

theorem sep_15_20 : QStrictSeparated sq_15 sq_20 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_20, normal_18]

theorem sep_15_21 : QStrictSeparated sq_15 sq_21 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_21, normal_19]

theorem sep_15_22 : QStrictSeparated sq_15 sq_22 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_22, normal_18]

theorem sep_15_23 : QStrictSeparated sq_15 sq_23 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_23, normal_19]

theorem sep_15_24 : QStrictSeparated sq_15 sq_24 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_24, normal_0]

theorem sep_15_25 : QStrictSeparated sq_15 sq_25 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_25, normal_0]

theorem sep_15_26 : QStrictSeparated sq_15 sq_26 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_26, normal_0]

theorem sep_15_27 : QStrictSeparated sq_15 sq_27 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_27, normal_0]

theorem sep_15_28 : QStrictSeparated sq_15 sq_28 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_28, normal_0]

theorem sep_15_29 : QStrictSeparated sq_15 sq_29 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_29, normal_0]

theorem sep_15_30 : QStrictSeparated sq_15 sq_30 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_30, normal_0]

theorem sep_15_31 : QStrictSeparated sq_15 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_31, normal_0]

theorem sep_15_32 : QStrictSeparated sq_15 sq_32 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_32, normal_0]

theorem sep_15_33 : QStrictSeparated sq_15 sq_33 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_33, normal_0]

theorem sep_15_34 : QStrictSeparated sq_15 sq_34 normal_20.1 normal_20.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_34, normal_20]

theorem sep_15_35 : QStrictSeparated sq_15 sq_35 normal_20.1 normal_20.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_35, normal_20]

theorem sep_15_36 : QStrictSeparated sq_15 sq_36 normal_21.1 normal_21.2 := by
  norm_num [QStrictSeparated, qsupport, sq_15, sq_36, normal_21]

theorem row_15 : ∀ j : Fin 37, (15 : Fin 37) < j →
    QStrictSeparated (squares 15) (squares j) (normal 15 j).1 (normal 15 j).2 := by
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
  · exact sep_15_16
  · exact sep_15_17
  · exact sep_15_18
  · exact sep_15_19
  · exact sep_15_20
  · exact sep_15_21
  · exact sep_15_22
  · exact sep_15_23
  · exact sep_15_24
  · exact sep_15_25
  · exact sep_15_26
  · exact sep_15_27
  · exact sep_15_28
  · exact sep_15_29
  · exact sep_15_30
  · exact sep_15_31
  · exact sep_15_32
  · exact sep_15_33
  · exact sep_15_34
  · exact sep_15_35
  · exact sep_15_36

theorem sep_16_17 : QStrictSeparated sq_16 sq_17 normal_1.1 normal_1.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_17, normal_1]

theorem sep_16_18 : QStrictSeparated sq_16 sq_18 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_18, normal_0]

theorem sep_16_19 : QStrictSeparated sq_16 sq_19 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_19, normal_19]

theorem sep_16_20 : QStrictSeparated sq_16 sq_20 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_20, normal_18]

theorem sep_16_21 : QStrictSeparated sq_16 sq_21 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_21, normal_19]

theorem sep_16_22 : QStrictSeparated sq_16 sq_22 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_22, normal_19]

theorem sep_16_23 : QStrictSeparated sq_16 sq_23 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_23, normal_0]

theorem sep_16_24 : QStrictSeparated sq_16 sq_24 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_24, normal_0]

theorem sep_16_25 : QStrictSeparated sq_16 sq_25 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_25, normal_0]

theorem sep_16_26 : QStrictSeparated sq_16 sq_26 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_26, normal_0]

theorem sep_16_27 : QStrictSeparated sq_16 sq_27 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_27, normal_0]

theorem sep_16_28 : QStrictSeparated sq_16 sq_28 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_28, normal_0]

theorem sep_16_29 : QStrictSeparated sq_16 sq_29 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_29, normal_0]

theorem sep_16_30 : QStrictSeparated sq_16 sq_30 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_30, normal_0]

theorem sep_16_31 : QStrictSeparated sq_16 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_31, normal_0]

theorem sep_16_32 : QStrictSeparated sq_16 sq_32 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_32, normal_0]

theorem sep_16_33 : QStrictSeparated sq_16 sq_33 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_33, normal_0]

theorem sep_16_34 : QStrictSeparated sq_16 sq_34 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_34, normal_0]

theorem sep_16_35 : QStrictSeparated sq_16 sq_35 normal_20.1 normal_20.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_35, normal_20]

theorem sep_16_36 : QStrictSeparated sq_16 sq_36 normal_21.1 normal_21.2 := by
  norm_num [QStrictSeparated, qsupport, sq_16, sq_36, normal_21]

theorem row_16 : ∀ j : Fin 37, (16 : Fin 37) < j →
    QStrictSeparated (squares 16) (squares j) (normal 16 j).1 (normal 16 j).2 := by
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
  · exact sep_16_17
  · exact sep_16_18
  · exact sep_16_19
  · exact sep_16_20
  · exact sep_16_21
  · exact sep_16_22
  · exact sep_16_23
  · exact sep_16_24
  · exact sep_16_25
  · exact sep_16_26
  · exact sep_16_27
  · exact sep_16_28
  · exact sep_16_29
  · exact sep_16_30
  · exact sep_16_31
  · exact sep_16_32
  · exact sep_16_33
  · exact sep_16_34
  · exact sep_16_35
  · exact sep_16_36

theorem sep_17_18 : QStrictSeparated sq_17 sq_18 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_18, normal_19]

theorem sep_17_19 : QStrictSeparated sq_17 sq_19 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_19, normal_18]

theorem sep_17_20 : QStrictSeparated sq_17 sq_20 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_20, normal_18]

theorem sep_17_21 : QStrictSeparated sq_17 sq_21 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_21, normal_18]

theorem sep_17_22 : QStrictSeparated sq_17 sq_22 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_22, normal_18]

theorem sep_17_23 : QStrictSeparated sq_17 sq_23 normal_19.1 normal_19.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_23, normal_19]

theorem sep_17_24 : QStrictSeparated sq_17 sq_24 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_24, normal_0]

theorem sep_17_25 : QStrictSeparated sq_17 sq_25 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_25, normal_0]

theorem sep_17_26 : QStrictSeparated sq_17 sq_26 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_26, normal_0]

theorem sep_17_27 : QStrictSeparated sq_17 sq_27 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_27, normal_0]

theorem sep_17_28 : QStrictSeparated sq_17 sq_28 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_28, normal_0]

theorem sep_17_29 : QStrictSeparated sq_17 sq_29 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_29, normal_0]

theorem sep_17_30 : QStrictSeparated sq_17 sq_30 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_30, normal_0]

theorem sep_17_31 : QStrictSeparated sq_17 sq_31 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_31, normal_0]

theorem sep_17_32 : QStrictSeparated sq_17 sq_32 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_32, normal_0]

theorem sep_17_33 : QStrictSeparated sq_17 sq_33 normal_0.1 normal_0.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_33, normal_0]

theorem sep_17_34 : QStrictSeparated sq_17 sq_34 normal_20.1 normal_20.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_34, normal_20]

theorem sep_17_35 : QStrictSeparated sq_17 sq_35 normal_20.1 normal_20.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_35, normal_20]

theorem sep_17_36 : QStrictSeparated sq_17 sq_36 normal_18.1 normal_18.2 := by
  norm_num [QStrictSeparated, qsupport, sq_17, sq_36, normal_18]

theorem row_17 : ∀ j : Fin 37, (17 : Fin 37) < j →
    QStrictSeparated (squares 17) (squares j) (normal 17 j).1 (normal 17 j).2 := by
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
  · exact sep_17_18
  · exact sep_17_19
  · exact sep_17_20
  · exact sep_17_21
  · exact sep_17_22
  · exact sep_17_23
  · exact sep_17_24
  · exact sep_17_25
  · exact sep_17_26
  · exact sep_17_27
  · exact sep_17_28
  · exact sep_17_29
  · exact sep_17_30
  · exact sep_17_31
  · exact sep_17_32
  · exact sep_17_33
  · exact sep_17_34
  · exact sep_17_35
  · exact sep_17_36

end Packing37
