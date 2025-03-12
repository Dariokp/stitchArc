def generate_67385a82(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(0, remove(8, interval(0, 10, 1)))
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    col = choice(cols)
    gi = canvas(0, (h, w))
    inds = totuple(asindices(gi))
    ncd = unifint(diff_lb, diff_ub, (0, len(inds) // 2))
    nc = choice((ncd, len(inds) - ncd))
    nc = min(max(1, nc), len(inds) - 1)
    locs = sample(inds, nc)
    gi = fill(gi, col, locs)
    objs = objects(gi, T, F, F)
    rems = toindices(merge(sizefilter(colorfilter(objs, col), 1)))
    blues = difference(ofcolor(gi, col), rems)
    go = fill(gi, 8, blues)
    return {'input': gi, 'output': go}

