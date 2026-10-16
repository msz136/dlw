# Error-field figure verification

The figure uses actual stored A fields from `transport/A_T0.040_dt0.000100`
at t=.01 and .04, for both PE and FD, and field index 1 (physical v).
Every plotted actual/prediction RMS was recomputed and agrees with the
independent transport timeseries CSV to less than 1e-15. Input file hashes,
scales, field norms and checks are retained in `error_fields_validation.json`.

The blue-white-red maps retain signs. There is no smoothing, interpolation,
phase alignment or fitted adjustment. Within each row actual and prediction
have exactly the same symmetric color limits. The residual has its own scale,
prominently marked in red, with its norm relative to the actual v error printed
below. Scales differ across rows and all endpoints are displayed. The panels
show the spatial change without identifying any ridge or band as a soliton.

| Method | Time | Relative v field residual |
|---|---:|---:|
| PE | .01 | 4.55009e-6 |
| FD | .01 | 2.98138e-6 |
| PE | .04 | 0.00196324 |
| FD | .04 | 0.00161953 |

These single-field values differ from the joint u/v residuals quoted in the
main text, as expected. The late v error increases and develops a stronger
vertical feature; both this feature and the oblique ridge are reproduced
by the independent prediction. This visual agreement is backed by the
full-grid norm checks rather than judged by the image alone.

PNG inspected at full rendered view: no clipped labels, overlapping text,
missing glyphs or obscured data. Output is 3187 by 3160 pixels with recorded
300 dpi. PDF uses embedded Type 42 fonts and rasterized field cells; axes,
labels and color bars remain vector elements. Both formats were generated
from the same figure. The standalone script is `error_fields.py`.

Suggested caption: A 算例 v 误差在 t=.01 和 .04 的空间分布。左、中分别为
真实误差与独立线性源传播预测，同一行共用色标；右为两者之差，采用单独
色标并标出相对场残差。误差的幅值和条带分布随时间改变，预测同时复现
这些变化。不同面板的相似颜色须结合其色标比较。
