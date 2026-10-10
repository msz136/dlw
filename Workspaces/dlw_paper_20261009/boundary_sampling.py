"""Complete the numerical boundary trace using the solver's continuation rules.

PE/FD physical fields use the same periodic continuation as their x stencils.
PF uses Q(x+L)=Q(x)+jump and R(x+L)=R(x)+rjump before reconstructing u,v.
No exact reference field is substituted for either numerical field.
"""
def completed_numerical_fields(problem, state, t):
    native = problem.fields(state, t)
    grid, model = problem.X, problem.m
    right_x = grid.x[0] + grid.L
    if problem.model == 'SD2':
        q, r = model.unpack(state[:-grid.n], t)
        q_right = q[:, :1] + model.jump
        r_right = r[:, :1] + model.rjump
        if np.any(q_right <= 0):
            raise ValueError('PF right boundary Q is nonpositive')
        # The additive jumps are independent of x, hence Q_x(x+L)=Q_x(x).
        qx_right = model.dx(q, model.jump)[:, :1]
        u_right = 2*qx_right/q_right
        ghosts = ghost_u(model.G, model.js, np.array([right_x]), t, u_right)
        v_right = 4*(1-q_right*r_right)+delta0(u_right, ghosts, model.h)
        right = (u_right, v_right)
    else:
        right = tuple(f[:, :1].copy() for f in native)
    extended_x = np.r_[grid.x, right_x]
    extended = tuple(np.concatenate((f, r), axis=-1) for f, r in zip(native, right))
    assert np.all(np.diff(extended_x) > 0)
    return extended_x, extended, native

def sample_numerical_fields(problem, state, t, points):
    extended_x, extended, native = completed_numerical_fields(problem, state, t)
    if points.min() < extended_x[0] or points.max() > extended_x[-1]:
        raise ValueError('Evaluation point lies outside the completed numerical grid')
    bc = 'not-a-knot' if problem.model == 'SD2' else 'periodic'
    sampled = tuple(CubicSpline(extended_x, f, axis=-1, bc_type=bc,
                                extrapolate=False)(points) for f in extended)
    if not all(np.isfinite(f).all() for f in sampled):
        raise ValueError('Numerical interpolation returned a nonfinite value')
    return sampled, extended_x, extended, native
