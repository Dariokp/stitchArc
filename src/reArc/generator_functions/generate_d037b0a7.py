def generate_d037b0a7(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    nlocs = unifint(diff_lb, diff_ub, (1, w))
    locs = sample(interval(0, w, 1), nlocs)
    for j in locs:
        col = choice(remcols)
        loci = randint(0, h - 1)
        loc = (loci, j)
        gi = fill(gi, col, {loc})
        go = fill(go, col, connect(loc, (h - 1, j)))
    return {'input': gi, 'output': go}

