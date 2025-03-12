def generate_cce03e0d(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (2, 8))    
    h = unifint(diff_lb, diff_ub, (2, 5))
    w = unifint(diff_lb, diff_ub, (2, 5))
    nred = unifint(diff_lb, diff_ub, (1, h * w - 1))
    ncols = unifint(diff_lb, diff_ub, (1, min(8, nred)))
    ncells = unifint(diff_lb, diff_ub, (1, h * w - nred))
    ccols = sample(cols, ncols)
    gi = canvas(0, (h, w))
    inds = asindices(gi)
    reds = sample(totuple(inds), nred)
    reminds = difference(inds, reds)
    gi = fill(gi, 2, reds)
    rest = sample(totuple(reminds), ncells)
    rest = {(choice(ccols), ij) for ij in rest}
    gi = paint(gi, rest)
    go = canvas(0, (h**2, w**2))
    locs = apply(rbind(multiply, (h, w)), reds)
    res = mapply(lbind(shift, asobject(gi)), locs)
    go = paint(go, res)
    return {'input': gi, 'output': go}

