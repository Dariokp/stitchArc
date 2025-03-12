def generate_ce22a75a(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(1, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    fgc = choice(remcols)
    c = canvas(bgc, (h, w))
    ndots = unifint(diff_lb, diff_ub, (1, (h * w) // 3))
    dots = sample(totuple(asindices(c)), ndots)
    gi = fill(c, fgc, dots)
    go = fill(c, 1, mapply(neighbors, dots))
    go = fill(go, 1, dots)
    return {'input': gi, 'output': go}

