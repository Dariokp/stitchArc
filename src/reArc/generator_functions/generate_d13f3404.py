def generate_d13f3404(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (3, 15))
    w = unifint(diff_lb, diff_ub, (3, 15))
    vopts = {(ii, 0) for ii in interval(0, h, 1)}
    hopts = {(0, jj) for jj in interval(1, w, 1)}
    opts = tuple(vopts | hopts)
    num = unifint(diff_lb, diff_ub, (1, len(opts)))
    locs = sample(opts, num)
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h*2, w*2))
    inds = asindices(gi)
    for loc in locs:
        ln = tuple(shoot(loc, (1, 1)) & inds)
        locc = choice(ln)
        col = choice(remcols)
        gi = fill(gi, col, {locc})
        go = fill(go, col, shoot(locc, (1, 1)))
    return {'input': gi, 'output': go}

