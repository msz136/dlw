"""Report cells for direct bilinear SD and matching comparisons."""
CELLS_UPDATE = {}
TEXT_UPDATE = {
    'spatial-text': r'''## 2　空间离散与边界

$x\in[-20,20)$ 分为 256 份，$\Delta x=0.15625$；$y\in[-1.5,1.5]$ 分为 24 份，$h=0.125$，场值取各份中点。

记 $\delta_-f_j=(f_j-f_{j-1})/h$、$\delta_0f_j=(f_{j+1}-f_{j-1})/(2h)$、$M_-f_j=(f_j+f_{j-1})/2$。$x$ 向采用三点二阶中心差分；二阶导数与 GSG 对照格式的式 (4.13)–(4.14) 使用相同的三点算子：

$$D_1f_i=\frac{f_{i+1}-f_{i-1}}{2\Delta x},\qquad
D_2f_i=\frac{f_{i+1}-2f_i+f_{i-1}}{\Delta x^2}.$$

SD 固定两端各四个节点的解析边界值；SD2 按端点跃变量延拓，FD 按周期延拓。各方案的下边界在本节对应部分给出。''',
    'sd-text': r'''### 2.1　SD

**原双线性方程。**

$$B_{s_-}F_j\!\cdot G_j=0,\qquad B_{s_+}F_j\!\cdot G_{j+1}=0,\qquad
B_s=D_x^2+D_t+2sD_x,\quad s_\pm=a\pm h/2.$$

展开空间项

$$\mathcal L_s(F,G)=F_{xx}G-2F_xG_x+FG_{xx}+2s(F_xG-FG_x),$$

两条方程分别成为 $F_{j,t}G_j-F_jG_{j,t}+\mathcal L_{s_-}(F_j,G_j)=0$ 与 $F_{j,t}G_{j+1}-F_jG_{j+1,t}+\mathcal L_{s_+}(F_j,G_{j+1})=0$，于是

$$F_{j,t}=\frac{F_jG_{j,t}-\mathcal L_{s_-}(F_j,G_j)}{G_j},\qquad
G_{j+1,t}=\frac{G_{j+1}F_{j,t}+\mathcal L_{s_+}(F_j,G_{j+1})}{F_j}.$$

**时间递推。** 用隐式中点离散，记 $\bar F=(F^{n+1}+F^n)/2$、$\delta_tF=(F^{n+1}-F^n)/\Delta t$。时间项满足

$$\delta_tF\,\bar G-\bar F\,\delta_tG=\frac{F^{n+1}G^n-F^nG^{n+1}}{\Delta t}.$$

把 $\mathcal L_s$ 中的 $\partial_x,\partial_x^2$ 换成 $D_1,D_2$，记所得算子为 $\mathcal L_s^h$，直接得到

$$\begin{aligned}
G_j^nF_j^{n+1}+\frac{\Delta t}{2}\mathcal L_{s_-}^h(F_j^{n+1},\bar G_j)
&=F_j^nG_j^{n+1}-\frac{\Delta t}{2}\mathcal L_{s_-}^h(F_j^n,\bar G_j),\\
F_j^nG_{j+1}^{n+1}-\frac{\Delta t}{2}\mathcal L_{s_+}^h(\bar F_j,G_{j+1}^{n+1})
&=F_j^{n+1}G_{j+1}^n+\frac{\Delta t}{2}\mathcal L_{s_+}^h(\bar F_j,G_{j+1}^n).
\end{aligned}$$

已知各层 $F^n,G^n$ 及最低层 $G_{j_L}^{n+1}$，先由第一式线性求解 $F_{j_L}^{n+1}$，再由第二式求解 $G_{j_L+1}^{n+1}$，依次向上推进：

$$G_{j_L}^{n+1}\longrightarrow F_{j_L}^{n+1}\longrightarrow G_{j_L+1}^{n+1}
\longrightarrow F_{j_L+1}^{n+1}\longrightarrow\cdots.$$

内部场值由 $\alpha=\log F$、$\beta=\log G$ 恢复：

$$u_j=D_1(2\alpha_j-\beta_j-\beta_{j+1}),\qquad
v_j=\frac4hD_1(\beta_{j+1}-\beta_j)+\delta_0u_j.$$

参数：$a=2$、$s_-=1.9375$、$s_+=2.0625$、$h=0.125$、$\Delta x=0.15625$、$\Delta t=0.000125$、$T=0.01$。初值由共同的 $u_*,v_*$ 求解上述恢复关系；最低层 $G$ 及两端边界取解析势函数值。

**对应代码。** `solve_one` 求解一层的线性方程，`advance` 依次更新 $F_j,G_{j+1}$；代码以新旧 $\tau$ 的比值求解。''',
    'mesh-text': r'''### 2.4　网格策略

固定网格取 $s=0$、$V=0$。动网格初始节点按 $\bar\rho$ 的累积积分等分，之后使用

$$\begin{aligned}
x_i&=\xi_i+s_i,\qquad J_i=1+D_\xi s_i,\qquad D_1=J^{-1}D_\xi,\\
D_2f&=J^{-2}D_{\xi\xi}f-J^{-3}(D_\xi J)(D_\xi f),\\
\rho_j&=1-(v_j-\delta_0u_j)/4,\qquad \bar\rho=\frac1{24}\sum_j\rho_j,\\
\bar q&=\frac1{24}\sum_j[(u_j+2a)\rho_j-D_1\rho_j-2a],\qquad
V_i=\frac{\bar q_i-\bar q_0}{\bar\rho_i},\qquad \dot x_i=V_i.
\end{aligned}$$

$D_\xi$、$D_{\xi\xi}$ 分别采用上述三点一阶、二阶差分，格距为 $\Delta\xi=0.15625$。SD 在中点网格上将 $s_\pm$ 换成 $s_\pm-V/2$，并用 $x^{n+1}=x^n+\Delta t(V^n+V^{n+1})/2$ 更新节点。SD2、FD 对场值加入 $VD_1z$，场与节点同步使用 Euler 或 RK4 更新。''',
}

