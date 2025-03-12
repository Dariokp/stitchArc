def generate_bda2d7a6(diff_lb: float, diff_ub: float) -> dict:
    colopts = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (2, 14))
    w = unifint(diff_lb, diff_ub, (2, 14))
    ncols = unifint(diff_lb, diff_ub, (2, 10))
    cols = sample(colopts, ncols)
    colord = [choice(cols) for j in range(min(h, w))]
    shp = (h*2, w*2)
    gi = canvas(0, shp)
    for idx, (ci, co) in enumerate(zip(colord, colord[-1:] + colord[:-1])):
        ulc = (idx, idx)
        lrc = (h*2 - 1 - idx, w*2 - 1 - idx)
        bx = box(frozenset({ulc, lrc}))
        gi = fill(gi, ci, bx)
    I = gi
    objso = order(objects(I, T, F, F), compose(maximum, shape))
    if color(objso[0]) == color(objso[-1]):
        objso = (combine(objso[0], objso[-1]),) + objso[1:-1]
    res = mpapply(recolor, apply(color, objso), (objso[-1],) + objso[:-1])
    go = paint(gi, res)
    return {'input': gi, 'output': go}

