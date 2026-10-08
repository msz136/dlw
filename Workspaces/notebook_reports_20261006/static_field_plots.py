"""Self-contained notebook cells: cached physical fields, static KP panels."""
import nbformat as nbf

PLOT_HELPERS = r'''
from matplotlib.colors import Normalize, BoundaryNorm, ListedColormap, LinearSegmentedColormap
from matplotlib.ticker import MaxNLocator

def checked_window(window, available, label):
    lo, hi = window
    if not np.isfinite([lo, hi]).all() or lo >= hi:
        raise ValueError(f'{label} 必须是有限且递增的 (下限, 上限)。')
    if lo < available[0]-1e-10 or hi > available[1]+1e-10:
        raise ValueError(f'{label}={window} 超出已计算范围 {available}；请扩大计算域后重新准备场数据。')
    return lo, hi

def draw_field_panels(x, y, numerical, exact, title, names, config, second_axis='y'):
    # 只裁剪已有数据；完整数组保留，改变展示参数不会触发计算。
    xm = (x >= config['xlim'][0]) & (x <= config['xlim'][1])
    ym = (y >= config['ylim'][0]) & (y <= config['ylim'][1])
    if xm.sum() < 3 or ym.sum() < 2:
        raise ValueError('绘图区间至少需要三个 x 点和两个纵向采样点。')
    xx, yy = x[xm], y[ym]
    X, Y = np.meshgrid(xx, yy)
    fig = plt.figure(figsize=(14, 8.5), layout='constrained')
    grid = fig.add_gridspec(2, 3, width_ratios=(1.15, 1, 1))
    cropped = []
    for row, name in enumerate(names):
        n = numerical[row][np.ix_(ym, xm)]
        e = exact[row][np.ix_(ym, xm)]
        cropped.append(abs(n-e))
        lower, upper = min(n.min(), e.min()), max(n.max(), e.max())
        if upper <= lower:
            upper = lower+1e-12
        center = config.get('centers', {}).get(name, 0.)
        color_map = config['cmap']
        if color_map == 'zero_white':
            # 线性色阶保持幅值含义；零附近留白，其余用清楚、柔和的分层颜色。
            steps = config.get('color_steps', 12)
            blue = LinearSegmentedColormap.from_list('muted_blue', ['#a9c6d1', '#668fa3', '#355c73'])
            red = LinearSegmentedColormap.from_list('muted_red', ['#d7b4a4', '#bc8574', '#965e54'])
            negative = [blue(t) for t in np.linspace(1, 0, steps-1)] + ['#ffffff']
            positive = ['#ffffff'] + [red(t) for t in np.linspace(0, 1, steps-1)]
            tolerance = max(abs(lower-center), abs(upper-center), 1e-12)*1e-6
            if upper <= center+tolerance:
                color_map = ListedColormap(negative)
                bounds = np.linspace(lower, center, steps+1)
            elif lower >= center-tolerance:
                color_map = ListedColormap(positive)
                bounds = np.linspace(center, upper, steps+1)
            else:
                # 两侧使用相同幅值尺度，不把微小异号误差放大成深色波峰。
                span = max(abs(lower-center), abs(upper-center))
                color_map = ListedColormap(negative + positive)
                bounds = np.linspace(center-span, center+span, 2*steps+1)
            norm = BoundaryNorm(bounds, color_map.N, clip=True)
        else:
            norm = Normalize(lower, upper)
        error_map = config['error_cmap']
        if error_map == 'white_red':
            muted = LinearSegmentedColormap.from_list('muted_error', ['#d8bd91', '#b98c59', '#896540'])
            error_map = ListedColormap(['#ffffff'] + [muted(t) for t in np.linspace(0, 1, config.get('color_steps', 12)-1)])
        levels = np.linspace(lower, upper, config['levels']+2)[1:-1]
        ax = fig.add_subplot(grid[row, 0], projection='3d')
        sy, sx = max(1, len(yy)//160), max(1, len(xx)//300)
        ax.plot_surface(X[::sy, ::sx], Y[::sy, ::sx], n[::sy, ::sx],
                        cmap=color_map, norm=norm, linewidth=0,
                        rcount=len(yy[::sy]), ccount=len(xx[::sx]), antialiased=False, shade=False)
        ax.set(xlabel='$x$', ylabel=f'${second_axis}$', zlabel=f'${name}$',
               xlim=config['xlim'], ylim=config['ylim'])
        ax.view_init(config['elev'], config['azim'])
        ax.set_box_aspect((1.2, 1, .85))
        ax.set_title(f'${name}$: numerical surface')
        for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
            axis.set_major_locator(MaxNLocator(4))
        for col, values, label in ((1, n, 'Numerical'), (2, e, 'Exact')):
            ax = fig.add_subplot(grid[row, col])
            if config.get('map_style', 'contour') == 'contour':
                if values.max() > values.min():
                    ax.contour(xx, yy, values, levels=levels, cmap=color_map, norm=norm,
                               linewidths=config.get('contour_width', 1.1))
                image = plt.cm.ScalarMappable(norm=norm, cmap=color_map)
                label += ' contours'
                ax.grid(color='#dddddd', linewidth=.4, alpha=.45)
            else:
                image = ax.pcolormesh(xx, yy, values, cmap=color_map, norm=norm, shading='auto')
                label += ' field'
            ax.set(xlabel='$x$', ylabel=f'${second_axis}$',
                   xlim=config['xlim'], ylim=config['ylim'], title=f'${name}$: {label}')
            ax.set_box_aspect(1)
            if col == 2:
                fig.colorbar(image, ax=ax, fraction=.045, pad=.025, label=f'${name}$')
    fig.suptitle(title, fontsize=16)
    plt.show()

    fig = plt.figure(figsize=(11, 8), layout='constrained')
    grid = fig.add_gridspec(2, 2)
    for row, name in enumerate(names):
        error = cropped[row]
        ax = fig.add_subplot(grid[row, 0], projection='3d')
        ax.plot_surface(X[::sy, ::sx], Y[::sy, ::sx], error[::sy, ::sx],
                        cmap=error_map, vmin=0, vmax=float(error.max()), linewidth=0,
                        rcount=len(yy[::sy]), ccount=len(xx[::sx]), antialiased=False, shade=False)
        ax.set(xlabel='$x$', ylabel=f'${second_axis}$', zlabel=f'$e_{{{name}}}$',
               xlim=config['xlim'], ylim=config['ylim'])
        ax.view_init(config['elev'], config['azim'])
        ax.set_box_aspect((1.2, 1, .85))
        ax.ticklabel_format(axis='z', style='sci', scilimits=(0, 0))
        ax.set_title(f'${name}$: absolute error surface')
        ax = fig.add_subplot(grid[row, 1])
        error_norm = Normalize(0, max(float(error.max()), 1e-15))
        if config.get('map_style', 'contour') == 'contour':
            error_levels = np.linspace(0, error_norm.vmax, config['levels']+2)[1:-1]
            if error.max() > 0:
                ax.contour(xx, yy, error, levels=error_levels, cmap=error_map, norm=error_norm,
                           linewidths=config.get('contour_width', 1.1))
            image = plt.cm.ScalarMappable(norm=error_norm, cmap=error_map)
            ax.grid(color='#dddddd', linewidth=.4, alpha=.45)
        else:
            image = ax.pcolormesh(xx, yy, error, shading='auto', cmap=error_map, norm=error_norm)
        ax.set(xlabel='$x$', ylabel=f'${second_axis}$', xlim=config['xlim'],
               ylim=config['ylim'], title=f'${name}$: absolute error '+config.get('map_style', 'contour'))
        ax.set_box_aspect(1)
        fig.colorbar(image, ax=ax, fraction=.045, pad=.025, format='%.1e')
    fig.suptitle(title+' | absolute error', fontsize=16)
    plt.show()
'''

