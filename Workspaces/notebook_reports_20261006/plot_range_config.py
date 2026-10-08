"""Shared notebook transformation for independently configurable plot windows."""

HS_CONFIG = '''# 计算域使用辅助坐标 X；绘图和误差评价使用物理坐标 x。
CONFIG = dict(
    X_domain=(-6.0, 6.0),       # 辅助计算区间；物理端点由孤子映射给出
    N=2400,                    # 网格份数；a = 区间长度 / N
    dt=0.003125, T=0.5,         # 时间步长、终止时间
    plot_xlim=(-5.0, 5.0),      # 所有波形图和误差图的 x 范围
    xMin=-1.0, xMax=1.0,        # 误差表的评价区间
    evaluationPoints=32001,    # 评价与绘图采样点数
)
hs_cfg = CONFIG
hs_N = CONFIG["N"]
hs_Xleft, hs_Xright = CONFIG["X_domain"]
hs_dt, hs_T = CONFIG["dt"], CONFIG["T"]
hs_xmin, hs_xmax = CONFIG["xMin"], CONFIG["xMax"]
hs_neval = CONFIG["evaluationPoints"]
if not np.isfinite([hs_Xleft, hs_Xright, hs_dt, hs_T, hs_xmin, hs_xmax, *CONFIG["plot_xlim"]]).all():
    raise ValueError("计算域、时间、评价和绘图范围须取有限实数。")
if not (hs_Xleft < hs_Xright and hs_dt > 0 and hs_T >= 0 and hs_xmin < hs_xmax):
    raise ValueError("计算域、评价区间须递增，且 dt>0、T≥0。")
if CONFIG["plot_xlim"][0] >= CONFIG["plot_xlim"][1]:
    raise ValueError("plot_xlim 须为递增的 (左端, 右端)。")
if not isinstance(hs_N, int) or not 20 <= hs_N <= 6400:
    raise ValueError("N 应为 20—6400 的整数。")
hs_a = (hs_Xright-hs_Xleft)/hs_N
if not isinstance(hs_neval, int) or not 101 <= hs_neval <= 64001:
    raise ValueError("评价点数应为 101—64001 的整数。")
hs_steps = round(hs_T/hs_dt)
if abs(hs_steps*hs_dt-hs_T) > 1e-12 or hs_steps > 3200:
    raise ValueError("T 须为 dt 的整数倍，且步数≤3200。")
print(pd.DataFrame([{
    "N": hs_N, "a": hs_a, "X 左端": hs_Xleft, "X 右端": hs_Xright,
    "dt": hs_dt, "T": hs_T, "时间步数": hs_steps, "评价点数": hs_neval,
    "绘图左端": CONFIG["plot_xlim"][0], "绘图右端": CONFIG["plot_xlim"][1],
}]).to_string(index=False))
'''

HS_HELPER = '''def hs_plot_data(fields):
    lo, hi = hs_cfg["plot_xlim"]
    if not np.isfinite([lo, hi]).all() or lo >= hi:
        raise ValueError("plot_xlim 须为有限且递增的 (左端, 右端)。")
    for values in fields.values():
        for key in ("x", "rhoX"):
            if lo < values[key][0] or hi > values[key][-1]:
                raise ValueError("plot_xlim 超出数值解范围；请扩大 CONFIG['X_domain'] 后重新计算。")
    xx = np.linspace(lo, hi, hs_neval)
    reference = hs_exact_physical(xx, hs_T)
    errors = {}
    for name, values in fields.items():
        errors[name] = {
            "eu": np.abs(hs_interpolate(values["x"], values["u"], xx)-reference["u"]),
            "er": np.abs(hs_interpolate(values["rhoX"], values["rho"], xx)-reference["rho"]),
        }
    return lo, hi, xx, reference, errors

'''


def apply_hs_plot_range(notebook):
    for cell in notebook.cells:
        source = cell.source
        if cell.cell_type == 'markdown':
            source = source.replace('N=1600', 'N=2400').replace('等分 1600 段', '等分 2400 段')
            source = source.replace('X\\in[-4,4]', 'X\\in[-6,6]').replace('X_k=-4+ka', 'X_k=-6+ka').replace('X=-4,4', 'X=-6,6')
            source = source.replace('[-4.8,\\,3.8]', '[-6.8,\\,5.8]').replace('[-5.7,\\,3.7]', '[-7.7,\\,5.7]')
            source = source.replace('0.005375', '0.005250').replace('0.005886', '0.005591')
            source = source.replace('误差图每段宽 $0.02$', '误差图按 `plot_xlim` 指定的区间等分为 100 段')
            if cell.id == 'hs-single-model' and 'CONFIG' not in source:
                source += '\n\n默认参数如下；计算域、网格数、时间和绘图范围均可在 `CONFIG` 中调整。'
        if cell.id == 'hs-config':
            source = HS_CONFIG
        if cell.id in ('hs-reference', 'hs-two-initial') and '绘图区间必须位于' not in source:
            source += '\nif not (hs_left < CONFIG["plot_xlim"][0] < CONFIG["plot_xlim"][1] < hs_right):\n    raise ValueError("绘图区间必须位于物理计算域内部；请扩大 CONFIG[\'X_domain\']。")\n'
        if cell.id == 'hs-error' and 'def hs_plot_data' not in source:
            marker = '# 每个绘图区间保留其评价点上的最大误差。'
            before, after = source.split(marker, 1)
            plot, tail = after.split('hs_single_summary =', 1)
            plot = plot.replace('hs_xmin', 'plot_lo').replace('hs_xmax', 'plot_hi').replace('hs_xx', 'plot_xx').replace('hs_results[hs_name][hs_key]', 'plot_errors[hs_name][hs_key]')
            plot = plot.replace('ax.set(xlabel=', 'ax.set(xlim=(plot_lo, plot_hi), xlabel=')
            source = before + HS_HELPER + 'plot_lo, plot_hi, plot_xx, plot_reference, plot_errors = hs_plot_data(hs_live_fields)\n' + marker + plot + 'hs_single_summary =' + tail
        if cell.id == 'hs-waveforms' and 'hs_plot_data(fields)' not in source:
            source = source.replace('    fig, axes =', '    plot_lo, plot_hi, plot_xx, reference, _ = hs_plot_data(fields)\n    fig, axes =', 1)
            source = source.replace('ax.plot(hs_xx,', 'ax.plot(plot_xx,').replace('coordinates >= hs_xmin', 'coordinates >= plot_lo').replace('coordinates <= hs_xmax', 'coordinates <= plot_hi')
            source = source.replace('            ax.set_title', '            ax.set_xlim(plot_lo, plot_hi)\n            ax.set_title')
        if cell.id == 'hs-two-plots' and 'hs_plot_data(hs_live_fields)' not in source:
            plot, tail = source.split('print(pd.DataFrame', 1)
            plot = plot.replace('hs_xmin', 'plot_lo').replace('hs_xmax', 'plot_hi').replace('hs_xx', 'plot_xx').replace('hs_reference[field]', 'plot_reference[field]').replace('hs_results[name][key]', 'plot_errors[name][key]')
            plot = plot.replace('ax.set(', 'ax.set(xlim=(plot_lo, plot_hi), ')
            source = 'plot_lo, plot_hi, plot_xx, plot_reference, plot_errors = hs_plot_data(hs_live_fields)\n' + plot + 'print(pd.DataFrame' + tail
        cell.source = source
    return notebook
