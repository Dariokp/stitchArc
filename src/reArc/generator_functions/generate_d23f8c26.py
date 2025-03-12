def generate_d23f8c26(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)    
    h = unifint(diff_lb, diff_ub, (2, 30))
    wh = unifint(diff_lb, diff_ub, (1, 14))
    w = 2 * wh + 1
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    numn = unifint(diff_lb, diff_ub, (1, (h * w) // 2 - 1))
    numcols = unifint(diff_lb, diff_ub, (1, 9))
    remcols = sample(remcols, numcols)
    inds = totuple(asindices(gi))
    locs = sample(inds, numn)
    for ij in locs:
        col = choice(remcols)
        gi = fill(gi, col, {ij})
        a, b = ij
        if b == w // 2:
            go = fill(go, col, {ij})
    return {'input': gi, 'output': go}