DLW_CONFIG = '''# 只调整下面的绘图参数，并重运行本单元与最后的画图单元。
# 不改变已经计算好的数值场；时间取 FIELD_CONFIG['T']。
PLOT_CONFIG = dict(
    cases=('A', 'B', 'C'),
    windows={
        'A': dict(xlim=(-3., 4.), ylim=(-3., 3.)),
        'B': dict(xlim=(-30., 30.), ylim=(-30., 30.)),
        'C': dict(xlim=(-30., 30.), ylim=(-30., 30.)),
    },
    # KP 参考图：jet 彩色等高线，二维白底；可改为 map_style='mesh'。
    cmap='jet', error_cmap='jet', map_style='contour', levels=11, contour_width=1.1,
    elev=28., azim=-62.,
)
'''

DLW_DATA = '''# 与前面的误差表分开准备宽域场图；保持原空间、时间步长。
# 改变计算范围、方案或时间后运行本单元；只改 PLOT_CONFIG 不用运行它。
FIELD_CONFIG = dict(CONFIG, L=80., nx=512, yhalf=30.,
                    eval_half=30., eval_points=1201)
FIELD_MODEL, FIELD_METHOD, FIELD_MESH = 'SD2', 'RK4', 'fixed'
if not 0 < FIELD_CONFIG['eval_half'] < FIELD_CONFIG['L']/2:
    raise ValueError('场图评价范围须位于 x 计算域内部。')
if FIELD_CONFIG['yhalf'] <= 0 or FIELD_CONFIG['h'] <= 0:
    raise ValueError('y 计算域半宽与格距必须为正。')
dlw_field_cache = globals().get('dlw_field_cache', {})
field_signature = (tuple(sorted(FIELD_CONFIG.items())), FIELD_MODEL, FIELD_METHOD, FIELD_MESH)
for field_case in CASES:
    cache_key = field_signature, field_case
    if cache_key not in dlw_field_cache:
        computed = solve(field_case, FIELD_MODEL, FIELD_METHOD, FIELD_MESH, FIELD_CONFIG)
        if not computed['completed']:
            raise RuntimeError(f"Case {field_case} 未达到指定时间：{computed['reason']}")
        dlw_field_cache[cache_key] = computed
print(f"场数据已准备：{FIELD_MODEL}, {FIELD_METHOD}, {FIELD_MESH}, T={FIELD_CONFIG['T']:g}。")
'''

