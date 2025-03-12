def generate_97999447(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(5, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    opts = interval(0, h, 1)
    num = unifint(diff_lb, diff_ub, (1, h))
    locs = sample(opts, num)
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    numc = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(remcols, numc)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    for idx in locs:
        col = choice(ccols)
        j = randint(0, w - 1)
        dot = (idx, j)
        gi = fill(gi, col, {dot})
        go = fill(go, col, {(idx, x) for x in range(j, w, 2)})
        go = fill(go, 5, {(idx, x) for x in range(j+1, w, 2)})
    return {'input': gi, 'output': go}

