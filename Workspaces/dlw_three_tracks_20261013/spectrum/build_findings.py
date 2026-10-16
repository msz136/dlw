"""Build the compact numerical findings table from completed analysis outputs."""
from pathlib import Path
import csv
import json
import numpy as np

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"out"

def main():
    manifest=json.loads((OUT/"manifest.json").read_text(encoding="utf-8"))
    rows=[]
    for ds in manifest["inputs"]:
        if "halfdt" in ds["file"]:continue
        with np.load(ds["file"],allow_pickle=False) as d:
            for f,q in ds["final"].items():
                e=d[f][-1]-d["exact_"+f][-1]
                rows.append({"dataset":q["dataset"],"field":f,"rms_error":q["rms_error"],
                    "linf_error":q["linf_error"],"dominant_kx":q["dominant_kx"],"dominant_ky":q["dominant_ky"],
                    "high_fraction_hann":q["high_k_fraction"],"high_fraction_rectangular":q["raw_high_k_fraction"],
                    "central_cwt_peak_wavelength":q["cwt_peak_wavelength"],
                    "periodic_extension_x_jump_rms":float(np.sqrt(np.mean((e[:,0]-e[:,-1])**2))),
                    "periodic_extension_y_jump_rms":float(np.sqrt(np.mean((e[0]-e[-1])**2))),
                    "maximum_component_aspect_ratio":max((c["aspect_ratio"] for c in q["components"]),default=0)})
    with (OUT/"endpoint_summary.csv").open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
    lines=["# 1B 结果核对（2026-10-13）","",
        "全部为当前论文 A/C 算例真实轨道；原生网格 dx = dy = 0.1，21 帧，0 ≤ t ≤ 0.01。误差为物理数值场减同网格连续精确场。以下终态为 t = 0.01；本实验不作长期稳定性或空间收敛结论。","",
        "| 算例/方法 | 场 | RMS 误差 | 最大绝对误差 | Hann 主频 (kx,ky) | 高频占比 Hann / 矩形 | 中央截面小波峰波长 |",
        "|---|---|---:|---:|---|---|---:|"]
    for q in rows:
        lines.append(f"| {q['dataset']} | {q['field']} | {q['rms_error']:.6e} | {q['linf_error']:.6e} | ({q['dominant_kx']:.4f}, {q['dominant_ky']:.4f}) | {q['high_fraction_hann']:.3e} / {q['high_fraction_rectangular']:.3e} | {q['central_cwt_peak_wavelength']:.4f} |")
    lines += ["","## 已得到的证据","",
        "1. 误差包含条带与脊线，部分与真实线孤子方向一致。u 场还存在明显竖条，因此不能把全部误差归为沿原孤子的相位偏差。横向积分重构、边界传递与形变各贡献多少，尚未分解。",
        "2. 最强的阈值连通成分普遍呈伸长形状；一个脊线可产生很多格点极值。local_extrema.csv 中的条数不是独立波包数，更不是孤子数。阈值为每帧最大绝对误差的 25%；连通域默认阈值为 50%，另存 35%/50%/65% 敏感性。",
        "3. Fourier 高频尾非常依赖窗口。矩形截断将开边界误差场作周期延拓，边界不匹配引入泄漏；Hann 后高频占比下降多个数量级。该变化也重加权了场的边界部分，不能单凭这一比较将所有高频量严格归因于窗口，但足以否定直接把矩形谱尾解释为新增孤子或辐射的证据力。",
        "4. 当前 A 算例 SD 的误差大于 FD；C 算例 SD 在 u 上略好，而 v 相近。因此这组结果不支持可积半离散普遍降低误差。比较需保持相同网格、时间推进、误差定义与边界。",
        "5. 中央 x 截面的 Morlet 局域尺度可重复辨认；它是形态诊断，不是 Lax 谱。未求逆散射离散本征值，因此没有证据认定“幽灵孤子”。","",
        "## 时间步长稳健性","",
        "| 算例 | 场 | 半 dt 相对场差 | 归一化 Fourier 功率 L1 差 | 主频相同 | 最强绝对峰坐标距离 |",
        "|---|---|---:|---:|---|---:|"]
    for q in manifest["dt_refinement"]:
        lines.append(f"| {q['case']} | {q['field']} | {q['relative_field_difference']:.3e} | {q['normalized_power_L1_difference']:.3e} | {q['dominant_k_unchanged']} | {q['abs_peak_distance']:.2g} |")
    maximum=max(c["max_parseval_relative_residual"] for d in manifest["inputs"] for c in d["checks"])
    allzero=all(c["initial_error_below_roundoff_floor"] for d in manifest["inputs"] for c in d["checks"])
    lines += ["",f"所有 t = 0 场误差均低于参考尺度的舍入阈值：{allzero}。Hann Parseval 最大相对残差 {maximum:.3e}；已知二维模态、偶数网格 Nyquist 模态与 Morlet 波长标尺另作校准，见 manifest。",
        "","四个 GIF 均为 21 帧，真实时间标注、每段动画全时段固定色阶。A/C 和不同方法各自的色阶不同；方法比较应读取数值表或色条，而非比较色彩饱和度。",
        "","## 文件入口","",
        "- `out/error_diagnostics_summary.png`：误差时序总览。",
        "- `out/A_SD_RK4_fourier.png`、`out/C_SD_RK4_fourier.png`：场与频谱。",
        "- `out/A_SD_RK4_wavelet.png`、`out/C_SD_RK4_wavelet.png`：共同中央截面小波。",
        "- `out/A_SD_RK4_error_evolution.gif`、`out/C_SD_RK4_error_evolution.gif`：误差动画；FD 对照同目录。",
        "- `out/endpoint_summary.csv`、`out/spectral_metrics.csv`、`out/dt_refinement.csv`、`out/threshold_sensitivity.csv`：数值表。",
        "- `out/manifest.json`：输入哈希、版本、校验、方法定义。",
        "- `README.md`：公式与完整复现说明。"]
    (ROOT/"FINDINGS.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"endpoint_rows":len(rows),"max_parseval_residual":maximum,"initial_zero":allzero}))

if __name__=="__main__":main()