DLW_DRAW = '''# 范围检查基于缓存建立时的计算参数，避免使用尚未重新计算的新参数。
saved_field_config = dict(field_signature[0])
for field_case in PLOT_CONFIG['cases']:
    record = dlw_field_cache[field_signature, field_case]
    drawing = dict(PLOT_CONFIG, **PLOT_CONFIG['windows'][field_case])
    checked_window(drawing['xlim'], (-saved_field_config['eval_half'], saved_field_config['eval_half']), f'{field_case}: xlim')
    checked_window(drawing['ylim'], (-saved_field_config['yhalf'], saved_field_config['yhalf']), f'{field_case}: ylim')
    draw_field_panels(record['x'], record['y'], record['fields'], record['exact'],
        f"DLW Case {field_case} | {record['model']} + {record['method']}, {record['mesh']} | t={record['reached']:g}",
        ('u', 'v'), drawing)
'''

HS_HISTORY = '''# 保存原有推进过程中的快照，末尾画图不再重新求解。
from types import FunctionType
hs_histories = {}
hs_saved_steps = set(np.unique(np.linspace(0, hs_steps, min(33, hs_steps+1), dtype=int)))
def hs_start_history(case):
    reference = FunctionType(hs_exact_physical.__code__, dict(globals()),
                             hs_exact_physical.__name__, hs_exact_physical.__defaults__)
    hs_histories[case] = dict(reference=reference, records=[], T=hs_T)
def hs_capture(case, step_index):
    if step_index not in hs_saved_steps:
        return
    t = step_index*hs_dt
    fields = {'Integrable': hs_integrable_fields(t, hs_integrable),
              'FD': hs_fd_fields(t, hs_fd)}
    hs_histories[case]['records'].append((t, {
        name: {key: np.array(value, copy=True) for key, value in field.items()}
        for name, field in fields.items()}))
'''

