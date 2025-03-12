def generate_3ac3eb23(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    nlocs = unifint(diff_lb, diff_ub, (1, max(1, (w - 2) // 3)))
    locopts = interval(1, w - 1, 1)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    for k in range(nlocs):
        if len(locopts) == 0:
            break
        locj = choice(locopts)
        locopts = difference(locopts, interval(locj - 2, locj + 3, 1))
        col = choice(remcols)
        gi = fill(gi, col, {(0, locj)})
        go = fill(go, col, {(p, locj) for p in interval(0, h, 2)})
        go = fill(go, col, {(p, locj - 1) for p in interval(1, h, 2)})
        go = fill(go, col, {(p, locj + 1) for p in interval(1, h, 2)})
    mf = choice((identity, rot90, rot180, rot270))
    gi = mf(gi)
    go = mf(go)
    return {'input': gi, 'output': go}

