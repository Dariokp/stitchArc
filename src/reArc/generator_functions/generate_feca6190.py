def generate_feca6190(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    w = unifint(diff_lb, diff_ub, (2, 6))
    bgc = 0
    remcols = remove(bgc, cols)
    ncols = unifint(diff_lb, diff_ub, (1, min(w, 5)))
    ccols = sample(remcols, ncols)
    cands = interval(0, w, 1)
    locs = sample(cands, ncols)
    gi = canvas(bgc, (1, w))
    go = canvas(bgc, (w*ncols, w*ncols))
    for col, j in zip(ccols, locs):
        gi = fill(gi, col, {(0, j)})
        go = fill(go, col, shoot((w*ncols-1, j), UP_RIGHT))
    return {'input': gi, 'output': go}

