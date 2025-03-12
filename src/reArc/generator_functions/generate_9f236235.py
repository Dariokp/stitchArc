def generate_9f236235(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    numh = unifint(diff_lb, diff_ub, (2, 14))
    numw = unifint(diff_lb, diff_ub, (2, 14))
    h = unifint(diff_lb, diff_ub, (1, 31 // numh - 1))
    w = unifint(diff_lb, diff_ub, (1, 31 // numw - 1))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    frontcol = choice(remcols)
    remcols = remove(frontcol, cols)
    numcols = unifint(diff_lb, diff_ub, (1, min(9, numh * numw)))
    ccols = sample(remcols, numcols)
    numcells = unifint(diff_lb, diff_ub, (1, numh * numw))
    cands = asindices(canvas(-1, (numh, numw)))
    inds = asindices(canvas(-1, (h, w)))
    locs = sample(totuple(cands), numcells)
    gi = canvas(frontcol, (h * numh + numh - 1, w * numw + numw - 1))
    go = canvas(bgc, (numh, numw))
    for cand in cands:
        a, b = cand
        plcd = shift(inds, (a * (h + 1), b * (w + 1)))
        col = choice(remcols) if cand in locs else bgc
        gi = fill(gi, col, plcd)
        go = fill(go, col, {cand})
    go = vmirror(go)
    return {'input': gi, 'output': go}