CELLS_UPDATE['time'] = r'''def step(fun, t, state, dt, method):
    if method == 'Euler':
        return state+dt*fun(t, state)
    k1 = fun(t, state)
    k2 = fun(t+dt/2, state+dt*k1/2)
    k3 = fun(t+dt/2, state+dt*k2/2)
    k4 = fun(t+dt, state+dt*k3)
    return state+dt*(k1+2*k2+2*k3+k4)/6

PRIMARY = dict(SD='Midpoint', SD2='RK4', FD='RK4')

def solve(case, model, method, mesh, config=CONFIG):
    p = Problem(case, model, mesh, config)
    state = p.initial()
    initial = p.fields(state, 0.)
    initial_ref = p.m.G.uv(p.m.js, p.X.x, 0.)
    mask = abs(p.X.x) <= config['eval_half']
    initial_error = max(float(abs(u[:, mask]-v[:, mask]).max())
                        for u, v in zip(initial, initial_ref))
    nsteps = round(config['T']/config['dt'])
    if not np.isclose(nsteps*config['dt'], config['T'], rtol=0, atol=1e-13):
        raise ValueError('T 必须是 dt 的整数倍')
    reached, reason = 0., ''
    for n in range(nsteps):
        try:
            with np.errstate(over='raise', invalid='raise', divide='raise'):
                candidate = (p.m.step(n*config['dt'], state, config['dt'], mesh)
                             if model == 'SD' else
                             step(p.stage, n*config['dt'], state, config['dt'], method))
                if not np.all(np.isfinite(candidate)) or abs(candidate).max() > 1000:
                    raise ValueError('状态非有限或绝对值超过 1000')
                p.X.set_s(candidate[-p.X.n:])
        except (ValueError, FloatingPointError, OverflowError, RuntimeError) as e:
            reason = str(e)
            break
        state, reached = candidate, (n+1)*config['dt']
    xx = np.linspace(-config['eval_half'], config['eval_half'], config['eval_points'])
    native = p.fields(state, reached)
    sampled = [CubicSpline(p.X.x, f, axis=-1)(xx) for f in native]
    exact = p.m.G.uv(p.m.js, xx, reached)
    errors = {f: abs(u-v) for f, u, v in zip(('u', 'v'), sampled, exact)}
    return dict(case=case, model=model, method=method, mesh=mesh,
        reached=reached, completed=not reason and np.isclose(reached, config['T']), reason=reason,
        initial_error=initial_error, x=xx, y=p.m.y, fields=sampled, exact=exact,
        errors=errors, max_errors={f: float(e.max()) for f, e in errors.items()},
        min_J=float(p.X.J.min()), native_x=p.X.x.copy(), native_fields=native)

results = {}
def calculate(method, mesh, models=MODELS):
    for case in CASES:
        for model in models:
            actual = PRIMARY[model] if method == 'primary' else method
            key = case, model, actual, mesh
            if key not in results:
                results[key] = solve(case, model, actual, mesh)
            if not results[key]['completed']:
                raise RuntimeError(str(key)+': '+results[key]['reason'])

def error_table(mesh):
    return pd.DataFrame([{'算例': case, '场': field,
        **{m: results[case, m, PRIMARY[m], mesh]['max_errors'][field] for m in MODELS}}
        for case in CASES for field in ('u', 'v')]).set_index(['算例', '场'])
'''
CELLS_UPDATE['space_experiment'] = r'''calculate('primary', 'fixed')
space_table = error_table('fixed')
space_table.style.format('{:.3e}').highlight_min(axis=1, props='font-weight: bold')
'''
CELLS_UPDATE['time_experiment'] = r'''calculate('Euler', 'fixed', ('SD2', 'FD'))
time_table = pd.DataFrame([{'算例': case, '方案': model, '场': field,
    **{method: results[case, model, method, 'fixed']['max_errors'][field]
       for method in ('Euler', 'RK4')}}
    for case in CASES for model in ('SD2', 'FD') for field in ('u', 'v')]).set_index(['算例', '方案', '场'])
time_table.style.format('{:.3e}').highlight_min(axis=1, props='font-weight: bold')
'''
CELLS_UPDATE['order'] = r'''order_rows = []
for case in CASES:
    for model, method in (('SD', 'Midpoint'), ('SD2', 'Euler')):
        fields = [results[case, model, method, 'fixed']['fields']]
        for divisor in (2, 4):
            refined = solve(case, model, method, 'fixed',
                            dict(CONFIG, dt=CONFIG['dt']/divisor))
            if not refined['completed']:
                raise RuntimeError(refined['reason'])
            fields.append(refined['fields'])
        for i, field in enumerate(('u', 'v')):
            d1 = np.max(abs(fields[0][i]-fields[1][i]))
            d2 = np.max(abs(fields[1][i]-fields[2][i]))
            order_rows.append({'算例': case, '方案': model, '时间算法': method, '场': field,
                              'dt 与 dt/2 场差': d1, 'dt/2 与 dt/4 场差': d2,
                              '观测阶': np.log2(d1/d2)})
pd.DataFrame(order_rows).set_index(['算例', '方案', '时间算法', '场']).style.format({
    'dt 与 dt/2 场差': '{:.3e}', 'dt/2 与 dt/4 场差': '{:.3e}', '观测阶': '{:.4f}'})
'''
CELLS_UPDATE['mesh_experiment'] = r'''calculate('primary', 'moving')
mesh_table = pd.DataFrame([{'算例': case, '方案': model, '场': field,
    **{mesh: results[case, model, PRIMARY[model], mesh]['max_errors'][field]
       for mesh in ('fixed', 'moving')}}
    for case in CASES for model in MODELS for field in ('u', 'v')]).set_index(['算例', '方案', '场'])
mesh_table.style.format('{:.3e}').highlight_min(axis=1, props='font-weight: bold')
'''
CELLS_UPDATE['curves'] = r'''for case in CASES:
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7), layout='constrained')
    for i, field in enumerate(('u', 'v')):
        upper = max(results[case, model, PRIMARY[model], mesh]['errors'][field][:,
            (results[case, model, PRIMARY[model], mesh]['x'] >= -1) &
            (results[case, model, PRIMARY[model], mesh]['x'] <= 1)].max()
            for model in MODELS for mesh in ('fixed', 'moving'))
        for j, mesh in enumerate(('fixed', 'moving')):
            ax = axes[i, j]
            for model, style in zip(MODELS, ('-', '--', ':')):
                r = results[case, model, PRIMARY[model], mesh]
                take = (r['x'] >= -1) & (r['x'] <= 1)
                curve = r['errors'][field].max(axis=0)
                ax.plot(r['x'][take], curve[take], color=COLORS[model], ls=style,
                        lw=1.3, label=model)
            ax.set(xlabel='$x$', ylabel=f'$e_{field}(x)$', xlim=(-1, 1),
                   ylim=(0, upper*1.06), title=f'{field}: {mesh}')
            ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
            ax.grid(alpha=.16, lw=.5)
            ax.legend(frameon=False)
    fig.suptitle(f'Case {case} | SD: midpoint; SD2/FD: RK4 | T={CONFIG["T"]:g}')
    plt.show()
'''
CELLS_UPDATE['summary'] = r'''for case in CASES:
    best_u = space_table.loc[(case, 'u')].idxmin()
    best_v = space_table.loc[(case, 'v')].idxmin()
    print(f'算例 {case}：固定网格下，u / v 的最小误差方案为 {best_u} / {best_v}。')
mesh_ratios = mesh_table['moving']/mesh_table['fixed']
ratio_table = mesh_ratios.unstack('场').rename(columns={'u': 'u 动格/固定', 'v': 'v 动格/固定'})
display(ratio_table.style.format('{:.3f}'))
sd_orders = [r['观测阶'] for r in order_rows if r['方案'] == 'SD']
print(f'SD 隐式中点的时间观测阶为 {min(sd_orders):.3f}–{max(sd_orders):.3f}。')
print(f'全部 {len(results)} 组主试验到达 T={CONFIG["T"]:g}；'
      f'评价区间内的初始物理场最大节点差为 {max(r["initial_error"] for r in results.values()):.3e}。')
'''
