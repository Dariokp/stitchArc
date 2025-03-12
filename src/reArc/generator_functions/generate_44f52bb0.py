def generate_44f52bb0(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)    
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    ncols = unifint(diff_lb, diff_ub, (2, 9))
    ccols = sample(remcols, ncols)
    gi = canvas(bgc, (h, w))
    numcells = unifint(diff_lb, diff_ub, (1, h * w - 1))
    inds = asindices(gi)
    while gi == hmirror(gi):
        cells = sample(totuple(inds), numcells)
        gi = canvas(bgc, (h, w))
        for ij in cells:
            a, b = ij
            col = choice(ccols)
            gi = fill(gi, col, {ij})
            gi = fill(gi, col, {(a, w - 1 - b)})
    issymm = choice((True, False))
    if not issymm:
        numpert = unifint(diff_lb, diff_ub, (1, h * (w // 2)))
        cands = asindices(canvas(-1, (h, w // 2)))
        locs = sample(totuple(cands), numpert)
        for a, b in locs:
            col = gi[a][b]
            newcol = choice(totuple(remove(col, insert(bgc, set(ccols)))))
            gi = fill(gi, newcol, {(a, b)})
        go = canvas(7, (1, 1))
    else:
        go = canvas(1, (1, 1))
    mfs = (identity, dmirror, cmirror, vmirror, hmirror, rot90, rot180, rot270)
    nmfs = choice((1, 2))
    for fn in sample(mfs, nmfs):
        gi = fn(gi)
        go = fn(go)
    return {'input': gi, 'output': go}