HS_CONFIG = '''# 2HS 只有一个空间变量 x；三维图的第二个坐标为时间 t。
# 只修改此配置并重运行最后画图单元，无需重新推进。
PLOT_CONFIG = dict(
    xlim=(-5., 5.), tlim=(0., hs_T),
    cases=('one', 'two'), methods=('Integrable', 'FD'),
    xpoints=601, cmap='jet', error_cmap='jet', map_style='contour', levels=11, contour_width=1.1,
    centers={'u': 0., r'\\rho': 1.},
    elev=28., azim=-62.,
)
'''

HS_DRAW = r'''
for hs_case in PLOT_CONFIG['cases']:
    history = hs_histories[hs_case]
    checked_window(PLOT_CONFIG['tlim'], (0., history['T']), 'tlim')
    records = history['records']
    for hs_method in PLOT_CONFIG['methods']:
        left = max(float(fields[hs_method][key][0]) for _, fields in records for key in ('x', 'rhoX'))
        right = min(float(fields[hs_method][key][-1]) for _, fields in records for key in ('x', 'rhoX'))
        checked_window(PLOT_CONFIG['xlim'], (left, right), 'xlim')
        x = np.linspace(*PLOT_CONFIG['xlim'], PLOT_CONFIG['xpoints'])
        t = np.array([time for time, _ in records])
        numerical, exact = [], []
        for field, coordinate in (('u', 'x'), ('rho', 'rhoX')):
            numerical.append(np.array([hs_interpolate(fields[hs_method][coordinate], fields[hs_method][field], x)
                                       for _, fields in records]))
            exact.append(np.array([history['reference'](x, time)[field] for time in t]))
        drawing = dict(PLOT_CONFIG, ylim=PLOT_CONFIG['tlim'])
        title = f"2HS {hs_case} soliton | {hs_method} + RK4 | x,t"
        draw_field_panels(x, t, numerical, exact, title, ('u', r'\rho'), drawing, second_axis='t')
        # 固定终点的波形与误差，直接比较数值精度。
        fig, axes = plt.subplots(2, 2, figsize=(10, 6), layout='constrained')
        for row, (field, name) in enumerate((('u', 'u'), ('rho', r'\rho'))):
            axes[row, 0].plot(x, exact[row][-1], 'r-', label='Exact')
            axes[row, 0].plot(x, numerical[row][-1], 'b--', label='Numerical')
            axes[row, 1].plot(x, abs(numerical[row][-1]-exact[row][-1]), color='#7d247c')
            axes[row, 0].set(ylabel=f'${name}$', title='Numerical / exact')
            axes[row, 1].set(ylabel=f'$e_{{{name}}}$', title='Absolute error')
            axes[row, 0].legend(frameon=False)
        for ax in axes.flat:
            ax.set(xlabel='$x$', xlim=PLOT_CONFIG['xlim']);ax.grid(alpha=.2)
        fig.suptitle(f"2HS {hs_case} soliton | {hs_method} | t={t[-1]:g}")
        plt.show()
'''

def code(id, text):
    return nbf.v4.new_code_cell(text.strip(), id=id)

def md(id, text):
    return nbf.v4.new_markdown_cell(text.strip(), id=id)

