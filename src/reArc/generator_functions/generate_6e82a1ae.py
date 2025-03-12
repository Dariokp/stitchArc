def generate_6e82a1ae(diff_lb: float, diff_ub: float) -> dict:
    b = frozenset({frozenset({ORIGIN, RIGHT}), frozenset({ORIGIN, DOWN})})
    c = frozenset({
    frozenset({ORIGIN, DOWN, UNITY}),
    frozenset({ORIGIN, DOWN, RIGHT}),
    frozenset({UNITY, DOWN, RIGHT}),
    frozenset({UNITY, ORIGIN, RIGHT}),
    shift(frozenset({ORIGIN, UP, DOWN}), DOWN),
    shift(frozenset({ORIGIN, LEFT, RIGHT}), RIGHT)
    })
    d = set()
    for k in range(100):
        shp = {(0, 0)}
        for jj in range(3):
            shp.add(choice(totuple(mapply(dneighbors, shp) - shp)))
        shp = frozenset(normalize(shp))
        d.add(shp)
    d = frozenset(d)
    d, b, c = totuple(d), totuple(b), totuple(c)
    prs = [(b, 3), (c, 2), (d, 1)]
    cols = difference(interval(0, 10, 1), (1, 2, 3))
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    fgc = choice(remcols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    reminds = asindices(gi)
    nobjs = unifint(diff_lb, diff_ub, (1, ((h * w) // 2) // 3))
    maxtr = 10
    for k in range(nobjs):
        ntr = 0
        objs, col = choice(prs)
        obj = choice(objs)
        while ntr < maxtr:
            loc = choice(totuple(reminds))
            olcd = shift(obj, loc)
            if olcd.issubset(reminds):
                gi = fill(gi, fgc, olcd)
                go = fill(go, col, olcd)
                reminds = (reminds - olcd) - mapply(dneighbors, olcd)
                break
            ntr += 1
    return {'input': gi, 'output': go}

