def generate_2204b7a8(diff_lb: float, diff_ub: float) -> dict:
    dim_bounds = (4, 30)
    colopts = interval(0, 10, 1)
    while True:
        h = unifint(diff_lb, diff_ub, dim_bounds)
        w = unifint(diff_lb, diff_ub, dim_bounds)
        bgc = choice(colopts)
        remcols = remove(bgc, colopts)
        c = canvas(bgc, (h, w))
        inds = totuple(shift(asindices(canvas(0, (h, w - 2))), RIGHT))
        ccol = choice(remcols)
        remcols2 = remove(ccol, remcols)
        c1 = choice(remcols2)
        c2 = choice(remove(c1, remcols2))
        nc_bounds = (1, (h * (w - 2)) // 2 - 1)
        nc = unifint(diff_lb, diff_ub, nc_bounds)
        locs = sample(inds, nc)
        if w % 2 == 1:
            locs = difference(locs, vfrontier(tojvec(w // 2)))
        gi = fill(c, c1, vfrontier(ORIGIN))
        gi = fill(gi, c2, vfrontier(tojvec(w - 1)))
        gi = fill(gi, ccol, locs)
        a = sfilter(locs, lambda ij: last(ij) < w // 2)
        b = difference(locs, a)
        go = fill(gi, c1, a)
        go = fill(go, c2, b)
        if len(palette(gi)) == 4:
            break
    if choice((True, False)):
        gi = dmirror(gi)
        go = dmirror(go)
    return {'input': gi, 'output': go}

