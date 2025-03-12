def generate_bdad9b1f(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(4, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (4, 30))
    numh = unifint(diff_lb, diff_ub, (1, h // 2 - 1))
    numw = unifint(diff_lb, diff_ub, (1, w // 2 - 1))
    hlocs = sample(interval(2, h - 1, 1), numh)
    wlocs = sample(interval(2, w - 1, 1), numw)
    numcols = unifint(diff_lb, diff_ub, (2, 8))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    ccols = sample(remcols, numcols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    fc = -1
    for ii in sorted(hlocs):
        col = choice(remove(fc, ccols))
        fc = col
        objw = randint(2, ii)
        gi = fill(gi, col, connect((ii, 0), (ii, objw - 1)))
        go = fill(go, col, connect((ii, 0), (ii, w - 1)))
    fc = -1
    for jj in sorted(wlocs):
        col = choice(remove(fc, ccols))
        fc = col
        objh = randint(2, jj)
        gi = fill(gi, col, connect((0, jj), (objh - 1, jj)))
        go = fill(go, col, connect((0, jj), (h - 1, jj)))
    yells = product(set(hlocs), set(wlocs))
    go = fill(go, 4, yells)
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

