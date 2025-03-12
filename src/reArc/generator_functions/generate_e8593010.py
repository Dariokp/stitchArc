def generate_e8593010(diff_lb: float, diff_ub: float) -> dict:
    a = frozenset({frozenset({ORIGIN})})
    b = frozenset({frozenset({ORIGIN, RIGHT}), frozenset({ORIGIN, DOWN})})
    c = frozenset({
    frozenset({ORIGIN, DOWN, UNITY}),
    frozenset({ORIGIN, DOWN, RIGHT}),
    frozenset({UNITY, DOWN, RIGHT}),
    frozenset({UNITY, ORIGIN, RIGHT}),
    shift(frozenset({ORIGIN, UP, DOWN}), DOWN),
    shift(frozenset({ORIGIN, LEFT, RIGHT}), RIGHT)
    })
    a, b, c = totuple(a), totuple(b), totuple(c)
    prs = [(a, 3), (b, 2), (c, 1)]
    cols = difference(interval(0, 10, 1), (1, 2, 3))
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    fgc = choice(remcols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    reminds = asindices(gi)
    nobjs = unifint(diff_lb, diff_ub, (1, ((h * w) // 2) // 2))
    maxtr = 10
    for k in range(nobjs):
        ntr = 0
        objs, col = choice(prs)
        obj = choice(objs)
        while ntr < maxtr:
            if len(reminds) == 0:
                break
            loc = choice(totuple(reminds))
            olcd = shift(obj, loc)
            if olcd.issubset(reminds):
                gi = fill(gi, fgc, olcd)
                go = fill(go, col, olcd)
                reminds = (reminds - olcd) - mapply(dneighbors, olcd)
                break
            ntr += 1
    return {'input': gi, 'output': go}