def apply_dlw(notebook):
    if any(c.id == 'dlw-field-config' for c in notebook.cells):
        return notebook
    cells=[]
    for cell in notebook.cells:
        if cell.id in ('dlw-curve-text', 'dlw-curves'):
            continue
        if cell.id == 'dlw-config':
            start=cell.source.index("    plot_xlim=")
            end=cell.source.index('\n', start)
            cell.source=cell.source[:start]+cell.source[end+1:]
            start=cell.source.index("if not np.isfinite(CONFIG['plot_xlim'])")
            end=cell.source.index('MODELS =', start)
            cell.source=cell.source[:start]+cell.source[end:]
            cell.source=cell.source.replace('；绘图区间须包含在评价区间内。', '；绘图参数在末尾独立设置。')
        if cell.id == 'dlw-conclusion-text':
            cell.source=cell.source.replace('## 8', '## 7')
        cells.append(cell)
    cells += [md('dlw-field-text', r'''## 8　物理场与误差分布

固定 $t=0.01$，A 在 $x\in[-3,4]$、$y\in[-3,3]$ 展示完整波谷；B、C 在 $x,y\in[-30,30]$ 展示全貌。每个算例上行为 $u$，下行为 $v$；三列依次为数值曲面、数值二维彩图、解析二维彩图，后两者共用色标与等高线高度。物理场零值为白色，负值为蓝色，正值为红色；另图显示绝对误差曲面和二维误差分布，零误差也为白色。

场图采用 SD2、RK4 与固定网格；实际计算域扩大为 $x\in[-40,40)$、$y\in[-30,30)$，保持 $\Delta x=0.15625$、$h=0.125$、$\Delta t=0.000125$。此前误差表仍取各自的原计算与评价范围。A、B 为单孤子，C 的两条相互作用波脊在宽 $y$ 范围内可分辨。'''),
        code('dlw-field-data', DLW_DATA),
        md('dlw-plot-config-text', '绘图参数集中在下方；改变展示范围、颜色、等高线数量或视角后，只需运行配置与最后的画图单元。超出已计算范围时，需要先扩大场数据计算域。'),
        code('dlw-field-config', DLW_CONFIG), code('dlw-field-helpers', PLOT_HELPERS),
        code('dlw-field-plots', DLW_DRAW)]
    notebook.cells=cells
    return notebook

def apply_hs(notebook):
    if any(c.id == 'hs-field-config' for c in notebook.cells):
        return notebook
    cells=[]
    for cell in notebook.cells:
        if cell.id in ('hs-waveform-lead', 'hs-waveforms', 'hs-two-figures'):
            continue
        if cell.id == 'hs-config':
            cell.source=cell.source.replace('    plot_xlim=(-5.0, 5.0),      # 所有波形图和误差图的 x 范围\n','')
            cell.source=cell.source.replace(', *CONFIG["plot_xlim"]','')
            cell.source=cell.source.replace('if CONFIG["plot_xlim"][0] >= CONFIG["plot_xlim"][1]:\n    raise ValueError("plot_xlim 须为递增的 (左端, 右端)。")\n','')
            cell.source=cell.source.replace('    "绘图左端": CONFIG["plot_xlim"][0], "绘图右端": CONFIG["plot_xlim"][1],\n','')
        if cell.id in ('hs-reference','hs-two-initial'):
            cell.source=cell.source.split('\nif not (hs_left < CONFIG["plot_xlim"]',1)[0]
        if cell.id == 'hs-evolve':
            cells.append(code('hs-history', HS_HISTORY))
        if cell.id in ('hs-evolve', 'hs-two-evolve'):
            case='one' if cell.id == 'hs-evolve' else 'two'
            cell.source=cell.source.replace('hs_integrable, hs_fd = hs_initial_states()',
                f'hs_integrable, hs_fd = hs_initial_states()\nhs_start_history("{case}")\nhs_capture("{case}", 0)',1)
            cell.source=cell.source.replace('\nhs_live_fields =', f'\n    hs_capture("{case}", hs_step+1)\nhs_live_fields =',1)
        if cell.id == 'hs-error':
            a=cell.source.index('\ndef hs_plot_data(')
            b=cell.source.index('hs_single_summary =')
            cell.source=cell.source[:a]+'\n'+cell.source[b:]
        if cell.id == 'hs-two-plots':
            cell.source=cell.source[cell.source.index('print(pd.DataFrame'):]
        cells.append(cell)
    cells += [md('hs-field-text', r'''## 6　物理场与误差分布

2HS 的两个物理场为 $u,\rho$，只有一个空间变量 $x$。三维图以 $x,t$ 为底面：上行为 $u$，下行为 $\rho$，三列依次为数值曲面、数值二维彩图、解析二维彩图；数值与解析使用同一色标。另列绝对误差曲面、二维误差图及终点数值／解析波形对照。图包含单孤子、二孤子和两种空间方案。

保存原时间推进中的33个快照；绘图不再推进方程。右尾偏差在完整 $x$ 范围的物理场与误差中均保留。'''),
        code('hs-field-config', HS_CONFIG), code('hs-field-helpers', PLOT_HELPERS), code('hs-field-plots', HS_DRAW)]
    notebook.cells=cells
    return notebook
